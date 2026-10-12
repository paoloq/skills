---
status: accepted
date: 2026-10-12
---

# mise runs the tasks, hk runs the hooks

## Context and Problem Statement

The checks need pinned tools and must run the same way locally, before a commit, and in CI. mise already pins the tools. Which task runner sits next to it?

## Considered Options

* mise tasks
* go-task
* just

## Decision Outcome

Chosen option: "mise tasks", because a few checks do not earn a second runner next to the tool manager that already exists.

### Consequences

* Bad, because a contributor needs mise before any check runs.
