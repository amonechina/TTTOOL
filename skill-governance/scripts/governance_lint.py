#!/usr/bin/env python3
"""governance_lint.py — validate the governance layer of a skill.

Checks:
  1. governance/permission-manifest.yaml exists and parses (or --yaml-less mode
     falls back to key-presence scan)
  2. Required manifest sections present: scope, destructive_operations,
     approval_gates, audit
  3. Every irreversible destructive operation has approval gate "manual"
  4. governance/rollback-plan.md exists and covers every declared operation
  5. SKILL.md contains a "## Governance" section
  6. Gate levels are valid: auto | confirm | manual

Usage:
    python governance_lint.py <path-to-skill-folder> [--strict]

Exit codes: 0 = pass, 1 = failures found, 2 = usage error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GATES = {"auto", "confirm", "manual"}
REQUIRED_SECTIONS = ["scope", "destructive_operations", "approval_gates", "audit"]


def warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")
    global failures
    failures += 1


failures = 0


def strip_yaml_comments(text: str) -> str:
    return "\n".join(
        line.split("#", 1)[0] if not line.lstrip().startswith("#") else ""
        for line in text.splitlines()
    )


def check_manifest(skill: Path, strict: bool) -> list[str]:
    """Return the list of destructive operation names found."""
    mf = skill / "governance" / "permission-manifest.yaml"
    if not mf.exists():
        fail("missing governance/permission-manifest.yaml")
        return []
    text = mf.read_text(encoding="utf-8", errors="replace")
    body = strip_yaml_comments(text)

    try:
        import yaml  # type: ignore
        data = yaml.safe_load(body) or {}
    except ImportError:
        data = None
        if strict:
            fail("PyYAML not installed; cannot fully parse manifest in --strict mode")
        else:
            warn("PyYAML not installed; falling back to key-presence checks")
    except Exception as exc:
        fail(f"permission-manifest.yaml does not parse: {exc}")
        return []

    operations: list[str] = []
    if data is not None:
        for section in REQUIRED_SECTIONS:
            if section not in data:
                fail(f"manifest missing required section: {section}")
        for op in data.get("destructive_operations") or []:
            if isinstance(op, dict) and op.get("operation"):
                name = str(op["operation"])
                operations.append(name)
                gate = str(op.get("approval_gates", "")).strip().lower()
                if gate not in GATES:
                    fail(f"operation '{name}': invalid gate level '{gate or '(empty)'}' (use auto|confirm|manual)")
                elif str(op.get("reversible", "")).lower() == "false" and gate != "manual":
                    fail(f"operation '{name}' is irreversible but gate is '{gate}' — must be 'manual'")
                elif not str(op.get("rollback", "")).strip():
                    warn(f"operation '{name}' has no rollback reference")
        creds = data.get("credentials") or []
        for c in creds:
            if isinstance(c, dict) and c.get("name") and not c.get("source"):
                fail(f"credential '{c['name']}' has no declared source")
    else:
        for section in REQUIRED_SECTIONS:
            if not re.search(rf"^\s*{section}\s*:", body, re.M):
                fail(f"manifest missing required section: {section}")
        operations = re.findall(r"^\s*-?\s*operation:\s*(\S+)", body, re.M)

    # placeholder scan: empty string values or template markers left unfilled
    unfilled = re.findall(r':\s*(?:""\s*$|""\s+#)', text, re.M)
    if unfilled:
        warn(f"{len(unfilled)} placeholder value(s) still empty — manifest not filled in")
    if "<skill_name>" in text or "e.g." in text:
        warn("manifest still contains template placeholder text (e.g. '<skill_name>', 'e.g.')")
    return operations


def check_rollback(skill: Path, operations: list[str]) -> None:
    rp = skill / "governance" / "rollback-plan.md"
    if not rp.exists():
        fail("missing governance/rollback-plan.md")
        return
    text = rp.read_text(encoding="utf-8", errors="replace")
    if "<skill_name>" in text or "<operation name>" in text:
        warn("rollback plan still contains template placeholders")
    for op in operations:
        if op not in text:
            fail(f"rollback plan does not mention declared operation: {op}")


def check_skill_md(skill: Path) -> None:
    sm = skill / "SKILL.md"
    if not sm.exists():
        fail("missing SKILL.md")
        return
    text = sm.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"^##\s+Governance\b", text, re.M):
        fail("SKILL.md has no '## Governance' section (Step 4 of the wrapper)")
    if not re.search(r"permission-manifest", text):
        warn("SKILL.md governance section does not reference the permission manifest")


def main() -> int:
    global failures
    ap = argparse.ArgumentParser(description="Lint the governance layer of a skill")
    ap.add_argument("skill", help="path to the skill folder")
    ap.add_argument("--strict", action="store_true", help="treat missing PyYAML as failure")
    args = ap.parse_args()

    skill = Path(args.skill)
    if not skill.is_dir():
        print(f"error: not a directory: {skill}")
        return 2

    print(f"Governance lint: {skill.name}")
    operations = check_manifest(skill, args.strict)
    check_rollback(skill, operations)
    check_skill_md(skill)

    if failures:
        print(f"\nRESULT: FAIL — {failures} issue(s). Fix before production use.")
        return 1
    print("\nRESULT: PASS — governance layer complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
