# block-destructive hook

A Claude Code `PreToolUse` hook that blocks destructive shell commands
(`rm -rf /`, `git push --force`, `drop table`, `mkfs`, `dd of=/dev/...`,
etc.) **before** they execute.

## Install

Copy this folder into your repo's `.claude/`:

```bash
mkdir -p .claude/hooks
cp -r hooks/block-destructive .claude/hooks/
cp hooks/block-destructive/settings.json .claude/settings.json   # merge if you have one
```

Now any Bash tool call matching a foot-gun pattern is refused with a reason
printed to stderr, and the command does **not** run.

## How it works

Claude Code streams the tool input JSON to the hook on stdin. The script
extracts the `command` field and greps it against a deny-list of dangerous
patterns. Exit `1` blocks; exit `0` allows.

Edit the `PATTERNS` array to tune what's forbidden for your environment.
