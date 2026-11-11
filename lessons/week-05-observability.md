# Week 5 — OpenTelemetry and observability

## Objectives
- Distinguish a trace/span view of execution from a quality evaluation score.
- Identify useful boundaries for instrumentation while preserving privacy.

## Prerequisites
- Weeks 1–4; understand one run and its metrics.

## Read
- [OpenTelemetry Python instrumentation](https://opentelemetry.io/docs/languages/python/instrumentation/) — SDK setup and manual spans/metrics.
- [OpenTelemetry Python libraries](https://opentelemetry.io/docs/languages/python/libraries/) — automatic instrumentation options, including HTTPX.
- [Week 4](week-04-metrics-regression.md), [reading map](../references/reading-list.md).

## Build
Sketch a trace for one synthetic case: label stages for load, agent execution, and scoring, and list one duration or count that could aid diagnosis. Then review the source runner and adapter boundaries. Do not add instrumentation that exports data; the exercise is a design sketch and requires no collector.

## Check your understanding
1. What question does a trace answer that a quality metric does not?
2. Why are span boundaries useful for finding latency or failures?
3. What data should never be placed in telemetry attributes?

## Reflection
Which trace detail would help debugging, and how would you keep it data-minimal?

## Done when
- [ ] Your synthetic trace sketch has distinct stages and one diagnostic measure.
- [ ] You explain why instrumentation alone cannot establish answer quality.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
- [ ] No telemetry export, account, or confidential data is used.
