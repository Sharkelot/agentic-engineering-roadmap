# Reading list

## Week 1 — Python and APIs

- [Python 3.12 documentation](https://docs.python.org/3.12/) — Reference for the language and standard library used to build the course client and deterministic local runner.
- [Python `asyncio`](https://docs.python.org/3.12/library/asyncio.html) — Core async/await concepts and APIs for concurrent I/O without introducing an external runtime.
- [HTTPX async support](https://www.python-httpx.org/async/) — Official guide to asynchronous HTTP requests, client lifecycle, and streaming; useful for the API-facing path.

## Week 2 — Schemas and data

- [Pydantic models](https://pydantic.dev/docs/validation/latest/concepts/models/) — Shows how typed models parse, validate, and serialize structured input; useful for defining support-case and result contracts.
- [Pydantic JSON Schema](https://pydantic.dev/docs/validation/latest/concepts/json_schema/) — Connects Python models to portable JSON Schema representations for inspecting and documenting data contracts.

## Week 3 — Evaluation design

- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — First-party design guidance on scoped objectives, representative test cases, combining metrics with human judgment, and iterative evaluation. Apply the methodology to synthetic cases and a local grader; the course need not use a paid API.
- [OpenAI Evals guide](https://developers.openai.com/api/docs/guides/evals) — Concrete example of separating a dataset schema from testing criteria and graders. Treat the hosted Evals API as an illustrative pattern, not a course dependency; the page notes platform deprecation.
- [NVIDIA NeMo Evaluator](https://docs.nvidia.com/nemo/evaluator/) — Relevant optional framework reference for benchmark environments, pluggable solvers, reports, and run comparisons. It is not required for this independent course or its deterministic local default.

## Week 4 — Metrics and regression

- [scikit-learn F1 score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html) — Primary scoring reference defining F1 as a harmonic mean of precision and recall, with averaging and zero-division conventions to consider when aggregating labeled outcomes.
- [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/) — Defines counters, gauges, histograms, and summaries for operational telemetry; complementary observability context, not an evaluation-scoring source.
- [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html) — Official method for applying the same assertions across explicit cases, a practical basis for repeatable regression checks over synthetic inputs.

## Week 5 — OpenTelemetry and tracing

- [OpenTelemetry Python instrumentation](https://opentelemetry.io/docs/languages/python/instrumentation/) — Walks through SDK setup and manual spans and metrics, suitable for tracing a local request/evaluation path.
- [OpenTelemetry Python libraries](https://opentelemetry.io/docs/languages/python/libraries/) — Covers automatic instrumentation for dependencies such as HTTPX, complementing explicit application spans.

## Week 6 — Orchestration and reliability

- [HTTPX async support](https://www.python-httpx.org/async/) — Practical reference for reusing async clients, managing their lifetime, and handling streamed responses in concurrent workflows.
- [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/) — Explains timeout behavior and configuration, useful for making network failure boundaries explicit rather than allowing stalled calls.
- [Python asyncio tasks](https://docs.python.org/3.12/library/asyncio-task.html) — Documents task creation, cancellation, and structured concurrency tools for coordinating asynchronous workflow steps.

## Week 7 — Docker, Kubernetes, and CI

- [Docker: What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) — Introduces the container as a runnable instance of an image and its isolation model, groundwork for packaging the local evaluator.
- [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) — Describes one-off workloads that run to completion, including retries and completion status; relevant to batch evaluation without assuming a cluster is needed locally.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) — Primary reference for configuring workflow triggers and jobs in YAML, supporting automated tests and regression checks in CI.

## Week 8 — Capstone and technical storytelling

- [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) — Explains how a README communicates purpose, usefulness, setup, help, and maintainership; use it to make the independent capstone reproducible and understandable.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) — Useful when presenting verifiable automated checks as part of the project’s evidence and reproducibility story.

Course explanations should be original; link rather than reproduce third-party documentation. This is an independent learning project using synthetic support cases; it is not affiliated with NVIDIA or any employer. The course should remain runnable locally with deterministic defaults and should not require paid services, accounts, or API keys.
