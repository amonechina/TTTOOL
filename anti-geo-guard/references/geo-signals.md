# GEO Signal Catalog

Real tactics used to get content cited by AI engines, with detection notes. Use this list when the scanner's textual signals are insufficient (scanners can't see site-level behavior — you can).

## S1. LLM Seeding ("answer engine optimization")

**Tactic**: vendors plant content engineered to be quoted verbatim by LLMs: FAQ blocks phrased as user queries, "TL;DR" summaries stuffed with brand claims, comparison pages answering "what is the best X" with themselves.

**Detect**: FAQ questions that mirror search queries word-for-word; answers written as declarative one-liners an LLM could lift; the same Q&A text syndicated across multiple domains (search one distinctive sentence in quotes).

**Weight**: strong.

## S2. Affiliate / review-farm content

**Tactic**: "Best X for Y in 2026" sites monetized by affiliate links; content farms producing hundreds of near-identical roundups under different brand names.

**Detect**: `/go/`, `/ref/`, `tag=`, `amzn.to`, `utm_content=affiliate`; "we may earn a commission"; identical comparison-table structure across "competing" sites; author pages with no real history; the "best" product is always one with a high affiliate payout.

**Weight**: strong when combined with rankings.

## S3. Astroturfing in communities

**Tactic**: fake "genuine user" posts on Reddit/HN/forums recommending a brand; coordinated upvoting so the post surfaces in AI-cited threads.

**Detect**: new accounts whose history is only one product; identical phrasing across accounts ("total game-changer for my workflow"); posts that read like the product's landing page; defensive replies from a second fresh account.

**Weight**: strong per-post, medium per-source (verify the account before excluding the whole community).

## S4. Press-release laundering

**Tactic**: vendors publish a press release ("Survey finds 73% of enterprises adopt…"), then dozens of syndication sites republish it; AI engines cite the syndicated copies, making a marketing claim look independently reported.

**Detect**: search the exact statistic in quotes — if all hits trace back to one vendor release, it's laundering. "According to a new report" with no named methodology. PR-newswire/businesswire URL patterns.

**Weight**: strong.

## S5. Statistics without provenance

**Tactic**: invented or distorted stats that get repeated because LLMs and writers copy plausible numbers.

**Detect**: no sample size, no date, no methodology, no primary link; round, quotable numbers ("87%", "3x faster"); the stat supports exactly the sponsor's product.

**Weight**: medium alone, strong with S4.

## S6. Reciprocal citation rings

**Tactic**: a cluster of sites (often same owner) citing each other to build apparent consensus.

**Detect**: "as reported by [site in the same network]"; several "independent" reviewers all citing one seeded origin; whois/network overlap if you check.

**Weight**: medium.

## S7. Superlative saturation / no-trade-off writing

**Tactic**: every option framed positively; the sponsored option just has more adjectives. No failure cases, no pricing criticism, no "who should NOT buy this".

**Detect**: density of best/leading/#1/revolutionary/cutting-edge; absence of any negative statement; comparison "criteria" that exactly match the vendor's feature list.

**Weight**: medium (style alone isn't proof — combine with other signals).

## S8. Recency-synchronized content waves

**Tactic**: near-identical articles published across unrelated sites within days of a launch or funding announcement, to dominate the fresh-citation window.

**Detect**: same structure/claims across domains, all dated within ~72 hours of an event; generic author names; no original screenshot or hands-on detail.

**Weight**: medium.

## Source-tier quick reference

| Tier | Examples | Handling |
|---|---|---|
| T1 | Official docs, RFCs, source code, filings | Use freely |
| T2 | Peer-reviewed work, investigative journalism, verifiable first-hand accounts | Use freely |
| T3 | Reddit/HN/issues/forums | Verify account & specifics before citing |
| T4 | Vendor blogs, affiliate sites, PR | Only with T1/T2 corroboration; disclose commercial nature |
| T5 | GEO-optimized per S1–S8 | Exclude from evidence; may cite as object of analysis, labeled |
