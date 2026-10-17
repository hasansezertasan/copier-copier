import subprocess
import tomllib


def test_rendered_repo_passes_its_own_tests(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    gate = subprocess.run(
        ["uv", "run", "pytest", "-q"], cwd=dest, capture_output=True, text=True
    )
    assert gate.returncode == 0, gate.stdout + gate.stderr
    assert "passed" in gate.stdout


def test_rendered_lockfile_is_current(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    lock = subprocess.run(
        ["uv", "lock", "--check"], cwd=dest, capture_output=True, text=True
    )
    assert lock.returncode == 0, lock.stdout + lock.stderr


def test_lock_floor_does_not_depend_on_the_chosen_python(tmp_path, render):
    """`uv lock --check` only validates metadata, so assert the invariant that keeps the lock valid:
    every render declares the same requires-python floor and ships the identical lockfile."""
    result, dest = render(python_version="3.14")
    assert result.returncode == 0, result.stderr
    other = tmp_path / "other"
    from conftest import REPO, copier, data_flags, DEFAULT_ANSWERS

    answers = {**DEFAULT_ANSWERS, "python_version": "3.12"}
    assert copier("copy", "--defaults", *data_flags(answers), str(REPO), str(other), cwd=REPO).returncode == 0
    floor = lambda d: tomllib.loads((d / "pyproject.toml").read_text())["project"]["requires-python"]
    assert floor(dest) == floor(other) == ">=3.12"
    assert (dest / "uv.lock").read_text() == (other / "uv.lock").read_text()


def test_python_older_than_the_lock_floor_is_rejected(render):
    result, _ = render(python_version="3.11")
    assert result.returncode != 0
    assert "3.12" in result.stdout + result.stderr
