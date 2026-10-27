---
name: skill-from-workflow
description: Captures an expert's repeatable personal workflow through a structured interview and packages it into a distributable SKILL.md skill that teammates can run without the author present. Extracts tacit judgment (exceptions, "looks wrong" signals, quality bars) into decision tables, then verifies the result is author-independent via a transferability review. This skill should be used when a user says "帮我把我做XX的方法做成技能", "turn my workflow into a skill", "package how I do this for the team", when onboarding documents keep failing because the real know-how lives in one person's head, or when a team lead wants to convert an individual's repeated process into a team asset.
---

# Skill From Workflow

The most valuable knowledge in any team is the expert's judgment: which exceptions to take, which row "looks wrong", what the client's request *really* means. It never lands in process documents, it leaves when the expert does, and individual excellence never becomes team capability. This skill closes that gap with a three-stage pipeline: **interview → spec → package**, gated by an author-independence test.

## When to Use

- An expert does the same multi-step task weekly, with consistent professional output
- Documentation exists but new hires still fail — the real know-how is oral
- A team lead says "make what she does repeatable" or "沉淀团队经验"
- Building a paid/commissioned skill from a client's personal method

Skip when the workflow is fully documented AND exceptions are enumerated (then just edit the docs) — interviewing adds nothing.

## Stage 1: Scope the Workflow (10 minutes)

Answer four questions with the expert before interviewing:

1. **Trigger**: what starts this workflow? (a file arrives, a meeting ends, a request comes in)
2. **Output**: what does the finished work look like? Get one real finished example now — it becomes the quality bar and the worked example.
3. **Frequency & variance**: weekly or daily? Does every run differ? (High variance = more interview rounds needed)
4. **Audience**: who will run the packaged skill — teammates with shared context, or strangers? (Determines how much background to encode)

**Reject** if output varies wildly with no stable quality bar, or the expert cannot produce a finished example — capture candidates are not packaged well.

## Stage 2: Structured Interview (3 rounds, 30–45 minutes)

Use the question bank in `references/interview-guide.md` (bilingual 中/英). Rules that make the extraction work:

- **Ask for stories, not procedures.** "Walk me through the last one that went wrong" extracts exceptions; "describe your process" extracts the sanitized version already in the docs.
- **Probe every judgment verb.** When the expert says "check if it looks right" / "觉得不对就退回", demand the operational test: what do you look at, what values make it wrong, what do you do then?
- **Capture refusals.** When does the expert decline the task or escalate? A skill that never says no is dangerous.
- Record everything into `assets/workflow-spec.template.md` as you go — the spec is the deliverable of this stage.

Round structure:
- **Round 1 — The happy path**: trigger, inputs, steps, tools, output format
- **Round 2 — The judgment layer**: exceptions, decision points, "looks wrong" signals, refusal conditions, quality bar against the real example
- **Round 3 — The transfer test**: hand the drafted spec back; ask the expert to find what a new hire would still get wrong; capture the deltas

**Gate**: the expert must explicitly approve the completed spec (签字确认). Never package from half-recalled notes — wrong tacit knowledge packages faster than no knowledge.

## Stage 3: Generate the Skill Package

From the approved spec, produce a standard skill folder:

1. **SKILL.md** — third-person description with concrete trigger phrases (both the phrases teammates actually say and file types); imperative-voice workflow mirroring the spec's steps; every judgment call from Round 2 encoded as a **decision table** (signal → condition → action), not as prose like "use your judgment"
2. **Worked example** — the real output from Stage 1, annotated: what a good output looks like and why each part is there
3. **Templates** — input/output scaffolds the runner fills in, so results are consistent
4. **Refusal section** — the escalation/no conditions from the interview, verbatim in effect
5. **skill-info.yaml** — bilingual metadata card (name, problem, capabilities, when to use)

### Author-Independence Test (the gate)

Run `scripts/package_review.py <generated-skill-folder>` — it flags:

- Author-dependent phrases ("as I mentioned", "ask me", contact-only troubleshooting, "my usual approach")
- Personal absolute paths and machine-specific references
- Missing worked example, missing refusal/escalation section
- Judgment left as prose ("use your judgment") instead of decision tables
- Undefined jargon the author's team knows but strangers won't

Then the live test: have someone who was NOT interviewed (a teammate, or the agent role-playing a new hire) run the packaged skill on a real task. The expert grades the output against the quality bar. Any gap returns to Stage 2 as a new interview question. Iterate until the expert says "I would have done the same."

## Distribution Checklist

- [ ] package_review.py: 0 high findings
- [ ] Live test passed with a non-author runner
- [ ] SKILL.md description contains real trigger phrases
- [ ] Version + date stamped in skill-info.yaml
- [ ] Update path agreed: who maintains it when the underlying process changes (unmaintained skills rot — name the owner)

## References

- `references/interview-guide.md` — bilingual question bank, tacit-knowledge extraction techniques, common interview failure modes

## Assets

- `assets/workflow-spec.template.md` — the Stage 2 deliverable / Stage 3 source
- `assets/distribution-readme.template.md` — README for the packaged skill

## Scripts

- `scripts/package_review.py` — transferability checker (`--format text|json`)
