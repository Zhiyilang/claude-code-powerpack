#!/usr/bin/env python3
"""commit_lint.py - dependency-free conventional-commit linter.

Validates a commit message against the Conventional Commits spec
(https://www.conventionalcommits.org). Exits non-zero when the message
is invalid, so it can run as a pre-commit / pre-push gate.

Usage:
    python commit_lint.py "feat: add login button"          # lint a string
    python commit_lint.py --from-git                        # lint last commit
    python commit_lint.py --file COMMIT_MSG                 # lint a file
    git log -1 --pretty=%B | python commit_lint.py --stdin  # pipe

Exit codes:
    0  valid
    1  invalid message
    2  usage / environment error

MIT License.
"""
import sys
import re

# type(scope)!: subject
# type: one of the common Conventional Commit types (extensible)
TYPES = {
    "feat", "fix", "docs", "style", "refactor", "perf",
    "test", "build", "ci", "chore", "revert",
}
RE = re.compile(r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s?(?P<subject>.+)$", re.S)

MAX_SUBJECT = 72  # soft limit; warn only


def lint(message: str):
    """Return (ok: bool, errors: list[str], warns: list[str])."""
    errors, warns = [], []
    msg = message.strip()
    if not msg:
        return False, ["empty commit message"], []
    # strip comment lines and trailing diff cruft produced by some editors
    lines = [ln for ln in msg.splitlines() if not ln.startswith("#")]
    head = lines[0].strip() if lines else ""
    if not head:
        return False, ["empty subject line"], []
    m = RE.match(head)
    if not m:
        errors.append(
            "subject must match '<type>(<scope>): <subject>' "
            f"e.g. 'feat: add retry support'  (got: {head!r})"
        )
        return False, errors, warns
    typ = m.group("type")
    if typ not in TYPES:
        errors.append(
            f"unknown type '{typ}'. allowed: {', '.join(sorted(TYPES))}"
        )
    subject = m.group("subject").strip()
    if not subject[0].isalpha() and not subject[0].isdigit():
        errors.append("subject should start with a letter or number")
    if subject.endswith("."):
        warns.append("subject conventionally omits trailing period")
    if len(head) > MAX_SUBJECT:
        warns.append(f"subject is {len(head)} chars (> {MAX_SUBJECT}); consider shortening")
    # body present should be separated by blank line
    if len(lines) > 1:
        if lines[1].strip() != "":
            warns.append("expected blank line between subject and body")
    return (len(errors) == 0), errors, warns


def _read_from_git():
    import subprocess
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"],
            capture_output=True, text=True, timeout=15,
        )
        return out.stdout
    except Exception as e:  # pragma: no cover
        sys.stderr.write(f"commit_lint: cannot read git log: {e}\n")
        sys.exit(2)


def main(argv):
    msg = None
    if "--from-git" in argv:
        msg = _read_from_git()
    elif "--stdin" in argv:
        msg = sys.stdin.read()
    elif "--file" in argv:
        i = argv.index("--file")
        if i + 1 >= len(argv):
            sys.stderr.write("commit_lint: --file needs a path\n")
            return 2
        try:
            msg = open(argv[i + 1], encoding="utf-8").read()
        except OSError as e:
            sys.stderr.write(f"commit_lint: {e}\n")
            return 2
    else:
        # first non-flag arg is the message
        rest = [a for a in argv if not a.startswith("--")]
        if not rest:
            sys.stderr.write(
                "usage: commit_lint.py [MSG | --from-git | --stdin | --file PATH]\n"
            )
            return 2
        msg = " ".join(rest)

    ok, errors, warns = lint(msg)
    for w in warns:
        sys.stderr.write(f"  warn: {w}\n")
    if not ok:
        sys.stderr.write("commit_lint: INVALID commit message\n")
        for e in errors:
            sys.stderr.write(f"  error: {e}\n")
        return 1
    sys.stderr.write("commit_lint: OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
