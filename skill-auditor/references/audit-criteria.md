# Audit Criteria & Finding Taxonomy

## Severity Definitions

| Severity | Meaning | Examples |
|---|---|---|
| **high** | Grounds for rejection on its own | Secret-file access + network send; executes downloaded code; obfuscated payload |
| **medium** | Requires explanation before install | Network calls at all; broad deletes; stale maintenance; TODO scaffolding |
| **low** | Hygiene issues; note but do not block | Oversized SKILL.md; weak description; orphans/example files |

## Danger Pattern Details (what the scanner flags)

### Network egress
- `curl`, `wget`, `Invoke-WebRequest`, Python `requests`/`urllib`/`httpx`, Node `fetch`/`axios`
- Severity escalates when combined with: reading files, environment variables, or credential paths, or when the URL is not a documented API endpoint of the skill's purpose.

### Execution
- `subprocess`, `os.system`, `eval`, `exec`, `Function(`, `child_process`, `bash -c`, piping downloads into interpreters
- `eval`/`exec` in a bundled script is high. In example snippets inside references, medium.

### Credential access
- Paths: `~/.ssh`, `.aws/credentials`, `.env`, `.netrc`, `.gitconfig`, browser profile dirs, keychains
- Any combination of credential path + network call in the same skill = presumptive **reject**.

### Destructive operations
- `rm -rf`, `shutil.rmtree`, `del /S`, wildcards over home/system directories
- Broad deletes without a backup/confirmation step in the surrounding instructions = high.

### Obfuscation
- Long base64/hex blobs, multiple decode passes, `compile()` of strings, exec after decode — all **high**. Legitimate skills have no need for these.

## Metadata Quality Bar

- **description**: must state what the skill does AND when to use it, in third person, with concrete triggers (file types, task verbs). A description that is generic praise ("makes you 10x productive") fails.
- **name**: kebab-case, matches the folder name.
- **structure**: SKILL.md exists at root; referenced scripts/assets exist; references/ used for detail rather than a 10k-word SKILL.md.

## Maintenance Signals

- All files last modified > 12 months ago, in a fast-moving platform: medium (skills are cheap, but stale skills drift from platform behavior).
- TODO/placeholder markers still in SKILL.md: medium — signals unfinished or auto-generated-without-review content.
- Changelog absent is fine for skills; broken references are not.

## Scoring to Verdict

| Automated result | Then |
|---|---|
| Any high finding | Default **reject**; only flip to caution if the pattern is clearly documented and justified in the skill's own README |
| Mediums only | **install-with-caution**, list the concerns |
| No findings | Proceed to manual review; verdict from coherence + claims-match + maintenance |

## Report Template Reminder

Always end with the structured verdict block (see SKILL.md Step 4) — verdict, risk level, category, findings summary, manual notes, and what would change the verdict. Audits without a falsifiable "what would change my mind" clause are opinions; this one is evidence.
