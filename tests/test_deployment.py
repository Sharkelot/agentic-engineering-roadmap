import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_readme_quickstart_paths_exist() -> None:
    readme = (ROOT / "README.md").read_text()
    assert "synthetic-data/support_cases.jsonl" in readme
    assert (ROOT / "synthetic-data/support_cases.jsonl").exists()
    assert "python -m scripts.validate_course" in readme
    assert "Dockerfile" in readme


def test_course_validator_cli() -> None:
    result = subprocess.run([sys.executable, "-m", "scripts.validate_course"], check=False, cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "valid" in result.stdout.lower()


def test_workflow_contains_required_checks_and_no_secrets() -> None:
    path = ROOT / ".github/workflows/ci.yml"
    text = path.read_text().lower()
    workflow = yaml.safe_load(text)
    assert workflow["jobs"]["test"]["steps"]
    for check in ("pytest", "ruff", "mypy src scripts", "validate_course", "agent-eval"):
        assert check in text
    assert "3.12" in text
    assert "python -m pip install -e '.[dev,local-http]'" in text
    assert not any(word in text for word in ("api_key", "api-key", "secrets.", "password:"))


def test_dockerfile_runs_nonroot() -> None:
    dockerfile = (ROOT / "Dockerfile").read_text()
    assert "python:3.12-slim" in dockerfile
    assert "USER " in dockerfile
    assert "agent-eval" in dockerfile


def test_kubernetes_job_structure() -> None:
    job = yaml.safe_load((ROOT / "deploy/kubernetes/eval-job.yaml").read_text())
    assert job["kind"] == "Job"
    pod = job["spec"]["template"]["spec"]
    container = pod["containers"][0]
    assert container["image"] == "agentic-engineering-roadmap:local"
    assert container["volumeMounts"]
    assert pod["securityContext"]["runAsNonRoot"] is True
    assert pod["securityContext"]["fsGroup"] == 10001
    assert not any(key in container for key in ("envFrom", "env"))
    assert "emptyDir" in pod["volumes"][0]
