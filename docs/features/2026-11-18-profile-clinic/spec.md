---
status: shipped
approved_at: 590674ee87d1e6e6b015e32787e760a553a8da53
commits: 590674ee87d1e6e6b015e32787e760a553a8da53..238036b4b8d5692d04e9536546da5cd8a1aab1af
---

# Clinic profile samples (`clinic`)

## Problem

The `/profile/` gallery has no sample for the `clinic` (병원 · 의원) industry. The clinic filter shows a
"디자인 준비 중" tile. A dentist, a family doctor or a dermatologist who runs a small practice and opens the
gallery sees nothing for their business. Sales has no clinic sample to show, and clinics differ by 진료과목
enough that one sample does not speak to all of them. A clinic site also carries a legal risk the other
samples do not: Korean medical advertising rules (의료법 제56조) forbid patient reviews, before-and-after
photos, superlatives and discount lures, which many real clinic sites use.

## Scope

"Each clinic sample" below means each of the three folders `profile/clinic-neuru/`,
`profile/clinic-byeotteul/` and `profile/clinic-bonui/`. An AC that says "each clinic sample" holds for all three.

- **In:** Sample A, `profile/clinic-neuru/`: 느루치과, a design-led dental practice; reference Studio Dental (AC63–AC69).
- **In:** Sample B, `profile/clinic-byeotteul/`: 볕뜰가정의학과의원, a friendly neighbourhood family-medicine practice; reference Tia (AC70–AC76).
- **In:** Sample D, `profile/clinic-bonui/`: 보늬피부과, a calm dermatology practice; reference Ever/Body (AC77–AC83).
- **In:** For each clinic sample: `index.html`, `style.css`, `thumb.jpg`, and photos in `img/` with `img/sources.txt`, built per `docs/profile-playbook.md`.
- **In:** Three `live` entries with `industry: "clinic"` in `PROFILES` in `scripts/profiles.py`.
- **In:** The regenerated `profile/index.html`, made by `python3 scripts/build.py`.
- **In:** Copy that follows Korean medical advertising rules in each clinic sample (AC25–AC31, AC81–AC83).
- **In:** Shared improvements over the references: 진료시간 on the first screen, a booking and call bar reachable on mobile, patient information in order, Korean typography (AC14–AC20).
- **In:** Per-sample mood, distinctness and improvements (AC50–AC54, AC63–AC83).
- **In:** Reconcile `docs/current_system/` (the sample list in `profile-samples/component.md`) and set `last_reconciled`.
- **Out:** Candidate C (One Medical) and any sample built on it.
- **Out:** Changes to `assets/`, to the gallery part of `scripts/build.py`, to `docs/profile-playbook.md`, and to `profile/flower-bomgyeol/` and `profile/food-saebyeokmil/`.
- **Out:** Real booking, map, KakaoTalk or phone integration. Patient buttons link to `#` placeholders.
- **Out:** Online consultation, patient login, insurance or payment features.
- **Out:** Self-hosting fonts. Google Fonts and Pretendard on jsDelivr stay allowed.
- **Out:** Samples for other industries.
- **Design:** none. Trigger 1 (crosses a component boundary): no. The change adds data and three samples through the existing named interfaces (`PROFILES` item, URL `profile/<slug>/`, `thumb.jpg`), unchanged. Trigger 2 (adds a component): no. Each sample is one more instance of the existing `profile-samples` component. Trigger 3 (alters a named interface): no. The `PROFILES` fields, the URL, the thumbnail contract and the `profile_thumb.py` CLI stay the same; `img/` and `img/sources.txt` are files inside each self-contained folder that no other component reads. Several live profiles in one industry are already supported: `build.py` counts live profiles per industry for the filter chip and adds one card per live profile, and neither `overview.md` nor `site-generator/component.md` assumes one sample per industry. Trigger 4 (internal module boundary): no. Each sample is one folder with one page, one stylesheet and its images. So `spec.md` + `tasks.md` are enough.

## Acceptance criteria

Folder and registration

- [ ] AC1 Each clinic sample contains `index.html`, `style.css` and `thumb.jpg`.
- [ ] AC2 In each clinic sample, `index.html` and `style.css` reference no local file outside that sample's folder (no `../`, no root-relative `/` path, no `assets/`).
- [ ] AC3 `scripts/profiles.py` has exactly one `PROFILES` entry for each of the slugs `clinic-neuru`, `clinic-byeotteul` and `clinic-bonui`, each with `industry` `clinic`, `status` `live` and `demo` `True`.
- [ ] AC4 Each clinic sample's `thumb.jpg` is 1200 px wide with a 16:10 ratio and shows the sample's current 1440×900 first screen (freshness rule in `tasks.md`).
- [ ] AC5 `python3 scripts/build.py` exits 0.
- [ ] AC6 Compared with `main`, the branch changes no file outside the three clinic sample folders, `profile/index.html`, `scripts/profiles.py` and `docs/`, and does not change `docs/profile-playbook.md`.

Sample markers and metadata

- [ ] AC7 In each clinic sample, the text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" is visible without scrolling at 1440 px and at 390 px width (browser).
- [ ] AC8 Each clinic sample's footer contains "Website by RobinTech".
- [ ] AC9 Each clinic sample's footer has a "Photos:" credit that names each source used in its `img/sources.txt` (Unsplash, Pexels).
- [ ] AC10 Each clinic sample's `index.html` contains `<meta name="robots" content="noindex">`.
- [ ] AC86 Each clinic sample's footer also contains "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다".
- [ ] AC87 Each clinic sample's `<title>` contains "디자인 샘플".
- [ ] AC11 Each clinic name (느루치과, 볕뜰가정의학과의원, 보늬피부과) does not match a real clinic found by a Kakao Map place search and a Daum web search for the name with its own suffix and the neighbouring suffixes (의원, 치과, 내과, 가정의학과, 피부과, 클리닉) (agent check, recorded in `name-check.txt` in this feature folder).
- [ ] AC12 In each clinic sample, every address on the page includes "(가상 주소)".
- [ ] AC13 In each clinic sample, every phone number on the page is `02-000-0000`, and every business registration number is `000-00-00000`.

Shared improvements over the references

- [ ] AC14 In each clinic sample at 390 px width, the 네이버 예약 button and the 전화 button are visible without scrolling (browser).
- [ ] AC15 In each clinic sample at 390 px width, the 네이버 예약 and 전화 buttons stay reachable on every scroll position (sticky bar or fixed buttons) (browser).
- [ ] AC16 In each clinic sample at 1440 px and at 390 px width, today's or the weekday 진료시간 (hours as digits, next to 평일, 오늘, 요일 or a weekday range such as 월–금) is visible without scrolling (browser).
- [ ] AC17 Each clinic sample's Korean body text uses `word-break: keep-all`.
- [ ] AC18 In each clinic sample, the section headings come in this order: 진료 안내 (what the practice treats), then 의료진, then 진료시간, then 오시는 길 (address and directions). Other sections may sit between them. The first-screen hours line of AC16 is not a section heading.
- [ ] AC19 Each clinic sample's 진료시간 section shows 점심시간 with its hours.
- [ ] AC20 Each clinic sample's 진료시간 section shows the 휴진일 (closed days, 일요일 · 공휴일 included).

Fonts, numbers and photos

- [ ] AC21 In each clinic sample, every external stylesheet comes from `fonts.googleapis.com` or from Pretendard on `cdn.jsdelivr.net`; no other external CSS or JS is loaded.
- [ ] AC22 In each clinic sample, the digits of 진료시간, phone numbers and any price render in a Korean typeface or a monospaced face as listed in `tasks.md` (never in a proportional Latin face with old-style figures), and every web font request succeeds (browser).
- [ ] AC23 In each clinic sample, `index.html` and `style.css` contain no `http://` or `https://` URL whose host is not `fonts.googleapis.com`, `fonts.gstatic.com` or `cdn.jsdelivr.net`.
- [ ] AC24 No photo ID recorded in one clinic sample's `img/sources.txt` appears in `profile/flower-bomgyeol/img/sources.txt`, in `profile/food-saebyeokmil/img/sources.txt` or in another clinic sample's `img/sources.txt`.

Medical advertising rules (의료법 제56조), each clinic sample

- [ ] AC25 The text of each clinic sample's `index.html` (visible text, `<title>`, `meta` description and `og:` content, `aria-label` and `title` attributes) contains none of: 최고, 최초, 최상, 유일, 1위, 1등, No.1, 최첨단, 독보적, 완벽, 영구적, 완치, 100%, 100 %, 100％, 보장, 보증, 부작용 없, 부작용이 없, 부작용 걱정, 무통, 통증 없, 아프지 않, 안 아픈, 전문병원, 할인, 특가, 반값, 이벤트, 후기, 리뷰, 체험담, 평점, 별점, 만족도, ★, 전후 사진, 비포, 애프터.
- [ ] AC26 No clinic sample shows a patient review, testimonial, rating or star score (human).
- [ ] AC27 No clinic sample shows a before-and-after photo or comparison image (human).
- [ ] AC28 No clinic sample makes a claim of treatment results, a superlative or ranking claim, an award, certification or endorsement claim, a "○○ 전문" claim other than a 전문의 credential, a comparison with other clinics, a price-based enticement, or names a drug or device brand (human).
- [ ] AC29 In each clinic sample, every doctor or practitioner named on the page has a visible marker containing "가상" next to the name.
- [ ] AC30 No clinic sample contains a 면허번호 or 의료기관 번호 with digits other than `0`.
- [ ] AC31 No photo on a clinic sample's page or in its `img/` shows an identifiable patient during treatment (human).

Korean patient flow, each clinic sample

- [ ] AC32 Each clinic sample has a 네이버 예약 button with an accessible name containing "네이버 예약".
- [ ] AC33 Each clinic sample has a 전화 button with an accessible name containing "전화".
- [ ] AC34 Each clinic sample has a 카카오톡 채널 link with an accessible name containing "카카오톡".
- [ ] AC35 Each clinic sample has a 네이버 지도 link with an accessible name containing "네이버 지도".
- [ ] AC36 In each clinic sample, the 네이버 예약, 전화, 카카오톡 and 네이버 지도 controls have `href="#"`.

Accessibility and motion, each clinic sample

- [ ] AC37 Every `<img>` in each clinic sample has a non-empty `alt`.
- [ ] AC38 Each clinic sample has exactly one `<h1>`, and no heading level is skipped.
- [ ] AC39 In each clinic sample under `prefers-reduced-motion: reduce`, at 1440 px and at 390 px, no element runs or declares an animation or transition longer than 0.01 s (browser).

Full-page checks, each clinic sample

- [ ] AC40 At 1440 px width, no clinic sample has horizontal overflow on the full page (browser).
- [ ] AC41 At 390 px width (page inside a `width:390px` iframe), no clinic sample has horizontal overflow on the full page (browser).
- [ ] AC42 A full-page screenshot of each clinic sample at 1440 px shows no overlapping or clipped text (browser, human review).
- [ ] AC43 A full-page screenshot of each clinic sample at 390 px shows no overlapping or clipped text (browser, human review).

Gallery (served by `python3 -m http.server 8000`)

- [ ] AC44 On `/profile/`, the `clinic` filter shows three cards, one for each clinic sample (browser).
- [ ] AC45 On `/profile/`, the `clinic` filter shows no "준비 중" tile (browser).
- [ ] AC46 In the generated `profile/index.html`, the `clinic` filter chip shows the count `3`.
- [ ] AC47 Clicking each of the three clinic cards opens the preview with that sample loaded in the iframe (browser).
- [ ] AC48 For each clinic card, the preview's desktop and mobile buttons switch the iframe between desktop and mobile width (browser).
- [ ] AC49 For each clinic card, pressing Esc closes the preview (browser).

Not the same site

- [ ] AC50 Each clinic sample shares no text, logo, clinic name or photo with its own reference site (A: studiodental.com, B: asktia.com, D: everbody.com).
- [ ] AC51 Side by side with its own reference site, a person does not read a clinic sample as the same site (human).
- [ ] AC52 Side by side with `profile/flower-bomgyeol/`, `profile/food-saebyeokmil/` and the other two clinic samples, a person does not read a clinic sample as the same design as any of them (human).
- [ ] AC53 The last `palette` hex of each clinic `PROFILES` entry (its accent) differs from the other two clinic entries' accents and from `#b8325a` (flower) and `#2d43b4` (food).
- [ ] AC54 Each clinic sample's `style.css` contains the accent hex of its `PROFILES` entry (case-insensitive).

Local photos, each clinic sample

- [ ] AC55 Every image path referenced in a clinic sample's `index.html` and `style.css` (`src`, `srcset`, CSS `url()`) resolves to an existing file inside that sample's folder.
- [ ] AC56 Every photo referenced in a clinic sample's `index.html` and `style.css` lives in that sample's `img/`.
- [ ] AC57 Every file in each clinic sample's `img/` other than `sources.txt` is a `.jpg` or `.webp` file.
- [ ] AC58 No image in a clinic sample's `img/` is wider than 2000 px.
- [ ] AC59 No image file in a clinic sample's `img/` is larger than 500 KB.
- [ ] AC60 The image files in each clinic sample's `img/` total at most 3 MB (`thumb.jpg` is not counted).
- [ ] AC61 Each clinic sample's `img/sources.txt` has exactly one line per image file in its `img/` (dotfiles aside), written `<file> <page URL> <download URL>`; the page URL starts with `https://unsplash.com/photos/` or `https://www.pexels.com/photo/`, or is `-`.
- [ ] AC62 Every download URL in each clinic sample's `img/sources.txt` starts with `https://images.unsplash.com/photo-` or `https://images.pexels.com/photos/`, and no line contains `plus.unsplash.com` or `premium_photo`.

Sample A — 느루치과 (`profile/clinic-neuru/`), reference Studio Dental

- [ ] AC63 At 1440 px, the `clinic-neuru` hero has an interior photo that spans the full viewport width (browser).
- [ ] AC64 The `clinic-neuru` hero has no overlay or gradient over the photo with a dark colour at alpha above 0.3 (browser).
- [ ] AC65 The `clinic-neuru` hero headline is dark text: its computed colour has every RGB channel at or below `0x40` (browser).
- [ ] AC66 At 1440 px, the `clinic-neuru` wordmark is not horizontally centred: its left edge is within the left quarter of the viewport (browser).
- [ ] AC67 `clinic-neuru` loads no `Cormorant Garamond` font.
- [ ] AC68 The `clinic-neuru` 진료 안내 section names at least four dental 진료 items (for example 일반 진료, 스케일링, 신경 치료, 보존 치료).
- [ ] AC69 `clinic-neuru` has a 의료진 section that names at least one dentist.

Sample B — 볕뜰가정의학과의원 (`profile/clinic-byeotteul/`), reference Tia

- [ ] AC70 The `body` background colour declared in `clinic-byeotteul/style.css` (custom properties resolved) has a blue channel greater than or equal to its red channel (neutral or cool white, not cream).
- [ ] AC71 Every RGB channel of that `body` background colour is at least `0xF0`.
- [ ] AC72 `clinic-byeotteul` loads no `IBM Plex Mono` font.
- [ ] AC73 `clinic-byeotteul` loads no `Cormorant Garamond` font.
- [ ] AC74 `clinic-byeotteul` has a notice bar above the header whose text contains "휴진".
- [ ] AC75 `clinic-byeotteul` has no login, sign-up or insurance-network control.
- [ ] AC76 The `clinic-byeotteul` 진료 안내 section names at least four everyday 진료 items (for example 감기, 만성질환 관리, 예방접종, 건강검진).

Sample D — 보늬피부과 (`profile/clinic-bonui/`), reference Ever/Body

- [ ] AC77 The `clinic-bonui` wordmark has a computed `letter-spacing` of at most `0.05em` (browser).
- [ ] AC78 The first family in the `clinic-bonui` wordmark's computed `font-family` is not a serif face (not `Noto Serif KR`, not `Cormorant Garamond`, not any other serif) (browser).
- [ ] AC79 `clinic-bonui` loads no `Cormorant Garamond` font.
- [ ] AC80 The `clinic-bonui` hero has no overlay or gradient over the photo with a dark colour at alpha above 0.3 (browser).
- [ ] AC81 The text of `clinic-bonui` (read as in AC25) contains none of: 동안 피부, 동안 시술, 젊어지, 효과 보장, 확실한 효과, 즉각적, 드라마틱, 극적인.
- [ ] AC82 The `clinic-bonui` 진료 안내 section contains the sentence "시술 결과와 부작용은 개인에 따라 다를 수 있으며, 진료 상담 후 결정합니다."
- [ ] AC83 Each `clinic-bonui` 진료 안내 item names a procedure and the skin concern it addresses, with no statement of its outcome (human).

Reconciliation

- [ ] AC84 The Source line of `docs/current_system/profile-samples/component.md` lists `clinic-neuru`, `clinic-byeotteul` and `clinic-bonui`.
- [ ] AC85 `git diff` from the `last_reconciled` commit in `docs/current_system/overview.md` to `HEAD` shows no change outside `docs/`.

Every AC above is checked by a `tasks.md` verify (command, browser or human); there is no `verify.md`.

## Assumptions

- **Names (human and agent decisions, 2026-11-18).** A: 느루 was kept by the human at G1, as 느루치과. B and D were chosen by the agent. All three share no syllable with each other or with 봄결 and 새벽밀. 볕뜰, 보늬 and 봄결 all start with ㅂ; the syllables and the meanings differ, so this is accepted. AC11 repeats the checks and records them in `name-check.txt`.
- **느루치과**, slug `clinic-neuru` ("slowly, at length"; unhurried care). On 2026-11-18 a web search for `"느루" 의원 OR 치과 OR 한의원 OR 내과 OR 정형외과` found no clinic of that name (nearest: 늘봄, 늘찬). Daum web searches for 느루의원, 느루치과 and 느루한의원 showed no clinic place listing on the first screen of results (only the top of each page was looked at); hits were an art exhibition, a 스튜디오느루 shopping listing for a massage bed, and blog posts. Kakao Map place searches for 느루의원, 느루치과, 느루내과, 느루피부과, 느루 병원 and 느루 물리치료 returned no result; 느루한의원 and 느루정형외과 returned none and were auto-corrected to other names (나무한의원, 나우정형외과). A place search for the word on its own (typed by mistake as 느루느루) listed 253 places, among them a butcher (느루정) and a coffee shop (느루커피), so the word is common in business names, just not for a clinic. 고른숨 was rejected (연세고른숨이비인후과의원 exists) and 솔빛숨 was rejected (close to 솔빛한방병원).
- **볕뜰가정의학과의원**, slug `clinic-byeotteul` ("a sunlit yard"; a bright, everyday place). On 2026-11-18 Kakao Map place searches for 볕뜰의원, 볕뜰가정의학과, 볕뜰내과, 볕뜰클리닉, 볕뜰 병원, 볕뜰치과 and 볕뜰한의원 returned no result and no auto-correction. A place search for 볕뜰 alone listed two places: LH 햇볕뜰 작은도서관 (a library) and a cafe named 볕뜰 in 강릉. A Daum web search for 볕뜰의원 showed no place card for that name; the first results were unrelated 의원 pages. A Daum web search for 볕뜰가정의학과 showed no place card; the top hit was an unrelated blog post.
- **보늬피부과**, slug `clinic-bonui` (보늬: the thin inner skin of a chestnut; care for skin). On 2026-11-18 Kakao Map place searches for 보늬피부과, 보늬피부과의원, 보늬의원, 보늬클리닉, 보늬 병원, 보늬에스테틱 and 보늬한의원 returned no result and no auto-correction. A search for 보늬 피부 did not load and is not counted. A place search for 보늬 alone listed 21 places; the first two were a nail shop (보늬네일) and a photo studio (스튜디오보늬); the rest of the list was not read. A Daum web search for 보늬피부과 showed no place card; the top hit was a blog post about a skincare product line whose name contains 보늬밤, not a clinic.
- **Names rejected for D:** 고요 (고요의원, a 피부과 in 성남, exists), 담연 (담연한의원 in 인천 exists; 담연피부과의원 was auto-corrected to 다온피부과의원), 하늬 (하늬피부과 was auto-corrected to the existing 한희피부과), 여울 (the search resolved to 여울동 and listed its 피부과).
- Naver search was refused by the browser's site restrictions on both checks and was not checked.
- **B is 가정의학과**, not 여성의원: it sits further from Tia's women's-health positioning and its copy (감기, 만성질환, 예방접종, 건강검진) stays plain under AC25–AC28.
- The industry key is `clinic`; it already exists in `INDUSTRIES`.
- Primary action: 네이버 예약 (appointment). Secondary: 전화, 카카오톡 채널 상담, 네이버 지도. Korean clinics already use these; jaseng.co.kr puts 오시는 길 · 진료시간 안내 · 진료비 안내 in a quick bar under the hero and floats 바로 예약 and 전화 상담 예약 buttons at the right edge.
- No price list on any clinic sample. A "비급여 진료비 안내" link to `#` stands in for the legally required notice. AC22 still applies to any number shown.
- Doctor names are invented and not checked against real doctors: any common Korean name matches some real doctor, so the visible "가상" marker (AC29) is what keeps them fictional.
- Credentials are generic (e.g. "○○과 전문의"), never a real university, hospital or licence number. The designated term 전문병원 is not used (AC25).
- AC25 and AC81 are plain substring checks on the page text they name. Words that look like hits but are allowed (for example "무료 주차") are not on the lists. If the copy needs a listed word in an allowed sense, the copy changes rather than the list.
- Photos: free Unsplash or Pexels photos of the practice space, hands, instruments, plants or a practitioner who is not treating a patient. Compared on a contact sheet in the implement stage, then downloaded at web size into each sample's `img/`.
- Mood targets, against the two shipped samples. `flower-bomgyeol`: dark photo hero, centred spaced serif wordmark (Cormorant Garamond), sand and raspberry `#b8325a`. `food-saebyeokmil`: warm paper cream `#f4efe5`, IBM Plex Mono labels, dawn blue `#2d43b4`. A resolves its full-bleed-photo overlap by a light photo, dark headline and a wordmark that is not centred (AC63–AC66). B resolves its cream overlap by a neutral or cool white base and no mono labels (AC70–AC72). D resolves its spaced-serif-wordmark overlap by an unspaced sans wordmark and a hero without a dark overlay (AC77–AC80). Exact palettes and faces are chosen in `tasks.md` within AC53–AC54.
- Per-sample ACs fix mood, the overlaps with the shipped samples and the improvements only. They do not fix a reference's composition (split hero, three-point panel, header button placement); the layout is new work per playbook §2.
- Improvements over each reference (playbook §1-4). A: Studio Dental's home is a photo and a footer only; 느루치과 adds 진료 안내, 의료진, 진료시간 and 오시는 길 (AC18, AC68, AC69). B: Tia's bar sells and its hero carries login and network checks; 볕뜰 uses the bar for 휴진 notices and drops login and insurance controls (AC74, AC75). D: Ever/Body leads with a discount and "Gold Standard" claims; 보늬 replaces them with law-safe 진료 안내 copy and a results-vary sentence (AC81–AC83). All three: first-screen hours, mobile booking bar and Korean typography (AC14–AC17).
- Mobile behaviour of the reference sites was not checked; mobile improvement points are targets for our samples, not defects found in the references.
- The reference sites use copy our samples must not use under AC25–AC28 (Tia: "The highest quality"; Ever/Body: "Take 20% Off Your First Visit", "The Gold Standard"; Studio Dental: a "Patient Stories" page). We take mood and level from them, never copy.
- `docs/current_system/` is current: on 2026-11-18 `git diff --stat 408af13..HEAD` lists only the docs commit that re-pointed SHAs after the flower squash (`overview.md` `last_reconciled`, flower spec and tasks frontmatter) and this feature's own `spec.md`. No reconciliation is needed before design.

### Research: sites looked at (2026-11-18, Chrome, 1492 px wide)

| Site | Result |
| --- | --- |
| studiodental.com | Candidate A |
| asktia.com | Candidate B |
| onemedical.com | Candidate C |
| everbody.com | Candidate D |
| kins.com | Runner-up. Warm cream page, terracotta wordmark, rounded inset photo card hero, phone number in the header. At-home physiotherapy with a zipcode-eligibility hero, not visit-first; cream close to `food-saebyeokmil` |
| parsleyhealth.com | Runner-up. Mint announcement bar, dark green nav, serif headline, warm portrait right. Same split-hero type as B; would suit a 한의원 |
| mavenclinic.com | Hero only. Virtual women's and family care; framed photo hero behind a cookie panel. Not a place to visit |
| kindbody.com | Hero only. Fertility clinic; yellow text block over an ultrasound photo. Shows a procedure with a patient-side screen |
| lanserhof.com | Hero only. Medical spa resort; dark aerial landscape, serif "Health & Beauty". Close to `flower-bomgyeol` in mood; a resort, not a practice |
| remedyplace.com | Hero only. Wellness club; black and red, booking bar. Not a clinic; dark |
| oakphysicaltherapy.com | Hero only. Plain sans, large face photo with white headline. Simple, less refined |
| emilygraceacupuncture.com | Hero only. Pink accent, treatment photo with needles in a patient's back, marquee banner. Shows a patient in treatment |
| symmetrytcm.com | Hero only. Olive green, serif title over a herb-book photo, practitioner photo. Template feel |
| jaseng.co.kr | Korean 한방병원. Seasonal illustration slider, quick bar (오시는 길, 진료시간 안내, 진료비 안내), floating 바로 예약 / 전화 상담 예약. Busy; useful for Korean patient flow |
| oracleclinic.com | Korean dermatology chain. Award photo slider, branch picker grid, 카카오톡 상담 box. Dated |
| hellotend.com | Excluded: blocked by a security service |
| toothbar.com | Excluded: redirected to another domain during load |
| bridgetownpt.com | Excluded: 403 Forbidden |

Site names came from web search results for curated lists (colorlib.com physical-therapy and acupuncture lists, seahawkmedia.com, designrush.com, freshysites.com) and from known clinics. The two colorlib lists were opened to read the links; the other list pages were not opened.

Screenshots of the four candidates' first screens (1440 × 900, headless Chrome, 2026-11-18) are kept outside the repository for G1: `A-studiodental.png`, `B-asktia.png`, `C-onemedical.png`, `D-everbody.png` and `contact-sheet.jpg` in the orchestrate run's scratchpad `clinic-candidates/` folder. Ever/Body's cookie banner was hidden with CSS before the shot; no consent was given.


### Candidates shown at G1 (history)

The descriptions below are the four candidates as shown to the human at G1. A, B and D were picked; C was not.

**A. Studio Dental — https://www.studiodental.com**
Architectural, photo-only home: one full-bleed photo of a warm wood corridor, a small serif wordmark top left, a black "Book Now" box and a menu icon top right, then only name, phone and email in the footer. The menu groups About (team, insurance and pricing, cancellation policy) and Visit (location, book). Inner pages are white with large dark sans paragraphs under a hairline.

```
+---------------------------------------------------------------+
| STUDIO                                        [Book Now]  ≡   |
| DENTAL                                                        |
|                                                               |
|          (full-bleed photo: wood corridor, person             |
|           walking past, soft light)                           |
|                                                               |
+---------------------------------------------------------------+
| Studio Dental                                                 |
| phone · email                                                 |
| Google  Yelp                                                  |
+---------------------------------------------------------------+
```

- Suits: a design-led 치과 or 피부과 whose interior is its brand.
- Korean flow: "Book Now" becomes 네이버 예약; the footer block grows into 진료시간 · 오시는 길 · 전화 · 카카오톡.
- Distance: from `flower-bomgyeol` medium (full-bleed photo hero, but light wood, no centred wordmark); from `food-saebyeokmil` high.
- Gap to fill: the home has almost no content; our sample must add 진료 안내, 의료진 and 진료시간 sections of our own. Mood-led reference more than layout.

**B. Tia — https://www.asktia.com**
Women's primary care. Thin announcement bar, nav with a coral "Book now" and an outline "Log In". Split hero: warm cream left with a large serif headline (one italic word), a five-item check list and two pill buttons; right, a photo of the clinic lounge with an arched magenta wall. Then an insurance logo row and "Services we offer" photo cards.

```
+---------------- announcement bar (orange) ------------------+
| tia Health  Services v Locations v ...   [Book now] [Log In] |
+------------------------------+------------------------------+
| Large serif headline,        |  (photo: clinic lounge,      |
| one italic word              |   arched colour wall)        |
| ✓ item  ✓ item  ✓ item       |                              |
| [Book an appointment] [Find] |                              |
+------------------------------+------------------------------+
|        logo row  ·  [See if you're in network]              |
|        Services we offer                                     |
|   [photo card]   [photo card]   [photo card]                 |
+-------------------------------------------------------------+
```

- Suits: 여성의원, 가정의학과, 내과 — a warm, friendly practice for regular visits.
- Korean flow: the announcement bar carries 휴진 notices; "Book now" becomes 네이버 예약; the check list becomes 진료 안내 points (law-safe wording); logo row becomes 진료시간 strip.
- Distance: from `flower-bomgyeol` high; from `food-saebyeokmil` medium (warm cream base; would need a cooler or whiter base).

**C. One Medical — https://www.onemedical.com**
Primary care. Pale yellow announcement bar, white nav with a dark green "Sign up" pill. Hero on light grey: blue serif headline left, short line, dark green "Book an appointment" button; right, a portrait cropped by a thin blue arc. Then a mint band with three photo cards, each with a small green uppercase label, a serif title and "Learn more".

```
+---------------- announcement bar (pale yellow) --------------+
| logo                 Locations v  For You v  Log in [Sign up]|
+-------------------------------------------+------------------+
| Big blue serif                            |   ( portrait     |
| headline                                  |  cropped by a    |
| one-line summary                          |   thin arc )     |
| [Book an appointment]                     |                  |
+-------------------------------------------+------------------+
| mint band:  [photo]       [photo]       [photo]             |
|             LABEL         LABEL         LABEL               |
|             Serif title   Serif title   Serif title  >      |
+-------------------------------------------------------------+
```

- Suits: 내과, 가정의학과, 소아청소년과 — a bright, trustworthy neighbourhood practice.
- Korean flow: "Book an appointment" becomes 네이버 예약 with 전화 beside it; the three cards become 진료 안내 (e.g. 일반 진료 · 건강검진 · 예방접종).
- Distance: from `flower-bomgyeol` high; from `food-saebyeokmil` high (white and grey base, green and blue).

**D. Ever/Body — https://www.everbody.com**
Cosmetic dermatology. White header with a centred spaced serif wordmark, two-line nav below it, a dark teal "Book Now" box right. Wide photo hero with a large white serif headline and a teal button left. Then an offset layout: a photo left, a pale grey panel right with a serif title and three hairline-separated points.

```
+-------------------------------------------------------------+
| Welcome to ...          E V E R / B O D Y       [Book Now v] |
|      Treatments  Our Locations  Our Providers  Philosophy    |
+-------------------------------------------------------------+
| Large white serif headline       (wide photo)               |
| one line                                                    |
| [Book An Appointment]  Explore treatments                   |
+-------------------------------------------------------------+
| [photo]            | grey panel: Serif title                 |
|                    | ── point                                |
|                    | ── point                                |
|                    | ── point      Discover link             |
+-------------------------------------------------------------+
```

- Suits: 피부과, 성형외과 상담 의원, 에스테틱 의원 — a calm, premium consultation practice.
- Korean flow: "Book Now" becomes 네이버 예약 with 카카오톡 상담; the hairline points become 진료 원칙 (law-safe, no result claims); a 진료시간 strip goes under the hero.
- Distance: from `flower-bomgyeol` medium (centred spaced serif wordmark is close to flower's logo; needs a different wordmark treatment); from `food-saebyeokmil` high.
- Caution: dermatology copy sits closest to the banned claims (AC25–AC28).

## Open questions

- **Q1. Which reference? — resolved 2026-11-18 at G1 by Seokhyun Kim.** Answer, as relayed by the orchestrator: candidates A (Studio Dental), B (Tia) and D (Ever/Body), one clinic sample each; C (One Medical) is not used. The human's words: "카테고리 별로 몇개 있어도 되니까". The name 느루 is kept. The orchestrator then fixed A as 치과 (`clinic-neuru`), B as a neighbourhood 의원 and D as 피부과, all three in this one feature. No open question remains.
