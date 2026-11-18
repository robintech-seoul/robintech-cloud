---
status: approved
---

# `site-generator`

**Role:** Builds every generated page from the data files. Without it the pages drift from the data.

**Source:** `scripts/build.py`, `scripts/cases.py`, `scripts/profiles.py`

## Public contract

| Entry point | Signature or route | Notes |
| --- | --- | --- |
| Build | `python3 scripts/build.py` | Writes `index.html`, `cases/index.html`, `cases/<slug>/index.html`, `profile/index.html`, `privacy/index.html`, `404.html` |
| Profile entry | `PROFILES` item: `slug, industry, name, title, summary, features[], palette[], status ('live'|'draft'), demo` | Only `live` items get a card; industries with no live profile show a "준비 중" tile |
| Industry list | `INDUSTRIES: [(key, label)]` | Filter chip order; a `live` profile whose `industry` is not listed stops the build |

## Internals

- The gallery embeds profile metadata as JSON in `<script id="pf-data">`; `main.js` reads it for the preview panel.
- A card uses `profile/<slug>/thumb.jpg` when it exists, else a palette-coloured fallback.

## Depends on

| Component | Used for |
| --- | --- |
| `profile-samples` | Existence of `thumb.jpg` at build time |
