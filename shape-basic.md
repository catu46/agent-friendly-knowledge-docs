# Shape: the flat `index.md` + `log.md` (the only shape in this skill)

Open this reference when you build a folder. It holds the exact files and copy-paste blocks. The reasoning is
in [SKILL.md](SKILL.md); the launcher is in [LAUNCHER.md](LAUNCHER.md).

## The shape (per meaningful folder) — FLAT, not a bundle

```
folder/
├── CLAUDE.md        # one line: @AGENTS.md  (the auto-load bridge)
├── AGENTS.md        # THIN router: Rules + "detail → ./index.md" + up-pointer + Keep-current
├── index.md         # the folder's knowledge (current state), inline
├── log.md           # APPEND-ONLY history: what changed & why (Drive/SharePoint has no git)
└── .okf-state.json  # (hidden) the watcher's snapshot
```

- **`index.md` = the knowledge** — what's in this folder, where the real artifacts live, definitions, caveats.
  One readable file a non-technical person can actually read and trust.
- **`log.md` = memory** — every real change appends one dated line (what + why + who). Append-only, so "what
  we used to do" is never overwritten.

Write the generated docs — `index.md`, `log.md`, and the human-readable **Rules** in `AGENTS.md` — in the
**content/project language** (the language of the material and the user). This *reference* file, and the fixed
agent-protocol blocks below (tone, catch-up), stay English. Replace every `<placeholder>`. Timestamps are
ISO-8601 UTC. The `## If you opened only this folder` and `## Keep this current` sections are **mandatory** in
every `AGENTS.md`. Outer fences are `~~~` so nested ``` blocks render.

---

## 1. `AGENTS.md` (the thin router — every NON-root folder)

This is the template for a **subfolder**. The **root** `AGENTS.md` is the same but swaps the up-pointer and
adds two blocks — see **§1b**. (Do NOT paste this verbatim at the root: its `../AGENTS.md` link does not
resolve there and `validate.py` fails.)

~~~md
---
type: agent-guide
title: <Folder name>
description: <one line: what this folder is for>
resource: .
tags: [<tag>, <tag>]
timestamp: 2026-07-01T12:00:00Z
---

# <Folder name>

## Rules
- Scope: <what this folder is responsible for; how far to go>.
- Do NOT touch: <what's off-limits — client inputs, other folders, sent deliverables>.

## Knowledge
This folder's knowledge → [`./index.md`](./index.md). History → [`./log.md`](./log.md).

## If you opened only this folder
Global rules and the parent map → [`../AGENTS.md`](../AGENTS.md). Read it before acting if it isn't already
in context.

## Keep this current
After changing anything here, before you finish: update the relevant part of `index.md`, **append** one line
to `log.md`, restamp `timestamp`, then refresh the change-memory (`snapshot.py write .`). **Never overwrite
history** (log is append-only). Created a new meaningful subfolder? Scaffold it (CLAUDE.md + AGENTS.md +
index.md + log.md + snapshot) before finishing — no blind spots. Then walk up to `../AGENTS.md` only if the
change affects global rules or the map.
~~~

---

## 1b. The ROOT `AGENTS.md` — three differences

The root uses the §1 template with **three changes**. (1) Its up-pointer says it IS the root — no
`../AGENTS.md` link (that link would not resolve and fails `validate.py`). It also carries two root-only
blocks that set the voice and the self-maintenance for the whole tree.

**(1) Replace `## If you opened only this folder` with:**

~~~md
## This is the top of the tree
You are at the root. There is no parent — the global rules above apply to everything below. Each subfolder has
its own `AGENTS.md` with its local rules.
~~~

**(2) Add `## How to talk to the user`** (the tone block — makes the in-app chat feel like a friendly assistant
instead of a developer tool; the reason a non-technical person can use the launcher without being scared):

~~~md
## How to talk to the user
- Reply **in the language the user writes in**, in **plain words** — no jargon, no programming terms.
- Be **concise and kind**. Say what you're about to do in one sentence before doing it.
- **Confirm before anything destructive**: deleting, overwriting an original file, or sending anything out.
  For safe, reversible actions (reading, summarizing, creating a new file), go ahead.
- If something is ambiguous (which version? which client?), **ask** instead of guessing.
- Never touch anything listed under "Do NOT touch".
~~~

**(3) Add `## Catch up on changes`** (the self-maintenance protocol — how the docs stay current with edits made
outside the chat; runs when the user asks, or proactively when the snapshot looks stale on opening):

~~~md
## Catch up on changes
When the user opens this folder — especially if it's been a while — or asks "what changed?", reconcile the
docs with the real files before doing anything else that depends on them:
1. Run `python3 <skill-dir>/scripts/snapshot.py diff .` in each folder to see added / modified / renamed /
   deleted files since the last snapshot. (`<skill-dir>` = where this skill lives.)
2. For each change, open the file (bounded read) and tell the user in plain words what changed — including
   changed numbers in a re-saved spreadsheet; do NOT dismiss those as cosmetic.
3. On the user's OK, update `index.md` (repoint/add/remove entries), APPEND one dated line per change to
   `log.md`, and restamp `timestamp`. A rename → repoint the entry, don't record it as delete + new.
4. Refresh the memory: `python3 <skill-dir>/scripts/snapshot.py write .`.
5. If a new folder of documents appeared with no docs, scaffold it (CLAUDE.md + AGENTS.md + index.md + log.md
   + snapshot). When anything is unclear, ASK the user here in the chat — don't guess, don't defer to a file.
~~~

---

## 1c. Router-only folders (a "mother" that holds ONLY subfolders)

A folder that holds **no artifacts of its own — only topic subfolders** (e.g. a root over `Decks/`, `Model/`,
`Reports/`) is NOT a "meaningful folder": it gets **only `CLAUDE.md` + `AGENTS.md`**, and **no `index.md` /
`log.md` / `.okf-state.json`.** Its `AGENTS.md` `## Knowledge` section points **DOWN at the subfolders**, not at
a local `index.md` that wouldn't exist (that would leave a dangling link and fail `validate.py`). Use this
`## Knowledge` in place of the one in §1:

~~~md
## Knowledge
This folder routes to topic subfolders, each self-contained:
- [`Decks/`](./Decks/) — <one line>
- [`Model/`](./Model/) — <one line>
- [`Reports/`](./Reports/) — <one line>
~~~

If the root is a router-only folder, it still carries the root-only blocks from §1b (top-of-tree, tone,
catch-up). Everything else — the five files — lives in the meaningful subfolders below. (If a folder holds
BOTH its own artifacts AND subfolders, it's meaningful: give it the full five files, and list the subfolders as
extra links under `## Knowledge`.)

---

## 2. `CLAUDE.md` stub (root and every folder — identical)

~~~md
@AGENTS.md
~~~

The whole file is that one line: Claude Code only auto-loads `CLAUDE.md`, and `@AGENTS.md` imports the router
in the same directory. (You may add a single `<!-- comment -->` line above it.)

---

## 3. `index.md` (the folder's knowledge — current state, inline)

~~~md
---
type: index
title: <Folder name> — knowledge
description: <one line>
tags: [<tag>]
timestamp: 2026-07-01T12:00:00Z
---

# <Folder name> — knowledge

## What's here
<The deliverables/artifacts in this folder and what each is for. Where the real file lives.>
- `<file>` — <what it is; the current version>. See [decisions](#decisions) if it changed.

## Definitions & assumptions
<Terms, metrics, premises a reader needs. Keep it readable — this is for a human too.>

## How to work here
<Common tasks; what NOT to touch; where a value comes from.>

## Decisions
<The "why" behind the current state — short. Full timeline is in log.md.>
~~~

> For a **document folder**, `## What's here` is the heart: name each deck/sheet/PDF, its current version, and
> where it lives (path or Drive/SharePoint URL). Point at the real artifact; don't paste it in.

---

## 4. `log.md` (append-only history — the memory)

~~~md
---
type: log
title: <Folder name> — change log
timestamp: 2026-07-01T12:00:00Z
---

# <Folder name> — change log

Append-only. Newest first. Never rewrite a past line.

- 2026-06-28T10:00:00Z — model v7→v8: NRR now excludes one-offs (it was overstating retention).
  v7 archived to _archive/model_q3_v7.xlsx. (J. Smith, via Drive)
- 2026-05-10T09:00:00Z — model v7 created.
~~~

---

## 5. `.okf-state.json` (the watcher's snapshot)

~~~json
{
  "generated": "2026-07-01T12:00:00Z",
  "files": [
    { "path": "model_q3_v8.xlsx", "sha256": "<hex>", "mtime": 1782900000, "size": 184320 }
  ]
}
~~~

---

## Resulting tree

```
your-folder/
├── Talk to my files.command   # launcher — drop ONLY the one matching the OS
│                              #   (.command on Mac, .bat on Windows). See LAUNCHER.md.
├── CLAUDE.md            # @AGENTS.md
├── AGENTS.md            # thin router (Rules + pointers + Keep current; root adds tone + catch-up)
├── index.md            # the folder's knowledge (inline)
├── log.md              # append-only history
├── .okf-state.json     # change-memory snapshot (written by snapshot.py)
├── _archive/           # old artifacts kept for recall (e.g. model_q3_v7.xlsx)
└── subfolder/          # every meaningful subfolder is self-contained:
    ├── CLAUDE.md       #   open it alone and its context still auto-loads
    ├── AGENTS.md       #   (carries its own "If you opened only this folder" up-pointer)
    ├── index.md
    └── log.md
```

The launcher lives at the **root only** — it opens `claude` at the top of the tree, which auto-loads every
router down the chain.

---

## When a folder outgrows this skill

Move a specific folder to the heavier sibling skill **`agent-friendly-docs`** (OKF concept bundle + graph) only
when it's genuinely **complex and dense** — several of these at once:

- **many versioned artifacts with real history** worth linkable, superseded nodes (v6→v7→v8 + the "why");
- **knowledge reused across many folders** (one canonical definition linked everywhere, not copy-pasted);
- **a web of files that RUN and depend on each other** — the construction itself is the deliverable.

A folder that merely *contains* a few SQL queries or a script but stays readable and independent is **not** that
— keep the flat shape. Clarity over machinery; escalate only when the density demands it.
