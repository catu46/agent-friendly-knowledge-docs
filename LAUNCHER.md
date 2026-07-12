# The one-click launcher — "Falar com meus arquivos"

The front door. A non-technical person double-clicks it and talks to the folder — **no VS Code, no terminal
commands, no `cd`.** Under the hood it just `cd`s into the folder and opens the `claude` chat there; the whole
value is removing the "open an IDE and type a command" friction.

This skill ships two ready launchers in **[assets/](assets/)**:

- **`assets/Falar com meus arquivos.bat`** — Windows (the majority audience). Double-click in File Explorer.
- **`assets/Falar com meus arquivos.command`** — macOS. Double-click in Finder.

## How to deploy (loop step 6)

1. **Copy both into the mother (root) folder only.** They open `claude` at the top of the tree, which
   auto-loads every router down the chain. Don't scatter one per subfolder.
   - A folder synced by Drive/SharePoint can be opened on either OS, so dropping **both** is the safe default.
     If you know the audience is Windows-only (or Mac-only), you may drop just the one.
2. **Translate the banner to the user's language.** The shipped copy is Portuguese. If the user writes to you
   in another language, edit the `echo`/`printf` lines to match — the banner is for the person clicking, not
   the project content.
3. **Rename to taste.** Keep it obvious and inviting: "Falar com meus arquivos", "Talk to my files",
   "Assistente desta pasta". Keep the `.bat` / `.command` extension.
4. **On macOS, make it executable and de-quarantine** the copy you place:
   `chmod +x "<root>/Falar com meus arquivos.command"` and, if it was synced/downloaded,
   `xattr -d com.apple.quarantine "<root>/Falar com meus arquivos.command" 2>/dev/null || true`.
5. **Tell the user in one plain sentence** how to open it, and warn about the first-run OS prompt (below).

## What the banner does (both files)

- `clear` / `cls` the screen so no scary shell text shows.
- Print a warm greeting in the user's language + two or three example questions.
- If `claude` isn't found, print a **gentle install message** with the link instead of a technical error.
  The `.bat` also tries `wsl claude` (Claude Code inside WSL) before giving up.
- Open `claude` in the folder, then print a friendly goodbye when the chat ends.

Keep the banner short and human. The tone of the **chat itself** is set separately by the
`## How to talk to the user` block in the root `AGENTS.md` (see [shape-basic.md](shape-basic.md)).

## Honest limits — state these to the user

- **First-run OS gatekeeping.** An unsigned launcher trips a one-time warning:
  - **Windows / SmartScreen:** *"O Windows protegeu o seu computador"* → **Mais informações → Executar assim
    mesmo.**
  - **macOS / Gatekeeper:** *"desenvolvedor não identificado"* → **botão-direito no arquivo → Abrir → Abrir.**
  - Removing this permanently needs a paid code-signing certificate — usually not worth it. Just tell them the
    one click to get past it.
- **It does not install or log in Claude Code.** First ever run still needs `claude` installed and
  authenticated once. The launcher removes daily friction, not the one-time setup.
- **It's still a terminal underneath.** The banner + `clear` make it calm and friendly, but it renders as a
  clean terminal chat, not a rounded web-bubble UI. That ceiling is inherent; a real web UI is a different,
  much heavier project and generally worse than the `claude` chat it would wrap.
- **Emoji/box characters are best-effort** on legacy Windows `cmd`; they render cleanly in Windows Terminal
  (default on Windows 11).

## Optional next step (only if asked)

A macOS `.app` bundle gives the launcher a real name + icon in Finder and can open Terminal with a large-font,
calm-color profile. On Windows the equivalent (a custom icon) needs a `.lnk` shortcut, which breaks if the
folder is moved. For most audiences the nicely-named `.bat` / `.command` is enough — don't build the `.app`
unless the user asks.
