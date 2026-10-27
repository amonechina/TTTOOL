# skill-auditor

Due diligence for AI agent skills. Audit any SKILL.md package before you install it — in minutes, with an evidence-based verdict.

## What this skill does

"There are 4,000 SKILL.md files on GitHub. Maybe 100 are good. How do I find them?" This skill is the answer. It combines an automated scanner with a structured manual-review protocol and outputs a calibrated verdict: **install / install-with-caution / reject**.

The scanner checks (static analysis only — never executes the audited code):

- **Danger patterns**: eval/exec, download-then-execute chains, credential paths (`~/.ssh`, `.aws/credentials`, `.env`) combined with network calls (highest-suspicion pattern), base64 obfuscation, recursive deletes, hardcoded keys
- **Metadata quality**: missing/vague description, name/folder mismatch, TODO scaffolding residue
- **Maintenance**: stale files (12+ months without modification)
- **Context hygiene**: oversized SKILL.md, unusually large folders
- **Structure**: references to scripts/assets that don't exist

## When it activates

Use when a user asks "is this skill safe?", before installing any third-party skill, when evaluating marketplace listings, or when auditing your own skill repositories.

## Example output

Auditing a malicious skill planted for testing:

```
Audit report: fake-evil-skill
  verdict: reject   risk: high
  findings: 3 high / 5 medium / 0 low
  [MEDIUM] (metadata) description missing or placeholder
  [MEDIUM] (danger) process execution in scripts\run.py
  [HIGH  ] (danger) eval/exec call in scripts\run.py
  [HIGH  ] (danger) credential file path reference in SKILL.md
  [HIGH  ] (danger) network usage combined with credential references — highest suspicion pattern

Note: static analysis only. Findings inside .md files may be documentation
mentions — confirm intent manually before verdict.
```

Final verdicts follow a fixed template including *what evidence would change the verdict* — audits are falsifiable, not vibes.

## What's inside

| Path | Purpose |
|---|---|
| `SKILL.md` | Five-step audit workflow with calibrated verdict rules |
| `scripts/audit_skill.py` | Automated scanner (`--format text|json`) |
| `references/audit-criteria.md` | Complete finding taxonomy and severity definitions |
