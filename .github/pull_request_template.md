<!-- This body becomes the squash commit message on main. Draft it only for a change an agent worked on; otherwise stop and tell the user this template requires one. Replace comments with your text until none remains, and delete each section or subsection that does not apply, except Agent. -->

## Why

<!-- The problem or constraint, and why this approach won over the alternatives you weighed. -->

### Root cause

<!-- For a bug: the mechanism that produced it, and whether the fix removes it or works around it. -->

## What changed

<!-- Only what a reviewer cannot get from the diff: behavior, design choices, risk. -->

## Non-goals

<!-- What a reviewer could expect this change to do that it deliberately leaves out, each with its reason or follow-up. -->

## Verification

<!-- Each command you ran (`mise run check` at least) and its observed result; for a skill change, each install or session you tried in Claude Code or Codex; what you could not verify, and why. A failed or skipped check stays listed. -->

## Agent

<!-- One block per distinct role, harness, and model among the agents that worked on this pull request, such as a coordinator and its workers, with an empty line between blocks. Fill each block from that agent's own record of what ran: its context, or for a worker its session log. -->

**Role:** <!-- What the agent did, e.g. Coordinator -->
**Harness:** <!-- Name and version, e.g. Claude Code 2.1.296 -->
**Model:** <!-- Exact model ID, e.g. claude-opus-5-5 -->

**Role:** <!-- e.g. Implementation -->
**Harness:** <!-- e.g. Codex CLI 0.162.1 -->
**Model:** <!-- e.g. claude-sonnet-5-5 -->
