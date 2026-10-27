# 发布执行清单（含需要你注册/操作的步骤）

> ✅ = 已由 AI 完成并就绪　｜　⚠️ = 需要你本人操作（涉及账号注册，我无法代填凭据）

## 发布前状态

- ✅ 4 个技能源码 + skill-info.yaml + 英文 README（含示例输出）+ 上架文案（listings.md）
- ✅ 定价方案：governance $9 / infra $12 / auditor $7 / compat 免费 / 合集 $19
- ✅ 本目录已 git 初始化，可直接推送

---

## 渠道 1：Agensi（主力收入，70% 分成）

⚠️ **步骤 1（你操作）**：打开 https://www.agensi.io → Sign Up（邮箱注册）
- 需要填写：邮箱、密码；收款需连接 **Stripe Connect**（准备：邮箱、银行/PayPal 收款信息）
- 💡 提醒：Stripe 注册可能要求身份验证，预留 10–20 分钟

⚠️ **步骤 2（你操作）**：进入 Creator 后台 → Submit Skill，按 `listings.md` 渠道一逐条填写：
- 标题/描述/标签/价格：直接从 `listings.md` 复制
- 上传文件：对应技能的 zip（`D:\skill-governance.zip` 等 4 个）或仓库链接
- 每个技能附 README 中的示例输出作为 "Example output" 图/文

✅ 材料已备齐：`listings.md`（文案+定价）、各技能 `README.md`（示例输出）

## 渠道 2：SkillSafe（按次计费 app）

⚠️ **步骤 1（你操作）**：打开 https://skillsafe.ai → 注册（支持邮箱；提现用 PayPal 或 USDC 钱包地址）
⚠️ **步骤 2（你操作或让我继续）**：
- 先把 4 个技能保存（Save）到账号 —— 新技能默认私密
- 再 Share 全部 4 个 —— 自动过安全扫描（我们已自测过无高危模式，.md 中的模式说明已在文档里解释）
- 把 **infra-deploy-guard** 发布为 hosted app（apps/create 页面有可复制提示词），slug 建议 `infra-deploy-guard`，加价从默认 10% 起步，有流量后调 25–50%
✅ 材料已备齐：app 简介文案在 `listings.md` 渠道二

## 渠道 3：Claude Skills Market（免费社区 + 接单入口）

⚠️ **步骤 1（你操作）**：打开 https://www.claudeskillsmarket.com/auth?mode=signup → 免费注册（无需信用卡）
⚠️ **步骤 2（你操作）**：Submit a Skill × 4 —— 每次粘贴对应技能的 SKILL.md 内容 + README；平台会自动做注入/恶意模式扫描
✅ 材料已备齐：Builder 个人简介与定制服务话术在 `listings.md` 渠道三

## 渠道 4：GitHub（源仓库 + 信誉）

⚠️ **步骤 1（你操作）**：告诉我你的 GitHub 用户名/仓库名偏好，或你自己在 github.com/new 建一个空仓库（建议名：`skill-factory-toolkit`，Public，不要初始化 README）

⚠️ **步骤 2（你操作授权后我来推送）**：
- 方式 A：你在本机配好 git 凭据后，告诉我仓库地址，我执行 push（当前目录已 git init + 待提交）
- 方式 B：你手动执行：
  ```bash
  cd D:\AI-Skills
  git add -A && git commit -m "Skill Factory Toolkit: 4 skills + docs"
  git remote add origin https://github.com/<你的用户名>/skill-factory-toolkit.git
  git push -u origin main
  ```
✅ 材料已备齐：仓库描述、Topics 标签（`listings.md` 渠道四）

---

## 发布后 48 小时内建议（我可直接代劳的部分）

1. 在 r/ClaudeAI、dev.to 发推广帖（Agensi 官方推荐渠道）—— 文案我可以起草，发帖账号需要你
2. 监控 Agensi 后台安装数据，一周后根据转化调价
3. 收到第一条定制委托（Claude Skills Market）后，告诉我，我帮你评估范围与报价

## 提醒机制

注册环节共 4 处（Agensi+Stripe / SkillSafe / CSM / GitHub），每处需要 5–20 分钟。
如果你想让我在特定时间提醒你逐步完成，告诉我时间，我可以创建定时提醒。
