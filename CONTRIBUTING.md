# Contributing

How to set up the repository, and how a change reaches `main` and, from there, users. Skill-authoring rules live in [AGENTS.md](AGENTS.md), and the reasons behind the setup in [docs/decisions/](docs/decisions/).

This collection takes no outside pull requests.

## Set up

The repository uses [mise](https://mise.jdx.dev) for its tools and checks:

```sh
mise install
mise exec -- hk install
mise run check
```

## Make a change

1. Branch from `main`, naming the branch `<type>/<topic>` after the change's Conventional Commits type, such as `fix/readme-style-by-audience`; `main` takes changes only through pull requests. A skill is the product, so a change under `skills/` takes the type of its effect, such as `feat`, `fix`, `refactor`, or `perf`; `docs` covers only the repository's own docs, such as `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, and the decision records.
2. Commit with [Conventional Commits](https://www.conventionalcommits.org) messages; the hk `commit-msg` hook rejects any other message, and the pre-commit hook runs `mise run check`.
3. Push and open a pull request to `main`, titled as a Conventional Commits message, with a body written from [the pull request template](.github/pull_request_template.md). `gh pr create --body` skips the template, so read it first. [CI](.github/workflows/ci.yml) runs `mise run check`.
4. Squash-merge once CI passes, with the pull request title as the commit message.

The plugins carry no version, so a merge reaches users the next time they update ([why](docs/decisions/0005-no-versions.md)).

## Security

Report a vulnerability privately through [GitHub's private reporting](https://github.com/paoloq/skills/security/advisories/new), never in an issue or pull request.
