---
status: accepted
date: __DATE__
---

# Self-contained `AGENTS.md`, `CLAUDE.md` as a symlink

## Context and Problem Statement

Codex reads `AGENTS.md` and Claude Code reads `CLAUDE.md`. The plugin is the repository root, and `claude plugin validate --strict` fails on a regular `CLAUDE.md` file there, because Claude Code never loads a plugin's `CLAUDE.md` as context. How do both agents get the same instructions?

## Considered Options

* `AGENTS.md` with all instructions, `CLAUDE.md` as a symlink to it
* `CLAUDE.md` as a one-line `@AGENTS.md` import
* `AGENTS.md` that points to writing skills installed outside the repository

## Decision Outcome

Chosen option: "`AGENTS.md` with all instructions, `CLAUDE.md` as a symlink to it", because the symlink passes `claude plugin validate --strict` where the import file fails, and an `AGENTS.md` without outside pointers works for any contributor's agent. EveryInc/compound-engineering-plugin, vercel-labs/agent-skills, and wshobson/agents use the same symlink.

### Consequences

* Good, because both agents read one file.
* Bad, because a checkout without symlink support (Windows without developer mode) gets a `CLAUDE.md` holding only the path.
