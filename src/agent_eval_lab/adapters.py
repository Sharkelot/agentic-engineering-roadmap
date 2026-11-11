from typing import Protocol

from .models import AgentResponse, EvalCase, ToolCallRecord


class AgentAdapter(Protocol):
    async def run(self, case: EvalCase) -> AgentResponse: ...


class DeterministicSupportAgent:
    async def run(self, case: EvalCase) -> AgentResponse:
        return AgentResponse(
            answer=" ".join(case.expected_answer_terms),
            route=case.expected_route,
            citation_ids=list(case.required_source_ids),
            tool_calls=[ToolCallRecord(name=name, succeeded=True, error=None) for name in case.expected_tool_names],
            abstained=case.should_abstain,
            latency_ms=0.0,
            error=None,
        )
