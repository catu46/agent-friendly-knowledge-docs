# agent-friendly-knowledge-docs

**Turn a folder of documents into something an AI can navigate — and that keeps itself organized.**

For the **knowledge worker**, not the engineer. If your work lives in slide decks, spreadsheets, PDFs,
proposals, and notes — filed by topic on your computer, Google Drive, or SharePoint — this skill makes that
folder tree *agent-navigable*: any AI assistant can walk in, read the files, and actually help, and the
documentation **keeps itself current** as you add and change files.

It's deliberately **simple**. One readable index per folder. No knowledge-graphs, no versioned concept
bundles, no "which mode do you want?" question. If your folder is full of **code, SQL, or operational models
that run and depend on each other**, use the heavier sibling skill
[`agent-friendly-docs`](https://github.com/catu46/agent-friendly-docs) instead — this one is for the filing
cabinet, not the machine.

## What you get

1. **Organized docs in every folder** — a thin router (`AGENTS.md`), a one-line bridge (`CLAUDE.md`), a
   readable `index.md` (what's here, where the real files live, the definitions), and an append-only `log.md`
   (what changed and why). Small, human-readable, and structured so an AI loads only what it needs.
2. **A one-click launcher — "Talk to my files"** — dropped in the top folder. Double-click it, pick your
   assistant (Claude Code or Codex), and you're talking to your files. No VS Code, no terminal commands. Just
   ask *"summarize the proposal for client X"* or *"which is the latest version of the model?"*
3. **A watcher that keeps it current** — a scheduled agent that notices when files change *outside* the
   assistant (a new deck, an Excel saved as `v8`, a rename in Drive) and updates the docs, append-only, on its
   own.

## Install

This is a Claude Code skill. Clone it and symlink it into your skills folder:

```bash
git clone https://github.com/catu46/agent-friendly-knowledge-docs.git
ln -s "$(pwd)/agent-friendly-knowledge-docs" ~/.claude/skills/agent-friendly-knowledge-docs
```

Then, in Claude Code, just ask in your own words — *"organize my folders for AI"*, *"make this folder
agent-friendly"*, *"make my documents AI-navigable"* — and the skill takes over: it interviews you, reads the
files, proposes a structure, builds it, proves it works with a fresh-eyes test, drops the launcher, and offers
to arm the watcher.

## The one-click launcher

Two ready-made launchers ship in [`assets/`](assets/):

- **Windows** — `Talk to my files.bat` (double-click in File Explorer)
- **macOS** — `Talk to my files.command` (double-click in Finder)

The skill copies the right one into your top folder. On launch it lets you pick Claude Code or Codex (whichever
you have installed). The first time you open it, your OS shows a one-time safety prompt (Windows SmartScreen →
*More info → Run anyway*; macOS Gatekeeper → *right-click → Open*) — that's normal for any unsigned helper.
Full details: [LAUNCHER.md](LAUNCHER.md).

> You still need an assistant **installed and logged in once** — Claude Code
> (https://claude.com/claude-code) or Codex (https://developers.openai.com/codex). The launcher removes the
> daily friction of opening an IDE and typing a command, not the one-time setup.

## The watcher

After setup, arm the reconciliation watcher so the docs self-maintain:

```bash
scripts/arm-watcher.sh ~/path/to/your/folder            # dry run — prints the schedule, installs nothing
scripts/arm-watcher.sh ~/path/to/your/folder --install  # once you're happy, schedule it
```

It works over a plain folder, a git checkout, or a synced Drive/SharePoint folder. Full spec:
[WATCHER.md](WATCHER.md).

## How it's built

- **[SKILL.md](SKILL.md)** — the skill itself (the instructions the agent follows).
- **[shape-basic.md](shape-basic.md)** — the exact files and copy-paste blocks for each folder.
- **[LAUNCHER.md](LAUNCHER.md)** — the one-click launcher spec.
- **[WATCHER.md](WATCHER.md)** — the self-maintenance watcher.
- **[scripts/validate.py](scripts/validate.py)** — checks the doc shape (Python 3, stdlib only).
- **[scripts/artifact-diff.py](scripts/artifact-diff.py)** — the materiality gate (structural diff of
  decks/sheets/PDFs so cosmetic edits don't churn the docs).

## Honest limits

- The launcher is a **friendly terminal chat**, not a polished web app — calm and non-scary, but a terminal
  underneath.
- The watcher is **scheduled, not real-time** — the safety net for edits made outside the assistant.
- **Attribution depends on the source** — git gives a real author; a plain folder often gives only an OS
  account. The docs never fabricate a name.

## License

MIT — see [LICENSE](LICENSE).
