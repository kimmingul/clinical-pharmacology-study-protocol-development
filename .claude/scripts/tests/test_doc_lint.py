"""Tests for the shared document linter (qa/doc_lint.py)."""
import json

import doc_lint


PROTOCOL_OK = "\n".join(f"# B.{i} x" for i in range(1, 17)) + """
- 필수 문서 보존: 시험 종료 후 최소 15년 (KGCP)
1차 평가변수 동등성 90% CI 80.00–125.00%
"""

PROTOCOL_BAD_RETENTION = "\n".join(f"# B.{i} x" for i in range(1, 17)) + """
- 보존 기간: 시험 종료 후 3년 (KGCP)
"""


def test_protocol_full_sections_pass():
    errors, _ = doc_lint.lint_protocol(PROTOCOL_OK)
    assert errors == []


def test_protocol_missing_sections_error():
    errors, _ = doc_lint.lint_protocol("# B.1 only")
    assert any("Appendix B sections missing" in e for e in errors)


def test_protocol_retention_3year_is_error():
    errors, _ = doc_lint.lint_protocol(PROTOCOL_BAD_RETENTION)
    assert any("retention" in e.lower() and "15년" in e for e in errors)


def test_protocol_retention_15year_ok():
    errors, _ = doc_lint.lint_protocol(PROTOCOL_OK)
    assert not any("retention" in e.lower() for e in errors)


def test_disease_history_3year_not_flagged():
    """'최근 3년 이내 만성질환' is a medical criterion, not retention."""
    text = "\n".join(f"# B.{i} x" for i in range(1, 17)) + \
        "\n- 최근 3년 이내 만성질환이 없는 자\n- 보존 기간: 최소 15년 (KGCP)\n"
    errors, _ = doc_lint.lint_protocol(text)
    assert errors == []


def test_ci_bounds_warning_when_missing():
    text = "\n".join(f"# B.{i} x" for i in range(1, 17)) + \
        "\n- 보존: 최소 15년\n동등성 90% 신뢰구간으로 평가\n"
    _, warnings = doc_lint.lint_protocol(text)
    assert any("80.00" in w and "125.00" in w for w in warnings)


def test_unverified_marker_warns():
    _, warnings = doc_lint.lint_protocol("# B.1 [출처 미확인]")
    assert any("unverified" in w.lower() for w in warnings)


def test_bare_nct_word_not_flagged():
    """Generic prose mention of 'NCT' must not warn (only malformed ids)."""
    _, warnings = doc_lint.lint_protocol("각 NCT 번호를 표로 기재했다.")
    assert not any("NCT" in w for w in warnings)


def test_malformed_nct_warns():
    _, warnings = doc_lint.lint_protocol("관련 시험 NCT12345 (7자리 미만)")
    assert any("NCT" in w for w in warnings)


def test_icf_missing_pipa_warns():
    _, warnings = doc_lint.lint_icf("동의설명서 본문")
    assert any("PIPA" in w or "개인정보" in w for w in warnings)


def test_icf_pg_without_part4_warns():
    _, warnings = doc_lint.lint_icf("개인정보 동의. 약물유전체(PG) 분석을 수행한다.")
    assert any("Part 4" in w or "선택 동의" in w for w in warnings)


def test_lint_file_dispatches_by_name(tmp_path):
    p = tmp_path / "04_icf_draft.md"
    p.write_text("개인정보 동의 내용", encoding="utf-8")
    doc_type, _, _ = doc_lint.lint_file(str(p))
    assert doc_type == "icf"


# --- score_file / goal-spec scoring -----------------------------------------

def _write_protocol(tmp_path, text, name="03_protocol_draft.md"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_lint_file_tuple_unchanged(tmp_path):
    """The public lint_file API must still return (doc_type, errors, warnings)."""
    p = _write_protocol(tmp_path, PROTOCOL_OK)
    result = doc_lint.lint_file(p)
    assert isinstance(result, tuple) and len(result) == 3
    doc_type, errors, warnings = result
    assert doc_type == "protocol"
    assert errors == []
    assert isinstance(warnings, list)


def test_score_clean_protocol_is_100(tmp_path):
    p = _write_protocol(tmp_path, PROTOCOL_OK)
    r = doc_lint.score_file(p)
    assert r["doc_type"] == "protocol"
    assert r["score"] == 100
    assert r["critical"] == []
    assert r["passed"] is True


def test_score_missing_sections_critical_and_failed(tmp_path):
    p = _write_protocol(tmp_path, "# B.1 only")
    r = doc_lint.score_file(p)
    assert r["critical"], "missing sections must produce a critical finding"
    assert r["score"] < 100
    assert r["passed"] is False


def test_score_retention_3year_critical(tmp_path):
    p = _write_protocol(tmp_path, PROTOCOL_BAD_RETENTION)
    r = doc_lint.score_file(p)
    assert any("retention" in c.lower() for c in r["critical"])
    assert r["passed"] is False


def test_score_goal_spec_required_section_enforced(tmp_path):
    """A goal_spec requiring B.99 (absent) adds a critical finding."""
    p = _write_protocol(tmp_path, PROTOCOL_OK)
    goal = {"schema": "trial_goal_spec/v1", "required_ich_sections": ["B.99"]}
    r = doc_lint.score_file(p, goal_spec=goal)
    assert any("B.99" in c for c in r["critical"])
    assert r["passed"] is False


def test_score_goal_spec_retention_min_critical(tmp_path):
    """goal_spec retention_years_min flags a too-short retention period."""
    text = "\n".join(f"# B.{i} x" for i in range(1, 17)) + \
        "\n- 보존 기간: 시험 종료 후 10년\n동등성 90% CI 80.00–125.00%\n"
    p = _write_protocol(tmp_path, text)
    goal = {"schema": "trial_goal_spec/v1", "retention_years_min": 15}
    r = doc_lint.score_file(p, goal_spec=goal)
    assert any("retention" in c.lower() or "보존" in c for c in r["critical"])


def test_load_goal_spec_roundtrip(tmp_path):
    spec = {"schema": "trial_goal_spec/v1", "drug": "x", "trial_type": "DDI",
            "primary_objective": "y"}
    p = tmp_path / "goal.json"
    p.write_text(json.dumps(spec), encoding="utf-8")
    assert doc_lint.load_goal_spec(str(p)) == spec


def test_load_goal_spec_missing_returns_none(tmp_path):
    assert doc_lint.load_goal_spec(str(tmp_path / "nope.json")) is None
    bad = tmp_path / "bad.json"
    bad.write_text("{ not json", encoding="utf-8")
    assert doc_lint.load_goal_spec(str(bad)) is None


def test_icf_retention_3year_is_error():
    # ICF with 보관 기간 3년 must be flagged (statutory min 15년).
    errs, _warns = doc_lint.lint_icf("개인정보 보관 기간은 최소 3년으로 한다.")
    assert any("retention" in e.lower() or "15년" in e for e in errs)


def test_retention_legal_basis_present():
    _e = doc_lint._retention_errors("필수문서 보존 기간은 3년으로 한다.")
    assert _e and "별표 4" in _e[0]
