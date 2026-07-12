#!/bin/bash
# ─────────────────────────────────────────────────────────────
# Organize a folder with AI
# Double-click, pick a folder, pick an assistant, and watch the
# AI set that folder up to be navigable and self-updating.
# Carries its own skill, so it installs itself on first run.
# (agent-friendly-knowledge-docs)
# ─────────────────────────────────────────────────────────────

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"   # this folder IS the skill
SKILL_NAME="agent-friendly-knowledge-docs"

clear
if [ -t 1 ]; then
  B=$'\033[1m'; DIM=$'\033[2m'; BLUE=$'\033[38;5;68m'; GREEN=$'\033[38;5;71m'; R=$'\033[0m'
else
  B=""; DIM=""; BLUE=""; GREEN=""; R=""
fi

printf '\n   %s%sLet'\''s organize a folder with AI 🗂️%s\n\n' "$B" "$BLUE" "$R"
printf '   I'\''ll set up a folder of yours so any AI assistant can navigate it\n'
printf '   and keep it updated. Two clicks: pick the folder, pick the assistant.\n\n'
printf '   %s──────────────────────────────────────────────%s\n\n' "$DIM" "$R"

# 1) Install the skill for BOTH assistants (idempotent — safe to repeat).
for base in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
  mkdir -p "$base"
  if [ ! -e "$base/$SKILL_NAME" ]; then
    ln -s "$SKILL_DIR" "$base/$SKILL_NAME" 2>/dev/null \
      && printf '   %s✓ installed the skill%s (%s)\n' "$GREEN" "$R" "$base"
  fi
done
printf '\n'

# 2) Native folder picker.
printf '   Opening a window to choose the folder…\n'
TARGET="$(osascript -e 'try
POSIX path of (choose folder with prompt "Which folder should the AI organize?")
end try' 2>/dev/null)"
if [ -z "$TARGET" ]; then
  printf '\n   %sNo folder chosen — nothing to do. You can close this window.%s\n\n' "$DIM" "$R"
  exit 0
fi
TARGET="${TARGET%/}"
printf '   %sFolder:%s %s\n\n' "$B" "$R" "$TARGET"

# 3) Which assistant? (both can run this skill natively)
have() { command -v "$1" >/dev/null 2>&1; }
have_claude=0; have claude && have_claude=1
have_codex=0;  have codex  && have_codex=1
status() { if [ "$1" -eq 1 ]; then printf '%s✓ installed%s' "$GREEN" "$R"; else printf "%s— not installed%s" "$DIM" "$R"; fi; }

printf '   %sWhich assistant should apply it?%s\n\n' "$B" "$R"
printf '   %s[1]%s Claude Code   ' "$B" "$R"; status "$have_claude"; printf '\n'
printf '   %s[2]%s Codex         ' "$B" "$R"; status "$have_codex";  printf '\n\n'
printf '   Type 1 or 2 and press Enter: '
read -r choice
printf '\n'
case "$choice" in 2) sel=codex; installed=$have_codex ;; *) sel=claude; installed=$have_claude ;; esac

if [ "$installed" -ne 1 ]; then
  printf "   %sThat assistant isn'\''t installed yet.%s Install it once, then run this again:\n" "$B" "$R"
  if [ "$sel" = codex ]; then
    printf '   %shttps://learn.chatgpt.com/docs/codex/cli%s\n\n' "$BLUE" "$R"
    open "https://learn.chatgpt.com/docs/codex/cli" >/dev/null 2>&1
  else
    printf '   %shttps://claude.com/claude-code%s\n\n' "$BLUE" "$R"
    open "https://claude.com/claude-code" >/dev/null 2>&1
  fi
  printf '   %s(You can close this window.)%s\n\n' "$DIM" "$R"
  exit 0
fi

# 4) Apply the skill inside the chosen folder — the user watches it work.
cd "$TARGET" || { printf '   Could not open that folder.\n'; exit 1; }
PROMPT="Use the $SKILL_NAME skill to organize this folder (the current directory) so an AI can navigate it and keep it updated. Interview me in my language, then set it up."
printf '   %sApplying the skill in your folder now — watch below.%s\n' "$GREEN" "$R"
printf '   %s(If it just opens a chat, paste this: "organize this folder for AI".)%s\n\n' "$DIM" "$R"

if [ "$sel" = codex ]; then
  codex "$PROMPT"
else
  claude "$PROMPT"
fi

printf '\n   %sDone! Your folder is set up. You can close this window 👋%s\n\n' "$BLUE" "$R"
