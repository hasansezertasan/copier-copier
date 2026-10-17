import json


def test_first_release_is_0_1_0_and_breaking_changes_stay_pre_1_0(render):
    result, dest = render()
    assert result.returncode == 0, result.stderr
    config = json.loads((dest / ".github" / "release-please-config.json").read_text())
    assert config["packages"]["."]["initial-version"] == "0.1.0"
    assert config["bump-minor-pre-major"] is True
    assert config["bump-patch-for-minor-pre-major"] is False
    assert config["include-v-in-tag"] is True
