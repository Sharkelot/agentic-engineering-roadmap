# Design: Agentic Engineering Learning Repository

## Intent
Create a public GitHub course the learner can work through to build toward agent-evaluation/platform engineering roles such as agent-evaluation and platform engineering roles. Personalize the learning sequence to a learner's general interest in software systems and agent evaluation; keep the public course and capstone generic unless the user separately approves project links or attribution.

## Audience and starting point
For learners with existing technical or systems-building experience who want a Python-first path into agent evaluation, observability, reliability, and production deployment rather than a generic programming introduction.

## Approaches considered
1. **Public, hands-on course plus capstone (selected):** best portfolio signal and practical learning; requires careful use of synthetic data and public-safe examples.
2. Private hands-on course: safer for personal notes but less useful as an immediately shareable portfolio.
3. Public reading syllabus only: quickest to author, but weak practice and no runnable evidence.

## Goals
- Provide an 8-week, sequential lesson plan with outcomes, official/source-first readings, original notes, exercises, checks, and reflection prompts.
- Build a small Python agent-evaluation kit incrementally as the capstone.
- Teach Python SDK/API design, typed schemas, evaluation datasets/metrics, trace and artifact modeling, reliability, and containerized execution.
- Make the default path reproducible without paid APIs or a GPU; use deterministic mock agents and synthetic tickets. Make local OpenAI-compatible model use optional.
- Include progress tracking and knowledge checks that support retrieval practice and continued study.

## Non-goals / guardrails
- Do not copy employer, customer, internal, or other confidential data/code; capstone cases are synthetic.
- Do not name an employer or publish work artifacts, private project details, or portfolio links unless the user explicitly approves them; never publish secrets or credentials.
- Do not teach model training or CUDA as core requirements; they are not the main gap for this role.
- Do not claim the course guarantees a job or substitutes for the posting's professional-experience requirement.
- State that the repository is an independent learning project and is not affiliated with NVIDIA or any employer.
- Do not depend on a cloud account, paid API, or heavyweight NeMo install for the baseline exercises. NeMo Evaluator is an official reference and optional integration target.

## Proposed curriculum
1. **Baseline and Python SDK foundations:** typing, Pydantic, async, pytest, packaging, API contracts.
2. **Agent and evaluation data models:** tasks, datasets, run manifests, traces, tool calls, result schemas, validation.
3. **Evaluation design:** representative cases, task adapters, deterministic graders, RAG/citation and tool-use checks, safe abstention.
4. **Metrics and regression:** repeated runs, judge rubrics/calibration, uncertainty, baseline comparisons, CI gates.
5. **Observability:** OpenTelemetry spans/events, trace correlation, failure diagnostics, latency/cost fields, redaction.
6. **Ingestion and orchestration:** batch evaluation, concurrency, retries, idempotency, cancellation, sharding, resumability.
7. **Production packaging:** CLI and Python API, Docker, GitHub Actions, optional Kubernetes Job, artifacts and reports.
8. **Capstone demo and engineering communication:** end-to-end run, report, architecture/tradeoff note, and interview walkthrough.

Every lesson will include: objectives, prerequisites, source links, a concise original explanation, a hands-on task, a verifiable done checklist, a short retrieval quiz, and a reflection/next-step prompt.

## Capstone
A generic support-agent evaluation lab with synthetic ticket/evidence cases. Implement typed `Case`, `AgentAdapter`, `Trace`, `Metric`, and `Run` models; a deterministic baseline agent; evaluation metrics for resolution correctness, citation/evidence support, routing, safe abstention, tool success, latency, and failures; JSONL run artifacts; a compact report; and a CI regression check. Include an optional adapter for a locally hosted OpenAI-compatible agent endpoint. NeMo Evaluator can be explored as an optional interoperability exercise after the core runner works.

## Proposed repository
- Name: `agentic-engineering-roadmap` (check availability before creation).
- Owner: `Sharkelot`, confirmed by the user; verify the authenticated GitHub identity before publishing.
- Public visibility, as selected by the user.
- Suggested layout: `README.md`, `ROADMAP.md`, `lessons/`, `study-guides/`, `capstone/`, `synthetic-data/`, `progress/`, `references/`, `pyproject.toml`, `tests/`, and GitHub Actions CI.

## Success checks
- The README explains who the course is for, the 8-week order, and how to start/track progress.
- Every lesson has checked primary-source links and a testable exercise.
- The capstone runs locally with synthetic data and no secret/API key; tests and lint/type checks run in CI.
- The public repo contains no proprietary work data, secrets, or copied source material.
- GitHub owner, visibility, default branch, pushed commit, and CI result are read back and verified before reporting completion.

## Decisions still open
The name is a proposal, not guaranteed available. Before implementation, verify the GitHub account authenticated in `gh` matches `Sharkelot`, check the proposed name is unused, and use a different name only if it is unavailable.
