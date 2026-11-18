---
status: shipped
test: `python3 docs/features/2026-11-18-profile-clinic/check_static.py all`
preflight(browser): `python3 -c "from playwright.sync_api import sync_playwright as s; p = s().start(); b = p.chromium.launch(channel='chrome'); b.close(); p.stop()" && python3 -c "import urllib.request as u; [u.urlopen(x, timeout=10) for x in ('https://fonts.googleapis.com/css2?family=Noto+Sans+KR', 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css')]"`
commits: 7a7ed55c4e37bddc5106e7c2e3dceef9a586c5ea..6dd13abc86ae69433d9b419015629f4e1a3327a3
---

# Clinic profile samples (`clinic`) — Tasks

`[x]` means the `verify:` command ran and passed. It does not mean the code was written.
If a check has not been run, the box stays empty, whatever the code looks like.

All work is inside the existing `profile-samples` component (spec Scope, `Design: none`); there are no modules to
order. The tasks go sample by sample: A `clinic-neuru`, then B `clinic-byeotteul`, then D `clinic-bonui`, then the
gallery. Every command runs from the repository root. The checks live next to this file:
`check_static.py <check> [<slug>]` (standard library and `sips`; no browser, no network; without `<slug>` a
per-sample check runs for all three) and `check_browser.py page <slug> | gallery | compare` (Playwright driving the
installed Google Chrome; it serves the repository on a free local port itself and needs the network for web fonts,
which `preflight(browser)` checks). `compare` is not a check: it saves first-screen shots of the samples and of the
reference sites for the reviews below, and exits 0 even when a reference site does not answer.
`check_static.py` and `check_browser.py` are approved together with this file. Changing what they check is a change
to approved checks and goes back to a person for re-approval.

## Picks (spec Assumptions: palettes and faces are chosen here)

The accent is the last `palette` entry in `PROFILES` (AC53·AC54). Faces are Google Fonts or Pretendard (AC21).

| Sample | `palette` (base, ink, tint, accent) | Faces |
| --- | --- | --- |
| A `clinic-neuru` | `#ffffff`, `#1f2326`, `#e9e4dc`, `#2f6f62` (pine) | Gothic A1 for the wordmark and headings, Pretendard for body text |
| B `clinic-byeotteul` | `#f7f9fb` (the `body` background), `#1d2733`, `#e4edf4`, `#e08a2c` (sun amber) | Gowun Dodum for headings, Pretendard for the wordmark and body text |
| D `clinic-bonui` | `#fbf9f7`, `#2a2725`, `#eee5de`, `#8c5a43` (chestnut) | Pretendard for the wordmark and body text, Noto Sans KR 300 for headings |

## Fixed parameters of the checks (the page contract)

- **First screen** is 1440×900 and 390×844. "Visible" means inside the viewport, opacity (multiplied up the ancestors)
  above 0.5, and not covered at its centre by an element (or its `::before`/`::after`) painted above it with a
  background image or colour at alpha × opacity (multiplied up its ancestors) above 0.5 (`pointer-events: none` does
  not exempt a cover), judged 1.5 s after load; at each
  AC15 scroll position (every half screen down to the end) within 1.5 s. The page clock is fixed at Sunday 2026-11-15
  11:00 in the `Asia/Seoul` time zone, so the first screen must not depend on the date. The AC16 hours line is plain
  text with a time range `HH:MM–HH:MM` (also `-`, `—`, `~`, `～` or `〜`) that shows whatever the day, with 평일, 오늘,
  요일 or a weekday range such as 월–금 in the same element or its parent, for example "평일 09:30 – 18:30"; it is not a
  heading, and a special-day line in the notice bar does not count. 390 px overflow (AC41) is judged inside a `width:390px` iframe; everything else at 390 in a
  390×844 viewport.
- **Controls** (AC14·AC15·AC32–AC36): `<a href="#">` links whose accessible name (text, or `aria-label`) contains
  네이버 예약, 전화, 카카오톡 or 네이버 지도. Any link or button whose name contains one of these words counts, so an in-page
  link such as "전화 · 오시는 길" to `#visit` fails AC36; name it without the word. AC14·AC15 need one 네이버 예약 and one 전화 visible at each position.
- **Sections** (AC18–AC20·AC68·AC69·AC76·AC82): an `h2`–`h6` heading containing 진료 안내, 의료진, 진료시간 or
  오시는 길 (space optional); its section runs to the next heading of the same or a higher level. AC19 needs 점심 and a
  time range within 40 characters of it; AC20 needs 휴진, 일요일 and 공휴일 in the 진료시간 section.
- **Practitioners** (AC29·AC69) are written `<이름> <직함>` with one space, 직함 one of 대표원장 (or 대표 원장), 원장,
  부원장, optionally followed by 님 (credentials such as "치과보존과 전문의" go separately), and the same text block (a `p`,
  `li`, `dd` … ; `<br>` does not split it) contains 가상 other than in "(가상 주소)", for example "한서윤 대표원장 (가상
  인물)". AC69 needs one such name and 치과 or 치의 in the 의료진 section.
- **Item lists** (AC68·AC76) count distinct terms, spaces ignored, in the 진료 안내 section. Dental (A): 일반진료,
  스케일링, 신경치료, 보존치료, 잇몸치료, 충치치료, 발치, 임플란트, 교정, 미백, 레진, 크라운, 보철, 구강검진, 틀니,
  불소, 실란트, 소아진료, 치주. Everyday (B): 감기, 독감, 만성질환, 고혈압, 당뇨, 고지혈증, 예방접종, 건강검진, 소화기,
  장염, 알레르기, 비염, 천식, 갑상선, 골다공증, 금연, 비만, 상처, 두통, 수면, 피로.
- **Page text** (AC25·AC81) is the text of `index.html` outside `script`, `style`, `template` and `title`, plus
  image `alt`, the `<title>` text, `meta` description and `og:` content, and `aria-label` and `title` attributes,
  whitespace collapsed, matched as plain substrings.
- **Addresses** (AC12) are block text matching `<한글>로|길 <번호>`, as in the food feature: the word before 로 does not
  end in 으 and the number is not followed by a letter, digit, `%`, `~`, `:`, `.`, `-`, `,<digit>` or a counter word
  (원, 분, 시, 개, 인, 일, 명, 번, 미터, 층, m). Phone numbers are `0\d{1,2}-\d{3,4}-\d{4}` and `1[5-9]\d{2}-\d{4}` (also
  `.` or space), registration numbers `\d{3}-\d{2}-\d{5}` (also `.` or space). AC30 reads digits after 면허, 면허번호,
  의료기관 번호/기호 or 요양기관 번호/기호, with an optional 제 or No.
- **Digits** (AC22): every visible element holding a time `HH:MM`, a phone number or a price `\d[\d,]*\s?원` gets a probe
  (a `0123456789` span plus one span per character `0`–`9`, `i` and `M`, off-screen, inheriting the element's font). The
  probe's main rendered font (CDP `CSS.getPlatformFontsForNode`) must be monospaced, meaning the twelve character spans
  have widths within 0.5 % of one another, or match the Korean list: Pretendard, a `KR` family, Nanum, Gowun, Gothic A1,
  Hahmlet, Song Myung, Black Han Sans, Do Hyeon, Jua, Orbit, Sunflower, Gaegu, Dongle, Hi Melody, Gamja Flower,
  Poor Story, Stylish, Yeon Sung, Gugi, Dokdo, Single Day, Cute Font, Kirang Haerang, Bagel Fat One, Diphylleia. Every
  request to the font hosts returns 200.
- **Hero photo** (AC63·AC64·AC80) is the `<img>` with the largest visible area on the 1440 first screen (a CSS
  background photo does not count). AC63: its box runs from the left edge to the right edge of the viewport.
  **Dark overlay** (AC64·AC80): any element painted above the photo (z-order at the centre of the overlap) or any
  `::before`/`::after` whose parent overlaps the photo, covering at least 10 % of the photo's area (a pseudo-element
  measured by its own width and height), whose background colour, any gradient stop or inset `box-shadow` colour has
  every RGB channel at or below `0x80` with alpha × opacity above 0.3; also a `brightness()`
  filter below 0.8 on the photo or an ancestor, or a photo opacity below 0.7. Overlay colours must compute to `rgb()` /
  `rgba()` (no `oklch()`, `color-mix()` and the like). A's accent `#2f6f62` counts as dark under this rule; D's
  `#8c5a43` does not.
- **Headline** (AC65) is the page's `h1`; every element inside it that holds text has every RGB channel at or below
  `0x40`.
- **Wordmark** (AC66·AC77·AC78) is live text containing the name stem (느루, 보늬) inside the first `<header>`: the
  element holding the first such text node, or the `<a>` around it. AC66: left edge at or below 360 px at 1440. AC77:
  `letter-spacing` at most 0.05 × `font-size` (`normal` passes) on every element in it that holds text. AC78: the first
  `font-family` of those elements and the wordmark's rendered font match the sans list: Pretendard, any family with
  Sans, Gothic or Dodum in its name, SUIT, Inter, Spoqa, NanumSquare, system-ui, -apple-system, BlinkMacSystemFont,
  Apple SD Gothic, Malgun.
- **Notice bar** (AC74) is text in `<body>` before the first `<header>`. **Controls** for AC75 are `a`, `button` and
  `input[type=submit|button]` whose name contains 로그인, 가입, 보험, 네트워크, login, log in, sign up, sign in,
  insurance or network.
- **Body background** (AC70·AC71) is the last `background` or `background-color` in a top-level `body` rule of
  `style.css`, with `var()` resolved from `:root` or `html` rules; written as hex, `rgb()` or `white`. Rules inside
  `@media` are not read.
- **Thumbnail** (AC4): `check_browser.py page` compares `thumb.jpg` with a fresh 1440×900 first screen (both scaled to
  160×100, mean absolute RGB difference at most 15 of 255). Make the thumbnail last, after the sample's visual work;
  any later change to the first screen means running `python3 scripts/profile_thumb.py <slug>` again. The thumbnail
  is shot from `file://` with 6 s of virtual time, the check over http at 1.5 s, so the first screen must not depend on
  module scripts or `fetch`, must not auto-advance, and its entrance effects end within 1.5 s.
- **Name check** (AC11): `name-check.txt` in this folder has, for each name, the queries stem + 의원, 치과, 내과,
  가정의학과, 피부과, 클리닉 and the full name (볕뜰가정의학과의원), each run on Kakao Map and on Daum, written as
  `query: kakao-map <query>` or `query: daum <query>`, each followed by a `hits: <what came up>` line, and one
  `verdict: <full name> no match` per name. On a match, stop and report it; do not change the name yourself.
- **Screenshots** for the reviews go to `/tmp/profile-clinic-shots/<slug>/`: `desktop-1440.png` and `mobile-390.png`
  (full page, after a scroll through), the same cut into 1200 px tall bands (`desktop-1440-01.png` …), and
  `summary.txt` written last (`site tree` = `git rev-parse HEAD:profile/<slug>`, `site working tree` clean or dirty, the
  page heights, `result PASS|FAIL`). `compare` rewrites `/tmp/profile-clinic-shots/compare/`: `<slug>-1440.png` and
  `<slug>-390.png` first screens for the three clinic samples, `flower-bomgyeol` and `food-saebyeokmil`; full pages of
  the last two (`<slug>-1440-full.png`, `<slug>-390-full.png` and their `-NN` bands); `ref-<slug>.png` (1440 first
  screen), `ref-<slug>-full.png` and its `-NN` bands (1440 full page) and `ref-<slug>.txt` (visible text) of each
  sample's reference home page, keeping the last good copy when a site does not answer or answers with an HTTP error; and `summary.txt` with a `local <slug> tree <hash> clean|dirty` line per sample and a
  `reference <slug> <url> ok|cached <date>|unreachable` line per reference.
- **Gallery** (AC44–AC49): AC44·AC45 after one click on the clinic chip; AC47–AC49 for each card on a fresh load of
  `/profile/`. AC47 needs the name stem (느루, 볕뜰, 보늬) in the iframe.
- **Evidence rule** for the reviews: a sample's page folder `/tmp/profile-clinic-shots/<slug>/` is current when its
  `summary.txt` exists, its `site tree` equals `git rev-parse HEAD:profile/<slug>` and its `site working tree` is
  `clean`; the compare folder is current for a sample when `compare/summary.txt` has that sample's `local` line with
  the same tree and `clean`. A review uses a current folder as it is and runs the named command only when the folder is
  not current. If it is still not current after the run, the evidence is missing and the review is UNSURE. A `cached`
  reference is evidence; `unreachable` makes the reference review UNSURE.

## Shared

- [x] T1 Run the name checks for 느루치과, 볕뜰가정의학과의원 and 보늬피부과 on Kakao Map and Daum and record them in `docs/features/2026-11-18-profile-clinic/name-check.txt` (AC11) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py name`

## Sample A — 느루치과 (`profile/clinic-neuru/`)

- [x] T2 Pick photos for A: free Unsplash (not Unsplash+) and Pexels candidates of interiors, instruments, hands or a dentist not treating anyone, compared on a contact sheet in the scratchpad (not committed); download the picks at web size into `img/` and write `img/sources.txt` (AC24·AC57·AC58·AC59·AC60·AC61·AC62) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py photos clinic-neuru`
- [x] T3 Write `index.html` and `style.css` with the sample notice (on the first screen and in the footer), a `<title>` naming the sample, noindex, footer credits, and fictional address, phone and registration number (AC7·AC8·AC9·AC10·AC12·AC13·AC86·AC87) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py markers clinic-neuru`
- [x] T4 Build the patient flow: 진료 안내, 의료진, 진료시간 with 점심시간 and 휴진일, 오시는 길; 네이버 예약, 전화, 카카오톡 and 네이버 지도 as `href="#"` links; alt text, one `h1`, no skipped heading level, `word-break: keep-all` (AC17·AC18·AC19·AC20·AC32·AC33·AC34·AC35·AC36·AC37·AC38) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py flow clinic-neuru`
- [x] T5 Keep the copy inside the medical advertising rules: no listed word, a 가상 marker on every practitioner, no non-zero licence number (AC25·AC29·AC30) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py law clinic-neuru`
- [x] T6 Keep the sample self-contained: relative paths only, photos from `img/`, fonts only from Google Fonts and Pretendard on jsDelivr, no other `http(s)://` URL, nothing naming Studio Dental (AC1·AC2·AC21·AC23·AC50·AC55·AC56) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py assets clinic-neuru`
- [x] T7 Give A its own mood: light interior photo full width, no dark overlay, dark `h1`, wordmark at the left in Gothic A1, no Cormorant Garamond; at least four dental 진료 items and a named dentist (AC67·AC68·AC69) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py sample clinic-neuru`
- [x] T8 Register A after its visual work: add the `PROFILES` entry with the A palette, run `python3 scripts/profile_thumb.py clinic-neuru`, regenerate the gallery (AC1·AC3·AC4·AC5·AC54) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-clinic/check_static.py register clinic-neuru`
- [x] T9 Check A in a browser at 1440 and 390: thumbnail current, sample notice, hours line, 네이버 예약 and 전화 on the first screen and at every scroll position at 390, computed `keep-all`, digits in a Korean or monospaced face, no motion under reduced motion, no horizontal overflow, full-width hero photo without a dark overlay, dark `h1`, wordmark at the left; writes the screenshots for T10–T12 (AC4·AC7·AC14·AC15·AC16·AC17·AC22·AC39·AC40·AC41·AC63·AC64·AC65·AC66) — verify(browser): `python3 docs/features/2026-11-18-profile-clinic/check_browser.py page clinic-neuru`
- [ ] T10 Review A's content and photos (AC12·AC26·AC27·AC28·AC29·AC31·AC63) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/clinic-neuru/` (command: `python3 docs/features/2026-11-18-profile-clinic/check_browser.py page clinic-neuru`). Read `profile/clinic-neuru/index.html` and `profile/clinic-neuru/style.css` (for CSS `content:` text), open every image in `profile/clinic-neuru/img/` and the bands `desktop-1440-NN.png` and `mobile-390-NN.png` in that folder, and confirm each: (1) no patient review, testimonial, rating or star score; (2) no before-and-after photo or side-by-side comparison image; (3) no claim of a treatment result (cure, painlessness, guaranteed effect), no superlative or ranking (가장, 1등, 최첨단 and the like), no award, certification or endorsement claim or badge, no "○○ 전문" claim other than a 전문의 credential, no comparison with other clinics, no price-based enticement (discount, free treatment, event price, price comparison), no drug or device brand name (보톡스 and the like); (4) every person named as a doctor or practitioner, in any wording, has a visible marker containing 가상 next to the name; (5) every address on the page carries (가상 주소); (6) no photo shows an identifiable patient during treatment, and no photo of an identifiable person sits next to or is captioned as a named practitioner; (7) the hero photo shows an interior
      reason: whether copy promises a result, whether a photo is a before-and-after or shows a patient, and whether a hero photo is an interior are judgements about meaning; the static checks only catch listed words and fixed formats.
      scope: profile/clinic-neuru
      reviewed: PASS @6dd13ab #65056b4b 2026-11-18 — (1)-(7) pass; footer index.html:216 '대표자 한서윤(가상 인물)', doctors :134/:143 marked, both addresses (가상 주소), no people in photos, hero is a waiting-room interior
- [ ] T11 Review A's full-page screenshots for overlapping or clipped text (AC42·AC43) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/clinic-neuru/` (command as in T10). Look at `/tmp/profile-clinic-shots/clinic-neuru/desktop-1440-NN.png` and `mobile-390-NN.png` band by band and confirm: (1) at 1440, no text overlaps other text, an image or a control so that letters are hidden; (2) at 1440, no text is cut off at a box edge; (3) and (4) the same at 390. The fixed booking bar appears once in a full-page shot; what it covers there is not counted
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page; no command decides it reliably.
      scope: profile/clinic-neuru
      reviewed: PASS @6dd13ab #a3c217c3 2026-11-18 — desktop-1440-01..05 and mobile-390-01..06 plus band seams: no overlapping or clipped text; booking-bar cover excluded by rule
- [ ] T12 Compare A with Studio Dental (AC50·AC51) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/compare/` for clinic-neuru and to `/tmp/profile-clinic-shots/clinic-neuru/` (commands: `python3 docs/features/2026-11-18-profile-clinic/check_browser.py compare`, `check_browser.py page clinic-neuru`). Compare `clinic-neuru-1440.png` and `clinic-neuru-390.png` with `ref-clinic-neuru.png`, the bands of `/tmp/profile-clinic-shots/clinic-neuru/` with the `ref-clinic-neuru-full-NN.png` bands, and `ref-clinic-neuru.txt` with the text of `profile/clinic-neuru/index.html` (the reference is its home page), and confirm: (1) the sample shows no logo, wordmark or clinic name of the reference; (2) no sentence of the reference appears in the sample, translated or not; (3) no photo on the sample is one of the reference's photos; (4) the first screens differ in at least two of: hero composition (photo placement and size, where the headline sits), wordmark face and position, base and accent colour
      reason: copied wording or logos in another language, and "reads as the same site", are judgements a person makes.
      scope: profile/clinic-neuru
      reviewed: PASS @6dd13ab #8f68d48e 2026-11-18 — no Studio Dental name, logo, sentence or photo; first screens differ in hero composition, wordmark and colours

## Sample B — 볕뜰가정의학과의원 (`profile/clinic-byeotteul/`)

- [x] T13 Pick photos for B: free Unsplash and Pexels candidates of a bright waiting room, a consulting room, plants or a doctor not treating anyone, compared on a contact sheet in the scratchpad; download the picks into `img/` and write `img/sources.txt` (AC24·AC57·AC58·AC59·AC60·AC61·AC62) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py photos clinic-byeotteul`
- [x] T14 Write `index.html` and `style.css` as in T3 (AC7·AC8·AC9·AC10·AC12·AC13·AC86·AC87) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py markers clinic-byeotteul`
- [x] T15 Build the patient flow as in T4 (AC17·AC18·AC19·AC20·AC32·AC33·AC34·AC35·AC36·AC37·AC38) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py flow clinic-byeotteul`
- [x] T16 Keep the copy inside the medical advertising rules (AC25·AC29·AC30) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py law clinic-byeotteul`
- [x] T17 Keep the sample self-contained, nothing naming Tia (AC1·AC2·AC21·AC23·AC50·AC55·AC56) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py assets clinic-byeotteul`
- [x] T18 Give B its own mood: `body` background `#f7f9fb`, no IBM Plex Mono, no Cormorant Garamond, a 휴진 notice bar above the header, no login, sign-up or insurance control, at least four everyday 진료 items (AC70·AC71·AC72·AC73·AC74·AC75·AC76) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py sample clinic-byeotteul`
- [x] T19 Register B after its visual work: `PROFILES` entry with the B palette, `python3 scripts/profile_thumb.py clinic-byeotteul`, regenerate the gallery (AC1·AC3·AC4·AC5·AC54) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-clinic/check_static.py register clinic-byeotteul`
- [x] T20 Check B in a browser at 1440 and 390 as in T9, without the A-only hero and wordmark checks (AC4·AC7·AC14·AC15·AC16·AC17·AC22·AC39·AC40·AC41) — verify(browser): `python3 docs/features/2026-11-18-profile-clinic/check_browser.py page clinic-byeotteul`
- [ ] T21 Review B's content and photos (AC12·AC26·AC27·AC28·AC29·AC31·AC75) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/clinic-byeotteul/` (command: `python3 docs/features/2026-11-18-profile-clinic/check_browser.py page clinic-byeotteul`), read `profile/clinic-byeotteul/index.html` and `style.css`, open every image in its `img/` and the bands, and confirm items (1)–(6) of T10 for this sample, and (7) there is no login, sign-up, member, insurance-network or insurance-check control in any wording
      reason: whether copy promises a result, whether a photo is a before-and-after or shows a patient, and whether a control is a login or insurance control under another wording are judgements about meaning.
      scope: profile/clinic-byeotteul
      reviewed: PASS @6dd13ab #4bf1dc7f 2026-11-18 — (1)-(7) pass; footer index.html:209 '대표자 윤해솔(가상 인물)', doctors :140/:145 marked, addresses (가상 주소), no identifiable person, no login or insurance control
- [ ] T22 Review B's full-page screenshots for overlapping or clipped text (AC42·AC43) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/clinic-byeotteul/` (command: `python3 docs/features/2026-11-18-profile-clinic/check_browser.py page clinic-byeotteul`), and confirm items (1)–(4) of T11 on `/tmp/profile-clinic-shots/clinic-byeotteul/desktop-1440-NN.png` and `mobile-390-NN.png`
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page; no command decides it reliably.
      scope: profile/clinic-byeotteul
      reviewed: PASS @6dd13ab #21440973 2026-11-18 — desktop-1440-01..04 and mobile-390-01..06 plus band seams: no overlapping or clipped text; booking-bar cover excluded by rule
- [ ] T23 Compare B with Tia (AC50·AC51) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/compare/` for clinic-byeotteul and to `/tmp/profile-clinic-shots/clinic-byeotteul/` (commands: `python3 docs/features/2026-11-18-profile-clinic/check_browser.py compare`, `check_browser.py page clinic-byeotteul`). Compare `clinic-byeotteul-1440.png` and `clinic-byeotteul-390.png` with `ref-clinic-byeotteul.png`, the bands of `/tmp/profile-clinic-shots/clinic-byeotteul/` with the `ref-clinic-byeotteul-full-NN.png` bands, and `ref-clinic-byeotteul.txt` with the text of `profile/clinic-byeotteul/index.html`, and confirm items (1)–(4) of T12
      reason: copied wording or logos in another language, and "reads as the same site", are judgements a person makes.
      scope: profile/clinic-byeotteul
      reviewed: PASS @6dd13ab #154a0a4e 2026-11-18 — no Tia name, logo, sentence or photo; first screens differ in hero composition, wordmark and colours

## Sample D — 보늬피부과 (`profile/clinic-bonui/`)

- [x] T24 Pick photos for D: free Unsplash and Pexels candidates of a calm treatment room, skincare objects, textures, plants or a doctor not treating anyone (no faces mid-procedure, no skin close-ups that read as results), compared on a contact sheet in the scratchpad; download the picks into `img/` and write `img/sources.txt` (AC24·AC57·AC58·AC59·AC60·AC61·AC62) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py photos clinic-bonui`
- [x] T25 Write `index.html` and `style.css` as in T3 (AC7·AC8·AC9·AC10·AC12·AC13·AC86·AC87) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py markers clinic-bonui`
- [x] T26 Build the patient flow as in T4 (AC17·AC18·AC19·AC20·AC32·AC33·AC34·AC35·AC36·AC37·AC38) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py flow clinic-bonui`
- [x] T27 Keep the copy inside the medical advertising rules (AC25·AC29·AC30) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py law clinic-bonui`
- [x] T28 Keep the sample self-contained, nothing naming Ever/Body (AC1·AC2·AC21·AC23·AC50·AC55·AC56) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py assets clinic-bonui`
- [x] T29 Give D its own mood and law-safe copy: no Cormorant Garamond, none of the D words, the results-vary sentence in 진료 안내 (AC79·AC81·AC82) — verify: `python3 docs/features/2026-11-18-profile-clinic/check_static.py sample clinic-bonui`
- [x] T30 Register D after its visual work: `PROFILES` entry with the D palette, `python3 scripts/profile_thumb.py clinic-bonui`, regenerate the gallery (AC1·AC3·AC4·AC5·AC54) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-clinic/check_static.py register clinic-bonui`
- [x] T31 Check D in a browser at 1440 and 390 as in T9, with D's hero and wordmark checks: hero without a dark overlay, unspaced sans wordmark (AC4·AC7·AC14·AC15·AC16·AC17·AC22·AC39·AC40·AC41·AC77·AC78·AC80) — verify(browser): `python3 docs/features/2026-11-18-profile-clinic/check_browser.py page clinic-bonui`
- [ ] T32 Review D's content and photos (AC12·AC26·AC27·AC28·AC29·AC31·AC83) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/clinic-bonui/` (command: `python3 docs/features/2026-11-18-profile-clinic/check_browser.py page clinic-bonui`), read `profile/clinic-bonui/index.html` and `style.css`, open every image in its `img/` and the bands, and confirm items (1)–(6) of T10 for this sample, and (7) each item in the 진료 안내 section names a procedure and the skin concern it addresses (for example "여드름 · 압출과 진정 관리") and says nothing about its outcome (no "깨끗해집니다", "개선됩니다", "효과", durations of effect)
      reason: whether a sentence states an outcome is a judgement about meaning; AC81 only catches listed words.
      scope: profile/clinic-bonui
      reviewed: PASS @6dd13ab #328ad5fe 2026-11-18 — (1)-(7) pass; footer index.html:167 '대표자 서지안(가상 인물)', doctors :115/:120 marked, addresses (가상 주소), no people in photos, 진료 안내 items pair concern and procedure with no outcome
- [ ] T33 Review D's full-page screenshots for overlapping or clipped text (AC42·AC43) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/clinic-bonui/` (command: `python3 docs/features/2026-11-18-profile-clinic/check_browser.py page clinic-bonui`), and confirm items (1)–(4) of T11 on `/tmp/profile-clinic-shots/clinic-bonui/desktop-1440-NN.png` and `mobile-390-NN.png`
      reason: whether text overlaps or is clipped is a visual judgement over the whole rendered page; no command decides it reliably.
      scope: profile/clinic-bonui
      reviewed: PASS @6dd13ab #5ae559c5 2026-11-18 — desktop-1440-01..05 and mobile-390-01..06 plus band seams: no overlapping or clipped text; booking-bar cover excluded by rule
- [ ] T34 Compare D with Ever/Body (AC50·AC51) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/compare/` for clinic-bonui and to `/tmp/profile-clinic-shots/clinic-bonui/` (commands: `python3 docs/features/2026-11-18-profile-clinic/check_browser.py compare`, `check_browser.py page clinic-bonui`). Compare `clinic-bonui-1440.png` and `clinic-bonui-390.png` with `ref-clinic-bonui.png`, the bands of `/tmp/profile-clinic-shots/clinic-bonui/` with the `ref-clinic-bonui-full-NN.png` bands, and `ref-clinic-bonui.txt` with the text of `profile/clinic-bonui/index.html`, and confirm items (1)–(4) of T12
      reason: copied wording or logos in another language, and "reads as the same site", are judgements a person makes.
      scope: profile/clinic-bonui
      reviewed: PASS @6dd13ab #71f218ec 2026-11-18 — no Ever/Body name, logo, sentence or photo; first screens differ in hero composition, wordmark and colours

## Gallery and branch

- [x] T35 Regenerate the gallery with all three entries: clinic chip count 3, a card per sample, no clinic 준비 중 tile, accents distinct from each other and from flower and food (AC5·AC44·AC45·AC46·AC53) — verify: `python3 scripts/build.py && python3 docs/features/2026-11-18-profile-clinic/check_static.py gallery`
- [x] T36 Check the gallery: the clinic filter shows the three cards and no 준비 중 tile; each card, from a fresh load, opens the preview with that clinic's page, its desktop/mobile buttons switch the width, Esc closes it (AC44·AC45·AC47·AC48·AC49) — verify(browser): `python3 docs/features/2026-11-18-profile-clinic/check_browser.py gallery`
- [x] T37 Keep the branch inside its scope (AC6) — verify: `base="$(git merge-base main HEAD)" && test -n "$base" && test -z "$(git diff --name-only "$base" | grep -v -e '^profile/clinic-neuru/' -e '^profile/clinic-byeotteul/' -e '^profile/clinic-bonui/' -e '^profile/index\.html$' -e '^scripts/profiles\.py$' -e '^docs/')$(git diff --name-only "$base" -- docs/profile-playbook.md)"`
- [ ] T38 Compare the five designs (AC52) — verify(human): apply the evidence rule to `/tmp/profile-clinic-shots/compare/` for all three clinic samples and to each `/tmp/profile-clinic-shots/<slug>/` (commands: `check_browser.py compare`, `check_browser.py page <slug>`). In `compare/`, set each clinic sample's `-1440.png` and `-390.png` beside those of `flower-bomgyeol`, `food-saebyeokmil` and the other two clinic samples; for the rest of each page use the bands in `/tmp/profile-clinic-shots/<slug>/` and the `-full-NN.png` bands of flower and food in `compare/`. Confirm for each clinic sample, against each of the four others: (1) the first screens differ in at least two of: hero composition (photo placement and size, where the headline sits), wordmark face and position, base and accent colour; (2) the rest of the page does not repeat the other's section layout and styling: no run of three or more consecutive bands with the same grid, card shape and heading style. Shared elements that every sample needs (sample notice, footer credits, a mobile booking bar) do not count
      reason: "reads as the same design" is a taste judgement a person makes.
      scope: profile/clinic-neuru, profile/clinic-byeotteul, profile/clinic-bonui
      reviewed: PASS @6dd13ab #475c3137 2026-11-18 — every pair differs in 2+ first-screen traits; no 3-band run with the same grid, card shape and heading style (closest: neuru×bonui 의료진/진료시간 share grid and rule lines, heading style differs)

Always last, never removed:

- [x] T39 Reconcile `docs/current_system/` with what shipped (in `profile-samples/component.md`, the Source line lists `clinic-neuru`, `clinic-byeotteul` and `clinic-bonui`), and set `last_reconciled` in `overview.md` to the new HEAD (AC84·AC85) — verify: `cd "$(git rev-parse --show-toplevel)" && git diff --quiet "$(sed -n 's/^last_reconciled: *//p' docs/current_system/overview.md)" HEAD -- . ':(exclude)docs' && python3 docs/features/2026-11-18-profile-clinic/check_static.py current`
