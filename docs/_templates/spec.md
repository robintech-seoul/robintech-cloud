---
status: draft
approved_at: <commit that holds the approved documents — filled on approval>
---

# `<Feature>`

## Problem

What is broken or missing today, and for whom. No solution in this section.

## Scope

One line per item — what is built. Conditions, exceptions and values belong in the acceptance
criteria, not here.

- **In:**
- **Out:**
- **Design:** which §6-2 trigger applies and so whether `system_design.md` is written — or
  "none" and why.

## Acceptance criteria

Observable and checkable from outside the system. One line each. Each one is checked by
a task's `verify:` in `tasks.md` or, when no task checks all of it, by a criterion in
`verify.md`; both refer to it as `(ACn)`. Once the tasks exist, say so here if they cover
every item. Number them; tasks refer to the number instead of restating the criterion.

- [ ] AC1 `<criterion>`

## Assumptions

What this spec takes as given without having checked it — one line each. Approving the spec
approves these; if one turns out false, the spec goes back for re-approval. An empty section
is a valid answer.

## Open questions

Blocking ones only — questions that change the design if answered differently. An empty
section is a valid and common answer.
