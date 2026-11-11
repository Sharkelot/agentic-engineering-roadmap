import json
import subprocess
import sys
from pathlib import Path

from agent_eval_lab.artifacts import load_run, write_run
from agent_eval_lab.models import EvalCase


def write_cases(path: Path, *, route: str = "support", terms: list[str] | None = None) -> None:
    case = EvalCase(case_id="c1", prompt="Help", evidence=[], required_source_ids=[],
                    expected_route=route, expected_answer_terms=terms if terms is not None else ["answer"],
                    expected_tool_names=[], should_abstain=False, dataset_version="d1")
    path.write_text(case.model_dump_json() + "\n")


def invoke(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "agent_eval_lab.cli", *args],
                          capture_output=True, text=True, check=False)


def test_cli_run_then_compare_emits_json_and_pass_exit_code(tmp_path: Path) -> None:
    cases, baseline, candidate = tmp_path / "cases.jsonl", tmp_path / "base", tmp_path / "candidate"
    write_cases(cases)
    for out in (baseline, candidate):
        result = invoke("run", "--cases", str(cases), "--out", str(out))
        assert result.returncode == 0, result.stderr
        assert json.loads((out / "summary.json").read_text())["total"] == 1
    comparison = invoke("compare", "--baseline", str(baseline), "--candidate", str(candidate),
                        "--max-regression", "0.02")
    assert comparison.returncode == 0
    assert json.loads(comparison.stdout)["passed"] is True


def test_cli_compare_regression_and_invalid_artifact_exit_codes(tmp_path: Path) -> None:
    cases, baseline, candidate = tmp_path / "cases.jsonl", tmp_path / "base", tmp_path / "candidate"
    write_cases(cases)
    assert invoke("run", "--cases", str(cases), "--out", str(baseline)).returncode == 0
    assert invoke("run", "--cases", str(cases), "--out", str(candidate)).returncode == 0

    # Lower a scored metric while preserving a valid, internally consistent bundle.
    candidate_run = load_run(candidate)
    trial = candidate_run.trials[0]
    lowered_metrics = [
        metric.model_copy(update={"value": 0.0}) if metric.name == "answer_term_support" else metric
        for metric in trial.metrics
    ]
    regressed_run = candidate_run.model_copy(
        update={"trials": [trial.model_copy(update={"metrics": lowered_metrics})]}
    )
    regressed_candidate = tmp_path / "regressed-candidate"
    write_run(regressed_run, regressed_candidate)
    result = invoke("compare", "--baseline", str(baseline), "--candidate", str(regressed_candidate),
                    "--max-regression", "0.0")
    assert result.returncode == 1

    # Malformed artifacts are an independent input-validation failure.
    invalid_candidate = tmp_path / "invalid-candidate"
    write_run(candidate_run, invalid_candidate)
    (invalid_candidate / "trials.jsonl").write_text("not-json\n")
    result = invoke("compare", "--baseline", str(baseline), "--candidate", str(invalid_candidate),
                    "--max-regression", "0.02")
    assert result.returncode == 2
