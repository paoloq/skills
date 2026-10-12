---
status: accepted
date: 2026-10-12
---

# Self-contained `AGENTS.md`, `CLAUDE.md` as a symlink

## Context and Problem Statement

Codex reads `AGENTS.md` and Claude Code reads `CLAUDE.md`. The repository root is also the plugin root, where `claude plugin validate --strict` rejects a regular `CLAUDE.md` file. How do both agents get the same instructions?

## Considered Options

* `AGENTS.md` with all instructions, `CLAUDE.md` as a symlink to it
* `CLAUDE.md` as a one-line `@AGENTS.md` import
* `AGENTS.md` that points to writing skills installed outside the repository

## Decision Outcome

Chosen option: "`AGENTS.md` with all instructions, `CLAUDE.md` as a symlink to it", because the symlink passes strict validation where the import file fails, and instructions without outside pointers work for any contributor's agent.

### Consequences

* Bad, because a checkout without symlink support, such as Windows without developer mode, gets a `CLAUDE.md` holding only the path.
