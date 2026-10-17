# Self-hosting with `_skip_if_exists` on `copier.yml` and the payload

copier-copier applies itself to its own repo (its `.copier-answers.yml` points at `gh:hasansezertasan/copier-copier`), so its scaffolding stays in sync with what it generates. Its own `copier.yml` and `template/` are hand-written, so the generated `copier.yml` and `template/` are listed in `_skip_if_exists`: written once, then owned by the author. This also stops `copier update` from clobbering a generated repo's real payload.

## Considered Options

- **One-way generation, no self-hosting**: simpler, but copier-copier's own CI and release setup would drift from what it generates.
- **Self-hosting without `_skip_if_exists`**: applying the template would overwrite the hand-written `copier.yml` and `template/`.

## Consequences

The self-hosted copy lags one release behind, and its `_commit` needs re-anchoring to the first release tag once one exists. Testing local changes needs `copier update --vcs-ref=HEAD`.
