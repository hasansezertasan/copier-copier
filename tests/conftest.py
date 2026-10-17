import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

DEFAULT_ANSWERS = {
    "subject": "demo",
    "description": "A demo template.",
    "owner": "example",
    "author_name": "Example Author",
    "author_email": "author@example.com",
    "license": "MIT",
    "python_version": "3.14",
}


def copier(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "copier", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def render(tmp_path):
    """Render this template into a fresh dir and return the CompletedProcess and dest."""

    def _render(**overrides):
        answers = {**DEFAULT_ANSWERS, **overrides}
        dest = tmp_path / "out"
        data = [f"--data={k}={v}" for k, v in answers.items()]
        result = copier(
            "copy", "--defaults", *data, str(REPO), str(dest), cwd=REPO
        )
        return result, dest

    return _render
