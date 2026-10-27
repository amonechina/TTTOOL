# Governance Guide (Detailed)

## Why Governed Skills

The 2026 agent market signal is unambiguous: users do not lack demos, they lack installable, inspectable, recoverable workflows. The recurring objections collected from community discussions:

1. "I do not know whether I can safely let this thing act inside my business."
2. "It failed halfway through — why, and how do I recover?"
3. "What credentials did it use? What files could it touch?"
4. "Can I reproduce, inspect, resume, or roll back the work?"

A governance wrapper answers all four before the first run.

## The Wrapper Layer by Layer

### 1. Permission Manifest (the contract)

The manifest is a machine-readable boundary. Keep it strict:

- Use exact paths or narrowly globed patterns. `D:/projects/**` is acceptable; `**` is not.
- List every external host. Wildcard domains defeat the purpose.
- Destructive operations must map to named approval gates. If an operation is not in the manifest, the skill must refuse it — even if the user asks casually. Amend the manifest deliberately instead.

Example manifest excerpt:

```yaml
scope:
  filesystem:
    allow_write:
      - "D:/reports/out/**"
    deny:
      - "**/.git/**"
  network:
    allow:
      - "https://api.example.com/v1/*"
```

### 2. Approval Gates (the throttle)

Three levels, mapped by blast radius:

| Level | Meaning | Use for |
|-------|---------|---------|
| `auto` | Proceed without asking | Reads, cache writes, scratch files |
| `confirm` | One inline question, proceed on yes | Writes inside project scope, sends to internal recipients |
| `manual` | Stop; require out-of-band sign-off | Production changes, deletions, external sends, credential use beyond declared scope |

Anti-pattern: escalating everything to `manual`. Teams route around bureaucracy; the wrapper then gets deleted and you lose governance entirely. Visible, lightweight defaults survive contact with real work.

### 3. Failure Recovery (the safety net)

For every destructive operation, the rollback plan must name a pre-state capture mechanism:

- Files: copy to a timestamped backup directory, or require a clean git tree before starting
- Databases: record affected row keys; restore from transaction or snapshot
- External services: prefer operations with a reverse counterpart (create ↔ delete); flag irreversible ones as `manual`

Partial completion is the most common failure shape. Recovery steps must answer: how do I detect which steps completed (the audit log), and how do I undo exactly those?

### 4. Audit Log (the evidence)

Two lines per gated operation — before (intent) and after (outcome). Never log secret values. For scheduled/headless runs the log doubles as the resume checkpoint: a run must read the tail first and refuse to start if the previous run ended in an unresolved failure.

## Anti-Patterns

- **The demo skill**: works when conditions are kind, undefined behavior otherwise. If failure modes are not written down, they are not handled.
- **Silent fallback**: substituting a different tool or skipping a step without recording it. Any fallback must emit a `[AUDIT]` line marked `fallback`.
- **Credential leakage**: echoing secrets into logs, outputs, or error messages. Redact always.
- **Undocumented tribal knowledge**: the workflow exists only in the author's head. The manifest and rollback plan are the documentation.
- **Priority inversion**: framework instructions overriding the user's own project configuration. State explicitly that user/project instructions win.

## Worked Example: "weekly-report" Skill

Before governance: reads a data folder, generates a report, emails it to the team. Fails halfway through a send → nobody knows who received what.

After governance:
- Manifest: read `D:/data/**` (auto); write `D:/reports/out/` (confirm); SMTP send to `team@company.com` (confirm); send to external domains (manual — absent from allowlist, therefore refused)
- Rollback: report generation is idempotent (regenerate); email has no undo → send is a single batched step performed last, after the report file is fully written and verified
- Audit: `intent:email team@company.com` then `result:email sent msgId=...`
- Contract in SKILL.md: one paragraph a non-technical reviewer can read in 30 seconds

## Compliance Review Checklist

For team/enterprise adoption, reviewers should be able to answer from the governance files alone:

- [ ] What is the worst thing this skill can do?
- [ ] What requires a human decision, and where is that decision recorded?
- [ ] What happens when step N fails — what state is the system in?
- [ ] Where is the evidence of what ran, when, with what authority?
- [ ] How do I turn the whole thing off?
