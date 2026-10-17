# Self-hosting with `_skip_if_exists` for author-owned files

copier-copier applies itself to its own repo (its `.copier-answers.yml` points at `gh:hasansezertasan/copier-copier`), so its scaffolding stays in sync with what it generates. Its own `copier.yml`, `template/` and the other files an author is expected to edit are hand-written, so they are listed in `_skip_if_exists`: written once, then owned by the author. The list is `copier.yml`, `template/`, `tests/`, `README.md`, `AGENTS.md`, `pyproject.toml`, `uv.lock`, `CHANGELOG.md` and `.github/release-please-manifest.json`. This also stops `copier update` from clobbering a generated repo's real payload.

## Considered Options

- **One-way generation, no self-hosting**: simpler, but copier-copier's own CI and release setup would drift from what it generates.
- **Self-hosting without `_skip_if_exists`**: applying the template would overwrite the hand-written `copier.yml` and `template/`.

## Consequences

The self-hosted copy lags one release behind, and its `_commit` needs re-anchoring to the first release tag once one exists. Author-owned files are not compared by the self-hosting sync test (only checked for existence), so they can drift from the template's seed values by design.
