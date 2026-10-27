#!/usr/bin/env python3
"""geo_scan.py — static GEO (Generative Engine Optimization) content scanner.

Scores text files for markers of content engineered to be cited by AI engines:
superlative saturation, affiliate plumbing, astroturf phrasing, PR laundering,
unverifiable statistics, and LLM-seeding fingerprints.

Usage:
    python geo_scan.py <file-or-directory> [--threshold-geo N] [--threshold-suspect N]

Exit codes:
    0 = clean (within thresholds)
    1 = suspect (at/above suspect threshold)
    2 = likely GEO (at/above geo threshold)

This is a heuristic triage tool, not a verdict. Every finding carries the
matched signal and line number for manual verification (see SKILL.md Step 2).
"""
from __future__ import annotations

import argparse
import os
import re
import sys

# ---------------------------------------------------------------- signals ---
# (signal_id, compiled_regex, weight, label)

SUPERLATIVES = re.compile(
    r"\b(best|top|leading|premier|world[- ]class|cutting[- ]edge|"
    r"revolutionary|game[- ]chang\w+|next[- ]generation|unparalleled|"
    r"#1|number one)\b",
    re.I,
)

AFFILIATE = re.compile(
    r"(amzn\.to|/go/|/ref/|/out/|[?&](tag|affiliate|aff)=|utm_content=affiliate|"
    r"earn(s)? a commission|affiliate (link|partner)|sponsored (post|content)|"
    r"advertiser disclosure)",
    re.I,
)

ASTROTURF = re.compile(
    r"(i'?ve been using \w+ (for|since)|total game[- ]changer|"
    r"absolute(ly)? (love|adore)|life[- ]?saver|blown away|"
    r"changed my (life|workflow)|never going back)",
    re.I,
)

PR_LAUNDER = re.compile(
    r"(proud(ly)? to announce|delighted to announce|press release|"
    r"new (survey|report|study) (finds|shows|reveals)|"
    r"according to a new (report|study)|"
    r"prnewswire|businesswire|globenewswire)",
    re.I,
)

UNVERIFIED_STATS = re.compile(
    r"\b(\d{2,3}(\.\d)?%|(\d+(\.\d)?)[ -]?x (faster|better|more))\b"
    r"[^.]{0,80}\b(teams|users|companies|enterprises|marketers|businesses)\b",
    re.I,
)

SEEDING_FINGERPRINT = re.compile(
    r"(what (is|are) the best|which \w+ is (best|right for you)|"
    r"tl;dr|frequently asked questions|faqs?\b|"
    r"as featured in|recommended by (ai|leading)|"
    r"in (this|our) (guide|roundup|review), we)",
    re.I,
)

BUY_CTA = re.compile(
    r"\b(buy now|get started (free|today)|sign up (now|today|free)|"
    r"claim your (discount|trial)|limited[- ]time offer|free trial)\b",
    re.I,
)

SIGNALS = [
    ("G1", SUPERLATIVES, 3, "Superlative saturation"),
    ("G2", AFFILIATE, 12, "Affiliate / sponsored plumbing"),
    ("G3", ASTROTURF, 8, "Astroturf review phrasing"),
    ("G4", PR_LAUNDER, 8, "Press-release laundering language"),
    ("G5", UNVERIFIED_STATS, 8, "Statistic without visible provenance"),
    ("G6", SEEDING_FINGERPRINT, 5, "LLM-seeding fingerprint"),
    ("G7", BUY_CTA, 6, "Commercial call-to-action"),
]

TEXT_EXTS = {".md", ".txt", ".html", ".htm", ".markdown", ".rst", ".csv", ".json"}


def scan_text(text: str):
    """Yield (signal_id, line_no, weight, label, snippet) for every match."""
    lines = text.splitlines()
    for sid, rx, weight, label in SIGNALS:
        for m in rx.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            snippet = lines[line_no - 1].strip()
            if len(snippet) > 100:
                snippet = snippet[:97] + "..."
            yield sid, line_no, weight, label, snippet


def scan_file(path: str, geo_threshold: int, suspect_threshold: int) -> int:
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    words = max(len(text.split()), 1)
    # density normalization: per 500 words, capped so huge docs aren't auto-flagged
    density_factor = min(max(words / 500.0, 1.0), 3.0)

    findings = list(scan_text(text))
    raw_score = sum(w for _, _, w, _, _ in findings)
    score = min(int(round(raw_score / density_factor)), 100)

    # per-signal hit counts for the summary
    counts = {}
    for sid, _, _, _, _ in findings:
        counts[sid] = counts.get(sid, 0) + 1

    print(f"\n== {path}")
    print(f"   words: {words}  |  signals: {len(findings)}  |  GEO score: {score}/100")

    if not findings:
        print("   CLEAN — no GEO markers found")
        return 0

    for sid, line_no, _, label, snippet in findings[:15]:
        print(f"   [{sid}] L{line_no:<5} {label}: {snippet}")
    shown = len(findings)
    if shown > 15:
        print(f"   … +{shown - 15} more findings")
    print("   breakdown:", ", ".join(f"{s}×{c}" for s, c in sorted(counts.items())))

    if score >= geo_threshold:
        print("   VERDICT: LIKELY GEO — exclude from evidence (SKILL.md Step 3)")
        return 2
    if score >= suspect_threshold:
        print("   VERDICT: SUSPECT — treat as T3/T4, discount or corroborate")
        return 1
    print("   VERDICT: LOW RISK — manual spot-check advised")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="GEO content scanner")
    ap.add_argument("target", help="file or directory to scan")
    ap.add_argument("--threshold-geo", type=int, default=50)
    ap.add_argument("--threshold-suspect", type=int, default=20)
    args = ap.parse_args()

    if os.path.isfile(args.target):
        targets = [args.target]
    elif os.path.isdir(args.target):
        targets = [
            os.path.join(r, fn)
            for r, _, fns in os.walk(args.target)
            for fn in fns
            if os.path.splitext(fn)[1].lower() in TEXT_EXTS
        ]
    else:
        print(f"error: {args.target} not found", file=sys.stderr)
        return 2

    worst = 0
    for t in sorted(targets):
        worst = max(worst, scan_file(t, args.threshold_geo, args.threshold_suspect))

    print("\nSummary: " + {0: "all clean", 1: "suspect content present — discount", 2: "GEO content present — exclude"}[worst])
    return worst


if __name__ == "__main__":
    sys.exit(main())
