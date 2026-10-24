# Do not reseed deleted payload files on update

An adopted template repo has its own payload, so it deletes the seeded `template/PLACEHOLDER.md` and the default answers-file template `template/.copier-answers.yml.jinja` (copier-rust keeps its own under custom delimiters). Both sit under `template` in `_skip_if_exists`, but Copier skips a file there only when it exists: it recreates a deleted one on every `copier update`, so each update PR carries the two files back and the author deletes them again.

## Decision

List both paths in `_exclude`, each wrapped in `{% if _copier_operation == 'update' %}…{% endif %}`. A fresh copy still seeds them; an update never renders them, so a deleted file stays deleted and an author's edited one is left alone. `_exclude` honours the update-only condition, which `_skip_if_exists` patterns cannot (they are rendered without `_copier_operation`); `_min_copier_version` is already 9.10.3, the release from which excluded paths are protected on update.

## Considered Options

- **Add the paths to the adopted repo's own `_exclude`**: rejected, the repo's `copier.yml` configures it as a template for its projects, not how copier-copier updates it, and Copier takes no per-project exclude from the answers file.
- **Document deleting them after every update**: rejected, the adoption notes already say so and the work repeats on each update.
- **Drop the two seeds**: rejected, a new template repo needs both.

## Consequences

- An author who wants the seeds back copies them from a fresh render.
- Only these two payload files are covered; other deleted seeds under `template` are still recreated.
