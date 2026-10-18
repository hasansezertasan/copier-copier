# Record a full git URL as `_src_path`, never the `gh:` shortcut

Renovate's copier manager detects `.copier-answers.yml` but looks `_src_path` up as a git remote, so the `gh:hasansezertasan/copier-copier` shortcut fails with `Failed to look up git-tags package … no-result` and no update PR is opened. A full URL such as `https://github.com/hasansezertasan/copier-copier.git` works: the repos generated from copier-pyproject record that form and receive Renovate update PRs. So the README, the generated README and the self-hosted answers file all use the full URL, and adopters should too (`copier copy <url> …`, or edit `_src_path` in an existing answers file; copier resolves both the same way).

## Considered Options

- **Keep the `gh:` shortcut**: shorter to type, but Renovate never proposes a template update.
- **Ask Renovate to expand the shortcut** (a custom regex or datasource config): breaks the native-manager preference and still has to be maintained per repo.

## Verification status (issue #9)

Verified from existing repos, not by a controlled run:

- Renovate's copier manager detects `.copier-answers.yml` and parses the `_src_path` and `_commit` pair (the dependency dashboards of copier-scoop-bucket and copier-homebrew-tap list `gh:hasansezertasan/copier-copier v0.2.0`).
- With the `gh:` shortcut the lookup fails (`no-result`), so no PR is opened.
- With a full URL the lookup works and Renovate opens and keeps current PRs (hwid, olink and peta, generated from copier-pyproject).

Not verified:

- That Renovate runs on this repository at all: copier-copier has no Dependency Dashboard issue and no Renovate PRs, unlike the repos above.
- That `.github/renovate.json` behaves as intended here: the shared `renovate-config:python` preset resolving, and the `template/**` freeze keeping payload pins out of update PRs.
- That a new copier-copier tag produces an update PR in an adopter after its `_src_path` is switched to the URL.

Issue #9 stays open until those are observed.
