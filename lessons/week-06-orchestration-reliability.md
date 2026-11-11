# Week 6 — Orchestration and reliability

## Objectives
- Explain how concurrency, timeouts, cancellation, and client lifecycle affect an evaluation run.
- Design failure handling that distinguishes a failed trial from a low score.

## Prerequisites
- Weeks 1 and 5; basic async/await and run artifact structure.

## Read
- [HTTPX async support](https://www.python-httpx.org/async/) — client lifecycle and async request patterns.
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/) — explicit bounds on network waits.
- [Python asyncio tasks](https://docs.python.org/3.12/library/asyncio-task.html) — tasks, cancellation, and structured concurrency.
- [Week 5](week-05-observability.md), [reading map](../references/reading-list.md).

## Build
Inspect `src/agent_eval_lab/runner.py` and the HTTP adapter. Draw the path when one case succeeds and one fails; annotate where errors are captured and how total expected trials remain visible. If exercising HTTP, use only the local mock fixture documented by its tests; do not contact a live service.

## Check your understanding
1. Why bound a network call with a timeout?
2. What can cancellation change about sibling tasks?
3. Why report failed trials separately from metric averages?

## Reflection
What reliability failure would most distort your evaluation if it disappeared from the report?

## Done when
- [ ] Your synthetic failure-flow sketch identifies timeout/cancellation and artifact behavior.
- [ ] You explain why a failed run is not equivalent to a poor quality score.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
