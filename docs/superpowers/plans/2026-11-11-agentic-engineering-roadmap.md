# Agentic Engineering Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a public, source-grounded 8-week agentic-engineering course and runnable synthetic evaluation capstone in `Sharkelot/agentic-engineering-roadmap`.

**Architecture:** A small Python package provides typed evaluation cases, an agent adapter protocol, a deterministic baseline, graders, run artifacts, and a CLI. Markdown lessons teach each piece; the default tests and example use synthetic data and no model endpoint, while an optional local OpenAI-compatible adapter can be exercised separately.

**Tech Stack:** Python 3.12, Pydantic v2, pytest, Ruff, mypy, argparse, optional httpx, Docker, GitHub Actions; optional Kubernetes Job manifest and NeMo Evaluator interoperability lesson.

**Spec:** `docs/superpowers/specs/2026-11-11-agentic-engineering-roadmap-design.md`

## Global Constraints

- Repository visibility: public; owner: `Sharkelot`; verify authenticated GitHub identity before creating or pushing.
- Use synthetic support-agent cases only; no employer, customer, internal, confidential, or private project data/code.
- Do not include employer names, portfolio links, or private project details in public materials unless the user separately approves them.
- Default capstone runs locally with deterministic fixtures and no paid API, GPU, or secret; the HTTP model adapter is optional and tested against a local mock.
- Do not add a repository license unless the user approves one; public visibility does not itself grant reuse rights.
- Keep all readings as links and original explanations; do not copy third-party documentation text.
- State that the repository is an independent learning project and is not affiliated with NVIDIA or any employer.
- Do not track or publish `.superpowers/` SDD ledgers, briefs, reports, or review diffs.

## Review Focus

1. Duplicate/blank case IDs or malformed JSONL must fail with a useful validation error, not silently overwrite or skip cases; test in Task 2.
2. Unknown or unsupported citation IDs must not count as supported evidence; test in Task 4.
3. An agent exception or timeout must be recorded as a failed trial with diagnostics while preserving run completeness; test in Task 3.
4. Missing metric results and failed trials must be counted in coverage and must not inflate aggregate scores; test in Task 4.
5. Baseline/candidate comparisons with different dataset versions or incompatible metric definitions must be refused with an actionable error; test in Task 4.

---

### Task 1: Repository foundation and course skeleton

**Files:**
- Create: `README.md`, `ROADMAP.md`, `pyproject.toml`, `.gitignore`
- Keep and verify: `docs/superpowers/specs/2026-11-11-agentic-engineering-roadmap-design.md` (already present in the approved planning baseline)
- Create: `lessons/_TEMPLATE.md`, `progress/CHECKLIST.md`, `references/reading-list.md`
- Create: `scripts/validate_course.py`, `tests/test_course_structure.py`

**Interfaces:** The lesson validator checks required headings (`Objectives`, `Read`, `Build`, `Check your understanding`, `Done when`) and validates that source references are present. It must not fetch the network during ordinary tests.

- [ ] Write failing tests for missing headings, missing readings, and a valid lesson file.
- [ ] Run `python -m pytest tests/test_course_structure.py -q`; confirm the missing-validator failures.
- [ ] Add package/test configuration for Python 3.12, Pydantic v2, pytest, Ruff, and mypy; do not add a license.
- [ ] Implement the validator and a lesson template; document the eight-week course, setup, privacy rules, and no-affiliation note in README/ROADMAP.
- [ ] Run `python -m pytest tests/test_course_structure.py -q` and `ruff check .`; confirm pass.
- [ ] Commit the foundation.

### Task 2: Typed cases, outputs, and dataset loading

**Files:**
- Create: `src/agent_eval_lab/models.py`, `src/agent_eval_lab/datasets.py`
- Create: `synthetic-data/support_cases.jsonl`, `synthetic-data/README.md`
- Modify: `pyproject.toml` to include the new `src/agent_eval_lab` package while preserving `scripts` imports.
- Modify: `.gitignore` to exclude `.superpowers/` and `.worktrees/`.
- Test: `tests/test_models.py`, `tests/test_datasets.py`, `tests/test_package_bootstrap.py`, `tests/test_public_data_disclaimer.py`

**Interfaces:** Define Pydantic v2 models with `ConfigDict(extra="forbid")`: `EvidenceRef(source_id: str, excerpt: str)`; `EvalCase(case_id: str, prompt: str, evidence: list[EvidenceRef], required_source_ids: list[str], expected_route: str | None, expected_answer_terms: list[str], expected_tool_names: list[str], should_abstain: bool, dataset_version: str)`; `ToolCallRecord(name: str, succeeded: bool, error: str | None)`; `AgentResponse(answer: str, route: str | None, citation_ids: list[str], tool_calls: list[ToolCallRecord], abstained: bool, latency_ms: float, error: str | None)`; `MetricResult(name: str, value: float | None, status: Literal["scored", "unscored"], details: dict[str, str])`, where scored values are in `[0.0, 1.0]`; `TrialResult(case_id: str, status: Literal["completed", "failed"], response: AgentResponse | None, metrics: list[MetricResult], error: str | None)`; `RunManifest(run_id: str, agent_version: str, dataset_version: str, metric_version: str, created_at: datetime)` with an aware UTC timestamp; and `EvaluationRun(manifest: RunManifest, trials: list[TrialResult], expected_total: int)`. `load_cases(path: Path) -> list[EvalCase]` reads JSONL and rejects blank/duplicate IDs and malformed rows with line-specific errors.

- [ ] Write tests for valid fixtures, blank/duplicate IDs, malformed JSON, unsupported fields, missing required data, package presence, and the synthetic-data disclaimer.
- [ ] In a disposable copy of the base commit with pytest provisioned, run only the package-presence and disclaimer tests; confirm assertion failures for the missing package/README, not a missing-test-runner or collection error.
- [ ] Implement models and JSONL loader with explicit validation messages; update setuptools discovery for the `src` package without breaking the validator package.
- [ ] Add `synthetic-data/README.md` identifying the fixture as synthetic and the repo as an independent project not affiliated with NVIDIA or any employer.
- [ ] Ensure internal SDD artifacts are not tracked; remove any accidentally tracked report from the unpublished history before later tasks proceed.
- [ ] Run `uv run --python 3.12 --extra dev python -m pytest tests/test_models.py tests/test_datasets.py tests/test_package_bootstrap.py tests/test_public_data_disclaimer.py -q` and `uv run --python 3.12 --extra dev mypy src/agent_eval_lab/models.py src/agent_eval_lab/datasets.py`; confirm pass.
- [ ] Commit typed domain and data loading.

### Task 3: Agent adapter and evaluation runner

**Files:**
- Create: `src/agent_eval_lab/adapters.py`, `src/agent_eval_lab/runner.py`
- Test: `tests/test_runner.py`

**Interfaces:** Define `class AgentAdapter(Protocol)` with `async def run(self, case: EvalCase) -> AgentResponse`; provide `DeterministicSupportAgent`. Signature: `async def run_agent_trials(cases: Sequence[EvalCase], adapter: AgentAdapter, *, max_concurrency: int = 4, timeout_seconds: float = 10.0) -> list[TrialResult]`. The semaphore caps concurrent calls; each input yields exactly one completed or failed `TrialResult` with `metrics=[]`. On error/timeout, record a sanitized error string and continue other cases; retries are out of scope for v1.

- [ ] Write tests for success, bounded concurrency, timeout, raised exception, and preservation of one result per input case.
- [ ] Run `uv run --python 3.12 --extra dev python -m pytest tests/test_runner.py -q`; confirm failures.
- [ ] Implement the protocol, deterministic adapter, timeout handling, and error capture.
- [ ] Run `uv run --python 3.12 --extra dev python -m pytest tests/test_runner.py -q` and `uv run --python 3.12 --extra dev mypy src/agent_eval_lab/adapters.py src/agent_eval_lab/runner.py`; confirm pass.
- [ ] Commit the runner.

### Task 4: Metrics, summaries, and regression comparisons

**Files:**
- Create: `src/agent_eval_lab/metrics.py`, `src/agent_eval_lab/compare.py`
- Modify: `src/agent_eval_lab/runner.py`
- Test: `tests/test_metrics.py`, `tests/test_compare.py`, `tests/test_evaluation.py`

**Interfaces:**

- `score_trial(case: EvalCase, response: AgentResponse | None) -> list[MetricResult]`.
- `async evaluate(cases: Sequence[EvalCase], adapter: AgentAdapter, *, manifest: RunManifest, max_concurrency: int = 4, timeout_seconds: float = 10.0) -> EvaluationRun`.
  - Execution: `runner.py` calls `run_agent_trials`, scores every trial, and returns `EvaluationRun`.
  - Failure handling: when a trial fails, return score `0.0` for every applicable metric and `unscored` only for metrics that do not apply to that case; include a short reason in `details`.
  - Safe abstention: score `1.0` iff `response.abstained == case.should_abstain`; a failed trial scores `0.0`.
- `summarize(run: EvaluationRun) -> dict[str, object]` lives in `compare.py` and returns total/completed/failed counts plus per-metric mean, applicable count, scored count, unscored count, and coverage.
  - Counts: `applicable_count` counts cases to which the metric applies, including failed trials scored as zero; `scored_count` counts numeric values; `unscored_count` counts non-applicable cases; `coverage = scored_count / run.expected_total`.
  - Validation: reject missing or duplicate metric results.
  - Comparison types: `MetricComparison(name: str, baseline: float, candidate: float, delta: float, passed: bool)` and `ComparisonReport(baseline_run_id: str, candidate_run_id: str, metrics: list[MetricComparison], passed: bool)`.
  - Comparison API: `compare_runs(baseline: EvaluationRun, candidate: EvaluationRun, *, max_regression: float = 0.02) -> ComparisonReport`.
  - Policy: compare only higher-is-better quality metrics; all scored values are finite and in `[0.0, 1.0]`, and a metric passes when candidate is no more than `max_regression` below baseline.
  - Metrics: expected-answer-term support (fraction of expected terms present after casefold/whitespace collapse; unscored if none are specified);
    route accuracy (casefold/strip exact match; unscored if no expected route);
    citation F1 against `required_source_ids` (unscored if none are required; unknown IDs are false positives; missing required citations are false negatives), safe-abstention correctness (exact boolean match on every case), and expected-tool F1 against successful tool names (unscored if no tools are expected).
  - Compare guards: matching dataset and metric versions, the same case set, and one result per applicable metric/case; status/applicability must match between runs. Missing results, invalid metric values, or no comparable scored metrics are errors. Failed applicable trials are zero-valued, not dropped.

- [ ] Write tests for valid/unknown citations, no citation, incorrect routing, both false-positive and false-negative abstention, expected-tool F1, failed trials scored as zero when applicable, unscored non-applicable cases, coverage/mean behavior, missing/duplicate results, invalid values, empty comparisons, and incompatible dataset/metric versions. Add an integration test that observes `runner.evaluate` call `run_agent_trials` and attach the expected metrics.
- [ ] Run `uv run --python 3.12 --extra dev python -m pytest tests/test_metrics.py tests/test_compare.py tests/test_evaluation.py -q`; confirm the expected failures.
- [ ] Implement deterministic graders, coverage-aware summaries, and comparison guards.
- [ ] Run `uv run --python 3.12 --extra dev python -m pytest tests/test_metrics.py tests/test_compare.py tests/test_evaluation.py -q`, `uv run --python 3.12 --extra dev ruff check src/agent_eval_lab tests`, and `uv run --python 3.12 --extra dev mypy src/agent_eval_lab`; confirm pass.
- [ ] Commit metrics and regression comparison.

### Task 5: Run artifacts and CLI

**Files:**
- Create: `src/agent_eval_lab/artifacts.py`, `src/agent_eval_lab/cli.py`
- Modify: `pyproject.toml`
- Test: `tests/test_artifacts.py`, `tests/test_cli.py`

**Interfaces:** `write_run(run: EvaluationRun, output_dir: Path) -> None` writes `run.json`, `trials.jsonl`, and `summary.json` atomically; `load_run(input_dir: Path) -> EvaluationRun` validates these artifacts before comparison. CLI commands: `agent-eval run --cases PATH --out DIR` and `agent-eval compare --baseline DIR --candidate DIR --max-regression FLOAT`; comparison exits 0 on pass and nonzero on a regression or incompatible run metadata.

- [ ] Write tests for artifact round-trip, output-directory behavior, malformed input, and CLI exit codes.
- [ ] Run the targeted tests; confirm failures.
- [ ] Implement atomic JSON/JSONL output and argparse entry point.
- [ ] Run tests and a deterministic sample command; inspect the produced artifacts.
- [ ] Commit artifacts and CLI.

### Task 6: Optional local HTTP adapter and operational behavior

**Files:**
- Create: `src/agent_eval_lab/http_adapter.py`
- Modify: `pyproject.toml`
- Test: `tests/test_http_adapter.py`

**Interfaces:** Optional `local-http` extra installs httpx. `OpenAICompatibleAdapter(base_url: str, model: str, timeout_seconds: float = 10.0)` targets a configurable local base URL, posting to `/chat/completions`; no API token or external network is required by the default suite. It maps one case to a user message and validates the response into `AgentResponse`. Tests use `httpx.MockTransport`, never a real model endpoint.

- [ ] Write tests using a mocked transport for valid output, malformed response, connection failure, and absent optional dependency.
- [ ] Run the targeted tests with and without the extra; confirm expected behavior.
- [ ] Implement the adapter and safe configuration examples using an obviously local URL.
- [ ] Run tests; confirm no real network call was made.
- [ ] Commit the optional adapter.

### Task 7: Eight source-grounded lessons and study materials

**Files:**
- Create: `lessons/week-01-python-sdk.md` through `lessons/week-08-capstone.md`
- Create: `study-guides/glossary.md`, `study-guides/evaluation-checklist.md`, `solutions/README.md`
- Modify: `references/reading-list.md`, `ROADMAP.md`, `progress/CHECKLIST.md`

**Interfaces:** Each lesson follows `lessons/_TEMPLATE.md`, includes primary-source links, a hands-on task, verifiable acceptance criteria, a retrieval quiz, and a reflection prompt. Put answer keys/hints under `solutions/` and tell learners to attempt tasks before opening them.

- [ ] Add lesson-structure tests for all eight weeks and verify every lesson has a reading, exercise, and done checklist.
- [ ] Run the course validator and tests; confirm failures for any incomplete lesson.
- [ ] Write lessons in the approved sequence: Python/API; schemas/data; evaluation design; metrics/regression; OpenTelemetry; orchestration/reliability; Docker/Kubernetes/CI; capstone/storytelling.
- [ ] Review each external link against official documentation and record the source in `references/reading-list.md`.
- [ ] Run the validator and test suite; confirm all lessons pass.
- [ ] Commit curriculum and study materials.

### Task 8: Container, CI, and optional Kubernetes exercise

**Files:**
- Create: `Dockerfile`, `.dockerignore`, `.github/workflows/ci.yml`, `deploy/kubernetes/eval-job.yaml`
- Modify: `README.md`, `ROADMAP.md`

- [ ] Add tests/assertions that the documented quickstart and sample dataset paths exist.
- [ ] Add CI steps for Python 3.12, pytest, Ruff, mypy, course validation, and deterministic sample evaluation; no secrets.
- [ ] Add a non-privileged container for the deterministic CLI and an optional Kubernetes Job manifest using the same image.
- [ ] Run local checks and `docker build` if Docker is available; validate the manifest structurally without requiring a live cluster.
- [ ] Commit deployment and CI materials.

### Task 9: Final review and GitHub publication

**Files:** all public repository files; remote `Sharkelot/agentic-engineering-roadmap` if available.

- [ ] Run the full test, lint, type-check, lesson-validation, and sample-evaluation commands.
- [ ] Scan staged files for likely secrets, employer/customer names, and private project paths; correct any finding before publishing.
- [ ] Scan the tracked tree and commit history for internal SDD artifacts (`.superpowers/`); remove them from the unpublished history before creating or pushing the public remote.
- [ ] Verify `gh auth status` and `gh api user --jq .login` identify `Sharkelot`; check that the proposed public repository name is available. If authentication cannot be verified, stop and ask the user to connect GitHub.
- [ ] Create the public remote, push `main`, and verify the exact repository URL, visibility, pushed commit, and CI run by reading them back.
- [ ] Report the repo URL, course contents, verification results, and any remaining blockers.
