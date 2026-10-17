"""copier-copier is an application of itself (docs/adr/0001-self-hosting-with-skip-if-exists.md).

Rendering the template with the answers recorded in the repo's own
`.copier-answers.yml` must reproduce every file the template does not hand to the
author via `_skip_if_exists`.
"""

import filecmp

import yaml

from conftest import REPO, copier


def test_root_scaffolding_matches_a_fresh_render(tmp_path):
    answers = yaml.safe_load((REPO / ".copier-answers.yml").read_text())
    assert answers["_src_path"] == "gh:hasansezertasan/copier-copier"
    data = [f"--data={k}={v}" for k, v in answers.items() if not k.startswith("_")]

    dest = tmp_path / "fresh"
    result = copier("copy", "--defaults", *data, str(REPO), str(dest), cwd=REPO)
    assert result.returncode == 0, result.stderr

    skipped = set(yaml.safe_load((REPO / "copier.yml").read_text())["_skip_if_exists"])
    drifted = []
    for fresh in sorted(p for p in dest.rglob("*") if p.is_file()):
        rel = fresh.relative_to(dest)
        if rel.as_posix() in skipped or rel.parts[0] in skipped:
            continue
        if rel.as_posix() == ".copier-answers.yml":
            continue
        mine = REPO / rel
        if not mine.is_file() or not filecmp.cmp(fresh, mine, shallow=False):
            drifted.append(rel.as_posix())
    assert drifted == [], f"scaffolding drifted from the template: {drifted}"
