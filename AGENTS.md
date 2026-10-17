# copier-copier

A Copier template repo. The payload lives in `template/`; everything else is scaffolding. Here the payload is itself a template repo, generated from the `template/` directory (see `GLOSSARY.md`).

## Conventions

- Branch names follow [Conventional Branch](https://conventional-branch.github.io/); commits and PR titles follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). CI enforces both.
- Any lint configs sit under `.config/`, never at the repo root. Tools that cannot read from there (Renovate, release-please) live in `.github/`.
- Tool versions are pinned in `.config/mise.toml` so Renovate's native `mise` manager covers them.
- Do not add `_tasks` to `copier.yml`: they make the template unsafe and force `--trust`, which Renovate's copier manager does not pass.
- Run the tests with `mise run test`.

## Agent skills

### Issue tracker

Issues live in GitHub Issues (`gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
