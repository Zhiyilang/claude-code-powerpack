# Claude Code Powerpack 🤖

A small, dependency-free toolkit that makes Claude Code (and any agentic
coding workflow) safer and more productive. Every tool here is **stdlib-only**
Python or shell — no `pip install`, works offline, drops into any repo.

## What's inside

| Tool | Path | What it does |
|------|------|--------------|
| **gen-changelog** | `skills/gen-changelog/` | Generate a grouped `CHANGELOG.md` from `git log` (Conventional Commits aware). |
| **block-destructive** | `hooks/block-destructive/` | A Claude Code `PreToolUse` hook that blocks `rm -rf /`, force-push, drop-table, and other foot-guns before they run. |
| **pr-reviewer** | `pr-reviewer/` | A structured PR-review prompt that outputs a Markdown report (risk, breaking changes, tests, summary). |

## Install

```bash
git clone https://github.com/Zhiyilang/claude-code-powerpack.git
# gen-changelog:
python claude-code-powerpack/skills/gen-changelog/gen_changelog.py > CHANGELOG.md
# block-destructive: copy the hook + settings into your repo's .claude/
```

## Why this exists

Claude-builders-style bounty boards pay out via Stripe, which does **not**
serve mainland-China individuals. So instead of chasing bounties that can't be
collected, this pack is released as an open, ownable asset: free to use, with
a PayPal donation link for those who find it valuable. If it saves you an
afternoon, buy the maintainer a coffee. ☕

## Support

If this toolkit helps you ship faster or avoid a catastrophe, consider a
PayPal tip — it funds more free tooling.

👉 **Replace the link in [`.github/FUNDING.yml`](.github/FUNDING.yml) with your
own PayPal.me ID after you register a PayPal China personal-seller account.**

## License

MIT — do whatever you want, just keep the notice.
