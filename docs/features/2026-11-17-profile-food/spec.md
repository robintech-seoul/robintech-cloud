---
status: shipped
approved_at: 3c164d3f11879ff3315e24e5bb646b69e154c1c2
commits: 3c164d3f11879ff3315e24e5bb646b69e154c1c2..8c01a561b383b425feab6bd4f6bfb719ae55f024
---

# Restaurant · cafe profile sample (`food`)

## Problem

The `/profile/` gallery has no sample for the `food` (식당 · 카페) industry. The food filter shows a
"디자인 준비 중" tile. A restaurant or cafe owner who opens the gallery sees nothing for their business.
Sales has no restaurant or cafe sample to show.

## Scope

- **In:** One new self-contained sample site in `profile/food-saebyeokmil/`: a neighbourhood bakery-cafe (동네 베이커리 카페, brunch and dessert) named 새벽밀, built per `docs/profile-playbook.md`.
- **In:** Its gallery thumbnail `profile/food-saebyeokmil/thumb.jpg`.
- **In:** Its photos, downloaded into `profile/food-saebyeokmil/img/` and referenced by relative path, with a source record `img/sources.txt`.
- **In:** One `live` entry with `industry: "food"` in `PROFILES` in `scripts/profiles.py`.
- **In:** The regenerated `profile/index.html`, made by `python3 scripts/build.py`.
- **In:** Improvements over Tartine: first-screen order action on mobile, Korean typography, the order of the information guests look for (AC14–AC17).
- **In:** `docs/profile-playbook.md` §3: photos are stored in the sample folder instead of hotlinked (AC50–AC52), and prices may use a monospaced face (AC53).
- **In:** Reconcile `docs/current_system/` (the sample list and the "Depends on" photo row in `profile-samples/component.md`) and set `last_reconciled`.
- **Out:** Changes to `assets/`, to the gallery part of `scripts/build.py`, and to `profile/flower-bomgyeol/`.
- **Out:** Localizing the photos of `profile/flower-bomgyeol/`. It is a separate follow-up feature on its own branch, because one branch carries one feature (AGENTS.md §6-6).
- **Out:** Real reservation, ordering, map or KakaoTalk integration. Customer buttons link to `#` placeholders.
- **Out:** Self-hosting fonts. Google Fonts and Pretendard on jsDelivr stay allowed.
- **Out:** Samples for other industries.
- **Design:** none. Trigger 1 (crosses a component boundary): no. The change adds data and one sample through the existing named interfaces (`PROFILES` item, URL `profile/<slug>/`, `thumb.jpg`), unchanged. Trigger 2 (adds a component): no. The sample is one more instance of the existing `profile-samples` component. Trigger 3 (alters a named interface): no. The `PROFILES` fields, the URL and the thumbnail contract stay the same; `img/` and `img/sources.txt` are extra files inside the self-contained folder, which no other component reads. Trigger 4 (internal module boundary): no. The sample is one folder with one page, one stylesheet and its images. So `spec.md` + `tasks.md` are enough.

## Acceptance criteria

Folder and registration

- [ ] AC1 `profile/food-saebyeokmil/` contains `index.html`, `style.css` and `thumb.jpg`.
- [ ] AC2 `index.html` and `style.css` reference no local file outside `profile/food-saebyeokmil/` (no `../`, no root-relative `/` path, no `assets/`).
- [ ] AC3 `scripts/profiles.py` has exactly one `PROFILES` entry with `slug` `food-saebyeokmil`, `industry` `food`, `status` `live` and `demo` `True`.
- [ ] AC4 `thumb.jpg` is 1200 px wide with a 16:10 ratio.
- [ ] AC5 `python3 scripts/build.py` exits 0.
- [ ] AC6 Compared with `feature/profile-gallery`, the branch changes no file outside `profile/food-saebyeokmil/`, `profile/index.html`, `scripts/profiles.py` and `docs/`.

Sample markers and metadata

- [ ] AC7 The text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" is visible without scrolling at 1440 px and at 390 px width (browser).
- [ ] AC8 The footer contains "Website by RobinTech".
- [ ] AC9 The footer has a "Photos:" credit that names each source used in `img/sources.txt` (Unsplash, Pexels).
- [ ] AC10 `index.html` contains `<meta name="robots" content="noindex">`.
- [ ] AC11 The shop name 새벽밀 does not match a real shop found by a web search for the name plus "빵집", "베이커리" or "카페" (agent check, recorded in `name-check.txt` in this feature folder).
- [ ] AC12 Every address on the page includes "(가상 주소)".
- [ ] AC13 Every phone number on the page is `02-000-0000`, and every business registration number is `000-00-00000`.

Improvements over the reference

- [ ] AC14 At 390 px width, the 카카오톡 주문 button (cake pre-order) is visible without scrolling (browser).
- [ ] AC15 At 390 px width, the 카카오톡 주문 button stays reachable on every scroll position (sticky bar or fixed button) (browser).
- [ ] AC16 Korean body text uses `word-break: keep-all`.
- [ ] AC17 The page has, in this order of first appearance, a menu with prices (bread, cakes, drinks), then opening hours with closed days, then address with directions (오시는 길).

Fonts, prices and photos

- [ ] AC18 Every external stylesheet comes from `fonts.googleapis.com` or from Pretendard on `cdn.jsdelivr.net`; no other external CSS or JS is loaded.
- [ ] AC19 Every price is written as digits plus 원 (e.g. 6,500원), its digits render in a Korean typeface from the list in `tasks.md` or in a monospaced face as defined there (never in a proportional Latin face such as a serif with old-style figures; 원 may fall back to a Korean face), and every web font request succeeds (browser).
- [ ] AC20 `index.html` and `style.css` contain no `http://` or `https://` URL whose host is not `fonts.googleapis.com`, `fonts.gstatic.com` or `cdn.jsdelivr.net` (no remote image, no `images.unsplash.com` or `images.pexels.com` preconnect).
- [ ] AC21 No line of `img/sources.txt` contains `plus.unsplash.com` or `premium_photo`.
- [ ] AC22 No photo ID recorded in `img/sources.txt` appears in `profile/flower-bomgyeol/index.html`.

Korean customer flow

- [ ] AC23 The page has a 카카오톡 주문 button with an accessible name containing "카카오톡".
- [ ] AC24 The page has a 네이버 예약 button with an accessible name containing "네이버 예약".
- [ ] AC25 The page has a 네이버 지도 link with an accessible name containing "네이버 지도".
- [ ] AC26 The page has a 전화 button with an accessible name containing "전화".
- [ ] AC27 The 카카오톡, 네이버 예약, 네이버 지도 and 전화 buttons have `href="#"`.

Accessibility and motion

- [ ] AC28 Every `<img>` has a non-empty `alt`.
- [ ] AC29 The page has exactly one `<h1>`, and no heading level is skipped.
- [ ] AC30 Under `prefers-reduced-motion: reduce`, at 1440 px and at 390 px, no element runs or declares an animation or transition longer than 0.01 s (browser).

Full-page checks

- [ ] AC31 At 1440 px width, the full page has no horizontal overflow (browser).
- [ ] AC32 At 390 px width (page inside a `width:390px` iframe), the full page has no horizontal overflow (browser).
- [ ] AC33 A full-page screenshot at 1440 px shows no overlapping or clipped text (browser, human review).
- [ ] AC34 A full-page screenshot at 390 px shows no overlapping or clipped text (browser, human review).

Gallery (served by `python3 -m http.server 8000`)

- [ ] AC35 On `/profile/`, the `food` filter shows the new card and no "준비 중" tile for `food` (browser).
- [ ] AC36 Clicking the card opens the preview with the sample loaded in the iframe (browser).
- [ ] AC37 The preview's desktop and mobile buttons switch the iframe between desktop and mobile width (browser).
- [ ] AC38 Pressing Esc closes the preview (browser).

Not the same site

- [ ] AC39 The sample shares no text, logo, shop name or photo with tartinebakery.com.
- [ ] AC40 Side by side with tartinebakery.com, a person does not read the sample as the same site (human).
- [ ] AC41 Side by side with `profile/flower-bomgyeol/`, a person does not read the sample as the same design (human).

Local photos

- [ ] AC42 Every image path referenced in `index.html` and `style.css` (`src`, `srcset`, CSS `url()`) resolves to an existing file inside `profile/food-saebyeokmil/`.
- [ ] AC43 Every photo referenced in `index.html` and `style.css` lives in `profile/food-saebyeokmil/img/`.
- [ ] AC44 Every file in `img/` other than `sources.txt` is a `.jpg` or `.webp` file.
- [ ] AC45 No image in `img/` is wider than 2000 px.
- [ ] AC46 No image file in `img/` is larger than 500 KB.
- [ ] AC47 The image files in `img/` total at most 3 MB (`thumb.jpg` is not counted).
- [ ] AC48 `img/sources.txt` has exactly one line per image file in `img/` (dotfiles aside), written `<file> <page URL> <download URL>`; the page URL starts with `https://unsplash.com/photos/` or `https://www.pexels.com/photo/`.
- [ ] AC49 Every download URL in `img/sources.txt` starts with `https://images.unsplash.com/photo-` or `https://images.pexels.com/photos/`.

Playbook

- [ ] AC50 The photo rule in §3 of `docs/profile-playbook.md` says photos are downloaded into `profile/<slug>/img/` and referenced by relative path, and no longer says they are linked directly to `images.unsplash.com`.
- [ ] AC51 The folder rule in §3 of `docs/profile-playbook.md` lists `img/` (with `img/sources.txt`) among the sample's files.
- [ ] AC52 `docs/profile-playbook.md` states that `profile/flower-bomgyeol/` still hotlinks its photos until its follow-up feature localizes them.
- [ ] AC53 The font rule in §3 of `docs/profile-playbook.md` says prices and numbers use a face with even figures, a Korean face or a monospaced (모노) face, and no longer says they use only a Korean face (한글 서체로).

Every AC is checked by a task's verify in `tasks.md` (commands in `check_static.py` and `check_browser.py` in this folder); there is no `verify.md`.

## Assumptions

- **Shop name (agent-decided; the human may overturn):** 새벽밀 ("dawn wheat", bread baked at dawn), slug `food-saebyeokmil`. Web searches on 2026-11-17 found no shop of that exact name: `"새벽밀" 베이커리 카페`, `"새벽밀" 빵집`, and `"새벽밀" 카페 베이커리 instagram` limited to instagram.com, kakao.com, daangn.com, diningcode.com and mangoplate.com. Nearest hits were differently named shops (밀봄숲, 카페밀, Mi Mill). Limits: the search tool is US-based, did not honour the quotes strictly, and could not search naver.com, so a small shop listed only on Naver may be missed. AC11 repeats the check during implementation.
- The industry key is `food`; it already exists in `INDUSTRIES`.
- Shop type: a neighbourhood bakery-cafe with brunch and dessert, take-out and whole-cake pre-orders. Primary action: 카카오톡 주문 for cake pre-orders. Secondary: 네이버 예약 (brunch seats), 네이버 지도, 전화.
- Mood: light warm off-white page with a mono, typewriter-adjacent feel, taken from Tartine as mood and level only. Layout, text, logo and photos are our own. The composition, palette and Korean typography are new and differ from both Tartine and `flower-bomgyeol` (dark hero, serif, beige and raspberry). The accent is neither Tartine's ochre nor flower's raspberry.
- The mono feel comes from Latin labels, small caps and numbers, prices included. Decided at G2 (Seokhyun Kim, 2026-11-18): the Tartine mood matters more than the playbook's "가격 · 숫자는 한글 서체로", so prices may use the page's monospaced face if that looks better. The rule's purpose stays: no uneven (old-style) figures in a proportional Latin face (AC19). Korean text stays in a Korean typeface, and the playbook's font rule is reworded to match (AC53).
- Section order after AC17 (for example a pre-order guide or 오늘의 빵 notice) is decided in the implement stage.
- Photos come from free Unsplash or Pexels photos, compared on a contact sheet in the implement stage, then downloaded at web size (at most 2000 px wide, JPEG or WebP) into `img/`. Fonts stay remote (Google Fonts, Pretendard on jsDelivr); the human asked only about photos.
- `img/sources.txt` (format in AC48) keeps the licence trail and makes AC21, AC22 and AC48–AC49 checkable now that the HTML holds no remote photo URL.
- The 3 MB total and 500 KB per-file budget assume about six to ten photos, with one hero near 2000 px.
- Mobile behaviour of the reference sites was not checked; mobile improvement points are targets for our sample, not defects found in the references.
- Layout sketches below show the top of each page only (hero and the first one or two sections). No footer was reached on any site.

### Research: sites looked at (2026-11-17, Chrome, 1492 px wide)

| Site | Result |
| --- | --- |
| noma.dk | Candidate D |
| septime-charonne.fr | Candidate A |
| tartinebakery.com | Candidate B |
| dishoom.com | Candidate C |
| stjohnrestaurant.com | Runner-up. White page, engraved pig logo, black Reservations button, grey centred quote. Classic bistro. Less refined photo grid than the four |
| elevenmadisonpark.com | Hero only. Centred logo, plain nav, framed chef photo. Refined but generic; fine-dining group site |
| atomixnyc.com | Hero only. Large text nav over a fabric photo. Art-led, little visit information on the first screen |
| lilianewyork.com | Hero only. Address bar, badge logo, nine-item nav, food carousel. Busy and dated |
| fritz.co.kr | Hero only. Korean coffee brand; vertical text nav over a hanok gate photo; store and wholesale first |
| jungsik.kr | Hero only. Dim interior photo with emblem. Fine dining; little information on the first screen |
| sightglasscoffee.com | Coffee e-commerce. Product-first, not visit-first |
| stumptowncoffee.com | Coffee e-commerce. Discount popup and cookie banner cover the page |
| timwendelboe.no | Coffee e-commerce. Product-first, not visit-first |
| lacabra.com (from lacabra.dk) | Coffee e-commerce. Cookie wall covers the page |
| mamannyc.com | Not evaluated. Only the loading screen showed |
| monstervegan.com, hartbageri.com, fuglen.com, gjusta.com | Did not load at the URL tried (browser error page) |

Site names came from web search results for curated lists (owner.com, krishaweb.com, menutiger.com, colorlib.com, freshysites.com, mycodelesswebsite.com) and from known restaurants and cafes. The list pages themselves were not opened. Septime, Tartine and Dishoom were opened by direct URL.

### Picked at G1 (Seokhyun Kim, 2026-11-17): B. Tartine — https://www.tartinebakery.com

Bakery-cafe: thin announcement bar, nav left / spaced-out wordmark centre / ochre ORDER button right. A soft photo hero with a short mono welcome. Then "Happenings" title left with two photo cards right, then two pre-order columns with underlined text links. Warm off-white background, mono type throughout.

```
+------------- announcement: pre-order holiday pies -------------+
| LOCATIONS >  ABOUT >        T A R T I N E      SHIPPING [ORDER] |
| +-----------------------------------------------------------+ |
| | Welcome to ...      (blurred bakery photo hero)            | |
| | short mono line                                            | |
| +-----------------------------------------------------------+ |
|   Happenings         [photo card]      [photo card]           |
|                      caption           caption                |
|   SPECIAL ORDER CAKES          PRE-ORDER CAKES & TARTS        |
|   text                          text                          |
|   ORDER LINK -> ________        PRE-ORDER LINK -> ________    |
+---------------------------------------------------------------+
```

- Suits: a bakery-cafe, brunch cafe or dessert shop with take-out and cake pre-orders. This is the only candidate that covers the "카페" half of the industry.
- Korean flow: the ORDER button becomes 카카오톡 주문 (cake pre-order); the announcement bar carries the season's 예약 notice; LOCATIONS becomes 네이버 지도 and 전화.
- Distance from `flower-bomgyeol`: high (light, mono, ochre accent).
- Mobile target: ORDER button stays in a sticky bar.

### Not picked at G1

- A. Septime (https://www.septime-charonne.fr): split screen, mono set menu left, one tall B/W photo right. Suits a dinner-led bistro or course restaurant.
- C. Dishoom (https://www.dishoom.com): dark storytelling restaurant with framed archive photos. Suits a 노포 or family restaurant; close to `flower-bomgyeol` in mood.
- D. Noma (https://www.noma.dk): calm, reservation-led, near-black green hero. Suits a tasting course or omakase; close to `flower-bomgyeol` in mood.

## Open questions

