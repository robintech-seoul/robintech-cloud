---
status: shipped
approved_at: 8df6219df2c162683a74928a0a8628928d591f7b
commits: 8a9a3b4182f9a77662f1265ba47c2eccbfd202ca..8df6219df2c162683a74928a0a8628928d591f7b
---

# Law firm profile samples (`law`)

## Problem

The `/profile/` gallery has no sample for the `law` (법무법인) industry. The law filter shows a
"디자인 준비 중" tile. A small or mid-sized law firm that opens the gallery sees nothing for its business,
and sales has no law-firm sample to show. A law-firm site also carries a legal risk: Korean lawyer
advertising rules (변호사법 제23조 and the 대한변호사협회 「변호사 광고에 관한 규정」) forbid superlatives,
"전문" claims by a firm, free-consultation and fee lures, outcome expectations, and 전관 · 출신 claims.
Many real Korean law-firm sites lean on case counts and win stories that a sample must not copy.

## Scope

"Each law sample" below means each of the two folders `profile/law-ganeum/` and `profile/law-goim/`.
An AC that says "each law sample" holds for both.

- **In:** Sample A, `profile/law-ganeum/`: 법무법인 가늠, a 송무 · 형사 (litigation and criminal) firm with a dark editorial look; reference Selendy Gay (AC82–AC93).
- **In:** Sample C, `profile/law-goim/`: 법무법인 고임, a 기업 자문 (corporate advisory) firm with a light stone, Korean look; reference Kim & Chang (AC94–AC106, AC108–AC117).
- **In:** For each law sample: `index.html`, `style.css`, `thumb.jpg`, and photos in `img/` with `img/sources.txt`, built per `docs/profile-playbook.md`.
- **In:** A sample notice that stays on screen at every scroll position of each law sample, so no screenshot of a law sample shows the firm name without it (AC119).
- **In:** Two `live` entries with `industry: "law"` in `PROFILES` in `scripts/profiles.py`.
- **In:** The regenerated `profile/index.html`, made by `python3 scripts/build.py`.
- **In:** Copy and page content that follow Korean lawyer advertising rules in each law sample (AC16–AC36, AC92, AC105, AC118).
- **In:** Shared improvements over the references: 상담 예약 and 전화 reachable on mobile, client information in order, Korean typography (AC37–AC48, AC77).
- **In:** Distinctness of each law sample from the five shipped samples, from the other law sample and from its own reference (AC71–AC74, AC81, AC107, AC82–AC90, AC94–AC102, AC108–AC117).
- **In:** Reconcile `docs/current_system/` (the sample list in `profile-samples/component.md`) and set `last_reconciled`.
- **Out:** Candidates B (Farrer & Co) and D (Fenwick), the runners-up, and any sample built on them.
- **Out:** Changes to `assets/`, to the gallery part of `scripts/build.py`, to `docs/profile-playbook.md`, and to the five shipped samples under `profile/`.
- **Out:** Real booking, map, KakaoTalk or phone integration. Client buttons link to `#` placeholders.
- **Out:** Online consultation forms, chat widgets, client login, case lookup, payment, AI consultation.
- **Out:** Inner pages (lawyer detail pages, 업무분야 detail pages). Each sample is one page.
- **Out:** Self-hosting fonts. Google Fonts and Pretendard on jsDelivr stay allowed.
- **Out:** Samples for other industries.
- **Design:** none. Trigger 1 (crosses a component boundary): no. The change adds data and two samples through the existing named interfaces (`PROFILES` item, URL `profile/<slug>/`, `thumb.jpg`), unchanged. Trigger 2 (adds a component): no. Each sample is one more instance of the existing `profile-samples` component. Trigger 3 (alters a named interface): no. The `PROFILES` fields, the URL, the thumbnail contract and the `profile_thumb.py` CLI stay the same; `img/` and `img/sources.txt` are files inside each self-contained folder that no other component reads. Two live profiles in one industry are already supported (three `clinic` samples shipped). Trigger 4 (internal module boundary): no. Each sample is one folder with one page, one stylesheet and its images. So `spec.md` + `tasks.md` are enough.

## Acceptance criteria

Folder and registration

- [ ] AC1 Each law sample contains `index.html`, `style.css` and `thumb.jpg`.
- [ ] AC2 In each law sample, `index.html` and `style.css` reference no local file outside that sample's folder (no `../`, no root-relative `/` path, no `assets/`).
- [ ] AC3 `scripts/profiles.py` has exactly one `PROFILES` entry for each of the slugs `law-ganeum` and `law-goim`, each with `industry` `law`, `status` `live` and `demo` `True`.
- [ ] AC4 Each law sample's `thumb.jpg` is 1200 px wide with a 16:10 ratio and shows the sample's current 1440×900 first screen.
- [ ] AC5 `python3 scripts/build.py` exits 0.
- [ ] AC6 Compared with `main`, the branch changes no file outside the two law sample folders, `profile/index.html`, `scripts/profiles.py` and `docs/`, and does not change `docs/profile-playbook.md`.

Sample markers and metadata

- [ ] AC7 In each law sample, the text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" is visible without scrolling at 1440 px and at 390 px width (browser).
- [ ] AC8 Each law sample's footer contains "Website by RobinTech".
- [ ] AC9 Each law sample's footer has a "Photos:" credit that names each source used in its `img/sources.txt` (Unsplash, Pexels).
- [ ] AC10 Each law sample's `index.html` contains `<meta name="robots" content="noindex">`.
- [ ] AC11 Each law sample's footer contains "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다".
- [ ] AC12 Each law sample's `<title>` contains "디자인 샘플".
- [ ] AC119 In each law sample, at 1440 px and at 390 px width, an element whose text contains "디자인 샘플 · 상호와 정보는 가상입니다" (the text of AC7 without 로빈테크, so AC7's full text also counts) is visible at every scroll position from the top to the end of the page, and with the page scrolled to the end, the last text line of the footer is visible, not covered by that element or any fixed bar (browser; sample policy against a review risk: 변호사법 제44조② and 제112조3호 may bar a non-lawyer from using the name 법무법인, and a screenshot taken mid-page must still say the firm is fictional).
- [ ] AC13 Each firm name (법무법인 가늠, 법무법인 고임) does not match a real firm found by a Kakao Map place search, a Daum web search and the 대한변호사협회 법인 검색 (koreanbar.or.kr) for the name (agent check, recorded in `name-check.txt` in this feature folder).
- [ ] AC14 In each law sample, every address on the page includes "(가상 주소)".
- [ ] AC15 In each law sample, every phone number on the page is `02-000-0000`, and every business registration number is `000-00-00000`.

Firm form (변호사법 제44조 · 제45조), each law sample

- [ ] AC16 Each law sample's header wordmark (its text or accessible name), `<title>` and footer each contain the firm's full name "법무법인 가늠" or "법무법인 고임" (변호사법 제44조①).
- [ ] AC17 Each law sample's 구성원 section lists at least three 변호사 (변호사법 제45조①).
- [ ] AC18 In each law sample, every lawyer named on the page, in any section, has a visible marker containing "가상" next to the name.
- [ ] AC19 Each law sample's footer names a 대표변호사, with the "가상" marker of AC18.
- [ ] AC20 Each law sample's footer contains the label "광고책임변호사" followed by the name, with the "가상" marker of AC18, of a lawyer listed in its 구성원 section (「변호사 광고에 관한 규정」 제3조②; 제2조③: the 광고책임변호사 is one of the 구성원).
- [ ] AC21 No law sample contains a 변호사 등록번호 or other registration number with digits other than `0`.

Lawyer advertising rules (변호사법 제23조, 「변호사 광고에 관한 규정」 as amended 2026-11-09), each law sample

- [ ] AC22 The text of each law sample (in `index.html`: visible text, `<title>`, `meta` description and `og:` content, `aria-label`, `alt` and `title` attributes; in `style.css`: `content:` strings) contains none of: 최고, 최초, 최상, 최대, 최다, 유일, 독보적, 1위, 1등, No.1, 넘버원, 완벽, 100%, 100 %, 100％, 보장, 보증, 무조건, 확실, 승소, 승률, 성공률, 성공사례, 성공 사례, 해결사례, 석방, 결과 예측 (규정 제9조② · 제4조12호; 「변호사 광고에 관한 규칙」 제4조④ for 승률, 성공률, 석방 and 결과 예측; 변호사법 제23조②3 · 4호. 승소, 성공사례 and 해결사례 are sample policy: 규정 제4조7호 allows a past case when the client cannot be identified).
- [ ] AC23 The text of each law sample (read as in AC22) contains none of: 전문, 전담, 특화 (규정 제9조① bars them for a 법무법인; an individual 변호사 may use them, and only "전문" with the 협회 name needs registration. The sample bans the words outright as sample policy).
- [ ] AC24 The text of each law sample (read as in AC22) contains none of: 무료, 공짜, 할인, 최저, 원가, 후불, 환불, 견적, 쿠폰, 이벤트, 저렴, 염가, 성공보수 (규정 제4조10 · 11호, 제5조④, 제10조①; 성공보수 is sample policy).
- [ ] AC25 The text of each law sample (read as in AC22) contains none of: 전관, 출신, 국제변호사 (규정 제7조 3호, 제4조6호; 변호사법 제23조②2호).
- [ ] AC26 The text of each law sample (read as in AC22) contains none of: 본사, 본점, 지점, 지사, 본부 (규정 제4조13호).
- [ ] AC27 The text of each law sample (read as in AC22) contains none of: 사무장, 실장, 국장 (sample policy: no person other than a lawyer is presented to clients; stricter than 규정 제4조14호, which bars only staff not registered with the 지방회, and 규칙 제4조⑤, which bars saying a non-lawyer handles a case or consultation).
- [ ] AC28 The text of each law sample (read as in AC22) contains none of: 후기, 리뷰, 별점, 평점, 만족도, ★, 감사 편지, 감사편지 (sample policy, stricter than 규정 제4조7호).
- [ ] AC29 No law sample shows a fee or price: no digit is followed by "원" or "만원", and no ₩ or KRW amount, anywhere in the page text (sample policy: 규정 제4조10 · 11호 bar only fees presented as a lure, such as 최저, 할인 or 무료).
- [ ] AC30 Each law sample's 상담 안내 section contains the sentence "상담 비용과 수임료는 상담 후 사건에 따라 안내드립니다."
- [ ] AC31 Each law sample contains the sentence "사건의 결과는 사실관계와 증거에 따라 달라질 수 있습니다." (변호사법 제23조②4호).
- [ ] AC32 No law sample shows a client testimonial, rating, client or adviser-company name or logo, or a story of a past case (human; sample policy, stricter than 규정 제4조7호).
- [ ] AC33 No law sample shows a count of cases, consultations, wins or years of cases, or an amount recovered or saved (human; sample policy, since a fictional firm has no true figures: 규정 제4조1호 bars only false ones; 제4조12호 and 규칙 제4조④ bar rates and predicted results).
- [ ] AC34 No law sample compares itself with other lawyers or firms, or suggests a tie to or influence over courts, prosecutors, police or other public bodies (human; 규정 제4조3 · 8호, 제7조).
- [ ] AC35 No photo on a law sample's page or in its `img/` shows a judge's robe, a prosecutor's or police uniform, or a courtroom scene with identifiable people (human; 규정 제7조4호).
- [ ] AC36 Every office named on a law sample's page is labelled 주사무소 or 분사무소 (규정 제4조13호).
- [ ] AC118 No law sample makes, in other words or in English, a superlative or similar claim (규정 제9조②: "최고", "유일" 기타 이와 유사한 용어), a low-fee or 성공보수 offer, a "<crime> 변호사" title (규칙 제7조), or shows a legal-platform name or badge (human).

Korean client flow, each law sample

- [ ] AC37 Each law sample has a 상담 예약 control with an accessible name containing "상담 예약".
- [ ] AC38 Each law sample has a 전화 link with an accessible name containing "전화".
- [ ] AC39 Each law sample has a 카카오톡 상담 link with an accessible name containing "카카오톡".
- [ ] AC40 Each law sample has a 네이버 지도 link with an accessible name containing "네이버 지도".
- [ ] AC41 In each law sample, the 상담 예약, 전화, 카카오톡 and 네이버 지도 controls have `href="#"`.
- [ ] AC42 In each law sample at 1440 px width, the 상담 예약 control and the 전화 link are visible without scrolling (browser).
- [ ] AC43 In each law sample at 390 px width, the 상담 예약 control and the 전화 link are visible without scrolling (browser).
- [ ] AC44 In each law sample at 390 px width, the 상담 예약 control and the 전화 link stay reachable on every scroll position (sticky bar or fixed buttons) (browser).
- [ ] AC45 In each law sample, the section headings come in this order: 주요 업무분야, then 구성원, then 상담 안내, then 오시는 길. Other sections may sit between them.
- [ ] AC46 Each law sample's 상담 안내 section shows the weekday 상담 시간 as digits.
- [ ] AC77 Each law sample's 상담 안내 section shows the closed days.
- [ ] AC47 Each law sample's Korean body text uses `word-break: keep-all`.
- [ ] AC48 No law sample has a portrait photo of a person next to a lawyer's name (human).

Fonts, numbers and photos, each law sample

- [ ] AC49 In each law sample, every external stylesheet comes from `fonts.googleapis.com` or from Pretendard on `cdn.jsdelivr.net`; no other external CSS or JS is loaded.
- [ ] AC50 In each law sample, the digits of 상담 시간 and phone numbers render in a Korean typeface or a monospaced face (never in a proportional Latin face with old-style figures), and every web font request succeeds (browser).
- [ ] AC51 In each law sample, `index.html` and `style.css` contain no `http://` or `https://` URL whose host is not `fonts.googleapis.com`, `fonts.gstatic.com` or `cdn.jsdelivr.net`.
- [ ] AC52 No photo ID recorded in a law sample's `img/sources.txt` appears in the `img/sources.txt` of any other sample under `profile/`.
- [ ] AC53 Every image path referenced in a law sample's `index.html` and `style.css` (`src`, `srcset`, CSS `url()`) resolves to an existing file inside that sample's folder.
- [ ] AC54 Every photo referenced in a law sample's `index.html` and `style.css` lives in that sample's `img/`.
- [ ] AC55 Every file in each law sample's `img/` other than `sources.txt` is a `.jpg` or `.webp` file.
- [ ] AC56 No image in a law sample's `img/` is wider than 2000 px.
- [ ] AC57 No image file in a law sample's `img/` is larger than 500 KB.
- [ ] AC58 The image files in each law sample's `img/` total at most 3 MB (`thumb.jpg` is not counted).
- [ ] AC59 Each law sample's `img/sources.txt` has exactly one line per image file in its `img/` (dotfiles aside), written `<file> <page URL> <download URL>`; the page URL starts with `https://unsplash.com/photos/` or `https://www.pexels.com/photo/`, or is `-`.
- [ ] AC60 Every download URL in each law sample's `img/sources.txt` starts with `https://images.unsplash.com/photo-` or `https://images.pexels.com/photos/`, and no line contains `plus.unsplash.com` or `premium_photo`.

Accessibility and motion, each law sample

- [ ] AC61 Every `<img>` in each law sample has a non-empty `alt`.
- [ ] AC62 Each law sample has exactly one `<h1>`, and no heading level is skipped.
- [ ] AC63 In each law sample under `prefers-reduced-motion: reduce`, at 1440 px and at 390 px, no element runs or declares an animation or transition longer than 0.01 s (browser).

Full-page checks, each law sample

- [ ] AC64 At 1440 px width, no law sample has horizontal overflow on the full page (browser).
- [ ] AC65 At 390 px width (page inside a `width:390px` iframe), no law sample has horizontal overflow on the full page (browser).
- [ ] AC66 A full-page screenshot of each law sample at 1440 px shows no overlapping or clipped text (browser, human review).
- [ ] AC67 A full-page screenshot of each law sample at 390 px shows no overlapping or clipped text (browser, human review).

Gallery (served by `python3 -m http.server 8000`)

- [ ] AC68 On `/profile/`, the `law` filter shows two cards, one for each law sample (browser).
- [ ] AC78 On `/profile/`, the `law` filter shows no "준비 중" tile (browser).
- [ ] AC69 In the generated `profile/index.html`, the `law` filter chip shows the count `2`.
- [ ] AC70 Clicking each law card opens the preview with that sample loaded in the iframe (browser).
- [ ] AC79 For each law card, the preview's desktop and mobile buttons switch the iframe between desktop and mobile width (browser).
- [ ] AC80 For each law card, pressing Esc closes the preview (browser).

Not the same site

- [ ] AC71 Each law sample shares no text, logo, firm name or photo with its own reference site (A: selendygay.com, C: kimchang.com).
- [ ] AC72 Side by side with its own reference site, a person does not read a law sample as the same site (human).
- [ ] AC73 Side by side with the five shipped samples and the other law sample, a person does not read a law sample as the same design as any of them (human).
- [ ] AC74 The HSL hue of each law sample's accent (the last `palette` hex of its `PROFILES` entry) is at least 25° away, measured round the colour circle, from the hue of every other `PROFILES` entry's accent: the five shipped `#b8325a` (342°), `#2d43b4` (230°), `#2f6f62` (168°), `#e08a2c` (31°), `#8c5a43` (19°), and the other law sample's.
- [ ] AC81 Each law sample's `style.css` contains the accent hex of its `PROFILES` entry (case-insensitive).
- [ ] AC107 The HSL saturation of each law sample's accent is at least 0.25 (a grey accent would pass AC74 on hue alone).

Sample A — 법무법인 가늠 (`profile/law-ganeum/`), reference Selendy Gay

- [ ] AC82 The `body` background colour declared in `law-ganeum/style.css` (custom properties resolved) has every RGB channel at or below `0x33` (the only dark page; flower is dark only in its photo hero).
- [ ] AC83 `law-ganeum` loads no `Cormorant Garamond` font.
- [ ] AC84 `law-ganeum` loads no `Noto Serif KR` font (flower's Korean serif).
- [ ] AC85 The first family in the `law-ganeum` `h1`'s `font-family` (custom properties resolved) is one of `Nanum Myeongjo`, `Gowun Batang`, `Hahmlet` or `Song Myung`.
- [ ] AC86 At 1440 px, the `law-ganeum` wordmark is not horizontally centred: its left edge is within the left quarter of the viewport (browser).
- [ ] AC87 The `law-ganeum` wordmark has a computed `letter-spacing` of at most `0.05em` (browser).
- [ ] AC88 At 1440 px, no image (`<img>`, `<video>`, `<picture>` or `<svg>`) and no element or pseudo-element with a CSS `url()` background image in the `law-ganeum` first screen is wider than 60% of the viewport (no full-bleed photo hero) (browser).
- [ ] AC89 `law-ganeum` contains no element whose text is a number set larger than the `h1` (Selendy Gay's big-figure band; AC33 bans the content, this bans the device) (browser).
- [ ] AC90 The first `<section>` of `law-ganeum` (or its `<header>` hero) contains at least three links whose `href` is `#<id>` of an element inside the 주요 업무분야 section.
- [ ] AC91 The `law-ganeum` 주요 업무분야 section names at least four 송무 · 형사 items (for example 민사소송, 형사 사건 변호, 행정소송, 가사소송, 손해배상).
- [ ] AC92 The text of `law-ganeum` (read as in AC22) contains none of: 무죄, 무혐의, 혐의없음, 불기소, 기소유예, 집행유예, 선고유예, 감형, 감경, 불구속, 선처, 기각 (규정 제4조12호; the list is sample policy).
- [ ] AC93 In `law-ganeum` at 390 px width, the phone number `02-000-0000` is visible as digits without scrolling (browser).

Sample C — 법무법인 고임 (`profile/law-goim/`), reference Kim & Chang

- [ ] AC94 Every RGB channel of the `body` background colour declared in `law-goim/style.css` (custom properties resolved) is between `0xD8` and `0xEA` (a stone tint: the clinic bases are `0xF7` or lighter; not dark like A).
- [ ] AC95 That `law-goim` `body` background colour has a blue channel greater than or equal to its red channel (not food's warm cream).
- [ ] AC96 `law-goim` loads none of the faces the shipped samples and A use as display or body faces: `Cormorant Garamond`, `Noto Serif KR`, `IBM Plex Mono`, `Gothic A1`, `Gowun Dodum`, `Noto Sans KR`, `Nanum Myeongjo`, `Gowun Batang`, `Hahmlet`, `Song Myung`.
- [ ] AC97 The first family in the `law-goim` `h1`'s computed `font-family` is not a serif face (browser).
- [ ] AC108 The first family in the `law-goim` `h1`'s `font-family` (custom properties resolved) is neither `Pretendard` nor `Pretendard Variable` (every shipped sample uses Pretendard for body text, so a Pretendard heading would look like theirs).
- [ ] AC109 The `law-goim` first screen at 1440 px shows a photo of Korean architecture or material (for example a stone or earthen wall, a 기와 or lattice detail, 한지 or ink), which is the mood C keeps from Kim & Chang (human).
- [ ] AC98 The text of the `law-goim` header wordmark contains no Latin letter (Kim & Chang and flower use Latin caps wordmarks).
- [ ] AC110 The accessible name of the `law-goim` header wordmark contains no Latin letter.
- [ ] AC99 At 1440 px, the `law-goim` first screen contains a visible Korean text element whose computed `writing-mode` is `vertical-rl` (browser).
- [ ] AC100 At 1440 px, the `law-goim` first screen has a photo from its `img/` (an `<img>` or a CSS background image) whose rendered box spans the full viewport width (a full-bleed photo hero, kept from Kim & Chang by the human's G1 decision) (browser).
- [ ] AC112 At 390 px width (page inside a `width:390px` iframe), the `law-goim` first screen has a photo from its `img/` (an `<img>` or a CSS background image) whose rendered box spans the full viewport width (browser).
- [ ] AC113 The `law-goim` hero photo neither is nor imitates a photo on kimchang.com: in particular it is not a glass curtain wall with dark louvre bands reflecting an orange sunset (Kim & Chang's facade shot), and not a view over snow-covered hanok roofs (its hanok shot); the same subject reframed or recoloured also fails (human).
- [ ] AC114 The main subject of the `law-goim` hero photo is not flowers, leaves or other plants (flower's photos are all close-ups of bouquets and blooms) (human).
- [ ] AC115 The `law-goim` hero photo, as rendered on the first screen, is not low-key: flower's hero and most of its photos are dim, side-lit close-ups against a near-black or charcoal ground, darkened further by a gradient over the hero; C's hero reads as lit by open daylight or even light, not as that dark, moody look (human).
- [ ] AC117 The colour of the `law-goim` hero photo, as rendered on the first screen, is not dominated by saturated warm hues: flower's photos are led by crimson, magenta, orange and violet blooms; C's hero reads as neutral or cool (stone, ink, grey, muted earth), clearly another colour temperature (human).
- [ ] AC116 The mean 8-bit greyscale value (ITU-R 601 luma) over all pixels of `law-goim/thumb.jpg` is at least 100 (a proxy for AC115, with a wide margin: flower's `thumb.jpg` measured 48.9 on 2026-11-18, the other shipped samples' 188–233).
- [ ] AC101 `law-goim` has no search field: no `<input type="search">` and no element with `role="search"`.
- [ ] AC111 `law-goim` has no `<form>` element.
- [ ] AC102 `law-goim` has no language switcher: no link or button whose text is EN, ENG, English, JP, CN, 日本語 or 中文.
- [ ] AC103 The `law-goim` 주요 업무분야 section names at least four 기업 자문 items (for example 회사 설립 · 지배구조, 계약 검토, 인사 · 노무, 공정거래, 개인정보 · 정보보호, 투자 · 인수합병).
- [ ] AC104 The `law-goim` 상담 안내 section has a list headed "상담 전 준비" with at least three items a business brings to a first consultation (for example 계약서, 정관, 관련 메일).
- [ ] AC105 The text of `law-goim` (read as in AC22) contains none of: 고문사, 고객사, 파트너사, 자문 실적, 절세, 리스크 제로 (규정 제4조7호 bars showing clients, 고문 included, for 고문사, 고객사, 파트너사 and 자문 실적; 절세 and 리스크 제로 are outcome promises under 변호사법 제23조②4호; the list is sample policy).
- [ ] AC106 Each lawyer card in the `law-goim` 구성원 section has a 주요취급분야 line naming at least one item of its 주요 업무분야 section.

Reconciliation

- [ ] AC75 The Source line of `docs/current_system/profile-samples/component.md` lists `law-ganeum` and `law-goim`.
- [ ] AC76 `git diff` from the `last_reconciled` commit in `docs/current_system/overview.md` to `HEAD` shows no change outside `docs/`.

Every AC above is checked by a `tasks.md` verify (command, browser or human); there is no `verify.md`.

## Assumptions

- **G1 result (2026-11-18, Seokhyun Kim):** "A, C로 만들어줘" — two samples in this feature, A on Selendy Gay and C on Kim & Chang. The human then approved both names and AC48, and decided C's hero photo question (Q2–Q4).
- **Firm name A (approved by the human at G1, Q3):** 법무법인 가늠, slug `law-ganeum`. 가늠 means "gauging, weighing up": careful judgment, with no claim of results. It shares no syllable with 봄결, 새벽밀, 느루, 볕뜰 or 보늬. Checks on 2026-11-18: the 대한변호사협회 법인 검색 (koreanbar.or.kr) for 법인명 "가늠" returned 0 results (the site notes that dissolved firms are not listed); the same search for "한올" returned 1 result (법무법인 한올, 부산), so the search works. Kakao Map place searches for 법무법인가늠, 가늠 법률 and 가늠 변호사 returned no result. A place search for 가늠 alone listed 10 places; the first three were a print shop, a company and a software firm, and the rest were not read. A Daum web search for `"법무법인 가늠"` showed an image strip and one ad, with no place card and no web document. Rejected: 한올 (법무법인 한올 exists in 부산 연제구). Naver was not searched. AC13 repeats the checks and records them.
- **Firm name C (approved by the human at G1, Q3):** 법무법인 고임, slug `law-goim`. 고임 is what is set under something to hold it level (고임돌); a firm that supports a business from underneath, with no claim of results. It shares no syllable with 봄결, 새벽밀, 느루, 볕뜰, 보늬 or 가늠. Checks on 2026-11-18: the 대한변호사협회 법인 검색 for 법인명 "고임" returned 0 results ("해산된 법무법인 … 검색되지 않습니다"); the control search for "호암" returned 1 result (법무법인 호암, 서울 영등포구), so the search works. Kakao Map place searches: 고임 법률 and 고임 법률사무소 returned no result; 법무법인고임 returned none and was auto-corrected to the existing 법무법인 호암; 고임 변호사 returned none and was auto-corrected to 게임 변호사 (one hit, 법률사무소 창작). 고임 alone listed 4 places: 카페고임, 고임 (피부관리), 바이고임 (여성의류), 고임시스템 (컴퓨터판매); none is a law office. A Daum web search for `"법무법인 고임"` showed an image strip and a video about 물고임 (water pooling) defects from another firm, and an ad, with no place card and no web document for the name. Naver was refused by the browser's site restrictions and was not searched. AC13 repeats the checks and records them.
- **Why the 호암 auto-correction is accepted:** the clinic feature rejected 하늬 because its auto-correction landed on a near-identical real name (한희피부과). 호암 shares neither syllable with 고임, and the KBA search for 고임 itself returned 0, so no real firm is confused with it.
- **Rejected for C:** 섬돌 (법률사무소 섬돌, 서울 서초구, is a real law office found by Kakao Map searches for 섬돌 변호사, 섬돌 법률 and 섬돌).
- **Accepted risk:** 가늠 and 고임 are both two-syllable words that start with ㄱ and end with ㅁ, so they look alike in the gallery. 고임 also brings 물고임 to mind in search. The human approved both names with this noted (Q3).
- The industry key is `law`; it already exists in `INDUSTRIES`.
- Primary action: 상담 예약 (consultation by appointment). Secondary: 전화, 카카오톡 상담, 네이버 지도. Korean firms put these in a right-hand fixed rail on desktop: 법무법인 YK shows 전화상담 with the number, 채팅 상담, 빠른 상담 and 방문 예약; 법무법인 대륜 shows 카톡 상담, 빠른상담 and 전화상담, plus a phone number in the top utility bar. Our improvement is a mobile bottom bar with 상담 예약 and 전화 (AC43–AC44).
- Practice areas are headed "주요 업무분야", and each lawyer shows "주요취급분야" instead of "전문" (규정 제9조①).
- Lawyer careers on the page are generic and fictional (for example "○○ 기업 법무팀"); no real court, prosecutors' office, university or firm is named. 규정 제7조 allows a homepage to list 공직 career facts, but the sample avoids them so it cannot read as 전관 advertising.
- Lawyer cards use initials or a monogram, not portrait photos (AC48). A stock model's face next to a fictional lawyer's name would present a real person as that lawyer. This matches the shipped clinic samples, whose 의료진 sections use no portrait photos. The human decided at G1 to keep AC48 (Q4).
- AC22–AC28 are plain substring checks on the page text they name. Words that hit in an allowed sense (for example 전문 in 전문가, 출신 in 출신 학교) are still not used; the copy changes, not the list.
- **Rule sources, read on 2026-11-18.** 변호사법 제23조, 제44조 and 제45조: read on law.go.kr (국가법령정보센터). 「변호사 광고에 관한 규정」: the 2026 법규집 PDF on koreanbar.or.kr (자료실 › 법규집 › 회규), last amended 2026-11-09. Its 부칙 (2026-11-17) puts the 2026-11-09 changes to 제4조8 · 12호, 제5조②3호 and 제7조 into force three months after promulgation; the sample follows them already. Article numbers moved on 2025-02-06: the "전문" rule cited as 제7조① in older articles is now 제9조①, and 제9조① as amended 2026-11-09 bars "전문", "전담" and "특화" for any 법무법인. 「변호사 광고에 관한 규칙」 (규칙 제45호, 2024-10-21) was read in the 2025 법규집 edition (amended 2025-06-30); no later edition was found. AC22, AC27 and AC118 cite its 제4조④ (승소율, 석방률, 결과 예측), 제4조⑤ and 제7조 (titles that name a crime).
- **Not verified against a primary source:** 변호사법 제112조3호, cited in AC119 with 제44조②, was raised as a risk in design review and not read on law.go.kr; AC119 holds whatever it says. The 법무부 platform guideline (2025-05-27) that bans 별점 and numeric ratings was read only in a marketing blog's summary (blog.lawyerad.kr). AC28 does not depend on it; it is sample policy. 「변호사 전문분야 등록에 관한 규정」 was opened only to confirm it governs registration; display rules come from 규정 제9조①.
- 승소율 and 석방률 are barred by 규칙 제4조④; the 규정 has no express item for them. AC22 bans the outcome words, and AC33 bans all case counts as sample policy, since a fictional firm has no true figures to show.
- Photos: free Unsplash or Pexels photos of an office, a meeting table, books, documents, architecture or a city view, with no identifiable person giving advice. They are compared on a contact sheet in the implement stage, then downloaded at web size into each sample's `img/`.
- Mood targets, against the shipped samples. `flower-bomgyeol`: dark photo hero, centred spaced serif wordmark (Cormorant Garamond), Noto Serif KR headings, sand, raspberry `#b8325a`. `food-saebyeokmil`: paper cream `#f4efe5`, IBM Plex Mono labels, dawn blue `#2d43b4`. `clinic-neuru`: white `#ffffff`, light full-bleed interior photo, left wordmark, Gothic A1, pine `#2f6f62`. `clinic-byeotteul`: cool white `#f7f9fb`, rounded cards, Gowun Dodum, sun orange `#e08a2c`. `clinic-bonui`: warm off-white `#fbf9f7`, thin Noto Sans KR, chestnut `#8c5a43`.
- **Distinctness map (pair → ACs).** Each pair that the candidate notes rated low or medium has at least one command-checkable AC; AC72–AC73 are the human backstop.
  - A vs flower (both dark and serif): dark solid page, not a dark photo (AC82); no full-bleed photo hero (AC88); wordmark left, not spaced (AC86–AC87); neither of flower's faces (AC83–AC84); a Korean serif of its own (AC85); a cool accent, not raspberry (AC74).
  - C vs flower (full-bleed photo plus centred serif caps wordmark): C keeps a full-bleed photo hero by the human's decision (AC100, AC112, Q2), so the distance comes from the photo's feel and from palette and type: a subject that is not flowers or plants (AC114); not low-key (AC115, proxy AC116); neutral or cool, not saturated warm blooms (AC117); a stone base below the hero (AC94, AC95); sans headings (AC97); Hangul-only wordmark (AC98, AC110); none of flower's faces (AC96, AC108).
  - C vs `clinic-neuru` (fixing flower's overlap the clinic way would copy neuru: light photo, left wordmark, Gothic sans): stone-tinted base, not white (AC94); no Gothic A1 or any other shipped heading face, Pretendard included (AC96, AC108); a Korean architecture or material photo, not a light interior like neuru's waiting room (AC109); a vertical Korean text motif no sample has (no shipped `style.css` sets `writing-mode`; AC99).
  - C vs `clinic-byeotteul` and `clinic-bonui` (light bases): base channels at most `0xEA` (AC94); none of their heading faces (AC96, AC108).
  - C vs `food-saebyeokmil` (tinted light base): cool, not warm cream (AC95); no IBM Plex Mono (AC96).
  - A vs the light samples (food, three clinics): dark base (AC82).
  - A vs C: dark vs stone base (AC82, AC94); serif vs sans headings, with no heading face in common (AC85, AC96, AC97, AC108); Pretendard may stay as both body faces, as in every shipped sample; accents at least 25° apart (AC74); different practice areas (AC91, AC103).
  - A vs Selendy Gay: no red `PROFILES` accent (AC74 leaves no allowed hue between raspberry 342° and chestnut 19°; a red link colour in `style.css` is caught only by the human check AC72); no big-figure band (AC89, AC33); Korean serif and Korean copy (AC85, AC71).
  - C vs Kim & Chang: no hero search (AC101); no language switcher (AC102); no Latin caps wordmark (AC98, AC110); no Kim & Chang photo, nor one imitating its facade or hanok shots (AC113; free-licence sources only, AC54, AC59, AC60; no shared photo, AC71). What C keeps from it: a full-bleed photo hero (AC100, AC112) of Korean architecture or material (AC109), restraint and a light container look.
- **Accent hues are feasible.** With AC74's 25° rule and the five shipped hues (342°, 230°, 168°, 31°, 19°), the allowed bands are about 56°–143°, 193°–205° and 255°–317°. Navy, burgundy, forest green and brass are all excluded. Examples that pass, to be fixed in `tasks.md`: A steel blue `#4f93ad` (197°, saturation 0.37) on a graphite base such as `#1f2226`; C 자주 (Korean purple) `#7b3f78` (303°, saturation 0.32) on a stone base (the value is fixed in `tasks.md` Picks), headings in a Korean sans such as `IBM Plex Sans KR` or `Nanum Gothic` (AC96, AC108). A and C are then 106° apart.
- Per-sample ACs fix mood, the overlaps and the improvements only. They do not fix a reference's composition; the layout is new work per playbook §2.
- Improvements over the references (playbook §1-4). Both: the reference homes lead with news, search and brand statements; each law sample leads with 주요 업무분야, 구성원, 상담 안내 and 오시는 길 in that order (AC45), adds a mobile 상담 · 전화 bar (AC43–AC44) and Korean typography (AC47), and replaces outcome claims with compliant copy (AC22–AC36). A: Selendy Gay's first screen carries a win headline and its next band a recovered-amount figure; 가늠 puts entry links to its 주요 업무분야 on the first screen (AC90), shows the phone number as digits on the first mobile screen for clients who call in a hurry (AC93), and bans criminal-outcome words (AC92). C: Kim & Chang's first screen is a wordmark and a search box, and its next screen is news; 고임 replaces the search with consultation controls (AC101, AC42–AC43), tells a business what to bring to a first consultation (AC104), and shows which lawyer handles which area (AC106).
- The reference sites use copy and content our samples must not use: Selendy Gay "The premier law firm", "$40+ Billion recovered by our partners", a "Significant Victories" menu and win headlines; Kim & Chang leads with a search box and regulatory newsletter cards (not banned content, but not what a client of a small firm looks for first), and its name form 법률사무소 is not one our firms can use (AC16). We take mood and level only.
- AC92 and AC105 are sample-policy word lists on top of AC22–AC28, for the words each practice is most tempted to use: criminal outcomes for A (규정 제4조12호 bars predicting 처분 · 판결 results), client and 고문 names and savings for C (규정 제4조7호). They are plain substring checks like AC22.
- Mobile behaviour of the reference sites was not checked; mobile points are targets for our samples, not defects found in the references.
- `docs/current_system/` is current: on 2026-11-18 `git diff --stat e8f2f6d..HEAD` lists only the docs commit that re-pointed SHAs after the gallery-industries squash (`overview.md` `last_reconciled`, that feature's `spec.md` and `tasks.md`). No reconciliation is needed before design.

### Research: sites looked at (2026-11-18, Chrome)

| Site | Result |
| --- | --- |
| selendygay.com | Candidate A |
| farrer.co.uk | Candidate B |
| kimchang.com | Candidate C |
| fenwick.com | Candidate D |
| stanchierifamilylaw.com | Runner-up. Near-black page, centred light serif "We Approach Family Law with Confidence", a fanned arc of tilted lawyer portrait cards. Small family-law firm; lawyer-first. Dark and centred serif, close to `flower-bomgyeol`; relies on portraits (see AC48) |
| mishcon.com | Runner-up. Dark nav, warm film-still hero with a large serif headline, red accent buttons, a wide "How can we help you?" search bar. Large-firm media hub |
| shinkim.com (법무법인 세종) | Korean. Full-bleed blue-gold water photo, thin sans "Your Firm of Choice", plum search bar, right-side dot pager. Refined; search-led, not consultation-led |
| kobrekim.com | Seoul office photo under a client testimonial quote ("Best litigation firm…") in large sans. Testimonial-plus-superlative hero is the pattern AC22 and AC28 forbid |
| bkl.co.kr (법무법인 태평양) | Korean. Impersonation-warning popup over a dark hero with a 3D sculpture and a practice slider |
| yulchon.com (법무법인 율촌) | Korean. Conference-room photo with a navy box of five English values. Splash page, dated |
| yklawfirm.co.kr (법무법인 YK) | Korean, consumer-facing. Coral notice bar, city photo hero "고객중심 법률파트너", right fixed rail (전화상담 number, 채팅 상담, 빠른 상담, 방문 예약), case and consultation counters below. Useful for flow; counters are what AC33 forbids |
| daeryunlaw.com (법무법인 대륜) | Korean, consumer-facing. Utility bar with phone number, tower photo hero "실력은 경험한 사건 수로 증명됩니다" with a case search, right rail (카톡 상담, 빠른상담, 전화상담). Copy rests on case counts |
| kbennettlaw.com | Black page, thin spaced sans, pink small caps label, grey CTA box, chat widget. IP boutique; template feel |
| ylaw.ca | Group cut-out photo of lawyers with "BE HEARD" over it, "Award Winning Lawyers" tagline, busy nav. Lively but crowded |
| lewissilkin.com | Umbrella photo, large grey "Ideas + People", cookie panel over the lower half |
| kingsleynapley.co.uk | Hero image did not load (grey gradient only), maroon contact button. Not judged |
| twobirds.com | Cookie consent modal covered the page; dark teal with a serif headline behind it. Hero only partly seen |
| cooley.com | Loader and cookie banner only; page not seen |
| harbottle.com | Excluded: blocked by a security check |
| osler.com | Excluded: blocked by a security check |
| wordstone.law | Excluded: browser error page |
| wordstone.com | Excluded: redirected to another domain during load |
| pallaspartners.com | Excluded: a strategic advisory firm, not the law firm |

Site names came from web search results for curated lists (reallygooddesigns.com "law firm website design", whose list was read; clio.com, seahawkmedia.com, azurodigital.com, which were not opened), from known large Korean firms and from Korean consumer-facing firms.

Screenshots of the four candidates (first screen and one scroll further, 2026-11-18) and a contact sheet are kept outside the repository for G1, in the orchestrate run's scratchpad `law-candidates/` folder: `A-selendygay-1-first.jpg`, `A-selendygay-2-scroll.jpg`, `B-farrer-1-first.jpg`, `B-farrer-2-scroll.jpg`, `C-kimchang-1-first.jpg`, `C-kimchang-2-scroll.jpg`, `D-fenwick-1-first.jpg`, `D-fenwick-2-scroll.jpg`, `contact-sheet.jpg`, and the runner-up `runnerup-stanchieri-*.jpg`. The two Selendy Gay files are 1492 × 812; the rest are 1512 × 767 (the browser window's viewport changed between captures). Cookie banners on Farrer & Co and Fenwick were hidden with CSS before the shot; no consent was given.

### Candidates shown at G1 (history)

The descriptions below are the four candidates as shown to the human at G1. A and C were picked; B and D were not. Their Distance lines are resolved by the distinctness map above.

**A. Selendy Gay — https://www.selendygay.com**
Litigation boutique. Dark graphite page under a black-and-white sculpture photo on the right. Thin serif wordmark with a vertical bar top left, small sans nav right. A large left-aligned serif statement, a spaced small-caps label "NOTABLE HEADLINES", then a serif news headline and a red underlined link. One scroll down: a warm off-white band with a huge italic serif figure and a spaced caps caption.

```
+---------------------------------------------------------------+
| Wordmark|Bar                      Firm People ... Contact  (o) |
|                                         (b/w sculpture photo, |
| Large serif statement,                   right two-thirds)    |
| two lines                                                     |
|                                                               |
| SMALL CAPS LABEL                                              |
| Serif headline, two lines                                     |
| sans summary · red link                                       |
+---------------------------------------------------------------+
|            off-white band: huge italic serif figure           |
|                     SPACED CAPS CAPTION                       |
+---------------------------------------------------------------+
```

- Suits: a 송무 (litigation) or 형사 boutique that wants a serious, editorial look.
- Korean flow: the label-and-headline block becomes 주요 업무분야 entry points; 상담 예약 and 전화 join the nav; 카카오톡 상담 sits beside them on mobile in the bottom bar; 네이버 지도 sits in 오시는 길; the big-figure band must carry a statement, not a number (AC33).
- Distance: from `flower-bomgyeol` low to medium (dark photo, serif); needs a non-photo or light base, or a sans wordmark. From the others high.
- Caution: its signature device, the big recovered-amount figure, is banned here (AC33).

**B. Farrer & Co — https://www.farrer.co.uk**
Private-client firm. White top bar with a nav row and a "CONTACT US" cell. A navy vertical panel on the left holds a serif caps wordmark and a hairline-separated menu, and it overlaps a full-width abstract oil-paint hero (blue, green, yellow) with a light sans headline and an outline button. One scroll down: a pale blue-grey band, a search box, then a white card "Meet our team" beside a portrait photo.

```
+---------------------------------------------------------------+
|  +----------+  Nav  Nav  Nav  Nav  Nav     Search | CONTACT    |
|  | WORDMARK |-------------------------------------------------|
|  | -------- |  (full-width abstract painting)                  |
|  | Menu   > |                                                  |
|  | Menu   > |    Light sans headline,                          |
|  | Menu     |    three lines                                   |
|  | Menu   > |    [EXPLORE]                                     |
|  +----------+--------------------------------------------------|
|  pale band: search                                            |
|  [ white card: label, title, text, button | photo ]           |
+---------------------------------------------------------------+
```

- Suits: a 가사 · 상속 · 자산관리 firm with steady, long-term clients; calm and personal.
- Korean flow: the navy panel can hold 상담 예약 and 전화 under the menu on desktop; the "CONTACT US" cell becomes 상담 예약; the team card becomes the 구성원 entry (initials, not a portrait, per AC48); 카카오톡 상담 joins the panel and the mobile bar; 네이버 지도 sits in 오시는 길.
- Distance: high from all five shipped samples (navy panel and painted art; no shipped sample uses either).

**C. Kim & Chang (김·장 법률사무소) — https://www.kimchang.com**
Korean. A full-bleed rotating photo (hanok roofs in snow on the first load, a sunset glass facade on the second) with a centred white serif caps wordmark, a centred search box, language links top left, a menu icon, and "SCROLL DOWN". One scroll down: a white container over the photo with news cards in Korean sans and red category labels.

```
+---------------------------------------------------------------+
| KO EN JP CN                                   util | util     |
| ≡                                                             |
|                (full-bleed photo, rotating)                   |
|                    SERIF CAPS WORDMARK                        |
|                 [ search ..............  (o) ]                |
|                         ↓ SCROLL DOWN                         |
+---------------------------------------------------------------+
|   [ white container: news cards, red labels, Korean sans ]    |
+---------------------------------------------------------------+
```

- Suits: a 기업 자문 firm that wants a Korean identity (hanok, ink, stone) with restraint.
- Korean flow: the search box becomes a 상담 예약 · 전화 · 카카오톡 상담 bar; the news cards become 주요 업무분야 cards; 네이버 지도 sits in 오시는 길.
- Distance: from `flower-bomgyeol` low (full-bleed photo plus a centred serif wordmark is flower's hero). It would need a wordmark that is not centred or not serif, and a light photo without a dark overlay. From the others high.
- Note: 김·장 is a 법률사무소, not a 법무법인; only its mood is used.

**D. Fenwick — https://www.fenwick.com**
Tech and life-sciences firm. White header with a heavy black sans wordmark and an evenly spaced nav. A full-width saturated blue band with a very large white grotesque headline, and below it a split card (image left, white panel right with a dotted rule label, a sans headline and a "Learn More" arrow link). One scroll down: a white field with offset image cards and sans captions.

```
+---------------------------------------------------------------+
| WORDMARK     Nav    Nav    Nav    Nav    Nav    Nav       (o) |
+---------------------------------------------------------------+
| (saturated blue band)                                         |
| Huge white grotesque headline,                                |
| two lines                                                     |
| +----------------------------------+------------------+       |
| | image                            | label ·········· |       |
| |                                  | Sans headline    |       |
| |                                  | Learn More  →    |       |
+---------------------------------------------------------------+
|  [ image card ]                     [ offset image card ]     |
+---------------------------------------------------------------+
```

- Suits: a 스타트업 · IT · 지식재산 firm; confident and modern.
- Korean flow: the blue band carries the headline with 상담 예약, 전화 and 카카오톡 상담 under it; the split card becomes 주요 업무분야 cards; 네이버 지도 sits in 오시는 길.
- Distance: high from all five (bright blue band, heavy grotesque, white). Its accent must differ from food's dawn blue `#2d43b4` (AC74).
- Caution: its cards name clients and deal values, which AC32 forbids; ours hold practice areas only.

## Open questions

- **Q1. Which reference or references? — resolved 2026-11-18 at G1 by Seokhyun Kim.** Answer, as relayed by the orchestrator: "A, C로 만들어줘" — candidates A (Selendy Gay) and C (Kim & Chang), one law sample each, both in this feature; B (Farrer & Co) and D (Fenwick) are not used. No open question remains.
- **Q2. C's first screen: keep Kim & Chang's full-bleed photo hero, or drop it to stay away from flower? — resolved 2026-11-18 at G1 by Seokhyun Kim.** His words: "전면 사진을 살리자. 다만 꽃집과 다른 느낌의 사진을 가져오면 되지 김앤장 사진을 배끼면 절대 안되지만". C keeps a full-bleed photo hero (AC100, AC112). Distance from flower comes from a photo of a different feel (subject, light, colour temperature: AC114, AC115, AC116, AC117) plus palette and type. Kim & Chang's own photos, and close look-alikes of them, are never used (AC113, AC71).
- **Q3. Firm names — resolved 2026-11-18 at G1 by Seokhyun Kim**, as relayed by the orchestrator: 법무법인 가늠 (`law-ganeum`) and 법무법인 고임 (`law-goim`) are both approved.
- **Q4. AC48 (no lawyer portraits) — resolved 2026-11-18 at G1 by Seokhyun Kim**, as relayed by the orchestrator: keep it.
