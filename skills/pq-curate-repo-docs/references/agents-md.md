# AGENTS.md files

The root AGENTS.md is the working agreement every agent session loads; a nested AGENTS.md holds the rules of one component.

## Root file

1. Hold what most tasks need: what the project is, its commands, testing rules, conventions that span the codebase, commit and pull request rules, and boundaries: what to ask before doing, and what never to do.
2. List the commands an agent cannot guess, plus the gate, and point to CONTRIBUTING or the task runner's own listing for the rest.
3. Point to the doc that owns a topic, such as CONTRIBUTING, the coding standards, the decision records, or the skills folder, rather than copying it.
4. When the repository has nested AGENTS.md files, include the line "Before editing a file, read every AGENTS.md on the path from the root to it": Codex loads only the files on the path to its working directory, so a session started at the root misses the rest.
5. Keep it under 200 lines; past that, propose moving component rules into nested files and procedures into their owning docs rather than compressing it.

## Nested files

6. Create one for a component with rules of its own: its key files, invariants, pitfalls, and local commands. It holds that component's rules and leaves project-wide rules to the root.

## Wording

7. Write each instruction concretely enough to verify, such as "run the gate before committing" rather than "test your changes", and group instructions under headings.
8. Keep capitalized NEVER and MUST for the boundaries; everywhere else a plain imperative carries the rule.

## CLAUDE.md

9. When a CLAUDE.md exists, move its rules into AGENTS.md and propose deleting it: Claude Code reads AGENTS.md files, nested ones included, only when no CLAUDE.md is present. Older Claude Code versions read only CLAUDE.md, so say so in the proposal.
