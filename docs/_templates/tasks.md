---
status: draft
test: `<command that runs the whole test suite, without a browser>`
test(browser): `<browser part of the suite — delete this line if there is none>`
preflight(browser): `<command that exits 0 only when a browser can start — delete if no browser checks>`
commits: <filled on ship — sha..sha>
---

# `<Feature>` — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

- [ ] T1 `<task>` (AC1·AC2) — verify: `<command>`
- [ ] T2 `<task>` (AC3) — verify: `<command>`

A check that starts a browser (Playwright, browser-mode Vitest, Storybook tests) is marked
`verify(browser):`. It runs only when the run asks for browser checks. Otherwise
`implement` writes the code, leaves the box empty and adds a `deferred:` line. A later
browser run closes it:

- [ ] T3 `<task>` (AC4) — verify(browser): `<command>`
      deferred: browser @<sha> <date>

Only when no command can decide it — a person checks, and only a person closes it:

- [ ] `<task>` — verify(human): `<what to look at, and where>`
      reason: `<why this cannot be automated>`

Always last, never removed:

- [ ] Reconcile `docs/current_system/` with what shipped, and set `last_reconciled` in
      `overview.md` to the new HEAD — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs'`
