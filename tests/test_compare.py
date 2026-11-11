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
        metrics=[MetricResult(name=name, value=(1.0 if name == "answer_term_support" else None), status=("scored" if name == "answer_term_support" else "unscored"), details={}) for name in NAMES], error=None))
    evaluation.expected_total = 2
    result = summarize(evaluation)
    item = result["metrics"]["answer_term_support"]
    assert result["failed"] == 1
    assert item == {"mean": 0.5, "applicable_count": 2, "scored_count": 2, "unscored_count": 0, "coverage": 1.0}


def test_summary_nonapplicable_count_is_unscored_and_coverage_uses_dataset_total() -> None:
    evaluation=run("r",cases=("c1",))
    evaluation.trials[0].metrics[0].status="unscored"
    evaluation.trials[0].metrics[0].value=None
    evaluation.trials[0].metrics = [MetricResult(name=name, value=None, status="unscored", details={}) if name == "answer_term_support" else metric for name, metric in zip(NAMES, evaluation.trials[0].metrics)]
    evaluation.trials.append(TrialResult(case_id="c2", status="completed", response=None, metrics=[MetricResult(name=name, value=None, status="unscored", details={}) for name in NAMES], error=None))
    evaluation.expected_total=2
    item=summarize(evaluation)["metrics"]["answer_term_support"]
    assert item == {"mean":None,"applicable_count":0,"scored_count":0,"unscored_count":2,"coverage":0.0}

def test_comparison_rejects_invalid_values_and_no_comparable_scores() -> None:
    bad=run("b"); bad.trials[0].metrics[0].value=1.5
    try: compare_runs(bad,run("c"))
    except ValueError: pass
    else: raise AssertionError("invalid value accepted")
    empty=run("e")
    for t in empty.trials:
        for m in t.metrics: m.status="unscored"; m.value=None
    try: compare_runs(empty,empty.model_copy(update={"manifest":empty.manifest.model_copy(update={"run_id":"e2"})}))
    except ValueError: pass
    else: raise AssertionError("empty comparison accepted")


def test_comparison_allows_matching_unscored_but_rejects_applicability_mismatch() -> None:
    baseline = run("b", cases=("c1",))
    candidate = run("c", cases=("c1",))
    for trial in (baseline.trials[0], candidate.trials[0]):
        trial.metrics[0].status = "unscored"
        trial.metrics[0].value = None
    compare_runs(baseline, candidate)
    candidate.trials[0].metrics[0].status = "scored"
    candidate.trials[0].metrics[0].value = 1.0
    try:
        compare_runs(baseline, candidate)
    except ValueError as error:
        assert "applicability" in str(error)
    else:
        raise AssertionError("applicability mismatch accepted")


def test_summary_rejects_missing_and_duplicate_metrics() -> None:
    evaluation = run("r", cases=("c1",))
    evaluation.trials[0].metrics.pop()
    try:
        summarize(evaluation)
    except ValueError as error:
        assert "missing" in str(error)
    else:
        raise AssertionError("missing metric accepted")
    evaluation = run("dup", cases=("c1",))
    evaluation.trials[0].metrics.append(evaluation.trials[0].metrics[0].model_copy())
    try:
        summarize(evaluation)
    except ValueError as error:
        assert "duplicate" in str(error)
    else:
        raise AssertionError("duplicate metric accepted")
