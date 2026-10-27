# 上架文案与定价方案（直接粘贴用）

> 各市场的 listing 文案。英文版用于 Agensi / SkillSafe / Claude Skills Market；中文版备用。

---

## 渠道〇：skill-from-workflow（2026-10-27 新增）

### Listing — skill-from-workflow

- **Title**: Skill From Workflow — turn an expert's personal workflow into a team-distributable skill
- **Price**: $15（访谈方法论含量高，对标 B 端价值；合集可并入）
- **Tags**: knowledge-management, onboarding, teams, interviewing, skill-engineering
- **Description**:
  > "Only super-individuals, no team capability." This skill runs a structured 3-round interview that extracts an expert's tacit judgment — exceptions, "looks wrong" signals, refusal conditions — into decision tables, packages it as a distributable SKILL.md skill, then gates distribution with a transferability review (author-dependence phrases, missing examples, unoperationalized judgment) and a live test where someone who wasn't interviewed runs it. Ships with a bilingual (EN/中文) question bank and a working package_review.py scanner.
- **示例输出**: README/上方实测记录——问题样例判 REVISE（7 项命中），合格样例 SHIP
- **渠道适配**：国内走"企业经验沉淀咨询"叙事；海外走 onboarding/knowledge-management 标签

---

## 渠道一：Agensi（agensi.io）— 付费市场，70% 分成

**店铺策略**：3 付费 + 1 免费（skill-compat-checker 免费引流）+ 1 合集。

### Listing 1 — skill-governance

- **Title**: Skill Governance Wrapper — permission manifest, approval gates, rollback & audit
- **Price**: $9
- **Tags**: governance, security, operations, production, reliability
- **Description**:
  > Wrap any agent skill or workflow in a trustable operational boundary: a deny-by-default permission manifest, three-level approval gates, a rollback plan for every destructive operation, and audit logging. Ships with a linter that catches rule violations like "irreversible operation gated at confirm instead of manual". For anyone shipping skills to schedules, teams, or production.
- **示例输出**: 用 `README.md` 里的 governance lint 输出片段

### Listing 2 — infra-deploy-guard

- **Title**: Infra Deploy Guard — plan-first, least-privilege guard for cloud/IaC changes
- **Price**: $12（高stakes场景，可定 $15）
- **Tags**: devops, terraform, iam, security, cloud, aws
- **Description**:
  > Stop AI agents from wild-carding your cloud account. Enforces plan/dry-run before apply, static least-privilege scanning (wildcard IAM, open admin ports, public-read storage, hardcoded secrets), a mandatory human-approved change plan with blast radius, and rollback playbooks. Includes a working scanner with JSON output for CI gates.
- **示例输出**: `README.md` 里的 iam_scan 5 findings 输出

### Listing 3 — skill-auditor

- **Title**: Skill Auditor — due diligence for any SKILL.md package before you install it
- **Price**: $7
- **Tags**: security, code-review, supply-chain, marketplace, quality
- **Description**:
  > "4,000 SKILL.md files on GitHub, maybe 100 are good." Audit any skill in minutes: automated danger-pattern scanning (eval/exec, credential+network combos, base64 obfuscation), maintenance and metadata checks, then a calibrated verdict — install / install-with-caution / reject — with falsifiable reasoning. Static analysis only; never executes the audited code.
- **示例输出**: `README.md` 里对恶意样例的 reject 报告

### Listing 4 — skill-compat-checker（免费引流款）

- **Title**: Skill Compat Checker — 6 cross-platform pitfalls, detected and fixed
- **Price**: FREE
- **Tags**: compatibility, testing, publishing, quality
- **Description**:
  > Platform-divergent agent behaviors are documented nowhere. This scanner detects all six known pitfalls — relative-path breakage, Write/create_file divergence, ask-limit compaction, missing-tool silent fallback, POSIX-only syntax, vague descriptions — and pairs every finding with a concrete fix. Free; if it saves you a debugging session, check out my other skills.

### Listing 5 — 合集

- **Title**: Skill Factory Toolkit — the complete skill-developer toolchain (bundle)
- **Price**: $19
- **Description**:
  > Build it → check it → audit it → govern it. Four production-grade skills covering the full lifecycle: governance wrapper (with linter), infra-deploy guard (with scanner), skill due-diligence auditor, and cross-platform compat checker. Save 40% vs buying individually.

---

## 渠道二：SkillSafe（skillsafe.ai）— 托管 app 按次计费

**策略**：4 个技能全部免费共享（攒安装量 + 通过安全扫描），把 **infra-deploy-guard** 做成托管 app 收费（每次云变更审查都是高价值单次行为），加价建议 **25–50%**。

- App slug 建议：`infra-deploy-guard`
- App 简介：> Paste your Terraform/CloudFormation or describe your planned change. Get a static least-privilege & secrets scan, a blast-radius assessment, and a fill-in change plan — before anything touches your real account.
- 定价：起步 10%（平台默认），有流量后调到 25–50%
- 提现：收益 14 天成熟，$25 起提（PayPal 或 USDC）

---

## 渠道三：Claude Skills Market（claudeskillsmarket.com）— 免费社区 + 接单

**策略**：4 个全部免费提交（SMB/agency 买家群体看到的是专业度），引导定制委托（commission）。

- Builder 个人简介建议：> I build trust-infrastructure skills: governance wrappers, infra-deploy safety rails, skill due-diligence and cross-platform compat tooling. Available for custom skill commissions.
- 提交入口：登录后 Submit a Skill，逐个粘贴对应技能的 SKILL.md 与 README（英文版已就绪）
- 定制服务挂牌价参考：单个定制 Skill $150–400（社区常见区间）

---

## 渠道四：GitHub — 源仓库（免费、开源信誉）

- 仓库描述：> Four production-grade agent skills closing the biggest trust gaps in the 2026 skill ecosystem: governance, infra safety, due diligence, compat.
- Topics：`agent-skills` `claude-code` `skill-md` `ai-agents` `devops` `security`
- 每个 README 已内置示例输出；顶层 README 有合集介绍与安装命令
- 开源协议：MIT（代码）
