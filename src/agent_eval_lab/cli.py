import argparse
import asyncio
import json
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError

from .adapters import DeterministicSupportAgent
from .artifacts import load_run, write_run
from .compare import compare_runs
from .datasets import load_cases
from .models import RunManifest
from .runner import evaluate


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-eval")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--cases", type=Path, required=True)
    run.add_argument("--out", type=Path, required=True)
    compare = commands.add_parser("compare")
    compare.add_argument("--baseline", type=Path, required=True)
    compare.add_argument("--candidate", type=Path, required=True)
    compare.add_argument("--max-regression", type=float, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "run":
            cases = load_cases(args.cases)
            versions = {case.dataset_version for case in cases}
            if len(versions) != 1:
                raise ValueError("all cases must use one dataset_version")
            manifest = RunManifest(
                run_id=str(uuid.uuid4()), agent_version="deterministic-support-v1",
                dataset_version=next(iter(versions)), metric_version="1.0",
                created_at=datetime.now(UTC),
            )
            result = asyncio.run(evaluate(cases, DeterministicSupportAgent(), manifest=manifest))
            write_run(result, args.out)
            print(json.dumps({"run_id": manifest.run_id, "output_dir": str(args.out)}, sort_keys=True))
            return 0
        baseline, candidate = load_run(args.baseline), load_run(args.candidate)
        report = compare_runs(baseline, candidate, max_regression=args.max_regression)
        print(report.model_dump_json())
        return 0 if report.passed else 1
    except (OSError, ValueError, ValidationError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
