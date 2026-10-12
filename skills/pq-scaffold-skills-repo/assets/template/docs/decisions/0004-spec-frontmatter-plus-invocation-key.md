---
status: accepted
date: __DATE__
---

# Spec frontmatter plus one invocation key

## Context and Problem Statement

The Agent Skills spec allows six frontmatter keys: `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. A skill that fires only when the user types its name needs Claude's `disable-model-invocation: true`, which strict consumers (skills-ref, claude.ai uploads) reject. Codex expresses the same setting as `policy.allow_implicit_invocation: false` in the skill's `agents/openai.yaml`. Which frontmatter keys may a skill use?

## Considered Options

* The six spec keys plus `disable-model-invocation`
* The six spec keys only
* Any key Claude Code accepts

## Decision Outcome

Chosen option: "The six spec keys plus `disable-model-invocation`", because a user-invoked skill costs no context in sessions that never use it, and that one key is the only Claude extension it needs.

A user-invoked skill sets both `disable-model-invocation: true` and, in `agents/openai.yaml`, `policy.allow_implicit_invocation: false`. [check:skills](../../mise-tasks/check/skills) runs the skills-ref spec checks without that key and fails when the two settings disagree.

### Consequences

* Good, because user-invoked skills behave the same in Claude and Codex.
* Bad, because a user-invoked skill fails claude.ai uploads and `skills-ref validate` run directly.
