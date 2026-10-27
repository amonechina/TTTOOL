#!/usr/bin/env python3
"""package_review.py — transferability checker for generated skills.

Verifies a skill produced by the interview-to-package pipeline can be run
by someone WITHOUT the author present. Checks:

  T1  author-dependent phrases ("as I mentioned", "ask me", "my usual", etc.)
  T2  personal absolute paths (C:/Users/<name>, /Users/<name>, D:/personal dirs)
  T3  missing worked example section
  T4  missing refusal/escalation section
  T5  judgment left as prose ("use your judgment") instead of decision tables
  T6  undefined jargon candidates (all-caps abbreviations without expansion)
  T7  metadata quality (frontmatter name/description, trigger phrases)

Static analysis only. Exit 0 = no high findings.

Usage:
    python package_review.py <skill-folder> [--format text|json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AUTHOR_PHRASES = [
    r"as I (?:mentioned|said|told)", r"ask (?:me|myself)",
    r"my usual (?:approach|method|way)", r"in my (?:opinion|experience)[,\.]",
    r"(?i)问我|按我平时|像我一样",
    r"contact (?:me|the author) (?:if|for|when)",
    r"ping me", r"refer to (?:my|the author's) notes",
]
PERSONAL_PATHS = [
    r"[A-Za-z]:[/\\]Users[/\\][^/\s\"']+", r"/Users/[^/\s\"']+",
    r"[A-Za-z]:[/\\](?:Documents|Desktop|Downloads)[/\\]",
]
JUDGMENT_PROSE = [
    r"use your (?:judgment|discretion|best judgment)",
    r"as (?:you see )?fit", r"灵活处理", r"自行判断", r"酌情",
]
EXAMPLE_HEADERS = ["example", "worked example", "示例", "范例", "样例"]
REFUSAL_HEADERS = [
    "refusal", "do not", "escalat", "reject", "stop when",
    "拒绝", "不适用", "上报", "退回",
]
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
CODE_EXTENSIONS = {".md", ".py", ".sh", ".js", ".ts", ".yaml", ".yml"}


def findings_for(skill: Path) -> list[dict]:
    out: list[dict] = []
    sm = skill / "SKILL.md"
    if not sm.exists():
        out.append({"id": "T7", "severity": "high", "message": "SKILL.md missing"})
        return out
    text = sm.read_text(encoding="utf-8", errors="replace")
    low = text.lower()

    # T7 metadata
    fm = FRONTMATTER_RE.match(text)
    desc = ""
    if fm:
        m = re.search(r"^description:\s*(.+?)(?=^\w[\w-]*:|\Z)", fm.group(1), re.M | re.S)
        desc = (m.group(1) if m else "").strip()
    if not desc:
        out.append({"id": "T7", "severity": "high", "message": "missing frontmatter description"})
    elif len(desc) < 60:
        out.append({"id": "T7", "severity": "medium", "message": "description too short to trigger discovery"})
    if "[TODO" in text:
        out.append({"id": "T7", "severity": "high", "message": "unfilled TODO scaffolding in SKILL.md"})

    all_text = text
    for f in skill.rglob("*"):
        if f.is_file() and f.suffix.lower() in CODE_EXTENSIONS and f != sm:
            try:
                all_text += "\n" + f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass

    # T1 author dependence
    for pat in AUTHOR_PHRASES:
        for m in re.finditer(pat, all_text, re.I):
            out.append({"id": "T1", "severity": "high",
                        "message": f"author-dependent phrase: …{all_text[max(0,m.start()-20):m.end()+20]!r}…"})

    # T2 personal paths
    for pat in PERSONAL_PATHS:
        for m in re.finditer(pat, all_text):
            out.append({"id": "T2", "severity": "medium",
                        "message": f"machine-specific path: {m.group(0)!r} — replace with skill-relative references"})

    # T3 worked example
    if not any(h in low for h in EXAMPLE_HEADERS):
        out.append({"id": "T3", "severity": "high",
                    "message": "no worked example section — runners cannot see the quality bar"})

    # T4 refusals
    if not any(h in low for h in REFUSAL_HEADERS):
        out.append({"id": "T4", "severity": "high",
                    "message": "no refusal/escalation section — skill will run where the expert would have stopped"})

    # T5 judgment prose
    for pat in JUDGMENT_PROSE:
        for m in re.finditer(pat, all_text, re.I):
            out.append({"id": "T5", "severity": "medium",
                        "message": f"unoperationalized judgment: {m.group(0)!r} — convert to a decision table or log as known limitation"})

    # T6 undefined abbreviations
    body_no_headers = re.sub(r"^#+ .*$", "", text, flags=re.M)
    for m in re.finditer(r"\b[A-Z]{2,6}\b", body_no_headers):
        abbr = m.group(0)
        if abbr in {"SKILL", "API", "YAML", "JSON", "TODO", "README", "II", "III", "IV", "AI"}:
            continue
        if abbr not in re.findall(rf"{abbr}\s*\(", text) and f"({abbr}" not in text and f"{abbr} (" not in text:
            out.append({"id": "T6", "severity": "low",
                        "message": f"abbreviation {abbr!r} used without expansion — new hires may not know it"})
            break  # one representative finding

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Check a generated skill is author-independent")
    ap.add_argument("skill", help="path to the generated skill folder")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    skill = Path(args.skill)
    if not skill.is_dir():
        print(f"error: not a directory: {skill}")
        return 2

    findings = findings_for(skill)
    highs = [f for f in findings if f["severity"] == "high"]
    verdict = "SHIP" if not highs else "REVISE"

    if args.format == "json":
        print(json.dumps({"verdict": verdict, "findings": findings}, indent=2, ensure_ascii=False))
    else:
        print(f"Transferability review: {skill.name}  →  {verdict}")
        for f in findings:
            print(f"  [{f['severity'].upper():6}] {f['id']}  {f['message']}")
        if not findings:
            print("  clean — proceed to the live test with a non-author runner")
        print("\nReminder: the live test (non-author runs it, expert grades) is still required before distribution.")
    return 1 if highs else 0


if __name__ == "__main__":
    sys.exit(main())
