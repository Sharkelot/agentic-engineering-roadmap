# Evaluation checklist

Use this before trusting or sharing a run report. The checklist is a review aid, not a claim that any one score establishes quality.

## Define
- [ ] State the user-facing objective and the decision this evaluation informs.
- [ ] Tie each metric to a criterion; document known blind spots and use human review where needed.
- [ ] Keep inputs synthetic and version the dataset, agent, and metric definitions.

## Validate the run
- [ ] Confirm expected case count, unique case IDs, and explicit failed-trial count.
- [ ] Preserve unscored applicability separately from scored zeroes.
- [ ] Check artifact schema, metric names, ranges, and reproducibility.
- [ ] Compare only runs with matching dataset and metric versions and the same case set.

## Interpret and share
- [ ] Report coverage and failures beside averages; do not hide missingness.
- [ ] State threshold and regression outcome only when based on actual compatible artifacts.
- [ ] Treat lexical checks as proxies, not semantic truth; review representative examples.
- [ ] Include no employer/customer/internal/private project data, secrets, or real user records.
- [ ] State limitations and provide commands another learner can run locally.

See [glossary](glossary.md), [Week 3 evaluation design](../lessons/week-03-evaluation-design.md), and [Week 4 metrics](../lessons/week-04-metrics-regression.md).
