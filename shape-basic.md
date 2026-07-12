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

Write docs in the **project's language**. Replace every `<placeholder>`. Timestamps are ISO-8601 UTC. The
`## If you opened only this folder` and `## Keep this current` sections are **mandatory** in every `AGENTS.md`.
Outer fences are `~~~` so nested ``` blocks render.

---

## 1. `AGENTS.md` (the thin router — root and every folder)

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
in context. (At the repo root there is no `../AGENTS.md`: KEEP this heading but reword it to state this IS
the root.)

## Keep this current
After changing anything here, before you finish: update the relevant part of `index.md`, **append** one line
to `log.md`, and restamp `timestamp`. **Never overwrite history** (log is append-only). Created a new
meaningful subfolder? Scaffold it (CLAUDE.md + AGENTS.md + index.md + log.md) before finishing — no blind
spots. Then walk up to `../AGENTS.md` only if the change affects global rules or the map.
~~~

---

## 1b. Root-only add-on: `## How to talk to the user` (the tone block)

Add this section to the **root** `AGENTS.md` **only** (it sets the voice for the whole tree). It makes the
in-app chat feel like a friendly assistant instead of a developer tool — the reason a non-technical person can
use the launcher without being scared. Write it in the **user's** language; the block below is Portuguese for a
Portuguese-speaking consultant — translate to match.

~~~md
## Como falar com a pessoa
- Responda **na língua da pessoa** e em **linguagem simples** — sem jargão técnico, sem termos de programação.
- Seja **conciso e gentil**. Explique o que você vai fazer em uma frase antes de fazer.
- **Confirme antes de qualquer coisa destrutiva**: apagar, sobrescrever um arquivo original, ou enviar algo
  para fora. Para ações seguras e reversíveis (ler, resumir, criar um arquivo novo), pode seguir.
- Se algo estiver ambíguo (qual versão? qual cliente?), **pergunte** em vez de adivinhar.
- Nunca mexa no que está listado em "Do NOT touch".
~~~

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

- 2026-06-28T10:00:00Z — modelo v7→v8: NRR passou a excluir one-offs (superestimava retenção).
  v7 arquivada em _archive/modelo_q3_v7.xlsx. (Fulano, via Drive)
- 2026-05-10T09:00:00Z — modelo v7 criado.
~~~

---

## 5. `.okf-state.json` (the watcher's snapshot)

~~~json
{
  "generated": "2026-07-01T12:00:00Z",
  "files": [
    { "path": "modelo_q3_v8.xlsx", "sha256": "<hex>", "mtime": 1782900000, "size": 184320 }
  ]
}
~~~

---

## Resulting tree

```
your-folder/
├── Falar com meus arquivos.command   # Mac launcher (root only — see LAUNCHER.md)
├── Falar com meus arquivos.bat       # Windows launcher (root only)
├── CLAUDE.md            # @AGENTS.md
├── AGENTS.md            # thin router (Rules + pointers + Keep current + tone block at root)
├── index.md            # the folder's knowledge (inline)
├── log.md              # append-only history
├── .okf-state.json     # watcher snapshot
├── _archive/           # old artifacts kept for recall (e.g. modelo_q3_v7.xlsx)
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

Move a specific folder to the heavier sibling skill **`agent-friendly-docs`** (OKF concept bundle + graph) when
it has:

- **versioned artifacts with real history** worth linkable, superseded nodes (v6→v7→v8 + the "why");
- **knowledge reused across many folders** (one canonical definition linked everywhere, not copy-pasted);
- **files that RUN and depend on each other** (code, SQL, operational models).

Otherwise this flat shape is the right, simpler default — clarity over machinery.
