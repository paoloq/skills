---
status: accepted
date: 2026-10-12
---

# No versions: installers track the latest commit

## Context and Problem Statement

A `version` in `plugin.json` keeps Claude Code users on that version until someone changes the string. Without one, Claude Code uses the commit SHA, Codex reinstalls a plugin whenever its marketplace upgrade pulls new commits, and `npx skills` compares a hash of each skill folder. `main` takes changes only through pull requests that pass CI. Does the repository version its releases?

## Considered Options

* No versions; every merge to `main` reaches users at their next update
* Each pull request bumps the version, and every merge publishes it
* Tags and GitHub releases, with no version in the manifests

## Decision Outcome

Chosen option: "No versions; every merge to `main` reaches users at their next update", because no installer needs a version to deliver an update, while a version adds a bump to every pull request and lets two parallel pull requests claim the same one.

### Consequences

* Bad, because there is no changelog or release to pin; users get whatever `main` held at their last update.
* Bad, because `claude plugin validate` warns about the missing version, so `check:plugin` accepts that one warning instead of running `--strict`.
