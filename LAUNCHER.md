# The one-click launcher — "Talk to my files"

The front door. A non-technical person double-clicks it and talks to the folder — **no VS Code, no terminal
commands, no `cd`.** Under the hood it just `cd`s into the folder and opens the `claude` chat there; the whole
value is removing the "open an IDE and type a command" friction.

This skill ships two ready launchers in **[assets/](assets/)**:

- **`assets/Talk to my files.bat`** — Windows (the majority audience). Double-click in File Explorer.
- **`assets/Talk to my files.command`** — macOS. Double-click in Finder.

**Both let the user pick the assistant at the start.** If both `claude` (Claude Code) and `codex` (Codex) are
installed, the launcher shows a one-key menu — `[1] Claude Code  [2] Codex` — and opens the chosen one. If only
one is installed, it opens that one directly (no menu). The `.bat` also falls back to `wsl claude`.

## How to deploy (loop step 6)

1. **Copy both into the mother (root) folder only.** They open `claude` at the top of the tree, which
   auto-loads every router down the chain. Don't scatter one per subfolder.
   - A folder synced by Drive/SharePoint can be opened on either OS, so dropping **both** is the safe default.
     If you know the audience is Windows-only (or Mac-only), you may drop just the one.
2. **The banner is English.** If you want it in another language for the person clicking, edit the
   `echo` / `printf` lines to match — the banner is for the person clicking, not the project content.
3. **Rename to taste.** Keep it obvious and inviting: "Talk to my files", "Ask this folder",
   "Folder assistant". Keep the `.bat` / `.command` extension.
4. **On macOS, make it executable and de-quarantine** the copy you place:
   `chmod +x "<root>/Talk to my files.command"` and, if it was synced/downloaded,
   `xattr -d com.apple.quarantine "<root>/Talk to my files.command" 2>/dev/null || true`.
5. **Tell the user in one plain sentence** how to open it, and warn about the first-run OS prompt (below).

## What the banner does (both files)

- `clear` / `cls` the screen so no scary shell text shows.
- Print a warm English greeting + two or three example questions.
- **Detect which assistants are installed** (`claude`, `codex`): if both, show a one-key `[1]/[2]` menu; if
  one, open it directly; if neither, print a **gentle install message** with both links instead of a technical
  error (the `.bat` also tries `wsl claude` first).
- Open the chosen assistant in the folder, then print a friendly goodbye when the chat ends.

Keep the banner short and human. The tone of the **chat itself** is set separately by the
`## How to talk to the user` block in the root `AGENTS.md` (see [shape-basic.md](shape-basic.md)).

## Honest limits — state these to the user

- **First-run OS gatekeeping.** An unsigned launcher trips a one-time warning:
  - **Windows / SmartScreen:** *"Windows protected your PC"* → **More info → Run anyway.**
  - **macOS / Gatekeeper:** *"unidentified developer"* → **right-click the file → Open → Open.**
  - Removing this permanently needs a paid code-signing certificate — usually not worth it. Just tell them the
    one click to get past it.
- **It does not install or log in the assistant.** First ever run still needs `claude` or `codex` installed and
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
