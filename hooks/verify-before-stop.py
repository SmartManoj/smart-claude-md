#!/usr/bin/env python3
"""Stop hook: require a green-tick (✅) rule-confirmation at the end of the reply.

The model self-certifies by ending its reply with ✅ ("I followed all rules").
This hook checks for that tick in the final assistant message:
  - tick present -> allow the stop (passes on the FIRST stop; no wasted loop).
  - tick missing -> block once, naming the rules, asking to re-affirm and add ✅.
  - tick still missing after one nag (stop_hook_active) -> allow with a warning,
    so a stubborn turn never hard-locks the session.
  - message unreadable -> fail OPEN (allow) with a warning; never lock up.

The final message is read from stdin's `last_assistant_message` when present,
falling back to parsing the transcript JSONL for older Claude Code versions.
"""
import json
import sys

TICK = "✅"


def last_assistant_text(path):
    """Fallback: most recent assistant message text from the transcript JSONL."""
    if not path:
        return None
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except Exception:
        return None
    for ln in reversed(lines):
        try:
            o = json.loads(ln)
        except Exception:
            continue
        if o.get("type") != "assistant":
            continue
        content = o.get("message", {}).get("content")
        if not isinstance(content, list):
            continue
        texts = [b.get("text", "") for b in content if b.get("type") == "text"]
        if texts:
            return "\n".join(texts)
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    # Prefer the message handed directly on stdin; fall back to the transcript.
    text = data.get("last_assistant_message")
    if text is None:
        text = last_assistant_text(data.get("transcript_path", ""))

    # Could not read the final message -> fail open (never hard-lock).
    if text is None:
        print(json.dumps({"systemMessage": "⚠️ Stop hook couldn't read the last message; skipped ✅ check."}))
        return

    # Complied: final reply carries the green tick.
    if TICK in text:
        return

    # Missing tick, but already nagged once this turn -> let it pass with a warning.
    if data.get("stop_hook_active"):
        print(json.dumps({"systemMessage": "⚠️ Finished without the ✅ rule-confirmation tick."}))
        return

    reason = (
        "Your reply is missing the ✅ rule-confirmation tick. Before finishing, confirm "
        "you followed every rule in SMART-CLAUDE.md (answer-first, don't-be-lazy, "
        "don't-assume — checked live state not memory — be-succinct), then end your "
        "reply with ✅. Re-send your reply ending with ✅."
    )
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    main()
