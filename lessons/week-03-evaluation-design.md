# Week 3 — Evaluation design

## Objectives
- Turn a product claim into observable criteria and representative test cases.
- Separate a dataset, a grader, and human review.

## Prerequisites
- Weeks 1–2; understanding of a case schema and deterministic run.

## Read
- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — first-party guidance on objectives, representative cases, and iterative evaluation; apply locally without a paid API.
- [Evals guide](https://developers.openai.com/api/docs/guides/evals) — an illustrative dataset/grader pattern only; the guide notes the hosted Evals API is deprecated. Reading only.
- [NeMo Evaluator](https://docs.nvidia.com/nemo/evaluator/) — optional framework comparison; no API key or framework required.
- [Week 2](week-02-schemas-data.md), [reading map](../references/reading-list.md).

## Build
Choose one synthetic support case and write a one-sentence quality objective, one observable pass/fail rule, and one limitation of that rule. Inspect `score_trial` in `src/agent_eval_lab/metrics.py`; relate the criterion to an existing deterministic metric or explain why it needs human judgment. Do not claim lexical matching proves semantic correctness.

## Check your understanding
1. How does a measurable criterion differ from a broad aspiration?
2. Why can a grader agree with itself and still be wrong?
3. When should human review complement an automated score?

## Reflection
What quality dimension does your chosen rule miss, and what evidence would help address that gap?

## Done when
- [ ] Your objective, rule, and limitation refer only to a synthetic case and are reviewable.
- [ ] You identify whether the rule is automated or needs human judgment.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
- [ ] No hosted evaluation service, paid API, or secret is required.
