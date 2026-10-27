# skill-governance

Add a trust wrapper to any agent skill or automated workflow: permission manifest, approval gates, failure recovery, rollback procedure, and audit logging.

## What this skill does

Turns "a clever prompt" into an operational package a team can trust. It produces, for any target skill:

- A **permission manifest** (YAML) declaring exactly what the skill may touch — deny by default
- **Approval gates** at three levels: `auto` (reads), `confirm` (in-scope writes), `manual` (irreversible/external/production — no exceptions)
- A **rollback plan** naming the pre-state capture, failure signals, and exact recovery steps for every destructive operation
- **Audit log hooks** — evidence lines before and after every gated operation; headless runs refuse to start if the previous run ended unresolved
- A plain-language **governance contract** section for the skill's own SKILL.md

## When it activates

Use when a skill writes/deletes files, calls external APIs, uses credentials, sends messages, runs on a schedule, or touches production — and when a user asks "is it safe to let the agent do this?"

## Example output

Running the bundled linter against a skill that hasn't been governed yet:

```
Governance lint: weekly-report
  [FAIL] missing governance/permission-manifest.yaml
  [FAIL] missing governance/rollback-plan.md
  [FAIL] SKILL.md has no '## Governance' section (Step 4 of the wrapper)

RESULT: FAIL — 3 issue(s). Fix before production use.
```

After adopting the wrapper, the linter also catches rule violations such as:

```
  [FAIL] operation 'purge_temp' is irreversible but gate is 'confirm' — must be 'manual'
  [WARN] operation 'email_team' has no rollback reference
  [WARN] 4 placeholder value(s) still empty — manifest not filled in
```

## What's inside

| Path | Purpose |
|---|---|
| `SKILL.md` | The five-step adoption workflow |
| `scripts/governance_lint.py` | Validates the governance layer (no dependencies) |
| `assets/permission-manifest.template.yaml` | Fill-in manifest schema |
| `assets/rollback-plan.template.md` | Fill-in recovery plan |
| `references/governance-guide.md` | Detailed guide, anti-patterns, compliance checklist |
