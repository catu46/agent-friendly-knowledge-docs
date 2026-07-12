# The reconciliation watcher

The second deliverable: after setup, the docs **keep themselves current** even when people edit files
**outside** Claude Code — dropping a new deck in, duplicating an Excel to `v8`, renaming in Drive/SharePoint.
A scheduled agent wakes up, reads what changed, and updates the flat `index.md` / `log.md` append-only.

The exact agent instructions live in **[scripts/watcher-prompt.txt](scripts/watcher-prompt.txt)** — that file
is the contract; this page is the operator's guide.

## What each run does

1. **Discover new scopes** — scaffold any meaningful folder that has artifacts but no docs yet (or queue an
   ask if it's ambiguous).
2. **Detect** — diff the filesystem against each folder's `.okf-state.json` snapshot (by `sha256`, not mtime),
   using the strongest backend available (git → filesystem → Drive/SharePoint API).
3. **Classify** — read each changed file (bounded reads) and decide: data-refresh / new-version / new-file /
   structural / deletion. A **materiality gate** (`artifact-diff.py`) skips cosmetic edits so the docs only
   move when the folder's *contents* actually change.
4. **Apply** — update `index.md` and append one line to `log.md`, append-only, in the owning folder.
5. **Ask when unsure** — queue a question in `ASKS.md` at the tree root instead of guessing; attribute the
   last editor honestly per source.
6. **Rewrite the snapshot** and **report** `validate.py` PASS/FAIL.

## Arming it — `scripts/arm-watcher.sh`

Runner-agnostic; drives any headless agent over any local path (including a synced SharePoint / OneDrive /
Drive folder) or a git checkout.

```
scripts/arm-watcher.sh <TARGET_DIR> [--runner "<cmd>"] [--cron "<expr>"] [--install]
```

- **`--runner`** — the headless agent command. Default `claude -p`; e.g. `codex exec`, `gemini -p`.
- **`--cron`** — schedule. Default `30 7 * * 1-5` (07:30, weekdays).
- **`--install`** — actually write the line into your crontab. **Omit it for a dry run** that just prints the
  line. **Confirm with the user before installing a scheduled job.**

It deploys `watcher-prompt.txt` + `validate.py` + `artifact-diff.py` into a hidden `.okf/` inside the target
(dotted, so `validate.py` prunes it), and resolves the runner to an absolute path (cron runs with a minimal
PATH, so a bare `claude` would silently fail).

```
# dry run first (prints the cron line, installs nothing)
scripts/arm-watcher.sh ~/SharePoint/ClientX
# then, once confirmed:
scripts/arm-watcher.sh ~/SharePoint/ClientX --install
```

## Optional control files (at the tree root)

- **`.okfignore`** — one glob per line; excludes files/folders from both the validator and the watcher.
- **`.okf/always-ask`** — one glob per line; any change to a matching file is **always** queued as an ask and
  never auto-applied, however confident the watcher is (use for sensitive artifacts).
- **`ASKS.md`** — append-only; where the watcher files questions it can't answer. Review it periodically.

## Honest limits — state these plainly

- **Scheduled = next run, not instant.** For a live update, just work in the folder agentically — the watcher
  is the safety net for edits made *outside* Claude Code, not a real-time sync.
- **Only meaningful folders are scaffolded;** clear cases auto-apply, ambiguous cases ask.
- **Attribution depends on the source.** git gives a real author; Drive/SharePoint give "last modified by";
  a plain filesystem often gives only an OS account, not the human. The watcher states which source a name
  came from and never fabricates one.
- **The watcher needs read access** to the source, and (for scheduled runs) the runner authenticated in a
  non-interactive context.
