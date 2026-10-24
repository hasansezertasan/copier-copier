# Template source path

## Record a full git URL as `_src_path`, never the `gh:` shortcut

**Id:** 6f5e47e0-1002-46be-9b53-992376696888
**Type:** decision
**Status:** active
**Evidence:** confirmed
**Source:** `docs/adr/0002-full-git-url-for-src-path.md`; issue #9 (still open)
**Verification:** uncorroborated — verified from other repos' Renovate behaviour, not by a controlled run on this repository; see the body
**Revisit when:** issue #9 is closed, or Renovate's copier manager changes how it resolves `_src_path`

The README, the generated README and the self-hosted answers file all record
`_src_path` as a full URL (`https://github.com/hasansezertasan/copier-copier.git`),
and adopters should too.

**Reason:** Renovate's copier manager detects `.copier-answers.yml` but looks
`_src_path` up as a git remote, so the `gh:` shortcut fails the tag lookup
(`no-result`) and no update PR is opened. A full URL works: repos generated
from copier-pyproject use that form and receive Renovate update PRs.

**Rejected alternative:** keep the `gh:` shortcut. Shorter to type, but
Renovate never proposes a template update.

**Rejected alternative:** have Renovate expand the shortcut through a custom
regex or datasource config. It breaks the native-manager preference and would
have to be maintained per repo.

**Verification status:** verified from existing repos (dependency dashboards
and PRs of other generated repos), not by a controlled run. Not verified:
that Renovate runs on this repository at all, that its `.github/renovate.json`
behaves as intended (shared preset resolving, `template/**` freeze), and that
a new tag produces an update PR in an adopter after its `_src_path` is
switched to the URL.
