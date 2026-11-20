---
status: shipped
test: `python3 docs/features/2026-11-20-profile-crypto/check_static.py all`
test(browser): `python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robincoin; a=$?; python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robincustody; b=$?; python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robinchain; c=$?; python3 docs/features/2026-11-20-profile-crypto/check_browser.py thumb crypto-robincoin; d=$?; python3 docs/features/2026-11-20-profile-crypto/check_browser.py thumb crypto-robincustody; e=$?; python3 docs/features/2026-11-20-profile-crypto/check_browser.py thumb crypto-robinchain; f=$?; python3 docs/features/2026-11-20-profile-crypto/check_browser.py gallery; g=$?; python3 docs/features/2026-11-20-profile-crypto/check_browser.py trio; h=$?; exit $((a|b|c|d|e|f|g|h))`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()" && python3 -c "import urllib.request as u; [u.urlopen(x, timeout=10) for x in ('https://fonts.googleapis.com/css2?family=Gasoek+One', 'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300', 'https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@700', 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css')]"`
commits: 018ff13e572b41751a6aacba546aff0df11976d0..dac1a954cf3b96827d04cb6244ba9140fe34fdcd
---

# Crypto profile samples (`crypto`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the existing `profile-samples` component (spec Scope, `Design: none`). There are no modules to
order. The tasks go sample by sample: A `crypto-robincoin`, then B `crypto-robincustody`, then D `crypto-robinchain`.
Registration, the gallery and the branch come after them. Every command runs from the repository root. A task names
one sample. The tasks of "Gallery, the three together and the branch" check what the three samples share (the gallery,
AC19, AC119, AC125–AC128, AC258, AC259, AC263, AC264), so they name all three.

The checks live next to this file and were written with it, before any sample exists; until then they fail:

- `check_static.py <check> [<slug>]`: standard library and `sips`; no browser, no network. Without `<slug>`, a
  per-sample check runs for all three samples.
- `check_browser.py page <slug> | thumb <slug> | gallery | trio | compare`: Playwright driving the installed Google
  Chrome. It serves the repository on a free local port itself and stops the server when it ends (never `file://`,
  playbook §4). It prints its verdict and exits without waiting for Chrome to close (the Playwright driver ends
  Chrome), and fails a run that has no verdict after 900 s; the eight commands of `test(browser)` take about two minutes together. It needs the network for web fonts, which `preflight(browser)` checks. `compare` is not a check: it
  saves first-screen shots of the samples and of the reference sites for the reviews below, and exits 0 even when a
  reference site does not answer.

`check_static.py` and `check_browser.py` are approved together with this file. Changing what they check is a change
to approved checks and goes back to a person for re-approval. The Picks are approved with it too.

## Picks (agent decisions)

Names, slugs, palettes and faces are spec AC150, AC193, AC224 and A5, A6. Card titles are spec A15. No sample uses a
photo (AC262). Copy is written in the implement stage and obeys AC53–AC76 and the 업태 blocks.

Headlines. AC179, AC232 and AC261 are decided by the length of the copy, so the `<h1>` texts are fixed here:

- **A:** `가상자산 거래를<br>단정한 화면으로` (two lines, broken by the `<br>`).
- **B:** `디지털자산을 <em>나누어 보관</em>하고 <em>함께 승인</em>합니다` (two lines at 1440 and at 390).
- **D:** `<span>블록체인을</span><span>제품으로</span><span>만듭니다</span>` (the second line in lime).

Section headings (`<h2>`) and order, after the first section:

- **A:** 서비스 안내; 이용 방법 (inside the dark panel); 화면 예시 (the grey band with the asset card); 고객센터 문의.
- **B:** 하는 일; 보관 방식 (the three word cards: 분리 보관, 다중 승인, 오프라인 보관); 도입 절차; 도입 문의.
- **D:** 서비스 (the bento cards: 스마트 컨트랙트 개발, 지갑 연동 개발, 노드 운영 대행, 보안 점검 지원); 진행 과정 (the
  lime band); 프로젝트 문의.

Bars. Every sample has, as the first element of `<body>`, a sample-marker strip: one `<p>` with the full marker text,
`position: sticky; top: 0`, 38 px high, text at 16 px (the body size), on an opaque background colour of its own (AC12). The `<header>` is sticky directly under the
strip and holds the 문의 link of the sample, so that link is on screen at every scroll position and no bottom bar is
needed (AC42, AC43, AC149). The strip and the header together cover 92–98 px at 390.

Pictures (spec A10), drawn new as inline SVG:

- **A:** the price line is one `<polyline>` in the phone; the phone and the panel are CSS boxes.
- **B:** six nested rounded squares (`<rect rx>`), each turned 8° more than the one outside it, two short `<line>`
  ticks at the sides and one centre dot 10 px wide; `fill="none"` on the `<svg>`, strokes `#2a1d14` at 1.5 px.
- **D:** three stacked rings (`<ellipse>`, stroke `#a9ef2c` at 10 px, opacity 1, 0.7 and 0.4), lit by
  `filter: drop-shadow(0 0 36px rgba(169, 239, 44, 0.5))` on the `<svg>`. No glyph, no slab (AC241).

Sizes measured on a fixture on 2026-11-20 (Chrome, real web fonts, 1440×900 and 390×844), as a starting point:

- A at 1440: strip 0–38, header 38–102, wordmark text 40–121 px (24 px, centre 81); panel 600×600 from (72, 134);
  phone 340 px wide from 56 px below the panel's top; `<h1>` at 68 px, line-height 1.15, text 744–1155 px, box 2.30 ×
  its font-size; links at 534 px; AC32 sentence at 606 px.
- A at 390: header 38–94 with the wordmark at 22 px and the three pills (34 px high, 13 px text) on one line; `<h1>`
  at 34 px from 118 to 200; links, the AC32 sentence to 396; panel 350×460 from 420 (AC183 allows 720); phone 280.
- B at 1440: header pill 56–1384 × 52–124 (72 px high, 14 px under the strip); wordmark at 30 px, text centre 731;
  `<h1>` at 62 px, weight 300, line-height 1.25, `max-width: 680px`, text 120–777 px, two lines (box 2.5 ×); drawing
  480×480 from (840, 256); the first section ends at 900 through `min-height: calc(100vh - 124px)`.
- B at 390: header 12–378 × 50–110, wordmark 25 px; `<h1>` at 32 px, two lines; drawing 260 px wide under the copy;
  the first section ends at 844.
- D at 1440: header 140–1300 × 50–110, wordmark at 36 px with its text from 172 to 299 px (centre 236); `<h1>` at
  76 px, line-height 1.2, each line 91 px high (1.2 ×), widest line 335 px; links at 571 px; object 440×440 from
  (860, 184).
- D at 390: `<h1>` at 40 px (widest line 176 px of 350; `Gasoek One` sets a Hangul syllable 0.88 em wide), wordmark
  32 px (text 32–145 px; the 프로젝트 문의 pill starts at 266 px), object 240 px.
- Wordmark distances (AC258, measured on rendered text): 155 px between A and D as picked. At the worst allowed ends
  (A at 64 px left and 25 px; D at 150 px left and 35 px) the centres are 106 px apart. A mark drawn inside A's
  wordmark link moves A's text right and eats that margin: keep A's wordmark text within 64 px of the left edge.
- Glass bar (AC226): over the lime band, `rgba(48, 48, 48, 0.7)` leaves the lime wordmark at 4.38:1, and
  `rgba(48, 48, 48, 0.75)` at 4.96:1. The pick `rgba(22, 26, 28, 0.8)` gives more.

## Fixed parameters of the checks (the page contract)

- **First screen** is 1440×900 and 390×844. "Visible" means inside the viewport, opacity (multiplied up the
  ancestors) above 0.5, the text whole (not cut by an `overflow` box of its own or of an ancestor, no ellipsis, not
  pushed off the side by `text-indent`), and not covered at its centre by an element (or its `::before`/`::after`) painted above it
  with a background image or colour at alpha × opacity above 0.5, judged 1.5 s after load. For the four fixed texts (the
  sample marker, the AC31 and AC58 sentences, the example marker) it also means drawn as written (spec A22): no `filter`, `transform`,
  `scale`, `zoom`, `mask-image` or `mix-blend-mode` on the element or on any ancestor, and no `-webkit-text-fill-color`
  other than its `color`. So the marker strip, the footer, the contact section and A's phone are placed and sized without those properties. "At every scroll position"
  (AC12, AC42) is every 40 px down to the end, each within 1.5 s. 390 px overflow (AC134) is judged inside a
  `width:390px` iframe; for AC133 and AC134 an element that reaches past the right edge fails even when `overflow-x`
  on `<html>` or `<body>` hides it (a wrapper that clips it inside the page is fine); everything else at 390 in a 390×844 viewport.
- **Markup the checks find by name:** `<a class="wordmark">` in the first `<header>`; A's example blocks
  (`data-example`) and, inside the first one, one `class="phone"`; B's three `class="word-card"`, each with one
  `class="term"` and one `<p>`. Everything else is found by tag, order or computed style. Write explicit end tags.
- **Sample marker** (AC8–AC12 · AC147): the full text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" as the own text of
  one element (not CSS `content:`, not split over child elements), with the `·` U+00B7, at the body font size or
  larger and at least 14 px. The element that stays on screen (AC12) is found the same way; it, or an element between it and its
  fixed or sticky ancestor (that ancestor included), has a background colour of alpha 1. AC13, AC14 and AC58 read
  the last `<footer>` that is not inside an `<article>`.
- **Sentences** (AC31 · AC32 · AC58–AC60 · AC83 · AC148): each fixed sentence is the own text of one element, written
  exactly as in the spec. The AC31 sentence in the contact section is set at 14 px or more at both widths, read on
  the copies that are visible there (the largest counts, as for AC148). AC59 and AC60 are checked on every displayed copy of the AC58 sentence, not on the footer's
  alone.
- **Sections** (AC28–AC30): each of the service, steps and contact sections is a `<section id="…">` with its own
  `<h2>`. A check finds a section by that `<h2>`: 서비스 or 하는 일; 절차, 과정 or 이용 방법; 문의 or 상담. Exactly one
  section may match each pattern, so the steps heading holds neither 문의 nor 상담 and no other `<h2>` holds 서비스
  ("서비스 문의" and "상담 절차" fail). The service section names its things as three or more `<li>` or `<h3>`. The
  steps are three or more `<li>` children of one `<ol>`.
- **First section** (AC180 · AC210 · AC211 · AC236 · AC239): every element before the service section in document
  order that is not inside the `<header>` and not inside a `position: fixed` or `sticky` element. Links are counted
  when displayed; in A, links and `<svg>` inside an example block are left out. B's drawing is the only
  `<svg aria-hidden="true">` there, an icon inside a link included, so B's first-section link holds no `<svg>`.
- **Contact section** (AC31 · AC35–AC39 · AC44–AC46): four separate links whose accessible names (`aria-label`, else
  text) contain 카카오톡, 전화, 네이버 예약 and 네이버 지도. The 상담 hours are `HH:MM–HH:MM` (also `-`, `—`, `~`). The
  closed-days line holds 휴무, 휴관, 쉽니다, 쉬어요, 쉬는 날 or 쉼 and a day name (일요일, 공휴일, 주말, 토요일 …) in one
  block, or one of the two in a label of at most 12 characters and the other in the next block
  (`<dt>쉬는 날</dt><dd>토요일 · 일요일 · 공휴일</dd>`). A closed-days block that holds 에도, 없이, 문의 or 휴무 없 is not
  counted (it reads as "no closed day"), so keep those words out of it. The section shows an address with "(가상 주소)" and `02-000-0000`.
- **Links** (AC40–AC43 · AC49 · AC56): every `<a>` has `href="#"` or `href="#<id on the page>"`; there is no `tel:`
  and no `mailto:` link. AC56 reads a link's accessible name and its text: in A exactly one header link is named
  로그인 and one 회원가입; in B and D no link holds 로그인, 회원가입, 가입하기 or 시작하기. The contact link of AC40–AC42 is an `<a href="#<contact section id>">` whose text contains
  문의 or 상담. AC43 reads the last element with its own text in the last `<footer>`.
- **Painted with elements:** bars and the backgrounds behind text are elements, and the checks fail the other way of
  drawing them. A `::before`/`::after` rule (also written `:before`, in a grouped selector, inside `@media` or
  with an `@media` or another rule nested in it, in `style.css` or `<style>`) may set `position` to `absolute`, `relative` or `static` only; `fixed`, `sticky`,
  `inherit` or a `var()` there fails AC149 in `check_static.py a11y`. A generated `::before`/`::after` (a `content`
  other than `none`, not `display: none`) with a `background-image` or a background colour of alpha above 0 fails AC60
  and AC132 for all text in its element, wherever the layer sits: a list dot, a step number badge, an underline bar or a card's colour
  edge beside text is an empty `aria-hidden="true"` element or a `border`, not a pseudo-element with a background. An
  element that holds no text (D's lit object, a line drawing, a dot element) may paint its `::before`/`::after`
  freely. A pseudo-element painted with `border`, `box-shadow` or `outline` alone is not read, nor is text other than the four fixed texts (First screen) hidden by
  `filter`, `transform` or `-webkit-text-fill-color`; the full-page reviews (T9, T19, T29) look at those.
- **Bars** (AC149): at 390, at scroll 0 and at mid-page, the check adds up the viewport height under every displayed
  `position: fixed` element and every `sticky` element that sits at its `top` or `bottom` offset (within 1 px);
  overlapping bars count once. A closed overlay is `display: none` or `visibility: hidden`. Only elements are
  counted, so a pinned `::before`/`::after` is barred outright (Painted with elements).
- **Header nav** (AC255): one `<nav>` in the first `<header>` with four or more `<a>`, each with an `href` starting
  with `#` and a text with a Hangul syllable and no Latin letter. It may be `display: none` at 390.
- **Measured boxes:** the horizontal edges and the horizontal centre of an `<h1>` and of a header wordmark are those
  of the rendered text (the union of its text nodes' line boxes), so neither `display: block`, padding nor a mark
  beside the text moves them (spec, per-sample preamble). This holds for AC153, AC177, AC200, AC202, AC203, AC206,
  AC229, AC235, AC258 and AC260. "Inside the viewport" and "not covered" read the element's box. The line-count
  checks read the element's box height: give the `<h1>` no vertical padding and keep its `line-height` from 1.0 to
  1.45 in A (AC179), from 1.0 to 1.3 in B (AC261), and above 0.75 up to 1.5 on D's three `<span>` (AC232). An element
  "with its own text" has a non-blank text node as a direct child.
- **Faces** (AC99 · AC101 · AC125 · AC126 · AC253 · AC254): the checks read the first family of the computed
  `font-family`. AC99 also needs every font Chrome renders for the `<h1>` and the `a.wordmark` (CDP
  `CSS.getPlatformFontsForNode`, descendants included) to be a loaded web font whose family name starts with the
  sample's face: Pretendard in A, `Noto Sans KR` or `Noto Serif KR` in B's `<h1>`, `Noto Serif KR` in B's wordmark,
  `Gasoek One` in D. A face that never loads, a fallback that draws a glyph, or a copy installed on the machine
  fails; so start the stack with `"Pretendard Variable"`. Every sample links the Pretendard
  stylesheet on jsDelivr (AC101; `check_static.py assets`): without it the body renders in a fallback. AC101 and
  AC254 also need the first family to be a name the linked stylesheets define (the variable sheet defines
  `Pretendard Variable`, not `Pretendard`), so a copy installed on the checking machine does not pass. Every element set in `Gasoek One` has `font-weight: 400`:
  headings are bold by default, so the rule that sets the face also sets the weight (AC253).
- **Body colours** (AC128 · AC151 · AC194 · AC225): the last `background`/`background-color` and the last `color` in a
  top-level `body` rule of `style.css`, each one colour written as hex or `rgb()`, or a `var()` that `:root` or `html`
  defines so. Every other rule whose subject is `body` (`html body`, `body.x`, a `body` rule inside `@media`, in
  `style.css`, `<style>` or `style=""`) sets the same colour or none.
- **Colours the checks parse** (AC221 · AC249): AC221 reads every `background`, `background-color` and
  `background-image` value in B's `style.css`, `<style>` and `style=""`, at any nesting, with `var()` resolved from
  every rule that defines the property. AC249 reads every declaration value in D's `style.css` and the `fill`,
  `stroke`, `stop-color`, `flood-color` and `color` attributes of its inline SVG. Write every colour there as hex or
  `rgb()`/`rgba()` with plain numbers. `hsl()`, a colour name other than `black`, `white` and the exact greys (`gold`, `lime`, `tan`) or an undefined
  `var()` fails, because the check cannot read it. `rgba(123, 35, 56, 0.6)` fails AC221: a saturated background is opaque.
- **Contrast** (AC60 · AC132): for every displayed element with its own text outside an `<svg>`, the text colour
  (with its alpha and the opacity of its ancestors) against the background colours of its ancestors, composited down
  to the first opaque one. Text over a CSS `background-image` (a gradient too) fails, because the check cannot judge
  it; so does text whose element or any ancestor up to `<html>` has a `::before`/`::after` with a background (Painted
  with elements). No single text colour reaches 4.5:1 at both ends of A's panel gradient (white is 2.9:1 on `#3f9cf0`), so text
  in the panel sits on the phone or on another flat opaque surface, and the AC83 sentence sits in the phone or in the
  element directly after the panel. A copy that an `overflow` box cuts off (the phone runs off the panel's lower
  edge) is not counted for AC83: keep it above the cut, or put it after the panel. D's light is a `filter` on the `<svg>`, or a `radial-gradient` on a wrapper that
  holds no text. A sticky header is judged over the `body` colour, not over what scrolls under it.
- **Page text** (AC25 · AC26 · AC53–AC55 · AC61–AC70 · AC85 · AC95 · AC97 · AC190 · AC251) is the text of `index.html`
  outside `style`, `template` and `title` (inline SVG text included), plus the `<title>` text, `meta` description
  and `og:` content, `aria-label`, `alt` and `title` attributes, and the strings of CSS `content:` declarations
  (`style.css`, `<style>` and `style=""`; a `content:` with `attr()` fails); whitespace collapsed. Matching is the
  spec's: plain substrings; a listed word with a space also matches without it; a word with a Latin letter in any
  case; a word made only of Latin capitals and digits as a whole word in any case; full-width forms folded, soft hyphens
  and zero-width characters dropped. Inline elements join with no space, so `<strong>로빈코인</strong><span>원화</span>`
  reads 로빈코인원화 (코인원). Words that hit in an allowed
  sense are rewritten, not exempted. Traps confirmed on the fixture: 지금 사용 (지금 사), 토스트 (토스), 고객사, 최대한
  and 최고급 (최대, 최고), 확실히, 보장 and 보증 even in "보장하지 않습니다", 수익성 and 수익 구조 (수익), 트리플 and 리플렛
  (리플), 자신한 (신한), 이율배반 (이율), 복리후생 (복리), 필수상담 and 수상한 (수상), 미스리딩 (리딩), 재단하다 (재단, D),
  코드 리뷰, 컨트랙트 이벤트 and 오픈소스 라이선스 (spec A14), `ico` as a word (ICO, D), 줄이자, 높이자 and 차이자 (이자), 목표가 정해지면 (목표가), 참신한 and 혁신한 (신한),
  속도지만 (도지), 시작하기 전에 (시작하기, A).
  "icon", "SOLID" and 개발사이자 pass.
- **Figures** (AC74 · AC77) are read per block (a `p`, `li`, `dd`, heading …; the `<title>`, each attribute and each
  CSS `content:` string is its own block), outside every example block, full-width digits folded, after the four
  uncounted kinds are taken out (`02-000-0000`, `000-00-00000`, `HH:MM`, the 3 of 웹3 or Web3). A hit is a digit
  before `%`; a digit, optional spaces, then 원, 만, 억, 조, 달러, 명, 건, 배 or 개국 (also after 천, 백 or 십); `₩`, `￦`
  or `$` beside a digit; a thousands comma; a block that holds only a number, followed by a block that starts with `%`
  or with one of the units (`<div>30</div><div>만 명</div>`). Traps: a building name after the lot number
  ("결로 12 명인빌딩"); a step number before 만남, 원하는, 건너, 명확 or 배포 in one block
  (`<span>1</span>만남` in one `<li>`; put the number in CSS, or use 하나 · 둘 · 셋). "평일 09:00–18:00", "웹3 만드는"
  and "결로 12 (가상 주소)" pass.
- **Wallet-shaped strings** (AC51) are searched in `index.html` and `style.css` after `http(s)://` URLs, CSS `url()`
  and the SVG attributes `d`, `points`, `viewBox` and `transform` are taken out, and in the page text, where a string
  split over `<wbr>` or `<span>` reads as one. An `integrity` hash on a `<link>` matches too: write none.
- **Numbers** (AC20 · AC22–AC24): addresses are block text matching `<한글>로|길 <번호>`, `<한글>동N가 <번호>`,
  `<번호> 번지` or `<한글>구|군|시 <한글>동 <번호>`; every such block holds "(가상 주소)". Every phone number is
  `02-000-0000`, whatever its separators (`02)…`, no separator, full-width digits, a `content:` string). 사업자등록번호 is
  `000-00-00000`. AC24 fails on 등록번호 without 사업자 before it, on 신고번호, 인증번호, 허가번호, 인가번호 and 면허번호,
  on 통신판매(업) directly before 등록 or 신고, on any `제 <number> 호` (digits and hyphens, a place name between them
  allowed: 제2026-서울강남-0001호), and on Registration, Licence, Certificate or Certification before No., Number or `#`.
- **Example blocks** (A; AC77–AC84 · AC159 · AC163–AC175 · AC187): exactly two elements with `data-example`, not
  nested; the first is the panel and the second the asset card. Each holds one element whose own text is "예시 화면 ·
  실제 시세가 아닙니다". An asset name is an element whose own text is "예시 자산" plus one Latin capital; a price is
  an element whose own text is digits (with commas) and 원; a change figure is an element whose own text ends in `%`
  and starts with `+` or `−` (U+2212, not a hyphen). A row is an `<li>` with one of each. No other Latin letter is in
  a block. The block holds no `<a>`, no `tabindex` and no `cursor: pointer`. The phone's first text is the example
  marker; its largest text is one price element, directly after an "예시 자산 A" element (AC166). `tabular-nums` is
  set on the block (AC174).
- **A's lower parts** (AC184–AC188): the dark panel is the nearest ancestor of the steps `<ol>` with the background
  `#0c1222` and a border-radius of 32 px or more; it holds no `<svg>` at all and no digit in its text. The band is
  an ancestor of the asset card that spans the viewport width.
- **B's parts:** AC195 reads `<html>`, `<body>`, every element and every `::before`/`::after` that intersects the
  first screen; no gradient, no image, at 1440 and at 390. AC196: the service section starts at or below the bottom
  of the first screen, and the topmost painted background at 4 px from each side edge, at mid-height and at 4 px
  above the bottom, is `#f5c08a` (fixed and sticky bars are looked through). AC199 samples the points 6 px above and
  6 px below the `<header>` at its horizontal centre, bars included: the marker strip must end 6 px or more above the
  header. AC212 counts `<path>`, `<rect>`, `<line>`, `<polygon>`, `<polyline>` and `<circle>`; a `<line>` has a
  computed `fill` too, so set `fill="none"` on the `<svg>`. AC220 needs a top border wider than 0.
- **D's parts:** AC226 and AC227 read the `<header>` element itself (its own `position`, background and
  `backdrop-filter`), at scroll 0 and at 1200. The cards of AC243 are the outermost elements of the service section
  with the background `#161a1c` and a border-radius of 20 px or more. The band (AC245–AC247) is the steps
  `<section>` itself; every element with its own text in it has the colour `#07090a`; its `<ol>` has three `<li>`.
  The object (AC239–AC242) is the one `<svg aria-hidden="true">` of the first section outside a link; AC240 reads
  the `<svg>` and its parent.
- **Folder and hosts** (AC1 · AC57): the folder holds `index.html`, `style.css` and `thumb.jpg` and no other file
  (dotfiles aside): no second page, no second stylesheet. A URL is judged with entities decoded and in any letter
  case, `//host` included.
- **Images** (AC102–AC116 · AC262): the sample has no `<img>`, `<picture>` or `<source>`, no `img/` folder, no `.svg`,
  `.png` or `.gif` file, no CSS `url()` to a local file, no `data:` URL of any kind (an icon is an inline `<svg>`) and no "Photos:" text in the footer.
  AC104–AC116 hold with nothing to check once that is so.
- **Thumbnail** (AC5): `check_browser.py thumb` compares `thumb.jpg` with a fresh 1440×900 first screen (both scaled
  to 160×100, mean absolute RGB difference at most 15 of 255 over the image and at most 40 in every 10×10 tile). It
  catches a changed colour or layout, not a changed line of text, a removed thin drawing or a recoloured button (T40 item 6 looks at those), so re-running `profile_thumb.py` after any
  first-screen change, a review fix included, is the implementer's step. Make the thumbnail last.
- **Screenshots** for the reviews go to `/tmp/profile-crypto-shots/<slug>/`: `desktop-1440.png` and `mobile-390.png`
  (full page, after a scroll through), the same cut into 1200 px tall bands (`desktop-1440-01.png` …), and
  `summary.txt` written last (`site tree` = `git rev-parse HEAD:profile/<slug>`, `site working tree` clean, dirty or
  unknown, the page heights, `result PASS|FAIL`). `compare` rewrites `/tmp/profile-crypto-shots/compare/`:
  `<slug>-1440.png` and `<slug>-390.png` first screens for the three crypto samples and the fifteen shipped samples;
  `<slug>-thumb.jpg` for the three crypto samples; full pages of the fifteen shipped samples (`<slug>-1440-full.png`,
  `<slug>-390-full.png` and their `-NN` bands); `ref-<slug>.png` (1440 first screen), `ref-<slug>-full.png` and its
  `-NN` bands and `ref-<slug>.txt` (visible text) of each sample's reference home page, keeping the last good copy
  when a site does not answer; and `summary.txt` with a `local <slug> tree <hash> clean|dirty` line per sample and a
  `reference <slug> <url> ok|cached <date>|unreachable` line per reference.
- **Gallery** (AC6 · AC137 · AC138 · AC140–AC142): `check_static.py gallery` also needs the card data in the
  generated `profile/index.html` (`pf-data`: title, name, summary, features, palette) to equal the `PROFILES` entry,
  so a `profiles.py` edit without `python3 scripts/build.py` fails. AC137 · AC138 after one click on the 코인 · 가상자산 chip; AC140–AC142 for
  each card on a fresh load of `/profile/`. AC140 needs the iframe `src` to end in `/profile/<slug>/` and the loaded
  frame to be that page with a `header a.wordmark`.
- **Evidence rule** for the reviews: a sample's page folder `/tmp/profile-crypto-shots/<slug>/` is current when its
  `summary.txt` exists, its `site tree` equals `git rev-parse HEAD:profile/<slug>`, its `site working tree` is
  `clean` and its last line is `result PASS` (a failed `page` run, a web font that did not load included, is not evidence); the compare folder is current for a sample when `compare/summary.txt` has that sample's `local` line with
  the same tree and `clean`. A review uses a current folder as it is and runs the named command only when the folder
  is not current. That command starts a browser, so it runs only when a person asked for browser checks (AGENTS.md
  §6-5); otherwise the evidence is missing and the review is UNSURE, noting that it needs a browser run. If the folder
  is still not current after the run, the review is UNSURE. Adding `thumb.jpg` (T31, T33, T35) changes the tree, so a
  page folder written before it is not current: the reviews are closed after registration, on a `page` run made
  after it, and item (9) of T8 reads the entry that registration added. `compare` exits 1 while a crypto sample's
  folder is missing. A `cached` reference is evidence. An `unreachable`
  reference does not by itself make a review UNSURE: the review then judges the reference items against the spec's
  description of that reference (the Candidate A, B or D text and sketch, "Reference fonts and colours", and AC176,
  AC192, AC213, AC241) and says so in its note. For A it also sets the sample beside
  `/tmp/profile-crypto-shots/ref-g1-coinbase.jpg`, the Coinbase first screen the human saw at G1 (spec A20); `page`
  and `compare` do not touch that file, and nothing else may delete it. If the file is missing, T10 is UNSURE. On 2026-11-20 `coinbase.com` answered headless Chrome with HTTP 403 (`unreachable`), and `copper.co`
  and `kaia.io` answered; so A's reference review is expected to use the spec's description.

## Sample A — 로빈코인 (`profile/crypto-robincoin/`)

- [x] T1 Write `index.html` and `style.css` with the sample marker (in the strip and in the footer), a `<title>`, a description and `og:` texts with 디자인 샘플, noindex, the footer credit and risk sentence, the live-text wordmark 로빈코인, fictional address, phone and 사업자등록번호, and no other registration number (AC8·AC13·AC14·AC15·AC16·AC18·AC20·AC22·AC23·AC24·AC58·AC145·AC146·AC256·AC257) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py markers crypto-robincoin`
- [x] T2 Build the page structure: the service, steps and contact sections, the AC31 sentence, the four contact links with hours, closed days, address and phone, a Hangul header nav, every link a `#` link, 로그인 and 회원가입 once each in the header, no form, field, button, script, handler or embedded frame (AC28·AC29·AC30·AC31·AC35·AC36·AC37·AC38·AC39·AC44·AC45·AC46·AC47·AC48·AC49·AC50·AC56·AC255) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py structure crypto-robincoin`
- [x] T3 Keep the copy free of the listed words (app stores, wallet and bank words, yield, leverage products, recommendations, superlatives, safety and registration claims, records, lures, real brands and assets, listing and account labels), of figures outside the example blocks, of outside e-mail addresses, handles, domains and wallet-shaped strings (AC25·AC26·AC51·AC53·AC54·AC55·AC61·AC62·AC63·AC64·AC65·AC66·AC67·AC68·AC69·AC70·AC74·AC77·AC85·AC190) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py copy crypto-robincoin`
- [x] T4 `word-break: keep-all`, one Korean `<h1>`, no skipped heading level, every `<svg>` hidden or named, no `::before` or `::after` rule with a `position` other than `absolute`, `relative` or `static` (AC33·AC34·AC129·AC130·AC149) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py a11y crypto-robincoin`
- [x] T5 Keep the sample self-contained and photo-free: relative paths only, Pretendard on jsDelivr and no Google Fonts family, no other `http(s)://` URL, no `<img>`, no `img/`, no picture file, nothing naming Coinbase or its faces (AC1·AC2·AC57·AC98·AC101·AC102·AC103·AC104·AC105·AC106·AC107·AC108·AC109·AC110·AC111·AC112·AC113·AC114·AC115·AC116·AC117·AC124·AC252·AC262) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py assets crypto-robincoin`
- [x] T6 Give A its kept traits in markup: the white `body` colours, the panel gradient ends, two example blocks with their marker and risk sentence, the phone with its marker first, one price line that rises and falls and does not end at its high, rows named 예시 자산 A onward with signed change figures both ways, no balance or gain word, no link in a block, the asset card's four rows in letter order, the section order, 고객센터 in the contact heading, none of Coinbase's blues (AC77·AC80·AC82·AC83·AC84·AC151·AC159·AC162·AC163·AC164·AC167·AC168·AC169·AC170·AC171·AC172·AC175·AC187·AC188·AC189·AC191) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py sample crypto-robincoin`
- [x] T7 Check A in a browser at 1440 and 390: sample marker, its size and its stay on screen, the AC31, AC32 and AC58 sentences visible with their sizes and contrast, a 문의 link on the first screen and at every scroll position at 390 with the footer's last line uncovered, bars within 220 px, computed `keep-all`, digit faces, web fonts loaded, Pretendard, contrast, no motion under reduced motion, no horizontal overflow; the white full-width header with the left wordmark, the grey 로그인 and 회원가입 pills and the blue 문의 pill rightmost; the rounded gradient panel at the left with the phone, its marker, its top figure and its tabular digits, red rises and blue falls; the two-line `<h1>` right of the panel in the right half, the two links under it; the dark rounded panel with the steps, the white asset card on the grey band; at 390 the header 문의 pill, the `<h1>` and the panel within 720 px; writes the screenshots for T8–T10 (AC8·AC9·AC10·AC12·AC31·AC32·AC34·AC40·AC41·AC42·AC43·AC58·AC59·AC60·AC79·AC83·AC99·AC100·AC101·AC131·AC132·AC133·AC134·AC147·AC148·AC149·AC152·AC153·AC154·AC155·AC156·AC157·AC158·AC160·AC161·AC163·AC164·AC165·AC166·AC173·AC174·AC175·AC177·AC178·AC179·AC180·AC181·AC182·AC183·AC184·AC185·AC186·AC253·AC254·AC260) — verify(browser): `python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robincoin`
- [ ] T8 Review A's content (AC21·AC27·AC52·AC53·AC55·AC56·AC69·AC70·AC71·AC72·AC73·AC75·AC76·AC81·AC86·AC87·AC176) — verify(human): apply the evidence rule to `/tmp/profile-crypto-shots/crypto-robincoin/` (command: `python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robincoin`). Read `profile/crypto-robincoin/index.html` and `style.css` (for CSS `content:` text and drawn pictures) and the `crypto-robincoin` entry of `scripts/profiles.py`, look at the bands `desktop-1440-NN.png` and `mobile-390-NN.png` in that folder, and confirm each: (1) every address names a district or road that does not exist (for example 가상구 결로), and no real 구, 동 or neighbourhood is named as the business's location (a 시 or 도 name alone is fine); (2) no person's name and no portrait or drawn face anywhere, as 대표, founder, analyst, developer, adviser or customer; (3) no QR code and no square dot pattern that reads as one, and no app-store badge; (4) no bank or payment brand, no real exchange, project, foundation, token or wallet brand, no real 가상자산 name or ticker, and no logo or coin mark of any of them (for example a circled ₿, a diamond glyph, a fox head); the sample's own name is not searched for a real namesake (spec Assumptions, Naming); (5) no platform other than 네이버 (예약 and 지도) and 카카오톡 by name, logo or icon (for example 텔레그램, 디스코드, X, 유튜브, 인스타그램, 오픈채팅); (6) no claim, in other words, in English or as a picture, of any of these nine kinds: an invitation to sign up, log in, start, open an app, connect a wallet or buy a token, other than the 로그인 and 회원가입 links AC155 gives A's header (for example Sign up, Get started, Launch App, Token Sale, Airdrop, a wallet chip such as 0x12ab…7890); a return or protected principal; a yield or leverage product; a recommendation or price forecast; a superlative or guarantee; a security record or insurance; a registration, licence or regulator; reviews, awards or records of users or volume; a free offer or event (for example 가장 안전한, 믿고 맡기는, trusted, secure, best, a shield with a tick, a rocket or an arrow that only rises); (7) no partner, investor, press, auditor or certificate logo or badge, and no row of such names; (8) no count of users, assets, trades or clients, no amount held or traded, no years in business and no fee, in words or in digits (for example 수만 명, 십 년, 수백 종, Since 2019); (9) the `title`, `summary` and `features` of this sample's entry in `scripts/profiles.py` pass items (4)–(8); (10) each example block shows at least one rise and at least one fall, and no row is styled as a recommendation (no highlight, badge, star, 추천 label or pointing arrow on one row); (11) nothing reads as an order ticket: no price or quantity field and no control whose text is 매수, 매도, 주문, 입금 or 출금; (12) no element ranks assets or shows a 급상승, 거래대금 or 인기 list, and the rows carry no rank number; (13) the phone shows no drawn search field, no input-shaped box, no keypad and no order button, and has no top bar of a menu icon, a search field and a bell
      reason: whether copy or a picture names a person or a brand, implies a count or a claim in other words, or reads as an order ticket is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/crypto-robincoin, scripts/profiles.py
      reviewed: PASS @2c72392386f1ddc4cd5b3c35fb7de1ca4c3ae127 #cf4fad7f 2026-11-21 — items 1–13 hold: only address 서울 가상구 결로 12 (가상 주소) (index.html:142,153); no person, QR, brand, ticker, logo row, count or fee; platforms only 카카오톡 · 네이버 예약 · 네이버 지도 with generic icons; 로그인 · 회원가입 once each (index.html:25–26); phone and card each show rises and falls with uniform rows in letter order; phone has no search field, keypad, order control or top bar (the marker chip at index.html:48 reads as a label); profiles.py:205–214 clean; hover and focus states read from CSS only
- [ ] T9 Review A's full-page screenshots (AC11·AC135·AC136) — verify(human): apply the evidence rule to `/tmp/profile-crypto-shots/crypto-robincoin/` (command as in T8). Look at `desktop-1440-NN.png` and `mobile-390-NN.png` band by band and at the seams between bands, and confirm: (1) at 1440, no text overlaps other text, a picture or a control so that letters are hidden; (2) at 1440, no text is cut off at a box edge (the phone running off the panel's lower edge is the design: text inside the phone above that edge is not cut); (3) and (4) the same at 390; (5) the sample marker on the first screen reads in a colour that stands out clearly from its background, at 1440 and at 390. The sticky strip and header appear once in a full-page shot; what they cover there is not counted
      reason: whether text overlaps, is clipped or stands out is a visual judgement over the rendered page.
      scope: profile/crypto-robincoin
      reviewed: PASS @2c72392386f1ddc4cd5b3c35fb7de1ca4c3ae127 #7537826c 2026-11-21 — all three 1440 bands, four 390 bands and every seam enlarged: no overlapping or clipped text; phone rows end whole above the panel's lower edge at both widths; marker white on rgb(12,18,34) at both widths (measured 18.7:1)
- [ ] T10 Compare A with Coinbase (AC102·AC117·AC118·AC120·AC123·AC192) — verify(human): apply the evidence rule to `/tmp/profile-crypto-shots/compare/` for crypto-robincoin and to `/tmp/profile-crypto-shots/crypto-robincoin/` (commands: `python3 docs/features/2026-11-20-profile-crypto/check_browser.py compare`, `python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robincoin`). Compare `crypto-robincoin-1440.png` and `-390.png` with `ref-crypto-robincoin.png`, the bands of the sample with the `ref-crypto-robincoin-full-NN.png` bands, and `ref-crypto-robincoin.txt` with the text of `profile/crypto-robincoin/index.html`, and confirm: (1) the sample shows no logo, wordmark or brand name of the reference; (2) no sentence of the reference appears in the sample; (3) no picture of the sample copies a picture of the reference: the phone screen is not a redrawing of Coinbase's phone screen, and every picture is CSS or inline SVG made for the sample; (4) side by side the two do not read as the same site: they differ in at least two of wordmark and mark, headline face and wording, the blue, what the phone shows, section order (the kept traits of item 6 do not count); (5) the sample's `<h1>` is not a translation or close paraphrase of "The future of finance is here."; (6) the sample keeps each trait listed for Candidate A under "Traits to keep" in the spec, as changed by A3, A7 and A8: a white bar header with pill buttons at the right; a rounded blue panel at the left that holds a phone screen with an example price at its top, a line chart and a short list; a large two-line headline at the right; below, a dark rounded panel (it holds the steps) and a card of asset rows (white, on a grey band); (7) a mark beside the wordmark, if there is one, is not a filled blue circle with a C-shaped opening
      reason: copied wording, pictures and marks, "reads as the same site" and "keeps the trait" are judgements a person makes.
      scope: profile/crypto-robincoin
      reviewed: PASS @2c72392386f1ddc4cd5b3c35fb7de1ca4c3ae127 #b4712fc2 2026-11-21 — reference unreachable (HTTP 403), judged against spec Candidate A and ref-g1-coinbase.jpg: no Coinbase name, mark or sentence; phone is not a redrawing (no menu, search field, bell, balance or period tabs; index.html:47–54); differs in wordmark, headline, blue and phone content; five kept traits present at 1440; h1 at index.html:34 is not a paraphrase; no mark beside the wordmark (index.html:17); the reference below its first screen seen only through the spec sketch

## Sample B — 로빈커스터디 (`profile/crypto-robincustody/`)

- [x] T11 Write `index.html` and `style.css` with the markers as in T1, with the wordmark 로빈커스터디 (AC8·AC13·AC14·AC15·AC16·AC18·AC20·AC22·AC23·AC24·AC58·AC145·AC146·AC256·AC257) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py markers crypto-robincustody`
- [x] T12 Build the page structure as in T2, with no 로그인 or 회원가입 link and no example block (AC28·AC29·AC30·AC31·AC35·AC36·AC37·AC38·AC39·AC44·AC45·AC46·AC47·AC48·AC49·AC50·AC56·AC78·AC255) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py structure crypto-robincustody`
- [x] T13 Keep the copy clean as in T3; B has no example block, so no figure anywhere (AC25·AC26·AC51·AC53·AC54·AC55·AC61·AC62·AC63·AC64·AC65·AC66·AC67·AC68·AC69·AC70·AC74·AC77) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py copy crypto-robincustody`
- [x] T14 keep-all, headings, Korean `<h1>` and SVG names and `::before`/`::after` positions as in T4 (AC33·AC34·AC129·AC130·AC149) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py a11y crypto-robincustody`
- [x] T15 Keep the sample self-contained and photo-free as in T5, with exactly `Noto Sans KR` and `Noto Serif KR` from Google Fonts and nothing naming Copper or its faces (AC1·AC2·AC57·AC98·AC101·AC102·AC103·AC104·AC105·AC106·AC107·AC108·AC109·AC110·AC111·AC112·AC113·AC114·AC115·AC116·AC117·AC124·AC252·AC262) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py assets crypto-robincustody`
- [x] T16 Give B its kept traits in markup: the apricot `body` colours, header links with Hangul text, an `<h1>` with one or two Hangul `<em>` and text outside them, three word cards with a Hangul term and one paragraph each, no `<ellipse>` and no SVG `<text>`, only apricot and wine as saturated backgrounds, none of Copper's colours, 도입 in the contact heading (AC194·AC205·AC208·AC209·AC213·AC216·AC221·AC222·AC223) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py sample crypto-robincustody`
- [x] T17 Check B in a browser at 1440 and 390, the common checks as in T7 and B's: a first screen with no gradient or image, filled with apricot to its lower edge; the white pill header with equal side gaps, apricot above and below it, the centred `Noto Serif KR` wordmark, the nav left of it and the wine 도입 문의 pill right of it; the light `Noto Sans KR` `<h1>` at the left in two or three lines with its heavy serif `<em>`; one dark 도입 문의 pill under it; the line drawing at the right; three word cards in a row with large serif terms; no digit above 24 px; two or more dashed rules; at 390 the header pill and its link, the `<h1>`, the drawing below it and the cards in one column; writes the screenshots for T18–T20 (AC8·AC9·AC10·AC12·AC31·AC32·AC34·AC40·AC41·AC42·AC43·AC58·AC59·AC60·AC99·AC100·AC101·AC131·AC132·AC133·AC134·AC147·AC148·AC149·AC195·AC196·AC197·AC198·AC199·AC200·AC201·AC202·AC203·AC204·AC206·AC207·AC208·AC210·AC211·AC212·AC213·AC214·AC215·AC216·AC217·AC218·AC219·AC220·AC253·AC254·AC260·AC261) — verify(browser): `python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robincustody`
- [ ] T18 Review B's content (AC21·AC27·AC52·AC53·AC55·AC56·AC69·AC70·AC71·AC72·AC73·AC75·AC76·AC88·AC89·AC90) — verify(human): apply the evidence rule to `/tmp/profile-crypto-shots/crypto-robincustody/` (command: `python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robincustody`), read `profile/crypto-robincustody/index.html`, `style.css` and the `crypto-robincustody` entry of `scripts/profiles.py`, look at the bands, and confirm items (1)–(9) of T8 for this sample; (10) the page states no cold-storage ratio, no amount under custody, no insurance cover and no client count, in digits or in words (for example 대부분을 오프라인에, 수천억 원 규모, 보험으로 보상); (11) every sentence about how assets are kept describes a method in general words (분리 보관, 다중 승인, 오프라인 보관) and makes no promise of safety (for example 안전하게 지킵니다, 잃을 일이 없습니다, 해킹에서 자유롭습니다); (12) the page names no client, fund, exchange or institution as a customer
      reason: whether copy names a person or a brand, implies a count, a promise of safety or a claim in other words is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/crypto-robincustody, scripts/profiles.py
      reviewed: PASS @947fbd709876d4b835f66cba8b1472058c086ce1 #a576281b 2026-11-21 — items 1–12 hold: only address 서울 가상구 금고길 7 (가상 주소) (index.html:100,111); no person, QR, brand, platform beyond 카카오톡 · 네이버, logo row, count or fee; custody sentences (index.html:31–32,55–56,67–69,81) describe methods with no ratio, amount, insurance or safety promise; no named client; profiles.py:219–221 clean
- [ ] T19 Review B's full-page screenshots (AC11·AC135·AC136) — verify(human): apply the evidence rule to `/tmp/profile-crypto-shots/crypto-robincustody/` (command as in T18), and confirm items (1)–(5) of T9 on its `desktop-1440-NN.png` and `mobile-390-NN.png`
      reason: whether text overlaps, is clipped or stands out is a visual judgement over the rendered page.
      scope: profile/crypto-robincustody
      reviewed: PASS @947fbd709876d4b835f66cba8b1472058c086ce1 #684b1841 2026-11-21 — all 1440 and 390 bands and seams enlarged: no overlapping or clipped text; h1 clear of the drawing; marker #fffdf9 on #2a1d14 at both widths (index.html:16, style.css:24–29)
- [ ] T20 Compare B with Copper (AC102·AC117·AC118·AC120·AC123) — verify(human): as in T10 for crypto-robincustody (`crypto-robincustody-1440.png`, `-390.png`, `ref-crypto-robincustody*`), confirming items (1) and (2) of T10 against Copper; (3) no picture of the sample copies a picture of the reference: the drawing is not Copper's sphere of ellipses, and every picture is CSS or inline SVG made for the sample; (4) side by side the two do not read as the same site: they differ in at least two of page colour, wordmark script, face and position, headline script and faces, the drawing, what the three cards hold, section order (the kept traits of item 6 do not count); (5) the sample's `<h1>` is not a translation or close paraphrase of "Collateral Mobility for Markets That Never Close"; (6) the sample keeps each trait listed for Candidate B under "Traits to keep" in the spec, as changed by A3: one flat warm colour over the whole first screen; a white pill-shaped header that floats on it; a headline that sets some words in a second, heavier face; a line drawing at the right; below, a row of three cards with one large word each; sections split by dashed rules
      reason: copied wording, pictures and marks, "reads as the same site" and "keeps the trait" are judgements a person makes.
      scope: profile/crypto-robincustody
      reviewed: PASS @947fbd709876d4b835f66cba8b1472058c086ce1 #aaf8a894 2026-11-21 — reference ok: no Copper name, mark or sentence (ref text all English); drawing is six nested rounded squares with no ellipse (index.html:36–46), not the sphere; differs in page colour, wordmark, headline script, drawing, card content and section order; six kept traits present (style.css:11,30–35,52–57,72,115; index.html:67–69); h1 at index.html:31 is not a paraphrase

## Sample D — 로빈체인 (`profile/crypto-robinchain/`)

- [x] T21 Write `index.html` and `style.css` with the markers as in T1, with the wordmark 로빈체인 (AC8·AC13·AC14·AC15·AC16·AC18·AC20·AC22·AC23·AC24·AC58·AC145·AC146·AC256·AC257) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py markers crypto-robinchain`
- [x] T22 Build the page structure as in T2, with no 로그인 or 회원가입 link and no example block (AC28·AC29·AC30·AC31·AC35·AC36·AC37·AC38·AC39·AC44·AC45·AC46·AC47·AC48·AC49·AC50·AC56·AC78·AC255) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py structure crypto-robinchain`
- [x] T23 Keep the copy clean as in T3, with no figure anywhere and none of the token-sale, app-entry and foundation words (AC25·AC26·AC51·AC53·AC54·AC55·AC61·AC62·AC63·AC64·AC65·AC66·AC67·AC68·AC69·AC70·AC74·AC77·AC95·AC97·AC251) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py copy crypto-robinchain`
- [x] T24 keep-all, headings, Korean `<h1>` and SVG names and `::before`/`::after` positions as in T4 (AC33·AC34·AC129·AC130·AC149) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py a11y crypto-robinchain`
- [x] T25 Keep the sample self-contained and photo-free as in T5, with exactly `Gasoek One` from Google Fonts and nothing naming Kaia or its faces (AC1·AC2·AC57·AC98·AC101·AC102·AC103·AC104·AC105·AC106·AC107·AC108·AC109·AC110·AC111·AC112·AC113·AC114·AC115·AC116·AC117·AC124·AC252·AC262) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py assets crypto-robinchain`
- [x] T26 Give D its kept traits in markup: the black `body` colours, an `<h1>` of exactly three `<span>` lines, no SVG `<text>`, the band's `<ol>` of three `<li>`, the section order with the band after the services, every saturated colour in the lime hue band, no Kaia lime (AC225·AC231·AC241·AC246·AC248·AC249·AC250) — verify: `python3 docs/features/2026-11-20-profile-crypto/check_static.py sample crypto-robinchain`
- [x] T27 Check D in a browser at 1440 and 390, the common checks as in T7 without the first-screen AC32 sentence, and D's: the inset glass bar header (blur, dark translucent background, pill radius, equal side gaps), fixed or sticky and unchanged at scroll 1200; the lime `Gasoek One` wordmark at its left end; the three-line `Gasoek One` `<h1>` at the left, one line per `<span>`, the middle one lime, at weight 400; the lime and dark pills side by side under it; the lit object at the right; four or more dark service cards of unequal width; the rounded lime band with dark text and three staggered cards; at 390 the header gaps, the three one-line `<h1>` lines at 30 px or more, the object, and the cards and band cards in one column; writes the screenshots for T28–T30 (AC8·AC9·AC10·AC12·AC31·AC34·AC40·AC41·AC42·AC43·AC58·AC59·AC60·AC99·AC100·AC101·AC131·AC132·AC133·AC134·AC147·AC149·AC226·AC227·AC228·AC229·AC230·AC231·AC232·AC233·AC234·AC235·AC236·AC237·AC238·AC239·AC240·AC242·AC243·AC244·AC245·AC246·AC247·AC253·AC254·AC260) — verify(browser): `python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robinchain`
- [ ] T28 Review D's content (AC21·AC27·AC52·AC53·AC55·AC56·AC69·AC70·AC71·AC72·AC73·AC75·AC76·AC96) — verify(human): apply the evidence rule to `/tmp/profile-crypto-shots/crypto-robinchain/` (command: `python3 docs/features/2026-11-20-profile-crypto/check_browser.py page crypto-robinchain`), read `profile/crypto-robinchain/index.html`, `style.css` and the `crypto-robinchain` entry of `scripts/profiles.py`, look at the bands, and confirm items (1)–(9) of T8 for this sample; (10) each service named in the service section is work done for other businesses (for example 스마트 컨트랙트 개발, 지갑 연동 개발, 노드 운영 대행, 보안 점검 지원), and none is trading, keeping, transferring or exchanging 가상자산 for users
      reason: whether copy names a person or a brand, implies a count or a claim in other words, or describes a service for users is a judgement about meaning; the static checks only catch listed words and digit forms.
      scope: profile/crypto-robinchain, scripts/profiles.py
      reviewed: PASS @947fbd709876d4b835f66cba8b1472058c086ce1 #3b0c78a5 2026-11-21 — items 1–10 hold: only address 서울 가상구 사슬로 3 (가상 주소) (index.html:111,122); no person, QR, brand, ticker, platform beyond 카카오톡 · 네이버, entry link, logo row, count or fee; four services (index.html:63,68,73,78) are work for other businesses; profiles.py:227–236 clean
- [ ] T29 Review D's full-page screenshots (AC11·AC135·AC136) — verify(human): apply the evidence rule to `/tmp/profile-crypto-shots/crypto-robinchain/` (command as in T28), and confirm items (1)–(5) of T9 on its `desktop-1440-NN.png` and `mobile-390-NN.png`
      reason: whether text overlaps, is clipped or stands out is a visual judgement over the rendered page.
      scope: profile/crypto-robinchain
      reviewed: PASS @947fbd709876d4b835f66cba8b1472058c086ce1 #256cd797 2026-11-21 — all 1440 and 390 bands and seams enlarged: no overlapping or clipped text; ring object clear of the headline; marker #f2f5ee on #161a1c at both widths (index.html:16, style.css:25–30)
- [ ] T30 Compare D with Kaia (AC102·AC117·AC118·AC120·AC123·AC241) — verify(human): as in T10 for crypto-robinchain (`crypto-robinchain-1440.png`, `-390.png`, `ref-crypto-robinchain*`), confirming items (1) and (2) of T10 against Kaia; (3) no picture of the sample copies a picture of the reference: the object is not Kaia's glass slab, and every picture is CSS or inline SVG made for the sample; (4) side by side the two do not read as the same site: they differ in at least two of wordmark script and face, headline script and face, the lime's value, the object, what stands under the buttons, section order (the kept traits of item 6 do not count); (5) the sample's `<h1>` is not a translation or close paraphrase of "Where Stablecoins Become Capital"; (6) the sample keeps each trait listed for Candidate D under "Traits to keep" in the spec, as changed by A3: a black page with a single lime colour; a three-line headline in a wide heavy face with the middle line in lime; two pill buttons under it; one lit object at the right; a rounded glass nav bar, present from the start; a full-width lime band with three staggered cards; dark bento cards; (7) the object shows no letter and no symbol, and it is not one rounded-rectangle slab
      reason: copied wording, pictures and marks, "reads as the same site" and "keeps the trait" are judgements a person makes.
      scope: profile/crypto-robinchain
      reviewed: PASS @947fbd709876d4b835f66cba8b1472058c086ce1 #21cf884d 2026-11-21 — reference ok: no Kaia name, mark or sentence; object is three stacked rings with two lines and three dots (index.html:39–51), no text, not a slab; differs in wordmark, headline, lime value, object, what stands under the buttons and section order; seven kept traits present (style.css:31–37,55–57,67–68,84–93); h1 at index.html:31 is not a paraphrase; reference bands 05–06 were blank, so later reference pictures were not seen

## Registration (`scripts/profiles.py`, `thumb.jpg`, `profile/index.html`)

Each sample is registered after its visual work. `python3 scripts/build.py` regenerates `profile/index.html`; never
edit that file by hand. After any later change to a sample's first screen, a fix from a review included, run
`python3 scripts/profile_thumb.py <slug>` again before its thumb task is checked.

- [x] T31 Register A: add its `PROFILES` entry (spec AC150, title from A15; the check needs that title and reads `title`, `summary` and `features` with the word lists of AC53–AC55, AC61–AC70 and the sample's own, and the digit rules of AC74), run `python3 scripts/profile_thumb.py crypto-robincoin`, run `python3 scripts/build.py` (AC1·AC3·AC4·AC5·AC6·AC17·AC76·AC121·AC122·AC150) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-20-profile-crypto/check_static.py register crypto-robincoin`
- [x] T32 Check that A's `thumb.jpg` shows its current first screen (AC5) — verify(browser): `python3 docs/features/2026-11-20-profile-crypto/check_browser.py thumb crypto-robincoin`
- [x] T33 Register B as in T31 (spec AC193), with `python3 scripts/profile_thumb.py crypto-robincustody` (AC1·AC3·AC4·AC5·AC6·AC17·AC76·AC121·AC122·AC193) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-20-profile-crypto/check_static.py register crypto-robincustody`
- [x] T34 Check that B's `thumb.jpg` shows its current first screen (AC5) — verify(browser): `python3 docs/features/2026-11-20-profile-crypto/check_browser.py thumb crypto-robincustody`
- [x] T35 Register D as in T31 (spec AC224), with `python3 scripts/profile_thumb.py crypto-robinchain` (AC1·AC3·AC4·AC5·AC6·AC17·AC76·AC121·AC122·AC224) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-20-profile-crypto/check_static.py register crypto-robinchain`
- [x] T36 Check that D's `thumb.jpg` shows its current first screen (AC5) — verify(browser): `python3 docs/features/2026-11-20-profile-crypto/check_browser.py thumb crypto-robinchain`

## Gallery, the three together and the branch

- [x] T37 Regenerate the gallery with all three entries: 코인 · 가상자산 chip count 3, a card per sample, no crypto 준비 중 tile, no other crypto entry, three different names, at most one dark page (AC3·AC6·AC19·AC128·AC137·AC138·AC139) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-20-profile-crypto/check_static.py gallery && python3 docs/features/2026-11-20-profile-crypto/check_static.py three`
- [x] T38 Check the gallery: the 코인 · 가상자산 filter shows the three cards and no 준비 중 tile; each card, from a fresh load, opens the preview with that sample, its desktop/mobile buttons switch the width, Esc closes it (AC137·AC138·AC140·AC141·AC142) — verify(browser): `python3 docs/features/2026-11-20-profile-crypto/check_browser.py gallery`
- [x] T39 Check that the three samples' `<h1>` faces and header wordmark faces differ pairwise, that the wordmark text centres are 60 px or more apart and the wordmark sizes 3 px or more apart at 1440, and the sizes 2 px or more apart at 390 (AC125·AC126·AC258·AC259·AC263) — verify(browser): `python3 docs/features/2026-11-20-profile-crypto/check_browser.py trio`
- [ ] T40 Review the three samples side by side (AC5·AC127·AC230·AC264) — verify(human): apply the evidence rule to `/tmp/profile-crypto-shots/compare/` for the three crypto samples (command: `python3 docs/features/2026-11-20-profile-crypto/check_browser.py compare`). Set `crypto-robincoin-1440.png`, `crypto-robincustody-1440.png` and `crypto-robinchain-1440.png` side by side, and the same at `-390.png`, and confirm for each of the three pairs: (1) at 1440 the wordmarks differ in position and in size; at 390, where all three sit at the left (spec A11), they differ in size, face and colour; (2) the palettes differ; (3) the typefaces of wordmark and headline differ; (4) the first-screen compositions differ (a blue panel with a phone left of a headline; a headline left of a line drawing on one flat colour under a floating pill; three heavy lines left of a lit object on black); (5) no two wordmarks read as one mark with a suffix added. Then set the three `crypto-…-thumb.jpg` files of that folder side by side (they are copies of `profile/<slug>/thumb.jpg`) and confirm: (6) they show three different first screens: a white page with a blue panel at the left, a flat apricot page with a white pill header, and a black page with lime type; each thumb shows what its sample's `-1440.png` shows (the marker text, the wordmark name, the headline, the typeface of the wordmark and of the headline, the picture, the buttons and their colours), with nothing present in one and missing in the other; (7) in `crypto-robinchain-1440.png` and `crypto-robinchain-390.png`, looked at without enlarging (they are taken at deviceScaleFactor 1), the header wordmark reads as 로빈체인, syllable by syllable
      reason: whether two designs or two marks read as one, and whether a heavy face reads at its size, is a visual judgement.
      scope: profile/crypto-robincoin, profile/crypto-robincustody, profile/crypto-robinchain
      reviewed: PASS @2c72392386f1ddc4cd5b3c35fb7de1ca4c3ae127 #b96e011b 2026-11-21 — three pairs differ in wordmark position and size at 1440 (text x 41–117 / 650–813 / 173–300) and in size, face and colour at 390, in palette, faces and first-screen composition; no two wordmarks read as one mark; thumbs are byte-equal to profile/<slug>/thumb.jpg and match the -1440 shots quadrant by quadrant; 로빈체인 reads 로/빈/체/인 unenlarged at both widths; weakest: A–B wordmark colour at 390 (both near black, navy against brown), B–D composition at 390, and the 로 at 390 (reviewer knew the word)
- [x] T41 Keep the branch inside its scope (AC7) — verify: `base="$(git merge-base main HEAD)" && test -n "$base" && test -z "$(git diff --name-only "$base" | grep -v -e '^profile/crypto-robincoin/' -e '^profile/crypto-robincustody/' -e '^profile/crypto-robinchain/' -e '^profile/index\.html$' -e '^scripts/profiles\.py$' -e '^docs/')$(git diff --name-only "$base" -- docs/profile-playbook.md)"`
- [ ] T42 Compare the eighteen designs (AC119) — verify(human): apply the evidence rule to `/tmp/profile-crypto-shots/compare/` for the three crypto samples and to each `/tmp/profile-crypto-shots/<slug>/` (commands: `python3 docs/features/2026-11-20-profile-crypto/check_browser.py compare`, `python3 docs/features/2026-11-20-profile-crypto/check_browser.py page <slug>`). In `compare/`, set each crypto sample's `-1440.png` and `-390.png` beside those of `flower-bomgyeol`, `food-saebyeokmil`, `clinic-neuru`, `clinic-byeotteul`, `clinic-bonui`, `law-ganeum`, `law-goim`, `fitness-mideoum`, `fitness-jjuuk`, `beauty-robinhair`, `beauty-robinsalon`, `beauty-robinhairsalon`, `interior-robininterior`, `interior-robindesign`, `interior-robinhome` and the other two crypto samples; for the rest of each page use the bands in `/tmp/profile-crypto-shots/<slug>/` and the `-full-NN.png` bands of the shipped samples in `compare/`. Confirm for each crypto sample, against each of the seventeen others: (1) the first screens differ in at least two of: first-screen composition (what stands where, and where the headline sits), wordmark face and position, base and accent colour; (2) the rest of the page does not repeat the other's section layout and styling: no run of three or more consecutive bands with the same grid, card shape and heading style. Shared elements that every sample needs (sample marker, footer credits, the contact links) do not count. Pairs to look at hardest (spec A16): A with `clinic-neuru`, `interior-robinhome` and `food-saebyeokmil` (the same headline and wordmark face); B with `flower-bomgyeol`, `clinic-bonui` and `interior-robindesign`; D with `law-ganeum` and `beauty-robinhair`
      reason: "reads as the same design" is a taste judgement a person makes.
      scope: profile/crypto-robincoin, profile/crypto-robincustody, profile/crypto-robinchain
      reviewed: PASS @2c72392386f1ddc4cd5b3c35fb7de1ca4c3ae127 #94661a02 2026-11-21 — all 51 pairs seen at 1440 and 390: every pair differs in at least two of composition, wordmark face and position, base and accent colour, and no pair repeats three consecutive bands; reading used: an aspect differs when one named member differs (face or position; base or accent); nearest pair crypto-robincoin with clinic-bonui at 1440 (picture left and headline right in both, same wordmark face and position; composition counted as different on its elements, colour on the accent); shipped samples' faces judged from pixels, their bands from reduced tiles

Always last, never removed:

- [x] T43 Reconcile `docs/current_system/` with what shipped (in `profile-samples/component.md`, the Source line lists `crypto-robincoin`, `crypto-robincustody` and `crypto-robinchain`, and the Depends on row no longer says "every sample keeps them in `profile/<slug>/img/`": the crypto samples have no photo), and set `last_reconciled` in `overview.md` to the new HEAD (AC143·AC144) — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && python3 docs/features/2026-11-20-profile-crypto/check_static.py current`
