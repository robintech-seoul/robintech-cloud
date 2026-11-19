---
status: shipped
test: `python3 docs/features/2026-11-18-profile-fitness/check_static.py all`
test(browser): `python3 docs/features/2026-11-18-profile-fitness/check_browser.py page fitness-mideoum; a=$?; python3 docs/features/2026-11-18-profile-fitness/check_browser.py page fitness-jjuuk; b=$?; python3 docs/features/2026-11-18-profile-fitness/check_browser.py gallery; c=$?; exit $((a|b|c))`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()" && python3 -c "import urllib.request as u; [u.urlopen(x, timeout=10) for x in ('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700', 'https://fonts.googleapis.com/css2?family=Bagel+Fat+One', 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css')]"`
commits: e284667587f0572e53713214eb7e5ba94bca0360..9d8f7e2e2cf27eca1842e1ba42faa163d57edbf1
---

# Pilates franchise profile samples (`fitness`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the existing `profile-samples` component (spec Scope, `Design: none`); there are no modules to
order. The tasks go sample by sample: D `fitness-mideoum`, then B `fitness-jjuuk`, then the gallery and the branch.
Every command runs from the repository root. The checks live next to this file:
`check_static.py <check> [<slug>]` (standard library and `sips`; no browser, no network; without `<slug>` a
per-sample check runs for both samples) and `check_browser.py page <slug> | gallery | compare` (Playwright driving
the installed Google Chrome; it serves the repository on a free local port itself and needs the network for web
fonts, which `preflight(browser)` checks). `compare` is not a check: it saves first-screen shots of the samples and
of the reference sites for the reviews below, and exits 0 even when a reference site does not answer.
`check_static.py` and `check_browser.py` are approved together with this file. Changing what they check is a change
to approved checks and goes back to a person for re-approval.

## Picks (spec Assumptions: palettes, faces, photos and branches are fixed here; agent decisions)

The accent is the last `palette` entry in `PROFILES` (AC71 · AC72 · AC73 · AC108). Faces are Google Fonts or
Pretendard (AC53).

| Sample | `palette` (base, ink, tint, accent) | Faces |
| --- | --- | --- |
| D `fitness-mideoum` | `#f8f7f5` (the `body` background), `#24221f`, `#efebe4` (warm beige panels), `#613d8f` (deep violet, hue 266°, saturation 0.40) | Gowun Batang for the wordmark, `h1` and every `h2`; Pretendard for body text, labels and digits |
| B `fitness-jjuuk` | `#fbf3e2` (the `body` background), `#1f2a22` (the `body` color), `#ece3cc` (tan panels), `#2f5e3a` (deep green, hue 134°, saturation 0.33, lightness 0.28) | Bagel Fat One for the wordmark, `h1` and every `h2`; Pretendard for body text, buttons and digits |

Hues: D is 36° from `food-saebyeokmil` (230°) and 37° from `law-goim` (303°); B is 34° from `clinic-neuru` (168°);
D and B are 132° apart. D takes the blue-violet band, not olive, so the two fitness samples do not both read green
(AC70); violet also sits opposite the warm wood of D's photos. AC123: D's base has red only 3 above blue; AC106 ·
AC107: B's base has every channel at least `0xE2` and red `0x19` above blue. Bagel Fat One is a chunky, rounded Korean
display face (AC114) that no shipped sample names (AC113); its Google Fonts subsets include 쭈 and 욱 (checked
2026-11-19). Gowun Batang is in AC99's list and no shipped sample loads it.

Photos (free Unsplash, not Unsplash+, or Pexels; compared on a contact sheet in the scratchpad, not committed):

| Sample | Hero | Other photos |
| --- | --- | --- |
| D | A wide landscape photo of a Pilates studio lit by daylight: reformers or mats, warm wood floor or wood frames, white or beige walls, with a calm bright area above or beside the centre for the headline. Search, in order: "pilates studio reformer daylight", "pilates reformer wood floor", "bright pilates studio". Not a laughing woman in a beige top reclining on a reformer before a row of windows (AC98), no arched window or opening (AC125), no logo or branded lettering on equipment (AC74) | Four goal-card photos, one per card: a beginner on a mat, gentle movement suited to 산전 · 산후 (no belly close-up), an older adult on a chair or reformer, an evening group or reformer class |
| B | A bright, friendly movement scene in a light room that sits on cream: a person reaching long on a mat, a side stretch. Not a street corner with a wordmark painted on a white brick wall, not a hand taking balls from a shelf (AC122), and not hands rolling up a mat on a wood floor (Scout's hero frame seen on 2026-11-19) | Three studio photos, one per branch (a reformer room, a mat room with props, a sunlit corner), used both in the branch entries and in the header 지점 menu (AC120) |

Branches (fictional; place names only, no brand-owned names): D 성수점, 판교점, 광교점, 해운대점 (regions 서울 ·
경기 · 부산); B 망원점, 연희점, 문래점. Every branch has its own weekday hours and closed days; every address ends in
"(가상 주소)"; every phone is `02-000-0000`.

**D `fitness-mideoum` page, in order** (neutral off-white page; full-bleed daylight photo hero):

1. Sample notice line, above the header, on the base colour.
2. Header on the base: `<a class="wordmark">` "미더움 필라테스" in Gowun Batang at the left; a `<nav>` with 미더움 소개 ·
   목적별 수업 · 지점 찾기 · 가맹 안내 (Hangul only); an outlined "가까운 지점 예약" link to the 지점 찾기 section at the
   right.
3. Hero, the first `<section>`: a full-bleed photo (`<img>` or the `background-image` of a real element) about 70–80 %
   of the 1440 first screen high, with no side margin. The `h1` (Gowun Batang, dark ink) and a short lead sit on the
   photo, centred over its bright area. No dark scrim or gradient (the first screen stays light, AC89); when the
   photo's bright area is busy, a white band at most 0.85 opaque may sit behind the text. Under the lead: the CTA
   "가까운 지점 상담 · 예약" (accent fill, link to the 지점 찾기 section; AC94) and a text link "목적별 수업 보기".
   Not Reborn's composition: no white fade from the left, no left-aligned sans headline with a pill under it.
   Suggested `h1`: "오래 다녀도 미더운 필라테스".
4. 미더움이 지키는 것 (`h2`): three principles in short sentences, step labels at most 24 px (AC105). No figures.
5. 목적별 수업 (`h2`, contains 목적): four `<article>` cards, each a photo, a `.tag` label (처음 시작, 산전 · 산후,
   시니어, 직장인) and an `h3` class name with one line. No outcome words.
6. 지점 찾기 (`h2`, in `<section id="branches">`): the four branch entries in a grid, each with its region word
   (서울, 경기, 부산) as a small label above the branch `h3`.
7. 가맹 안내 (`h2`, in `<section id="franchise">`): the AC40 sentence, the steps 상담 → 정보공개서 제공 → 계약 with no
   days, months or money, and 가맹 문의 links ("가맹 상담 전화", "가맹 카카오톡 상담"; AC29 needs 가맹 in each name).
8. Footer: 가맹본부 name, "(가상 주소)" address, `02-000-0000`, 사업자등록번호 `000-00-00000`, the sample notice,
   "Photos: Unsplash" (and Pexels when used), "Website by RobinTech".
9. Below 800 px: a fixed bottom bar with "지점 찾기" (link to `#branches`) and a 전화 link `href="#"`; the nav
   collapses (no hamburger needed; the bar and the hero CTA carry the flow).

**B `fitness-jjuuk` page, in order** (warm cream page; deep-green strip; chunky display type):

1. Full-width deep-green strip (`#2f5e3a`) holding the sample notice in cream (AC8 · AC9 · AC109).
2. Cream header: at the left a `<details>` whose `<summary>` reads "지점 보기" (AC118) with a panel of three photo
   links, one per branch (AC119 · AC120); in the centre `<a class="wordmark">` "쭈욱" in Bagel Fat One, large, in the
   accent; at the right "가맹 안내" (link to `#franchise`) and a pill "가까운 지점 예약" (link to `#branches`).
3. Hero, the first `<section>`: a big centred `h1` in Bagel Fat One in the accent, a 해요체 lead, two pills
   (가까운 지점 예약, 수업 알아보기), then a wide photo with large rounded corners (24–40 px), inset from the page
   edges. Suggested `h1`: "쭈욱 펴고, 천천히 숨 쉬어요".
4. 쭈욱은 이런 곳이에요 (`h2`): a large friendly paragraph in 해요체 with a few words on a pale green marker band.
5. 수업 (`h2`): a row of class cards (매트, 리포머 입문, 소도구, 산전 · 산후) with outlined pill tags.
6. 지점 찾기 (`h2`, in `<section id="branches">`): three branch entries as rounded cards with the branch photo,
   address, hours, closed days and four pill controls.
7. 가맹 안내 (`h2`, in `<section id="franchise">`): friendly 해요체 copy, the AC40 sentence, steps, 가맹 문의 pills.
8. Footer as in D.
9. Below 800 px: a fixed bottom bar in the accent with "지점 찾기" (link to `#branches`); the header keeps the
   wordmark and the 지점 보기 control.

## Fixed parameters of the checks (the page contract)

- **First screen** is 1440×900 and 390×844. "Visible" means inside the viewport, opacity (multiplied up the
  ancestors) above 0.5, and not covered at its centre by an element (or its `::before`/`::after`) painted above it
  with a background image or colour at alpha × opacity above 0.5, judged 1.5 s after load; at each AC35 scroll
  position (every half screen down to the end, at 390) within 1.5 s. A wrapped inline element is visible when the centre
  of any one of its line boxes is. 390 px overflow (AC77) is judged inside a
  `width:390px` iframe; everything else at 390 in a 390×844 viewport.
- **Sample notice** (AC8 · AC9 · AC10): the full text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" as real DOM text
  in one element (not CSS `content:`, not split), with the `·` U+00B7. AC10–AC12 read the last `<footer>` that is not
  inside an `<article>`.
- **Sections** (AC20 · AC22 · AC23 · AC40 · AC103): an `h2`–`h6` heading whose text contains 지점 찾기, 가맹 문의 or
  가맹 안내, or 목적 (spaces optional). Each of these headings sits directly inside its own `<section>`; a section
  runs to the next heading of the same or a higher level or to the end of that `<section>`, whichever comes first, so
  the footer and the mobile bar are never part of the 가맹 section. The 지점 찾기 `<section>` carries an `id`; that id
  is the target of every "link to the 지점 찾기 section" (AC33–AC35 · AC94), written `href="#<id>"`.
- **Branch entries** (AC21 · AC24–AC28 · AC30 · AC37 · AC38 · AC117 · AC119): each is an `<article id="…">` inside the
  지점 찾기 section whose first `h3`–`h6` ends in a word "<place>점" (성수점, or "미더움 성수점"). Inside it: an address
  line with "(가상 주소)", `02-000-0000`, a weekday hours line (one block, or a `dt`/`dd` pair, holding 평일 or a range
  월–금 and `HH:MM–HH:MM`; also `-`, `—`, `~`), a closed-days line (휴무, 휴관, 쉽니다, 쉬어요, 쉬는 날 or 쉼 and
  one of 일요일, 공휴일, 주말, 토요일 or 월요일 in one block, or one of the two in a label of at most 12 characters
  without a time and the other in the next block, as `<dt>쉬는 날</dt><dd>일요일</dd>` or
  `<dt>일요일 · 공휴일</dt><dd>휴무</dd>`; and none of 휴무 없, 휴무일: 없, 에도, 없이, 문의), and four `<a href="#">` whose accessible names contain 네이버 예약,
  카카오톡, 전화 and 네이버 지도. Any link or button in a branch entry whose name contains one of these words needs
  `href="#"`: no `tel:` link and no `<button>`.
- **가맹 controls** (AC29 · AC30): at least one `<a href="#">` in the 가맹 section whose name contains 가맹; every link
  or button there whose name contains 가맹 has `href="#"`, and every other `<a>` there is `href="#"` or an in-page
  `#<id>` (no `tel:`, no `mailto:`). In-page links elsewhere (header, hero, bottom bar) may
  point at `#branches` or `#franchise`.
- **Wordmark** (AC93 · AC112 · AC113): the `<a class="wordmark">` in the first `<header>`. Its accessible name
  (`aria-label`, else its text with image `alt`) contains the stem (미더움, 쭈욱) and no Latin letter, and its text has no
  Latin letter either. B's panel
  links show the branch name only. B's wordmark link holds only "쭈욱" in Bagel Fat One: AC113 reads the font that
  renders most of its glyphs, so a "필라테스" in Pretendard inside the same link could flip it.
- **D header nav** (AC90–AC92): every `<a>` inside a `<nav>` in the first `<header>` has Hangul text and no Latin
  letter; at 1440 a visible header link contains 지점 and one contains 가맹.
- **D hero** (AC94–AC96): AC95 needs an `<img>` (its `currentSrc`) or an element's own `background-image` in
  `/profile/fitness-mideoum/img/`, reaching into the first screen, whose box runs from the left edge (≤ 1 px) to the
  right edge (≥ width − 1 px); AC96 needs the `h1` box to overlap that box; AC94 needs a visible link outside every
  `<header>`, to the 지점 찾기 section, whose text contains 지점 and 상담 or 예약.
- **D digits** (AC105): at 1440 no element whose own text nodes hold a digit has a computed `font-size` above 24 px;
  a `::before`/`::after` whose `content` holds a digit or a `counter(` counts too.
- **D goal cards** (AC103 · AC104 · AC126): `<article>` elements inside the 목적 section; each holds an `<img>` whose
  `src` starts with `img/` and an element with class `tag` whose text is 1–12 characters of Hangul, spaces and `·`
  (no digit, no Latin). The `.tag` element holds text only, no nested element.
- **B menu** (AC118–AC120): a `<details>`/`<summary>` (no script needed) or a `<button>` with a small inline script,
  in the first `<header>`, whose text contains 지점. The panel lives inside the same `<header>` and holds one
  `<a href="#<branch id>">` per branch entry, each with an `<img>` from `img/`, without `loading="lazy"`. The panel is
  closed on load, so the thumbnail does not show it. A `hidden` panel whose CSS sets `display` also needs
  `[hidden] { display: none; }`.
- **B pills** (AC117): the 네이버 예약 link of each branch entry has a computed `border-radius` of at least half its
  rendered height on all four corners; write it in px (`999px`).
- **B green band** (AC109): at 1440 an element at least as wide as the viewport, reaching into the first screen, with
  an opaque computed `background-color` of hue 100°–160° and lightness at most 0.30: the notice strip in `#2f5e3a`.
- **Faces** (AC99 · AC100 · AC101 · AC113 · AC115 · AC116): a family counts as loaded (AC100 · AC101) when its name
  appears anywhere in `index.html` or `style.css`, spaces or `+` between words. D's font stacks therefore never name
  Noto Sans KR as a fallback; use `"Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui,
  sans-serif`. AC99 and AC116 read the first family
  of the computed `font-family` of every `h2` (and, for AC116, the `h1` and its rendered font); serif means a name
  matching serif, Myeongjo, Batang, Hahmlet, Song Myung, Garamond, Cormorant, Times, Georgia, Mincho, Diphylleia,
  Baskerville, Playfair, Lora, Merriweather, Libre Caslon or Spectral (the browser check also counts Myungjo), unless
  it has Sans in it. AC113 reads the
  wordmark's computed first family and its rendered font (CDP, glyphs of the element and its descendants; no font read
  fails AC113 and AC116), and fails when either starts with Pretendard or the
  family name appears in another `profile/<slug>/index.html` or `style.css`; D never names Bagel Fat One. AC115 reads
  the families requested from Google Fonts (`family=` of a link or `@import`) and every family in a `font-family`
  declaration or a `font` shorthand, at any nesting (`@media` too), in `style.css` and in `<style>` and `style=""`, with
  `var()` resolved from `:root` or `html`: none contains "mono" (any case), and no `font-family` begins with
  `monospace`.
- **Body colours** (AC106 · AC107 · AC110 · AC123): the last `background`/`background-color` (AC110: `color`) in a
  top-level `body` rule of `style.css`, with `var()` resolved from `:root` or `html`; written as hex, `rgb()` or
  `white`. Rules inside `@media` are not read.
- **Page text** (AC41 · AC44–AC48 · AC68 · AC88 · AC127 · AC128) is the text of `index.html` outside `script`, `style`, `template`
  and `title`, plus image `alt`, the `<title>` text, `meta` description and `og:` content, `aria-label` and `title`
  attributes, and the strings of CSS `content:` declarations, whitespace collapsed (not removed), matched as plain
  substrings. Words that hit in an allowed sense are rewritten, not exempted. Known traps: 산후기간 or 산후기 (후기;
  write 출산 후), 최대한 (최대), 최고의 (최고), 무료 체험 (무료), 물리치료사 (치료), 재활용 (재활), 보장 and 보증 even in
  "보장하지 않습니다", 보증금 (보증), 유일하게 (유일), 리뷰 in any sense, branch names such as 은평점 (평점), 무료 주차 (무료; write 주차 가능),
  최대 6인 (최대; write 6인 이하), 산후 회복 (회복), 긴장 완화 (완화), 자세 교정 (교정) and 상표등록 (write nothing about
  rights). An e-mail address (AC128), in text or a `mailto:` link, ends in `@example.com`. AC68 (static part): D never writes 리본 or
  Reborn (also not as "리본 장식"); B never writes Scout or 스카우트.
- **Digits in copy** (AC42 · AC43) are read per block (a `p`, `li`, `dd`, heading …; the `<title>`, each attribute
  and each CSS `content:` string is its own block), full-width digits folded. AC42 fails on a digit, optional spaces,
  then 호점, 개 지점, 개지점, 개 매장, 개점, 억, 만 or 원 (the last three also after 천, 백 or 십); AC43 on a digit, optional spaces, then `%`. Traps:
  "1:1 원데이", "02-000-0000 원하시는 시간" and "7원칙" fail AC42 (break the block or reword); "01위례점" holds 1위
  (AC44); a year before 개점 fails AC42.
- **Numbers** (AC16–AC19): addresses are block text matching `<한글>로|길 <번호>` as in the law feature, `<한글>동N가 <번호>`
  or `<번호> 번지`; every such block holds "(가상 주소)". Phone numbers are `0\d{1,2}-\d{3,4}-\d{4}`,
  `1[5-9]\d{2}-\d{4}` (also `.` or space), `(0N) NNN-NNNN` and `+82 …`, and all equal `02-000-0000`; a `tel:` link
  (none in a branch entry or the 가맹 section) dials 0200000000. 사업자등록번호 is `000-00-00000`. AC19 reads digits,
  full-width folded, up to the next space, after 등록번호, 등록, 허가번호, 신고번호 or 인가번호 and any of spaces, `:`, `(`,
  `[`, `#`, `-`, `–`, `—`, 는, 은, 제 or No.; write no year or other number after 등록 (정보공개서 등록, 가맹사업 등록).
- **Digit faces** (AC55): every visible element holding a time `HH:MM` or a phone number gets a probe (a
  `0123456789` span plus one span per character `0`–`9`, `i` and `M`, off-screen, inheriting the element's font). The
  probe's main rendered font (CDP `CSS.getPlatformFontsForNode`) must be monospaced (the twelve spans within 0.5 % of
  one another in width) or match the Korean list in `check_browser.py` (Pretendard, a `KR` family, Nanum, Gowun, Gothic
  A1, …, Bagel Fat One). Every request to the font hosts returns 200 (AC56).
- **Mobile bar** (AC35 · AC36): below 800 px a fixed bottom bar holds a link to the 지점 찾기 section; the page's
  bottom padding is at least the bar's height, so at the end of the page the footer's last text line (the last element
  in the last `<footer>` with a direct text node and no fixed or sticky ancestor) is not covered.
- **Images** (AC58 · AC2): every `src`/`srcset` of `<img>` and `<source>`, every `poster` and every CSS `url()` (in
  `style.css`, `<style>` and `style=""`; comments ignored) resolves to a file in `img/`. AC54 skips `http://www.w3.org/`
  (an inline SVG namespace, not a load). Scripts are inline (`<script>` without `src`), so no other local file is needed.
- **Thumbnail** (AC5 · AC89): `check_browser.py page` compares `thumb.jpg` with a fresh 1440×900 first screen (both
  scaled to 160×100, mean absolute RGB difference at most 15 of 255). AC89 is the mean ITU-R 601 luma of all pixels of
  `thumb.jpg`, decoded by `sips`, for each sample. Make the thumbnail last, after the sample's visual work; any later
  change to the first screen means running `python3 scripts/profile_thumb.py <slug>` again. The thumbnail is shot from
  `file://` with 6 s of virtual time, the check over http at 1.5 s, so the first screen must not depend on module
  scripts or `fetch`, must not auto-advance, and its entrance effects end within 1.5 s and are not timed with `Date`
  (the page clock is fixed). `thumb.jpg` must be a complete JPEG (starts with `FFD8`, ends with `FFD9`).
- **Name check** (AC15): `name-check.txt` has, per name, a block headed "D — CHOSEN: 미더움 (slug fitness-mideoum)" or
  "B — CHOSEN: 쭈욱 (slug fitness-jjuuk)" holding a `Kakao Map:` line with "<name> 필라테스", "<name>필라테스", "no
  result" and the name alone after a `;`, a `Google` and a `Daum` line naming the name with 필라테스, and a line
  "KFTC 영업표지 <name>: 0 results" (quotes ignored). The record was made at the spec stage; on a later match, stop and
  report it; do not change the name.
- **Screenshots** for the reviews go to `/tmp/profile-fitness-shots/<slug>/`: `desktop-1440.png` and `mobile-390.png`
  (full page, after a scroll through), the same cut into 1200 px tall bands (`desktop-1440-01.png` …), and
  `summary.txt` written last (`site tree` = `git rev-parse HEAD:profile/<slug>`, `site working tree` clean, dirty or
  unknown, the page heights, `result PASS|FAIL`). `compare` rewrites `/tmp/profile-fitness-shots/compare/`:
  `<slug>-1440.png` and `<slug>-390.png` first screens for the two fitness samples and the seven shipped samples; full
  pages of the seven shipped samples (`<slug>-1440-full.png`, `<slug>-390-full.png` and their `-NN` bands);
  `ref-<slug>.png` (1440 first screen), `ref-<slug>-full.png` and its `-NN` bands and `ref-<slug>.txt` (visible text)
  of each sample's reference home page, keeping the last good copy when a site does not answer; and `summary.txt`
  with a `local <slug> tree <hash> clean|dirty` line per sample and a
  `reference <slug> <url> ok|cached <date>|unreachable` line per reference.
- **Gallery** (AC80 · AC81 · AC83–AC85): AC80 · AC81 after one click on the 필라테스 chip; AC83–AC85 for each card on a
  fresh load of `/profile/`. AC83 needs the name stem (미더움, 쭈욱) in the iframe.
- **Evidence rule** for the reviews: a sample's page folder `/tmp/profile-fitness-shots/<slug>/` is current when its
  `summary.txt` exists, its `site tree` equals `git rev-parse HEAD:profile/<slug>` and its `site working tree` is
  `clean`; the compare folder is current for a sample when `compare/summary.txt` has that sample's `local` line with
  the same tree and `clean`. A review uses a current folder as it is and runs the named command only when the folder is
  not current. That command starts a browser, so it runs only when a person asked for browser checks (AGENTS.md §6-5);
  otherwise the evidence is missing and the review is UNSURE, noting that it needs a browser run. If the folder is still
  not current after the run, the evidence is missing and the review is UNSURE. A `cached`
  reference is evidence. An `unreachable` reference does not by itself make a review UNSURE: the review then judges the
  reference items against the spec's description of that reference (Candidate D or B text and sketch, AC93, AC98,
  AC102, AC111, AC112, AC122, AC124) and says so in its note.

## Shared

- [x] T1 Confirm the brand-name record for 미더움 and 쭈욱 in `docs/features/2026-11-18-profile-fitness/name-check.txt` (Kakao Map, Google, Daum and KFTC searches made at the spec stage) (AC15) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py name`

## Sample D — 미더움 필라테스 (`profile/fitness-mideoum/`)

- [x] T2 Pick photos for D as in Picks: contact sheet in the scratchpad (not committed), download the picks at web size into `img/`, write `img/sources.txt` (AC57·AC59·AC60·AC61·AC62·AC63·AC64) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py photos fitness-mideoum`
- [x] T3 Write `index.html` and `style.css` with the sample notice (on the first screen and in the footer), a `<title>` with 디자인 샘플, noindex, footer credits, fictional addresses, phone and 사업자등록번호, and no non-zero registration number (AC8·AC10·AC11·AC12·AC13·AC14·AC16·AC17·AC18·AC19) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py markers fitness-mideoum`
- [x] T4 Build the franchise flow: 지점 찾기 before 가맹 안내, four branch entries with address, phone, hours, closed days and the four `href="#"` controls, 가맹 문의 controls and the AC40 sentence (AC20·AC21·AC22·AC23·AC24·AC25·AC26·AC27·AC28·AC29·AC30·AC37·AC38·AC40) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py franchise fitness-mideoum`
- [x] T5 Keep the copy free of franchise figures, superlatives, reviews, health claims, lures, 피해보상 marks, rights or registration claims and outside e-mail addresses (AC41·AC42·AC43·AC44·AC45·AC46·AC47·AC48·AC88·AC127·AC128) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py ads fitness-mideoum`
- [x] T6 No form or field, `word-break: keep-all`, alt text, one Korean `h1`, no skipped heading level (AC31·AC32·AC39·AC65·AC66·AC75) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py flow fitness-mideoum`
- [x] T7 Keep the sample self-contained: relative paths only, images only from `img/`, fonts only from Google Fonts and Pretendard on jsDelivr, no other `http(s)://` URL, nothing naming 리본필라테스 (AC1·AC2·AC53·AC54·AC58·AC68) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py assets fitness-mideoum`
- [x] T8 Give D its own mood: Hangul-only header nav and wordmark, none of the banned faces or Reborn reds, goal cards with photos and tag labels, neutral off-white `body` (AC92·AC93·AC100·AC101·AC102·AC103·AC104·AC123·AC126) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py sample fitness-mideoum`
- [x] T9 Register D after its visual work: add the `PROFILES` entry with the D palette, run `python3 scripts/profile_thumb.py fitness-mideoum`, regenerate the gallery; the thumbnail stays light (AC1·AC3·AC4·AC5·AC6·AC73·AC89) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-fitness/check_static.py register fitness-mideoum`
- [x] T10 Check D in a browser at 1440 and 390: thumbnail current, sample notice, a 지점 찾기 link on the first screen and at every scroll position at 390 with the footer's last line uncovered, computed `keep-all`, digits in a Korean or monospaced face, font requests, no motion under reduced motion, no horizontal overflow, header 지점 and 가맹 links, hero CTA, full-bleed hero photo under the `h1`, serif `h2` faces, no digit above 24 px; writes the screenshots for T11–T14 (AC5·AC8·AC9·AC33·AC34·AC35·AC36·AC39·AC55·AC56·AC67·AC76·AC77·AC90·AC91·AC94·AC95·AC96·AC99·AC105) — verify(browser): `python3 docs/features/2026-11-18-profile-fitness/check_browser.py page fitness-mideoum`
- [ ] T11 Review D's content (AC49·AC50·AC51·AC52·AC126) — verify(human): apply the evidence rule to `/tmp/profile-fitness-shots/fitness-mideoum/` (command: `python3 docs/features/2026-11-18-profile-fitness/check_browser.py page fitness-mideoum`). Read `profile/fitness-mideoum/index.html` and `style.css` (for CSS `content:` text), look at the bands `desktop-1440-NN.png` and `mobile-390-NN.png` in that folder, and confirm each: (1) no count of 가맹점, 지점, 회원, 수강생, 강사 or years in business, no amount of 매출, 수익 or 창업 비용, and no opening timeline in days or months, in digits or in words (for example 수백 명, 십 년, 한 달 만에 오픈); a class capacity such as 6인 이하 is not such a count; (2) no member or owner testimonial, no quote attributed to a named person, no star rating, no partner or press logo, no award; (3) no photo captioned or labelled with a person's name or with 원장, 강사 or 점주, or placed under a heading naming 강사, 강사진, 원장 or 점주, as if that person works for the brand; (4) no superlative, guarantee, income or health-outcome claim in other words or in English (for example 가장, 손꼽히는, 확실한 효과, 통증이 사라, 살이 빠, 자세가 바로, best, guaranteed); (5) each goal card's `.tag` names a group or a purpose (who the class is for, or what it is for), not a result; (6) no claim of support, waived fees or costs the head office covers (지원, 면제, 무상, 본사 부담), and no 가맹 step that implies a contract on the day of, or right after, 상담 or 정보공개서
      reason: whether copy implies a count, a testimonial or an outcome in other words is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/fitness-mideoum
      reviewed: PASS @9d8f7e2 #b4dcf694 2026-11-19 — (1)-(6) pass; only count-like copy is class capacity '여섯 명 이하' (index.html:52); tags 처음 시작·산전 · 산후·시니어·직장인; 계약 step '검토를 마치신 뒤' (index.html:181)
- [ ] T12 Review D's photos (AC74·AC97·AC98·AC125) — verify(human): apply the evidence rule to `/tmp/profile-fitness-shots/fitness-mideoum/` and to `/tmp/profile-fitness-shots/compare/` for fitness-mideoum (commands: `python3 docs/features/2026-11-18-profile-fitness/check_browser.py page fitness-mideoum`, `check_browser.py compare`). Open every image in `profile/fitness-mideoum/img/`, `compare/fitness-mideoum-1440.png` and `-390.png`, and `ref-fitness-mideoum.png` with its `-full-NN` bands, and confirm: (1) every photo shows a Pilates or movement scene (reformer, mat, studio interior, hands or body in motion); (2) no photo shows a recognisable reference-site studio, a logo or branded lettering on equipment; (3) the hero as rendered on the first screen reads as a studio lit by daylight with warm wood, beige or cream tones; (4) the hero neither is nor imitates a rebornpilates.com photo, and is not a laughing woman in a beige top reclining on a reformer in front of a row of windows; (5) no photo frames a studio through or within an arched window or arched opening
      reason: subject, light, warmth and likeness to another photo are visual judgements.
      scope: profile/fitness-mideoum
      reviewed: PASS @9d8f7e2 #b52df489 2026-11-19 — (1)-(5) pass; full-res crops of all 5 photos show no equipment lettering or logo (only an unreadable ~5px apparel mark in goal-evening-reformer); hero is an empty daylit room with wooden reformers; no arched openings
- [ ] T13 Review D's full-page screenshots for overlapping or clipped text (AC78·AC79) — verify(human): apply the evidence rule to `/tmp/profile-fitness-shots/fitness-mideoum/` (command as in T11). Look at `desktop-1440-NN.png` and `mobile-390-NN.png` band by band and confirm: (1) at 1440, no text overlaps other text, an image or a control so that letters are hidden; (2) at 1440, no text is cut off at a box edge; (3) and (4) the same at 390; (5) the AC40 sentence reads at body-text size in the 가맹 section at 1440 and at 390. The fixed bottom bar appears once in a full-page shot; what it covers there is not counted
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page.
      scope: profile/fitness-mideoum
      reviewed: PASS @9d8f7e2 #332cb3ac 2026-11-19 — desktop-1440-01..04 and mobile-390-01..07 plus band seams: no overlapping or clipped text; bottom-bar cover excluded by rule; AC40 note 16px = body (style.css:414)
- [ ] T14 Compare D with 리본필라테스 (AC68·AC69·AC124) — verify(human): apply the evidence rule to `/tmp/profile-fitness-shots/compare/` for fitness-mideoum and to `/tmp/profile-fitness-shots/fitness-mideoum/` (commands: `check_browser.py compare`, `check_browser.py page fitness-mideoum`). Compare `fitness-mideoum-1440.png` and `-390.png` with `ref-fitness-mideoum.png`, the bands of the sample with the `ref-fitness-mideoum-full-NN.png` bands, and `ref-fitness-mideoum.txt` with the text of `profile/fitness-mideoum/index.html`, and confirm: (1) the sample shows no logo, wordmark or brand name of the reference (no ribbon mark); (2) no sentence of the reference appears in the sample; (3) no photo on the sample is one of the reference's photos; (4) the first screens differ in at least two of: hero composition (photo placement, where the headline sits and how it is set), wordmark face and position, base and accent colour; (5) the sample's `h1` is not a translation or close paraphrase of "회원의 변화를 만드는 것은 운동이 아니라, 사람입니다."; (6) below the first screen, no run of three or more consecutive bands repeats the reference's section layout and styling (same grid, card shape and heading style); the goal cards kept by the G1 pick do not count
      reason: copied wording, logos and "reads as the same site" are judgements a person makes.
      scope: profile/fitness-mideoum
      reviewed: PASS @9d8f7e2 #2efb4720 2026-11-19 — no ribbon mark or Reborn name; only shared string is hours '평일 07:00–22:00'; first screens differ in composition, wordmark and accent; h1 '오래 다녀도 미더운 필라테스' unrelated; no 3-band layout run

## Sample B — 쭈욱 필라테스 (`profile/fitness-jjuuk/`)

- [x] T15 Pick photos for B as in Picks, as in T2 (AC57·AC59·AC60·AC61·AC62·AC63·AC64) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py photos fitness-jjuuk`
- [x] T16 Write `index.html` and `style.css` with the markers as in T3 (AC8·AC10·AC11·AC12·AC13·AC14·AC16·AC17·AC18·AC19) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py markers fitness-jjuuk`
- [x] T17 Build the franchise flow as in T4, with B's three branches (AC20·AC21·AC22·AC23·AC24·AC25·AC26·AC27·AC28·AC29·AC30·AC37·AC38·AC40) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py franchise fitness-jjuuk`
- [x] T18 Keep the copy clean as in T5 (AC41·AC42·AC43·AC44·AC45·AC46·AC47·AC48·AC88·AC127·AC128) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py ads fitness-jjuuk`
- [x] T19 Forms, keep-all, alt, headings and Korean `h1` as in T6 (AC31·AC32·AC39·AC65·AC66·AC75) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py flow fitness-jjuuk`
- [x] T20 Keep the sample self-contained as in T7, nothing naming Scout Studios (AC1·AC2·AC53·AC54·AC58·AC68) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py assets fitness-jjuuk`
- [x] T21 Give B its own mood: cream `body` with warm red, green-black ink, none of Scout's colours, a Hangul-only wordmark, no mono face, the header 지점 menu linking every branch, at least five 해요체 sentences (AC106·AC107·AC110·AC111·AC112·AC115·AC118·AC119·AC121) — verify: `python3 docs/features/2026-11-18-profile-fitness/check_static.py sample fitness-jjuuk`
- [x] T22 Register B after its visual work: `PROFILES` entry with the B palette, `python3 scripts/profile_thumb.py fitness-jjuuk`, regenerate the gallery; the thumbnail stays light (AC1·AC3·AC4·AC5·AC6·AC73·AC89) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-fitness/check_static.py register fitness-jjuuk`
- [x] T23 Check B in a browser at 1440 and 390 as in T10, without the D-only checks, with B's: deep-green band on the first screen, wordmark face not Pretendard and used by no other sample, no serif `h1` or `h2`, pill 네이버 예약 controls, the header 지점 menu opening a panel with a photo link per branch (AC5·AC8·AC9·AC33·AC34·AC35·AC36·AC39·AC55·AC56·AC67·AC76·AC77·AC109·AC113·AC116·AC117·AC118·AC119·AC120) — verify(browser): `python3 docs/features/2026-11-18-profile-fitness/check_browser.py page fitness-jjuuk`
- [ ] T24 Review B's content (AC49·AC50·AC51·AC52) — verify(human): apply the evidence rule to `/tmp/profile-fitness-shots/fitness-jjuuk/` (command: `python3 docs/features/2026-11-18-profile-fitness/check_browser.py page fitness-jjuuk`), read `profile/fitness-jjuuk/index.html` and `style.css`, look at the bands, and confirm items (1)–(4) and (6) of T11 for this sample
      reason: whether copy implies a count, a testimonial or an outcome in other words is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/fitness-jjuuk
      reviewed: PASS @9d8f7e2 #568a6ba8 2026-11-19 — (1)-(4),(6) pass; no counts, testimonials, staff-labelled photos, outcome or support claims; 가맹 steps put 정보공개서 review before 계약 (index.html:147-149)
- [ ] T25 Review B's photos and wordmark (AC74·AC114·AC122) — verify(human): apply the evidence rule to `/tmp/profile-fitness-shots/fitness-jjuuk/` and to `/tmp/profile-fitness-shots/compare/` for fitness-jjuuk (commands as in T12, with `page fitness-jjuuk`). Open every image in `profile/fitness-jjuuk/img/`, `compare/fitness-jjuuk-1440.png` and `-390.png`, and `ref-fitness-jjuuk.png` with its `-full-NN` bands, and confirm: (1) and (2) of T12; (3) the hero neither is nor imitates a scoutstudios.com.au photo, and is not a street corner with a wordmark painted on a white brick wall, nor a hand taking balls from a shelf, nor hands rolling up a mat on a wood floor; (4) the wordmark "쭈욱" on the first screen reads as retro display lettering (tall and condensed, or chunky and rounded), not as a plain text sans and not as thin-stroke art-deco letterforms like Scout Studios' "SCOUT"
      reason: subject, likeness to another photo and the character of letterforms are visual judgements.
      scope: profile/fitness-jjuuk
      reviewed: PASS @9d8f7e2 #6dbe3dbb 2026-11-19 — (1)-(4) pass; full-res quadrant crops of all 4 photos (incl. replaced branch-reformer-room, branch-sunlit-room) show no logo or brand lettering; hero pregnant reverse plank on blue mat, unlike Scout frames; wordmark Bagel Fat One heavy rounded
- [ ] T26 Review B's full-page screenshots for overlapping or clipped text (AC78·AC79) — verify(human): apply the evidence rule to `/tmp/profile-fitness-shots/fitness-jjuuk/` (command as in T24), and confirm items (1)–(5) of T13 on its `desktop-1440-NN.png` and `mobile-390-NN.png`
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page.
      scope: profile/fitness-jjuuk
      reviewed: PASS @9d8f7e2 #e387c129 2026-11-19 — desktop-1440-01..04 and mobile-390-01..05 plus band seams: no overlapping or clipped text; card text over blobs stays legible; AC40 note 16px = body (style.css:444)
- [ ] T27 Compare B with Scout Studios (AC68·AC69·AC124) — verify(human): as in T14 for fitness-jjuuk (`fitness-jjuuk-1440.png`, `-390.png`, `ref-fitness-jjuuk*`), confirming items (1)–(4) and (6) of T14 against Scout Studios (the studio menu kept by the G1 pick does not count) and (5) the sample's `h1` is not a translation or close paraphrase of "pilates and yoga for everybody"
      reason: copied wording, logos and "reads as the same site" are judgements a person makes.
      scope: profile/fitness-jjuuk
      reviewed: PASS @9d8f7e2 #ec41543c 2026-11-19 — no Scout name, mark, sentence or photo; first screens differ in hero composition and wordmark face; h1 '쭈욱 펴고, 천천히 숨 쉬어요' unrelated; similar bands (about, location cards) not consecutive

## Gallery and branch

- [x] T28 Regenerate the gallery with both entries: 필라테스 chip count 2, a card per sample, no fitness 준비 중 tile, accents at least 25° from every other accent and saturated, B's accent in the green band (AC71·AC72·AC80·AC81·AC82·AC108) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-fitness/check_static.py gallery`
- [x] T29 Check the gallery: the 필라테스 filter shows the two cards and no 준비 중 tile; each card, from a fresh load, opens the preview with that sample, its desktop/mobile buttons switch the width, Esc closes it (AC80·AC81·AC83·AC84·AC85) — verify(browser): `python3 docs/features/2026-11-18-profile-fitness/check_browser.py gallery`
- [x] T30 Keep the branch inside its scope (AC7) — verify: `base="$(git merge-base main HEAD)" && test -n "$base" && test -z "$(git diff --name-only "$base" | grep -v -e '^profile/fitness-mideoum/' -e '^profile/fitness-jjuuk/' -e '^profile/index\.html$' -e '^scripts/profiles\.py$' -e '^docs/')$(git diff --name-only "$base" -- docs/profile-playbook.md)"`
- [ ] T31 Compare the nine designs (AC70) — verify(human): apply the evidence rule to `/tmp/profile-fitness-shots/compare/` for both fitness samples and to each `/tmp/profile-fitness-shots/<slug>/` (commands: `check_browser.py compare`, `check_browser.py page <slug>`). In `compare/`, set each fitness sample's `-1440.png` and `-390.png` beside those of `flower-bomgyeol`, `food-saebyeokmil`, `clinic-neuru`, `clinic-byeotteul`, `clinic-bonui`, `law-ganeum`, `law-goim` and the other fitness sample; for the rest of each page use the bands in `/tmp/profile-fitness-shots/<slug>/` and the `-full-NN.png` bands of the shipped samples in `compare/`. Confirm for each fitness sample, against each of the eight others: (1) the first screens differ in at least two of: hero composition (photo placement and size, where the headline sits), wordmark face and position, base and accent colour; (2) the rest of the page does not repeat the other's section layout and styling: no run of three or more consecutive bands with the same grid, card shape and heading style. Shared elements that every sample needs (sample notice, footer credits, a mobile bottom bar) do not count
      reason: "reads as the same design" is a taste judgement a person makes.
      scope: profile/fitness-mideoum, profile/fitness-jjuuk
      reviewed: PASS @9d8f7e2 #5523b140 2026-11-19 — 16 pairs: first screens differ in at least two of composition, wordmark and colour (closest pair mideoum vs law-goim differs in headline position and wordmark); no 3-band run of same grid, card shape and heading style

Always last, never removed:

- [x] T32 Reconcile `docs/current_system/` with what shipped (in `profile-samples/component.md`, the Source line lists `fitness-mideoum` and `fitness-jjuuk`), and set `last_reconciled` in `overview.md` to the new HEAD (AC86·AC87) — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && python3 docs/features/2026-11-18-profile-fitness/check_static.py current`
