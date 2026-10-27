---
name: gen-changelog
description: Generate a grouped CHANGELOG.md from git history using Conventional Commits. Use when the user asks for a changelog, release notes, or a summary of what changed.
---

# Generate Changelog

Produce a clean, grouped `CHANGELOG.md` from the repo's git log.

## How to run

```bash
python skills/gen-changelog/gen_changelog.py [since-tag] > CHANGELOG.md
```

- No dependencies (stdlib only).
- Groups commits by type: feat / fix / perf / refactor / docs / test / style / build / ci / chore.
- Commits that don't follow Conventional Commits go under "Other".

## Example

```bash
python skills/gen-changelog/gen_changelog.py v1.0.0 > CHANGELOG.md
```

Then review the output and trim noise before committing the CHANGELOG.
