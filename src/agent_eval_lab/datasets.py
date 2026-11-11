import json
from pathlib import Path

from pydantic import ValidationError

from .models import EvalCase


def load_cases(path: Path) -> list[EvalCase]:
    """Load and validate JSON Lines evaluation cases with line-specific errors."""
    cases: list[EvalCase] = []
    seen: set[str] = set()
    try:
        stream = path.open(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read dataset {path}: {exc}") from exc
    with stream:
        for line_number, raw_line in enumerate(stream, start=1):
            if not raw_line.strip():
                raise ValueError(f"line {line_number}: blank rows are not allowed")
            try:
                data = json.loads(raw_line)
                case = EvalCase.model_validate(data)
            except (json.JSONDecodeError, ValidationError, TypeError) as exc:
                raise ValueError(f"line {line_number}: invalid evaluation case: {exc}") from exc
            if not case.case_id.strip():
                raise ValueError(f"line {line_number}: case_id must not be blank")
            if case.case_id in seen:
                raise ValueError(f"line {line_number}: duplicate case_id {case.case_id!r}")
            seen.add(case.case_id)
            cases.append(case)
    return cases
