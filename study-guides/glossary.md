# Glossary

- **Agent** — a program that selects actions or tool calls to respond to an input.
- **Baseline** — a recorded reference run used for comparison with a candidate.
- **Case** — one input plus evidence, expected properties, and version metadata in the synthetic dataset.
- **Calibration** — agreement between predicted confidence levels and observed outcome frequencies; it is not the same as accuracy, and small samples are weak evidence.
- **Dispersion** — variation among scores, such as the range across repeated runs; it describes observed variation, not by itself a confidence interval.
- **Idempotency key** — stable identifier used to avoid duplicating work/results when a request or run is retried or resumed.
- **Safe abstention** — withholding an unsupported answer when the case requires abstaining; this course's grader checks the response flag, not semantic safety.
- **Citation F1** — harmonic mean of precision and recall over required versus returned source IDs in this course's deterministic scorer; not semantic citation quality.
- **Dataset version** — identifier for the case collection used by a run.
- **Evaluation** — systematic measurement against explicit criteria and cases.
- **Metric** — a defined numeric or categorical measurement with a scope and limitations.
- **Observability** — evidence about system behavior, such as traces and latency, used to diagnose execution.
- **Regression threshold** — tolerated decrease in a metric during baseline/candidate comparison.
- **Schema** — a machine-readable contract for valid data shape and constraints.
- **Synthetic data** — fictional constructed examples, not copied from real customers or private systems.
- **Unscored** — metric not applicable to a case; distinct from a zero score.
