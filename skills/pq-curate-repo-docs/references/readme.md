# READMEs

A README is the project's front door: what the project is, how to start using it, and where to go next.

## Root README

1. Open with the project's name and one line on what it is and who it is for.
2. Give install and a first run as copyable commands in fenced blocks; when a docs site owns installation, give one prominent link there instead.
3. Link the docs site or docs folder for everything deeper, such as API reference, configuration, guides, and architecture.
4. Link the contributing guide, and say where to get help.
5. State the license.

## Style

Every root README should scan at a glance.

6. Show the project's live status, such as CI, build, or deploy, in one row of badges under the title.
7. Put the single notice that matters most in a callout such as `> [!NOTE]` or `> [!TIP]`.
8. Keep images in the repository, link them relatively, and give each one alt text.

### Projects that seek outside users

When the README must win users outside the team, such as for an open-source library or tool, its readers are deciding whether to adopt the project, so make it look inviting:

9. Open with a logo or banner above the badge row, with light and dark variants when one would vanish on the other background.
10. Add badges for version, license, downloads, or chat to that row.
11. Show the product when it is visual or claims speed: a screenshot, a short animation, or a benchmark chart.
12. Near the top, list the highlights or the reasons to use it in a few short bullets.

## Package and component READMEs

13. Give each package published to a package registry, such as PyPI, npm, or crates.io, a README on one template shared across the repository: its name, a one-line purpose, install, a docs link, and where to get help.
14. Give an internal component, such as an unpublished workspace member or a service shipped only as a container image, a short README when a developer opening its folder needs orientation the code does not give: open by saying it is internal, then give its purpose, entry points, and how to run and test it. Its agent rules belong in its nested AGENTS.md.
