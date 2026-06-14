"""Tests for the shared document linter (qa/doc_lint.py)."""
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
