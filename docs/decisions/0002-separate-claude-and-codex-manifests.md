---
status: accepted
date: 2026-10-12
---

# Separate Claude and Codex manifests

## Context and Problem Statement

Codex 0.162 reads `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` when no Codex manifest exists, so one set of manifests could serve both agents. That fallback is recent. Does the repository rely on it?

## Considered Options

* Explicit Codex manifests next to the Claude ones
* Claude manifests only, relying on the Codex fallback

## Decision Outcome

Chosen option: "Explicit Codex manifests next to the Claude ones", because Codex then reads its own [plugin manifest](../../.codex-plugin/plugin.json) (with the `interface` block its plugin browser shows) and its own [marketplace](../../.agents/plugins/marketplace.json), as obra/superpowers, EveryInc/compound-engineering-plugin, wshobson/agents, and openai/plugins do.

### Consequences

* Good, because the Codex install does not depend on fallback behavior that can change.
* Bad, because two plugin manifests carry the same name and version; release-please bumps both and [check:manifests](../../mise-tasks/check/manifests) fails when they disagree.
