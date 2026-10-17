import shutil
import subprocess
import sys

from conftest import DEFAULT_ANSWERS, REPO

IGNORE = shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache")


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def git(*args, cwd):
    return run("git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args, cwd=cwd)


def test_update_keeps_author_files_and_refreshes_scaffolding(tmp_path):
    src = tmp_path / "copier-copier"
    shutil.copytree(REPO, src, ignore=IGNORE)
    git("init", "-q", "-b", "main", cwd=src)
    git("add", "-A", cwd=src)
    git("commit", "-q", "-m", "chore: initial", cwd=src)
    git("tag", "v0.0.0", cwd=src)

    dest = tmp_path / "copier-demo"
    data = [f"--data={k}={v}" for k, v in DEFAULT_ANSWERS.items()]
    first = run(sys.executable, "-m", "copier", "copy", "--defaults", *data, str(src), str(dest), cwd=tmp_path)
    assert first.returncode == 0, first.stderr
    git("init", "-q", "-b", "main", cwd=dest)

    # The author takes ownership of these files.
    (dest / "copier.yml").write_text("_subdirectory: template\n# author edit\n")
    (dest / "template" / "real-file.txt").write_text("the real payload\n")
    (dest / "tests" / "test_template.py").write_text("# author edit\n")
    (dest / "AGENTS.md").write_text("# author edit\n")
    git("add", "-A", cwd=dest)
    git("commit", "-q", "-m", "feat: real payload", cwd=dest)

    # The next copier-copier release touches scaffolding and author-owned seed files alike.
    editorconfig = src / "template" / ".editorconfig"
    editorconfig.write_text(editorconfig.read_text() + "# new scaffolding rule\n")
    (src / "template" / "AGENTS.md.jinja").write_text("# upstream rewrite\n")
    (src / "template" / "copier.yml").write_text("# upstream rewrite\n")
    (src / "template" / "tests" / "test_template.py").write_text("# upstream rewrite\n")
    git("commit", "-q", "-am", "feat: new rule", cwd=src)
    git("tag", "v0.0.1", cwd=src)

    update = run(sys.executable, "-m", "copier", "update", "--defaults", "--skip-answered", cwd=dest)
    assert update.returncode == 0, update.stderr

    assert "# new scaffolding rule" in (dest / ".editorconfig").read_text()
    assert (dest / "AGENTS.md").read_text() == "# author edit\n"
    assert (dest / "copier.yml").read_text() == "_subdirectory: template\n# author edit\n"
    assert (dest / "template" / "real-file.txt").read_text() == "the real payload\n"
    assert (dest / "tests" / "test_template.py").read_text() == "# author edit\n"
