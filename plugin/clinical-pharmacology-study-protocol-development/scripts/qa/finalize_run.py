#!/usr/bin/env python3
"""Fail-closed release gate for generated protocol / ICF drafts.

Design: docs/p0_release_gate_design_ko.md

The checkers (doc_lint, citation_verify, dose_safety_guard) report facts only;
this module owns the severity policy — which finding blocks a release, per
profile. The engines are located by a path relative to this file so the module
works both in the development tree and in the synced plugin copy.

Usage:
    finalize_run.py <target> [--profile draft|submission]
                             [--workspace _workspace]
                             [--goal-spec PATH] [--mrsd-json PATH]

Exit codes:
    0  release gate passed
    1  judged and rejected  -> fix the document
    2  undecidable          -> fix the gate or its inputs
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import doc_lint  # noqa: E402
import citation_verify  # noqa: E402
import dose_safety_guard  # noqa: E402

# Status vocabulary. "checker not run" is never conflated with "passed".
PASS = "PASS"
FAIL = "FAIL"
SKIPPED = "SKIPPED"
FORMAT_ONLY = "FORMAT_ONLY"
NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
ERROR = "ERROR"

PROFILES = ("draft", "submission")

EXIT_OK = 0
EXIT_REJECTED = 1
EXIT_UNDECIDABLE = 2


def _dim(dim_id, status, findings=None, **extra):
    """Build one dimension result."""
    out = {"id": dim_id, "status": status, "findings": list(findings or [])}
    out.update(extra)
    return out


# trial_type은 스키마상 자유 서술 문자열이므로 부분 일치가 필요하지만,
# 단어 경계 없이 매칭하면 다른 단어 속 SAD/MAD를 오탐한다.
_FIH_RE = re.compile(r"\b(FIH|SAD|MAD)\b", re.IGNORECASE)

# 스키마가 문서화한 비-FIH 유형 어휘(FIH/SAD/MAD/DDI/BE/FE/QTc/ADME 등). 스키마가
# type: string 자유 서술이므로 닫힌 enum이 아니라 '인식 가능한 토큰' 매칭으로 다룬다.
_NON_FIH_RE = re.compile(r"\b(DDI|BA|FE|ADME|QTc)\b", re.IGNORECASE)
# BE만 대소문자를 구분한다 — IGNORECASE로 두면 "to be determined" 같은 미정 문자열의
# 영어 단어 "be"가 생물학적 동등성 시험으로 인식되어 fail-open 경로가 된다.
_NON_FIH_CASED_RE = re.compile(r"\bBE\b")


def _is_fih(goal_spec):
    """FIH 계열 여부. 판별할 수 없으면 None('알 수 없음')을 돌려준다.

    None을 돌려주는 경우: goal_spec 자체가 없음, trial_type 키 없음, 문자열이 아님,
    공백뿐, 그리고 FIH 어휘·비-FIH 어휘 어느 쪽과도 매칭되지 않는 자유 서술
    (예: "최초 인체 투여 시험" — 영문 키워드 없음).

    '읽을 수 없음'을 False(비-FIH)로 접으면 확정된 DDI/BE 시험과 구분되지 않아
    dim_dose가 SKIPPED가 되고 FIH 용량 위반이 submission을 통과한다(fail-open).
    설계 §6.1의 "시험유형 확인 불가 시 제출 판정 불가" 원칙을 goal_spec 부재가
    아니라 trial_type 판별 가능 여부에 적용한다.
    """
    if not isinstance(goal_spec, dict):
        return None
    trial_type = goal_spec.get("trial_type")
    if not isinstance(trial_type, str) or not trial_type.strip():
        return None
    if _FIH_RE.search(trial_type):
        return True
    if _NON_FIH_RE.search(trial_type) or _NON_FIH_CASED_RE.search(trial_type):
        return False
    return None


def dim_structure(target, profile, ctx):
    """doc_lint ERROR — 구조·법정 보존기간 등 하드 결함. 프로파일 무관."""
    doc_type, errors, _warnings = doc_lint.lint_file(target)
    status = FAIL if errors else PASS
    return _dim("structure", status, errors, doc_type=doc_type)


def dim_advisory(target, profile, ctx):
    """doc_lint WARNING 전체. draft는 표시만, submission은 0건이어야 한다.

    warning을 분류하지 않는 것이 의도다 (설계 D5): 제출 직전에 미해결 권고가
    남아 있으면 종류를 따지지 않고 차단한다. placeholder·미확인 인용·PIPA
    누락·PG 선택동의 누락·CI 경계 표기 누락이 이 한 규칙으로 모두 커버된다.
    """
    _doc_type, _errors, warnings = doc_lint.lint_file(target)
    if not warnings:
        return _dim("advisory", PASS)
    if profile == "submission":
        return _dim("advisory", FAIL, warnings)
    return _dim("advisory", PASS, warnings,
                reason="draft — 권고 사항 표시만 (submission에서는 차단)")


_SUMMARY_KEYS = ("total", "format_fail", "not_found", "unverified_network")

# citation_verify.verify_online이 실제 레지스트리에 조회하는 유형은 pmid·nct뿐이다.
# 아래 유형은 추출·형식 검증만 되고 online 검증 대상이 아니므로, 이들만 있는 문서에서
# not_found=0은 '조회해서 다 있었다'가 아니라 '아무것도 조회하지 않았다'를 뜻한다.
_ONLINE_UNVERIFIABLE_TYPES = ("dailymed_setid", "url")


def _count_online_unverifiable(audit):
    """online 검증 대상이 아닌 인용 유형의 건수를 유형별로 센다."""
    return {
        kind: sum(f["counts"].get(kind, 0) for f in audit["files"])
        for kind in _ONLINE_UNVERIFIABLE_TYPES
    }


def dim_citation(target, profile, ctx):
    """인용 검증. draft는 형식만(FORMAT_ONLY), submission은 online 필수.

    offline에서는 not_found가 구조적으로 항상 0이므로 '통과'라고 부르지 않고
    FORMAT_ONLY로 표기한다. submission 프로파일에서 FORMAT_ONLY는 차단이다
    (_BLOCKING 참조).

    submission에서도 dailymed_setid·url은 verify_online이 조회하지 않는다. 이들만
    근거로 가진 문서를 PASS로 부르면 offline과 똑같은 '구조적 0을 통과로 세는' 오류가
    되므로, 해당 인용이 하나라도 있으면 FORMAT_ONLY로 표기한다. 심각도 자체는
    _BLOCKING이 소유하며 이 함수는 사실만 보고한다.
    """
    online = (profile == "submission")
    audit = citation_verify.audit_files(
        [target], workspace=ctx["workspace"], online=online)
    s = audit["summary"]
    detail = {k: s[k] for k in _SUMMARY_KEYS}

    findings = []
    if s["format_fail"]:
        findings.append(f"format_fail={s['format_fail']} — 잘못된 형식의 인용 id")

    if not online:
        return _dim("citation", FORMAT_ONLY, findings, detail=detail,
                    reason="offline — id 실제 존재 여부 미검증")

    unverifiable = _count_online_unverifiable(audit)
    n_unverifiable = sum(unverifiable.values())
    detail["online_unverifiable"] = n_unverifiable

    if s["not_found"]:
        findings.append(f"not_found={s['not_found']} — 레지스트리에 없는 인용 id")
    if s["unverified_network"]:
        findings.append(
            f"unverified_network={s['unverified_network']} — 네트워크 검증 불가")

    # 형식 오류·미존재·네트워크 실패는 확정된 불합격이므로 FORMAT_ONLY보다 우선한다.
    if findings:
        return _dim("citation", FAIL, findings, detail=detail)

    if n_unverifiable:
        kinds = ", ".join(f"{k}={v}" for k, v in unverifiable.items() if v)
        findings.append(
            f"online_unverifiable={n_unverifiable} ({kinds}) — "
            "online 조회 대상이 아닌 인용 유형이며 형식만 확인되었다")
        return _dim("citation", FORMAT_ONLY, findings, detail=detail,
                    reason="online 검증 불가 인용 유형 존재 — 통과로 세지 않는다")

    return _dim("citation", PASS, findings, detail=detail)


def dim_dose(target, profile, ctx):
    """FIH 시작 용량 대 MRSD. 시험유형·MRSD를 모르면 submission에서 판정 불가로 차단."""
    fih = _is_fih(ctx["goal_spec"])
    mrsd_path = ctx["mrsd_json"]
    # 파일 존재가 아니라 MRSD '값'을 얻었는지로 판단한다. 파일이 있다는 이유만으로
    # check_file에 위임하면, 손상·키 누락 파일에서 mrsd_mg=None -> status="skipped"가
    # 되어 FIH 용량 위반이 submission을 통과한다(fail-open).
    mrsd_mg = dose_safety_guard.mrsd_from_json(mrsd_path)
    has_mrsd = mrsd_mg is not None

    if fih is None:
        why = "goal_spec 없음 또는 trial_type을 판별할 수 없음"
        if profile == "submission":
            return _dim("dose", FAIL,
                        [f"{why} — 시험유형 확인 불가로 제출 판정 불가"])
        return _dim("dose", SKIPPED, reason=f"{why} (draft 허용)")

    if fih and not has_mrsd:
        # 부재와 '읽었으나 값 없음'을 같은 분기로 처리하되 사유는 구분해 남긴다.
        why = ("mrsd.json에서 MRSD 값을 얻지 못함(손상·키 누락)"
               if mrsd_path and os.path.isfile(mrsd_path)
               else "mrsd.json 없음")
        if profile == "submission":
            return _dim("dose", FAIL,
                        [f"FIH 계열이나 {why} — MRSD 대조 불가"])
        return _dim("dose", SKIPPED,
                    reason=f"FIH이나 {why} (draft 허용)")

    res = dose_safety_guard.check_file(target, mrsd_mg=mrsd_mg)
    if res["status"] == "violation":
        return _dim("dose", FAIL, [v["message"] for v in res["violations"]],
                    mrsd_mg=res["mrsd_mg"])
    if res["status"] == "skipped":
        return _dim("dose", SKIPPED, reason="MRSD 없음 — 대조 대상 없음")
    return _dim("dose", PASS, mrsd_mg=res["mrsd_mg"])


def dim_approval(target, profile, ctx):
    """사람 승인 이벤트. 서명 이벤트 스토어(P0-5)가 없어 아직 판정할 수 없다.

    이 차원을 조용히 빼는 대신 NOT_IMPLEMENTED로 매 실행 출력에 노출시킨다.
    이 게이트가 고치려는 문제 자체가 '검사가 있는 척'이었으므로, 같은 종류의
    공백을 새로 만들지 않는다.
    """
    return _dim("approval", NOT_IMPLEMENTED,
                reason="서명 이벤트 스토어 미구현 (P0-5)")


DIMENSIONS = (
    ("structure", dim_structure),
    ("citation", dim_citation),
    ("dose", dim_dose),
    ("advisory", dim_advisory),
    ("approval", dim_approval),
)

# 프로파일별 차단 상태 집합. SKIPPED/NOT_IMPLEMENTED는 어느 쪽도 차단하지 않는다.
_BLOCKING = {
    "draft": {FAIL, ERROR},
    "submission": {FAIL, ERROR, FORMAT_ONLY},
}

# 여섯 단어 어휘 전체. 집계는 '차단 집합에 속하는가'로 판단하므로, 어휘 밖 상태
# (오타나 새 차원 작성자의 "OK"/"WARN")는 그대로 두면 조용히 통과로 집계된다.
_KNOWN_STATUSES = frozenset(
    {PASS, FAIL, SKIPPED, FORMAT_ONLY, NOT_IMPLEMENTED, ERROR})


def _utc_now():
    """UTC ISO-8601. 형식은 citation_verify._utc_now()와 동일해야 한다 —
    두 산출물이 같은 _workspace/verification/ 디렉토리에서 같은 generated_utc
    필드명을 쓰므로 형식이 갈리면 안 된다 (citation_verify.py:59-60 참조).
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def run_gate(target, profile, workspace, goal_spec_path=None, mrsd_json=None):
    """모든 차원을 실행하고 집계한다. 예외를 밖으로 내보내지 않는다."""
    ctx = {
        "target": target,
        "profile": profile,
        "workspace": workspace,
        "goal_spec": doc_lint.load_goal_spec(goal_spec_path),
        "mrsd_json": mrsd_json,
    }

    dims = []
    for dim_id, fn in DIMENSIONS:
        try:
            dims.append(fn(target, profile, ctx))
        except Exception as exc:  # noqa: BLE001 — 크래시는 통과가 아니다
            dims.append(_dim(dim_id, ERROR,
                             [f"{type(exc).__name__}: {exc}"]))

    # 어휘 밖 상태는 ERROR로 강등한다 — 모르는 상태는 통과가 아니다.
    for d in dims:
        status = d.get("status")
        if not isinstance(status, str) or status not in _KNOWN_STATUSES:
            d.setdefault("findings", []).append(
                f"알 수 없는 상태 {status!r} — 상태 어휘 밖이므로 ERROR로 강등한다")
            d["status"] = ERROR

    blocking = _BLOCKING[profile]
    has_error = any(d["status"] == ERROR for d in dims)
    blocked = [d["id"] for d in dims if d["status"] in blocking]

    if has_error:
        result, exit_code = "UNDECIDABLE", EXIT_UNDECIDABLE
    elif blocked:
        result, exit_code = "FAIL", EXIT_REJECTED
    else:
        result, exit_code = "PASS", EXIT_OK

    doc_type = next((d.get("doc_type") for d in dims if d.get("doc_type")),
                    None)

    # score는 참고 수치이며 판정에 사용하지 않는다 (설계 D2). 계산이 실패해도
    # 차단하지 않고 None으로 둔다.
    try:
        score = doc_lint.score_file(target, goal_spec=ctx["goal_spec"])["score"]
    except Exception:  # noqa: BLE001 — 참고 수치이므로 실패를 삼킨다
        score = None

    gate_warnings = []
    not_implemented = [d["id"] for d in dims if d["status"] == NOT_IMPLEMENTED]
    if not_implemented:
        gate_warnings.append(
            f"미구현 차원이 있습니다 ({', '.join(not_implemented)}) — "
            "이 결과는 '제출 가능'을 의미하지 않습니다")

    return {
        "schema": "release_gate/v1",
        "generated_utc": _utc_now(),
        "target": target,
        "doc_type": doc_type,
        "profile": profile,
        "result": result,
        "exit_code": exit_code,
        "blocked_dimensions": blocked,
        "dimensions": dims,
        "score_informational": score,
        "warnings": gate_warnings,
    }


def _write_report(report, workspace):
    """리포트를 <workspace>/verification/release_gate.json에 원자적으로 기록한다.

    실패 시 예외를 전파한다 — 증거를 남기지 못하면 통과를 주장하지 않는다.
    임시 파일에 먼저 쓰고 os.replace로 교체하므로, 직렬화가 중간에 실패해도
    기존 리포트가 잘린 조각으로 덮이지 않는다.
    """
    out = os.path.join(workspace, "verification", "release_gate.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp, out)
    except Exception:  # noqa: BLE001 — 실패해도 잔여 임시 파일을 남기지 않는다
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise
    return out


def _undecidable_report(target, profile, workspace, reason):
    """판정에 이르지 못하고 조기 종료할 때 남길 최소 리포트.

    이전 실행의 PASS 리포트가 그대로 남으면 소비자(예: /finalize)가 이미 무효가 된
    판정을 읽는다. 종료코드와 리포트가 서로 다른 이야기를 하지 않게 한다.
    """
    return {
        "schema": "release_gate/v1",
        "generated_utc": _utc_now(),
        "target": target,
        "doc_type": None,
        "profile": profile,
        "result": "UNDECIDABLE",
        "exit_code": EXIT_UNDECIDABLE,
        "blocked_dimensions": [],
        "dimensions": [],
        "score_informational": None,
        "reason": reason,
        "warnings": [reason],
    }


def _harden_stream(stream):
    """인코딩 실패로 예외가 나가지 않도록 출력 스트림을 완화한다.

    ASCII 로케일에서 한국어 findings나 ⛔/⚠️를 출력하면 UnicodeEncodeError가 main을
    빠져나가고, 셸은 실제 판정(2) 대신 파이썬 기본 종료코드(1)를 본다 — '게이트가
    고장났다'가 '문서가 불량하다'로 보고되는 것이다. reconfigure가 없는 스트림
    (일부 테스트 대역·리다이렉트)도 있으므로 실패는 무시한다.
    """
    try:
        stream.reconfigure(errors="backslashreplace")
    except Exception:  # noqa: BLE001 — 출력 완화 실패가 판정을 바꿔선 안 된다
        pass


def main(argv=None):
    """CLI 진입점. 어떤 예외도 0/1로 착지하지 못하게 감싼다."""
    _harden_stream(sys.stdout)
    _harden_stream(sys.stderr)
    try:
        return _run_cli(argv)
    except Exception as exc:  # noqa: BLE001 — 게이트 자체의 고장은 판정이 아니다
        try:
            print(f"⛔ 판정 불가: 게이트 내부 오류 — {type(exc).__name__}: {exc}",
                  file=sys.stderr)
        except Exception:  # noqa: BLE001 — 보고 실패도 판정을 바꾸지 않는다
            pass
        return EXIT_UNDECIDABLE


def _run_cli(argv):
    ap = argparse.ArgumentParser(
        description="Fail-closed release gate for protocol / ICF drafts.")
    ap.add_argument("target")
    ap.add_argument("--profile", default="draft", choices=PROFILES)
    ap.add_argument("--workspace", default="_workspace")
    ap.add_argument("--goal-spec", default=None)
    ap.add_argument("--mrsd-json", default=None)
    args = ap.parse_args(argv)

    if not os.path.isfile(args.target):
        reason = f"대상 파일이 없습니다 — {args.target}"
        print(f"⛔ 최종화 거부: {reason}", file=sys.stderr)
        try:
            _write_report(
                _undecidable_report(args.target, args.profile, args.workspace,
                                    reason),
                args.workspace)
        except Exception as exc:  # noqa: BLE001 — 증거 기록 실패는 더 약한 판정이 아니다
            print(f"   (판정 불가 리포트 기록도 실패: {type(exc).__name__}: {exc})",
                  file=sys.stderr)
        return EXIT_UNDECIDABLE

    report = run_gate(args.target, args.profile, args.workspace,
                      goal_spec_path=args.goal_spec, mrsd_json=args.mrsd_json)

    try:
        report_path = _write_report(report, args.workspace)
    except Exception as exc:  # noqa: BLE001 — 어떤 실패도 판정으로 오인되면 안 된다
        print(f"⛔ 최종화 거부: 리포트 기록 실패 — {type(exc).__name__}: {exc}",
              file=sys.stderr)
        print("   증거를 남기지 못하면 통과를 주장하지 않습니다.", file=sys.stderr)
        return EXIT_UNDECIDABLE

    print(f"release gate ({args.profile}): {report['result']}")
    for d in report["dimensions"]:
        print(f"  [{d['id']}] {d['status']}")
        for f in d["findings"]:
            print(f"      - {f}")
    if report["score_informational"] is not None:
        print(f"  score {report['score_informational']}/100 (참고, 판정 미사용)")
    for w in report["warnings"]:
        print(f"  ⚠️  {w}")
    print(f"  -> {report_path}")
    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
