#!/usr/bin/env python3
"""audit_skill.py — automated due-diligence scanner for SKILL.md packages.

Checks metadata quality, danger patterns, maintenance signals, context
hygiene, and structural integrity of a skill folder. Static analysis only:
never executes any bundled script.

Usage:
    python audit_skill.py <path-to-skill-folder> [--format text|json]

Exit codes: 0 = no high findings, 1 = findings (see report), 2 = usage error.
Findings severity: high / medium / low.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DANGER_PATTERNS: list[tuple[str, str, str]] = [
    # (regex, label, severity)
    (r"\b(?:curl|wget)\b", "shell download/fetch command", "medium"),
    (r"\bInvoke-WebRequest\b|\bStart-BitsTransfer\b", "PowerShell network fetch", "medium"),
    (r"\b(?:requests|urllib|httpx|aiohttp)\.", "Python HTTP client usage", "medium"),
    (r"\bchild_process\b|\baxios\b|\bfetch\(", "Node network/child process", "medium"),
    (r"\bsubprocess\b|\bos\.system\b|child_process\.exec", "process execution", "medium"),
    (r"(?<!\w)(?:eval|exec)\s*\(", "eval/exec call", "high"),
    (r"\brm\s+-[rf]{1,2}\b|\bshutil\.rmtree\b|\bdel\s+/[sS]\b", "recursive delete command", "medium"),
    (r"\.ssh|\.aws/credentials|\.netrc|\.gitconfig|\.env\b", "credential file path reference", "high"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "embedded private key", "high"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key literal", "high"),
    (r"[A-Za-z0-9+/=]{200,}", "long encoded blob (possible obfuscation)", "high"),
    (r"base64\.b64decode|atob\s*\(|FromBase64String", "base64 decoding", "medium"),
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
KEYVAL_RE = re.compile(r"^(\w[\w-]*):\s*(.+)$", re.M)
MAX_SKILL_MD_WORDS = 5000
STALE_DAYS = 365


class Report:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, severity: str, category: str, message: str) -> None:
        self.items.append({"severity": severity, "category": category, "message": message})

    def count(self, severity: str) -> int:
        return sum(1 for i in self.items if i["severity"] == severity)


def check_metadata(skill: Path, rep: Report) -> None:
    sm = skill / "SKILL.md"
    if not sm.exists():
        rep.add("high", "structure", "SKILL.md missing at skill root")
        return
    text = sm.read_text(encoding="utf-8", errors="replace")
    fm = FRONTMATTER_RE.match(text)
    if not fm:
        rep.add("high", "metadata", "no YAML frontmatter found in SKILL.md")
        meta = {}
    else:
        meta = dict(KEYVAL_RE.findall(fm.group(1)))
    name = meta.get("name", "").strip()
    if not name:
        rep.add("medium", "metadata", "frontmatter missing 'name'")
    elif name != skill.name:
        rep.add("medium", "metadata", f"name '{name}' does not match folder '{skill.name}'")
    desc = meta.get("description", "").strip()
    if not desc or "[TODO" in desc:
        rep.add("medium", "metadata", "description missing or placeholder")
    elif len(desc) < 60:
        rep.add("low", "metadata", "description very short — weak trigger signal for discovery")
    elif not re.search(r"when|use|trigger|用于|场景", desc, re.I):
        rep.add("low", "metadata", "description does not state when to use the skill")
    if "[TODO" in text:
        rep.add("medium", "maintenance", "SKILL.md still contains TODO/placeholder scaffolding")


def check_danger(skill: Path, rep: Report) -> None:
    for f in sorted(skill.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in {
            ".md", ".py", ".sh", ".ps1", ".js", ".ts", ".json", ".yaml", ".yml", ".txt", ".bat"
        }:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = f.relative_to(skill)
        for pattern, label, sev in DANGER_PATTERNS:
            if re.search(pattern, text):
                rep.add(sev, "danger", f"{label} in {rel}")
    # combination rule: network + credential in same skill
    joined = " ".join(
        f.read_text(encoding="utf-8", errors="replace") for f in skill.rglob("*")
        if f.is_file() and f.suffix.lower() in {".md", ".py", ".sh", ".js", ".ts"}
    ).lower()
    has_net = re.search(r"curl|wget|requests\.|urllib|httpx|fetch\(|axios|invoke-webrequest", joined)
    has_cred = re.search(r"\.ssh|\.aws/credentials|\.netrc|\.env\b|credentials", joined)
    if has_net and has_cred:
        rep.add("high", "danger", "network usage combined with credential references — highest suspicion pattern")


def check_maintenance(skill: Path, rep: Report) -> None:
    now = time.time()
    newest = 0.0
    for f in skill.rglob("*"):
        if f.is_file():
            try:
                newest = max(newest, f.stat().st_mtime)
            except OSError:
                pass
    if newest:
        days = (now - newest) / 86400
        if days > STALE_DAYS:
            rep.add("medium", "maintenance", f"no file modified in {int(days)} days (stale)")


def check_context(skill: Path, rep: Report) -> None:
    sm = skill / "SKILL.md"
    if sm.exists():
        words = len(sm.read_text(encoding="utf-8", errors="replace").split())
        if words > MAX_SKILL_MD_WORDS:
            rep.add("low", "context", f"SKILL.md is {words} words (> {MAX_SKILL_MD_WORDS}); move detail to references/")
    total = sum(f.stat().st_size for f in skill.rglob("*") if f.is_file())
    if total > 50 * 1024 * 1024:
        rep.add("medium", "context", f"skill folder is {total // (1024 * 1024)} MB — unusually large")


def check_structure(skill: Path, rep: Report) -> None:
    sm = skill / "SKILL.md"
    if not sm.exists():
        return
    text = sm.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"(?:scripts|assets|references)/([\w.\-/]+)", text):
        target = skill / m.group(0)
        if not target.exists():
            rep.add("medium", "structure", f"SKILL.md references missing path: {m.group(0)}")
    for d in ("scripts", "assets", "references"):
        dp = skill / d
        if dp.is_dir() and not any(dp.iterdir()):
            rep.add("low", "structure", f"empty directory: {d}/")


def audit(skill: Path) -> Report:
    rep = Report()
    if not skill.is_dir():
        rep.add("high", "structure", f"not a directory: {skill}")
        return rep
    check_metadata(skill, rep)
    check_danger(skill, rep)
    check_maintenance(skill, rep)
    check_context(skill, rep)
    check_structure(skill, rep)
    return rep


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit a SKILL.md package for quality and safety")
    ap.add_argument("skill", help="path to the skill folder")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    rep = audit(Path(args.skill))
    verdict = "install" if not rep.count("high") and not rep.count("medium") else (
        "install-with-caution" if not rep.count("high") else "reject"
    )
    risk = "high" if rep.count("high") else ("medium" if rep.count("medium") else "low")

    if args.format == "json":
        print(json.dumps({
            "verdict": verdict, "risk": risk,
            "counts": {s: rep.count(s) for s in ("high", "medium", "low")},
            "findings": rep.items,
            "audited_at": datetime.now(timezone.utc).isoformat(),
        }, indent=2, ensure_ascii=False))
    else:
        print(f"Audit report: {Path(args.skill).name}")
        print(f"  verdict: {verdict}   risk: {risk}")
        print(f"  findings: {rep.count('high')} high / {rep.count('medium')} medium / {rep.count('low')} low")
        for i in rep.items:
            print(f"  [{i['severity'].upper():6}] ({i['category']}) {i['message']}")
        if not rep.items:
            print("  no findings — proceed to manual review per SKILL.md Step 3")
        print("\nNote: static analysis only. Findings inside .md files may be documentation")
        print("mentions of these patterns (e.g. security guides) — confirm intent manually")
        print("before verdict. Complete the manual review and produce the final verdict block.")
    return 1 if rep.count("high") else 0


if __name__ == "__main__":
    sys.exit(main())
