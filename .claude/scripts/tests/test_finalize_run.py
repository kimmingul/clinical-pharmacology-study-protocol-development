"""Tests for the fail-closed release gate (qa/finalize_run.py).

Design: docs/p0_release_gate_design_ko.md
NO test performs network I/O: the submission profile's online citation check is
always monkeypatched (same convention as test_citation_verify.py).
"""
import json
import os

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
