# Self-hosting

## Self-hosting with `_skip_if_exists` for author-owned files

**Id:** 10998059-628f-4e51-800c-3bb2cd27dc9e
**Type:** decision
**Status:** active
**Evidence:** confirmed
**Source:** `docs/adr/0001-self-hosting-with-skip-if-exists.md`
**Revisit when:** the self-hosted copy's `_commit` anchor or the `_skip_if_exists` list in `copier.yml` changes

copier-copier applies itself to its own repo, so its scaffolding stays in
sync with what it generates. Files an author is expected to edit
(`copier.yml`, `template/`, `tests/`, the README, `AGENTS.md`,
`pyproject.toml`, the seeded dotfiles and a few lock and manifest files)
are listed in `_skip_if_exists`: written once, then owned by the author.
The list itself lives in `copier.yml`.

**Reason:** the repo's own CI and release setup would otherwise drift from
what it generates. `_skip_if_exists` also keeps `copier update` from
clobbering a generated repo's real payload.

**Rejected alternative:** one-way generation with no self-hosting. Simpler,
but the repo's own CI and release setup would drift from what it generates.

**Rejected alternative:** self-hosting without `_skip_if_exists`. Applying
the template would overwrite the hand-written `copier.yml` and `template/`.

**Consequence:** the self-hosted copy lags one release behind, and its
`_commit` needs re-anchoring to the first release tag once one exists.
Author-owned files are only checked for existence by the self-hosting sync
test, so they can drift from the template's seed values by design.
