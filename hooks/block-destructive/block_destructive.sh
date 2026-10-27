#!/usr/bin/env bash
# Claude Code PreToolUse hook: block destructive bash before it runs.
# Exit 0 = allow, exit 1 = block (and print the reason to stderr).
#
# Wire it up in .claude/settings.json:
#   "hooks": { "PreToolUse": [{ "matcher": "Bash",
#       "hooks": [{ "type": "command", "command": "bash hooks/block-destructive/block_destructive.sh" }] }] }

set -u

# Claude Code passes tool input as JSON on stdin.
INPUT="$(cat || true)"
CMD="$(printf '%s' "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*:[[:space:]]*"\([^"]*\)"/\1/')"

# Patterns that should never auto-run.
PATTERNS=(
  'rm[[:space:]]\+-rf[[:space:]]\+/'
  'rm[[:space:]]\+-rf[[:space:]]\+~'
  'mkfs\.'
  '>[/ ]*/dev/sd'
  'dd[[:space:]].*of=/dev/'
  'git[[:space:]]\+push[[:space:]].*--force'
  'git[[:space:]]\+push[[:space:]].*-f[[:space:]]\+'
  'git[[:space:]]\+reset[[:space:]]\+--hard'
  'git[[:space:]]\+clean[[:space:]]\+-[a-z]*f'
  'drop[[:space:]]\+table'
  'truncate[[:space:]]\+table'
  ':'[[:space:]]*'[)]'
  'chmod[[:space:]]\+-R[[:space:]]\+777[[:space:]]\+/'
)

for p in "${PATTERNS[@]}"; do
  if printf '%s' "$CMD" | grep -Eq "$p"; then
    echo "BLOCKED by block-destructive hook: matches dangerous pattern '$p'" >&2
    echo "Command was: $CMD" >&2
    exit 1
  fi
done

exit 0
