---
status: accepted
date: 2026-10-12
---

# Flat skills in one plugin named `pq`

## Context and Problem Statement

Skills must install through Claude Code's and Codex's plugin installers and through cross-agent installers such as `npx skills`. Installers that copy bare skills drop the plugin namespace, so a skill name must stay unique next to skills from other collections. How are skills laid out and named?

## Considered Options

* Flat `skills/<name>/SKILL.md`, one plugin, `pq-` prefix on every skill
* Bucketed `skills/<category>/<name>/SKILL.md` with an explicit skill list in the manifest
* One plugin per category under `plugins/<plugin>/skills/`

## Decision Outcome

Chosen option: "Flat `skills/<name>/SKILL.md`, one plugin, `pq-` prefix on every skill", because Claude Code, Codex, `npx skills`, and `gh skill` all discover `skills/*/SKILL.md` without a skill list, and it is the layout of anthropics/skills, obra/superpowers, EveryInc/compound-engineering-plugin, vercel-labs/agent-skills, and K-Dense-AI/scientific-agent-skills.

The marketplace and the plugin are both named `pq`, and every skill name starts with `pq-`; [check:skills](../../mise-tasks/check/skills) enforces the prefix from the plugin name.

### Consequences

* Good, because a new skill ships by adding its folder; no manifest lists skills.
* Good, because a `pq-` skill keeps a unique name in installers that drop the plugin namespace (Codex `$pq-…`, `npx skills`).
* Bad, because Claude shows plugin skills as `/pq:pq-<name>`, repeating the prefix; the bare `/pq-<name>` also works unless another command takes that name.
* Bad, because every skill ships to every installer; a draft is hidden from `npx skills` only by `metadata.internal: true`.
