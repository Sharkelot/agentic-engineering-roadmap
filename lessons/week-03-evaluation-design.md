# Week 3 — Evaluation design

## Objectives
- Turn a product claim into observable criteria and representative test cases.
- Map citation/RAG evidence, required tool calls, and safe abstention to existing graders.
- Separate a dataset, a grader, and human review.

## Prerequisites
- Weeks 1–2; understanding of a case schema and deterministic run.

## Read
- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — first-party guidance on objectives, representative cases, and iterative evaluation; apply locally without a paid API.
- [Evals guide](https://developers.openai.com/api/docs/guides/evals) — an illustrative dataset/grader pattern only; the guide notes the hosted Evals API is deprecated. Reading only.
- [NeMo Evaluator](https://docs.nvidia.com/nemo/evaluator/) — optional framework comparison; no API key or framework required.
- [Week 2](week-02-schemas-data.md), [reading map](../references/reading-list.md).

## Build
Using only synthetic cases in `synthetic-data/support_cases.jsonl`, choose one case with required source IDs, one with expected tools, and one with `should_abstain=true`. For each, make a response fixture from the case schema and write a three-column mapping: expected evidence/behavior, response field to inspect, grader in `src/agent_eval_lab/metrics.py`. Map source IDs to `citation_f1`, successful required tool names to `expected_tool_success`, and the abstention flag to `safe_abstention`. Run `uv run python -c 'from pathlib import Path; from agent_eval_lab.datasets import load_cases; print(len(load_cases(Path("synthetic-data/support_cases.jsonl"))))'` to verify the dataset loads; inspect the grader to confirm your mapping. Add one counterexample where lexical matching can pass despite unsupported meaning, and state what human review must check. Do not call a model or service.

## Check your understanding
1. How does a measurable criterion differ from a broad aspiration?
2. Why can a grader agree with itself and still be wrong?
3. Which existing grader checks required tool success, and what does it miss?

## Reflection
What quality dimension does your chosen rule miss, and what evidence would help address that gap?

## Done when
- [ ] The three synthetic examples map evidence, response fields, and existing graders accurately.
- [ ] You give a lexical false-positive counterexample and a human-review criterion.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
- [ ] No hosted evaluation service, paid API, or secret is required.
