---
name: infra-deploy-guard
description: Guards production infrastructure changes made by AI coding agents. Reviews Terraform/CloudFormation/IaC and IAM policies for least-privilege violations and wildcards, produces a blast-radius assessment and a mandatory change plan before any real account is touched, and enforces a dry-run/plan-first, human-approval workflow. This skill should be used when an agent is about to modify cloud infrastructure (AWS/GCP/Azure), when writing or reviewing IAM policies, Terraform, CloudFormation or deployment scripts, when the user asks "is this change safe to apply", or before any apply/deploy command against a real environment.
---

# Infra Deploy Guard

The gap between "agent writes app code" and "agent touches real infrastructure" is trust. Close it with three disciplines: **plan before apply**, **least privilege always**, **blast radius stated in plain language**.

## Hard Rules (never violate)

1. **Never apply, deploy, or mutate a real environment without an explicit human "yes" for that exact plan.** "Go ahead", "fix it", or approval of a previous plan does not carry over to a changed plan.
2. **Plan/dry-run first, always.** `terraform plan` (or the platform equivalent) must run and be shown to the user before any apply. Diff count = resources created/destroyed/replaced. `replace` and `destroy` of stateful resources (databases, storage, queues) escalate to explicit typed confirmation.
3. **Read-only by default.** Inspect (list, describe, get) is allowed freely. Anything with `create|update|delete|put|attach` in the name is a mutation.
4. **No credentials in code, output, or logs.** Reference secret managers; refuse to echo resolved values.
5. **State the blast radius** for every change: services affected, data at risk, rollback path, estimated recovery time.

## Workflow

### Step 1: Inventory

Determine before proposing anything:
- Which environment (dev/staging/prod)? Which account/project/subscription ID?
- What exists there today (relevant resources, their names and tags)?
- What is the IaC source of truth, if any (Terraform state, CloudFormation stacks)?

If the target environment is unclear, stop and ask. Never guess "prod vs dev".

### Step 2: Static Review

Run the wildcard/least-privilege scanner on the files about to be applied:

```bash
python scripts/iam_scan.py <terraform-dir-or-file> [--format text|json]
```

It flags (see `references/cloud-checklists.md` for full criteria):
- IAM actions or resources using `*` in Allow statements
- `aws_iam_policy` / policy documents granting `*:*`
- Public access patterns (0.0.0.0/0 ingress, public-read buckets/objects)
- Security group rules opening admin ports (22/3389) to the world
- Hardcoded secrets/keys (AKIA..., private key blocks, generic `password = "..."`)

Every finding must be resolved (fixed or explicitly accepted with a written reason) before Step 3.

### Step 3: Change Plan

Write the plan into `assets/change-plan.template.md` format and present it to the user. A plan without all sections filled is not presentable. Include: intent, exact commands, resources created/modified/destroyed, blast radius, IAM permissions exercised, rollback procedure, and the approval request.

### Step 4: Execute with Checkpoints

After the user approves THIS plan:
1. Run the plan/dry-run command again immediately before apply (state may have drifted since review).
2. Compare: if the new diff differs from the approved plan, re-approve.
3. Apply. On failure, stop — capture full error output; do not retry with "fixes" that alter scope. Re-plan instead.
4. Record what was done (commands, outputs) into the change plan file as the post-change record.

### Step 5: Verify and Record

Post-apply verification reads only: `terraform state list` / `describe` calls to confirm the intended end state. Append the verification results and rollback availability to the change record.

## References

- `references/cloud-checklists.md` — least-privilege criteria, per-resource risk tables (databases/storage/network/IAM), and rollback playbooks

## Assets

- `assets/change-plan.template.md` — the mandatory pre-approval change plan

## Scripts

- `scripts/iam_scan.py` — static wildcard/least-privilege/secret scanner for Terraform, CloudFormation, and policy JSON
