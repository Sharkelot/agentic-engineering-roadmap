from scripts.validate_course import validate_lesson


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
    lesson.write_text("# Lesson\n\n## Objectives\nGoals\n## Read\n- [Python](https://docs.python.org/)\n## Build\nDo it\n## Check your understanding\nQuestion\n## Done when\nDone\n")
    assert validate_lesson(lesson) == []
