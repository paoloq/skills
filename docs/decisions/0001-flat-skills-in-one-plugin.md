---
status: accepted
date: 2026-10-12
---

# Flat skills in one plugin named `pq`

## Context and Problem Statement

Installers that copy bare skills, such as Codex's `$skill` and `npx skills`, drop the plugin namespace, so a skill name has to stay unique next to skills from other collections. How are skills laid out and named?

## Considered Options

* Flat `skills/<name>/SKILL.md`, one plugin, `pq-` prefix on every skill
* Category folders `skills/<category>/<name>/SKILL.md`
* One plugin per category

## Decision Outcome

Chosen option: "Flat `skills/<name>/SKILL.md`, one plugin, `pq-` prefix on every skill", because Claude Code, Codex, `npx skills`, and `gh skill` all find a flat `skills/` without a skill list, while category folders need every path listed in the manifest and `npx skills` still installs every category.

### Consequences

* Bad, because Claude names plugin skills `/pq:pq-<name>`, repeating the prefix.
* Bad, because every skill ships to every installer; `metadata.internal: true` is the only way to hide a draft from `npx skills`.
