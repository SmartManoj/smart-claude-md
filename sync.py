#!/usr/bin/env python3
"""Sync smart-claude-md into your global CLAUDE.md.

- Ensures `~/.claude/CLAUDE.md` imports this repo's CLAUDE.md via the
  native `@path` include (added once, idempotently).
- Pulls the latest rules from the repo so the import always sees fresh content.

Run:  python sync.py
"""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
REPO_CLAUDE_MD = REPO_DIR / "CLAUDE.md"
GLOBAL_CLAUDE_MD = Path.home() / ".claude" / "CLAUDE.md"

# Forward slashes work cross-platform in the @import path.
IMPORT_LINE = f"@{REPO_CLAUDE_MD.as_posix()}"
MARKER = "<!-- smart-claude-md (managed by sync.py) -->"


def pull() -> None:
    print(f"Pulling latest rules in {REPO_DIR} ...")
    subprocess.run(["git", "-C", str(REPO_DIR), "pull", "--ff-only"], check=False)


def ensure_import() -> None:
    GLOBAL_CLAUDE_MD.parent.mkdir(parents=True, exist_ok=True)
    text = GLOBAL_CLAUDE_MD.read_text(encoding="utf-8") if GLOBAL_CLAUDE_MD.exists() else ""

    if IMPORT_LINE in text:
        print(f"Import already present in {GLOBAL_CLAUDE_MD}")
        return

    block = f"\n{MARKER}\n{IMPORT_LINE}\n"
    GLOBAL_CLAUDE_MD.write_text(text.rstrip() + "\n" + block, encoding="utf-8")
    print(f"Added import to {GLOBAL_CLAUDE_MD}:\n  {IMPORT_LINE}")


if __name__ == "__main__":
    pull()
    ensure_import()
    print("Done.")
