"""Tests for the fail-closed release gate (qa/finalize_run.py).

Design: docs/p0_release_gate_design_ko.md
NO test performs network I/O: the submission profile's online citation check is
always monkeypatched (same convention as test_citation_verify.py).
"""
import json
import os

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


def test_citation_verified_passes_submission(tmp_path, monkeypatch):
    monkeypatch.setattr(citation_verify, "verify_online",
                        _mock_online("verified"))
    report = fr.run_gate(fixture("protocol_bad_pmid.md"), "submission",
                         str(tmp_path))
    citation = next(d for d in report["dimensions"] if d["id"] == "citation")
    assert citation["status"] == fr.PASS


def test_is_fih_word_boundary():
    assert fr._is_fih({"trial_type": "FIH (SAD/MAD 포함)"}) is True
    assert fr._is_fih({"trial_type": "sad"}) is True
    assert fr._is_fih({"trial_type": "DDI"}) is False
    assert fr._is_fih({"trial_type": "NOMADIC"}) is False, "부분 문자열 오탐 금지"
    assert fr._is_fih(None) is None, "goal_spec 없음은 '알 수 없음'"


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
        assert any("승인" in w for w in report["warnings"]), \
            "미구현 통제는 매 실행마다 경고로 노출되어야 함"


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
