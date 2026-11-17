---
status: approved
---

# `profile-samples`

**Role:** The industry sample sites the gallery shows. Without them the gallery has nothing to preview.

**Source:** `profile/<slug>/` (currently `flower-bomgyeol`)

## Public contract

| Entry point | Signature or route | Notes |
| --- | --- | --- |
| Page | `profile/<slug>/index.html` | Self-contained; own `style.css`; works inside the gallery iframe and on its own |
| Thumbnail | `profile/<slug>/thumb.jpg` | 1200px wide, 16:10, made by `scripts/profile_thumb.py` |

## Internals

How a sample is researched, built and checked: `docs/profile-playbook.md`.

## Depends on

| Component | Used for |
| --- | --- |
| (none) | Samples load only Google Fonts, Pretendard (jsDelivr) and free-licence photos |
