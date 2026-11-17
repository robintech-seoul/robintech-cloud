---
status: draft
last_reconciled: <git sha of the commit this was last checked against>
---

# System Overview

Top layer only. Names components and the contracts between them. Internals belong in
`./<component>/`, endpoint details in `docs/apis/`.

## Components

| Component | Role (one line — what breaks without it) | Doc |
| --- | --- | --- |
| `<name>` | | `./<name>/` |

## Interfaces

One row per contract that crosses a component boundary. Anything not listed here is an
implementation detail that callers must not depend on.

| From | To | Interface | Kind |
| --- | --- | --- | --- |
| `<a>` | `<b>` | `<function signature or route>` | function / HTTP / event / queue |

HTTP routes are named here but specified in `docs/apis/`. Do not duplicate the schema.

## Layers

Top to bottom. For each: what it owns, and what it is not allowed to know about.

| Layer | Owns | Must not depend on |
| --- | --- | --- |

## Invariants

System-wide rules that any change must preserve. Delete the section if there are none
yet — an empty promise is worse than no promise.
