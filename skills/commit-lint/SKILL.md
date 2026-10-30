---
name: commit-lint
description: Lint a git commit message against the Conventional Commits spec. Use before committing, in a pre-commit gate, or to validate an existing commit's message format.
---

# commit-lint

Dependency-free linter for [Conventional Commits](https://www.conventionalcommits.org).
Validates `type(scope)!: subject` format and rejects unknown types or malformed
headers. Returns exit code `0` when valid, `1` when invalid — so it drops
straight into a `commit-msg` hook or CI gate.

## When to use

- Validating a commit message before it lands.
- A `pre-commit` / `commit-msg` hook that fails the commit on a bad message.
- Pairing with `gen-changelog` (which groups by commit type) so the log
  actually contains well-typed commits to group.

## Usage

```bash
python commit_lint.py "feat(auth): add OAuth2 login"
python commit_lint.py --from-git          # lint the last commit
python commit_lint.py --file COMMIT_MSG    # lint a file
git log -1 --pretty=%B | python commit_lint.py --stdin
```

## Exit codes

- `0` valid
- `1` invalid message (errors printed to stderr)
- `2` usage / environment error (e.g. git not available for `--from-git`)

## Notes

- Allowed types: `feat, fix, docs, style, refactor, perf, test, build, ci,
  chore, revert`.
- Subject hard limit is enforced by rejecting empty/unknown headers; the 72-char
  soft limit emits a warning, not a failure.
- Pure stdlib — no `pip install`, runs offline.
