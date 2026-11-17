# `<Feature>` — Verification

What must hold before this feature ships, beyond each task's own `verify:` in `tasks.md`
and the `test:` suite. `robintech-dev:verify` checks every item here on every run and
returns the PASS/FAIL that automation reads. The same format in `docs/verify.md` applies
to every feature in the repository.

Anyone may add a criterion at any time — adding one only makes the verdict stricter. After
approval (`approved_at` in `spec.md`), nobody rewrites or removes one: that changes what
was approved, and it goes back to a person for re-approval.

Name the acceptance criteria an item checks as `(ACn)`, the way tasks do.

An item with a backticked command is run on every verdict; exit 0 passes and the box is
not used:

- [ ] `<criterion>` (AC3) — verify: `<command>`

A command that starts a browser is marked `verify(browser):` and runs only in a browser run.
In `docs/verify.md`, a `browser_match: <regex>` frontmatter line names this repository's own
browser commands (for example `--project layout`), so design catches them unmarked.

Any other item is a criterion in plain words. A fresh subagent reviews it and records its
opinion under the item; a person closes it with `[x]` and a `signed-off: <name> <date>`
line inside the item (indented like the rest of it) — or asks the agent to write it for them.
In automatic mode (`--auto`) the subagent's current PASS closes it instead. Say what
must be true and where to look. List the sub-items to check ("loading, error and empty
states; success, validation error and server error per action") instead of "every …" —
an open criterion lets each fresh reviewer find a different gap. A `scope:` line lists the files the review reads, from the
repository root (paths inside `docs/` too); the review goes stale only when one of them
changes. Without it, any change outside `docs/` stales the review:

- [ ] `<what must be true>` (AC4) — `<where to look>`
      scope: `<path>`, `<path>`
