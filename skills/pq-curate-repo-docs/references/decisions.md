# Decision records

A decision record says why a lasting choice was made, so a later reader can tell a deliberate choice from an accident.

## When to write one

1. Record a decision that is architecturally significant: hard to reverse, shaping how the system is built or depended on, and chosen over real alternatives. An everyday change needs no record.
2. Give each decision its own record.

## The log

3. Keep records in the repository's decision folder; when none exists, propose `docs/decisions/` with a copy of [the bundled MADR template](../assets/adr-template.md) in it as `adr-template.md`.
4. Match the existing log's format, template, and vocabulary; start a new log with MADR.
5. Name each record `NNNN-slug.md` with the next free number on the default branch, counting records in `archive/` folders, and check that number again just before merge, since parallel pull requests can take the same one. A number is never reused.
6. Let the numbered file names serve as the index rather than a hand-kept list of records; a README in the folder may explain when and how to write one.

## Each record

7. Fill the template as briefly as completeness allows: the title states the decision, the context ends in the question it answers, the considered options list every option weighed, and the outcome names the chosen option and why.
8. Set the status to one of `proposed`, `accepted`, `rejected`, `deprecated`, or `superseded by ADR-NNNN`, and date the record `YYYY-MM-DD` with the day the decision was made.
9. When a decision backs a coding-standards rule, keep the reasoning in the record and link it from the rule.

## Reversing a decision

10. Reverse a decision with a new record: set the old record's status to `superseded by ADR-NNNN` with a link to the new one, keep the old record, and link back to it from the new one. Fix wording in place.

## Archiving a record

11. Once a record's status is `deprecated` or `superseded by ADR-NNNN`, propose moving it into an `archive/` folder inside the folder that holds it: `docs/decisions/archive/` for a record at the top of the log, `docs/decisions/backend/archive/` for one in `docs/decisions/backend/`. Keep its file name and update every link to it inside the repository in the same change. When proposing the move, tell the user that links from pull requests, issues, and other repositories will keep the old path and break, since no change can reach them.
