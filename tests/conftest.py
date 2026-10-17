import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
IGNORE = shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache")

DEFAULT_ANSWERS = {
    "subject": "demo",
    "description": "A demo template.",
    "owner": "example",
    "author_name": "Example Author",
    "author_email": "author@example.com",
    "license": "MIT",
}


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=False)


def copier(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return run(sys.executable, "-m", "copier", *args, cwd=cwd)


def git(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return run(
        "git", "-c", "user.name=test", "-c", "user.email=test@example.com", *args, cwd=cwd
    )


def data_flags(answers: dict[str, str]) -> list[str]:
    return [f"--data={k}={v}" for k, v in answers.items()]


def versioned_copy(src: Path, dest: Path) -> Path:
    """Copy `src` to `dest` as a git repo tagged v0.0.0, so `copier update` has history."""
    shutil.copytree(src, dest, ignore=IGNORE)
    git("init", "-q", "-b", "main", cwd=dest)
    git("add", "-A", cwd=dest)
    git("commit", "-q", "-m", "chore: initial", cwd=dest)
    git("tag", "v0.0.0", cwd=dest)
    return dest


@pytest.fixture
def render(tmp_path):
    """Render this template into a fresh dir and return the CompletedProcess and dest."""

    def _render(**overrides):
        dest = tmp_path / "out"
        answers = {**DEFAULT_ANSWERS, **overrides}
        result = copier("copy", "--defaults", *data_flags(answers), str(REPO), str(dest), cwd=REPO)
        return result, dest

    return _render
