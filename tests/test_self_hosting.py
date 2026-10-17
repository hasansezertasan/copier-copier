"""copier-copier is an application of itself (docs/adr/0001-self-hosting-with-skip-if-exists.md).

Rendering the template with the answers recorded in the repo's own
`.copier-answers.yml` must reproduce every file the template does not hand to the
author via `_skip_if_exists`, and every author-owned file must exist.
"""

import filecmp
import re

import yaml

from conftest import REPO, copier, data_flags

ANSWERS = yaml.safe_load((REPO / ".copier-answers.yml").read_text())
SKIPPED = yaml.safe_load((REPO / "copier.yml").read_text())["_skip_if_exists"]


def is_author_owned(rel: str) -> bool:
    return any(rel == entry or rel.startswith(f"{entry}/") for entry in SKIPPED)


def test_root_scaffolding_matches_a_fresh_render(tmp_path):
    answers = {k: v for k, v in ANSWERS.items() if not k.startswith("_")}
    dest = tmp_path / "fresh"
    result = copier("copy", "--defaults", *data_flags(answers), str(REPO), str(dest), cwd=REPO)
    assert result.returncode == 0, result.stderr

    drifted = []
    for fresh in sorted(p for p in dest.rglob("*") if p.is_file()):
        rel = fresh.relative_to(dest).as_posix()
        if rel == ".copier-answers.yml" or is_author_owned(rel):
            continue
        mine = REPO / rel
        if not mine.is_file() or not filecmp.cmp(fresh, mine, shallow=False):
            drifted.append(rel)
    assert drifted == [], f"scaffolding drifted from the template: {drifted}"


def test_author_owned_files_exist():
    missing = [entry for entry in SKIPPED if not (REPO / entry).exists()]
    assert missing == []


def test_answers_file_is_anchored_to_the_published_template():
    assert ANSWERS["_src_path"] == "gh:hasansezertasan/copier-copier"
    # A tag or a commit sha, never copier's dev-version string for an untagged template.
    # (Not resolved against history: CI checks out shallow and squash-merges drop commits.)
    assert re.fullmatch(r"v?\d+\.\d+\.\d+|[0-9a-f]{7,40}", ANSWERS["_commit"]), ANSWERS["_commit"]
