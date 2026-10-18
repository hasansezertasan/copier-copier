import json


def test_first_release_is_0_1_0_and_breaking_changes_stay_pre_1_0(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    config = json.loads((dest / ".github" / "release-please-config.json").read_text())
    assert config["packages"]["."]["initial-version"] == "0.1.0"
    assert config["bump-minor-pre-major"] is True
    assert config["bump-patch-for-minor-pre-major"] is False
    assert config["include-v-in-tag"] is True


def test_changelog_groups_entries_and_hides_housekeeping(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    config = json.loads((dest / ".github" / "release-please-config.json").read_text())
    sections = {s["type"]: s for s in config["changelog-sections"]}
    assert sections["feat"]["section"] and sections["fix"]["section"]
    assert sections["chore"]["hidden"] is True
    assert sections["style"]["hidden"] is True
    # Repo-specific keys do not belong in a seed.
    assert "bootstrap-sha" not in config
    assert "package-name" not in config["packages"]["."]
