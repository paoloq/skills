---
status: accepted
date: 2026-10-12
---

# mise runs the tools and tasks, hk runs the hooks

## Context and Problem Statement

The checks need pinned tools (uv, Node, the Claude Code CLI, `skills`, actionlint) and the same commands locally, in a pre-commit hook, and in CI. Which task runner sits next to mise?

## Considered Options

* mise tasks
* go-task
* just

## Decision Outcome

Chosen option: "mise tasks", because mise already pins the tools, so the repository needs no second runner for its few checks. jdx/mise, jdx/hk, exercism/rust, LucasPickering/slumber, and blacknon/hwatch run their tasks the same way.

[mise.toml](../../mise.toml) declares the tools and short tasks; longer checks are scripts in [mise-tasks/](../../mise-tasks). `mise run check` is the gate: [hk.pkl](../../hk.pkl) runs it before every commit, and [CI](../../.github/workflows/ci.yml) runs it on every push and pull request.

### Consequences

* Good, because one tool installs and runs everything, locally and in CI through `jdx/mise-action`.
* Bad, because contributors need mise; `hk install` wires the hooks after cloning.
