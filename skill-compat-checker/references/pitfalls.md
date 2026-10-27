# Pitfall Catalog — Broken vs Fixed

## P1 Relative Paths

**Broken** (in SKILL.md instructions):

```
Read the schema from ../references/schema.md
Load the config at C:/Users/me/skills/my-skill/references/config.md
```

Relative paths (`../`, bare `references/...` without context) resolve against the process working directory, not the skill folder — they break on most platforms. Absolute personal paths break on every other machine.

**Fixed**:

```
Read schema.md from this skill's references/ directory
(base directory = the directory containing this SKILL.md)
```

If a platform exposes the skill base directory to the agent, use it; otherwise instruct the agent to locate the file relative to SKILL.md itself. Test the resolution on each target platform.

## P2 File Write APIs

**Broken**:

```
Create the report file. (implicit — runtime picks the API)
```

Code/desktop runtimes: `Write` overwrites silently. Web runtimes: `create_file` refuses to overwrite. Same instruction, opposite behavior, no error on either side.

**Fixed**:

```
Creating a file:
- On runtimes with Write: use Write (it overwrites existing files silently —
  verify the target before overwriting user content).
- On runtimes with create_file: check existence first; if the file exists,
  ask the user before overwriting.
```

## P3 Ask-User-Input Limits

**Broken**:

```
Ask the user 5 questions with 6 options each to gather requirements.
```

The tool enforces max 3 questions × 4 options and silently compacts larger requests. The skill loses questions it thinks it asked.

**Fixed**:

```
Gather requirements in two rounds:
- Round 1 (3 questions, ≤ 4 options each): purpose, audience, format.
- Round 2 (up to 3 questions): depth, tone, delivery target.
State the round structure explicitly so no question is dropped.
```

## P4 Missing-Tool Silent Fallback

**Broken**:

```
Use the web_search tool to find current pricing.
```

If the platform has no `web_search`, the agent degrades to prose ("pricing varies...") without warning. The skill looks like it worked.

**Fixed**:

```
Use the web_search tool to find current pricing.
If web_search is unavailable on this platform: STOP and tell the user
"this step requires web search, which is unavailable here" — do not
substitute an answer from memory.
```

Enumerate every tool the skill depends on; attach a fallback clause to each.

## P5 Shell Assumptions

**Broken**:

```
Run: cat data/*.csv | python aggregate.py > out.csv
```

Breaks on Windows runtimes without a POSIX shell.

**Fixed**:

```
Aggregate the CSVs:
- POSIX shell: cat data/*.csv | python aggregate.py > out.csv
- PowerShell: Get-Content data/*.csv | python aggregate.py > out.csv
Detect the runtime, or prefer a single cross-platform Python invocation:
python aggregate.py data/ --out out.csv
```

## P6 Frontmatter Description Drift

**Broken**:

```yaml
description: Helps with documents
```

Vague descriptions fail description-based skill matching on several platforms — the skill never triggers.

**Fixed**:

```yaml
description: Converts quarterly meeting notes into an internal newsletter,
  selecting notable items and formatting per company template. This skill
  should be used when the user asks to draft, generate, or compile a
  newsletter from meeting notes or a notes document.
```

Third person, names the task, names the trigger phrases.
