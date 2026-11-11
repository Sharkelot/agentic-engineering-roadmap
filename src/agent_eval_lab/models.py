from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceRef(StrictModel):
    source_id: str
    excerpt: str


class EvalCase(StrictModel):
    case_id: str
    prompt: str
    evidence: list[EvidenceRef]
    required_source_ids: list[str]
    expected_route: str | None
    expected_answer_terms: list[str]
    expected_tool_names: list[str]
    should_abstain: bool
    dataset_version: str


class ToolCallRecord(StrictModel):
    name: str
    succeeded: bool
    error: str | None


class AgentResponse(StrictModel):
    answer: str
    route: str | None
    citation_ids: list[str]
    tool_calls: list[ToolCallRecord]
    abstained: bool
    latency_ms: float
    error: str | None


class MetricResult(StrictModel):
    name: str
    value: float | None
    status: Literal["scored", "unscored"]
    details: dict[str, str]

    @model_validator(mode="after")
    def check_value(self) -> "MetricResult":
        if self.status == "scored" and (self.value is None or not 0.0 <= self.value <= 1.0):
            raise ValueError("scored metric value must be within [0.0, 1.0]")
        if self.status == "unscored" and self.value is not None:
            raise ValueError("unscored metric value must be null")
        return self


class TrialResult(StrictModel):
    case_id: str
    status: Literal["completed", "failed"]
    response: AgentResponse | None
    metrics: list[MetricResult]
    error: str | None


class RunManifest(StrictModel):
    run_id: str
    agent_version: str
    dataset_version: str
    metric_version: str
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def require_aware_utc(cls, value: datetime) -> datetime:
        offset = value.utcoffset()
        if value.tzinfo is None or offset is None or offset.total_seconds() != 0:
            raise ValueError("created_at must be an aware UTC timestamp")
        return value


class EvaluationRun(StrictModel):
    manifest: RunManifest
    trials: list[TrialResult]
    expected_total: int = Field(ge=0)
