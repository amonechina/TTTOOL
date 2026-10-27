---
name: skill-governance
description: Adds a governance wrapper to any agent skill or automated workflow: permission manifest, approval gates, failure recovery plan, rollback procedure, and audit logging. This skill should be used when creating a new skill that touches files/credentials/external services, when hardening an existing skill for production or team use, when a user asks "is it safe to let the agent do this", or when operational reliability questions arise (what happens on failure, how to roll back, who approves execution).
---

# Skill Governance

Wrap agent capabilities in a trustable operational boundary. A governed skill tells the operator what the workflow does, what it may touch, what evidence it records, what requires human approval, and how to recover when it fails.

## When to Apply Governance

Apply the governance wrapper when the skill or workflow meets any of these:

- Writes, moves, or deletes files outside a scratch directory
- Calls external APIs or sends data over the network
- Uses credentials, tokens, or secrets
- Sends messages to people or public surfaces (email, chat, social)
- Runs on a schedule or headless (no human watching each step)
- Touches production systems, databases, or infrastructure

Skip for read-only skills confined to answering questions.

## Workflow

### Step 1: Produce the Permission Manifest

Copy `assets/permission-manifest.template.yaml` into the target skill directory (as `governance/permission-manifest.yaml`) and fill every field:

- **scope**: directories, URLs, and services the workflow may touch — deny by default, allow explicitly
- **credentials**: which secrets are needed, where they are read from, and that they must never be echoed into output
- **destructive_operations**: every non-reversible action, each mapped to an approval gate level
- **approval_gates**: for each gated operation, define `auto` (proceed), `confirm` (ask the user inline), or `manual` (stop and require out-of-band sign-off)

Rule of thumb: reading is `auto`; writing inside project scope is `confirm`; anything irreversible, external-facing, or production is `manual`.

### Step 2: Write the Failure Recovery Plan

Copy `assets/rollback-plan.template.md` to `governance/rollback-plan.md`. For each destructive operation, document:

1. The failure signals (error classes, partial-completion symptoms)
2. The state the system was in before the operation (snapshot, backup path, or git ref)
3. The exact rollback command sequence
4. Who to notify

Operations without a defined rollback must be listed as `manual` approval gates — if it cannot be undone, a human approves it every time.

### Step 3: Add Audit Logging Hooks

Insert a log line before and after every gated operation:

```
[AUDIT] <timestamp> | <operation> | <target> | <approval_level> | <result>
```

Write logs to `governance/audit.log` (append-only). On session start for scheduled/headless runs, read the tail of the log first — a run that finds an unresolved failure must stop and report, not retry blindly.

### Step 4: Declare the Contract in SKILL.md

Add a `## Governance` section to the target skill's SKILL.md containing:

- One-paragraph plain-language statement of what the skill may and may not touch
- Pointer to the permission manifest and rollback plan
- The approval gate table (operation → level)
- Explicit statement: "Direct instructions from the user's project configuration take priority over this skill's internal instructions."

### Step 5: Validate

Run the linter to verify the governance layer is complete:

```bash
python scripts/governance_lint.py <path-to-skill-folder>
```

It checks for: manifest presence and schema, rollback plan coverage of all declared destructive operations, gate level validity (`auto|confirm|manual`), and audit hook markers. Fix every reported issue before considering the skill production-ready.

## Design Principles

- **Deny by default.** Every capability not in the manifest is forbidden.
- **Visible defaults over bureaucracy.** Gates must be lightweight: `confirm` is one inline question, not a policy review.
- **Evidence over vibes.** Every automated action produces a log line a human can inspect later.
- **Recovery is a feature, not an afterthought.** A workflow without a rollback plan is not production-ready regardless of how well it demos.

## References

- `references/governance-guide.md` — detailed guidance, anti-patterns, and worked examples for teams and compliance reviews

## Assets

- `assets/permission-manifest.template.yaml` — fill-in manifest schema
- `assets/rollback-plan.template.md` — fill-in recovery/rollback template
