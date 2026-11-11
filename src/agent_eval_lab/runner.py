import asyncio
from collections.abc import Sequence

from .adapters import AgentAdapter
from .models import EvalCase, TrialResult


async def run_agent_trials(
    cases: Sequence[EvalCase],
    adapter: AgentAdapter,
    *,
    max_concurrency: int = 4,
    timeout_seconds: float = 10.0,
) -> list[TrialResult]:
    if max_concurrency < 1:
        raise ValueError("max_concurrency must be at least 1")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than 0")

    semaphore = asyncio.Semaphore(max_concurrency)

    async def run_one(case: EvalCase) -> TrialResult:
        try:
            async with semaphore:
                response = await asyncio.wait_for(adapter.run(case), timeout=timeout_seconds)
            return TrialResult(case_id=case.case_id, status="completed", response=response, metrics=[], error=None)
        except TimeoutError:
            error = "Agent call timed out"
        except Exception as exc:  # noqa: BLE001 - adapter failures must not stop other trials
            error = "Agent call failed: " + type(exc).__name__
        return TrialResult(case_id=case.case_id, status="failed", response=None, metrics=[], error=error)

    return list(await asyncio.gather(*(run_one(case) for case in cases)))
