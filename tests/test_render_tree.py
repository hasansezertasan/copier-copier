from pathlib import Path

EXPECTED_ROOT = {
    ".copier-answers.yml",
    ".config",
    ".editorconfig",
    ".github",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "README.md",
    "copier.yml",
    "pyproject.toml",
    "template",
    "tests",
}


def root_names(dest: Path) -> set[str]:
    return {p.name for p in dest.iterdir()}


def test_render_produces_decluttered_root(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    assert root_names(dest) == EXPECTED_ROOT


def test_repo_name_is_derived_from_subject(render):
    result, dest = render(subject="widgets")
    assert result.returncode == 0, result.stderr
    assert (dest / "README.md").read_text().startswith("# copier-widgets")


def test_invalid_subject_is_rejected(render):
    result, _ = render(subject="Not Valid!")
    assert result.returncode != 0
    assert "lowercase letters" in result.stdout + result.stderr
