---
name: pq-scaffold-skills-repo
description: Scaffold an empty repository into a skills collection for Claude Code, Codex, and npx skills, tailored through an interview.
disable-model-invocation: true
---

# Scaffold a skills repository

Build a skills collection by copying paoloq/skills, itself a working collection, and tailoring the copy to the user's answers. [references/choices.md](references/choices.md) lists every choice with its default, its supported alternatives, and the exact edits each answer makes. Offer only those alternatives: when the user wants another, such as a different task runner or release tool, say the wizard does not support it and keep the default.

## 1. Confirm the target

The target is the current directory unless the user names another. It qualifies when all of these hold:

- It is a Git repository; when it is not, offer `git init -b main`.
- Its current branch is `main`, which the workflows and docs assume; when the repository has no commits yet, offer `git branch -m main`.
- It holds nothing beyond `.git`, `README.md`, `LICENSE`, and `.gitignore`. When `README.md` or `LICENSE` exists, tell the user the scaffold replaces it.

When it holds anything else, such as `skills/` or `mise.toml`, or has commits on another branch, stop and tell the user this wizard scaffolds new repositories only.

Done when the target qualifies, or you have stopped.

## 2. Fetch the source

Clone `main` of paoloq/skills, which takes changes only through pull requests that pass CI, into a new temporary folder:

```sh
source_dir=$(mktemp -d /tmp/pq-scaffold.XXXXXX) && echo "$source_dir"
git clone --quiet --depth 1 https://github.com/paoloq/skills "$source_dir"
```

Shell variables do not survive between commands, so write the printed path literally in every later command; this document calls it the source folder.

When the user names a local clone of paoloq/skills instead, run only the `mktemp` line, then copy the clone's working tree into the source folder without its top-level `.git`, a folder in a clone and a file in a worktree. Tell the user that uncommitted, untracked, and ignored files come along.

Done when every file and every quoted source text that [references/choices.md](references/choices.md) names exists in the source folder. When one is missing, the table is out of date: clean up (step 7), stop, and tell the user.

## 3. Interview the user

Grill the user through [references/choices.md](references/choices.md) in its order, one choice per question:

- Say what the choice decides, put the default first as the recommendation, and offer only its supported alternatives.
- Ask a follow-up value, such as a licence identifier or an email address, in the same question.
- Skip a choice an earlier answer settles.

Then show every answer in one summary and ask the user to confirm or change it.

Done when the user has confirmed the summary.

## 4. Write the files

1. Copy the source folder into the target, except the top-level `/.git`, `/skills`, `/mise.lock`, and `/.mise`. Anchor each exclusion to the top level, as rsync's `--exclude=/skills` does, so `mise-tasks/check/skills` is copied. Keep symlinks as symlinks: `CLAUDE.md` must stay a link to `AGENTS.md`, because `claude plugin validate --strict` rejects a regular file there.
2. Apply "Every scaffold" in the table, then each answer's edits, including the decision records it changes.

Done when every edit "Every scaffold" and the answers call for is applied, and a search of the target outside `.git` finds only the user's own values for `paoloq`, `Paolo Arduin`, the whole word `pq`, and `2026-10-12`, and no "## Scaffold source" heading.

## 5. Verify

In the target, confirm that `mise --version` is at least the `min_version` in `mise.toml`, then run `mise trust`, `mise install`, `mise lock`, `mise exec -- hk install` when hooks stay, and `mise run check`. `mise install` writes `mise.lock` for this machine only; `mise lock` adds the other platforms, such as the Linux one CI runs on. When a check fails in a generated file, fix that file; the checks encode the answers.

Done when `mise run check` passes and `mise.lock` lists `linux-x64`. When mise is missing or too old, the network fails, or a failure lies outside the generated files, clean up (step 7), stop, and tell the user what failed.

## 6. Apply GitHub settings

Follow "GitHub settings" in the table: propose the settings it lists for step 6, and run their commands only after the user agrees. Then run the table's read-back commands.

Done when every agreed setting reads back as set, or the user declined, or you listed a setting for the reasons the table gives.

## 7. Clean up

Delete the source folder, also when you stop at or after step 2.

Done when the source folder no longer exists.

## 8. Hand over

Tell the user what you wrote, which settings you changed, and the next steps:

- Commit everything, including the generated `mise.lock`, which pins the tool installs, and push it to `main`.
- After the user pushes the scaffold to `main`, apply the ruleset from "GitHub settings"; offer to run it once the user confirms the push. From then on, `main` takes changes only through pull requests.
- Add the first skill under `skills/` in a pull request, following the target's `AGENTS.md`; until then, the checks validate only the manifests.
- The README holds the install commands for each agent.

Leave committing and pushing to the user.
