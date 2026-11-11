# Week 5 — OpenTelemetry and observability

## Objectives
- Distinguish a trace/span view of execution from a quality evaluation score.
- Identify useful boundaries for instrumentation while preserving privacy.
- Implement and test local redaction on synthetic trace attributes without exporting anything.

## Prerequisites
- Weeks 1–4; understand one run and its metrics.

## Read
- [OpenTelemetry Python instrumentation](https://opentelemetry.io/docs/languages/python/instrumentation/) — SDK setup and manual spans/metrics.
- [OpenTelemetry Python libraries](https://opentelemetry.io/docs/languages/python/libraries/) — automatic instrumentation options, including HTTPX.
- [Week 4](week-04-metrics-regression.md), [reading map](../references/reading-list.md).

## Build
Create `redaction_exercise.py` locally (do not commit it) with a function `redact_attributes(attributes: dict[str, str]) -> dict[str, str]`. On a synthetic attribute dictionary containing `case_id`, `stage`, `email`, `prompt`, and `api_key`, return a fresh dictionary that retains only `case_id` and `stage`; do not mutate the input. Replace removed values with no placeholder—omit those keys entirely. Add a local test that asserts the returned allowlisted values, absence of all sensitive keys and values, and unchanged input. Run `python -m pytest -q` on that local test. Do not write traces, configure an exporter/collector, or send any data. Delete the exercise file after checking it.

## Check your understanding
1. What question does a trace answer that a quality metric does not?
2. Why are span boundaries useful for finding latency or failures?
3. Why can allowlisting be safer than attempting to recognize every sensitive field name?

## Reflection
Which trace detail would help debugging, and how would you keep it data-minimal?

## Done when
- [ ] A local test proves redaction preserves allowed fields, removes private fields/values, and does not mutate input.
- [ ] You explain why instrumentation alone cannot establish answer quality.
- [ ] No data is exported, no telemetry exporter/collector is configured, and no confidential data is used; the local exercise file is deleted.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
