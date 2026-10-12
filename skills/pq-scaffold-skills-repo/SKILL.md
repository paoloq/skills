---
name: pq-scaffold-skills-repo
description: Scaffold an empty repository into a skills collection that installs in Claude Code, Codex, and npx skills.
disable-model-invocation: true
---

# Scaffold a skills repository

Turn an empty Git repository into a skills collection that ships as one plugin to Claude Code and Codex and as plain skills to `npx skills`. [assets/template/](assets/template/) is a complete copy of such a repository with placeholders; its `docs/decisions/` records explain every choice, so read one before changing what it covers.

## 1. Confirm the target

The target is the current directory unless the user names another. It qualifies when it is a Git repository holding nothing beyond `.git`, `README.md`, `LICENSE`, and `.gitignore`.

When it holds anything else, such as `skills/`, a plugin manifest, or `mise.toml`, stop and tell the user this skill scaffolds new repositories only.

Done when the target qualifies, or you have stopped.

## 2. Collect the values

Propose every value at once, filled from the repository where it shows them, and ask the user to confirm or change them in one reply.

| Placeholder | Value | Proposal |
|---|---|---|
| `__OWNER__` | GitHub owner | from `git remote get-url origin` |
| `__REPO__` | GitHub repository name | from the remote, else the directory name |
| `__PLUGIN__` | Name of the marketplace, the plugin, and every skill's prefix | ask; suggest the author's initials |
| `__AUTHOR__` | Name in the manifests and the licence | `git config user.name` |
| `__DESCRIPTION__` | One sentence describing the collection | `__AUTHOR__'s agent skills.` |
| `__DATE__` | Today, `YYYY-MM-DD` | today |
| `__YEAR__` | This year | this year |

`__PLUGIN__` takes lowercase letters, digits, and hyphens, and cannot start with `claude-` or `anthropic-`, which Claude Code reserves. Keep it short: Claude shows each skill as `/__PLUGIN__:__PLUGIN__-<name>`.

Done when the user has confirmed every value.

## 3. Write the files

1. Copy everything under [assets/template/](assets/template/) into the target, keeping relative paths and dot-directories. When the target already has a `README.md` or `LICENSE` with content, show the user both versions and ask which to keep.
2. Replace every placeholder in file contents with its confirmed value.
3. Run `chmod +x mise-tasks/check/*` and `ln -s AGENTS.md CLAUDE.md`. The symlink matters: `claude plugin validate --strict` rejects a regular `CLAUDE.md` at the plugin root.

Done when a search of the target for `__[A-Z]+__`, outside `.git`, finds nothing.

## 4. Verify

Run `mise trust`, `mise install`, `mise exec -- hk install`, and `mise run check` in the target. When a check fails, fix the generated file; the checks encode the decisions.

Done when `mise run check` passes.

## 5. Hand over

Tell the user what you wrote and the next steps:

- Add the first skill as `skills/__PLUGIN__-<name>/SKILL.md`, following the target's `AGENTS.md`.
- Commit everything, including the generated `mise.lock` and `.mise/locks/`, which pin the tool installs, with a Conventional Commits message, such as `feat: scaffold skills collection`, and push; release-please opens the first release pull request from `main`.
- The README holds the install commands for each agent.

Leave committing and pushing to the user.
