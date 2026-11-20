---
status: shipped
approved_at: 648e8ab8ce70c1a236591cf59f0b241b0487f844
commits: 648e8ab8ce70c1a236591cf59f0b241b0487f844..f0dd5bbadba2a49e49bf57806c4b86517f40f84c
---

# Interior profile samples (`interior`)

## Problem

The `/profile/` gallery has no sample for the `interior` (인테리어) industry. The 인테리어 filter chip shows no count, and
the grid shows an "인테리어 프로파일 준비 중" tile. An interior business owner who opens the gallery finds nothing for
their business, and sales has no interior sample to show.

An interior site sells with its past work, and a sample has no past work. The sites opened for this spec (2026-11-20)
show real apartment complex names on every portfolio card (Apartmentary: "강남 타워팰리스2차", "용산 래미안첼리투스"),
figure rows ("1위 · 아파트 시공 경험", an NPS score, a portfolio count), star-rated reviews signed "김OO 님", discount
banners (한샘: "즉시할인 ~22%"), "Our services are free!" (Sweeten), and a person's portrait on the about page (Yellow
Plastic). On a sample, each of these would be fabricated. The sample's photos are stock photos, so a section that
presents them as the business's own projects would also be fabricated.

A visitor to an interior site wants to ask for an estimate (견적) or a consultation (상담). The reference sites send
that visitor to a 상담 신청 page or to a contact page with an inquiry form. A Korean visitor expects 카카오톡, 전화 and 네이버 next to it.

## Scope

"Each interior sample" below means each of the three folders `profile/interior-robininterior/`,
`profile/interior-robindesign/` and `profile/interior-robinhome/`. An AC that says "each interior sample" holds for all three.

- **In:** Sample A, `profile/interior-robininterior/`: 로빈인테리어, a light service-brand page with a white bar header, a wide photo under it, a three-card photo row and an FAQ; reference Apartmentary (AC108–AC137).
- **In:** Sample B, `profile/interior-robindesign/`: 로빈디자인, a type-led studio page whose first screen is two flat colour blocks with a giant Hangul wordmark and no photo; reference Studio Ashby (AC138–AC168).
- **In:** Sample C, `profile/interior-robinhome/`: 로빈홈, a mid-dark ink-blue page with one wide inset photo and a one-line serif statement under it; reference Studio McGee (AC169–AC194).
- **In:** For each interior sample: `index.html`, `style.css`, `thumb.jpg`, and photos in `img/` with `img/sources.txt`, built per `docs/profile-playbook.md`.
- **In:** A one-page site for one fictional interior business: what it does, example photos, how a job proceeds, and 견적 · 상담 문의.
- **In:** One `live` entry with `industry: "interior"` in `PROFILES` in `scripts/profiles.py` for each interior sample.
- **In:** The regenerated `profile/index.html`, made by `python3 scripts/build.py`.
- **In:** Content rules for a fictional interior business (AC27, AC29, AC30, AC51–AC67).
- **In:** Improvements over the references for Korean visitors: 견적 · 상담 reachable on every screen, and 카카오톡 · 전화 · 네이버 예약 · 네이버 지도 (AC33–AC50), plus the per-sample improvements in the sample blocks.
- **In:** Distinctness of each interior sample from the twelve shipped samples, from the other interior samples and from its own reference (AC82–AC92, AC108–AC204).
- **In:** Photo content rules (AC72, AC80, AC81).
- **In:** Reconcile `docs/current_system/` (the sample list in `profile-samples/component.md`) and set `last_reconciled`.
- **Out:** Candidate D (Yellow Plastic, proposed 로빈리빙 `interior-robinliving`). The human did not pick it at G1.
- **Out:** A business-name collision check and a `name-check.txt`. The human chose 로빈 + field-word names instead (Assumptions).
- **Out:** Changes to `assets/`, to `scripts/build.py`, to `docs/profile-playbook.md`, and to the twelve shipped samples under `profile/`.
- **Out:** Real estimate, booking, map, KakaoTalk or phone integration. Every action links to a `#` placeholder.
- **Out:** Forms of any kind (견적 신청서, 상담 신청서, file upload), chat widgets, an estimate calculator, member login, a shop and payment.
- **Out:** Inner pages (project detail pages, a portfolio archive, an about page, a contact page). Each sample is one page.
- **Out:** Franchise parts (지점 찾기, 가맹 문의). `interior` is not a franchise industry in playbook §3.
- **Out:** Self-hosting fonts. Google Fonts and Pretendard on jsDelivr stay allowed.
- **Out:** Samples for other industries.
- **Design:** none. Trigger 1 (crosses a component boundary): no. The change adds data and samples through the existing named interfaces (`PROFILES` item, URL `profile/<slug>/`, `thumb.jpg`), which stay unchanged. Trigger 2 (adds a component): no. Each sample is one more instance of the existing `profile-samples` component. Trigger 3 (alters a named interface): no. The `interior` key is already in `INDUSTRIES`, and the `PROFILES` fields, the URL, the thumbnail contract and the `profile_thumb.py` CLI stay the same. Trigger 4 (internal module boundary): no. A sample is one folder with one page, one stylesheet and its images. So `spec.md` + `tasks.md` are enough.

## Acceptance criteria

AC1–AC107 hold for every interior sample. AC108–AC194 are per-sample: the traits kept from each sample's
reference, its palette and typefaces, and what it must not copy from its reference. AC195–AC204 compare or
bind all three.

Folder and registration

- [ ] AC1 Each interior sample contains `index.html`, `style.css` and `thumb.jpg`.
- [ ] AC2 In each interior sample, `index.html` and `style.css` reference no local file outside that sample's folder (no `../`, no root-relative `/` path, no `assets/`).
- [ ] AC3 `scripts/profiles.py` has exactly one `PROFILES` entry for each interior sample's slug, each with `industry` `interior`, `status` `live` and `demo` `True`, and no `interior` entry for any other slug.
- [ ] AC4 Each interior sample's slug matches `interior-robin` followed by one or more lowercase ASCII letters only.
- [ ] AC5 Each interior sample's `thumb.jpg` is 1200 px wide with a 16:10 ratio and shows the sample's current 1440×900 first screen.
- [ ] AC6 `python3 scripts/build.py` exits 0.
- [ ] AC7 Compared with `main`, the branch changes no file outside the interior sample folders, `profile/index.html`, `scripts/profiles.py` and `docs/`, and does not change `docs/profile-playbook.md`.

Sample markers, names and metadata

- [ ] AC8 In each interior sample, the text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" is visible without scrolling at 1440 px width (browser).
- [ ] AC9 In each interior sample, the text of AC8 is visible without scrolling at 390 px width (browser).
- [ ] AC10 At 1440 px and at 390 px, the computed `font-size` of the AC8 text on the first screen is at least the computed `font-size` of `<body>` and at least 14 px (browser).
- [ ] AC11 At 1440 px and at 390 px, a person reads the AC8 text on the first screen in a colour that stands out clearly from its background (human).
- [ ] AC12 Each interior sample's footer contains "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다".
- [ ] AC13 Each interior sample's footer contains "Website by RobinTech".
- [ ] AC14 Each interior sample's footer has a "Photos:" credit that names each source used in its `img/sources.txt` (Unsplash, Pexels).
- [ ] AC15 Each interior sample's `index.html` contains `<meta name="robots" content="noindex">`.
- [ ] AC16 Each interior sample's `<title>` contains "디자인 샘플".
- [ ] AC17 The `name` of each interior sample's `PROFILES` entry is "로빈" followed by one or more Hangul syllables and nothing else.
- [ ] AC18 The accessible name of each interior sample's header wordmark starts with "로빈".
- [ ] AC19 No two interior samples share the same `PROFILES` `name`.
- [ ] AC20 In each interior sample, every address on the page includes "(가상 주소)".
- [ ] AC21 Every address in each interior sample names a district or road that does not exist (for example 가상구 결로), so no address points to a real building, and the page text names no real 구, 동, 신도시 or neighbourhood as the business's location or service area (for example 강남 · 서초 지역 전문); a 시 or 도 name alone is allowed (human).
- [ ] AC22 In each interior sample, every phone number on the page is `02-000-0000`.
- [ ] AC23 In each interior sample, every 사업자등록번호 on the page is `000-00-00000`.
- [ ] AC24 No interior sample shows a 건설업 등록번호, a 면허번호 or any other registration number; the 사업자등록번호 of AC23 is the only one allowed.
- [ ] AC25 Every e-mail address in each interior sample's page text or `mailto:` links ends in `@example.com`.
- [ ] AC26 The page text of each interior sample holds no social-media handle (`@` followed by a name, outside an `@example.com` e-mail address) and no domain name other than `example.com`.

Structure of the page

"Page text" below means, in `index.html`: visible text, `<title>`, `meta` description and `og:` content, `aria-label`, `alt` and `title` attributes; in `style.css`: `content:` strings. A listed word that holds a space is also banned written without the space (책임 시공 and 책임시공).

- [ ] AC27 The page text of each interior sample contains none of: 가맹, 프랜차이즈, 지점 찾기, 매장 찾기, 직영점 (one business, not a chain).
- [ ] AC28 Each interior sample has a section whose heading contains "서비스", "시공 범위" or "작업 범위" and that names at least three kinds of work (for example 전체 리모델링, 주방, 욕실).
- [ ] AC29 Each interior sample has exactly one section (the example section) that contains the visible sentence "예시 사진이며 실제 시공 사례가 아닙니다.", and that section contains at least three `<img>` from the sample's `img/`.
- [ ] AC30 The heading of the AC29 section contains "예시", and no heading or navigation link in the sample contains 시공 사례, 시공사례, 포트폴리오, Portfolio or Projects (any case).
- [ ] AC31 Each interior sample has a section whose heading contains "절차" or "과정" and that lists at least four steps in an `<ol>`.
- [ ] AC32 Each interior sample has a contact section whose heading contains "문의" or "상담".

Korean visitor flow

- [ ] AC33 The AC32 section of each interior sample has a link whose accessible name contains "견적".
- [ ] AC34 The AC32 section of each interior sample has a link whose accessible name contains "카카오톡".
- [ ] AC35 The AC32 section of each interior sample has a link whose accessible name contains "전화".
- [ ] AC36 The AC32 section of each interior sample has a link whose accessible name contains "네이버 예약".
- [ ] AC37 The AC32 section of each interior sample has a link whose accessible name contains "네이버 지도".
- [ ] AC38 No link in the AC32 section has an accessible name that contains two or more of 견적, 카카오톡, 전화, 네이버 예약 and 네이버 지도 (one link per action).
- [ ] AC39 In each interior sample, every AC33–AC37 control has `href="#"` (in-page navigation links such as a header's 문의 link are not such controls).
- [ ] AC40 Each interior sample has no `<form>` element.
- [ ] AC41 Each interior sample has no `<input>`, `<select>` or `<textarea>` element.
- [ ] AC42 In each interior sample at 1440 px width, a link to the AC32 section (`href="#<id>"` of that section) whose text contains "견적" or "상담" is visible without scrolling (browser).
- [ ] AC43 In each interior sample at 390 px width, a link of the AC42 kind is visible without scrolling (browser).
- [ ] AC44 In each interior sample at 390 px width, a link of the AC42 kind stays on screen at every scroll position (sticky bar or fixed button) (browser).
- [ ] AC45 In each interior sample at 390 px width, with the page scrolled to the end, the last text line of the footer is visible and not covered by a fixed or sticky element (browser).
- [ ] AC46 The AC32 section of each interior sample shows the 상담 hours as digits.
- [ ] AC47 The AC32 section of each interior sample shows the closed days.
- [ ] AC48 The AC32 section of each interior sample shows an address with "(가상 주소)" and the phone number `02-000-0000`.
- [ ] AC49 Each interior sample's Korean body text uses `word-break: keep-all`.
- [ ] AC50 Each interior sample's `<h1>` text is in Korean (contains at least one Hangul syllable).

Content of a fictional interior business, each interior sample

- [ ] AC51 The AC32 section contains the visible sentence "가상의 업체이며 실제 견적 · 상담을 받지 않습니다."
- [ ] AC52 The page text contains none of: 최고, 최초, 최대, 최다, 유일, 독보적, 1위, 1등, No.1 (any case), 넘버원, 업계 선두, 완벽, 보장, 보증, 무조건 (sample policy against superlative and guarantee claims; Apartmentary shows "1위").
- [ ] AC53 The page text contains none of: 수상, 어워드, Award (any case), 100대, 우수 업체, 인증, 공식 파트너, 협회, 면허 보유, 등록 업체 (sample policy: a fictional business has no award, certificate, licence or membership; 선정 is not listed because 자재 선정 is an ordinary process step, and AC65 covers it).
- [ ] AC54 The page text contains none of: 후기, 리뷰, 별점, 평점, 만족도, ★, 추천지수, NPS, 고객 인터뷰 (sample policy: no fabricated reviews or scores).
- [ ] AC55 The page text contains none of: 비포, 애프터, Before, After, 전후 사진, 시공 전후 (case-insensitive; sample policy: a before/after pair on a sample would be fabricated).
- [ ] AC56 The page text contains none of: 무료, 공짜, 할인, 이벤트, 선착순, 마감 임박, 프로모션, 쿠폰, 특가, 사은품 (sample policy: no lure offers).
- [ ] AC57 The page text contains none of: 무상, 평생, 하자 없, 무하자, 책임 시공 (sample policy: no warranty or after-service promise that no business stands behind).
- [ ] AC58 The page text contains no digit followed directly by 평, 건, 세대, 가구, 곳, 명, 년, 개월, 주 or 일; no digit followed, with optional spaces, by 억, 만 or 원, also after 천, 백 or 십; no `₩` or `￦` before a digit, no `KRW` after one, and no number with a thousands comma such as `35,000` (no floor area, project count, years in business, work period or money figure; sample policy; the first group allows no space, so that a phone number before 평일 or 주소 does not match).
- [ ] AC59 The page text contains no digit followed, with optional spaces, by `%`.
- [ ] AC60 The page text names no real interior, furniture, appliance, material or platform brand other than 네이버 and 카카오톡 (the footer credits of AC13 and AC14 aside): it contains none of 한샘, 리바트, Z:IN, KCC, 영림, 이케아, IKEA, 까사미아, 일룸, 오늘의집, 집닥, 숨고, 아파트멘터리, 삼성, 비스포크, 벤자민무어, 던에드워드, 구정마루, 동화자연마루, 그로헤, 콜러, 아메리칸스탠다드, 허먼밀러, 프리츠한센, 루이스폴센, 비트라 or USM (any case), nor LG or LX as a whole word, and a person finds no other such name; a social or video platform (for example 인스타그램, 유튜브, 페이스북, 핀터레스트, 네이버 블로그) counts as a platform brand, by name or by its logo or icon (human for the last part; 지인, 이건 and 오브제 are ordinary words and are left to the person).
- [ ] AC61 The page text names no real apartment brand or complex: it contains none of 래미안, 힐스테이트, 푸르지오, 아이파크, e편한세상, 롯데캐슬, 더샵, 타워팰리스, 아크로, 디에이치, 센트레빌, 위브, SK뷰 or 트리마제 (any case; 자이 is not listed because 디자이너 contains it), and a person finds no other real apartment brand, complex or building name anywhere on the page (human for the last part).
- [ ] AC62 The page text contains none of: 친환경, 무독성, 무해, 항균, 유해물질 없, E0, 새집증후군 (sample policy: a fictional business has no material facts behind a safety claim).
- [ ] AC63 No interior sample shows a person's name, whether as a designer, 대표, 실장, 시공 팀 or customer, and no photo is captioned or labelled as a staff member, a customer or a customer's home (human).
- [ ] AC64 No example photo is labelled with a real place, a complex, a floor area, a budget, a work period or a client, and no interior sample states a project count, years in business, a price or a period, in words or in digits (human; AC58 catches only a digit directly before a listed unit, so not "20여 년", "300채" or "Since 2009").
- [ ] AC65 No interior sample shows a testimonial, a quote attributed to a person, a star rating, a partner, press or product-brand logo, a mention of a partner, of press or broadcast coverage or of returning customers, an award, a licence or association claim, or a before/after pair of photos (human).
- [ ] AC66 No interior sample makes, in other words or in English, a claim of the kinds listed in AC52–AC57 and AC62, or presents the example photos as the business's own completed projects (human).
- [ ] AC67 No `alt` attribute in any interior sample contains 디자이너, 대표, 실장, 직원, 고객, 우리 팀, 시공 사례, 시공 현장 or 완공 (stock photos are never described as the business's staff or work).

Fonts, numbers and photos, each interior sample

- [ ] AC68 Every external stylesheet comes from `fonts.googleapis.com` or from Pretendard on `cdn.jsdelivr.net`; no other external CSS or JS is loaded.
- [ ] AC69 `index.html` and `style.css` contain no `http://` or `https://` URL whose host is not `fonts.googleapis.com`, `fonts.gstatic.com` or `cdn.jsdelivr.net`.
- [ ] AC70 The digits of 상담 hours and phone numbers render in a Korean typeface or a monospaced face, never in a proportional Latin face with old-style figures (browser).
- [ ] AC71 Every web font request succeeds, and the `<h1>` and the header wordmark render in a loaded web font, not in a fallback or a locally installed copy (browser).
- [ ] AC72 No photo ID recorded in an interior sample's `img/sources.txt` appears in the `img/sources.txt` of any other sample under `profile/`.
- [ ] AC73 Every image path referenced in `index.html` and `style.css` (`src`, `srcset`, CSS `url()`) resolves to an existing file inside that sample's `img/`, with the same letter case in every path part.
- [ ] AC74 Every file in `img/` other than `sources.txt` (dotfiles aside) is a `.jpg` or `.webp` file, and `img/` holds no folder.
- [ ] AC75 No image in `img/` is wider than 2000 px.
- [ ] AC76 No image file in `img/` is larger than 500 KB.
- [ ] AC77 The image files in `img/` total at most 3 MB (`thumb.jpg` is not counted).
- [ ] AC78 `img/sources.txt` has exactly one line per image file in `img/` (dotfiles aside), written as file name, photo page URL and download URL; the page URL starts with `https://unsplash.com/photos/` or `https://www.pexels.com/photo/`, or is `-`.
- [ ] AC79 Every download URL in `img/sources.txt` starts with `https://images.unsplash.com/photo-` or `https://images.pexels.com/photos/`, and no line contains `plus.unsplash.com` or `premium_photo`.
- [ ] AC80 Each interior sample's photos show home interiors, materials or details of them, and none shows a recognisable project of its reference site (human).
- [ ] AC81 A reviewer opens every image file in each interior sample's `img/` one by one at native resolution (100 % zoom, not on the page or a contact sheet) and finds no legible logo, brand name, signage, product label, appliance badge, book-spine or magazine title, poster or framed lettering, or other lettering (human).

Not the same site

- [ ] AC82 Each interior sample shares no text, logo, brand name or photo with its own reference site (the URL of its candidate in Assumptions).
- [ ] AC83 Side by side with its own reference site, a person does not read an interior sample as the same site (human).
- [ ] AC84 Side by side with the twelve shipped samples and the other interior samples, a person does not read an interior sample as the same design as any of them (human).
- [ ] AC85 Each interior sample keeps every layout trait listed for its candidate under "Traits to keep" in Assumptions (human; the measurable forms are AC108–AC194).
- [ ] AC86 The accent (the last `palette` hex) of each interior sample's `PROFILES` entry differs from the accent of every other `PROFILES` entry, and no hex appears in the `palette` of more than one interior sample (case-insensitive).
- [ ] AC87 Each interior sample's `style.css` contains the accent hex of its `PROFILES` entry (the last `palette` hex; case-insensitive).
- [ ] AC88 No interior sample's `<h1>` is a translation or close paraphrase of its reference's headline (human).
- [ ] AC89 No interior sample's hero photo is or imitates a photo on its reference site (human).

The interior samples against each other

- [ ] AC90 The first families in the computed `font-family` of the interior samples' `<h1>`s are pairwise different (browser).
- [ ] AC91 The first families in the computed `font-family` of the interior samples' header wordmarks are pairwise different (browser).
- [ ] AC92 Side by side, the interior samples differ pairwise in wordmark position and size, in palette, in typeface and in hero composition, and no two wordmarks read as one mark with a suffix added (human).

Accessibility and motion, each interior sample

- [ ] AC93 Every `<img>` has a non-empty `alt`.
- [ ] AC94 The page has exactly one `<h1>`, and no heading level is skipped.
- [ ] AC95 Under `prefers-reduced-motion: reduce`, at 1440 px and at 390 px, no element runs or declares an animation or transition longer than 0.01 s (browser).

Full-page checks, each interior sample

- [ ] AC96 At 1440 px width, the full page has no horizontal overflow (browser).
- [ ] AC97 At 390 px width (page inside a `width:390px` iframe), the full page has no horizontal overflow (browser).
- [ ] AC98 A full-page screenshot at 1440 px shows no overlapping or clipped text (browser, human review).
- [ ] AC99 A full-page screenshot at 390 px shows no overlapping or clipped text (browser, human review).

Gallery (served by `python3 -m http.server 8000`)

- [ ] AC100 On `/profile/`, the `interior` filter shows one card per interior sample (browser).
- [ ] AC101 On `/profile/`, the `interior` filter shows no "준비 중" tile (browser).
- [ ] AC102 In the generated `profile/index.html`, the `interior` filter chip shows the number of `interior` entries in `PROFILES` as its count.
- [ ] AC103 Clicking each interior card opens the preview with that sample loaded in the iframe (browser).
- [ ] AC104 For each interior card, the preview's desktop and mobile buttons switch the iframe between desktop and mobile width (browser).
- [ ] AC105 For each interior card, pressing Esc closes the preview (browser).

Reconciliation

- [ ] AC106 The Source line of `docs/current_system/profile-samples/component.md` lists each interior sample's slug.
- [ ] AC107 `git diff` from the `last_reconciled` commit in `docs/current_system/overview.md` to `HEAD` shows no change outside `docs/`.

Per-sample criteria. An AC marked (browser) below is measured in a 1440×900 viewport unless it names 390 px. 390 px means a 390×844 viewport; AC97 alone is measured inside a `width:390px` iframe 844 px high. "The example section" is the AC29 section, and "the contact section" is the AC32 section.

Sample A, `profile/interior-robininterior/` (로빈인테리어; reference Apartmentary, apartmentary.com)

- [ ] AC108 The `PROFILES` entry for `interior-robininterior` has `name` "로빈인테리어" and `palette` `["#f5f5f3", "#16181b", "#e3e2de", "#c8371f"]`, in that order.
- [ ] AC109 In `interior-robininterior/style.css` (custom properties resolved), the `body` background colour is `#f5f5f3` and the `body` text colour is `#16181b` (a neutral light page).
- [ ] AC110 Every RGB channel of the computed background colour of the `interior-robininterior` `<header>` is at least `0xF8`, and that colour is opaque (the white bar kept from Apartmentary) (browser).
- [ ] AC111 The left edge of the `interior-robininterior` header wordmark is within 144 px of the viewport's left edge (browser).
- [ ] AC112 The first family in the computed `font-family` of the `interior-robininterior` header wordmark is `Do Hyeon`, and its computed `font-size` is from 20 px to 26 px (browser).
- [ ] AC113 The `interior-robininterior` `<header>` holds a `<nav>` with at least four links, each with an `href` that starts with `#`.
- [ ] AC114 The horizontal centre of that `<nav>` box is within 144 px of the viewport's horizontal centre (centred navigation kept) (browser).
- [ ] AC115 The `interior-robininterior` `<header>` holds a link whose `href` is `#<id>` of the contact section, whose text contains "상담", and whose right edge is in the right quarter of the viewport (browser).
- [ ] AC116 The AC115 link has a computed `border-radius` of at least half its rendered height and the computed background colour `#16181b` (the dark pill kept) (browser).
- [ ] AC117 At 390 px, the AC115 link is visible in the header without scrolling (browser).
- [ ] AC118 The first `<img>` in `interior-robininterior` (document order) is from its `img/`, its rendered box spans the full viewport width, and its top edge is within 2 px of the bottom edge of the `<header>` (the wide photo directly under the header) (browser).
- [ ] AC119 The rendered height of the AC118 photo is from 450 px to 612 px (browser).
- [ ] AC120 The element that holds the AC118 photo contains exactly one `<img>` and no `<button>` (one static photo, no slider).
- [ ] AC121 Exactly one link has its rendered box inside the box of the AC118 photo: the caption. Its `href` is `#<id>` of the example section and its text contains "예시" (browser).
- [ ] AC122 The caption text contains at least one Hangul syllable, no digit and no Latin letter (not "포트폴리오 | 강남 타워팰리스2차"; AC64 covers what it names).
- [ ] AC123 The caption's box is at most 1.8 times as tall as its computed `font-size` (one line) (browser).
- [ ] AC124 No element with its own text, other than the caption and any fixed or sticky bar, overlaps the AC118 photo (browser).
- [ ] AC125 At 1440 px and at 390 px, a person reads the caption clearly against the photo (human).
- [ ] AC126 The `interior-robininterior` `<h1>` box lies below the bottom edge of the AC118 photo, and its top edge is at most 840 px from the top of the viewport (the headline is under the photo and starts on the first screen; `clinic-neuru` sets its text above its photo) (browser).
- [ ] AC127 The first family in the computed `font-family` of the `interior-robininterior` `<h1>` is `Do Hyeon` (browser).
- [ ] AC128 The example section of `interior-robininterior` holds exactly three cards, each with exactly one `<img>` and a caption that contains at least one Hangul syllable (the three-card photo row).
- [ ] AC129 The top edges of the three AC128 cards lie within 4 px of each other (one row) (browser).
- [ ] AC130 At 390 px, the three AC128 cards stack in one column (browser).
- [ ] AC131 `interior-robininterior` has a section whose heading contains "자주 묻는 질문" and that holds at least four `<details>` elements, each with a `<summary>` that contains at least one Hangul syllable (the FAQ accordion, with no script).
- [ ] AC132 In `interior-robininterior`, the AC31 section comes before the AC131 section, and the AC131 section comes before the contact section (document order).
- [ ] AC133 No question or answer in the AC131 section states a cost, a work period, a warranty or after-service term, or a discount, in digits or in words (human; an interior FAQ asks about these by habit, and AC56–AC58 catch only the listed words).
- [ ] AC134 The computed background colour of the `interior-robininterior` `<footer>` is `#16181b` (the dark footer kept) (browser).
- [ ] AC135 In `interior-robininterior`, no element whose own text contains a digit has a computed `font-size` above 24 px (no figures row like Apartmentary's "1,339±" and "1위") (browser).
- [ ] AC136 `interior-robininterior/index.html` and `style.css` contain neither `Decimal` nor `Spoqa` (Apartmentary's faces; any case).
- [ ] AC137 The AC118 photo shows no person, and it is not a kitchen island before a walnut wall with a high-rise view through the window (Apartmentary's home slide, seen on 2026-11-20) (human).

Sample B, `profile/interior-robindesign/` (로빈디자인; reference Studio Ashby, studioashby.com)

"The wordmark block" and "the headline block" are the two colour blocks of the first screen.

- [ ] AC138 The `PROFILES` entry for `interior-robindesign` has `name` "로빈디자인" and `palette` `["#0b5f65", "#f8f1fb", "#deb1f1", "#ee68ae"]`, in that order.
- [ ] AC139 In `interior-robindesign/style.css` (custom properties resolved), the `body` background colour is `#f8f1fb` and the `body` text colour is `#1b1430`.
- [ ] AC140 On load, no `<img>` box and no element whose computed `background-image` is other than `none` intersects the `interior-robindesign` viewport (a first screen with no photo) (browser).
- [ ] AC141 The `interior-robindesign` first screen shows the wordmark block and the headline block side by side: each is from 40 % to 60 % of the viewport width, the two do not overlap, and together they span the full viewport width (browser).
- [ ] AC142 The part of each block that lies inside the viewport is at least 720 px high (browser).
- [ ] AC143 The computed background colour of the wordmark block is `#ee68ae` and that of the headline block is `#0b5f65` (browser).
- [ ] AC144 The `interior-robindesign` header wordmark is live text inside `<header>` and inside the wordmark block, its accessible name is "로빈디자인", and `<header>` holds no other element whose text or accessible name is "로빈디자인". AC18, AC71 and AC91 are checked on this element.
- [ ] AC145 The AC144 wordmark has a computed `font-size` of at least 180 px, and its rendered text is at least 1.8 times as tall as that `font-size` (two or more lines) and at least 70 % as wide as the wordmark block (the giant stacked wordmark kept) (browser).
- [ ] AC146 The first family in the computed `font-family` of the AC144 wordmark is `Black Han Sans`, and its computed colour is `#1b1430` (browser).
- [ ] AC147 The AC144 wordmark has a computed `letter-spacing` of at most 0.05 times its `font-size` (browser).
- [ ] AC148 The lines of the AC144 wordmark start at one left edge (not Studio Ashby's staggered lines "STU / DIO / ASH / BY") (human).
- [ ] AC149 The `interior-robindesign` `<h1>` is inside the headline block and is not the wordmark; the first family in its computed `font-family` is `Black Han Sans`, and its computed colour is `#f8f1fb` (browser).
- [ ] AC150 The headline block holds a link whose `href` is `#<id>` of the contact section and whose text contains "견적" or "상담"; its computed background colour is `#ee68ae` and its computed colour is `#1b1430` (browser).
- [ ] AC151 The `interior-robindesign` `<header>` holds a `<nav>` with at least four links, each with an `href` that starts with `#`, and all of them are visible on the first screen (Studio Ashby's first screen has no navigation) (browser).
- [ ] AC152 On load, no fixed-position element covers more than half of the `interior-robindesign` viewport, and the document is more than 1800 px tall (the page scrolls on with no click; Studio Ashby's first screen is a gate) (browser).
- [ ] AC153 The `interior-robindesign` first screen names one business: it shows no second brand name and no brand mark or emblem (human; Studio Ashby's second block names its sister brand).
- [ ] AC154 At 390 px, the wordmark block spans the full width as the first block of the page (only the sample-marker strip of AC9 may sit above it), and the headline block spans the full width directly below it (browser).
- [ ] AC155 At 390 px, the AC144 wordmark has a computed `font-size` of at least 90 px, and the wordmark block is at most 420 px high (browser).
- [ ] AC156 At 390 px, on load, the `<h1>` box lies fully inside the viewport and no fixed or sticky element covers it (browser).
- [ ] AC157 `interior-robindesign` has a section that spans the full viewport width, has the computed background colour `#deb1f1`, and holds exactly one `<p>` and no `<img>` (the full-width colour band kept) (browser).
- [ ] AC158 The AC157 `<p>` has computed `text-align` `center`, the horizontal centre of its rendered text is within 24 px of the viewport's horizontal centre, and its computed colour is `#1b1430` (browser).
- [ ] AC159 The example section of `interior-robindesign` holds a feature: a panel with the computed background colour `#0b5f65` or `#ee68ae` and no background image, side by side with one `<img>` (top edges within 4 px, no overlap, each at least 35 % of the viewport width) (the colour block beside a photo kept) (browser).
- [ ] AC160 The AC159 panel holds a heading that contains at least one Hangul syllable, and one paragraph (AC64 covers what the heading names).
- [ ] AC161 The example section of `interior-robindesign` holds a row of exactly four tiles, each with exactly one `<img>` and a caption that contains at least one Hangul syllable (the four-tile photo row kept).
- [ ] AC162 The top edges of the four AC161 tiles lie within 4 px of each other (browser).
- [ ] AC163 At 390 px, the four AC161 tiles form two rows of two (browser).
- [ ] AC164 The example section of `interior-robindesign` holds exactly five `<img>` (the feature photo and the four tiles).
- [ ] AC165 In `interior-robindesign/style.css`, every colour in a `background`, `background-color` or `background-image` value (gradient stops, `:hover` and `@media` rules included) whose largest RGB channel minus its smallest is above `0x30` is `#ee68ae`, `#0b5f65` or `#deb1f1` at full opacity (case-insensitive; three saturated colours and no other, so no translucent tint of them either).
- [ ] AC166 `interior-robindesign/style.css` contains none of `#633B2F`, `#B19E18`, `#E87308`, `#45519F` or `#F9F3F0` (case-insensitive; Studio Ashby's brown, olive, orange, cobalt and body colour, read on 2026-11-20).
- [ ] AC167 `interior-robindesign/index.html` and `style.css` contain none of `BEAUX`, `Allrounder` or `Matter` (Studio Ashby's faces; any case).
- [ ] AC168 `interior-robindesign` has no hero photo, so AC89 is checked on its AC159 photo: that photo neither is nor imitates a photo on studioashby.com (human).

Sample C, `profile/interior-robinhome/` (로빈홈; reference Studio McGee, studio-mcgee.com)

- [ ] AC169 The `PROFILES` entry for `interior-robinhome` has `name` "로빈홈" and `palette` `["#2a3f63", "#f0eadf", "#1c2433", "#d2a96a"]`, in that order.
- [ ] AC170 In `interior-robinhome/style.css` (custom properties resolved), the `body` background colour is `#2a3f63` and the `body` text colour is `#f0eadf` (a mid-dark coloured page: HSL lightness 0.28, channel spread `0x39`, hue 218°; Studio McGee's `#484D49` has a spread of `0x05`).
- [ ] AC171 The computed background colour of the `interior-robinhome` `<header>` is `#2a3f63` or transparent (the header is part of the page colour) (browser).
- [ ] AC172 The first `<img>` in `interior-robinhome` (document order) is from its `img/`, lies fully inside the viewport, is at least 1150 px wide, and has a gap of at least 40 px to each side edge of the viewport, the two gaps differing by at most 4 px (the wide inset photo kept) (browser).
- [ ] AC173 The top edge of the AC172 photo is at least 16 px below the bottom edge of the `<header>` (browser).
- [ ] AC174 The AC172 photo is rendered at least 1.8 times as wide as it is tall, with a computed `border-radius` of at most 4 px (`clinic-byeotteul`'s inset photo is rounded) (browser).
- [ ] AC175 No element with its own text, other than a fixed or sticky bar, overlaps the AC172 photo (browser).
- [ ] AC176 The `interior-robinhome` `<h1>` box starts at least 16 px below the bottom edge of the AC172 photo, lies fully inside the viewport, and the horizontal centre of its rendered text is within 24 px of the viewport's horizontal centre (the centred statement under the photo kept) (browser).
- [ ] AC177 The nearest non-transparent background behind the `interior-robinhome` `<h1>` is `#2a3f63` (the page colour frames the photo on its fourth side too) (browser).
- [ ] AC178 The `interior-robinhome` `<h1>` box is at most 1.6 times as tall as its computed `font-size` (one line) (browser).
- [ ] AC179 The first family in the computed `font-family` of the `interior-robinhome` `<h1>` is `Diphylleia`, and its computed colour is `#f0eadf` (a Korean serif statement) (browser).
- [ ] AC180 The `interior-robinhome` `<h1>` holds exactly one `<em>`, whose computed `font-style` is `normal` and whose computed colour is `#d2a96a` (the second style is a colour, because Hangul has no italic) (browser).
- [ ] AC181 The text of the AC180 `<em>` contains at least one Hangul syllable, and the `<h1>` has text outside the `<em>` (one part of the line, not all of it).
- [ ] AC182 On load, the `interior-robinhome` first screen shows, outside the `<header>` and outside any fixed or sticky bar, a link that lies fully inside the viewport, whose `href` is `#<id>` of the contact section and whose text contains "견적" or "상담" (browser).
- [ ] AC183 The `interior-robinhome` `<header>` shows a visible link whose `href` is `#<id>` of the contact section and whose text contains "견적" or "상담" (Studio McGee's "Work With Us" is one navigation item among five) (browser).
- [ ] AC184 The horizontal centre of the `interior-robinhome` header wordmark is within 24 px of the viewport's horizontal centre (browser).
- [ ] AC185 The first family in the computed `font-family` of the `interior-robinhome` header wordmark is `Diphylleia`, its computed `font-size` is from 30 px to 44 px, and its computed `letter-spacing` is at most 0.05 times its `font-size` (`flower-bomgyeol`'s centred logo is spaced at 0.34 em) (browser).
- [ ] AC186 The computed background colour of the `interior-robinhome` example section is `#f0eadf`, and the computed colour of its captions is `#1c2433` (the light section under the dark first screen kept) (browser).
- [ ] AC187 The example section of `interior-robinhome` holds exactly three cards, each with exactly one `<img>` and a caption that contains at least one Hangul syllable.
- [ ] AC188 The top edges of the three AC187 cards lie within 4 px of each other (three columns) (browser).
- [ ] AC189 At 390 px, the three AC187 cards stack in one column (browser).
- [ ] AC190 In `interior-robinhome`, no element whose first computed family is `Diphylleia` has a digit in its own text or in its generated content (browser).
- [ ] AC191 `interior-robinhome/style.css` contains neither `#484D49` nor `#F9F7F4` (case-insensitive; Studio McGee's page and body colours, read on 2026-11-20).
- [ ] AC192 `interior-robinhome/index.html` and `style.css` contain none of `ftBureau`, `Jost` or `Schibsted` (Studio McGee's faces; any case).
- [ ] AC193 No heading and no navigation link in `interior-robinhome` contains 쇼핑, 스토어, 블로그, 매거진, Shop, Blog or Read (any case; Studio McGee's home leads to a shop and a blog).
- [ ] AC194 The AC172 photo is not a living room with a grand piano, a wall tapestry and an indoor olive tree (Studio McGee's home photo, seen on 2026-11-20) (human).

All three interior samples

- [ ] AC195 The text of every link in each interior sample's header `<nav>` contains at least one Hangul syllable and no Latin letter.
- [ ] AC196 The accessible name of each interior sample's header wordmark contains no Latin letter.
- [ ] AC197 Each interior sample's `index.html` requests exactly one family from `fonts.googleapis.com`: `Do Hyeon` in `interior-robininterior`, `Black Han Sans` in `interior-robindesign`, `Diphylleia` in `interior-robinhome` (no shipped sample loads any of the three).
- [ ] AC198 In each interior sample, every element whose first computed family is `Do Hyeon`, `Black Han Sans` or `Diphylleia` has the computed `font-weight` 400 (each face has one weight; no synthesised bold) (browser).
- [ ] AC199 The first family in the computed `font-family` of each interior sample's `<body>` is `Pretendard Variable` or `Pretendard` (browser).
- [ ] AC200 In each interior sample's contact section, the elements that show the 상담 hours and the phone number have `Pretendard Variable` or `Pretendard` as the first computed family (the measurable form of AC70) (browser).
- [ ] AC201 In each interior sample, at 1440 px and at 390 px, every element with its own text that does not overlap an `<img>` has a contrast ratio of at least 4.5:1 between its computed colour and the nearest non-transparent background behind it, or at least 3:1 when its computed `font-size` is 24 px or more (WCAG 2 AA) (browser).
- [ ] AC202 Each interior sample's `img/` holds at most six image files (`sources.txt` and dotfiles aside).
- [ ] AC203 The `title`, `summary` and `features` of each interior sample's `PROFILES` entry (the gallery card text) contain none of the words and digit forms that AC27 and AC52–AC62 ban in page text.
- [ ] AC204 The `title`, `summary` and `features` of each interior sample's `PROFILES` entry hold nothing that the human parts of AC60 and AC61 or AC63–AC66 forbid on the page (human).

Every AC above is checked by a `tasks.md` verify (command, browser or human); there is no feature `verify.md`; `docs/verify.md` applies.

## Assumptions

- The industry key is `interior` with the label 인테리어; it already exists in `INDUSTRIES` in `scripts/profiles.py`, and no `PROFILES` entry uses it yet (checked 2026-11-20).
- **Naming (human decision, binding).** Each sample's name is "로빈" plus a field word (로빈인테리어, 로빈홈, 로빈리빙, 로빈디자인), so the name alone shows it is a sample. The human accepted that a real business with the same name may exist. This feature runs no name-collision check and writes no `name-check.txt`. This overrides "상호는 가상" in playbook §2; the rest of §2 holds (AC20–AC24). The slug is `interior-` plus the name in Latin letters (AC4), with English words as the human's example `interior-robininterior` does.
- **Not a franchise, no advertising statute (human decision).** `interior` is one business's site, and it is not one of the playbook §3 advertising-rule industries. The content bans in AC51–AC67 are sample policy chosen by the agent. No statute was read for them (건설산업기본법's 실내건축공사업 registration and 표시광고법 were not read).
- **Example photos (agent decision).** An interior site's main proof is its portfolio, and a sample has stock photos only. Each sample keeps a photo section in the place where the reference shows its work, and the section says "예시 사진이며 실제 시공 사례가 아닙니다." (AC29). Its heading and captions name a room or a style (거실, 주방, 밝은 나무 톤), never a place, a complex, a floor area, a budget or a client (AC61, AC64). The heading says 예시 (for example "공간 예시"), and no heading or nav link says 시공 사례 or 포트폴리오 (AC30), for every candidate.
- **No prices, counts or periods (agent decision).** The sample states no price, floor area, project count, years in business or work period (AC58, AC64). The process section names its steps without days or money.
- **No named people (agent decision).** No designer, 대표 or customer is named or pictured as such (AC63, AC67). Yellow Plastic's about page shows a designer portrait; the sample has none.
- **Contact notice (agent decision).** The contact section says "가상의 업체이며 실제 견적 · 상담을 받지 않습니다." (AC51), as the beauty samples do for 가맹.
- **Contact shape (human decision at G1, A3 below).** 견적 문의, 카카오톡 상담, 전화, 네이버 예약 (방문 상담 예약) and 네이버 지도 (오시는 길) are links to `#`, with no form (AC33–AC41). A 견적 · 상담 link stays on the 390 px screen (AC44).
- **Photo route (human decision).** In the implement stage the agent opens Unsplash and Pexels search pages in Chrome, compares candidates on a contact sheet, and downloads only from `images.unsplash.com` and `images.pexels.com`. It does not call the `unsplash.com/napi` search API. Unsplash+ (`plus.unsplash.com`) is not used (AC79). Interior stock photos often show books, posters and appliance badges, so AC81 is checked at native resolution.
- **Kept traits (human decision, law run 2026-11-18; applied here by the orchestrator). This adjusts playbook §1-4 ("구성 … 은 새로 만들고") and §2 (no copied layout): the listed traits of the picked screenshot stay, and everything else is made new.** The human picks a candidate from its screenshot. The sample keeps the traits listed for it under "Traits to keep" (AC85). "Not the same site" is met through photos, palette, typeface, copy and section order (AC82, AC83, AC88, AC89), never by removing a kept trait. No photo, text or logo of a reference is used.
- **Reference fonts and colours (read 2026-11-20, Chrome, computed styles of the home pages).** Apartmentary: `Decimal`, `SpoqaHanSans`; white body. Studio Ashby: `BEAUX-Display`, `Allrounder Antiqua`, `Matter`; body `#F9F3F0`. Studio McGee: `ftBureau`, `Jost`, `Schibsted Grotesk`; header `#484D49`, body `#F9F7F4`. Yellow Plastic: `Helvetica Neue`, `SUIT`; white body. The colour blocks of Studio Ashby were read from the screenshot afterwards (A7 below).
- **Accent hues today (computed 2026-11-20 from `scripts/profiles.py`).** Chromatic accents: `#8c5a43` 19°, `#e08a2c` 31°, `#a3a34d` 60°, `#2f5e3a` 134°, `#2f6f62` 168°, `#4f93ad` 197°, `#2d43b4` 230°, `#613d8f` 266°, `#7b3f78` 303°, `#b8325a` 342°. Achromatic: `#2a2a2a`, `#8a847a`. Under the beauty rule (25° from every other accent) one band is free: about 85°–109° (yellow-green). That rule does not apply here (A2 below).
- **Body bases today (from each sample's `style.css`).** Near-black or dark: `flower-bomgyeol` (dark photo, ink `#1c1915`), `law-ganeum` `#1f2226`, `beauty-robinhair` `#17130f`. White: `clinic-neuru` `#ffffff`, `beauty-robinsalon` `#fcfcfb`, `fitness-mideoum` `#f8f7f5`, `clinic-byeotteul` `#f7f9fb`, `clinic-bonui` `#fbf9f7`. Cream: `food-saebyeokmil` `#f4efe5`, `fitness-jjuuk` `#fbf3e2`. Grey: `law-goim` `#e4e5e6`, `beauty-robinhairsalon` `#e8e3dc`. The twelve `thumb.jpg` files were viewed side by side on 2026-11-20. Every shipped sample carries the sample marker as a thin strip at the top. `law-ganeum` has a first screen with no photo (one graphite colour). `clinic-bonui` has a split first screen (photo left, text right). `clinic-byeotteul` has an inset rounded photo on a light page. `clinic-neuru` has a white text band above a wide photo. `fitness-jjuuk` is cream with deep-green type and a green button. No shipped sample has a mid-dark coloured page, or a first screen made of two flat saturated colour blocks.
- §6-1 check: `git diff --stat 5556f9a..HEAD` (the `last_reconciled` in `overview.md`) lists three files, all under `docs/` (the `last_reconciled` line and the beauty feature's SHA re-pointing). None is system code, so `current_system/` still describes the system.
- Mobile layouts of the reference sites were not checked. Mobile points are targets, not defects found in the references.
- Home pages were opened in Chrome at about 1440 px. Candidate A's home was scrolled to its footer. Candidate B's splash was entered and its home scrolled three screens. Candidate C's home was scrolled two screens. Candidate D's home, work, contact and about pages were opened. Mobbin was not used.
- The candidate screenshots (1440×900, taken 2026-11-20) are in the session scratchpad, not in the repository: `A-apartmentary.png`, `B-studioashby.png`, `C-studiomcgee.png`, `D-yellowplastic.png`.

### Decisions after G1

- A1 (decided 2026-11-20, human Seokhyun Kim, G1): build three samples under the proposed names: A Apartmentary → 로빈인테리어 `interior-robininterior`; B Studio Ashby → 로빈디자인 `interior-robindesign`; C Studio McGee → 로빈홈 `interior-robinhome`. D Yellow Plastic (로빈리빙 `interior-robinliving`) is not built. This closes Q1.
- A2 (decided 2026-11-20, human, G1): the 25° accent-hue rule of the beauty feature does not apply to `interior`. AC84 (a person, side by side) and AC86 (no shared accent hex) stay. This closes Q2.
- A3 (decided 2026-11-20, human, G1): 견적 문의 is a set of `#` links with no form (AC40, AC41). This closes Q3.
- A4 (decided 2026-11-20, agent): palettes. Contrast ratios are WCAG 2, computed on 2026-11-20.
  - A: page `#f5f5f3`, text and dark surfaces `#16181b` (16.29:1 on the page), line `#e3e2de`, accent vermilion `#c8371f` (hue 9°; 4.78:1 on the page, 5.22:1 on white, white on it 5.22:1). The header is white. Text on `#16181b` is `#f5f5f3`; the accent is not text there (3.41:1).
  - B: wordmark block pink `#ee68ae` (hue 329°) with `#1b1430` text (6.08:1); headline block teal `#0b5f65` (hue 184°) with `#f8f1fb` text (6.68:1); band lilac `#deb1f1` (hue 282°) with `#1b1430` text (9.81:1); page `#f8f1fb` with `#1b1430` text (15.95:1). On teal only `#f8f1fb` is used for text: pink, lilac and `#1b1430` fail there. The accent is the pink.
  - C: page `#2a3f63` (hue 218°, HSL lightness 0.28) with `#f0eadf` text (8.82:1); accent sand `#d2a96a` (hue 36°; 4.84:1 on the page); light section `#f0eadf` with `#1c2433` text (13.0:1). The accent is text on the dark page only: on `#f0eadf` it is 1.82:1.
  - No accent equals an accent in `scripts/profiles.py`, and no hex is in two of the three palettes (AC86). AC201 checks contrast on the built pages.
- A5 (decided 2026-11-20, agent): typefaces. A: `Do Hyeon` for the wordmark and `<h1>`. B: `Black Han Sans` for the wordmark and `<h1>`. C: `Diphylleia` for the wordmark and `<h1>`. Body text, hours and phone digits are Pretendard in all three, as in the twelve shipped samples. On 2026-11-20 `fonts.googleapis.com` served each of the three faces with Hangul in weight 400 only (Google Fonts lists `Diphylleia` as a serif), and no sample under `profile/` loads any of them (`grep` of every `index.html`). A sample may use its display face for other headings.
- A6 (decided 2026-11-20, agent): A's hero is one static photo, not a slider. A slider needs script or more photos, and an arrow that does nothing would mislead. The caption on the photo is a link to the example section and says "예시" (AC121), because a caption labels its photo and this photo sits outside that section. B's and C's photos outside the example section carry no caption; the sample marker (AC8) and AC66 cover them.
- A7 (decided 2026-11-20, agent): Studio Ashby's colours were read as pixels from `B-studioashby.png`: brown `#633B2F` (hue 14°), olive `#B19E18` (53°), orange `#E87308` (29°), cobalt `#45519F` (232°). The screenshot is the splash. The olive band and the cobalt block seen after entry were not captured and may differ by a few values. Each of B's three colours is at least 40° from each of the four hues (329° is 45° from 14°; 184° is 48° from 232°; 282° is 50° from 232°).
- A8 (decided 2026-11-20, agent): in B, the giant wordmark is the header wordmark (AC144), and the `<h1>` is the Korean headline in the second block. At 390 px the blocks stack, wordmark block first (AC154–AC156). The wordmark block is pink and the headline block teal, so that every text pair passes 4.5:1.
- A9 (decided 2026-11-20, agent): in C, the second style of the statement is the accent colour on a Hangul phrase (AC180), not a Latin italic word. `beauty-robinhair` already mixes a Latin italic into a Korean serif headline. C's wordmark is centred, so that it differs in position from A's (AC184, AC92).
- A10 (decided 2026-11-20, agent): the kept photo rows are the example section of AC29: A's three cards, B's feature photo and four tiles, C's three cards. Photo places: A four to six (hero, three cards, at most two more), B five or six, C four to six. AC202 caps each sample at six files, so six files of at most 500 KB (AC76) stay within 3 MB (AC77).
- A11 (decided 2026-11-20, agent): the 390 px checks of the per-sample ACs use a 390×844 viewport, as the beauty feature did.
- A12 (decided 2026-11-20, agent): gallery card titles. A "흰 바 헤더와 넓은 사진의 리모델링 인테리어"; B "두 색면과 큰 한글 워드마크의 주거 디자인 스튜디오"; C "짙은 청색 지면에 사진 한 장을 둔 홈스타일링". `summary` and `features` are written in the implement stage (AC203, AC204).
- A13 (decided 2026-11-20, agent): B's teal half screen is the nearest of the new colours to shipped ones (`clinic-neuru` accent 168°, `law-ganeum` accent 197°, `fitness-jjuuk` green band 134°). Those are accents or one band on a light or graphite page; here teal fills half the first screen beside pink. AC84 leaves the judgement to a person.
- A14 (decided 2026-11-20, agent, orchestrate auto): social and video platforms (인스타그램, 유튜브 and the like) count as platform brands in AC60, by name, logo or icon; 네이버 and 카카오톡 stay the only platforms named, and of 네이버 only 예약 and 지도 (not 네이버 블로그). A real 구, 동, 신도시 or neighbourhood is not named as the business's location or service area (AC21); a 시 or 도 name alone is allowed. The stricter reading is taken because a sample states nothing that reads as a real business's claim.

### Research: sites looked at (2026-11-20, Chrome)

| Site | Result |
| --- | --- |
| apartmentary.com (아파트멘터리, Korea, apartment remodelling brand) | Candidate A |
| studioashby.com (Studio Ashby, London, interior design studio) | Candidate B |
| studio-mcgee.com (Studio McGee, US, design house) | Candidate C |
| yellowplastic.co.kr (옐로플라스틱, Seoul, residential design studio) | Candidate D |
| blockrenovation.com (Block, US, renovation service) | Runner-up. Family photo hero with a large white all-caps sans headline, coral "Get Started" button, How It Works and Budgeting in the nav. Clear estimate flow; a photo-with-headline hero is near `fitness-mideoum`, and its coral sits in the closed hue band. |
| cathiehonginteriors.com (Cathie Hong Interiors, US) | Runner-up. Full-screen photo with a round monogram in the centre and the nav in a brown bar at the bottom of the first screen. The bottom bar is a distinct trait; the rest is a full-bleed photo hero like `clinic-neuru` and `law-goim`. |
| normcph.com (Norm Architects, Copenhagen) | Full-bleed muted photo slider, small spaced caps nav in the centre, caption on the photo. Refined; the same full-bleed type as above and an architecture office more than a home interior business. |
| jhinteriordesign.com (Jessica Helgerson Interior Design, US) | Full-bleed dark wood interior with a four-line spaced wordmark on the photo; mailing-list pop-up and cookie bar on load. Near `flower-bomgyeol`'s dark photo and spaced serif wordmark. |
| heidicaillierdesign.com (Heidi Caillier Design, US) | Full-bleed patterned living room, thin spaced wordmark and nav on the photo, hard to read. |
| kellywearstler.com (Kelly Wearstler, US) | Product-led: a vase close-up and a collection name. A shop and brand site, not a service site. |
| sweeten.com (Sweeten, US, contractor matching) | Kitchen photo slider, serif caps headline, blue CTA, "Our services are free!". A matching platform; template-like. |
| rimdesign.co.kr (림디자인, Korea) | Centred serif wordmark, 전화문의 and BLOG links, boxed photo. Office and commercial work, not homes. |
| lxzin.com (LX Z:IN, Korea, materials brand) | Kitchen photo with brush lettering, 시공사례 · 주방 셀프 견적 · 상담신청 in the nav, floating 견적 and 상담 buttons. A manufacturer portal; shows where Korean sites put 견적 and 상담. |
| remodeling.hanssem.com (한샘, Korea) | Redirected to `store.hanssem.com/interior`, a shopping mall with a discount banner and a floating "무료 견적 상담" button. Excluded as a redirect; promotion-led (AC56). |
| 817designspace.co.kr, dallstyle.com, ggumim.co.kr | Did not load (browser error page). Excluded. `www.apartmentary.com` also failed; the apex domain loads. |

Where Korean visitor actions sit on the sites seen: a 상담 신청 pill at the right of the header plus a floating round 상담
button (Apartmentary); 견적 and 상담신청 in the nav plus floating buttons (LX Z:IN); a floating 견적 상담 button (한샘); a
phone number, a map and an inquiry form on a contact page (Yellow Plastic); 전화문의 and BLOG links beside the wordmark
(림디자인). None of the four candidates shows 카카오톡 or 네이버 지도 on its first screen.

### Candidates shown at G1 (history)

At G1 the human picked A, B and C, and did not pick D (A1). The text below is kept as shown at G1. "Q1", "Q2" and "Q3"
in it are the questions that A1–A3 closed. Where it differs from the per-sample ACs, the ACs hold.

**A. Apartmentary — https://apartmentary.com** (Korea). A bright service-brand page for apartment remodelling.

```
+------------------------------------------------------------+
| Apartmentary     서비스 소개 포트폴리오 스토리 직영점  (상담 신청) |
+------------------------------------------------------------+
| <  (full-width interior photo slider, about 80% of screen)  > |
|              포트폴리오 | 강남 타워팰리스2차 >>               |
+------------------------------------------------------------+
|        1,339±        |      1위        |     31.1          |
|  [★★★★★ review] [★★★★ review] [★★★★★ review]  (card row)    |
|  [photo] 서초 …   [photo] 송파 …   [photo] 강남 …  (3 cards)  |
|                     FAQ  (accordion)                        |
| ## black footer: SPACE BETTERS LIFE | INFO | CONTACT ##     |
+------------------------------------------------------------+
```

- Suits: an apartment remodelling company that sells a managed service (턴키 리모델링) and wants 상담 신청 first.
- Proposed name: 로빈인테리어 (`interior-robininterior`).
- Traits to keep: a white bar header with the wordmark at the left, a centred Korean nav and a dark pill 상담 button at the right; a wide photo slider (or one wide photo) directly under the header with a caption line on it; a three-card photo row; an FAQ accordion.
- We would improve: no figures row and no reviews (AC54, AC58); room and style captions instead of complex names (AC61, AC64); 카카오톡 · 전화 · 네이버 예약 · 네이버 지도 beside 견적 문의 (AC33–AC37); a 견적 · 상담 bar that stays on the phone screen (AC44); a process section before the FAQ (AC31).
- Distance from shipped samples: A is the candidate nearest to them. Its white base is the most crowded zone (`clinic-neuru`, `beauty-robinsalon`, `fitness-mideoum`), and `clinic-neuru` also puts a wide photo under a white band. The distance comes from the parts no shipped sample has: a photo directly under the header with only a caption on it, a three-card photo row, an FAQ accordion and a dark footer; and from a Korean sans that no shipped sample loads. Colour: a green tint would sit near `fitness-jjuuk`, so the direction is a neutral light base with one clear accent, a vermilion near 5° if Q2 drops the hue rule, or the free yellow-green band if it stays.

**B. Studio Ashby — https://www.studioashby.com** (London). A colour-block, type-led studio site.

```
+------------------------------+-----------------------------+
| ## brown block ##            | ## olive block ##           |
|   S T U                      |  FURNITURE & ART    (mark)  |
|     D I O        (giant      |                             |
|   A S H           stacked    |                             |
|       B Y         wordmark)  |   S I S T E R               |
| STUDIO ASHBY                 |   (second brand; photo on hover)
+------------------------------+-----------------------------+
| after entry: two photos side by side, nav over them        |
| ## olive band: studio name + one centred paragraph ##      |
| ## cobalt block: project title, text, button ## | (photo)  |
| [photo][photo][photo][photo]  four project tiles with names|
+------------------------------------------------------------+
```

- Suits: a design studio with a strong point of view (주거 디자인 스튜디오, 홈스타일링) that sells taste more than price.
- Proposed name: 로빈디자인 (`interior-robindesign`).
- Traits to keep: a first screen split into two flat saturated colour blocks with no photo; a giant stacked wordmark that fills one block; a full-width colour band with one centred paragraph; a colour block beside a photo for a featured example; a four-tile photo row.
- We would improve: the reference's first screen is a gate between two brands with no nav and no contact. Ours is one business: the second block holds the Korean headline and the 견적 · 상담 link (AC42) in place of the second brand's name and mark, the sample marker is added (AC8), and the page scrolls on without a gate. So our first screen differs from the screenshot in what the second block says, not in its two-block layout. The wordmark is Hangul. Korean nav, process and contact sections are added.
- Distance from shipped samples: `law-ganeum` has a first screen without a photo, in one graphite colour, and `clinic-bonui` has a split first screen with a photo in one half. No shipped sample has two flat saturated colour blocks or a wordmark that fills half the screen, so the layout itself is the distance. The blocks must not reuse Studio Ashby's brown, orange, olive and cobalt. Under the 25° rule only a yellow-green accent is free, which would decide the block colours for us; see Q2.

**C. Studio McGee — https://studio-mcgee.com** (US). A framed photo on a deep grey-green page with a serif line under it.

```
+------------------------------------------------------------+
| STUDIO McGEE          Read Portfolio About Work With Us  Q | shop |
+------------------------------------------------------------+
| ## deep grey-green page ##                                 |
|  +------------------------------------------------------+  |
|  |        (one wide interior photo, inset, framed       |  |
|  |         by the page colour on all four sides)        |  |
|  +------------------------------------------------------+  |
|        A DESIGN HOUSE ROOTED IN *MODERN TRADITION*         |
+------------------------------------------------------------+
| (wide photo with a left caption block and outline button)  |
| ## warm off-white ## Read / Design & Lifestyle             |
| [photo+title+meta] [photo+title+meta] [photo+title+meta]   |
+------------------------------------------------------------+
```

- Suits: a home styling or classic residential studio (홈스타일링, 주택 · 빌라 리모델링) that wants a calm, magazine-like tone.
- Proposed name: 로빈홈 (`interior-robinhome`).
- Traits to keep: a mid-dark coloured page on the first screen; one wide photo inset with a margin of page colour on all four sides; a one-line serif statement centred under the photo, with one part in a second style; a light section below with a three-column card grid.
- We would improve: the reference's home leads to a shop and a blog, and "Work With Us" is one nav item among five. Ours puts a 견적 · 상담 button in the header and beside the statement (AC42), replaces the blog grid with example photos and the process, and uses a Korean serif headline. Hangul has no italic, so the second style is a weight or colour change, or one Latin word in a real italic.
- Distance from shipped samples: the three dark samples are near-black (`#17130f`, `#1f2226`, a dark photo). A mid-dark coloured page (HSL lightness about 0.25–0.35) in a hue away from the reference's grey-green, for example a deep umber or ink blue, is new. The inset photo framed by a dark page differs from the full-bleed heroes and from `clinic-byeotteul`'s rounded photo on a light page. Accent: an ivory (achromatic) or the free yellow-green band.

**D. Yellow Plastic — https://www.yellowplastic.co.kr** (Seoul). Not picked at G1; kept as a research record. A gallery-quiet studio site: white, one photo, almost no text.

```
+------------------------------------------------------------+
| Y E L L O W   P L A S T I C                             +  |
|                                                            |
|                  +--------------------+                    |
|                  |  (one tall photo,  |                    |
|                  |   centred, about   |                    |
|                  |   a third of the   |                    |
|                  |   width)           |                    |
|                  +--------------------+                    |
+------------------------------------------------------------+
| inner pages: left column  | All Modern Unique              |
|  about us                 | All 20 30 40 50 60             |
|  contact us               | [tall photo]   [tall photo]    |
|  work                     | [tall photo]   [tall photo]    |
|  media                    | contact: map, address, phones, |
|  (address, tel, ©)        |          inquiry form           |
+------------------------------------------------------------+
```

- Suits: a small residential design studio (소규모 주거 디자인 스튜디오) whose photos carry the brand and whose owner wants a quiet site.
- Proposed name: 로빈리빙 (`interior-robinliving`).
- Traits to keep: a white first screen with one tall photo centred and wide empty margins, as in the screenshot; a small letter-spaced wordmark at the top left; a two-column grid of tall photos. From the second screen on, a narrow left column holds the nav and the contact lines on a wide screen (seen on the reference's inner pages and open menu, not in the screenshot).
- We would improve: the reference's first screen has no headline, no nav and no contact until the `+` is pressed, and its contact page is a map, phone numbers and an inquiry form (about nineteen fields, file attachments included, counted from the page's markup). Ours keeps the photo alone in the centre and adds only small text to the first screen: the sample marker (AC8), a one-line Korean headline, and a 견적 · 상담 link where the reference has its `+` (AC42). So our first screen has a few more words than the screenshot. Below it come the left column, example photos, the process, and contact links instead of a form (AC33–AC41). Hangul wordmark and nav.
- Distance from shipped samples: white is crowded, and `beauty-robinsalon` is white with black. That sample is loud (a giant serif word behind a photo); this one is the opposite: small type, one small centred photo, a side column. Accent: achromatic, a grey that is no other entry's accent (AC86), or a pale wood tone if Q2 drops the hue rule.

## Open questions
