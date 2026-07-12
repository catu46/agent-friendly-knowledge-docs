#!/usr/bin/env python3
"""validate.py - shape checker for agent-friendly-knowledge-docs trees.

Stdlib only (no third-party imports); runs anywhere with Python 3.8+.
This skill is BASIC-ONLY: every meaningful folder is a flat `index.md` (the
folder's knowledge) + `log.md`. The knowledge/-bundle ("pro-max") checks below are
inherited from the sibling skill agent-friendly-docs and stay DORMANT here — a
basic-only tree never has a knowledge/ subdir, so those branches never fire. Do
NOT build a knowledge/ bundle for this skill; if a folder ever needs one, it
belongs to agent-friendly-docs instead.
Enforces the CONTRACT shape, AUTO-DETECTING each meaningful folder:
  - basic shape   = a flat index.md (the folder's knowledge) + log.md;   [this skill]
  - pro-max shape = a lazy knowledge/ OKF bundle (dormant; sibling skill only).
Both share the same front door: a thin AGENTS.md router + a one-line "@AGENTS.md"
CLAUDE.md stub that imports it (Claude Code auto-loads CLAUDE.md, not AGENTS.md;
the @import pulls AGENTS.md into context at launch). A folder with AGENTS.md but
neither shape is treated as a pure router (allowed for mother/intermediate
folders) and only WARNs.

Run it on a GENERATED documentation tree, not on the skill's own source
(whose shape-pro-max.md / shape-basic.md deliberately contain example links
inside code fences that do not resolve; those fences are skipped, but other
repo docs may not be).

Usage:
    python3 validate.py [PATH]      # PATH defaults to the current directory
    python3 validate.py --help

Directory skipping:
    A hardcoded skip list (.git, node_modules, dist, build, .next, target,
    vendor, __pycache__, _archive, and any dotted dir) is always applied.
    An optional .okfignore at the root adds more patterns, one per line
    (blank lines and '#' comments ignored; matched by basename or as an
    fnmatch glob against the path relative to root).

Exit code: nonzero ONLY when an ERROR is found. WARN findings are printed
but never fail the run.

ERROR checks (any failure -> exit 1):
  1. every non-excluded directory with content has BOTH AGENTS.md and CLAUDE.md
  2. each CLAUDE.md is exactly "@AGENTS.md" (one optional leading HTML-comment line allowed)
  3. every .md with YAML frontmatter has required keys: type + title + timestamp
     (title is required on every frontmatter doc, not just AGENTS.md/concepts)
  3b. the fixed-name files carry their canonical type value — AGENTS.md→agent-guide,
     index.md→index, log.md→log — a mismatch is an ERROR
  4. every relative markdown link resolves to an existing file
  5. every relative "resource:" path exists on disk (URLs are skipped)
  6. a knowledge/ subtree has an index.md (pro-max shape)
  7. timestamps parse as ISO-8601
  8. if "status" is present it is one of: active|superseded|deprecated
  9. relative "supersedes"/"superseded_by" paths resolve to existing files

(A basic-shape folder's flat index.md/log.md are guarded by the router's own
markdown links via CHECK 4: the template down-pointer "[./index.md](./index.md)"
fails to resolve if the file is missing.)

WARN checks (printed, never fail the run):
 10. a concept with status: superseded has no superseded_by
 11. a folder AGENTS.md lacks the "If you opened only this folder" up-pointer
     while a parent AGENTS.md exists
 12. an AGENTS.md is missing a load-bearing section
     ("## Rules" / "## Knowledge" / "## Keep this current")
 13. a basic-shape folder (flat index.md, no knowledge/) has no log.md
 14. a documented folder has neither a knowledge/ bundle nor an index.md
     (pure router — fine for a mother/intermediate folder, flagged in case not)
"""

import argparse
import datetime
import fnmatch
import os
import re
import sys

# Always-skipped directory basenames (plus any dotted dir, handled separately).
DEFAULT_EXCLUDED = {
    ".git", "node_modules", "dist", "build", ".next", "target",
    "vendor", "__pycache__", "_archive",
    "venv", "env", ".venv",          # Python virtualenvs
}
# Always-skipped directory glob patterns (matched against the basename).
DEFAULT_EXCLUDED_GLOBS = ("*.egg-info",)
VALID_STATUS = {"active", "superseded", "deprecated"}
UP_POINTER_HEADING = "## If you opened only this folder"

errors = []    # list of (path, message)
warnings = []  # list of (path, message)


def err(path, msg):
    errors.append((path, msg))


def warn(path, msg):
    warnings.append((path, msg))


def is_url(value):
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", value)) or value.startswith("mailto:")


# --------------------------------------------------------------------------- #
# Frontmatter / timestamp parsing (no pyyaml)
# --------------------------------------------------------------------------- #

def parse_frontmatter(text):
    """Return (frontmatter_dict_or_None, body) for a markdown file.

    Minimal YAML: only flat `key: value` lines are read (enough for the keys
    this validator cares about). Inline `# comments` and wrapping quotes are
    stripped. List values like `[a, b]` are kept as their raw string; no
    third-party YAML dependency.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    fm = {}
    for raw in lines[1:end]:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        m = re.search(r"\s+#", value)  # strip an inline ' # comment'
        if m:
            value = value[: m.start()].strip()
        if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
            value = value[1:-1]
        fm[key] = value
    body = "\n".join(lines[end + 1:])
    return fm, body


def parse_timestamp(value):
    v = value.strip()
    if v.endswith("Z"):
        v = v[:-1] + "+00:00"
    try:
        datetime.datetime.fromisoformat(v)
        return True
    except ValueError:
        return False


# --------------------------------------------------------------------------- #
# Markdown link resolution
# --------------------------------------------------------------------------- #

def strip_code_fences(text):
    """Remove fenced code blocks (``` and ~~~) so example links inside them
    are not treated as real links."""
    out = []
    fence_char = None
    for line in text.splitlines():
        s = line.lstrip()
        m = re.match(r"(`{3,}|~{3,})", s)
        if fence_char is None:
            if m:
                fence_char = m.group(1)[0]
                continue
            out.append(line)
        else:
            if m and m.group(1)[0] == fence_char:
                fence_char = None
            # drop fence body lines
    return "\n".join(out)


MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def check_markdown_links(path, body, base_dir):
    """CHECK 4: every relative markdown link resolves to an existing file."""
    scan = strip_code_fences(body)
    for m in MD_LINK_RE.finditer(scan):
        target = m.group(1).strip()
        if not target or target.startswith("#"):
            continue
        # strip an optional  "title"
        mt = re.match(r'^(.*?)\s+"[^"]*"$', target)
        if mt:
            target = mt.group(1).strip()
        # strip surrounding < >
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()
        if is_url(target):
            continue
        target = target.split("#", 1)[0]  # drop anchor
        if not target or target.startswith("/"):
            continue
        resolved = os.path.normpath(os.path.join(base_dir, target))
        if not os.path.exists(resolved):
            err(path, 'markdown link does not resolve: "%s"' % target)


# --------------------------------------------------------------------------- #
# Directory predicates
# --------------------------------------------------------------------------- #

def load_ignore_patterns(root):
    """Read an optional .okfignore at the root. One pattern per line; blank
    lines and '#' comments ignored. A trailing '/' is stripped."""
    patterns = []
    ignore_file = os.path.join(root, ".okfignore")
    if os.path.isfile(ignore_file):
        try:
            with open(ignore_file, encoding="utf-8") as f:
                for line in f:
                    s = line.strip()
                    if not s or s.startswith("#"):
                        continue
                    patterns.append(s.rstrip("/"))
        except OSError:
            pass
    return patterns


def dir_excluded(name, relpath, ignore_patterns):
    """Should this directory be pruned from the walk? (root is never pruned)."""
    if name in DEFAULT_EXCLUDED or name.startswith("."):
        return True
    if any(fnmatch.fnmatch(name, g) for g in DEFAULT_EXCLUDED_GLOBS):
        return True
    relpath = relpath.replace(os.sep, "/")
    for pat in ignore_patterns:
        if fnmatch.fnmatch(name, pat):
            return True
        if fnmatch.fnmatch(relpath, pat):
            return True
        if fnmatch.fnmatch(relpath, pat + "/*"):
            return True
    return False


def in_knowledge(dirpath, root):
    rel = os.path.relpath(dirpath, root)
    parts = [] if rel == "." else rel.split(os.sep)
    return "knowledge" in parts


def needs_both_docs(dirpath, root):
    """A directory 'with content' (any non-hidden file) needs both docs,
    unless it lives inside a knowledge/ bundle."""
    if in_knowledge(dirpath, root):
        return False
    try:
        entries = os.listdir(dirpath)
    except OSError:
        return False
    return any(
        os.path.isfile(os.path.join(dirpath, e)) and not e.startswith(".")
        for e in entries
    )


def parent_agents_exists(dirpath, root):
    """Is there an AGENTS.md in any ancestor up to (and including) root?"""
    root = os.path.abspath(root)
    cur = os.path.abspath(os.path.dirname(dirpath))
    while cur == root or cur.startswith(root + os.sep):
        if os.path.isfile(os.path.join(cur, "AGENTS.md")):
            return True
        if cur == root:
            break
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return False


# --------------------------------------------------------------------------- #
# Per-file checks
# --------------------------------------------------------------------------- #

def check_claude_stub(path):
    """CHECK 2: CLAUDE.md is exactly '@AGENTS.md' (one optional leading
    HTML-comment line allowed)."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = [ln.rstrip() for ln in text.splitlines()]
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines) and re.match(r"^\s*<!--.*-->\s*$", lines[i]):
        i += 1
        while i < len(lines) and lines[i].strip() == "":
            i += 1
    rest = [ln for ln in lines[i:] if ln.strip() != ""]
    if rest != ["@AGENTS.md"]:
        err(path, 'CLAUDE.md must be exactly "@AGENTS.md" '
                  "(one optional leading HTML-comment line allowed)")


def check_md(path, root):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm, body = parse_frontmatter(text)
    base_dir = os.path.dirname(path)
    name = os.path.basename(path)

    # CHECK 4: markdown links resolve
    check_markdown_links(path, body if fm is not None else text, base_dir)

    if fm is None:
        # A canonical doc (the three fixed-name files, or any concept .md inside a
        # knowledge/ subtree) MUST carry frontmatter — silently passing one with
        # its whole `---` block deleted would defeat CHECK 3. Free-form notes that
        # happen to be .md are fine without it, so only fire on canonical docs.
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        in_knowledge = "/knowledge/" in ("/" + rel)
        if name in ("AGENTS.md", "index.md", "log.md") or (in_knowledge and name.endswith(".md")):
            err(path, "missing YAML frontmatter (canonical docs require type + title + timestamp)")
        return

    # CHECK 3: required frontmatter keys (type + timestamp + title on every doc)
    if "type" not in fm:
        err(path, 'frontmatter missing required key "type"')
    if "timestamp" not in fm:
        err(path, 'frontmatter missing required key "timestamp"')
    if "title" not in fm:
        err(path, 'frontmatter missing required key "title"')
    typ = fm.get("type", "")
    # CHECK 3b: the three fixed-name files must carry their canonical type.
    expected_type = {"AGENTS.md": "agent-guide", "index.md": "index", "log.md": "log"}.get(name)
    if expected_type and typ and typ != expected_type:
        err(path, 'type "%s" should be "%s" for %s' % (typ, expected_type, name))

    # CHECK 7: timestamp parses as ISO-8601
    if "timestamp" in fm and not parse_timestamp(fm["timestamp"]):
        err(path, 'timestamp is not valid ISO-8601: "%s"' % fm["timestamp"])

    # CHECK 5: resource path exists (URLs skipped)
    res = fm.get("resource", "")
    if res and not is_url(res):
        resolved = os.path.normpath(os.path.join(base_dir, res))
        if not os.path.exists(resolved):
            err(path, 'resource path does not exist: "%s"' % res)

    # CHECK 8: status value valid
    status = fm.get("status", "")
    if status and status not in VALID_STATUS:
        err(path, 'invalid status "%s" (expected active|superseded|deprecated)' % status)

    # CHECK 9: supersedes / superseded_by resolve
    for key in ("supersedes", "superseded_by"):
        val = fm.get(key, "")
        if val and not is_url(val):
            resolved = os.path.normpath(os.path.join(base_dir, val))
            if not os.path.exists(resolved):
                err(path, '%s path does not resolve: "%s"' % (key, val))

    # WARN 10: superseded without superseded_by
    if status == "superseded" and not fm.get("superseded_by"):
        warn(path, 'status is "superseded" but "superseded_by" is missing')

    # WARN 11/12: folder AGENTS.md structure
    if name == "AGENTS.md":
        if UP_POINTER_HEADING not in body and parent_agents_exists(base_dir, root):
            warn(path, 'AGENTS.md lacks the "If you opened only this folder" up-pointer')
        for heading in ("## Rules", "## Knowledge", "## Keep this current"):
            if heading not in body:
                warn(path, 'AGENTS.md is missing the "%s" section' % heading)


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #

def run(root):
    ignore_patterns = load_ignore_patterns(root)
    md_files = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune excluded subdirectories in place.
        kept = []
        for d in dirnames:
            child = os.path.join(dirpath, d)
            rel = os.path.relpath(child, root)
            if not dir_excluded(d, rel, ignore_patterns):
                kept.append(d)
        dirnames[:] = kept

        name = os.path.basename(dirpath)

        # CHECK 1: meaningful folder needs BOTH AGENTS.md and CLAUDE.md
        if needs_both_docs(dirpath, root):
            missing = [f for f in ("AGENTS.md", "CLAUDE.md") if f not in filenames]
            if missing:
                err(dirpath, "folder with content is missing %s" % ", ".join(missing))

        # CHECK 6: a knowledge/ subtree must have an index.md (pro-max shape)
        if name == "knowledge" and "index.md" not in filenames:
            err(dirpath, "knowledge/ subtree has no index.md")

        # CHECK 13/14: a documented folder must carry ONE knowledge shape.
        # pro-max = a knowledge/ subdir (its index.md enforced by CHECK 6);
        # basic   = a flat index.md (+ log.md, the append-only history).
        # Neither = a pure router, allowed for mother/intermediate folders.
        # (A dangling basic down-pointer is caught as an ERROR by CHECK 4.)
        if "AGENTS.md" in filenames and not in_knowledge(dirpath, root):
            has_knowledge = os.path.isdir(os.path.join(dirpath, "knowledge"))
            has_index = "index.md" in filenames
            if not has_knowledge and has_index and "log.md" not in filenames:
                warn(dirpath, "basic-shape folder has index.md but no log.md "
                              "(append-only history)")
            elif not has_knowledge and not has_index:
                warn(dirpath, "folder has AGENTS.md but neither a knowledge/ bundle "
                              "(pro-max) nor an index.md (basic) — pure router?")

        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            if fn == "CLAUDE.md":
                check_claude_stub(fp)  # CHECK 2
            if fn.endswith(".md"):
                md_files.append(fp)

    for fp in md_files:
        check_md(fp, root)

    return md_files


def main(argv):
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="Shape checker for agent-friendly-knowledge-docs (AGENTS.md) trees. "
                    "Stdlib only. Exits 1 only on an ERROR; WARN findings never fail.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="ERROR checks 1-9 and WARN checks 10-14 are documented in the module "
               "docstring. Add a .okfignore at the root to skip extra paths.",
    )
    parser.add_argument(
        "path", nargs="?", default=".",
        help="root directory to validate (default: current directory)",
    )
    args = parser.parse_args(argv[1:])

    root = os.path.abspath(args.path)
    if not os.path.isdir(root):
        sys.stderr.write("ERROR: not a directory: %s\n" % root)
        return 2

    md_files = run(root)

    print("agent-friendly-knowledge-docs :: validate")
    print("root: %s" % root)
    print("markdown files scanned: %d" % len(md_files))

    if warnings:
        print("\nWARN (%d):" % len(warnings))
        for p, m in warnings:
            print("  WARN  %s: %s" % (os.path.relpath(p, root), m))

    if errors:
        print("\nERROR (%d):" % len(errors))
        for p, m in errors:
            print("  ERROR %s: %s" % (os.path.relpath(p, root), m))
        print("\nFAIL - %d error(s), %d warning(s)" % (len(errors), len(warnings)))
        return 1

    print("\nPASS - 0 errors, %d warning(s)" % len(warnings))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
