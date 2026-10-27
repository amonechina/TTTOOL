# Interview Guide — Extracting Tacit Knowledge (访谈指南)

The core difficulty: experts cannot directly verbalize judgment. They demonstrate it, they recognize it when they see it, but "how do you know it's wrong?" gets answered with "experience." These techniques convert recognition into operational rules.

## Technique 1: Stories Over Procedures

Never ask "what is your process?" first — you get the sanitized version that's already in the docs. Instead:

- "Tell me about the last one that went wrong." (找最近一次出错的)
- "Tell me about the fastest one you ever did."
- "When did you last return something to the requester? Why?"

Stories carry the exceptions, the refusal conditions, and the real sequence (which usually differs from the official one).

## Technique 2: Interrogate Judgment Verbs

Every time the expert uses a judgment verb, demand the operational test behind it:

| Expert says | You must extract |
|---|---|
| "check if it looks right" / "看看对不对" | What do you look at? Which values/patterns make it wrong? |
| "if it's urgent" / "着急的话" | What makes it urgent? Who decides? |
| "use your judgment" / "灵活处理" | What are the actual branches? |
| "a reasonable price" / "合理的价格" | What range? Derived from what? |
| "clean data" / "数据干净" | What do you check first? What fails most often? |

Rule: a judgment that cannot be turned into a decision table gets logged as a **known limitation** in the spec — do not silently convert it into "use your judgment" in the packaged skill.

## Technique 3: Capture Refusals and Escalations

Ask directly:
- "什么时候你会拒绝做这件事？" (When do you decline?)
- "什么情况你会找人/上报？" (When do you escalate, and to whom for what?)

A packaged skill without refusal conditions will happily produce confident garbage in exactly the situations where the expert would have stopped.

## Technique 4: Contrast Pairs

Show two real cases — one the expert approved, one they rejected — and ask what differs. Experts articulate the boundary faster when comparing than when defining. If only one example exists, ask "what would make this one unacceptable?"

## Technique 5: The Spec Read-Back

After each round, read the drafted spec back and ask: "如果新人照这个做，第一个会错在哪？" (Where would a new hire first get this wrong?) The answer is the next interview question. Repeat until the expert runs out of deltas.

## The Question Bank (Round-by-round / 分轮提问清单)

### Round 1 — Happy path / 正常流程
1. 这件事由什么触发？（文件到达/会议结束/收到请求）What triggers this?
2. 输入有哪些？从哪来？哪些输入经常不完整？What inputs, and which are usually incomplete?
3. 一步步说，每步用什么工具/看什么材料？Steps, tools, and materials per step?
4. 最终交付物长什么样？给我一个你满意的成品。What does a finished output look like? Show me one you're proud of.
5. 哪一步花时间最多？哪一步最容易出废品？Which step is slowest? Where does scrap happen?

### Round 2 — Judgment layer / 判断层
6. 上次出问题是什么情况？怎么发现、怎么补救、事后改了什么？
7. 你看结果时最先看哪三处？每一处的"不对"长什么样？
8. 哪些情况你会退回不做？哪些要上报？
9. 你自己踩过的最大的坑是什么？新人最容易踩哪个？
10. 你的质量标准是什么？对照刚才那个成品逐条说。

### Round 3 — Transfer test / 移交测试
11. （把规格书递过去）新人照这个做，第一个会错在哪？
12. 有没有什么是"只能现场判断"的？——标记为已知限制
13. 这个流程多久变一次？谁有权改？改了之后这个技能谁维护？

## Common Interview Failure Modes

- **The expert narrates the official SOP.** Redirect: "上次你实际是这么走的吗？"
- **Everything is "experience".** Force contrast pairs (Technique 4); if that fails, log as known limitation.
- **Polished plausible answers.** Ask for the most recent concrete instance; specifics expose gaps.
- **Over-long interview, expert fatigues.** Three rounds max per session; resume in a second session rather than compressing.
- **The expert is too busy to approve the spec.** Do not proceed. An unapproved spec produces a confident, wrong skill — worse than no skill.
