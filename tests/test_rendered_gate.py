import subprocess


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
