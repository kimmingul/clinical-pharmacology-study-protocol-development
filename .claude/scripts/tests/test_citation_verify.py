"""Tests for the zero-trust citation/evidence verifier.

Covers the offline (network-free) surface of qa/citation_verify.py and the
provenance snapshotter qa/source_snapshot.py. NO test performs network I/O:
audit_files is always called with online=False (the default).
"""
import hashlib
import json
import os

import citation_verify as cv
import source_snapshot as ss


SAMPLE = (
    "Background per PMID: 12345678 and PMID 9876543. "
    "Similar study NCT01234567 (valid). A malformed id NCT1234 appears too. "
    "Label setid 1234abcd-12ab-34cd-56ef-1234567890ab from DailyMed. "
    "See https://clinicaltrials.gov/study/NCT01234567 for details."
)


def test_extract_finds_all_citation_types():
    cites = cv.extract_citations(SAMPLE)
    assert "12345678" in cites["pmid"]
    assert "9876543" in cites["pmid"]
    assert "NCT01234567" in cites["nct"]
    # malformed short NCT is captured separately for the audit
    assert "NCT1234" in cites["nct_malformed"]
    assert "1234abcd-12ab-34cd-56ef-1234567890ab" in cites["dailymed_setid"]
    assert any(u.startswith("https://clinicaltrials.gov/") for u in cites["url"])


def test_extract_dedupes_and_preserves_order():
    text = "PMID 111 then PMID 222 then PMID 111 again."
    assert cv.extract_citations(text)["pmid"] == ["111", "222"]


def test_classify_offline_flags_short_nct():
    cites = {"nct": ["NCT12345678"], "nct_malformed": ["NCT1234"]}
    results = cv.classify_offline(cites)
    by_value = {r["value"]: r for r in results}
    assert by_value["NCT12345678"]["format_ok"] is True
    assert by_value["NCT1234"]["format_ok"] is False


def test_classify_offline_pmid_and_uuid():
    cites = {
        "pmid": ["12345678"],
        "dailymed_setid": ["1234abcd-12ab-34cd-56ef-1234567890ab"],
        "url": ["https://example.org/x"],
    }
    by_value = {r["value"]: r for r in cv.classify_offline(cites)}
    assert by_value["12345678"]["format_ok"] is True
    assert by_value["1234abcd-12ab-34cd-56ef-1234567890ab"]["format_ok"] is True
    assert by_value["https://example.org/x"]["format_ok"] is True


def test_audit_files_writes_json_with_summary(tmp_path):
    doc = tmp_path / "doc.md"
    doc.write_text(SAMPLE, encoding="utf-8")
    ws = str(tmp_path / "_ws")

    audit = cv.audit_files([str(doc)], workspace=ws, online=False)

    assert audit["schema"] == "citation_audit/v1"
    assert audit["online"] is False
    out = os.path.join(ws, "verification", "citation_audit.json")
    assert os.path.isfile(out)

    saved = json.load(open(out, encoding="utf-8"))
    assert saved["summary"]["total"] == audit["summary"]["total"]
    # exactly one malformed NCT in the sample -> one format failure
    assert saved["summary"]["format_fail"] == 1
    # offline run never touches the network
    assert saved["summary"]["not_found"] == 0
    assert saved["summary"]["unverified_network"] == 0


def test_audit_files_skips_missing_files(tmp_path):
    ws = str(tmp_path / "_ws")
    audit = cv.audit_files([str(tmp_path / "nope.md")], workspace=ws, online=False)
    assert audit["files"] == []
    assert audit["summary"]["total"] == 0


def test_snapshot_writes_file_and_provenance(tmp_path):
    ws = str(tmp_path / "_ws")
    content = "raw label body"
    entry = ss.snapshot(content, "https://dailymed.example/x", workspace=ws)

    expected = hashlib.sha256(content.encode("utf-8")).hexdigest()
    assert entry["sha256"] == expected
    assert entry["url"] == "https://dailymed.example/x"
    assert entry["bytes"] == len(content.encode("utf-8"))

    assert os.path.isfile(entry["path"])
    assert open(entry["path"], encoding="utf-8").read() == content

    prov = os.path.join(ws, "verification", "source_provenance.json")
    saved = json.load(open(prov, encoding="utf-8"))
    assert saved["schema"] == "source_provenance/v1"
    assert saved["sources"][0]["sha256"] == expected


def test_snapshot_hash_stable_and_appends(tmp_path):
    ws = str(tmp_path / "_ws")
    e1 = ss.snapshot("fixed", "https://a", workspace=ws)
    e2 = ss.snapshot("fixed", "https://b", workspace=ws)
    # identical content -> identical hash and snapshot path
    assert e1["sha256"] == e2["sha256"]
    assert e1["path"] == e2["path"]

    prov = os.path.join(ws, "verification", "source_provenance.json")
    saved = json.load(open(prov, encoding="utf-8"))
    assert len(saved["sources"]) == 2
    assert [s["url"] for s in saved["sources"]] == ["https://a", "https://b"]


def test_snapshot_accepts_bytes(tmp_path):
    ws = str(tmp_path / "_ws")
    entry = ss.snapshot(b"\x00\x01rawbytes", "https://b", workspace=ws)
    assert entry["bytes"] == len(b"\x00\x01rawbytes")
    assert entry["sha256"] == hashlib.sha256(b"\x00\x01rawbytes").hexdigest()
