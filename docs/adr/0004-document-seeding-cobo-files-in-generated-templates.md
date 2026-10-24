# Document seeding the cobo files in the generated template's config

`copier-copier` seeds `template/copier.yml` once and then leaves it to the author. A template that generates `.gitignore` and `cobo.lock` into its projects must not let `copier update` three-way merge them: cobo rewrites the sealed block and the lock in each project, so the template's copy would conflict. The author's own templates (copier-infra, copier-skills, copier-rust and the scoop and Homebrew ones) list those files in `_skip_if_exists`.

## Decision

The seeded `template/copier.yml` carries a commented `_skip_if_exists` block naming `.gitignore` and `cobo.lock`, with two notes the author needs: list only files the generated project's own `cobo.lock` tracks (a plain `.gitattributes` or `.editorconfig` nothing re-renders keeps receiving updates), and `_skip_if_exists` also applies to `copier copy --overwrite`, so adopters delete both files first to keep the pair matched.

## Considered Options

- **An active `_skip_if_exists` in the seed**: rejected, a new template's payload ships no cobo files, so an active entry would be a lie and the first author to add one would hit it silently.
- **Nothing, rely on the author remembering**: rejected, the miss is silent until the first update conflicts.
- **A conditional skip limited to updates**: not possible, Copier renders `_skip_if_exists` patterns without `_copier_operation` (it only offers that to `_exclude`).
