import tomllib
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


def test_description_survives_toml_escaping(render):
    description = 'C:\\projects\\tmp "quoted" and a\\tab'
    result, dest = render(description=description)
    assert result.returncode == 0, result.stderr
    parsed = tomllib.loads((dest / "pyproject.toml").read_text())
    assert parsed["project"]["description"] == description


def test_mit_license_names_the_holder_with_start_year_and_contact(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    first_lines = (dest / "LICENSE").read_text().splitlines()[:3]
    assert "Copyright (c) 2026-present Example Author <author@example.com>" in first_lines


def test_license_start_year_is_an_answer(render):
    result, dest = render(copyright_start_year="2019")
    assert result.returncode == 0, result.stderr
    assert "Copyright (c) 2019-present Example Author" in (dest / "LICENSE").read_text()
