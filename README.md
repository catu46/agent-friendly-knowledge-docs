# agent-friendly-knowledge-docs

**Turn a folder of documents into something an AI can navigate — and that keeps itself organized.**

For the **knowledge worker**, not the engineer. If your work lives in slide decks, spreadsheets, PDFs,
proposals, and notes — plus the odd useful SQL query or script — filed by topic on your computer, Google Drive,
or SharePoint, this skill makes that folder tree *agent-navigable*: any AI assistant can walk in, read the
files, and actually help, and the documentation **keeps itself current** as you add and change files.

It's deliberately **simple**, and it's for folders that **aren't extremely complex or dense**. One readable
index per folder. No knowledge-graphs, no versioned concept bundles, no "which mode do you want?" question. A
handful of SQL queries or scripts sitting alongside your decks is perfectly fine here — the line is
*density*, not file type. Only a **large, dense, interdependent system** whose files run and depend on each
other belongs to the heavier sibling skill
[`agent-friendly-docs`](https://github.com/catu46/agent-friendly-docs) — this one is for the filing cabinet,
not the machine room.

## When to use it

✅ **Reach for it when:**
- You have **folders of documents** — decks, spreadsheets, PDFs, proposals, notes — filed by topic, and you
  want an AI to navigate them and answer questions about them.
- Those folders live on **Drive / SharePoint and are shared with a team** — several non-technical people edit
  them outside any IDE. (This is the sweet spot: the notes live *in* each folder, so they travel with the files,
  respect per-folder permissions, and don't fight over one central file.)
- You want the docs to **stay current on their own** as people add and change files — without you maintaining a
  wiki by hand.

🚫 **Don't use it when:**
- The folder is a **dense codebase or an interdependent system that RUNS** (code, SQL, versioned pipelines) →
  use the heavier sibling [`agent-friendly-docs`](https://github.com/catu46/agent-friendly-docs) instead.
- It's a **single throwaway file** — there's no tree to organize.

## How to use it — start to finish

1. **Install once.** Either symlink the skill (see *Install* below), or hand someone the one-click
   **"Organize a folder with AI"** app — it self-installs the skill on first run. (One-time: the person also
   needs Claude Code or Codex installed + logged in.)
2. **Point it at a folder.** In the chat just say *"organize this folder for AI"* (or double-click the app and
   pick the folder). It **interviews you** (what's the goal, what to skip, which version is canonical), reads
   the files, builds a readable `index.md` + `log.md` + router in each folder, and drops the **"Talk to my
   files"** launcher — then proves it works with a fresh-eyes test.
3. **Use it day to day.** Double-click **"Talk to my files"** inside the folder → the chat opens right there.
   Ask *"summarize the Acme proposal"*, *"which is the latest model?"*, *"draft a reply about X"*.
4. **Let it stay current.** Next time you (or a teammate) opens it, ask *"what changed while I was away?"* — it
   catches up on edits made by **anyone**, outside the chat (a new deck, an Excel re-saved, a Drive rename),
   tells you in plain words, and updates the notes on your OK.
5. **Grow it without thinking.** Create new folders / files as usual; keep working through the chat and it
   scaffolds and updates the docs for you (it asks when it's unsure what a new folder is).

## What you get

1. **Organized docs in every folder** — a thin router (`AGENTS.md`), a one-line bridge (`CLAUDE.md`), a
   readable `index.md` (what's here, where the real files live, the definitions), and an append-only `log.md`
   (what changed and why). Small, human-readable, and structured so an AI loads only what it needs.
2. **A one-click launcher — "Talk to my files"** — dropped in the top folder. Double-click it, pick your
   assistant (Claude Code or Codex), and you're talking to your files. No VS Code, no terminal commands. Just
   ask *"summarize the proposal for client X"* or *"which is the latest version of the model?"*
3. **Docs that catch up when you open them** — you come back after two weeks, open the chat, and ask *"what
   changed while I was away?"* A small saved snapshot of each folder lets the assistant see everything that
   changed *outside* the chat (a new deck, an Excel re-saved with new numbers, a rename in Drive), tell you in
   plain words, and update `index.md` / `log.md` append-only on your OK. **No background job, no cron** — it
   runs when you're there. (A fully-unattended scheduled watcher exists as an optional v2 for always-on
   machines.)

## Hand it to a colleague — the "Organize a folder with AI" app

At the repo root are two self-contained apps — **`Organize a folder with AI.command`** (macOS) and
**`Organize a folder with AI.bat`** (Windows) — plus a plain-language **[`READ ME - How to use.txt`](READ%20ME%20-%20How%20to%20use.txt)**.
Send someone **just that one file** (Teams, email, Drive). On first run it **installs the skill itself** — using
the copy next to it if they cloned the whole repo, otherwise **downloading it from GitHub** — then opens a folder
picker, lets them pick Claude Code or Codex, and applies the skill to the folder they chose. No terminal
commands, ever.

- **First open:** a one-time OS safety prompt (macOS: right-click → **Open**; Windows: **More info → Run anyway**).
- They still need **Claude Code or Codex installed + logged in once** (the app opens the install link if it's missing).

## Install (for yourself, as a Claude Code skill)

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

## Keeping it current

Nothing to schedule. The assistant catches up whenever you open the folder and ask *"what changed?"* — it
compares a small saved snapshot (`.okf-state.json`) against the real files and shows you added / modified /
renamed / deleted, then updates the docs on your OK. Under the hood:

```bash
python3 scripts/snapshot.py diff  ~/path/to/your/folder   # what changed since last time
python3 scripts/snapshot.py write ~/path/to/your/folder   # save the new baseline
```

Want fully-unattended updates on an always-on machine (a server)? That's the optional v2 scheduled watcher —
with honest caveats (a sleeping laptop never runs it): [WATCHER.md](WATCHER.md).

## How it's built

- **[SKILL.md](SKILL.md)** — the skill itself (the instructions the agent follows).
- **[shape-basic.md](shape-basic.md)** — the exact files and copy-paste blocks for each folder.
- **[LAUNCHER.md](LAUNCHER.md)** — the one-click launcher spec.
- **[scripts/snapshot.py](scripts/snapshot.py)** — the change-memory (write/diff) that powers "what changed?".
- **[scripts/validate.py](scripts/validate.py)** — checks the doc shape (Python 3, stdlib only).
- **[WATCHER.md](WATCHER.md)** + **[scripts/arm-watcher.sh](scripts/arm-watcher.sh)** — the optional v2
  scheduled watcher (+ `artifact-diff.py`, its materiality gate).

## Honest limits

- The launcher is a **friendly terminal chat**, not a polished web app — calm and non-scary, but a terminal
  underneath.
- Catch-up runs **when you open the folder**, not while you're away — which is fine, since the docs matter when
  you come back to work. (The v2 scheduled watcher trades this for real cron/auth caveats.)
- A cloud **"Files On-Demand"** placeholder with no local bytes can't be hashed — keep files "always on this
  device" for reliable change-detection.
- **Attribution depends on the source** — git gives a real author; a plain folder often gives only an OS
  account. The docs never fabricate a name.

## License

MIT — see [LICENSE](LICENSE).
