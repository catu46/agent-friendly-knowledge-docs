# The one-click launcher — "Talk to my files"

The front door. A non-technical person double-clicks it and talks to the folder — **no VS Code, no terminal
commands, no `cd`.** Under the hood it just `cd`s into the folder and opens the `claude` chat there; the whole
value is removing the "open an IDE and type a command" friction.

This skill ships two ready launchers in **[assets/](assets/)** — one per OS:

- **`assets/Talk to my files.bat`** — Windows. Double-click in File Explorer.
- **`assets/Talk to my files.command`** — macOS. Double-click in Finder.

**Each always shows the same one-key picker at the start**, marking what's installed:

```
Which assistant do you want to use?
[1] Claude Code   ✓ installed
[2] Codex         — not installed, I'll help you set it up
```

Pick an **installed** one → it opens the chat in the folder. Pick a **not-installed** one → it prints a short
note and **opens that assistant's official setup page in the browser** (no dead-end error). The `.bat` also
falls back to `wsl claude` if Claude Code is picked but only present inside WSL.

## How to deploy (loop step 6)

1. **Detect the OS you're running on and copy ONLY the matching launcher** into the mother (root) folder — the
   `.command` on macOS, the `.bat` on Windows. **One file, so a non-technical person can't click the wrong
   one.** (Native Windows has no `bash`; a `.command` there just opens a text editor, and vice-versa.)
   - **Exception:** if the user says the folder is **shared across Mac and Windows** (e.g. a synced
     Drive/SharePoint folder opened on both), drop **both**.
   - Put it at the **root only** — it opens the assistant at the top of the tree, which auto-loads every router
     down the chain. Don't scatter one per subfolder.
2. **The banner is English.** If you want it in another language for the person clicking, edit the
   `echo` / `printf` lines to match — the banner is for the person clicking, not the project content.
3. **Rename to taste.** Keep it obvious and inviting: "Talk to my files", "Ask this folder",
   "Folder assistant". Keep the `.bat` / `.command` extension.
4. **On macOS, make it executable and de-quarantine** the copy you place:
   `chmod +x "<root>/Talk to my files.command"` and, if it was synced/downloaded,
   `xattr -d com.apple.quarantine "<root>/Talk to my files.command" 2>/dev/null || true`.
5. **Tell the user in one plain sentence** how to open it, and warn about the first-run OS prompt (below).

## What the launcher does (both files)

- `clear` / `cls` the screen so no scary shell text shows.
- Print a warm English greeting + two or three example questions.
- **Detect which assistants are installed** (`claude`, `codex`) and **always show the `[1]/[2]` picker**,
  labelling each as installed or not.
- On a pick: open the chosen assistant in the folder if installed; otherwise open its official setup page in
  the browser (`open` on macOS, `start` on Windows) and pause with a friendly note.
- Print a friendly goodbye when the chat ends.

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
