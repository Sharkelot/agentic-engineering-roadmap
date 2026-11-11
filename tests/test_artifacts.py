import json
from pathlib import Path

import pytest

from agent_eval_lab.artifacts import load_run, write_run
from agent_eval_lab.metrics import METRIC_NAMES
from agent_eval_lab.models import EvaluationRun, MetricResult, RunManifest, TrialResult


def sample() -> EvaluationRun:
    return EvaluationRun(
        manifest=RunManifest(run_id="r1", agent_version="a", dataset_version="d",
                             metric_version="1.0", created_at="2026-01-01T00:00:00Z"),
        trials=[TrialResult(case_id="c1", status="completed", response=None, error=None,
        metrics=[MetricResult(name=name, value=1.0, status="scored", details={}) for name in METRIC_NAMES])],
        expected_total=1,
    )


def test_artifacts_round_trip(tmp_path: Path) -> None:
    destination = tmp_path / "run"
    write_run(sample(), destination)
    assert load_run(destination) == sample()
    assert {p.name for p in destination.iterdir()} == {"run.json", "trials.jsonl", "summary.json"}


def test_write_run_refuses_existing_directory_without_modifying_it(tmp_path: Path) -> None:
    destination = tmp_path / "run"
    destination.mkdir()
    marker = destination / "keep"
    marker.write_text("kept")
    with pytest.raises(FileExistsError):
        write_run(sample(), destination)
    assert marker.read_text() == "kept"


def test_load_run_rejects_malformed_or_inconsistent_artifacts(tmp_path: Path) -> None:
    destination = tmp_path / "run"
    write_run(sample(), destination)
    (destination / "trials.jsonl").write_text("not-json\n")
    with pytest.raises(ValueError):
        load_run(destination)
    (destination / "trials.jsonl").write_text(json.dumps(sample().trials[0].model_dump(mode="json")) + "\n")
    (destination / "summary.json").write_text("{}")
    with pytest.raises(ValueError):
        load_run(destination)
