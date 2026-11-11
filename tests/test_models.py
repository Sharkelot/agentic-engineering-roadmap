from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from agent_eval_lab.models import EvidenceRef, MetricResult, RunManifest


def test_models_validate_extra_fields_score_and_utc() -> None:
    assert EvidenceRef(source_id="s1", excerpt="x").source_id == "s1"
    with pytest.raises(ValidationError):
        EvidenceRef(source_id="s1", excerpt="x", extra=1)
    with pytest.raises(ValidationError):
        MetricResult(name="m", value=1.1, status="scored", details={})
    fields = {"run_id": "r", "agent_version": "a", "dataset_version": "d", "metric_version": "m"}
    with pytest.raises(ValidationError):
        RunManifest(**fields, created_at=datetime(2026, 1, 1))
    RunManifest(**fields, created_at=datetime.now(UTC))
