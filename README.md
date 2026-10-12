# pq skills

Paolo Arduin's agent skills. They ship as the plugin `pq` for Claude Code and Codex, and as plain skills for every agent [`npx skills`](https://github.com/vercel-labs/skills) supports.

## Install

Pick one route per agent; installing through both gives you every skill twice.

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

## Development

The repository uses [mise](https://mise.jdx.dev) for its tools and checks:

```sh
mise install
mise exec -- hk install
mise run check
```

[AGENTS.md](AGENTS.md) holds the authoring rules, and [docs/decisions/](docs/decisions/) records why the repository is set up this way.
