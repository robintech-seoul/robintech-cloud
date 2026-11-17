---
status: shipped
test: `python3 docs/features/2026-11-17-profile-food/check_static.py all`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()" && python3 -c "import urllib.request as u; [u.urlopen(x, timeout=10) for x in ('https://fonts.googleapis.com/css2?family=Noto+Sans+KR', 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css')]"`
commits: 3c164d3f11879ff3315e24e5bb646b69e154c1c2..8c01a561b383b425feab6bd4f6bfb719ae55f024
---

# Restaurant · cafe profile sample (`food`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the existing `profile-samples` component (spec Scope, `Design: none`); there are no modules
to order. Every command runs from the repository root. The checks live next to this file:
`check_static.py <check>` (standard library and `sips`, no browser) and `check_browser.py page|gallery`
(Playwright driving the installed Google Chrome; it serves the repository on a free local port itself and needs the
network for web fonts, which `preflight(browser)` checks).
Fixed parameters of the checks: first screen is 1440×900 and 390×844; "visible" means inside the
viewport and not covered at its centre, judged 1.5 s after load (at each AC15 scroll position, within 1.5 s);
the 카카오톡 주문 button is a link or button whose accessible name matches `카카오톡.*주문`; a price is written
as digits plus 원 inside one text node (`\d[\d,]*\s?원`); its digits are judged by a probe appended to the
element that holds it (a `0123456789` span plus one span per character `0`–`9`, `i` and `M`, absolutely positioned
off-screen and removed afterwards, inheriting the element's font). The probe's main rendered font (CDP
`CSS.getPlatformFontsForNode`) must either be monospaced, meaning the twelve character spans have widths within
0.5 % of one another, or match Pretendard, a `KR` family, Nanum, Gowun, Gothic A1, Hahmlet,
Song Myung, Black Han Sans, Do Hyeon, Jua, Orbit, Sunflower, Gaegu, Dongle, Hi Melody, Gamja Flower,
Poor Story, Stylish, Yeon Sung, Gugi, Dokdo, Single Day, Cute Font, Kirang Haerang, Bagel Fat One or
Diphylleia (the Korean list); and every font request returns 200; AC17 reads the first `h2`–`h6` headings containing 메뉴, 영업시간 (or 영업 시간) and
오시는 길, the text between the menu and hours headings must contain 빵, 케이크, 음료 and a price, and the
text between the hours and directions headings must contain 휴무; an address is block text (`<br>` and links do not
split it) matching `<한글>로|길 <번호>`, where the word before 로 does not end in 으 and the number is not
followed by a letter, digit, `%`, `~`, `:`, `.`, `-`, `,<digit>` or a counter word (원, 분, 시, 개, 인, 일, 명, 번); AC53 reads the §3 `**글꼴:**` bullet with its wrapped lines, whitespace collapsed: it must contain
가격, 한글 서체 and 모노 (or 고정폭), and must not contain `숫자는 한글 서체로`.

`check_static.py` and `check_browser.py` are approved together with this file. Changing what they check
is a change to approved checks and goes back to a person for re-approval.

- [x] T1 Re-run the shop-name web search for 새벽밀 with 빵집, 베이커리 and 카페 (Naver too if reachable) and record it in `docs/features/2026-11-17-profile-food/name-check.txt` as `query: <query>` lines, the hits, and `verdict: no match` or `verdict: match <shop>`; on a match stop and ask for a new name (AC11) — verify: `python3 docs/features/2026-11-17-profile-food/check_static.py name`
- [x] T2 Pick photos: gather free Unsplash (not Unsplash+) and Pexels candidates, compare them on a contact sheet made in the scratchpad (not committed), download the picks at web size into `profile/food-saebyeokmil/img/` and write `img/sources.txt` (AC21·AC22·AC44·AC45·AC46·AC47·AC48·AC49) — verify: `python3 docs/features/2026-11-17-profile-food/check_static.py photos`
- [x] T3 Write `index.html` and `style.css` with the sample markers, noindex, footer credits, and fictional address, phone and registration number (AC7 text·AC8·AC9·AC10·AC12·AC13) — verify: `python3 docs/features/2026-11-17-profile-food/check_static.py markers`
- [x] T4 Build the content and customer flow: menu with prices, then 영업시간 with 휴무, then 오시는 길; 카카오톡 주문, 네이버 예약, 네이버 지도 and 전화 as `href="#"` links; alt text, one `h1`, no skipped heading level, `word-break: keep-all` (AC16·AC17·AC23·AC24·AC25·AC26·AC27·AC28·AC29) — verify: `python3 docs/features/2026-11-17-profile-food/check_static.py flow`
- [x] T5 Keep the sample self-contained: relative paths only, photos from `img/`, fonts only from Google Fonts and Pretendard on jsDelivr, no other `http(s)://` URL in either file (so inline SVG without `xmlns`, no data-URI SVG, no JSON-LD, photo credits as plain text), nothing from Tartine (AC1·AC2·AC18·AC20·AC39·AC42·AC43) — verify: `python3 docs/features/2026-11-17-profile-food/check_static.py assets`
- [x] T6 Register the sample: add the `PROFILES` entry, run `python3 scripts/profile_thumb.py food-saebyeokmil`, regenerate the gallery (AC1·AC3·AC4·AC5) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-17-profile-food/check_static.py register`
- [x] T7 Check the page in a browser at 1440 and 390: sample notice on the first screen, 카카오톡 주문 on the first screen and at every scroll position at 390, computed `keep-all` on Korean text, price digits in a Korean or monospaced font, no motion under reduced motion, no horizontal overflow (390 inside a `width:390px` iframe); also writes the full-page screenshots for T11 to `/tmp/profile-food-shots/` (AC7·AC14·AC15·AC16·AC19·AC30·AC31·AC32) — verify(browser): `python3 docs/features/2026-11-17-profile-food/check_browser.py page`
- [x] T8 Check the gallery: food filter shows the card and no 준비 중 tile, card opens the preview with the sample, desktop/mobile buttons switch the width, Esc closes (AC35·AC36·AC37·AC38) — verify(browser): `python3 docs/features/2026-11-17-profile-food/check_browser.py gallery`
- [x] T9 Update `docs/profile-playbook.md` §3: the photo rule (download into `profile/<slug>/img/`, relative path, no `images.unsplash.com` hotlink), the folder rule (`img/`, `img/sources.txt`), a line saying `profile/flower-bomgyeol/` still links its photos directly (직접 링크) until its follow-up feature, and the font rule's last sentence reworded to "영문 세리프는 숫자가 들쭉날쭉한 서체가 있으니 가격 · 숫자는 숫자 폭이 고른 서체(한글 서체나 모노 서체)로." (AC50·AC51·AC52·AC53) — verify: `python3 docs/features/2026-11-17-profile-food/check_static.py playbook`
- [x] T10 Keep the branch inside its scope (AC6) — verify: `base="$(git merge-base feature/profile-gallery HEAD)" && test -n "$base" && test -z "$(git diff --name-only "$base" | grep -v -e '^profile/food-saebyeokmil/' -e '^profile/index\.html$' -e '^scripts/profiles\.py$' -e '^docs/')"`
- [x] T11 Review the full-page screenshots for overlapping or clipped text (AC33·AC34) — verify(human): run `python3 docs/features/2026-11-17-profile-food/check_browser.py page`, then look at `/tmp/profile-food-shots/desktop-1440.png` and `/tmp/profile-food-shots/mobile-390.png` top to bottom
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page; no command decides it reliably.
      검토: PASS @c07c9b3eb3e56bb17916950d1ca9a3997b570cae #aeea9950 2026-11-18 — check_browser.py page 재실행(PASS) 뒤 1440x5991·390x9018 전체를 구간별로 봄, 겹치거나 잘린 글자 없음 (모바일 고정 바는 사진만 덮음)
      확인: Seokhyun Kim 2026-11-18
- [x] T12 Compare the sample side by side with tartinebakery.com and with `profile/flower-bomgyeol/` (AC39·AC40·AC41) — verify(human): open `http://localhost:8000/profile/food-saebyeokmil/` (after `python3 -m http.server 8000`) next to https://www.tartinebakery.com and `http://localhost:8000/profile/flower-bomgyeol/`; confirm no shared text, logo, name or photo with Tartine, that it does not read as the same site as Tartine, and that it does not read as the same design as flower-bomgyeol
      reason: "reads as the same site / design" and copied logo or wording are taste judgements a person makes.
      검토: PASS @c07c9b3eb3e56bb17916950d1ca9a3997b570cae #fe77ea58 2026-11-18 — Tartine 문구 grep 일치 없음·자체 SVG 로고·사진 dHash 최소 100+/256; 히어로 구조·서체·강조색이 Tartine·flower-bomgyeol 과 다름
      확인: Seokhyun Kim 2026-11-18

Always last, never removed:

- [x] Reconcile `docs/current_system/` with what shipped (in `profile-samples/component.md`, the Source line lists `food-saebyeokmil` and the Depends on row says samples keep their photos in `img/`, with `flower-bomgyeol` still hotlinking Unsplash), and set `last_reconciled` in `overview.md` to the new HEAD — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && grep -q 'food-saebyeokmil' docs/current_system/profile-samples/component.md && grep -q 'img/' docs/current_system/profile-samples/component.md`
