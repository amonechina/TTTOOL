# Cloud & IaC Security Checklists

## 1. IAM Least-Privilege Criteria

A policy statement is a **finding** if any of these hold:

- `Effect: Allow` with `Action: "*"` or `"service:*"` where narrower actions suffice
- `Resource: "*"` in an Allow statement that is not identity-scoped (e.g. `sts:GetCallerIdentity` may legitimately use `*`)
- `NotAction` combined with `Allow` (denies-by-omission, easily widens)
- Trust policies with `"Principal": "*"` without a condition block
- Admin-equivalent grants: `iam:*`, `*:*`, or `AdministratorAccess` attached to workload roles
- Wildcards inside actions like `s3:Get*` / `s3:*Object` that cover more than intended

Preferred shape:

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::my-app-assets/prod/*"
}
```

## 2. Resource Risk Table

| Resource type | Risk when destroyed/replaced | Default posture |
|---|---|---|
| RDS / SQL databases | Data loss; worst blast radius | `manual` typed confirmation; snapshot before change |
| S3 / object storage buckets | Data loss or public exposure | Never public-read unless stated in plan |
| SQS / queues / event buses | Message loss | Replace requires drain confirmation |
| Security groups | Exposure or outage | No 0.0.0.0/0 on admin ports (22, 3389) |
| Load balancers / DNS | Full outage of entry point | Plan must state traffic impact |
| IAM roles / policies | Privilege escalation path | Least privilege per §1 |
| KMS keys | Permanent data-access loss | Never delete; schedule key rotation instead |
| VPC / subnets / route tables | Connectivity for everything inside | Change requires network diagram in plan |

## 3. Pre-Apply Checklist

- [ ] Environment identified by ID, not by name-guess
- [ ] `plan`/`dry-run` output shown to the user, diff counts stated
- [ ] Every destroy/replace of a stateful resource explicitly acknowledged
- [ ] `iam_scan.py` findings resolved or accepted in writing
- [ ] Rollback path written (snapshot/backup/previous state ref)
- [ ] Approval obtained for THIS exact plan (a changed plan = new approval)
- [ ] No secrets in the diff or the plan file

## 4. Rollback Playbook Patterns

- **Terraform**: `terraform plan -destroy -target=<resource>` is rarely the answer; prefer `git revert` of the IaC commit → plan → apply. For stateful resources, restore from snapshot into a NEW resource, cut over, then clean up.
- **CloudFormation**: keep previous template version; `aws cloudformation update-stack` with previous template, or use change sets to preview.
- **Security group change gone wrong**: apply the inverse rule set immediately; do not investigate first.
- **Failed apply leaving partial state**: run plan again, read the diff, and reconcile — never hand-edit remote state unless recovery is otherwise impossible, and never without a state backup (`terraform state pull > backup.json`).

## 5. Signals to STOP and Re-Plan

- Plan output differs from the approved plan in any resource
- Plan wants to replace a stateful resource nobody mentioned
- Apply errors mention permissions/authorization — the agent must not request broader IAM to "unblock" itself; report and wait
- Any command would print resolved secret values
