#!/usr/bin/env python3
"""Sync smart-claude-md into your global CLAUDE.md.

- Ensures `~/.claude/CLAUDE.md` imports this repo's rules via the native
  `@path` include (added once, idempotently).
- Pulls the latest rules from the repo so the import always sees fresh content.

Run:
  python sync.py            # pull + ensure the import line
  python sync.py --install  # also install login auto-sync + the ✅ Stop hook
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
REPO_CLAUDE_MD = REPO_DIR / "SMART-CLAUDE.md"
GLOBAL_CLAUDE_MD = Path.home() / ".claude" / "CLAUDE.md"
STARTUP_VBS_NAME = "smart-claude-md-sync.vbs"
REPO_HOOK = REPO_DIR / "hooks" / "verify-before-stop.py"
HOOKS_DIR = Path.home() / ".claude" / "hooks"
HOOK_DEST = HOOKS_DIR / "verify-before-stop.py"
SETTINGS_JSON = Path.home() / ".claude" / "settings.json"

# Forward slashes work cross-platform in the @import path.
IMPORT_LINE = f"@{REPO_CLAUDE_MD.as_posix()}"


def pull() -> None:
    print(f"Pulling latest rules in {REPO_DIR} ...")
    subprocess.run(["git", "-C", str(REPO_DIR), "pull", "--ff-only"], check=False)


def ensure_import() -> None:
    GLOBAL_CLAUDE_MD.parent.mkdir(parents=True, exist_ok=True)
    text = GLOBAL_CLAUDE_MD.read_text(encoding="utf-8") if GLOBAL_CLAUDE_MD.exists() else ""

    if IMPORT_LINE in text:
        print(f"Import already present in {GLOBAL_CLAUDE_MD}")
        return

    GLOBAL_CLAUDE_MD.write_text(text.rstrip() + "\n" + IMPORT_LINE + "\n", encoding="utf-8")
    print(f"Added import to {GLOBAL_CLAUDE_MD}:\n  {IMPORT_LINE}")


def install() -> None:
    """Install a silent login auto-sync (this script) into the OS startup."""
    if sys.platform != "win32":
        print("--install supports Windows (Startup folder) only.")
        print("On macOS/Linux, add a cron entry instead (see README).")
        return

    appdata = os.environ.get("APPDATA")
    if not appdata:
        print("Could not locate the Startup folder (%APPDATA% is unset).")
        return

    startup_dir = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    startup_dir.mkdir(parents=True, exist_ok=True)

    py = sys.executable or "python"
    script = Path(__file__).resolve()
    # VBS launches python with a hidden window (0) so login stays flash-free.
    # Double-quotes are doubled to escape them inside the VBS string literal.
    vbs = (
        "' Silently sync smart-claude-md at login (no console window).\n"
        f'CreateObject("WScript.Shell").Run """{py}"" ""{script}""", 0, False\n'
    )
    target = startup_dir / STARTUP_VBS_NAME
    target.write_text(vbs, encoding="utf-8")
    print(f"Installed login auto-sync: {target}")


def install_hook() -> None:
    """Copy the Stop hook into ~/.claude/hooks and wire it into settings.json."""
    if not REPO_HOOK.exists():
        print(f"Hook source not found: {REPO_HOOK}")
        return

    HOOKS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO_HOOK, HOOK_DEST)
    print(f"Installed Stop hook: {HOOK_DEST}")

    settings = {}
    if SETTINGS_JSON.exists():
        try:
            settings = json.loads(SETTINGS_JSON.read_text(encoding="utf-8"))
        except Exception:
            print(f"Could not parse {SETTINGS_JSON}; skipping hook wiring.")
            return

    stop = settings.setdefault("hooks", {}).setdefault("Stop", [])
    for group in stop:
        for h in group.get("hooks", []):
            if "verify-before-stop.py" in h.get("command", ""):
                print("Stop hook already wired in settings.json")
                return

    py = sys.executable or "python"
    stop.append({
        "matcher": "",
        "hooks": [{
            "type": "command",
            "shell": "bash",
            "command": f'"{py}" "{HOOK_DEST.as_posix()}"',
            "statusMessage": "Checking ✅ rule-confirmation...",
        }],
    })
    SETTINGS_JSON.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("Wired Stop hook into settings.json")


if __name__ == "__main__":
    if "--install" in sys.argv[1:]:
        install()
        install_hook()
    pull()
    ensure_import()
    print("Done.")
