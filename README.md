# Agentic Engineering Roadmap

An independent learning project; not affiliated with NVIDIA or any employer. This course uses synthetic support-agent scenarios only. Do not add employer, customer, confidential, or private project data or code.

## Course

See [ROADMAP.md](ROADMAP.md) for the eight-week plan. Lessons use deterministic local fixtures by default; no paid API, GPU, secret, account, or remote service is required.

## Local quickstart (Python 3.12)

```sh
python -m pip install -e '.[dev,local-http]'
python -m scripts.validate_course
python -m pytest
ruff check .
mypy src scripts
agent-eval run --cases synthetic-data/support_cases.jsonl --out ./artifacts/local-run
```

The commands read the checked-in synthetic dataset only. Choose a new output path for each run. `validate-course` is also installed as a console command.

## Docker

```sh
docker build -t agentic-engineering-roadmap:local .
mkdir -p artifacts
docker run --rm -v "$PWD/artifacts:/output" agentic-engineering-roadmap:local
```

The image is built from the repository `Dockerfile`, runs as a non-root user, and uses the deterministic adapter. `.dockerignore` excludes worktrees, development metadata, caches, and likely secret files.

## CI and optional Kubernetes exercise

CI on Python 3.12 installs `.[dev,local-http]` and runs pytest, Ruff, mypy on source/scripts, offline course validation, and a deterministic synthetic evaluation. Strict mypy targets `src scripts`; pytest runs the tests, but tests are not type-checked. It uses no credentials or remote model services.

For the optional Kubernetes Job, build the local image above, then apply `deploy/kubernetes/eval-job.yaml` to a cluster where that image is available. It writes to a temporary `emptyDir`; artifacts are ephemeral. This is an optional local exercise, not needed for the course; do not push to a registry or add credentials.

## References

Readings are linked in [references/reading-list.md](references/reading-list.md); explanations in lessons are original. No license is included.
