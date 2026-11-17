# AGENTS.md

Behavioral rules for coding work. Biased toward caution over speed — use judgment
on trivial tasks. User instructions and existing authorization take precedence; do not
ask again for work already approved in the current conversation.

## 1. Think before coding
- State assumptions before implementing. If unsure, ask.
- Multiple valid readings? Present them. Never pick one silently.
- Confused? Stop and name the confusion. Don't proceed on a guess.
- If a simpler approach exists, say so. Push back instead of complying.

## 2. Simplicity first
- Minimum code that solves the stated problem. Nothing speculative.
- No abstraction for single-use code. No unrequested flexibility or config.
- No error handling for impossible states.
- Wrote 200 lines where 50 would do? Rewrite before showing it.

## 3. Surgical changes
- Every changed line must trace to the request. That is the test.
- Don't "improve" adjacent code, comments, or formatting.
- Match existing style even if you'd write it differently.
- Unrelated dead code: mention it, don't delete it.
- Delete only the imports and variables your own change orphaned.

## 4. Verify, don't assume
- Turn tasks into checkable goals: "fix the bug" → "write a failing repro test, then pass it".
- Multi-step work: state the plan as `step → verify:` pairs before starting.
- Not done until verification actually ran. "Looks right" is not evidence.
- Report failures with real output. Never claim a check passed that didn't run.

## 5. Docs layout

You are the primary reader of `docs/`. Keep it accurate or delete it — a stale doc is
worse than none. Skeletons live in `docs/_templates/`; copy them, don't invent a shape.

- `docs/current_system/` — what exists now, shaped by architecture rather than by the
  source tree. `overview.md` names the components, their roles, and the interfaces
  between them, and carries `last_reconciled: <sha>` in its frontmatter. One subfolder
  per component for internals. Nest deeper only where the contract isn't obvious from
  signatures and types.
- `docs/features/<YYYY-MM-DD>-<name>/` — one folder per planned change: `spec.md`,
  `system_design.md`, `tasks.md`, and `verify.md` when acceptance needs checks beyond
  the tasks' own. The date is when the folder was created, so a plain
  listing reads in the order features were started. Never rename it afterwards — commit
  messages point at this path. Ship date comes from the recorded commit range, not the
  folder name.
- `docs/verify.md` — optional. Criteria every feature's verdict must meet (lint, type
  checks, repository-wide rules), in the same format as a feature's `verify.md`.
- `docs/apis/` — generated OpenAPI. Never hand-edit. `current_system/` links here
  instead of listing endpoints.

Every doc opens with frontmatter carrying
`status: draft | approved | shipped | superseded-by: <path>`. Once shipped, `spec.md`
and `system_design.md` are history — supersede them, don't edit them.

## 6. Working a feature

1. Before designing, run `git diff --stat <last_reconciled>..HEAD`. Any output means
   `docs/current_system/` is stale — reconcile it first. If that folder is empty, this
   feature's `system_design.md` defines the initial architecture instead.
2. `system_design.md` is required only when the change crosses a component boundary,
   adds a component, alters an interface named in `current_system/`, or introduces a
   module boundary inside a component. Otherwise `spec.md` + `tasks.md` is enough.
   Say which case applies and why on the `Design:` line of the spec's Scope.
3. When required, `system_design.md` opens with the layer-by-layer delta to
   `current_system/`, before any rationale or implementation detail. When the trigger is
   an internal boundary, that delta is module-by-module inside the component and carries
   two tables, not one: what each module owns and must not depend on, and the interfaces
   between them with signatures. Direction alone hides cycles. Stop subdividing where the
   contract is obvious from signatures and types (§5).
4. Name the modules and the interfaces between them before writing tasks. A task that
   spans three modules means the decomposition has not happened yet.
5. Tasks carry their own check: `- [ ] <task> — verify: <command>`.
   Mark `[x]` only after that command ran and passed — not after writing the code.
   A check no command can decide is written `verify(human):` with a `reason:` line, and
   only a person closes it — `[x]` plus a `signed-off: <name> <date>` line, written by the
   person or, when the person asks, by the agent in that person's name. A fresh
   subagent reviews it first and records a `reviewed:` line; that opinion closes it only
   when the run was explicitly started in automatic mode. Criteria beyond the tasks go in
   `verify.md`: a backticked command, or plain words handled like `verify(human)`.
   A check that starts a browser is written `verify(browser):`, and the browser part of the
   suite goes in `test(browser):`. These run only when a person asks for browser checks.
   Until then the task stays `[ ]` with a `deferred:` line, and the verdict lists it.
   After approval, approved tasks, criteria and the `test:` command are not rewritten or
   removed — only added to. Changing them is a re-approval, and that belongs to a person.
6. Commit messages name the feature folder: `feature: docs/features/<YYYY-MM-DD>-<name>/`.
   A feature ships only on a PASS verdict. On ship, record the commit range in the feature's frontmatter as `commits: <sha>..<sha>`.
   One branch carries one feature. Its PR holds two commits: the squashed feature, whose message
   summarises the implementation, and a docs commit that points every recorded SHA at it.
   Merge it with a merge commit — squash and rebase merges change the SHAs again.
7. The final task of every feature is always: reconcile `docs/current_system/` with what
   shipped and set `last_reconciled` to the new HEAD. The feature is not done until
   that lands.

## 8. This repository

- RobinTech company homepage: a static site served by GitHub Pages from `main` (root).
  Pushing to `main` publishes it, so every change lands on a branch first.
- Generated pages (`index.html`, `cases/`, `profile/index.html`, `privacy/`, `404.html`) come
  from `scripts/build.py` and data files in `scripts/`. Edit the generator and data, never the
  generated HTML, then run `python3 scripts/build.py`.
- `profile/<slug>/` holds hand-built, self-contained industry sample sites. The generator never
  writes there. How to make one, and when it is done: `docs/profile-playbook.md`.
- Profile samples branch from and merge back into `feature/profile-gallery`
  (pass `base=feature/profile-gallery`) until that branch is merged to `main`.
- Check pages through a local server (`python3 -m http.server 8000`). Opened as `file://`, the
  gallery preview shows a directory listing instead of the sample.
