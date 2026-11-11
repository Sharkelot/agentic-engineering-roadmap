# Answer hints

Try each lesson's exercise and three retrieval questions before reading this file. These are reasoning prompts, not hidden execution results; verify commands and code behavior locally. Examples refer only to synthetic course data.

## Week 1 — Python and API clients
- The dataset loader validates rows and unique IDs; `asyncio.run` owns the async entry point. Artifact metadata makes results interpretable over time.
- A successful run writes `run.json`, `trials.jsonl`, and `summary.json`; the run ID and output directory are generated, so do not assume fixed values.

## Week 2 — Schemas and data contracts
- `extra="forbid"` rejects unknown fields, while required fields and Pydantic types reject malformed records. JSON syntax alone does not establish a valid case.
- Dataset and metric versions help constrain meaningful comparisons.

## Week 3 — Evaluation design
- A useful objective names an observable behavior and a case population. A deterministic grader can consistently implement a flawed proxy; human review and iteration address gaps.
- The hosted Evals material is optional reading; no service or credential is needed.

- A concrete Week 3 mapping pairs required IDs with `citation_f1`, successful expected tool names with `expected_tool_success`, and the abstention label with `safe_abstention`; these are deterministic proxies, not semantic verification.
- The Week 4 repeated-run table and its human labels/confidence inputs are explicitly didactic synthetic values. Ranges over five examples are not a population uncertainty estimate; calibration compares confidence groups with observed label frequencies and needs more evidence.
- For redaction, return an allowlisted copy of synthetic attributes and assert private fields/values are absent while the source mapping stays unchanged; never configure an exporter.
- For sets, precision = TP/(TP+FP), recall = TP/(TP+FN), and F1 = 2TP/(2TP+FP+FN), subject to the documented zero-division and averaging convention.
- This repository's citation F1 uses required source IDs and returned IDs. Unscored means not applicable, not a failure/zero. The compare command requires actual compatible run directories and returns a regression status; never invent its report.
- Prometheus types describe telemetry, not classification scoring.

## Week 5 — OpenTelemetry
- Traces describe execution flow and timing; evaluation metrics describe measured behavior against criteria. Avoid prompts, personal data, secrets, and raw sensitive content in telemetry.

## Week 6 — Orchestration and reliability
- Timeouts bound waiting; cancellation may affect outstanding tasks. Failed trials should stay visible and separate from completed-trial quality scores.
- Check actual runner behavior before asserting details; local mock tests are the safe HTTP exercise.

## Week 7 — Docker, Kubernetes, and CI
- An image is a packaged template; a container is a running instance. Jobs model bounded batch work. CI should run tests and structural validation against the candidate change.
- Deployment technologies are conceptual options; nothing paid or clustered is required.

## Week 8 — Capstone
- Reproducible commands, inputs, artifact definitions, and checks help others inspect a project. Without compatible real baseline artifacts, make no regression claim.
- Put limitations beside evidence; scores alone do not prove semantic quality.

## Further study
Ask follow-up questions when an answer depends on implementation details; use the source code, official reading links, and actual local outputs rather than guessing.
