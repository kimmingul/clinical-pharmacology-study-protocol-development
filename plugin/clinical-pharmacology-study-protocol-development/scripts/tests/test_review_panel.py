"""Offline tests for the Phase 9 cross-vendor critic panel (review_panel.py).

No network, no subprocess: build_panel runs against a hand-built routing plan
and the REAL review_roles.json; synthesize runs against fixture vendor JSON
files written into tmp_path.
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS = os.path.dirname(_HERE)
_LLM = os.path.join(_SCRIPTS, "llm")
if _LLM not in sys.path:
    sys.path.insert(0, _LLM)

import review_panel  # noqa: E402

_REF = os.path.join(os.path.dirname(_SCRIPTS), "references", "llm")

with open(os.path.join(_REF, "review_roles.json"), encoding="utf-8") as f:
    ROLES = json.load(f)

_FIXED_NOW = "2026-06-16T00:00:00+00:00"


def _routing():
    return {
        "schema": "llm_routing/v1",
        "host": "anthropic",
        "available": ["anthropic", "google", "xai"],
        "multi_llm": True,
        "assignment": {
            "regulatory_cross_check": "google",
            "biostat_adversarial": "xai",
            "citation_integrity": "google",
            "authoring": "anthropic",
        },
    }


def _draft(tmp_path):
    p = tmp_path / "draft.md"
    p.write_text("# Protocol\nThis is the DDI study draft body.", encoding="utf-8")
    return str(p)


def _entry(plan, role):
    return next(e for e in plan["entries"] if e["role"] == role)


# --- build_panel ------------------------------------------------------------

def test_build_panel_biostat_external_xai(tmp_path):
    plan = review_panel.build_panel(
        _routing(), ROLES, _draft(tmp_path), "anthropic",
        workspace=str(tmp_path), now=_FIXED_NOW)
    e = _entry(plan, "biostat_adversarial")
    assert e["mode"] == "external"
    assert e["provider"] == "xai"
    assert os.path.isfile(e["prompt_file"])
    assert e["out_file"].endswith("vendor_xai_biostat_adversarial.json")


def test_build_panel_regulatory_external_google(tmp_path):
    plan = review_panel.build_panel(
        _routing(), ROLES, _draft(tmp_path), "anthropic",
        workspace=str(tmp_path), now=_FIXED_NOW)
    e = _entry(plan, "regulatory_cross_check")
    assert e["mode"] == "external"
    assert e["provider"] == "google"
    assert os.path.isfile(e["prompt_file"])


def test_build_panel_host_role_inline(tmp_path):
    """A panel role assigned to the host provider runs inline, no prompt file."""
    routing = _routing()
    routing["assignment"]["citation_integrity"] = "anthropic"
    plan = review_panel.build_panel(
        routing, ROLES, _draft(tmp_path), "anthropic",
        workspace=str(tmp_path), now=_FIXED_NOW)
    e = _entry(plan, "citation_integrity")
    assert e["mode"] == "host"
    assert "prompt_file" not in e


def test_build_panel_unavailable_provider_skipped(tmp_path):
    routing = _routing()
    routing["assignment"]["biostat_adversarial"] = "openai"  # not in available
    plan = review_panel.build_panel(
        routing, ROLES, _draft(tmp_path), "anthropic",
        workspace=str(tmp_path), now=_FIXED_NOW)
    e = _entry(plan, "biostat_adversarial")
    assert e["mode"] == "skipped"
    assert e["reason"] == "provider_unavailable"


def test_build_panel_none_assignment_is_host(tmp_path):
    routing = _routing()
    routing["assignment"]["citation_integrity"] = None
    plan = review_panel.build_panel(
        routing, ROLES, _draft(tmp_path), "anthropic",
        workspace=str(tmp_path), now=_FIXED_NOW)
    assert _entry(plan, "citation_integrity")["mode"] == "host"


def test_prompt_file_contains_instruction_and_draft(tmp_path):
    plan = review_panel.build_panel(
        _routing(), ROLES, _draft(tmp_path), "anthropic",
        workspace=str(tmp_path), now=_FIXED_NOW)
    e = _entry(plan, "biostat_adversarial")
    text = open(e["prompt_file"], encoding="utf-8").read()
    assert ROLES["roles"]["biostat_adversarial"]["instruction"] in text
    assert "DDI study draft body" in text
    assert ROLES["output_contract"] in text


def test_build_panel_schema_and_now(tmp_path):
    plan = review_panel.build_panel(
        _routing(), ROLES, _draft(tmp_path), "anthropic",
        workspace=str(tmp_path), classification="REGULATORY_PUBLIC",
        now=_FIXED_NOW)
    assert plan["schema"] == "review_panel/v1"
    assert plan["host"] == "anthropic"
    assert plan["classification"] == "REGULATORY_PUBLIC"
    assert plan["generated_at"] == _FIXED_NOW


def test_write_panel(tmp_path):
    plan = review_panel.build_panel(
        _routing(), ROLES, _draft(tmp_path), "anthropic",
        workspace=str(tmp_path), now=_FIXED_NOW)
    path = review_panel.write_panel(plan, str(tmp_path))
    assert os.path.isfile(path)
    assert json.load(open(path, encoding="utf-8"))["schema"] == "review_panel/v1"


# --- synthesize -------------------------------------------------------------

def _write_vendor(tmp_path, provider, role, payload):
    review_dir = tmp_path / "review"
    review_dir.mkdir(exist_ok=True)
    p = review_dir / f"vendor_{provider}_{role}.json"
    if isinstance(payload, str):
        p.write_text(payload, encoding="utf-8")
    else:
        p.write_text(json.dumps(payload), encoding="utf-8")
    return str(p)


def test_synthesize_deterministic_first_and_vendor_tagged(tmp_path):
    det = [{"severity": "Critical", "source": "doc_lint",
            "issue": "missing B.8 efficacy section"}]
    valid = _write_vendor(tmp_path, "xai", "biostat_adversarial", {
        "role": "biostat_adversarial",
        "verdict": "fail",
        "findings": [{"severity": "Critical", "section": "B.10",
                      "issue": "CV% unjustified",
                      "evidence": "no source", "recommendation": "cite"}],
    })
    malformed = _write_vendor(
        tmp_path, "google", "regulatory_cross_check", "not json at all {{{")

    result = review_panel.synthesize(det, [valid, malformed],
                                     workspace=str(tmp_path))

    # Deterministic Critical is listed FIRST among criticals.
    assert result["critical"][0]["source"] == "doc_lint"
    assert result["critical"][0]["issue"] == "missing B.8 efficacy section"
    # Vendor Critical tagged by <provider>:<role>.
    vendor_crit = result["critical"][1]
    assert vendor_crit["source"] == "xai:biostat_adversarial"
    # Malformed -> a Minor "unparseable" finding (never raised).
    unparseable = [f for f in result["minor"]
                   if f["issue"] == "critic output unparseable"]
    assert len(unparseable) == 1
    assert unparseable[0]["source"] == "google:regulatory_cross_check"
    # by_source counts.
    assert result["by_source"]["doc_lint"] == 1
    assert result["by_source"]["xai:biostat_adversarial"] == 1
    assert result["by_source"]["google:regulatory_cross_check"] == 1
    assert result["schema"] == "review_synthesis/v1"


def test_synthesize_conflict_detection(tmp_path):
    a = _write_vendor(tmp_path, "xai", "biostat_adversarial", {
        "role": "biostat_adversarial", "verdict": "concerns",
        "findings": [{"severity": "Critical", "section": "B.10",
                      "issue": "underpowered"}],
    })
    b = _write_vendor(tmp_path, "google", "regulatory_cross_check", {
        "role": "regulatory_cross_check", "verdict": "concerns",
        "findings": [{"severity": "Minor", "section": "B.10",
                      "issue": "wording"}],
    })
    result = review_panel.synthesize([], [a, b], workspace=str(tmp_path))
    assert len(result["conflicts"]) == 1
    conflict = result["conflicts"][0]
    assert conflict["section"] == "B.10"
    assert set(conflict["sources"]) == {
        "xai:biostat_adversarial", "google:regulatory_cross_check"}


def test_synthesize_no_conflict_same_severity(tmp_path):
    a = _write_vendor(tmp_path, "xai", "biostat_adversarial", {
        "findings": [{"severity": "Major", "section": "B.10", "issue": "x"}],
    })
    b = _write_vendor(tmp_path, "google", "regulatory_cross_check", {
        "findings": [{"severity": "Major", "section": "B.10", "issue": "y"}],
    })
    result = review_panel.synthesize([], [a, b], workspace=str(tmp_path))
    assert result["conflicts"] == []


def test_synthesize_missing_vendor_skipped(tmp_path):
    missing = str(tmp_path / "review" / "vendor_xai_biostat_adversarial.json")
    result = review_panel.synthesize([], [missing], workspace=str(tmp_path))
    assert result["sources_skipped"] == [missing]
    assert result["sources_used"] == []


def test_synthesize_write(tmp_path):
    result = review_panel.synthesize([], [], workspace=str(tmp_path))
    path = review_panel.write_synthesis(result, str(tmp_path))
    assert os.path.isfile(path)
    assert json.load(open(path, encoding="utf-8"))["schema"] \
        == "review_synthesis/v1"
