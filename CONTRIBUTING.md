# Contributing

How a change reaches `main` and, from there, users. Setup lives in the [README](README.md), skill-authoring rules in [AGENTS.md](AGENTS.md), and the reasons behind the setup in [docs/decisions/](docs/decisions/).

This collection takes no outside pull requests.

## Make a change

1. Branch from `main`; `main` takes changes only through pull requests.
2. Commit with [Conventional Commits](https://www.conventionalcommits.org) messages; the hk `commit-msg` hook rejects any other message, and the pre-commit hook runs `mise run check`.
3. Push and open a pull request to `main`, titled as a Conventional Commits message, with a body written from [the pull request template](.github/pull_request_template.md). `gh pr create --body` skips the template, so read it first. [CI](.github/workflows/ci.yml) runs `mise run check`.
4. Squash-merge once CI passes, with the pull request title as the commit message.

The plugins carry no version, so a merge reaches users the next time they update ([why](docs/decisions/0005-no-versions.md)).

## Security

Report a vulnerability privately through [GitHub's private reporting](https://github.com/paoloq/skills/security/advisories/new), never in an issue or pull request.
