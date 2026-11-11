# Week 4 — Metrics and regression

## Objectives
- Explain precision, recall, and F1 as measures over labeled positives.
- Compare compatible baseline and candidate runs without hiding unscored cases.

## Prerequisites
- Weeks 1–3; basic set operations and familiarity with run artifacts.

## Read
- [scikit-learn F1 documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html) — primary scoring reference: F1 is the harmonic mean of precision and recall, with averaging choices that matter.
- [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/) — monitoring vocabulary; useful context, but not an evaluation-scoring recipe.
- [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html) — repeat assertions over explicit cases.
- [Week 3](week-03-evaluation-design.md), [reading map](../references/reading-list.md).

## Build
Use synthetic baseline and candidate artifacts or inspect `score_trial` and `compare_runs` in the source. For citation F1, write down the required and returned source-ID sets, derive true positives and F1, then run `uv run agent-eval compare --baseline BASELINE_DIR --candidate CANDIDATE_DIR --max-regression 0.02` only when you have two compatible real artifact directories. The CLI exits 1 on a regression failure and 2 on invalid artifacts/arguments; do not invent a successful output. Note why unscored results are not zeros.

## Check your understanding
1. When do precision and recall trade off, and what does F1 summarize?
2. Why can zero-positive labels make a score convention-dependent?
3. Why must compared runs have matching dataset and metric versions?

## Reflection
Which metric is actionable for your example, and what would its aggregate conceal?

## Done when
- [ ] You derive an F1 value from a small synthetic set and state the averaging/zero-division caveat.
- [ ] You can distinguish evaluation scores from operational telemetry.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
