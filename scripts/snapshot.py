#!/usr/bin/env python3
"""snapshot.py — the change-memory for agent-friendly-knowledge-docs.

This is what makes "what changed while I was away?" work WITHOUT any background
job. A small snapshot of each folder's real artifacts (sha256 + size + mtime) is
saved to `<folder>/.okf-state.json`. Because it persists between sessions, a fresh
chat can diff the folder against the last known state on demand — no cron, no
daemon, no headless auth. The user is present and authenticated in the chat.

Stdlib only. Per-folder, non-recursive (each meaningful folder owns its snapshot;
subfolders have their own).

Usage:
  python3 snapshot.py write <folder>     # write/refresh <folder>/.okf-state.json
  python3 snapshot.py diff  <folder>     # print what changed vs the saved snapshot
  python3 snapshot.py diff  <folder> --json   # same, machine-readable

`diff` reports added / modified / deleted, and detects a rename/move within the
folder (a deleted file and an added file with the SAME sha256 = a rename, not a
loss). Exit code is always 0; the change set is the output.

Tracks real artifacts only. Skips: dotfiles/dotdirs, the doc set the skill itself
writes (AGENTS.md, CLAUDE.md, index.md, log.md, README.md), the launchers
(`Talk to my files.*`), and anything matched by a `.okfignore` in the folder
(one glob per line, '#' comments). A file it cannot read (e.g. a cloud
"Files On-Demand" placeholder with no local bytes) is recorded with
sha256 "unreadable" and still tracked by size+mtime, plus a stderr warning.
"""

import sys
import os
import json
import hashlib
import fnmatch
import datetime

DOC_FILES = {
    "AGENTS.md", "CLAUDE.md", "index.md", "log.md", "README.md",
    ".okf-state.json", ".okfignore", "ASKS.md", "LAST-CHECK.md",
}
LAUNCHER_PREFIX = "Talk to my files"


def load_okfignore(folder):
    globs = []
    path = os.path.join(folder, ".okfignore")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    globs.append(line)
    return globs


def is_tracked(name, ignore_globs):
    if name.startswith("."):
        return False
    if name in DOC_FILES:
        return False
    if name.startswith(LAUNCHER_PREFIX):
        return False
    for g in ignore_globs:
        if fnmatch.fnmatch(name, g):
            return False
    return True


def fingerprint(path):
    """Return (sha256, size, mtime). sha256 is 'unreadable' if bytes can't be read."""
    st = os.stat(path)
    size, mtime = st.st_size, int(st.st_mtime)
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest(), size, mtime
    except OSError as e:
        sys.stderr.write(
            "warning: could not read %s (%s) — likely a cloud placeholder; "
            "tracking by size+mtime only. Set it to 'always keep on this device'.\n"
            % (os.path.basename(path), e.__class__.__name__)
        )
        return "unreadable", size, mtime


def scan(folder, ignore_globs):
    files = {}
    for name in sorted(os.listdir(folder)):
        full = os.path.join(folder, name)
        if not os.path.isfile(full):
            continue
        if not is_tracked(name, ignore_globs):
            continue
        sha, size, mtime = fingerprint(full)
        files[name] = {"path": name, "sha256": sha, "mtime": mtime, "size": size}
    return files


def now_iso():
    # UTC, no microseconds. (Date.now() is fine here — this is a real CLI, not a workflow.)
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cmd_write(folder):
    ignore_globs = load_okfignore(folder)
    files = scan(folder, ignore_globs)
    snap = {"generated": now_iso(), "files": list(files.values())}
    out = os.path.join(folder, ".okf-state.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(snap, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote %s (%d artifact%s)" % (out, len(files), "" if len(files) == 1 else "s"))


def load_snapshot(folder):
    path = os.path.join(folder, ".okf-state.json")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {e["path"]: e for e in data.get("files", [])}


def cmd_diff(folder, as_json):
    old = load_snapshot(folder)
    ignore_globs = load_okfignore(folder)
    cur = scan(folder, ignore_globs)

    if old is None:
        result = {"baseline": True, "added": [], "modified": [], "deleted": [], "renamed": []}
        _emit_diff(folder, result, as_json, no_snapshot=True)
        return

    added = [n for n in cur if n not in old]
    deleted = [n for n in old if n not in cur]
    modified = [n for n in cur if n in old and cur[n]["sha256"] != old[n]["sha256"]
                and cur[n]["sha256"] != "unreadable" and old[n]["sha256"] != "unreadable"]

    # Rename detection: a deleted file and an added file sharing a real sha256.
    renamed = []
    old_sha = {}
    for n in deleted:
        s = old[n]["sha256"]
        if s != "unreadable":
            old_sha.setdefault(s, []).append(n)
    for n in list(added):
        s = cur[n]["sha256"]
        if s in old_sha and old_sha[s]:
            src = old_sha[s].pop(0)
            renamed.append({"from": src, "to": n})
            added.remove(n)
            if src in deleted:
                deleted.remove(src)

    result = {"baseline": False, "added": added, "modified": modified,
              "deleted": deleted, "renamed": renamed}
    _emit_diff(folder, result, as_json)


def _emit_diff(folder, result, as_json, no_snapshot=False):
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if no_snapshot:
        print("No snapshot yet in %s — run `snapshot.py write` to set the baseline." % folder)
        return
    n = (len(result["added"]) + len(result["modified"])
         + len(result["deleted"]) + len(result["renamed"]))
    if n == 0:
        print("No changes since the last snapshot.")
        return
    print("Changes since the last snapshot:")
    for f in result["renamed"]:
        print("  renamed:  %s  ->  %s" % (f["from"], f["to"]))
    for f in result["added"]:
        print("  added:    %s" % f)
    for f in result["modified"]:
        print("  modified: %s" % f)
    for f in result["deleted"]:
        print("  deleted:  %s" % f)


def main(argv):
    if len(argv) < 3 or argv[1] not in ("write", "diff"):
        sys.stderr.write(__doc__)
        return 2
    cmd, folder = argv[1], argv[2]
    as_json = "--json" in argv[3:]
    if not os.path.isdir(folder):
        sys.stderr.write("not a directory: %s\n" % folder)
        return 2
    if cmd == "write":
        cmd_write(folder)
    else:
        cmd_diff(folder, as_json)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
