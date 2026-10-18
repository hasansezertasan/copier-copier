# Record a full git URL as `_src_path`, never the `gh:` shortcut

Renovate's copier manager detects `.copier-answers.yml` but looks `_src_path` up as a git remote, so the `gh:hasansezertasan/copier-copier` shortcut fails with `Failed to look up git-tags package … no-result` and no update PR is opened. A full URL such as `https://github.com/hasansezertasan/copier-copier.git` works: the repos generated from copier-pyproject record that form and receive Renovate update PRs. So the README, the generated README and the self-hosted answers file all use the full URL, and adopters should too (`copier copy <url> …`, or edit `_src_path` in an existing answers file; copier resolves both the same way).

## Considered Options

- **Keep the `gh:` shortcut**: shorter to type, but Renovate never proposes a template update.
- **Ask Renovate to expand the shortcut** (a custom regex or datasource config): breaks the native-manager preference and still has to be maintained per repo.
