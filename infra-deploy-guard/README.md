# infra-deploy-guard

Safety rails for AI coding agents that touch real cloud infrastructure. Plan-first, least-privilege, human-approved.

## What this skill does

Closes the gap between "agent writes app code" and "agent mutates your AWS account". It enforces:

- **Plan/dry-run before every apply** — diff shown to the human; a changed diff invalidates the approval
- **Static least-privilege review** via the bundled scanner (wildcard IAM actions/resources, public ingress on admin ports, public-read storage, hardcoded secrets, unconditioned `Principal: *`)
- **A mandatory change plan** — intent, exact commands, resource diff, blast radius, IAM permissions exercised, rollback procedure — presented for approval before anything runs
- **Typed confirmation** for replace/destroy of stateful resources (databases, buckets, queues, KMS)
- **Agent self-restraint rules**: on a permissions error the agent must stop and report, never request broader IAM to "unblock itself"; no secrets in code, output, or logs

## When it activates

Use when an agent is about to modify cloud infrastructure (AWS/GCP/Azure), when writing or reviewing Terraform/CloudFormation/IAM policies, or before any apply/deploy against a real environment.

## Example output

`scripts/iam_scan.py` against a Terraform file with planted risks:

```
[HIGH  ] R1  infra/main.tf
        HCL Allow statement with wildcard Action
[HIGH  ] R2  infra/main.tf
        HCL Allow statement with wildcard Resource
[HIGH  ] R4  infra/main.tf
        admin port open to 0.0.0.0/0 (0.0.0.0/0)
[HIGH  ] R5  infra/main.tf
        public-read ACL on storage
[HIGH  ] R6  infra/main.tf
        Terraform variable 'db_password' has a hardcoded default value

5 finding(s). A clean scan is not a certification — review before apply.
```

Supports `--format json` for CI integration and `--fail-on high|medium|any` as a pipeline gate.

## What's inside

| Path | Purpose |
|---|---|
| `SKILL.md` | Five-step guarded workflow (inventory → static review → change plan → checkpointed execution → verify) |
| `scripts/iam_scan.py` | Static scanner for Terraform / CloudFormation / policy JSON |
| `assets/change-plan.template.md` | The mandatory pre-approval change plan |
| `references/cloud-checklists.md` | Least-privilege criteria, per-resource risk table, rollback playbooks |
