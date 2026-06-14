#!/usr/bin/env python3
"""Zero-trust citation / evidence verifier for generated trial documents.

Premise: a citation in a draft is *untrusted* until it is independently
checked. This module extracts the machine-checkable references the harness
relies on (PubMed PMIDs, ClinicalTrials.gov NCT ids, DailyMed SPL setids, and
bare URLs), validates their *shape* offline, and — only when explicitly asked —
confirms a PMID/NCT actually resolves against its public registry.

Three trust layers:
  1. extract_citations  — pure, find the ids in the prose.
  2. classify_offline   — pure, is each id well-formed? (NCT = NCT + exactly 8
                          digits, consistent with qa/doc_lint.py).
  3. verify_online      — optional network round-trip; every failure degrades
                          to "unverified-network" instead of raising.

audit_files() ties them together and writes a JSON audit trail to
<workspace>/verification/citation_audit.json.

Usage
-----
    citation_verify.py extract <file>
    citation_verify.py audit <file>... [--workspace _workspace] [--online]

Default is OFFLINE so CI and tests never reach the network. stdlib only.
"""
import argparse
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone

AUDIT_NAME = "citation_audit.json"

# --- extraction regexes ------------------------------------------------------
_PMID_RE = re.compile(r"PMID[:\s#]*([0-9]{1,9})")
_NCT_RE = re.compile(r"\bNCT[0-9]{8}\b")
_NCT_BAD_RE = re.compile(r"\bNCT[0-9]{1,7}\b(?![0-9])")
_UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)
_SETID_CTX_RE = re.compile(
    r"(?:setid|dailymed)[^0-9a-fA-F]{0,40}?"
    r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
    re.IGNORECASE,
)
_URL_RE = re.compile(r"https?://[^\s)>\]]+")

# offline-validation shapes
_PMID_OK_RE = re.compile(r"^[0-9]{1,8}$")
_NCT_OK_RE = re.compile(r"^NCT[0-9]{8}$")
_UUID_OK_RE = re.compile(r"^" + _UUID_RE.pattern + r"$")


def _utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _dedupe(seq):
    """De-duplicate while preserving first-seen order."""
    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def extract_citations(text):
    """Pure, network-free. Return de-duplicated, order-preserved citation hits.

    Keys: pmid, nct, nct_malformed, dailymed_setid, url. The malformed NCT list
    (NCT + 1-7 digits) is surfaced separately so the audit can flag it.
    """
    text = text or ""
    return {
        "pmid": _dedupe(_PMID_RE.findall(text)),
        "nct": _dedupe(_NCT_RE.findall(text)),
        "nct_malformed": _dedupe(_NCT_BAD_RE.findall(text)),
        "dailymed_setid": _dedupe(
            m.group(1) for m in _SETID_CTX_RE.finditer(text)
        ),
        "url": _dedupe(_URL_RE.findall(text)),
    }


def classify_offline(citations):
    """Pure, network-free. Per citation: {type, value, format_ok, reason}."""
    out = []
    for value in citations.get("pmid", []):
        ok = bool(_PMID_OK_RE.match(value))
        out.append({
            "type": "pmid", "value": value, "format_ok": ok,
            "reason": "ok" if ok else "PMID should be 1-8 digits",
        })
    for value in citations.get("nct", []):
        ok = bool(_NCT_OK_RE.match(value))
        out.append({
            "type": "nct", "value": value, "format_ok": ok,
            "reason": "ok" if ok else "NCT must be NCT + exactly 8 digits",
        })
    for value in citations.get("nct_malformed", []):
        out.append({
            "type": "nct", "value": value, "format_ok": False,
            "reason": "NCT must be NCT + exactly 8 digits",
        })
    for value in citations.get("dailymed_setid", []):
        ok = bool(_UUID_OK_RE.match(value))
        out.append({
            "type": "dailymed_setid", "value": value, "format_ok": ok,
            "reason": "ok" if ok else "malformed UUID",
        })
    for value in citations.get("url", []):
        ok = bool(_URL_RE.match(value))
        out.append({
            "type": "url", "value": value, "format_ok": ok,
            "reason": "ok" if ok else "unparseable URL",
        })
    return out


def _http_ok(url, timeout):
    """GET url; return (status_code, body_text_or_None). Never raises."""
    req = urllib.request.Request(url, headers={"User-Agent": "citation-verify/1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", "replace")
        return resp.getcode(), body


def _verify_pmid(value, timeout):
    url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        f"?db=pubmed&id={value}&retmode=json"
    )
    code, body = _http_ok(url, timeout)
    if code != 200:
        return None, "unverified-network", f"HTTP {code}"
    try:
        data = json.loads(body)
    except ValueError:
        return None, "unverified-network", "non-JSON response"
    result = data.get("result", {})
    uids = result.get("uids", [])
    if value in uids and "error" not in result.get(value, {}):
        return True, "verified", "esummary returned record"
    return False, "not-found", "esummary returned no record"


def _verify_nct(value, timeout):
    url = f"https://clinicaltrials.gov/api/v2/studies/{value}"
    try:
        code, _ = _http_ok(url, timeout)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False, "not-found", "study not found (404)"
        raise
    if code == 200:
        return True, "verified", "study found"
    return None, "unverified-network", f"HTTP {code}"


def verify_online(citations, timeout=8):
    """Optional network check of PMID and NCT ids. Catches ALL network errors
    and returns status 'unverified-network' instead of raising."""
    out = []
    for value in citations.get("pmid", []):
        if not _PMID_OK_RE.match(value):
            out.append({"type": "pmid", "value": value, "exists": None,
                        "status": "bad-format", "detail": "skipped (bad format)"})
            continue
        try:
            exists, status, detail = _verify_pmid(value, timeout)
        except Exception as exc:  # noqa: BLE001 - degrade gracefully
            exists, status, detail = None, "unverified-network", str(exc)
        out.append({"type": "pmid", "value": value, "exists": exists,
                    "status": status, "detail": detail})
    for value in citations.get("nct", []):
        if not _NCT_OK_RE.match(value):
            out.append({"type": "nct", "value": value, "exists": None,
                        "status": "bad-format", "detail": "skipped (bad format)"})
            continue
        try:
            exists, status, detail = _verify_nct(value, timeout)
        except Exception as exc:  # noqa: BLE001 - degrade gracefully
            exists, status, detail = None, "unverified-network", str(exc)
        out.append({"type": "nct", "value": value, "exists": exists,
                    "status": status, "detail": detail})
    for value in citations.get("nct_malformed", []):
        out.append({"type": "nct", "value": value, "exists": None,
                    "status": "bad-format",
                    "detail": "NCT must be NCT + exactly 8 digits"})
    return out


def _path(workspace):
    return os.path.join(workspace, "verification", AUDIT_NAME)


def audit_files(paths, workspace="_workspace", online=False):
    """Audit each existing file: extract -> classify_offline (-> verify_online).

    Aggregates to a citation_audit/v1 dict and writes it to
    <workspace>/verification/citation_audit.json. Returns the dict.
    """
    files = []
    items = []
    total = 0
    format_fail = 0
    not_found = 0
    unverified_network = 0

    online_by_value = {}

    for path in paths:
        if not os.path.isfile(path):
            continue
        text = open(path, encoding="utf-8").read()
        cites = extract_citations(text)
        offline = classify_offline(cites)

        online_results = []
        if online:
            online_results = verify_online(cites)
            for r in online_results:
                online_by_value[(r["type"], r["value"])] = r

        file_total = len(offline)
        file_fail = sum(1 for r in offline if not r["format_ok"])
        total += file_total
        format_fail += file_fail

        for r in offline:
            entry = {
                "file": path,
                "type": r["type"],
                "value": r["value"],
                "format_ok": r["format_ok"],
                "reason": r["reason"],
            }
            if online:
                online_r = online_by_value.get((r["type"], r["value"]))
                if online_r is not None:
                    entry["online_status"] = online_r["status"]
                    entry["exists"] = online_r["exists"]
                    if online_r["status"] == "not-found":
                        not_found += 1
                    elif online_r["status"] == "unverified-network":
                        unverified_network += 1
            items.append(entry)

        files.append({
            "path": path,
            "counts": {
                k: len(v) for k, v in cites.items()
            },
            "format_fail": file_fail,
        })

    audit = {
        "schema": "citation_audit/v1",
        "generated_utc": _utc_now(),
        "online": bool(online),
        "files": files,
        "summary": {
            "total": total,
            "format_fail": format_fail,
            "not_found": not_found,
            "unverified_network": unverified_network,
        },
        "items": items,
    }

    out_path = _path(workspace)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return audit


def main():
    ap = argparse.ArgumentParser(description="Zero-trust citation verifier.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ext = sub.add_parser("extract")
    p_ext.add_argument("file")

    p_aud = sub.add_parser("audit")
    p_aud.add_argument("files", nargs="+")
    p_aud.add_argument("--workspace", default="_workspace")
    p_aud.add_argument("--online", action="store_true",
                       help="also resolve PMID/NCT against public registries")

    args = ap.parse_args()

    if args.cmd == "extract":
        text = open(args.file, encoding="utf-8").read()
        print(json.dumps(extract_citations(text), ensure_ascii=False, indent=2))
    elif args.cmd == "audit":
        audit = audit_files(args.files, workspace=args.workspace,
                            online=args.online)
        s = audit["summary"]
        print(
            f"citation audit ({'online' if audit['online'] else 'offline'}): "
            f"total={s['total']} format_fail={s['format_fail']} "
            f"not_found={s['not_found']} "
            f"unverified_network={s['unverified_network']} "
            f"-> {_path(args.workspace)}"
        )


if __name__ == "__main__":
    main()
