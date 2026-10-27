---
name: skill-auditor
description: Performs due diligence on an AI agent skill (a SKILL.md-based package from GitHub, a marketplace, or a local folder) before installation. Runs automated checks for dangerous operations, secret leakage, stale maintenance, oversized context load, and metadata quality, then combines the results into a structured audit report with a verdict and risk level. This skill should be used when the user asks "is this skill safe", "review this skill before I install it", "audit my skill repo", when evaluating marketplace skills, or before adopting any third-party SKILL.md package.
---

# Skill Auditor

Turn "maybe it works" into an evidence-based verdict. Audit any skill in minutes using the automated scanner plus judgment on what automation cannot see.

## Workflow

### Step 1: Acquire the Skill Read-Only

- If given a GitHub URL: clone or download to a temporary directory. Never install into a live skills directory during audit.
- If given a local folder: audit in place, read-only. Do not execute any bundled script as part of the audit.

### Step 2: Run the Automated Scanner

```bash
python scripts/audit_skill.py <path-to-skill-folder> [--format text|json]
```

The scanner checks (full criteria in `references/audit-criteria.md`):

| Category | Checks |
|---|---|
| **Metadata** | Frontmatter present; `name` matches folder; `description` is specific and trigger-rich (not "a helpful skill") |
| **Danger patterns** | Network calls (curl/wget/requests/urllib), subprocess/eval/exec, credential file access (~/.ssh, .aws, .env), broad file deletion, base64-encoded blobs, obfuscated payloads |
| **Maintenance** | Last-modified time of files; TODO/placeholder residue in SKILL.md |
| **Context hygiene** | SKILL.md size (recommend < 5k words); total repo size; duplicate content between SKILL.md and references/ |
| **Structure** | Referenced scripts/assets actually exist; no orphan example scaffolding |

Exit code 0 = no high-risk findings.

### Step 3: Manual Review (what the scanner cannot see)

Read the SKILL.md yourself and judge:

1. **Does the skill do what its description claims?** Description-skill mismatch is the classic junk-skill signature.
2. **Are the instructions coherent for an agent?** Vague, self-contradictory, or padded instruction text ("you are a world-class expert...") lowers trust.
3. **Network + credentials together?** A skill that both calls out to a server and reads secrets deserves the highest suspicion even if each pattern looks benign alone.
4. **Where does data go?** Any instruction sending content to an external URL must be explainable; check what is sent (file contents? directory listings?).
5. **If scripts exist, read them.** The scanner flags patterns; only reading confirms intent. Watch for downloads-then-executes chains.

### Step 4: Produce the Verdict

Report using this structure:

```
VERDICT: install | install-with-caution | reject
RISK LEVEL: low | medium | high
CATEGORY: <domain>, e.g. document-processing / dev-tooling

Automated findings: <N high / M medium / K low — summarize the important ones>
Manual review notes: <2-5 bullets>
What would change the verdict: <concrete conditions, e.g. "if the fetch URL is pinned to an HTTPS release asset, medium → low">
```

Calibration:
- **install** — no high findings, instructions coherent, does what it claims, actively maintained
- **install-with-caution** — mediums present, or maintenance stale (> 6 months), or network use that is plausible but unpinned
- **reject** — any secret exfiltration pattern, obfuscated code, executes downloads, or claims mismatch that suggests SEO-spam skill

### Step 5: Advise on Installation

If verdict is install: give the exact install command and suggest pinning to a specific version/commit. If install-with-caution: list the specific guardrails (e.g. "run with network disabled first", "replace the curl URL with a mirror you control").

## References

- `references/audit-criteria.md` — complete finding taxonomy with severity definitions and examples

## Scripts

- `scripts/audit_skill.py` — the automated scanner (metadata, danger patterns, maintenance, structure)
