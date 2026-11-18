---
status: shipped
approved_at: a9f9f246fef30eacf7a90b34aa97f105fe2eb88e
commits: a9f9f246fef30eacf7a90b34aa97f105fe2eb88e..bf5d250c8b12d92caa5933ef84ecf7809ec46879
---

# Flower sample photos stored in the repository (`flower-bomgyeol`)

## Problem

The flower sample `profile/flower-bomgyeol/` loads its nine photos straight from `images.unsplash.com`.
If Unsplash removes a photo, changes its CDN or is slow, the sample in the gallery breaks or loads
slowly, and the sample cannot be copied to a customer's domain as a self-contained folder. It is the
only sample left that breaks the playbook photo rule (photos in `profile/<slug>/img/` with
`img/sources.txt`). The playbook carries an exception line for it, and `current_system` records it as a
hotlink. The human (Seokhyun Kim) asked for this follow-up on 2026-11-17.

## Scope

- **In:** The nine photos the flower page uses today, downloaded into `profile/flower-bomgyeol/img/` and referenced by relative path.
- **In:** `profile/flower-bomgyeol/img/sources.txt`, recording where each photo came from.
- **In:** `profile/flower-bomgyeol/index.html`: the nine `<img>` `src` values and the removal of the `images.unsplash.com` preconnect line. Nothing else changes.
- **In:** `docs/profile-playbook.md` §3: remove the line that exempts `flower-bomgyeol` from the photo rule, and say that the page URL in `img/sources.txt` may be `-` when the photo page cannot be found.
- **In:** Reconcile `docs/current_system/` (the "Depends on" photo row in `profile-samples/component.md`) and set `last_reconciled`.
- **Out:** Any visual change: other photos, other crops, layout, text or CSS. This is a hosting change, not a redesign (orchestrator decision).
- **Out:** `profile/flower-bomgyeol/style.css` and `thumb.jpg`. The look does not change, so the thumbnail is not regenerated.
- **Out:** `scripts/`, `assets/`, the generated pages (`profile/index.html` included) and `profile/food-saebyeokmil/`.
- **Out:** Self-hosting fonts. Google Fonts and Pretendard on jsDelivr stay allowed.
- **Out:** Editing the shipped `docs/features/2026-11-17-profile-food/` docs and checks. After this change its `check_static.py playbook` (food AC52) fails by design, and its AC22 check no longer finds photo IDs in the flower HTML; AC18 here takes over that check.
- **Design:** none. Trigger 1 (crosses a component boundary): no. Every changed file is inside the `profile-samples` component or in `docs/`. Trigger 2 (adds a component): no. Trigger 3 (alters a named interface): no. The interfaces named in `current_system/overview.md` (URL `profile/<slug>/`, `thumb.jpg`, the `profile_thumb.py` CLI) stay the same. The "Depends on" row in `component.md` documents an external host, not an interface between components. `img/` and `img/sources.txt` are files inside the self-contained folder that no other component reads, as in `food-saebyeokmil`. Trigger 4 (internal module boundary): no. The sample stays one page, one stylesheet and its images. So `spec.md` + `tasks.md` are enough.

## Acceptance criteria

"Merge-base" below means `git merge-base HEAD main` (today `b045fa1`).

Scope of the change

- [ ] AC1 Compared with the merge-base, the branch changes no file outside `profile/flower-bomgyeol/` and `docs/`.
- [ ] AC2 `profile/flower-bomgyeol/style.css` is byte-identical to its merge-base version.
- [ ] AC3 `profile/flower-bomgyeol/thumb.jpg` is byte-identical to its merge-base version.
- [ ] AC4 `profile/flower-bomgyeol/index.html` equals its merge-base version once both are normalised: the `<link rel="preconnect" href="https://images.unsplash.com">` line removed and every `<img>` `src` value replaced by one placeholder.

No remote photos

- [ ] AC5 `index.html` and `style.css` contain no `http://` or `https://` URL whose host is not `fonts.googleapis.com`, `fonts.gstatic.com` or `cdn.jsdelivr.net`.
- [ ] AC6 Every `<img>` `src` in `index.html` is a relative path `img/<file>` that resolves to an existing file in `profile/flower-bomgyeol/img/`.
- [ ] AC7 Every image file in `img/` is referenced by at least one `<img>` in `index.html`.

Photo files and budget

- [ ] AC8 Every file in `img/` other than `sources.txt` is a JPEG named `.jpg` or a WebP named `.webp`, judged by its content.
- [ ] AC9 No image in `img/` is wider than 2000 px.
- [ ] AC10 No image file in `img/` is larger than 500 KB.
- [ ] AC11 The image files in `img/` total at most 3 MB (`thumb.jpg` is not counted).

Source record

- [ ] AC12 `img/sources.txt` has exactly one line per image file in `img/` (dotfiles aside), written `<file> <page URL> <download URL>`, and each page URL either starts with `https://unsplash.com/photos/` or is `-`.
- [ ] AC13 Every download URL in `img/sources.txt` starts with `https://images.unsplash.com/photo-`.
- [ ] AC14 No line of `img/sources.txt` contains `plus.unsplash.com` or `premium_photo`.

Same photos, same crops

- [ ] AC15 For each `<img>` in the merge-base `index.html`, the `<img>` at the same position now references a file whose download URL in `img/sources.txt` equals that merge-base `src` exactly, query string included.
- [ ] AC16 Each image file's pixel width equals the `w=` value of its download URL in `img/sources.txt`.
- [ ] AC17 Each image file's pixel height equals the height of the image its download URL serves (needs network).
- [ ] AC18 No photo ID in `profile/flower-bomgyeol/img/sources.txt` appears in `profile/food-saebyeokmil/img/sources.txt`.

Page in the browser (served over HTTP on a local port by the check)

- [ ] AC19 At 1440 px width, every `<img>` on the page finishes loading with a non-zero natural width (browser).
- [ ] AC20 At 390 px width (page inside a `width:390px` iframe), every `<img>` on the page finishes loading with a non-zero natural width (browser).
- [ ] AC21 Loading the page and scrolling it to the end at 1440 px requests nothing from any host other than the local server, `fonts.googleapis.com`, `fonts.gstatic.com` and `cdn.jsdelivr.net` (browser).
- [ ] AC22 On `/profile/`, the `flower` card's thumbnail image loads with a non-zero natural width (browser).
- [ ] AC23 Clicking the `flower` card opens the preview with the sample loaded in the iframe (browser).

Looks the same

- [ ] AC24 Full-page screenshots at 1440 px of the merge-base page and the branch page, side by side, show the same photos, crops and layout (browser, review).
- [ ] AC25 Full-page screenshots at 390 px of the merge-base page and the branch page, side by side, show the same photos, crops and layout (browser, review).

Docs

- [ ] AC26 `docs/profile-playbook.md` no longer says that `profile/flower-bomgyeol/` links its photos directly (the §3 exception line is gone).
- [ ] AC27 `docs/current_system/profile-samples/component.md` no longer says that `flower-bomgyeol` hotlinks Unsplash.
- [ ] AC28 The photo rule in `docs/profile-playbook.md` §3 (the `**사진:**` item) says the page URL may be `-` when the photo page cannot be found.

Every AC is checked by a `verify` in `tasks.md`; there is no `verify.md`.

## Assumptions

- The page uses nine photos: nine `<img>` tags with nine distinct `images.unsplash.com` URLs, plus one bare `images.unsplash.com` preconnect (ten unique URLs in all). `style.css` has no image URL. None is an Unsplash+ (`plus.unsplash.com`, `premium_photo`) photo.
- **Page URL not found (human decision, Seokhyun Kim 2026-11-18):** the photo is kept and its `sources.txt` page URL is written `-` (AC12). The page slug is not derivable from the CDN ID (`photo-<digits>-<hex>`), so a lookup can fail. The download URL stays mandatory (AC13, AC15).
- Each file is downloaded from exactly the URL the page uses today (same `w`, `q`, `fit=crop`, `crop=top`), so the pixel size and crop match. Without an `Accept: image/avif` or `image/webp` header, `auto=format` returns a JPEG, saved as `.jpg`.
- The photo budget stays as the human set it for food: at most 2000 px wide, 500 KB per file, 3 MB in total. The nine requested widths (2000, 1400 ×2, 1200 ×2, 800 ×4) fit 2000 px. If a file exceeds 500 KB (most likely the 2000 px hero), it is re-encoded at the same pixel size with the highest JPEG quality that fits. It is not resized or swapped. Its download URL stays the URL it came from.
- Visual sameness is judged from before and after screenshots (AC24, AC25), as food did for AC33–AC34. A pixel diff is not used: the merge-base baseline needs live Unsplash, and Chrome receives AVIF or WebP from `auto=format` while the saved file is JPEG, so a tolerance would be a guess.
- **Review closes AC24 and AC25 (human decision, Seokhyun Kim 2026-11-18):** this run is automatic, so a fresh subagent's review PASS closes them in an `--auto` verdict.
- `thumb.jpg` is kept as it is. It is a static screenshot, and the page should look the same, so regenerating it would only change bytes.
- File names describe the photo (for example `hero-ranunculus.jpg`), as in `food-saebyeokmil/img/`.
- The footer credit "Photos: Unsplash" stays as it is (AC4). All photos are from Unsplash.

## Open questions
