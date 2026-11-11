import asyncio

from agent_eval_lab.adapters import DeterministicSupportAgent
from agent_eval_lab.models import AgentResponse, EvalCase
from agent_eval_lab.runner import run_agent_trials


def case(case_id: str = "case-1") -> EvalCase:
    return EvalCase(
        case_id=case_id, prompt="Help", evidence=[], required_source_ids=["src1"],
        expected_route="billing", expected_answer_terms=["refund"],
        expected_tool_names=["lookup"], should_abstain=False, dataset_version="v1",
    )


def test_deterministic_agent_matches_case_expectations() -> None:
    async def run() -> None:
        result = await run_agent_trials([case()], DeterministicSupportAgent())
        assert len(result) == 1
        assert result[0].status == "completed"
        assert result[0].response is not None
        assert result[0].response.route == "billing"
        assert "refund" in result[0].response.answer
        assert result[0].response.citation_ids == ["src1"]
        assert [tool.name for tool in result[0].response.tool_calls] == ["lookup"]
        assert result[0].metrics == []
    asyncio.run(run())


def test_runner_bounds_concurrency_and_preserves_input_order() -> None:
    class Agent:
        active = 0
        peak = 0

        async def run(self, item: EvalCase) -> AgentResponse:
            self.active += 1
            self.peak = max(self.peak, self.active)
            await asyncio.sleep(0.01)
            self.active -= 1
            return await DeterministicSupportAgent().run(item)

    async def run() -> None:
        agent = Agent()
        results = await run_agent_trials([case(str(i)) for i in range(7)], agent, max_concurrency=2)
        assert agent.peak == 2
        assert [item.case_id for item in results] == [str(i) for i in range(7)]
    asyncio.run(run())


def test_timeout_and_exception_create_failed_results_and_continue() -> None:
    class Agent:
        async def run(self, item: EvalCase) -> AgentResponse:
            if item.case_id == "slow":
                await asyncio.sleep(0.05)
            if item.case_id == "bad":
                raise RuntimeError("private details")
            return await DeterministicSupportAgent().run(item)

    async def run() -> None:
        results = await run_agent_trials(
            [case("slow"), case("bad"), case("ok")], Agent(), timeout_seconds=0.01
        )
        assert [item.case_id for item in results] == ["slow", "bad", "ok"]
        assert [item.status for item in results] == ["failed", "failed", "completed"]
        assert results[0].response is None and results[0].error == "Agent call timed out"
        assert results[1].response is None and "private details" not in (results[1].error or "")
        assert all(item.metrics == [] for item in results)
    asyncio.run(run())


def test_invalid_concurrency_is_rejected() -> None:
    async def run() -> None:
        try:
            await run_agent_trials([case()], DeterministicSupportAgent(), max_concurrency=0)
        except ValueError:
            return
        raise AssertionError("expected ValueError")
    asyncio.run(run())
