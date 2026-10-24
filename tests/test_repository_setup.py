import re
import subprocess


def conventions_check(guide: str) -> str:
    """The shell block under "Checking the conventions"."""
    section = guide.split("## Checking the conventions", 1)[1]
    return re.search(r"```sh\n(.*?)```", section, re.S).group(1)


def test_guide_names_the_generated_repo(render):
    result, dest = render(subject="widgets")
    assert result.returncode == 0, result.stderr
    guide = (dest / "REPOSITORY_SETUP.md").read_text()
    assert "example/copier-widgets" in guide
    assert "Generated from [copier-widgets](https://github.com/example/copier-widgets)." in guide
    assert "`## Credits`" in guide


def test_a_fresh_repo_passes_the_guides_convention_checks(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    script = conventions_check((dest / "REPOSITORY_SETUP.md").read_text())
    check = subprocess.run(["bash", "-c", script], cwd=dest, capture_output=True, text=True, check=False)
    assert check.returncode == 0, check.stdout + check.stderr


def test_the_convention_checks_catch_a_missing_back_reference(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    (dest / "template" / "README.md").write_text("# Payload\n")
    script = conventions_check((dest / "REPOSITORY_SETUP.md").read_text())
    check = subprocess.run(["bash", "-c", script], cwd=dest, capture_output=True, text=True, check=False)
    assert check.returncode != 0


def test_a_payload_readme_without_a_credits_heading_fails_the_check(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    (dest / "template" / "README.md").write_text(
        "# Payload\n\nGenerated from [copier-demo](https://github.com/example/copier-demo).\n"
    )
    script = conventions_check((dest / "REPOSITORY_SETUP.md").read_text())
    check = subprocess.run(["bash", "-c", script], cwd=dest, capture_output=True, text=True, check=False)
    assert check.returncode != 0


def test_a_payload_readme_with_credits_and_the_back_reference_passes_the_check(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    (dest / "template" / "README.md").write_text(
        "# Payload\n\n## Credits\n\nGenerated from [copier-demo](https://github.com/example/copier-demo).\n"
    )
    script = conventions_check((dest / "REPOSITORY_SETUP.md").read_text())
    check = subprocess.run(["bash", "-c", script], cwd=dest, capture_output=True, text=True, check=False)
    assert check.returncode == 0, check.stdout + check.stderr


def test_the_generated_readme_credits_copier_copier_under_its_own_heading(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    assert (dest / "README.md").read_text().rstrip().endswith(
        "## Credits\n\nGenerated from [copier-copier](https://github.com/hasansezertasan/copier-copier)."
    )
