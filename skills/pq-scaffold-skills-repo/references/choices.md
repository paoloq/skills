# Scaffold choices

The choices, in the order to ask them, with the edits each answer makes to the target's copy.

- Text in quotes is source text to find; text after → replaces it. Where a quote holds `pq`, find the plugin name instead, since [Every scaffold](#every-scaffold) runs first.
- Steps of `CONTRIBUTING.md` are named by their opening words, which stay stable while other edits delete steps.
- A choice marked **open** also takes any tool the user names; follow [Another tool](#another-tool).
- A choice's **Pitch** is what the user reads when deciding: what the default gives them, and what they lose without it. Its **Show**, when it has one, names what to put in front of the user as a table when asking it.

## Every scaffold

Apply these whatever the answers:

1. Replace the source's identity in every copied regular file, in this order:
   - "https://github.com/paoloq" → the author URL, only where a `"` follows it, which is in the manifests' `url` fields; matching that quote leaves alone an owner whose name starts with `paoloq`.
   - "paoloq/skills" → `<owner>/<repo>`.
   - "Paolo Arduin's agent skills." → the description, then "Paolo Arduin" → the author.
   - Every whole word "pq" → the plugin name; it names the plugin, the marketplace, and the skill prefix. Match it as a whole word, as the regex `\bpq\b` does; macOS `sed` ignores `\b`.
   - Every record's `date:` in `docs/decisions/` → today, leaving the placeholder in `adr-template.md`, and "Copyright (c) 2026" in `LICENSE` → this year.
2. Delete the "## Scaffold source" section of `AGENTS.md`; it describes this wizard's source, not the new repository.
3. After the answers' edits, renumber every list they shortened and repair any sentence a deleted clause left broken.

## Identity

Ask these together as the new repository's identity, proposing values from the target:

| Value | Proposal |
|---|---|
| Owner and repository | `git remote get-url origin`, else ask |
| Plugin name | ask; suggest the author's initials |
| Author | `git config user.name`, else `gh api user --jq .name`, else ask |
| Author URL | `gh api user --jq .html_url`, else `https://github.com/<owner>` |
| Description | `<author>'s agent skills.` |

The plugin name takes lowercase letters, digits, and hyphens, and cannot start with `claude-` or `anthropic-`, which Claude Code reserves. It also names the marketplace and, by default, prefixes every skill, so keep it short.

## Claude Code plugin

Pitch: Claude Code users install every skill at once with `/plugin install` and update it with one command. Without it, they install through `npx skills`.

Default: yes. Ships `.claude-plugin/` so Claude Code installs the collection with `/plugin install`.

No:
- Delete `.claude-plugin/` and `mise-tasks/check/plugin`, and the `claude-code` tool in `mise.toml`.
- In `README.md`, delete the "Claude Code:" line and the code block under it, and under "## Update" the paragraph that starts "Claude Code updates only" and the code block under it.
- In `docs/decisions/0001-…`, delete the consequence that starts "Bad, because Claude names plugin skills".
- In `docs/decisions/0005-…`, delete the sentence "A `version` in `plugin.json` keeps Claude Code users on that version until someone changes the string." and the consequence that starts "Bad, because `claude plugin validate` warns".
- In `docs/decisions/0007-…`, delete ", and `claude plugin validate` warns about a `CLAUDE.md` at the plugin root".
- Apply [One agent dropped](#one-agent-dropped) for Claude Code, unless the Codex plugin is off too.

## Codex plugin

Pitch: Codex users install every skill at once with `codex plugin add` and update it with one command. Without it, they install through `npx skills`.

Default: yes. Ships `.codex-plugin/` and `.agents/plugins/` so Codex installs the collection with `codex plugin add`.

No:
- Delete `.codex-plugin/` and `.agents/plugins/`.
- In `README.md`, delete each "Codex:" line and the code block under it, under "## Install" and "## Update".
- Apply [One agent dropped](#one-agent-dropped) for Codex, unless the Claude Code plugin is off too.

### One agent dropped

Drop the agent from each sentence that names both "Claude Code" and "Codex" as plugin targets:
- `README.md`: "for Claude Code and Codex".
- `AGENTS.md`: "to Claude Code and Codex".
- `docs/decisions/0005-…`: the clause on the dropped agent in "Claude Code uses the commit SHA, Codex reinstalls a plugin whenever its marketplace upgrade pulls new commits".

The decision record for this choice is 0002; see [Decision records](#decision-records). Every other mention stays: it describes how each agent works with skills, which holds without the plugin.

### Both plugins dropped

Apply both "No" lists above, without [One agent dropped](#one-agent-dropped), then:
- In `README.md`:
  - "They ship as the plugin `pq` for Claude Code and Codex, and as plain skills" → They ship as plain skills.
  - Delete the line "Pick one route per agent; installing through both gives you every skill twice."
  - "Any other agent:" → Any agent:, in both sections.
  - "The plugin has no versions, so every merge to `main` is an update, and it reaches you when you update." → Every merge to `main` reaches you when you update.
- In `AGENTS.md`, "shipped as the plugin `pq` to Claude Code and Codex and as plain skills to `npx skills`." → shipped as plain skills to `npx skills`; [CONTRIBUTING.md](CONTRIBUTING.md) covers the pull request flow., and delete the "## Manifests" section.
- In `CONTRIBUTING.md`, "The plugins carry no version, so a merge reaches users" → A merge reaches users.
- Delete `mise-tasks/check/manifests`, `docs/decisions/0002-…`, and `docs/decisions/0003-…`; with no plugin manifest, nothing is left for them to guard.
- In `docs/decisions/0001-…`, drop ", one plugin" from both the option and the "Chosen option" quote, which must stay identical, and retitle → Flat skills with a shared name prefix. When the prefix is none too, retitle → Flat skills.
- In `docs/decisions/0005-…`, change "Without one, Claude Code uses the commit SHA, Codex reinstalls a plugin whenever its marketplace upgrade pulls new commits, and `npx skills` compares" → `npx skills` compares, and retitle → No versions: npx skills tracks each skill's contents.

## Skill name prefix

Pitch: every skill name starts with the plugin name, such as `ak-review`, so it cannot clash with a same-named skill from another collection once installed side by side. Without it, names are shorter but can collide.

Default: `<plugin name>-` on every skill, so names stay unique where installers drop the plugin namespace.

None:
- In `mise.toml`, set `SKILL_PREFIX = ""`.
- In `AGENTS.md`, change "skills/pq-<name>/SKILL.md" → skills/<name>/SKILL.md.

## Frontmatter

Pitch: a skill can be made typed-only, so it runs when the user types its name and costs no context in sessions that never use it; such a skill cannot be uploaded to claude.ai. Spec keys only keeps every skill uploadable anywhere, but each one can then fire on its own.

Default: the six spec keys plus `disable-model-invocation`, so a skill can fire only when typed.

Spec keys only:
- In `mise.toml`, set `SKILL_INVOCATION_KEY = ""`.
- In `AGENTS.md`, change "spec keys plus `disable-model-invocation`" → spec keys, keeping its link; delete the line that starts "A skill that fires only when the user types its name"; and delete the sentence that starts "A user-invoked skill's `description`".

## Task runner

Pitch: mise installs pinned versions of every tool and runs all the checks with one command, the same way on a laptop and in CI.

Default: mise pins the tools and runs the checks as tasks, and `mise run check` is the gate. **Open**: the gate becomes the named tool's command that runs every `mise-tasks/check/*` script and `hk check --all`, or the workflow linter itself when hk goes. When the user also drops mise for pinning tools, have the named tool install them, or list them in the README's "## Development" section. Its record is 0006.

## Git hooks

Pitch: before each commit, the hook runs the same checks as CI and rejects a commit message that is not a Conventional Commit, so problems surface before a push. Without it, the checks surface in CI, and the hk linters for merge-conflict markers, final newlines, and trailing whitespace go away.

Default: hk runs `mise run check` before each commit, and hosts the linters in `hk.pkl`, such as the workflow linter, which the gate runs through the `check:lint` task. **Open**: the named tool runs the gate before each commit, and checks commit messages against Conventional Commits; the linters move to it, or to mise tasks. Its record is 0006.

None:
- Delete `hk.pkl`, and the `hk` tool in `mise.toml`.
- In `mise.toml`, replace the `[tasks."check:lint"]` table with a `[tasks."check:workflows"]` table whose `run` is `jactionlint` and whose description is "Lint the GitHub Actions workflows".
- Tell the user, in the round that raises it, that the merge-conflict, final-newline, and trailing-whitespace linters go with hk; only the workflow linter moves to mise.
- In `README.md`, delete the line "mise exec -- hk install".
- In `CONTRIBUTING.md`, replace the step that starts "Commit with" → Commit with [Conventional Commits](https://www.conventionalcommits.org) messages.
- In `AGENTS.md`, change "the hk pre-commit hook and CI run it too" → CI runs it too.
- In `AGENTS.md`, change "Write task and hook commands" → Write task commands.
- In `docs/decisions/0006-…`, retitle → mise runs the tasks, keeping its file name, and change "locally, before a commit, and in CI" → locally and in CI; its options stay, since they compare task runners.

## CI

Pitch: every push and pull request runs the checks, and the branch rule blocks a merge until they pass.

Default: GitHub Actions, through `.github/workflows/ci.yml`, runs the gate on every push and pull request to `main`; a final job named `check` passes only when every gate run passes, so the ruleset requires that one job. **Open**: the named CI runs the gate on the same events and operating systems. With a CI other than GitHub Actions, skip [Workflow linter](#workflow-linter) and apply its None, and drop the whole `required_status_checks` rule from the ruleset in [GitHub settings](#github-settings), since GitHub no longer receives the `check` job.

## Workflow linter

Pitch: catches mistakes in the CI workflow files, such as a wrong action input or an unsafe permission, before they run.

Default: jactionlint lints the GitHub Actions workflows as the `jactionlint` step in `hk.pkl`'s `linters`, which `mise run check` runs through `hk check --all`. **Open**: the named linter replaces that step, through hk's builtin for it when one exists, else as a `check` command; when hk is gone, it runs as the `check:workflows` task.

None: delete the `["jactionlint"]` line from `hk.pkl`, or the `[tasks."check:workflows"]` table from `mise.toml` when hk is gone, and the `jactionlint` tool from `mise.toml`.

## Windows support

Pitch: contributors on Windows get the same checks, and CI proves it on a Windows runner for every pull request. Without it, CI runs on Linux only and finishes sooner, and Windows may break unnoticed.

Default: yes. CI runs the gate on `ubuntu-latest` and `windows-latest`. The repository's other Windows fixes, such as LF endings and no symlinks, stay either way, since they cost nothing elsewhere.

No:
- In `.github/workflows/ci.yml`, change "os: [ubuntu-latest, windows-latest]" → os: [ubuntu-latest]. With a CI other than GitHub Actions, run that CI on Linux only.
- In `mise.toml`, delete the `PYTHONUTF8` line and the comment above it.
- In `AGENTS.md`, under "## Windows", replace the line that starts "CI runs the gate on Windows too" → Keep every file working on Windows, should the repository support it later:

## Decision records

Pitch: [MADR](https://adr.github.io/madr/) (Markdown Architectural Decision Records) keeps one short file per lasting choice: the problem, the options weighed, the one chosen and its downsides. The repository starts with records for the setup choices, rewritten to match your answers, so you and later agents know why something is set up a certain way before changing it. Without them, the reasons live only in commit messages.

Show: the title of each record in the source's `docs/decisions/`, rewritten for the answers given so far.

Default: MADR records in `docs/decisions/`, updated to match these answers.

Choices map to records: the plugins to 0002, the prefix to 0001, frontmatter to 0004, Windows support to 0008. When such an answer differs from the default, edit its record in place, since the new repository has no history to supersede:
- Retitle it after the chosen option, rename its file to match, and fix links to the old name.
- List the chosen option under "Considered Options", adding it when missing, and keep the rejected default there.
- Rewrite "Chosen option" with the user's reason, and edit or delete any context sentence or consequence that no longer holds.

The plugin and hook sections above name their own record edits. Records whose choices kept their defaults stay as copied.

None:
- Delete `docs/decisions/`.
- In `AGENTS.md`, delete each link that starts " ([why](docs/decisions/", through its closing parenthesis, and the "## Decisions" section.
- In `README.md`, ", [AGENTS.md](AGENTS.md) holds the authoring rules, and [docs/decisions/](docs/decisions/) records why the repository is set up this way." → and [AGENTS.md](AGENTS.md) holds the authoring rules.
- In `CONTRIBUTING.md`, ", skill-authoring rules in [AGENTS.md](AGENTS.md), and the reasons behind the setup in [docs/decisions/](docs/decisions/)." → and skill-authoring rules in [AGENTS.md](AGENTS.md)., and delete " ([why](docs/decisions/0005-no-versions.md))".
- Delete the reference to `docs/decisions/` from each comment in `mise-tasks/check/manifests` and `mise-tasks/check/plugin`, where those files remain.

## Pull request template

Pitch: a pull request description form written for AI agents. Squash merges turn it into the commit message, so `main`'s history stays readable. Without it, descriptions are free-form.

Show: each `##` section of the source's `.github/pull_request_template.md`, with what its comment asks for in a few words.

Default: `.github/pull_request_template.md`, written for agent authors.

None:
- Delete the file.
- In the `CONTRIBUTING.md` step that starts "Push and open", delete ", with a body written from [the pull request template](.github/pull_request_template.md)" and the sentence that starts "`gh pr create --body`".

## Licence

Pitch: the terms under which others may use, change, and share the skills. MIT allows all of it with attribution and no warranty.

Default: the identifier of the target's existing `LICENSE` when it has one, matched against the SPDX licence texts and confirmed with the user; else MIT.

When the identifier is not MIT:
- Replace `LICENSE` with the text at `https://raw.githubusercontent.com/spdx/license-list-data/main/text/<id>.txt`, or with the target's original `LICENSE` when the default came from it; when the fetch fails, ask the user for the licence text. Fill the copyright holder and year only when the text opens with a copyright line, as MIT and BSD do; keep other texts, such as Apache-2.0, verbatim, including their appendix placeholders.
- Set the `license` field of each `plugin.json` to the identifier.

## Outside pull requests

Pitch: whether `CONTRIBUTING.md` invites pull requests from other people, or states that the collection is maintained privately.

Default: not accepted.

Accepted, in `CONTRIBUTING.md`:
- "This collection takes no outside pull requests." → Outside pull requests are welcome; open an issue before proposing a new skill.
- "Branch from `main`;" → Fork the repository or branch from `main`;.

## Security reports

Pitch: where someone reports a vulnerability privately: GitHub's private reporting form, an email address, or nowhere.

Default: GitHub private vulnerability reporting.

- Email: in `CONTRIBUTING.md`, replace the sentence under "## Security" → Report a vulnerability privately to <email>, never in an issue or pull request.
- None: delete the "## Security" section.

## Another tool

When the user names a tool for an open choice:

1. Tell the user, in the round that raises it, that the wizard has not tested that tool and will set it up to do the default's job.
2. Replace the default's files with the named tool's own setup, doing the same job on the same triggers, and swap the default's entry in `mise.toml` for the named tool's while mise stays.
3. Replace every mention of the default and its commands across `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `.github/pull_request_template.md`, the remaining workflows, and `hk.pkl` when it stays.
4. When the decision records stay, rewrite the record the choice names, or add one from `docs/decisions/adr-template.md` when it names none.

Step 5 then installs and runs the named tool instead of the default.

## GitHub settings

Not asked in step 3; step 6 and step 8 propose these. When the repository does not exist on GitHub yet, or `gh auth status` fails, list the settings for the user to apply later instead: one plain line each, with the commands offered on request. When GitHub rejects a setting for the repository's plan or visibility, list it the same way.

In step 6:

- Squash merges only, titled from the pull request, so `main` gets one commit per pull request.

  ```sh
  gh api -X PATCH repos/<owner>/<repo> -F allow_merge_commit=false -F allow_rebase_merge=false -F allow_squash_merge=true -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=PR_BODY
  gh api repos/<owner>/<repo> --jq '{allow_merge_commit, allow_rebase_merge, allow_squash_merge, squash_merge_commit_title, squash_merge_commit_message}'
  ```

- When security reports go through GitHub: private vulnerability reporting on.

  ```sh
  gh api -X PUT repos/<owner>/<repo>/private-vulnerability-reporting
  gh api repos/<owner>/<repo>/private-vulnerability-reporting --jq .enabled
  ```

In step 8, after the user pushes the scaffold to `main`, because the ruleset rejects direct pushes:

- A ruleset on `main`: changes only through squash-merged pull requests, no force-push, no deletion, linear history, and the CI job `check` must pass.

  First list the rules already active on `main`; the rulesets list itself omits which branch each ruleset targets:

  ```sh
  gh api repos/<owner>/<repo>/rules/branches/main --jq '[.[] | {type, ruleset_id}]'
  ```

  When that shows no `ruleset_id`, create the ruleset:

  ```sh
  gh api -X POST repos/<owner>/<repo>/rulesets --input - <<'JSON'
  {
    "name": "main",
    "target": "branch",
    "enforcement": "active",
    "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
    "rules": [
      {"type": "deletion"},
      {"type": "non_fast_forward"},
      {"type": "required_linear_history"},
      {"type": "pull_request", "parameters": {"required_approving_review_count": 0, "dismiss_stale_reviews_on_push": false, "require_code_owner_review": false, "require_last_push_approval": false, "required_review_thread_resolution": false, "allowed_merge_methods": ["squash"]}},
      {"type": "required_status_checks", "parameters": {"strict_required_status_checks_policy": false, "required_status_checks": [{"context": "check", "integration_id": 15368}]}}
    ]
  }
  JSON
  ```

  When it shows a `ruleset_id`, update that ruleset instead of creating a second one: read it with `gh api repos/<owner>/<repo>/rulesets/<id>`, add the rules it lacks to its own, and send the merged `name`, `target`, `enforcement`, `bypass_actors`, `conditions`, and `rules` with `gh api -X PUT repos/<owner>/<repo>/rulesets/<id> --input -`.

  Read back with the same `rules/branches/main` call: it lists all five rule types.
