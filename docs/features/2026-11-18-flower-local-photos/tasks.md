---
status: shipped
test: `python3 docs/features/2026-11-18-flower-local-photos/check_static.py all`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()" && python3 -c "import urllib.request as u; [u.urlopen(x, timeout=10) for x in ('https://fonts.googleapis.com/css2?family=Noto+Serif+KR', 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css')]; [u.urlopen(l.split()[-1], timeout=20) for l in open('profile/flower-bomgyeol/img/sources.txt') if l.strip()]"`
commits: b045fa1a02baa9986b2ca074a3572490c5a1a96e..408af13cfb6761c21a4ce4dc7b61a5cd16b24f31
---

# Flower sample photos stored in the repository (`flower-bomgyeol`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the `profile-samples` component (spec Scope, `Design: none`); there are no modules to
order. Every command runs from the repository root. The checks live next to this file:
`check_static.py <check>` (standard library, `git` and `sips`; no browser, no network) and
`check_browser.py page|gallery|compare` (Playwright driving the installed Google Chrome; it serves the
repository on a free local port itself). `page` and `gallery` need the network only for web fonts. `compare`
also needs `images.unsplash.com`: AC17 reads the served heights, and the "before" page still hotlinks Unsplash.
`preflight(browser)` checks Chrome, the font hosts and every download URL in `img/sources.txt`, so an Unsplash
outage or a removed photo shows as an environment problem, not a defect. "Merge-base" is `git merge-base HEAD main`, as in the spec.

`check_static.py` and `check_browser.py` are approved together with this file. Changing what they check
is a change to approved checks and goes back to a person for re-approval.

Known side effect (spec Scope Out): after this change the shipped food feature's
`check_static.py playbook` (its AC52) fails by design. No task here runs the food feature's checks.

- [x] T1 Download the nine photos and write `img/sources.txt`: fetch each merge-base `<img>` `src` exactly (no `Accept` header, so JPEG) into `profile/flower-bomgyeol/img/<descriptive name>.jpg`; re-encode a file over 500 KB at the same pixel size with `sips -s formatOptions <quality>`, using the highest quality that fits 500 KB; look up each photo's Unsplash page, and write `-` as its page URL when the page is not found or the lookup is refused (do not work around a refusal) (AC8·AC9·AC10·AC11·AC12·AC13·AC14·AC16·AC18) — verify: `python3 docs/features/2026-11-18-flower-local-photos/check_static.py photos`
- [x] T2 In `profile/flower-bomgyeol/index.html`, point each `<img>` `src` at its `img/` file and delete the `images.unsplash.com` preconnect line; change nothing else (AC4·AC5·AC6·AC7·AC15) — verify: `python3 docs/features/2026-11-18-flower-local-photos/check_static.py page`
- [x] T3 In `docs/profile-playbook.md` §3, delete the `flower-bomgyeol` exception line and add to the photo rule that the page URL is written `-` when the photo page cannot be found; the download URL is still required (AC26·AC28) — verify: `python3 docs/features/2026-11-18-flower-local-photos/check_static.py playbook`
- [x] T4 Keep the branch inside its scope: no file outside `profile/flower-bomgyeol/` and `docs/`, `style.css` and `thumb.jpg` untouched (AC1·AC2·AC3) — verify: `python3 docs/features/2026-11-18-flower-local-photos/check_static.py scope`
- [x] T5 Check the page in a browser: every image loads at 1440 and inside a `width:390px` iframe, and a load plus scroll to the end at 1440 requests only the local server and the font hosts (AC19·AC20·AC21) — verify(browser): `python3 docs/features/2026-11-18-flower-local-photos/check_browser.py page`
- [x] T6 Check the gallery: the flower card's thumbnail loads and the card opens the preview with the sample (AC22·AC23) — verify(browser): `python3 docs/features/2026-11-18-flower-local-photos/check_browser.py gallery`
- [x] T7 Compare with the merge-base: each local file's height equals the height its download URL serves; then the merge-base page (from `git show`, served from a temporary folder, still hotlinking Unsplash) and the branch page are shot full-page at 1440 and 390 once every image has loaded, both alike with reduced motion, transitions and smooth scrolling off, scrolled instantly to 0 and the fixed header pinned to the top in its unscrolled state; the run fails, and writes no screenshot for that page, if any image of either page does not load, and fails if any image's natural size differs between the two pages; it empties the shot folder first and writes `summary.txt` last (AC17·AC24·AC25) — verify(browser): `python3 docs/features/2026-11-18-flower-local-photos/check_browser.py compare`
- [ ] T8 Review the screenshots T7 wrote for visual sameness (AC24·AC25) — verify(human): open `/tmp/flower-local-photos-shots/`. First confirm `summary.txt` ends with `result PASS`, its `site tree` equals the output of `git rev-parse HEAD:profile/flower-bomgyeol` and its site working tree is `clean`; if not (or if the folder is missing because browser checks have not run), the evidence is missing and the review is UNSURE, not FAIL. `side-1440.png` and `side-390.png` put the merge-base page (left, "merge-base") next to the branch page (right, "branch"); `side-1440-NN.png` and `side-390-NN.png` are the same images cut into 1200 px tall bands, to read at full size; `before-*.png` and `after-*.png` are the single pages; `summary.txt` lists each page height and, per `<img>`, alt text, natural size, box size and position (the script already fails on a natural-size difference). At each width confirm, band by band: (1) the two page heights in `summary.txt` are equal; (2) the nine photos appear in the same order — hero ranunculus and protea, bronze-vase centrepiece, dahlia and rose bouquet, pink peony, white snapdragon, rose and chrysanthemum, purple hydrangea, purple flower before a grey wall, candle-lit long table; (3) each photo shows the same subject with the same crop and framing; (4) text, sections and spacing line up between the two sides, header included. Slight colour or detail differences from JPEG against AVIF/WebP are not a difference; visible blocking or banding, for example on the re-encoded hero, is
      reason: whether two renderings show the same photo with the same crop is a visual judgement; a pixel diff cannot decide it, because the merge-base page gets AVIF or WebP from Unsplash while the branch serves JPEG (spec Assumptions).
      scope: profile/flower-bomgyeol
      검토: PASS @408af13cfb6761c21a4ce4dc7b61a5cd16b24f31 #067662c4 2026-11-18 — summary.txt result PASS, site tree 2f9bd3c matches, clean; heights equal (1440: 5827/5827, 390: 6618/6618); all bands show the nine photos in the same order, crop and layout; full-size hero crops show no blocking or banding

Always last, never removed:

- [x] Reconcile `docs/current_system/` with what shipped (in `profile-samples/component.md`, the Depends on row says every sample keeps its photos in `img/` with `img/sources.txt`, and names no sample as an exception), and set `last_reconciled` in `overview.md` to the new HEAD (AC27) — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && python3 docs/features/2026-11-18-flower-local-photos/check_static.py current`
