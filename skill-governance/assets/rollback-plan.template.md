# Rollback & Failure Recovery Plan — <skill_name>

## Operation 1: <operation name>

- **Reversible**: yes/no
- **Pre-state capture** (choose one and fill in):
  - Backup: copy to `____` before running
  - Git: require clean tree; record commit `____`
  - Snapshot: `____`
- **Failure signals** (how to detect this operation failed or half-finished):
  - Error classes: `____`
  - Partial-completion symptoms: `____`
- **How to check what completed**: read tail of `governance/audit.log`; lines with `intent:` but no matching `result:` are unfinished.
- **Rollback steps**:
  1. `____`
  2. `____`
  3. Verify: `____`
- **Notify**: `____`

## Operation 2: <operation name>

_(repeat the block above for every entry in `destructive_operations`)_

## Runbook: Unresolved Previous Run

1. Stop. Do not start a new run.
2. Read `governance/audit.log` tail; list unfinished `intent:` operations.
3. Execute the matching rollback steps above.
4. Mark resolution in the log: `[AUDIT] <ts> | recovery | <operation> | manual | resolved`.
5. Only then start a new run.

## Hard Kill Switch

Describe the single fastest way to disable this skill entirely (e.g. remove the skill directory, revoke the credential, disable the schedule):

- `____`
