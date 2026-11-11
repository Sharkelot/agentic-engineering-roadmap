import json
import os
import tempfile
from pathlib import Path

from pydantic import ValidationError

from .compare import summarize
from .models import EvaluationRun


def write_run(run: EvaluationRun, output_dir: Path) -> None:
    output_dir = Path(output_dir)
    if output_dir.exists() or output_dir.is_symlink():
        raise FileExistsError(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.", dir=output_dir.parent))
    try:
        _write_json(temporary / "run.json", run.model_dump(mode="json", exclude={"trials"}))
        with (temporary / "trials.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
            for trial in run.trials:
                stream.write(json.dumps(trial.model_dump(mode="json"), sort_keys=True, allow_nan=False) + "\n")
        _write_json(temporary / "summary.json", summarize(run))
        os.rename(temporary, output_dir)
    except OSError as exc:
        if exc.errno == 39:
            raise FileExistsError(output_dir) from exc
        raise
    except BaseException:
        if temporary.exists():
            import shutil
            shutil.rmtree(temporary)
        raise


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def load_run(input_dir: Path) -> EvaluationRun:
    input_dir = Path(input_dir)
    try:
        manifest_run = json.loads((input_dir / "run.json").read_text(encoding="utf-8"))
        trials: list[object] = []
        with (input_dir / "trials.jsonl").open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                if not line.strip():
                    raise ValueError(f"blank trial row at line {line_number}")
                trials.append(json.loads(line))
        stored_summary = json.loads((input_dir / "summary.json").read_text(encoding="utf-8"))
        run = EvaluationRun.model_validate({**manifest_run, "trials": trials})
        computed_summary = summarize(run)
        if stored_summary != computed_summary:
            raise ValueError("summary does not match run artifacts")
        return run
    except (OSError, json.JSONDecodeError, ValidationError, TypeError, KeyError) as exc:
        raise ValueError(f"invalid run artifacts in {input_dir}: {exc}") from exc
