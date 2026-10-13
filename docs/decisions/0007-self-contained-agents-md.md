---
status: accepted
date: 2026-10-13
---

# Self-contained `AGENTS.md`, no `CLAUDE.md`

## Context and Problem Statement

Codex reads `AGENTS.md`, and Claude Code 2.1.277 or later reads it too when no `CLAUDE.md` exists. Git for Windows checks a symlink out as a file holding only its target path unless Developer Mode is on, and `claude plugin validate` warns about a `CLAUDE.md` at the plugin root. How do both agents get the same instructions?

## Considered Options

* `AGENTS.md` with all instructions, and no `CLAUDE.md`
* `AGENTS.md` with all instructions, `CLAUDE.md` as a one-line `@AGENTS.md` import
* `AGENTS.md` with all instructions, `CLAUDE.md` as a symlink to it
* `AGENTS.md` that points to writing skills installed outside the repository

## Decision Outcome

Chosen option: "`AGENTS.md` with all instructions, and no `CLAUDE.md`", because both agents read the one file in every checkout, and instructions without outside pointers work for any contributor's agent.

### Consequences

* Bad, because Claude Code before 2.1.277, or with its built-in `AGENTS.md` plugin disabled, loads no project instructions.
