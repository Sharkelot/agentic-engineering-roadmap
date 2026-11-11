from agent_eval_lab.compare import compare_runs, summarize
from agent_eval_lab.models import EvaluationRun, MetricResult, RunManifest, TrialResult

NAMES = ("answer_term_support", "route_accuracy", "citation_f1", "safe_abstention", "expected_tool_success")


def run(run_id: str, *, dataset: str = "d1", version: str = "m1", score: float = 1.0,
        cases: tuple[str, ...] = ("c1", "c2")) -> EvaluationRun:
    manifest = RunManifest(run_id=run_id, agent_version="a1", dataset_version=dataset,
                           metric_version=version, created_at="2026-01-01T00:00:00Z")
    trials = [TrialResult(case_id=cid, status="completed", response=None,
        metrics=[MetricResult(name=name, value=score, status="scored", details={}) for name in NAMES], error=None)
        for cid in cases]
    return EvaluationRun(manifest=manifest, trials=trials, expected_total=len(cases))


def test_comparison_accepts_within_threshold_regression() -> None:
    report = compare_runs(run("b"), run("c", score=0.99), max_regression=0.02)
    assert report.passed
    assert abs(report.metrics[0].delta + 0.01) < 1e-9


def test_comparison_rejects_dataset_metric_versions_and_case_sets() -> None:
    for baseline, candidate, message in [
        (run("b"), run("c", dataset="d2"), "dataset"),
        (run("b"), run("c", version="m2"), "metric"),
        (run("b"), run("c", cases=("c1",)), "case"),
    ]:
        try:
            compare_runs(baseline, candidate)
        except ValueError as error:
            assert message in str(error)
        else:
            raise AssertionError(f"expected {message} mismatch")


def test_comparison_rejects_missing_metric_results() -> None:
    baseline = run("b")
    baseline.trials[0].metrics = []
    try:
        compare_runs(baseline, run("c"))
    except ValueError as error:
        assert "missing" in str(error)
    else:
        raise AssertionError("expected missing metric error")


def test_summary_includes_coverage_and_failed_zero() -> None:
    evaluation = run("r", cases=("c1",))
    evaluation.trials[0].status = "failed"
    evaluation.trials[0].metrics[0].value = 0.0
    evaluation.trials.append(TrialResult(case_id="c2", status="completed", response=None,
        metrics=[MetricResult(name="answer_term_support", value=1.0, status="scored", details={})], error=None))
    evaluation.expected_total = 2
    result = summarize(evaluation)
    item = result["metrics"]["answer_term_support"]
    assert result["failed"] == 1
    assert item == {"mean": 0.5, "applicable_count": 2, "scored_count": 2, "coverage": 1.0}
