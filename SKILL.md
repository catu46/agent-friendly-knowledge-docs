---
name: agent-friendly-knowledge-docs
description: Make a folder tree of DOCUMENTS agent-navigable and self-maintaining — decks, spreadsheets, PDFs, proposals, notes filed by topic on a computer, Drive, or SharePoint. For non-engineers (consultants, managers, analysts) who edit files outside any IDE. Scaffolds a thin AGENTS.md router + CLAUDE.md stub + a readable index.md + append-only log.md per folder, drops a one-click "talk to my files" launcher in the top folder, proves it with a fresh-eyes test, and arms a watcher that keeps the docs current when files change outside Claude Code (new deck, Excel saved as v8, a Drive/SharePoint rename). Deliberately simple — one index per folder, no knowledge-graph, no versioned concept bundles, no mode question; folders of CODE/SQL/operational models that RUN belong to the sibling skill agent-friendly-docs. Triggers: "organize my documents/folders for AI", "make my folders agent-friendly", "index.md per folder", "mother CLAUDE.md", "talk to my files launcher", "reconciliation watcher for docs", "AGENTS.md for documents", "Drive/SharePoint docs for AI".
---

# Agent-Friendly Knowledge Docs

**For a folder tree of DOCUMENTS you read for the knowledge inside** — decks, spreadsheets, PDFs,
proposals, one-pagers, notes filed by topic on a computer, Drive, or SharePoint. The audience is the
**non-engineer**: strategy consultants, managers, analysts, directors who change files **outside** any
IDE, git, or Claude Code. So the docs **route by reference** instead of dumping everything into context,
and stay **deliberately simple**.

**Three deliverables, one skill:**

1. **Set up the house** — scaffold documentation any AI agent can navigate for the folder tree, then
   **prove it works** with a cold fresh-eyes test before you rely on it.
2. **Hang the front door** — drop a **one-click launcher** in the mother folder so a non-technical person
   double-clicks and just *talks to the folder* (no VS Code, no typing commands). See
   **[LAUNCHER.md](LAUNCHER.md)**.
3. **Keep the house tidying itself** — arm a watcher **and** embed a self-update protocol so the docs stay
   current **as the project grows**, even when people edit files **outside** Claude Code.

North-star loop: walk into a folder, ask a question, the agent **reads the files**, helps — and the docs
**feed themselves back**, so tomorrow a fresh chat is instantly smart again.

**This skill is `basic` by design — no tiers, no question.** One readable `index.md` per folder + an
append-only `log.md`. **No** `knowledge/` bundle, **no** concept files, **no** `status`/`supersede`
frontmatter, **no** knowledge-graph — that machinery is the heavier sibling skill **`agent-friendly-docs`**,
for folders of CODE / SQL / operational models that **RUN** and depend on each other. When to reach for it:
see [When a folder outgrows this skill](#when-a-folder-outgrows-this-skill).

**Language — English by default, everywhere authored.** Skill instructions, the launcher banner, and the docs
you generate (`index.md`, `log.md`, `AGENTS.md`) are all **English** — one consistent language, never mixed.
The only place language adapts is the **live conversation**: reply in whatever language the user writes to you
in (that's the `## How to talk to the user` tone block). So a Portuguese-speaking consultant still gets
Portuguese answers, while every file on disk stays English.

---

## The shape (per meaningful folder) — FLAT, not a bundle

Every meaningful folder gets the same five files. Full copy-paste blocks: **[shape-basic.md](shape-basic.md)**.

```
folder/
├── CLAUDE.md        # one line: @AGENTS.md  (the auto-load bridge)
├── AGENTS.md        # THIN router: Rules + "detail → ./index.md" + up-pointer + Keep-current
├── index.md         # the folder's knowledge (current state), inline — a human can read it
├── log.md           # APPEND-ONLY history: what changed & why (Drive/SharePoint has no git)
└── .okf-state.json  # (hidden) the watcher's snapshot
```

- **`CLAUDE.md`** = one-line stub `@AGENTS.md`. Claude Code auto-loads `CLAUDE.md` (walking cwd up the
  tree), **not `AGENTS.md`** — the stub is the only auto-load bridge. The `@import` is **eager**, so the
  stub must point ONLY at the thin router, **never** at the whole `index.md`, or you re-bloat context.
- **`AGENTS.md`** = the THIN front door, a **ROUTER, not a content store**. Holds ONLY: (a) **Rules** — how
  to act, scope, what NOT to touch; (b) a lazy **DOWN pointer** to `./index.md`; (c) an **UP pointer**
  `## If you opened only this folder → ../AGENTS.md`; (d) the **Keep this current** protocol. No definitions.
- **`index.md`** = the folder's **knowledge**, inline — what's here, where the real artifacts live,
  definitions, caveats. One readable file a non-technical person can actually read and trust.
- **`log.md`** = **memory** — every real change appends one dated line (what + why + who). Append-only, so
  "what we used to do" is never overwritten.

**Split by LOAD-TIMING, not category.** Always-needed + small (rules, pointers) → `AGENTS.md`, eager.
Sometimes-needed + large (the knowledge, the history) → `index.md` / `log.md`, opened on demand. The payoff:
a per-folder mega-`CLAUDE.md` (loaded every chat = token bloat) becomes a ~15-line router that loads almost
nothing eagerly.

**Opened-in-isolation reality.** Claude Code walks UP the `CLAUDE.md` chain, so opening a subfolder still
loads its ancestors' routers. But other tools (Copilot/Cursor) often scope to the opened root and never read
upward — that's why every `AGENTS.md` carries `## If you opened only this folder → ../AGENTS.md`.

---

## Survey and adapt — no named modes

Whatever you find — nothing, thin docs, or folders full of files behind a bloated mega-`CLAUDE.md` — gets the
**same** target shape; only the ratio of create-vs-reorganize shifts, and that's self-evident from what you read.

The one non-obvious rule: **DECOMPOSE, DON'T COPY.** When existing docs are bloated, route each chunk to its
layer instead of dumping the wall into `AGENTS.md`:

- a **RULE / scope / what-not-to-touch** → the thin `AGENTS.md` router;
- a **DEFINITION / reference** → an `index.md` section;
- an **OLD / replaced** thing → note it under `## Decisions` + a `log.md` line (keep it);
- a **STALE** claim → ask "still true?" and archive.

**Preserve everything;** keep the ORIGINAL file as a backup (and in git/Drive version history) until the user
validates the new tree.

---

## Memory and history — keep current AND keep history

The self-update protocol is **APPEND-ONLY, never destructive.** Distinguish current-state from memory:

- **`index.md`** holds current state. On **v7 → v8**: repoint the `## What's here` entry at the new file,
  note the WHY under `## Decisions`, archive the old artifact (or rely on source version history).
- **`log.md`** holds the story. **Append** one dated line; never overwrite a `log.md` line.

Either way an agent can recover **what you used to do, and why**: git/Drive version the *bytes*; this layer
adds the readable *story*.

---

## Works for any document — read content by default

You *can* open these files, so **read the content by default, not just filenames.** The interview decides what
to **skip**, not what to open.

- **PDF** — the Read tool reads PDFs natively via a `pages` range (max 20/request; a range is required above
  10 pages).
- **Modern `.pptx` / `.xlsx` / `.docx`** are ZIP+XML: `python-pptx` / `openpyxl` / `python-docx` (pip if
  missing), or zero-install `unzip -p file.xlsx xl/sharedStrings.xml` etc. and strip tags.
- **Legacy `.doc` / `.ppt` / `.xls`** are binary: `textutil -convert txt old.doc` (.doc, macOS), else
  `soffice --headless --convert-to txt|csv`.
- **Big spreadsheets** — never dump every cell: used range + headers + dtypes + ~20 sample rows
  (`openpyxl` `read_only=True`).

---

## The discovery loop (interview ⇄ read — co-equal, alternating)

Understanding a real, messy tree is **iterative, not linear phases.** Interview and reading are **co-equal**:
reading reveals WHAT IS; the human reveals WHAT MATTERS and WHAT'S STILL TRUE.

1. **Interview** (in the user's language): goals, what to **SKIP** (required exclusion step), what's stale.
2. **Read**: survey the tree, then read the **content** the answers point to — by default.
3. **Re-interview**, sharper and evidence-based: *"you said the Q3 model is canonical, but there's v8,
   v8_FINAL, v8_FINAL_real — which? this note claims X but the deck shows Y — stale?"*
4. **Read deeper → converge.** Usually 2–3 rounds. Stop when reading stops surprising and the human confirms.
5. **PROPOSE → BUILD.** Propose the tree, confirm, then build: for each meaningful folder write `AGENTS.md`
   + the `CLAUDE.md` stub + `index.md` + `log.md`, wire the cross-links, embed the self-update protocol,
   write `.okf-state.json`. **Open [shape-basic.md](shape-basic.md)** for the exact blocks.
   **Done when** every meaningful folder has all five files and `validate.py` passes.
6. **Hang the front door — drop the launcher.** In the **mother (root) folder**, drop the one-click launcher
   so the user can start talking to the tree without a terminal. Details and the exact files:
   **[LAUNCHER.md](LAUNCHER.md).** Confirm before adding it. **Done when** the launcher sits in the root,
   is executable/de-quarantined, its English banner is intact, and the root `AGENTS.md` carries the
   `## How to talk to the user` tone block.
7. **Verify with fresh eyes — the acceptance test before self-maintenance takes over.** Deploy a subagent
   carrying **none** of this conversation's context, rooted at the built tree, as a brand-new agent who just
   opened the folder. Using ONLY the docs, have it: (a) state what the folder is and how it'd do a
   representative task; (b) flag anything it could **not** determine. Whatever it stumbles on is a **real gap**
   → fix the docs and re-verify. `validate.py` checks the **shape**; this checks **comprehension** — ship only
   when both pass.
8. **Arm the watcher — the handoff to self-maintenance.** Once the tree passes shape + comprehension, arm the
   daily reconciliation so the docs self-feed from day one: `scripts/arm-watcher.sh <tree> --install`
   (runner-agnostic; pick the backend for the source — git / Drive / SharePoint / plain folder). **Confirm
   before installing a scheduled job** (see [WATCHER.md](WATCHER.md)). **Done when** the dry-run cron line
   has been shown and, on the user's OK, installed.

**At scale (hundreds of folders), DECENTRALIZE:** one subagent per leaf folder writes that folder's docs; roll
summaries leaf → mid → root so no context ever holds the whole tree.

**Keep this current** (embedded in every `AGENTS.md`): after real changes, update this folder's `index.md` +
APPEND to `log.md` + restamp `timestamp`; and when you **CREATE a new meaningful folder, scaffold its docs
before you finish** (`CLAUDE.md` + `AGENTS.md` + `index.md` + `log.md`) — so the tree never grows a blind spot.
Change only what the edit touched.

---

## The in-app experience (what the consultant feels)

The launcher opens the plain assistant chat (Claude Code or Codex, the user's pick) inside the folder — capable,
but it can feel like a developer tool. Three levers, all set at build time, make it feel like a **friendly
assistant** instead. Set them so a non-technical person is never scared or confused:

1. **The welcome banner** (in the launcher) — a warm, plain-language English greeting with two or three example
   questions, and a one-key pick between Claude Code and Codex when both are installed. See
   [LAUNCHER.md](LAUNCHER.md).
2. **A tone block in the root `AGENTS.md`** — so the assistant **replies in the user's language, in plain
   words (no jargon), stays concise, and asks a friendly confirmation before anything destructive** (deleting,
   overwriting, sending). The copy-paste `## How to talk to the user` block is in
   [shape-basic.md](shape-basic.md); include it in the **root** `AGENTS.md`.
3. **Permission comfort** — by default Claude Code asks before editing a file, which reads as a scary popup to
   a layperson. Explain it once in plain words, and offer (never impose) a `.claude/settings.json` in the
   mother folder that pre-allows **safe, reversible** actions (reading, creating new files) while still
   pausing on **destructive** ones (deleting, overwriting the user's originals). Get consent before relaxing
   any permission; when in doubt, keep the prompt.

**Yes, it can act on the folder.** Because the launcher `cd`s into the folder and opens `claude` there, the
assistant reads, summarizes, edits, renames, creates, and organizes the files in that folder and everything
under it. That is the point — pair it with the confirmation-before-destructive rule so it stays safe.

---

## Self-maintenance: the reconciliation watcher (+ new-folder discovery)

How the docs self-feed when people edit **outside** Claude Code. Each scheduled run:

1. **Discovers new scopes.** Scan for meaningful folders that have real artifacts but no `AGENTS.md`/snapshot
   → scaffold them (same flat shape), so a folder created after setup doesn't stay a blind spot. If a new
   folder is ambiguous, **queue an ask** instead of guessing.
2. **Reconciles known scopes.** A snapshot (`.okf-state.json`, per-file `sha256`) diffs the filesystem (and/or
   `git diff`, and/or a source API's "modified by/at") to find added/modified/deleted files, classifies each by
   **reading** it (data-refresh → maybe no change; v7→v8 → repoint + archive; new file → add a line; deletion
   → mark removed), applies the update **append-only**, and rewrites the snapshot.
3. **Reports** `validate.py` PASS/FAIL.
4. **Asks when unsure** — never guesses; attributes the last editor honestly per source.

Honest limits: scheduled = **next run, not instant** (work agentically for live updates); only **meaningful**
folders are scaffolded; clear cases auto-apply, ambiguous cases ask. Full spec + the copy-paste agent prompt:
**[WATCHER.md](WATCHER.md).**

---

## When a folder outgrows this skill

`basic` is the right, simpler default. Move a specific folder to the heavier sibling skill
**`agent-friendly-docs`** (OKF concept bundle + knowledge-graph) only when it has:

- **versioned artifacts with real history** worth linkable, superseded nodes (v6→v7→v8 + the "why");
- **knowledge reused across many folders** (one canonical definition linked everywhere, not copy-pasted);
- **files that RUN and depend on each other** (code, SQL, operational models) — where the exact file, its
  structure and dependencies, is what matters.

Otherwise stay here: clarity over machinery.

---

## Honesty notes (state these plainly)

- **Auto-load is a harness feature tied to the filenames `CLAUDE.md` / `AGENTS.md`.** Claude Code reads
  `CLAUDE.md`, not `AGENTS.md`; the `@AGENTS.md` stub bridges. `index.md` does **not** auto-load — it's opened
  on demand. That lazy boundary is the whole point.
- **The launcher does not install or log in Claude Code.** First run still needs `claude` installed and
  authenticated; the launcher removes the "open an IDE, cd, type a command" friction, not the one-time setup.
- **Descriptions can drift** from the artifacts they point at — which is why every doc carries a `timestamp`
  and why the watcher exists. Plain-filesystem edits may not reveal *who* changed a file; non-git sources need
  their own "modified by"; the watcher needs read access.

---

## Validate

A bundled **[scripts/validate.py](scripts/validate.py)** (Python 3, **stdlib only**) enforces the flat shape
per folder: both `AGENTS.md` + `CLAUDE.md` present, the stub is exactly `@AGENTS.md`, required frontmatter,
links and `resource:` paths resolve, timestamps parse. Run it after building and after every watcher pass —
it's the **shape** half of acceptance; pair it with the **fresh-eyes** comprehension check (loop step 7). It
skips dotfiles and common build/dep dirs; add a `.okfignore` at the root (one glob per line) to exclude
anything else.
