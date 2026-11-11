# Week 1 — Python and API clients

## Objectives
- Explain the request/response boundary and why an evaluation client separates data loading, execution, and reporting.
- Run a deterministic local evaluation from the command line.

## Prerequisites
- Python 3.12, a terminal, and the repository checkout.

## Read
- [Python 3.12 documentation](https://docs.python.org/3.12/) — language and standard-library reference.
- [Python asyncio](https://docs.python.org/3.12/library/asyncio.html) — async I/O concepts used by the runner.
- [HTTPX async support](https://www.python-httpx.org/async/) — optional local HTTP adapter reference.
- [Course roadmap](../ROADMAP.md) and [reading map](../references/reading-list.md).

## Build
Install the project with its development extra (`uv sync --extra dev` if using uv), then run `uv run agent-eval run --cases synthetic-data/support_cases.jsonl --out /tmp/week1-run`. Inspect the created run manifest, trial rows, and summary. The built-in adapter is deterministic; no network service is used. Do not reuse the output directory.

## Check your understanding
1. Which module loads and validates JSONL cases, and why should it reject duplicate IDs?
2. What does `asyncio.run` do at the CLI boundary?
3. Why does an evaluation artifact record dataset and metric versions?

## Reflection
Which boundary made the run easiest to inspect? What would you investigate next about async execution?

## Done when
- [ ] The local command completes and produces `run.json`, `trials.jsonl`, and `summary.json`.
- [ ] You can point to the synthetic input and explain that no paid API is needed.
- [ ] You attempted the exercise and quiz before opening [answer hints](../solutions/README.md).
- [ ] Ask follow-up questions about any unclear step.
