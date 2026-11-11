# Week 6 — Orchestration and reliability

## Objectives
- Explain how concurrency, timeouts, cancellation, and client lifecycle affect an evaluation run.
- Design failure handling that distinguishes a failed trial from a low score.
- Apply retry, idempotency, cancellation, sharding, and resumability concepts to the actual local runner; retries are not v1 implementation scope.

## Prerequisites
- Weeks 1 and 5; basic async/await and run artifact structure.

## Read
- [HTTPX async support](https://www.python-httpx.org/async/) — client lifecycle and async request patterns.
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/) — explicit bounds on network waits.
- [Python asyncio tasks](https://docs.python.org/3.12/library/asyncio-task.html) — tasks, cancellation, and structured concurrency.
- [Week 5](week-05-observability.md), [reading map](../references/reading-list.md).

## Build
Inspect `src/agent_eval_lab/runner.py`, `artifacts.py`, and relevant runner/artifact tests. Produce a concrete change design against these actual functions and artifact fields (no code changes):
1. Mark the current trial execution and persistence boundary. Propose retry only for transient adapter failures, with a bounded attempt count and visible attempt metadata; explicitly keep this out of v1.
2. Define a deterministic idempotency key from run ID and case ID so resuming a run cannot append a duplicate trial. Name where uniqueness is checked.
3. Trace cancellation from a user/task cancel through in-flight tasks, recording unfinished trials as interrupted rather than silently losing expected-total accounting.
4. Define a stable shard function using case ID and shard count; show which fields ensure shards cover each case exactly once.
5. Specify a resume command/input and how it loads compatible prior artifacts, skips completed cases, and preserves manifest/dataset/metric versions.

For each item cite the actual function or test that would change, plus one test assertion that would verify it. Do not implement retries or contact a live service. Verify your references with `rg -n 'run_agent_trials|evaluate|write_run|case_id|expected_total' src/agent_eval_lab tests`.

## Check your understanding
1. Why bound a network call with a timeout?
2. How should an idempotency key prevent duplicate persisted results during resume?
3. Why must canceled or failed trials remain visible in total and failure reporting?

## Reflection
Which reliability failure would most distort your evaluation if it disappeared from the report?

## Done when
- [ ] Your synthetic failure-flow/design table cites actual runner/artifact functions and specifies a test assertion for each reliability concern.
- [ ] Retry handling is explicitly marked out of v1 scope; cancellation, sharding, and resume retain expected trial accounting.
- [ ] No source changes or external service calls are made.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
