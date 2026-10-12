---
status: accepted
date: 2026-10-12
---

# Separate Claude and Codex manifests

## Context and Problem Statement

Codex 0.162 falls back to `.claude-plugin/` when a repository has no Codex manifest, so one set of manifests could serve both agents. The fallback appeared in October 2026. Does the repository rely on it?

## Considered Options

* Codex manifests next to the Claude ones
* Claude manifests only, relying on the Codex fallback

## Decision Outcome

Chosen option: "Codex manifests next to the Claude ones", because a Codex install then does not depend on fallback behavior that is new and can change.

### Consequences

* Bad, because two plugin manifests repeat the same name and metadata.
