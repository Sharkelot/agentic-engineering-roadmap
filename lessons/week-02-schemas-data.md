# Week 2 — Schemas and data contracts

## Objectives
- Describe how explicit schemas make evaluation inputs and outputs inspectable.
- Identify validation boundaries and the value of rejecting unknown fields.

## Prerequisites
- Week 1; familiarity with JSON and Python type annotations.

## Read
- [Pydantic models](https://pydantic.dev/docs/validation/latest/concepts/models/) — parsing and validating typed records.
- [Pydantic JSON Schema](https://pydantic.dev/docs/validation/latest/concepts/json_schema/) — deriving an interoperable contract.
- [Week 1](week-01-python-sdk.md), [course roadmap](../ROADMAP.md), and [reading map](../references/reading-list.md).

## Build
Inspect `src/agent_eval_lab/models.py` and `synthetic-data/support_cases.jsonl`. In a scratch copy of a synthetic case, remove a required field, add an unexpected field, then attempt loading it with the course loader or a small `EvalCase.model_validate` snippet. Keep original fixtures untouched; document which boundary rejects each change.

## Check your understanding
1. What does `extra="forbid"` protect against?
2. Why validate each JSONL row rather than trust it because it parses as JSON?
3. Which fields let a result be interpreted alongside its dataset?

## Reflection
Which invalid input was easiest to catch, and what contract would you add before extending the data model?

## Done when
- [ ] You correctly predict validation of the altered synthetic records and verify the result locally.
- [ ] Your notes identify a schema boundary and explain why it matters.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
- [ ] No private or confidential data is used.
