# pq skills

A collection of agent skills, shipped as the plugin `pq` to Claude Code and Codex and as plain skills to `npx skills`. `mise run check` is the gate; the hk pre-commit hook and CI run it too. [CONTRIBUTING.md](CONTRIBUTING.md) covers setup and the pull request flow.

Keep every agent instruction in this file, and add no `CLAUDE.md`: Claude Code 2.1.277 or later reads `AGENTS.md` when no `CLAUDE.md` exists, and `claude plugin validate` warns about one at the plugin root.

## Skills

- A skill lives in `skills/pq-<name>/SKILL.md`; the folder is the whole skill, because `npx skills` copies only that folder.
- Start every skill name with `pq-`: Codex and `npx skills` install skills without the plugin namespace, so the prefix keeps names unique next to other collections.
- Frontmatter uses the six Agent Skills spec keys plus `disable-model-invocation`, the one Claude extension a user-invoked skill needs; every other key stays portable.
- A skill that fires only when the user types its name sets `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; Claude reads the first, Codex the second.
- A model-invoked skill's `description` is a context pointer loaded in every session: lead with what the skill does, then one trigger per distinct case. A user-invoked skill's `description` is a one-line summary for the human.
- Write the body as ordered steps, each ending on a completion criterion the agent can check; push material only some cases need into a sibling file the step links.
- Keep paths in a skill relative to its own folder.
- List each skill in the README's "## Skills" section with a one-line purpose, adding the section with the first skill.

## Windows

CI runs the gate on Windows too, so keep every file working there:

- Write regular files, never symlinks: Git for Windows checks a symlink out as a file holding its target path.
- Start a Python check script with the `#!/usr/bin/env -S uv run --script` shebang; mise reads it on Windows, where `python3` is often missing or a Microsoft Store placeholder.
- Write task and hook commands as one program and its arguments; on Windows they run through `cmd.exe`.

## Scaffold source

[pq-scaffold-skills-repo](skills/pq-scaffold-skills-repo/SKILL.md) builds new repositories by copying this one from `main` and editing the copy per [its choices table](skills/pq-scaffold-skills-repo/references/choices.md). When a change adds, removes, or renames a repository file, or moves text the table names, update the table in the same change.
