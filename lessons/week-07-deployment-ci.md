# Week 7 — Docker, Kubernetes, and CI

## Objectives
- Distinguish local reproducibility, image packaging, batch scheduling, and automated checks.
- Describe a minimal CI sequence that validates an evaluation change.

## Prerequisites
- Weeks 1–6; command-line use and basic test concepts.

## Read
- [Docker containers](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) — image/runtime concepts for packaging.
- [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) — one-off workloads that run to completion; optional conceptual reading, no cluster required.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) — workflow triggers and jobs.
- [Week 6](week-06-orchestration-reliability.md), [reading map](../references/reading-list.md).

## Build
Write a short deployment sketch for the local evaluator: a container image holds code/dependencies, a batch job runs fixed synthetic cases, and CI runs tests plus course validation before packaging. Identify one secret that should not be placed in source or image. No container build or Kubernetes cluster is required for this exercise.

## Check your understanding
1. What is the distinction between an image and a running container?
2. Why is a batch evaluation naturally modeled as a job?
3. What should CI verify before a candidate is considered for comparison?

## Reflection
Which layer is necessary for your local project and which is merely a future deployment option?

## Done when
- [ ] Your synthetic deployment sketch names image, job, and CI responsibilities.
- [ ] You state that Kubernetes is optional and the course runs without paid infrastructure.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
