import re
import subprocess

import pytest

from conftest import REPO

BACK_REFERENCE = "## Credits\n\nGenerated from [copier-demo](https://github.com/example/copier-demo).\n"


def conventions_check(guide: str) -> str:
    """The shell block under "Checking the conventions"."""
    section = guide.split("## Checking the conventions", 1)[1]
    return re.search(r"```sh\n(.*?)```", section, re.S).group(1)


def run_check(dest):
    script = conventions_check((dest / "REPOSITORY_SETUP.md").read_text())
    return subprocess.run(["bash", "-c", script], cwd=dest, capture_output=True, text=True, check=False)


def point_answers_at_the_published_template(dest):
    """Rendering from a local path records that path; an author re-points it at the published URL."""
    answers = dest / ".copier-answers.yml"
    answers.write_text(
        re.sub(
            r"(?m)^_src_path:.*$",
            "_src_path: https://github.com/hasansezertasan/copier-copier.git",
            answers.read_text(),
        )
    )


def rendered(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    point_answers_at_the_published_template(dest)
    return dest


def test_guide_names_the_generated_repo(render):
    result, dest = render(subject="widgets")
    assert result.returncode == 0, result.stderr
    guide = (dest / "REPOSITORY_SETUP.md").read_text()
    assert "example/copier-widgets" in guide
    assert "Generated from [copier-widgets](https://github.com/example/copier-widgets)." in guide
    assert "`## Credits`" in guide


def test_a_fresh_repo_passes_the_guides_convention_checks(render):
    check = run_check(rendered(render))
    assert check.returncode == 0, check.stdout + check.stderr


def test_a_payload_readme_with_credits_and_the_back_reference_passes_the_check(render):
    dest = rendered(render)
    (dest / "template" / "README.md").write_text("# Payload\n\n" + BACK_REFERENCE)
    check = run_check(dest)
    assert check.returncode == 0, check.stdout + check.stderr


@pytest.mark.parametrize(
    "readme",
    [
        "# Payload\n",
        "# Payload\n\nGenerated from [copier-demo](https://github.com/example/copier-demo).\n",
    ],
    ids=["no-back-reference", "no-credits-heading"],
)
def test_a_payload_readme_that_does_not_credit_the_template_fails_the_check(render, readme):
    dest = rendered(render)
    (dest / "template" / "README.md").write_text(readme)
    assert run_check(dest).returncode != 0


def test_the_gh_shortcut_in_the_readme_fails_the_check(render):
    dest = rendered(render)
    readme = dest / "README.md"
    readme.write_text(readme.read_text() + "\ncopier copy gh:example/copier-demo .\n")
    assert run_check(dest).returncode != 0


@pytest.mark.parametrize(
    "line",
    [
        "_src_path: gh:hasansezertasan/copier-copier",
        "_src_path: 'gh:hasansezertasan/copier-copier'",
        '_src_path: "gh:hasansezertasan/copier-copier"',
        "'_src_path': 'gh:hasansezertasan/copier-copier'",
        "_src_path: /tmp/copier-copier",
        "_src_path: https://",
        "_src_path: https://github.com",
    ],
    ids=["gh", "gh-single-quoted", "gh-double-quoted", "gh-quoted-key", "local-path", "bare-scheme", "host-only"],
)
def test_an_answers_file_that_is_not_a_full_https_url_fails_the_check(render, line):
    dest = rendered(render)
    (dest / ".copier-answers.yml").write_text(f"{line}\n_commit: v0.1.0\n")
    assert run_check(dest).returncode != 0


@pytest.mark.parametrize(
    "line",
    ["_src_path: https://github.com/hasansezertasan/copier-copier.git", "'_src_path': 'https://github.com/example/copier-copier.git'"],
)
def test_an_answers_file_with_a_full_https_url_passes_the_check(render, line):
    dest = rendered(render)
    (dest / ".copier-answers.yml").write_text(f"{line}\n_commit: v0.1.0\n")
    check = run_check(dest)
    assert check.returncode == 0, check.stdout + check.stderr


@pytest.mark.parametrize("key", ["_tasks", "'_tasks'", '"_tasks"'])
def test_tasks_fail_the_check_however_the_key_is_quoted(render, key):
    dest = rendered(render)
    copier_yml = dest / "copier.yml"
    copier_yml.write_text(copier_yml.read_text() + f"\n{key}:\n  - echo hi\n")
    assert run_check(dest).returncode != 0


def test_a_missing_answers_file_fails_the_check(render):
    dest = rendered(render)
    (dest / ".copier-answers.yml").unlink()
    assert run_check(dest).returncode != 0


def test_a_missing_answers_template_fails_even_when_a_backup_remains(render):
    dest = rendered(render)
    answers = dest / "template" / ".copier-answers.yml.jinja"
    answers.rename(answers.with_name(answers.name + ".bak"))
    assert run_check(dest).returncode != 0


def move_answers_template_one_level_down(dest):
    exact = dest / "template" / ".copier-answers.yml.jinja"
    nested = dest / "template" / "template" / ".copier-answers.yml.jinja.jinja"
    nested.parent.mkdir(parents=True)
    nested.write_text(exact.read_text())
    exact.unlink()


@pytest.mark.parametrize("subject", ["demo", "copier"])
def test_an_ordinary_repo_requires_the_exact_answers_template_path(render, subject):
    """Even a repo named copier-copier: only a payload that is itself a template may nest it."""
    result, dest = render(subject=subject)
    assert result.returncode == 0, result.stderr
    point_answers_at_the_published_template(dest)  # so only the nested path can fail the check
    move_answers_template_one_level_down(dest)
    assert run_check(dest).returncode != 0


def test_a_payload_that_is_itself_a_template_may_hold_the_answers_template_one_level_down(render):
    dest = rendered(render)
    move_answers_template_one_level_down(dest)
    (dest / "template" / "copier.yml").write_text("_subdirectory: template\n")
    check = run_check(dest)
    assert check.returncode == 0, check.stdout + check.stderr


def test_the_guide_makes_squash_merges_take_the_pr_title(render):
    guide = (rendered(render) / "REPOSITORY_SETUP.md").read_text()
    assert guide.count("squash_merge_commit_title") == 2  # set, then verified
    assert "squash_merge_commit_title=PR_TITLE" in guide


def test_the_generated_readme_credits_copier_copier_under_its_own_heading(render):
    dest = rendered(render)
    assert (dest / "README.md").read_text().rstrip().endswith(
        "## Credits\n\nGenerated from [copier-copier](https://github.com/hasansezertasan/copier-copier)."
    )


def test_this_repos_own_guide_passes_its_own_convention_checks():
    """copier-copier is self-hosted, so the checks it ships must pass on its own tree."""
    script = conventions_check((REPO / "REPOSITORY_SETUP.md").read_text())
    check = subprocess.run(["bash", "-c", script], cwd=REPO, capture_output=True, text=True, check=False)
    assert check.returncode == 0, check.stdout + check.stderr


def test_the_guide_describes_release_prs_as_waiting_for_approval(render):
    guide = (rendered(render) / "REPOSITORY_SETUP.md").read_text()
    assert "approval-required" in guide
    assert "merge it as a repository admin" not in guide.lower()


def test_the_guide_qualifies_when_the_pull_request_target_checks_do_not_run_on_release_prs(render):
    guide = (rendered(render) / "REPOSITORY_SETUP.md").read_text()
    assert "approval-required state" in guide
    assert "`pull_request_target` checks" in guide
    assert "do not run when release-please\n  creates or updates the PR" in guide
    assert "Reopening it by hand starts both" in guide
    assert "never run on that PR" not in guide


def test_a_payload_with_custom_delimiters_passes_with_its_answers_file_template(render):
    dest = rendered(render)
    (dest / "template" / ".copier-answers.yml.jinja").rename(
        dest / "template" / "[[ _copier_conf.answers_file ]].jinja"
    )
    check = run_check(dest)
    assert check.returncode == 0, check.stdout + check.stderr


def test_a_payload_without_any_answers_file_template_fails_the_check(render):
    dest = rendered(render)
    (dest / "template" / ".copier-answers.yml.jinja").unlink()
    check = run_check(dest)
    assert check.returncode != 0
    assert "is missing" in check.stdout + check.stderr


def test_a_nested_payload_with_custom_delimiters_passes_with_its_nested_answers_file_template(render):
    dest = rendered(render)
    nested = dest / "template" / "template"
    nested.mkdir(parents=True)
    (nested / "[[ _copier_conf.answers_file ]].jinja.jinja").write_text("answers\n")
    (dest / "template" / "copier.yml").write_text("_subdirectory: template\n")
    (dest / "template" / ".copier-answers.yml.jinja").unlink()
    check = run_check(dest)
    assert check.returncode == 0, check.stdout + check.stderr


def test_a_nested_payload_with_the_top_level_custom_file_only_fails_the_check(render):
    dest = rendered(render)
    (dest / "template" / "copier.yml").write_text("_subdirectory: template\n")
    (dest / "template" / ".copier-answers.yml.jinja").rename(
        dest / "template" / "[[ _copier_conf.answers_file ]].jinja"
    )
    check = run_check(dest)
    assert check.returncode != 0
    assert "is missing" in check.stdout + check.stderr
