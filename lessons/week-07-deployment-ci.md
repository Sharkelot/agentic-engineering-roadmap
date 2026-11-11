# Week 7 — Docker, Kubernetes, and CI

## Objectives
- Distinguish local reproducibility, image packaging, batch scheduling, and automated checks.
- Inspect local CI/container artifacts and identify concrete validation evidence.
- Describe a minimal CI sequence; Kubernetes remains optional.

## Prerequisites
- Weeks 1–6; command-line use and basic test concepts.

## Read
- [Docker containers](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) — image/runtime concepts for packaging.
- [Kubernetes Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) — one-off workloads that run to completion; optional conceptual reading, no cluster required.
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) — workflow triggers and jobs.
- [Week 6](week-06-orchestration-reliability.md), [reading map](../references/reading-list.md).

## Build
Work from this repository's local artifacts; run `git status --short`, `find . -maxdepth 3 -type f \( -path './.github/workflows/*' -o -iname 'Dockerfile*' -o -name 'pyproject.toml' -o -name 'uv.lock' \) -print`, and inspect any workflow/container files found. Inspect `pyproject.toml` and `uv.lock` as packaging artifacts. Run the repository's actual local gates (`uv run --extra dev pytest -q`, `uv run ruff check .`, and `uv run mypy src`) and make a four-row evidence table: artifact/command, observed result, what it validates, and one limitation. Do not invent a workflow or claim remote CI ran if no local workflow is present. If no container definition exists, document that absence and sketch the minimal `Dockerfile` inputs it would require without building/publishing an image. Kubernetes is optional design context only; do not access a cluster or use paid infrastructure. Note any secret-like build input that should not enter source, logs, or an image.

## Check your understanding
1. What is the distinction between an image and a running container?
2. Which local artifact and command provide evidence that dependencies and tests are reproducible?
3. What must CI verify before a candidate is considered for comparison?

## Reflection
Which layer is necessary for your local project and which is merely a future deployment option?

## Done when
- [ ] Your evidence table cites inspected local artifacts and actual command output for the synthetic evaluation package, including unavailable artifacts as absent.
- [ ] You state that Kubernetes is optional and the course runs without paid infrastructure.
- [ ] Attempt the exercise and quiz before opening [answer hints](../solutions/README.md); ask follow-up questions as needed.
