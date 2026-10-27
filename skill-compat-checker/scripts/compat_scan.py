#!/usr/bin/env python3
"""compat_scan.py — static cross-platform compatibility scanner for skills.

Implements checks P1-P6 (see references/pitfalls.md):

  P1  relative/absolute personal paths into skill resources
  P2  file-write API usage without platform guidance
  P3  ask_user_input requests exceeding 3 questions / 4 options
  P4  tool references without a fallback clause
  P5  shell-specific syntax without a cross-platform alternative
  P6  vague or missing frontmatter description

Usage:
    python compat_scan.py <path-to-skill-folder> [--format text|json]

Exit codes: 0 = no findings, 1 = findings, 2 = usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

TOOL_NAMES = [
    "web_search", "web_fetch", "browser", "image_gen", "video_gen",
    "audio_transcribe", "library_search", "conversation_search",
]

SHELLisms = [
    (r"(?m)^\s*\w[\w.-]*\s*>>?\s*/(dev|null)/", "POSIX null-device redirect"),
    (r"\|\s*awk|\|\s*sed\s|grep\s+-", "POSIX pipe utilities"),
    (r"<<\s*'?EOF", "heredoc (<<EOF)"),
    (r"\$\{?[A-Z_][A-Z0-9_]*\}?", "POSIX variable expansion"),
    (r"&&\s|\|\|\s", "shell chaining operators"),
]

CODE_EXTENSIONS = {".md", ".py", ".sh", ".ps1", ".js", ".ts"}


def find_text_files(skill: Path) -> list[Path]:
    return sorted(
        f for f in skill.rglob("*")
        if f.is_file() and f.suffix.lower() in CODE_EXTENSIONS
    )


def check_p1_paths(skill: Path, findings: list[dict]) -> None:
    for f in find_text_files(skill):
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if re.search(r"\.\./", line) or re.search(r"[A-Za-z]:[/\\]Users[/\\]", line):
                findings.append({
                    "id": "P1", "file": str(f.relative_to(skill)), "line": i,
                    "message": "relative '../' or absolute personal path — resource paths must resolve from the skill's own directory",
                    "fix": "instruct loading 'from this skill's directory' + filename; drop ../ and personal absolute paths",
                })


def check_p2_write(skill: Path, findings: list[dict]) -> None:
    sm = skill / "SKILL.md"
    if not sm.exists():
        return
    text = sm.read_text(encoding="utf-8", errors="replace")
    mentions_writing = re.search(r"(?i)\b(create|write|save|generate)\b.{0,40}\b(file|document|report|output)", text)
    if not mentions_writing:
        return
    if "create_file" not in text and "Write" not in text:
        findings.append({
            "id": "P2", "file": "SKILL.md", "line": 0,
            "message": "skill writes files but gives no platform guidance (Write vs create_file diverge silently)",
            "fix": "add a platform note: Write overwrites on code/desktop; create_file refuses overwrite on web — state both",
        })


def check_p3_ask(skill: Path, findings: list[dict]) -> None:
    for f in find_text_files(skill):
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"(?is)ask(?:_user_input)?[^.\n]*(?:question|option)", text):
            seg = m.group(0)
            nums = [int(n) for n in re.findall(r"\b(\d+)\b", seg)]
            if any(n > 4 for n in nums) or any(n > 3 for n in nums if "question" in seg):
                findings.append({
                    "id": "P3", "file": str(f.relative_to(skill)), "line": text[:m.start()].count("\n") + 1,
                    "message": "ask request may exceed tool limits (max 3 questions / 4 options) — silent compaction risk",
                    "fix": "split input gathering into rounds of <= 3 questions with <= 4 options each",
                })


def check_p4_tools(skill: Path, findings: list[dict]) -> None:
    sm = skill / "SKILL.md"
    if not sm.exists():
        return
    text = sm.read_text(encoding="utf-8", errors="replace")
    for tool in TOOL_NAMES:
        if re.search(rf"\b{tool}\b", text, re.I):
            window = text.lower()
            near = re.search(
                rf"{tool}.{{0,400}}?(unavailable|fallback|not available|do not substitute|不可用)", window, re.S
            )
            if not near:
                findings.append({
                    "id": "P4", "file": "SKILL.md", "line": 0,
                    "message": f"tool '{tool}' referenced without a fallback clause — silent-degradation risk if the platform lacks it",
                    "fix": "add: 'If <tool> is unavailable, stop and tell the user — do not substitute an answer from memory'",
                })


def check_p5_shell(skill: Path, findings: list[dict]) -> None:
    for f in find_text_files(skill):
        if f.suffix == ".py":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        for pattern, label in SHELLisms:
            for m in re.finditer(pattern, text):
                findings.append({
                    "id": "P5", "file": str(f.relative_to(skill)), "line": text[:m.start()].count("\n") + 1,
                    "message": f"POSIX-specific shell syntax ({label}) without a stated cross-platform alternative",
                    "fix": "provide both bash and PowerShell variants, or prefer a runtime-neutral command",
                })
                break  # one finding per pattern per file


def check_p6_frontmatter(skill: Path, findings: list[dict]) -> None:
    sm = skill / "SKILL.md"
    if not sm.exists():
        findings.append({
            "id": "P6", "file": "SKILL.md", "line": 0,
            "message": "SKILL.md missing", "fix": "create SKILL.md with name/description frontmatter",
        })
        return
    text = sm.read_text(encoding="utf-8", errors="replace")
    fm = FRONTMATTER_RE.match(text)
    desc = ""
    if fm:
        m = re.search(r"^description:\s*(.+?)(?=^\w[\w-]*:|\Z)", fm.group(1), re.M | re.S)
        desc = (m.group(1) if m else "").strip()
    if not desc:
        findings.append({
            "id": "P6", "file": "SKILL.md", "line": 0,
            "message": "missing or empty description — description-based skill matching will never trigger",
            "fix": "write a third-person description naming the task and concrete trigger phrases",
        })
    elif len(desc) < 60 or not re.search(r"(?i)when|use|trigger|用于|场景", desc):
        findings.append({
            "id": "P6", "file": "SKILL.md", "line": 0,
            "message": "description too vague — weak trigger signal across platforms",
            "fix": "state what the skill does AND when to use it, with concrete user phrases",
        })


def main() -> int:
    ap = argparse.ArgumentParser(description="Static cross-platform compatibility scan for a skill")
    ap.add_argument("skill", help="path to the skill folder")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    skill = Path(args.skill)
    if not skill.is_dir():
        print(f"error: not a directory: {skill}")
        return 2

    findings: list[dict] = []
    check_p1_paths(skill, findings)
    check_p2_write(skill, findings)
    check_p3_ask(skill, findings)
    check_p4_tools(skill, findings)
    check_p5_shell(skill, findings)
    check_p6_frontmatter(skill, findings)
    findings.sort(key=lambda x: (x["id"], x["file"], x.get("line", 0)))

    if args.format == "json":
        print(json.dumps({"findings": findings}, indent=2, ensure_ascii=False))
    else:
        if not findings:
            print("✅ no compatibility findings")
        for f in findings:
            loc = f"{f['file']}:{f.get('line', 0)}" if f.get("line") else f["file"]
            print(f"[{f['id']}] {loc}\n    {f['message']}\n    FIX: {f['fix']}")
        print(f"\n{len(findings)} finding(s). Apply fixes from references/pitfalls.md, re-scan, then smoke-test on 2+ platforms.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
