---
name: skill-compat-checker
description: Statically checks an agent skill for known cross-platform compatibility pitfalls before it is shipped or installed. Detects platform-divergent file APIs (Write vs create_file), broken relative paths in references/, ask-user-input limits (max 3 questions / 4 options), silent fallback risks when referenced tools may not exist, and platform-specific assumptions, then generates concrete adaptation suggestions. This skill should be used when creating or editing a skill and before publishing it, when a skill behaves differently on different agent platforms, or when the user reports "this skill works on one platform but not another".
---

# Skill Compat Checker

Platform differences in agent runtimes are documented nowhere and discovered painfully. This skill encodes the known pitfalls as static checks so a skill can be fixed before it ships.

## Known Pitfalls (the check catalog)

| ID | Pitfall | Why it breaks |
|----|---------|---------------|
| P1 | Relative paths pointing into `references/`, `scripts/`, `assets/` | Relative paths from the skill's own directory do not resolve on most platforms — use paths relative to the SKILL.md location only when the platform documents it, otherwise instruct loading by skill base directory |
| P2 | `Write`/`create_file` divergence | Write silently overwrites on code/desktop runtimes; `create_file` refuses to overwrite on web runtimes. Skills must state which to use per platform or use a platform check |
| P3 | `ask_user_input` limits | Max 3 questions, 4 options each; requests beyond that are silently compacted with no error. Skills needing more input must split into multiple rounds |
| P4 | Missing-tool silent fallback | Referencing a tool that does not exist on the running platform degrades to prose without warning — the skill appears to work while skipping steps |
| P5 | Shell assumptions | Bash-only syntax (pipes, heredocs, `$VAR`) breaks on Windows runtimes; PowerShell-only cmdlets break elsewhere |
| P6 | Frontmatter drift | Missing or vague `description` makes the skill unreachable on platforms that match skills by description only |

## Workflow

### Step 1: Run the Static Scan

```bash
python scripts/compat_scan.py <path-to-skill-folder> [--format text|json]
```

The scanner emits one finding per pitfall hit, with file, line, and a suggested fix. Exit code 0 = no findings.

### Step 2: Apply Fixes

For each finding, apply the adaptation from `references/pitfalls.md`:

- **P1** — resolve resource paths at instruction time: prefer telling the agent to load files "from this skill's directory" plus the exact filename; never `../` or absolute personal paths.
- **P2** — add a platform note in SKILL.md: "On runtimes with `Write`, use Write (overwrites). On web runtimes use `create_file` and check existence first."
- **P3** — split input gathering into rounds of ≤ 3 questions with ≤ 4 options; state the round structure explicitly.
- **P4** — for every tool referenced in instructions, add a fallback clause: "If tool X is unavailable, state that the step cannot be completed rather than approximating." Prefer prose checks over silent degradation.
- **P5** — write commands in a runtime-neutral way or branch: detect shell, or provide both variants.
- **P6** — rewrite `description` to third person, naming what it does and concrete triggers.

### Step 3: Re-Scan and Confirm

Run the scanner again; all findings must clear. Then do a live smoke test on at least two target platforms if available: trigger the skill once and verify every step executed (no silent fallbacks — compare actions taken against the instruction list).

### Step 4: Ship with a Compatibility Note

Add a short `## Compatibility` section to SKILL.md listing tested platforms and any known limitations. Unstated limitations get rediscovered by every user, in production.

## References

- `references/pitfalls.md` — full pitfall catalog with examples of broken and fixed instruction text

## Scripts

- `scripts/compat_scan.py` — static scanner implementing checks P1–P6
