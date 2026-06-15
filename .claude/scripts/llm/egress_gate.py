#!/usr/bin/env python3
"""Fail-closed data-egress gate for the Multi-LLM pipeline (host-agnostic).

Before any text is sent to an external (non-host) LLM, this gate classifies the
content by sensitivity and decides whether the target provider is permitted.
Vendor names are never hard-coded: the policy uses ``"host"`` (the current
orchestrator provider, passed in) and ``"*"`` (any verified provider). With
``fail_closed`` true, anything unclassifiable is blocked.

Classification precedence (most → least restrictive):
    SAFETY_CRITICAL > SPONSOR_CONFIDENTIAL > REGULATORY_PUBLIC > PUBLIC
If no marker matches, the policy's ``default_classification`` applies
(SPONSOR_CONFIDENTIAL — conservative).

Usage
-----
    egress_gate.py --provider openai --host anthropic \
        [--file f ...] [--text "..."] [--policy <path>]

Prints the decision as JSON; exit 0 if allowed, exit 3 if blocked.
"""
import argparse
import json
import os
import sys

DEFAULT_POLICY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))),
    "references", "llm", "egress_policy.json",
)

# Most → least restrictive. classify() walks this order and returns the first
# classification whose markers appear in the text.
PRECEDENCE = [
    "SAFETY_CRITICAL",
    "SPONSOR_CONFIDENTIAL",
    "REGULATORY_PUBLIC",
    "PUBLIC",
]


# Severity ranking (higher = more restrictive). Used to combine a caller-declared
# floor with marker-detected classification: the effective class is the MORE
# restrictive of the two (declared can never loosen what markers detect).
SEVERITY = {"PUBLIC": 0, "REGULATORY_PUBLIC": 1, "SPONSOR_CONFIDENTIAL": 2, "SAFETY_CRITICAL": 3}


def detect(text, policy):
    """Return the most-restrictive classification whose markers appear in text,
    or None if no marker matches."""
    haystack = (text or "").lower()
    markers = policy.get("markers", {})
    for cls in PRECEDENCE:
        for marker in markers.get(cls, []):
            if marker.lower() in haystack:
                return cls
    return None


def classify(text, policy, declared=None):
    """Effective classification = most-restrictive of (caller-declared floor,
    marker-detected). When neither is set, fall back to the policy default
    (SPONSOR_CONFIDENTIAL — conservative / fail-closed).

    A caller may DECLARE a less-restrictive floor (e.g. REGULATORY_PUBLIC for an
    approved-drug study) to enable cross-vendor egress, but markers can only
    ESCALATE — declaring PUBLIC on text containing 'NOAEL' still yields
    SAFETY_CRITICAL. Declaring nothing keeps the conservative default."""
    detected = detect(text, policy)
    default = policy.get("default_classification", "SPONSOR_CONFIDENTIAL")
    floor = declared if declared in SEVERITY else default
    if detected is None:
        return floor
    return floor if SEVERITY[floor] >= SEVERITY[detected] else detected


def allowed(provider, classification, policy, host):
    """Resolve allowed_providers for a classification against (provider, host).

    "*" -> any provider; "host" -> provider must equal host; a literal provider
    key -> exact match. Unknown classification + fail_closed -> False.
    """
    classes = policy.get("classifications", {})
    spec = classes.get(classification)
    if spec is None:
        # Unknown classification: blocked when fail_closed, else permissive.
        return not policy.get("fail_closed", True)
    for entry in spec.get("allowed_providers", []):
        if entry == "*":
            return True
        if entry == "host":
            if provider == host:
                return True
        elif entry == provider:
            return True
    return False


def _reason(classification, provider, host, is_allowed, known):
    if not known:
        return (f"classification {classification!r} not defined in policy; "
                f"fail-closed blocks egress")
    if is_allowed:
        return (f"{classification} permits provider {provider!r} "
                f"(host={host!r})")
    return (f"{classification} does not permit provider {provider!r} "
            f"(host={host!r})")


def check(provider, text, policy, host, declared=None):
    """Classify text (with optional caller-declared floor) and decide egress."""
    classification = classify(text, policy, declared=declared)
    known = classification in policy.get("classifications", {})
    is_allowed = allowed(provider, classification, policy, host)
    return {
        "provider": provider,
        "host": host,
        "declared": declared,
        "classification": classification,
        "allowed": is_allowed,
        "reason": _reason(classification, provider, host, is_allowed, known),
    }


def check_files(provider, paths, policy, host, declared=None):
    """Classify the concatenation of files (most-restrictive wins) and decide."""
    chunks = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            chunks.append(f.read())
    result = check(provider, "\n".join(chunks), policy, host, declared=declared)
    result["files"] = list(paths)
    return result


def _load_policy(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(
        description="Fail-closed data-egress gate (host-agnostic).")
    ap.add_argument("--provider", required=True)
    ap.add_argument("--host", required=True)
    ap.add_argument("--file", action="append", default=[],
                    help="file(s) to classify; repeatable")
    ap.add_argument("--text", default=None, help="inline text to classify")
    ap.add_argument("--classification", default=None,
                    choices=list(SEVERITY.keys()),
                    help="caller-declared floor (markers can only escalate)")
    ap.add_argument("--policy", default=DEFAULT_POLICY)
    args = ap.parse_args()

    policy = _load_policy(args.policy)

    if args.file:
        result = check_files(args.provider, args.file, policy, args.host,
                             declared=args.classification)
    else:
        result = check(args.provider, args.text or "", policy, args.host,
                       declared=args.classification)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["allowed"] else 3)


if __name__ == "__main__":
    main()
