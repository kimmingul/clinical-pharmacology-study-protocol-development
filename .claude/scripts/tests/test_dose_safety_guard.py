"""Tests for the FIH dose-safety guardrail."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "qa"))

import dose_safety_guard as g  # noqa: E402


def test_extract_only_labelled_starting_doses():
    text = (
        "본 시험의 시작 용량은 10 mg으로 한다.\n"
        "이후 용량은 30 mg, 100 mg으로 증량한다.\n"  # not labelled as starting
    )
    doses = g.extract_starting_doses(text)
    assert len(doses) == 1
    assert doses[0]["dose_mg"] == 10.0


def test_violation_when_start_exceeds_mrsd():
    text = "starting dose: 50 mg"
    res = g.check_doses(text, mrsd_mg=29.0)
    assert res["status"] == "violation"
    assert res["violations"][0]["dose_mg"] == 50.0


def test_ok_when_start_within_mrsd():
    text = "시작 용량 20 mg"
    res = g.check_doses(text, mrsd_mg=29.0)
    assert res["status"] == "ok"
    assert res["violations"] == []


def test_skipped_when_no_mrsd():
    text = "시작 용량 500 mg"  # would violate, but no MRSD to check against
    res = g.check_doses(text, mrsd_mg=None)
    assert res["status"] == "skipped"


def test_microgram_normalized_to_mg():
    # 5000 µg = 5 mg, under a 10 mg MRSD -> ok
    res = g.check_doses("initial dose 5000 µg", mrsd_mg=10.0)
    assert res["status"] == "ok"
    # 50000 µg = 50 mg, over 10 mg -> violation
    res2 = g.check_doses("initial dose 50000 mcg", mrsd_mg=10.0)
    assert res2["status"] == "violation"


def test_mrsd_from_json(tmp_path):
    p = tmp_path / "mrsd.json"
    p.write_text(json.dumps({"mrsd_mg": 12.3456, "mrsd_mg_rounded": 12.0}))
    assert g.mrsd_from_json(str(p)) == 12.0  # rounded preferred
    assert g.mrsd_from_json(str(tmp_path / "missing.json")) is None


def test_check_file_strict_paths(tmp_path):
    proto = tmp_path / "03_protocol_draft.md"
    proto.write_text("시작 용량 40 mg 투여")
    mrsd = tmp_path / "mrsd.json"
    mrsd.write_text(json.dumps({"mrsd_mg_rounded": 29.0}))
    res = g.check_file(str(proto), mrsd_json=str(mrsd))
    assert res["status"] == "violation"
