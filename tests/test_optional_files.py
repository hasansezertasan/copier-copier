"""Adopters decline the seeded payload and Python harness through recorded answers.

`_skip_if_exists` only protects files that already exist, so `copier update` recreates
anything an adopter deleted. An answer recorded in `.copier-answers.yml` survives updates.
"""

import tomllib

from conftest import DEFAULT_ANSWERS, REPO, copier, data_flags, git, versioned_copy

HARNESS_FILES = ["pyproject.toml", "uv.lock", "tests", ".github/workflows/test.yml"]


def test_declining_the_seed_payload_leaves_no_payload_directory(render):
    result, dest = render(seed_payload="false")
    assert result.returncode == 0, result.stderr
    assert not (dest / "template").exists()
    assert (dest / "copier.yml").is_file()


def test_declining_the_python_harness_leaves_no_python_files(render):
    result, dest = render(python_harness="false")
    assert result.returncode == 0, result.stderr
    for name in HARNESS_FILES:
        assert not (dest / name).exists(), name
    mise = tomllib.loads((dest / ".config" / "mise.toml").read_text())
    assert "uv" not in mise["tools"]
    assert "test" not in mise.get("tasks", {})
    assert "mise run test" not in (dest / "AGENTS.md").read_text()
    assert "mise run test" not in (dest / "README.md").read_text()


def test_defaults_still_seed_everything(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    assert (dest / "template" / "PLACEHOLDER.md").is_file()
    for name in HARNESS_FILES:
        assert (dest / name).exists(), name


def test_update_does_not_recreate_declined_files(tmp_path):
    src = versioned_copy(REPO, tmp_path / "copier-copier")
    dest = tmp_path / "adopter"
    answers = {**DEFAULT_ANSWERS, "seed_payload": "false", "python_harness": "false"}
    first = copier("copy", "--defaults", *data_flags(answers), str(src), str(dest), cwd=tmp_path)
    assert first.returncode == 0, first.stderr
    git("init", "-q", "-b", "main", cwd=dest)
    git("add", "-A", cwd=dest)
    git("commit", "-q", "-m", "chore: render", cwd=dest)

    git("commit", "-q", "--allow-empty", "-m", "chore: release", cwd=src)
    git("tag", "v0.0.1", cwd=src)
    update = copier("update", "--defaults", "--skip-answered", cwd=dest)
    assert update.returncode == 0, update.stderr

    for name in ["template", *HARNESS_FILES]:
        assert not (dest / name).exists(), name
