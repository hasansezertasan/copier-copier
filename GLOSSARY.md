# copier-copier

A Copier template that generates Copier template repositories named `copier-<subject>`, following the owner's conventions.

## Language

**Template repo**:
A repository named `copier-<subject>` whose purpose is to be applied with Copier to produce projects.
_Avoid_: Template project, copier repo

**Subject**:
The thing a template repo generates, and the only name the generator asks for. The repo name is derived from it as `copier-<subject>`.
_Avoid_: Repo name, project name, topic

**Generated template repo**:
A template repo produced by running copier-copier.
_Avoid_: Child template, output repo

**Payload**:
The `template/` subdirectory of a template repo: the files that end up in projects generated from it. A generated template repo starts with a minimal placeholder payload.
_Avoid_: Template contents, template dir

**Scaffolding**:
Everything in a template repo outside the payload: `copier.yml`, tests, CI, Renovate config, release-please config, README, LICENSE.
_Avoid_: Boilerplate, infrastructure

**Self-hosting**:
copier-copier's own repository being an application of itself, kept in sync with its own template via `copier update`.
_Avoid_: Dogfooding, bootstrapping
