# Skill Factory Toolkit

Four production-grade skills that close the biggest trust gaps in the 2026 agent-skill ecosystem: governance, infrastructure safety, skill due diligence, and cross-platform compatibility.

Built from community-validated pain points (r/ClaudeAI, marketplace research). Each skill ships with a working scanner script, reference documentation, and fill-in templates.

## The Collection

| Skill | What it does | Suggested price |
|---|---|---|
| [skill-governance](./skill-governance/) | Wraps any skill/workflow with a permission manifest, approval gates, rollback plan, and audit logging. Includes a governance linter. | $9 |
| [infra-deploy-guard](./infra-deploy-guard/) | Guards cloud/IaC changes: static IAM & secrets scanning, mandatory plan-first workflow, human approval gates, blast-radius assessment. | $12 |
| [skill-auditor](./skill-auditor/) | Due diligence for any third-party SKILL.md package: danger-pattern scanning, maintenance checks, verdict report (install / caution / reject). | $7 |
| [skill-compat-checker](./skill-compat-checker/) | Static cross-platform compatibility scan (P1–P6 pitfalls) with concrete fixes for each finding. | FREE (lead gen) |

**Bundle: "Skill Factory Toolkit" — $19** (all four + governance linting)

## Why these four

Community research in 2026 converged on four unsolved gaps:

1. Operators don't trust agents to act inside their business — **no governed-skill layer exists** → skill-governance
2. Agents write app code but nobody safely automates cloud/IAM changes → infra-deploy-guard
3. "4,000 SKILL.md files on GitHub, maybe 100 are good" — no due-diligence tooling → skill-auditor
4. Platform-divergent behaviors (silent overwrites, relative-path breakage, ask-limit compaction) are undocumented → skill-compat-checker

## Install

```bash
# Claude Code / any SKILL.md-compatible agent
npx skills add <this-repo-url>

# or copy a skill folder into your skills directory
cp -r skill-auditor ~/.claude/skills/
```

## Verification

Every bundled scanner script was tested against crafted positive and negative samples before release (see each skill's README for example output).

## License

MIT for code. Skill instructions free to use with attribution.
