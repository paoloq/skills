---
name: pq-curate-repo-docs
description: Decides whether a repository doc change earns a line, where it lives, and how to word it. Applies before adding, editing, or deleting a repo's AGENTS.md, CLAUDE.md, README, CONTRIBUTING, coding standards, or decision record; when asked to record a rule or decision; and when a code change or rename makes a doc statement false. Not for skills, changelogs, docs sites, runbooks, or answering questions from the docs.
---

# Curate repo docs

Repo docs carry what is costly to reconstruct: traps, contracts, reasons, and procedures. The code, tests, configuration, and tool help are the source of truth; a doc that restates them is a cache that goes stale. The repository's own rules for its docs override this skill.

## 1. Decide whether it earns a line

A fact earns a line when it is all of these:

- **Not derivable:** a reader of the code, configuration, or tool help would still get it wrong or need long to work it out.
- **Costly:** getting it wrong breaks a contract, leaks data, duplicates a side effect, or wastes significant time or money.
- **Not enforced:** no configured check catches it; when a reliable check can, configure the check instead.
- **Durable:** it stays true through ordinary changes; status, history, incident stories, and inventories fail this, since git and the code hold them.
- **Grounded:** current code, tests, configuration, or an explicit maintainer decision supports it; past commits alone make no rule.

A README or CONTRIBUTING also holds what its reader needs to start or to contribute; its reference says what earns a line there. Look for a trap where a mistake repeats, review keeps catching it, or working it out took many files.

Done when the fact passes every test, or you drop it and tell the user which test it failed.

## 2. Find its home

List the doc homes this repository has, then put the fact in the narrowest one:

| What you have | Home |
|---|---|
| A one-off preference or task detail | Nowhere |
| Behavior that must not regress | A test |
| A rule a tool can check | That tool's configuration |
| Why one piece of code looks wrong but is right | A comment beside that code |
| How a user installs and uses the project or a package | Its README |
| How the parts fit together | An existing docs page, linked from the README |
| How a contributor prepares, checks, and lands a change, development commands included | CONTRIBUTING |
| Per-pull-request evidence | The pull request template |
| A review criterion no tool checks | The coding standards |
| Why a lasting choice was made | A decision record |
| A rule agents need on most tasks | The root AGENTS.md |
| Rules that hold only for one component | That component's nested AGENTS.md |
| Security reporting or code ownership | SECURITY.md or CODEOWNERS |
| A repeatable procedure | A skill: hand it to a skill-authoring skill when one is installed; otherwise follow the repository's rules for skills |

Extend an existing page or section before adding one, link to the home from elsewhere, and delete a superseded copy in the same change. When no existing home fits, propose creating one. When the repository shows no habit for a choice that is hard to reverse, such as a new file's name or place, survey it with the pq-ask-top-repos skill when it is installed, and otherwise ask the user. When the change states or contradicts a recorded decision, read the decision log first, and ask the user before contradicting an accepted one.

Read the target's reference before writing:

- AGENTS.md or CLAUDE.md: [references/agents-md.md](references/agents-md.md)
- README: [references/readme.md](references/readme.md)
- CONTRIBUTING: [references/contributing.md](references/contributing.md)
- Coding standards: [references/coding-standards.md](references/coding-standards.md)
- Decision records: [references/decisions.md](references/decisions.md)

Done when the fact sits in exactly one home, other docs link to it, no superseded copy remains, and the target's reference is read.

## 3. Propose or write

Propose these before writing them, with the exact text and its evidence, and write once the user accepts:

- a new or changed rule in an AGENTS.md, CONTRIBUTING, or the coding standards;
- a new decision record;
- a new doc file.

Write directly a fix that keeps an existing statement true, and README content that describes code changed in the same task.

Done when every proposed change is accepted or dropped, and every accepted or direct change is written.

## 4. Word it

**Agent docs** (AGENTS.md files): when a skill for writing agent-facing documents is installed, such as writing-for-agents, draft with it; otherwise:

- A pointer says what its target holds and when to read it.
- A procedure ends each step on a check the agent can verify.

**Every doc:**

- Use one term per concept.
- State what to do, then why, in one sentence where possible; state the target behavior, and keep "only" and "never" for guardrails.
- Shape by content: numbered steps when order matters, a table for routing, short lines for traps.
- Name durable things: concepts, files, symbols; line numbers, pull request numbers, and people's names go stale.
- Write every repository path as a relative link; keep an exact symbol or command only when the reader needs it to act, and confirm it exists first.
- Cut a line that no longer bears on the doc's job.

**Human docs** (README, CONTRIBUTING): write in plain language, leading with what the reader came for, and run every copyable command before writing it.

Done when every path is a link and every named symbol or command exists in the current tree.

## 5. Keep it true

1. Update docs in the same change as the code, configuration, or policy that made a statement false; when nothing became false and nothing new earns a line, change no doc.
2. Fix or delete a false statement; a caveat stacked on it keeps the falsehood.
3. On a rename, search the docs for the old name and fix every reference.

Done when every doc statement about what the change touched matches the current tree.
