from pydantic import BaseModel, ConfigDict
from .metrics import METRIC_NAMES
from .models import EvaluationRun


class MetricComparison(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    baseline: float
    candidate: float
    delta: float
    passed: bool


class ComparisonReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    baseline_run_id: str
    candidate_run_id: str
    metrics: list[MetricComparison]
    passed: bool


def summarize(run: EvaluationRun) -> dict[str, object]:
    completed = sum(trial.status == "completed" for trial in run.trials)
    values: dict[str, list[float]] = {}
    unscored: dict[str, int] = {}
    for trial in run.trials:
        for metric in trial.metrics:
            if metric.status == "scored":
                assert metric.value is not None
                values.setdefault(metric.name, []).append(metric.value)
            else:
                unscored[metric.name] = unscored.get(metric.name, 0) + 1
    metrics: dict[str, object] = {}
    for name in sorted(set(values) | set(unscored)):
        scores = values.get(name, [])
        unscored_count = unscored.get(name, 0)
        applicable = len(scores) + unscored_count
        metrics[name] = {"mean": sum(scores) / len(scores) if scores else None,
                         "applicable_count": applicable, "scored_count": len(scores),
                         "coverage": len(scores) / applicable if applicable else 0.0}
    return {"total": run.expected_total, "completed": completed,
            "failed": sum(trial.status == "failed" for trial in run.trials), "metrics": metrics}


def compare_runs(baseline: EvaluationRun, candidate: EvaluationRun, *,
                 max_regression: float = 0.02) -> ComparisonReport:
    if not 0.0 <= max_regression <= 1.0:
        raise ValueError("max_regression must be within [0.0, 1.0]")
    if baseline.manifest.dataset_version != candidate.manifest.dataset_version:
        raise ValueError("dataset version mismatch")
    if baseline.manifest.metric_version != candidate.manifest.metric_version:
        raise ValueError("metric version mismatch")
    baseline_trials = {trial.case_id: trial for trial in baseline.trials}
    candidate_trials = {trial.case_id: trial for trial in candidate.trials}
    if baseline_trials.keys() != candidate_trials.keys():
        raise ValueError("case set mismatch")
    baseline_values: dict[str, list[float]] = {name: [] for name in METRIC_NAMES}
    candidate_values: dict[str, list[float]] = {name: [] for name in METRIC_NAMES}
    for case_id in sorted(baseline_trials):
        baseline_trial, candidate_trial = baseline_trials[case_id], candidate_trials[case_id]
        b_metrics = {metric.name: metric for metric in baseline_trial.metrics}
        c_metrics = {metric.name: metric for metric in candidate_trial.metrics}
        if len(b_metrics) != len(baseline_trial.metrics) or len(c_metrics) != len(candidate_trial.metrics):
            raise ValueError(f"duplicate metric result for case {case_id}")
        for name in METRIC_NAMES:
            b_result, c_result = b_metrics.get(name), c_metrics.get(name)
            if b_result is None or c_result is None:
                raise ValueError(f"missing metric result {name} for case {case_id}")
            if b_result.status != c_result.status:
                raise ValueError(f"applicability mismatch for {name} case {case_id}")
            if b_result.status == "scored":
                assert b_result.value is not None and c_result.value is not None
                baseline_values[name].append(b_result.value)
                candidate_values[name].append(c_result.value)
    comparisons: list[MetricComparison] = []
    for name in METRIC_NAMES:
        b_values, c_values = baseline_values[name], candidate_values[name]
        if b_values:
            b_mean, c_mean = sum(b_values) / len(b_values), sum(c_values) / len(c_values)
            delta = c_mean - b_mean
            comparisons.append(MetricComparison(name=name, baseline=b_mean, candidate=c_mean,
                                                delta=delta, passed=delta >= -max_regression))
    return ComparisonReport(baseline_run_id=baseline.manifest.run_id,
                            candidate_run_id=candidate.manifest.run_id, metrics=comparisons,
                            passed=all(item.passed for item in comparisons))

