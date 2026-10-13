---
status: accepted
date: 2026-10-13
---

# Windows support, verified in CI

## Context and Problem Statement

Contributors may work on Windows, where Git converts line endings and drops symlinks, Codex runs PowerShell, and Python writes pipes in the locale encoding. Does the repository promise that the gate passes there?

## Considered Options

* Windows supported, with CI running the gate on Windows and Linux
* macOS and Linux only

## Decision Outcome

Chosen option: "Windows supported, with CI running the gate on Windows and Linux", because a Windows contributor then gets the same gate, and only a Windows runner proves it.

### Consequences

* Good, because `.gitattributes` keeps every text file on LF endings, and the check scripts run through `uv`, which needs no system Python.
* Bad, because the repository gives up symlinks, and each pull request waits for the slower Windows runner.
