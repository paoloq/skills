---
status: accepted
date: 2026-10-12
---

# Spec frontmatter plus one invocation key

## Context and Problem Statement

A skill that fires only when the user types its name loads nothing into sessions that never use it. Claude marks one with `disable-model-invocation: true`, a key outside the six the Agent Skills spec allows. Which frontmatter keys may a skill use?

## Considered Options

* The six spec keys plus `disable-model-invocation`
* The six spec keys only
* Any key Claude Code accepts

## Decision Outcome

Chosen option: "The six spec keys plus `disable-model-invocation`", because it is the one Claude extension a user-invoked skill needs, and every other key stays portable.

### Consequences

* Bad, because a user-invoked skill fails claude.ai uploads and a plain `skills-ref validate`, which both reject keys outside the spec.
