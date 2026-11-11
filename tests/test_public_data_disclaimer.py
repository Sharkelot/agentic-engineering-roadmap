from pathlib import Path


def test_public_dataset_disclaimer_is_present() -> None:
    readme = Path(__file__).parents[1] / "synthetic-data" / "README.md"
    assert readme.is_file(), "synthetic-data/README.md must exist"
    text = readme.read_text(encoding="utf-8").lower()
    assert "synthetic" in text, "dataset must be identified as synthetic"
    assert "independent learning project" in text
    assert "not affiliated" in text and "nvidia" in text and "employer" in text
