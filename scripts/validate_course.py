import argparse
from pathlib import Path

REQUIRED_HEADINGS = (
    "Objectives",
    "Prerequisites",
    "Read",
    "Build",
    "Check your understanding",
    "Reflection",
    "Done when",
)


def validate_lesson(path: str | Path) -> list[str]:
    """Return structural issues in a lesson without accessing the network."""
    content = Path(path).read_text(encoding="utf-8")
    errors = [f"Missing required heading: {heading}" for heading in REQUIRED_HEADINGS if f"## {heading}" not in content]
    read_section = content.split("## Read", 1)[1].split("\n## ", 1)[0] if "## Read" in content else ""
    if not any("](http://" in line or "](https://" in line for line in read_section.splitlines()):
        errors.append("Read section must contain at least one linked reference")
    return errors


def validate_course(root: Path | None = None) -> list[str]:
    """Validate every weekly lesson using local filesystem reads only."""
    course_root = root or Path(__file__).resolve().parents[1]
    lessons = sorted((course_root / "lessons").glob("week-*.md"))
    if not lessons:
        return ["No weekly lessons found"]
    return [f"{path.relative_to(course_root)}: {error}" for path in lessons for error in validate_lesson(path)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate course lesson structure offline")
    parser.parse_args()
    errors = validate_course()
    if errors:
        print("Course validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Course validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
