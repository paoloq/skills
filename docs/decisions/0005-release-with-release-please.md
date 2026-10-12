---
status: accepted
date: 2026-10-12
---

# Release with release-please

## Context and Problem Statement

Claude Code keeps a user on the installed plugin until the manifest `version` changes, and Codex refreshes an installed plugin only on a version change. A release therefore has to bump the version in both plugin manifests at once. How are versions bumped and released?

## Considered Options

* release-please
* Changesets
* No version, so Claude tracks the commit SHA

## Decision Outcome

Chosen option: "release-please", because it derives the version and changelog from conventional commit messages and bumps both manifests through `extra-files` in [its config](../../release-please-config.json), with no Node package in the repository. EveryInc/compound-engineering-plugin releases the same way.

### Consequences

* Good, because merging the release pull request tags `vX.Y.Z`, publishes a GitHub release, and updates `CHANGELOG.md`.
* Good, because `bump-minor-pre-major` keeps breaking changes on `0.x` minor bumps until a deliberate `1.0.0`.
* Bad, because every commit on `main` must follow Conventional Commits; the hk `commit-msg` hook checks local commits and CI checks pull request titles, since a squash merge uses the title as the commit message.
