from pathlib import Path


def test_readme_references_visual_assets():
    repo_root = Path(__file__).resolve().parents[1]
    readme = (repo_root / "README.md").read_text(encoding="utf-8")

    assert "assets/architecture.svg" in readme
    assert "assets/smoke-output.svg" in readme
    assert (repo_root / "assets" / "architecture.svg").exists()
    assert (repo_root / "assets" / "smoke-output.svg").exists()
