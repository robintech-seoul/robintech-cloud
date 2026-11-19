---
status: shipped
commits: 59a58c0cb77e7d45fafcfd0207c05b55209b9c17..674c7bd494cea2ab421b0d904775734fd990b58c
approved_at: 59a58c0cb77e7d45fafcfd0207c05b55209b9c17
---

# Pilates franchise profile sample (`fitness`)

## Problem

The `/profile/` gallery has no sample for the `fitness` (필라테스) industry. The 필라테스 filter chip shows no
count and the grid shows a "필라테스 · 디자인 준비 중" tile. A Pilates brand owner who opens the gallery sees nothing
for their business, and sales has no fitness sample to show.

`docs/profile-playbook.md` §3 says a `fitness` sample is a franchise head-office (본사) brand site, not one studio:
a visitor must be able to find a branch, book or contact that branch, and an owner-to-be must find the 가맹 문의
path. A franchise site also carries a legal risk. Many Korean Pilates franchise sites show 가맹점 수, 예상 매출,
창업 비용 and member reviews to recruit owners; 가맹사업법 제9조 forbids false or inflated information given to a
가맹희망자, and a fictional brand has no true figures at all.

## Scope

"Each fitness sample" below means each of the two folders `profile/fitness-mideoum/` and `profile/fitness-jjuuk/`.
An AC that says "each fitness sample" holds for both.

- **In:** Sample D, `profile/fitness-mideoum/`: 미더움, a Korean Pilates franchise head office with a warm daylight photo hero and Korean serif headings; reference 리본필라테스 (AC90–AC105, AC123–AC126).
- **In:** Sample B, `profile/fitness-jjuuk/`: 쭈욱, a friendly neighbourhood Pilates franchise on cream and deep green with a retro display wordmark; reference Scout Studios (AC106–AC122, AC124).
- **In:** For each fitness sample: `index.html`, `style.css`, `thumb.jpg`, and photos in `img/` with `img/sources.txt`, built per `docs/profile-playbook.md`.
- **In:** A franchise head-office page for a fictional Pilates brand: brand and class introduction, 지점 찾기, per-branch 예약 and contact, and 가맹 문의.
- **In:** Two `live` entries with `industry: "fitness"` in `PROFILES` in `scripts/profiles.py`.
- **In:** The regenerated `profile/index.html`, made by `python3 scripts/build.py`.
- **In:** Copy that gives no fabricated franchise figures, reviews, superlatives, health claims or rights claims (AC40–AC52, AC88, AC127, AC128).
- **In:** Improvements over the references for Korean visitors: 지점 찾기 and 예약 reachable on mobile, per-branch 네이버 예약 · 카카오톡 채널 · 전화 · 네이버 지도, Korean typography (AC24–AC39), and the per-sample improvements in Assumptions.
- **In:** Distinctness of each fitness sample from the seven shipped samples, from the other fitness sample and from its own reference (AC68–AC75, AC89–AC126).
- **In:** Reconcile `docs/current_system/` (the sample list in `profile-samples/component.md`) and set `last_reconciled`.
- **Out:** Candidates A (Heartcore) and C (Club Pilates), not picked at G1, and any sample built on them.
- **Out:** Changes to `assets/`, to the gallery part of `scripts/build.py`, to `docs/profile-playbook.md`, and to the seven shipped samples under `profile/`.
- **Out:** Real booking, map, KakaoTalk, phone or franchise-lead integration. Every action links to a `#` placeholder.
- **Out:** Forms of any kind (가맹 상담 신청서, 지점 검색 입력란), chat widgets, member login, class timetables tied to a booking system, payment.
- **Out:** Inner pages (branch detail pages, 가맹 안내 detail page, 정보공개서 download). Each sample is one page.
- **Out:** Self-hosting fonts. Google Fonts and Pretendard on jsDelivr stay allowed.
- **Out:** Samples for other industries, including `beauty`, the other franchise industry.
- **Design:** none. Trigger 1 (crosses a component boundary): no; the change adds data and two samples through the existing named interfaces (`PROFILES` item, URL `profile/<slug>/`, `thumb.jpg`), unchanged. Trigger 2 (adds a component): no; each sample is one more instance of the existing `profile-samples` component. Trigger 3 (alters a named interface): no; the `PROFILES` fields, the URL, the thumbnail contract and the `profile_thumb.py` CLI stay the same, and `img/` with `img/sources.txt` are files inside the self-contained folder that no other component reads. Trigger 4 (internal module boundary): no; a sample is one folder with one page, one stylesheet and its images, and a branch list inside the page is markup, not a module. So `spec.md` + `tasks.md` are enough.

## Acceptance criteria

Folder and registration

- [ ] AC1 Each fitness sample contains `index.html`, `style.css` and `thumb.jpg`.
- [ ] AC2 In each fitness sample, `index.html` and `style.css` reference no local file outside that sample's folder (no `../`, no root-relative `/` path, no `assets/`).
- [ ] AC3 `scripts/profiles.py` has exactly one `PROFILES` entry for each of the slugs `fitness-mideoum` and `fitness-jjuuk`, each with `industry` `fitness`, `status` `live` and `demo` `True`.
- [ ] AC4 Each fitness sample's slug matches `fitness-` followed by lowercase ASCII letters only.
- [ ] AC5 Each fitness sample's `thumb.jpg` is 1200 px wide with a 16:10 ratio and shows the sample's current 1440×900 first screen.
- [ ] AC6 `python3 scripts/build.py` exits 0.
- [ ] AC7 Compared with `main`, the branch changes no file outside the fitness sample folders, `profile/index.html`, `scripts/profiles.py` and `docs/`, and does not change `docs/profile-playbook.md`.

Sample markers and metadata

- [ ] AC8 In each fitness sample, the text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" is visible without scrolling at 1440 px width (browser).
- [ ] AC9 In each fitness sample, the text of AC8 is visible without scrolling at 390 px width (browser).
- [ ] AC10 Each fitness sample's footer contains "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다".
- [ ] AC11 Each fitness sample's footer contains "Website by RobinTech".
- [ ] AC12 Each fitness sample's footer has a "Photos:" credit that names each source used in its `img/sources.txt` (Unsplash, Pexels).
- [ ] AC13 Each fitness sample's `index.html` contains `<meta name="robots" content="noindex">`.
- [ ] AC14 Each fitness sample's `<title>` contains "디자인 샘플".
- [ ] AC15 Each brand name does not match a Pilates or fitness business found by a Kakao Map place search (the name alone, and the name with 필라테스), a Google and a Daum web search for the name with 필라테스, and a KFTC 정보공개서 영업표지 search (franchise.ftc.go.kr) (agent check, recorded in `name-check.txt` in this feature folder).
- [ ] AC16 In each fitness sample, every address on the page includes "(가상 주소)".
- [ ] AC17 In each fitness sample, every phone number on the page is `02-000-0000`.
- [ ] AC18 In each fitness sample, every 사업자등록번호 on the page is `000-00-00000`.
- [ ] AC19 No fitness sample shows a 정보공개서 등록번호, 가맹사업 등록번호 or other registration number with a digit other than `0`.

Franchise structure

- [ ] AC20 Each fitness sample has a section whose heading contains "지점 찾기".
- [ ] AC21 Each fitness sample's 지점 찾기 section lists at least three branches, each named with a place name followed by "점" (for example 성수점).
- [ ] AC22 Each fitness sample has a section whose heading contains "가맹 문의" or "가맹 안내".
- [ ] AC23 In each fitness sample, the 지점 찾기 section comes before the 가맹 section of AC22 in document order.

Korean visitor flow

- [ ] AC24 Each branch entry in each fitness sample has a link whose accessible name contains "네이버 예약".
- [ ] AC25 Each branch entry in each fitness sample has a link whose accessible name contains "카카오톡".
- [ ] AC26 Each branch entry in each fitness sample has a link whose accessible name contains "전화".
- [ ] AC27 Each branch entry in each fitness sample has a link whose accessible name contains "네이버 지도".
- [ ] AC28 Each branch entry in each fitness sample shows an address with "(가상 주소)" and the phone number `02-000-0000`.
- [ ] AC29 Each fitness sample's 가맹 section has a 가맹 문의 control whose accessible name contains "가맹".
- [ ] AC30 In each fitness sample, every 네이버 예약, 카카오톡, 전화 and 네이버 지도 control in a branch entry, and every 가맹 문의 control in the 가맹 section, has `href="#"` (in-page navigation links such as the header's 지점 and 가맹 links are not such controls).
- [ ] AC31 Each fitness sample has no `<form>` element.
- [ ] AC32 Each fitness sample has no `<input>`, `<select>` or `<textarea>` element.
- [ ] AC33 In each fitness sample at 1440 px width, a link to the 지점 찾기 section (`href="#<id>"` of that section) is visible without scrolling (browser).
- [ ] AC34 In each fitness sample at 390 px width, a link to the 지점 찾기 section is visible without scrolling (browser).
- [ ] AC35 In each fitness sample at 390 px width, a link to the 지점 찾기 section stays on screen at every scroll position (sticky bar or fixed button) (browser).
- [ ] AC36 In each fitness sample at 390 px width, with the page scrolled to the end, the last text line of the footer is visible and not covered by a fixed or sticky element (browser).
- [ ] AC37 Each branch entry in each fitness sample shows its weekday opening hours as digits.
- [ ] AC38 Each branch entry in each fitness sample shows its closed days.
- [ ] AC39 Each fitness sample's Korean body text uses `word-break: keep-all`.

Franchise and advertising content, each fitness sample

"Page text" below means, in `index.html`: visible text, `<title>`, `meta` description and `og:` content, `aria-label`, `alt` and `title` attributes; in `style.css`: `content:` strings.

- [ ] AC40 Each fitness sample's 가맹 section contains the sentence "가상의 가맹 안내이며 실제 가맹점을 모집하지 않습니다."
- [ ] AC41 The page text of each fitness sample contains none of: 수익률, 순수익, 순이익, 월매출, 연매출, 매출액, 예상 매출, 예상매출, 예상 수익, 예상수익, 투자금 회수, 원금, 손익분기, 대박 (modelled on 가맹사업법 제9조: ①1호 bars inflated information to a 가맹희망자, ③ requires past or expected 수익상황 information to be given in 서면, and ④·⑤ require its 산출근거; a fictional brand has no figures, so the sample states none; the word list is sample policy).
- [ ] AC42 The page text of each fitness sample contains no digit followed, with optional spaces, by 호점, 개 지점, 개지점, 개 매장, 개점, 억, 만 or 원, the last three also after 천, 백 or 십 (3,000만 원, 5천만 원) (no 가맹점 count and no money figure; sample policy, since a fictional brand has no true figures).
- [ ] AC43 The page text of each fitness sample contains no digit followed, with optional spaces, by `%`.
- [ ] AC44 The page text of each fitness sample contains none of: 최고, 최초, 최대, 최다, 유일, 독보적, 1위, 1등, No.1, 넘버원, 업계 선두, 완벽, 보장, 보증, 무조건 (sample policy against superlative and guarantee claims; no consumer-advertising source was read for this list).
- [ ] AC45 The page text of each fitness sample contains none of: 후기, 리뷰, 별점, 평점, 만족도, ★, 성공 사례, 성공사례, 점주 인터뷰 (sample policy: no fabricated reviews or owner stories presented as genuine).
- [ ] AC46 The page text of each fitness sample contains none of: 치료, 완치, 통증 개선, 통증개선, 감량, 다이어트 효과 (sample policy: no health or weight-loss outcome claims; no medical-advertising source was read for this list).
- [ ] AC47 The page text of each fitness sample contains none of: 무료, 공짜, 할인, 이벤트, 선착순, 마감 임박 (sample policy: no lure offers on a sample).
- [ ] AC48 The page text of each fitness sample contains none of: 가맹점사업자피해보상보험, 피해보상보험, 공제조합 가입, 지급보증, 공제계약, 가맹금 예치 (가맹사업법 제15조의2⑥ bars a 피해보상 표지 for a 가맹본부 that has no such contract; a fictional brand has none).
- [ ] AC49 No fitness sample shows a count of 가맹점, 지점, 회원, 수강생, 강사 or years in business, an amount of 매출, 수익 or 창업 비용, or an opening timeline in days or months, whether in digits or in words; a class capacity such as 6인 이하 is not such a count (human; sample policy; AC42–AC43 catch only digit forms).
- [ ] AC50 No fitness sample shows a member or owner testimonial, a quote attributed to a named person, a star rating, a partner or press logo, or an award (human).
- [ ] AC51 No photo in a fitness sample is captioned or labelled with a person's name or role (원장, 강사, 점주), or placed under a heading naming 강사, 강사진, 원장 or 점주, as if that person works for the brand (human).
- [ ] AC52 No fitness sample makes, in other words or in English, a superlative, guarantee, income or health-outcome claim of the kinds listed in AC41, AC44 and AC46 (human).
- [ ] AC88 The page text of each fitness sample contains none of: 체형교정, 체형 교정, 재활, 교정, 회복, 완화, 통증, 디스크, 예방, 메디컬, 처방 (sample policy: 리본필라테스's goal cards lead with 체형교정 and 통증개선 tags; a posture-correction, recovery, pain or rehabilitation promise is a health-outcome claim of the kind AC46 bans, and 표시광고법 제5조① asks an advertiser to substantiate factual claims; plain class names such as 자세 and 코어 stay allowed).
- [ ] AC127 The page text of each fitness sample contains none of: 특허, 상표등록, 상표 등록, ®, ™, 저작권 등록, 공정거래위원회, 공정위, 등록 완료 (가맹사업법 시행령 제8조①3 names claiming 지식재산권 the 가맹본부 does not hold as 허위·과장 정보제공, and a fictional brand holds no rights or 정보공개서 registration; sample policy).
- [ ] AC128 Every e-mail address in each fitness sample's page text or `mailto:` links ends in `@example.com` (a guessed domain may reach a real mailbox).

Fonts, numbers and photos, each fitness sample

- [ ] AC53 In each fitness sample, every external stylesheet comes from `fonts.googleapis.com` or from Pretendard on `cdn.jsdelivr.net`; no other external CSS or JS is loaded.
- [ ] AC54 In each fitness sample, `index.html` and `style.css` contain no `http://` or `https://` URL whose host is not `fonts.googleapis.com`, `fonts.gstatic.com` or `cdn.jsdelivr.net`.
- [ ] AC55 In each fitness sample, the digits of opening hours and phone numbers render in a Korean typeface or a monospaced face, never in a proportional Latin face with old-style figures (browser).
- [ ] AC56 In each fitness sample, every web font request succeeds (browser).
- [ ] AC57 No photo ID recorded in a fitness sample's `img/sources.txt` appears in the `img/sources.txt` of any other sample under `profile/`.
- [ ] AC58 Every image path referenced in a fitness sample's `index.html` and `style.css` (`src`, `srcset`, CSS `url()`) resolves to an existing file inside that sample's `img/`.
- [ ] AC59 Every file in each fitness sample's `img/` other than `sources.txt` is a `.jpg` or `.webp` file.
- [ ] AC60 No image in a fitness sample's `img/` is wider than 2000 px.
- [ ] AC61 No image file in a fitness sample's `img/` is larger than 500 KB.
- [ ] AC62 The image files in each fitness sample's `img/` total at most 3 MB (`thumb.jpg` is not counted).
- [ ] AC63 Each fitness sample's `img/sources.txt` has exactly one line per image file in its `img/` (dotfiles aside), written `<file> <page URL> <download URL>`; the page URL starts with `https://unsplash.com/photos/` or `https://www.pexels.com/photo/`, or is `-`.
- [ ] AC64 Every download URL in each fitness sample's `img/sources.txt` starts with `https://images.unsplash.com/photo-` or `https://images.pexels.com/photos/`, and no line contains `plus.unsplash.com` or `premium_photo`.

Accessibility and motion, each fitness sample

- [ ] AC65 Every `<img>` in each fitness sample has a non-empty `alt`.
- [ ] AC66 Each fitness sample has exactly one `<h1>`, and no heading level is skipped.
- [ ] AC67 In each fitness sample under `prefers-reduced-motion: reduce`, at 1440 px and at 390 px, no element runs or declares an animation or transition longer than 0.01 s (browser).

Not the same site

- [ ] AC68 Each fitness sample shares no text, logo, brand name or photo with its own reference site (D `fitness-mideoum`: rebornpilates.com; B `fitness-jjuuk`: scoutstudios.com.au).
- [ ] AC69 Side by side with its own reference site, a person does not read a fitness sample as the same site (human).
- [ ] AC70 Side by side with the seven shipped samples and the other fitness sample, a person does not read a fitness sample as the same design as any of them (human).
- [ ] AC71 The HSL hue of each fitness sample's accent (the last `palette` hex of its `PROFILES` entry) is at least 25° away, measured round the colour circle, from the accent hue of every other `PROFILES` entry: `#b8325a` (342°), `#2d43b4` (230°), `#2f6f62` (168°), `#e08a2c` (31°), `#8c5a43` (19°), `#4f93ad` (197°), `#7b3f78` (303°), and the other fitness sample's.
- [ ] AC72 The HSL saturation of each fitness sample's accent is at least 0.25.
- [ ] AC73 Each fitness sample's `style.css` contains the accent hex of its `PROFILES` entry (case-insensitive).
- [ ] AC74 Each fitness sample's photos show Pilates or movement scenes (reformer, mat, studio interior, hands or body in motion), and none shows a recognisable reference-site studio, a logo or branded equipment lettering (human).
- [ ] AC75 Each fitness sample's `<h1>` text is in Korean (contains at least one Hangul syllable).
- [ ] AC89 The mean 8-bit greyscale value (ITU-R 601 luma) over all pixels of each fitness sample's `thumb.jpg` is at least 100 (both fitness samples are light; measured on 2026-11-18: `flower-bomgyeol` 48.9 and `law-ganeum` 38.8 are the dark shipped samples, the others 154.7–232.8).

Sample D, `profile/fitness-mideoum/` (미더움; reference 리본필라테스, rebornpilates.com)

- [ ] AC90 At 1440 px, the `fitness-mideoum` header shows a visible link whose text contains "지점" (browser).
- [ ] AC91 At 1440 px, the `fitness-mideoum` header shows a visible link whose text contains "가맹" (browser).
- [ ] AC92 The text of every link in the `fitness-mideoum` header navigation contains at least one Hangul syllable and no Latin letter (Korean navigation, kept from 리본필라테스).
- [ ] AC93 The accessible name of the `fitness-mideoum` header wordmark contains no Latin letter (리본필라테스's wordmark is the Latin "REBORN PILATES" beside a red ribbon mark).
- [ ] AC94 At 1440 px, the `fitness-mideoum` first screen shows, outside the `<header>`, a link whose `href` is `#<id>` of the 지점 찾기 section and whose text contains "지점" together with "상담" or "예약" (the per-branch 상담 · 예약 call to action kept from 리본필라테스's "지점별 상담 신청") (browser).
- [ ] AC95 At 1440 px, the `fitness-mideoum` first screen has a photo from its `img/` (an `<img>` or a CSS background image) whose rendered box spans the full viewport width (the photo hero kept from 리본필라테스 by the G1 pick) (browser).
- [ ] AC96 At 1440 px, the bounding box of the `fitness-mideoum` `<h1>` overlaps the rendered box of the hero photo of AC95 (headline set on the photo, as 리본필라테스 does; `clinic-neuru` sets its headline on white above its photo and `clinic-bonui` beside it) (browser).
- [ ] AC97 The `fitness-mideoum` hero photo, as rendered on the first screen, reads as warm daylight: a Pilates studio lit by daylight, with warm wood, beige or cream tones (the mood kept from 리본필라테스) (human).
- [ ] AC98 The `fitness-mideoum` hero photo neither is nor imitates a photo on rebornpilates.com: in particular it is not a laughing woman in a beige top reclining on a reformer in front of a row of windows (its home hero) (human).
- [ ] AC99 The first family in the computed `font-family` of every `<h2>` in `fitness-mideoum` is `Gowun Batang` or `Song Myung` (Korean serif section headings kept from 리본필라테스; no shipped sample names these two) (browser).
- [ ] AC100 `fitness-mideoum` loads neither `Playfair Display` nor `Montserrat` (리본필라테스's Latin faces, read from its home page on 2026-11-18).
- [ ] AC101 `fitness-mideoum` loads none of `Noto Serif KR`, `Cormorant Garamond`, `Hahmlet` (the shipped serif faces) or `Noto Sans KR` (`clinic-bonui`).
- [ ] AC102 `fitness-mideoum/style.css` contains neither `#C7000B` nor `#9A0008` (case-insensitive; 리본필라테스's carmine and wine, read on 2026-11-18).
- [ ] AC103 `fitness-mideoum` has a section whose heading contains "목적" with at least three cards (the goal cards kept from 리본필라테스's "BY YOUR GOAL").
- [ ] AC104 Each card of the AC103 section contains an `<img>` from the sample's `img/`.
- [ ] AC105 At 1440 px, no element in `fitness-mideoum` whose own text contains a digit has a computed `font-size` above 24 px (no big-figure band like 리본필라테스's "13년" and "연 6회+"; AC42 and AC49 ban the content, this bans the device) (browser).

Sample B, `profile/fitness-jjuuk/` (쭈욱; reference Scout Studios, scoutstudios.com.au)

- [ ] AC106 Every RGB channel of the `body` background colour declared in `fitness-jjuuk/style.css` (custom properties resolved) is at least `0xE0` (the cream base kept from Scout Studios).
- [ ] AC107 That `fitness-jjuuk` `body` background colour has a red channel at least `0x10` above its blue channel (a warm cream: `food-saebyeokmil`'s `#f4efe5` is `0x0F`; `fitness-mideoum` is held below it by AC123).
- [ ] AC108 The HSL hue of the `fitness-jjuuk` accent (the last `palette` hex of its `PROFILES` entry) is between 100° and 143° (the deep green kept from Scout Studios; 143° is the limit AC71 sets against pine `#2f6f62` at 168°).
- [ ] AC109 At 1440 px, the `fitness-jjuuk` first screen has an element at least as wide as the viewport whose computed background colour has an HSL hue between 100° and 160° and a lightness of at most 0.30 (a deep-green strip or band; every shipped sample's top strip is near-black or grey) (browser).
- [ ] AC110 The `color` declared for `body` in `fitness-jjuuk/style.css` (custom properties resolved) has an HSL hue between 60° and 200° or a saturation of at most 0.12 (not Scout Studios' chocolate-brown ink `#6F2D1D`).
- [ ] AC111 `fitness-jjuuk/style.css` contains none of `#6F2D1D`, `#FFF9EB`, `#DEBF9D` or `#A0B6F6` (case-insensitive; Scout Studios' brown, cream, tan and lilac, read on 2026-11-18).
- [ ] AC112 The accessible name of the `fitness-jjuuk` header wordmark contains no Latin letter (Scout Studios' wordmark is the Latin "SCOUT").
- [ ] AC113 The first family in the computed `font-family` of the `fitness-jjuuk` header wordmark is neither `Pretendard` nor `Pretendard Variable`, and no other sample under `profile/` loads it (browser).
- [ ] AC114 The `fitness-jjuuk` wordmark reads as retro display lettering (tall and condensed, or chunky and rounded), not a plain text sans, and not thin-stroke art-deco letterforms like Scout Studios' "SCOUT" (human).
- [ ] AC115 `fitness-jjuuk` loads no font whose family name contains "Mono", and no `font-family` in its `style.css` begins with `monospace` (`food-saebyeokmil`'s signature is IBM Plex Mono on cream).
- [ ] AC116 The first family in the computed `font-family` of the `<h1>` and of every `<h2>` in `fitness-jjuuk` is not a serif face (`fitness-mideoum` sets serif section headings, AC99) (browser).
- [ ] AC117 The 네이버 예약 control of each branch entry in `fitness-jjuuk` has a computed `border-radius` of at least half its rendered height (pill buttons kept from Scout Studios; `food-saebyeokmil` uses 2 px corners) (browser).
- [ ] AC118 At 1440 px, the `fitness-jjuuk` header shows a `<button>` or `<summary>` whose text contains "지점" (the "Our Studios +" menu kept from Scout Studios) (browser).
- [ ] AC119 At 1440 px, activating the AC118 control shows a panel with one link per branch entry of the 지점 찾기 section, each `href="#<id>"` of that branch entry (browser).
- [ ] AC120 Each branch link in the AC119 panel shows a photo from the sample's `img/` (browser).
- [ ] AC121 The visible text of `fitness-jjuuk` contains at least five sentences that end in "요" followed by ".", "!" or "?" (the friendly voice kept from Scout Studios, in 해요체).
- [ ] AC122 The `fitness-jjuuk` hero photo neither is nor imitates a photo on scoutstudios.com.au: in particular it is not a street corner with a wordmark painted on a white brick wall, not a hand taking balls from a shelf, and not hands rolling up a mat on a wood floor (its hero video frames, the last seen on 2026-11-19) (human).

Both samples

- [ ] AC123 The `body` background colour declared in `fitness-mideoum/style.css` (custom properties resolved) has a red channel less than `0x10` above its blue channel (white or a neutral off-white, as 리본필라테스's `#FFFFFF` and `#F7F6F4`, so D does not share B's cream).
- [ ] AC124 Neither fitness sample's `<h1>` is a translation or close paraphrase of its reference's hero headline (D: "회원의 변화를 만드는 것은 운동이 아니라, 사람입니다."; B: "pilates and yoga for everybody") (human).
- [ ] AC125 No photo in `fitness-mideoum` frames a studio through or within an arched window or arched opening (리본필라테스's goal cards and franchise page) (human).
- [ ] AC126 Each card of the `fitness-mideoum` AC103 section has a short tag label that names a group or a purpose (for example 처음 시작, 산전 · 산후, 시니어, 직장인); the outcome words themselves are banned by AC46 and AC88.

Full-page checks, each fitness sample

- [ ] AC76 At 1440 px width, no fitness sample has horizontal overflow on the full page (browser).
- [ ] AC77 At 390 px width (page inside a `width:390px` iframe), no fitness sample has horizontal overflow on the full page (browser).
- [ ] AC78 A full-page screenshot of each fitness sample at 1440 px shows no overlapping or clipped text (browser, human review).
- [ ] AC79 A full-page screenshot of each fitness sample at 390 px shows no overlapping or clipped text (browser, human review).

Gallery (served by `python3 -m http.server 8000`)

- [ ] AC80 On `/profile/`, the `fitness` filter shows one card per fitness sample (browser).
- [ ] AC81 On `/profile/`, the `fitness` filter shows no "준비 중" tile (browser).
- [ ] AC82 In the generated `profile/index.html`, the `fitness` filter chip shows the number of fitness samples as its count.
- [ ] AC83 Clicking each fitness card opens the preview with that sample loaded in the iframe (browser).
- [ ] AC84 For each fitness card, the preview's desktop and mobile buttons switch the iframe between desktop and mobile width (browser).
- [ ] AC85 For each fitness card, pressing Esc closes the preview (browser).

Reconciliation

- [ ] AC86 The Source line of `docs/current_system/profile-samples/component.md` lists each fitness sample's slug.
- [ ] AC87 `git diff` from the `last_reconciled` commit in `docs/current_system/overview.md` to `HEAD` shows no change outside `docs/`.

Every AC above is checked by a `tasks.md` verify (command, browser or human); there is no feature `verify.md`; `docs/verify.md` applies.

## Assumptions

- The industry key is `fitness` with the label 필라테스; it already exists in `INDUSTRIES`. Today the gallery shows its "디자인 준비 중" tile and the chip has no count (checked in `profile/index.html` on 2026-11-18).
- **G1 decision (human, Seokhyun Kim, 2026-11-18):** build two samples, on D 리본필라테스 and on B Scout Studios. A Heartcore and C Club Pilates are out. The candidate notes below are kept as history. This closes Q1 (references) and, with the next item, Q2 (brand name).
- **Brand names.** D `fitness-mideoum`: 미더움 (agent decision, delegated by the human at Q3), from 미덥다, to be trustworthy: a plain native word for the trust an owner-to-be and a member place in a franchise head office, with no claim of results. Romanization `mideoum` follows the Revised Romanization (미 mi, 더 deo, 움 um; no sound change). B `fitness-jjuuk`: 쭈욱 (agent decision, accepted by the human at Q3), from 쭈욱 펴다, stretching out long and slowly: an everyday, friendly word that suits B's casual neighbourhood voice and makes no claim of results. Romanization `jjuuk` follows the Revised Romanization (ㅉ jj, ㅜ u, 욱 uk). Neither name shares a syllable with 봄결, 새벽밀, 느루, 볕뜰, 본의, 가늠 or 고임, nor with 리본, nor with each other. Checks (full record in `name-check.txt`): 쭈욱 (2026-11-18) is clean on Kakao Map (쭈욱 필라테스 and 쭈욱필라테스 none; 쭈욱 alone a Jeju guesthouse only), Google and Daum (only the adverb in posts, no studio), and KFTC (0). 미더움 (2026-11-19) is clean on Kakao Map (미더움 필라테스 and 미더움필라테스 none; 미더움 alone an interior firm in Daegu and a farming company in Gangjin), Google (only the adjective, as in "못 미더움", and non-fitness companies), Daum (shopping strip only, no place or web document) and KFTC (0). The earlier proposals 숨고름 and 곧추 and the given name 필라나라 are not used.
- **Q3 decision (human, Seokhyun Kim, at G1):** the name 필라나라 is dropped, because a Pilates YouTube channel and instructor-education brand already uses it (@narapilates, linked Instagram narapilates_, run by the 원장 of 웨이크필라테스; evidence in `name-check.txt`). The human delegated the new D name to the agent, which chose 미더움 (`fitness-mideoum`, previous item). The human accepted B's name 쭈욱 (`fitness-jjuuk`). This closes Q3.
- Whether a brand shows 필라테스 beside its name (for example "미더움 필라테스", "쭈욱 필라테스") or uses the bare name is left to design; the wordmark itself has no Latin letter (AC93, AC112).
- **지점 찾기 shape (agent decision):** a static list of three to six fictional branches, optionally grouped by region with in-page anchors; no search box and no map embed (AC31, AC32, AC54). A region filter driven by buttons and JS is allowed if it needs no `<input>`.
- **가맹 문의 shape (agent decision):** 가맹 문의 links (가맹 상담 전화, 가맹 카카오톡 상담) to `#`, not a form, and no e-mail address outside `@example.com` (AC128), as in the law samples (AC31). The section may describe the 가맹 process in steps (상담 → 정보공개서 제공 → 계약) without days, months or money (AC42, AC49).
- 가맹사업법 (read on law.go.kr, 2026-11-18, 시행 2026-10-02; 제2조4호, 제9조③–⑤, 제7조③, 제11조①, 시행령 제8조 and 표시광고법 제5조① re-read on casenote.kr, same 시행 text, 2026-11-19): 제9조① bars 허위·과장 and 기만적 정보제공 to a 가맹희망자 or 가맹점사업자; 제9조③ requires past or expected 수익상황 information in 서면 and ④·⑤ its 산출근거; 제7조③ bars 가맹금 or a contract within 14 days of giving the 정보공개서 (7 days after advice from a 변호사 or 가맹거래사), and 제11조① sets the same bar from the 가맹계약서; 제15조의2⑥ bars the 피해보상보험 표지 without such a contract; 제41조① sets the penalty for 제9조① breaches. These bind what a 가맹본부 tells a 가맹희망자 (제2조4호); whether public web copy counts as such 정보제공 was not checked, so AC41, AC48 and AC127 follow the statute as sample policy, and the consumer-side bans (AC44–AC47, AC88) are sample policy too. 시행령 제8조 (read on casenote.kr, 2026-11-19) lists the 허위·과장 types (①1 보장 of 최저수익, ①3 지식재산권) and the 기만 types (②2 support offered without its conditions; T11 item 6). The FTC 고시 under 제8조①4 and ②3 was not read.
- Photos: free Unsplash or Pexels photos of reformer and mat Pilates, studio interiors and movement details. They are compared on a contact sheet in the implement stage and downloaded at web size into `img/`.
- Mood targets, against the shipped samples (from `scripts/profiles.py` and their specs). `flower-bomgyeol`: dark photo hero, centred spaced serif wordmark, sand, raspberry `#b8325a`. `food-saebyeokmil`: paper cream `#f4efe5`, IBM Plex Mono labels, dawn blue `#2d43b4`. `clinic-neuru`: white, light full-bleed interior photo, Gothic A1, pine `#2f6f62`. `clinic-byeotteul`: cool white, rounded cards, Gowun Dodum, sun orange `#e08a2c`. `clinic-bonui`: warm off-white, thin Noto Sans KR, chestnut `#8c5a43`. `law-ganeum`: dark solid graphite page, Korean serif, steel blue `#4f93ad`. `law-goim`: stone `#e4e5e6`, full-bleed stone-wall photo, vertical Korean text, aubergine `#7b3f78`.
- B's base window: AC106 and AC107 together allow a blue channel of `0xE0`–`0xEF` with red at least `0x10` above it (for example `#fbf3e2` or `#f9f0e0`); Scout's exact `#FFF9EB` is banned by AC111, and food's `#f4efe5` fails AC107.
- Accent hues are feasible. AC71's 25° rule against the seven shipped hues leaves about 56°–143° (yellow-green to green) and 255°–278° (blue-violet). B's green must sit in 100°–143° (AC108), so with B near 134° (for example `#2f5d3a`, 134°, saturation 0.33) D has about 56°–109° or 255°–278° left; The hexes are fixed in `tasks.md`. D cannot keep 리본필라테스's red: the band between raspberry 342° and chestnut 19° is closed by AC71, and AC102 bans its two reds outright.
- Distinctness rule for this spec (lesson from the law run): no AC forbids the trait the human picked. D keeps a full-bleed warm daylight photo hero with the headline on it (AC95–AC97), Korean navigation with 지점 and 가맹 (AC90–AC92), a 지점 CTA in the hero (AC94), Korean serif section headings (AC99) and goal cards (AC103, AC104, AC126). B keeps a warm cream base (AC106–AC107), deep green (AC108–AC109), a retro display wordmark (AC113–AC114), pill buttons (AC117), a header branch menu (AC118–AC120) and a friendly voice (AC121). Distance comes from photos, palette, type and copy.
- **Distinctness map (pair → ACs).** AC69 and AC70 are the human backstop for every pair.
  - D vs 리본필라테스: Hangul wordmark, not "REBORN PILATES" (AC93); none of its faces (AC100) and a named Google Korean serif instead of its system-serif fallback (AC99); none of its reds (AC102, AC71); not its hero or arched-window photos (AC98, AC125, AC68); no big-figure band (AC105, AC42, AC49); no 후기 or 체형교정 · 통증개선 tags (AC45, AC46, AC88); not a paraphrase of its headline (AC124).
  - B vs Scout Studios: Hangul wordmark, not "SCOUT" (AC112), and not its art-deco letterforms (AC114); none of its brown, cream, tan or lilac (AC111); ink not brown (AC110); not its painted-wall or shelf frames (AC122); not a translation of "pilates and yoga for everybody" (AC124); Scout has no franchise entry, B adds 가맹 (AC22, AC29, AC40).
  - D vs `clinic-neuru` (white, light full-bleed interior photo, Gothic A1, headline on white above the photo): headline set on the photo (AC96); Korean serif section headings (AC99); accent hue (AC71).
  - D vs `clinic-bonui` (warm off-white, split hero with the photo beside the headline, thin Noto Sans KR): full-bleed photo (AC95) with the headline on it (AC96); no Noto Sans KR (AC101); serif headings (AC99).
  - D vs `clinic-byeotteul` (inset rounded photo with a card over it): full-bleed photo (AC95); serif headings (AC99).
  - D vs `flower-bomgyeol` (dark photo hero, Noto Serif KR, Cormorant): light first screen (AC89); none of flower's faces (AC101); warm daylight Pilates interior, not dark blooms (AC97, AC74).
  - D vs `law-ganeum` (dark page, Hahmlet): light (AC89, AC123); no Hahmlet (AC101).
  - D vs `law-goim` (full-bleed stone-wall photo with a card over it, stone base, IBM Plex Sans KR, vertical text): Pilates interior photo, warm not neutral (AC74, AC97); serif section headings (AC99); white or neutral base, not stone (AC123 with AC89).
  - B vs `food-saebyeokmil` (paper cream `#f4efe5`, IBM Plex Mono, dawn blue, 2 px buttons): warmer cream (AC107); no mono face (AC115); green accent and a deep-green band (AC108, AC109); pill buttons (AC117); a display wordmark (AC113).
  - B vs `clinic-byeotteul` (rounded, friendly, Gowun Dodum, orange): cream base, not cool white (AC106–AC107); its wordmark face is loaded by no other sample (AC113); green accent (AC108).
  - B vs `flower-bomgyeol` and `law-ganeum`: light (AC89).
  - D vs B: neutral white vs warm cream (AC123, AC107); serif vs non-serif headings (AC99, AC116); accents at least 25° apart (AC71); B's wordmark face is not loaded by D (AC113).
- **Improvements over the references (playbook §1-4).** Both: per-branch 네이버 예약 · 카카오톡 · 전화 · 네이버 지도 with hours and closed days (AC24–AC28, AC37–AC38), a 지점 찾기 link that stays on the mobile screen (AC35), Korean typography (AC39, AC55), and 가맹 copy modelled on 가맹사업법 제9조 (AC40–AC49, AC127). D: 리본필라테스 puts 후기 in its navigation and big year and seminar figures on the page; 미더움 drops both (AC45, AC105) and its hero CTA goes straight to the branch list on the same page (AC94) instead of a separate 상담 신청. B: Scout Studios has no franchise entry and its studio menu is English; 쭈욱 adds 가맹 안내 (AC22, AC29) and a Korean branch menu that jumps to each branch's 예약 and 전화 (AC118–AC119), and drops the intro-pass price strip (AC42, AC47).
- **체형교정 (agent decision).** AC46 did not list it; AC88 now bans 체형교정, 교정, 재활 and related outcome words for both samples, because D's reference uses them as goal tags. 자세 and 코어 as class words stay allowed.
- §6-1 check: `git diff --stat 8df6219..HEAD` (the `last_reconciled` in `overview.md`) lists four files: `AGENTS.md` (§8 now says profile samples branch from `main`), `docs/current_system/overview.md` (`last_reconciled` line), and the law feature's `spec.md` and `tasks.md` (SHA re-pointing). None is system code and none changes a component, interface or the `profile-samples` sample list, so `current_system/` still describes the system. AC87 will still see `AGENTS.md` until `last_reconciled` moves at this feature's reconciliation task.
- Mobile behaviour of the reference sites was not checked; mobile points are targets, not defects found in the references.
- Before G1 only the home pages were opened. After G1 (2026-11-18): rebornpilates.com's 지점 section (`#branches`: centred serif headline, a region label, four-column photo cards with branch name and walking distance) and its 가맹안내 page (`franchise.html`: large Korean serif headline beside an arched studio photo); scoutstudios.com.au's "Our Studios +" menu (a sage panel of three rounded studio photo cards with outlined pill tags and lowercase suburb names). Fonts and colours of both were read from their home-page HTML.

### Research: sites looked at (2026-11-18, Chrome)

| Site | Result |
| --- | --- |
| weareheartcore.com (Heartcore, London; heartcore.co.uk redirects) | Candidate A |
| scoutstudios.com.au (Scout Studios, Sydney) | Candidate B |
| clubpilates.com (Club Pilates, US franchise) | Candidate C |
| rebornpilates.com (리본필라테스, Korean franchise) | Candidate D |
| studiopilates.com (Studio Pilates International, AU franchise) | Runner-up. White top bar with centred lowercase wordmark, black nav bar (FIND A STUDIO, OWN A STUDIO), reformer photo hero, condensed caps "PILATES" with outline "REIMAGINED", BUY CLASSES / FIND A STUDIO buttons, three tiles (find a studio, instructing, franchising). Most franchise-native layout seen; below the fold it is a sale banner and a generic two-column block |
| bloklondon.com (BLOK, London) | Runner-up. Dark warm photo hero, large two-tone grotesk "Build the habit. Feel the difference.", Studios dropdown. Below the fold: video band, generic split rows. Multi-discipline gym, not Pilates-led |
| jetsetpilates.com (JETSET, US franchise) | Blue duotone celebrity portrait, "CANDICE SWANEPOEL FOR JETSET", Locations and Own a JETSET in nav. Celebrity-led; nothing to carry over without a person |
| solidcore.co ([solidcore], US) | Black band, condensed caps "STRONGER FOR IT.", blue Book now, cut-out class photo. Plain, template feel |
| bodybarpilates.com (BODYBAR, US franchise) | Full-bleed class photo, centred bold sans with italic "your", teal pill CTA, curved white edge; privacy panel over the lower left |
| purebarre.com (Pure Barre, US franchise) | Serif italic "The Best Full Body Workout" over a class photo, red CTA, gift-card pop-up and cookie panel on load |
| newyorkpilates.com | Cyber-week marquee, blurred video, script headline "Cyber Week", "1,000+ verified 5-star google reviews" (the pattern AC45 forbids) |
| pilatesrepublic.com (San Diego) | Bold condensed "REFORMER REBELS ONLY." over a reformer photo, serif wordmark, chat widget, cookie bar |
| exhalepilateslondon.com | Washed-out reformer-strap photo, spaced caps "LONDONS MOST LOVED PILATES STUDIO" (superlative claim) |
| kxpilates.com.au (KX, AU franchise) | Teal page with the KX logo as a photo mask, GET STARTED. Logo-led, little else on the first screen |
| pvolve.com (Pvolve) | Black Friday promo hero over a floor-graphic video; shop-led, cookie bar |
| pilatesyul.com (필라테스율, Korean franchise) | Lavender rooftop video, thin caps nav (ABOUT, BRANCH, PROGRAM). Pretty video, little structure on the first screen |
| allbaropilates.com (올바로필라테스, Korean franchise) | 가맹문의 first in nav, 방문상담예약 pill, blurred video, a "전문가의 무료 상담" pop-up on load. Recruitment-heavy |
| mpa.kr (MPA필라테스) | Excluded: hosting "지금은 사이트에 접속할 수 없습니다" traffic-limit page |
| strongpilates.com, formapilates.com | Excluded: browser error page (URLs guessed, not verified brand domains) |
| forma-pilates.com, zen-place.com | Excluded: GoDaddy parked-domain pages (URLs guessed, not verified brand domains) |

Site names came from the colorlib.com "26 Best Pilates Studio Website Examples 2026" list (read), a Mobbin section search for "pilates studio website hero section" (ClassPass, Framer showcase of BLOK, The Performance Lab), a Google search for Korean 필라테스 프랜차이즈 가맹문의 sites, and known franchise brands.

Screenshots for G1 are kept outside the repository, in the orchestrate run's scratchpad `fitness-candidates/` folder: `A-heartcore-1-first.jpg`, `A-heartcore-2-scroll.jpg`, `A-heartcore-3-scroll.jpg`, `B-scout-1-first.jpg`, `B-scout-2-scroll.jpg`, `B-scout-3-scroll.jpg`, `C-clubpilates-1-first.jpg`, `C-clubpilates-2-scroll.jpg`, `C-clubpilates-3-scroll.jpg`, `D-reborn-1-first.jpg`, `D-reborn-2-scroll.jpg`, `D-reborn-3-scroll.jpg`, and `runnerup-studiopilates-1-first.jpg`. The first-screen files are headless Chrome at 1440 × 900; the scroll files are from the Chrome window, at 1492 × 812 (A), 1440 × 723 (B, C) and 1440 × 779 (D). Cookie banners show on the C and Studio Pilates first screens; no consent was given (on C's scroll shots the banner was hidden with CSS).

### Candidates shown at G1 (history)

**A. Heartcore — https://weareheartcore.com**
London Pilates group with several "Neighbourhoods". Full-bleed warm, low-lit class photo (reformer rings, wall sconces); spaced caps wordmark top left, three small links centred, a white "Book a class →" pill and a menu icon right; a small mono "WELCOME TO / THE HOME OF PILATES / EST. 2007" stack centred. Below: a warm paper page set entirely in a monospaced face, caps section labels ("THE METHOD", "TWO WAYS TO THE FEELING"), two big photo cards (Coreformer, Hot Pilates), then a sideways class carousel ("FIND YOUR MATCH") with "BOOK HERE →" under each. Suits a calm, premium brand with few class types.

```
+----------------------------------------------------------+
| HEARTCORE        get started  neighbourhoods   [Book ->] |
|                                                          |
|        (full-bleed warm studio photo, low light)         |
|                     WELCOME TO                           |
|               THE HOME OF PILATES      (mono caps)       |
|                     EST. 2007                            |
+----------------------------------------------------------+
| paper bg      mono paragraph, centred   [Start ->]       |
|              THE METHOD / TWO WAYS TO THE FEELING        |
|        [ photo card A ]        [ photo card B ]          |
| OUR CLASSES / FIND YOUR MATCH                   SEE ALL  |
| [img][img][img][img][img][img]  -> sideways carousel     |
+----------------------------------------------------------+
```

Franchise fit: the nav has "Neighbourhoods" (locations) but no franchise entry; 가맹 would be new design. Distance: dark photo hero is near `flower-bomgyeol`; the all-mono type is near `food-saebyeokmil`'s mono labels; paper bg near food's cream.

**B. Scout Studios — https://scoutstudios.com.au**
Sydney Pilates, yoga and barre studios in three suburbs. Dark-green promo strip, cream header with a tall condensed retro serif wordmark centred, "Our Studios +" dropdown left, "book now →" outlined right. Full-bleed street video with the wordmark painted on a white brick wall, rounded sans "pilates and yoga for everybody". Below: big brown sans paragraph with tan-highlighted keywords beside a photo; a "new to scout?" offer band with lilac pill tags and a ticket graphic; a horizontal class strip (mat pilates, yoga, barre) with outlined pill tags and a bordered "memberships → scout out the details" row. Suits a friendly neighbourhood brand with a playful voice.

```
+----------------------------------------------------------+
|                 [green promo strip]                      |
| Our Studios+  About  Classes   SCOUT    Shop  [book ->]  |
+----------------------------------------------------------+
|   (full-bleed street video, wordmark on a brick wall)    |
|              pilates and yoga for everybody              |
+----------------------------------------------------------+
| cream: BIG brown paragraph with tan keywords   [photo]   |
| [photo band]  new to scout?  (pill)(pill)  [ticket card] |
| | mat pilates | yoga | barre | parents |  <- photo strip |
| memberships ---------------------- scout out the details |
+----------------------------------------------------------+
```

Franchise fit: "Our Studios +" gives a location entry; no franchise entry seen, so 가맹 would be new design. Distance: cream base near `food-saebyeokmil`; the playful brown and lilac palette is far from all shipped samples.

**C. Club Pilates — https://www.clubpilates.com**
US reformer franchise. Pale-blue promo strip; a floating white rounded nav card (logo, OUR CLASSES, FIND A STUDIO, … , Book Now, navy "Try a Free Intro Class"). Full-bleed class photo with a left-aligned headline mixing sans and serif italic ("Pilates for *every*body"), "Find your local studio!" and an address search box with a round arrow button, then an intro-class pill. Below: a stats band (studio and member counts), "Whoever you are *there's a class* for you." with three dark photo cards (new arrival / member / returner, each with its own button), and a dark "How it works" band with three numbered glass cards and FAQ toggles. Suits a large franchise whose first job is sending visitors to the nearest branch.

```
+----------------------------------------------------------+
|                 [pale promo strip]                       |
| ( CLUB*PILATES  classes  find a studio ...  [Book][Try] )|
|                                                          |
|  Pilates for                 (full-bleed class photo)    |
|  *every*body                                             |
|  Find your local studio!                                 |
|  [ address, city, or state ...     ] (->)                |
|  ( Book a Free Intro Class -> )                          |
+----------------------------------------------------------+
|   [ 0,000 ]   |   [ 00K ]   |   [ 00 ]    <- stats band  |
|     Whoever you are *there's a class* for you.           |
|  [dark photo card] [dark photo card] [dark photo card]   |
|  ##### How it works: (1) (2) (3) glass cards #####       |
+----------------------------------------------------------+
```

Franchise fit: strongest 지점 찾기 pattern (search in the hero); TEACH PILATES in nav, franchise link not seen on the first screen. The stats band and "Free Intro Class" are what AC42, AC47 and AC49 forbid, so they would be replaced (for example by a region list and a 체험 예약 link). The hero search box would become region links, since AC32 allows no input. Distance: light full-bleed photo with a left headline is near `clinic-neuru`; the serif-italic accent word is new among the samples.

**D. 리본필라테스 (Reborn Pilates) — https://rebornpilates.com**
Korean Pilates franchise. White header: red ribbon logo and "REBORN PILATES" left, Korean nav (리본은 다릅니다, 목적별, 프로그램, 후기, 지점, 회원 케어, 가맹안내, 교육협회), outlined "체험 예약" pill right. Hero: warm daylight reformer photo fading to white on the left, small spaced "REBORN PILATES · SINCE 2013", a large Korean sans headline in two lines, a short line on instructors, a red "지점별 상담 신청" pill and a "프로그램 보기" text button. Below: a warm off-white page with Korean serif (명조) section headlines, three numbered points with big serif figures ("13년", "연 6회+"), "BY YOUR GOAL" cards with tag pills (통증개선, 체형교정, 산전 · 산후, 골프, 맨즈, 시니어) over light, arched-window studio photos. Suits a domestic brand selling to adults with specific goals.

```
+----------------------------------------------------------+
| (RB) REBORN PILATES  리본은 다릅니다 목적별 ... 가맹안내 (체험예약) |
+----------------------------------------------------------+
| REBORN PILATES · SINCE 2013   (daylight reformer photo,  |
| 회원의 변화를 만드는 것은          fading to white at left) |
| 운동이 아니라, 사람입니다.                                  |
| (지점별 상담 신청)  프로그램 보기                              |
+----------------------------------------------------------+
|        명조 headline, centred, two lines                  |
|  01 13년 ...     02 연 6회+ ...    03 운동과학이 ...       |
|               BY YOUR GOAL / 명조 question               |
|  [tag|photo]   [tag|photo]   [tag|photo]  (rounded cards) |
+----------------------------------------------------------+
```

Franchise fit: 지점 and 가맹안내 in nav and a 지점별 상담 신청 CTA in the hero, closest to the request. Its 후기 nav item, year and seminar figures and 통증개선 · 체형교정 tags are what AC45, AC46 and AC49 forbid, so those would be dropped. Distance: warm off-white near `clinic-bonui`; Korean serif headings near `law-ganeum` and flower's Noto Serif KR; a red accent near flower's raspberry (AC71 forces a different hue).

## Open questions

