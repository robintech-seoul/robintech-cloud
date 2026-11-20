---
status: shipped
approved_at: d61f2c43cbbcaf37032e02146f038dab9705d979
commits: 61959edac9bf44c6a6dc4207cbe7ca62a991cf5b..d61f2c43cbbcaf37032e02146f038dab9705d979
---

# Crypto profile samples (`crypto`)

## Problem

The `/profile/` gallery has no sample for the `crypto` (코인 · 가상자산) industry. The 코인 · 가상자산 filter chip shows no
count, and the grid shows a "코인 · 가상자산 프로파일 준비 중" tile. A crypto business owner who opens the gallery finds nothing
for their business, and sales has no crypto sample to show.

A crypto site sells with figures, backers and a sign-up, and a sample has none of them. The sites opened for this spec
(2026-11-20) show "고객이 인정한 압도적 1위!" (빗썸), an event pop-up "5천 원 거래하면 USDT 100% 지급!" (코인원), "$2T+" of
volume (Kraken), "$105bn" and "60mn" cards (Copper), a "Backed by" row of investor logos (Kaia), an e-mail field with a
"Sign up" button on the first screen (Coinbase, Kraken), a QR code for the app (업비트) and live prices of real assets
(Coinbase, Xangle). On a sample, each of these would be fabricated or would be a working entry point.

A public page that looks like an exchange, a custodian or a token project can be read as a phishing page. DAXA's press
list (2026-07-08) warns of apps that impersonate 원화거래소. Korean law also reaches the content: trading or keeping 가상자산
for users as a business needs a registration, advertising unregistered fund-raising is barred, and so is a false price
used to induce trading (rule sources in Assumptions).

## Scope

"Each crypto sample" below means each of the three folders `profile/crypto-robincoin/`, `profile/crypto-robincustody/`
and `profile/crypto-robinchain/`. An AC that says "each crypto sample" holds for all three. "업태" is the kind of business
a sample presents. It is fixed per sample: `crypto-robincoin` is 거래소, `crypto-robincustody` is 수탁, and
`crypto-robinchain` is 웹3 개발사. An AC that names an 업태 holds for the sample of that 업태.

- **In:** Sample A, `profile/crypto-robincoin/`: 로빈코인, a 거래소 page on white with a blue panel that holds a phone screen of example prices, and a large sans headline; reference Coinbase (AC150–AC192).
- **In:** Sample B, `profile/crypto-robincustody/`: 로빈커스터디, a 수탁 page in one flat apricot colour with a white pill header, a headline in two faces and a line drawing; reference Copper (AC193–AC223).
- **In:** Sample D, `profile/crypto-robinchain/`: 로빈체인, a 웹3 개발사 page in black and one lime with a three-line wide headline, two pill buttons, a lit object and a glass bar header; reference Kaia (AC224–AC251).
- **In:** For each crypto sample: `index.html`, `style.css` and `thumb.jpg`, built per `docs/profile-playbook.md`, with pictures in CSS and inline SVG and no photo.
- **In:** A one-page site for one fictional crypto business: what it does, how it works, risk notice, and 문의.
- **In:** One `live` entry with `industry: "crypto"` in `PROFILES` in `scripts/profiles.py` for each crypto sample.
- **In:** The regenerated `profile/index.html`, made by `python3 scripts/build.py`.
- **In:** Advertising and display rules for 가상자산 businesses, as content rules (AC58–AC90, AC95–AC97).
- **In:** No working entry point: no sign-up, login, wallet connection, deposit address, form or script (AC47–AC57).
- **In:** Korean visitor flow: 문의 reachable on every screen, and 카카오톡 · 전화 · 네이버 예약 · 네이버 지도 (AC35–AC46).
- **In:** Distinctness of each crypto sample from the fifteen shipped samples, from the other crypto samples and from its own reference (AC117–AC128, AC252–AC264).
- **In:** Reconcile `docs/current_system/` (the sample list in `profile-samples/component.md`) and set `last_reconciled`.
- **Out:** Candidate C (Hashed, proposed 로빈리서치 `crypto-robinresearch`, 리서치). The human did not pick it at G1.
- **Out:** Photos. No crypto sample has an `img/` folder (AC262).
- **Out:** A business-name collision check and a `name-check.txt`. The human chose 로빈 + field-word names (Assumptions).
- **Out:** Changes to `assets/`, to `scripts/build.py`, to `docs/profile-playbook.md`, and to the fifteen shipped samples under `profile/`.
- **Out:** Live price data, a price API, charts of real assets, and any script.
- **Out:** Real sign-up, login, KYC, wallet connection, deposit, withdrawal, order, app download, KakaoTalk, booking, map or phone integration. Every link is a `#` placeholder.
- **Out:** Forms of any kind, chat widgets, calculators, newsletter sign-up.
- **Out:** Inner pages (market pages, asset pages, reports, docs, a blog). Each sample is one page.
- **Out:** Self-hosting fonts. Google Fonts and Pretendard on jsDelivr stay allowed.
- **Out:** Samples for other industries (`invest` is a separate feature).
- **Design:** none. Trigger 1 (crosses a component boundary): no. The change adds data and samples through the existing named interfaces (`PROFILES` item, URL `profile/<slug>/`, `thumb.jpg`), which stay unchanged. Trigger 2 (adds a component): no. Each sample is one more instance of the existing `profile-samples` component. Trigger 3 (alters a named interface): no. The `crypto` key is already in `INDUSTRIES`, and the `PROFILES` fields, the URL, the thumbnail contract and the `profile_thumb.py` CLI stay the same. Trigger 4 (internal module boundary): no. A sample is one folder with one page, one stylesheet and its images. So `spec.md` + `tasks.md` are enough.

## Acceptance criteria

AC1–AC149 hold for every crypto sample unless a block names one 업태 (Scope says which sample has which 업태).
AC150–AC251 are per-sample: the traits kept from each sample's reference, its palette and typefaces, and what it must not
copy. AC252–AC264 compare or bind all three. AC91–AC94 are not in use. A tag at the end of a rule AC says where it comes
from: a statute and article, or "sample policy". Every criterion is checked by a task's `verify` in `tasks.md`; there is
no `verify.md`.

"Page text" means, in `index.html`: visible text, `<title>`, `meta` description and `og:` content, `aria-label`, `alt` and
`title` attributes, and the text of inline `<svg>`; in `style.css`: `content:` strings. A listed word that holds a space is
also banned written without the space. Full-width letters and digits are read as their plain forms, and soft hyphens and
zero-width characters are ignored. Latin words are matched in any case. A listed word made only of Latin capitals
and digits (APY, APR, APK, ISMS, FIU, AUM, TVL, ICO, IDO, IEO, OKX, DAXA, KYC and the tickers of AC70) is matched as a whole
word, so that "icon" does not match ICO.

Folder and registration

- [ ] AC1 Each crypto sample contains `index.html`, `style.css` and `thumb.jpg`, and no other file (dotfiles aside).
- [ ] AC2 In each crypto sample, `index.html` and `style.css` reference no local file outside that sample's folder (no `../`, no root-relative `/` path, no `assets/`).
- [ ] AC3 `scripts/profiles.py` has exactly one `PROFILES` entry for each crypto sample's slug, each with `industry` `crypto`, `status` `live` and `demo` `True`, and no `crypto` entry for any other slug.
- [ ] AC4 Each crypto sample's slug matches `crypto-robin` followed by one or more lowercase ASCII letters only.
- [ ] AC5 Each crypto sample's `thumb.jpg` is 1200 px wide with a 16:10 ratio and shows the sample's current 1440×900 first screen.
- [ ] AC6 `python3 scripts/build.py` exits 0.
- [ ] AC7 Compared with `main`, the branch changes no file outside the crypto sample folders, `profile/index.html`, `scripts/profiles.py` and `docs/`, and does not change `docs/profile-playbook.md`.

Sample markers, names and metadata

- [ ] AC8 In each crypto sample, the text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" is visible without scrolling at 1440 px width (browser).
- [ ] AC9 In each crypto sample, the text of AC8 is visible without scrolling at 390 px width (browser).
- [ ] AC10 At 1440 px and at 390 px, the computed `font-size` of the AC8 text on the first screen is at least the computed `font-size` of `<body>` and at least 14 px (browser).
- [ ] AC11 At 1440 px and at 390 px, a person reads the AC8 text on the first screen in a colour that stands out clearly from its background (human).
- [ ] AC12 At 1440 px and at 390 px, an element whose text contains "디자인 샘플 · 상호와 정보는 가상입니다" is visible at every scroll position from the top to the end of the page, and it or the fixed or sticky element that holds it has an opaque background colour, so the page that scrolls under it does not show through (browser; sample policy: a screenshot taken mid-page must still say the business is fictional).
- [ ] AC13 Each crypto sample's footer contains "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다".
- [ ] AC14 Each crypto sample's footer contains "Website by RobinTech".
- [ ] AC15 Each crypto sample's `index.html` contains `<meta name="robots" content="noindex">`.
- [ ] AC16 Each crypto sample's `<title>` contains "디자인 샘플".
- [ ] AC17 The `name` of each crypto sample's `PROFILES` entry is "로빈" followed by one or more Hangul syllables and nothing else.
- [ ] AC18 The accessible name of each crypto sample's header wordmark starts with "로빈".
- [ ] AC19 No two crypto samples share the same `PROFILES` `name`.
- [ ] AC20 In each crypto sample, every address on the page includes "(가상 주소)".
- [ ] AC21 Every address in each crypto sample names a district or road that does not exist (for example 가상구 결로), and the page text names no real 구, 동 or neighbourhood as the business's location; a 시 or 도 name alone is allowed (human).
- [ ] AC22 In each crypto sample, every phone number on the page is `02-000-0000`.
- [ ] AC23 In each crypto sample, every 사업자등록번호 on the page is `000-00-00000`.
- [ ] AC24 No crypto sample shows a 가상자산사업자 신고번호, an ISMS or ISMS-P 인증번호, a 통신판매업 신고번호 or any other registration or certificate number; the 사업자등록번호 of AC23 is the only number of that kind (decided by the orchestrator).
- [ ] AC25 Every e-mail address in each crypto sample's page text ends in `@example.com`.
- [ ] AC26 The page text of each crypto sample holds no social-media handle (`@` followed by a name, outside an `@example.com` e-mail address) and no domain name other than `example.com`.
- [ ] AC27 No crypto sample shows a person's name or portrait, whether as 대표, a founder, an analyst, a developer, an adviser or a customer (human; decided by the orchestrator).

Structure of the page

- [ ] AC28 Each crypto sample has a section whose heading contains "서비스" or "하는 일" and that names at least three things the business does.
- [ ] AC29 Each crypto sample has a section whose heading contains "절차", "과정" or "이용 방법" and that lists at least three steps in an `<ol>`.
- [ ] AC30 Each crypto sample has a contact section whose heading contains "문의" or "상담".
- [ ] AC31 The AC30 section contains the visible sentence "가상의 업체이며 가상자산사업자가 아닙니다. 실제 거래 · 보관 · 상담을 제공하지 않습니다.", and at 1440 px and at 390 px that sentence has a computed `font-size` of at least 14 px (browser) (sample policy; 특금법 제7조① requires a 가상자산사업자 to be registered, and 유사수신법 제4조 bars advertising unregistered fund-raising).
- [ ] AC32 The sentence of AC31 is also visible without scrolling at 1440 px and at 390 px in a sample whose 업태 is 거래소 or 수탁 (browser; sample policy: these two 업태 are 가상자산사업자 under 가상자산이용자보호법 제2조2호).
- [ ] AC33 Each crypto sample's `<h1>` text is in Korean (contains at least one Hangul syllable).
- [ ] AC34 Each crypto sample's Korean body text uses `word-break: keep-all`.

Korean visitor flow

- [ ] AC35 The AC30 section of each crypto sample has a link whose accessible name contains "카카오톡".
- [ ] AC36 The AC30 section of each crypto sample has a link whose accessible name contains "전화".
- [ ] AC37 The AC30 section of each crypto sample has a link whose accessible name contains "네이버 예약".
- [ ] AC38 The AC30 section of each crypto sample has a link whose accessible name contains "네이버 지도".
- [ ] AC39 No link in the AC30 section has an accessible name that contains two or more of 카카오톡, 전화, 네이버 예약 and 네이버 지도.
- [ ] AC40 In each crypto sample at 1440 px width, a link to the AC30 section (`href="#<id>"` of that section) whose text contains "문의" or "상담" is visible without scrolling (browser).
- [ ] AC41 In each crypto sample at 390 px width, a link of the AC40 kind is visible without scrolling (browser).
- [ ] AC42 In each crypto sample at 390 px width, a link of the AC40 kind stays on screen at every scroll position (browser).
- [ ] AC43 In each crypto sample at 390 px width, with the page scrolled to the end, the last text line of the footer is visible and not covered by a fixed or sticky element (browser).
- [ ] AC44 The AC30 section of each crypto sample shows the 상담 hours as digits.
- [ ] AC45 The AC30 section of each crypto sample shows the closed days.
- [ ] AC46 The AC30 section of each crypto sample shows an address with "(가상 주소)" and the phone number `02-000-0000`.

No working entry point (decided by the orchestrator; sample policy against a phishing reading)

- [ ] AC47 Each crypto sample has no `<form>`, `<input>`, `<select>`, `<textarea>` or `<button>` element.
- [ ] AC48 Each crypto sample has no `<script>` element, no inline event-handler attribute (`on…=`), no `javascript:` URL, and no `.js` file in its folder.
- [ ] AC49 Every `<a>` in each crypto sample has an `href` that is `#` or `#` followed by the `id` of an element on the page.
- [ ] AC50 Each crypto sample has no `<iframe>`, `<embed>`, `<object>`, `<video>` or `<audio>` element.
- [ ] AC51 The page text and markup of each crypto sample hold no wallet-address-shaped string: no `0x` followed by eight or more hexadecimal characters, no `bc1` followed by twenty or more characters, and no unbroken run of 26 or more letters and digits that mixes both (font and image URLs and inline SVG geometry attributes such as `d` and `points` aside).
- [ ] AC52 No crypto sample shows a QR code or an image that reads as one (human).
- [ ] AC53 The page text of each crypto sample contains none of: App Store, Google Play, 앱스토어, 플레이스토어, 앱 다운로드, APK, and no app-store badge is shown (human for the badge).
- [ ] AC54 The page text of each crypto sample contains none of: 지갑 연결, 지갑 연동하기, Connect Wallet, 시드 문구, 복구 문구, 니모닉, 개인키 입력, 입금 주소, 입금하기, 출금하기, 계좌번호, 가상계좌, 실명계좌.
- [ ] AC55 The page text of each crypto sample names no bank or payment brand: it contains none of 케이뱅크, 카카오뱅크, 토스, 농협, 신한, 국민은행, 우리은행, 하나은행, 기업은행, 페이팔, Visa or Mastercard, and a person finds no other such name (human for the last part).
- [ ] AC56 A link whose accessible name or text contains 로그인, 회원가입, 가입하기 or 시작하기 appears only in the sample whose 업태 is 거래소. There the `<header>` holds exactly one link whose accessible name is 로그인 and exactly one whose accessible name is 회원가입, no other link holds either word, and AC190 bans 가입하기 and 시작하기 (A20).
- [ ] AC57 `index.html` and `style.css` of each crypto sample contain no `http://`, `https://` or protocol-relative (`//host`) URL, in any letter case, whose host is not `fonts.googleapis.com`, `fonts.gstatic.com` or `cdn.jsdelivr.net`.

Advertising and display rules, every 업태

- [ ] AC58 Each crypto sample's footer contains the visible sentence "가상자산은 가격 변동이 커서 원금의 전부 또는 일부를 잃을 수 있습니다." (decided by the orchestrator; 가상자산이용자보호법 제10조④2호 bars a display that leaves out a material fact; DAXA 광고 · 홍보 행위 모범규준 not read, so the notice is required for every 업태).
- [ ] AC59 At 1440 px and at 390 px, the computed `font-size` of the AC58 sentence is at least 13 px (browser).
- [ ] AC60 At 1440 px and at 390 px, the contrast ratio of the AC58 sentence against the background behind it is at least 4.5:1 (browser).
- [ ] AC61 The page text contains none of: 수익, 원금 보장, 원금 보전, 원금 보호, 손실 보전, 손실 없, 무위험, 이율, 배당, APY, APR, 복리, 불로소득, 패시브 인컴, and no 이자 other than the ending of the three words 개발사이자, 운영사이자 and 회사이자 (so 이자율, 무이자 and 예치이자 are banned) (decided by the orchestrator; 유사수신법 제2조1 · 2 · 4호: a promise to return the principal or more, or to make good a loss; 표시광고법 제3조①1호).
- [ ] AC62 The page text contains none of: 스테이킹, 예치 상품, 예치 서비스, 렌딩, 대여 서비스, 레버리지, 마진, 선물 거래, 무기한, 옵션 거래, 파생, 채굴, 마이닝, 노드 분양, 락업 상품 (sample policy: no yield or leverage product; the DAXA rule on these products was not read).
- [ ] AC63 The page text contains none of: 매수 추천, 추천 종목, 추천 코인, 유망 코인, 급등, 떡상, 대박, 저점 매수, 지금 사, 목표가, 리딩, 시그널, 시세 예측, 가격 전망, 수익 인증 (decided by the orchestrator; sample policy. 가상자산이용자보호법 제10조② · ③ bar matched, sham and price-moving trades, not displays; 제10조④2호 bars a misleading display used to gain money).
- [ ] AC64 The page text contains none of: 최고, 최초, 최대, 최다, 최저, 유일, 독보적, 압도적, 1위, 1등, No.1, 넘버원, 업계 선두, 완벽, 보장, 보증, 무조건, 확실 (decided by the orchestrator; 표시광고법 제3조①1 · 3호; 빗썸 shows "압도적 1위").
- [ ] AC65 The page text contains none of: 해킹 불가, 해킹 걱정 없, 무사고, 사고 없, 안전 자산, 안전 보장, 절대 안전, 보험 가입, 보상 한도, 예금자 보호 (sample policy: a fictional business has no security record, and no insurance under 가상자산이용자보호법 제8조).
- [ ] AC66 The page text contains none of: 신고 수리, 신고 완료, 사업자 신고, 신고필, ISMS, 인증 획득, 인허가, 정식 인가, 인가 완료, 정식 허가, 허가 완료, 라이선스, 금융위원회, 금융감독원, 금융정보분석원, FIU, 금융당국, 제도권, 합법 (decided by the orchestrator; 특금법 제7조① · ③1호 and 제17조①: registration and the ISMS certificate are facts a fictional business does not have).
- [ ] AC67 The page text contains none of: 후기, 리뷰, 별점, 평점, 만족도, ★, 수상, 어워드, Award, 누적, 가입자, 회원 수, 이용자 수, 거래액, 거래대금, 거래량, 수탁고, 예치금 규모, 운용 자산, AUM, TVL, 다운로드 수, 파트너사, 투자사, 고객사 (decided by the orchestrator: no fabricated record; 표시광고법 제3조①1호).
- [ ] AC68 The page text contains none of: 무료, 공짜, 할인, 이벤트, 선착순, 마감 임박, 프로모션, 쿠폰, 특가, 사은품, 에어드랍, 에어드롭, 리워드, 캐시백, 추천인, 수수료 면제, 혜택 (sample policy: no lure offer; 코인원 shows "USDT 100% 지급").
- [ ] AC69 The page text names no real exchange, project, foundation, token or wallet brand: it contains none of 업비트, 빗썸, 코인원, 코빗, 고팍스, 바이낸스, 코인베이스, 크라켄, 바이비트, 메타마스크, 팬텀, 카이아, 클레이튼, Upbit, Bithumb, Coinone, Korbit, Gopax, Binance, Coinbase, Kraken, Bybit, OKX, MetaMask, Phantom, Kaia, Klaytn, Uniswap or DAXA, and a person finds no other such name or logo (decided by the orchestrator; human for the last part).
- [ ] AC70 The page text names no real 가상자산: it contains none of 비트코인, 이더리움, 리플, 솔라나, 테더, 도지, 에이다, 바이낸스코인, Bitcoin, Ethereum, Ripple, Solana, Tether or Dogecoin, none of BTC, ETH, XRP, SOL, USDT, USDC, BNB, DOGE, ADA or TRX as a whole word, and a person finds no other real asset name, ticker or coin logo (agent decision, Assumptions; human for the last part).
- [ ] AC71 The page text names no platform other than 네이버 (예약 and 지도 only) and 카카오톡: no social, video, messenger or community platform by name, logo or icon, for example 텔레그램, 디스코드, X, 유튜브, 오픈채팅 (human; sample policy: 리딩방 and 오픈채팅 are where unlawful solicitation happens).
- [ ] AC72 No crypto sample makes, in other words, in English or in a picture, a claim of the kinds listed in AC61–AC68 (human).
- [ ] AC73 No crypto sample shows a partner, investor, press, auditor or certificate logo or badge, or a row of such names (human; Kaia shows a "Backed by" row).
- [ ] AC74 Outside an example block (AC77), the page text contains no digit followed, with optional spaces, by `%`; no digit followed, with optional spaces, by 원, 만, 억, 조, 달러, 명, 건, 배 or 개국, also after 천, 백 or 십; no `₩`, `￦` or `$` next to a digit; and no number with a thousands comma (no price, fee, yield, user count or volume; sample policy). A number alone in one block with one of these units at the start of the next block counts too. Four kinds of digit are not counted: the phone number `02-000-0000`, the 사업자등록번호 `000-00-00000`, a clock time written `HH:MM`, and the 3 of 웹3 or Web3.
- [ ] AC75 No crypto sample states a count of users, assets, trades or clients, an amount held or traded, years in business or a fee, in words or in digits (human; AC74 catches only the listed forms).
- [ ] AC76 The `title`, `summary` and `features` of each crypto sample's `PROFILES` entry (the gallery card text) contain none of the words and digit forms that AC53–AC55, AC61–AC70, AC74 and the sample's own lists (AC85 and AC190 for `crypto-robincoin`; AC95, AC97 and AC251 for `crypto-robinchain`) ban in page text, and nothing that AC71–AC73 forbid; the `title` is the one A15 gives (command for the lists and the title, human for the rest; A20).

Example figures (`crypto-robincoin` only)

An "example block" is an element with the attribute `data-example` that holds the visible text "예시 화면 · 실제 시세가 아닙니다".

- [ ] AC77 Every element whose own text holds a price, an amount or a `%` figure is inside an example block (decided by the orchestrator: figures are marked "예시").
- [ ] AC78 A sample whose 업태 is not 거래소 has no example block.
- [ ] AC79 At 1440 px and at 390 px, the text "예시 화면 · 실제 시세가 아닙니다" of each example block has a computed `font-size` of at least 12 px and lies inside the block's rendered box (browser).
- [ ] AC80 Inside an example block, every asset is named "예시 자산" followed by one Latin capital letter (예시 자산 A, 예시 자산 B), with no ticker and no coin logo (가상자산이용자보호법 제10조④3호: no false price of a 가상자산 used to induce trading; agent decision).
- [ ] AC81 An example block that shows price changes shows at least one rise and at least one fall, and no row is styled as a recommendation (human; AC63).
- [ ] AC82 No example block shows a personal gain: its text contains none of 평가손익, 손익 or 평가 금액, and AC61 bans 수익 there too (decided by the orchestrator: no yield figure; Coinbase's phone screen shows a balance with a gain line).
- [ ] AC83 The sentence of AC58 is also visible inside or directly after each example block (sample policy; 가상자산이용자보호법 제10조④2호).
- [ ] AC84 The figures of an example block are static text in `index.html` (AC48 holds; no price is fetched).

Rules by 업태

A block applies to the sample of that 업태 only.

거래소: `crypto-robincoin` (a 가상자산사업자 under 가상자산이용자보호법 제2조2호 가 · 나 · 마목)

- [ ] AC85 The page text contains none of: 신규 상장, 상장 예정, 거래지원 개시, 원화 마켓 오픈, 거래 대회, 트레이딩 대회, 입금 이벤트 (sample policy: no listing or trading promotion; 업비트 shows a pop-up for a trading race with a token prize).
- [ ] AC86 No element reads as an order ticket: no price or quantity field, and no control whose text is 매수, 매도, 주문, 입금 or 출금 (human; AC47 holds).
- [ ] AC87 No element ranks assets or shows a "급상승", "거래대금" or "인기" list (human; AC63, AC67).

수탁: `crypto-robincustody` (a 가상자산사업자 under 가상자산이용자보호법 제2조2호 라목)

- [ ] AC88 The page text states no cold-storage ratio, no amount under custody, no insurance cover and no client count, in digits or in words (human; 가상자산이용자보호법 제7조③ · 제8조 set duties whose figures a fictional business does not have).
- [ ] AC89 A sentence about how assets are kept describes a method in general words (분리 보관, 다중 승인, 오프라인 보관) and makes no promise of safety (human; AC65).
- [ ] AC90 The page names no client, fund, exchange or institution as a customer (human).

AC91–AC94 were the 리서치 block. No 리서치 sample is built (Decisions after G1, A1), so the four criteria are withdrawn and their numbers are not used again.

웹3 개발사: `crypto-robinchain` (not a 가상자산사업자 by 제2조2호 when it only builds software for other businesses)

- [ ] AC95 The page text contains none of: 토큰 세일, 토큰 판매, ICO, IDO, IEO, 프리세일, 화이트리스트, 민팅, 토큰 분배, 토크노믹스, 백서, 로드맵 상장, 거버넌스 토큰, 재단 물량 (sample policy: the sample issues and sells no token; 유사수신법 제2조 — 가상자산 counts as funds; 가상자산이용자보호법 제10조① names issuers).
- [ ] AC96 The services named in the AC28 section are work done for other businesses (for example 스마트 컨트랙트 개발, 지갑 연동 개발, 노드 운영 대행, 보안 점검 지원), and none is trading, keeping, transferring or exchanging 가상자산 for users (human; 가상자산이용자보호법 제2조2호).
- [ ] AC97 No link or control is labelled as a way into an app: the page text contains none of 앱 실행, 포털 열기, 브리지, 스왑, Launch App, Open App, Bridge or Swap (Kaia's first screen has "Open DeFi Portal" and "Bridge to Kaia").

Fonts and pictures, each crypto sample

- [ ] AC98 Every external stylesheet comes from `fonts.googleapis.com` or from Pretendard on `cdn.jsdelivr.net`.
- [ ] AC99 Every web font request succeeds, and the `<h1>` and the header wordmark render in a loaded web font, not in a fallback or a locally installed copy (browser).
- [ ] AC100 The digits of 상담 hours, phone numbers and example figures render in a Korean typeface or a monospaced face, never in a proportional Latin face with old-style figures (browser).
- [ ] AC101 The first family in the computed `font-family` of each crypto sample's `<body>` is `Pretendard Variable` or `Pretendard` (browser), and its `index.html` links the Pretendard stylesheet on `cdn.jsdelivr.net`.
- [ ] AC102 Every picture that is not a photo is made for the sample as CSS or inline `<svg>` in `index.html` or `style.css`; no `.svg`, `.png` or `.gif` file is in the sample's folder, and no picture copies a reference's illustration, render or mark (human for the last part).
- [ ] AC103 `index.html` and `style.css` contain no `data:` URL, whatever it holds (a raster image, an SVG or a stylesheet).
- [ ] AC104 Every image path referenced in `index.html` and `style.css` (`src`, `srcset`, CSS `url()`) resolves to an existing file inside that sample's `img/`, with the same letter case in every path part.
- [ ] AC105 Every file in a sample's `img/` other than `sources.txt` (dotfiles aside) is a `.jpg` or `.webp` file, and `img/` holds no folder.
- [ ] AC106 A sample with no image file in `img/` has no "Photos:" text in its footer and no `img/sources.txt`.
- [ ] AC107 A sample with an image file in `img/` has a footer "Photos:" credit that names each source used in its `img/sources.txt` (Unsplash, Pexels).
- [ ] AC108 In a sample with an image file in `img/`, `img/sources.txt` has exactly one line per image file (dotfiles aside), written as file name, photo page URL and download URL; the page URL starts with `https://unsplash.com/photos/` or `https://www.pexels.com/photo/`, or is `-`.
- [ ] AC109 Every download URL in an `img/sources.txt` starts with `https://images.unsplash.com/photo-` or `https://images.pexels.com/photos/`, and no line contains `plus.unsplash.com` or `premium_photo`.
- [ ] AC110 No photo ID recorded in a crypto sample's `img/sources.txt` appears in the `img/sources.txt` of any other sample under `profile/`.
- [ ] AC111 No image in `img/` is wider than 2000 px.
- [ ] AC112 No image file in `img/` is larger than 500 KB.
- [ ] AC113 The image files in a sample's `img/` total at most 3 MB (`thumb.jpg` is not counted).
- [ ] AC114 A sample's `img/` holds at most six image files (`sources.txt` and dotfiles aside).
- [ ] AC115 No photo shows a recognisable person, a coin with a real asset's mark, a trading screen, a chart of a real market, a banknote, or a real company's building or sign (human).
- [ ] AC116 A reviewer opens every image file in each crypto sample's `img/` one by one at native resolution and finds no legible logo, brand name, ticker, signage, screen text or other lettering (human).

Not the same site

- [ ] AC117 Each crypto sample shares no text, logo, brand name, illustration or photo with its own reference site (the URL of its candidate in Assumptions).
- [ ] AC118 Side by side with its own reference site, a person does not read a crypto sample as the same site (human).
- [ ] AC119 Side by side with the fifteen shipped samples and the other crypto samples, a person does not read a crypto sample as the same design as any of them (human).
- [ ] AC120 Each crypto sample keeps every layout trait listed for its candidate under "Traits to keep" in the G1 history, as changed by A3, A7, A8 and A12 (section order: in D the bento cards come before the lime band) in Decisions after G1 (human; the measurable forms are AC150–AC251).
- [ ] AC121 The accent (the last `palette` hex) of each crypto sample's `PROFILES` entry differs from the accent of every other `PROFILES` entry, and no hex appears in the `palette` of more than one crypto sample (case-insensitive).
- [ ] AC122 Each crypto sample's `style.css` contains the accent hex of its `PROFILES` entry (case-insensitive).
- [ ] AC123 No crypto sample's `<h1>` is a translation or close paraphrase of its reference's headline (human).
- [ ] AC124 No crypto sample's `index.html` or `style.css` names a typeface of its reference (Assumptions, "Reference fonts and colours"; any case).

The crypto samples against each other

- [ ] AC125 The first families in the computed `font-family` of the crypto samples' `<h1>`s are pairwise different (browser).
- [ ] AC126 The first families in the computed `font-family` of the crypto samples' header wordmarks are pairwise different (browser).
- [ ] AC127 Side by side, the crypto samples differ pairwise in wordmark position and size, in palette, in typeface and in first-screen composition, and no two wordmarks read as one mark with a suffix added (human; decided by the orchestrator).
- [ ] AC128 At most one crypto sample has a `body` background colour whose HSL lightness is below 0.2 (the genre leans to dark pages with neon gradients; decided by the orchestrator).

Accessibility and motion, each crypto sample

- [ ] AC129 Every `<img>` has a non-empty `alt`, and every inline `<svg>` that carries meaning has an accessible name or is hidden with `aria-hidden="true"` beside a text that says the same.
- [ ] AC130 The page has exactly one `<h1>`, and no heading level is skipped.
- [ ] AC131 Under `prefers-reduced-motion: reduce`, at 1440 px and at 390 px, no element runs or declares an animation or transition longer than 0.01 s (browser).
- [ ] AC132 At 1440 px and at 390 px, every element with its own text that does not overlap an `<img>` has a contrast ratio of at least 4.5:1 between its computed colour and the nearest non-transparent background behind it, or at least 3:1 when its computed `font-size` is 24 px or more (browser).

Full-page checks, each crypto sample

- [ ] AC133 At 1440 px width, the full page has no horizontal overflow (browser).
- [ ] AC134 At 390 px width (page inside a `width:390px` iframe), the full page has no horizontal overflow (browser).
- [ ] AC135 A full-page screenshot at 1440 px shows no overlapping or clipped text (browser, human review).
- [ ] AC136 A full-page screenshot at 390 px shows no overlapping or clipped text (browser, human review).

Gallery (served by `python3 -m http.server 8000`)

- [ ] AC137 On `/profile/`, the `crypto` filter shows one card per crypto sample (browser).
- [ ] AC138 On `/profile/`, the `crypto` filter shows no "준비 중" tile (browser).
- [ ] AC139 In the generated `profile/index.html`, the `crypto` filter chip shows the number of `crypto` entries in `PROFILES` as its count.
- [ ] AC140 Clicking each crypto card opens the preview with that sample loaded in the iframe (browser).
- [ ] AC141 For each crypto card, the preview's desktop and mobile buttons switch the iframe between desktop and mobile width (browser).
- [ ] AC142 For each crypto card, pressing Esc closes the preview (browser).

Reconciliation

- [ ] AC143 The Source line of `docs/current_system/profile-samples/component.md` lists each crypto sample's slug.
- [ ] AC144 `git diff` from the `last_reconciled` commit in `docs/current_system/overview.md` to `HEAD` shows no change outside `docs/`.

Added after G1, each crypto sample

- [ ] AC145 The `content` of each crypto sample's `meta name="description"` contains "디자인 샘플".
- [ ] AC146 Every `og:title` and `og:description` in each crypto sample has a `content` that contains "디자인 샘플" (sample policy: a shared link preview says it is a sample).
- [ ] AC147 At 1440 px and at 390 px, the AC12 element has a computed `font-size` of at least 14 px, at scroll position 0 and at the end of the page (browser).
- [ ] AC148 In `crypto-robincoin` and `crypto-robincustody`, at 1440 px and at 390 px, the first-screen sentence of AC32 has a computed `font-size` of at least 14 px (browser).
- [ ] AC149 In each crypto sample at 390 px, at scroll position 0 and at mid-page, the fixed and sticky elements pinned to the top or bottom of the viewport cover at most 220 px of its height together (browser), and no rule of the sample's CSS whose selector has `::before` or `::after` declares a `position` other than `absolute`, `relative` or `static`, so that every such bar is an element the check counts.

Per-sample criteria. An AC marked (browser) below is measured in a 1440×900 viewport on load unless it names 390 px. 390 px means a 390×844 viewport; AC134 alone is measured inside a `width:390px` iframe. "The service section" is the AC28 section, "the steps section" is the AC29 section, and "the contact section" is the AC30 section. "The first section" is the part of the page from its top to the start of the service section, the `<header>` and any fixed or sticky bar aside. A link "outside the bars" is outside the `<header>` and outside any fixed or sticky bar. The horizontal edges and the horizontal centre of an `<h1>` and of a header wordmark are those of its rendered text, not of the element's box.

Sample A, `profile/crypto-robincoin/` (로빈코인; 거래소; reference Coinbase, coinbase.com)

"The panel" is the first example block in document order and "the asset card" is the second. "The phone" is the phone-screen element inside the panel. A "change figure" is an element whose own text ends in `%`.

- [ ] AC150 The `PROFILES` entry for `crypto-robincoin` has `name` "로빈코인" and `palette` `["#ffffff", "#0c1222", "#eef2f7", "#0a69c7"]`, in that order.
- [ ] AC151 In `crypto-robincoin/style.css` (custom properties resolved), the `body` background colour is `#ffffff` and the `body` text colour is `#0c1222` (the white page kept).
- [ ] AC152 Every RGB channel of the computed background colour of the `crypto-robincoin` `<header>` is at least `0xF8`, that colour is opaque, and the `<header>` box spans the full viewport width (the white bar kept) (browser).
- [ ] AC153 The left edge of the `crypto-robincoin` header wordmark is within 64 px of the viewport's left edge (browser).
- [ ] AC154 The first family in the computed `font-family` of the `crypto-robincoin` header wordmark is `Pretendard Variable` or `Pretendard`, its computed `font-size` is from 23 px to 25 px, and its computed `font-weight` is at least 700 (browser).
- [ ] AC155 The `crypto-robincoin` `<header>` holds exactly one link with the text "로그인" and exactly one with the text "회원가입"; each has `href="#"`, the computed background colour `#eef2f7` and the computed colour `#0c1222` (AC56; grey, so that neither is the main action) (browser).
- [ ] AC156 The `crypto-robincoin` `<header>` holds a link whose `href` is `#<id>` of the contact section and whose text contains "문의"; its computed background colour is `#0a69c7`, its computed colour is `#ffffff`, and no header link has a right edge further right (browser).
- [ ] AC157 Each of the three links of AC155 and AC156 has a computed `border-radius` of at least half its rendered height (the pill buttons at the right kept) (browser).
- [ ] AC158 At 390 px, the AC156 link is visible in the header without scrolling (browser).
- [ ] AC159 `crypto-robincoin` has exactly two example blocks.
- [ ] AC160 The panel lies fully inside the viewport, its left edge is within 144 px of the viewport's left edge, its width is from 480 px to 660 px, and its height is from 480 px to 720 px (browser).
- [ ] AC161 The panel has a computed `border-radius` of at least 32 px and a computed `background-image` that is a `linear-gradient`, and it holds no `<img>` (the rounded blue panel kept) (browser).
- [ ] AC162 `crypto-robincoin/style.css` contains `#3f9cf0` and `#06357a`, the two ends of the panel gradient (case-insensitive).
- [ ] AC163 The panel holds exactly one phone: an element whose top corners have a computed radius of at least 28 px, whose computed background colour is opaque with every RGB channel at least `0xF4`, whose width is from 280 px to 400 px, whose left and right edges lie inside the panel, and whose top edge is at least 24 px below the panel's top edge (browser).
- [ ] AC164 The text "예시 화면 · 실제 시세가 아닙니다" of the panel is the first text inside the phone, and at 1440 px and at 390 px its computed `font-size` is at least 13 px (a crop of the phone still carries it) (browser).
- [ ] AC165 That text of the panel is visible without scrolling at 1440 px (browser).
- [ ] AC166 The element with the largest computed `font-size` inside the phone has own text made of a number and 원, and the text directly before it in the phone is "예시 자산 A" (the top figure is one asset's example price, not a balance) (browser).
- [ ] AC167 The text of each example block contains none of: 잔고, 보유, 총 자산, 내 자산, 자산 현황, 포트폴리오, 입금, 출금 (human decision A3: no balance and no gain line; AC75).
- [ ] AC168 The phone holds exactly one inline `<svg>` with `aria-hidden="true"`, and that `<svg>` holds exactly one `<polyline>` (the price line).
- [ ] AC169 Along the points of that `<polyline>`, y goes up at least once and down at least once, and the last point is not the point with the smallest y (the line does not end at its high; AC63).
- [ ] AC170 The phone holds a list of at least three rows; each row holds a name "예시 자산" plus one Latin capital, a price that ends in 원 and one change figure.
- [ ] AC171 Every change figure in an example block starts with `+` or `−` (U+2212) (the direction is not shown by colour alone).
- [ ] AC172 Each example block holds at least one change figure that starts with `+` and at least one that starts with `−` (the measurable form of AC81).
- [ ] AC173 The computed colour of every change figure that starts with `+` is `#c8323c`, and of every one that starts with `−` is `#0a69c7` (the Korean convention: red for a rise, blue for a fall; Coinbase shows a rise in green) (browser).
- [ ] AC174 Every element in an example block whose own text holds a digit has `Pretendard Variable` or `Pretendard` as the first computed family and a computed `font-variant-numeric` that includes `tabular-nums` (browser).
- [ ] AC175 No example block holds an `<a>`, an element with a `tabindex` attribute, or an element whose computed `cursor` is `pointer` (browser).
- [ ] AC176 The phone shows no drawn search field, no input-shaped box, no keypad and no order button, and does not repeat the top bar of Coinbase's phone screen (menu icon, search field, bell) (human).
- [ ] AC177 The left edge of the `crypto-robincoin` `<h1>` is at least 40 px to the right of the panel's right edge, and the `<h1>` lies fully inside the viewport (the headline beside the panel kept) (browser).
- [ ] AC178 The first family in the computed `font-family` of the `crypto-robincoin` `<h1>` is `Pretendard Variable` or `Pretendard`, its computed `font-size` is from 56 px to 80 px, its computed `font-weight` is from 600 to 800, and its computed colour is `#0c1222` (browser).
- [ ] AC179 The `crypto-robincoin` `<h1>` box is from 1.9 to 2.9 times as tall as its computed `font-size` (two lines) (browser).
- [ ] AC180 The first section of `crypto-robincoin` holds exactly two links outside the bars and outside the panel: one whose text is "고객센터 문의" and whose `href` is `#<id>` of the contact section, and one whose text is "서비스 보기" and whose `href` is `#<id>` of the service section (two links in place of Coinbase's e-mail field and "Sign up" button).
- [ ] AC181 The "고객센터 문의" link of AC180 has the computed background colour `#0a69c7`, the computed colour `#ffffff` and a computed `border-radius` of at least half its rendered height (browser).
- [ ] AC182 At 390 px, the `crypto-robincoin` `<h1>` has a computed `font-size` of at least 32 px, lies fully inside the viewport on load, and is not covered by a fixed or sticky element (browser).
- [ ] AC183 At 390 px, the panel comes below the `<h1>`, its top edge is at most 720 px below the top of the viewport on load, its width is at least 300 px, and the phone is at least 240 px wide (browser).
- [ ] AC184 `crypto-robincoin` has a dark panel: an element with the computed background colour `#0c1222` and a computed `border-radius` of at least 32 px, with a gap of at least 24 px to each side edge of the viewport at 1440 px, that holds the `<ol>` of the steps section (the dark rounded panel kept) (browser).
- [ ] AC185 The dark panel holds no example block, no `<svg>` chart and no digit in its text (it shows the steps, not Coinbase's trading screen; AC86).
- [ ] AC186 The asset card has the computed background colour `#ffffff` and a computed `border-radius` of at least 24 px, and it sits in a band that spans the full viewport width with the computed background colour `#eef2f7` (the card of asset rows on a grey band kept; Coinbase's card is black) (browser).
- [ ] AC187 The asset card holds at least four rows of the AC170 shape, and their names run in letter order from 예시 자산 A (no ranking; AC87).
- [ ] AC188 In `crypto-robincoin`, the service section comes before the dark panel, the dark panel before the asset card, and the asset card before the contact section (document order).
- [ ] AC189 The heading of the `crypto-robincoin` contact section contains "고객센터".
- [ ] AC190 The page text of `crypto-robincoin` contains none of: 거래하기, 거래 시작, 지금 거래, 계정 만들기, 계좌 개설, 본인 인증, 인증하기, 간편 가입, KYC, 가입하기, 시작하기 (sample policy against a phishing reading: no label invites a visitor to trade or to open an account).
- [ ] AC191 `crypto-robincoin/style.css` contains none of `#0052ff`, `#2d60ef` or `#001767` (case-insensitive; Coinbase's blues, read on 2026-11-20).
- [ ] AC192 A mark beside the `crypto-robincoin` wordmark, if there is one, is not a filled blue circle with a C-shaped opening (human; Coinbase's mark).

Sample B, `profile/crypto-robincustody/` (로빈커스터디; 수탁; reference Copper, copper.co)

"The drawing" is the line drawing of the first section. "The word cards" are the three cards that replace Copper's figure cards.

- [ ] AC193 The `PROFILES` entry for `crypto-robincustody` has `name` "로빈커스터디" and `palette` `["#f5c08a", "#2a1d14", "#fffdf9", "#7b2338"]`, in that order.
- [ ] AC194 In `crypto-robincustody/style.css` (custom properties resolved), the `body` background colour is `#f5c08a` and the `body` text colour is `#2a1d14` (the flat warm page kept).
- [ ] AC195 At 1440 px and at 390 px, on load, no element whose computed `background-image` is other than `none` intersects the `crypto-robincustody` viewport (one flat colour, no gradient) (browser).
- [ ] AC196 At 1440 px and at 390 px, the bottom edge of the first section of `crypto-robincustody` is at or below the bottom of the viewport on load, and the nearest non-transparent background behind it is `#f5c08a` (the colour fills the first screen) (browser).
- [ ] AC197 Every RGB channel of the computed background colour of the `crypto-robincustody` `<header>` is at least `0xF8`, that colour is opaque, its computed `border-radius` is at least half its rendered height, and its height is from 60 px to 88 px (the white pill header kept) (browser).
- [ ] AC198 The `crypto-robincustody` `<header>` has a gap of at least 40 px to each side edge of the viewport at 1440 px, the two gaps differing by at most 4 px, and a gap of at least 12 px to each side at 390 px (browser).
- [ ] AC199 At 1440 px, the nearest non-transparent background at the points 6 px above the top edge and 6 px below the bottom edge of the `crypto-robincustody` `<header>` is `#f5c08a` (the pill floats on the colour) (browser).
- [ ] AC200 The horizontal centre of the `crypto-robincustody` header wordmark is within 24 px of the viewport's horizontal centre (browser).
- [ ] AC201 The first family in the computed `font-family` of the `crypto-robincustody` header wordmark is `Noto Serif KR`, its computed `font-weight` is 700, and its computed `font-size` is from 28 px to 32 px (browser).
- [ ] AC202 The right edge of the `<nav>` box in the `crypto-robincustody` `<header>` is left of the wordmark's left edge (browser).
- [ ] AC203 The `crypto-robincustody` `<header>` holds a link whose `href` is `#<id>` of the contact section and whose text contains "도입 문의"; it lies right of the wordmark, and it has the computed background colour `#7b2338`, the computed colour `#fffdf9` and a computed `border-radius` of at least half its rendered height (browser).
- [ ] AC204 At 390 px, the AC203 link is visible in the header without scrolling (browser).
- [ ] AC205 Every link in the `crypto-robincustody` `<header>` has visible text that contains at least one Hangul syllable (no icon-only link; Copper's header has an account icon).
- [ ] AC206 The left edge of the `crypto-robincustody` `<h1>` is within 144 px of the viewport's left edge, its right edge is at most 800 px from that edge, and the `<h1>` lies fully inside the viewport (browser).
- [ ] AC207 The first family in the computed `font-family` of the `crypto-robincustody` `<h1>` is `Noto Sans KR`, its computed `font-weight` is 300, its computed `font-size` is from 52 px to 76 px, and its computed colour is `#2a1d14` (browser).
- [ ] AC208 The `crypto-robincustody` `<h1>` holds one or two `<em>`; each has `Noto Serif KR` as the first computed family, the computed `font-weight` 700, the computed `font-style` `normal` and the computed `font-size` of the `<h1>` (the second, heavier face kept; Hangul has no italic) (browser).
- [ ] AC209 The text of each AC208 `<em>` contains at least one Hangul syllable, and the `<h1>` has text outside every `<em>`.
- [ ] AC210 The first section of `crypto-robincustody` holds exactly one link outside the bars: its text contains "도입 문의", its `href` is `#<id>` of the contact section, and it has the computed background colour `#2a1d14`, the computed colour `#fffdf9` and a computed `border-radius` of at least half its rendered height (browser).
- [ ] AC211 The first section of `crypto-robincustody` holds exactly one inline `<svg>` with `aria-hidden="true"` (the drawing); its left edge is at or right of the viewport's horizontal centre, its width is from 360 px to 560 px, and it lies fully inside the viewport (the line drawing at the right kept) (browser).
- [ ] AC212 The drawing holds at least six shape elements (`<path>`, `<rect>`, `<line>`, `<polygon>`, `<polyline>`, `<circle>`); each has the computed `fill` `none` or a rendered box at most 16 px wide, and each stroked one has the computed `stroke` `#2a1d14` (browser).
- [ ] AC213 The drawing holds no `<ellipse>`, no `<text>` and no `<circle>` rendered wider than 16 px (not Copper's sphere of ellipses) (browser).
- [ ] AC214 At 390 px, the `crypto-robincustody` `<h1>` has a computed `font-size` of at least 30 px, lies fully inside the viewport on load, and is not covered by a fixed or sticky element (browser).
- [ ] AC215 At 390 px, the drawing is displayed below the `<h1>` and is at least 200 px wide (browser).
- [ ] AC216 `crypto-robincustody` has a row of exactly three word cards; each holds one term whose computed `font-size` is at least 40 px at 1440 px and whose text is Hangul syllables and spaces only, and one paragraph (word cards in place of Copper's figure cards; human decision A3) (browser).
- [ ] AC217 The term of each word card has `Noto Serif KR` as the first computed family and the computed `font-weight` 700 (browser).
- [ ] AC218 The top edges of the three word cards lie within 4 px of each other at 1440 px, and the three stack in one column at 390 px (browser).
- [ ] AC219 In `crypto-robincustody`, no element whose own text contains a digit has a computed `font-size` above 24 px (no figure such as Copper's "$105bn"; AC88) (browser).
- [ ] AC220 At 1440 px, at least two elements of `crypto-robincustody` that are 900 px wide or wider have the computed `border-top-style` `dashed` (the dashed rules between sections kept) (browser).
- [ ] AC221 In `crypto-robincustody/style.css`, every colour in a `background`, `background-color` or `background-image` value (`:hover` and `@media` rules included) whose largest RGB channel minus its smallest is above `0x30` is `#f5c08a` or `#7b2338` at full opacity (case-insensitive; two colours and no other, so no mint button like Copper's).
- [ ] AC222 `crypto-robincustody/style.css` contains neither `#fdbda4` nor `#222426` (case-insensitive; Copper's page and text colours, read on 2026-11-20).
- [ ] AC223 The heading of the `crypto-robincustody` contact section contains "도입".

Sample D, `profile/crypto-robinchain/` (로빈체인; 웹3 개발사; reference Kaia, kaia.io)

"The object" is the lit picture of the first section. "The band" is the steps section.

- [ ] AC224 The `PROFILES` entry for `crypto-robinchain` has `name` "로빈체인" and `palette` `["#07090a", "#f2f5ee", "#161a1c", "#a9ef2c"]`, in that order.
- [ ] AC225 In `crypto-robinchain/style.css` (custom properties resolved), the `body` background colour is `#07090a` and the `body` text colour is `#f2f5ee` (the black page kept; HSL lightness 0.03).
- [ ] AC226 The `crypto-robinchain` `<header>` has a computed `backdrop-filter` (or `-webkit-backdrop-filter`) that contains `blur`, and a computed background colour whose alpha is from 0.75 to 0.92 and whose RGB channels are each at most `0x30` (the glass bar kept; dark enough that the lime wordmark stays readable when the band passes under it) (browser).
- [ ] AC227 The computed `position` of the `crypto-robinchain` `<header>` is `fixed` or `sticky`, and its computed background, `backdrop-filter`, `border-radius`, width and height are the same at scroll position 0 and at 1200 px (a glass bar from the start; Kaia changes its header on scroll by script) (browser).
- [ ] AC228 The `crypto-robinchain` `<header>` has a computed `border-radius` of at least half its rendered height, a gap of at least 120 px to each side edge of the viewport at 1440 px, the two gaps differing by at most 4 px, and a gap of at least 12 px to each side at 390 px (browser).
- [ ] AC229 The left edge of the `crypto-robinchain` header wordmark is from 150 px to 260 px from the viewport's left edge (browser).
- [ ] AC230 The first family in the computed `font-family` of the `crypto-robinchain` header wordmark is `Gasoek One`, its computed colour is `#a9ef2c`, and its computed `font-size` is from 35 px to 38 px at 1440 px and from 30 px to 34 px at 390 px (browser); in a screenshot at device scale 1 a person reads the name as 로빈체인 (human for the last part; A19).
- [ ] AC231 The `crypto-robinchain` `<h1>` holds exactly three child `<span>` elements and no text outside them, and each `<span>` has the computed `display` `block` (browser).
- [ ] AC232 At 1440 px and at 390 px, the box of each AC231 `<span>` is at most 1.5 times as tall as its computed `font-size` (three lines, one per `<span>`) (browser).
- [ ] AC233 The computed colour of the second AC231 `<span>` is `#a9ef2c`, and that of the first and the third is `#f2f5ee` (the middle line in lime kept) (browser).
- [ ] AC234 The first family in the computed `font-family` of the `crypto-robinchain` `<h1>` is `Gasoek One`, and its computed `font-size` is from 60 px to 84 px at 1440 px and at least 30 px at 390 px (the wide heavy face kept) (browser).
- [ ] AC235 The left edge of the `crypto-robinchain` `<h1>` is within 200 px of the viewport's left edge at 1440 px, and at 1440 px and at 390 px the `<h1>` lies fully inside the viewport on load and is not covered by a fixed or sticky element (browser).
- [ ] AC236 The first section of `crypto-robinchain` holds exactly two links outside the bars: the first has text that contains "프로젝트 문의" and the `href` `#<id>` of the contact section, and the second has the text "서비스 보기" and the `href` `#<id>` of the service section (in place of Kaia's "Open DeFi Portal" and "Bridge to Kaia"; AC97).
- [ ] AC237 The first AC236 link has the computed background colour `#a9ef2c` and the computed colour `#07090a`; the second has the computed background colour `#161a1c` and the computed colour `#f2f5ee`; each has a computed `border-radius` of at least half its rendered height (the two pill buttons kept) (browser).
- [ ] AC238 At 1440 px, the top edges of the two AC236 links lie within 4 px of each other and below the bottom edge of the `<h1>` (browser).
- [ ] AC239 The first section of `crypto-robinchain` holds exactly one inline `<svg>` with `aria-hidden="true"` that is not inside a link (the object); its left edge is at or right of the viewport's horizontal centre, its width is from 300 px to 560 px, and it lies fully inside the viewport (the lit object at the right kept) (browser).
- [ ] AC240 The object or the element that wraps it has a computed `filter` that contains `drop-shadow` or `blur`, or a computed `background-image` that contains `radial-gradient` (the light kept) (browser).
- [ ] AC241 The object holds no `<text>`, shows no letter or symbol, and is not one rounded-rectangle slab (human for the last two parts; Kaia's object is a glass slab with a glyph in it).
- [ ] AC242 At 390 px, the object is displayed and is at least 160 px wide (browser).
- [ ] AC243 The service section of `crypto-robinchain` holds at least four cards, each with the computed background colour `#161a1c` and a computed `border-radius` of at least 20 px (the dark bento cards kept) (browser).
- [ ] AC244 At 1440 px, the widest and the narrowest of the AC243 cards differ in width by at least 80 px, and at 390 px the cards stack in one column (browser).
- [ ] AC245 The band of `crypto-robinchain` has the computed background colour `#a9ef2c`, a computed `border-radius` of at least 32 px and, at 1440 px, a width of at least 90 % of the viewport; the computed colour of its text is `#07090a` (the lime band kept) (browser).
- [ ] AC246 The `<ol>` of the band holds exactly three `<li>` cards; at 1440 px the three sit side by side with no horizontal overlap, and their top edges differ pairwise by at least 16 px (the three staggered cards kept) (browser).
- [ ] AC247 At 390 px, the three AC246 cards stack in one column (browser).
- [ ] AC248 In `crypto-robinchain`, the service section comes before the band, and the band before the contact section (document order; Kaia has the band first).
- [ ] AC249 In `crypto-robinchain/style.css` and in the colour attributes of the inline `<svg>` elements of its `index.html`, every colour whose largest RGB channel minus its smallest is above `0x30` has an HSL hue from 74° to 90°, at any opacity (one lime and no second colour).
- [ ] AC250 `crypto-robinchain/style.css` contains no `#bff009` (case-insensitive; Kaia's lime, read on 2026-11-20).
- [ ] AC251 The page text of `crypto-robinchain` contains none of: 재단, 그랜트, 생태계 기금 (sample policy: the sample is a 개발사, and Kaia is a foundation; AC95).

All three crypto samples

- [ ] AC252 Each crypto sample's `index.html` requests from `fonts.googleapis.com`: no family in `crypto-robincoin`; exactly `Noto Sans KR` and `Noto Serif KR` in `crypto-robincustody`; exactly `Gasoek One` in `crypto-robinchain`.
- [ ] AC253 Every element whose first computed family is `Gasoek One` has the computed `font-weight` 400 (the face has one weight; no synthesised bold) (browser).
- [ ] AC254 In each crypto sample's contact section, the elements that show the 상담 hours and the phone number have `Pretendard Variable` or `Pretendard` as the first computed family (the measurable form of AC100) (browser).
- [ ] AC255 Each crypto sample's `<header>` holds a `<nav>` with at least four links; each has an `href` that starts with `#` and text that contains at least one Hangul syllable and no Latin letter.
- [ ] AC256 The accessible name of each crypto sample's header wordmark is exactly the `name` of its `PROFILES` entry.
- [ ] AC257 Each crypto sample's header wordmark is live text, not a picture of text.
- [ ] AC258 At 1440 px, the horizontal centres of the three header wordmarks differ pairwise by at least 60 px (browser).
- [ ] AC259 At 1440 px, the computed `font-size` values of the three header wordmarks differ pairwise by at least 3 px (browser).
- [ ] AC260 At 1440 px, the horizontal centre of the `<h1>` is in the right half of the viewport in `crypto-robincoin` and in the left half in `crypto-robincustody` and `crypto-robinchain` (browser).
- [ ] AC261 At 1440 px, the `crypto-robincustody` `<h1>` box is from 1.9 to 3.9 times as tall as its computed `font-size` (two or three lines; AC179 and AC232 hold the line counts of the other two) (browser).
- [ ] AC262 No crypto sample has an `<img>` element or an `img/` folder (agent decision A6: pictures are CSS and inline SVG).
- [ ] AC263 At 390 px, the computed `font-size` values of the three header wordmarks differ pairwise by at least 2 px (browser).
- [ ] AC264 Side by side, the three `thumb.jpg` files show three different first screens: a white page with a blue panel at the left, a flat apricot page with a white pill header, and a black page with lime type (human).

## Assumptions

- The industry key is `crypto` with the label 코인 · 가상자산; it already exists in `INDUSTRIES` in `scripts/profiles.py`, and no `PROFILES` entry uses it yet (checked 2026-11-20).
- **Naming (human decision, binding).** Each sample's name is "로빈" plus a field word (로빈코인, 로빈커스터디, 로빈체인), so the name alone shows it is a sample. This feature runs no name-collision check and writes no `name-check.txt`. This overrides "상호는 가상" in playbook §2; the rest of §2 holds. The slug is `crypto-` plus the name in Latin letters (AC4).
- **Decided by the orchestrator (binding for this run).** No yield, interest or guaranteed-return figure and no "원금 보장" wording (AC61); no recommendation of a coin (AC63); no superlative or first-place claim (AC64); no fabricated reviews, awards or user counts (AC67); no fake 가상자산사업자 신고번호 or ISMS 인증번호 (AC24, AC66); no named person (AC27); no real exchange, project, foundation or wallet brand or logo (AC69); no live price API, and "예시" on any figure (AC77, AC48); no working sign-up, login, wallet connection, deposit address or input form, and every link a `#` placeholder (AC47–AC57); a risk notice (AC58); the sample marker at body size or larger (AC10); different wordmark position and size per sample (AC127).
- **Real coin names and tickers (agent decision).** No sample names a real 가상자산 or shows its ticker or logo (AC70). Reason: 가상자산이용자보호법 제10조④3호 bars a false price of a 가상자산 used to induce trading. A made-up price beside 비트코인 or BTC on a public page is a false price of a real asset. Example rows are named "예시 자산 A" and so on (AC80). The generic words 가상자산, 디지털자산, 코인, 토큰, 블록체인, 스테이블코인 and 원화 stay allowed; 로빈코인 holds 코인.
- **No script (agent decision).** No sample has a `<script>` (AC48). Thirteen of the fifteen shipped samples have none. A page that looks like an exchange and runs no code cannot collect or send anything.
- **Sticky marker and non-business notice (agent decision).** The sample marker stays on screen at every scroll position (AC12), as the law samples do. The contact section says the business is not a 가상자산사업자 and offers no service (AC31); for 거래소 and 수탁 the sentence is also on the first screen (AC32).
- **Login and sign-up labels (agent decision).** The 거래소 sample shows 로그인 and 회원가입 as `#` links in its header, once each (AC155), because an exchange header without them does not read as an exchange (AC56). No other sample shows them.
- **Contact shape (agent decision).** Every sample has 카카오톡 상담, 전화, 네이버 예약 (방문 상담 예약) and 네이버 지도 (오시는 길) as `#` links in its contact section (AC35–AC38), and a 문의 link that stays on the 390 px screen (AC42). The main action by 업태: 거래소 고객센터 문의, 수탁 도입 문의, 웹3 개발사 프로젝트 문의. No e-mail link is used (AC49).
- **업태 of the samples.** 웹3 개발사 means a company that builds software for other businesses; it is not a foundation and issues no token (AC95). 거래소 and 수탁 are the two 업태 that the Act lists as 가상자산사업자, so their samples carry the non-business sentence on the first screen (AC32).
- **Kept traits (human decision, law run 2026-11-18; applied here by the orchestrator). This adjusts playbook §1-4 and §2: the listed traits of the picked screenshot stay, and everything else is made new.** "Not the same site" is met through pictures, palette, typeface, copy and section order (AC117, AC118, AC123), never by removing a kept trait. Where a content rule removes or changes a trait that the screenshot shows, the candidate lists it under "Conflicts", and A3 records the human's answer.
- **Rule sources, read on 2026-11-20 in Chrome on law.go.kr (국가법령정보센터).**
  - 가상자산 이용자 보호 등에 관한 법률 [시행 2026-10-02, 법률 제21857호], `https://www.law.go.kr/법령/가상자산이용자보호등에관한법률`. 제2조1호 (가상자산), 제2조2호 (가상자산사업자: 매매, 교환, 대통령령으로 정하는 이전, 보관 또는 관리, 매매 · 교환의 중개 · 알선 · 대행을 영업으로 하는 자), 제4조, 제7조② · ③ (분리 보관, 인터넷과 분리한 보관 비율), 제8조 (보험 · 공제 · 준비금), 제10조① (가상자산을 발행하는 자 포함), 제10조② · ③ (통정매매 · 가장매매 and 시세를 변동시키는 매매: rules on trades, not on displays), 제10조④2호 (중요사항의 거짓 표시 또는 누락) and 3호 (매매를 유인할 목적의 거짓 시세). The article titles 제1조–제22조 were read; none is about 광고. The Act has no advertising article.
  - 특정 금융거래정보의 보고 및 이용 등에 관한 법률 [시행 2026-10-02], `https://www.law.go.kr/법령/특정금융거래정보의보고및이용등에관한법률`. 제2조1호 하목 (가상자산사업자 is the one of 가상자산이용자보호법 제2조2호), 제7조① (신고 to the 금융정보분석원장), 제7조③1호 (정보보호 관리체계 인증) and 2호 (실명확인 입출금 계정), 제17조① (미신고 영업: 5년 이하 징역 또는 5천만원 이하 벌금).
  - 표시 · 광고의 공정화에 관한 법률 [시행 2025-01-21, 법률 제20712호], `https://www.law.go.kr/법령/표시ㆍ광고의공정화에관한법률`. 제3조①1–4호 (거짓 · 과장, 기만, 부당 비교, 비방).
  - 유사수신행위의 규제에 관한 법률 [시행 2024-05-28, 법률 제20367호], `https://www.law.go.kr/법령/유사수신행위의규제에관한법률`. 제2조 (자금에 가상자산 포함; 특금법 제7조 신고를 하지 않은 경우 포함; 1 · 2 · 4호), 제3조, 제4조 (유사수신행위를 위한 표시 · 광고 금지).
  - 금융소비자 보호에 관한 법률 [시행 2026-01-02, 법률 제21065호], `https://www.law.go.kr/법령/금융소비자보호에관한법률`. 제2조1호 가–바목 lists 예금 · 대출, 금융투자상품, 보험상품 and the like. The word 가상자산 does not appear anywhere in the Act's text. So this spec takes no rule from it.
  - 자본시장과 금융투자업에 관한 법률 [시행 2026-11-13], 제101조①: 유사투자자문업 is advice on 금융투자상품 for a fee. The article does not name 가상자산.
- **Not verified against a primary source.**
  - DAXA 「가상자산사업자의 광고 · 홍보 행위 모범규준」 (`26.6.4. 개정). `https://www.kdaxa.org/support/regulation.php` lists it (item 13 of 14, posted 2025-11-13). Its text is an attached file only, and this stage downloads no file. Content not read. A title search of the DAXA press board (`/support/press.php`) for 광고 returned no post. AC58, AC62, AC68 and AC85 are written on the strict side for that reason.
  - 금융위원회 and 금융정보분석원 guidance pages: not opened (no page of fsc.go.kr or kofiu.go.kr was visited). The DAXA home page links a "[금융정보분석원] 가상자산사업자 신고 현황(2026.10.30. 기준)" notice; it was not read.
  - 가상자산이용자보호법 시행령 and 감독규정 (which 이전 행위 count, the cold-storage ratio, insurance standards), 표시광고법 시행령, and 금융소비자보호법 시행령 (제2조1호 바목) were not read.
  - Whether a given 가상자산 is a 금융투자상품 (증권) under 자본시장법, and whether paid advice on 가상자산 needs a registration. No built sample offers advice or a fund, so the point is left open.
  - Whether a company that only builds software is outside 제2조2호 in every case. AC96 keeps the sample's services away from the listed acts.
- **Reference fonts and colours (read 2026-11-20, Chrome, computed styles and screenshot pixels of the home pages).** Coinbase: `CoinbaseDisplay`, `CoinbaseSans`; white page; hero panel a blue gradient from about `#2d60ef` to `#001767`; brand blue near `#0052ff` (hue 221°). Copper: `regola`, `richmond-text`; hero `#fdbda4` (hue 17°), text `#222426`. Hashed: `SangBleu Kingdom` (weight 300), `Matter`; page `#f4f4f4`. Kaia: `owners-wide`, `Manrope`; page `#000000`, lime `#bff009` (hue 73°).
- **Accent hues today (from `scripts/profiles.py`, 2026-11-20).** Chromatic accents: 9°, 19°, 31°, 36°, 60°, 134°, 168°, 197°, 230°, 266°, 303°, 329°, 342°. Achromatic: `#2a2a2a`, `#8a847a`. Under the beauty feature's rule (25° from every other accent) one band is free: about 85°–109° (yellow-green). That rule does not apply here (A2).
- **Shipped samples seen (the fifteen `thumb.jpg` files, side by side, 2026-11-20).** Dark first screens: `beauty-robinhair` (brown-black photo), `flower-bomgyeol` (dark flower photo), `law-ganeum` (graphite, no photo), `interior-robinhome` (ink blue, inset photo). Flat saturated colour: `interior-robindesign` (pink and teal halves). White or near white: `clinic-neuru`, `clinic-bonui`, `clinic-byeotteul`, `fitness-mideoum`, `beauty-robinsalon`, `interior-robininterior`. Cream or grey: `food-saebyeokmil`, `fitness-jjuuk`, `beauty-robinhairsalon`, `law-goim`. No shipped sample has a product-screen mock, a flat peach page, a page of numbered serif statements with no hero, or a black page with one acid colour.
- §6-1 check: the orchestrator ran `git diff --stat 30706b2..HEAD` (the `last_reconciled` in `overview.md`): one `overview.md` line and SHA updates in the interior documents, all under `docs/`. `current_system/` describes the system.
- Home pages were opened in Chrome at 1440×779 (the screen allows no taller window, so the screenshots are 1440×779, not 1440×900). Each candidate's home was scrolled two or three screens. Mobile layouts of the references were not checked; mobile points are targets, not defects found in the references. Mobbin was not used.
- No cookie banner was accepted. The banners of Coinbase and Copper were hidden with CSS before the screenshot. No file was downloaded, and no login or sign-up was made.
- The candidate screenshots (2026-11-20) are in the orchestrate run's scratchpad `crypto-candidates/` folder, not in the repository: `A.jpg` (Coinbase), `B.jpg` (Copper), `C.jpg` (Hashed), `D.jpg` (Kaia). `C.jpg` shows a real person's photo and name at its lower edge, as the reference does.

### Decisions after G1

- A1 (decided 2026-11-20, human Seokhyun Kim, G1): build three samples under the proposed names: A Coinbase → 로빈코인 `crypto-robincoin` (거래소); B Copper → 로빈커스터디 `crypto-robincustody` (수탁); D Kaia → 로빈체인 `crypto-robinchain` (웹3 개발사). C Hashed (로빈리서치 `crypto-robinresearch`, 리서치) is not built. The sample letters stay A, B and D. This closes Q1.
- A2 (decided 2026-11-20, human, G1): the 25° accent-hue rule of the beauty feature does not apply to `crypto`. AC121 (no shared accent hex) and AC119 and AC127 (a person, side by side) stay. This closes Q2.
- A3 (decided 2026-11-20, human, G1): the substitutions are accepted as the candidates state them. This closes Q3.
  - A: option (a). The phone shows example prices that both rise and fall, with change figures in `%`, under the text "예시 화면 · 실제 시세가 아닙니다". It has no balance gain line and no real coin name. Two `#` links replace the e-mail field (AC180).
  - B: three word cards replace the three figure cards (AC216).
  - D: no investor logo row, no app button and no token (AC73, AC97, AC95). The header is a glass bar from the start (AC227).
- A4 (decided 2026-11-20, agent): the 리서치 block (AC91–AC94) is withdrawn with candidate C, and its numbers stay unused. The request's "리서치 · 운용" had been narrowed to 리서치; with no such sample, neither word names a sample.
- A5 (decided 2026-11-20, agent): palettes. Each takes the colour family of its reference at other values. Contrast ratios are WCAG 2, computed on 2026-11-20. AC132 checks contrast on the built pages.
  - A: page `#ffffff`; text and dark panel `#0c1222` (18.66:1 on the page); grey band and grey pills `#eef2f7`; accent blue `#0a69c7` (hue 210°; 5.44:1 on white, 4.84:1 on `#eef2f7`). The panel gradient runs from `#3f9cf0` to `#06357a`. A rise is `#c8323c` (5.28:1 on white) and a fall is the accent. Coinbase's blue is `#0052ff` (hue 221°).
  - B: page apricot `#f5c08a` (hue 30°) with `#2a1d14` text (9.96:1); pill header and light surfaces `#fffdf9` with `#2a1d14` text (16.09:1); accent wine `#7b2338` (hue 346°; 5.98:1 on the page, 9.66:1 against `#fffdf9`). Copper's page is `#fdbda4` (hue 17°).
  - D: page `#07090a` with `#f2f5ee` text (18.12:1); cards `#161a1c` with `#f2f5ee` text (15.91:1); lime `#a9ef2c` (hue 82°; 14.32:1 on the page, and `#07090a` on it 14.32:1). Kaia's lime is `#bff009` (hue 73°).
  - No accent equals an accent in `scripts/profiles.py`, and no hex is in two of the three palettes (AC121). `#ffffff` is also in `clinic-neuru`'s palette, which AC121 allows.
- A6 (decided 2026-11-20, agent): typefaces and pictures. A: Pretendard for the wordmark and `<h1>`, and no Google Fonts family. B: `Noto Sans KR` 300 for the `<h1>`, `Noto Serif KR` 700 for its `<em>` words, the wordmark and the word-card terms. D: `Gasoek One` for the wordmark and `<h1>`. Body text, hours, phone digits and example figures are Pretendard in all three; figures use `tabular-nums` (AC174). On 2026-11-20 `fonts.googleapis.com` served `Gasoek One` with Hangul in weight 400 only, `Noto Sans KR` in 300 and `Noto Serif KR` in 700. No shipped sample loads `Gasoek One`. One shipped sample, `food-saebyeokmil`, sets its `<h1>` and its wordmark in Pretendard, as A does (A16); A's headline and body share one family and differ in size and weight. `clinic-bonui` and `flower-bomgyeol` load a Noto KR family in light weights; B uses the heavy serif beside the light sans in one headline, which neither does. No crypto sample uses a photo, so none has an `img/` folder (AC262) and AC104–AC116 hold with nothing to check.
- A7 (decided 2026-11-20, agent): A's phone. The top figure is the example price of 예시 자산 A, not a balance (AC166, AC167); AC75 bars an amount held, and the human's option (a) drops the gain line. The price line rises and falls and does not end at its high (AC169). A rise is red and a fall is blue, as Korean exchanges show them, and each change figure carries a sign (AC171, AC173). The panel is the example block, so its marker and the risk sentence (AC83) need not fit inside the clipped phone; the marker is still the first text in the phone (AC164).
- A8 (decided 2026-11-20, agent): A's lower parts. The dark rounded panel holds the steps, not a picture of a trading screen (AC184, AC185; AC86). The card of asset rows is a second example block, white on a grey band, with rows in letter order (AC186, AC187; AC87). Coinbase's card is black.
- A9 (decided 2026-11-20, agent): A's header shows 로그인 and 회원가입 once each as grey `#` pills, and the one filled pill is the 문의 link (AC155, AC156; AC56). Under the headline the two links are 고객센터 문의 and 서비스 보기 (AC180). AC190 adds labels that invite trading or an account to the banned words.
- A10 (decided 2026-11-20, agent): pictures are drawn new. B's drawing is line work with no ellipse and no large circle, so it cannot be Copper's sphere (AC213); the direction is nested rounded squares, each turned a little. D's object has no glyph and is not one slab (AC241); the direction is three stacked rings lit in lime. The design stage fixes the shapes.
- A11 (decided 2026-11-20, agent): wordmarks. A: left, 23–25 px, Pretendard 700. B: centred in the pill header, 28–32 px, `Noto Serif KR`. D: at the left end of an inset glass bar, 35–38 px (30–34 px at 390 px; A19), `Gasoek One` in lime. AC258, AC259 and AC263 hold the pairwise gaps. All three references put the mark at the top left; B is moved to the centre for the distance. At 390 px all three sit at the left and differ in face, colour and size only.
- A12 (decided 2026-11-20, agent): section order. A: first section, 서비스, dark panel with 이용 방법, grey band with the asset card, 고객센터 문의. B: first section, 하는 일, word cards, 도입 절차, 도입 문의. D: first section, 서비스 (bento), 진행 과정 (lime band), 프로젝트 문의; Kaia has the band first (AC248). The design stage fixes the headings within AC28–AC30.
- A13 (decided 2026-11-20, agent): the 390 px checks of every (browser) AC, the common ones included, use a 390×844 viewport; AC134 alone uses the `width:390px` iframe of playbook §4. The reference screenshots are 1440×779, so fixed sizes are ranges, and the design stage confirms them by a run.
- A14 (decided 2026-11-20, agent): word lists made checkable without a weaker meaning.
  - AC61: 이자 matched every word that ends in the particle 이자. Three such words are now let through: 개발사이자, 운영사이자 and 회사이자. Every other 이자 still matches, and 수익 is unchanged.
  - AC74: a phone number, the 사업자등록번호, a clock time and the 3 of 웹3 are not counted. Before, "18:00 명절 휴무" and "웹3 만드는" matched as a count.
  - Latin abbreviations in the lists match as whole words, as the tickers of AC70 already did.
  - Not changed: 리뷰 (AC67), 이벤트 (AC68) and 라이선스 (AC66) also bar 코드 리뷰, 컨트랙트 이벤트 and 오픈소스 라이선스 in D. D's copy uses 점검, 검토 and other words instead.
- A15 (decided 2026-11-20, agent): gallery card titles. A "흰 바탕에 파란 패널과 예시 화면을 둔 거래소"; B "살구색 지면과 흰 알약 헤더의 수탁 서비스"; D "검정 지면에 라임 한 색을 쓴 웹3 개발사". `summary` and `features` are written in the implement stage (AC76).
- A16 (decided 2026-11-20, agent): nearest shipped designs, for the person who judges AC119. A: `clinic-neuru` (white bar header, wordmark at the left, heavy sans headline); A's accent hue 210° is 8° from `interior-robinhome`'s page colour (218°) and 20° from `food-saebyeokmil`'s accent (230°), and `food-saebyeokmil` sets its `<h1>` and wordmark in Pretendard too (wordmark 700 at 22 px; A's is 23–25 px), so that pair differs in page colour and first-screen composition. B: its wine accent (346°) is 4° from `flower-bomgyeol`'s accent (342°), and its Noto KR families are also loaded by `clinic-bonui` and `flower-bomgyeol`. D: `law-ganeum` is the other dark page with a text column at the left; D's lime (82°) is 22° from `beauty-robinhair`'s accent (60°).
- A17 (decided 2026-11-20, agent): AC145–AC149 add what the common criteria left open: the description and link-preview text say "디자인 샘플", the marker that stays on screen and the first-screen non-business sentence have a size floor, and the fixed bars leave room on a phone screen.

### Research: sites looked at (2026-11-20, Chrome; history)

| Site | 업태 | Result |
| --- | --- | --- |
| coinbase.com (Coinbase, US) | 거래소 | Candidate A |
| copper.co (Copper, UK) | 수탁 | Candidate B |
| hashed.com (해시드, Korea) | 리서치 · 투자 | Candidate C |
| kaia.io (Kaia) | 재단 · 웹3 | Candidate D |
| lambda256.io (람다256, Korea) | 웹3 개발사 | Runner-up for D. White page, centred Korean headline, a black pill "문의하기", a greyscale globe with mint arcs. The light option for a 개발사; white is the most crowded base among shipped samples. |
| upbit.com (업비트, Korea) | 거래소 | Runner-up for A. Pale blue-white page, Korean headline at the left, a dotted world map, an index strip and tabs for 거래대금 below. A pop-up for a trading race with a token prize covers the centre, and a QR code sits at the right. |
| variant.fund (Variant, US) | 투자 | Runner-up for C. One flat cobalt page, a sans headline and a list of writings with mono dates. Its blue is near candidate A's and near `interior-robinhome`. |
| xangle.io (쟁글, Korea) | 리서치 | Light portal: a report carousel, a calendar, a news list and a live price column. Dense and useful; a portal, not a business site, and its price column is live data of real assets. |
| bithumb.com (빗썸, Korea) | 거래소 | Warm beige page with a gold trophy render and three "1위" labels. The picture is the claim (AC64). |
| coinone.co.kr (코인원, Korea) | 거래소 | White page with coin renders; an event pop-up on load and a "실시간 수익 인증" list (AC61). |
| korbit.co.kr (Korea) | 거래소 | The page shows a "DIGITAL X" wordmark, a pop-up about the new name, an orange glow and a cookie bar. |
| kdac.io (한국디지털자산수탁, Korea) | 수탁 | Stock picture of a padlock on a circuit board, blue on navy. The genre cliché. |
| anchorage.com (Anchorage Digital, US) | 수탁 | Near-black page, indigo glow, large light headline; a cookie panel on load. Refined; near `law-ganeum` and the genre's dark default. |
| bitgo.com (BitGo, US) | 수탁 | Black page with a glowing blue shield outline. Dark and neon. |
| fireblocks.com (Fireblocks, US) | 수탁 · 인프라 | White page, navy headline, a pastel gradient panel with glass cards and a gauge figure; a large cookie panel on load. Near candidate A in structure. |
| kraken.com (Kraken, US) | 거래소 | Pale lavender-grey page, centred headline, an e-mail field with social sign-up buttons, three figure blocks. |
| gemini.com (Gemini, US) | 거래소 | A sky photo with coral clouds and a white card over it. The only photo-led exchange seen; the card is a prediction-market ticket. |
| base.org (Base, US) | 웹3 | White page, a blue square mark, centred headline, partner logo row. Near candidate A's colours. |
| ethereum.org (Ethereum) | 재단 | A wide line illustration band over a black page. The illustration is the site; a sample cannot match it with CSS. |
| galaxy.com (Galaxy, US) | 운용 | Black page with a dot grid, a large white headline with one mint word; a cookie panel on load. |
| grayscale.com (Grayscale, US) | 운용 | A zebra photo under a deep purple bar; a cookie panel covers the lower half. |
| a16zcrypto.com (US) | 투자 | Now titled "a16z frontier". Black page, a lime pattern band. Near candidate D. |
| paradigm.xyz (Paradigm, US) | 투자 | A white page with a small animated diagram and key hints. An experiment, not a business page. |
| bitwiseinvestments.com (Bitwise, US) | 운용 | Excluded: an investor-type gate and a cookie box cover the page. |
| kodaglobal.com | 수탁 | Excluded: the domain is for sale (a registrar page). |
| dsrvlabs.com | 웹3 개발사 | Excluded: did not load (browser error page). |
| zodia.io (Zodia Custody) | 수탁 | Excluded: stopped at a Cloudflare security check. |

Where Korean visitor actions sit on the sites seen: 로그인 and 회원가입 at the right of the header, 고객센터 beside them, an
app QR code on the first screen and 공지사항 under the hero (업비트); a floating "도움이 필요하세요?" button and a 전화 number
card (빗썸); a black pill "문의하기" in the header and under the headline (람다256). None of the four candidates shows 카카오톡,
네이버 예약 or 네이버 지도.

### Candidates shown at G1 (history)

At G1 the human picked A, B and D, and did not pick C (A1). The text below is kept as shown at G1. "Q1", "Q2" and "Q3" in
it are the questions that A1–A3 closed, and "the 리서치 block" is the withdrawn AC91–AC94. Where it differs from the
per-sample ACs or from Decisions after G1, those hold.

The four differ in base: white with one blue panel (A), flat peach (B), pale grey with serif type (C), black with lime
(D). D is the only dark one (AC128).

**A. Coinbase — https://www.coinbase.com** (US). 업태: 거래소. A white product page: one blue panel that holds a phone screen, and a large sans headline beside it.

```
+------------------------------------------------------------+
| (o)  Crypto Individuals Businesses ...   (Q)(@) (Sign in)(Sign up) |
+------------------------------------------------------------+
|  +------------------------+                                |
|  | ## blue gradient    ## |    The future of               |
|  |  +------------------+  |    finance is here.            |
|  |  | $33,683.80       |  |    one line of text            |
|  |  | /\/\__/\/ (line) |  |    [ e-mail field ] (Sign up)  |
|  |  | Crypto   $14,186 |  |                                |
|  |  | Stocks    $8,133 |  |                                |
|  |  +------------------+  |                                |
|  +------------------------+                                |
+------------------------------------------------------------+
| ## dark rounded panel: trading screen | headline, button ##|
| grey band: headline, button | ## black card: asset rows,   |
|                             |    price and change % ##     |
+------------------------------------------------------------+
```

- Suits: an exchange or a trading app that wants a clean, bank-like first screen (원화 거래소, 간편 투자 앱).
- Proposed name: 로빈코인 (`crypto-robincoin`).
- Rules that apply: every common AC, the example-figure block and the 거래소 block. This candidate carries the highest phishing reading of the four.
- Picture material: CSS and inline SVG; no photo.
- Traits to keep: a white bar header with pill buttons at the right; a rounded blue panel at the left that holds a phone screen with a balance line, a line chart and a short list; a large two-line headline at the right; below, a dark rounded panel and a card of asset rows.
- We would improve: Korean headline and nav; the sample marker and the non-business notice on the first screen; a 문의 link in place of the e-mail field; 카카오톡 · 전화 · 네이버 예약 · 네이버 지도 in the contact section; a risk notice; a 문의 bar that stays on the phone screen.
- Conflicts with the rules: (1) the e-mail field and "Sign up" button are an input (AC47); ours has two `#` links. (2) The phone screen shows a balance with a green gain line "$131.36 (1.38%)" and a rising chart; a gain figure is out (AC82). (3) The asset card names real coins with prices; ours says 예시 자산 A (AC80). See Q3.
- Distance from shipped samples: white is the crowded base. The distance is the blue panel with a product screen, which no shipped sample has, and the absence of any photo. Its blue (221°) is 9° from `food-saebyeokmil`'s accent (230°); see Q2.

**B. Copper — https://copper.co** (UK). 업태: 수탁. One flat peach page with a white pill header, a headline that mixes a light sans and a bold serif, and a line-drawn sphere.

```
+------------------------------------------------------------+
| ## peach page ##                                           |
|  ( (C) Copper     Solutions Insights Company ...  (Talk) ) |  <- white pill bar
|                                                            |
|  Collateral *Mobility*                  .-''''''-.         |
|  *for Markets* That                   /  | ( ) |  \        |
|  Never Close                         (---+-----+---)  line |
|  two lines of text                    \  | ( ) |  /  sphere|
|  (Speak to our team)                    '-......-'         |
+------------------------------------------------------------+
| white: headline (sans + serif) | paragraph                 |
| [ 60mn ]      [ $105bn ]      [ $3bn ]    three figure cards|
| centred label chip, centred headline, paragraph            |
| pale grey: headline, text, button | card with the sphere   |
+------------------------------------------------------------+
```

- Suits: a custodian or an institutional service that wants to look calm and unlike the genre (수탁, 기관 대상 보관 · 결제).
- Proposed name: 로빈커스터디 (`crypto-robincustody`).
- Rules that apply: every common AC and the 수탁 block. No example block.
- Picture material: inline SVG line drawing; no photo.
- Traits to keep: one flat warm colour over the whole first screen; a white pill-shaped header that floats on it; a headline that sets some words in a second, heavier face; a line drawing at the right; below, a row of three cards with one large glyph each, and sections split by dashed rules.
- We would improve: Korean headline with the second face on a Hangul phrase; the sample marker and the non-business notice on the first screen; 도입 문의 in the pill header and under the headline; contact links and a risk notice.
- Conflicts with the rules: the three cards show business figures ("60mn", "$105bn", "$3bn"); a fictional business has none (AC67, AC88). Ours keeps three cards with one large word each (for example 분리 보관, 다중 승인, 오프라인 보관). See Q3.
- Distance from shipped samples: no shipped sample has a full page in one warm colour; `interior-robindesign` has two saturated halves and a giant wordmark. The peach (17°) sits between two shipped accents (9° and 19°), as a page colour and not as an accent; see Q2. The page must not reuse `#fdbda4`.

**C. Hashed — https://www.hashed.com** (Korea). Not picked at G1; kept as a research record. 업태: 리서치 · 투자. A pale grey page of numbered statements in a thin serif, with tilted photos between them.

```
+------------------------------------------------------------+
| #HASHED                      Portfolio Team Content About ...|
|                                                            |
| 01.  Frontier Technology at                                |
|      Global Scale              (thin serif, about 62 px)   |
|                                                            |
|      a paragraph, six lines                                |
|                     /------------------\                   |
|                    /  (tilted photo)    \   name           |
+------------------------------------------------------------+
|                    \____________________/   caption        |
| 02.  second statement, three lines                         |
|      a paragraph         /--(tilted photo)--\   caption    |
| 03.  third statement ...                                   |
+------------------------------------------------------------+
```

- Suits: a research house, a media or an investment firm that sells its point of view (리서치 하우스, 크립토 미디어).
- Proposed name: 로빈리서치 (`crypto-robinresearch`).
- Rules that apply: every common AC and the 리서치 block. No example block.
- Picture material: three to five photos from Unsplash or Pexels, with `img/sources.txt` and a "Photos:" credit.
- Traits to keep: a pale grey page with no hero picture; a heavy wordmark at the top left and a plain nav at the right; statements numbered 01, 02, 03 with a small coloured index, set large in a thin serif; a narrow paragraph under each; a slightly tilted photo with a caption column at its right between statements.
- We would improve: Korean statements in a Korean serif; the sample marker; a 제휴 문의 link in the header and after the first statement; a list of example note titles; contact links, the "투자 권유가 아닙니다" line and a risk notice.
- Conflicts with the rules: the photos show named people and events; ours shows no person and no event (AC27, AC115). The captions describe a topic. The reference is an investment firm with a portfolio; ours is a research house with no fund (AC91). See Q3.
- Distance from shipped samples: `law-goim` and `beauty-robinhairsalon` have grey bases, both with a photo on the first screen; `law-ganeum` has a first screen with no photo, in graphite. A pale page that opens with a numbered serif statement and no picture is new. Korean serifs are already used by four shipped samples, so the face must be one that none of them loads.

**D. Kaia — https://www.kaia.io** (Kaia). 업태: 재단 · 웹3. A black page with one acid lime: a wide extended sans headline, pill buttons and a glass object lit in lime.

```
+------------------------------------------------------------+
| ## black page ##                                           |
| kaia  About Ecosystem Build ...   (For Institutions)(Portal)|
|                                                            |
|  Where                                 ___                 |
|  *Stablecoins*   (lime line)          /   \  glass object  |
|  Become Capital                       | & |  in lime light |
|  two lines of text                    \___/                |
|  (Open DeFi Portal) (Bridge to Kaia)                       |
|  BACKED BY   logo   logo   logo   logo   logo              |
+------------------------------------------------------------+
| on scroll the nav becomes a green glass pill bar           |
| ## lime band, rounded: three staggered cards ##            |
| ## black: bento cards with small glowing marks ##          |
+------------------------------------------------------------+
```

- Suits: a blockchain developer or infrastructure company that wants the genre's look done well (웹3 개발사, 블록체인 인프라).
- Proposed name: 로빈체인 (`crypto-robinchain`).
- Rules that apply: every common AC and the 웹3 개발사 block. No example block.
- Picture material: CSS gradients and one inline SVG object; no photo.
- Traits to keep: a black page with a single lime colour; a three-line headline in a wide heavy sans with the middle line in lime; two pill buttons under it; one lit object at the right; a rounded glass nav bar; a full-width lime band with three staggered cards; dark bento cards below.
- We would improve: Korean headline in a heavy Korean sans; the sample marker; 프로젝트 문의 as the first pill; services written as work for other businesses; contact links and a risk notice.
- Conflicts with the rules: (1) the "Backed by" logo row is out (AC73); ours has no row there. (2) "Open DeFi Portal" and "Bridge" are app entries (AC97); ours has 프로젝트 문의 and 서비스 보기. (3) The reference is a token foundation; ours is a 개발사 with no token (AC95). (4) The nav turns into a glass bar on scroll by script; ours is a glass bar from the start, with no script (AC48). See Q3.
- Distance from shipped samples: four shipped samples are dark, none black with a neon colour: `law-ganeum` is graphite with steel blue, `interior-robinhome` ink blue with sand. The lime (73°) is 13° from `beauty-robinhair`'s olive accent (60°); see Q2. This is the genre's default look; A, B and C are the answer to "not all dark and neon".

- A18 (decided 2026-11-20, agent, design stage): two changes after a run on a fixture (Chrome, 1440×900 and 390×844, real web fonts).
  - AC226: the lowest alpha of the glass bar is 0.75, not 0.7. Over the lime band, `rgba(48, 48, 48, 0.7)` leaves the lime wordmark at 4.38:1, below the 4.5:1 that AC132 asks of text; at 0.75 it is 4.96:1. The upper end and the channel limit stay.
  - Per-sample preamble: the horizontal edges and centre of an `<h1>` and of a header wordmark are measured on the rendered text (AC153, AC177, AC200, AC202, AC203, AC206, AC229, AC235, AC258, AC260). A block `<h1>` as wide as its column has a box centre that is not where the words are, and a mark inside a wordmark link moves the box, not the name.
  - Confirmed with no change: AC149 (the fixture's bars cover 94–98 px of 220), AC179 (box 2.30 × the font-size), AC183 (panel top at 420 px of 720), AC199 (apricot 6 px above and below the pill with a 14 px gap under the strip), AC232 (each line 1.2 × at 40 px; a line of twelve syllables and three spaces still fits on one line at 30 px), AC258 (A19 has the distance) and AC263.
- A19 (decided 2026-11-20, orchestrator, design stage): D's wordmark is larger. At 18–20 px on a 1x screen the inner gaps of `Gasoek One` close and 로빈체인 does not read. Header crops at deviceScaleFactor 1 were read at 19, 30, 36, 40 and 44 px: the name reads from 30 px, and at 36 px a reader who was not told the word scored it as high as a 19 px `Black Han Sans` control. The face stays.
  - AC230: 35–38 px at 1440 px, 30–34 px at 390 px. The lower end at 1440 px is 3 px above B's largest (AC201, 32 px), so AC259 holds at every allowed size and D is the largest of the three marks. The upper ends keep the line box (1.45 × the font-size) inside the 60 px and 54 px bar. At 390 px the range is the first size bound on a wordmark there; it leaves AC263 room over A and B.
  - AC258, AC259, AC263, AC154 and AC201 are unchanged. AC258 at the worst allowed ends (A at 64 px left and 25 px; D at 150 px left and 35 px): the text centres are 106 px apart.
  - T40 asks a person to read the name in the 1x screenshots.
- A20 (decided 2026-11-20, orchestrator, before approval): three rules made stricter and one evidence source.
  - AC56: entry links are judged by accessible name. A's header holds exactly one 로그인 and one 회원가입 link; 가입하기 and 시작하기 join the AC190 list.
  - AC76: the gallery card text also obeys AC53–AC55 and the sample's own word lists, and the `title` equals A15.
  - Reference evidence for A: the candidate screenshot the human saw at G1 (1440×779, Chrome, 2026-11-20) is evidence for T10. It is kept at `/tmp/profile-crypto-shots/ref-g1-coinbase.jpg`, outside the folders that `page` and `compare` rewrite.
  - `preflight(browser)` in `tasks.md` stays: the verdict runs it before the browser checks.
- A21 (decided 2026-11-20, orchestrator, before approval): three rules made stricter, so that the checks fail what they could not read before.
  - AC149: the browser check counts elements only. A `::before` or `::after` rule may declare `position: absolute`, `relative` or `static` and nothing else (`fixed`, `sticky`, `inherit` and a `var()` fail), in `style.css` and `<style>`, inside `@media` (around the rule or nested in it) and in a grouped selector too. `check_static.py a11y` reads it.
  - AC60 and AC132: the background behind text is the background of elements. When the element with the text or one of its ancestors has a generated `::before` or `::after` with a `background-image` or a background colour of alpha above 0, the check cannot tell whether that layer lies under or over the text, and the text fails. The AC sentences stay; the rule is in the page contract of `tasks.md`. A `::before` or `::after` on an element that holds no text and is not an ancestor of text (D's lit object, a line drawing, an empty `aria-hidden` dot) is not read.
  - AC31: the contact-section sentence has a computed `font-size` of at least 14 px at 1440 px and at 390 px, the floor AC148 gives the first-screen copy.
- A22 (decided 2026-11-20, agent, before approval): three rules made stricter.
  - AC12: the marker that stays on screen has an opaque background colour, on itself or on the fixed or sticky element that holds it.
  - "Visible", for the four fixed texts (the sample marker, the AC31 sentence, the AC58 sentence and the example marker): the text is drawn as written. A `filter`, `transform`, `scale`, `zoom`, mask or blend mode on the element or an ancestor, or a `-webkit-text-fill-color` that differs from `color`, hides or shrinks glyphs while the computed colour and size stay, so the text then counts as not visible (AC8, AC9, AC12, AC31, AC32, AC58, AC79, AC83, AC164, AC165). The rule is in the page contract of `tasks.md`.
  - AC103: no `data:` URL of any kind. The word, figure and colour checks do not read what a `data:` URL holds.

## Open questions
