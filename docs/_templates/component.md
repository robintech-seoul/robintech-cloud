---
status: draft
---

# `<Component>`

**Role:** one sentence. What breaks if this is removed.

**Source:** `<path/to/source>`

## Public contract

What callers may depend on. Everything not listed is free to change without notice.

| Entry point | Signature or route | Notes |
| --- | --- | --- |

## Internals

Only what a caller cannot infer from the contract above: invariants, ordering
requirements, concurrency assumptions, and why a boundary sits where it does. If the
signature and types already say it, leave it out.

## Depends on

| Component | Used for |
| --- | --- |

## Modules

The same judgment as `overview.md`, one level in. Fill this only once the component holds
more than one module; leave it out while the layering is already obvious from the source
tree.

| Module | Owns | Must not depend on |
| --- | --- | --- |

Interfaces between them. Signatures, not just direction — direction alone hides cycles.

| From | To | Interface |
| --- | --- | --- |

## Sub-components

Add a subfolder here only where a sub-part has its own contract that is not obvious
from signatures and types. Otherwise stop at this level.
