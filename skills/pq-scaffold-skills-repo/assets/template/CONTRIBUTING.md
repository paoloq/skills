# Contributing

How a change reaches `main` and becomes a release. Setup lives in the [README](README.md), skill-authoring rules in [AGENTS.md](AGENTS.md), and the reasons behind the setup in [docs/decisions/](docs/decisions/).

This collection takes no outside pull requests.

## Make a change

1. Branch from `main`.
2. Commit with [Conventional Commits](https://www.conventionalcommits.org) messages; the hk `commit-msg` hook rejects any other message, and the pre-commit hook runs `mise run check`.
3. Pick the type by what users receive, because release-please cuts a release only for `feat`, `fix`, `perf`, and `revert` ([config](release-please-config.json)):
   - `feat`: a new skill, or a new capability in one; bumps the minor version.
   - `fix`: a skill that behaved wrongly now behaves as intended; bumps the patch version.
   - `feat!`, or a `BREAKING CHANGE:` footer on a `feat`: a renamed or removed skill; bumps the minor version while the version is `0.x`.
   - `docs`, `chore`, `ci`, `refactor`, `test`: no release. A change to a skill's `SKILL.md` that users should get is a `feat` or `fix`, never `docs`.
4. Push and open a pull request to `main`, titled as a Conventional Commits message, with a body written from [the pull request template](.github/pull_request_template.md). `gh pr create --body` skips the template, so read it first. [CI](.github/workflows/ci.yml) runs `mise run check` and checks the title.
5. Squash-merge once CI passes, with the pull request title as the commit message. Only that squash commit reaches `main`, so it is the one release-please reads.

## Release

1. Each push to `main` that holds a releasable commit makes [release-please](.github/workflows/release-please.yml) open or update a release pull request. It bumps `version` in both plugin manifests and adds the entries to `CHANGELOG.md`; leave those edits to it.
2. Squash-merge the release pull request when you want to ship. release-please then tags `vX.Y.Z` and publishes the GitHub release.
3. Installed plugins update only when the version changes, so changes merged since the last release reach Claude Code and Codex users only through the next release.

## Security

Report a vulnerability privately through [GitHub's private reporting](https://github.com/__OWNER__/__REPO__/security/advisories/new), never in an issue or pull request.
