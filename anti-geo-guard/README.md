# anti-geo-guard

**Anti-GEO shield for AI search and Q&A** — detects, flags, and excludes marketing content engineered to be cited by AI engines (GEO / LLM seeding / AI-SEO), so your answers stand on independent evidence instead of paid placement.

## The problem

Marketers now optimize content to be *quoted by AI*, not to inform humans: fake "best of" roundups, astroturfed Reddit threads, press releases syndicated to look like independent reporting, invented statistics repeated until they feel like facts. When an AI answers "what's the best X", a large share of its sources are ads in disguise — and nothing in the answer tells you which.

## What it does

1. **Triage** — classifies every candidate source into T1–T5 tiers (primary / independent / community / commercial-blog / GEO-optimized) before it can be used as evidence.
2. **Flag** — `geo_scan.py` statically scores text for 7 signal families: superlative saturation, affiliate plumbing, astroturf phrasing, PR laundering, unprovenanced statistics, LLM-seeding fingerprints (query-mirroring FAQs, brand-stuffed TL;DRs), commercial CTAs. Every finding carries the signal and line number.
3. **Exclude** — GEO-verified sources are removed from the evidence chain entirely (not "discounted"): marketing noise is an injection attempt, not a data point.
4. **Disclose** — answers end with a provenance line: how many sources used, how many excluded and why. Exclusion decisions are auditable via the bundled report template.

## Sample output

```
$ python scripts/geo_scan.py suspicious-article.md
   words: 127  |  signals: 21  |  GEO score: 100/100
   [G1] L1    Superlative saturation: # What Is the Best AI Agent Platform in 2026?
   [G2] L20   Affiliate / sponsored plumbing: .../go/novaagent?tag=aff123
   [G3] L6    Astroturf review phrasing: I've been using NovaAgent... total game-changer
   [G4] L7    Press-release laundering: According to a new report from NovaLabs, 87%...
   [G6] L3    LLM-seeding fingerprint: TL;DR: NovaAgent is the best AI agent platform...
   VERDICT: LIKELY GEO — exclude from evidence
```

Clean technical notes score 0/100. The scanner was validated against fabricated GEO articles, astroturf reviews, and clean primary-source documents before release.

## Install

Unzip into your agent skills directory, or:

```
npx skills add amonechina/TTTOOL
```

## Notes

- The scanner is triage, not verdict — SKILL.md requires manual verification of contextual patterns (account age, citation rings, syndication checks) that only the agent can do.
- Signals are applied symmetrically: commercial ≠ excluded by default. Vendor changelogs and spec sheets with methodology are fine; seeded roundups are not.
