"""Tests for the pipeline reproducibility manifest (qa/pipeline_manifest.py)."""
import hashlib
import json
import os

import pipeline_manifest as pm


def test_init_creates_manifest(tmp_path):
    ws = str(tmp_path)
    m = pm.init(ws, trial="DDI X+Y")
    assert m["schema"] == "pipeline_manifest/v1"
    assert m["trial"] == "DDI X+Y"
    assert m["phases"] == []
    assert os.path.isfile(os.path.join(ws, "pipeline_manifest.json"))


def test_record_appends_with_sha256(tmp_path):
    ws = str(tmp_path)
    out = tmp_path / "03_protocol_draft.md"
    out.write_text("protocol body", encoding="utf-8")
    pm.init(ws)
    entry = pm.record(ws, phase="8", agent="protocol-writer", model="opus",
                      output=str(out))
    expected = hashlib.sha256(b"protocol body").hexdigest()
    assert entry["output"]["sha256"] == expected
    assert entry["phase"] == "8"

    saved = json.load(open(os.path.join(ws, "pipeline_manifest.json"), encoding="utf-8"))
    assert len(saved["phases"]) == 1


def test_record_auto_inits(tmp_path):
    ws = str(tmp_path)
    pm.record(ws, phase="2", agent="clinician", model="sonnet")
    saved = json.load(open(os.path.join(ws, "pipeline_manifest.json"), encoding="utf-8"))
    assert saved["schema"] == "pipeline_manifest/v1"
    assert len(saved["phases"]) == 1


def test_records_preserve_order(tmp_path):
    ws = str(tmp_path)
    pm.init(ws)
    for ph in ("2", "5", "8"):
        pm.record(ws, phase=ph, agent="a", model="sonnet")
    saved = json.load(open(os.path.join(ws, "pipeline_manifest.json"), encoding="utf-8"))
    assert [p["phase"] for p in saved["phases"]] == ["2", "5", "8"]


def test_inputs_hashed(tmp_path):
    ws = str(tmp_path)
    src = tmp_path / "02_synopsis.md"
    src.write_text("synopsis", encoding="utf-8")
    pm.init(ws)
    entry = pm.record(ws, phase="8", agent="protocol-writer", model="opus",
                      inputs=[str(src)])
    assert entry["inputs"][0]["sha256"] == hashlib.sha256(b"synopsis").hexdigest()


def test_missing_output_file_sha_none(tmp_path):
    ws = str(tmp_path)
    pm.init(ws)
    entry = pm.record(ws, phase="8", agent="x", model="opus",
                      output=str(tmp_path / "does_not_exist.md"))
    assert entry["output"]["sha256"] is None


def test_harness_version_resolves_in_repo():
    """When started from the repo, the version comes from .claude-plugin/."""
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))))
    v = pm._harness_version(start=repo_root)
    assert v[0].isdigit()  # semver-like, not "unknown"
