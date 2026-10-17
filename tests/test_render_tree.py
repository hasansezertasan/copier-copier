from pathlib import Path

EXPECTED_ROOT = {
    ".python-version",
    ".copier-answers.yml",
    ".config",
    ".editorconfig",
    ".github",
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "LICENSE",
    "cobo.lock",
    "README.md",
    "copier.yml",
    "pyproject.toml",
    "uv.lock",
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


def test_python_version_has_one_source_that_mise_reads(render):
    result, dest = render(python_version="3.13")
    assert result.returncode == 0, result.stderr
    assert (dest / ".python-version").read_text().strip() == "3.13"
    mise = (dest / ".config" / "mise.toml").read_text()
    assert "read_file" in mise and ".python-version" in mise
    assert 'python = "3.' not in mise  # no literal pin to drift
