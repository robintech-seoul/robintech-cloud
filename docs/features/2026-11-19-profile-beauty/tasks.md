---
status: shipped
test: `python3 docs/features/2026-11-19-profile-beauty/check_static.py all`
test(browser): `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinhair; a=$?; python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinsalon; b=$?; python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinhairsalon; c=$?; python3 docs/features/2026-11-19-profile-beauty/check_browser.py gallery; d=$?; python3 docs/features/2026-11-19-profile-beauty/check_browser.py trio; e=$?; exit $((a|b|c|d|e))`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()" && python3 -c "import urllib.request as u; [u.urlopen(x, timeout=10) for x in ('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;800&family=Newsreader:ital,wght@1,400', 'https://fonts.googleapis.com/css2?family=Song+Myung', 'https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&family=Sunflower:wght@300;500', 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css')]"`
commits: a0ac015bd7e7865ffc24b35c648f9bc56d08fa99..815a77aec309c8f14aa1e304aea13217f4f7631a
---

# Hair-salon franchise profile samples (`beauty`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the existing `profile-samples` component (spec Scope, `Design: none`). There are no modules to
order. The tasks go sample by sample: A `beauty-robinhair`, then B `beauty-robinsalon`, then C
`beauty-robinhairsalon`, then the gallery and the branch. Every command runs from the repository root.

The checks live next to this file and were written with it, before any sample exists; until then they fail:

- `check_static.py <check> [<slug>]`: standard library and `sips`; no browser, no network. Without `<slug>`, a
  per-sample check runs for all three samples.
- `check_browser.py page <slug> | gallery | trio | compare`: Playwright driving the installed Google Chrome. It serves
  the repository on a free local port itself (never `file://`, playbook §4) and needs the network for web fonts,
  which `preflight(browser)` checks. `compare` is not a check: it saves first-screen shots of the samples and of the
  reference sites for the reviews below, and exits 0 even when a reference site does not answer.

`check_static.py` and `check_browser.py` are approved together with this file. Changing what they check is a change
to approved checks and goes back to a person for re-approval. The Picks are approved with it too; the one exception
is a photo replaced as T12, T26 or T40 directs.

## Picks (spec Assumptions: palettes, faces, photos and branches are fixed here; agent decisions)

The accent is the last `palette` entry in `PROFILES` (AC75 · AC76 · AC77 · AC111 · AC157). Faces are Google Fonts or
Pretendard (AC60).

| Sample | `palette` (base, ink, tint, accent) | Faces |
| --- | --- | --- |
| A `beauty-robinhair` 로빈헤어 | `#17130f` (the `body` background; warm near-black, lightness 0.075, red 8 above blue), `#efe6d8` (warm cream text), `#2a231d` (panels), `#a3a34d` (olive brass, hue 60°, saturation 0.36) | Nanum Myeongjo 800 for the wordmark, the `h1` and every `h2`; Newsreader italic (`ital,wght@1,400`) for the one Latin word in `h1 em` only; Pretendard for body text, buttons and digits |
| B `beauty-robinsalon` 로빈살롱 | `#fcfcfb` (the `body` background; neutral white), `#111111` (ink), `#ebeae7` (pale grey panels), `#2a2a2a` (achromatic ink accent) | Song Myung for the display word, the wordmark, the `h1` and every `h2`; Pretendard for body text, buttons and digits |
| C `beauty-robinhairsalon` 로빈헤어살롱 | `#e8e3dc` (the `body` background; greige, red 12 above blue), `#2e2b27` (ink), `#d6d0c6` (darker greige panels), `#8a847a` (achromatic greige accent, channel spread 16) | Sunflower 300 for the wordmark; Nanum Gothic 400/700 for the `h1` and every `h2`; Pretendard for body text, buttons and digits |

A's accent is 29° from `clinic-byeotteul` (31°) and 74° from `fitness-jjuuk` (134°); B and C are achromatic and
exempt from the hue rule (AC75 · AC76). The three `<h1>` faces (Nanum Myeongjo, Song Myung, Nanum Gothic) and the three
wordmark faces (Nanum Myeongjo, Song Myung, Sunflower) differ pairwise (AC154 · AC155). No hex is in two of the
palettes (AC157). C's accent has low contrast on its base (2.9:1), so it is used for rules, borders and the mobile bar,
never for body text.

Photos (free Unsplash, not Unsplash+, or Pexels; compared on a contact sheet in the scratchpad, not committed):

| Sample | Hero | Other photos |
| --- | --- | --- |
| A | A dark, warm, low-key photo whose subject is a person's hair: wavy or long brown hair seen from behind or the side, or hands styling hair, in amber or brown light, wide enough to fill a 1440 × 640 crop. Search, in order: "hair dark background warm light", "brunette hair back view low light", "hair styling dark moody". Not a woman with short dark hair in a white shirt in a dry grass field with pale fabric behind her (AC117) | Two or three service photos: scissors cutting hair close-up, a comb and dryer on a dark counter, a warm salon interior |
| B | One model, head and shoulders, before a plain light or grey studio backdrop, hair as the subject (a bob, a wave or a sleek long cut), portrait or square, placed in front of the display word. Search: "short bob hair portrait studio", "hair model plain background". Not four long-haired women in a row before a wall (AC126); no brick wall and no lettering on a wall (AC125) | Four or more style-card photos, one hairstyle and one model each, on plain or soft backgrounds |
| C | Two tall interior photos in soft daylight, used side by side: a salon chair before a mirror by a window, a wash basin, a shelf with combs and a dryer, light wood or greige walls. Search: "minimal hair salon interior daylight", "salon chair mirror natural light", "hair wash basin salon bright". Not a black salon chair before a mirror with palm fronds, and not books and magazines on a table beside a plant (AC146) | One or two more interior or hair-detail photos for the branch or brand sections |

Every photo shows hair or a salon scene (AC78). Salon photos often show product bottles, tubes, capes and mirrors with
printed labels. The fitness verdict failed once on lettering visible only at full size, so every downloaded file is
opened at 100 % before it is used, and any file with legible lettering is cropped or replaced (AC158).

Branches (fictional; place names only; every branch has its own weekday hours and closed days, every address names a made-up district and road, as
"서울 가상구 결로 1 (가상 주소)", and ends in "(가상 주소)" (AC163); every phone is `02-000-0000`): A 연남점, 서촌점, 해운대점; B 압구정점, 합정점, 분당점, 광안리점; C 삼청점,
후암점, 수영점. No branch name contains a banned word (은평점 holds 평점).

**A `beauty-robinhair` page, in order** (warm near-black page; full-bleed dark photo hero):

1. Sample notice line above the header, on the base colour.
2. Header: `<a class="wordmark">` "로빈헤어" in Nanum Myeongjo 800 at the left; a `<nav>` with 브랜드 · 시술 · 지점 찾기 ·
   가맹 안내; an outlined pill "지점 예약" (link to `#branches`) at the right.
3. Hero, the first `<section>`: a full-bleed photo (an `<img>` or the `background-image` of a real element) about
   70 % of the 1440 first screen high, darkened (scrim or `filter`) so the first screen stays dark (AC101). On it, the
   centred `h1` in Nanum Myeongjo with one Latin word in `<em>` (Newsreader italic), a short lead, and two pills: "가까운
   지점 예약" (accent fill, link to `#branches`; AC113) and "시술 안내" (outlined). Suggested `h1`: "결대로 자르고,
   <em>softly</em> 다듬습니다". No figures row, no portrait band.
4. 로빈헤어 소개 (`h2`): a large statement paragraph in Nanum Myeongjo on a panel.
5. 시술 안내 (`h2`): a service list (커트, 펌, 염색, 두피 케어, 스타일링) without prices, and the line "시술 가격은 지점마다
   다릅니다. 지점의 네이버 예약에서 확인해 주세요."
6. 지점 찾기 (`h2`, in `<section id="branches">`): the branch entries with pill controls (AC112).
7. 가맹 안내 (`h2`, in `<section id="franchise">`): the AC42 sentence, the steps 상담 → 정보공개서 제공 → 계약 with no
   days, months or money, and 가맹 문의 links ("가맹 상담 전화", "가맹 카카오톡 상담").
8. Footer: 가맹본부 name, "(가상 주소)" address, `02-000-0000`, 사업자등록번호 `000-00-00000`, the sample notice,
   "Photos: Unsplash" (and Pexels when used), "Website by RobinTech".
9. Below 800 px: a fixed bottom bar with "지점 찾기" (link to `#branches`); the nav may collapse.

**B `beauty-robinsalon` page, in order** (white editorial page; giant Korean word behind the hero photo):

1. Sample notice line above the header.
2. Header: `<a class="wordmark">` "로빈살롱" in Song Myung; a `<nav>` with 브랜드 · 스타일 · 지점 찾기 · 가맹 안내
   (Hangul only).
3. Hero, the first `<section>`: one `<p class="display-word">` in Song Myung at 200 px or more at 1440 (suggested
   "머릿결"), live text, with the hero photo positioned over part of it and painted in front (higher `z-index`). Beside
   or under it: the `h1` (suggested "계절마다 새로 고르는 머리"), a lead and a "가까운 지점 찾기" link to `#branches`. At
   390 px the word may shrink, move above the photo or be hidden.
4. 이번 계절 스타일 (`h2`, contains 스타일, in a `<section>`): at least four `<article>` cards in one row at 1440 (a
   flex row or a four-column grid; a horizontal scroll strip is allowed), each an `<img>` from `img/` and an `h3`
   style name in Hangul. Suggested names: 목선 단발, 둥근 단발, 굵은 컬 펌, 가벼운 앞머리 커트 (no 슬릭, 레이어, 웨이브, 물결,
   느와르 or 마리; AC130).
5. 로빈살롱 소개 (`h2`): a short editorial paragraph and one interior or detail photo.
6. 지점 찾기 (`h2`, in `<section id="branches">`), 7. 가맹 안내 (`h2`, in `<section id="franchise">`) and 8. the footer,
   as in A.
9. Below 800 px: a fixed bottom bar with "지점 찾기".

**C `beauty-robinhairsalon` page, in order** (quiet greige page; spaced navigation; tall photo pair):

1. Sample notice line above the header, on a slightly darker greige strip.
2. Header: `<a class="wordmark">` "로빈헤어살롱" in Sunflower 300 with wide letter-spacing, on one line, with no rule
   and no stacked letters (AC150); a `<nav>` with 브랜드 · 시술 · 지점 찾기 · 가맹 안내, each link spaced at 0.14 em or
   more.
3. Hero, the first `<section>`: a left text column with the `h1` in Nanum Gothic (suggested "조용한 오후에 머리를
   다듬는 곳"), a lead and an outlined "가까운 지점 보기" link to `#branches` (AC152); at the right, two `<img>` side by
   side, each about 300 × 460 px or taller in ratio, tops aligned, with a gap.
4. 로빈헤어살롱의 방식 (`h2`): three short principles. 5. 시술 안내 (`h2`): services without prices.
6. 지점 찾기, 7. 가맹 안내 and 8. the footer, as in A.
9. Below 800 px: a fixed bottom bar with "지점 찾기"; the photo pair may stack or shrink.

## Fixed parameters of the checks (the page contract)

- **First screen** is 1440×900 and 390×844. "Visible" means inside the viewport, opacity (multiplied up the
  ancestors) above 0.5, and not covered at its centre by an element (or its `::before`/`::after`) painted above it
  with a background image or colour at alpha × opacity above 0.5, judged 1.5 s after load; at each AC37 scroll
  position (every half screen down to the end, at 390) within 1.5 s. A wrapped inline element is visible when the
  centre of any one of its line boxes is. 390 px overflow (AC86) is judged inside a `width:390px` iframe; everything
  else at 390 in a 390×844 viewport.
- **Sample notice** (AC8 · AC9 · AC10): the full text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" as real DOM text
  in one element (not CSS `content:`, not split), with the `·` U+00B7. AC10–AC12 read the last `<footer>` that is not
  inside an `<article>`.
- **Sections** (AC22 · AC24 · AC25 · AC42 · AC127): an `h2`–`h6` heading whose text contains 지점 찾기 or 매장 찾기, 가맹
  문의 or 가맹 안내, or 스타일 (spaces optional). Each of these headings sits directly inside its own `<section>`; a
  section runs to the next heading of the same or a higher level or to the end of that `<section>`, whichever comes
  first, so the footer and the mobile bar are never part of the 가맹 section. The 지점 찾기 `<section>` carries an
  `id`; that id is the target of every "link to the 지점 찾기 section" (AC35–AC37 · AC113 · AC152), written
  `href="#<id>"`. Write no other heading containing 스타일 before the style section.
- **Branch entries** (AC23 · AC26–AC30 · AC32 · AC39 · AC40 · AC112): each is an `<article id="…">` inside the 지점
  찾기 section whose first `h3`–`h6` ends in a word "<place>점" (연남점, or "로빈헤어 연남점"); every other `<article>`
  there fails AC23, so write no region or notice card as an `<article>`. Inside it: an address
  line with "(가상 주소)", `02-000-0000`, a weekday hours line (one block, or a `dt`/`dd` pair, holding 평일 or a range
  월–금 or 화–금 and `HH:MM–HH:MM`; also `-`, `—`, `~`), a closed-days line (휴무, 휴관, 쉽니다, 쉬어요, 쉬는 날 or 쉼
  and one of 일요일, 공휴일, 주말, 토요일, 월요일, 화요일, 수요일, 목요일 or 금요일 in one block, or one of the two in a label of at most 12
  characters without a time and the other in the next block, as `<dt>쉬는 날</dt><dd>매주 화요일</dd>`; and none of
  휴무 없, 휴무일: 없, 에도, 없이, 문의), and four separate `<a href="#">` whose accessible names contain 네이버 예약, 카카오톡,
  전화 and 네이버 지도; a link whose name holds two of these words fails AC26. Any link or button in a branch entry whose name contains one of these words needs `href="#"`:
  no `tel:` link and no `<button>`.
- **가맹 controls** (AC31 · AC32): at least one `<a href="#">` in the 가맹 section whose name contains 가맹; every link
  or button there whose name contains 가맹 has `href="#"`, and every other `<a>` there is `href="#"` or an in-page
  `#<id>` (no `tel:`, no `mailto:`). In-page links elsewhere (header, hero, bottom bar) may point at `#branches` or
  `#franchise`.
- **Wordmark** (AC16 · AC116 · AC134 · AC149 · AC155): the `<a class="wordmark">` in the first `<header>`. Its
  accessible name (`aria-label`, else its text with image `alt`) starts with 로빈 and has no Latin letter. AC155 reads
  its computed first family, so the link's own `font-family` is the wordmark face (not a child's).
- **Header nav** (AC131 · AC140 · AC141): every `<a>` inside a `<nav>` in the first `<header>` has Hangul text and no
  Latin letter (B and C). In C every such link has a computed `letter-spacing` of at least 0.1 × its `font-size` at
  1440. Header links "containing 지점 / 가맹" (AC114 · AC115 · AC132 · AC133 · AC142 · AC143) are any visible `<a>` in a
  `<header>` at 1440.
- **Hero links** (AC113 · AC152): a visible `<a href="#<지점 찾기 id>">` outside every `<header>` and every `position: fixed` or `sticky`
  element less than a quarter of the screen high (the mobile bar does not count; a sticky hero does) on the 1440 first screen; its text contains 지점 and 예약 (A) or 지점 (C).
- **A hero** (AC97–AC99): AC97 needs an `<img>` (its `currentSrc`) or an element's own `background-image` in
  `/profile/beauty-robinhair/img/`, reaching into the first screen, whose box runs from the left edge (≤ 1 px) to the
  right edge (≥ width − 1 px); AC98 needs the `h1` box to overlap that box; AC99 compares the centre of the `h1` box
  with half of `document.documentElement.clientWidth`.
- **A italic** (AC105–AC107): one `<em>` in the `h1` holding one Latin word (no Hangul). A CSS rule whose selector holds `h1` and ends
  in `em` (`h1 em`, `.hero h1 em`) sets its `font-family` with a `font-family` declaration (the `font` shorthand is not
  read); its first family is a family whose Google Fonts `family=`
  value in `index.html` requests `ital` (`Newsreader:ital,wght@1,400`). The browser check reads the `em`'s computed
  `font-style` and first family against the same list.
- **A digits and images** (AC118 · AC119): at 1440 no element whose own text nodes hold a digit has a computed
  `font-size` above 24 px; a `::before`/`::after` whose `content` holds a digit or a `counter(` counts too, and so does the `::marker` of a
  list item with a `decimal` list style whose marker `content` is not `none` or empty (an `<ol>` of 가맹 steps set large). No `<img>`
  has all four corner radii at least half its rendered width.
- **Pills** (AC112): the 네이버 예약 link of each branch entry has a computed `border-radius` of at least half its
  rendered height on all four corners; write it in px (`999px`).
- **B display word** (AC120–AC124): one element with class `display-word` holds the word as its own text node (not
  `content:`, not an image). The browser check takes every first-screen element whose own text is set at 160 px or
  more, so no other first-screen text reaches 160 px. AC123 needs its box to overlap a first-screen photo from
  `img/` (an `<img>` or an element's own `background-image`); AC124 forces `pointer-events: auto` on every element,
  calls `document.elementsFromPoint` at the centre of the largest overlap (clipped to the viewport), and needs the photo
  listed before the word. The photo is not an ancestor of the word.
- **B style strip** (AC127–AC129): `<article>` elements inside the 스타일 section; each holds an `<img>` whose `src`
  starts with `img/` and a first `h3`–`h6` with the style name. AC129 scrolls the section into view at 1440 and compares
  the top edges of the cards whose boxes reach into the viewport horizontally.
- **C photo pair** (AC144 · AC147): two `<img>` (not backgrounds) from `img/`, reaching into the 1440 first screen,
  each with rendered height ≥ 1.4 × rendered width, top edges within 8 px, boxes not overlapping; the `h1` box overlaps
  neither (when several pairs qualify, it overlaps none of their photos).
- **Faces** (AC63 · AC104 · AC108 · AC109 · AC122 · AC135 · AC148 · AC154 · AC155): the browser checks read the first family of
  the computed `font-family`. AC63 also needs the main font Chrome renders for the `h1`, the `a.wordmark` and the
  `.display-word` (CDP `CSS.getPlatformFontsForNode`) to be a web font (`isCustomFont`): a face that never loads, or a
  copy installed on the machine, fails. A family counts as loaded (AC108 · AC109 · AC135) when it is a whole family token, case
  ignored, in a Google Fonts `family=` value (link or `@import`) or in any `font-family` declaration or `font`
  shorthand, at any nesting (`@media` too), in `style.css`, `<style>` and `style=""`, with `var()` resolved from
  `:root` or `html`. So A's stacks never name Noto Serif KR, Cormorant Garamond, Hahmlet, Gowun Batang, Instrument
  Serif or Inter, and B's stacks never name Roboto: use `"Pretendard Variable", Pretendard, -apple-system,
  BlinkMacSystemFont, system-ui, sans-serif` (the usual system stack with `Roboto` in it fails AC135).
- **Body colours** (AC102 · AC103 · AC137 · AC138 · AC139): the last `background`/`background-color` in a top-level
  `body` rule of `style.css`, with `var()` resolved from `:root` or `html`; written as hex, `rgb()` or `white`. Rules
  inside `@media` are not read.
- **Page text** (AC43 · AC46–AC54 · AC59 · AC72 · AC159–AC161 · AC164) is the text of `index.html` outside `script`, `style`,
  `template` and `title`, plus the string literals of inline `<script>` that hold Hangul, `<`, `@`, `₩` or a space (tags stripped;
  text a script may put on the page), plus image `alt`, the `<title>` text, `meta` description and `og:` content, `aria-label` and
  `title` attributes, and the strings of CSS `content:` declarations, whitespace collapsed (not removed), matched as
  plain substrings; AC49, AC161 and the Latin words of AC46 and AC47 ignore case, typographic apostrophes and accents. AC164 fails on `@` and a name not
  inside an e-mail address, and on a domain ending in .com, .net, .org, .kr, .io, .me, .co, .shop or .cloud other than
  `example.com`. AC159 reads `alt` only. Words that hit in an allowed sense are rewritten, not
  exempted. Known traps: 은평점 (평점), 산후기 (후기), 최고급 or 최고의 (최고), 최대한 (최대), 유일하게 (유일), 보장 and 보증
  even in "보장하지 않습니다", 무료 주차 (무료; write 주차 가능), 효과적 (효과), 치료 in 두피 치료 (write 두피 케어), 맞춤
  처방 (처방; write 맞춤 관리), 선정한 (선정; write 고른), 의학적 (의학), any Latin word holding "after" or "before"
  (aftercare, afternoon; A's italic word too), 원장 in an `alt` (AC159), 1년 차 or 경력 (AC54), 리뷰 in any sense,
  ★ as decoration, ® or ™ after a name. An e-mail address (AC59), in text or a `mailto:` link, ends in `@example.com`.
  AC72 (static part): A never writes Spoke, Weal or 스포크; B never writes 박승철, pschair, Park Seung or the word STAGE;
  C never writes The Lane, thelane or 더 레인 (in `index.html` or `style.css`, class names included). These are
  substrings, case ignored (`bespoke` holds spoke), except STAGE, which is matched as a whole word (`\bstage\b`): a
  class such as `.stage` or `stage-word` hits it, `backstage` does not.
- **Digits in copy** (AC44 · AC45) are read per block (a `p`, `li`, `dd`, heading …; the `<title>`, each attribute and
  each CSS `content:` string is its own block), full-width digits folded. AC44 fails on a digit, optional spaces, then
  호점, 개 지점, 개지점, 개 매장, 개매장, 개점, 곳, 명, 억, 만 or 원 (the last three also after 천, 백 or 십), and on `₩` or `￦`
  before a digit, a digit before `KRW`, or a number with a thousands comma (`35,000`); script strings count as blocks; AC45 on a digit,
  optional spaces, then `%`. Traps: "1:1 원데이", "02-000-0000 원하시는 시간", "21:00 명절 당일" and "결로 1 원효빌딩" fail AC44 (break the
  block or reword); "2층 제201호" in an address fails AC21 (leave out the room); "공휴일에도 엽니다" in a closed-days
  line fails AC40 (put it in its own block); 화·수 without 요일 is not a closed day;
  "01위례점" holds 1위 (AC46); a year before 개점 fails AC44.
- **Numbers** (AC18–AC21): addresses are block text matching `<한글>로|길 <번호>`, `<한글>동N가 <번호>` or `<번호> 번지`;
  every such block holds "(가상 주소)". Phone numbers are `0\d{1,2}-\d{3,4}-\d{4}`, `1[5-9]\d{2}-\d{4}` (also `.` or
  space), `(0N) NNN-NNNN` and `+82 …`, and all equal `02-000-0000`; a `tel:` link (none in a branch entry or the 가맹
  section) dials 0200000000. 사업자등록번호 is `000-00-00000`. AC21 reads digits, full-width folded, up to the next
  space, after 등록번호, 등록, 허가번호, 신고번호 or 인가번호 and any of spaces, `:`, `(`, `[`, `#`, `-`, `–`, `—`, 는, 은,
  제 or No.; and any 제<number>호 with a digit other than 0; write no year or other number after 등록 (정보공개서 등록,
  가맹사업 등록).
- **Digit faces** (AC62): every visible element holding a time `HH:MM` or a phone number gets a probe (a `0123456789`
  span plus one span per character `0`–`9`, `i` and `M`, off-screen, inheriting the element's font). The probe's main
  rendered font (CDP `CSS.getPlatformFontsForNode`) must be monospaced (the twelve spans within 0.5 % of one another in
  width) or match the Korean list in `check_browser.py` (Pretendard, a `KR` family, Nanum, Song Myung, Sunflower, …).
  Every request to the font hosts returns 200 (AC63).
- **Mobile bar** (AC37 · AC38): below 800 px a fixed bottom bar holds a link to the 지점 찾기 section; the page's
  bottom padding is at least the bar's height, so at the end of the page the footer's last text line (the last element
  in the last `<footer>` with a direct text node and no fixed or sticky ancestor) is not covered; it is judged as
  "visible" within 1.5 s of the last scroll.
- **Images** (AC65 · AC2): every `src`/`srcset` of `<img>` and `<source>`, every `poster` and every CSS `url()` (in
  `style.css`, `<style>` and `style=""`; comments ignored) resolves to a file in `img/`, with the same letter case in every path part (AC65). `img/` holds no folder (AC66).
  A `cdn.jsdelivr.net` URL with a path anywhere in `index.html` or `style.css` must hold `pretendard` in its path (AC60), and
  `@import` in `<style>` is read like `@import` in `style.css`. AC61 skips `http://www.w3.org/`
  (an inline SVG namespace, not a load). Scripts are inline (`<script>` without `src`), so no other local file is
  needed.
- **Thumbnail** (AC5 · AC101 · AC153): `check_browser.py page` compares `thumb.jpg` with a fresh 1440×900 first screen
  (both scaled to 160×100 with high-quality smoothing, mean absolute RGB difference at most 15 of 255 over the image and at most 40 in every 10×10
  tile). It catches a changed photo or layout, not a changed line of text, so re-running `profile_thumb.py` after a
  first-screen text change is the implementer's step. AC101 and AC153 are the mean ITU-R 601 luma
  of all pixels of `thumb.jpg`, decoded by `sips`. Make the thumbnail last, after the sample's visual work; any later
  change to the first screen means running `python3 scripts/profile_thumb.py <slug>` again. The thumbnail is shot from
  `file://` with 6 s of virtual time, the check over http at 1.5 s, so the first screen must not depend on module
  scripts or `fetch`, must not auto-advance, and its entrance effects end within 1.5 s and are not timed with `Date`
  (the page clock is fixed). `thumb.jpg` must be a complete JPEG (starts with `FFD8`, ends with `FFD9`).
- **Screenshots** for the reviews go to `/tmp/profile-beauty-shots/<slug>/`: `desktop-1440.png` and `mobile-390.png`
  (full page, after a scroll through), the same cut into 1200 px tall bands (`desktop-1440-01.png` …), and
  `summary.txt` written last (`site tree` = `git rev-parse HEAD:profile/<slug>`, `site working tree` clean, dirty or
  unknown, the page heights, `result PASS|FAIL`). `compare` rewrites `/tmp/profile-beauty-shots/compare/`:
  `<slug>-1440.png` and `<slug>-390.png` first screens for the three beauty samples and the nine shipped samples; full
  pages of the nine shipped samples (`<slug>-1440-full.png`, `<slug>-390-full.png` and their `-NN` bands);
  `ref-<slug>.png` (1440 first screen), `ref-<slug>-full.png` and its `-NN` bands and `ref-<slug>.txt` (visible text)
  of each sample's reference home page, keeping the last good copy when a site does not answer; and `summary.txt`
  with a `local <slug> tree <hash> clean|dirty` line per sample and a
  `reference <slug> <url> ok|cached <date>|unreachable` line per reference.
- **Gallery** (AC89 · AC90 · AC92–AC94): AC89 · AC90 after one click on the 미용실 chip; AC92–AC94 for each card on a
  fresh load of `/profile/`. AC92 needs the iframe `src` to end in `/profile/<slug>/` and the loaded frame to be that
  page with a `header a.wordmark` (a name stem is not used: 로빈헤어 is inside 로빈헤어살롱).
- **Evidence rule** for the reviews: a sample's page folder `/tmp/profile-beauty-shots/<slug>/` is current when its
  `summary.txt` exists, its `site tree` equals `git rev-parse HEAD:profile/<slug>` and its `site working tree` is
  `clean`; the compare folder is current for a sample when `compare/summary.txt` has that sample's `local` line with
  the same tree and `clean`. A review uses a current folder as it is and runs the named command only when the folder is
  not current. That command starts a browser, so it runs only when a person asked for browser checks (AGENTS.md §6-5);
  otherwise the evidence is missing and the review is UNSURE, noting that it needs a browser run. If the folder is still
  not current after the run, the evidence is missing and the review is UNSURE. A `cached` reference is evidence. An
  `unreachable` reference does not by itself make a review UNSURE: the review then judges the reference items against
  the spec's description of that reference (Candidate A, B or C text and sketch, and AC117, AC126, AC146) and says so
  in its note. The photo-lettering reviews (AC158) read the files in `profile/<slug>/img/` directly, need no
  browser, and are current only while `git rev-parse HEAD:profile/<slug>/img` equals the hash in their note.

## Sample A — 로빈헤어 (`profile/beauty-robinhair/`)

- [x] T1 Pick photos for A as in Picks: contact sheet in the scratchpad (not committed), download the picks at web size into `img/` (free Unsplash or Pexels only; no `plus.unsplash.com`), write `img/sources.txt`; open every downloaded file at 100 % and crop or replace any with legible lettering before going on (AC64·AC66·AC67·AC68·AC69·AC70·AC71) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py photos beauty-robinhair`
- [x] T2 Write `index.html` and `style.css` with the sample notice (on the first screen and in the footer), a `<title>` with 디자인 샘플, noindex, footer credits, a 로빈 wordmark, fictional addresses, phone and 사업자등록번호, and no non-zero registration number (AC8·AC10·AC11·AC12·AC13·AC14·AC16·AC18·AC19·AC20·AC21) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py markers beauty-robinhair`
- [x] T3 Build the franchise flow: 지점 찾기 before 가맹 안내, three branch entries with address, phone, hours, closed days and the four `href="#"` controls, 가맹 문의 controls and the AC42 sentence (AC22·AC23·AC24·AC25·AC26·AC27·AC28·AC29·AC30·AC31·AC32·AC39·AC40·AC42) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py franchise beauty-robinhair`
- [x] T4 Keep the copy free of franchise figures, prices, superlatives, awards, reviews, before/after, treatment claims, lures, 피해보상 marks, rights claims, staff words, staff words in `alt`, outside e-mail addresses, ingredient or safety claims, product brand names, handles and domains (AC43·AC44·AC45·AC46·AC47·AC48·AC49·AC50·AC51·AC52·AC53·AC54·AC59·AC159·AC160·AC161·AC164) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py ads beauty-robinhair`
- [x] T5 No form or field, `word-break: keep-all`, alt text, one Korean `h1`, no skipped heading level (AC33·AC34·AC41·AC79·AC82·AC83) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py flow beauty-robinhair`
- [x] T6 Keep the sample self-contained: relative paths only, images only from `img/`, fonts only from Google Fonts and Pretendard on jsDelivr, no other `http(s)://` URL, nothing naming Spoke & Weal (AC1·AC2·AC60·AC61·AC65·AC72) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py assets beauty-robinhair`
- [x] T7 Give A its own mood: warm near-black `body`, one Latin word in a real italic inside the `h1`, none of the banned faces or Spoke & Weal's colours, a wordmark without Latin letters (AC102·AC103·AC106·AC107·AC108·AC109·AC110·AC116) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py sample beauty-robinhair`
- [x] T8 Register A after its visual work: add the `PROFILES` entry (name 로빈헤어, the A palette), run `python3 scripts/profile_thumb.py beauty-robinhair`, regenerate the gallery with `python3 scripts/build.py` (never edit `profile/index.html` by hand); the thumbnail stays dark and the accent chromatic (AC1·AC3·AC4·AC5·AC6·AC15·AC77·AC101·AC111) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-19-profile-beauty/check_static.py register beauty-robinhair`
- [x] T9 Check A in a browser at 1440 and 390: thumbnail current, sample notice, a 지점 찾기 link on the first screen and at every scroll position at 390 with the footer's last line uncovered, computed `keep-all`, digits in a Korean or monospaced face, font requests, no motion under reduced motion, no horizontal overflow, the full-bleed hero photo under a centred Nanum Myeongjo `h1` with a real italic `em`, pill 네이버 예약 controls, the hero CTA and header 지점 · 가맹 links, no digit above 24 px, no circular image; writes the screenshots for T10–T14 (AC5·AC8·AC9·AC35·AC36·AC37·AC38·AC41·AC62·AC63·AC84·AC85·AC86·AC97·AC98·AC99·AC104·AC105·AC107·AC112·AC113·AC114·AC115·AC118·AC119) — verify(browser): `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinhair`
- [ ] T10 Review A's content (AC55·AC56·AC57·AC58·AC161·AC163) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/beauty-robinhair/` (command: `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinhair`). Read `profile/beauty-robinhair/index.html` and `style.css` (for CSS `content:` text), look at the bands `desktop-1440-NN.png` and `mobile-390-NN.png` in that folder, and confirm each: (1) no person's name anywhere, as designer, 원장, 점주, founder or customer, and no photo captioned or labelled with a name or a staff role, or placed under a heading naming 디자이너, 스타일리스트, 원장 or 점주, as if that person works for the brand; (2) no count of 가맹점, 지점, 매장, 고객, 디자이너 or years in business, no amount of 매출, 수익, 창업 비용 or a service price, and no opening timeline in days or months, in digits or in words (for example 수십 곳, 십 년, 한 달 만에 오픈); (3) no testimonial, no quote attributed to a named person, no star rating, no partner, press or product-brand logo, no award, no before/after pair of photos; (4) no superlative, guarantee, income or hair-treatment outcome claim in other words or in English (for example 가장, 손꼽히는, 확실한, 머리가 다시 나, 탈모가 멈, best, guaranteed, regrowth), and no ingredient or safety claim (for example 순한, 자극 없는, 상하지 않는, gentle formula); (5) no claim of support, waived fees or costs the head office covers (지원, 면제, 무상, 본사 부담), no claim that opening is cheap, easy, fast or stable (소자본, 쉽게 시작, 빠른 오픈, 안정적인 운영), and no 가맹 step that implies a contract on the day of, or right after, 상담 or 정보공개서; (6) no real product, tool, booking or salon brand named anywhere other than 네이버 and 카카오톡, and no photo presented as the brand's or a branch's own work or customer (실제 시술, 고객 스타일, 완성한 스타일); (7) every address names a district or road that does not exist (for example 가상구 결로), not a real road with a building number
      reason: whether copy names a person, implies a count, a testimonial or an outcome in other words is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/beauty-robinhair
      reviewed: PASS @24e3256 #4449cb9c 2026-11-19 — (1)-(7) pass; no names, counts, prices, testimonials or claims; price note gives no price (index.html:67); contract step after review (:147-148); brands only 네이버/카카오톡; addresses all 가상구 (:84,:101,:118,:157); evidence tree 0926c5f current
- [ ] T11 Review A's photos (AC78·AC100·AC117) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/beauty-robinhair/` and to `/tmp/profile-beauty-shots/compare/` for beauty-robinhair (commands: `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinhair`, `python3 docs/features/2026-11-19-profile-beauty/check_browser.py compare`). Open every image in `profile/beauty-robinhair/img/`, `compare/beauty-robinhair-1440.png` and `-390.png`, and `ref-beauty-robinhair.png` with its `-full-NN` bands, and confirm: (1) every photo shows hair or a salon scene (hair, cutting, styling, salon interior, tools); (2) no photo shows a recognisable reference-site salon; (3) the hero as rendered on the first screen reads as dark and warm (darkened, with earth, brown or amber tones) and has a person's hair as its subject; (4) the hero neither is nor imitates a spokeandweal.com photo, and is not a woman with short dark hair in a white shirt standing in a dry grass field with pale fabric blowing behind her
      reason: subject, light, warmth and likeness to another photo are visual judgements.
      scope: profile/beauty-robinhair
      reviewed: PASS @24e3256 #08817c5b 2026-11-19 — (1)-(4) pass; hero-hair-dark, cut-wet-comb, tools-wood all hair/cutting/tools, no reference salon; rendered hero dark brown with amber long hair as subject at 1440 and 390; not the S&W field hero nor any ref photo (ref ok); evidence tree 0926c5f current
- [ ] T12 Inspect A's photos for lettering at native resolution (AC78·AC158) — verify(human): open every image file in `profile/beauty-robinhair/img/` one by one at 100 % zoom (not on the page, not on a contact sheet; for a file wider than the screen, view it in quadrants), and confirm each shows no legible brand name, logo, product label, sticker, signage, book or magazine title, or other lettering on bottles, tubes, mirrors, capes, aprons, tools, packaging, walls or anywhere else. On a hit, the implementer crops or replaces the file, updates `img/sources.txt`, re-runs T1, T8 and T9, and the review starts again. Name each file checked and record `git rev-parse HEAD:profile/<slug>/img` in the note; the review counts only while that hash is unchanged, so any later change to `img/` (a crop or a swap for any reason) opens it again
      reason: lettering on products in a photo is seen only by eye at full size; the fitness verdict failed once on lettering seen only there.
      scope: profile/beauty-robinhair/img
      reviewed: PASS @847f2c8 #8e50252c 2026-11-19 — 1:1 tiles plus zoomed/contrast crops of cut-wet-comb.jpg 1200x1500, hero-hair-dark.jpg 1920x1280, tools-wood.jpg 1184x784: no lettering, logo, label or engraving on clip, scissors, guard, comb or backdrop; img tree 32f1f3540f46384ce0cb2c2f1d3b6c1787bdafc8
- [ ] T13 Review A's full-page screenshots for overlapping or clipped text and the readability of the notices (AC87·AC88·AC162) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/beauty-robinhair/` (command as in T10). Look at `desktop-1440-NN.png` and `mobile-390-NN.png` band by band and at the seams between bands, and confirm: (1) at 1440, no text overlaps other text, an image or a control so that letters are hidden; (2) at 1440, no text is cut off at a box edge; (3) and (4) the same at 390; (5) the sample notice on the first screen and the AC42 sentence in the 가맹 section read at body-text size or larger, in a colour that stands out clearly from its background, at 1440 and at 390. The fixed bottom bar appears once in a full-page shot; what it covers there is not counted
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page.
      scope: profile/beauty-robinhair
      reviewed: PASS @24e3256 #4ec0013c 2026-11-19 — (1)-(5) pass; no overlap or clipping in 1440/390 bands or seam crops; .notice 16px #efe6d8 on #17130f (style.css:43-49), AC42 .fr-note 16px/600 #d9d58e (:374-379), body 16px (:21); evidence tree 0926c5f current
- [ ] T14 Compare A with Spoke & Weal (AC72·AC73·AC80·AC81) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/compare/` for beauty-robinhair and to `/tmp/profile-beauty-shots/beauty-robinhair/` (commands: `python3 docs/features/2026-11-19-profile-beauty/check_browser.py compare`, `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinhair`). Compare `beauty-robinhair-1440.png` and `-390.png` with `ref-beauty-robinhair.png`, the bands of the sample with the `ref-beauty-robinhair-full-NN.png` bands, and `ref-beauty-robinhair.txt` with the text of `profile/beauty-robinhair/index.html`, and confirm: (1) the sample shows no logo, wordmark or brand name of the reference; (2) no sentence of the reference appears in the sample; (3) no photo on the sample is one of the reference's photos, and the hero does not imitate the reference's hero; (4) the first screens differ in at least two of: wordmark face and position, header layout, headline face, base and accent colour (the full-bleed dark photo hero with a centred upright-and-italic headline and pill buttons was kept by the G1 pick and does not count); (5) the sample's `h1` is not a translation or close paraphrase of "A full service hair salon."; (6) below the first screen, no run of three or more consecutive bands repeats the reference's section layout and styling (same grid, card shape and heading style)
      reason: copied wording, logos and "reads as the same site" are judgements a person makes.
      scope: profile/beauty-robinhair
      reviewed: PASS @24e3256 #0ab5af1f 2026-11-19 — (1)-(6) pass vs Spoke & Weal (ref ok); no name/logo/sentence (grep spoke|weal|aveda empty); Unsplash studio/cut/tools photos unlike the field hero; wordmark, header and olive accent differ; h1 not a paraphrase; no 3-band run; evidence tree 0926c5f current

## Sample B — 로빈살롱 (`profile/beauty-robinsalon/`)

- [x] T15 Pick photos for B as in Picks, as in T1 (AC64·AC66·AC67·AC68·AC69·AC70·AC71) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py photos beauty-robinsalon`
- [x] T16 Write `index.html` and `style.css` with the markers as in T2 (AC8·AC10·AC11·AC12·AC13·AC14·AC16·AC18·AC19·AC20·AC21) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py markers beauty-robinsalon`
- [x] T17 Build the franchise flow as in T3, with B's four branches (AC22·AC23·AC24·AC25·AC26·AC27·AC28·AC29·AC30·AC31·AC32·AC39·AC40·AC42) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py franchise beauty-robinsalon`
- [x] T18 Keep the copy clean as in T4 (AC43·AC44·AC45·AC46·AC47·AC48·AC49·AC50·AC51·AC52·AC53·AC54·AC59·AC159·AC160·AC161·AC164) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py ads beauty-robinsalon`
- [x] T19 Forms, keep-all, alt, headings and Korean `h1` as in T5 (AC33·AC34·AC41·AC79·AC82·AC83) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py flow beauty-robinsalon`
- [x] T20 Keep the sample self-contained as in T6, nothing naming 박승철헤어스투디오 or STAGE (AC1·AC2·AC60·AC61·AC65·AC72) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py assets beauty-robinsalon`
- [x] T21 Give B its own mood: one Korean `display-word`, the 스타일 section with at least four photo cards named in Hangul, Hangul-only header nav and wordmark, no Roboto and none of the reference purples, a neutral white `body` (AC121·AC127·AC128·AC131·AC134·AC135·AC136·AC137) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py sample beauty-robinsalon`
- [x] T22 Register B after its visual work: `PROFILES` entry (name 로빈살롱, the B palette), `python3 scripts/profile_thumb.py beauty-robinsalon`, regenerate the gallery with `python3 scripts/build.py` (AC1·AC3·AC4·AC5·AC6·AC15·AC77) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-19-profile-beauty/check_static.py register beauty-robinsalon`
- [x] T23 Check B in a browser at 1440 and 390 as in T9, without the A-only checks, with B's: a Hangul word of 160 px or more in Song Myung on the first screen, live text overlapping a photo from `img/` that is painted in front of it, the style cards in one strip, header 지점 · 가맹 links (AC5·AC8·AC9·AC35·AC36·AC37·AC38·AC41·AC62·AC63·AC84·AC85·AC86·AC120·AC121·AC122·AC123·AC124·AC129·AC132·AC133) — verify(browser): `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinsalon`
- [ ] T24 Review B's content (AC55·AC56·AC57·AC58·AC161·AC163) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/beauty-robinsalon/` (command: `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinsalon`), read `profile/beauty-robinsalon/index.html` and `style.css`, look at the bands, and confirm items (1)–(7) of T10 for this sample; also (6) no style card names a designer or reads as a seasonal launch with a date or a count
      reason: whether copy names a person, implies a count, a testimonial or an outcome in other words is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/beauty-robinsalon
      reviewed: PASS @51c2d6d #d123e380 2026-11-19 — (1)-(7) and extra (6) pass; no names, counts, prices, testimonials, logos or claims; steps 상담→정보공개서→계약 after review; only 네이버/카카오톡; style cards plain style names, no date or count; addresses all 가상구 (index.html:95,:179); evidence tree 039d772 current
- [ ] T25 Review B's photos (AC78·AC125·AC126) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/beauty-robinsalon/` and to `/tmp/profile-beauty-shots/compare/` for beauty-robinsalon (commands as in T11, with `page beauty-robinsalon`). Open every image in `profile/beauty-robinsalon/img/`, `compare/beauty-robinsalon-1440.png` and `-390.png`, and `ref-beauty-robinsalon.png` with its `-full-NN` bands, and confirm: (1) and (2) of T11; (3) no photo shows a brick wall or lettering painted on a wall; (4) the hero neither is nor imitates a pschair.co.kr photo, and is not a row of four long-haired women standing before a wall
      reason: subject and likeness to another photo are visual judgements.
      scope: profile/beauty-robinsalon
      reviewed: PASS @51c2d6d #1202a43a 2026-11-19 — (1)-(4) pass; 6 photos hair portraits or strand close-up on plain backgrounds, no salon, brick, wall lettering or logo (native-size crops); hero one short-bob woman on cream wall, not the four-model STAGE slide (ref ok); evidence tree 039d772 current
- [ ] T26 Inspect B's photos for lettering at native resolution, as in T12 (AC78·AC158) — verify(human): as in T12, for every image file in `profile/beauty-robinsalon/img/` (on a hit, re-run T15, T22 and T23)
      reason: lettering on products in a photo is seen only by eye at full size; the fitness verdict failed once on lettering seen only there.
      scope: profile/beauty-robinsalon/img
      reviewed: PASS @847f2c8 #4bb89d61 2026-11-19 — 1:1 tiles of all 6 files (detail-hair-strands 1000x1500, hero-round-bob 1400x1890, style-bangs-bob, style-long-curl, style-short-curl, style-straight-bob 900x1125): hair, clothes, plain walls only; no lettering, logo or label; img tree 0b4f6b852548f68426f02982e8cc30322ee84d0a
- [ ] T27 Review B's full-page screenshots for overlapping or clipped text and the readability of the notices (AC87·AC88·AC162) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/beauty-robinsalon/` (command as in T24), and confirm items (1)–(5) of T13 on its `desktop-1440-NN.png` and `mobile-390-NN.png`. The display word (the AC120 word) may be covered by its photo by design (AC124) and that cover is not counted; any other text it covers, or that covers it, is
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page.
      scope: profile/beauty-robinsalon
      reviewed: PASS @51c2d6d #0b908ebc 2026-11-19 — T13 (1)-(5) pass at 1440/390; only the AC120 word 머릿결 covered by its photo (AC124); no other overlap or clipping at bands or seams; .notice 16px ink on grey (style.css:43-49), .fr-note 16px/600 on #2a2a2a (:303-310); evidence tree 039d772 current
- [ ] T28 Compare B with 박승철헤어스투디오 (AC72·AC73·AC80·AC81·AC130) — verify(human): as in T14 for beauty-robinsalon (`beauty-robinsalon-1440.png`, `-390.png`, `ref-beauty-robinsalon*`), confirming items (1)–(3) and (6) of T14 against 박승철헤어스투디오 (the style-collection strip and the giant word behind the hero photo kept by the G1 pick do not count), (4) the first screens differ in at least two of: wordmark face and position, header layout, base and accent colour, (5) the sample's `h1` and display word are not a translation or close paraphrase of the reference's hero text ("26 Hair Design Look : My Stage", "STAGE"), and (7) no style name is a translation or transliteration of "Noir sleek", "Scuro signature", "Rêve layer" or "Marie wave"
      reason: copied wording, logos and "reads as the same site" are judgements a person makes.
      scope: profile/beauty-robinsalon
      reviewed: PASS @51c2d6d #441ab165 2026-11-19 — (1)-(7) pass vs 박승철헤어스투디오 (ref ok); no name, text or photo shared; centred Hangul wordmark, header and colour differ; h1 and 머릿결 not a My Stage/STAGE paraphrase; style names not translations; lower bands differ; 390 seen as first screen only; evidence tree 039d772 current

## Sample C — 로빈헤어살롱 (`profile/beauty-robinhairsalon/`)

- [x] T29 Pick photos for C as in Picks, as in T1 (AC64·AC66·AC67·AC68·AC69·AC70·AC71) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py photos beauty-robinhairsalon`
- [x] T30 Write `index.html` and `style.css` with the markers as in T2 (AC8·AC10·AC11·AC12·AC13·AC14·AC16·AC18·AC19·AC20·AC21) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py markers beauty-robinhairsalon`
- [x] T31 Build the franchise flow as in T3, with C's three branches (AC22·AC23·AC24·AC25·AC26·AC27·AC28·AC29·AC30·AC31·AC32·AC39·AC40·AC42) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py franchise beauty-robinhairsalon`
- [x] T32 Keep the copy clean as in T4 (AC43·AC44·AC45·AC46·AC47·AC48·AC49·AC50·AC51·AC52·AC53·AC54·AC59·AC159·AC160·AC161·AC164) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py ads beauty-robinhairsalon`
- [x] T33 Forms, keep-all, alt, headings and Korean `h1` as in T5 (AC33·AC34·AC41·AC79·AC82·AC83) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py flow beauty-robinhairsalon`
- [x] T34 Keep the sample self-contained as in T6, nothing naming The Lane (AC1·AC2·AC60·AC61·AC65·AC72) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py assets beauty-robinhairsalon`
- [x] T35 Give C its own mood: greige `body` warmer than stone and darker than cream, Hangul-only header nav and wordmark, none of The Lane's colours (AC138·AC139·AC141·AC149·AC151) — verify: `python3 docs/features/2026-11-19-profile-beauty/check_static.py sample beauty-robinhairsalon`
- [x] T36 Register C after its visual work: `PROFILES` entry (name 로빈헤어살롱, the C palette), `python3 scripts/profile_thumb.py beauty-robinhairsalon`, regenerate the gallery with `python3 scripts/build.py`; the thumbnail stays light (AC1·AC3·AC4·AC5·AC6·AC15·AC77·AC153) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-19-profile-beauty/check_static.py register beauty-robinhairsalon`
- [x] T37 Check C in a browser at 1440 and 390 as in T9, without the A-only checks, with C's: letter-spaced header nav, header 지점 · 가맹 links, two tall photos side by side on the first screen with the `h1` beside them, Nanum Gothic or Sunflower for the `h1` and every `h2`, the hero link to 지점 찾기 (AC5·AC8·AC9·AC35·AC36·AC37·AC38·AC41·AC62·AC63·AC84·AC85·AC86·AC140·AC142·AC143·AC144·AC147·AC148·AC152) — verify(browser): `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinhairsalon`
- [ ] T38 Review C's content (AC55·AC56·AC57·AC58·AC161·AC163) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/beauty-robinhairsalon/` (command: `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page beauty-robinhairsalon`), read `profile/beauty-robinhairsalon/index.html` and `style.css`, look at the bands, and confirm items (1)–(7) of T10 for this sample
      reason: whether copy names a person, implies a count, a testimonial or an outcome in other words is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/beauty-robinhairsalon
      reviewed: PASS @24e3256 #aa58f2dd 2026-11-19 — (1)-(7) pass; no names, counts, prices, testimonials or claims; 두피 케어 line describes washing, not an outcome; steps 상담→정보공개서→계약 after review; brands only 네이버/카카오톡; addresses all 가상구; evidence tree 5f4da94 current
- [ ] T39 Review C's photos and wordmark (AC78·AC145·AC146·AC150) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/beauty-robinhairsalon/` and to `/tmp/profile-beauty-shots/compare/` for beauty-robinhairsalon (commands as in T11, with `page beauty-robinhairsalon`). Open every image in `profile/beauty-robinhairsalon/img/`, `compare/beauty-robinhairsalon-1440.png` and `-390.png`, and `ref-beauty-robinhairsalon.png` with its `-full-NN` bands, and confirm: (1) and (2) of T11; (3) the two tall first-screen photos show salon interiors or hair scenes in soft daylight; (4) neither is or imitates a thelanesalon.com photo: neither is a black salon chair before a mirror with palm fronds, nor books and magazines on a table beside a plant; (5) the wordmark has no vertical rule followed by stacked letters
      reason: subject, light, likeness to another photo and the shape of a wordmark are visual judgements.
      scope: profile/beauty-robinhairsalon
      reviewed: PASS @24e3256 #51338290 2026-11-19 — (1)-(5) pass; chair-round-mirror, updo-window-light, tools-flatlay are hair/salon/tools, no lettering; both tall first-screen photos in soft daylight; neither is The Lane's empty-chair or books hero (ref ok); wordmark one letterspaced line, no rule or stacked letters (index.html:21, style.css:58-65); evidence tree 5f4da94 current
- [ ] T40 Inspect C's photos for lettering at native resolution, as in T12 (AC78·AC158) — verify(human): as in T12, for every image file in `profile/beauty-robinhairsalon/img/` (on a hit, re-run T29, T36 and T37)
      reason: lettering on products in a photo is seen only by eye at full size; the fitness verdict failed once on lettering seen only there.
      scope: profile/beauty-robinhairsalon/img
      reviewed: PASS @24e3256 #5c9c38d8 2026-11-19 — 1:1 500px tiles plus 2-5x contrast crops of chair-round-mirror.jpg 910x1500, tools-flatlay.jpg 1000x1500, updo-window-light.jpg 1000x1500 (mirror, chair, scissors, brushes, comb, claw clip, hand mirror, window): no lettering, logo, label or engraving; img tree 7103a8e50cff9165b295a73390c355b7421bcced
- [ ] T41 Review C's full-page screenshots for overlapping or clipped text and the readability of the notices (AC87·AC88·AC162) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/beauty-robinhairsalon/` (command as in T38), and confirm items (1)–(5) of T13 on its `desktop-1440-NN.png` and `mobile-390-NN.png`
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page.
      scope: profile/beauty-robinhairsalon
      reviewed: PASS @24e3256 #3bf1b691 2026-11-19 — (1)-(5) pass; no overlap or clipping in 1440/390 bands or crops; .notice 16px ink on panel (style.css:42-47), AC42 .fr-note 16px/700 ink on greige (:264-268), body 16px (:20); evidence tree 5f4da94 current
- [ ] T42 Compare C with The Lane (AC72·AC73·AC80·AC81) — verify(human): as in T14 for beauty-robinhairsalon (`beauty-robinhairsalon-1440.png`, `-390.png`, `ref-beauty-robinhairsalon*`), confirming items (1)–(3) and (6) of T14 against The Lane (the greige base, spaced navigation and tall photo pair kept by the G1 pick do not count), (4) the first screens differ in at least two of: wordmark face and layout, header layout (The Lane's taupe top bar), headline face, accent colour, and (5) the sample's `h1` is not a translation or close paraphrase of The Lane's hero line ("A clean beauty salon specializing in …")
      reason: copied wording, logos and "reads as the same site" are judgements a person makes.
      scope: profile/beauty-robinhairsalon
      reviewed: PASS @24e3256 #1ae26f27 2026-11-19 — (1)-(6) pass vs The Lane (ref ok); no Lane name, text or photo; h1 '조용한 오후에 머리를 다듬는 곳' not a paraphrase; wordmark, header and headline face differ; no 3-band run of its sections; evidence tree 5f4da94 current

## Gallery and branch

- [x] T43 Regenerate the gallery with all three entries: 미용실 chip count 3, a card per sample, no beauty 준비 중 tile, no other beauty entry, distinct names, accents achromatic or saturated and chromatic ones at least 25° from every other chromatic accent, no hex shared across the three palettes (AC3·AC17·AC75·AC76·AC89·AC90·AC91·AC157) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-19-profile-beauty/check_static.py gallery`
- [x] T44 Check the gallery: the 미용실 filter shows the three cards and no 준비 중 tile; each card, from a fresh load, opens the preview with that sample, its desktop/mobile buttons switch the width, Esc closes it (AC89·AC90·AC92·AC93·AC94) — verify(browser): `python3 docs/features/2026-11-19-profile-beauty/check_browser.py gallery`
- [x] T45 Check that the three samples' `h1` faces and header wordmark faces differ pairwise (AC154·AC155) — verify(browser): `python3 docs/features/2026-11-19-profile-beauty/check_browser.py trio`
- [ ] T46 Review the three wordmarks side by side (AC156) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/compare/` for the three beauty samples (command: `python3 docs/features/2026-11-19-profile-beauty/check_browser.py compare`). Set the headers of `beauty-robinhair-1440.png`, `beauty-robinsalon-1440.png` and `beauty-robinhairsalon-1440.png` side by side, and the same at `-390.png`, and confirm: (1) the three wordmarks differ in face (stroke weight, serif or sans, letter shape); (2) they differ in layout (size, letter-spacing, position in the header); (3) 로빈헤어 and 로빈헤어살롱 do not read as one mark with a suffix added
      reason: whether two marks read as one is a visual judgement.
      scope: profile/beauty-robinhair, profile/beauty-robinsalon, profile/beauty-robinhairsalon
      reviewed: PASS @51c2d6d #4391ddee 2026-11-19 — (1)-(3) pass; faces Myeongjo 800 / Song Myung brush / Sunflower 300; B centred 48px over nav; A and C share left header position but differ in weight, tracking (-0.03em vs 0.32em) and colour, so 로빈헤어살롱 does not read as 로빈헤어 plus suffix; compare trees current
- [x] T47 Keep the branch inside its scope (AC7) — verify: `base="$(git merge-base main HEAD)" && test -n "$base" && test -z "$(git diff --name-only "$base" | grep -v -e '^profile/beauty-robinhair/' -e '^profile/beauty-robinsalon/' -e '^profile/beauty-robinhairsalon/' -e '^profile/index\.html$' -e '^scripts/profiles\.py$' -e '^docs/')$(git diff --name-only "$base" -- docs/profile-playbook.md)"`
- [ ] T48 Compare the twelve designs (AC74) — verify(human): apply the evidence rule to `/tmp/profile-beauty-shots/compare/` for the three beauty samples and to each `/tmp/profile-beauty-shots/<slug>/` (commands: `python3 docs/features/2026-11-19-profile-beauty/check_browser.py compare`, `python3 docs/features/2026-11-19-profile-beauty/check_browser.py page <slug>`). In `compare/`, set each beauty sample's `-1440.png` and `-390.png` beside those of `flower-bomgyeol`, `food-saebyeokmil`, `clinic-neuru`, `clinic-byeotteul`, `clinic-bonui`, `law-ganeum`, `law-goim`, `fitness-mideoum`, `fitness-jjuuk` and the other two beauty samples; for the rest of each page use the bands in `/tmp/profile-beauty-shots/<slug>/` and the `-full-NN.png` bands of the shipped samples in `compare/`. Confirm for each beauty sample, against each of the eleven others: (1) the first screens differ in at least two of: hero composition (photo placement and size, where the headline sits), wordmark face and position, base and accent colour; (2) the rest of the page does not repeat the other's section layout and styling: no run of three or more consecutive bands with the same grid, card shape and heading style. Shared elements that every sample needs (sample notice, footer credits, a mobile bottom bar, the branch-entry controls) do not count. Pairs to look at hardest: A with `flower-bomgyeol`, `law-ganeum` and `fitness-mideoum`; B with `clinic-neuru`; C with `clinic-bonui` and `law-goim`
      reason: "reads as the same design" is a taste judgement a person makes.
      scope: profile/beauty-robinhair, profile/beauty-robinsalon, profile/beauty-robinhairsalon
      reviewed: PASS @51c2d6d #b4033987 2026-11-19 — (1)(2) pass for A, B, C against all eleven others; first screens differ on 2+ axes per pair; no 3-band run of same grid, card shape and heading style; closest A vs C share section order and grid in 4 bands but card shape and heading face differ in each; evidence trees current

Always last, never removed:

- [x] T49 Reconcile `docs/current_system/` with what shipped (in `profile-samples/component.md`, the Source line lists `beauty-robinhair`, `beauty-robinsalon` and `beauty-robinhairsalon`), and set `last_reconciled` in `overview.md` to the new HEAD (AC95·AC96) — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && python3 docs/features/2026-11-19-profile-beauty/check_static.py current`
