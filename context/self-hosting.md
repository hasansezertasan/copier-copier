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

## Dashboard pin lives in `.config/mise/conf.d/`, not in `.config/mise.toml`

**Id:** d3efd4fa-cf2f-41b4-ae48-bad01494f1b7
**Type:** decision
**Type:** constraint
**Status:** active
**Evidence:** confirmed
**Source:** CI failure on the Keep the Why setup pull request (#22); `tests/test_self_hosting.py`; Renovate's mise manager documentation
**Revisit when:** `.config/mise.toml` becomes author-owned in `_skip_if_exists`, or the self-hosting test stops comparing it with a fresh render
**See:** self-hosting.md#self-hosting-with-_skip_if_exists-for-author-owned-files — 10998059-628f-4e51-800c-3bb2cd27dc9e — as of 2026-10-24

The `keep-the-why-dashboard` pin and its `dashboard-export` task sit in
`.config/mise/conf.d/keep-the-why.toml`. `.config/mise.toml` stays
byte-identical to what the template renders.

**Reason:** `.config/mise.toml` is template-managed, not author-owned, so the
self-hosting test compares it with a fresh render, and any repo-only edit
fails it. mise reads `conf.d` natively, and Renovate's mise manager matches
`.config/mise/conf.d/*.toml`, so the pin still gets update PRs.

**Rejected alternative:** add `.config/mise.toml` to `_skip_if_exists`.
That changes the template for every generated repo: `copier update` would
stop touching their tool pins.

**Rejected alternative:** add the dashboard to `template/.config/mise.toml`.
It would ship a tool to every generated repo that does not use it.
