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
