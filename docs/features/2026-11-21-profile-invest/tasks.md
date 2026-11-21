---
status: shipped
test: `python3 docs/features/2026-11-21-profile-invest/check_static.py all`
test(browser): `python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robinfamilyoffice; a=$?; python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robinwealth; b=$?; python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robincapital; c=$?; python3 docs/features/2026-11-21-profile-invest/check_browser.py thumb invest-robinfamilyoffice; d=$?; python3 docs/features/2026-11-21-profile-invest/check_browser.py thumb invest-robinwealth; e=$?; python3 docs/features/2026-11-21-profile-invest/check_browser.py thumb invest-robincapital; f=$?; python3 docs/features/2026-11-21-profile-invest/check_browser.py gallery; g=$?; python3 docs/features/2026-11-21-profile-invest/check_browser.py trio; h=$?; exit $((a|b|c|d|e|f|g|h))`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()" && python3 -c "import urllib.request as u; [u.urlopen(x, timeout=10) for x in ('https://fonts.googleapis.com/css2?family=Grandiflora+One', 'https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700', 'https://fonts.googleapis.com/css2?family=Orbit', 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css')]"`
commits: 01f250696cc63764cf0772f437f8020dbd04ac1d..efd70d310d6e5213d65ba08a327acecc74455476
---

# Invest profile samples (`invest`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the existing `profile-samples` component (spec Scope, `Design: none`). There are no modules to
order. The tasks go sample by sample: B `invest-robinfamilyoffice`, then C `invest-robinwealth`, then D
`invest-robincapital`. Registration, the gallery and the branch come after them. Every command runs from the
repository root. A task names one sample. The tasks of "Gallery, the three together and the branch" check what the
three samples share (the gallery, AC19, AC103, AC104, AC109, AC110, AC241–AC251), so they name all three.

The checks live next to this file and were written with it, before any sample exists; until then they fail:

- `check_static.py <check> [<slug>]`: standard library and `sips`; no browser, no network. Without `<slug>`, a
  per-sample check runs for all three samples. `all` takes about 0.3 s.
- `check_browser.py page <slug> | thumb <slug> | gallery | trio | compare`: Playwright driving the installed Google
  Chrome. It serves the repository on a free local port itself and stops the server when it ends (never `file://`,
  playbook §4). It prints its verdict and exits without waiting for Chrome to close (the Playwright driver ends
  Chrome), and fails a run that has no verdict after 900 s. One `page` run takes about 22 s; the eight commands of
  `test(browser)` took 90 s together on the fixture, and `compare` 136 s. It needs the network for web fonts, which `preflight(browser)`
  checks. `compare` is not a check: it saves first-screen shots and side-by-side sheets for the reviews below.

`check_static.py` and `check_browser.py` are approved together with this file. Changing what they check is a change
to approved checks and goes back to a person for re-approval. The Picks are approved with it too.

## Picks (agent decisions)

Names, slugs, palettes, faces and card titles are spec AC128, AC168, AC204 and A6, A8, A13. Copy is written in the
implement stage and obeys AC52–AC84 and the per-sample lists.

Headlines. AC144, AC158, AC183, AC193, AC218 and AC247 are decided by the length of the copy, so the `<h1>` texts are
fixed here:

- **B:** `<span>가족의 자산을 서두르지 않고 살핍니다. 목표와 사정을 먼저 듣고, 그 뒤에 맞는 길을</span><em>함께 찾습니다</em>`
  (the `<span>` runs three lines at 1440 and at 390; the `<em>` is one line at both).
- **C:** `<span>자산의 방향을</span><span>삶의 목표와 사정에 맞추어</span><span>함께 정합니다</span>` (each `<span>` is one line
  at 1440 and at 390).
- **D:** `오래 일군 사업을 책임 있게 이어받습니다` (one line at 1440, two at 390).

Section headings (`<h2>`) and order, below the first screen (spec A11):

- **B:** 하는 일 (three columns); 일하는 방식; 상담 문의.
- **C:** the statement (a `<p class="statement">`, no heading); 하는 일 (a list); 상담 과정; 상담 문의.
- **D:** 투자 분야 (tags and cards, on the sheet); 투자 방식 (on the sheet); 기업 문의 (the pale closing section).

Bars (spec A9):

- **B:** the first element of `<body>` is the strip: one `<p>` with the full marker text, `position: sticky; top: 0`,
  38 px high, text at 16 px, `#18261e` on `#e3cf8e`. At 390 a bar is fixed to the bottom and holds the one 상담 문의
  link; at 1440 that bar is `display: none`.
- **C:** nothing is pinned to the top. One bar is fixed to the bottom at both widths (`#211a16`): the marker `<p>` at
  16 px and the one 상담 문의 link. It is 60 px high at 1440 and 102 px at 390 (two rows).
- **D:** the strip as in B, `#f4effc` on `#16062e`. At 390 the pink 기업 문의 link is fixed 20 px above the bottom
  edge, at the right; at 1440 it is `display: none`.

Pictures (spec A7), drawn new:

- **B:** the pattern is one inline `<svg>` over the whole panel: one `<path>` of straight diagonal strokes that cross
  into a lattice, stroke `#f3eee2`, `opacity: 0.1`. The rule is an empty `<span aria-hidden="true">`, 2 px by 180 px.
- **D:** the contours are one inline `<svg>` placed behind the header and the headline: eight long wavy `<path>` lines
  across the width and two closed rings at the lower right, stroke `#8f6fd6` (hue 259°), `opacity: 0.45`.

Photos (free Unsplash, not Unsplash+, or Pexels). The implementer opens Unsplash and Pexels search pages in Chrome
(`mcp__claude-in-chrome__*`), compares candidates on a contact sheet in the scratchpad (not committed), and downloads
only from `images.unsplash.com` and `images.pexels.com`. It never calls `unsplash.com/napi`. What to pick:

- **B, two photos**, shown in black and white in portrait frames (350 × 450 and 400 × 460 at 1440). Subjects: a desk
  with paper and a pen, a window with a curtain, a stair rail, a chair by a window, a door with a brass handle. Each
  shows no person, no hand and no silhouette. The two differ in tone (one lighter, one darker), so the overlap reads
  in grey. Not: a furniture showroom, a hotel lobby, a café, a co-working space, a kitchen or a living room that
  reads as a home-interior advertisement, a bookshelf with readable spines, a skyline, a trading floor, coins,
  banknotes or a chart.
- **C, one photo**, in colour, landscape, at least 1800 px wide: a bright interior with daylight (a corridor, a
  meeting room, a stair with glass). Mean luminance 0.55 or more (AC190; pick one near 0.7, the blocks need a light
  ground). The blocks cover the top 430 px at 1440 and the top 270 px at 390, so the subject sits in the lower half.
  No person is the first choice. Not: a home living room, a café, a shop, a hotel lobby, a gym, a hospital corridor,
  a view of a skyline that names a city district, a screen or a sign with readable text.
- A photo that fits the list but reads as another kind of place fails T10 or T22. Pick the plainer one.

Sizes measured on a fixture on 2026-11-21 (Chrome, real web fonts, 1440×900 and 390×844; boxes as left–right ×
top–bottom in px). These are measurements of one build that meets the ACs, not Picks: a build may
differ from them inside the AC ranges.

- B at 1440: strip 0–38; header 38–178 (a wordmark row and a nav row from 122, side padding 48); wordmark at 22 px,
  `letter-spacing: 0.3em`, text centre 723; 상담 문의 button 1290–1392 × 58–104; panel 178–798; `<h1>` text 96–629
  from 250 to 539: the `<span>` at 42 px with `line-height: 1.45` (three lines, 4.36 ×), the `<em>` at 72 px; rule
  72–74 × 256–436; the AC32 sentence at 14 px, 567–591; back frame 920–1320 × 238–698; front frame 750–1100 × 388–838,
  so it ends 40 px below the panel.
- B at 390: header 38–138 (wordmark 17 px; three nav links in one row, 90–138); panel 138–682; `<h1>` 170–348 (the
  `<span>` at 26 px in three lines, the `<em>` at 44 px in one); the AC32 sentence at 13 px, 364–404; back frame
  137–370 × 432–682; front frame 20–224 × 492–732; bottom bar 776–844.
- C at 1440: narrow block 0–440 × 0–300; wide block 440–1440 × 0–430; wordmark at 42 px, weight 800,
  `line-height: 1.12`, box 48–193 × 166–260; nav 40–69, ending 48 px from the right; `<h1>` at 52 px, weight 400,
  `line-height: 1.25`, 117–312, text 536–1055; the AC32 sentence at 14 px, 336–360; the photo 0–900; bottom bar
  840–900; the statement at 34 px from 900.
- C at 390: narrow block 0–120 × 0–190; wide block 120–390 × 0–270; wordmark at 22 px, 16–92 × 123–172; three nav
  links at 14 px, 16–40; `<h1>` at 23 px, 62–151; the AC32 sentence at 13 px in three lines, 165–224; bottom bar
  742–844; 472 px of the photo shows between the wide block and the bar.
- D at 1440: strip 0–38; header 38–134; wordmark at 30 px, 40–175 × 67–106; nav pill 989–1281 × 60–112; pink pill
  1293–1400 × 60–112; `<h1>` at 64 px with `word-spacing: -0.2em`, 284–367, text 166–1274; outline pill 652–789 ×
  395–442; the AC32 sentence at 14 px, 478–502; sheet 24–1416 from 640; tags 760–797; cards from 837; contours
  1440 × 720.
- D at 390: header 38–110; wordmark at 27 px, 20–142 × 56–92; `<h1>` at 30 px in two lines, 174–252; outline pill
  274–321; the AC32 sentence at 13 px in two lines, 349–389; sheet 8–382 from 580; tags 684–767 (two rows); cards from
  807; floating link 267–374 × 775–824, 20 px above the bottom edge; contours 390 × 640.
- Wordmarks (AC243–AC246): text centres at 1440 are B (723, 79), C (121, 212), D (108, 86); sizes 22, 42 and 30 px. At
  390 the centres are B 198, C 54, D 81 px and the sizes 17, 22 and 27 px. AC178 allows C's centre from 160 px and
  AC208 allows D's to 120 px, and those two ends break AC244: keep C's centre 190 px or more from the top and D's
  100 px or less.
- AC247 for C depends on the copy: with the `<h1>` text from 536 px, the widest line must be wider than 368 px. The
  picked middle line is 519 px wide, which puts the centre at 795 px.
- The crops of the wordmarks and headlines at these sizes read syllable by syllable at deviceScaleFactor 1.

## Fixed parameters of the checks (the page contract)

- **First screen** is 1440×900 and 390×844. "Visible" means inside the viewport, opacity (multiplied up the
  ancestors) above 0.5, the text whole (not cut by an `overflow` box of its own or of an ancestor, no ellipsis, not
  pushed off the side by `text-indent`), and not covered at the centre of any of its lines by an element (or its
  `::before`/`::after`) painted above it with a background image or colour at alpha × opacity above 0.5, by an
  `<img>` or by a filled SVG shape, judged 1.5 s after load. For the
  fixed texts (the sample marker, the AC31, AC57, AC77 and AC81 sentences) it also means drawn as written: no `filter`,
  `transform`, `scale`, `zoom`, `mask-image` or `mix-blend-mode` on the element or on any ancestor, and no
  `-webkit-text-fill-color` other than its `color`. "At every scroll position" (AC12, AC43) is every 40 px down to
  the end, each within 1.5 s. AC96 is judged at 1440, at 390 and inside a `width:390px` iframe; an element that
  reaches past the right edge fails even when `overflow-x` on `<html>` or `<body>` hides it.
- **Widths.** A per-sample AC is read at 1440 unless it names 390 (spec, per-sample preamble). The checks follow
  that: AC173, AC207 and AC228 are read at 1440 only. AC148, AC164, AC219 and AC236 are read at both widths.
- **Markup the checks find by name:** `<a class="wordmark">` in the first `<header>`; C's `<p class="statement">`;
  D's `<ul class="tags">` and its cards `class="card"`. Everything else is found by tag, order or computed style.
  Write explicit end tags.
- **Sample marker** (AC8–AC12 · AC117): the full text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" as the own text of
  one element (not CSS `content:`, not split over child elements), with the `·` U+00B7, at the body font size or
  larger and at least 14 px. The element that stays on screen (AC12) is found the same way; it, or an element
  between it and its fixed or sticky ancestor (that ancestor included), has a background colour of alpha 1. AC13,
  AC14, AC57, AC81 and AC93 read the last `<footer>` that is not inside an `<article>`.
- **Sentences** (AC31 · AC32 · AC57–AC59 · AC77 · AC81): each fixed sentence is the own text of one element, written
  exactly as in the spec. AC31 and AC77 are read on the copies visible in the contact section (the largest counts).
  AC32 is read on a copy visible on the first screen. AC58 and AC59 are checked on every displayed copy of the AC57
  sentence. AC81 is read on a copy visible in the footer, at 13 px or more.
- **Sections** (AC28–AC30): each of the service, steps and contact sections is a `<section id="…">` with its own
  `<h2>`. The service section is the one section whose `<h2>` holds 하는 일, 서비스 or 투자 분야. The steps section is
  the one whose `<h2>` holds 절차, 과정 or 방식. The contact section is the one whose `<h2>` holds 문의 or 상담 among the
  sections that match neither of those two, so "상담 과정" is the steps section and "상담 문의" the contact section.
  "서비스 문의" fails (two matches). The service section names its things as three or more `<li>` or `<h3>`. The steps
  are three or more `<li>` children of one `<ol>`.
- **First section, bars, holds.** "The first section" for pictures (`<img>`, the pattern, the contours) is every
  element before the service section. For links (AC148, AC219) it leaves out the `<header>` and every bar. A bar is
  an outermost displayed `position: fixed` element, or a `sticky` element that sits at its `top` or `bottom` offset;
  its side is the half of the viewport that holds its centre. "The strip" is the top bar that holds the marker. A
  block, panel, sheet or bar "holds" an element when the element is its descendant; "lies inside" compares boxes.
  Bars are known only to a browser, so `page` counts the links of AC148 and AC219, at 1440 and at 390.
- **Contact section** (AC31 · AC36–AC40 · AC45–AC47): four separate links whose accessible names (`aria-label`, else
  text) contain 카카오톡, 전화, 네이버 예약 and 네이버 지도. The 상담 hours are `HH:MM–HH:MM` (also `-`, `—`, `~`). The
  closed-days line holds 휴무, 휴관, 쉽니다, 쉬어요, 쉬는 날 or 쉼 and a day name (일요일, 공휴일, 주말, 토요일 …) in one
  block, or one of the two in a label of at most 12 characters and the other in the next block
  (`<dt>쉬는 날</dt><dd>토요일 · 일요일 · 공휴일</dd>`). A closed-days block that holds 에도, 없이, 문의 or 휴무 없 is not
  counted. The section shows an address with "(가상 주소)" and `02-000-0000`. `page` reads the hours, a closed-days
  word, "(가상 주소)" and the phone number again from the displayed text of the section, so none of them is hidden
  at either width.
- **Links** (AC41–AC44 · AC50 · AC101 · AC102): every `<a>` has `href="#"` or `href="#<id on the page>"`; there is no
  `tel:` and no `mailto:` link. The contact link of AC41–AC43 is an `<a href="#<contact section id>">` whose text
  contains 문의 or 상담. AC44 reads the last element with its own text in the last `<footer>`, by its box: leave room so no bar or
  floating link overlaps that box. The header `<nav>` has
  three or more `<a>`, each with an `href` starting with `#` and a text with a Hangul syllable. AC101: the check
  presses Tab through the page; every displayed `<a href>` must be reached, match `:focus-visible`, and then show an
  outline of 1 px or more, or a changed `box-shadow`, background, border colour, text colour or underline. Where
  an AC counts the links with one text (AC136, AC211), a link counts by its text or by its `aria-label`, so an icon
  link labelled 상담 문의 is a second one.
- **No toggle** (AC125): no `<details>`, `<summary>` or `<dialog>`. The drawn-toggle part is T11, T23 and T34.
- **Painted with elements:** bars and the backgrounds behind text are elements. A `::before`/`::after` rule (also
  written `:before`, in a grouped selector, inside `@media`, in `style.css` or `<style>`) may set `position` to
  `absolute`, `relative` or `static` only (AC118). A generated `::before`/`::after` with a `background-image` or a
  background colour of alpha above 0 fails AC59 and AC98 for all text in its element: a list dot, a step number
  badge or an underline bar beside text is an empty `aria-hidden="true"` element or a `border`. An element that
  holds no text may paint its `::before`/`::after` freely.
- **Contrast** (AC59 · AC98): for every displayed element with its own text outside an `<svg>`, the text colour (with
  its alpha and the opacity of its ancestors) against the background colours of its ancestors, composited down to
  the first opaque one. The text is also read where it is drawn, at the centre of each of its lines: an element that
  is not the text and not its ancestor and paints there (a background, an `<img>`, a filled SVG shape; with
  `pointer-events: none` too) fails as "cannot judge", so text is laid on its own ancestors only. A bar that passes
  over page text is left out of this. The limit is 4.5:1; text of 24 px or more inside an `<h1>`–`<h6>` needs 3:1 (AC98 names body
  text, navigation links and button labels). One `linear-gradient` of opaque `rgb()` stops on an ancestor is judged at
  every stop, and the text colour must not lie between the stops in luminance (C's blocks: white is 4.93:1 and
  7.50:1). Any other `background-image` behind text fails, because the check cannot judge it. Text whose rendered
  box overlaps an `<img>` that is painted over the background that was read fails too ("the text lies over an
  `<img>`"): in C the blocks are not ancestors of the photo, so text inside them is judged on the gradient; in B no
  text may touch a frame.
- **Page text** (AC25 · AC26 · AC52–AC55 · AC60–AC69 · AC73 · AC78 · AC82 · AC83 · AC115 · AC116 · AC167 · AC203 · AC240)
  is the text of `index.html` outside `style`, `template` and `title` (inline SVG text included), plus the `<title>`
  text, `meta` description, keywords, `og:` and `twitter:` content (`name` or `property`), `aria-label`, `alt` and `title` attributes, and the text of CSS
  `content:` declarations: every string of the value joined, CSS escapes decoded, a `counter()` read as the digit 1 (a
  `content:` with `attr()` or `var()` fails); whitespace collapsed, so a line break in the source is a space. Matching is the spec's: plain
  substrings; a listed word with a space also matches without it; a word with a Latin letter in any case; a word made
  only of Latin capitals and digits as a whole word in any case; full-width forms folded, soft hyphens and
  zero-width and other format characters dropped. The AC31 and AC57 sentences are taken out before the lists of AC60–AC68 are read.
  AC26 reads any dotted Latin name that ends in two or more letters as a domain (`robin.vc`), `example.com` and file names (`thumb.jpg`) aside.
  Words that hit in an allowed sense are rewritten, not exempted. Traps: 인가요 and 허가 (인가, 허가), 수익자 and 수익성
  (수익), 사회보장 and 보장하지 (보장), 미스리딩 (리딩), 선도적 and 선두 (선도), 배수진 (배수), 알파벳 (알파), 지금 가입, 누적,
  영업 실적 (실적), 후기 and 리뷰, 수상한 (수상), 혜택, 토스트 (토스), 자신한 and 참신한 (신한), 키움, 결제, 계좌 이체 (이체),
  다우, 만기, 청약, 반드시, 확실히, 최대한 and 최고급 (최대, 최고), 무료 상담 (무료), 이벤트, 포털, 시작하기 전에 (시작하기).
  In a 자문 sample: 출자 and 사모펀드. In D: 누구나, 소액, 노후, 구독. AC115 reads the word that holds 로빈 and the word
  after it: "로빈캐피탈은 금융투자업자가" fails (금융투자), so do not put the name directly before such a word.
- **Figures** (AC73) are read per block (a `p`, `li`, `dd`, heading …; the `<title>`, each attribute and each CSS
  `content:` string is its own block), full-width digits folded, after the three uncounted kinds are taken out
  (`02-000-0000`, `000-00-00000`, `HH:MM`). A hit is a digit before `%`; a digit, optional spaces, then 원, 만, 억, 조,
  달러, 유로, 명, 건, 배, 개국, 개사, 곳, 년 or 호 (also after 천, 백 or 십); `₩`, `￦`, `$` or `€` beside a digit; `x`
  directly beside a digit; `+` after a digit; a thousands comma; a block that holds only a number, followed by a block
  that starts with `%` or with a unit, whatever follows the unit. Traps: a step number before 만남, 원하는, 건너, 명확,
  곳곳 or 년간, in one block or as a block of its own before it (use a CSS counter with no unit string beside it, or
  하나 · 둘 · 셋); a building name after the lot number ("결로 12 명인빌딩"); a room number with 호.
  "평일 09:00–18:00" and "결로 12 (가상 주소)" pass.
- **Numbers** (AC20 · AC22–AC24): addresses are block text matching `<한글>로|길 <번호>`, `<한글>동N가 <번호>`,
  `<번호> 번지` or `<한글>구|군|시 <한글>동 <번호>`; every such block holds "(가상 주소)". Every phone number is
  `02-000-0000`, whatever its separators (0507 and 0505 numbers included). 사업자등록번호 is `000-00-00000`. AC24 fails on 등록번호 without 사업자 before
  it, on 신고번호, 인증번호, 허가번호, 인가번호, 면허번호 and 심의번호, on 통신판매(업) directly before 등록 or 신고, on any
  `제 <number> 호`, and on Registration, Licence, Certificate or Certification before No., Number or `#`.
- **Folder, hosts and fonts** (AC1 · AC2 · AC56 · AC99 · AC120 · AC122 · AC127 · AC163 · AC200 · AC236): the folder holds
  `index.html`, `style.css`, `thumb.jpg` and, in B and C, `img/` with its image files and `sources.txt`; no other
  file (dotfiles aside), no `.svg`, `.png` or `.gif`, no `data:` URL. A URL is judged with entities decoded and in
  any letter case, `//host` included. Fonts come from the two linked stylesheets only: no `@font-face`, no
  `@import` to another host. On jsDelivr only `/gh/orioncactus/pretendard@…` or `/npm/pretendard@…` is loaded. `fonts.googleapis.com` is asked for exactly `Grandiflora One` and `Gowun Batang` (B),
  nothing (C), `Orbit` (D). AC127 reads `font-family` and `font` values, custom properties, SVG
  `font-family` attributes and font URLs, as whole words.
- **Faces** (AC119–AC121 · AC164 · AC236 · AC242): the checks read the first family of the computed `font-family`.
  AC119 also needs every font Chrome renders for the `<h1>` and the `a.wordmark` (CDP `CSS.getPlatformFontsForNode`,
  descendants included) to be a loaded web font whose family name starts with the sample's face: `Grandiflora One`
  or `Gowun Batang` in B's `<h1>`, `Gowun Batang` in B's wordmark, Pretendard in C, `Orbit` in D. Start the body
  stack with `"Pretendard Variable"` (the name the linked sheet defines). AC242 reads the `<h1>` element itself, so
  B's `h1` rule sets `font-family: "Grandiflora One"` and `font-weight: 400`, and the `<em>` overrides the family.
  Headings are bold by default: every rule that sets `Grandiflora One` or `Orbit` also sets `font-weight: 400`.
  Digits (hours, phone number, 사업자등록번호) stay in Pretendard.
- **Body colours** (AC129 · AC169 · AC205 · AC248): the last `background`/`background-color` and the last `color` in a
  top-level `body` rule of `style.css`, each one colour written as hex or `rgb()`, or a `var()` that `:root` or `html`
  defines so. Every other rule whose subject is `body` sets the same colour or none.
- **Colours the checks parse** (AC166 · AC202 · AC237): AC166 reads every `background`, `background-color` and
  `background-image` value of B, with `var()` resolved. AC202 and AC237 read every declaration value of C and D;
  AC237 and AC239 also read the `fill`, `stroke`, `stop-color` and `color` attributes of D's inline SVG. Write every
  colour as hex or `rgb()`/`rgba()` with plain numbers. `hsl()`, a colour name other than `black`, `white` and the
  exact greys, a system colour (`Highlight`, `LinkText` …) or an undefined `var()` fails, because the check cannot read it. AC165, AC201 and AC239 read
  `style.css`, `<style>` and `style=""`; AC239 reads the whole `index.html` too.
- **Photos** (AC85–AC89 · AC93 · AC124 · AC149 · AC187 · AC190 · AC235): a photo is an `<img>` with `src="img/<file>"`
  and `alt=""`, before the service section; there is no `<picture>`, no `<source>` and no CSS `url()` to a local
  file. Every file of `img/` is the `src` of an `<img>`. Files are `.jpg`, `.jpeg` or `.webp` with matching content.
  A page URL in `sources.txt` starts with `https://unsplash.com/photos/` or `https://www.pexels.com/photo/`, or is
  `-`; a downloaded URL is `https://images.unsplash.com/photo-…` or `https://images.pexels.com/photos/<id>/…` (the
  photo ID is read from it). "Photos:" in the footer names Unsplash when `sources.txt` has an Unsplash URL and
  Pexels when it has a Pexels URL, and names neither otherwise. AC190 is the mean Rec. 709 luma of the
  gamma-encoded pixels of the file, read from a 64 × 64 copy made by `sips`.
- **B's parts:** the panel is the nearest ancestor of the `<h1>` with the background `#123524`. The pattern is the
  one `<svg>` of the first section outside the `<header>`; write `fill="none"` on each `<path>` or on the `<svg>`
  (AC140). The rule is the one `aria-hidden="true"` element in the panel with no text, at most 3 px wide, 120 px or
  taller, with the background `#e3cf8e`. The back frame is the first `<img>` and the front frame the second; the
  front one needs a `z-index` above the back one. The three columns are the `<li>` children of the one `<ul>` of
  the service section, each with one `<h3>` and one `<p>`. The edges of the `<h1>` are those of its rendered text.
  Line counts read box heights: no vertical padding on the `<span>`, `line-height` from 1.0 to 1.75. AC144 also
  counts the lines of the `<span>`'s text: three or four.
- **C's parts:** the `<header>` is the whole first screen: it holds the photo, the narrow block with the wordmark
  and the wide block with the `<nav>`, the `<h1>` and the AC32 sentence. The blocks are the only two displayed
  elements of the page with a `linear-gradient` background-image, so no other element uses a gradient; the narrower
  one is the narrow block. The wordmark is a positioned or block-level box of two lines (two `<span>` with
  `display: block`, no `<br>` and no space, and `aria-label="로빈자산관리"` on the link: Chrome joins two block lines
  with a space, and `page` reads the name Chrome computes, AC18), with no vertical padding and a
  `line-height` from 1.0 to 1.3. Each `<span>` of the `<h1>` is `display: block`, one line, `line-height` at most
  1.5. The statement's lines are counted from its line boxes. AC194 counts the row that holds the 상담 문의 link. The service list is the `<ul>` of four or more `<li>`.
- **D's parts:** the contours are the one `<svg aria-hidden="true">` before the service section outside a link; write
  `fill="none"` and the stroke on each `<path>` or on the `<svg>`. The nav pill is the `<nav>` element itself (its
  own border and radius). The pink pill is the one link of the `<header>` outside the `<nav>` and the wordmark. The
  sheet is the nearest ancestor (or self) of the service section with the background `#fbf9ff`. Tags are the `<li>`
  of `ul.tags`; cards are the `class="card"` elements of the sheet, each with one `<h3>` and one `<p>`. The four
  contact links are `<a>` in `<li>` of one list. The floating link at 390 is an `<a>` that is itself
  `position: fixed`. AC238 lets `#ff6685` be a background only there, on the pink pill and in `:focus-visible`.
- **Thumbnail** (AC5): `check_browser.py thumb` compares `thumb.jpg` with a fresh 1440×900 first screen (both scaled
  to 160×100, mean absolute RGB difference at most 15 of 255 over the image and at most 40 in every 10×10 tile). It
  catches a changed colour or layout of a large area, not a changed button, pill, strip or headline colour and not a
  changed line of text; T45 item 6 looks at those. Re-run
  `profile_thumb.py` after any first-screen change, a review fix included. Make the thumbnail last.
- **Screenshots** for the reviews go to `/tmp/profile-invest-shots/<slug>/`: `desktop-1440.png` and `mobile-390.png`
  (full page, after a scroll through), the same cut into 1200 px tall bands (`desktop-1440-01.png` …),
  `iframe-390-01.png` … (the page inside the `width:390px`, 844 px tall iframe of playbook §4, one shot every 600 px
  of scroll down to the end, with the bars where a visitor sees them; AC118 limits the bars to 220 px, so what a bar
  covers in one shot is uncovered in the next; AC97's 390 px judgement reads these),
  `wordmark-1440.png`, `wordmark-390.png`, `h1-1440.png` and `h1-390.png` (crops at deviceScaleFactor 1), and
  `summary.txt` written last (`site tree` = `git rev-parse HEAD:profile/<slug>`, `site working tree` clean, dirty or
  unknown, the page heights, the iframe's among them, `result PASS|FAIL`). `compare` rewrites `/tmp/profile-invest-shots/compare/`:
  `<slug>-1440.png`, `<slug>-390.png` and `<slug>-thumb.jpg` for the three invest samples and the eighteen shipped
  samples; `<slug>-wordmark-1440.png` and `-390.png` for the three; `ref-g1-<slug>-1440.jpg` and `-390.jpg`, the
  reference screenshots the human saw at G1, copied from `.git/robintech-dev/keep/`; `ref-<slug>.png` and
  `ref-<slug>.txt`, a live first screen and the visible text of the reference home page when it answers (the last
  good copy is kept); the sheets `sheet-all-1440.png`, `sheet-all-390.png`, `sheet-thumbs.png` (twenty-one each),
  `sheet-six-390.png` (the three and the six of AC250), `sheet-trio-1440.png`, `sheet-trio-390.png`,
  `sheet-trio-thumbs.png`, `sheet-ref-<slug>-1440.png` and `sheet-ref-<slug>-390.png` (a sample beside its G1
  screenshot); and `summary.txt` with a `local <slug> tree <hash> clean|dirty` line per sample, a
  `reference-g1 <slug> ok|missing` line, a `reference <slug> <url> ok|cached <date>|unreachable` line per reference
  and `result PASS|FAIL` last (FAIL when a shot or a sheet is missing, or a face of an invest sample did not load).
  `trio` and `compare` need the real faces as `page` does (AC119).
- **Gallery** (AC111): `check_static.py gallery` needs the chip count 3, a card per sample, no 준비 중 tile and card
  data in the generated `profile/index.html` equal to the `PROFILES` entries, so a `profiles.py` edit without
  `python3 scripts/build.py` fails. `check_browser.py gallery` clicks the 투자자문 chip, then opens each card from a
  fresh load of `/profile/`, switches desktop and mobile, and closes with Esc.
- **Evidence rule** for the reviews: a sample's page folder `/tmp/profile-invest-shots/<slug>/` is current when its
  `summary.txt` exists, its `site tree` equals `git rev-parse HEAD:profile/<slug>`, its `site working tree` is
  `clean` and its last line is `result PASS`. The compare folder is current for a sample when `compare/summary.txt`
  has that sample's `local` line with the same tree and `clean`, and its last line is `result PASS`. A review uses a current folder as it is and runs the
  named command only when the folder is not current. That command starts a browser, so it runs only when a person
  asked for browser checks (AGENTS.md §6-5); otherwise the evidence is missing and the review is UNSURE, noting that
  it needs a browser run. If the folder is still not current after the run, the review is UNSURE. One run at a time
  writes a folder: a second `page <slug>` or `compare` that starts before the first ends empties its files; whoever starts reviews side by side runs the commands first (under the same condition), one after the other, and those reviews start none. Adding `thumb.jpg`
  changes the tree, so the reviews are closed after registration, on a `page` run made after it. A reference review
  uses the `ref-g1-<slug>` screenshots as its evidence: the three reference sites load their lower sections on
  scroll and may refuse headless Chrome. When a `reference-g1` line says `missing`, the review is UNSURE. Below the
  first screen the review judges against the spec's description of the reference (the Candidate B, C or D text and
  sketch, "Reference fonts and colours") and says so in its note.
- **What a review is bound to.** Every `verify(human)` note records what it judged: `git rev-parse HEAD:profile/<slug>`
  for each sample in its scope and, where the scope names `scripts/profiles.py`, `git rev-parse HEAD:scripts/profiles.py`
  (those reviews are made after T40, when all three entries are in). A review counts only while every hash it records
  is unchanged. After any later change to a sample or to an entry, a fix from another review included, the reviews
  whose hashes changed are made again; a box ticked on an older hash does not close its criteria.

## Sample B — 로빈패밀리오피스 (`profile/invest-robinfamilyoffice/`)

- [x] T1 Pick the two photos for B as in Picks: download them at web size into `img/`, write `img/sources.txt` (write the photo page URL without a locale part such as `/ko-kr/`; a downloaded URL without a readable photo ID fails AC124); open each file at 100 % and replace any with a person, a hand or legible lettering before going on (AC86·AC87·AC88·AC124) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py photos invest-robinfamilyoffice`
- [x] T2 Write `index.html` and `style.css` with the sample marker (in the strip and in the footer), a `<title>`, a description and an `og:title` with 디자인 샘플, noindex, the footer credit, the risk sentence and the 설명서 sentence, the live-text wordmark 로빈패밀리오피스, fictional address, phone and 사업자등록번호, and no other registration number (AC8·AC13·AC14·AC15·AC16·AC18·AC20·AC22·AC23·AC24·AC57·AC81) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py markers invest-robinfamilyoffice`
- [x] T3 Build the page structure: the service, steps and contact sections, the AC31 sentence, the four contact links with hours, closed days, address and phone, a Hangul header nav, every link a `#` link, no form, field, button, script, handler, embedded frame or `<details>` (AC28·AC29·AC30·AC31·AC36·AC37·AC38·AC39·AC40·AC45·AC46·AC47·AC48·AC49·AC50·AC51·AC102·AC125) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py structure invest-robinfamilyoffice`
- [x] T4 Keep the copy free of the listed words (app stores, deposits, banks, entry labels, returns, superlatives, comparisons, tips, registration claims, records, lures, funds, real firms, real stocks), of the 자문 lists, of B's history words, of reserved name words, of figures, of outside e-mail addresses, handles and domains (AC25·AC26·AC52·AC53·AC54·AC55·AC60·AC61·AC62·AC63·AC64·AC65·AC66·AC67·AC68·AC69·AC73·AC82·AC83·AC115·AC116·AC167) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py copy invest-robinfamilyoffice`
- [x] T5 `lang="ko"`, `word-break: keep-all`, one Korean `<h1>`, no skipped heading level, a `prefers-reduced-motion: reduce` block, no `::before` or `::after` rule with a `position` other than `absolute`, `relative` or `static` (AC33·AC34·AC94·AC95·AC118) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py a11y invest-robinfamilyoffice`
- [x] T6 Keep the sample self-contained: relative paths only, Pretendard on jsDelivr and exactly `Grandiflora One` and `Gowun Batang` from Google Fonts, no other `http(s)://` URL, no picture file and no `data:` URL, two `<img>` with `src="img/…"` and `alt=""` before the service section, the "Photos:" credit, neither `Chiswick` nor `Inter` (AC1·AC2·AC56·AC85·AC89·AC93·AC99·AC120·AC122·AC127·AC149·AC163) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py assets invest-robinfamilyoffice`
- [x] T7 Give B its kept traits in markup: the cream `body` colours, the lattice pattern of straight strokes, an `<h1>` of one `<span>` and one `<em>` in Hangul, the section order, 상담 in the contact heading, every dark background green, none of Rockefeller's colours (AC129·AC140·AC142·AC161·AC162·AC165·AC166) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py sample invest-robinfamilyoffice`
- [x] T8 Check B in a browser at 1440 and 390: sample marker, its size and its stay on screen, the AC31, AC32 and AC57 sentences visible with their sizes and contrast, the 설명서 sentence visible in the footer (자문 samples), the hours, closed days, address and phone number displayed in the contact section, a 상담 link on the first screen and at every scroll position at 390 with the footer's last line uncovered, bars within 220 px, web fonts loaded, Pretendard for body and digits, contrast, focus indicators, no motion under reduced motion, no horizontal overflow; the straw strip, the cream two-row header with the centred letter-spaced wordmark, the nav row and the framed 상담 문의 button; the green panel under it to 680–840 px with the faint pattern, the rule, the thin serif paragraph headline at the left and its slanted last words, no link under it; the two greyscale frames that overlap and break the panel's lower edge, right of the headline; three service columns on cream; at 390 the short header with a nav row, the bottom bar with one link, the whole headline on load and both frames under it; writes the screenshots for T9–T12 (AC8·AC9·AC10·AC12·AC18·AC31·AC32·AC34·AC41·AC42·AC43·AC44·AC45·AC46·AC47·AC57·AC58·AC59·AC81·AC95·AC96·AC98·AC101·AC117·AC118·AC119·AC120·AC121·AC130·AC131·AC132·AC133·AC134·AC135·AC136·AC137·AC138·AC139·AC141·AC143·AC144·AC145·AC146·AC148·AC150·AC151·AC152·AC153·AC154·AC156·AC157·AC158·AC159·AC160·AC164) — verify(browser): `python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robinfamilyoffice`
- [ ] T9 Review B's content (AC21·AC27·AC35·AC52·AC54·AC62·AC67·AC68·AC69·AC70·AC71·AC72·AC74·AC75·AC76·AC82·AC84) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/invest-robinfamilyoffice/` (command: `python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robinfamilyoffice`). Read `profile/invest-robinfamilyoffice/index.html` and `style.css` (for CSS `content:` text and drawn pictures) and the `invest-robinfamilyoffice` entry of `scripts/profiles.py`, look at the bands `desktop-1440-NN.png` and `mobile-390-NN.png` in that folder, and confirm each: (1) every address names a district or road that does not exist (for example 가상구 결로), and no real 구, 동 or neighbourhood is named as the business's location (a 시 or 도 name alone is fine); (2) no person's name and no portrait or drawn face anywhere, as 대표, partner, 운용역, adviser, analyst or client, and no family is named; (3) no app-store badge and no QR code or square dot pattern that reads as one; (4) no bank, 증권사 or payment brand, no real investment firm, fund or investor, no real company, listed stock, ticker or index, and no logo of any of them; (5) no platform other than 네이버 (예약 and 지도) and 카카오톡 by name, logo or icon (for example 텔레그램, 오픈채팅, 밴드, 유튜브, 링크드인, X); (6) no claim, in other words, in English or as a picture, of any of these eight kinds: a return, a protected principal or a made-good loss; a superlative or a guarantee; a comparison with another firm, product or index; a stock tip or a 리딩방 offer; a registration, a licence, a review or a regulator; a record of assets, deals, clients, awards or ratings; a free offer, a discount or an event; a named or offered fund or product (for example 믿고 맡기는, 꾸준한 성과, trusted, secure, best, a shield with a tick, an arrow that only rises); (7) no portfolio-company, investor, press, auditor, award or certificate logo or badge, and no row of such names, real or made up; (8) no amount managed or raised, no count of funds, deals, companies, clients or staff, no years in business, no founding year, no return and no fee, in words or in digits (for example 수천억, 수십 가문, 삼십 년, Since 1998); (9) no chart, graph, gauge or table that reads as a return, a growth of assets or a comparison of results; the pattern has no axis, no rising line and no figure; (10) the page presents one 업태 only, 자문 for families: it does not present itself as a 사모펀드 운용사, offers no fund, and does not show 투자일임 as pooled management in any words; (11) the page says that advice follows a talk about the client's goals and situation, and promises no result of the advice; (12) the `title`, `summary` and `features` of this sample's entry in `scripts/profiles.py` pass items (2) and (4)–(8)
      reason: whether copy or a picture names a person or a brand, implies a count or a claim in other words, or presents a second business is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/invest-robinfamilyoffice, scripts/profiles.py
      reviewed: PASS @4399e5310377787d956cfecf6c68cf658ebc3115 #c2d4536f 2026-11-21 — judged profile/invest-robinfamilyoffice 0fc77f2457fa5527cb16a1180863f1d963114fce, scripts/profiles.py 217886ebe7d6fd07681e721d37cadfc40d5af634; items 1-12 hold: only address "서울 가상구 느티길 7 (가상 주소)" (index.html:85), no person, brand, logo, figure or chart, platforms 카카오톡 and 네이버 only, one 업태 (가족 자산 자문), advice follows a talk and no result is promised (index.html:60), card text in profiles.py describes layout only
- [ ] T10 Inspect B's photos at native resolution (AC90·AC91·AC92·AC155) — verify(human): open each image file in `profile/invest-robinfamilyoffice/img/` one by one at 100 % zoom and again at 200 % (not on the page, not on a contact sheet; view a file wider than the screen in quadrants), and confirm for each: (1) no legible logo, brand name, sign, screen text, number plate, book-spine or magazine title, framed lettering or other lettering; (2) no person, no hand and no silhouette, so no face at all; (3) no landmark building, named tower or stock-exchange floor that places the business in a real firm or a real city district; (4) the subject is a still life or a room that fits a family office (Picks): it does not read as a furniture showroom, a hotel, a café, a co-working space or a home-interior advertisement. On a hit, the implementer replaces the file, updates `img/sources.txt`, re-runs T1, T6, T8, T36 and T37, and the review starts again. Name each file checked and record `git rev-parse HEAD:profile/invest-robinfamilyoffice/img` in the note; the review counts only while that hash is unchanged
      reason: lettering, a recognisable person or place and whether a stock photo fits the business are seen only by looking at the pixels.
      scope: profile/invest-robinfamilyoffice/img
      reviewed: PASS @4399e5310377787d956cfecf6c68cf658ebc3115 #e31d60b9 2026-11-21 — judged profile/invest-robinfamilyoffice/img 8590b5718f6b9b617ed24700be60acc10c21d165 (profile/invest-robinfamilyoffice 0fc77f2457fa5527cb16a1180863f1d963114fce); desk-chair.jpg (1000x1500) and window-curtain.jpg (1000x1333) each viewed in 6 tiles at 100 % and 6 at 200 % plus 300-400 % details: no lettering, no person, hand or silhouette (the darker columns behind the sheer curtain are folds), no landmark, subjects are on the Picks list
- [ ] T11 Review B's full-page screenshots (AC11·AC97·AC100·AC125·AC147) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/invest-robinfamilyoffice/` (command as in T9). Look at `desktop-1440-NN.png` and `mobile-390-NN.png` band by band and at the seams between bands, and at `wordmark-1440.png`, `wordmark-390.png`, `h1-1440.png` and `h1-390.png` without enlarging, and confirm: (1) at 1440, no text overlaps other text, a picture or a control so that letters are hidden, and no element covers another by accident (the front frame over the back frame and over the panel's lower edge is the design); (2) at 1440, no text is cut off at a box edge; (3) and (4) the same at 390, judged on the `iframe-390-NN.png` shots (the `width:390px` iframe of AC97) from the first to the last, where the bars sit as a visitor sees them and what a bar covers in one shot is judged on the next; (5) the sample marker on the first screen reads in a colour that stands out clearly from its background, at 1440 and at 390; (6) the 상담 hours and the phone number are set in a face with even digit widths; (7) no menu toggle is drawn at 390 (three bars, a "메뉴" pill) or at 1440; (8) the ornament left of the headline is a plain line, with no plant, crest or emblem on it; (9) the wordmark reads 로빈패밀리오피스 syllable by syllable at both widths, and the thin headline and its slanted words read at both widths. The strip and the bottom bar appear once in a full-page shot; what they cover there is not counted
      reason: whether text overlaps, is clipped, stands out or reads at its size is a visual judgement over the rendered page.
      scope: profile/invest-robinfamilyoffice
      reviewed: PASS @4399e5310377787d956cfecf6c68cf658ebc3115 #95437f28 2026-11-21 — judged profile/invest-robinfamilyoffice 0fc77f2457fa5527cb16a1180863f1d963114fce; items 1-9 hold on desktop-1440-01..03, mobile-390-01..04, iframe-390-01..07 and the four crops: no hidden or clipped text, what the strip and bottom bar cover is whole in the next shot, marker dark on straw (10.2:1), hours and phone in Pretendard with tabular-nums (style.css:121), no menu toggle, ornament is a plain 2 px rule (style.css:66), wordmark and headline read at both widths
- [ ] T12 Compare B with Rockefeller Capital Management (AC106·AC107·AC108·AC126) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/compare/` for invest-robinfamilyoffice and to `/tmp/profile-invest-shots/invest-robinfamilyoffice/` (commands: `python3 docs/features/2026-11-21-profile-invest/check_browser.py compare`, `python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robinfamilyoffice`). Look at `sheet-ref-invest-robinfamilyoffice-1440.png` and `-390.png`, at `ref-invest-robinfamilyoffice.txt` when it exists, and at the bands of the sample, and confirm: (1) the sample shows no logo, wordmark or brand name of the reference; (2) no sentence or slogan of the reference appears in the sample; (3) no picture of the sample copies a picture of the reference: the pattern is a lattice and not a street map, the photos are not the reference's archive photos, and the ornament is not a thistle; (4) side by side the two are not taken for the same site: pictures, palette values, typeface, copy and section order are new (the kept traits of item 6 do not count); (5) the sample's `<h1>` is not a translation or close paraphrase of "For more than seven generations, we have grown and evolved alongside members of the Rockefeller family, pursuing extraordinary possibilities."; (6) the sample keeps each trait listed for Candidate B under "Traits to keep" in the spec, as changed by A3–A7: a two-row cream header with a letter-spaced serif wordmark and a framed outline button; a dark panel (green) with a faint line pattern; a thin serif paragraph as the headline, with its last words slanted in a second face on their own lines; two overlapping picture frames at the right that break the panel's lower edge; a small ornament at the paragraph's start; a cream section of three service columns below
      reason: copied wording, pictures and marks, "taken for the same site" and "keeps the trait" are judgements a person makes.
      scope: profile/invest-robinfamilyoffice
      reviewed: PASS @4399e5310377787d956cfecf6c68cf658ebc3115 #16975b74 2026-11-21 — judged profile/invest-robinfamilyoffice 0fc77f2457fa5527cb16a1180863f1d963114fce; compare and page folders current; items 1-6 hold: no Rockefeller name, mark, sentence, archive photo, street-map pattern or thistle; palette, faces, copy and lower sections are new (none of the reference hex values or font names in index.html or style.css); h1 is not a version of the reference headline; every Candidate B trait is seen at 1440; below the first screen the reference was judged against ref-invest-robinfamilyoffice.txt and the spec description

## Sample C — 로빈자산관리 (`profile/invest-robinwealth/`)

- [x] T13 Pick the one photo for C as in Picks, as in T1; its mean luminance is 0.55 or more (AC86·AC87·AC88·AC124·AC190) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py photos invest-robinwealth`
- [x] T14 Write `index.html` and `style.css` with the markers as in T2, with the marker in the bottom bar and the two-line wordmark 로빈자산관리 (AC8·AC13·AC14·AC15·AC16·AC18·AC20·AC22·AC23·AC24·AC57·AC81) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py markers invest-robinwealth`
- [x] T15 Build the page structure as in T3 (AC28·AC29·AC30·AC31·AC36·AC37·AC38·AC39·AC40·AC45·AC46·AC47·AC48·AC49·AC50·AC51·AC102·AC125) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py structure invest-robinwealth`
- [x] T16 Keep the copy clean as in T4, with C's own list in place of B's (AC25·AC26·AC52·AC53·AC54·AC55·AC60·AC61·AC62·AC63·AC64·AC65·AC66·AC67·AC68·AC69·AC73·AC82·AC83·AC115·AC116·AC203) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py copy invest-robinwealth`
- [x] T17 Language, keep-all, headings, reduced-motion block and `::before`/`::after` positions as in T5 (AC33·AC34·AC94·AC95·AC118) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py a11y invest-robinwealth`
- [x] T18 Keep the sample self-contained as in T6, with no Google Fonts family, one `<img>` and no `pjtSans` (AC1·AC2·AC56·AC85·AC89·AC93·AC99·AC120·AC122·AC127·AC187·AC200) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py assets invest-robinwealth`
- [x] T19 Give C its kept traits in markup: the warm white `body` colours, the two gradient hex values, an `<h1>` of three `<span>` lines, the statement before the service list of four or more items, the section order, 상담 in the contact heading, one warm colour family, none of PJT's colours (AC169·AC173·AC183·AC197·AC198·AC199·AC201·AC202) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py sample invest-robinwealth`
- [x] T20 Check C in a browser at 1440 and 390, the common checks as in T8 and C's: no top bar and a transparent header; the dark bottom bar with the marker and one 상담 문의 link; the two terracotta gradient blocks that step down from the top edge, the narrow one holding only the two-line white wordmark at its lower left, the wide one holding the text nav at the top right, the three-line white headline and the AC32 sentence; the photo under both blocks down to the bottom bar with no text on it; the large statement; the bordered service list; at 390 the narrow block at the top left, the wide block at its right with three nav links in a row and the headline, and 220 px or more of the photo; writes the screenshots for T21–T24 (AC8·AC9·AC10·AC12·AC18·AC31·AC32·AC34·AC41·AC42·AC43·AC44·AC45·AC46·AC47·AC57·AC58·AC59·AC81·AC95·AC96·AC98·AC101·AC117·AC118·AC119·AC120·AC121·AC170·AC171·AC172·AC173·AC174·AC175·AC176·AC177·AC178·AC179·AC180·AC181·AC182·AC183·AC184·AC185·AC186·AC187·AC188·AC189·AC192·AC193·AC194·AC195·AC196·AC197) — verify(browser): `python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robinwealth`
- [ ] T21 Review C's content (AC21·AC27·AC35·AC52·AC54·AC62·AC67·AC68·AC69·AC70·AC71·AC72·AC74·AC75·AC76·AC82·AC84) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/invest-robinwealth/` (command: `python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robinwealth`), read `profile/invest-robinwealth/index.html`, `style.css` and the `invest-robinwealth` entry of `scripts/profiles.py`, look at the bands, and confirm items (1)–(12) of T9 for this sample; in (9) no drawing is in the first screen; in (10) the 업태 is 자문 for individuals and families, and the page offers no advice on mergers, restructuring or fund-raising for companies
      reason: whether copy or a picture names a person or a brand, implies a count or a claim in other words, or presents a second business is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/invest-robinwealth, scripts/profiles.py
      reviewed: PASS @4399e5310377787d956cfecf6c68cf658ebc3115 #fb77668f 2026-11-21 — judged profile/invest-robinwealth bb3f578ad2f04b9362676d5ca5a90862648706f2, scripts/profiles.py 217886ebe7d6fd07681e721d37cadfc40d5af634; items 1-12 hold: only address "서울 가상구 볕뜰로 21 (가상 주소)" (index.html:80, :95), no person, brand, logo, figure, chart or drawing in the first screen, platforms 카카오톡 and 네이버 only, 업태 is 자문 for individuals and families with no company advice, no result promised, card text in profiles.py describes layout only
- [ ] T22 Inspect C's photo at native resolution (AC90·AC91·AC92·AC191) — verify(human): open the image file in `profile/invest-robinwealth/img/` at 100 % zoom and again at 200 % (in quadrants), and confirm: (1) no legible logo, brand name, sign, screen text, number plate or other lettering; (2) no person, or only figures blurred past recognition who show no face; (3) no landmark building, named tower or stock-exchange floor; (4) it shows a bright interior with daylight that fits an advisory office (Picks): it does not read as a home, a café, a shop, a hotel, a gym or a hospital. On a hit, the implementer replaces the file, updates `img/sources.txt`, re-runs T13, T18, T20, T38 and T39, and the review starts again. Name the file checked and record `git rev-parse HEAD:profile/invest-robinwealth/img` in the note; the review counts only while that hash is unchanged
      reason: lettering, a recognisable person or place and whether a stock photo fits the business are seen only by looking at the pixels.
      scope: profile/invest-robinwealth/img
      reviewed: PASS @4399e5310377787d956cfecf6c68cf658ebc3115 #823ab773 2026-11-21 — judged profile/invest-robinwealth/img 8bc65bb11d25758d1cbdab9ea12833c6963c4113 (profile/invest-robinwealth bb3f578ad2f04b9362676d5ca5a90862648706f2); corridor.jpg (2000x1333) viewed in 4 quadrants at 100 %, 16 tiles at 200 % and 400 % details: no lettering (door-side plaques are edge-on and blank), no person or face (a soft featureless shadow lies on the right wall, lower right), no landmark, a sunlit office corridor that does not read as a home, café, shop, hotel, gym or hospital
- [ ] T23 Review C's full-page screenshots (AC11·AC97·AC100·AC125) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/invest-robinwealth/` (command as in T21), and confirm items (1)–(7) of T11 on its bands and crops, items (3) and (4) on its `iframe-390-NN.png` shots; in (1) the blocks over the photo are the design; (9) the wordmark reads 로빈 over 자산관리 at both widths, and the headline reads on the gradient at both widths. The bottom bar appears once in a full-page shot; what it covers there is not counted
      reason: whether text overlaps, is clipped, stands out or reads at its size is a visual judgement over the rendered page.
      scope: profile/invest-robinwealth
      reviewed: PASS @4399e5310377787d956cfecf6c68cf658ebc3115 #d566df4d 2026-11-21 — judged profile/invest-robinwealth bb3f578ad2f04b9362676d5ca5a90862648706f2; items 1-7 and 9 hold on desktop-1440-01..04, mobile-390-01..04, iframe-390-01..08 and the four crops: no hidden or clipped text, every line the bottom bar cuts is whole in the next shot, marker white on the dark bar, hours and phone in Pretendard with tabular-nums (style.css:106), no menu toggle, wordmark reads 로빈 over 자산관리 and the headline reads on the gradient at both widths
- [ ] T24 Compare C with PJT Partners (AC106·AC107·AC108·AC126) — verify(human): as in T12 for invest-robinwealth (`sheet-ref-invest-robinwealth-1440.png`, `-390.png`, `ref-invest-robinwealth.txt`), confirming items (1) and (2) of T12 against PJT; (3) the photo is not the reference's office photo and shows another room; (4) side by side the two are not taken for the same site: pictures, palette values (terracotta, not blue), typeface, copy and section order are new (the kept traits of item 6 do not count); (5) the sample's `<h1>` is not a translation or close paraphrase of "PJT is a next-generation global investment bank where advice is the main event"; (6) the sample keeps each trait listed for Candidate C under "Traits to keep" in the spec, as changed by A3–A7: no header bar; two colour blocks of different width that step down from the top edge, in one gradient; the mark alone in the narrow block; the nav and a three-line sans headline in white inside the wide block, with no button; a bright photo that runs under both blocks and fills the rest of the first screen; at 390 the wide block at the right with the photo under it; below, a section of large plain text and a list of services
      reason: copied wording, pictures and marks, "taken for the same site" and "keeps the trait" are judgements a person makes.
      scope: profile/invest-robinwealth
      reviewed: PASS @4399e5310377787d956cfecf6c68cf658ebc3115 #fe8e1a15 2026-11-21 — judged profile/invest-robinwealth bb3f578ad2f04b9362676d5ca5a90862648706f2; compare and page folders current; items 1-6 hold: no PJT name, mark or sentence, the photo is another room (an empty corridor, not the glass office with figures), terracotta palette with none of the reference hex values, Pretendard only, new copy, added 상담 과정 and 상담 문의 sections; h1 is not a version of the reference headline; every Candidate C trait is seen at 1440 and 390; below the first screen the reference was judged against ref-invest-robinwealth.txt and the spec description

## Sample D — 로빈캐피탈 (`profile/invest-robincapital/`)

- [x] T25 Write `index.html` and `style.css` with the markers as in T2, without the 설명서 sentence, with the wordmark 로빈캐피탈 (AC8·AC13·AC14·AC15·AC16·AC18·AC20·AC22·AC23·AC24·AC57) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py markers invest-robincapital`
- [x] T26 Build the page structure as in T3 (AC28·AC29·AC30·AC31·AC36·AC37·AC38·AC39·AC40·AC45·AC46·AC47·AC48·AC49·AC50·AC51·AC102·AC125) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py structure invest-robincapital`
- [x] T27 Keep the copy clean as in T4, with the PE list in place of the 자문 lists and D's own list (AC25·AC26·AC52·AC53·AC54·AC55·AC60·AC61·AC62·AC63·AC64·AC65·AC66·AC67·AC68·AC69·AC73·AC78·AC115·AC116·AC240) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py copy invest-robincapital`
- [x] T28 Language, keep-all, headings, reduced-motion block and `::before`/`::after` positions as in T5 (AC33·AC34·AC94·AC95·AC118) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py a11y invest-robincapital`
- [x] T29 Keep the sample self-contained and photo-free: as in T6 with exactly `Orbit` from Google Fonts, no `<img>`, no `img/` folder, no "Photos:" credit, neither `F37Bolton` nor `Bolton` (AC1·AC2·AC56·AC85·AC89·AC93·AC99·AC120·AC122·AC127·AC235·AC236) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py assets invest-robincapital && python3 docs/features/2026-11-21-profile-invest/check_static.py photos invest-robincapital`
- [x] T30 Give D its kept traits in markup: the violet `body` colours, contours of eight or more curved stroked paths, the section order, 투자 분야 and 기업 문의 in the headings, violet and one pink only, none of Hg's colours (AC205·AC214·AC233·AC234·AC237·AC239) — verify: `python3 docs/features/2026-11-21-profile-invest/check_static.py sample invest-robincapital`
- [x] T31 Check D in a browser at 1440 and 390, the common checks as in T8 and D's: the PE sentence visible in the contact section; the dark strip; a transparent header on the violet page with the small `Orbit` wordmark at the top left, the outlined nav pill and the pink 기업 문의 pill beside it at the right; the contours behind; the centred one-line `Orbit` headline with the outline pill 투자 분야 보기 under it; the white sheet with rounded top corners that enters the first screen from below and stays in place on scroll, its tag row inside the first screen, its cards; the pale contact section with the large list of four links; at 390 the wordmark alone in the header, the floating pink link near the bottom edge with 60 px or more of the sheet above it; writes the screenshots for T32–T35 (AC8·AC9·AC10·AC12·AC18·AC31·AC32·AC34·AC41·AC42·AC43·AC44·AC45·AC46·AC47·AC57·AC58·AC59·AC77·AC95·AC96·AC98·AC101·AC117·AC118·AC119·AC120·AC121·AC206·AC207·AC208·AC209·AC210·AC211·AC212·AC213·AC216·AC217·AC218·AC219·AC220·AC221·AC222·AC223·AC224·AC225·AC226·AC228·AC229·AC230·AC231·AC232·AC236) — verify(browser): `python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robincapital`
- [ ] T32 Review D's content (AC21·AC27·AC35·AC52·AC54·AC62·AC67·AC68·AC69·AC70·AC71·AC72·AC74·AC75·AC76·AC79·AC80·AC227) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/invest-robincapital/` (command: `python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robincapital`), read `profile/invest-robincapital/index.html`, `style.css` and the `invest-robincapital` entry of `scripts/profiles.py`, look at the bands, and confirm items (1)–(9) and (12) of T9 for this sample; (10) the page presents one 업태 only, PE: it offers no 투자자문, 투자일임 or 자산관리 service to individuals and does not address the public as investors; (11) the pink pill, the floating link and the contact heading address a company or an institution (기업 문의), not a person who wants to invest; (13) the page names no portfolio company, real or made up, and describes its investments by sector and by kind of deal only; (14) no card of the sheet shows a date, a company, a person or a news headline
      reason: whether copy or a picture names a person, a company or a brand, implies a count or a claim in other words, or addresses the public as investors is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/invest-robincapital, scripts/profiles.py
      reviewed: PASS @258eee21ed953aad87bae8a72d72c922e2700a68 #785a733f 2026-11-21 — judged profile/invest-robincapital d79d0598b79a5ea609cd84dbeebbd0b0d7c8b45e, scripts/profiles.py 217886ebe7d6fd07681e721d37cadfc40d5af634; page folder current; items 1-14 hold: only address "서울 가상구 능선로 15 (가상 주소)" (index.html:108, :126), no person, photo, brand, logo, badge row, figure or table, platforms 카카오톡 and 네이버 only, the contours (index.html:17-28) are wavy lines with two closed loops and no axis or figure at 1440 and at 390 (desktop-1440-01.png, mobile-390-01.png), PE only with 기업 문의 on the pill, the floating link and the contact heading (index.html:36, :131, :101), no portfolio company, cards hold a drawing, a deal kind and one sentence, card text in profiles.py describes layout only
- [ ] T33 Review D's drawing and pink (AC215·AC238) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/compare/` for invest-robincapital and to `/tmp/profile-invest-shots/invest-robincapital/` (commands: `python3 docs/features/2026-11-21-profile-invest/check_browser.py compare`, `python3 docs/features/2026-11-21-profile-invest/check_browser.py page invest-robincapital`). Look at `sheet-ref-invest-robincapital-1440.png` and at the bands, read the inline `<svg>` of `profile/invest-robincapital/index.html` and every rule of `style.css` that holds `#ff6685`, and confirm: (1) the contours read as faint terrain lines behind the text; (2) they have no axis, no rising line and no figure, and do not read as a chart; (3) they are drawn new: the lines do not follow the shaded shapes of the reference screenshot; (4) `#ff6685` is a `background` or `background-color` value only in rules for the pink pill of the header, the floating link at 390 and `:focus-visible` outlines; (5) on the rendered page the pink pill (the floating link at 390) is the only pink surface
      reason: whether a drawing reads as terrain or as a chart, and whether it was traced, is a visual judgement; which rule paints which element needs a reading of the stylesheet.
      scope: profile/invest-robincapital
      reviewed: PASS @258eee21ed953aad87bae8a72d72c922e2700a68 #90946c18 2026-11-21 — judged profile/invest-robincapital d79d0598b79a5ea609cd84dbeebbd0b0d7c8b45e; compare and page folders current; items 1-5 hold: the contours svg (index.html:17-28) is ten stroked paths, eight wavy lines across the width and two closed loops, with no text, axis or figure; the lines undulate and none climbs across the screen at 1440 or at 390 (desktop-1440-01.png, iframe-390-01.png); they do not follow the shaded blobs of the G1 screenshot; #ff6685 is a background only at style.css:44 (.pink) and :156 (.float), an outline at :25; pink pixels only in the header pill at 1440 (box 1289,60-1399,111) and the floating link at 390 (box 267,775-373,823)
- [ ] T34 Review D's full-page screenshots (AC11·AC97·AC100·AC125) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/invest-robincapital/` (command as in T32), and confirm items (1)–(7) of T11 on its bands and crops, items (3) and (4) on its `iframe-390-NN.png` shots; in (1) the sheet over the contours is the design; (9) the wordmark reads 로빈캐피탈 syllable by syllable at both widths, and the headline reads over the contours at both widths. The strip and the floating link appear once in a full-page shot; what they cover there is not counted
      reason: whether text overlaps, is clipped, stands out or reads at its size is a visual judgement over the rendered page.
      scope: profile/invest-robincapital
      reviewed: PASS @258eee21ed953aad87bae8a72d72c922e2700a68 #43ba9a7d 2026-11-21 — judged profile/invest-robincapital d79d0598b79a5ea609cd84dbeebbd0b0d7c8b45e; page folder current; items 1-7 and 9 hold on desktop-1440-01..03, mobile-390-01..04, iframe-390-01..06 and the four crops: no hidden or clipped text, what the strip and the floating link cover is whole in the next shot (iframe-390-04 to -05), marker near-white on the dark strip, hours and phone in Pretendard with tabular-nums (style.css:87), no menu toggle, wordmark reads 로빈캐피탈 and the headline reads over the contours at both widths
- [ ] T35 Compare D with Hg (AC106·AC107·AC108·AC126) — verify(human): as in T12 for invest-robincapital (`sheet-ref-invest-robincapital-1440.png`, `-390.png`, `ref-invest-robincapital.txt`), confirming items (1) and (2) of T12 against Hg; (3) no picture of the sample copies a picture of the reference: the contours are lines and not the reference's shaded shapes, and the cards hold no picture of the reference; (4) side by side the two are not taken for the same site: pictures, palette values, typeface, copy and section order are new (the kept traits of item 6 do not count); (5) the sample's `<h1>` is not a translation or close paraphrase of "Navigate what's next."; (6) the sample keeps each trait listed for Candidate D under "Traits to keep" in the spec, as changed by A3–A7: one deep violet page with a faint contour-line pattern; a small wordmark at the top left; an outlined pill that holds the nav, and one hot-pink filled pill beside it; a centred light-weight one-line headline with a small outline pill under it; a white sheet with rounded top corners that enters the first screen from below and holds tag pills and cards; a pale closing section with a large list of links
      reason: copied wording, pictures and marks, "taken for the same site" and "keeps the trait" are judgements a person makes.
      scope: profile/invest-robincapital
      reviewed: PASS @258eee21ed953aad87bae8a72d72c922e2700a68 #600b768b 2026-11-21 — judged profile/invest-robincapital d79d0598b79a5ea609cd84dbeebbd0b0d7c8b45e; compare and page folders current; items 1-6 hold: no Hg name, mark or sentence, contours are stroked lines (index.html:17-28) and not shaded shapes, card drawings are new and there is no img, none of the reference hex values or font names in index.html or style.css, Orbit and Pretendard, new copy and sections; h1 "오래 일군 사업을 책임 있게 이어받습니다" (index.html:40) is not a version of "Navigate what's next."; every Candidate D trait is seen at 1440; below the first screen the reference was judged against ref-invest-robincapital.txt and the spec description

## Registration (`scripts/profiles.py`, `thumb.jpg`, `profile/index.html`)

Each sample is registered after its visual work. `python3 scripts/build.py` regenerates `profile/index.html`; never
edit that file by hand. After any later change to a sample's first screen, a fix from a review included, run
`python3 scripts/profile_thumb.py <slug>` again before its thumb task is checked.

- [x] T36 Register B: add its `PROFILES` entry (spec AC128, title from A13; the check needs that palette and title and reads `title`, `summary` and `features` with the word lists and digit rules of T4), run `python3 scripts/profile_thumb.py invest-robinfamilyoffice`, run `python3 scripts/build.py` (AC1·AC3·AC4·AC5·AC6·AC17·AC76·AC105·AC114·AC115·AC116·AC123·AC128) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-21-profile-invest/check_static.py register invest-robinfamilyoffice`
- [x] T37 Check that B's `thumb.jpg` shows its current first screen (AC5) — verify(browser): `python3 docs/features/2026-11-21-profile-invest/check_browser.py thumb invest-robinfamilyoffice`
- [x] T38 Register C as in T36 (spec AC168; the card text is read with the lists of T16), with `python3 scripts/profile_thumb.py invest-robinwealth` (AC1·AC3·AC4·AC5·AC6·AC17·AC76·AC105·AC114·AC115·AC116·AC123·AC168) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-21-profile-invest/check_static.py register invest-robinwealth`
- [x] T39 Check that C's `thumb.jpg` shows its current first screen (AC5) — verify(browser): `python3 docs/features/2026-11-21-profile-invest/check_browser.py thumb invest-robinwealth`
- [x] T40 Register D as in T36 (spec AC204; the card text is read with the lists of T27), with `python3 scripts/profile_thumb.py invest-robincapital` (AC1·AC3·AC4·AC5·AC6·AC17·AC76·AC105·AC114·AC115·AC116·AC123·AC204) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-21-profile-invest/check_static.py register invest-robincapital`
- [x] T41 Check that D's `thumb.jpg` shows its current first screen (AC5) — verify(browser): `python3 docs/features/2026-11-21-profile-invest/check_browser.py thumb invest-robincapital`

## Gallery, the three together and the branch

- [x] T42 Regenerate the gallery with all three entries: 투자자문 chip count 3, a card per sample, no invest 준비 중 tile, no other invest entry, the three names, no shared palette hex, only D dark (AC3·AC6·AC19·AC111·AC114·AC241·AC248) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-21-profile-invest/check_static.py gallery && python3 docs/features/2026-11-21-profile-invest/check_static.py three`
- [x] T43 Check the gallery: the 투자자문 filter shows the three cards and no 준비 중 tile; each card, from a fresh load, opens the preview with that sample, its desktop/mobile buttons switch the width, Esc closes it (AC111) — verify(browser): `python3 docs/features/2026-11-21-profile-invest/check_browser.py gallery`
- [x] T44 Check the three together: `<h1>` faces and wordmark faces differ pairwise; B's wordmark centre is 300 px or more right of the others at 1440 and 60 px or more at 390; C's wordmark sits 90 px or more lower than D's; the wordmark sizes differ by 4 px or more at 1440, and C's and D's by 3 px or more at 390; B's `<h1>` is left of the centre, C's centre right of it, D's on it (AC242·AC243·AC244·AC245·AC246·AC247) — verify(browser): `python3 docs/features/2026-11-21-profile-invest/check_browser.py trio`
- [ ] T45 Review the three samples side by side (AC5·AC109·AC110·AC249·AC251) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/compare/` for the three invest samples (command: `python3 docs/features/2026-11-21-profile-invest/check_browser.py compare`). Look at `sheet-trio-1440.png`, `sheet-trio-390.png`, `sheet-trio-thumbs.png` and the six `<slug>-wordmark-1440.png` and `-390.png` crops (without enlarging), and confirm for each of the three pairs: (1) the first screens differ in base colour (cream and dark green; terracotta over a bright photo; violet); (2) the first screens differ in composition (a headline paragraph left of two overlapping photos under a two-row header; two stepped blocks over a photo with the headline inside the wide one; a centred one-line headline over contours with a sheet rising from below); (3) at 1440 the wordmarks differ in position or in size; (4) the wordmarks differ in position, size and typeface, and no two read as one mark with a word changed. Then: (5) the three thumbs show three different first screens: a cream header over a dark green panel with two overlapping black-and-white photos; two terracotta blocks stepping down over a bright room; a violet page of contour lines with a centred headline and a white sheet; (6) each thumb shows what its sample's `-1440.png` shows (the marker text, the wordmark, the headline and its face, the pictures, the buttons and their colours), with nothing present in one and missing in the other
      reason: whether two designs or two marks read as one, and whether a thumbnail shows the page, is a visual judgement.
      scope: profile/invest-robinfamilyoffice, profile/invest-robinwealth, profile/invest-robincapital
      reviewed: PASS @258eee21ed953aad87bae8a72d72c922e2700a68 #5adda020 2026-11-21 — judged profile/invest-robinfamilyoffice 0fc77f2457fa5527cb16a1180863f1d963114fce, profile/invest-robinwealth bb3f578ad2f04b9362676d5ca5a90862648706f2, profile/invest-robincapital d79d0598b79a5ea609cd84dbeebbd0b0d7c8b45e; compare folder current; items 1-6 hold on sheet-trio-1440.png, sheet-trio-390.png, sheet-trio-thumbs.png and the six wordmark crops: base colours and compositions differ in all three pairs, wordmarks differ in position, size and face (B serif 22 px centred, C weight 800 42 px in two lines, D Orbit 30 px at the top left) and none reads as another with a word changed, the three thumbs show three different first screens and each matches its -1440.png with nothing missing
- [x] T46 Keep the branch inside its scope (AC7·AC112) — verify: `base="$(git merge-base main HEAD)" && test -n "$base" && test -z "$(git diff --name-only "$base" | grep -v -e '^profile/invest-robinfamilyoffice/' -e '^profile/invest-robinwealth/' -e '^profile/invest-robincapital/' -e '^profile/index\.html$' -e '^scripts/profiles\.py$' -e '^docs/')$(git diff --name-only "$base" -- docs/profile-playbook.md)" && python3 scripts/build.py >/dev/null && test -z "$(git diff --name-only "$base" -- index.html 404.html cases privacy)"`
- [ ] T47 Compare the twenty-one designs (AC103·AC104·AC250) — verify(human): apply the evidence rule to `/tmp/profile-invest-shots/compare/` for the three invest samples (command: `python3 docs/features/2026-11-21-profile-invest/check_browser.py compare`). Look at `sheet-thumbs.png`, `sheet-all-1440.png`, `sheet-all-390.png` and `sheet-six-390.png`; open the single `<slug>-1440.png` and `<slug>-390.png` files where a sheet is too small to judge. Confirm for each invest sample: (1) beside the eighteen shipped `thumb.jpg` files, its 1440 first screen is not taken for any shipped sample; (2) it differs from its nearest shipped designs in composition, not only in colour: B from `law-ganeum`, `interior-robinhome` and `fitness-jjuuk`; C from `law-goim` and `crypto-robincoin`; D from `crypto-robinchain` and `law-ganeum` (spec A14); (3) beside the 390 first screens of the eighteen shipped samples, its 390 first screen differs in composition, not only in colour; (4) beside the 390 first screens of `food-saebyeokmil`, `clinic-bonui`, `crypto-robincoin`, `law-ganeum`, `crypto-robinchain` and `interior-robinhome`, its 390 first screen is not the usual stack of those six in other colours (a top strip, a bar with the wordmark at the left and a button at the right, a small label, a headline at the left, a paragraph, two buttons side by side and a picture). Shared elements that every sample needs (sample marker, footer credits, the contact links) do not count
      reason: "taken for another design" and "differs in composition" are judgements a person makes.
      scope: profile/invest-robinfamilyoffice, profile/invest-robinwealth, profile/invest-robincapital
      reviewed: PASS @258eee21ed953aad87bae8a72d72c922e2700a68 #11d3869e 2026-11-21 — judged profile/invest-robinfamilyoffice 0fc77f2457fa5527cb16a1180863f1d963114fce, profile/invest-robinwealth bb3f578ad2f04b9362676d5ca5a90862648706f2, profile/invest-robincapital d79d0598b79a5ea609cd84dbeebbd0b0d7c8b45e; compare folder current; items 1-4 hold on sheet-thumbs.png, sheet-all-1440.png, sheet-all-390.png, sheet-six-390.png and the three invest -1440.png shots: no invest first screen is taken for a shipped sample, each differs from its nearest designs of A14 in the placing of wordmark, headline, buttons and picture and not only in colour, at 390 too, and none is the usual stack of the six named samples in other colours

Always last, never removed:

- [x] T48 Reconcile `docs/current_system/` with what shipped (in `profile-samples/component.md`, the Source line lists `invest-robinfamilyoffice`, `invest-robinwealth` and `invest-robincapital`, and the Depends on row says that `invest-robincapital` has no photo), and set `last_reconciled` in `overview.md` to the new HEAD (AC113) — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && python3 docs/features/2026-11-21-profile-invest/check_static.py current`
