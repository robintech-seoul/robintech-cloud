---
status: shipped
approved_at: 003195c9b817e97856b9584eadbfdb267cc7b278
commits: 90f5b86b2342ea0710a82816a2ca4b05ee8f1479..003195c9b817e97856b9584eadbfdb267cc7b278
---

# Invest profile samples (`invest`)

## Problem

The `/profile/` gallery has no sample for the `invest` (투자자문) industry. The 투자자문 filter chip shows no count, and
the grid shows a "투자자문 프로파일 준비 중" tile. An owner of a 투자자문사 or a private-equity house who opens the gallery
finds nothing for their business, and sales has no sample to show.

The request names two kinds of business: "투자자문(프라이빗에쿼티)". They are different businesses under 자본시장법. A
투자자문업자 or 투자일임업자 needs a registration (제17조 bars the business without one) and may serve individuals. The 업무집행사원 of a 기관전용 사모집합투자기구
(a PE house) registers under 제249조의15, and its fund takes no individual as a 유한책임사원 (제249조의11⑥). The pages of
the two kinds differ, and so do the rules on what they may show.

A site of this industry sells with a record, people and a way in, and a sample has none of them. The sites opened for
this spec (2026-11-21) show "$346 billion" of assets (TPG), "$23B", "#1" and "4.5x" cards and a chart of hypothetical
account growth (Farther), "EUR 10Bn" and "200+" (Verdane), "cumulative AUM of $4.9 billion" (글렌우드), "1,411,237명이
선택한" with app-store buttons and a trophy (핀트), "4.45% APY" (Wealthfront), "The World's Leading Consumer Growth
Investor" (L Catterton), photos of the firm's own people (Permira, Warburg Pincus, Nordic Capital), cards of real portfolio
companies (Advent), a row of press logos (Farther) and "Investor Portal" or "Client Login" in the header (Verdane,
Farther, Rockefeller). On a sample, each of these would be fabricated or would be a working entry point.

A public page that looks like an investment firm can be read as an investment scam page. Eight of the sites opened
carry a warning about people who impersonate the firm to solicit money: 스틱인베스트먼트, VIG파트너스, IMM, MBK파트너스,
타임폴리오자산운용, KKR, Ardian and Affinity. Korean law also reaches the content: only a 금융상품판매업자등 may advertise
a 금융상품 or its business (금융소비자보호법 제22조①), advice and discretionary management need a registration (자본시장법
제17조), and advertising unregistered fund-raising is barred (유사수신법 제4조). Rule sources are in Assumptions.

## Scope

"Each invest sample" below means each of the three folders this feature builds (human decision at G1, A1):
`profile/invest-robinfamilyoffice/` (로빈패밀리오피스, sample B), `profile/invest-robinwealth/` (로빈자산관리, sample C) and
`profile/invest-robincapital/` (로빈캐피탈, sample D). "업태" is the kind of business a sample presents, one of two:
"PE" (기관전용 사모펀드 운용사, a 업무집행사원) or "자문" (자문 · 자산관리 for individuals and families). B and C are 자문
samples and D is the PE sample. An AC that names an 업태 holds for the samples of that 업태. The sample letters stay B,
C and D; candidate A is not built.

- **In:** Three hand-built samples: `profile/invest-robinfamilyoffice/`, `profile/invest-robinwealth/` and `profile/invest-robincapital/`.
- **In:** For each invest sample: `index.html`, `style.css`, `thumb.jpg` and, when it uses photos, `img/` with `img/sources.txt`, built per `docs/profile-playbook.md`.
- **In:** A one-page site for one fictional investment business: what it does, how it works, risk notice, and 문의.
- **In:** One `live` entry with `industry: "invest"` in `PROFILES` in `scripts/profiles.py` for each invest sample.
- **In:** The regenerated `profile/index.html`, made by `python3 scripts/build.py`.
- **In:** Advertising and solicitation rules for 금융투자업 and 사모펀드, as content rules (AC57–AC84).
- **In:** No working entry point: no sign-up, login, portal, account, form or script (AC48–AC56).
- **In:** Korean visitor flow: 문의 reachable on every screen, and 카카오톡 · 전화 · 네이버 예약 · 네이버 지도 (AC36–AC47).
- **In:** Distinctness of each invest sample from the eighteen shipped samples, from the other invest samples and from its own reference (AC103–AC110, AC241–AC251).
- **In:** For each sample, the traits kept from its reference, its palette, typefaces, pictures and first screens at 1440 px and 390 px (AC128–AC240).
- **In:** Photos in two samples: two black-and-white photos in sample B and one colour photo in sample C; sample D is drawn in CSS and inline SVG.
- **In:** Reconcile `docs/current_system/` (the sample list in `profile-samples/component.md`) and set `last_reconciled`.
- **Out:** Candidate A (Verdane, 로빈에쿼티 `invest-robinequity`) and the name 로빈투자자문; the human did not pick them at G1.
- **Out:** A business-name collision check and a `name-check.txt`. The human chose 로빈 + field-word names (Assumptions).
- **Out:** Changes to `assets/`, to `scripts/build.py`, to `docs/profile-playbook.md`, and to the eighteen shipped samples under `profile/`.
- **Out:** Real or example performance data: returns, AUM, fund sizes, charts of results, market data, a price or index feed.
- **Out:** Real sign-up, login, investor portal, account opening, subscription, KakaoTalk, booking, map or phone integration. Every link is a `#` placeholder.
- **Out:** Inner pages (team pages, portfolio pages, fund pages, reports, news, a blog). Each sample is one page.
- **Out:** Self-hosting fonts. Google Fonts and Pretendard on jsDelivr stay allowed.
- **Out:** Venture capital (벤처투자회사), 증권사, 은행 PB, 부티크 IB (M&A 자문) and 유사투자자문업 as an 업태. Samples for other industries.
- **Design:** none. Trigger 1 (crosses a component boundary): no. The change adds data and samples through the existing named interfaces (`PROFILES` item, URL `profile/<slug>/`, `thumb.jpg`), which stay unchanged. Trigger 2 (adds a component): no. Each of the three samples is one more instance of the existing `profile-samples` component. Trigger 3 (alters a named interface): no. The `invest` key is already in `INDUSTRIES`, and the `PROFILES` fields, the URL, the thumbnail contract and the `profile_thumb.py` CLI stay the same. Trigger 4 (internal module boundary): no. A sample is one folder with one page, one stylesheet and its images. So `spec.md` + `tasks.md` are enough.

## Acceptance criteria

AC1–AC113 hold for every invest sample unless a block names one 업태 (Scope says which sample has which 업태).
AC114–AC127 are common criteria added after G1. AC128–AC240 are per-sample: the traits kept from each
sample's reference, its palette, typefaces and pictures, and what it must not copy. AC241–AC251 compare or bind all
three. No criterion is withdrawn: none of AC1–AC113 depended on candidate A. A tag at the end of a rule AC says where it
comes from: a statute and article, the KOFIA rule, or "sample policy". The criteria that were marked for G1 stand in
their strict form (human decision, A3). "(human)" marks a check a person closes, and "(browser)" a check that needs a
browser; an AC with neither mark is decided by a command on the files. Every criterion is checked by a task's
`verify` in `tasks.md`; there is no `verify.md`.

"Page text" means, in `index.html`: visible text, `<title>`, `meta` description, keywords, `og:` and `twitter:` content (as `name` or `property`), `aria-label`, `alt` and
`title` attributes, and the text of inline `<svg>`; in `style.css`: the text a `content:` declaration draws (every string of its value, CSS escapes decoded; a `counter()` is read as a digit). A listed word that holds a space is
also banned written without the space. Full-width letters and digits are read as their plain forms, and soft hyphens and
zero-width characters and other invisible format characters are ignored. Latin words are matched in any case. A listed word made only of Latin capitals and
digits (AUM, IRR, MOIC, TVPI, DPI, APY, VIP, KKR, MBK, IMM, STIC, TPG, CVC, EQT, PJT, ETF) is matched as a whole word.

Two fixed sentences are not read against the word lists of AC60–AC68: the
non-business sentence of AC31 and the risk sentence of AC57.

Folder and registration

- [ ] AC1 Each invest sample contains `index.html`, `style.css` and `thumb.jpg`, an `img/` folder only when the sample uses photos, and no other file (dotfiles aside).
- [ ] AC2 In each invest sample, `index.html` and `style.css` reference no local file outside that sample's folder (no `../`, no root-relative `/` path, no `assets/`).
- [ ] AC3 `scripts/profiles.py` has exactly one `PROFILES` entry for each invest sample's slug, each with `industry` `invest`, `status` `live` and `demo` `True`, and no `invest` entry for any other slug.
- [ ] AC4 Each invest sample's slug matches `invest-robin` followed by one or more lowercase ASCII letters only.
- [ ] AC5 Each invest sample's `thumb.jpg` is 1200 px wide with a 16:10 ratio and shows the sample's current 1440×900 first screen (browser for the colours and the layout; human for its text, AC251).
- [ ] AC6 `python3 scripts/build.py` exits 0.
- [ ] AC7 Compared with `git merge-base main HEAD` (as in AC112), the branch changes no file outside the invest sample folders, `profile/index.html`, `scripts/profiles.py` and `docs/`, and does not change `docs/profile-playbook.md`.

Sample markers, names and metadata

- [ ] AC8 In each invest sample, the text "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다" is visible without scrolling at 1440 px width (browser).
- [ ] AC9 In each invest sample, the text of AC8 is visible without scrolling at 390 px width (browser).
- [ ] AC10 At 1440 px and at 390 px, the computed `font-size` of the AC8 text on the first screen is at least the computed `font-size` of `<body>` and at least 14 px (browser).
- [ ] AC11 At 1440 px and at 390 px, a person reads the AC8 text on the first screen in a colour that stands out clearly from its background (human).
- [ ] AC12 At 1440 px and at 390 px, an element whose text contains "디자인 샘플 · 상호와 정보는 가상입니다" is visible at every scroll position from the top to the end of the page, and it or the fixed or sticky element that holds it has an opaque background colour (browser; sample policy: a screenshot taken mid-page must still say the business is fictional).
- [ ] AC13 Each invest sample's footer contains "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다".
- [ ] AC14 Each invest sample's footer contains "Website by RobinTech".
- [ ] AC15 Each invest sample's `index.html` contains `<meta name="robots" content="noindex">`.
- [ ] AC16 Each invest sample's `<title>`, `meta` description and `og:title` each contain "디자인 샘플".
- [ ] AC17 The `name` of each invest sample's `PROFILES` entry is "로빈" followed by one or more Hangul syllables and nothing else.
- [ ] AC18 The accessible name of each invest sample's header wordmark is exactly the `name` of its `PROFILES` entry, and the wordmark is live text, not a picture of text (the name as the browser computes it: browser).
- [ ] AC19 No two invest samples share the same `PROFILES` `name`.
- [ ] AC20 In each invest sample, every address on the page includes "(가상 주소)".
- [ ] AC21 Every address in each invest sample names a district or road that does not exist (for example 가상구 결로), and the page text names no real 구, 동 or neighbourhood as the business's location; a 시 or 도 name alone is allowed (human).
- [ ] AC22 In each invest sample, every phone number on the page is `02-000-0000`.
- [ ] AC23 In each invest sample, every 사업자등록번호 on the page is `000-00-00000`.
- [ ] AC24 No invest sample shows a 금융투자업 등록번호 or 인가번호, a 업무집행사원 등록번호, a 유사투자자문업 신고번호, a 통신판매업 신고번호, a 준법감시인 심의번호 or any other registration or certificate number; the 사업자등록번호 of AC23 is the only number of that kind (sample policy: a fictional business has none).
- [ ] AC25 Every e-mail address in each invest sample's page text ends in `@example.com`.
- [ ] AC26 The page text of each invest sample holds no social-media handle (`@` followed by a name, outside an `@example.com` e-mail address) and no domain name other than `example.com`.
- [ ] AC27 No invest sample shows a person's name or portrait, whether as 대표, a partner, a 운용역, an adviser, an analyst or a client (human; sample policy; KOFIA 제2-38조 13호 bars a display that may infringe a person's 초상권).

Structure of the page

- [ ] AC28 Each invest sample has a section whose heading contains "하는 일", "서비스" or "투자 분야" and that names at least three things the business does.
- [ ] AC29 Each invest sample has a section whose heading contains "절차", "과정" or "방식" and that lists at least three steps in an `<ol>`.
- [ ] AC30 Each invest sample has a contact section whose heading contains "문의" or "상담".
- [ ] AC31 The AC30 section contains the visible sentence "가상의 업체이며 금융투자업자가 아닙니다. 투자 권유가 아니며 실제 자문 · 운용 · 상담을 제공하지 않습니다.", and at 1440 px and at 390 px that sentence has a computed `font-size` of at least 14 px (browser) (sample policy; 자본시장법 제17조 bars unregistered 투자자문업 and 투자일임업, and 금융소비자보호법 제22조① lets only a 금융상품판매업자등 advertise).
- [ ] AC32 The sentence of AC31 is also visible without scrolling at 1440 px and at 390 px, with a computed `font-size` of at least 13 px (browser; sample policy: both 업태 need a registration).
- [ ] AC33 Each invest sample's `<h1>` text is in Korean (contains at least one Hangul syllable).
- [ ] AC34 Each invest sample's Korean body text uses `word-break: keep-all`.
- [ ] AC35 Each invest sample presents one 업태 only: a PE sample offers no 투자자문, 투자일임 or 자산관리 service to individuals, and a 자문 sample does not present itself as a 사모펀드 운용사 or offer a fund (human).

Korean visitor flow

- [ ] AC36 The AC30 section of each invest sample has a link whose accessible name contains "카카오톡".
- [ ] AC37 The AC30 section of each invest sample has a link whose accessible name contains "전화".
- [ ] AC38 The AC30 section of each invest sample has a link whose accessible name contains "네이버 예약".
- [ ] AC39 The AC30 section of each invest sample has a link whose accessible name contains "네이버 지도".
- [ ] AC40 No link in the AC30 section has an accessible name that contains two or more of 카카오톡, 전화, 네이버 예약 and 네이버 지도.
- [ ] AC41 In each invest sample at 1440 px width, a link to the AC30 section (`href="#<id>"` of that section) whose text contains "문의" or "상담" is visible without scrolling (browser).
- [ ] AC42 In each invest sample at 390 px width, a link of the AC41 kind is visible without scrolling (browser).
- [ ] AC43 In each invest sample at 390 px width, a link of the AC41 kind stays on screen at every scroll position (browser).
- [ ] AC44 In each invest sample at 390 px width, with the page scrolled to the end, the last text line of the footer is visible and not covered by a fixed or sticky element (browser).
- [ ] AC45 The AC30 section of each invest sample shows the 상담 hours as digits (displayed at 1440 px and at 390 px: browser).
- [ ] AC46 The AC30 section of each invest sample shows the closed days (displayed at 1440 px and at 390 px: browser).
- [ ] AC47 The AC30 section of each invest sample shows an address with "(가상 주소)" and the phone number `02-000-0000` (displayed at 1440 px and at 390 px: browser).

No working entry point (sample policy against a scam reading)

- [ ] AC48 Each invest sample has no `<form>`, `<input>`, `<select>`, `<textarea>` or `<button>` element.
- [ ] AC49 Each invest sample has no `<script>` element, no inline event-handler attribute (`on…=`), no `javascript:` URL, and no `.js` file in its folder.
- [ ] AC50 Every `<a>` in each invest sample has an `href` that is `#` or `#` followed by the `id` of an element on the page.
- [ ] AC51 Each invest sample has no `<iframe>`, `<embed>`, `<object>`, `<video>` or `<audio>` element.
- [ ] AC52 The page text of each invest sample contains none of: App Store, Google Play, 앱스토어, 플레이스토어, 앱 다운로드, 앱 설치, APK, and no app-store badge or QR code is shown (human for the badge and the code).
- [ ] AC53 The page text of each invest sample contains none of: 계좌번호, 가상계좌, 입금, 송금, 납입, 이체, 계좌 개설, 비대면 개설, 결제, 카드 등록.
- [ ] AC54 The page text of each invest sample names no bank, 증권사 or payment brand: it contains none of 케이뱅크, 카카오뱅크, 토스, 농협, 신한, 국민은행, 우리은행, 하나은행, 기업은행, 미래에셋, 한국투자증권, 삼성증권, 키움, 페이팔, Visa or Mastercard, and a person finds no other such name (human for the last part).
- [ ] AC55 The page text of each invest sample contains none of: 로그인, 회원가입, 가입하기, 시작하기, 투자하기, 청약하기, 출자 신청, 포털, Portal, Login, Log in, Sign up, Get started (sample policy; the references show "Investor Portal", "Client Login" and "Get Started").
- [ ] AC56 `index.html` and `style.css` of each invest sample contain no `http://`, `https://` or protocol-relative (`//host`) URL, in any letter case, whose host is not `fonts.googleapis.com`, `fonts.gstatic.com` or `cdn.jsdelivr.net`.

Advertising and solicitation rules, every 업태

- [ ] AC57 Each invest sample's footer contains the visible sentence "투자에는 원금 손실 위험이 있으며, 손실은 투자자에게 귀속됩니다." (금융소비자보호법 제22조③3호 나목 and 시행령 제18조①2호: 원금 손실 발생 가능성 and 원금 손실에 대한 소비자의 책임; required here for every 업태, strict side).
- [ ] AC58 At 1440 px and at 390 px, the computed `font-size` of the AC57 sentence is at least 13 px (browser; KOFIA 제2-37조⑥2호 asks for 9 pt on A4, about 12 px).
- [ ] AC59 At 1440 px and at 390 px, the contrast ratio of the AC57 sentence against the background behind it is at least 4.5:1 (browser; KOFIA 제2-37조⑥1호: a colour that differs from the background).
- [ ] AC60 The page text contains none of: 수익, 원금 보장, 원금 보전, 원금 보호, 손실 보전, 손실 없, 이익 보장, 무위험, 안전한 투자, 안정적, 이율, 이자율, 배당, 복리, 불로소득, 패시브 인컴, IRR, MOIC, TVPI, DPI, APY, 배수, 초과 성과, 알파 (자본시장법 제55조: no promise to make good a loss or to guarantee a gain; 금융소비자보호법 제22조④2호 가목; KOFIA 제2-38조 1호 and 3호: no expected or target return; 유사수신법 제2조 1 · 2 · 4호).
- [ ] AC61 The page text contains none of: 최고, 최초, 최대, 최다, 최저, 유일, 독보적, 압도적, 1위, 1등, No.1, 넘버원, 선도, 선두, 리딩, 완벽, 보장, 보증, 무조건, 확실, 반드시, 틀림없 (금융소비자보호법 제21조 1호 and 시행령 제20조①4호: no 단정적 판단; 표시광고법 제3조①1호; L Catterton shows "The World's Leading", 글렌우드 "Leading Buyout Firm").
- [ ] AC62 The page text contains none of: 업계 평균, 타사, 경쟁사, 은행보다, 예금보다, 시장 대비, 벤치마크, 지수 대비, and no invest sample compares itself or a product with another firm, product or index in other words (human for the last part; 금융소비자보호법 제21조 4호 and 시행령 제20조①3호; KOFIA 제2-38조 6호; 표시광고법 제3조①3호).
- [ ] AC63 The page text contains none of: 추천 종목, 종목 추천, 추천주, 매수 추천, 매도 추천, 급등, 테마주, 대박, 저점 매수, 목표가, 시그널, 주식 방송, 종목 상담, 무료 체험, 유료 회원, 정회원, VIP, 수익 인증, 리딩방 (sample policy: the page must not read as a 유사투자자문업자 or a 리딩방; 자본시장법 제101조① requires a 신고 for 유사투자자문업, and 제101조의3 fixes what its advertising must say).
- [ ] AC64 The page text contains none of: 등록 완료, 정식 등록, 등록 업체, 인가, 인허가, 허가, 신고 수리, 신고 완료, 라이선스, 금융위원회, 금융감독원, 금융당국, 금융투자협회, 제도권, 합법, 심의필, 심사필, 준법감시인, 예금자 보호 (sample policy: registration, review and protection are facts a fictional business does not have; 자본시장법 제17조, 제249조의15①; 금융소비자보호법 시행령 제19조②).
- [ ] AC65 The page text contains none of: AUM, 운용자산, 운용 자산, 운용 규모, 수탁고, 약정액, 약정 총액, 펀드 규모, 누적, 실적, 트랙레코드, 트랙 레코드, Track Record, 투자 건수, 성과보수, 성과 보수, 후기, 리뷰, 별점, 평점, 만족도, ★, 수상, 어워드, Award, 고객 수, 가입자, 회원 수, 파트너사, 고객사, 출자자 명단 (sample policy: no fabricated record; 표시광고법 제3조①1호; KOFIA 제2-38조 2호 and 12호 on 수익률, 운용실적, 수상실적 and 통계수치).
- [ ] AC66 The page text contains none of: 무료, 공짜, 할인, 이벤트, 선착순, 마감 임박, 프로모션, 쿠폰, 특가, 사은품, 캐시백, 혜택, 수수료 면제, 지금 투자, 지금 가입, 소액으로 (sample policy: no lure offer; 유사수신법 제4조).
- [ ] AC67 No invest sample names or offers a fund, a product or a 투자일임 상품: the page text contains none of 호 펀드, 1호, 2호, 3호, 신규 펀드, 펀드 출시, 펀드 가입, 판매 중, 모집 중, 모집 기간, 청약, 최소 가입, 최소 투자, 가입 금액, 환매, 만기, and a person finds no named fund or product (human for the last part; 자본시장법 제249조의5 lets a 일반 사모펀드 be advertised only to 전문투자자 and listed investors, one by one; KOFIA 제2-38조 5호 bars showing a privately placed product; 자본시장법 제9조⑦ · ⑧: an offer to fifty or more is a 모집).
- [ ] AC68 The page text names no real investment firm, fund or investor: it contains none of KKR, 블랙스톤, Blackstone, 칼라일, Carlyle, 베인, Bain, TPG, CVC, EQT, MBK, IMM, 한앤컴퍼니, 스틱, STIC, 어피니티, Affinity, 글렌우드, 버데인, Verdane, 록펠러, Rockefeller, Farther, PJT, 타임폴리오, 국민연금, 사학연금, 공무원연금, 교직원공제회, 한국투자공사, 산업은행, and a person finds no other such name or logo (human for the last part; sample policy; KOFIA 제2-38조 13호).
- [ ] AC69 The page text names no real company, listed stock, ticker or index: it contains none of 삼성전자, 코스피, 코스닥, 나스닥, 다우, S&P, 니프티, 비트코인, ETF, and a person finds no other such name (human for the last part; sample policy: no 종목 and no 시황).
- [ ] AC70 The page text names no platform other than 네이버 (예약 and 지도 only) and 카카오톡: no social, video, messenger or community platform by name, logo or icon, for example 텔레그램, 오픈채팅, 밴드, 유튜브, 링크드인, X (human; sample policy: the impersonation warnings on 스틱 and VIG name SNS and 밴드 as where the solicitation happens).
- [ ] AC71 No invest sample makes, in other words, in English or in a picture, a claim of the kinds listed in AC60–AC67 (human).
- [ ] AC72 No invest sample shows a portfolio-company, investor, press, auditor, award or certificate logo or badge, or a row of such names, real or made up (human; Farther shows an "As covered by" row, Advent a row of portfolio cards).
- [ ] AC73 The page text contains no digit followed, with optional spaces, by `%`; no digit followed, with optional spaces, by 원, 만, 억, 조, 달러, 유로, 명, 건, 배, 개국, 개사, 곳, 년 or 호, also after 천, 백 or 십; no `₩`, `￦`, `$`, `€` or `x` next to a digit; no `+` after a digit; and no number with a thousands comma (no return, size, fee, count or founding year; sample policy). A number alone in one block with one of these units at the start of the next block counts too, whatever follows the unit. Three kinds of digit are not counted: the phone number `02-000-0000`, the 사업자등록번호 `000-00-00000`, and a clock time written `HH:MM`.
- [ ] AC74 No invest sample states an amount managed or raised, a count of funds, deals, companies, clients or staff, years in business, a founding year, a return or a fee, in words or in digits (human; AC73 catches only the listed forms).
- [ ] AC75 No invest sample shows a chart, graph, gauge or table that reads as a return, a growth of assets or a comparison of results; a drawing in a first screen is abstract and has no axis, no rising line and no figures (human; sample policy; Farther shows a chart of hypothetical account growth).
- [ ] AC76 The `title`, `summary` and `features` of each invest sample's `PROFILES` entry (the gallery card text) contain none of the words and digit forms that AC52–AC55, AC60–AC69, AC73, the lists of the sample's 업태 (AC78 for `invest-robincapital`; AC82 and AC83 for `invest-robinfamilyoffice` and `invest-robinwealth`) and the sample's own list (AC167, AC203 or AC240) ban in page text, and nothing that AC70–AC72 forbid; the `title` is the one A13 gives (command for the lists and the title, human for the rest).

PE samples only

- [ ] AC77 The contact section of a PE sample contains the visible sentence "저희가 운용하는 기관전용 사모펀드는 개인의 출자를 받지 않습니다.", with a computed `font-size` of at least 14 px at 1440 px and at 390 px (browser) (the sentence states the sample firm's own policy and does not restate the law; background: 자본시장법 제249조의11⑥, a 유한책임사원 is not an individual, with listed exceptions).
- [ ] AC78 The page text of a PE sample contains none of: 개인 투자자, 개인 고객, 개인 출자, 일반 투자자, 누구나, 소액, 재테크, 노후, 자산관리 상담 (sample policy: the page does not address the public as investors; 자본시장법 제9조⑲1호).
- [ ] AC79 The main 문의 link of a PE sample has text that addresses a company or an institution (for example 기업 문의, 매각 · 투자 유치 문의), not a person who wants to invest (human).
- [ ] AC80 A PE sample names no portfolio company, real or made up, and describes its investments by sector and by kind of deal only (human; sample policy).

자문 samples only

- [ ] AC81 The footer of a 자문 sample contains the visible sentence "계약을 체결하기 전에 설명서와 약관을 읽어 보시기 바랍니다.", with a computed `font-size` of at least 13 px at 1440 px and at 390 px (browser) (금융소비자보호법 제22조③1호; strict side: the sample offers no contract).
- [ ] AC82 The page text of a 자문 sample contains none of: 공동 운용, 합동 운용, 모아서 운용, 펀드처럼, and a 자문 sample does not show 투자일임 as pooled management in other words (human for the last part; KOFIA 제2-38조 7호: 투자일임재산 is managed per investor).
- [ ] AC83 The page text of a 자문 sample contains none of: 사모펀드, 출자, 블라인드, 프로젝트 펀드, 비상장 주식 추천, 공모주 (sample policy: a 자문 sample offers no fund and no access to private placements; AC35, AC67).
- [ ] AC84 A 자문 sample says that advice follows a talk about the client's goals and situation, and promises no result of the advice (human; 금융소비자보호법 제17조: 적합성원칙).

Photos (hold for a sample that has an `img/` folder)

- [ ] AC85 A sample with no photo has no `<img>` element and no `img/` folder.
- [ ] AC86 `img/sources.txt` has one line per image file in `img/`, in the form `<파일> <사진 페이지 URL 또는 -> <내려받은 URL>`, and lists no file that is not in `img/`.
- [ ] AC87 Every downloaded URL in `img/sources.txt` has the host `images.unsplash.com` or `images.pexels.com`, and no URL in the file has the host `plus.unsplash.com`.
- [ ] AC88 Every image in `img/` is a JPEG or WebP at most 2000 px wide and at most 500 KB, and the images of one sample total at most 3 MB.
- [ ] AC89 Every `<img>` has a `src` that starts with `img/` and an `alt` attribute; a decorative image has `alt=""`.
- [ ] AC90 Viewed at 200 % zoom, no photo shows a logo, a brand name, a sign, a screen with readable text, a number plate or any other readable letters (human).
- [ ] AC91 No photo shows a person whose face can be recognised (human; sample policy; AC27).
- [ ] AC92 No photo shows a landmark building that identifies a real firm or a real city district as the business's home (for example a named tower or a stock-exchange floor) (human).
- [ ] AC93 The footer of a sample with photos contains "Photos: Unsplash" or "Photos: Pexels", matching the hosts in `img/sources.txt`.

Accessibility and layout

- [ ] AC94 Each invest sample's `<html>` has `lang="ko"`, and the page has exactly one `<h1>` and no skipped heading level.
- [ ] AC95 Each invest sample's `style.css` has a `prefers-reduced-motion: reduce` block that turns off every animation and transition the sample defines.
- [ ] AC96 At 1440 px and at 390 px, each invest sample has no horizontal scroll: the document's `scrollWidth` is at most the viewport width (browser).
- [ ] AC97 At 1440 px and at 390 px (a `width:390px` iframe, playbook §4), a person scrolls each invest sample from top to end and finds no overlapping text, no clipped text and no element that covers another by accident (human).
- [ ] AC98 At 1440 px and at 390 px, body text, navigation links and button labels of each invest sample have a contrast ratio of at least 4.5:1 against the background behind them (browser).
- [ ] AC99 Each invest sample loads fonts only from Google Fonts and from Pretendard on jsDelivr.
- [ ] AC100 The 상담 hours and the phone number of each invest sample are set in a typeface with even digit widths: a Hangul face or a mono face, not a Latin serif (human).
- [ ] AC101 Every link and every focusable element of each invest sample shows a visible focus indicator on keyboard focus (browser).
- [ ] AC102 Each invest sample's `<header>` holds a `<nav>` with at least three links; each has an `href` that starts with `#` and text that contains at least one Hangul syllable.

Distinctness

- [ ] AC103 Side by side with the eighteen shipped `thumb.jpg` files, each invest sample's 1440 px first screen is not taken for any shipped sample, and differs from the nearest one (named per candidate in Assumptions) in composition, not only in colour (human).
- [ ] AC104 Side by side with the 390 px first screens of the eighteen shipped samples, each invest sample's 390 px first screen differs in composition, not only in colour (human).
- [ ] AC105 No accent colour of an invest sample (the last hex of its `palette`) equals any hex in another `PROFILES` entry's `palette`.
- [ ] AC106 Each invest sample keeps the traits listed for its candidate under "Traits to keep", as changed by A3–A7 in Decisions after G1, and no kept trait is removed to meet AC103–AC105 (human; the measurable forms are AC128–AC240).
- [ ] AC107 Side by side with its reference screenshot, no invest sample is taken for the reference's site: pictures, palette values, typeface, copy and section order are new, and the kept traits of AC106 do not count against this (human).
- [ ] AC108 No invest sample copies a sentence, a slogan, a logo, a picture or a photo from its reference, and its `style.css` holds none of the reference's brand hex values (human for the copying; the hex lists are AC165, AC201 and AC239).
- [ ] AC109 When two or more invest samples are built, their first screens differ pairwise in base colour and in composition (human).
- [ ] AC110 When two or more invest samples are built, their header wordmarks differ pairwise in position or in size at 1440 px (human; AC243–AC246 hold the measured gaps).

Gallery and close-out

- [ ] AC111 In `/profile/` served by `python3 -m http.server 8000`, the 투자자문 chip shows the number of invest samples, no "투자자문 프로파일 준비 중" tile is shown, and each invest card opens the preview, switches between desktop and mobile, and closes on Esc (browser).
- [ ] AC112 After `python3 scripts/build.py`, `git diff --stat "$(git merge-base main HEAD)"` (the working tree against the commit where this branch left `main`, so a later commit on `main` is not counted) lists, among generated pages, `profile/index.html` only.
- [ ] AC113 `docs/current_system/profile-samples/component.md` lists each invest sample, and `last_reconciled` in `docs/current_system/overview.md` is the feature's last commit.

Added after G1, each invest sample

- [ ] AC114 `scripts/profiles.py` has exactly three `PROFILES` entries with `industry` `invest`: `invest-robinfamilyoffice` with `name` "로빈패밀리오피스", `invest-robinwealth` with `name` "로빈자산관리" and `invest-robincapital` with `name` "로빈캐피탈" (human decision A1, A2).
- [ ] AC115 No word reserved by 자본시장법 제38조 is part of a sample's name: in the `name`, the header wordmark, the page text and the gallery card text (`title`, `summary`, `features`) of each invest sample, "로빈" is never followed, in the same word or in the next word, by 금융투자, 증권, 파생, 선물, 집합투자, 투자신탁, 자산운용, 투자자문, 투자일임 or 신탁 (human decision A2).
- [ ] AC116 The page text and the gallery card text of each invest sample contain none of, in any letter case: Asset Management, Investment Management, Investment Advisory, Investment Adviser, Securities, Investment Trust, Financial Investment, and no slug holds `asset`, `advisory`, `securities` or `trust` after `invest-robin` (human decision A2; 자본시장법 시행령 제42조 also reserves the foreign-word forms).
- [ ] AC117 At 1440 px and at 390 px, the AC12 element has a computed `font-size` of at least 14 px and at least the computed `font-size` of `<body>`, at scroll position 0 and at the end of the page (browser).
- [ ] AC118 In each invest sample at 390 px, at scroll position 0 and at mid-page, the fixed and sticky elements pinned to the top or bottom of the viewport cover at most 220 px of its height together (browser), and no rule of the sample's CSS whose selector has `::before` or `::after` declares a `position` other than `absolute`, `relative` or `static`, so that every such bar is an element the check counts.
- [ ] AC119 Every web font request of each invest sample succeeds, and the `<h1>` and the header wordmark render in a loaded web font, not in a fallback or a locally installed copy (browser).
- [ ] AC120 The first family in the computed `font-family` of each invest sample's `<body>` is `Pretendard Variable` or `Pretendard` (browser), and its `index.html` links the Pretendard stylesheet on `cdn.jsdelivr.net`.
- [ ] AC121 In each invest sample's contact section, the elements that show the 상담 hours and the phone number have `Pretendard Variable` or `Pretendard` as the first computed family (the measurable form of AC100) (browser).
- [ ] AC122 Every picture that is not a photo is made for the sample as CSS or inline `<svg>` in `index.html` or `style.css`; no `.svg`, `.png` or `.gif` file is in a sample's folder, and `index.html` and `style.css` contain no `data:` URL.
- [ ] AC123 Each invest sample's `style.css` contains the accent hex (the last `palette` hex) of its `PROFILES` entry (case-insensitive).
- [ ] AC124 No photo ID recorded in an invest sample's `img/sources.txt` appears in the `img/sources.txt` of any other sample under `profile/`.
- [ ] AC125 No invest sample has a `<details>` or `<summary>` element, and at 390 px no sample draws a menu toggle (three bars, a "메뉴" pill) that cannot open (human for the last part; AC48 and AC49 leave nothing to open it with; all three references show one).
- [ ] AC126 No invest sample's `<h1>` is a translation or close paraphrase of its reference's headline (human).
- [ ] AC127 No `font-family` value and no font URL in an invest sample's `index.html` or `style.css` names a typeface of its reference: `Chiswick` or `Inter` in `invest-robinfamilyoffice`, `pjtSans` in `invest-robinwealth`, `F37Bolton` or `Bolton` in `invest-robincapital` (any case; Assumptions, "Reference fonts and colours").

Per-sample criteria. An AC marked (browser) below is measured in a 1440×900 viewport on load unless it names 390 px. 390 px means a 390×844 viewport on load; AC97 uses the `width:390px` iframe of playbook §4, and AC96 is read there too. "The service section" is the AC28 section, "the steps section" is the AC29 section, and "the contact section" is the AC30 section. "The first section" is the part of the page from its top to the start of the service section. "The bars" are the fixed and sticky elements pinned to the top or bottom of the viewport; "the strip" is the bar that holds the AC12 marker. A link "outside the header and the bars" is outside the `<header>` and outside every bar. The edges and the centres of an `<h1>` and of a header wordmark are those of its rendered text, not of the element's box. A distance "from the top" is from the top edge of the viewport.

Sample B, `profile/invest-robinfamilyoffice/` (로빈패밀리오피스; 자문 · 가문 자산관리; reference Rockefeller Capital Management, rockco.com)

"The panel" is the dark green block of the first section. "The rule" is the thin vertical line at the left of the `<h1>`. "The back frame" is the first `<img>` of the first section in document order and "the front frame" is the second. "The script words" are the `<em>` of the `<h1>`: the last words of the headline, set slanted where Rockefeller sets a script.

- [ ] AC128 The `PROFILES` entry for `invest-robinfamilyoffice` has `palette` `["#f3eee2", "#18261e", "#123524", "#e3cf8e"]`, in that order, and the `title` "크림 헤더와 짙은 초록 패널의 패밀리오피스".
- [ ] AC129 In `invest-robinfamilyoffice/style.css` (custom properties resolved), the `body` background colour is `#f3eee2` and the `body` text colour is `#18261e`.
- [ ] AC130 At 1440 px and at 390 px, the strip of `invest-robinfamilyoffice` is pinned to the top of the viewport, spans its full width and has the computed background colour `#e3cf8e` and the computed text colour `#18261e` (a straw strip; `fitness-jjuuk` has a dark green strip over a cream header, A14) (browser).
- [ ] AC131 The `invest-robinfamilyoffice` `<header>` spans the full viewport width, has the computed background colour `#f3eee2`, is from 110 px to 180 px tall and is not fixed or sticky (the cream header kept) (browser).
- [ ] AC132 In the `invest-robinfamilyoffice` `<header>`, the bottom edge of the wordmark is above the top edge of the `<nav>` box, and the left edge of the `<nav>` box is within 64 px of the viewport's left edge (two rows kept: the wordmark above, the nav below) (browser).
- [ ] AC133 The horizontal centre of the `invest-robinfamilyoffice` header wordmark is within 24 px of the viewport's horizontal centre, at 1440 px and at 390 px (browser; Rockefeller's is at the left, A10).
- [ ] AC134 The first family in the computed `font-family` of the `invest-robinfamilyoffice` header wordmark is `Gowun Batang`, its computed `font-weight` is 700, its computed colour is `#123524`, and its computed `font-size` is from 20 px to 24 px at 1440 px and from 16 px to 19 px at 390 px (browser).
- [ ] AC135 The computed `letter-spacing` of the `invest-robinfamilyoffice` header wordmark is at least 0.25 times its computed `font-size`, at 1440 px and at 390 px (the letter-spaced serif wordmark kept) (browser).
- [ ] AC136 The `invest-robinfamilyoffice` `<header>` holds exactly one link whose text is "상담 문의"; its `href` is `#<id>` of the contact section, its computed background colour is transparent, each of its four borders is solid, at least 1 px wide and `#123524`, its computed `border-radius` is 0, and at 1440 px its right edge is within 64 px of the viewport's right edge and its top edge is above the top edge of the `<nav>` box (the framed outline button kept) (browser).
- [ ] AC137 The panel has the computed background colour `#123524`, spans the full viewport width, and its top edge is within 2 px of the bottom edge of the `<header>` (browser).
- [ ] AC138 The bottom edge of the panel is from 680 px to 840 px from the top (browser).
- [ ] AC139 The panel holds exactly one inline `<svg>` with `aria-hidden="true"` (the pattern); it is at least 90 % as wide and at least 90 % as tall as the panel, and its computed `opacity` is from 0.04 to 0.2 (the faint line pattern kept) (browser).
- [ ] AC140 The pattern holds only straight strokes: every shape in it is a `<line>`, or a `<path>` or `<polyline>` with the `fill` `none` whose path data uses only the commands M, L, H, V and Z in either case; it holds no `<text>`, `<circle>`, `<ellipse>` or `<image>` (a lattice, not Rockefeller's street map and not the curves of sample D).
- [ ] AC141 The `invest-robinfamilyoffice` `<h1>` lies inside the panel and fully inside the viewport, its left edge is from 48 px to 160 px from the viewport's left edge, and its right edge is at most 700 px from that edge (browser).
- [ ] AC142 The `invest-robinfamilyoffice` `<h1>` holds exactly one child `<span>` followed by exactly one child `<em>` and no text outside them; the text of each contains at least one Hangul syllable and no Latin letter.
- [ ] AC143 The `<span>` of AC142 has `Grandiflora One` as the first computed family, the computed `font-weight` 400, the computed colour `#f3eee2` and a computed `font-size` from 38 px to 52 px (the thin serif kept) (browser).
- [ ] AC144 The box of that `<span>` is from 3.0 to 7.0 times as tall as its computed `font-size` at 1440 px, and its text runs in three or four lines there (a paragraph of three or four lines as the headline, kept) (browser).
- [ ] AC145 The script words have `Gowun Batang` as the first computed family, the computed `font-weight` 400, the computed `font-style` `italic`, the computed colour `#e3cf8e`, the computed `display` `block`, and a computed `font-size` at least 1.6 times that of the `<span>` of AC142, at 1440 px and at 390 px (the last words slanted in a second face, larger, on their own lines, kept; Hangul has no italic, so the slant is the browser's, A8) (browser).
- [ ] AC146 The panel holds exactly one rule: an element with `aria-hidden="true"` and no text that is at most 3 px wide and at least 120 px tall and has the computed background colour `#e3cf8e`; its right edge is from 8 px to 40 px left of the `<h1>`'s left edge and its top edge is within 24 px of the `<h1>`'s top edge (the small ornament at the paragraph's start kept) (browser).
- [ ] AC147 The ornament of `invest-robinfamilyoffice` is a plain line, with no plant, crest or emblem on it (human; Rockefeller's is a thistle).
- [ ] AC148 At 1440 px and at 390 px, the first section of `invest-robinfamilyoffice` holds no link outside the header and the bars (a paragraph and no button under it, as in the reference) (browser).
- [ ] AC149 `invest-robinfamilyoffice` has exactly two `<img>` elements, both in the first section, each with `alt=""`, and its `img/` holds exactly two image files.
- [ ] AC150 Each frame has a computed `filter` that contains `grayscale(1)` and a computed `border-radius` of 0 (browser).
- [ ] AC151 Each frame is at least 320 px wide and at least 380 px tall, and the left edge of each is at least 640 px from the viewport's left edge (browser).
- [ ] AC152 The boxes of the two frames overlap by at least 80 px in width and at least 200 px in height; the left edge of the front frame is at least 80 px left of the left edge of the back frame, its top edge is at least 40 px below the top edge of the back frame, and at the centre of the overlap the front frame is the element on top (the two overlapping frames kept) (browser).
- [ ] AC153 The top edge of the back frame is inside the panel, and the bottom edge of the front frame is at least 24 px below the bottom edge of the panel and inside the viewport (the frames break the panel's lower edge) (browser).
- [ ] AC154 The left edge of the front frame is at least 24 px right of the right edge of the `<h1>` (browser).
- [ ] AC155 Each of the two photos shows a still life or a room with no person in it, not a hand and not a silhouette (human; A7; Rockefeller's two are archive photos of people).
- [ ] AC156 At 390 px, the `invest-robinfamilyoffice` `<header>` is at most 130 px tall, at least three links of its `<nav>` are visible in one row, and the AC136 link is not displayed (browser).
- [ ] AC157 At 390 px, `invest-robinfamilyoffice` has one bar pinned to the bottom of the viewport; it has an opaque background colour and holds exactly one link, whose text is "상담 문의" and whose `href` is `#<id>` of the contact section (AC42, AC43) (browser).
- [ ] AC158 At 390 px, the `<span>` of AC142 has a computed `font-size` of at least 26 px, and the whole `<h1>`, the script words included, lies inside the viewport on load and is not covered by a bar (the headline before the photos, A12) (browser).
- [ ] AC159 At 390 px, both frames are displayed below the `<h1>`, each is at least 200 px wide, their boxes overlap by at least 40 px in width and in height, the top edge of the higher frame is at most 660 px from the top, and at least 100 px of that frame's height shows above the bottom bar on load (the photos are part of the 390 px first screen) (browser).
- [ ] AC160 The service section of `invest-robinfamilyoffice` has the computed background colour `#f3eee2` behind it and holds exactly three columns, each with one heading and one paragraph; at 1440 px their top edges lie within 4 px of each other and no two overlap in width, and at 390 px they stack in one column (the cream section of three service columns kept) (browser).
- [ ] AC161 In `invest-robinfamilyoffice`, the service section comes before the steps section, and the steps section before the contact section (document order).
- [ ] AC162 The heading of the `invest-robinfamilyoffice` contact section contains "상담".
- [ ] AC163 `invest-robinfamilyoffice/index.html` requests from `fonts.googleapis.com` exactly the families `Grandiflora One` and `Gowun Batang`.
- [ ] AC164 In `invest-robinfamilyoffice`, at 1440 px and at 390 px, every element whose first computed family is `Grandiflora One` has the computed `font-weight` 400, every element whose first computed family is `Gowun Batang` has the computed `font-weight` 400 or 700, and no element of either family has own text that holds a digit (no synthesised bold; AC100) (browser).
- [ ] AC165 `invest-robinfamilyoffice/style.css` contains none of `#002a3a`, `#06262d`, `#bba984`, `#806a4d`, `#84744d`, `#ceb28a`, `#f3f1ec`, `#3b5542` or `#914124` (case-insensitive; Rockefeller's colours, read on 2026-11-21).
- [ ] AC166 In `invest-robinfamilyoffice/style.css`, every colour in a `background`, `background-color` or `background-image` value whose HSL lightness is below 0.3 and whose largest RGB channel minus its smallest is above `0x18` has an HSL hue from 135° to 165° (the dark surfaces are green; none is the teal 197° of the reference and of `law-ganeum`'s accent).
- [ ] AC167 The page text of `invest-robinfamilyoffice` contains none of: 세대째, 대대로, 대를 이어, 유서 깊, 전통의, 역사와 전통, 창립, 설립 이래, 명문가, 재벌 (sample policy: a fictional business has no history and names no family; Rockefeller's headline is "For more than seven generations"; AC74).

Sample C, `profile/invest-robinwealth/` (로빈자산관리; 자문 · 개인과 가족 자산관리; reference PJT Partners, pjtpartners.com, layout only)

"The narrow block" is the gradient block that holds the header wordmark. "The wide block" is the gradient block that holds the `<h1>`. "The photo" is the one `<img>` of the page. "The bottom bar" is the bar pinned to the bottom of the viewport.

- [ ] AC168 The `PROFILES` entry for `invest-robinwealth` has `palette` `["#fdfbf8", "#211a16", "#efe6dc", "#a6462b"]`, in that order, and the `title` "계단처럼 놓은 색 블록 둘과 밝은 실내 사진의 자산관리".
- [ ] AC169 In `invest-robinwealth/style.css` (custom properties resolved), the `body` background colour is `#fdfbf8` and the `body` text colour is `#211a16`.
- [ ] AC170 At 1440 px and at 390 px, `invest-robinwealth` has no bar pinned to the top of the viewport, and the computed background colour of its `<header>` is transparent (no header bar, kept) (browser).
- [ ] AC171 At 1440 px and at 390 px, the bottom bar of `invest-robinwealth` spans the full viewport width, has the computed background colour `#211a16`, and holds the AC12 marker and exactly one link, whose text is "상담 문의" and whose `href` is `#<id>` of the contact section (A9; AC42, AC43) (browser).
- [ ] AC172 The bottom bar of `invest-robinwealth` is at most 72 px tall at 1440 px and at most 120 px tall at 390 px (browser).
- [ ] AC173 Each of the two blocks has a computed `background-image` that is a `linear-gradient` whose colour stops are `rgb(181, 83, 58)` and `rgb(143, 58, 36)` and no other, and `invest-robinwealth/style.css` contains `#b5533a` and `#8f3a24` (case-insensitive; two blocks in one gradient, kept; the hue moved from blue, A6) (browser).
- [ ] AC174 The top and left edges of the narrow block are at the top and left edges of the viewport, its width is from 380 px to 480 px, and its height is from 250 px to 340 px (browser).
- [ ] AC175 The top edge of the wide block is at the top edge of the viewport, its left edge is within 2 px of the right edge of the narrow block, and its right edge is at the right edge of the viewport (browser).
- [ ] AC176 The wide block is from 370 px to 480 px tall and at least 80 px taller than the narrow block (the two blocks step down, kept) (browser).
- [ ] AC177 The narrow block holds the header wordmark and no other text and no other link (the mark alone in the narrow block, kept) (browser).
- [ ] AC178 The left edge of the `invest-robinwealth` header wordmark is within 64 px of the viewport's left edge, and its vertical centre is from 160 px to 300 px from the top at 1440 px (the lower left of the narrow block; PJT's mark is at the top left, A10) (browser).
- [ ] AC179 The first family in the computed `font-family` of the `invest-robinwealth` header wordmark is `Pretendard Variable` or `Pretendard`, its computed `font-weight` is at least 700, its computed colour is `#ffffff`, and its computed `font-size` is from 38 px to 46 px at 1440 px and from 20 px to 23 px at 390 px (browser).
- [ ] AC180 At 1440 px and at 390 px, the box of the `invest-robinwealth` header wordmark is from 1.9 to 2.7 times as tall as its computed `font-size` (two lines: 로빈 above 자산관리) (browser).
- [ ] AC181 The `<nav>` box of `invest-robinwealth` lies inside the wide block, its right edge is within 64 px of the viewport's right edge and its top edge is at most 100 px from the top; it holds at least four links, and the last one has the text "상담 문의" and the `href` `#<id>` of the contact section (browser).
- [ ] AC182 Every link of that `<nav>` has the computed colour `#ffffff`, a transparent computed background colour and no border (the nav as plain text with no button, kept) (browser).
- [ ] AC183 The `invest-robinwealth` `<h1>` holds exactly three child `<span>` elements and no text outside them, each `<span>` has the computed `display` `block`, and at 1440 px the box of each is at most 1.5 times as tall as its computed `font-size` (the three-line headline kept) (browser).
- [ ] AC184 The first family in the computed `font-family` of the `invest-robinwealth` `<h1>` is `Pretendard Variable` or `Pretendard`, its computed `font-weight` is from 400 to 500, its computed colour is `#ffffff`, and its computed `font-size` is from 44 px to 60 px (browser).
- [ ] AC185 The `invest-robinwealth` `<h1>` lies inside the wide block, its left edge is from 40 px to 120 px right of the wide block's left edge, and its top edge is below the bottom edge of the `<nav>` box (browser).
- [ ] AC186 At 1440 px and at 390 px, the wide block holds the sentence of AC32 below the `<h1>`, in the computed colour `#ffffff`, and holds no link outside the `<nav>` (browser).
- [ ] AC187 `invest-robinwealth` has exactly one `<img>` element, in the first section, with `alt=""`, and its `img/` holds exactly one image file.
- [ ] AC188 At 1440 px and at 390 px, the photo spans the full viewport width, its top edge is at most 4 px below the top of the viewport, its bottom edge is at or below the top edge of the bottom bar, and its box holds the boxes of both blocks (the photo runs under both blocks and fills the rest of the first screen, kept) (browser).
- [ ] AC189 At 1440 px and at 390 px, no element with own text intersects the photo's box outside the two blocks and the bars (no text on the photo, so every contrast of AC98 is measured on a flat colour) (browser).
- [ ] AC190 The image file of the photo has a mean luminance of at least 0.55 on a scale from 0 to 1, as the mean Rec. 709 luma of its gamma-encoded pixels (the bright photo kept).
- [ ] AC191 The photo shows a bright interior with daylight, and it shows no person, or only figures blurred past recognition who show no face (human; A7; PJT's photo shows people whose faces can be made out).
- [ ] AC192 At 390 px, the narrow block is at the top left of the viewport, from 100 px to 140 px wide and from 170 px to 240 px tall; the wide block runs from the narrow block's right edge to the viewport's right edge, starts at the top of the viewport, is at least 60 px taller than the narrow block, and its bottom edge is at most 500 px from the top (the wide block at the right and the photo under it, kept) (browser).
- [ ] AC193 At 390 px, the `invest-robinwealth` `<h1>` has a computed `font-size` of at least 22 px and lies inside the wide block and inside the viewport on load (browser).
- [ ] AC194 At 390 px, at least three links of the `<nav>`, the "상담 문의" link among them, are visible in one row inside the wide block above the `<h1>` (links in place of PJT's menu toggle; AC125) (browser).
- [ ] AC195 At 390 px, at least 220 px of the photo's height shows between the bottom edge of the wide block and the top edge of the bottom bar (browser).
- [ ] AC196 Between the first section's photo and the service list, `invest-robinwealth` has a statement: one paragraph of at least two lines with a computed `font-size` of at least 30 px at 1440 px and at least 20 px at 390 px, on the computed background colour `#fdfbf8` (the section of large plain text kept) (browser).
- [ ] AC197 The service section of `invest-robinwealth` holds a `<ul>` of at least four `<li>`; each `<li>` spans at least 60 % of the viewport width at 1440 px and has a solid top or bottom border at least 1 px wide (the list of services kept; not cards) (browser).
- [ ] AC198 In `invest-robinwealth`, the statement comes before the service section, the service section before the steps section, and the steps section before the contact section (document order).
- [ ] AC199 The heading of the `invest-robinwealth` contact section contains "상담".
- [ ] AC200 `invest-robinwealth/index.html` requests no family from `fonts.googleapis.com`.
- [ ] AC201 `invest-robinwealth/style.css` contains none of `#5050a7`, `#60b6f6`, `#4e3b98`, `#5ca1e6`, `#4e3f9b`, `#5c9de3`, `#1b1c52`, `#fa4a1f`, `#f78230`, `#f5ab71`, `#f9e49e`, `#f6deb7` or `#ffdbff` (case-insensitive; PJT's blue and orange gradient sets, read on 2026-11-21).
- [ ] AC202 In `invest-robinwealth/style.css`, every colour whose largest RGB channel minus its smallest is above `0x30` has an HSL hue from 5° to 40°, at any opacity (one warm family; no blue of 207°–229°, the reference's hue and that of `crypto-robincoin` and `food-saebyeokmil`).
- [ ] AC203 The page text of `invest-robinwealth` contains none of: 인수합병, M&A, 구조조정, 기업 매각, 자금 조달, 상장 주관 (sample policy: the sample is a 자문 business for individuals and families, and PJT is an advisory investment bank; Scope Out).

Sample D, `profile/invest-robincapital/` (로빈캐피탈; PE · 경영권 인수; reference Hg, hgcapital.com)

"The contours" are the line drawing behind the first section. "The nav pill" is the `<nav>` of the `<header>`. "The pink pill" is the 기업 문의 link. "The outline pill" is the link under the `<h1>`. "The sheet" is the element with the computed background colour `#fbf9ff` that holds the service section.

- [ ] AC204 The `PROFILES` entry for `invest-robincapital` has `palette` `["#230a47", "#f4effc", "#fbf9ff", "#ff6685"]`, in that order, and the `title` "보라 지면에 등고선과 분홍 알약을 둔 사모펀드 운용사".
- [ ] AC205 In `invest-robincapital/style.css` (custom properties resolved), the `body` background colour is `#230a47` and the `body` text colour is `#f4effc` (the deep violet page kept; hue 265°).
- [ ] AC206 At 1440 px and at 390 px, the strip of `invest-robincapital` is pinned to the top of the viewport, spans its full width and has the computed background colour `#16062e` (browser).
- [ ] AC207 The computed background colour of the `invest-robincapital` `<header>` is transparent, the `<header>` is not fixed or sticky, and the nearest non-transparent background behind the wordmark is `#230a47` (no header bar; the parts sit on the violet page) (browser).
- [ ] AC208 The left edge of the `invest-robincapital` header wordmark is within 64 px of the viewport's left edge, and its vertical centre is at most 120 px from the top, at 1440 px and at 390 px (the small wordmark at the top left kept) (browser).
- [ ] AC209 The first family in the computed `font-family` of the `invest-robincapital` header wordmark is `Orbit`, its computed `font-weight` is 400, its computed colour is `#f4effc`, its box is at most 1.6 times as tall as its computed `font-size`, and its computed `font-size` is from 28 px to 32 px at 1440 px and from 26 px to 29 px at 390 px (browser).
- [ ] AC210 The nav pill has a transparent computed background colour, four solid borders at least 1 px wide, and a computed `border-radius` of at least half its rendered height; it holds at least three links, each with the computed colour `#f4effc` (the outlined pill that holds the nav, kept) (browser).
- [ ] AC211 The `invest-robincapital` `<header>` holds exactly one pink pill: a link outside the nav pill whose text is "기업 문의" and whose `href` is `#<id>` of the contact section, with the computed background colour `#ff6685`, the computed colour `#230a47` and a computed `border-radius` of at least half its rendered height (browser; AC79; Hg's pill has white text at about 3.8:1, A6).
- [ ] AC212 At 1440 px, the right edge of the pink pill is within 64 px of the viewport's right edge, and the nav pill's right edge is from 0 px to 24 px left of the pink pill's left edge, with their vertical centres within 6 px of each other (the hot pill beside the nav pill, kept) (browser).
- [ ] AC213 The first section of `invest-robincapital` holds exactly one inline `<svg>` with `aria-hidden="true"` that is not inside a link (the contours); at 1440 px it is at least 1300 px wide and at least 560 px tall, and at 390 px at least 370 px wide and at least 480 px tall (browser).
- [ ] AC214 The contours hold at least eight `<path>` elements; each has the `fill` `none`, a stroke, and path data that holds a curve command (C, S, Q, T or A in either case), and the `<svg>` holds no `<text>`, `<line>`, `<rect>`, `<polyline>` or `<image>` (curved lines only; not the straight lattice of sample B).
- [ ] AC215 The contours read as faint terrain lines behind the text, with no axis, no rising line and no figure, and they are drawn new, not traced from Hg's shaded shapes (human; AC75).
- [ ] AC216 At 1440 px and at 390 px, the horizontal centre of the `invest-robincapital` `<h1>` is within 24 px of the viewport's horizontal centre, and the `<h1>` lies fully inside the viewport on load, above the sheet, and is not covered by a bar (the centred headline kept) (browser).
- [ ] AC217 The first family in the computed `font-family` of the `invest-robincapital` `<h1>` is `Orbit`, its computed `font-weight` is 400, its computed colour is `#f4effc`, and its computed `font-size` is from 56 px to 80 px at 1440 px and at least 28 px at 390 px (the light one-weight face kept) (browser).
- [ ] AC218 The box of the `invest-robincapital` `<h1>` is at most 1.5 times as tall as its computed `font-size` at 1440 px (one line, kept) and at most 2.9 times at 390 px (browser).
- [ ] AC219 At 1440 px and at 390 px, the first section of `invest-robincapital` holds, above the sheet, exactly one link outside the header and the bars (the outline pill): its text is "투자 분야 보기" and its `href` is `#<id>` of the service section; it has a transparent computed background colour, four solid borders at least 1 px wide, a computed `border-radius` of at least half its rendered height and the computed colour `#f4effc` (browser).
- [ ] AC220 At 1440 px and at 390 px, the top edge of the outline pill is below the bottom edge of the `<h1>` and at most 64 px from it, and its horizontal centre is within 24 px of the viewport's horizontal centre (browser).
- [ ] AC221 The top-left and top-right corners of the sheet have a computed radius of at least 12 px; at 1440 px the sheet has a gap from 8 px to 40 px to each side edge of the viewport, the two gaps differing by at most 4 px, and at 390 px a gap from 4 px to 16 px to each side (the white sheet with rounded top corners, kept) (browser).
- [ ] AC222 On load, the top edge of the sheet is from 600 px to 780 px from the top at 1440 px and from 540 px to 740 px at 390 px, and the nearest non-transparent background 6 px above that edge is `#230a47` (the sheet enters the first screen from below, kept) (browser).
- [ ] AC223 The top edge of the sheet is at the same document position at scroll position 0 and after a scroll of 600 px (no scroll effect; Hg's lower sections load on scroll) (browser).
- [ ] AC224 The sheet holds a row of at least four tags above its cards: each tag has own text made of Hangul syllables and spaces only, four solid borders and a computed `border-radius` of at least half its rendered height; no tag is or holds an `<a>`, and none has the computed `cursor` `pointer` (the tag pills kept, as labels of sectors and not as filters; AC80) (browser).
- [ ] AC225 At 1440 px, the top edge of every tag is inside the viewport on load (browser).
- [ ] AC226 The sheet holds at least three cards below the tags; each has a computed `border-radius` of at least 12 px and holds one heading and one paragraph; at 1440 px at least three sit side by side with top edges within 4 px of each other, and at 390 px the cards stack in one column (the cards kept) (browser).
- [ ] AC227 No card of the sheet shows a date, a company, a person or a news headline (human; A3; Hg's cards are dated news with a named person; AC27, AC73, AC80).
- [ ] AC228 The contact section of `invest-robincapital` has the computed background colour `#ece6fb` and the computed text colour `#230a47`, and spans the full viewport width (the pale closing section kept) (browser).
- [ ] AC229 The four links of AC36–AC39 in `invest-robincapital` are the items of one list; each has a computed `font-size` of at least 28 px at 1440 px and at least 20 px at 390 px, each spans at least 50 % of the viewport width at 1440 px, and each `<li>` has a solid top or bottom border at least 1 px wide (the large list of links kept) (browser).
- [ ] AC230 At 390 px, the nav pill and the pink pill of the `<header>` are not displayed, and no element is right of the wordmark in the `<header>` (browser; AC125: no "메뉴" pill).
- [ ] AC231 At 390 px, `invest-robincapital` has exactly one element pinned to the bottom of the viewport: a link whose text is "기업 문의" and whose `href` is `#<id>` of the contact section, with the computed background colour `#ff6685`, the computed colour `#230a47` and a computed `border-radius` of at least half its rendered height; it is at most 200 px wide and at most 56 px tall, and its bottom edge is from 12 px to 28 px above the bottom of the viewport (a floating pill, not a bar; AC42, AC43) (browser).
- [ ] AC232 At 390 px on load, at least 60 px of the sheet's height shows above the top edge of the AC231 link (browser).
- [ ] AC233 In `invest-robincapital`, the service section comes before the steps section, and the steps section before the contact section (document order).
- [ ] AC234 The heading of the `invest-robincapital` service section contains "투자 분야", and the heading of its contact section contains "기업 문의".
- [ ] AC235 `invest-robincapital` has no `<img>` element and no `img/` folder (pictures are CSS and inline SVG).
- [ ] AC236 `invest-robincapital/index.html` requests from `fonts.googleapis.com` exactly the family `Orbit`, and at 1440 px and at 390 px every element whose first computed family is `Orbit` has the computed `font-weight` 400 and no own text that holds a digit (browser for the second part; the face has one weight; AC100).
- [ ] AC237 In `invest-robincapital/style.css` and in the colour attributes of the inline `<svg>` elements of its `index.html`, every colour whose largest RGB channel minus its smallest is above `0x30` is `#ff6685` or has an HSL hue from 240° to 285°, at any opacity (violet and one hot pink, no third colour).
- [ ] AC238 In `invest-robincapital/style.css`, `#ff6685` appears as a `background` or `background-color` value only in rules for the pink pill, the AC231 link and `:focus-visible` outlines (human; one hot pill on the page, kept).
- [ ] AC239 `invest-robincapital/style.css` and the inline `<svg>` of its `index.html` contain none of `#160535`, `#1a0838`, `#1c0a44`, `#29155e`, `#2a0f6a`, `#6021d8`, `#b99fff`, `#ded7ff`, `#ff0078` or `#ba0050` (case-insensitive; Hg's colours, read on 2026-11-21).
- [ ] AC240 The page text of `invest-robincapital` contains none of: 뉴스레터, 구독, 소식 받기, 보도자료 (sample policy: no sign-up and no news; Hg's pink pill is "Stay informed" and its sheet is "Latest from Hg"; AC48).

All three invest samples

- [ ] AC241 No hex appears in the `palette` of more than one invest sample (case-insensitive).
- [ ] AC242 The first families in the computed `font-family` of the three `<h1>`s are pairwise different, and so are those of the three header wordmarks (browser).
- [ ] AC243 At 1440 px, the horizontal centre of the `invest-robinfamilyoffice` header wordmark is at least 300 px right of the horizontal centres of the other two header wordmarks (browser).
- [ ] AC244 At 1440 px, the vertical centre of the `invest-robinwealth` header wordmark is at least 90 px further from the top than that of the `invest-robincapital` header wordmark (browser).
- [ ] AC245 At 1440 px, the computed `font-size` values of the three header wordmarks differ pairwise by at least 4 px (browser).
- [ ] AC246 At 390 px, the horizontal centre of the `invest-robinfamilyoffice` header wordmark is at least 60 px right of the horizontal centres of the other two, and the computed `font-size` values of the `invest-robinwealth` and `invest-robincapital` header wordmarks differ by at least 3 px (browser).
- [ ] AC247 At 1440 px, the `<h1>` lies wholly left of the viewport's horizontal centre in `invest-robinfamilyoffice`, its horizontal centre is right of the viewport's horizontal centre in `invest-robinwealth`, and its horizontal centre is within 24 px of the viewport's in `invest-robincapital` (browser).
- [ ] AC248 Exactly one invest sample, `invest-robincapital`, has a `body` background colour whose HSL lightness is below 0.2.
- [ ] AC249 Side by side, the three header wordmarks differ in position, size and typeface, and no two read as one mark with a word changed (human).
- [ ] AC250 Side by side with the 390 px first screens of `food-saebyeokmil`, `clinic-bonui`, `crypto-robincoin`, `law-ganeum`, `crypto-robinchain` and `interior-robinhome`, no invest sample's 390 px first screen is the usual stack of those six in other colours: a top strip, a bar with the wordmark at the left and a button at the right, a small label, a headline at the left, a paragraph, two buttons side by side and a picture (human; the measurable forms are AC133, AC148, AC158, AC192, AC195, AC216, AC222 and AC230; AC104).
- [ ] AC251 Side by side, the three `thumb.jpg` files show three different first screens: a cream header over a dark green panel with two overlapping black-and-white photos; two terracotta blocks stepping down over a bright room; and a violet page of contour lines with a centred headline and a white sheet (human; AC109).

## Assumptions

- The industry key is `invest` with the label 투자자문; it already exists in `INDUSTRIES` in `scripts/profiles.py`, and no `PROFILES` entry uses it yet (checked 2026-11-21).
- **Naming (human decision, binding).** Each sample's name is "로빈" plus a field word, so the name alone shows it is a sample. This feature runs no name-collision check and writes no `name-check.txt`. This overrides "상호는 가상" in playbook §2; the rest of §2 holds. The slug is `invest-` plus the name in Latin letters (AC4). The human's example was 로빈투자자문; at G1 the human chose names that hold no word of 자본시장법 제38조 (A2).
- **Two 업태, not one (orchestrator decision).** The request's "투자자문(프라이빗에쿼티)" is not narrowed. The human's pick at G1 (A1) gives two 자문 samples, B and C, and one PE sample, D. A 자문 sample presents advice and care of assets for individuals and families, and its name holds no word of 자본시장법 제38조 (A2).
- **Kept traits (human decision, law run 2026-11-18; applied here by the orchestrator).** The listed traits of a picked screenshot stay, and everything else is made new. "Not the same site" is met through pictures, palette, typeface, copy and section order (AC107), never by removing a kept trait (AC106). Where a content rule or a shipped sample collides with a trait, the candidate lists it under "Conflicts" with a substitute; the human accepted the substitutes at G1 (A3), and A5 fixes the hue moves.
- **Strict forms (human decision, G1 2026-11-21, A3).** No person, no form, no login or portal label, no figure and no portfolio company. The looser forms that the references show are not used.
- **No script (agent decision).** No sample has a `<script>` (AC49). Sixteen of the eighteen shipped samples have none. A page that looks like an investment firm and runs no code cannot collect or send anything.
- **Sticky marker and non-business sentence (agent decision).** The sample marker stays on screen at every scroll position (AC12), as the law and crypto samples do. The contact section and the first screen say the business is not a 금융투자업자 and that the page is no 투자 권유 (AC31, AC32). One sentence serves both 업태. A real PE house is a registered 업무집행사원 and not a 금융투자업자 in every case; for a fictional business the sentence is true either way.
- **Contact shape (agent decision).** Every sample has 카카오톡 상담, 전화, 네이버 예약 (방문 상담 예약) and 네이버 지도 (오시는 길) as `#` links in its contact section, as playbook §3 asks. On a PE page these are for a company owner or an institution (AC79). None of the sites opened shows 카카오톡 or 네이버 except 쿼터백 (a floating 카카오톡 "문의하기" button and a "문의하기" button under the headline).
- **Word lists (agent decision).** 수익 also bars 수익자 and 수익성; 보장 bars 사회보장; 실적 bars 영업 실적; 리딩 bars 리딩 as "leading"; 인가 and 허가 bar 인가받은 and 허가받은; 호 after a digit bars a fund number and also a room number in an address, so addresses carry no 호. Copy uses other words. 펀드, 사모펀드 (PE only), 투자, 운용, 자문, 일임, 포트폴리오, 회수, 위험 and 수수료 (with no figure) stay allowed.
- **Rule sources, read on 2026-11-21 in Chrome (headless) on law.go.kr (국가법령정보센터) and law.kofia.or.kr. Articles were found by text search in the saved page text.**
  - 자본시장과 금융투자업에 관한 법률 [시행 2026-11-13, 법률 제21647호], `https://www.law.go.kr/법령/자본시장과금융투자업에관한법률`. 제6조⑦ (투자자문업) · ⑧ (투자일임업: 투자자별로 구분하여 운용); 제9조⑦ (모집: 50인 이상에 대한 청약의 권유) · ⑧ (사모) · ⑲ (사모집합투자기구: 기관전용 and 일반); 제11조 (무인가 영업 금지; 투자자문업 · 투자일임업 · 일반 사모집합투자업 제외); 제17조 (미등록 투자자문업 · 투자일임업 금지; 제445조: 3년 이하 징역); 제38조 (상호: 금융투자, 증권, 파생, 선물, 집합투자, 투자신탁, 자산운용, 투자자문, 투자일임, 신탁; 제446조 has the penalty); 제55조 (손실보전 · 이익보장 금지); 제57조 (투자광고) is **deleted** (2020-03-24), and so are 제46조, 제47조 and 제49조 (적합성, 설명의무, 부당권유) — these moved to 금융소비자보호법; 제98조의2 (성과보수의 제한, title only); 제101조① (유사투자자문업 신고: 대가를 받고 간행물 · 방송 등으로 하는 개별성 없는 조언); 제101조의3 (유사투자자문업자의 표시 · 광고: 개별 상담 불가, 원금 손실, 정식 금융투자업자가 아님); 제249조 (미등록 일반 사모집합투자업 금지); 제249조의5 (일반 사모집합투자기구의 투자광고: 전문투자자와 잔고 1억원 이상 일반투자자에게만, 서면 · 전화 · 전자우편 등으로 개별적으로); 제249조의11⑥ (기관전용 사모집합투자기구의 유한책임사원: 개인이 아닌 자); 제249조의15① (업무집행사원의 등록); 제249조의20① (제249조의2–제249조의6 do not apply to 기관전용 사모집합투자기구, so 제249조의5 does not either).
  - 자본시장법 시행령 [시행 2026-11-13, 대통령령 제36823호]: 제42조 (상호의 제한: financial investment, securities, asset management, investment advisory and their Hangul forms and like foreign words); 제2조2호 (청약의 권유: 광고, 안내문, 전자통신 등으로 증권을 발행한다는 사실을 알리거나 취득 절차를 안내하는 활동). No other article of the 시행령 was read.
  - 금융소비자 보호에 관한 법률 [시행 2026-01-02, 법률 제21065호], `https://www.law.go.kr/법령/금융소비자보호에관한법률`. 제3조3호 (투자성 상품); 제11조, 제12조 (금융상품판매업등 등록; 제67조: 5년 이하 징역 또는 2억원 이하 벌금); 제17조 (적합성원칙; ⑤: 전문투자형 사모집합투자기구에는 적용 제외); 제21조 1 · 2 · 4 · 6호 (부당권유: 단정적 판단, 사실과 다른 내용, 근거 없는 비교, 요청 없는 방문 · 전화 권유); 제22조① (금융상품판매업자등이 아닌 자는 금융상품등에 관한 광고를 할 수 없다; 협회등 예외), ② (명확하고 공정하게), ③ (필수 내용: 설명서 및 약관 읽기 권유, 명칭과 상품 내용, 투자에 따른 위험, 과거 운용실적이 미래 수익률을 보장하지 않는다는 사항; 제17조⑤ 본문의 투자성 상품은 제외), ④2호 (투자성 상품: 손실보전 · 이익보장 오인, 좋은 기간의 수익률만 표시); 제69조①5호 (제22조① · ③ · ④ 위반: 1억원 이하 과태료).
  - 금융소비자보호법 시행령 [시행 2026-04-28, 대통령령 제36287호]: 제17조 (광고의 주체: ① 투자성 상품을 취급하는 금융상품판매대리 · 중개업자는 광고할 수 없다; ② 금융지주회사, 증권의 발행인 · 매출인, 집합투자업자 등은 광고할 수 있다); 제18조①2호 (투자에 따른 위험: 원금 손실 발생 가능성, 원금 손실에 대한 소비자의 책임), ③ (설명을 받을 권리 등); 제19조② (준법감시인 심의); 제20조① (단정적 판단, 근거 없는 비교 등), ③ (집합투자증권 광고에 쓸 수 있는 사항), ④.
  - 금융투자협회 「금융투자회사의 영업 및 업무에 관한 규정」 (law.kofia.or.kr, 현행; 개정 이력의 마지막 2026-08-19). 제2-35조 (투자광고의 정의; ②2호 가목: 명칭, 로고, 주소 · 연락처, 업무절차 등 단순 정보는 투자광고가 아님), 제2-36조, 제2-37조 (의무 표시사항; ⑥: 위험고지의 색과 활자 크기), 제2-38조 1–15호 (금지행위: 손실보전 오인, 좋은 기간의 수익률, 예상 · 목표수익률, 사모 상품 내용 표시 (5호), 근거 없는 비교, 투자일임재산의 집합 운용 표시 (7호), 수상실적 · 통계수치 (12호), 초상권 (13호)).
  - 유사수신행위의 규제에 관한 법률 [시행 2024-05-28, 법률 제20367호]: 제2조 1 · 2 · 4호, 제3조, 제4조 (표시 · 광고 금지; 제6조②: 2년 이하 징역 또는 2천만원 이하 벌금), 제5조 (금융업 유사상호).
  - 표시 · 광고의 공정화에 관한 법률 [시행 2025-01-21, 법률 제20712호]: 제3조①1–4호 (거짓 · 과장, 기만, 부당 비교, 비방).
- **What the reading means for a sample (agent reading, not legal advice).** A sample is a design demonstration by RobinTech, which is not a 금융상품판매업자등. Under 금융소비자보호법 제22조① a page that advertises a 금융상품 or such a business may not be published by anyone else. 시행령 제17조② adds a short list of others, and a web agency is not on it. So the samples name no product, state no result, say on the first screen that the business is fictional and that the page is no 투자 권유 (AC31, AC32), and stay close to what KOFIA 제2-35조②2호 calls simple information: name, contact and how the work goes.
- **Not verified against a primary source.**
  - KOFIA 규정 별표 9 (의무 고지사항), 별표 10 (투자광고 금지행위) and 별표 10-1 (온라인 투자광고 심사기준): attached files, not opened. 제2-39조 (온라인 투자광고) and 제2-40조 onward were not read. AC57–AC59 and AC71 are written on the strict side for that reason.
  - 금융소비자보호 감독규정 (제17조, 제19조: 광고의 글자 · 내용 기준) and 금융투자업규정: not opened.
  - 자본시장법 제18조 (등록 요건), 제98조 (투자자문업자 · 투자일임업자의 불건전 영업행위), 제98조의2 (body), 제101조의2 and the 시행령 beyond the two articles above: not read. 표시광고법 시행령: not read. 유사수신법 시행령 제2조 (제5조의 명칭 목록) was read after G1 (A15).
  - Whether 자본시장법 제38조 reaches a name shown on a sample page that is no registered 상호: not settled by the text read. The human chose to use none of its words (A2).
  - Whether a 기관전용 사모집합투자기구's 업무집행사원 may advertise itself at all, and under which rule: no article on it was found in the text read. 제249조의5 does not apply to it (제249조의20①). AC77–AC80 are written on the strict side.
  - 금융위원회, 금융감독원 guidance (투자광고 가이드라인, 유사투자자문업 유의사항): no page of fsc.go.kr or fss.or.kr was opened.
- **Accent hues today (from the crypto spec's list and its palettes, not re-measured).** Chromatic accents: 9°, 19°, 31°, 36°, 60°, 82°, 134°, 168°, 197°, 210°, 230°, 266°, 303°, 329°, 342°, 346°. Under the beauty feature's rule (25° from every other accent) one band stays free: about 107°–109° (a yellow-green).
- **Shipped samples seen (the eighteen `thumb.jpg` files, side by side, 2026-11-21).** Dark first screens: `beauty-robinhair`, `flower-bomgyeol`, `law-ganeum`, `interior-robinhome`, `crypto-robinchain`. Flat saturated colour: `interior-robindesign`, `crypto-robincustody`. White or near white: `clinic-neuru`, `clinic-bonui`, `clinic-byeotteul`, `fitness-mideoum`, `beauty-robinsalon`, `interior-robininterior`, `crypto-robincoin`. Cream or grey: `food-saebyeokmil`, `fitness-jjuuk`, `beauty-robinhairsalon`, `law-goim`. No shipped sample has a soft colour-field gradient, a deep teal panel with overlapping black-and-white photos, colour blocks that step down over a bright photo, or a violet page of contour lines.
- §6-1 check: `git diff --stat d61f2c4..HEAD` (the `last_reconciled` in `overview.md`) shows one `overview.md` line and SHA updates in the crypto documents, all under `docs/`. `current_system/` describes the system.
- **How the sites were opened.** Headless Chrome (the installed Google Chrome), 1440×900, Korean locale, 2026-11-21. 45 addresses were tried and 42 pages rendered; three did not load and two more showed only a gate (the table below). The eight short-listed pages were opened again at 1440×900 and at 390×844 with cookie panels hidden by CSS, and as full-page captures. No cookie banner was accepted, no file was downloaded, and no login or sign-up was made. Lower sections of Rockefeller, PJT and Hg load on scroll and did not render in the full-page capture; their sketches below the first screen come from the page text. Mobbin was not used.
- **Candidate screenshots (2026-11-21)** are in the orchestrate run's scratchpad `invest-candidates/` folder and in `.git/robintech-dev/keep/` as `ref-g1-invest-A.jpg` … `ref-g1-invest-D.jpg` (1440×900) and `ref-g1-invest-A-390.jpg` … (390×844), not in the repository. Rockefeller's first screen is a slide show that starts with a loader; `B.jpg` is its first slide (deep teal), taken about ten seconds after load, and `ref-g1-invest-B-slide2.jpg` is its second slide (cream, same layout). `B.jpg` shows two archive photos of real people, `C.jpg` shows blurred people in an office, and `A.jpg` shows faces in two cards at its lower edge, as the references do.
- **Photos.** No photo is downloaded at this stage. A7 states the direction for B and C. The Unsplash search API (`unsplash.com/napi`) is not used.
- **Reference fonts and colours (read 2026-11-21: the home pages' public stylesheets, and pixels of the G1 screenshots).** Rockefeller: `Chiswick Headline Web` and `Inter`; panel `#002a3a` (hue 197°), gold `#bba984`, brown `#806a4d`, cream `#f3f1ec`; the stylesheet also holds `#06262d`, `#84744d`, `#ceb28a`, `#3b5542` and `#914124`. PJT: `pjtSans`; the first screen's blocks run from `#5050a7` to `#60b6f6` (screenshot pixels: hue 207°–239°); the stylesheet holds more gradient sets, among them `#4e3b98`, `#5ca1e6`, `#4e3f9b`, `#5c9de3`, `#1b1c52` (blue), `#347e53`, `#a4d089` (green), `#286382`, `#58cab8` (turquoise), `#b42c6b` (magenta), `#553d98` (purple) and `#fa4a1f`, `#f78230`, `#f5ab71`, `#f9e49e`, `#f6deb7`, `#ffdbff` (orange and pink). Hg: `F37Bolton`; page `#160535` (hue 261°), pink `#ff0078` (332°), `#ba0050`, violets `#6021d8`, `#b99fff`, `#ded7ff`, `#29155e`, `#1a0838`, `#1c0a44`, `#2a0f6a`. AC165, AC201, AC239 and AC127 ban these.
- **390 px first screens of shipped samples (rendered 2026-11-21 in 390×844 frames: `food-saebyeokmil`, `clinic-bonui`, `crypto-robincoin`, `law-ganeum`, `crypto-robinchain`, `interior-robinhome`, `crypto-robincustody`, `law-goim`).** Six of the eight share one stack: a top strip, a bar with the wordmark at the left and a button at the right, a small label, a headline at the left, a paragraph, two buttons side by side, a picture, and a bottom bar of buttons. `interior-robinhome` centres its wordmark and headline over and under a photo, and `law-goim` opens with a photo. AC250 is written against that stack.
- **Design stage.** The checks start from `check_static.py` and `check_browser.py` of the crypto feature. An AC marked (browser) needs the browser checker, an AC marked (human) a person, and the rest a command on the files. Fixed pixel ranges come from the 1440×900 and 390×844 reference screenshots. The design stage rendered a fixture page for each sample on 2026-11-21 (Chrome, real web fonts, 1440×900 and 390×844): every pixel range of AC128–AC247 held together on it, and no range was changed. The design stage changed three criteria, in wording only: AC148 and AC177 got the (browser) mark, because a bar and a gradient block are known only from computed styles, and AC190 names its measure. It also replaced the fixed sentence of AC77 with one that states the sample firm's own policy, and made AC112 name the commit it compares against. `tasks.md` ("Fixed parameters") holds how each check reads the page, among them: the contact section of AC30 is the one 문의 · 상담 section that is neither the service nor the steps section (C's steps heading is 상담 과정, A11); AC98 judges a gradient at each of its stops and asks 3:1 of heading text of 24 px or more; AC242 reads the `<h1>` element, so B's `<h1>` rule names `Grandiflora One`.

### Decisions after G1

- A1 (decided 2026-11-21, human Seokhyun Kim, G1): build three samples: B, C and D. Candidate A (Verdane, 로빈에쿼티 `invest-robinequity`) is not built. The sample letters stay B, C and D. So the feature has two 자문 samples and one PE sample. This closes Q1.
- A2 (decided 2026-11-21, human, G1): no word of 자본시장법 제38조 is used in a name. B Rockefeller Capital Management → 로빈패밀리오피스 `invest-robinfamilyoffice` (자문 · 가문 자산관리); C PJT Partners, layout only → 로빈자산관리 `invest-robinwealth` (자문 · 개인과 가족 자산관리); D Hg → 로빈캐피탈 `invest-robincapital` (PE · 경영권 인수). 로빈투자자문 is not used (AC114–AC116). This closes Q2.
- A3 (decided 2026-11-21, human, G1): "none of them", the strict substitutes as each candidate states them. Figure tiles become words; no portfolio company, no named person and no date; no team; no form; no "출자자 전용", "고객 로그인" or other portal label; no block of example figures. 문의 is the four `#` links only: 카카오톡, 전화, 네이버 예약 and 네이버 지도. AC27, AC48, AC55, AC73, AC74, AC80 and AC91 stand as written, and their G1 marks are removed. This closes Q3 and Q4.
- A4 (decided 2026-11-21, human, G1): the 25° accent-hue rule of the beauty feature does not apply to `invest`. AC105 (no shared accent hex) and the side-by-side checks AC103, AC104, AC109, AC250 and AC251 stay. This closes Q5.
- A5 (decided 2026-11-21, orchestrator): the picked compositions stay, and the distance from shipped samples comes from palette, pictures, typeface, copy and section order.
  - B keeps the first slide: a two-row cream header, a dark patterned panel, a thin serif paragraph as the headline with its last words in a script or italic face, and two overlapping frames that break the panel's lower edge. The panel moves off teal 197°, the hue of `law-ganeum`'s accent. The frames hold black-and-white photos with no person, or line drawings; the agent picks (A7).
  - C keeps two stepped blocks of different width, the nav and a three-line headline inside the wide block, and a bright interior photo under both. The blocks move off blue 207°–229° (`crypto-robincoin` 210°, `food-saebyeokmil` 230°). One photo, with no person or with figures blurred past recognition.
  - D keeps the deep violet page, the contour lines, the pill nav with one pink pill, the centred one-line headline and the rising white sheet. Its distance from `crypto-robinchain` is the violet page, the contours, the white sheet and the centred headline. No photo.
  - The three wordmarks differ in position, size and typeface. Each sample's 390 px first screen is fixed by ACs, so that none is a shipped first screen in other colours. The sample marker is at body size or larger. Pixel ACs are written only for what a kept trait needs, and each AC says whether a command or a person decides it.
- A6 (decided 2026-11-21, agent): palettes. Contrast ratios are WCAG 2, computed on 2026-11-21; AC98 checks contrast on the built pages. The three hue families sit about 120° apart: green 151°, terracotta 13°, violet 265°.
  - B: page and header cream `#f3eee2`; text on cream `#18261e` (13.59:1); panel dark green `#123524` (hue 151°; cream on it 11.62:1); accent straw `#e3cf8e` (hue 46°; 8.70:1 on the panel), used for the slanted words, the rule and the strip, where `#18261e` text on it is 10.18:1. The accent is not used for text on cream. Green was picked over a burgundy panel because burgundy sits beside D's pink and beside the dark red photo of `flower-bomgyeol`; 151° lies between `fitness-jjuuk`'s accent (134°) and `clinic-neuru`'s (168°), and neither of those is a dark surface. Rockefeller's panel is `#002a3a` (197°).
  - C: page `#fdfbf8`; text and bottom bar `#211a16` (16.61:1 on the page); soft surface `#efe6dc`; accent terracotta `#a6462b` (hue 13°; 5.76:1 on the page, 4.82:1 on `#efe6dc`). The block gradient runs from `#b5533a` to `#8f3a24`; white text on it is 4.93:1 at the lightest point and 7.50:1 at the darkest, so the nav links pass AC98 anywhere on the block. PJT's stylesheet holds gradient sets in blue, green, turquoise, magenta, purple and orange; no hue is free of them, so the distance is in the values (AC201) and in the muted tone. Green was not picked for C: it is B's family and PJT's second set. The warm page of `crypto-robincustody` (`#f5c08a`, 30°) is a flat light apricot; C's blocks are darker and redder and sit over a photo.
  - D: page violet `#230a47` (hue 265°); text `#f4effc` (15.42:1); sheet `#fbf9ff` with `#230a47` text (16.67:1); closing section `#ece6fb` with `#230a47` text (14.33:1); strip `#16062e`; accent pink `#ff6685` (hue 348°) with `#230a47` text (6.21:1). White on this pink is 2.80:1, and white on Hg's `#ff0078` is about 3.8:1, so the pill label is dark. Hg's page is `#160535` (261°); `fitness-mideoum`'s accent is 266°, on a near-white page.
  - No accent equals a hex in another `PROFILES` entry (AC105), and no hex is in two of the three palettes (AC241).
- A7 (decided 2026-11-21, agent): pictures.
  - B: two photos, shown in black and white by a CSS filter (AC150). Photos were picked over line drawings: D is line work in SVG and `crypto-robincustody` has a line drawing, so photos keep B apart from both. Direction: still lifes and rooms with no person, for example a desk with paper and a pen, a window with a curtain, a stair rail. The panel's pattern is a lattice of straight lines drawn in inline SVG (AC140), like a window lattice; it is not a map.
  - C: one colour photo of a bright interior with daylight (a corridor, a meeting room or a stair with glass), with no readable sign. No person is the first choice; figures blurred past recognition are allowed (AC191).
  - D: no photo. The contours are curved stroked paths in one inline SVG (AC214), drawn new.
  - The photos are chosen and downloaded in the implement stage under playbook §3 and AC85–AC93. The Unsplash search API (`unsplash.com/napi`) is not used.
- A8 (decided 2026-11-21, agent): typefaces. Body text, nav, hours and phone digits are Pretendard in all three (AC120, AC121).
  - B: `Grandiflora One` (one weight, a thin Hangul display face) for the headline paragraph, and `Gowun Batang` for the wordmark (weight 700) and for the last words of the headline (weight 400, slanted by `font-style: italic`). Hangul has no italic and Google Fonts has no formal Hangul script; the faces were rendered at the AC sizes on 2026-11-21. `Nanum Pen Script` reads as a marker pen, too casual for this business, and `Grandiflora One` is too thin for a wordmark of 16–24 px on cream, so both were set aside for those uses. `Hahmlet` and `Diphylleia` were set aside because `law-ganeum` and `interior-robinhome`, B's nearest shipped samples, use them. No shipped sample loads `Grandiflora One`; `fitness-mideoum` loads `Gowun Batang` for an upright headline on a near-white page.
  - C: Pretendard only, with no Google Fonts family: the wordmark at weight 700 or more in two lines, the `<h1>` at weight 400–500 in white. `IBM Plex Sans KR` was set aside because `law-goim`, the other sample with a box over a wide photo, uses it. `crypto-robincoin` and `food-saebyeokmil` also set their `<h1>` in Pretendard, at weight 600 or more and in dark type on a light page.
  - D: `Orbit` (one weight, a monoline face) for the wordmark and the `<h1>`. No shipped sample loads it.
  - On 2026-11-21 `fonts.googleapis.com` served `Grandiflora One` and `Orbit` with Hangul ranges in weight 400 only, and `Gowun Batang` in 400 and 700. `Orbit` sets wide gaps between words at headline size; the design stage may tighten `word-spacing`.
- A9 (decided 2026-11-21, agent): where the common first-screen items sit, at 1440 px and at 390 px. AC48 and AC49 leave no way to open a menu, so no sample draws a menu toggle (AC125).
  - B: the marker in a straw strip pinned to the top (AC130). The non-business sentence of AC32 in the panel under the headline. The 문의 link is the framed button of the header at 1440 px, and a bottom bar with one 상담 문의 link at 390 px (AC157), where the header shows the wordmark and a row of nav links.
  - C: nothing is pinned to the top, so the blocks start at the top edge. The marker and one 상담 문의 link are in a bar pinned to the bottom at both widths (AC171). The non-business sentence is in the wide block under the headline (AC186). The nav stays a row of text links inside the wide block at 390 px (AC194). No text lies on the photo (AC189).
  - D: the marker in a strip pinned to the top (AC206). The non-business sentence under the outline pill, above the sheet. The 문의 link is the pink pill of the header at 1440 px; at 390 px the header shows the wordmark alone and the pink pill floats near the bottom edge (AC231), so the sheet still shows above it (AC232).
- A10 (decided 2026-11-21, agent): wordmarks. All three references put the mark at the top left. B: centred in the first row of the cream header, 20–24 px, letter-spaced `Gowun Batang` 700 in green. C: at the lower left of the narrow block, 38–46 px, Pretendard in white, in two lines; the break between 로빈 and 자산관리 is made without a space or a `<br>` in the name: by the box width, or by block `<span>`s with `aria-label="로빈자산관리"` on the link (a browser joins two block lines with a space), so that AC18 holds. D: at the top left, 28–32 px, `Orbit`. AC243–AC246 hold the pairwise gaps. `interior-robinhome` and `crypto-robincustody` also centre their wordmarks; B's sits in a cream header above a second row.
- A11 (decided 2026-11-21, agent): section order and headings, within AC28–AC30. B: first section, 하는 일 in three columns, 일하는 방식, 상담 문의. C: first section, a statement in large type, 하는 일 as a list, 상담 과정, 상담 문의. D: first section, 투자 분야 on the sheet (tags and cards), 투자 방식, 기업 문의 as a large list of links on the pale closing section. The design stage fixes the wording.
- A12 (decided 2026-11-21, agent): what each sample improves on its reference. B: a Korean headline that is readable on load (the reference's script words fade in); the headline before the photos at 390 px (AC158); no login label. C: a 상담 문의 link on a first screen that has no action in the reference; no text over the photo; lower sections that show without a scroll effect. D: a dark label on the pink pill for contrast; a sheet that is in place on load (AC223); sector words in place of dated news. All three: the sample marker, the non-business sentence, the Korean contact links and the risk sentence.
- A13 (decided 2026-11-21, agent): gallery card titles. B "크림 헤더와 짙은 초록 패널의 패밀리오피스"; C "계단처럼 놓은 색 블록 둘과 밝은 실내 사진의 자산관리"; D "보라 지면에 등고선과 분홍 알약을 둔 사모펀드 운용사". `summary` and `features` are written in the implement stage under AC76. Counts in card text are written as words, because AC73 bars digits with units.
- A14 (decided 2026-11-21, agent): nearest shipped designs, for the person who judges AC103 and AC104. B: `law-ganeum` (dark panel, serif headline at the left), `interior-robinhome` (centred wordmark, serif line on dark blue) and, in the header zone, `fitness-jjuuk` (a dark green strip, a cream header and a centred green wordmark in a fat face); B differs by the straw strip, the two-row header with a thin letter-spaced wordmark, the dark green panel, the paragraph headline with slanted words, the two overlapping photos and the absence of a button under the headline. C: `law-goim` (a box over a wide photo) and `crypto-robincoin` (a gradient panel on a light page); C differs by the stepped blocks at the top edge with the headline inside and by having no header bar. D: `crypto-robinchain` (dark page, one hot colour, pill parts) and `law-ganeum`; D differs by the violet page, the contours, the centred one-line headline and the white sheet.
- A15 (decided 2026-11-21, agent): the names and 유사수신법. 유사수신행위의 규제에 관한 법률 시행령 제2조 [시행 2019-01-08, 대통령령 제29477호], read on 2026-11-21 on law.go.kr, lists the names of 법 제5조: 금융 or 파이낸스; 자본 or 캐피탈; 신용 or 크레디트; 투자 or 인베스트먼트; 자산운용 or 자산관리; 펀드, 보증, 팩토링 or 선물; and foreign words of the same meaning. 캐피탈 and 자산관리 are on it. 법 제5조 bars such a name only "유사수신행위를 하기 위하여", and the samples raise no funds, take no deposit and are marked as fictional on every screen (AC12, AC31, AC32). The names are the human's decision at G1 (A2), made on 자본시장법 제38조; they stay. This is an agent reading, not legal advice, and it is reported to the human as a remaining risk.
- A16 (decided 2026-11-21, agent): no criterion is withdrawn. Each of AC1–AC113 was checked against A1: none names candidate A or holds only for it. AC106, AC108 and AC110 now point at the per-sample criteria in place of "after G1".

### Research: sites looked at (2026-11-21, headless Chrome; history)

| Site | 업태 | Result |
| --- | --- | --- |
| verdane.com (Verdane, Norway) | PE (growth) | Candidate A |
| rockco.com (Rockefeller Capital Management, US) | 자문 · 자산관리 (family office) | Candidate B |
| pjtpartners.com (PJT Partners, US) | 부티크 IB (reference for a 자문 layout) | Candidate C |
| hgcapital.com (Hg, UK) | PE (buyout) | Candidate D |
| cinven.com (Cinven, UK) | PE | Runner-up for D. Photos cut by two large arcs on a dark teal page, a floating dark pill nav, a centred light headline. Strong; its teal sits beside candidate B's, and the photos carry the page. |
| farther.com (Farther, US) | 자문 · 자산관리 | Runner-up for C. A dark photo of forest in mist, a centred thin serif headline, and three pale blue figure cards ("$23B", "#1", "4.5x") that straddle the photo's lower edge. Refined; a dark photo with a centred serif headline is the first screen of `beauty-robinhair`, and word cards in place of the figures would repeat `crypto-robincustody`. |
| nordiccapital.com (Nordic Capital) | PE | White header with a copper small-caps serif wordmark and a three-column text nav, then a dark photo of people with a serif headline. Near `law-goim` in tone. |
| summaequity.com (Summa Equity) | PE | White pill header over a full photo of a recycling plant, centred serif headline. Near `fitness-mideoum` and `crypto-robincustody` (pill header). |
| generalcatalyst.com (General Catalyst, US) | VC | Pale paper page, a condensed display wordmark, a centred video and a right column of figures ("$43B+", "900+"). 벤처투자 is another 업태 (Scope Out). |
| thomabravo.com (Thoma Bravo, US) | PE | Black page of grey rounded shapes, thin wide capitals, "the world's largest software-focused investment firm". Near `law-ganeum` and `crypto-robinchain`. |
| adventinternational.com (Advent) | PE | Royal blue page, a centred serif line and a row of tall portfolio cards with real company marks. Near `interior-robinhome`; the cards are the page. |
| kkr.com (KKR, US) | PE | White page, a yellow brush stroke, a large purple thin headline; a scam-impersonation notice in Korean and English on top. |
| carlyle.com (Carlyle, US) | PE | A full photo of the US Capitol with a centred serif headline and a white rounded header. |
| apollo.com (Apollo, US) | PE · credit | Black page with a light-bulb photo and a green band. |
| tpg.com (TPG, US) | PE | Dark aerial city photo, a very large thin headline, "$346 billion" under it. |
| cvc.com (CVC) | PE | Dark navy page with an olive headline; captured mid-load with a spinner. |
| generalatlantic.com (General Atlantic, US) | PE (growth) | A full photo of the earth, capitals "VISIONARY GROWTH." |
| permira.com (Permira) | PE | A full photo of three named partners walking; orange pill button. |
| warburgpincus.com (Warburg Pincus, US) | PE | Dark teal page, bold sans headline, a video of three men at a table. |
| lcatterton.com (L Catterton, US) | PE | Navy stripes, a white card and "The World's Leading Consumer Growth Investor". |
| ardian.com (Ardian, France) | PE | A city photo with thin wide capitals and a fraud warning bar on top. |
| bridgepoint.eu (Bridgepoint, UK) | PE | An amber blurred photo and a very large "Ideas. Realised." |
| altor.com (Altor, Sweden) | PE | A full bokeh photo with a side list of links at the left edge. |
| insightpartners.com (Insight Partners, US) | PE · VC | Three blue-tinted photos of speakers side by side. |
| evercore.com (Evercore, US) | 부티크 IB | A blue-tinted skyline photo with a thin headline. |
| mbkpartners.com (MBK파트너스, Korea) | PE | Rendered as a white page with one faint line and an impersonation notice. Not judged. |
| immpe.com (IMM, Korea) | PE | A night photo of a palace wall with traffic light trails and a dark text box; an impersonation notice over it. |
| stic.co.kr (스틱인베스트먼트, Korea) | PE | A night skyline carousel under two impersonation notices. |
| vigpartners.com (VIG파트너스, Korea) | PE | Navy page with a gold word in the headline, behind an impersonation notice. |
| affinityequity.com (Affinity, Hong Kong) | PE | A skyline photo with a cyan bar; a notice that it offers nothing to the public. |
| glenwoodpe.com (글렌우드PE, Korea) | PE | A drone photo of a river bridge, "Leading Buyout Firm in Korea" and an AUM line. |
| vipasset.co.kr (VIP자산운용, Korea) | 자산운용 | Near-black page, a bold white Korean headline and a pill "View more". Near `law-ganeum`. |
| timefolio.co.kr (타임폴리오자산운용, Korea) | 자산운용 | Blue page with a wave photo, behind a black-and-red impersonation warning. |
| quarterback.co.kr (쿼터백자산운용, Korea) | 자문 · 자산운용 | A dark city photo, a centred Korean headline, a "문의하기" button and a floating 카카오톡 button. The usual Korean shape; near `beauty-robinhair` in structure. |
| fint.co.kr (핀트, Korea) | 투자일임 (app) | Pale teal page, "1,411,237명이 선택한", app-store buttons, phone screens and a trophy. Near `crypto-robincoin`. |
| fount.co (파운트, Korea) | 투자자문 (app) | One flat green page with two translucent rounded cards. A gateway to two sites, with no content of its own. |
| wealthfront.com (Wealthfront, US) | 자문 (app) | Violet page, "4.45% APY", a card and a phone screen. Near `crypto-robincoin` in structure. |
| iconiqcapital.com (ICONIQ, US) | family office | A cream page that held a letter to one company on the day; a cookie bar. Not a home page layout. |
| pictet.com (Pictet, Switzerland) | 자산관리 | Pale grey page, a serif question as headline, a greyscale photo; a cookie box covered the centre. |
| lombardodier.com (Lombard Odier, Switzerland) | 자산관리 | A full dark photo of riveted metal; a cookie box covered the centre. |
| blackstone.com (Blackstone, US) | PE | Excluded: a residency gate covers the page. |
| bailliegifford.com (Baillie Gifford, UK) | 자산운용 | Excluded: an investor-type gate and a cookie box cover the page. |
| eqtgroup.com (EQT, Sweden) | PE | Excluded: did not finish loading (two tries). |
| hahnandco.com (한앤컴퍼니, Korea) | PE | Excluded: did not load (two tries). |
| lifeasset.co.kr (라이프자산운용, Korea) | 자산운용 | Excluded: did not load (two tries). |

### Candidates for G1 (history)

This block is the comparison the human saw at G1, kept as written. Candidate A is not built, B is built as 로빈패밀리오피스 and not as 로빈투자자문, and the hue moves that B and C list as options are fixed in A5 and A6 (Decisions after G1).

The four differ in base: white with a colour field (A), cream and deep teal (B), blue blocks over a bright photo (C),
violet with pink (D). A and D are PE houses; B and C are proposed as 자문 · 자산관리 samples. A and C have a light first
screen, and B and D a dark one. A reference's own business need not be the sample's 업태: C's reference is an advisory
investment bank, and only its layout is used, as the crypto feature used a foundation's site for a 개발사.

**A. Verdane — https://verdane.com** (Norway). 업태: PE (성장 투자). A white page with a soft field of colour that rises like light from the right, a large two-line sans headline at the left and dark rounded cards below.

```
+------------------------------------------------------------+
| verdane      About Team Portfolio Investors ...  (Investor Portal ->) |
+------------------------------------------------------------+
|                                    . : | || ||| |||| ||||  |
|  Investing in a world            . : || pink / violet ||   |
|  shaped by technology          . : | || orange streaks ||  |
|                              .  : | pale blue haze        |
|  three lines of small text                                  |
|  ___________ (a short dark rule)                            |
+------------------------------------------------------------+
|                         +----------------------------+     |
|  +------------------+   | ## dark rounded card:   ## |     |
|  | ## news card  ## |   |    photo, "Career ->"      |     |
|  +------------------+   +----------------------------+     |
|  cards: [7 offices] [EUR 20M-150M | 200+] [EUR 10Bn | 190+]|
|  two teal tiles: Digitalisation | Decarbonisation          |
+------------------------------------------------------------+
```

- Suits: a PE or growth-equity house that invests in technology companies and wants a light, modern first screen.
- Proposed name: 로빈에쿼티 (`invest-robinequity`). No word of 자본시장법 제38조.
- Picture material: the colour field in CSS gradients; no photo needed. The lower cards can be flat colour tiles.
- Traits to keep: a white page; a plain header with a small wordmark at the left and one filled orange-red pill at the right; a large two-line sans headline at the left; a soft vertical-streak colour field that fills the right half and fades into the page; rounded dark cards and gradient tiles in an uneven grid below; two flat tiles for two themes.
- We would improve: a Korean headline and nav; the sample marker and the non-business sentence on the first screen; a 기업 문의 link in the pill; the colour field kept on the 390 px first screen (the reference shows it only as a thin edge there); 카카오톡 · 전화 · 네이버 예약 · 네이버 지도 in the contact section; the risk sentence.
- Conflicts and substitutes: (1) "Investor Portal" pill (AC55) → a 기업 문의 pill. (2) Figure tiles "EUR 10Bn", "200+", "7 offices" (AC73, AC74) → word tiles that name what the house looks for (for example 소프트웨어, 에너지 전환). (3) News cards with photos of named people and real companies (AC27, AC68, AC80) → cards with flat gradients and a topic line, no person and no company. (4) "Leading European …" (AC61) → a plain description.
- Nearest shipped samples: `crypto-robincoin` and `clinic-neuru` (white page, sans headline at the left, pill button). The distance is the colour field and the absence of a product screen or photo. At 390 px a white page with a Pretendard headline would sit beside `food-saebyeokmil`, `clinic-bonui` and `crypto-robincoin`; the colour field must fill part of that first screen (AC104).

**B. Rockefeller Capital Management — https://www.rockco.com** (US). 업태: 자문 · 자산관리 (가문 자산관리, family office). A cream header with a spaced serif wordmark, then a deep teal panel with a faint map pattern, a thin serif paragraph that ends in two gold script words, and two overlapping black-and-white photos.

```
+------------------------------------------------------------+
| R O C K E F E L L E R              <[ REQUEST AN INTRODUCTION ]> |
|  CAPITAL MANAGEMENT                                         |
| WEALTH MGMT  INVESTMENT MGMT  INV. BANKING ...  [CLIENT LOGIN] (Q) |
+------------------------------------------------------------+
| ## deep teal, faint street-map lines ##                    |
|  * For more than seven           +-----------------+       |
|  | generations, we have     +----|  b/w photo      |       |
|  | grown and evolved ...    | b/w photo  |         |       |
|                             | (man at a  |---------+       |
|   extraordinary             |  desk)     |                 |
|   possibilities.  (gold     +------------+                 |
|                    script)                                  |
+------------------------------------------------------------+
| cream: "Distinct Solutions, Personal Service"              |
| three columns: Wealth Mgmt | Investment Mgmt | Inv. Banking|
| What We Believe In | A Distinct Heritage                   |
+------------------------------------------------------------+
```

- Suits: a 투자자문 · 투자일임 firm or a family office that serves families over a long time and wants a quiet, old-house tone.
- Proposed name: 로빈투자자문 (`invest-robinadvisory`), the human's example. It holds 투자자문, a word of 자본시장법 제38조⑤ (Q2). Substitute name: 로빈패밀리오피스 (`invest-robinfamilyoffice`).
- Picture material: two photos, or none. Direction: black-and-white still lifes with no person (a desk with paper and a pen, a window with a curtain, a stair rail), or line drawings in CSS and SVG in the same two overlapping frames.
- Traits to keep: a two-row cream header with a letter-spaced serif wordmark and a framed outline button; a deep teal panel with a faint line pattern; a thin serif paragraph as the headline, with its last words in a gold script or italic face on their own lines; two overlapping picture frames at the right that break the panel's lower edge; a small ornament at the paragraph's start; a cream section of three service columns below.
- We would improve: a Korean thin serif headline that stays readable (the reference's script words fade at load); the sample marker and the non-business sentence on the first screen; 상담 문의 in the framed button; a 390 px first screen that shows the headline before the photos; the Korean contact links; the risk sentence and the 설명서 sentence (AC81).
- Conflicts and substitutes: (1) Archive photos of real people (AC27, AC91) → still lifes or drawings with no person. (2) "For more than seven generations", "over 140 years" (AC73, AC74: years in business) → a sentence about how the firm works, with no history claim. (3) "CLIENT LOGIN" (AC55) → removed. (4) The name word 투자자문 (Q2). (5) The teal `#002a3a` has the hue (197°) of `law-ganeum`'s accent `#4f93ad`, and a dark panel with a serif headline is the tone of `law-ganeum` and `interior-robinhome` → keep the trait and move the panel's hue to a green-black or a brown-black; or build the reference's second slide, which is the same layout on cream with dark type (`ref-g1-invest-B-slide2.jpg`); or keep teal if the human prefers (Q3).
- Nearest shipped samples: `law-ganeum` (dark panel, serif headline at the left, list at the right), `interior-robinhome` (dark blue page, serif line) and `law-goim` (professional tone). The distance is the cream two-row header, the paragraph-as-headline with script words, and the overlapping frames.

**C. PJT Partners — https://www.pjtpartners.com** (US). 업태 of the sample: 자문 · 자산관리 (the reference is an advisory investment bank). Two blue gradient blocks step down from the top edge: a narrow one behind the mark at the left, and a wide one that holds the nav and a three-line white sans headline. A bright office photo with blurred walking figures fills the screen below them.

```
+------------------------------------------------------------+
| ## blue ## | ## blue gradient block (lighter at left) ##   |
|  PJT       |        About v  Team  Expertise v  Investors  Careers v |
|  (mark)    |                                               |
|            |  PJT is a next-generation global              |
+------------+  investment bank where advice is the          |
| bright     |  main event                                   |
| office     +-----------------------------------------------+
| photo: glass walls, white floor, three blurred figures     |
| walking; the photo runs under both blocks                  |
+------------------------------------------------------------+
| white: "Together, we create differentiated solutions ..."  |
| "One Firm. Many Capabilities." + a list of five services   |
| a rule, contact e-mail at the right, small footer links    |
+------------------------------------------------------------+
```

- Suits: a 투자자문 · 투자일임 firm or an advice boutique that wants a bright, plain-spoken first screen with no stock skyline.
- Proposed name: 로빈자산관리 (`invest-robinwealth`). No word of 자본시장법 제38조 (자산운용 is listed; 자산관리 is not).
- Picture material: one photo. Direction: a bright interior with glass and daylight and no readable sign (a corridor, a meeting room, a stair), with no person or with figures blurred past recognition.
- Traits to keep: no header bar; two colour blocks of different width that step down from the top edge, in one gradient; the mark alone in the narrow block; the nav and a three-line sans headline in white inside the wide block, with no button; a bright photo that runs under both blocks and fills the rest of the first screen; at 390 px the wide block moves to the right and the photo fills the screen under it; below, white sections of large plain text and a list of services.
- We would improve: a Korean headline and nav; the sample marker and the non-business sentence on the first screen (the reference's first screen has no action at all); a 상담 문의 link in the wide block; the Korean contact links; the risk sentence and the 설명서 sentence (AC81); lower sections that show without a scroll effect.
- Conflicts and substitutes: (1) People in the photo, some with faces that can be made out (AC91) → no person, or blurred figures only. (2) "Investors" in the nav and "raise billions of dollars of capital" (AC73, AC74) → removed. (3) "leading advice", "the world's most consequential companies" (AC61, AC65) → a plain description. (4) The reference's content is M&A and restructuring advice (Scope Out) → rewritten as 투자자문 · 투자일임 for individuals and families. (5) The block's blue (`#5fadef` to `#5365b7`, hue 207°–229°) sits by `crypto-robincoin`'s blue panel (210°) and `food-saebyeokmil`'s accent (230°), and `crypto-robincoin` also has a blue gradient panel on a white page → keep the two stepped blocks and move their hue (for example to a green or a warm clay), or keep blue if the human prefers (Q3).
- Nearest shipped samples: `crypto-robincoin` (blue panel on white) and `interior-robininterior` (a wide bright photo with the headline apart from it). The distance is the stepped blocks with the headline inside, the absence of a header bar and of a product screen. At 390 px the first screen is a colour block and a photo, which no shipped sample shows.

**D. Hg — https://hgcapital.com** (UK). 업태: PE (경영권 인수, 소프트웨어 · 서비스). A deep violet page of soft contour lines with a centred light headline, a small outline pill under it, an outlined pill nav at the right with one hot-pink pill, and a white rounded sheet that rises from the lower edge.

```
+------------------------------------------------------------+
| ## deep violet, faint contour lines like a terrain map ##  |
| hg                      ( About Companies Invest People Q ) (Stay informed) |
|                                                            |
|                                                            |
|                  Navigate what's next.                     |
|                      ( About Hg )                          |
|                                                            |
|                                        [small dark panel]  |
| +--------------------------------------------------------+ |
| | white sheet: "Latest from Hg"  (tag)(tag)(tag)  filter | |
| | [line drawing] [gradient picture] [list of news]       | |
| +--------------------------------------------------------+ |
| pale violet closing section with a large link list         |
+------------------------------------------------------------+
```

- Suits: a buyout house that invests in software and services companies and wants a bold, technical first screen.
- Proposed name: 로빈캐피탈 (`invest-robincapital`). No word of 자본시장법 제38조.
- Picture material: CSS and inline SVG; no photo. The contour lines are drawn new.
- Traits to keep: one deep violet page with a faint contour-line pattern; a small wordmark at the top left; an outlined pill that holds the nav, and one hot-pink filled pill beside it; a centred light-weight one-line headline with a small outline pill under it; a white sheet with rounded top corners that enters the first screen from below and holds tag pills and cards; a pale closing section with a large list of links.
- We would improve: a Korean headline; the sample marker and the non-business sentence on the first screen; 기업 문의 in the pink pill; the white sheet holds 투자 분야 word tags and cards in place of news; the Korean contact links; the risk sentence and the PE sentence (AC77).
- Conflicts and substitutes: (1) "Stay informed" opens a newsletter sign-up (AC48) → the pill is the 기업 문의 link. (2) "a portfolio of 60+ companies", "Companies", case studies with real company names (AC73, AC80) → sectors and kinds of deal, no company. (3) "Ways to invest with Hg" with Institutional, Wealth and Listed (AC78: the page does not address the public as investors) → removed. (4) News cards with dates and a named person (AC27, AC73) → topic cards with no date and no person. (5) A dark page with one hot accent and pill-shaped header parts is the make of `crypto-robinchain` (black, lime, glass pill header), and violet 261° sits by `fitness-mideoum`'s accent (266°) → keep the traits; the distance is the violet base, the contour pattern, the centred one-line headline and the white sheet.
- Nearest shipped samples: `crypto-robinchain` (dark, one hot accent, pill header) and `law-ganeum` (dark, no photo).

## Open questions

None. Q1–Q5 of the first draft were answered by the human at G1 on 2026-11-21 (A1–A4 in Decisions after G1).
