# __PLUGIN__ skills

__DESCRIPTION__ They ship as the plugin `__PLUGIN__` for Claude Code and Codex, and as plain skills for every agent [`npx skills`](https://github.com/vercel-labs/skills) supports.

## Install

Pick one route per agent; installing through both gives you every skill twice.

Claude Code:

```text
/plugin marketplace add __OWNER__/__REPO__
/plugin install __PLUGIN__@__PLUGIN__
```

Codex:

```sh
codex plugin marketplace add __OWNER__/__REPO__
codex plugin add __PLUGIN__@__PLUGIN__
```

Any other agent:

```sh
npx skills add __OWNER__/__REPO__
```

`npx skills add __OWNER__/__REPO__ --list` lists the skills without installing them.

## Development

The repository uses [mise](https://mise.jdx.dev) for its tools and checks:

```sh
mise install
mise exec -- hk install
mise run check
```

[CONTRIBUTING.md](CONTRIBUTING.md) covers making a change and releasing it, [AGENTS.md](AGENTS.md) holds the authoring rules, and [docs/decisions/](docs/decisions/) records why the repository is set up this way.
