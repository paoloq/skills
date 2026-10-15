# Coding standards

The coding standards hold the judgment calls a reviewer applies that no tool checks: the project's own rules, each with the reason it exists.

## What belongs

1. Keep only rules specific to this project: invariants, contracts, concurrency, error handling, compatibility, and testing rules whose violation looks fine locally but costs later.

## The file

2. Open with a scope line: what the file covers, which tools own mechanical style, and the linked language style guide for generic idioms, saying which wins on conflict.
3. State the fallback: where the file is silent, follow the conventions already in the surrounding code; the rules apply to new and changed code.
4. Define the keywords once, after the scope line, per RFC 2119 and RFC 8174: **MUST** blocks the merge, **SHOULD** needs a stated reason to deviate, and **MAY** marks an accepted option. The keywords carry this meaning only in capitals.
5. Group rules by concern under a capitalized `##` heading with a one-word name, such as `## Async`, `## Errors`, `## Data`, or `## Tests`.
6. Keep one file, linked from CONTRIBUTING and AGENTS.md; give a subtree with rules of its own a nested standards file that adds to the root one.

## Each rule

7. Give each rule a `###` heading that is its ID, so the ID is also a link anchor.
8. Write the ID in lowercase kebab-case: the group's name, then one to three words for what the rule governs, not how it is worded, such as `async-blocking-io`. Rewording keeps the ID, and a retired ID is never reused; when the repository already uses another identifier form, keep that form.
9. Under the heading, state the rule as a full sentence with its keyword in capitals, then its reason, meaning what breaks and for whom when the rule is ignored: "Code **MUST** keep blocking I/O off the event loop. One blocking call stalls every request the loop is serving."
10. Use **MUST** only where a violation causes real harm, such as a broken contract, leaked data, or corrupted state; **SHOULD** is the default.
11. Add a compliant and a noncompliant example when the boundary of the rule is not obvious from the rule itself.

## Keeping it current

12. When review repeats the same comment, turn it into a tool rule if a tool can check it, and into a standards rule otherwise.
