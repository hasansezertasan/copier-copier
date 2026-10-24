from conftest import DEFAULT_ANSWERS, REPO, copier, data_flags, git, versioned_copy


def test_update_keeps_author_files_and_refreshes_scaffolding(tmp_path):
    src = versioned_copy(REPO, tmp_path / "copier-copier")

    dest = tmp_path / "copier-demo"
    first = copier("copy", "--defaults", *data_flags(DEFAULT_ANSWERS), str(src), str(dest), cwd=tmp_path)
    assert first.returncode == 0, first.stderr
    git("init", "-q", "-b", "main", cwd=dest)

    # The author takes ownership of these files.
    (dest / "copier.yml").write_text("_subdirectory: template\n# author edit\n")
    (dest / "template" / "real-file.txt").write_text("the real payload\n")
    (dest / "tests" / "test_template.py").write_text("# author edit\n")
    (dest / "AGENTS.md").write_text("# author edit\n")
    (dest / ".gitignore").write_text("# author edit\n")
    (dest / ".python-version").write_text("3.99\n")
    git("add", "-A", cwd=dest)
    git("commit", "-q", "-m", "feat: real payload", cwd=dest)

    # The next copier-copier release touches scaffolding and author-owned seed files alike.
    workflow = src / "template" / ".github" / "workflows" / "test.yml"
    workflow.write_text(workflow.read_text() + "# new scaffolding rule\n")
    (src / "template" / ".gitignore").write_text("# upstream rewrite\n")
    (src / "template" / ".python-version.jinja").write_text("3.13\n")
    (src / "template" / "AGENTS.md.jinja").write_text("# upstream rewrite\n")
    (src / "template" / "copier.yml").write_text("# upstream rewrite\n")
    (src / "template" / "tests" / "test_template.py").write_text("# upstream rewrite\n")
    git("commit", "-q", "-am", "feat: new rule", cwd=src)
    git("tag", "v0.0.1", cwd=src)

    update = copier("update", "--defaults", "--skip-answered", cwd=dest)
    assert update.returncode == 0, update.stderr

    assert "# new scaffolding rule" in (dest / ".github" / "workflows" / "test.yml").read_text()
    assert (dest / ".gitignore").read_text() == "# author edit\n"
    assert (dest / ".python-version").read_text() == "3.99\n"
    assert (dest / "AGENTS.md").read_text() == "# author edit\n"
    assert (dest / "copier.yml").read_text() == "_subdirectory: template\n# author edit\n"
    assert (dest / "template" / "real-file.txt").read_text() == "the real payload\n"
    assert (dest / "tests" / "test_template.py").read_text() == "# author edit\n"


def test_update_does_not_recreate_deleted_payload_seeds(tmp_path):
    src = versioned_copy(REPO, tmp_path / "copier-copier")

    dest = tmp_path / "copier-demo"
    first = copier("copy", "--defaults", *data_flags(DEFAULT_ANSWERS), str(src), str(dest), cwd=tmp_path)
    assert first.returncode == 0, first.stderr
    seeds = [dest / "template" / "PLACEHOLDER.md", dest / "template" / ".copier-answers.yml.jinja"]
    for seed in seeds:
        assert seed.is_file(), f"a fresh copy seeds {seed.name}"
    git("init", "-q", "-b", "main", cwd=dest)
    git("add", "-A", cwd=dest)
    git("commit", "-q", "-m", "chore: render", cwd=dest)

    # The author's repo has its own payload, so the seeds are deleted.
    for seed in seeds:
        seed.unlink()
    git("commit", "-q", "-am", "chore: drop the seeded payload files", cwd=dest)

    workflow = src / "template" / ".github" / "workflows" / "test.yml"
    workflow.write_text(workflow.read_text() + "# new scaffolding rule\n")
    git("commit", "-q", "-am", "feat: new rule", cwd=src)
    git("tag", "v0.0.1", cwd=src)

    update = copier("update", "--defaults", "--skip-answered", cwd=dest)
    assert update.returncode == 0, update.stderr
    assert "# new scaffolding rule" in (dest / ".github" / "workflows" / "test.yml").read_text()
    for seed in seeds:
        assert not seed.exists(), f"update recreated {seed.name}"
