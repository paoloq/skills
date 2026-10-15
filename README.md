# pq skills

[![CI](https://github.com/paoloq/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/paoloq/skills/actions/workflows/ci.yml) [![License](https://img.shields.io/github/license/paoloq/skills)](LICENSE)

Agent skills, shipped as the plugin `pq` for Claude Code and Codex, and as plain skills for every agent [`npx skills`](https://github.com/vercel-labs/skills) supports.

## Skills

| Skill | What it does |
|---|---|
| [pq-ask-top-repos](skills/pq-ask-top-repos/SKILL.md) | Finds how top open-source projects handle a convention, with evidence. |
| [pq-curate-repo-docs](skills/pq-curate-repo-docs/SKILL.md) | Decides whether a fact belongs in your repository's docs, where, and how to word it. |
| [pq-scaffold-skills-repo](skills/pq-scaffold-skills-repo/SKILL.md) | Turns an empty repository into a skills collection like this one. |

## Install

> [!WARNING]
> Pick one route per agent; installing through both gives you every skill twice.

Claude Code:

```text
/plugin marketplace add paoloq/skills
/plugin install pq@pq
```

Codex:

```sh
codex plugin marketplace add paoloq/skills
codex plugin add pq@pq
```

Any other agent:

```sh
npx skills add paoloq/skills
```

`npx skills add paoloq/skills --list` lists the skills without installing them.

## Update

The plugin has no versions, so every merge to `main` is an update, and it reaches you when you update.

Claude Code updates only marketplaces with auto-update on, which is off by default for this one. Turn on **Enable auto-update** for `pq` under `/plugin` → **Marketplaces**, or update by hand:

```sh
claude plugin marketplace update pq
claude plugin update pq@pq
```

Codex:

```sh
codex plugin marketplace upgrade pq
```

Any other agent:

```sh
npx skills update
```

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) covers setup and making a change, [AGENTS.md](AGENTS.md) holds the authoring rules, and [docs/decisions/](docs/decisions/) records why the repository is set up this way.

## Help

Report a problem or ask a question in [GitHub issues](https://github.com/paoloq/skills/issues).

## License

Released under the [MIT License](LICENSE).
