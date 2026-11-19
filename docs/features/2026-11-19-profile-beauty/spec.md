---
status: shipped
approved_at: a0ac015bd7e7865ffc24b35c648f9bc56d08fa99
commits: a0ac015bd7e7865ffc24b35c648f9bc56d08fa99..815a77aec309c8f14aa1e304aea13217f4f7631a
---

# Hair-salon franchise profile samples (`beauty`)

## Problem

The `/profile/` gallery has no sample for the `beauty` (미용실) industry. The 미용실 filter chip shows no count, and
the grid shows a "미용실 · 디자인 준비 중" tile. A hair-salon brand owner who opens the gallery finds nothing for their
business, and sales has no beauty sample to show.

`docs/profile-playbook.md` §3 says a `beauty` sample is a franchise head-office (본사) brand site, not one salon. A
visitor must be able to find a branch and then book or contact that branch. An owner-to-be must be able to find the
가맹 문의 path.

A salon franchise site also carries legal and trust risks. The Korean salon franchise sites opened for this spec
show award banners ("미용업계 최초 … 수상"), store counts ("230개 매장 운영"), discount promotions ("전 시술 50% 할인")
and recruitment pop-ups. 가맹사업법 제9조 forbids false or inflated information given to a 가맹희망자, and a fictional
brand has no true figures at all. Salon sites in this run also lean on named stylists and team photos (The Lane, Spoke & Weal's founder band, colorlib's
notes on stylist bios) and on review counts ("4.9★ from 5751 reviews"), and colorlib names before/after galleries as
the usual proof of quality. On a sample, any of these would be fabricated.

## Scope

"Each beauty sample" below means each of the three folders `profile/beauty-robinhair/`, `profile/beauty-robinsalon/`
and `profile/beauty-robinhairsalon/` picked at G1. An AC that says "each beauty sample" holds for all three.

- **In:** Sample A, `profile/beauty-robinhair/`: 로빈헤어, a dark warm photo hero with a centred Korean serif headline and pill buttons; reference Spoke & Weal (AC97–AC119).
- **In:** Sample B, `profile/beauty-robinsalon/`: 로빈살롱, a bold white editorial page with a giant Korean display-serif word behind the hero photo and a style-collection strip; reference 박승철헤어스투디오 (AC120–AC137).
- **In:** Sample C, `profile/beauty-robinhairsalon/`: 로빈헤어살롱, a quiet greige page with letter-spaced navigation and a tall interior photo pair; reference The Lane (AC138–AC153).
- **In:** For each beauty sample: `index.html`, `style.css`, `thumb.jpg`, and photos in `img/` with `img/sources.txt`, built per `docs/profile-playbook.md`.
- **In:** A franchise head-office page for a fictional hair-salon brand: brand and service introduction, 지점 찾기, per-branch 예약 and contact, and 가맹 문의.
- **In:** One `live` entry with `industry: "beauty"` in `PROFILES` in `scripts/profiles.py` for each beauty sample.
- **In:** The regenerated `profile/index.html`, made by `python3 scripts/build.py`.
- **In:** Franchise and advertising content rules (AC42–AC59, AC160–AC164).
- **In:** Improvements over the references for Korean visitors: 지점 찾기 and 예약 reachable on mobile, per-branch 네이버 예약 · 카카오톡 채널 · 전화 · 네이버 지도, and Korean typography (AC26–AC41), plus the per-sample improvements in Assumptions.
- **In:** Distinctness of each beauty sample from the nine shipped samples, from the other beauty samples and from its own reference (AC72–AC81, AC97–AC157).
- **In:** Photo content rules (AC78, AC158, AC159).
- **In:** Reconcile `docs/current_system/` (the sample list in `profile-samples/component.md`) and set `last_reconciled`.
- **Out:** Candidate D (궁서채, 로빈미용실, `beauty-robinmiyongsil`), dropped at G1, and any sample built on it.
- **Out:** A brand-name collision check (Kakao Map, Google, Daum, KFTC) and a `name-check.txt`. The human chose 로빈 + field-word names instead (Assumptions).
- **Out:** Changes to `assets/`, to the gallery part of `scripts/build.py`, to `docs/profile-playbook.md`, and to the nine shipped samples under `profile/`.
- **Out:** Real booking, map, KakaoTalk, phone or franchise-lead integration. Every action links to a `#` placeholder.
- **Out:** Forms of any kind (가맹 상담 신청서, 지점 검색 입력란), chat widgets, member login, a shop or cart, designer booking tied to a booking system, and payment.
- **Out:** Inner pages (branch detail pages, style gallery pages, 가맹 안내 detail page, 정보공개서 download). Each sample is one page.
- **Out:** Self-hosting fonts. Google Fonts and Pretendard on jsDelivr stay allowed.
- **Out:** Samples for other industries.
- **Design:** none. Trigger 1 (crosses a component boundary): no. The change adds data and samples through the existing named interfaces (`PROFILES` item, URL `profile/<slug>/`, `thumb.jpg`), which stay unchanged. Trigger 2 (adds a component): no. Each sample is one more instance of the existing `profile-samples` component. Trigger 3 (alters a named interface): no. The `PROFILES` fields, the URL, the thumbnail contract and the `profile_thumb.py` CLI stay the same, and `img/` with `img/sources.txt` are files inside the self-contained folder that no other component reads. Trigger 4 (internal module boundary): no. A sample is one folder with one page, one stylesheet and its images, and a branch list inside the page is markup, not a module. So `spec.md` + `tasks.md` are enough.

## Acceptance criteria

Folder and registration

- [ ] AC1 Each beauty sample contains `index.html`, `style.css` and `thumb.jpg`.
- [ ] AC2 In each beauty sample, `index.html` and `style.css` reference no local file outside that sample's folder (no `../`, no root-relative `/` path, no `assets/`).
- [ ] AC3 `scripts/profiles.py` has exactly one `PROFILES` entry for each beauty sample's slug, each with `industry` `beauty`, `status` `live` and `demo` `True`, and no `beauty` entry for any other slug.
- [ ] AC4 Each beauty sample's slug matches `beauty-robin` followed by one or more lowercase ASCII letters only.
- [ ] AC5 Each beauty sample's `thumb.jpg` is 1200 px wide with a 16:10 ratio and shows the sample's current 1440×900 first screen.
- [ ] AC6 `python3 scripts/build.py` exits 0.
- [ ] AC7 Compared with `main`, the branch changes no file outside the beauty sample folders, `profile/index.html`, `scripts/profiles.py` and `docs/`, and does not change `docs/profile-playbook.md`.

Sample markers, names and metadata

- [ ] AC8 In each beauty sample, the text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" is visible without scrolling at 1440 px width (browser).
- [ ] AC9 In each beauty sample, the text of AC8 is visible without scrolling at 390 px width (browser).
- [ ] AC10 Each beauty sample's footer contains "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다".
- [ ] AC11 Each beauty sample's footer contains "Website by RobinTech".
- [ ] AC12 Each beauty sample's footer has a "Photos:" credit that names each source used in its `img/sources.txt` (Unsplash, Pexels).
- [ ] AC13 Each beauty sample's `index.html` contains `<meta name="robots" content="noindex">`.
- [ ] AC14 Each beauty sample's `<title>` contains "디자인 샘플".
- [ ] AC15 The `name` of each beauty sample's `PROFILES` entry starts with "로빈".
- [ ] AC16 The accessible name of each beauty sample's header wordmark starts with "로빈".
- [ ] AC17 No two beauty samples share the same `PROFILES` `name`.
- [ ] AC18 In each beauty sample, every address on the page includes "(가상 주소)".
- [ ] AC19 In each beauty sample, every phone number on the page is `02-000-0000`.
- [ ] AC20 In each beauty sample, every 사업자등록번호 on the page is `000-00-00000`.
- [ ] AC21 No beauty sample shows a 정보공개서 등록번호, 가맹사업 등록번호 or other registration number with a digit other than `0`.

Franchise structure

- [ ] AC22 Each beauty sample has a section whose heading contains "지점 찾기" or "매장 찾기".
- [ ] AC23 Each beauty sample's AC22 section lists at least three branches, each named with a place name followed by "점" (for example 연남점), and every entry in that section is such a branch.
- [ ] AC24 Each beauty sample has a section whose heading contains "가맹 문의" or "가맹 안내".
- [ ] AC25 In each beauty sample, the AC22 section comes before the AC24 section in document order.

Korean visitor flow

- [ ] AC26 Each branch entry in each beauty sample has a link whose accessible name contains "네이버 예약", and no link in a branch entry has an accessible name that contains two or more of 네이버 예약, 카카오톡, 전화 and 네이버 지도 (one link per action).
- [ ] AC27 Each branch entry in each beauty sample has a link whose accessible name contains "카카오톡".
- [ ] AC28 Each branch entry in each beauty sample has a link whose accessible name contains "전화".
- [ ] AC29 Each branch entry in each beauty sample has a link whose accessible name contains "네이버 지도".
- [ ] AC30 Each branch entry in each beauty sample shows an address with "(가상 주소)" and the phone number `02-000-0000`.
- [ ] AC31 Each beauty sample's 가맹 section has a 가맹 문의 control whose accessible name contains "가맹".
- [ ] AC32 In each beauty sample, every 네이버 예약, 카카오톡, 전화 and 네이버 지도 control in a branch entry, and every 가맹 문의 control in the 가맹 section, has `href="#"` (in-page navigation links such as a header's 지점 and 가맹 links are not such controls).
- [ ] AC33 Each beauty sample has no `<form>` element.
- [ ] AC34 Each beauty sample has no `<input>`, `<select>` or `<textarea>` element.
- [ ] AC35 In each beauty sample at 1440 px width, a link to the AC22 section (`href="#<id>"` of that section) is visible without scrolling (browser).
- [ ] AC36 In each beauty sample at 390 px width, a link to the AC22 section is visible without scrolling (browser).
- [ ] AC37 In each beauty sample at 390 px width, a link to the AC22 section stays on screen at every scroll position (sticky bar or fixed button) (browser).
- [ ] AC38 In each beauty sample at 390 px width, with the page scrolled to the end, the last text line of the footer is visible and not covered by a fixed or sticky element (browser).
- [ ] AC39 Each branch entry in each beauty sample shows its weekday opening hours as digits.
- [ ] AC40 Each branch entry in each beauty sample shows its closed days.
- [ ] AC41 Each beauty sample's Korean body text uses `word-break: keep-all`.

Franchise and advertising content, each beauty sample

"Page text" below means, in `index.html`: visible text, `<title>`, `meta` description and `og:` content, `aria-label`, `alt` and `title` attributes; in `style.css`: `content:` strings.

- [ ] AC42 Each beauty sample's 가맹 section contains the sentence "가상의 가맹 안내이며 실제 가맹점을 모집하지 않습니다."
- [ ] AC43 The page text of each beauty sample contains none of: 수익률, 순수익, 순이익, 월매출, 연매출, 매출액, 예상 매출, 예상매출, 예상 수익, 예상수익, 투자금 회수, 원금, 손익분기, 대박, 소자본 (modelled on 가맹사업법 제9조, as read for the fitness feature; a fictional brand has no figures, so the sample states none; the word list is sample policy).
- [ ] AC44 The page text of each beauty sample contains no digit followed, with optional spaces, by 호점, 개 지점, 개지점, 개 매장, 개매장, 개점, 곳, 명, 억, 만 or 원, the last three also after 천, 백 or 십; no `₩` or `￦` before a digit, no `KRW` after one, and no number with a thousands comma such as `35,000` (no 가맹점 count and no money figure, service prices included; sample policy).
- [ ] AC45 The page text of each beauty sample contains no digit followed, with optional spaces, by `%`.
- [ ] AC46 The page text of each beauty sample contains none of: 최고, 최초, 최대, 최다, 유일, 독보적, 1위, 1등, No.1 (any case), 넘버원, 업계 선두, 완벽, 보장, 보증, 무조건 (sample policy against superlative and guarantee claims).
- [ ] AC47 The page text of each beauty sample contains none of: 수상, 어워드, Award (any case), 선정, 100대, 공식 인증, 인증 받은 (sample policy: 박승철헤어스투디오's first hero slide is an award banner; a fictional brand has won nothing).
- [ ] AC48 The page text of each beauty sample contains none of: 후기, 리뷰, 별점, 평점, 만족도, ★, 성공 사례, 성공사례, 점주 인터뷰, 고객 인터뷰 (sample policy: no fabricated reviews or owner stories presented as genuine).
- [ ] AC49 The page text of each beauty sample contains none of: 비포, 애프터, Before, After, 전후 사진, 시술 전후 (case-insensitive; sample policy: no before/after result photos, which on a sample would be fabricated).
- [ ] AC50 The page text of each beauty sample contains none of: 치료, 완치, 탈모 개선, 탈모개선, 탈모 예방, 탈모예방, 발모, 육모, 모발 재생, 모발재생, 두피 재생, 처방, 의학, 메디컬, 피부과, 효능, 효과, 탈모, 진단, 염증 (sample policy against hair-loss and scalp-treatment outcome claims; 탈모, 진단 and 염증 keep the copy off the 의료법 제56조① line, which bars anyone but a 의료인 from advertising medical care; no cosmetics- or advertising-law text was read for this list; menu words such as 클리닉, 케어, 두피 케어 stay allowed).
- [ ] AC51 The page text of each beauty sample contains none of: 무료, 공짜, 할인, 이벤트, 선착순, 마감 임박, 프로모션, 쿠폰 (sample policy: no lure offers on a sample).
- [ ] AC52 The page text of each beauty sample contains none of: 가맹점사업자피해보상보험, 피해보상보험, 공제조합 가입, 지급보증, 공제계약, 가맹금 예치 (가맹사업법 제15조의2⑥ bars a 피해보상 표지 for a 가맹본부 that has no such contract, as read for the fitness feature).
- [ ] AC53 The page text of each beauty sample contains none of: 특허, 상표등록, 상표 등록, ®, ™, 저작권 등록, 공정거래위원회, 공정위, 등록 완료 (가맹사업법 시행령 제8조①3 names claiming 지식재산권 the 가맹본부 does not hold as 허위·과장 정보제공, as read for the fitness feature; sample policy).
- [ ] AC54 The page text of each beauty sample contains none of: 원장님, 대표 원장, 대표원장, 수석 디자이너, 스타 디자이너, 경력, 년차, 년 차 (sample policy: no named or ranked staff with career claims).
- [ ] AC55 No beauty sample shows a person's name, whether as a designer, 원장, 점주, founder or customer, and no photo is captioned or labelled with a name or a staff role as if that person works for the brand, or presented as the brand's or a branch's own work or customer (실제 시술, 고객 스타일, 완성한 스타일) (human).
- [ ] AC56 No beauty sample shows a count of 가맹점, 지점, 매장, 고객, 디자이너 or years in business, an amount of 매출, 수익, 창업 비용 or a service price, or an opening timeline in days or months, whether in digits or in words (human; AC44–AC45 catch only digit forms).
- [ ] AC57 No beauty sample shows a testimonial, a quote attributed to a named person, a star rating, a partner, press or product-brand logo, an award, or a before/after pair of photos (human).
- [ ] AC58 No beauty sample makes, in other words or in English, a superlative, guarantee, income or hair-treatment outcome claim of the kinds listed in AC43, AC46 and AC50; an ingredient or safety claim of the kind listed in AC160; a claim of support, waived fees or costs the head office covers (지원, 면제, 무상, 본사 부담); a claim that opening is cheap, easy, fast or stable (소자본, 쉽게 시작, 빠른 오픈, 안정적인 운영); or a 가맹 step that implies a contract on the day of, or right after, 상담 or 정보공개서 (human).
- [ ] AC59 Every e-mail address in each beauty sample's page text or `mailto:` links ends in `@example.com`.

Fonts, numbers and photos, each beauty sample

- [ ] AC60 In each beauty sample, every external stylesheet comes from `fonts.googleapis.com` or from Pretendard on `cdn.jsdelivr.net`; no other external CSS or JS is loaded.
- [ ] AC61 In each beauty sample, `index.html` and `style.css` contain no `http://` or `https://` URL whose host is not `fonts.googleapis.com`, `fonts.gstatic.com` or `cdn.jsdelivr.net`.
- [ ] AC62 In each beauty sample, the digits of opening hours and phone numbers render in a Korean typeface or a monospaced face, never in a proportional Latin face with old-style figures (browser).
- [ ] AC63 In each beauty sample, every web font request succeeds, and the `<h1>`, the header wordmark and the AC120 element render in a loaded web font, not in a fallback or a locally installed copy (browser).
- [ ] AC64 No photo ID recorded in a beauty sample's `img/sources.txt` appears in the `img/sources.txt` of any other sample under `profile/`.
- [ ] AC65 Every image path referenced in a beauty sample's `index.html` and `style.css` (`src`, `srcset`, CSS `url()`) resolves to an existing file inside that sample's `img/`, with the same letter case in every path part (GitHub Pages is case-sensitive).
- [ ] AC66 Every file in each beauty sample's `img/` other than `sources.txt` (dotfiles aside) is a `.jpg` or `.webp` file, and `img/` holds no folder.
- [ ] AC67 No image in a beauty sample's `img/` is wider than 2000 px.
- [ ] AC68 No image file in a beauty sample's `img/` is larger than 500 KB.
- [ ] AC69 The image files in each beauty sample's `img/` total at most 3 MB (`thumb.jpg` is not counted).
- [ ] AC70 Each beauty sample's `img/sources.txt` has exactly one line per image file in its `img/` (dotfiles aside), written `<file> <page URL> <download URL>`; the page URL starts with `https://unsplash.com/photos/` or `https://www.pexels.com/photo/`, or is `-`.
- [ ] AC71 Every download URL in each beauty sample's `img/sources.txt` starts with `https://images.unsplash.com/photo-` or `https://images.pexels.com/photos/`, and no line contains `plus.unsplash.com` or `premium_photo`.

Not the same site

- [ ] AC72 Each beauty sample shares no text, logo, brand name or photo with its own reference site (the URL of its candidate in Assumptions).
- [ ] AC73 Side by side with its own reference site, a person does not read a beauty sample as the same site (human).
- [ ] AC74 Side by side with the nine shipped samples and the other beauty samples, a person does not read a beauty sample as the same design as any of them (human).
- [ ] AC75 Each beauty sample's accent (the last `palette` hex of its `PROFILES` entry) is either achromatic, meaning its largest RGB channel minus its smallest is at most `0x18` (24), or chromatic with an HSL saturation of at least 0.25; an accent that is neither (spread above `0x18` and saturation below 0.25) is not allowed (G1 answer "무채색은 예외").
- [ ] AC76 The HSL hue of each chromatic beauty accent (AC75) is at least 25° away, measured round the colour circle, from the accent hue of every other `PROFILES` entry: `#b8325a` (342°), `#2d43b4` (230°), `#2f6f62` (168°), `#e08a2c` (31°), `#8c5a43` (19°), `#4f93ad` (197°), `#7b3f78` (303°), `#613d8f` (266°), `#2f5e3a` (134°), and every other beauty sample's chromatic accent; an achromatic accent is exempt and is not compared with any hue.
- [ ] AC77 Each beauty sample's `style.css` contains the accent hex of its `PROFILES` entry (case-insensitive).
- [ ] AC78 Each beauty sample's photos show hair or salon scenes (hair, cutting, styling, salon interior, tools), and none shows a recognisable reference-site salon, a logo or branded product lettering (human).
- [ ] AC79 Each beauty sample's `<h1>` text is in Korean (contains at least one Hangul syllable).
- [ ] AC80 No beauty sample's `<h1>` is a translation or close paraphrase of its reference's hero headline (human).
- [ ] AC81 No beauty sample's hero photo is or imitates its reference's hero photo (human).

Accessibility and motion, each beauty sample

- [ ] AC82 Every `<img>` in each beauty sample has a non-empty `alt`.
- [ ] AC83 Each beauty sample has exactly one `<h1>`, and no heading level is skipped.
- [ ] AC84 In each beauty sample under `prefers-reduced-motion: reduce`, at 1440 px and at 390 px, no element runs or declares an animation or transition longer than 0.01 s (browser).

Full-page checks, each beauty sample

- [ ] AC85 At 1440 px width, no beauty sample has horizontal overflow on the full page (browser).
- [ ] AC86 At 390 px width (page inside a `width:390px` iframe), no beauty sample has horizontal overflow on the full page (browser).
- [ ] AC87 A full-page screenshot of each beauty sample at 1440 px shows no overlapping or clipped text, except that in `beauty-robinsalon` the AC120 word may be covered by its photo by design (AC124) (browser, human review).
- [ ] AC88 A full-page screenshot of each beauty sample at 390 px shows no overlapping or clipped text, except that in `beauty-robinsalon` the AC120 word may be covered by its photo by design (AC124) (browser, human review).

Gallery (served by `python3 -m http.server 8000`)

- [ ] AC89 On `/profile/`, the `beauty` filter shows one card per beauty sample (browser).
- [ ] AC90 On `/profile/`, the `beauty` filter shows no "준비 중" tile (browser).
- [ ] AC91 In the generated `profile/index.html`, the `beauty` filter chip shows the number of beauty samples as its count.
- [ ] AC92 Clicking each beauty card opens the preview with that sample loaded in the iframe (browser).
- [ ] AC93 For each beauty card, the preview's desktop and mobile buttons switch the iframe between desktop and mobile width (browser).
- [ ] AC94 For each beauty card, pressing Esc closes the preview (browser).

Reconciliation

- [ ] AC95 The Source line of `docs/current_system/profile-samples/component.md` lists each beauty sample's slug.
- [ ] AC96 `git diff` from the `last_reconciled` commit in `docs/current_system/overview.md` to `HEAD` shows no change outside `docs/`.

Sample A, `profile/beauty-robinhair/` (로빈헤어; reference Spoke & Weal, spokeandweal.com)

- [ ] AC97 At 1440 px, the `beauty-robinhair` first screen has a photo from its `img/` (an `<img>` or a CSS background image) whose rendered box spans the full viewport width (the full-bleed photo hero kept from Spoke & Weal) (browser).
- [ ] AC98 At 1440 px, the bounding box of the `beauty-robinhair` `<h1>` overlaps the rendered box of the AC97 photo (headline set on the photo) (browser).
- [ ] AC99 At 1440 px, the horizontal centre of the `beauty-robinhair` `<h1>` box is within 24 px of the viewport's horizontal centre (centred headline kept) (browser).
- [ ] AC100 The `beauty-robinhair` hero photo, as rendered on the first screen, reads as dark and warm (darkened, with earth, brown or amber tones) and has a person's hair as its subject (the mood kept from Spoke & Weal) (human).
- [ ] AC101 The mean 8-bit greyscale value (ITU-R 601 luma) over all pixels of `beauty-robinhair/thumb.jpg` is below 100 (dark first screen kept; measured 2026-11-19: the dark shipped samples are `flower-bomgyeol` 48.9 and `law-ganeum` 39.1, the others 154.7–232.7).
- [ ] AC102 The `body` background colour declared in `beauty-robinhair/style.css` (custom properties resolved) has an HSL lightness of at most 0.15 (a near-black page, as Spoke & Weal's page and founders band).
- [ ] AC103 That `beauty-robinhair` `body` background colour has a red channel at least `0x04` above its blue channel (warm, not `law-ganeum`'s cool graphite `#1f2226`).
- [ ] AC104 The first family in the computed `font-family` of the `beauty-robinhair` `<h1>` is `Nanum Myeongjo` (a Korean serif headline; no other sample under `profile/` loads it) (browser).
- [ ] AC105 The `beauty-robinhair` `<h1>` contains an `<em>` whose computed `font-style` is `italic` (the upright and italic mix kept from Spoke & Weal's headline) (browser).
- [ ] AC106 The text of the AC105 `<em>` contains at least one Latin letter and no Hangul syllable (Hangul has no true italic, so the italic part is a Latin word).
- [ ] AC107 The `fonts.googleapis.com` URL in `beauty-robinhair/index.html` that loads the first family of the AC105 `<em>`'s computed `font-family` requests that family's italic (`ital` in its `family=` value), so the italic is a real italic, not a synthesised slant.
- [ ] AC108 `beauty-robinhair` loads neither `Instrument Serif` nor `Inter` (Spoke & Weal's faces, read from its home page on 2026-11-19).
- [ ] AC109 `beauty-robinhair` loads none of `Noto Serif KR`, `Cormorant Garamond` (`flower-bomgyeol`), `Hahmlet` (`law-ganeum`) or `Gowun Batang` (`fitness-mideoum`).
- [ ] AC110 `beauty-robinhair/style.css` contains none of `#FAF7F2`, `#0A0A0A`, `#F2EDE3`, `#C2A176` or `#83643A` (case-insensitive; Spoke & Weal's cream, black, greige, tan and bronze, read on 2026-11-19).
- [ ] AC111 The `beauty-robinhair` accent is chromatic in the sense of AC75 (its largest RGB channel minus its smallest is above `0x18`).
- [ ] AC112 The 네이버 예약 control of each branch entry in `beauty-robinhair` has a computed `border-radius` of at least half its rendered height (pill buttons kept from Spoke & Weal) (browser).
- [ ] AC113 At 1440 px, the `beauty-robinhair` first screen shows, outside the `<header>` and outside any fixed or sticky bar, a link whose `href` is `#<id>` of the 지점 찾기 section and whose text contains "지점" and "예약" (Spoke & Weal's "SCHEDULE ONLINE" leaves the site; this one goes to the branch list on the page) (browser).
- [ ] AC114 At 1440 px, the `beauty-robinhair` header shows a visible link whose text contains "지점" (Spoke & Weal hides its locations behind a menu icon) (browser).
- [ ] AC115 At 1440 px, the `beauty-robinhair` header shows a visible link whose text contains "가맹" (browser).
- [ ] AC116 The accessible name of the `beauty-robinhair` header wordmark contains no Latin letter (Spoke & Weal's wordmark is the Latin "SPOKE &WEAL").
- [ ] AC117 The `beauty-robinhair` hero photo neither is nor imitates a photo on spokeandweal.com: in particular it is not a woman with short dark hair in a white shirt standing in a dry grass field with pale fabric blowing behind her (its home hero, seen on 2026-11-19) (human).
- [ ] AC118 At 1440 px, no element in `beauty-robinhair` whose own text contains a digit has a computed `font-size` above 24 px (no figures row like Spoke & Weal's "9 CITIES"; AC44 and AC56 ban the content, this bans the device) (browser).
- [ ] AC119 No `<img>` in `beauty-robinhair` has a computed `border-radius` of at least half its rendered width (no circular portrait like Spoke & Weal's founders band) (browser).

Sample B, `profile/beauty-robinsalon/` (로빈살롱; reference 박승철헤어스투디오, pschair.co.kr)

- [ ] AC120 At 1440 px, the `beauty-robinsalon` first screen shows a text element whose computed `font-size` is at least 160 px (the giant display word kept from 박승철헤어스투디오's hero) (browser).
- [ ] AC121 The text of the AC120 element contains at least one Hangul syllable and no Latin letter (not "STAGE" or any other English word).
- [ ] AC122 The first family in the computed `font-family` of the AC120 element is `Song Myung` (a Korean display serif; no other sample under `profile/` loads it) (browser).
- [ ] AC123 The AC120 element is live page text, and at 1440 px its bounding box overlaps the rendered box of a photo from the sample's `img/` (the word set behind the hero photo, never lettering inside an image) (browser).
- [ ] AC124 At 1440 px, at the centre of the overlap of AC123, `document.elementsFromPoint` lists the photo before the AC120 element (the photo is painted in front of the word) (browser).
- [ ] AC125 No photo in `beauty-robinsalon` shows a brick wall or lettering painted on a wall (박승철헤어스투디오's brick backdrop with "STAGE") (human).
- [ ] AC126 The `beauty-robinsalon` hero photo neither is nor imitates a photo on pschair.co.kr: in particular it is not a row of four long-haired women standing before a wall (its "My Stage" slide, seen on 2026-11-19) (human).
- [ ] AC127 `beauty-robinsalon` has a section whose heading contains "스타일" with at least four cards, each containing an `<img>` from the sample's `img/` (the style-collection strip kept from "hair trend Collection").
- [ ] AC128 Each card of the AC127 section shows a style name that contains at least one Hangul syllable.
- [ ] AC129 At 1440 px, the top edges of the visible AC127 cards lie within 4 px of each other (one horizontal strip) (browser).
- [ ] AC130 No AC127 style name is a translation or transliteration of 박승철헤어스투디오's look names "Noir sleek", "Scuro signature", "Rêve layer" or "Marie wave" (human).
- [ ] AC131 The text of every link in the `beauty-robinsalon` header navigation contains at least one Hangul syllable and no Latin letter (박승철헤어스투디오's navigation is English: About, Salon, Style, Franchise …).
- [ ] AC132 At 1440 px, the `beauty-robinsalon` header shows a visible link whose text contains "지점" (browser).
- [ ] AC133 At 1440 px, the `beauty-robinsalon` header shows a visible link whose text contains "가맹" (browser).
- [ ] AC134 The accessible name of the `beauty-robinsalon` header wordmark contains no Latin letter (박승철헤어스투디오's wordmark is the Latin "PARK SEUNG CHOL / HAIR-STUDIO").
- [ ] AC135 `beauty-robinsalon` loads no `Roboto` (박승철헤어스투디오's text face, read on 2026-11-19).
- [ ] AC136 `beauty-robinsalon/style.css` contains none of `#635595`, `#5F518E` or `#686199` (case-insensitive; 박승철헤어스투디오's purples, read on 2026-11-19).
- [ ] AC137 Every RGB channel of the `body` background colour declared in `beauty-robinsalon/style.css` (custom properties resolved) is at least `0xF8`, and its largest channel minus its smallest is at most `0x04` (a neutral white editorial page).

Sample C, `profile/beauty-robinhairsalon/` (로빈헤어살롱; reference The Lane, thelanesalon.com)

- [ ] AC138 Every RGB channel of the `body` background colour declared in `beauty-robinhairsalon/style.css` (custom properties resolved) is from `0xDC` to `0xF2` inclusive (the light greige base kept from The Lane).
- [ ] AC139 That `beauty-robinhairsalon` `body` background colour has a red channel from `0x04` to `0x14` inclusive above its blue channel (greige: `law-goim`'s stone `#e4e5e6` is cool, `food-saebyeokmil`'s `#f4efe5` is above `0xF2`).
- [ ] AC140 At 1440 px, every link in the `beauty-robinhairsalon` header navigation has a computed `letter-spacing` of at least 0.1 times its computed `font-size` (the spaced navigation kept from The Lane; Hangul has no capitals, so spacing carries the trait) (browser).
- [ ] AC141 The text of every link in the `beauty-robinhairsalon` header navigation contains at least one Hangul syllable and no Latin letter (The Lane's navigation is English caps).
- [ ] AC142 At 1440 px, the `beauty-robinhairsalon` header shows a visible link whose text contains "지점" (browser).
- [ ] AC143 At 1440 px, the `beauty-robinhairsalon` header shows a visible link whose text contains "가맹" (browser).
- [ ] AC144 At 1440 px, the `beauty-robinhairsalon` first screen shows two `<img>` from its `img/` side by side, each rendered at least 1.4 times as tall as it is wide, with top edges within 8 px of each other and boxes that do not overlap (the tall photo pair kept from The Lane) (browser).
- [ ] AC145 The two AC144 photos show salon interiors or hair scenes in soft daylight (human).
- [ ] AC146 Neither AC144 photo is or imitates a photo on thelanesalon.com: in particular neither is a black salon chair before a mirror with palm fronds, nor books and magazines on a table beside a plant (its home hero, seen on 2026-11-19) (human).
- [ ] AC147 At 1440 px, the bounding box of the `beauty-robinhairsalon` `<h1>` overlaps neither AC144 photo (headline beside the pair, unlike A's headline on its photo) (browser).
- [ ] AC148 The first family in the computed `font-family` of the `<h1>` and of every `<h2>` in `beauty-robinhairsalon` is `Nanum Gothic` or `Sunflower` (a quiet Korean sans; no other sample under `profile/` loads either) (browser).
- [ ] AC149 The accessible name of the `beauty-robinhairsalon` header wordmark contains no Latin letter (The Lane's wordmark is the Latin "THE LANE | SF").
- [ ] AC150 The `beauty-robinhairsalon` wordmark has no vertical rule followed by stacked letters (The Lane's "| S F" device) (human).
- [ ] AC151 `beauty-robinhairsalon/style.css` contains none of `#5D564B`, `#837E73`, `#F4F3F2` or `#754E36` (case-insensitive; The Lane's taupe bar, grey, off-white and brown, read on 2026-11-19).
- [ ] AC152 At 1440 px, the `beauty-robinhairsalon` first screen shows, outside the `<header>` and outside any fixed or sticky bar, a link whose `href` is `#<id>` of the 지점 찾기 section and whose text contains "지점" (The Lane's first screen offers only BOOK NOW and SERVICES) (browser).
- [ ] AC153 The mean ITU-R 601 luma of `beauty-robinhairsalon/thumb.jpg` is at least 100 (light first screen, unlike A).

All three beauty samples

- [ ] AC154 The first families in the computed `font-family` of the three beauty samples' `<h1>`s are pairwise different (browser).
- [ ] AC155 The first families in the computed `font-family` of the three beauty samples' header wordmarks are pairwise different (browser).
- [ ] AC156 Side by side, the three header wordmarks read as three different marks, in face and in layout, so 로빈헤어 and 로빈헤어살롱 do not read as one mark with a suffix added (human).
- [ ] AC157 No hex appears in the `palette` of more than one beauty sample's `PROFILES` entry (case-insensitive; keeps the gallery colour chips apart when two accents are achromatic).
- [ ] AC158 A reviewer opens every image file in each beauty sample's `img/` one by one at native resolution (100 % zoom, not on the page or a contact sheet) and finds no legible brand name, logo, product label, sticker, signage, book or magazine title, or other lettering, on bottles, tubes, mirrors, capes, aprons, tools, packaging, walls or anywhere else (human; the fitness verdict failed once on lettering seen only at full size).
- [ ] AC159 No `alt` attribute in any beauty sample contains 디자이너, 원장, 스타일리스트, 직원, 점주, 대표 원장, 대표원장, 우리 팀, 미용사 or 실장 (people in the photos are stock models, never presented as the brand's staff).
- [ ] AC160 The page text of each beauty sample contains none of: 천연, 유기농, 무독성, 무자극, 저자극, 무암모니아, 암모니아 없, 무손상, 손상 없, 친환경, 무첨가 (sample policy: a fictional brand has no product facts behind an ingredient or safety claim; 표시광고법 제3조 bars false or exaggerated claims; the act was not read for this list).
- [ ] AC161 No beauty sample names a real product, tool, booking or salon brand other than 네이버 and 카카오톡: its page text contains none of K18, 올라플렉스, Olaplex, 밀본, Milbon, 로레알, L'Oreal, L'Oréal, 웰라, Wella, 아베다, Aveda, 다이슨, Dyson, 케라스타즈, Kerastase, Kérastase, 슈바르츠코프, Schwarzkopf, 아모스 or 미쟝센 (any case), and a person finds no other such name (human for the second part; a named brand reads as a partnership the sample does not have).
- [ ] AC162 At 1440 px and at 390 px, a person reads the AC8 text and the AC42 sentence at body-text size or larger, in a colour that stands out clearly from its background (human).
- [ ] AC163 Every address in each beauty sample names a district or road that does not exist (for example 가상구 결로), so no address points to a real building (human; playbook §2 bars real addresses, and "(가상 주소)" alone does not stop one).
- [ ] AC164 The page text of each beauty sample holds no social-media handle (`@` followed by a name, outside an `@example.com` e-mail address) and no domain name other than `example.com` (no `robinhair.co.kr`; a real account or site with that name may exist).

Every AC above is checked by a `tasks.md` verify (command, browser or human); there is no feature `verify.md`; `docs/verify.md` applies.

## Assumptions

- The industry key is `beauty` with the label 미용실; it already exists in `INDUSTRIES` in `scripts/profiles.py`, and no `PROFILES` entry uses it yet (checked 2026-11-19).
- **Naming (human decision, binding).** The human chose not to invent fictional brand names. Each sample's name is "로빈" plus a hair or salon word, so the name alone shows it is a sample. The human accepted that a real salon with the same name may exist, because it is a sample. So this feature runs no name-collision check and writes no `name-check.txt`. AC15–AC17 and AC4 check the naming. The other parts of playbook §2 still hold: the business is fictional, every address is "(가상 주소)", the phone is `02-000-0000`, the 사업자번호 is `000-00-00000`, and the marker text is unchanged (AC8–AC10, AC18–AC21).
- **G1 decision (human, Seokhyun Kim, 2026-11-19):** build three samples in this feature, under the proposed names unchanged: A Spoke & Weal → 로빈헤어 `beauty-robinhair`; B 박승철헤어스투디오 → 로빈살롱 `beauty-robinsalon`; C The Lane → 로빈헤어살롱 `beauty-robinhairsalon`. D 궁서채 (proposed 로빈미용실 `beauty-robinmiyongsil`) is out. This closes Q1. English words in the slugs (hair, salon) follow the human's example `beauty-robinhair`. 로빈헤어 and 로빈헤어살롱 share a prefix; AC155 and AC156 keep their wordmarks visibly different.
- **Q2 decision (human, at G1): "무채색은 예외".** An achromatic accent is exempt from the 25° hue rule; a chromatic accent keeps it, against the nine shipped accents and against each other beauty sample's chromatic accent (AC75, AC76). Distinctness for an achromatic sample comes from photos, typefaces and layout. This closes Q2.
- **Achromatic threshold (agent decision).** "Achromatic" is an RGB channel spread (largest channel minus smallest) of at most `0x18` (24 of 255), not an HSL saturation floor. HSL saturation inflates near white and black: cream `#faf7f2` computes 0.44 and warm near-black `#14110e` 0.18, though both read as neutral, while greige `#9a9284` (spread 22, saturation 0.10) and The Lane's taupe `#5d564b` (spread 18) read as greige. A chromatic accent (spread above `0x18`) still needs HSL saturation 0.25 or more, so the muddy zone between the two is banned (AC75). Planned: A chromatic, a brass or olive in the free band of about 56°–109°; B achromatic, a near-black ink; C achromatic, a greige. The hexes are fixed in `tasks.md`; AC157 stops two achromatic samples from sharing a chip.
- **Orchestrator decisions (2026-11-19, stated as decided).** Per-sample AC blocks are numbered on from AC97, as fitness did; each keeps the trait the human picked (A: dark warm photo hero, centred serif headline mixing upright and italic, pill buttons; B: bold editorial with a large display-serif word behind the hero photo and a style-collection strip; C: quiet greige, spaced navigation, tall interior photo pair), states its palette and type direction and its improvements for Korean visitors, and bans what would copy the reference (layout grid one-to-one, text, logo, photos; B gets no brick wall and no "STAGE"-like English word). The three samples must differ from each other (AC154–AC157, and the mutually exclusive body backgrounds of AC102, AC137 and AC138). A photo-lettering check at full resolution (AC158) and a staff-word ban in `alt` text (AC159) answer the fitness verdict that failed once on lettering in a photo; the named-staff ban (AC54, AC55) stays.
- **Translating Latin type traits to Hangul (agent decisions).** AC79 needs a Korean `<h1>`, and Hangul has neither italic nor capitals. A keeps the upright and italic mix with one Latin word in a real italic inside the Korean headline (AC105–AC107). C keeps the spaced caps navigation as Korean links with letter-spacing of at least 0.1 em (AC140). B keeps the giant word as live Korean text in a display serif, set behind the photo (AC120–AC124), never as lettering inside an image (AC158). AC120–AC124 are checked at 1440 px only; at 390 px the word may shrink, move above the photo or be hidden, left to design, as long as AC86 and AC88 hold.
- **Typeface picks (agent decisions).** A `<h1>` `Nanum Myeongjo` (AC104), B's giant word `Song Myung` (AC122), C's headings `Nanum Gothic` or `Sunflower` (AC148). On 2026-11-19 `fonts.googleapis.com` served each with Hangul (Nanum Myeongjo 400/700/800, Song Myung 400, Nanum Gothic 400/700, Sunflower 300/500/700), and no sample under `profile/` loads any of them (`flower-bomgyeol/style.css` names `Nanum Myeongjo` only as an unloaded fallback after `Noto Serif KR`). Pretendard is loaded by every shipped sample, so no AC uses it to tell samples apart. A's italic Latin word needs a Google serif with an italic style (for example Fraunces or Newsreader, both served with `ital` on 2026-11-19), not Instrument Serif (AC108) or Cormorant Garamond (AC109).
- **Reference fonts and colours (read 2026-11-19, Chrome, computed styles of the home pages).** Spoke & Weal: `Instrument Serif` and `Inter`; `#0A0A0A` body, `#FAF7F2`, `#F2EDE3`, `#C2A176`, `#83643A`. 박승철헤어스투디오: `Roboto` text (the wordmark and "STAGE" are images); purples `#635595`, `#5F518E`, `#686199`; white body. The Lane: three Wix-hosted faces whose names are hashes (`wfont_…`) and Arial, so C has no "does not load" AC for its reference faces; `#5D564B` top bar, `#837E73`, `#F4F3F2`, `#754E36`; its greige page is a background image, not a declared colour.
- **Content adaptations from the fitness spec (agent decisions).**
  - **No prices.** AC44 bans money figures, so the service menu names services without prices. Salon franchise prices differ by branch, so a line such as "시술 가격은 지점마다 다릅니다" points to the branch's 네이버 예약.
  - **No named staff.** AC54 and AC55 ban named staff. The orchestrator suggested named designers labelled as fictional. The agent chose to ban names outright, because a fictional name and bio on a polished page still reads as a real person, and a career year would be a fabricated figure (AC56).
  - **Outcome claims.** Fitness AC88 (체형교정, 교정, 회복, 예방…) is not carried over, because 교정 and 회복 are ordinary salon menu words (매직 교정, 손상 회복 케어). AC50 targets hair-loss and scalp-treatment claims instead.
  - **Awards and before/after.** AC47 (awards) and AC49 (before/after) are new. They answer patterns seen in this run: 박승철헤어스투디오's award slide, and colorlib's note that salon sites lean on before/after galleries.
- **Law reading.** The 가맹사업법 reading (제9조, 제15조의2⑥, 시행령 제8조) is the one the fitness feature recorded in its spec Assumptions on 2026-11-18/19. No statute was read again in this run. Every other content ban here (AC46–AC51, AC54) is sample policy, and no medical, cosmetics or advertising-law text was read for it.
- **지점 찾기 shape (agent decision):** a static list of three to six fictional branches, optionally grouped by region with in-page anchors. It has no search box and no map embed (AC33, AC34, AC61). A region filter driven by buttons and JS is allowed if it needs no `<input>`.
- **가맹 문의 shape (agent decision):** 가맹 문의 links (가맹 상담 전화, 가맹 카카오톡 상담) go to `#`. There is no form, and no e-mail address outside `@example.com` (AC59). The section may describe the 가맹 process in steps (상담 → 정보공개서 제공 → 계약) without days, months or money (AC44, AC56).
- **Accent-hue room.** AC76 keeps the 25° rule for chromatic accents against the nine shipped accents (hues computed 2026-11-19 from `scripts/profiles.py`). Only one band is free: about 56°–109° (yellow, olive, yellow-green). The band between aubergine 303° and raspberry 342° is closed (328° > 317°). With only A chromatic as planned, A sits in that band; B's purple is not kept (AC136), and B and C go achromatic under the Q2 answer.
- Photos: free Unsplash or Pexels photos of hair, cutting, styling and salon interiors. They are compared on a contact sheet in the implement stage and downloaded at web size into `img/`.
- Mood targets, against the shipped samples (from `scripts/profiles.py` and their specs):
  - `flower-bomgyeol`: dark photo hero, centred spaced serif wordmark, raspberry `#b8325a`.
  - `food-saebyeokmil`: paper cream, IBM Plex Mono, dawn blue.
  - `clinic-neuru`: white, light full-bleed interior photo, pine.
  - `clinic-byeotteul`: cool white, rounded cards, orange.
  - `clinic-bonui`: warm off-white, split hero, thin Noto Sans KR, chestnut.
  - `law-ganeum`: dark solid graphite page, Korean serif, steel blue.
  - `law-goim`: stone grey, full-bleed stone-wall photo, aubergine.
  - `fitness-mideoum`: white, warm daylight full-bleed photo with a serif headline on it, Korean serif headings, purple `#613d8f`.
  - `fitness-jjuuk`: warm cream, deep-green band, retro display wordmark, pill buttons.
- §6-1 check: `git diff --stat 9d8f7e2..HEAD` (the `last_reconciled` in `overview.md`) lists three files: `docs/current_system/overview.md` (the `last_reconciled` line) and the fitness feature's `spec.md` and `tasks.md` (SHA re-pointing in its docs commit). None is system code, and none changes a component, an interface or the `profile-samples` sample list, so `current_system/` still describes the system.
- Mobile behaviour of the reference sites was not checked. Mobile points are targets, not defects found in the references.
- Only the home pages were opened: first screen plus two scrolls for A, B and D, one scroll for C. After G1, the home pages of A, B and C were opened again to read their fonts and colours (the "Reference fonts and colours" item above).
- **Distinctness rule for this spec (lesson from the law run).** No AC forbids the trait the human picked. A keeps a full-bleed dark warm photo hero (AC97, AC100, AC101) with a centred serif headline on it (AC98, AC99, AC104) mixing upright and italic (AC105–AC107) and pill buttons (AC112). B keeps the giant display-serif word behind the hero photo (AC120–AC124) and a style strip (AC127–AC129). C keeps a greige base (AC138, AC139), spaced navigation (AC140) and a tall photo pair (AC144, AC145). The candidate note on A below ("A would need a light first screen or a non-serif headline") is superseded by G1: A's distance from `flower-bomgyeol` and `fitness-mideoum` comes from typeface, photo subject, wordmark, pills and accent instead.
- **Distinctness map (pair → ACs).** AC73 and AC74 are the human backstop for every pair.
  - A vs Spoke & Weal: Hangul wordmark (AC116); none of its faces (AC108) or colours (AC110); not its field-and-fabric hero (AC117); no figures row (AC118, AC44, AC56) and no circular founder portrait (AC119, AC55); not a paraphrase of "A full service hair salon." (AC80).
  - B vs 박승철헤어스투디오: Korean word in Song Myung, not "STAGE" (AC121, AC122); no brick wall or painted lettering (AC125); not its four-model slide (AC126); Korean style names, not its look names (AC128, AC130); Korean navigation (AC131); Hangul wordmark (AC134); no Roboto (AC135) or purple (AC136); no award, store count or grand-open strip (AC44, AC47, AC56).
  - C vs The Lane: Hangul wordmark (AC149) without the "| S F" device (AC150); Korean navigation (AC141); none of its colours (AC151); not its chair-and-palm or books photos (AC146); a Korean `<h1>` beside the photos (AC79, AC147); a franchise layer it does not have (AC22, AC24).
  - A vs `flower-bomgyeol` (dark photo hero, Noto Serif KR, Cormorant, raspberry): Nanum Myeongjo with a Latin italic word (AC104–AC107); none of flower's faces (AC109); a brass or olive accent at least 25° from raspberry (AC76, AC111); hair, not blooms (AC100, AC78); pill buttons (AC112).
  - A vs `law-ganeum` (dark graphite page, Hahmlet, steel blue): warm, not cool, near-black (AC103); photo hero (AC97); no Hahmlet (AC109).
  - A vs `fitness-mideoum` (white, warm daylight photo with a serif headline on it, Gowun Batang): dark page and first screen (AC101, AC102); no Gowun Batang (AC109).
  - B vs `clinic-neuru`, `clinic-byeotteul`, `fitness-mideoum` (white or near-white bases): giant Korean display word over a photo (AC120–AC124); style strip (AC127); achromatic ink accent with no shared chip (AC157).
  - C vs `clinic-bonui` (warm off-white `#fbf9f7`, Noto Sans KR): greige at or below `0xF2` (AC138); Nanum Gothic or Sunflower, not Noto Sans KR (AC148); tall photo pair (AC144).
  - C vs `law-goim` (cool stone `#e4e5e6`, stone-wall photo, IBM Plex Sans KR): warm greige (AC139); interior photo pair, not a wall (AC144, AC145); AC148 faces.
  - C vs `food-saebyeokmil` (cream `#f4efe5`, IBM Plex Mono): darker, greyer base (AC138); AC148 faces.
  - A vs B vs C: near-black warm vs neutral white vs greige bodies (AC102, AC137, AC138 cannot all hold for one colour); photo hero with headline on it vs giant word behind photo vs headline beside a photo pair (AC98, AC123, AC147); pairwise different `<h1>` and wordmark faces (AC154, AC155); visibly different wordmarks (AC156); no shared palette hex (AC157); no shared photo (AC64).
- **Improvements over the references (playbook §1-4).** All three: per-branch 네이버 예약 · 카카오톡 · 전화 · 네이버 지도 with hours and closed days (AC26–AC30, AC39, AC40), a 지점 찾기 link that stays on the mobile screen (AC37), Korean typography (AC41, AC62), and 가맹 copy modelled on 가맹사업법 제9조 (AC42–AC53). A: Spoke & Weal hides its salons behind a menu icon and sends "SCHEDULE ONLINE" off-site; 로빈헤어 puts 지점 and 가맹 in the header (AC114, AC115) and a hero CTA to the branch list (AC113), and drops the figures row and founder band (AC118, AC119). B: 박승철헤어스투디오's navigation is English and its hero rotates an award slide; 로빈살롱 has Korean navigation with 지점 and 가맹 (AC131–AC133), Korean style names (AC128), and no award or store count (AC47, AC44). C: The Lane is one salon with English caps navigation; 로빈헤어살롱 adds 지점 찾기 and 가맹 (AC22, AC24, AC142, AC143), a Korean headline (AC79), and a hero CTA to the branch list (AC152).

### Research: sites looked at (2026-11-19, Chrome)

| Site | Result |
| --- | --- |
| spokeandweal.com (Spoke & Weal, US, "10 salons across 9 cities") | Candidate A |
| pschair.co.kr (박승철헤어스투디오, Korean franchise) | Candidate B |
| thelanesalon.com (The Lane, San Francisco, one salon) | Candidate C |
| gungseochae.com (궁서채, Korean franchise) | Candidate D |
| crowsnestbarbershop.com (Crowsnest, multi-shop barbershop, Canada) | Runner-up. Blurred barbershop-through-window photo, retro mustard badge lettering ("FINEST QUALITY / CROWSNEST / BARBERSHOP") with stars, Shops in nav, mustard Book Now. Strong character; a men's cut brand rather than a 미용실, and its dark photo first screen is near `flower-bomgyeol` and `law-ganeum`. |
| junohair.com (준오헤어, Korean franchise) | Splash page with three dark tiles (juno hair, JUNO ACADEMY, Avenue JUNO); the juno hair page opens on a pink "수험생 프로모션 · 전 시술 50% 할인" slide. Promotion-led (AC45, AC51 forbid) |
| blueclub.co.kr (블루클럽, Korean men's franchise) | A "2026 GRAND OPEN" poster grid of branch dates over the first screen, and a recruitment ad. Cluttered |
| soonsoofamily.com (순수, Korean franchise) | Black-and-white photo slider of a stage cutting show, Korean nav (매장정보, 가맹안내, 아카데미). Little structure on the first screen |
| salonsck.com (Salon SCK, New York) | Dark page, a close-up portrait with a centred serif name, teal buttons. Template feel |
| toniandguy.com (TONI&GUY World) | Product shop with a sale banner and a cookie wall |
| drybar.com (Drybar, US chain) | Product shop with a "30% off" banner and a consent dialog |
| hershesons.com (Hershesons, London) | Product shop led by a "4.9★ from 5751 reviews" bar; Stores and Book Now in nav |
| headmasters.com (Headmasters, UK chain) | "50% OFF HAIR COLOUR SALE" hero (AC45, AC51) |
| jetrhys.com (Jet Rhys, San Diego) | Black-and-white video, condensed caps "CUT + COLOR", script "we welcome walk ins", chat widget |
| igkhair.com (IGK) | Product shop, holographic gift-edit hero, cookie panel |
| andylecompte.com (Andy LeCompte, LA) | Celebrity photo collage with a big caps name. Celebrity-led |
| grandnoirsalon.com (Grand Noir, Wisconsin) | Booking-rules modal over the page on load |
| rossanoferretti.com (Rossano Ferretti) | Product shop with a country-picker modal |
| taylortaylorlondon.com (Taylor Taylor, London) | Darkened baroque salon-interior photo, Book Now. Dark |
| butterflystudiosalon.com | Excluded: "We are under construction" page |
| chahong.co.kr (차홍) | Excluded: the domain now shows a Coupang Partners ad page |
| ivyandmane.com | Excluded: GoDaddy parked-domain page (URL guessed, not a verified brand domain) |
| hareandbone.com, idhair.co.kr, parkseungchul.com, zeohair.co.kr, xeohair.com | Excluded: browser error page (hareandbone.com from the colorlib list; the others guessed or from a Google result, not verified) |
| junohair.com/avenuejuno | Not counted: did not render |

Nineteen salon sites rendered and were looked at in the browser (the excluded rows aside). Site names came from the colorlib.com "33 Best Hair Salon
Website Examples 2026" list (read), a Google search for Korean 미용실 프랜차이즈 가맹문의 매장찾기 sites, a Google search for
블루클럽 · 리안헤어 · 박승철헤어스투디오, and known brands. A Mobbin section search ("hair salon website hero section")
returned booking-software and agency sites only, and nothing was used from it. 리안헤어 and 이철헤어커커 home pages were not
found in this run.

Screenshots for G1 were taken in a session scratchpad and are not kept; the candidate text and sketches above are the record. They were:
`A-spokeandweal-first.jpg` (Chrome window, 1440 × 779, after the loader; the site's cookie panel shows at lower left
and no consent was given), `B-pschair-first.jpg` (Chrome window, 1440 × 779, slide "26 Hair Design Look : My Stage"),
`B-pschair-first-awardslide.png` (headless Chrome, 1440 × 900, the award slide that also rotates in the hero),
`C-thelane-first.png` and `D-gungseochae-first.png` (headless Chrome, 1440 × 900).

### Candidates shown at G1 (history)

Kept as shown to the human. G1 picked A, B and C and dropped D; the "Distance" notes are superseded by the Distinctness rule above.

**A. Spoke & Weal — https://spokeandweal.com**
A US salon group ("10 salons across 9 cities"). It opens on a black loader with a thin wordmark and an "EST. 2013" counter.
The first screen is a full-bleed, muted earth-tone photo (a woman with short dark hair in a dry field, drapes moving),
darkened. On it sit a centred thin stacked wordmark, a small spaced "10 SALONS ACROSS 9 CITIES" line and a large serif
headline that mixes upright and italic ("A *full service* hair salon."). Below are a spaced service list, a cream
"SCHEDULE ONLINE" pill and an outlined "SEE THE MENU" pill. Below the fold: a warm greige page with a big serif statement
mixing upright and italic, a figures row ("9 CITIES", "K18 REPAIR"), and a black founders band with a circular portrait.
Suits a calm, premium multi-city brand.

```
+----------------------------------------------------------+
| =                     SPOKE&WEAL          (SCHEDULE NOW) |
|        (full-bleed muted earth-tone photo, darkened)     |
|               10 SALONS ACROSS 9 CITIES                  |
|            A *full service* hair salon.   (serif)        |
|      CUSTOM COLOR · DRY HAIRCUTS · KERATIN · ...         |
|          (SCHEDULE ONLINE)   ( SEE THE MENU )            |
+----------------------------------------------------------+
| greige: BIG serif statement w/ italic   | small para     |
|  [ 9 CITIES ]   [ K18 REPAIR ]   <- figures row          |
| ##### black founders band, circular portrait #####       |
+----------------------------------------------------------+
```

Proposed name: 로빈헤어 (`beauty-robinhair`). We would improve: a 지점 찾기 list on the page instead of a hidden menu,
per-branch 네이버 예약 · 카카오톡 · 전화 · 네이버 지도, Korean headline typography, and no figures row (AC44, AC56) or
founder portrait (AC55). Franchise fit: the multi-city line and the menu give a location entry, but no franchise entry was
seen, so 가맹 would be new design. Distance: the darkened photo with a centred serif headline is near `flower-bomgyeol`'s
dark hero and `fitness-mideoum`'s headline-on-photo. A would need a light first screen or a non-serif headline, plus a
hue in the free band, for example a muted olive.

**B. 박승철헤어스투디오 — https://www.pschair.co.kr**
A Korean salon franchise. The white header has a spaced Latin serif wordmark ("PARK SEUNG CHOL / HAIR-STUDIO") and English
nav (About, Salon, Style, Customer, News, Franchise, Academy). A thin left rail holds a menu icon, search and social icons.
The hero is an inset photo slider. One slide shows four models in front of a grey brick wall, with giant pale serif
letters "STAGE" painted large behind them and a caption rule ("26 Hair Design Look : My Stage — Noir sleek | Scuro signature | Rêve layer
| Marie wave"). Other slides are an award banner ("미용업계 최초 14회 수상") and an academy recruitment slide. Below the fold:
a "hair trend Collection" carousel of style cards, a hand-on-hair video band, and a store strip ("230개 매장 운영", "GRAND
OPEN STORE" cards with branch names and phone numbers). Suits a fashion-led brand that sells seasonal looks.

```
+----------------------------------------------------------+
| =  PARK SEUNG CHOL          About Salon Style ... Franchise|
| |  HAIR-STUDIO                                           |
| | [ inset photo: models + giant serif "STAGE" letters ]  |
|(o)[ 26 Hair Design Look ------ Noir | Scuro | Reve ... ] |
+----------------------------------------------------------+
| hair trend / Collection   [style card][style card][>]    |
| ######## video band: hand in hair, View More ########    |
| 000개 매장 운영 [photo]  | GRAND OPEN STORE [card][card][card]|
+----------------------------------------------------------+
```

Proposed name: 로빈살롱 (`beauty-robinsalon`). We would improve: named seasonal style looks kept, but the award, store
count and grand-open strip dropped (AC44, AC47, AC56); Korean nav with 지점 찾기 and 가맹 in place of English labels; a
real 지점 찾기 list with per-branch actions; mobile sticky 지점 link. Franchise fit: Franchise in nav and a store strip,
closest to the request. Distance: the grey brick backdrop is near `law-goim`'s stone wall; the Latin serif wordmark and
editorial look are new among the samples. Its purple UI accent sits in the closed band (AC75).

**C. The Lane — https://www.thelanesalon.com**
One salon in San Francisco. A warm-grey top bar carries spaced caps nav (HOME, ABOUT | ARTISTS, SERVICES, GALLERY,
SALON POLICIES, CAREERS, CONTACT). Under it, a light greige page: a light Latin serif wordmark "THE LANE | SF" left; phone,
address and an outlined "BOOK NOW" pill right. The hero is two tall photos side by side on the right (a salon chair with a
palm frond and a mirror; a table with books and a plant in soft light), and a short sans line with an outlined
"SERVICES" pill on the left. Below: a large team photo beside "THE ARTISTS" and a paragraph. Suits a quiet, design-minded
neighbourhood brand.

```
+----------------------------------------------------------+
| HOME  ABOUT|ARTISTS  SERVICES  GALLERY ... CONTACT (bar) |
| THE LANE | SF              (415)… / address  (BOOK NOW>) |
|                        +-----------+   +-----------+     |
|                        | chair +   |   | table +   |     |
| A clean beauty salon   | palm,     |   | books,    |     |
| specializing in ...    | mirror    |   | plant     |     |
| (SERVICES >)           +-----------+   +-----------+     |
+----------------------------------------------------------+
| [ big team photo ]         THE ARTISTS / paragraph       |
+----------------------------------------------------------+
```

Proposed name: 로빈헤어살롱 (`beauty-robinhairsalon`). We would improve: a franchise layer the reference does not have
(지점 찾기 with three or more branches, 가맹 안내), per-branch Korean actions, and no named team photo (AC55). C is a single
salon, so 지점 찾기 and 가맹 would be new design. Distance: the warm greige base is near `clinic-bonui`'s warm off-white;
the two-tall-photo hero and spaced caps nav are new among the samples.

**D. 궁서채 — https://gungseochae.com**
A Korean salon franchise site. The white header has a Latin sans wordmark "Gungseochae" and Korean nav (매장 찾기,
교육·창업·가맹, 가맹 문의), a 브랜드 menu, cart, 로그인 and a red 회원가입 button. The hero is split: a dark graphite panel
on the left with a small red "GUNGSEOCHAE · HAIR SALON" label, a large Korean sans headline in two lines, two lines of copy,
a red "가까운 매장 찾기 →" button and a "시술 알아보기" text button; a salon photo (designer cutting a seated customer's hair)
fills the right. Under it is a beige three-tile bar: 내 동네 궁서채 (지역별 매장·위치·연락처), 가맹 창업 상담, 궁서채몰. Further
down: four numbered service columns (01 / CUT, 02 / PERM, 03 / COLOR, 04 / CARE) with the note "시술 종류와 가격, 예약 방법은
매장별로 확인해 주세요", a mall band, a beige 가맹 band, brand cards and a footer with app-store buttons. Suits a
mainstream neighbourhood brand whose first job is sending visitors to the nearest branch.

```
+----------------------------------------------------------+
| Gungseochae  매장 찾기 교육·창업·가맹 가맹 문의  ... [회원가입] |
+---------------------------+------------------------------+
| ## graphite panel ##      |                              |
| GUNGSEOCHAE · HAIR SALON  |   (salon photo: designer     |
| 당신의 일상에             |    cutting a seated customer)|
| 어울리는 헤어.            |                              |
| [가까운 매장 찾기 ->] 시술 알아보기 |                     |
+---------------------------+------------------------------+
| (pin) 내 동네 …  -> | (hand) 가맹 창업 상담 -> | (bag) 몰 -> |
| 01/CUT    02/PERM    03/COLOR    04/CARE   (columns)     |
+----------------------------------------------------------+
```

Proposed name: 로빈미용실 (`beauty-robinmiyongsil`). We would improve: a branch list on the same page instead of a separate
store page, with per-branch 네이버 예약 · 카카오톡 · 전화 · 네이버 지도; no login, cart or mall (Out); a warmer, less
template-like type and photo treatment. Franchise fit: the most franchise-native structure seen (매장 찾기 and 가맹 in nav,
a 매장 찾기 CTA in the hero, a tile bar). Distance: the graphite panel is near `law-ganeum`'s graphite; the split hero is near
`clinic-bonui`'s; its red accent sits in the closed band (AC75). Caution: the site looks newly built (its schema names a
company "Make Your Dreams"), and the server HTML of its store page (`/customer/stores`) shows "전체 0개 매장" before
scripts run. Whether it is an operating brand was not confirmed.

## Open questions
