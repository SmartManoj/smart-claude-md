# Guideline — adding a new rule

These rules load into context **every session** (via the `@import` in your global
`CLAUDE.md`), so every word is a recurring token cost. Keep each rule cheap and sharp.

## Checklist for a new rule

1. **One sentence.** If it needs two, the second is usually a restatement — cut it.
2. **Name a trigger.** State *when* the rule fires (e.g. "when a tool fails", "when
   the user's meaning is unclear"). A rule with no trigger ("don't assume",
   "be careful") is a platitude — it's true always, so it changes nothing.
3. **Name the action.** Say what to *do*, not just what to avoid.
4. **State priority when options compete.** If two actions apply, rank them
   ("check first, ask only if you can't") instead of listing them as equals.
5. **Plain English.** No literary or abstract phrasing — write it the way you'd
   say it out loud.
6. **Portable.** Phrase as "the user", project-agnostic — no personal handles, no
   repo-specific details, so it copies verbatim into any project.

## Format

```
N. **Short title.** When <trigger>, <action>.
```

The title alone should carry the gist; the clause adds the trigger/action only if
it isn't already obvious from the title.

## Before you commit

- Does it overlap an existing rule? Merge instead of adding.
- Could it be one word shorter? It loads every session — trim.
- Does it earn its place, or is it advice you'd follow anyway without being told?
