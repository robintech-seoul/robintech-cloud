---
status: shipped
test: `python3 docs/features/2026-11-20-profile-interior/check_static.py all`
test(browser): `python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robininterior; a=$?; python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robindesign; b=$?; python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robinhome; c=$?; python3 docs/features/2026-11-20-profile-interior/check_browser.py thumb interior-robininterior; d=$?; python3 docs/features/2026-11-20-profile-interior/check_browser.py thumb interior-robindesign; e=$?; python3 docs/features/2026-11-20-profile-interior/check_browser.py thumb interior-robinhome; f=$?; python3 docs/features/2026-11-20-profile-interior/check_browser.py gallery; g=$?; python3 docs/features/2026-11-20-profile-interior/check_browser.py trio; h=$?; exit $((a|b|c|d|e|f|g|h))`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()" && python3 -c "import urllib.request as u; [u.urlopen(x, timeout=10) for x in ('https://fonts.googleapis.com/css2?family=Do+Hyeon', 'https://fonts.googleapis.com/css2?family=Black+Han+Sans', 'https://fonts.googleapis.com/css2?family=Diphylleia', 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css')]"`
commits: 2540b11e6851837a99c6ff795b2d8c900162ba9e..30706b2080dd0f40f640551e9b6e7ed30721fe30
---

# Interior profile samples (`interior`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the existing `profile-samples` component (spec Scope, `Design: none`). There are no modules to
order. The tasks go sample by sample: A `interior-robininterior`, then B `interior-robindesign`, then C
`interior-robinhome`. Registration, the gallery and the branch come after them. Every command runs from the repository
root. A task names one sample. The tasks of "Gallery, the three together and the branch" check what the three samples
share (the gallery, AC84, AC90–AC92), so they name all three.

The checks live next to this file and were written with it, before any sample exists; until then they fail:

- `check_static.py <check> [<slug>]`: standard library and `sips`; no browser, no network. Without `<slug>`, a
  per-sample check runs for all three samples.
- `check_browser.py page <slug> | thumb <slug> | gallery | trio | compare`: Playwright driving the installed Google
  Chrome. It serves the repository on a free local port itself (never `file://`, playbook §4) and needs the network
  for web fonts, which `preflight(browser)` checks. `compare` is not a check: it saves first-screen shots of the
  samples and of the reference sites for the reviews below, and exits 0 even when a reference site does not answer.

`check_static.py` and `check_browser.py` are approved together with this file. Changing what they check is a change
to approved checks and goes back to a person for re-approval. The Picks are approved with it too; the one exception
is a photo replaced as T11, T24 or T37 directs.

## Picks (agent decisions)

Names, slugs, palettes and faces are spec AC108, AC138, AC169 and A4, A5. Card titles are spec A12.

Photos (free Unsplash, not Unsplash+, or Pexels). The implementer opens Unsplash and Pexels search pages in Chrome
(`mcp__claude-in-chrome__*`), compares candidates on a contact sheet in the scratchpad (not committed), and downloads
only from `images.unsplash.com` and `images.pexels.com`. It never calls `unsplash.com/napi`. Each sample holds four
to six files (AC202).

| Sample | First photo | Other photos |
| --- | --- | --- |
| A | One wide, bright living room or kitchen with no person, cropped to about 1920 × 800. Search: "bright living room interior", "minimal kitchen interior daylight". Not a kitchen island before a walnut wall with a high-rise view (AC137) | Three example cards, one room each: living room, kitchen, bathroom |
| B | No photo on the first screen (AC140). The feature photo is one room with a strong wall or furniture colour, about 1200 × 900. Search: "colorful living room interior", "painted wall interior" | Four example tiles, portrait, one room or detail each, with colour in them |
| C | One wide, calm room in soft daylight (warm wood, linen, plaster), cropped to about 1800 × 800 or wider. Search: "warm minimal living room", "japandi interior". Not a living room with a grand piano, a wall tapestry and an indoor olive tree (AC194) | Three example cards, portrait: living room, kitchen or dining, bedroom |

Interior stock photos often show book spines, posters, framed prints, appliance badges and product labels. The
implementer opens every downloaded file at native resolution (100 % zoom, in quadrants when it is wider than the
screen) before using it, and crops or replaces any file with legible lettering or a logo (AC81).

Page outlines. Every sample has, in this order after its first screen: the service section, the example section,
the process section, the contact section and the footer. A adds the FAQ section between process and contact (AC132).
B adds the colour band (AC157) after its first screen. Copy is written in the implement stage and obeys AC51–AC67.

- **A** (light page): notice strip; white `<header>` with the wordmark at the left, the nav in the centre and the
  dark pill "상담 신청" at the right; the wide photo with its caption link; the `<h1>` under the photo.
- **B** (two colour blocks): notice strip; the pink wordmark block, which holds the `<header>` (or is it) with the
  giant two-line wordmark "로빈 / 디자인" and the nav; the teal headline block with the `<h1>` and the 견적 · 상담 link.
- **C** (ink-blue page): notice strip; `<header>` with the nav at the left, the wordmark in the centre and a
  견적 · 상담 link at the right; the inset photo; the one-line `<h1>` with one `<em>` phrase; the 견적 · 상담 link.

Sizes measured on a fixture on 2026-11-20 (Chrome, real web fonts), as a starting point:

- B at 1440: in a 720 px block, `Black Han Sans` at 230 px sets "디자인" 570 px wide (0.83 em a syllable). Below about
  205 px the widest line is under 70 % of a 720 px block (AC145).
- B at 390: notice 38 px, wordmark at 104 px with the nav under it in a block 281 px high, `<h1>` from 351 px to
  397 px, fixed bar from 788 px (AC154–AC156).
- C at 1440: notice 38 px, header 84 px, photo 1360 × 500 px from 142 px, `<h1>` at 44 px (17 syllables, 796 px wide)
  from 666 px to 723 px, link to 792 px (AC172, AC176, AC178, AC182).

## Fixed parameters of the checks (the page contract)

- **First screen** is 1440×900 and 390×844. "Visible" means inside the viewport, opacity (multiplied up the
  ancestors) above 0.5, and not covered at its centre by an element (or its `::before`/`::after`) painted above it
  with a background image or colour at alpha × opacity above 0.5, judged 1.5 s after load; at each AC44 scroll
  position (every 40 px down to the end, at 390) within 1.5 s. The AC29 and AC51 sentences are judged the same way,
  each scrolled to the middle of the screen, at 1440 and at 390. 390 px overflow (AC97) is judged inside a
  `width:390px` iframe; everything else at 390 in a 390×844 viewport.
- **Markup the checks find by name:** `<a class="wordmark">` in the first `<header>`; A's caption
  `<a class="hero-caption">`; B's `class="wordmark-block"`, `class="headline-block"` (one element each), and in the
  example section one `class="feature"` holding one `class="feature-panel"` and one `<img>`; the example cards and
  tiles are `<figure>` elements with one `<img>` and one `<figcaption>` each, and the example section holds no other
  `<figure>`. Write explicit end tags.
- **Sample notice** (AC8–AC10): the full text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" as real DOM text in one
  element (not CSS `content:`, not split), with the `·` U+00B7, at the body font size or larger and at least 14 px.
  AC12–AC14 read the last `<footer>` that is not inside an `<article>`.
- **Sections** (AC28–AC32 · AC131): each of the service, example, process and contact sections, and A's FAQ, is a
  `<section id="…">` with its own `<h2>`. A check finds a section by that `<h2>`: 서비스, 시공 범위 or 작업 범위; 예시;
  절차 or 과정; 문의 or 상담; 자주 묻는 질문. Exactly one section may match each pattern, so the process heading holds
  neither 문의 nor 상담 ("상담 절차" fails; write "진행 과정"). The service section names its kinds of work as three or
  more `<li>` or `<h3>`. The process steps are the `<li>` children of one `<ol>`. The sentence of AC29 appears once on
  the page, inside the example section, and that section is not nested in another `<section>`.
- **Contact section** (AC33–AC39 · AC46–AC48 · AC51): five separate `<a href="#">` whose accessible names (`aria-label`,
  else text) contain 견적, 카카오톡, 전화, 네이버 예약 and 네이버 지도. A link naming two of them fails AC38. Any link or
  button in the section whose name holds one of these words needs `href="#"`: no `tel:` link, no `<button>`. The
  상담 hours are `HH:MM–HH:MM` (also `-`, `—`, `~`). The closed-days line holds 휴무, 휴관, 쉽니다, 쉬어요, 쉬는 날 or 쉼
  and a day name (일요일, 공휴일, 주말, 토요일 …) in one block, or one of the two in a label of at most 12 characters and
  the other in the next block (`<dt>쉬는 날</dt><dd>일요일 · 공휴일</dd>`), and none of 휴무 없, 에도, 없이, 문의. The section
  shows an address with "(가상 주소)" and `02-000-0000`.
- **Contact links** (AC42–AC44 · AC115 · AC150 · AC182 · AC183): an `<a href="#<contact section id>">` whose text
  contains 견적 or 상담. One is visible on the first screen at 1440 and at 390. For AC115 and AC116 the link is the header 상담 link whose right edge is in the right quarter; for AC150 one link of the headline block with both colours is enough. Below 800 px a fixed or sticky one stays
  on screen at every scroll position; the page's bottom padding is at least its height, so the footer's last text
  line is not covered at the end of the page (AC45). A closed overlay (a mobile menu) is `display: none` or
  `visibility: hidden`: a `position: fixed` layer at `opacity: 0` still counts as covering (AC45 · AC152 · AC156). This link sits outside the contact section. For AC182 the link
  is outside `<header>` and outside every `position: fixed` or `sticky` element less than a quarter of the screen high.
- **Header nav** (AC113 · AC151 · AC195): the first `<header>` holds a `<nav>`; every `<a>` in it has Hangul text and
  no Latin letter. In A and B it has four or more links, each with an `href` starting with `#`.
- **Faces** (AC71 · AC112 · AC127 · AC146 · AC149 · AC179 · AC185 · AC197–AC200): the checks read the first family of
  the computed `font-family`; the link's own `font-family` is the wordmark face. AC71 also needs the main font Chrome
  renders for the `<h1>` and the `a.wordmark` (CDP `CSS.getPlatformFontsForNode`) to be the sample's display face, loaded as a web font: a face that never
  loads, a fallback that draws the text (`display=optional`), or a copy installed on the machine, fails. `index.html` asks `fonts.googleapis.com` for the sample's one
  family and no other, and for nothing else there (no `/icon?family=`; a preconnect hint is fine) (AC197). Every element set in `Do Hyeon`, `Black Han Sans` or `Diphylleia` has
  `font-weight: 400`; headings are bold by default, so the rule that sets the face also sets the weight, and no
  `<strong>` or `<b>` sits inside such an element (AC198). `<body>` and the elements that show the 상담 hours and the
  phone number in the contact section start their stack with `"Pretendard Variable"` or `Pretendard` (AC199 · AC200).
  In C no element in `Diphylleia` holds a digit; an `<ol>` there is not set in `Diphylleia` (AC190).
- **Body colours** (AC109 · AC139 · AC170): the last `background`/`background-color` and the last `color` in a
  top-level `body` rule of `style.css`, each one colour written as hex or `rgb()`, or a `var()` that `:root` or `html`
  defines so. Rules inside `@media` are not read.
- **B's backgrounds** (AC165): the check reads every `background`, `background-color` and `background-image` value in
  `style.css`, `<style>` and `style=""`, at any nesting (`:hover`, `@media`, CSS nesting), with `var()` resolved from every
  rule that defines the property; a property defined twice is read with each value. Write
  every colour there as hex or `rgb()`/`rgba()` with plain numbers. A named colour, `hsl()`, `currentcolor` or an
  undefined `var()` fails, because the check cannot read it. A colour whose channel spread is above `0x30` must be one
  of the three and opaque: `rgba(238, 104, 174, 0.5)` fails. `#1b1430` and `#f8f1fb` are below the spread and are free.
- **Contrast** (AC201): for every visible element with its own text, the text colour (with its alpha and the opacity
  of its ancestors) against the background colours of its ancestors, composited down to the first opaque one, with
  every `<details>` opened. Text whose box overlaps an `<img>` is left to the screenshot reviews, unless it is in a
  fixed or sticky element. Text over a CSS `background-image` (a gradient too) fails, because the check cannot judge
  it: put photos in `<img>` and text on flat colours. Write colours so that Chrome computes them as `rgb()`.
- **Measured boxes:** the wordmark's size in AC145, the band paragraph's centre in AC158 and the `<h1>`'s centre in
  AC176 are those of the rendered text (the union of its text nodes' line boxes), so `display: block` on the element or on a child `<span>` does not widen
  them. The one-line checks (AC123 · AC178) read the element's own box: give A's caption link no vertical padding
  (pad its wrapper) and keep C's `<h1>` `line-height` at 1.6 or less. An element "with its own text" (AC124 · AC135 ·
  AC175 · AC190 · AC201) has a non-blank text node as a direct child.
- **A first photo** (AC118–AC124): the first `<img>` of the page. Its parent element holds that one `<img>`, the
  caption (inside a wrapper if needed) and no `<button>`. The caption is the only link inside the photo's box. The `<img>` is not wrapped in `<picture>`.
- **A digits** (AC135): at 1440 no element whose own text holds a digit is set above 24 px; a `::before`/`::after`
  whose `content` holds a digit or a `counter(` counts too, and so does the `::marker` of a `decimal` list item.
- **B first screen** (AC140 · AC152): on load at 1440 no visible `<img>` and no element (or `::before`/`::after`) with
  a `background-image`, a gradient included, intersects the viewport; `<html>` and `<body>` count.
- **Page text** (AC25–AC27 · AC52–AC62) is the text of `index.html` outside `script`, `style`, `template` and `title`,
  plus image `alt`, the `<title>` text, `meta` description and `og:` content, `aria-label` and `title` attributes, the
  strings of CSS `content:` declarations (`style.css`, `<style>` and `style=""`; a `content:` with `attr()` fails), and the string literals of inline `<script>` that hold Hangul, `<`, `@`, `₩`
  or a space; whitespace collapsed, matched as plain substrings; a listed word with a space also matches without it (책임시공, 하자없, 시공사례 in an `alt`). AC55, AC60, AC61 and the Latin words of AC52 and AC53
  ignore case; LG and LX match as whole words. AC67 reads `alt` only. Words that hit in an allowed sense are
  rewritten, not exempted. Traps confirmed on the fixture: 필수상담 and 수상한 (수상), 업무상 (무상), 스타일룸 (일룸),
  거실장 in an `alt` (실장), 최대한 and 최고급 (최대, 최고), 보장 and 보증 even in "보장하지 않습니다", 인증 in any sense,
  any Latin word holding "after" or "before" (aftercare; `::after` in a script string too), 삼성동 (삼성), 숨고르기 (숨고), ★ as decoration.
- **Digits in copy** (AC58 · AC59) are read per block (a `p`, `li`, `dd`, heading …; the `<title>`, each attribute
  and each CSS `content:` string is its own block), full-width digits folded. AC58 fails on a digit directly before
  평, 건, 세대, 가구, 곳, 명, 년, 개월, 주 or 일, on a digit, optional spaces, then 억, 만 or 원 (also after 천, 백 or 십),
  on `₩` or `￦` before a digit, a digit before `KRW`, and a thousands comma. Traps confirmed on the fixture: "결로 1
  원목", "19:00 만나서", "02-000-0000 원하시는", a step number before 주방, 일정 or 원목
  (`<span>1</span>주방`), `rootMargin: '0px 0px -10% 0px'` in a script string (break the block or reword; use px). "02-000-0000 평일 10:00–19:00" passes.
- **Numbers** (AC20 · AC22–AC24): addresses are block text matching `<한글>로|길 <번호>`, `<한글>동N가 <번호>` or
  `<번호> 번지`; every such block holds "(가상 주소)". Every phone number is `02-000-0000`; a `tel:` link dials
  020000000 (`tel:02-000-0000`). 사업자등록번호 is `000-00-00000`. AC24 fails on 등록번호 without 사업자 before it, on 면허번호, 허가번호,
  신고번호, 인가번호, on 공사업, 건설업 or 통신판매(업) directly before 등록, 신고 or 면허, on any `제 <number> 호` (zeros too),
  and on a non-zero number after 등록 or 면허. "사업자 등록번호" with a space passes.
- **Reference names and faces** (AC82 · AC136 · AC167 · AC192): substrings of `index.html` and `style.css`, case
  ignored, class names and comments included. A: apartmentary, 아파트멘터리, `decimal`, `spoqa`, so A writes no
  `list-style: decimal` and no `counter(…, decimal)` (an `<ol>` is decimal by default). B: studio ashby, studioashby,
  애쉬비, 애시비, `beaux`, `allrounder`, `matter`. C: mcgee, 맥기, `ftbureau`, `jost`, `schibsted`.
- **Images** (AC2 · AC68 · AC69 · AC73): every `src`/`srcset` of `<img>` and `<source>`, every `poster` and every CSS
  `url()` resolves to a file in `img/`, with the same letter case. A `cdn.jsdelivr.net` URL must hold `pretendard` in
  its path. AC69 skips `http://www.w3.org/` (an inline SVG namespace). Scripts are inline: a `<script src>` fails, because the copy checks read inline scripts only.
- **Thumbnail** (AC5): `check_browser.py thumb` compares `thumb.jpg` with a fresh 1440×900 first screen (both scaled
  to 160×100, mean absolute RGB difference at most 15 of 255 over the image and at most 40 in every 10×10 tile). It
  catches a changed photo, colour or layout, not a changed line of text, so re-running `profile_thumb.py` after a
  first-screen text change is the implementer's step. The thumbnail is shot from `file://` with 6 s of virtual time,
  the check over http at 1.5 s, so the first screen must not depend on module scripts or `fetch`, must not
  auto-advance, and its entrance effects end within 1.5 s. Make the thumbnail last, after the sample's visual work.
- **Screenshots** for the reviews go to `/tmp/profile-interior-shots/<slug>/`: `desktop-1440.png` and
  `mobile-390.png` (full page, after a scroll through), the same cut into 1200 px tall bands (`desktop-1440-01.png` …),
  and `summary.txt` written last (`site tree` = `git rev-parse HEAD:profile/<slug>`, `site working tree` clean, dirty
  or unknown, the page heights, `result PASS|FAIL`). `compare` rewrites `/tmp/profile-interior-shots/compare/`:
  `<slug>-1440.png` and `<slug>-390.png` first screens for the three interior samples and the twelve shipped samples;
  full pages of the twelve shipped samples (`<slug>-1440-full.png`, `<slug>-390-full.png` and their `-NN` bands);
  `ref-<slug>.png` (1440 first screen), `ref-<slug>-full.png` and its `-NN` bands and `ref-<slug>.txt` (visible text)
  of each sample's reference home page, keeping the last good copy when a site does not answer; and `summary.txt`
  with a `local <slug> tree <hash> clean|dirty` line per sample and a
  `reference <slug> <url> ok|cached <date>|unreachable` line per reference.
- **Gallery** (AC100 · AC101 · AC103–AC105): AC100 · AC101 after one click on the 인테리어 chip; AC103–AC105 for each
  card on a fresh load of `/profile/`. AC103 needs the iframe `src` to end in `/profile/<slug>/` and the loaded frame
  to be that page with a `header a.wordmark`.
- **Evidence rule** for the reviews: a sample's page folder `/tmp/profile-interior-shots/<slug>/` is current when its
  `summary.txt` exists, its `site tree` equals `git rev-parse HEAD:profile/<slug>` and its `site working tree` is
  `clean`; the compare folder is current for a sample when `compare/summary.txt` has that sample's `local` line with
  the same tree and `clean`. A review uses a current folder as it is and runs the named command only when the folder
  is not current. That command starts a browser, so it runs only when a person asked for browser checks (AGENTS.md
  §6-5); otherwise the evidence is missing and the review is UNSURE, noting that it needs a browser run. If the folder
  is still not current after the run, the review is UNSURE. A `cached` reference is evidence. An `unreachable`
  reference does not by itself make a review UNSURE: the review then judges the reference items against the spec's
  description of that reference (the Candidate A, B or C text and sketch, and AC137, AC148, AC153, AC194) and says so
  in its note. The photo-lettering reviews (AC81) read the files in `profile/<slug>/img/` directly, need no browser,
  and are current only while `git rev-parse HEAD:profile/<slug>/img` equals the hash in their note.

## Sample A — 로빈인테리어 (`profile/interior-robininterior/`)

- [x] T1 Pick photos for A as in Picks: download the picks at web size into `img/`, write `img/sources.txt` (a download URL without a readable photo ID fails AC72; write the photo page URL without a locale part such as `/ko-kr/` or `/ko/`, not `-`); open every downloaded file at 100 % and crop or replace any with legible lettering or a logo before going on (AC72·AC74·AC75·AC76·AC77·AC78·AC79·AC202) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py photos interior-robininterior`
- [x] T2 Write `index.html` and `style.css` with the sample notice (on the first screen and in the footer), a `<title>` with 디자인 샘플, noindex, footer credits, a 로빈 wordmark without Latin letters, fictional address, phone and 사업자등록번호, and no other registration number (AC8·AC12·AC13·AC14·AC15·AC16·AC18·AC20·AC22·AC23·AC24·AC196) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py markers interior-robininterior`
- [x] T3 Build the page structure: the service, example, process and contact sections, the example notice, the five `href="#"` contact controls with hours, closed days, address, phone and the AC51 sentence, a Hangul header nav, no form or field (AC28·AC29·AC30·AC31·AC32·AC33·AC34·AC35·AC36·AC37·AC38·AC39·AC40·AC41·AC46·AC47·AC48·AC51·AC195) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py structure interior-robininterior`
- [x] T4 Keep the copy free of chain words, superlatives, awards, reviews, before/after, lures, warranty and safety claims, figures, brand and complex names, staff words in `alt`, outside e-mail addresses, handles and domains (AC25·AC26·AC27·AC52·AC53·AC54·AC55·AC56·AC57·AC58·AC59·AC60·AC61·AC62·AC67) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py copy interior-robininterior`
- [x] T5 `word-break: keep-all`, alt text, one Korean `<h1>`, no skipped heading level (AC49·AC50·AC93·AC94) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py a11y interior-robininterior`
- [x] T6 Keep the sample self-contained: relative paths only, images only from `img/`, `Do Hyeon` as the one Google Fonts family and Pretendard on jsDelivr, no other `http(s)://` URL, nothing naming Apartmentary (AC1·AC2·AC68·AC69·AC73·AC82·AC197) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py assets interior-robininterior`
- [x] T7 Give A its kept traits in markup: the light `body` colours, a header nav of four or more `#` links, one static first photo with the 예시 caption link, three example cards, the FAQ of four or more `<details>` between process and contact, neither `Decimal` nor `Spoqa` (AC109·AC113·AC120·AC121·AC122·AC128·AC131·AC132·AC136) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py sample interior-robininterior`
- [x] T8 Check A in a browser at 1440 and 390: sample notice and its size, the example and fictional-business notices visible, a 견적 · 상담 link on the first screen and at every scroll position at 390 with the footer's last line uncovered, computed `keep-all`, digit faces, web fonts loaded, weights and Pretendard, contrast, no motion under reduced motion, no horizontal overflow; the white header with left wordmark, centred nav and dark pill, the wide photo under it with one caption link and no other text, the `<h1>` under the photo, the card row, the dark footer, no digit above 24 px; writes the screenshots for T9–T13 (AC8·AC9·AC10·AC29·AC51·AC42·AC43·AC44·AC45·AC49·AC70·AC71·AC95·AC96·AC97·AC110·AC111·AC112·AC114·AC115·AC116·AC117·AC118·AC119·AC121·AC123·AC124·AC126·AC127·AC129·AC130·AC134·AC135·AC198·AC199·AC200·AC201) — verify(browser): `python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robininterior`
- [ ] T9 Review A's content (AC21·AC60·AC61·AC63·AC64·AC65·AC66·AC133·AC204) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/interior-robininterior/` (command: `python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robininterior`). Read `profile/interior-robininterior/index.html` and `style.css` (for CSS `content:` text) and the `interior-robininterior` entry of `scripts/profiles.py`, look at the bands `desktop-1440-NN.png` and `mobile-390-NN.png` in that folder, and confirm each: (1) every address names a district or road that does not exist (for example 가상구 결로), not a real road with a building number, and no real 구, 동, 신도시 or neighbourhood is named as the business's location or service area (a 시 or 도 name alone is fine); (2) no real interior, furniture, appliance, material or platform brand is named other than 네이버 and 카카오톡, and no social or video platform (인스타그램, 유튜브, 네이버 블로그 and the like) appears by name, logo or icon (지인, 이건 and 오브제 as ordinary words are fine), and no real apartment brand, complex or building is named anywhere on the page (for example 자이, 한남더힐, 헬리오시티); (3) no person's name anywhere, as designer, 대표, 실장, 시공 팀 or customer, and no photo captioned or labelled as a staff member, a customer or a customer's home; (4) no example photo is labelled with a real place, a complex, a floor area, a budget, a work period or a client, and the page states no project count, years in business, price or period, in words or in digits (for example 수백 곳, 십 년, 한 달 만에, 20여 년, 300채, Since 2009, 프로젝트 300+); (5) no testimonial, no quote attributed to a person, no star rating, no partner, press or product-brand logo, no mention of a partner, of press or broadcast coverage or of returning customers (for example 방송에 소개된, 건설사 협력사, 다시 찾는 고객), no award, licence or association claim, no before/after pair of photos; (6) no superlative, guarantee, award or certificate, review or score, before/after, lure, warranty or material-safety claim in other words or in English (for example 가장, 손꼽히는, 확실한, 끝까지 책임, 건강한 자재, best, guaranteed), and the example photos are not presented as the business's own completed projects (우리가 완성한, 실제 시공); (7) no FAQ question or answer states a cost, a work period, a warranty or after-service term or a discount, in digits or in words; (8) the `title`, `summary` and `features` of this sample's entry in `scripts/profiles.py` pass items (2)–(6)
      reason: whether copy names a person or a brand, implies a count, a testimonial or a claim in other words is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/interior-robininterior, scripts/profiles.py
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #88a04f81 2026-11-20 — (1)-(8) pass on index.html, style.css, bands desktop-1440-01..04 and mobile-390-01..05, profiles.py:172-181: only address '서울 가상구 결로 12 (가상 주소)' (index.html:163, :172); platforms only 카카오톡 · 네이버 예약 · 네이버 지도; no person, count, price, period, testimonial or claim; FAQ (:123-142) states no cost, period, warranty or discount; examples disclaimed at :73
- [ ] T10 Review A's photos (AC80·AC89·AC137) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/interior-robininterior/` and to `/tmp/profile-interior-shots/compare/` for interior-robininterior (commands: `python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robininterior`, `python3 docs/features/2026-11-20-profile-interior/check_browser.py compare`). Open every image in `profile/interior-robininterior/img/`, `compare/interior-robininterior-1440.png` and `-390.png`, and `ref-interior-robininterior.png` with its `-full-NN` bands, and confirm: (1) every photo shows a home interior, a material or a detail of one; (2) no photo shows a recognisable project of apartmentary.com; (3) the first photo neither is nor imitates a photo on apartmentary.com; (4) the first photo shows no person, and it is not a kitchen island before a walnut wall with a high-rise view through the window
      reason: subject and likeness to another photo are visual judgements.
      scope: profile/interior-robininterior
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #71a88569 2026-11-20 — folders current (site tree c61cbd44, compare ok 2026-11-20); (1)-(4) pass: four photos are living room, living room, kitchen, bathroom; none matches the four photos in the Apartmentary capture; hero-living.jpg is a white living room with no person, no kitchen island, walnut wall or high-rise view; only the captured slide of the reference slider was seen
- [ ] T11 Inspect A's photos for lettering at native resolution (AC81) — verify(human): open every image file in `profile/interior-robininterior/img/` one by one at 100 % zoom (not on the page, not on a contact sheet; for a file wider than the screen, view it in quadrants), and confirm each shows no legible logo, brand name, signage, product label, appliance badge, book-spine or magazine title, poster or framed lettering, or other lettering. On a hit, the implementer crops or replaces the file, updates `img/sources.txt`, re-runs T1, T8, T40 and T41, and the review starts again. Name each file checked and record `git rev-parse HEAD:profile/interior-robininterior/img` in the note; the review counts only while that hash is unchanged
      reason: lettering in a photo is seen only by eye at full size; the fitness verdict failed once on lettering seen only there.
      scope: profile/interior-robininterior/img
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #aa34514b 2026-11-20 — img tree 53367c9d0581e8bc253bffb1a07bae5d47987387; 28 tiles of 500x500 at 1:1 over the whole area: card-bath.jpg 1200x900 (6), card-kitchen.jpg 1200x900 (6), card-living.jpg 1200x900 (6), hero-living.jpg 1920x800 (10); no legible lettering, logo or badge; bottle labels in card-bath and the oven panel in card-kitchen show shapes only, unreadable also at 4x
- [ ] T12 Review A's full-page screenshots (AC11·AC98·AC99·AC125) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/interior-robininterior/` (command as in T9). Look at `desktop-1440-NN.png` and `mobile-390-NN.png` band by band and at the seams between bands, and confirm: (1) at 1440, no text overlaps other text, an image or a control so that letters are hidden; (2) at 1440, no text is cut off at a box edge; (3) and (4) the same at 390; (5) the sample notice on the first screen reads in a colour that stands out clearly from its background, at 1440 and at 390; (6) the caption on the first photo reads clearly against the photo, at 1440 and at 390. The fixed bottom bar appears once in a full-page shot; what it covers there is not counted
      reason: whether text overlaps, is clipped or reads clearly on a photo is a visual judgement over the rendered page.
      scope: profile/interior-robininterior
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #3ad8ee60 2026-11-20 — folder current (site tree c61cbd44, clean); (1)-(6) pass on desktop-1440-01..04, mobile-390-01..05 and all seams cropped at 1:1: no overlapping or clipped text; notice is near-white on rgb(22,24,27) at both widths; caption '거실 예시 · 공간 예시 보기' sits in an opaque dark box on the photo; fixed bar at mobile-390-01 y786-844 not counted
- [ ] T13 Compare A with Apartmentary (AC82·AC83·AC85·AC88) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/compare/` for interior-robininterior and to `/tmp/profile-interior-shots/interior-robininterior/` (commands: `python3 docs/features/2026-11-20-profile-interior/check_browser.py compare`, `python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robininterior`). Compare `interior-robininterior-1440.png` and `-390.png` with `ref-interior-robininterior.png`, the bands of the sample with the `ref-interior-robininterior-full-NN.png` bands, and `ref-interior-robininterior.txt` with the text of `profile/interior-robininterior/index.html`, and confirm: (1) the sample shows no logo, wordmark or brand name of the reference; (2) no sentence of the reference appears in the sample; (3) no photo on the sample is one of the reference's photos; (4) side by side the two do not read as the same site: they differ in at least two of wordmark face, headline face and place, accent colour, photo subject, section order (the kept traits of item 6 do not count); (5) the sample's `<h1>` is not a translation or close paraphrase of the reference's headline; (6) the sample keeps each trait listed for Candidate A under "Traits to keep" in the spec: a white bar header with the wordmark at the left, a centred Korean nav and a dark pill 상담 button at the right; one wide photo directly under the header with a caption line on it; a three-card photo row; an FAQ accordion
      reason: copied wording, logos, "reads as the same site" and "keeps the trait" are judgements a person makes.
      scope: profile/interior-robininterior
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #14fd9b07 2026-11-20 — folders current, reference ok 2026-11-20; (1)-(6) pass: no Apartmentary name or logo in index.html/style.css; no shared sentence (only the button label '상담 신청', index.html:28, equals the reference's header button); photos differ from the four visible reference photos; differs in wordmark face, headline face and place, accent colour, photo subject and section order; h1 (:38) is not the reference headline; four kept traits present at 1440

## Sample B — 로빈디자인 (`profile/interior-robindesign/`)

- [x] T14 Pick photos for B as in Picks, as in T1 (AC72·AC74·AC75·AC76·AC77·AC78·AC79·AC202) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py photos interior-robindesign`
- [x] T15 Write `index.html` and `style.css` with the markers as in T2 (AC8·AC12·AC13·AC14·AC15·AC16·AC18·AC20·AC22·AC23·AC24·AC196) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py markers interior-robindesign`
- [x] T16 Build the page structure as in T3 (AC28·AC29·AC30·AC31·AC32·AC33·AC34·AC35·AC36·AC37·AC38·AC39·AC40·AC41·AC46·AC47·AC48·AC51·AC195) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py structure interior-robindesign`
- [x] T17 Keep the copy clean as in T4 (AC25·AC26·AC27·AC52·AC53·AC54·AC55·AC56·AC57·AC58·AC59·AC60·AC61·AC62·AC67) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py copy interior-robindesign`
- [x] T18 keep-all, alt, headings and Korean `<h1>` as in T5 (AC49·AC50·AC93·AC94) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py a11y interior-robindesign`
- [x] T19 Keep the sample self-contained as in T6, with `Black Han Sans` as the one Google Fonts family and nothing naming Studio Ashby (AC1·AC2·AC68·AC69·AC73·AC82·AC197) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py assets interior-robindesign`
- [x] T20 Give B its kept traits in markup: the lilac-white `body` colours, the live-text wordmark 로빈디자인 inside the header and the wordmark block and named once, a header nav of four or more `#` links, the feature panel with a Hangul heading and one paragraph, four example tiles and five example photos, only the three saturated background colours, none of Studio Ashby's colours or faces (AC139·AC144·AC151·AC160·AC161·AC164·AC165·AC166·AC167) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py sample interior-robindesign`
- [x] T21 Check B in a browser at 1440 and 390, the common checks as in T8 and B's: a first screen with no photo, two colour blocks side by side at least 720 px high in pink and teal, the giant two-line wordmark in `Black Han Sans`, the `<h1>` and the pink 견적 · 상담 link in the headline block, the nav visible, no gate, the page longer than 1800 px; at 390 the blocks stacked with the wordmark at 90 px or more in a block of at most 420 px and the `<h1>` on the first screen; the lilac band with one centred paragraph, the colour panel beside a photo, the four-tile row and its two rows of two at 390; writes the screenshots for T22–T26 (AC8·AC9·AC10·AC29·AC51·AC42·AC43·AC44·AC45·AC49·AC70·AC71·AC95·AC96·AC97·AC140·AC141·AC142·AC143·AC145·AC146·AC147·AC149·AC150·AC151·AC152·AC154·AC155·AC156·AC157·AC158·AC159·AC162·AC163·AC198·AC199·AC200·AC201) — verify(browser): `python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robindesign`
- [x] T22 Review B's content (AC21·AC60·AC61·AC63·AC64·AC65·AC66·AC204) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/interior-robindesign/` (command: `python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robindesign`), read `profile/interior-robindesign/index.html`, `style.css` and the `interior-robindesign` entry of `scripts/profiles.py`, look at the bands, and confirm items (1)–(6) and (8) of T9 for this sample; in (4) the feature panel's heading and paragraph count as labels of the feature photo
      reason: whether copy names a person or a brand, implies a count, a testimonial or a claim in other words is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/interior-robindesign, scripts/profiles.py
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #b0aed1f9 2026-11-20 — (1)-(6) and (8) pass on index.html, style.css (no content: text), bands desktop-1440-01..04 and mobile-390-01..04, profiles.py:183-192: only address '서울 가상구 물감길 7 (가상 주소)' (index.html:117, :125); platforms only 카카오톡 · 네이버 예약 · 네이버 지도; feature panel heading and paragraph (:78-79) and tile captions (:84-87) name rooms and colours only; no person, count, testimonial or claim; examples disclaimed at :74
      확인: Seokhyun Kim 2026-11-20
- [x] T23 Review B's photos (AC80·AC168) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/interior-robindesign/` and to `/tmp/profile-interior-shots/compare/` for interior-robindesign (commands as in T10, with `page interior-robindesign`). Open every image in `profile/interior-robindesign/img/`, `compare/interior-robindesign-1440.png` and `-390.png`, and `ref-interior-robindesign.png` with its `-full-NN` bands, and confirm: (1) every photo shows a home interior, a material or a detail of one; (2) no photo shows a recognisable project of studioashby.com; (3) the feature photo (the one beside the colour panel) neither is nor imitates a photo on studioashby.com
      reason: subject and likeness to another photo are visual judgements.
      scope: profile/interior-robindesign
      reviewed: FAIL(behavior) @30706b2080dd0f40f640551e9b6e7ed30721fe30 #20685910 2026-11-20 — (1) FAIL: img/feature-teal.jpg (the feature photo, index.html:81, alt says 거실) does not read as a home interior but as a showroom or lobby furniture display: wall more than 2.5x the seat-back height with the ceiling out of frame, a large commercial ventilation grille, modular bench seating with tall panel backs, three pedestal side tables, terrazzo floor, no window, door or sign of living; the four tiles pass (1). (2) PASS and (3) PASS against the seven photos visible in the Studio Ashby capture
      확인: Seokhyun Kim 2026-11-20
- [x] T24 Inspect B's photos for lettering at native resolution, as in T11 (AC81) — verify(human): as in T11, for every image file in `profile/interior-robindesign/img/` (on a hit, re-run T14, T21, T42 and T43), recording `git rev-parse HEAD:profile/interior-robindesign/img`
      reason: lettering in a photo is seen only by eye at full size; the fitness verdict failed once on lettering seen only there.
      scope: profile/interior-robindesign/img
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #3629a82e 2026-11-20 — img tree 700c010728d8f891319da8aa86063b5021c3ea44; 20 tiles of 700x700 at 1:1 over the whole area: feature-teal.jpg 1200x900 (4), tile-bath.jpg 800x1000 (4), tile-bed.jpg 800x1000 (4), tile-kitchen.jpg 720x900 (4), tile-living.jpg 800x1000 (4); no legible lettering, logo or badge; the pump bottle print in tile-bath, three furniture tags in feature-teal and an embossed mark on a moka pot in tile-kitchen are unreadable also enlarged
      확인: Seokhyun Kim 2026-11-20
- [x] T25 Review B's full-page screenshots and first screen (AC11·AC98·AC99·AC148·AC153) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/interior-robindesign/` (command as in T22), and confirm items (1)–(5) of T12 on its `desktop-1440-NN.png` and `mobile-390-NN.png`; (6) the lines of the giant wordmark start at one left edge, at 1440 and at 390 (not staggered like "STU / DIO / ASH / BY"); (7) the first screen names one business: no second brand name, no brand mark or emblem
      reason: whether text overlaps or is clipped, whether lines align and whether a mark reads as a second brand are visual judgements.
      scope: profile/interior-robindesign
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #e16d75aa 2026-11-20 — folder current (site tree 9c343e8a, clean); (1)-(7) pass on desktop-1440-01..04, mobile-390-01..04 and all seams: no overlapping or clipped text; notice near-white on rgb(27,20,48); wordmark lines start at x=70/70 at 1440 and x=27/27 at 390; first screen names only 로빈디자인, no mark or emblem (index.html:18-38 holds no img or svg); fixed bar at mobile-390-01 y788-844 not counted
      확인: Seokhyun Kim 2026-11-20
- [x] T26 Compare B with Studio Ashby (AC82·AC83·AC85·AC88) — verify(human): as in T13 for interior-robindesign (`interior-robindesign-1440.png`, `-390.png`, `ref-interior-robindesign*`), confirming items (1)–(3) of T13 against Studio Ashby; (4) side by side the two do not read as the same site: they differ in at least two of the block colours, the wordmark's script and face, what the second block holds, navigation, section order (the kept traits of item 6 do not count); (5) the sample's `<h1>` is not a translation or close paraphrase of a Studio Ashby headline; (6) the sample keeps each trait listed for Candidate B under "Traits to keep" in the spec: a first screen split into two flat saturated colour blocks with no photo; a giant stacked wordmark that fills one block; a full-width colour band with one centred paragraph; a colour block beside a photo for a featured example; a four-tile photo row
      reason: copied wording, logos, "reads as the same site" and "keeps the trait" are judgements a person makes.
      scope: profile/interior-robindesign
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #1d2d4014 2026-11-20 — folders current, reference ok 2026-11-20; (1)-(6) pass: no Studio Ashby name, wordmark or mark; ref text is all English, no shared sentence; five photos differ from the reference photos seen; differs in block colours, wordmark script and face, second block, navigation and section order; h1 '색 하나로 달라지는 집' (index.html:33) is no reference headline; five kept traits present at 1440
      확인: Seokhyun Kim 2026-11-20

## Sample C — 로빈홈 (`profile/interior-robinhome/`)

- [x] T27 Pick photos for C as in Picks, as in T1 (AC72·AC74·AC75·AC76·AC77·AC78·AC79·AC202) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py photos interior-robinhome`
- [x] T28 Write `index.html` and `style.css` with the markers as in T2 (AC8·AC12·AC13·AC14·AC15·AC16·AC18·AC20·AC22·AC23·AC24·AC196) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py markers interior-robinhome`
- [x] T29 Build the page structure as in T3 (AC28·AC29·AC30·AC31·AC32·AC33·AC34·AC35·AC36·AC37·AC38·AC39·AC40·AC41·AC46·AC47·AC48·AC51·AC195) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py structure interior-robinhome`
- [x] T30 Keep the copy clean as in T4 (AC25·AC26·AC27·AC52·AC53·AC54·AC55·AC56·AC57·AC58·AC59·AC60·AC61·AC62·AC67) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py copy interior-robinhome`
- [x] T31 keep-all, alt, headings and Korean `<h1>` as in T5 (AC49·AC50·AC93·AC94) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py a11y interior-robinhome`
- [x] T32 Keep the sample self-contained as in T6, with `Diphylleia` as the one Google Fonts family and nothing naming Studio McGee (AC1·AC2·AC68·AC69·AC73·AC82·AC197) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py assets interior-robinhome`
- [x] T33 Give C its kept traits in markup: the ink-blue `body` colours, an `<h1>` with one Hangul `<em>` phrase and text outside it, three example cards, none of Studio McGee's colours or faces, no shop or blog word in a heading or nav link (AC170·AC180·AC181·AC187·AC191·AC192·AC193) — verify: `python3 docs/features/2026-11-20-profile-interior/check_static.py sample interior-robinhome`
- [x] T34 Check C in a browser at 1440 and 390, the common checks as in T8 and C's: the header in the page colour with the centred `Diphylleia` wordmark and a 견적 · 상담 link, the wide inset photo with equal side gaps and square corners and no text on it, the centred one-line `<h1>` under it on the page colour with one accent-coloured upright `<em>`, a 견적 · 상담 link on the first screen outside the header, the light example section with three cards in a row and in one column at 390, no digit in `Diphylleia`; writes the screenshots for T35–T39 (AC8·AC9·AC10·AC29·AC51·AC42·AC43·AC44·AC45·AC49·AC70·AC71·AC95·AC96·AC97·AC171·AC172·AC173·AC174·AC175·AC176·AC177·AC178·AC179·AC180·AC182·AC183·AC184·AC185·AC186·AC188·AC189·AC190·AC198·AC199·AC200·AC201) — verify(browser): `python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robinhome`
- [ ] T35 Review C's content (AC21·AC60·AC61·AC63·AC64·AC65·AC66·AC204) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/interior-robinhome/` (command: `python3 docs/features/2026-11-20-profile-interior/check_browser.py page interior-robinhome`), read `profile/interior-robinhome/index.html`, `style.css` and the `interior-robinhome` entry of `scripts/profiles.py`, look at the bands, and confirm items (1)–(6) and (8) of T9 for this sample
      reason: whether copy names a person or a brand, implies a count, a testimonial or a claim in other words is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/interior-robinhome, scripts/profiles.py
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #0c98e97c 2026-11-20 — (1)-(6) and (8) pass on index.html (no svg, no script), style.css (no content: text), bands desktop-1440-01..04 and mobile-390-01..05, profiles.py:193-203: only address '서울 가상구 볕길 3 (가상 주소)' (index.html:101, :109); platforms only 카카오톡 · 네이버 예약 · 네이버 지도; captions 거실 / 다이닝 / 침실 only; no person, count, testimonial or claim; examples disclaimed at :58
- [ ] T36 Review C's photos (AC80·AC89·AC194) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/interior-robinhome/` and to `/tmp/profile-interior-shots/compare/` for interior-robinhome (commands as in T10, with `page interior-robinhome`). Open every image in `profile/interior-robinhome/img/`, `compare/interior-robinhome-1440.png` and `-390.png`, and `ref-interior-robinhome.png` with its `-full-NN` bands, and confirm: (1) every photo shows a home interior, a material or a detail of one; (2) no photo shows a recognisable project of studio-mcgee.com; (3) the first photo neither is nor imitates a photo on studio-mcgee.com; (4) the first photo is not a living room with a grand piano, a wall tapestry and an indoor olive tree
      reason: subject and likeness to another photo are visual judgements.
      scope: profile/interior-robinhome
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #53b0b022 2026-11-20 — folders current (site tree cd99058f, compare ok 2026-11-20); (1)-(4) pass: four images are interiors (low-table room, living, dining, bedroom; the three cards look like 3D renders); none matches the scenes in the Studio McGee capture; hero-floor-table.jpg has no grand piano, tapestry or olive tree; only the captured hero frames of the reference were seen
- [ ] T37 Inspect C's photos for lettering at native resolution, as in T11 (AC81) — verify(human): as in T11, for every image file in `profile/interior-robinhome/img/` (on a hit, re-run T27, T34, T44 and T45), recording `git rev-parse HEAD:profile/interior-robinhome/img`
      reason: lettering in a photo is seen only by eye at full size; the fitness verdict failed once on lettering seen only there.
      scope: profile/interior-robinhome/img
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #0368c55e 2026-11-20 — img tree aee9ae11174d639897c4fc30afddd6ab1c1d45b1; 20 tiles of 600x600 at 1:1 over the whole area: card-bed.jpg 720x900 (4), card-dining.jpg 720x900 (4), card-living.jpg 800x1000 (4), hero-floor-table.jpg 1800x720 (8); no legible lettering, logo or badge; the books on the shelf in card-living show colour fields only, also at 4x; the wall clock in card-bed has no numerals
- [ ] T38 Review C's full-page screenshots (AC11·AC98·AC99) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/interior-robinhome/` (command as in T35), and confirm items (1)–(5) of T12 on its `desktop-1440-NN.png` and `mobile-390-NN.png`
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page.
      scope: profile/interior-robinhome
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #56360fa2 2026-11-20 — folder current (site tree cd99058f, clean); (1)-(5) pass on desktop-1440-01..04, mobile-390-01..05 and all seven seams cropped at 1:1: no overlapping or clipped text; notice is (240,234,223) on (28,36,51) at both widths; fixed bar at mobile-390-01 y786-844 sits between text blocks and is not counted
- [ ] T39 Compare C with Studio McGee (AC82·AC83·AC85·AC88) — verify(human): as in T13 for interior-robinhome (`interior-robinhome-1440.png`, `-390.png`, `ref-interior-robinhome*`), confirming items (1)–(3) of T13 against Studio McGee; (4) side by side the two do not read as the same site: they differ in at least two of page colour, wordmark script, face and position, headline script and face, navigation, section order (the kept traits of item 6 do not count); (5) the sample's `<h1>` is not a translation or close paraphrase of "A design house rooted in modern tradition"; (6) the sample keeps each trait listed for Candidate C under "Traits to keep" in the spec: a mid-dark coloured page on the first screen; one wide photo inset with a margin of page colour on all four sides; a one-line serif statement centred under the photo, with one part in a second style; a light section below with a three-column card grid
      reason: copied wording, logos, "reads as the same site" and "keeps the trait" are judgements a person makes.
      scope: profile/interior-robinhome
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #b68cecf9 2026-11-20 — folders current, reference ok 2026-11-20; (1)-(6) pass: no Studio McGee name or logo (grep 0 hits); no shared sentence with ref-interior-robinhome.txt; four photos differ from the reference scenes seen; differs in page colour, wordmark script, face and position, headline script and face, navigation and section order; h1 (index.html:33) is not a paraphrase of the reference headline; four kept traits present at 1440 (at 390 the statement wraps to three lines and the cards stack)

## Registration (`scripts/profiles.py`, `thumb.jpg`, `profile/index.html`)

Each sample is registered after its visual work. `python3 scripts/build.py` regenerates `profile/index.html`; never
edit that file by hand.

- [x] T40 Register A: add its `PROFILES` entry (spec AC108, title from A12; the check reads `title`, `summary` and `features` with the word lists and digit rules of AC27 and AC52–AC62), run `python3 scripts/profile_thumb.py interior-robininterior`, run `python3 scripts/build.py` (AC1·AC3·AC4·AC5·AC6·AC17·AC86·AC87·AC108·AC203) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-20-profile-interior/check_static.py register interior-robininterior`
- [x] T41 Check that A's `thumb.jpg` shows its current first screen (AC5) — verify(browser): `python3 docs/features/2026-11-20-profile-interior/check_browser.py thumb interior-robininterior`
- [x] T42 Register B as in T40 (spec AC138), with `python3 scripts/profile_thumb.py interior-robindesign` (AC1·AC3·AC4·AC5·AC6·AC17·AC86·AC87·AC138·AC203) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-20-profile-interior/check_static.py register interior-robindesign`
- [x] T43 Check that B's `thumb.jpg` shows its current first screen (AC5) — verify(browser): `python3 docs/features/2026-11-20-profile-interior/check_browser.py thumb interior-robindesign`
- [x] T44 Register C as in T40 (spec AC169), with `python3 scripts/profile_thumb.py interior-robinhome` (AC1·AC3·AC4·AC5·AC6·AC17·AC86·AC87·AC169·AC203) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-20-profile-interior/check_static.py register interior-robinhome`
- [x] T45 Check that C's `thumb.jpg` shows its current first screen (AC5) — verify(browser): `python3 docs/features/2026-11-20-profile-interior/check_browser.py thumb interior-robinhome`

## Gallery, the three together and the branch

- [x] T46 Regenerate the gallery with all three entries: 인테리어 chip count 3, a card per sample, no interior 준비 중 tile, no other interior entry, distinct names (AC3·AC19·AC100·AC101·AC102) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-20-profile-interior/check_static.py gallery`
- [x] T47 Check the gallery: the 인테리어 filter shows the three cards and no 준비 중 tile; each card, from a fresh load, opens the preview with that sample, its desktop/mobile buttons switch the width, Esc closes it (AC100·AC101·AC103·AC104·AC105) — verify(browser): `python3 docs/features/2026-11-20-profile-interior/check_browser.py gallery`
- [x] T48 Check that the three samples' `<h1>` faces and header wordmark faces differ pairwise (AC90·AC91) — verify(browser): `python3 docs/features/2026-11-20-profile-interior/check_browser.py trio`
- [x] T49 Review the three samples side by side (AC92) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/compare/` for the three interior samples (command: `python3 docs/features/2026-11-20-profile-interior/check_browser.py compare`). Set `interior-robininterior-1440.png`, `interior-robindesign-1440.png` and `interior-robinhome-1440.png` side by side, and the same at `-390.png`, and confirm for each of the three pairs: (1) the wordmarks differ in position and size; (2) the palettes differ; (3) the typefaces of wordmark and headline differ; (4) the hero compositions differ (a wide photo under a white bar; two colour blocks with no photo; an inset photo on a dark page); (5) no two wordmarks read as one mark with a suffix added
      reason: whether two designs or two marks read as one is a visual judgement.
      scope: profile/interior-robininterior, profile/interior-robindesign, profile/interior-robinhome
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #d6993643 2026-11-20 — compare folder current for the three samples; (1)-(5) pass for all three pairs at 1440 and 390: wordmark boxes A (72,62,202,83), B (70,410,626,811), C (663,65,775,101) at 1440; palettes light+vermilion / pink+teal / ink-blue+sand; faces Do Hyeon / Black Han Sans / Diphylleia; heroes wide photo under white bar / two colour blocks / inset photo on dark page; no two marks read as one with a suffix; at 390 A and B both start top-left, told apart by size
      확인: Seokhyun Kim 2026-11-20
- [x] T50 Keep the branch inside its scope (AC7) — verify: `base="$(git merge-base main HEAD)" && test -n "$base" && test -z "$(git diff --name-only "$base" | grep -v -e '^profile/interior-robininterior/' -e '^profile/interior-robindesign/' -e '^profile/interior-robinhome/' -e '^profile/index\.html$' -e '^scripts/profiles\.py$' -e '^docs/')$(git diff --name-only "$base" -- docs/profile-playbook.md)"`
- [x] T51 Compare the fifteen designs (AC84) — verify(human): apply the evidence rule to `/tmp/profile-interior-shots/compare/` for the three interior samples and to each `/tmp/profile-interior-shots/<slug>/` (commands: `python3 docs/features/2026-11-20-profile-interior/check_browser.py compare`, `python3 docs/features/2026-11-20-profile-interior/check_browser.py page <slug>`). In `compare/`, set each interior sample's `-1440.png` and `-390.png` beside those of `flower-bomgyeol`, `food-saebyeokmil`, `clinic-neuru`, `clinic-byeotteul`, `clinic-bonui`, `law-ganeum`, `law-goim`, `fitness-mideoum`, `fitness-jjuuk`, `beauty-robinhair`, `beauty-robinsalon`, `beauty-robinhairsalon` and the other two interior samples; for the rest of each page use the bands in `/tmp/profile-interior-shots/<slug>/` and the `-full-NN.png` bands of the shipped samples in `compare/`. Confirm for each interior sample, against each of the fourteen others: (1) the first screens differ in at least two of: hero composition (photo placement and size, where the headline sits), wordmark face and position, base and accent colour; (2) the rest of the page does not repeat the other's section layout and styling: no run of three or more consecutive bands with the same grid, card shape and heading style. Shared elements that every sample needs (sample notice, footer credits, a mobile bottom bar, the contact controls) do not count. Pairs to look at hardest: A with `clinic-neuru`, `beauty-robinsalon` and `fitness-mideoum`; B with `law-ganeum`, `clinic-bonui` and `clinic-neuru`; C with `clinic-byeotteul`, `flower-bomgyeol` and `beauty-robinhair`
      reason: "reads as the same design" is a taste judgement a person makes.
      scope: profile/interior-robininterior, profile/interior-robindesign, profile/interior-robinhome
      reviewed: PASS @30706b2080dd0f40f640551e9b6e7ed30721fe30 #783e8eb8 2026-11-20 — folders current; all 42 pairs pass (1) at 1440 and at 390 and (2); longest run of alike consecutive sections is 2 (A with clinic-neuru, C with fitness-mideoum), below three; thinnest cell is A with law-goim at 390, where hero composition is nearly the same and the pass rests on colour and wordmark face; shipped samples' 1440 shots were viewed at 50-60 % scale
      확인: Seokhyun Kim 2026-11-20

Always last, never removed:

- [x] T52 Reconcile `docs/current_system/` with what shipped (in `profile-samples/component.md`, the Source line lists `interior-robininterior`, `interior-robindesign` and `interior-robinhome`), and set `last_reconciled` in `overview.md` to the new HEAD (AC106·AC107) — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && python3 docs/features/2026-11-20-profile-interior/check_static.py current`
