# Infrastructure Change Plan — <title>

**Status**: DRAFT | **APPROVED (this exact plan)** | **EXECUTED** | **ROLLED BACK**
**Environment**: <dev|staging|prod> — account/project ID: `____`
**Requested by**: ____ **Plan author (agent)**: ____ **Date**: ____

## 1. Intent

One paragraph: what this change achieves and why.

## 2. Exact Commands

```
____
```

(First run as plan/dry-run; the apply command is listed but executed only after approval.)

## 3. Resource Diff

- **Create**: `____`
- **Modify**: `____`
- **Replace**: `____` (stateful? → typed confirmation required)
- **Destroy**: `____` (stateful? → typed confirmation required)

## 4. Blast Radius

- Services/teams affected: `____`
- Data at risk: `____`
- Expected downtime or degradation: `____`
- Estimated recovery time if it goes wrong: `____`

## 5. IAM Permissions Exercised

List the cloud actions this change requires (e.g. `ec2:CreateSecurityGroup`). If any are new grants, state why the role should keep them permanently.

## 6. Static Review Result

`iam_scan.py` findings: ____
Resolved / accepted with reason: ____

## 7. Rollback Procedure

1. `____`
2. `____`
3. Verify: `____`

Backup/snapshot taken before change: `____`

## 8. Approval

> Approving this plan authorizes exactly the commands and resource diff in sections 2–3. Any changed plan requires new approval.

- [ ] Human approved — name/time: `____`

## 9. Post-Change Record (fill during execution)

- Actual commands run and outputs (or log path): `____`
- Verification results: `____`
- Deviations from plan (must be empty; deviations → rollback + re-plan): `____`
