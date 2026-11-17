---
status: approved
last_reconciled: 6a12639aeab41ffdda335c0ecfd6547f5ca42c93
---

# System Overview

RobinTech company homepage. A static site with no build tooling beyond one Python script,
served by GitHub Pages from `main` at the repository root.

## Components

| Component | Role (one line — what breaks without it) | Doc |
| --- | --- | --- |
| `site-generator` | Turns the data files into every generated page; without it the HTML goes out of date | `./site-generator/` |
| `site-assets` | Shared CSS and JS (header, filters, gallery preview viewer, GA events) for generated pages | `assets/` (no internals doc: one stylesheet, one script) |
| `profile-samples` | Hand-built, self-contained industry sample sites shown in the gallery | `./profile-samples/` |

## Interfaces

| From | To | Interface | Kind |
| --- | --- | --- | --- |
| `site-generator` | data files | `CASES: list[dict]` in `scripts/cases.py`; `INDUSTRIES: list[tuple[key, label]]`, `PROFILES: list[dict]` in `scripts/profiles.py` | function (import) |
| generated pages | `site-assets` | `assets/css/style.css`, `assets/js/main.js` (classes `pf-*`, ids `pf-grid`, `pf-viewer`, `pf-data`) | file |
| gallery (`profile/index.html`) | `profile-samples` | URL `profile/<slug>/` (loaded in an iframe and opened in a new tab), image `profile/<slug>/thumb.jpg` (16:10) | file / HTTP |
| `scripts/profile_thumb.py` | `profile-samples` | `python3 scripts/profile_thumb.py <slug>` writes `profile/<slug>/thumb.jpg` from `index.html` via headless Chrome | CLI |

## Layers

| Layer | Owns | Must not depend on |
| --- | --- | --- |
| Data (`scripts/cases.py`, `scripts/profiles.py`) | Content: cases, industries, profile metadata | HTML structure |
| Generator (`scripts/build.py`) | Page HTML, nav, footer, gallery markup | Anything inside `profile/<slug>/` |
| Assets (`assets/`) | Shared look and behaviour of generated pages | Sample sites |
| Samples (`profile/<slug>/`) | Their own HTML, CSS and design | `assets/`, the generator, other samples |

## Invariants

- Generated HTML is never edited by hand; after `python3 scripts/build.py` the working tree has no diff in generated files.
- `build.py` never writes inside `profile/<slug>/`.
- Each sample works when its folder is copied elsewhere on its own (relative paths, no shared site assets).
- Sample business names, addresses and phone numbers are fictional and marked as samples (`docs/profile-playbook.md`).
