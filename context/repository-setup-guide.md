# Repository setup guide

## Template conventions are checked by a script in the setup guide, not by a seeded test

**Id:** 0eec513d-8da2-4b5a-abf2-0dabf5862161
**Type:** decision
**Status:** active
**Evidence:** inferred
**Source:** maintainer request for a dedicated `REPOSITORY_SETUP.md.jinja` to enforce template best practices, 2026-10-24; `copier.yml` `_skip_if_exists` list; `tests/test_repository_setup.py`
**Revisit when:** `tests/` stops being author-owned in `_skip_if_exists`, or generated repos get a way to receive new seeded tests through `copier update`
**See:** self-hosting.md#self-hosting-with-_skip_if_exists-for-author-owned-files — 10998059-628f-4e51-800c-3bb2cd27dc9e — as of 2026-10-24

Every generated `copier-<subject>` repo carries `REPOSITORY_SETUP.md`, rendered
from `template/REPOSITORY_SETUP.md.jinja`. Besides the one-time GitHub
settings it lists the conventions a template repo keeps (a `## Credits` back
reference in the payload README, a full git URL as `_src_path`, no `_tasks`, the
payload's answers-file template, `_skip_if_exists` for owned files, custom
delimiters) and ends with a shell block that checks the four a script can see.
Someone runs the block by hand; `tests/test_repository_setup.py` here renders a
repo and runs it, with a failing case for each check.

The maintainer's request was for a dedicated guide file that enforces these
conventions; that part is confirmed. The reason it is a guide and not a seeded
test is the reading of `copier.yml`, not a stated one, hence the Evidence grade:
`tests/` is author-owned (`_skip_if_exists`), so a seeded test is written once and
never refreshed, while the guide is not in the list and `copier update` carries
new conventions into existing repos.

**Rejected alternative:** a seeded test in the generated `tests/test_template.py`.
It would run in CI, but could never receive a convention added later.

**Rejected alternative:** a seeded test that `copier update` may overwrite. It
would drop the author's own tests, which is why `tests/` is author-owned.

**Consequence:** the checks are not enforced by CI in generated repos. A shell
block cannot negate a command under `set -e` (`! grep` never aborts), so every
check calls an explicit `fail` helper, and the tests assert that each check fails
on its violation. The checks are text checks on purpose: no YAML parse, and an
`_src_path` only has to be an `https://` URL with a host and a path.

## Two conventions have no scriptable check

**Id:** 8369ecff-e7e5-4ec4-b69a-b2f701b056b8
**Type:** constraint
**Status:** active
**Evidence:** confirmed
**Source:** `tests/test_repository_setup.py`; the shipped `tests/test_template.py` update test; code review on the setup guide pull request
**Revisit when:** the shipped update test edits a project-owned payload file before updating
**See:** repository-setup-guide.md#template-conventions-are-checked-by-a-script-in-the-setup-guide-not-by-a-seeded-test — 0eec513d-8da2-4b5a-abf2-0dabf5862161 — as of 2026-10-24

`_skip_if_exists` ownership and the custom Jinja delimiters are listed as
conventions in the guide but are not in its check block. `mise run test` renders
the template and walks a `copier update`, which catches a payload that does not
render, but not a project-owned file missing from `_skip_if_exists`: the update
test tags an empty commit, so both versions render the same bytes and the
mistake only shows when the template next changes that file. The guide says so
and leaves it to review.

**Reason:** the mistake has no observable difference until a later template
change, so there is nothing for a script to assert on today.
