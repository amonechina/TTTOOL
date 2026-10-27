# skill-compat-checker

Ship skills that behave the same everywhere. Static cross-platform compatibility checks with concrete fixes.

## What this skill does

Platform-divergent agent behaviors are documented nowhere and discovered painfully in production. This skill encodes the six known pitfalls as automated static checks, each finding paired with a fix:

| ID | Pitfall | Detected |
|---|---|---|
| P1 | Relative/personal paths into `references/` fail to resolve | `../` paths, absolute user paths |
| P2 | `Write` (silent overwrite) vs `create_file` (refuses overwrite) divergence | file-writing skills with no platform guidance |
| P3 | ask-user tool silently compacts requests beyond 3 questions / 4 options | oversized ask requests |
| P4 | Referencing a missing tool silently degrades to prose | tool references without fallback clauses |
| P5 | POSIX-only shell syntax breaks Windows runtimes | heredocs, pipe utilities, `/dev/null` redirects |
| P6 | Vague descriptions never trigger on description-matching platforms | short/generic frontmatter |

## When it activates

Use before publishing or installing any skill, when a skill behaves differently across platforms, or when a user reports "works on one platform, breaks on another".

## Example output

Scanning a skill planted with five compatibility problems:

```
[P1] SKILL.md:5
    relative '../' or absolute personal path — resource paths must resolve
    from the skill's own directory
    FIX: instruct loading 'from this skill's directory' + filename
[P2] SKILL.md
    skill writes files but gives no platform guidance (Write vs create_file
    diverge silently)
    FIX: add a platform note stating both behaviors
[P3] SKILL.md:6
    ask request may exceed tool limits (max 3 questions / 4 options)
    FIX: split input gathering into rounds
[P4] SKILL.md
    tool 'web_search' referenced without a fallback clause
    FIX: add 'If unavailable, stop and tell the user — do not substitute'
[P6] SKILL.md
    description too vague — weak trigger signal across platforms
    FIX: state what the skill does AND when to use it

5 finding(s). Apply fixes from references/pitfalls.md, re-scan, then
smoke-test on 2+ platforms.
```

## What's inside

| Path | Purpose |
|---|---|
| `SKILL.md` | Scan → fix → re-scan → smoke-test → ship-with-compat-note workflow |
| `scripts/compat_scan.py` | Static scanner P1–P6 (`--format text|json`) |
| `references/pitfalls.md` | Full catalog: broken vs fixed instruction text for every pitfall |
