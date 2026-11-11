from datetime import UTC, datetime

from agent_eval_lab.adapters import DeterministicSupportAgent
from agent_eval_lab.compare import evaluate
from agent_eval_lab.models import EvalCase, RunManifest


def test_evaluate_runs_trials_and_attaches_metrics() -> None:
    case = EvalCase(case_id="c1", prompt="help", evidence=[], required_source_ids=[],
        expected_route="billing", expected_answer_terms=["refund"], expected_tool_names=[],
        should_abstain=False, dataset_version="d1")
    manifest = RunManifest(run_id="r1", agent_version="a1", dataset_version="d1",
        metric_version="m1", created_at=datetime.now(UTC))

    async def execute() -> None:
        result = await evaluate([case], DeterministicSupportAgent(), manifest=manifest)
        assert result.expected_total == 1
        assert result.trials[0].case_id == "c1"
        assert {metric.name for metric in result.trials[0].metrics} == {
            "answer_term_support", "route_accuracy", "citation_f1", "safe_abstention",
            "expected_tool_success",
        }
    import asyncio
    asyncio.run(execute())
