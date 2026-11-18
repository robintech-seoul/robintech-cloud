---
status: shipped
test: `python3 docs/features/2026-11-18-profile-law/check_static.py all`
test(browser): `python3 docs/features/2026-11-18-profile-law/check_browser.py page law-ganeum && python3 docs/features/2026-11-18-profile-law/check_browser.py page law-goim && python3 docs/features/2026-11-18-profile-law/check_browser.py gallery`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()" && python3 -c "import urllib.request as u; [u.urlopen(x, timeout=10) for x in ('https://fonts.googleapis.com/css2?family=Hahmlet:wght@300..700', 'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600', 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css')]"`
commits: 8a9a3b4182f9a77662f1265ba47c2eccbfd202ca..8df6219df2c162683a74928a0a8628928d591f7b
---

# Law firm profile samples (`law`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the existing `profile-samples` component (spec Scope, `Design: none`); there are no modules to
order. The tasks go sample by sample: A `law-ganeum`, then C `law-goim`, then the gallery and the branch. Every
command runs from the repository root. The checks live next to this file:
`check_static.py <check> [<slug>]` (standard library and `sips`; no browser, no network; without `<slug>` a
per-sample check runs for both samples) and `check_browser.py page <slug> | gallery | compare` (Playwright driving
the installed Google Chrome; it serves the repository on a free local port itself and needs the network for web
fonts, which `preflight(browser)` checks). `compare` is not a check: it saves first-screen shots of the samples and
of the reference sites for the reviews below, and exits 0 even when a reference site does not answer.
`check_static.py` and `check_browser.py` are approved together with this file. Changing what they check is a change
to approved checks and goes back to a person for re-approval.

## Picks (spec Assumptions: palettes, faces and names are fixed here)

The accent is the last `palette` entry in `PROFILES` (AC74 · AC81 · AC107). Faces are Google Fonts or Pretendard
(AC49).

| Sample | `palette` (base, ink, tint, accent) | Faces |
| --- | --- | --- |
| A `law-ganeum` | `#1f2226` (the `body` background), `#e8e4dc`, `#2b2f34`, `#4f93ad` (steel blue, hue 197°, saturation 0.37) | Hahmlet for the wordmark, `h1` and `h2`; Pretendard for body text, labels and digits |
| C `law-goim` | `#e4e5e6` (the `body` background), `#1d2124`, `#d3d6d8`, `#7b3f78` (자주, hue 303°, saturation 0.32) | IBM Plex Sans KR for the wordmark, `h1`–`h3` and the vertical line; Pretendard for body text and digits |

The nearest other accents: A is 29° from `clinic-neuru` (168°) and 33° from `food-saebyeokmil` (230°); C is 39° from
`flower-bomgyeol` (342°); A and C are 106° apart.

Fixed lawyer names (fictional; used nowhere else under `profile/`). The 대표변호사 and the 광고책임변호사 are named in
the footer (AC19 · AC20). The fourth name is optional.

| Sample | 대표변호사 | 광고책임변호사 | Other 변호사 |
| --- | --- | --- | --- |
| A `law-ganeum` | 남도윤 | 문지후 | 오세린, 신태오 |
| C `law-goim` | 정다인 | 백승우 | 류하은, 임서하 |

**A `law-ganeum` page, in order** (dark solid page; no photo on the first screen):

1. Sample notice line, above the header. From 800 px up, the notice line and the header stay at the top
   together (`position: sticky; top: 0` on one opaque wrapper; AC119).
2. Header: wordmark "법무법인 가늠" at the left, nav (업무분야 · 구성원 · 상담 안내 · 오시는 길), a "전화 02-000-0000"
   link and a "상담 예약" link styled as a button in the accent, with graphite `#1f2226` text.
3. Hero, the first `<section>`: the `h1` statement in Hahmlet and a short lead at the left; at the right a numbered
   index of the practice items (01–05), each a link to that item's `id` (AC90). The index numerals stay smaller than
   the `h1` (AC89).
4. 주요 업무분야 (`h2`): five items, each an `h3` with an `id`: 민사소송, 형사 사건 변호, 행정소송, 가사소송, 손해배상.
   One line of scope each, no outcome.
5. 사건을 보는 순서 (`h2`): three steps (사실관계 정리, 증거 검토, 절차 안내), one photo no wider than 50% of the
   viewport, and the AC31 sentence.
6. 구성원 (`h2`): three or four lawyer cards with a monogram (initials), no portrait.
7. 상담 안내 (`h2`): steps, 상담 시간 ("평일 09:00 – 18:00"), the closed-days line, the AC30 sentence, and the
   상담 예약 and 카카오톡 상담 controls.
8. 오시는 길 (`h2`): 주사무소 with "(가상 주소)", the 네이버 지도 link, the phone number.
9. Footer (AC8 · AC9 · AC11 · AC15 · AC19 · AC20).
10. Below 800 px: a fixed bottom bar with a line "디자인 샘플 · 상호와 정보는 가상입니다" (AC119) above 상담 예약,
    "전화 02-000-0000" and 카카오톡 상담.

**C `law-goim` page, in order** (stone page; full-bleed daylight photo hero):

1. Sample notice line, above the header. From 800 px up, the notice line and the header stay at the top
   together, as in A (AC119).
2. Header on the stone base: wordmark "법무법인 고임" (Hangul only, also in any `aria-label`), nav, 전화 and 상담 예약.
3. Hero, the first `<section>`: a full-bleed photo of Korean material in daylight (`<img>` or the `background-image`
   of a real element, not of a pseudo-element). Subjects to search, in this order: 한지 창호 (a paper lattice door or
   window) in daylight; an earthen or granite wall; a close detail of grey 기와. Never a glass facade at sunset, never a
   view over snow-covered roofs (AC113). Over the photo: a stone panel (`#e4e5e6`, opaque) at the lower left holding
   the `h1`, a lead, 상담 예약 and 전화; a short vertical Korean line (`writing-mode: vertical-rl`, for example
   "바닥을 고르게") on a stone strip at the right. Dark ink on light ground only: no dark overlay, scrim or gradient
   over the photo (AC115 · AC116). At 390 the photo stays full width above the panel.
4. 주요 업무분야 (`h2`): six cards with hairline borders, each an `h3`: 회사 설립 · 지배구조, 계약 검토, 인사 · 노무,
   공정거래, 개인정보 · 정보보호, 투자 · 인수합병.
5. 일하는 방식 (`h2`): three principles with no outcome promise, and the AC31 sentence.
6. 구성원 (`h2`): three or four cards with a monogram; each card has a "주요취급분야: …" line (AC106).
7. 상담 안내 (`h2`): steps, 상담 시간, the closed-days line, an `h3` "상담 전 준비" with a list (계약서, 정관,
   등기사항전부증명서, 관련 메일), the AC30 sentence.
8. 오시는 길 (`h2`): 주사무소 with "(가상 주소)", the 네이버 지도 link.
9. Footer.
10. Below 800 px: a fixed bottom bar with the notice line of A's bar (AC119) above 상담 예약, 전화 and 카카오톡 상담.

## Fixed parameters of the checks (the page contract)

- **First screen** is 1440×900 and 390×844. "Visible" means inside the viewport, opacity (multiplied up the ancestors)
  above 0.5, and not covered at its centre by an element (or its `::before`/`::after`) painted above it with a
  background image or colour at alpha × opacity above 0.5 (`pointer-events: none` does not exempt a cover), judged
  1.5 s after load; at each AC44 and AC119 scroll position (every half screen down to the end, at 390 for AC44 and at
  both widths for AC119) within 1.5 s. Text on C's photo
  sits in its own box above the photo; a gradient layer above text counts as a cover. 390 px overflow (AC65) and
  AC112 are judged inside a `width:390px` iframe; everything else at 390 in a 390×844 viewport.
- **Sample notice** (AC7 · AC11 · AC119): AC7 and AC11 need the full text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다";
  AC119 matches the short text "디자인 샘플 · 상호와 정보는 가상입니다" (the full text holds it). Write each as real DOM text
  in one element (not CSS `content:`, not split across elements), with the `·` of the full text (U+00B7). At 1440 a sticky
  top line carries it; a fixed bottom bar at 1440 can cover C's hero controls and fail AC42. Set `scroll-padding-top` on
  `html` to the sticky block's height so the AC90 entry links do not land under it. AC119 reads the footer's last text
  line as the last element in the last `<footer>` with a direct text node and no fixed or sticky ancestor.
- **Controls** (AC37–AC44) are `<a href="#">` links whose accessible name (text, or `aria-label`) contains 상담 예약,
  전화, 카카오톡 or 네이버 지도. Any link or button whose name contains one of these words counts, so it needs
  `href="#"`: no `tel:` link, and no `<button>` (it has no `href`). An in-page link such as "상담 예약 안내" to
  `#consult` fails AC41; name it without the word.
- **Sections** (AC45 · AC46 · AC77 · AC90 · AC91 · AC103 · AC104 · AC106 · AC30 · AC36): an `h2`–`h6` heading
  containing 주요 업무분야, 구성원, 상담 안내 or 오시는 길 (spaces optional); the section runs to the next heading of
  the same or a higher level. Put each item under its own `h3` inside the section. "상담 전 준비" is an `h3`–`h6` inside
  상담 안내 followed by at least three `<li>` before the next heading of its level.
- **상담 시간** (AC46): one block (`p`, `li`, `dd` …) holds a time range `HH:MM–HH:MM` (also `-`, `—`, `~`, `～`, `〜`),
  and that block or the one before it (a `dt`/`dd` pair) holds 평일 or a range 월–금. **Closed days** (AC77): one block,
  or a `dt`/`dd` pair, holds 휴무 or 쉽니다 and 공휴일, 일요일 or 주말, and none of 휴무 없, 에도, 없이, for example
  "토요일 · 일요일 · 공휴일 휴무".
- **Lawyers** (AC17–AC20 · AC106) are the fixed names in Picks. Each occurrence of a fixed name, anywhere in the page
  text, is followed within three non-Hangul characters (and an optional 대표변호사 or 변호사) by 가상, in the same block:
  "남도윤 대표변호사 (가상 인물)", "문지후 (가상 인물)" (the title may also be 광고책임변호사 or 구성원 변호사). So the name
  and its marker sit in one block, not a name in an `h3` and the marker in the next `p`. AC17 counts the fixed names in
  구성원 whose block also holds 변호사. The footer writes "대표변호사 <name> (가상 인물)" and "광고책임변호사 <name>
  (가상 인물)", and the 광고책임변호사 is one of the names AC17 counts (AC20); the sample notice and "(가상 주소)" do
  not count as markers. No other person is named on the page. AC106 (C): a card runs from a lawyer's first mention in
  구성원 to the next lawyer's; it holds a block with 주요취급분야 that names a term of the C list below that also
  appears in an `h3` of 주요 업무분야, or a whole `h3` text.
- **Firm name** (AC16 · AC98 · AC110): the wordmark is the first `<a>` in the first `<header>` whose text or
  `aria-label` contains the stem (가늠, 고임). The wordmark, the `<title>` and the footer each contain "법무법인 가늠" or
  "법무법인 고임", and none of them contains 법률사무소 or "<stem> 법률". Body copy may use 가늠하다 or 고임돌.
- **Page text** (AC22–AC29 · AC31 · AC36 · AC92 · AC105) is the text of `index.html` outside `script`, `style`,
  `template` and `title`, plus image `alt`, the `<title>` text, `meta` description and `og:` content, and
  `aria-label` and `title` attributes, and the strings of CSS `content:` declarations in `style.css`, whitespace
  collapsed, matched as plain substrings. Words that hit in an
  allowed sense are rewritten, not exempted. Known traps: 최대한 (최대), 최초 상담 (최초), 전문가 · 전문성 (전문), 전담 변호사 (전담),
  공지사항 (지사), 기본사항 (본사), 본부장 (본부), 출신 학교 (출신), 계약서 리뷰 (리뷰, write 검토), 보증금 반환 (보증),
  불확실 · 확실히 (확실), 보장 (also in "보장하지 않습니다"), 지원가능 written without a space (원가), 기각 and 우선처리 (선처) (A),
  고객사 · 파트너사 (C), 이행을 최고 (催告; 최고), 무죄추정 (A; 무죄), 연대보증 (보증), 쟁점이 갈리는 지점 (지점), 판결 전문
  (전문), 하도급 대금과 원가 (원가). An inline step numeral runs into the next word ("<span>01</span>위임" reads 01위임,
  which holds 1위), so put a space or a block break after it. Hours and fees: AC29 reads a digit, an optional space, an
  optional 만 and space, then 원 inside one block (also ₩ before a digit or KRW after one), so "18:00 원하시는" and
  "3원칙" fail; break the sentence or write 세 가지 원칙.
- **Offices** (AC36): every 사무소 in the page text is 주사무소 or 분사무소, and the 오시는 길 section contains 주사무소.
  The page never writes 법률사무소, and calls an office only 사무소 (not 사무실, 오피스 or 센터).
- **Numbers**: addresses (AC14) are written as road-name addresses, block text matching `<한글>로|길 <번호>` as in the clinic feature (the word before
  로 does not end in 으; the number is not followed by a letter, digit, `%`, `~`, `:`, `.`, `-`, `,<digit>` or a counter
  word 원, 분, 시, 개, 인, 일, 명, 번, 미터, 층, m). Phone numbers (AC15) are `0\d{1,2}-\d{3,4}-\d{4}` and
  `1[5-9]\d{2}-\d{4}` (also `.` or space; no parentheses or +82), registration numbers `\d{3}-\d{2}-\d{5}`. AC21
  reads digits, full-width ones folded, after 등록번호, 등록, 허가번호, 신고번호 or 인가번호 and any of spaces, `:`, `(`,
  `#`, 는, 은, 제 or No.; write no year or other number after 등록.
- **Digits** (AC50): every visible element holding a time `HH:MM` or a phone number gets a probe (a `0123456789` span
  plus one span per character `0`–`9`, `i` and `M`, off-screen, inheriting the element's font). The probe's main
  rendered font (CDP `CSS.getPlatformFontsForNode`) must be monospaced (the twelve spans within 0.5 % of one another
  in width) or match the Korean list: Pretendard, a `KR` family, Nanum, Gowun, Gothic A1, Hahmlet, Song Myung, Black
  Han Sans, Do Hyeon, Jua, Orbit, Sunflower, Gaegu, Dongle, Hi Melody, Gamja Flower, Poor Story, Stylish, Yeon Sung,
  Gugi, Dokdo, Single Day, Cute Font, Kirang Haerang, Bagel Fat One, Diphylleia. Every request to the font hosts
  returns 200.
- **Fonts** (AC83 · AC84 · AC96): a family counts as loaded when its name appears anywhere in `index.html` or
  `style.css` (a link, an `@import`, a font stack, a comment), spaces or `+` between words.
- **`h1` face** (AC85 · AC108): the first family of the last `font-family` or `font` declaration in a top-level rule
  whose selector list has a selector ending in `h1` (`h1`, `.hero h1`, `h1.title`), with `var()` resolved from `:root`
  or `html`. Set the `h1` face in such a rule, not only through a class on the `h1`. AC97 (browser): the first family
  of the computed `font-family` and the rendered font of the `h1` do not match serif, Myeongjo, Batang, Hahmlet, Song
  Myung, Garamond, Cormorant, Times, Georgia, Mincho, Diphylleia, Baskerville, Playfair, Lora, Merriweather, Libre
  Caslon or Spectral (a name with Sans in it passes). `check_browser.py page` also reads the cascade: AC85 fails when
  the computed first family of A's `h1` is not in AC85's list, and AC108 when C's computed first family or rendered
  font starts with Pretendard.
- **Body background** (AC82 · AC94 · AC95) is the last `background` or `background-color` in a top-level `body` rule
  of `style.css`, with `var()` resolved from `:root` or `html` rules; written as hex, `rgb()` or `white`. Rules inside
  `@media` are not read.
- **Practice items** (AC91 · AC103) count the item headings (`h3`–`h6`) of the 주요 업무분야 section that name at
  least one group of spellings below, spaces, middots, commas and slashes ignored; one heading counts once. A (송무 · 형사): 민사소송; 형사(사건)변호 or 형사사건; 행정소송; 가사소송; 손해배상; 이혼; 상속;
  부동산분쟁; 건설분쟁; 노동분쟁 or 노동사건; 의료분쟁; 강제집행; 보전처분, 가압류 or 가처분; 수사대응; 고소대리.
  C (기업 자문): 회사설립 or 법인설립; 지배구조; 계약(서)검토 or 계약자문; 인사노무 or 노무; 공정거래; 개인정보 or
  정보보호; 투자, 인수합병 or M&A; 지식재산, 상표 or 특허; 가맹 or 하도급; 상사분쟁 or 기업분쟁; 규제대응 or 인허가.
- **Entry links** (AC90): links inside the first `<section>` or the first `<header>` whose `href` is `#<id>` of an
  `h3`–`h6` or `<article>` that starts after the 주요 업무분야 heading and before its section ends (an `id` on any
  other element, such as the `<section>` that holds the `h2` or the next section, does not count). Three distinct
  targets.
- **A first screen** (AC86–AC89): the wordmark is live text containing 가늠 in the first `<header>` (the element that
  holds it, or the `<a>` around it); its left edge is at or below 360 px at 1440, and every element in it that holds
  text has `letter-spacing` at most 0.05 × `font-size` (`normal` passes). AC88: no `<img>`, `<video>`, `<picture>` or
  `<svg>`, and no element (`html` and `body` included) or pseudo-element with a CSS `url()` background, that reaches into the 1440 first screen is
  wider than 60 % of the viewport (864 px). AC89: no element whose own text (its direct text nodes) is a number (digits
  with `.,:+%~–-` and an optional 건, 명, 년, 억, 만, %, 원, 회, 개, 위, 배 or `+`) has a larger `font-size` than the
  largest text in the `h1`, anywhere on the page; a `::before` or `::after` whose `content` string is such a number
  counts too.
- **C first screen** (AC99 · AC100 · AC112): AC99 needs a visible element with a direct Hangul text node whose
  computed `writing-mode` is `vertical-rl`. AC100 · AC112: an `<img>` (its `currentSrc`) or an element's own
  `background-image` pointing into `/profile/law-goim/img/`, reaching into the first screen, whose box runs from the
  left edge (≤ 1 px) to the right edge (≥ width − 1 px) of the viewport; AC112 inside the 390 iframe after 1.5 s.
- **Thumbnail** (AC4 · AC116): `check_browser.py page` compares `thumb.jpg` with a fresh 1440×900 first screen (both
  scaled to 160×100, mean absolute RGB difference at most 15 of 255). AC116 is the mean ITU-R 601 luma of all pixels
  of `law-goim/thumb.jpg`, decoded by `sips` (flower's measures 48.9 this way). Make the thumbnail last, after the
  sample's visual work; any later change to the first screen means running `python3 scripts/profile_thumb.py <slug>`
  again. The thumbnail is shot from `file://` with 6 s of virtual time, the check over http at 1.5 s, so the first
  screen must not depend on module scripts or `fetch`, must not auto-advance, and its entrance effects end within
  1.5 s and are not timed with `Date` (the page clock is fixed). `thumb.jpg` must be a complete JPEG (starts with
  `FFD8`, ends with `FFD9`); `check_static.py register` fails AC4 otherwise.
- **Mobile bar**: the page's bottom padding below 800 px is at least the bar's height, notice line included, and at
  any width at least the height of any fixed bottom element, so the footer's last lines (AC8 · AC9 · AC11 · AC19 · AC20)
  are not hidden behind it at the end of the page (AC119 checks the last line).
- **Name check** (AC13): `name-check.txt` in this folder has, for each name, the queries `kakao-map` 법무법인<stem>,
  <stem> 법률, <stem> 변호사, <stem> 법률사무소 and <stem>; `daum` "법무법인 <stem>"; `kba` <stem> (the 법인 search on
  koreanbar.or.kr); and one `kba-control <name>` query for a firm that exists, showing that the search works. Each is
  written `query: <engine> <query>` (spaces and quotes ignored), followed by a `hits: <what came up>` line, and one
  `verdict: 법무법인 <stem> no match` per name. A `hits:` line names what came up without repeating the query, so a
  `hits:` line (other than the control's) that contains 법무법인 <stem> is a match and fails AC13. On a match, stop and report it; do not change the name yourself.
- **Screenshots** for the reviews go to `/tmp/profile-law-shots/<slug>/`: `desktop-1440.png` and `mobile-390.png`
  (full page, after a scroll through), the same cut into 1200 px tall bands (`desktop-1440-01.png` …), and
  `summary.txt` written last (`site tree` = `git rev-parse HEAD:profile/<slug>`, `site working tree` clean, dirty or
  unknown (git failed),
  the page heights, `result PASS|FAIL`). `compare` rewrites `/tmp/profile-law-shots/compare/`: `<slug>-1440.png` and
  `<slug>-390.png` first screens for the two law samples and the five shipped samples; full pages of the five shipped
  samples (`<slug>-1440-full.png`, `<slug>-390-full.png` and their `-NN` bands); `ref-<slug>.png` (1440 first screen),
  `ref-<slug>-full.png` and its `-NN` bands and `ref-<slug>.txt` (visible text) of each sample's reference home page,
  keeping the last good copy (all of its files, swapped in only when every step of a visit succeeds) when a site does
  not answer or answers with an HTTP error; and `summary.txt` with a
  `local <slug> tree <hash> clean|dirty` line per sample and a `reference <slug> <url> ok|cached <date>|unreachable`
  line per reference.
- **Gallery** (AC68 · AC70 · AC78–AC80): AC68 · AC78 after one click on the law chip; AC70 · AC79 · AC80 for each card
  on a fresh load of `/profile/`. AC70 needs the name stem (가늠, 고임) in the iframe.
- **Evidence rule** for the reviews: a sample's page folder `/tmp/profile-law-shots/<slug>/` is current when its
  `summary.txt` exists, its `site tree` equals `git rev-parse HEAD:profile/<slug>` and its `site working tree` is
  `clean`; the compare folder is current for a sample when `compare/summary.txt` has that sample's `local` line with
  the same tree and `clean`. A review uses a current folder as it is and runs the named command only when the folder is
  not current. If it is still not current after the run, the evidence is missing and the review is UNSURE. A `cached`
  reference is evidence; `unreachable` makes the reference review UNSURE.

## Shared

- [x] T1 Run the name checks for 법무법인 가늠 and 법무법인 고임 on Kakao Map, Daum and the 대한변호사협회 법인 검색, with one KBA control search, and record them in `docs/features/2026-11-18-profile-law/name-check.txt` (AC13) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py name`

## Sample A — 법무법인 가늠 (`profile/law-ganeum/`)

- [x] T2 Pick photos for A: free Unsplash (not Unsplash+) and Pexels candidates of stone stairs, columns, archive shelves, documents or a street, in black and white or low colour, with no identifiable person and no robe, uniform or courtroom, compared on a contact sheet in the scratchpad (not committed); download the picks at web size into `img/` and write `img/sources.txt` (AC52·AC55·AC56·AC57·AC58·AC59·AC60) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py photos law-ganeum`
- [x] T3 Write `index.html` and `style.css` with the sample notice (on the first screen and in the footer; the sticky top line and the mobile bar line of Picks are judged in T10 / T22), a `<title>` naming the sample, noindex, footer credits, and fictional address, phone and registration number (AC7·AC8·AC9·AC10·AC11·AC12·AC14·AC15) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py markers law-ganeum`
- [x] T4 Give the firm its legal form: "법무법인 가늠" in the wordmark, `<title>` and footer, at least three fixed lawyers in 구성원, a 가상 marker on every lawyer name, 대표변호사 and 광고책임변호사 in the footer, no non-zero registration number (AC16·AC17·AC18·AC19·AC20·AC21) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py form law-ganeum`
- [x] T5 Keep the copy inside the lawyer advertising rules: none of the listed words, no price, the fee and outcome sentences, offices labelled 주사무소 (AC22·AC23·AC24·AC25·AC26·AC27·AC28·AC29·AC30·AC31·AC36·AC92) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py ads law-ganeum`
- [x] T6 Build the client flow: 주요 업무분야, 구성원, 상담 안내 with 상담 시간 and closed days, 오시는 길; 상담 예약, 전화, 카카오톡 and 네이버 지도 as `href="#"` controls; alt text, one `h1`, no skipped heading level, `word-break: keep-all` (AC37·AC38·AC39·AC40·AC41·AC45·AC46·AC47·AC61·AC62·AC77) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py flow law-ganeum`
- [x] T7 Keep the sample self-contained: relative paths only, photos from `img/`, fonts only from Google Fonts and Pretendard on jsDelivr, no other `http(s)://` URL, nothing naming Selendy Gay (AC1·AC2·AC49·AC51·AC53·AC54·AC71) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py assets law-ganeum`
- [x] T8 Give A its own mood: graphite `body` background, no Cormorant Garamond or Noto Serif KR, Hahmlet `h1`, entry links from the hero to the practice items, at least four 송무 · 형사 items (AC82·AC83·AC84·AC85·AC90·AC91) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py sample law-ganeum`
- [x] T9 Register A after its visual work: add the `PROFILES` entry with the A palette, run `python3 scripts/profile_thumb.py law-ganeum`, regenerate the gallery (AC1·AC3·AC4·AC5·AC81) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-law/check_static.py register law-ganeum`
- [x] T10 Check A in a browser at 1440 and 390: thumbnail current, sample notice, 상담 예약 and 전화 on the first screen and at every scroll position at 390, the short sample notice at every scroll position at 1440 and 390 with the footer's last line uncovered, computed `keep-all`, digits in a Korean or monospaced face, no motion under reduced motion, no horizontal overflow, wordmark at the left and unspaced, no wide image on the first screen, no number larger than the `h1`, the phone number on the first 390 screen, the computed `h1` face; writes the screenshots for T11–T13 (AC4·AC7·AC42·AC43·AC44·AC47·AC50·AC63·AC64·AC65·AC85·AC86·AC87·AC88·AC89·AC93·AC119) — verify(browser): `python3 docs/features/2026-11-18-profile-law/check_browser.py page law-ganeum`
- [ ] T11 Review A's content and photos (AC18·AC32·AC33·AC34·AC35·AC48·AC118) — verify(human): apply the evidence rule to `/tmp/profile-law-shots/law-ganeum/` (command: `python3 docs/features/2026-11-18-profile-law/check_browser.py page law-ganeum`). Read `profile/law-ganeum/index.html` and `profile/law-ganeum/style.css` (for CSS `content:` text), open every image in `profile/law-ganeum/img/` and the bands `desktop-1440-NN.png` and `mobile-390-NN.png` in that folder, and confirm each: (1) no client testimonial, rating, client or adviser-company name or logo, and no story of a past case; (2) no count of cases, consultations, wins or years of cases, and no amount recovered or saved, in figures or in words; (3) no comparison with other lawyers or firms, and nothing that suggests a tie to or influence over courts, prosecutors, police or other public bodies; (4) no photo shows a judge's robe, a prosecutor's or police uniform, or a courtroom with identifiable people; (5) no portrait photo of a person next to a lawyer's name; (6) every person named as a lawyer, in any wording and any section, is a fixed name from Picks and has a visible marker containing 가상 next to the name; (7) no superlative or similar claim in other words or in English (for example 가장, 손꼽히는, 선도하는, best, leading), no low-fee or 성공보수 offer, no "<crime> 변호사" title (for example 음주운전 변호사), and no legal-platform name or badge
      reason: whether copy tells a case story, implies a count or an influence, or a photo shows a uniform or a person, is a judgement about meaning; the static checks only catch listed words and fixed formats.
      scope: profile/law-ganeum
      reviewed: PASS @8df6219df2c162683a74928a0a8628928d591f7b #1c9c2a3b 2026-11-18 — all 7 sub-items PASS: no testimonial/case story/count/influence/superlative/fee offer; columns.jpg and stairs.jpg show no person, robe or courtroom; lawyers 남도윤·문지후·오세린·신태오 carry "(가상 인물)" (index.html:151,162,173,184,257); initials only, no portraits
- [ ] T12 Review A's full-page screenshots for overlapping or clipped text (AC66·AC67) — verify(human): apply the evidence rule to `/tmp/profile-law-shots/law-ganeum/` (command as in T11). Look at `/tmp/profile-law-shots/law-ganeum/desktop-1440-NN.png` and `mobile-390-NN.png` band by band and confirm: (1) at 1440, no text overlaps other text, an image or a control so that letters are hidden; (2) at 1440, no text is cut off at a box edge; (3) and (4) the same at 390. The fixed bottom bar appears once in a full-page shot; what it covers there is not counted
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page; no command decides it reliably.
      scope: profile/law-ganeum
      reviewed: PASS @8df6219df2c162683a74928a0a8628928d591f7b #dd853260 2026-11-18 — 1440 bands 01-05 and 390 bands 01-08 show no hidden or clipped text; band seams checked on full-page crops; fixed 390 bottom bar over practice item 03 excluded by the rule
- [ ] T13 Compare A with Selendy Gay (AC71·AC72) — verify(human): apply the evidence rule to `/tmp/profile-law-shots/compare/` for law-ganeum and to `/tmp/profile-law-shots/law-ganeum/` (commands: `python3 docs/features/2026-11-18-profile-law/check_browser.py compare`, `check_browser.py page law-ganeum`). Compare `law-ganeum-1440.png` and `law-ganeum-390.png` with `ref-law-ganeum.png`, the bands of `/tmp/profile-law-shots/law-ganeum/` with the `ref-law-ganeum-full-NN.png` bands, and `ref-law-ganeum.txt` with the text of `profile/law-ganeum/index.html` (the reference is its home page), and confirm: (1) the sample shows no logo, wordmark or firm name of the reference; (2) no sentence of the reference appears in the sample, translated or not; (3) no photo on the sample is one of the reference's photos; (4) the first screens differ in at least two of: hero composition (photo placement and size, where the headline sits), wordmark face and position, base and accent colour; (5) no link, rule or label on the sample uses a red like the reference's red links
      reason: copied wording or logos in another language, and "reads as the same site", are judgements a person makes.
      scope: profile/law-ganeum
      reviewed: PASS @8df6219df2c162683a74928a0a8628928d591f7b #6cde47ee 2026-11-18 — no Selendy Gay name/logo/sentence/photo (grep, ref-law-ganeum.txt); first screens differ in hero composition (no photo, statement + practice index) and accent (steel blue #4f93ad vs red); no red in style.css or screenshots

## Sample C — 법무법인 고임 (`profile/law-goim/`)

- [x] T14 Pick photos for C: free Unsplash and Pexels candidates for the hero in the order given in Picks (한지 창호, an earthen or granite wall, a 기와 detail), all in open daylight, neutral or cool in colour, with no plants as the subject and no person; plus one or two detail photos for later sections. Compare them on a contact sheet in the scratchpad beside flower's hero and Kim & Chang's two hero shots (the G1 screenshots named in the spec, or, when they are gone, the spec's descriptions in Candidate C and AC113); download the picks into `img/` and write `img/sources.txt` (AC52·AC55·AC56·AC57·AC58·AC59·AC60) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py photos law-goim`
- [x] T15 Write `index.html` and `style.css` as in T3 (AC7·AC8·AC9·AC10·AC11·AC12·AC14·AC15) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py markers law-goim`
- [x] T16 Give the firm its legal form as in T4, with C's fixed lawyers (AC16·AC17·AC18·AC19·AC20·AC21) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py form law-goim`
- [x] T17 Keep the copy inside the lawyer advertising rules as in T5, with C's words (AC22·AC23·AC24·AC25·AC26·AC27·AC28·AC29·AC30·AC31·AC36·AC105) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py ads law-goim`
- [x] T18 Build the client flow as in T6 (AC37·AC38·AC39·AC40·AC41·AC45·AC46·AC47·AC61·AC62·AC77) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py flow law-goim`
- [x] T19 Keep the sample self-contained as in T7, nothing naming Kim & Chang (AC1·AC2·AC49·AC51·AC53·AC54·AC71) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py assets law-goim`
- [x] T20 Give C its own mood: stone `body` background, none of the shipped or A faces, a sans `h1` that is not Pretendard, a Hangul-only wordmark, no search field, form or language switcher, at least four 기업 자문 items, a "상담 전 준비" list, a 주요취급분야 line on every lawyer card (AC94·AC95·AC96·AC98·AC101·AC102·AC103·AC104·AC106·AC108·AC110·AC111) — verify: `python3 docs/features/2026-11-18-profile-law/check_static.py sample law-goim`
- [x] T21 Register C after its visual work: `PROFILES` entry with the C palette, `python3 scripts/profile_thumb.py law-goim`, regenerate the gallery; the thumbnail stays light (AC1·AC3·AC4·AC5·AC81·AC116) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-law/check_static.py register law-goim`
- [x] T22 Check C in a browser at 1440 and 390 as in T10, without the A-only checks, with C's: sans `h1` that is not Pretendard as computed and rendered, vertical Korean line on the first screen, full-bleed photo at 1440 and in the 390 iframe (AC4·AC7·AC42·AC43·AC44·AC47·AC50·AC63·AC64·AC65·AC97·AC99·AC100·AC108·AC112·AC119) — verify(browser): `python3 docs/features/2026-11-18-profile-law/check_browser.py page law-goim`
- [ ] T23 Review C's content and photos (AC18·AC32·AC33·AC34·AC35·AC48·AC118) — verify(human): apply the evidence rule to `/tmp/profile-law-shots/law-goim/` (command: `python3 docs/features/2026-11-18-profile-law/check_browser.py page law-goim`), read `profile/law-goim/index.html` and `style.css`, open every image in its `img/` and the bands, and confirm items (1)–(7) of T11 for this sample
      reason: whether copy tells a case story, implies a count or an influence, or a photo shows a uniform or a person, is a judgement about meaning; the static checks only catch listed words and fixed formats.
      scope: profile/law-goim
      reviewed: PASS @8df6219df2c162683a74928a0a8628928d591f7b #3157d1a6 2026-11-18 — all 7 sub-items PASS: no testimonial/case story/count/influence/superlative/fee offer (fee line index.html:175); hero-wall.jpg and hanji.jpg show no person or uniform; 정다인·백승우·류하은·임서하 carry "(가상 인물)" (index.html:131-149,223); initials only
- [ ] T24 Review C's hero photo (AC109·AC113·AC114·AC115·AC117) — verify(human): apply the evidence rule to `/tmp/profile-law-shots/compare/` for law-goim (command: `python3 docs/features/2026-11-18-profile-law/check_browser.py compare`). Look at `law-goim-1440.png` and `law-goim-390.png`, the hero file in `profile/law-goim/img/`, `ref-law-goim.png` with its `-full-NN` bands, `flower-bomgyeol-1440.png` with its `-full-NN` bands, and the description of Kim & Chang's two hero shots in the spec (Candidate C and AC113), and confirm: (1) the hero shows Korean architecture or material (a stone or earthen wall, a 기와 or lattice detail, 한지 or ink); (2) it is not a Kim & Chang photo, and not a glass curtain wall with dark louvre bands reflecting a sunset, and not a view over snow-covered hanok roofs, reframed or recoloured; (3) its main subject is not flowers, leaves or other plants; (4) as rendered on the first screen it reads as lit by open daylight or even light, not a dim, side-lit, low-key look; (5) as rendered its colour is neutral or cool (stone, ink, grey, muted earth), not led by saturated warm hues
      reason: subject, likeness to another photo, light and colour temperature are visual judgements; AC116 is only a luma proxy.
      scope: profile/law-goim
      reviewed: PASS @8df6219df2c162683a74928a0a8628928d591f7b #f4fc5b74 2026-11-18 — hero-wall.jpg is a 기와 roof over a hexagon-pattern stone wall in overcast daylight; not K&C sunset facade or snow hanok roofs; no plants; mean V 0.58 vs flower 0.26, saturation 0.17 vs 0.39; no overlay on .hero-img
- [ ] T25 Review C's full-page screenshots for overlapping or clipped text (AC66·AC67) — verify(human): apply the evidence rule to `/tmp/profile-law-shots/law-goim/` (command: `python3 docs/features/2026-11-18-profile-law/check_browser.py page law-goim`), and confirm items (1)–(4) of T12 on `/tmp/profile-law-shots/law-goim/desktop-1440-NN.png` and `mobile-390-NN.png`
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page; no command decides it reliably.
      scope: profile/law-goim
      reviewed: PASS @8df6219df2c162683a74928a0a8628928d591f7b #50d5fa10 2026-11-18 — 1440 bands 01-05 and 390 bands 01-07 show no hidden or clipped text; vertical line box legible over photo; band seams whole on full-page crops
- [ ] T26 Compare C with Kim & Chang (AC71·AC72) — verify(human): apply the evidence rule to `/tmp/profile-law-shots/compare/` for law-goim and to `/tmp/profile-law-shots/law-goim/` (commands: `python3 docs/features/2026-11-18-profile-law/check_browser.py compare`, `check_browser.py page law-goim`). Compare `law-goim-1440.png` and `law-goim-390.png` with `ref-law-goim.png`, the bands of `/tmp/profile-law-shots/law-goim/` with the `ref-law-goim-full-NN.png` bands, and `ref-law-goim.txt` with the text of `profile/law-goim/index.html`, and confirm items (1)–(4) of T13
      reason: copied wording or logos in another language, and "reads as the same site", are judgements a person makes.
      scope: profile/law-goim
      reviewed: PASS @8df6219df2c162683a74928a0a8628928d591f7b #2a2647f5 2026-11-18 — no K&C wordmark/sentence/photo (grep, ref-law-goim.txt is nav labels only); first screens differ in hero composition (headline in grey panel bottom-left vs centred wordmark+search), wordmark (Korean sans left vs serif caps centred) and colour (stone/plum vs dark/orange)

## Gallery and branch

- [x] T27 Regenerate the gallery with both entries: law chip count 2, a card per sample, no law 준비 중 tile, accents at least 25° from every other accent and saturated (AC5·AC68·AC69·AC74·AC78·AC107) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-law/check_static.py gallery`
- [x] T28 Check the gallery: the law filter shows the two cards and no 준비 중 tile; each card, from a fresh load, opens the preview with that firm's page, its desktop/mobile buttons switch the width, Esc closes it (AC68·AC70·AC78·AC79·AC80) — verify(browser): `python3 docs/features/2026-11-18-profile-law/check_browser.py gallery`
- [x] T29 Keep the branch inside its scope (AC6) — verify: `base="$(git merge-base main HEAD)" && test -n "$base" && test -z "$(git diff --name-only "$base" | grep -v -e '^profile/law-ganeum/' -e '^profile/law-goim/' -e '^profile/index\.html$' -e '^scripts/profiles\.py$' -e '^docs/')$(git diff --name-only "$base" -- docs/profile-playbook.md)"`
- [ ] T30 Compare the seven designs (AC73) — verify(human): apply the evidence rule to `/tmp/profile-law-shots/compare/` for both law samples and to each `/tmp/profile-law-shots/<slug>/` (commands: `check_browser.py compare`, `check_browser.py page <slug>`). In `compare/`, set each law sample's `-1440.png` and `-390.png` beside those of `flower-bomgyeol`, `food-saebyeokmil`, `clinic-neuru`, `clinic-byeotteul`, `clinic-bonui` and the other law sample; for the rest of each page use the bands in `/tmp/profile-law-shots/<slug>/` and the `-full-NN.png` bands of the shipped samples in `compare/`. Confirm for each law sample, against each of the six others: (1) the first screens differ in at least two of: hero composition (photo placement and size, where the headline sits), wordmark face and position, base and accent colour; (2) the rest of the page does not repeat the other's section layout and styling: no run of three or more consecutive bands with the same grid, card shape and heading style. Shared elements that every sample needs (sample notice, footer credits, a mobile bottom bar) do not count
      reason: "reads as the same design" is a taste judgement a person makes.
      scope: profile/law-ganeum, profile/law-goim
      reviewed: PASS @8df6219df2c162683a74928a0a8628928d591f7b #c52bcc9a 2026-11-18 — all 12 pairs PASS: first screens differ in 2-3 aspects each; no run of 3 consecutive bands with same grid, card shape and heading style; closest calls ganeum vs goim mobile (headings and colour differ) and goim vs byeotteul hero (photo treatment, wordmark, colour differ)

Always last, never removed:

- [x] T31 Reconcile `docs/current_system/` with what shipped (in `profile-samples/component.md`, the Source line lists `law-ganeum` and `law-goim`), and set `last_reconciled` in `overview.md` to the new HEAD (AC75·AC76) — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && python3 docs/features/2026-11-18-profile-law/check_static.py current`
