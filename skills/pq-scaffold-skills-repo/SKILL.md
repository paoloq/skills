---
name: pq-scaffold-skills-repo
description: Scaffold an empty repository into a skills collection for Claude Code, Codex, and npx skills, tailored through an interview.
disable-model-invocation: true
---

# Scaffold a skills repository

Build a skills collection by copying paoloq/skills, itself a working collection, and tailoring the copy to the user's answers. [references/choices.md](references/choices.md) lists every choice with its default, its supported alternatives, and the exact edits each answer makes. Offer the alternatives it lists; a choice the table marks **open** also takes any tool the user names.

## Voice

Talk like a friendly, brief setup wizard about the user's new repository. The copied source and the table's replacements are how you build it, so they stay behind the scenes.

- Each step speaks once, when it is done, opening with its badge; when one reply covers several steps, their parts follow the step order: 🔍 Checking the folder, 🎒 Getting ready, 🎤 Interview, 🛠️ Building, ✅ Checking, ⚙️ GitHub, 🧹 Tidying up, 🚀 All set.
- A progress note while you work is one badge line about the user's repository, such as "🛠️ Building your plugin files…" or "✅ Running the checks…".
- Name what comes later by what it does, such as "the GitHub settings", since the user never sees these steps' numbers.
- Mark every recommended answer with ⭐.

## 1. Confirm the target

The target is the current directory unless the user names another. It qualifies when both of these hold:

- It is a Git repository; when it is not, offer `git init -b main`.
- Its working tree holds nothing beyond `.git`, `README.md`, `LICENSE`, and `.gitignore`. When `README.md` or `LICENSE` exists, tell the user the scaffold replaces it.

Any branch and any history are fine: the scaffold can land on a feature branch through a pull request. The workflows and the ruleset assume the repository's default branch is `main`; when the remote's default branch, from `git ls-remote --symref origin HEAD`, is another one, tell the user.

When the working tree holds anything else, such as `skills/` or `mise.toml`, stop and tell the user this wizard scaffolds new repositories only.

Done when the target qualifies, or you have stopped.

## 2. Fetch the source

Clone `main` of paoloq/skills, which takes changes only through pull requests that pass CI, into a new temporary folder:

```sh
source_dir=$(mktemp -d /tmp/pq-scaffold.XXXXXX) && echo "$source_dir"
git clone --quiet --depth 1 https://github.com/paoloq/skills "$source_dir"
```

Shell variables do not survive between commands, so write the printed path literally in every later command; this document calls it the source folder.

When the user names a local clone of paoloq/skills instead, run only the `mktemp` line, then copy the clone's working tree into the source folder without its top-level `.git`, a folder in a clone and a file in a worktree. Tell the user in one line that uncommitted work in that folder is included.

Done when every file and every quoted source text that [references/choices.md](references/choices.md) names exists in the source folder. When one is missing, the table is out of date: clean up (step 7), stop, and tell the user.

## 3. Interview the user

Interview the user from [references/choices.md](references/choices.md) in rounds, in plain chat. Each round is one message: the round's table written out in full, then its one-line question as the last line, ending your turn so the user reads the table and replies. A question picker would hide the table behind it, so the rounds use chat replies.

1. **🎤 Identity:** a table of the identity values with your proposals; ask the user to reply `ok` or say what to change.
2. **⚡ Express:** a table of every remaining choice in the table's order, one row each: number, choice, ⭐ answer in a few plain words, what it gives the user from its pitch in one line, and its alternatives, ending with "or another tool" for an open choice. Ask the user to reply `ok` to take them all, name the numbers to change, or say "one by one". For "one by one", ask each choice in its own short message, numbered as "🎤 3/14 · Skill name prefix", opening with its pitch and its **Show** table, when it has one, so the user can judge before answering.
3. **🎤 Summary:** a table with one row per identity value and one row per choice, in the table's order; ask the user to reply `ok` to build it or say what to change.

Ask a follow-up value, such as a licence identifier or an email address, in the round that raises it, and skip a choice an earlier answer settles.

Done when the user has replied `ok`, or any plain yes, to the summary.

## 4. Write the files

1. Copy the source folder into the target, except the top-level `/.git`, `/skills`, `/mise.lock`, and `/.mise`. Anchor each exclusion to the top level, as rsync's `--exclude=/skills` does, so `mise-tasks/check/skills` is copied. Keep symlinks as symlinks: `CLAUDE.md` must stay a link to `AGENTS.md`, because `claude plugin validate --strict` rejects a regular file there.
2. Apply "Every scaffold" in the table, then each answer's edits, including the decision records it changes.

Done when every edit "Every scaffold" and the answers call for is applied, and a search of the target outside `.git` finds only the user's own values for `paoloq`, `Paolo Arduin`, the whole word `pq`, and `2026-10-12`, and no "## Scaffold source" heading.

## 5. Verify

In the target, set up the chosen tools and run the gate. With the defaults: confirm that `mise --version` is at least the `min_version` in `mise.toml`, then run `mise trust`, `mise install`, `mise lock`, `mise exec -- hk install` when hooks stay, and `mise run check`; `mise install` writes `mise.lock` for this machine only, and `mise lock` adds the other platforms, such as the Linux one CI runs on. With another tool, run its own install and gate commands. When a check fails in a generated file, fix that file; the checks encode the answers.

Done when the gate passes and, while mise stays, `mise.lock` lists `linux-x64`. When a chosen tool is missing or too old, the network fails, or a failure lies outside the generated files, clean up (step 7), stop, and tell the user what failed.

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
