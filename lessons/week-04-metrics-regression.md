# Week 4 — Metrics and regression

## Objectives
- Explain precision, recall, and F1 as measures over labeled positives.
- Calculate this repository's metric summary and compare compatible artifacts.
- Use explicitly didactic repeated-run scores to reason about dispersion, uncertainty, and toy-judge calibration.

## Prerequisites
- Weeks 1–3; basic set operations and familiarity with run artifacts.

## Read
- [scikit-learn F1 documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html) — primary scoring reference: F1 is the harmonic mean of precision and recall, with averaging choices that matter.
- [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/) — monitoring vocabulary; useful context, but not an evaluation-scoring recipe.
- [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html) — repeat assertions over explicit cases.
- [Week 3](week-03-evaluation-design.md), [reading map](../references/reading-list.md).

## Build
First compute a real repository metric summary without invoking an external agent: run `uv run agent-eval run --cases synthetic-data/support_cases.jsonl --out .cache/week-04-run`, then load that actual local artifact with `uv run python -c 'from pathlib import Path; from agent_eval_lab.artifacts import load_run; from agent_eval_lab.compare import summarize; print(summarize(load_run(Path(".cache/week-04-run"))))'`. Preserve the actual printed output in your notes and identify applicable/unscored counts. This uses the repository's deterministic local adapter on synthetic data, not a model evaluation or a real agent result. Do not invent CLI output.

Now use this **didactic synthetic example only — not model, repository, or observed run results**. A fictional binary judge is repeated across 5 fixed examples in three imagined runs. Positive label means the judge accepts an answer:

| Case | Synthetic human label | Run A | Run B | Run C |
|---|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 0 | 1 |
| 3 | 0 | 0 | 0 | 1 |
| 4 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 1 | 0 |

For each run calculate accuracy and the positive-class F1 against human labels, then calculate the range (max minus min) of each score across runs. State what this dispersion says and does not say about uncertainty; the five examples are not a population confidence interval. For the toy calibration check, group predictions by judge confidence: attach confidence 0.9 to positive calls and 0.8 to negative calls for all runs. Compare each confidence group with its empirical human-label acceptance rate, noting that confidence numbers are another stipulated synthetic teaching input, not actual judge outputs. Explain why calibration is distinct from accuracy and why five labels cannot establish reliable calibration. Never present any table value or computation here as an actual model result.

## Check your understanding
1. When do precision and recall trade off, and what does F1 summarize?
2. Why can a small repeated-run range fail to establish low uncertainty?
3. How does calibration against human labels differ from accuracy?

## Reflection
Which metric is actionable for your example, and what would its aggregate conceal?

## Done when
- [ ] You report an actual local repository metric or clearly identify the manual synthetic calculation and its source.
- [ ] The illustrative repeated-run table is labeled synthetic; you calculate scores and dispersion without presenting them as model results.
- [ ] You compare toy confidence groups with synthetic human-label rates and state the sample-size limitation.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
