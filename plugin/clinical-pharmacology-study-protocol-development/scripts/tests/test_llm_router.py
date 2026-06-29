"""Offline tests for the Multi-LLM router scripts (.claude/scripts/llm/).

No network, no subprocess: probe_provider is exercised with an injected fake
runner, and the routing/egress logic runs against the REAL reference data files
in .claude/scripts/../references/llm/.
"""
import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS = os.path.dirname(_HERE)
_LLM = os.path.join(_SCRIPTS, "llm")
if _LLM not in sys.path:
    sys.path.insert(0, _LLM)

import egress_gate  # noqa: E402
import health_check  # noqa: E402
import route_select  # noqa: E402

_REF = os.path.join(os.path.dirname(_SCRIPTS), "references", "llm")


def _load(name):
    with open(os.path.join(_REF, name), encoding="utf-8") as f:
        return json.load(f)


PROFILES = _load("model_profiles.json")
COMBOS = _load("combination_profiles.json")
POLICY = _load("egress_policy.json")


# --- fake runners -----------------------------------------------------------

def _is_version_call(cmd):
    """The version probe uses a --version flag; the live probe carries the prompt
    either via stdin or as the final CLI argument (convention: trailing '-' ->
    stdin, else arg)."""
    return any("--version" in str(c) or c == "version" for c in cmd)


def _payload(cmd, stdin_text):
    """Recover the prompt regardless of arg- vs stdin-passing."""
    return stdin_text if stdin_text else (cmd[-1] if cmd else "")


def _ok_runner(expected_sum=17):
    """Runner that returns the correct probe JSON, echoing the nonce."""
    def run(cmd, stdin_text, timeout):
        if _is_version_call(cmd):
            return 0, "claude 1.2.3\n", ""
        nonce = _payload(cmd, stdin_text).split('"probe":"', 1)[1].split('"', 1)[0]
        return 0, json.dumps({"probe": nonce, "sum": expected_sum}), ""
    return run


def _timeout_runner(cmd, stdin_text, timeout):
    if _is_version_call(cmd):
        return 0, "v1\n", ""
    raise subprocess.TimeoutExpired(cmd, timeout)


def _auth_fail_runner(cmd, stdin_text, timeout):
    if _is_version_call(cmd):
        return 0, "v1\n", ""
    return 1, "", "Error: unauthorized — please run login to refresh your key"


# --- evaluate_probe ---------------------------------------------------------

def test_evaluate_probe_ok():
    status, _ = health_check.evaluate_probe(
        '{"probe":"abc123","sum":17}', "abc123")
    assert status == "ok"


def test_evaluate_probe_echo_only_no_sum():
    """Model echoes the prompt without computing the sum -> bad_output."""
    status, _ = health_check.evaluate_probe('{"probe":"abc123"}', "abc123")
    assert status == "bad_output"


def test_evaluate_probe_wrong_sum():
    status, _ = health_check.evaluate_probe(
        '{"probe":"abc123","sum":16}', "abc123")
    assert status == "bad_output"


def test_evaluate_probe_surrounding_prose_ok():
    out = 'Sure! Here is the JSON: {"probe":"zz99","sum":17} — hope that helps.'
    status, _ = health_check.evaluate_probe(out, "zz99")
    assert status == "ok"


def test_evaluate_probe_nonce_mismatch():
    status, _ = health_check.evaluate_probe(
        '{"probe":"other","sum":17}', "abc123")
    assert status == "bad_output"


# --- probe_provider (fake runner only) --------------------------------------

def test_probe_provider_ok():
    prof = PROFILES["providers"]["anthropic"]
    # shutil.which must see the CLI; monkeypatch-free: force via fake which.
    orig_which = health_check.shutil.which
    health_check.shutil.which = lambda c: "/usr/bin/" + c
    try:
        r = health_check.probe_provider(
            "anthropic", prof, "nonce123", runner=_ok_runner())
    finally:
        health_check.shutil.which = orig_which
    assert r["status"] == "ok"
    assert r["cli_version"] == "claude 1.2.3"
    assert r["latency_ms"] is not None


def test_probe_provider_timeout(monkeypatch):
    prof = PROFILES["providers"]["anthropic"]
    monkeypatch.setattr(health_check.shutil, "which", lambda c: "/usr/bin/" + c)
    r = health_check.probe_provider(
        "anthropic", prof, "nonce123", runner=_timeout_runner)
    assert r["status"] == "timeout"


def test_probe_provider_missing(monkeypatch):
    prof = PROFILES["providers"]["anthropic"]
    monkeypatch.setattr(health_check.shutil, "which", lambda c: None)
    r = health_check.probe_provider(
        "anthropic", prof, "nonce123", runner=_ok_runner())
    assert r["status"] == "missing"


def test_probe_provider_auth_fail(monkeypatch):
    prof = PROFILES["providers"]["anthropic"]
    monkeypatch.setattr(health_check.shutil, "which", lambda c: "/usr/bin/" + c)
    r = health_check.probe_provider(
        "anthropic", prof, "nonce123", runner=_auth_fail_runner)
    assert r["status"] == "auth_fail"


def test_check_all_and_write(tmp_path, monkeypatch):
    monkeypatch.setattr(health_check.shutil, "which", lambda c: "/usr/bin/" + c)
    health = health_check.check_all(
        PROFILES, providers=["anthropic", "xai"], runner=_ok_runner())
    assert health["schema"] == "llm_health/v1"
    assert set(health["providers"]) == {"anthropic", "xai"}
    assert all(v["status"] == "ok" for v in health["providers"].values())
    path = health_check.write_health(health, str(tmp_path))
    assert os.path.isfile(path)
    assert json.load(open(path, encoding="utf-8"))["schema"] == "llm_health/v1"


# --- select_routing ---------------------------------------------------------

def _health(*ok_providers):
    return {
        "schema": "llm_health/v1",
        "providers": {p: {"status": "ok"} for p in ok_providers},
    }


def test_available_providers():
    h = {"providers": {"a": {"status": "ok"}, "b": {"status": "auth_fail"}}}
    assert route_select.available_providers(h) == ["a"]


def test_routing_single_llm_all_host():
    plan = route_select.select_routing(
        _health("anthropic"), PROFILES, COMBOS, "anthropic", today="2026-06-15")
    assert plan["multi_llm"] is False
    assert all(v == "anthropic" for v in plan["assignment"].values())


def test_routing_host_plus_xai_biostat():
    plan = route_select.select_routing(
        _health("anthropic", "xai"), PROFILES, COMBOS, "anthropic",
        today="2026-06-15")
    assert plan["multi_llm"] is True
    assert plan["assignment"]["authoring"] == "anthropic"
    assert plan["assignment"]["biostat_adversarial"] == "xai"


def test_routing_full_panel_host_openai():
    plan = route_select.select_routing(
        _health("anthropic", "openai", "google", "xai"),
        PROFILES, COMBOS, "openai", today="2026-06-15")
    assert plan["assignment"]["authoring"] == "openai"
    assert plan["assignment"]["biostat_adversarial"] == "xai"
    assert plan["assignment"]["regulatory_cross_check"] == "google"
    # judge must differ from the authoring provider (openai tops judge_synth).
    assert plan["assignment"]["judge_synth"] != "openai"
    assert plan["assignment"]["judge_synth"] is not None


def test_routing_judge_differs_from_author():
    plan = route_select.select_routing(
        _health("anthropic", "openai"), PROFILES, COMBOS, "openai",
        today="2026-06-15")
    assert plan["assignment"]["judge_synth"] != "openai"


def test_routing_stale_warning():
    plan = route_select.select_routing(
        _health("anthropic", "openai"), PROFILES, COMBOS, "anthropic",
        today="2027-01-01")
    assert plan["stale_warning"] is True
    assert any("stale" in n.lower() or "older" in n.lower() for n in plan["notes"])


def test_routing_not_stale_when_recent():
    plan = route_select.select_routing(
        _health("anthropic", "openai"), PROFILES, COMBOS, "anthropic",
        today="2026-06-20")
    assert plan["stale_warning"] is False


def test_rank_for_role_deterministic_tiebreak():
    # regulatory_cross_check: google 9 > openai 7 > anthropic 8? check ordering
    ranked = route_select.rank_for_role(
        "biostat_adversarial", ["anthropic", "openai", "google", "xai"], PROFILES)
    # xai 9 > openai 8 > anthropic 6 == google? google 5 -> xai, openai, anthropic, google
    assert ranked[0] == "xai"


def test_write_routing(tmp_path):
    plan = route_select.select_routing(
        _health("anthropic", "openai"), PROFILES, COMBOS, "anthropic",
        today="2026-06-15")
    path = route_select.write_routing(plan, str(tmp_path))
    assert os.path.isfile(path)
    assert json.load(open(path, encoding="utf-8"))["schema"] == "llm_routing/v1"


# --- egress_gate ------------------------------------------------------------

def test_classify_safety_critical():
    assert egress_gate.classify(
        "NOAEL was 50 mg/kg in the rat study", POLICY) == "SAFETY_CRITICAL"


def test_classify_sponsor_confidential():
    assert egress_gate.classify(
        "see the confidential Investigator's Brochure", POLICY) \
        == "SPONSOR_CONFIDENTIAL"


def test_classify_default_is_conservative():
    # plain pharmacology text matches no marker -> default SPONSOR_CONFIDENTIAL
    assert egress_gate.classify(
        "aspirin pharmacokinetics overview", POLICY) == "SPONSOR_CONFIDENTIAL"


def test_classify_precedence_safety_over_confidential():
    text = "confidential IB note: starting dose derived from NOAEL"
    assert egress_gate.classify(text, POLICY) == "SAFETY_CRITICAL"


def test_allowed_public_any_provider():
    assert egress_gate.allowed("xai", "PUBLIC", POLICY, "anthropic") is True


def test_allowed_safety_critical_non_host_blocked():
    assert egress_gate.allowed(
        "openai", "SAFETY_CRITICAL", POLICY, "anthropic") is False


def test_allowed_safety_critical_host_ok():
    assert egress_gate.allowed(
        "anthropic", "SAFETY_CRITICAL", POLICY, "anthropic") is True


def test_check_blocks_confidential_to_non_host():
    r = egress_gate.check(
        "openai", "confidential IB data", POLICY, "anthropic")
    assert r["classification"] == "SPONSOR_CONFIDENTIAL"
    assert r["allowed"] is False


def test_check_files_most_restrictive(tmp_path):
    f1 = tmp_path / "a.txt"
    f1.write_text("aspirin pharmacokinetics", encoding="utf-8")
    f2 = tmp_path / "b.txt"
    f2.write_text("MRSD derived from NOAEL", encoding="utf-8")
    r = egress_gate.check_files(
        "openai", [str(f1), str(f2)], POLICY, "anthropic")
    assert r["classification"] == "SAFETY_CRITICAL"
    assert r["allowed"] is False
    assert r["files"] == [str(f1), str(f2)]


def test_check_unknown_classification_fail_closed():
    policy = {"fail_closed": True, "default_classification": "MYSTERY",
              "classifications": {}, "markers": {}}
    r = egress_gate.check("openai", "anything", policy, "anthropic")
    assert r["allowed"] is False


# --- declared-floor (caller can downgrade unmarked content to enable egress,
#     but markers can only escalate) -----------------------------------------

def test_declared_public_allows_unmarked_cross_vendor():
    # Approved-drug public content, caller declares REGULATORY_PUBLIC -> egress ok.
    r = egress_gate.check(
        "openai", "clopidogrel public DDI pharmacokinetics", POLICY,
        "anthropic", declared="REGULATORY_PUBLIC")
    assert r["classification"] == "REGULATORY_PUBLIC"
    assert r["allowed"] is True


def test_declared_public_cannot_override_safety_markers():
    # Even if caller declares PUBLIC, a NOAEL marker escalates to SAFETY_CRITICAL.
    r = egress_gate.check(
        "openai", "starting dose from NOAEL 30 mg/kg", POLICY,
        "anthropic", declared="PUBLIC")
    assert r["classification"] == "SAFETY_CRITICAL"
    assert r["allowed"] is False


def test_no_declaration_stays_conservative():
    # Declaring nothing keeps the fail-closed default (blocked to non-host).
    r = egress_gate.check(
        "openai", "aspirin pharmacokinetics", POLICY, "anthropic")
    assert r["classification"] == "SPONSOR_CONFIDENTIAL"
    assert r["allowed"] is False


# --- egress: word-boundary markers + confidential IB context (review fixes) -

def test_marker_word_boundary_no_false_positive():
    # 'ib' must not match inside 'calibration'/'fibrosis'; plain text -> default.
    r = egress_gate.check(
        "openai", "calibration and fibrosis of the assay", POLICY, "anthropic",
        declared="REGULATORY_PUBLIC")
    assert r["classification"] == "REGULATORY_PUBLIC"
    assert r["allowed"] is True


def test_marker_word_boundary_real_ib_still_detected():
    r = egress_gate.check(
        "openai", "see the IB section 3", POLICY, "anthropic",
        declared="REGULATORY_PUBLIC")
    assert r["classification"] == "SPONSOR_CONFIDENTIAL"
    assert r["allowed"] is False


def test_confidential_context_overrides_public_declaration():
    # Even declaring REGULATORY_PUBLIC, an IB-confidential study can't egress.
    r = egress_gate.check(
        "openai", "aspirin pharmacokinetics (no markers)", POLICY, "anthropic",
        declared="REGULATORY_PUBLIC", confidential_context=True)
    assert r["classification"] == "SPONSOR_CONFIDENTIAL"
    assert r["allowed"] is False


def test_load_ib_confidential(tmp_path):
    p = tmp_path / "ib_manifest.json"
    p.write_text('{"confidential": true}', encoding="utf-8")
    assert egress_gate.load_ib_confidential(str(p)) is True
    p2 = tmp_path / "open.json"
    p2.write_text('{"confidential": false}', encoding="utf-8")
    assert egress_gate.load_ib_confidential(str(p2)) is False
    assert egress_gate.load_ib_confidential(str(tmp_path / "missing.json")) is False


# --- v4.2: agy migration + explicit snapshot model pins ---------------------

def test_google_cli_is_agy_not_gemini():
    """gemini CLI was force-migrated to agy (antigravity, 2026-06-18)."""
    g = PROFILES["providers"]["google"]
    assert g["cli"] == "agy"
    assert g["version_cmd"][0] == "agy"


def test_resolved_models_are_bare_pinnable_ids():
    """resolved_model is passed to each CLI via --model, so it must be a bare id
    (no descriptive prose like 'gpt-5.5 (OpenAI; codex-cli)')."""
    for key, prof in PROFILES["providers"].items():
        rm = prof["resolved_model"]
        assert rm and " " not in rm and "(" not in rm, \
            f"{key} resolved_model {rm!r} is not a bare --model id"


def test_probe_cmd_pins_the_resolved_model():
    """The health probe must exercise the SAME model ask_model.sh will call:
    --model <resolved_model> appears in probe_cmd."""
    for key, prof in PROFILES["providers"].items():
        cmd = prof["probe_cmd"]
        assert "--model" in cmd, f"{key} probe_cmd missing --model pin"
        i = cmd.index("--model")
        assert cmd[i + 1] == prof["resolved_model"], \
            f"{key} probe pins {cmd[i+1]!r} != resolved_model {prof['resolved_model']!r}"


def test_probe_cmd_prompt_lands_as_value_or_stdin():
    """Append convention: probe_cmd must end with '-p' (prompt appended as its
    value) or '-' (stdin), so health_check's payload extraction keeps working."""
    for key, prof in PROFILES["providers"].items():
        assert prof["probe_cmd"][-1] in ("-p", "-"), \
            f"{key} probe_cmd must end with -p or -, got {prof['probe_cmd'][-1]!r}"


def test_anthropic_pins_opus_and_forbids_fable():
    """Export-controlled Fable must never be auto-selected; Opus is pinned."""
    a = PROFILES["providers"]["anthropic"]
    assert a["resolved_model"] == "claude-opus-4-8"
    assert "fable" in a.get("availability_constraint", "").lower()


def test_check_all_honors_per_provider_probe_timeout():
    """google (agy) declares probe_timeout=70; anthropic uses the global default."""
    seen = {}

    def capturing_runner(cmd, stdin_text, timeout):
        if _is_version_call(cmd):
            return 0, "v1\n", ""
        seen[cmd[0]] = timeout
        nonce = _payload(cmd, stdin_text).split('"probe":"', 1)[1].split('"', 1)[0]
        return 0, json.dumps({"probe": nonce, "sum": 17}), ""

    orig = health_check.shutil.which
    health_check.shutil.which = lambda c: "/usr/bin/" + c
    try:
        health_check.check_all(
            PROFILES, providers=["anthropic", "google"],
            runner=capturing_runner, timeout=15)
    finally:
        health_check.shutil.which = orig
    assert seen.get("agy") == 70, "google probe_timeout override not honored"
    assert seen.get("claude") == 15, "anthropic should use the global default timeout"
