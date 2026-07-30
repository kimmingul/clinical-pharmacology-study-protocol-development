"""Tests for the fail-closed release gate (qa/finalize_run.py).

Design: docs/p0_release_gate_design_ko.md

NO test performs network I/O. The submission profile calls
citation_verify.verify_online, and TWO distinct mechanisms keep it offline —
both must be preserved:

  1. monkeypatch — tests that need a specific online verdict replace
     citation_verify.verify_online (see _mock_online). Only a few tests do this.
  2. zero citations — the majority of submission-profile tests instead rely on
     their fixture containing NO PMID/NCT at all, so verify_online receives an
     empty list and never opens a socket. protocol_clean.md,
     protocol_missing_b7.md, protocol_unverified_marker.md, icf_no_pipa.md and
     icf_pg_without_part4.md are offline-relied-upon fixtures for this reason.

Adding a PMID or NCT to a mechanism-2 fixture would silently start making real
network calls. test_offline_fixtures_carry_no_citations() below is the guard
that fails loudly if that happens; do not weaken it. New scenarios that need
citations belong in a tmp_path document, not in an existing fixture.
"""
import io
import json
import os
import sys

import pytest

import citation_verify
import doc_lint as doc_lint_module
import finalize_run as fr


def test_missing_target_exits_undecidable(tmp_path):
    code = fr.main([str(tmp_path / "nope.md"), "--workspace", str(tmp_path)])
    assert code == fr.EXIT_UNDECIDABLE


def test_status_constants_are_self_named():
    assert fr.PASS == "PASS"
    assert fr.FAIL == "FAIL"
    assert fr.SKIPPED == "SKIPPED"
    assert fr.FORMAT_ONLY == "FORMAT_ONLY"
    assert fr.NOT_IMPLEMENTED == "NOT_IMPLEMENTED"
    assert fr.ERROR == "ERROR"


def test_exit_codes():
    assert (fr.EXIT_OK, fr.EXIT_REJECTED, fr.EXIT_UNDECIDABLE) == (0, 1, 2)


def test_dim_helper_shape():
    d = fr._dim("citation", fr.PASS, ["x"], detail={"total": 1})
    assert d["id"] == "citation"
    assert d["status"] == "PASS"
    assert d["findings"] == ["x"]
    assert d["detail"] == {"total": 1}


def test_dim_helper_defaults_findings_to_empty_list():
    d = fr._dim("dose", fr.SKIPPED)
    assert d["findings"] == []


FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "fixtures", "gate")


def fixture(name):
    return os.path.join(FIXTURES, name)


def test_clean_protocol_passes_draft(tmp_path):
    code = fr.main([fixture("protocol_clean.md"),
                    "--profile", "draft", "--workspace", str(tmp_path)])
    assert code == fr.EXIT_OK


def test_missing_section_fails_both_profiles(tmp_path):
    for profile in ("draft", "submission"):
        report = fr.run_gate(fixture("protocol_missing_b7.md"),
                             profile, str(tmp_path))
        structure = next(d for d in report["dimensions"]
                         if d["id"] == "structure")
        assert structure["status"] == fr.FAIL
        assert report["exit_code"] == fr.EXIT_REJECTED


def test_structure_dimension_reports_doc_type(tmp_path):
    report = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path))
    assert report["doc_type"] == "protocol"


ADVISORY_FIXTURES = [
    "protocol_unverified_marker.md",
    "icf_no_pipa.md",
    "icf_pg_without_part4.md",
]


@pytest.mark.parametrize("name", ADVISORY_FIXTURES)
def test_advisory_findings_pass_draft_but_block_submission(name, tmp_path):
    draft = fr.run_gate(fixture(name), "draft", str(tmp_path))
    assert draft["exit_code"] == fr.EXIT_OK
    draft_advisory = next(d for d in draft["dimensions"]
                          if d["id"] == "advisory")
    assert draft_advisory["status"] == fr.PASS
    assert draft_advisory["findings"], "draft에서도 findings는 기록되어야 함"

    sub = fr.run_gate(fixture(name), "submission", str(tmp_path))
    sub_advisory = next(d for d in sub["dimensions"] if d["id"] == "advisory")
    assert sub_advisory["status"] == fr.FAIL
    assert sub["exit_code"] == fr.EXIT_REJECTED


def test_clean_protocol_advisory_passes_submission(tmp_path):
    report = fr.run_gate(fixture("protocol_clean.md"), "submission",
                         str(tmp_path))
    advisory = next(d for d in report["dimensions"] if d["id"] == "advisory")
    assert advisory["status"] == fr.PASS
    assert advisory["findings"] == []


def _mock_online(status):
    """verify_online 대체 — 네트워크 접근 없이 지정 status를 돌려준다."""
    def _fake(citations, timeout=8):
        out = []
        for kind in ("pmid", "nct"):
            for value in citations.get(kind, []):
                out.append({"type": kind, "value": value,
                            "exists": status == "verified",
                            "status": status, "detail": "mocked"})
        return out
    return _fake


def test_citation_is_format_only_in_draft(tmp_path):
    report = fr.run_gate(fixture("protocol_bad_pmid.md"), "draft",
                         str(tmp_path))
    citation = next(d for d in report["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FORMAT_ONLY
    assert citation["detail"]["not_found"] == 0
    assert report["exit_code"] == fr.EXIT_OK


def test_citation_not_found_blocks_submission(tmp_path, monkeypatch):
    monkeypatch.setattr(citation_verify, "verify_online",
                        _mock_online("not-found"))
    report = fr.run_gate(fixture("protocol_bad_pmid.md"), "submission",
                         str(tmp_path))
    citation = next(d for d in report["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FAIL
    assert citation["detail"]["not_found"] == 1
    assert report["exit_code"] == fr.EXIT_REJECTED


def test_citation_network_failure_blocks_submission(tmp_path, monkeypatch):
    monkeypatch.setattr(citation_verify, "verify_online",
                        _mock_online("unverified-network"))
    report = fr.run_gate(fixture("protocol_bad_pmid.md"), "submission",
                         str(tmp_path))
    citation = next(d for d in report["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FAIL
    assert citation["detail"]["unverified_network"] == 1


def _setid_document(tmp_path):
    """online 조회 대상이 아닌 인용(DailyMed setid)만 가진 문서를 만든다."""
    doc = tmp_path / "protocol_setid.md"
    doc.write_text(
        open(fixture("protocol_clean.md"), encoding="utf-8").read()
        + "\n라벨 근거: DailyMed setid "
          "12345678-1234-1234-1234-123456789abc\n",
        encoding="utf-8")
    return doc


def test_online_unverifiable_citation_is_format_only_in_submission(
        tmp_path, monkeypatch):
    """setid/url은 verify_online이 조회하지 않는다 — PASS로 세면 안 된다."""
    def _unreached(*a, **k):
        raise AssertionError("이 문서에는 pmid/nct가 없어 네트워크를 타면 안 된다")

    monkeypatch.setattr(citation_verify, "_http_ok", _unreached)
    doc = _setid_document(tmp_path)

    draft = fr.run_gate(str(doc), "draft", str(tmp_path),
                        goal_spec_path=fixture("goal_spec_ddi.json"))
    assert draft["exit_code"] == fr.EXIT_OK, "draft에서는 차단하지 않는다"

    sub = fr.run_gate(str(doc), "submission", str(tmp_path),
                      goal_spec_path=fixture("goal_spec_ddi.json"))
    citation = next(d for d in sub["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FORMAT_ONLY
    assert citation["detail"]["online_unverifiable"] == 1
    assert any("dailymed_setid" in f for f in citation["findings"])
    assert "citation" in sub["blocked_dimensions"]
    assert sub["exit_code"] == fr.EXIT_REJECTED


def test_online_unverifiable_does_not_mask_a_hard_citation_failure(
        tmp_path, monkeypatch):
    """확정된 not_found는 FORMAT_ONLY로 덮이지 않고 FAIL로 남아야 한다."""
    monkeypatch.setattr(citation_verify, "verify_online",
                        _mock_online("not-found"))
    doc = tmp_path / "protocol_mixed.md"
    doc.write_text(
        open(fixture("protocol_bad_pmid.md"), encoding="utf-8").read()
        + "\n라벨 근거: DailyMed setid "
          "12345678-1234-1234-1234-123456789abc\n",
        encoding="utf-8")

    sub = fr.run_gate(str(doc), "submission", str(tmp_path))
    citation = next(d for d in sub["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FAIL
    assert citation["detail"]["online_unverifiable"] == 1


def test_citation_verified_passes_submission(tmp_path, monkeypatch):
    monkeypatch.setattr(citation_verify, "verify_online",
                        _mock_online("verified"))
    report = fr.run_gate(fixture("protocol_bad_pmid.md"), "submission",
                         str(tmp_path))
    citation = next(d for d in report["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.PASS


def test_malformed_nct_is_format_only_in_draft_and_fail_in_submission(
        tmp_path, monkeypatch):
    """draft는 format_fail이 있어도 FORMAT_ONLY(비차단), submission은 FAIL이다.

    nct_malformed는 verify_online이 네트워크 없이 bad-format으로 단락시키므로
    이 경로는 monkeypatch 없이도 네트워크를 타지 않는다 — _http_ok 대역으로 확인한다.
    """
    def _unreached(*a, **k):
        raise AssertionError("잘못된 형식의 NCT는 네트워크 조회 대상이 아니다")

    monkeypatch.setattr(citation_verify, "_http_ok", _unreached)
    doc = tmp_path / "protocol_malformed_nct.md"
    doc.write_text(
        open(fixture("protocol_clean.md"), encoding="utf-8").read()
        + "\n유사 시험: NCT1234 참조.\n", encoding="utf-8")

    draft = fr.run_gate(str(doc), "draft", str(tmp_path),
                        goal_spec_path=fixture("goal_spec_ddi.json"))
    citation = next(d for d in draft["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FORMAT_ONLY
    assert citation["detail"]["format_fail"] == 1
    assert any("format_fail=1" in f for f in citation["findings"])
    assert draft["exit_code"] == fr.EXIT_OK

    sub = fr.run_gate(str(doc), "submission", str(tmp_path),
                      goal_spec_path=fixture("goal_spec_ddi.json"))
    citation = next(d for d in sub["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.FAIL
    assert sub["exit_code"] == fr.EXIT_REJECTED


def test_offline_fixtures_carry_no_citations():
    """아래 submission 테스트들은 이 fixture들이 verify_online에 도달하지 않는 데 의존한다."""
    for name in ("protocol_clean.md", "protocol_missing_b7.md",
                 "protocol_unverified_marker.md", "icf_no_pipa.md",
                 "icf_pg_without_part4.md"):
        cites = citation_verify.extract_citations(
            open(fixture(name), encoding="utf-8").read())
        assert not any(cites.values()), name


def test_is_fih_word_boundary():
    assert fr._is_fih({"trial_type": "FIH (SAD/MAD 포함)"}) is True
    assert fr._is_fih({"trial_type": "sad"}) is True
    assert fr._is_fih({"trial_type": "DDI"}) is False
    assert fr._is_fih({"trial_type": "NOMADIC"}) is not True, "부분 문자열 오탐 금지"
    assert fr._is_fih(None) is None, "goal_spec 없음은 '알 수 없음'"


UNKNOWN_TRIAL_TYPES = [
    pytest.param({"schema": "trial_goal_spec/v1", "drug": "X",
                  "primary_objective": "Y"}, id="key-missing"),
    pytest.param({"trial_type": ""}, id="empty-string"),
    pytest.param({"trial_type": "   "}, id="blank-string"),
    pytest.param({"trial_type": None}, id="null"),
    pytest.param({"trial_type": 123}, id="non-string"),
    pytest.param({"trial_type": "최초 인체 투여 시험"}, id="korean-free-text"),
    pytest.param({"trial_type": "NOMADIC"}, id="unrecognized-token"),
]


@pytest.mark.parametrize("goal_spec", UNKNOWN_TRIAL_TYPES)
def test_is_fih_returns_none_for_unreadable_trial_type(goal_spec):
    """판별 불가는 '비-FIH'가 아니라 '알 수 없음'이어야 한다."""
    assert fr._is_fih(goal_spec) is None


@pytest.mark.parametrize("trial_type", ["DDI", "BE", "FE", "QTc", "ADME",
                                        "BA/BE 시험", "약물상호작용(DDI) 시험"])
def test_is_fih_recognizes_non_fih_vocabulary(trial_type):
    assert fr._is_fih({"trial_type": trial_type}) is False


def test_is_fih_does_not_read_english_be_as_bioequivalence():
    """'to be determined' 같은 미정 문자열이 BE 시험으로 인식되면 fail-open이다."""
    assert fr._is_fih({"trial_type": "to be determined"}) is None


@pytest.mark.parametrize("goal_spec", UNKNOWN_TRIAL_TYPES)
def test_unknown_trial_type_blocks_submission(tmp_path, goal_spec):
    """trial_type을 읽을 수 없는 goal_spec은 확정된 비-FIH와 구분되어야 한다.

    구분하지 못하면 FIH 초과용량 문서가 dose=SKIPPED로 submission을 통과한다.
    """
    gs = tmp_path / "goal_spec.json"
    gs.write_text(json.dumps(goal_spec), encoding="utf-8")
    doc = tmp_path / "protocol_overdose.md"
    doc.write_text(
        open(fixture("protocol_clean.md"), encoding="utf-8").read()
        + "\n시작 용량: 9999 mg\n", encoding="utf-8")

    code = fr.main([str(doc), "--profile", "submission",
                    "--workspace", str(tmp_path), "--goal-spec", str(gs)])
    saved = json.loads((tmp_path / "verification" / "release_gate.json")
                       .read_text(encoding="utf-8"))
    dose = next(d for d in saved["dimensions"] if d["id"] == "dose")
    assert dose["status"] == fr.FAIL
    assert code == fr.EXIT_REJECTED

    draft = fr.run_gate(str(doc), "draft", str(tmp_path),
                        goal_spec_path=str(gs))
    assert next(d for d in draft["dimensions"]
                if d["id"] == "dose")["status"] == fr.SKIPPED


def test_recognized_non_fih_type_stays_skipped(tmp_path):
    """과잉교정 방지 — 확정된 비-FIH 시험은 양쪽 프로파일에서 SKIPPED다."""
    doc = tmp_path / "protocol_overdose.md"
    doc.write_text(
        open(fixture("protocol_clean.md"), encoding="utf-8").read()
        + "\n시작 용량: 9999 mg\n", encoding="utf-8")

    for profile in ("draft", "submission"):
        report = fr.run_gate(str(doc), profile, str(tmp_path),
                             goal_spec_path=fixture("goal_spec_ddi.json"))
        dose = next(d for d in report["dimensions"] if d["id"] == "dose")
        assert dose["status"] == fr.SKIPPED, profile


def test_fih_without_mrsd_blocks_submission_only(tmp_path):
    draft = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path),
                        goal_spec_path=fixture("goal_spec_fih.json"))
    dose = next(d for d in draft["dimensions"] if d["id"] == "dose")
    assert dose["status"] == fr.SKIPPED
    assert draft["exit_code"] == fr.EXIT_OK

    sub = fr.run_gate(fixture("protocol_clean.md"), "submission",
                      str(tmp_path),
                      goal_spec_path=fixture("goal_spec_fih.json"))
    dose = next(d for d in sub["dimensions"] if d["id"] == "dose")
    assert dose["status"] == fr.FAIL
    assert sub["exit_code"] == fr.EXIT_REJECTED


def test_non_fih_dose_is_skipped_in_both_profiles(tmp_path):
    for profile in ("draft", "submission"):
        report = fr.run_gate(fixture("protocol_clean.md"), profile,
                             str(tmp_path),
                             goal_spec_path=fixture("goal_spec_ddi.json"))
        dose = next(d for d in report["dimensions"] if d["id"] == "dose")
        assert dose["status"] == fr.SKIPPED


def test_missing_goal_spec_blocks_submission(tmp_path):
    draft = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path))
    dose = next(d for d in draft["dimensions"] if d["id"] == "dose")
    assert dose["status"] == fr.SKIPPED

    sub = fr.run_gate(fixture("protocol_clean.md"), "submission",
                      str(tmp_path))
    dose = next(d for d in sub["dimensions"] if d["id"] == "dose")
    assert dose["status"] == fr.FAIL
    assert "trial_type" in " ".join(dose["findings"])


def test_dose_violation_blocks_both_profiles(tmp_path):
    mrsd = tmp_path / "mrsd.json"
    mrsd.write_text(json.dumps({"mrsd_mg": 1.0}), encoding="utf-8")
    doc = tmp_path / "protocol_overdose.md"
    doc.write_text(
        "\n".join(f"# B.{i} section" for i in range(1, 17))
        + "\n시작 용량: 50 mg\n", encoding="utf-8")

    for profile in ("draft", "submission"):
        report = fr.run_gate(str(doc), profile, str(tmp_path),
                             goal_spec_path=fixture("goal_spec_fih.json"),
                             mrsd_json=str(mrsd))
        dose = next(d for d in report["dimensions"] if d["id"] == "dose")
        assert dose["status"] == fr.FAIL


@pytest.mark.parametrize("payload", ['{ not json', '{"unexpected_key": 1.0}',
                                     '{"mrsd_mg_rounded": null}'])
def test_fih_unusable_mrsd_json_blocks_submission(tmp_path, payload):
    """mrsd.json이 있어도 MRSD 값을 못 얻으면 부재와 동일하게 취급해야 한다."""
    mrsd = tmp_path / "mrsd.json"
    mrsd.write_text(payload, encoding="utf-8")
    doc = tmp_path / "protocol.md"
    doc.write_text(
        open(fixture("protocol_clean.md"), encoding="utf-8").read()
        + "\n시작 용량: 9999 mg\n", encoding="utf-8")

    sub = fr.run_gate(str(doc), "submission", str(tmp_path),
                      goal_spec_path=fixture("goal_spec_fih.json"),
                      mrsd_json=str(mrsd))
    assert next(d for d in sub["dimensions"] if d["id"] == "dose")["status"] == fr.FAIL
    assert sub["exit_code"] == fr.EXIT_REJECTED

    draft = fr.run_gate(str(doc), "draft", str(tmp_path),
                        goal_spec_path=fixture("goal_spec_fih.json"),
                        mrsd_json=str(mrsd))
    assert next(d for d in draft["dimensions"] if d["id"] == "dose")["status"] == fr.SKIPPED


def test_approval_dimension_is_not_implemented(tmp_path):
    for profile in ("draft", "submission"):
        report = fr.run_gate(fixture("protocol_clean.md"), profile,
                             str(tmp_path),
                             goal_spec_path=fixture("goal_spec_ddi.json"))
        approval = next(d for d in report["dimensions"]
                        if d["id"] == "approval")
        assert approval["status"] == fr.NOT_IMPLEMENTED
        assert report["exit_code"] == fr.EXIT_OK, "미구현은 차단하지 않는다"
        assert any("미구현" in w and "approval" in w
                   for w in report["warnings"]), \
            "미구현 통제는 차원 id와 함께 매 실행마다 경고로 노출되어야 함"
        assert any("'제출 가능'을 의미하지 않습니다" in w
                   for w in report["warnings"])


def test_not_implemented_warning_names_every_such_dimension(tmp_path,
                                                            monkeypatch):
    """경고 문구는 '사람 승인'을 하드코딩하지 않고 실제 차원 id를 나열해야 한다."""
    def dim_future(target, profile, ctx):
        return fr._dim("future", fr.NOT_IMPLEMENTED, reason="미구현")

    monkeypatch.setattr(fr, "DIMENSIONS",
                        fr.DIMENSIONS + (("future", dim_future),))
    report = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path),
                         goal_spec_path=fixture("goal_spec_ddi.json"))
    warning = " ".join(report["warnings"])
    assert "approval" in warning and "future" in warning
    assert report["exit_code"] == fr.EXIT_OK


def test_unknown_dimension_status_is_coerced_to_error(tmp_path, monkeypatch):
    """상태 어휘 밖의 값은 조용히 통과로 집계되지 않고 ERROR로 강등된다."""
    def dim_rogue(target, profile, ctx):
        return fr._dim("approval", "OK")

    monkeypatch.setattr(fr, "DIMENSIONS", tuple(
        (i, dim_rogue if i == "approval" else fn) for i, fn in fr.DIMENSIONS))
    report = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path),
                         goal_spec_path=fixture("goal_spec_ddi.json"))
    rogue = next(d for d in report["dimensions"] if d["id"] == "approval")
    assert rogue["status"] == fr.ERROR
    assert any("'OK'" in f for f in rogue["findings"])
    assert report["result"] == "UNDECIDABLE"
    assert report["exit_code"] == fr.EXIT_UNDECIDABLE


def test_non_string_dimension_status_is_coerced_to_error(tmp_path,
                                                         monkeypatch):
    """해시 불가한 상태값(리스트 등)도 집계를 깨뜨리지 않고 ERROR가 된다."""
    def dim_rogue(target, profile, ctx):
        return {"id": "approval", "status": ["WARN"]}

    monkeypatch.setattr(fr, "DIMENSIONS", tuple(
        (i, dim_rogue if i == "approval" else fn) for i, fn in fr.DIMENSIONS))
    report = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path),
                         goal_spec_path=fixture("goal_spec_ddi.json"))
    rogue = next(d for d in report["dimensions"] if d["id"] == "approval")
    assert rogue["status"] == fr.ERROR
    assert report["exit_code"] == fr.EXIT_UNDECIDABLE


def test_checker_crash_yields_undecidable(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("simulated engine crash")

    monkeypatch.setattr(doc_lint_module, "lint_file", boom)
    report = fr.run_gate(fixture("protocol_clean.md"), "draft", str(tmp_path))
    statuses = {d["id"]: d["status"] for d in report["dimensions"]}
    assert statuses["structure"] == fr.ERROR
    assert report["result"] == "UNDECIDABLE"
    assert report["exit_code"] == fr.EXIT_UNDECIDABLE


def test_error_takes_precedence_over_fail(tmp_path, monkeypatch):
    """structure는 ERROR, dose는 FAIL — exit는 2여야 한다."""
    def boom(*a, **k):
        raise RuntimeError("simulated engine crash")

    monkeypatch.setattr(doc_lint_module, "lint_file", boom)
    report = fr.run_gate(fixture("protocol_clean.md"), "submission",
                         str(tmp_path))
    statuses = {d["id"]: d["status"] for d in report["dimensions"]}
    assert statuses["structure"] == fr.ERROR
    assert statuses["dose"] == fr.FAIL, "goal_spec 없음 → submission FAIL"
    assert report["exit_code"] == fr.EXIT_UNDECIDABLE


def test_score_is_informational_only(tmp_path):
    report = fr.run_gate(fixture("protocol_clean.md"), "submission",
                         str(tmp_path),
                         goal_spec_path=fixture("goal_spec_ddi.json"))
    assert isinstance(report["score_informational"], int)
    assert "score" not in [d["id"] for d in report["dimensions"]], \
        "score는 차원이 아니다"


def test_report_is_written_with_schema_and_all_dimensions(tmp_path):
    code = fr.main([fixture("protocol_clean.md"),
                    "--profile", "draft",
                    "--workspace", str(tmp_path),
                    "--goal-spec", fixture("goal_spec_ddi.json")])
    assert code == fr.EXIT_OK

    out = tmp_path / "verification" / "release_gate.json"
    assert out.is_file()
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["schema"] == "release_gate/v1"
    assert saved["profile"] == "draft"
    assert saved["result"] == "PASS"
    assert saved["exit_code"] == 0
    assert [d["id"] for d in saved["dimensions"]] == [
        "structure", "citation", "dose", "advisory", "approval"]
    assert saved["warnings"], "approval NOT_IMPLEMENTED 경고가 기록되어야 함"


def test_report_write_failure_is_undecidable(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise OSError("read-only filesystem")

    monkeypatch.setattr(fr, "_write_report", boom)
    code = fr.main([fixture("protocol_clean.md"),
                    "--workspace", str(tmp_path)])
    assert code == fr.EXIT_UNDECIDABLE


def test_report_records_failure_details(tmp_path):
    code = fr.main([fixture("protocol_missing_b7.md"),
                    "--profile", "draft",
                    "--workspace", str(tmp_path)])
    assert code == fr.EXIT_REJECTED

    saved = json.loads(
        (tmp_path / "verification" / "release_gate.json").read_text(
            encoding="utf-8"))
    assert saved["result"] == "FAIL"
    assert "structure" in saved["blocked_dimensions"]
    structure = next(d for d in saved["dimensions"]
                     if d["id"] == "structure")
    assert structure["findings"], "차단 사유가 리포트에 남아야 함"


def test_unserializable_report_is_undecidable_and_preserves_prior(
        tmp_path, monkeypatch):
    """직렬화 실패도 exit 2 — exit 1(판정했고 불합격)과 구분되어야 한다."""
    assert fr.main([fixture("protocol_clean.md"),
                    "--workspace", str(tmp_path),
                    "--goal-spec", fixture("goal_spec_ddi.json")]) == fr.EXIT_OK
    out = tmp_path / "verification" / "release_gate.json"
    prior = out.read_text(encoding="utf-8")

    def dim_unserializable(target, profile, ctx):
        return fr._dim("approval", fr.PASS, bad={"set은 JSON 불가"})

    monkeypatch.setattr(fr, "DIMENSIONS", tuple(
        (i, dim_unserializable if i == "approval" else fn)
        for i, fn in fr.DIMENSIONS))

    code = fr.main([fixture("protocol_clean.md"),
                    "--workspace", str(tmp_path),
                    "--goal-spec", fixture("goal_spec_ddi.json")])
    assert code == fr.EXIT_UNDECIDABLE
    assert out.read_text(encoding="utf-8") == prior, "이전 리포트가 보존되어야 함"
    assert not (tmp_path / "verification" /
                "release_gate.json.tmp").exists(), "임시 파일이 남으면 안 된다"


def test_ascii_stdout_does_not_downgrade_undecidable_to_rejected(
        tmp_path, monkeypatch):
    """출력 인코딩 실패가 exit 2를 exit 1로 낮추면 안 된다.

    ASCII 로케일(PYTHONIOENCODING=ascii)에서 한국어 findings·⚠️를 출력하면
    UnicodeEncodeError가 main을 빠져나가고 셸은 1을 본다 — '게이트 고장'이
    '문서 불량'으로 보고되는 fail-open의 거울상이다.
    """
    def boom(*a, **k):
        raise RuntimeError("simulated engine crash")

    monkeypatch.setattr(doc_lint_module, "lint_file", boom)
    ascii_stdout = io.TextIOWrapper(io.BytesIO(), encoding="ascii",
                                    errors="strict")
    monkeypatch.setattr(sys, "stdout", ascii_stdout)

    code = fr.main([fixture("protocol_clean.md"), "--workspace",
                    str(tmp_path)])
    assert code == fr.EXIT_UNDECIDABLE
    ascii_stdout.flush()
    assert ascii_stdout.buffer.getvalue(), "판정 요약은 그래도 출력되어야 한다"


def test_exception_escaping_run_gate_is_undecidable(tmp_path, monkeypatch):
    """run_gate 밖으로 나온 예외(예: 잘못된 profile 키)도 0/1로 착지하면 안 된다."""
    def boom(*a, **k):
        raise KeyError("bogus-profile")

    monkeypatch.setattr(fr, "run_gate", boom)
    code = fr.main([fixture("protocol_clean.md"), "--workspace",
                    str(tmp_path)])
    assert code == fr.EXIT_UNDECIDABLE


def test_undecidable_run_replaces_a_prior_pass_report(tmp_path):
    """이전 실행의 PASS 리포트가 판정 불가 실행 뒤에도 남으면 안 된다."""
    assert fr.main([fixture("protocol_clean.md"),
                    "--workspace", str(tmp_path),
                    "--goal-spec", fixture("goal_spec_ddi.json")]) == fr.EXIT_OK
    out = tmp_path / "verification" / "release_gate.json"
    assert json.loads(out.read_text(encoding="utf-8"))["result"] == "PASS"

    missing = str(tmp_path / "gone.md")
    assert fr.main([missing, "--workspace", str(tmp_path)]) == \
        fr.EXIT_UNDECIDABLE

    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["schema"] == "release_gate/v1"
    assert saved["result"] == "UNDECIDABLE"
    assert saved["exit_code"] == fr.EXIT_UNDECIDABLE
    assert saved["target"] == missing
    assert "gone.md" in saved["reason"]
    assert saved["warnings"]


def test_undecidable_report_write_failure_stays_undecidable(tmp_path,
                                                            monkeypatch):
    """증거를 남기지 못해도 더 약한 판정으로 내려가지 않는다."""
    def boom(*a, **k):
        raise OSError("read-only filesystem")

    monkeypatch.setattr(fr, "_write_report", boom)
    code = fr.main([str(tmp_path / "gone.md"), "--workspace", str(tmp_path)])
    assert code == fr.EXIT_UNDECIDABLE


_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
V2_GOLDEN = os.path.join(
    _REPO_ROOT, "e2e", "v2_2026_04_14_DDI", "_workspace",
    "03_protocol_draft.md")


def test_v2_golden_fixture_passes_draft(tmp_path):
    """기존 산출물 회귀 방지 — CI가 --strict로 통과시키는 파일."""
    assert os.path.isfile(V2_GOLDEN), V2_GOLDEN
    report = fr.run_gate(V2_GOLDEN, "draft", str(tmp_path))
    assert report["exit_code"] == fr.EXIT_OK, report["blocked_dimensions"]
