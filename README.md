# smart-claude-md

Plain-English, **universal** rules for [Claude Code](https://code.claude.com) — the ones the popular CLAUDE.md repos don't quite give you.

## Why this exists

Most shared CLAUDE.md rule sets fall into one of two gaps:

- **Personalized, not portable** — e.g. the widely-shared "Working with Q" protocol phrases rules as *"when Q asks a question…"*, where `Q` is the author's personal handle. You can't copy it verbatim.
- **Dense, not plain** — other template repos are written in jargon-heavy prose that's hard to read and adapt.

This repo keeps every rule **one sentence, plain English, phrased as "the user," and portable to any project.**

## The rules

See [`CLAUDE.md`](./CLAUDE.md). Currently:

1. **Answer first.** When the user asks a question, answer it first — give the reason — before taking any action or calling a tool.

## Usage

Append a rule to your global config (applies to every project):

```
~/.claude/CLAUDE.md      # macOS / Linux
%USERPROFILE%\.claude\CLAUDE.md   # Windows
```

…or to a project-level `CLAUDE.md` in the repo root.

## Background

The "answer the question before acting" behavior is a recognized one. In
[anthropics/claude-code#742](https://github.com/anthropics/claude-code/issues/742)
("Claude Doesn't Follow Instructions"), Anthropic noted model-level improvements
are "expected over time" and recommended **explicit prompting** as the practical
mitigation — which is exactly what these rules are.

### Prior art / credit

- [ctoth — "Working with Q" global CLAUDE.md gist](https://gist.github.com/ctoth/d8e629209ff1d9748185b9830fa4e79f) — the canonical (personalized) phrasing of "think before tool use."
- [abhishekray07/claude-md-templates](https://github.com/abhishekray07/claude-md-templates) — CLAUDE.md template collection.
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — the main curated hub.

## Contributing

Found a Claude behavior worth correcting? Open a PR adding one rule. Keep it: one sentence, plain English, "the user" phrasing, project-agnostic.

## License

MIT
