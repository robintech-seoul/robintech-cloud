---
status: draft
---

# `<Feature>` — System Design

Required only when this change crosses a component boundary, adds a component, alters
an interface named in `docs/current_system/overview.md`, or introduces a module boundary
inside a component. If none of those apply, delete
this file and say so in `spec.md`.

## Architecture delta

This section comes first, before any rationale. Per layer: what changes, what stays.

| Layer | Today | After | Why it must change |
| --- | --- | --- | --- |

Interfaces added, changed, or removed:

| From | To | Interface | Change |
| --- | --- | --- | --- |
| `<a>` | `<b>` | `<signature or route>` | new / changed / removed |

Components added or removed:

| Component | Change | Absorbs / replaces |
| --- | --- | --- |

When the trigger is a module boundary inside one component, the same tables apply one
level in — `From` and `To` are modules — plus what each of them owns:

| Module | Owns | Must not depend on |
| --- | --- | --- |

## Why this shape

Only decisions someone might reverse — one or two lines each: what was chosen, which
alternative was rejected and why. No evidence lists or "why this is safe" arguments;
review and tests check those. Do not restate the spec's problem or criteria.

## Implementation

Concrete enough to become tasks without further design. Name the files and functions.

## Risks and rollback

What breaks if this design is wrong, how it surfaces, and how it is backed out. One line
each. A "someone might later…" risk stays only if a concrete path exists and the failure
would be silent (billing, data, security, legal notices).
