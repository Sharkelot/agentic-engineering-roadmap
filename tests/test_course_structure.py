from pathlib import Path

from scripts.validate_course import validate_lesson

ROOT = Path(__file__).resolve().parents[1]
LESSONS = [ROOT / "lessons" / f"week-{i:02d}-{slug}.md" for i, slug in enumerate(("python-sdk", "schemas-data", "evaluation-design", "metrics-regression", "observability", "orchestration-reliability", "deployment-ci", "capstone"), 1)]
HEADINGS = ("Objectives", "Prerequisites", "Read", "Build", "Check your understanding", "Reflection", "Done when")


def test_missing_headings_are_reported(tmp_path):
    lesson = tmp_path / "lesson.md"
    lesson.write_text("# Lesson\n\n## Objectives\n")
    errors = validate_lesson(lesson)
    assert any("Read" in error for error in errors)
    assert any("Build" in error for error in errors)


def test_missing_readings_are_reported(tmp_path):
    lesson = tmp_path / "lesson.md"
    lesson.write_text("# Lesson\n\n## Objectives\nGoals\n## Read\n## Build\n## Check your understanding\n## Done when\n")
    assert any("reference" in error.lower() for error in validate_lesson(lesson))


def test_valid_lesson_has_no_errors(tmp_path):
    lesson = tmp_path / "lesson.md"
    lesson.write_text("# Lesson\n\n## Objectives\nGoals\n## Prerequisites\nNone\n## Read\n- [Python](https://docs.python.org/)\n## Build\nDo it\n## Check your understanding\nQuestion\n## Reflection\nNext?\n## Done when\nDone\n")
    assert validate_lesson(lesson) == []


def test_all_eight_lessons_have_required_sections_and_source_links():
    assert all(path.is_file() for path in LESSONS)
    for path in LESSONS:
        text = path.read_text(encoding="utf-8")
        assert all(f"## {heading}" in text for heading in HEADINGS), path
        assert "](https://" in text and "](../" in text, path
        assert not validate_lesson(path), path


def test_validator_rejects_missing_reflection(tmp_path):
    lesson = tmp_path / "lesson.md"
    lesson.write_text("# Lesson\n## Objectives\n## Prerequisites\n## Read\n[Source](https://example.org)\n## Build\n## Check your understanding\n## Done when\n")
    assert any("Reflection" in error for error in validate_lesson(lesson))


def test_each_lesson_has_three_retrieval_questions_and_reflection_prompt():
    for path in LESSONS:
        text = path.read_text(encoding="utf-8")
        quiz = text.split("## Check your understanding", 1)[1].split("\n## ", 1)[0]
        assert all(f"{n}. " in quiz for n in range(1, 4)), path
        reflection = text.split("## Reflection", 1)[1].split("\n## ", 1)[0].strip()
        assert reflection, path
        assert "Done when" in text and "synthetic" in text.lower(), path
        assert "solutions/README.md" in text, path


def test_core_agent_evaluation_topics_are_taught():
    week3 = (ROOT / "lessons/week-03-evaluation-design.md").read_text(encoding="utf-8").lower()
    week4 = (ROOT / "lessons/week-04-metrics-regression.md").read_text(encoding="utf-8").lower()
    week5 = (ROOT / "lessons/week-05-observability.md").read_text(encoding="utf-8").lower()
    week6 = (ROOT / "lessons/week-06-orchestration-reliability.md").read_text(encoding="utf-8").lower()
    week7 = (ROOT / "lessons/week-07-deployment-ci.md").read_text(encoding="utf-8").lower()
    assert all(topic in week3 for topic in ("citation", "rag", "tool", "abstain"))
    assert all(topic in week4 for topic in ("repeated-run", "uncertainty", "judge calibration", "human labels"))
    assert all(topic in week5 for topic in ("redaction", "synthetic attribute", "no data"))
    assert all(topic in week6 for topic in ("retry", "idempotency", "cancellation", "sharding", "resumability"))
    assert all(topic in week7 for topic in ("local ci", "container", "artifact"))
