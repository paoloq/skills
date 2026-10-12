---
status: accepted
date: __DATE__
---

# No root `plugin.json`

## Context and Problem Statement

The Agent Plugins format puts a `plugin.json` at the repository root that declares the agent-plugins.org schema. When Codex finds one, it treats the skills as Agent Plugin skills and truncates each `SKILL.md` to 8,000 bytes before the model reads it. Does the repository ship that manifest?

## Considered Options

* No root `plugin.json`
* A root Agent Plugins `plugin.json` next to the agent-specific manifests

## Decision Outcome

Chosen option: "No root `plugin.json`", because a silently truncated skill loses its later steps, and Codex reads the [Codex manifest](../../.codex-plugin/plugin.json) instead. [check:manifests](../../mise-tasks/check/manifests) fails when a root `plugin.json` appears.

### Consequences

* Good, because skill bodies reach Codex whole.
* Bad, because installers that read only the Agent Plugins manifest see no plugin metadata; they still find the skills under `skills/`.
