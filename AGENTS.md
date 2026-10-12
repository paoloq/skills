# pq skills

A collection of agent skills, shipped as the plugin `pq` to Claude Code and Codex and as plain skills to `npx skills`. `mise run check` is the gate; the hk pre-commit hook and CI run it too.

## Skills

- A skill lives in `skills/pq-<name>/SKILL.md`; the folder is the whole skill, because `npx skills` copies only that folder.
- Frontmatter uses the six Agent Skills spec keys plus `disable-model-invocation` ([why](docs/decisions/0004-spec-frontmatter-plus-invocation-key.md)).
- A skill that fires only when the user types its name sets `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; Claude reads the first, Codex the second.
- A model-invoked skill's `description` is a context pointer loaded in every session: lead with what the skill does, then one trigger per distinct case. A user-invoked skill's `description` is a one-line summary for the human.
- Write the body as ordered steps, each ending on a completion criterion the agent can check; push material only some cases need into a sibling file the step links.
- Keep paths in a skill relative to its own folder.

## Releases

- Follow [CONTRIBUTING.md](CONTRIBUTING.md) for commit types, pull requests, and releases; a skill change users should get is `feat` or `fix`, never `docs`.
- release-please owns every `version` field; edit none by hand.
- Keep `plugin.json` out of the repository root: Codex would truncate every skill to 8,000 bytes ([why](docs/decisions/0003-no-root-plugin-json.md)).

## Mirrored files

[pq-scaffold-skills-repo](skills/pq-scaffold-skills-repo/SKILL.md) generates new repositories from copies of this repository's files in its `assets/` folder. When you change a mirrored file, make the same change to its copy there.

## Decisions

Lasting choices live in [docs/decisions/](docs/decisions/), one MADR record each. Record a new one by copying [adr-template.md](docs/decisions/adr-template.md) to the next free number; supersede a record with a new one rather than rewriting it.
