#!/usr/bin/env python3
"""로빈테크 홈페이지 정적 페이지 생성기.

사용법: python3 scripts/build.py
생성물: index.html, cases/index.html, cases/<slug>/index.html, 404.html
외부 의존성 없음 (Python 3.9+).
"""
from html import escape as e
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cases import CASES  # noqa: E402

SITE = {
    "name": "로빈테크",
    "name_en": "RobinTech",
    "email": "contact@robintech.cloud",
    "tel": "070-4685-3042",
    # 전화번호 노출 여부 — 문의 섹션 카드와 하단 사업자 정보 모두에 적용 (False면 숨김, 값은 보존)
    "show_phone_contact": False,
    "address": "서울특별시 강남구 테헤란로79길 6, 제이에스타워 3층 브이423호",
    "ceo": "김석현",
    "biz_no": "572-72-00462",
    "mail_order_no": "제 2026-서울강남-04001 호",
    "consult_url": "https://ax.robin-cloud.com/#contact",
    # Google Analytics 4 측정 ID (공개 값). 비우면 GA 태그를 넣지 않습니다.
    "ga_id": "G-TE7M2NEXWM",
}

STATUS_LABEL = {"done": "완료", "ongoing": "진행 중", "upcoming": "예정"}
CATEGORIES = [("all", "전체"), ("edu", "임직원 · 개발자 교육"), ("talk", "강연 · 세미나"), ("online", "온라인 강의")]

ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'


def ga_snippet():
    """GA4 태그. localhost 에서는 ?ga=1 을 붙였을 때만 로드해 개발 중 방문이 집계되지 않게 합니다."""
    gid = SITE.get("ga_id")
    if not gid:
        return ""
    return f"""<script>
(function () {{
  var id = "{gid}", h = location.hostname;
  var local = /^(localhost|127\\.0\\.0\\.1|\\[::1\\])$/.test(h) || /\\.localhost$/.test(h);
  if (local && !/[?&]ga=1/.test(location.search)) return;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () {{ dataLayer.push(arguments); }};
  gtag("js", new Date());
  gtag("config", id);
  var s = document.createElement("script");
  s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + id;
  document.head.appendChild(s);
}})();
</script>
"""


def head(title, desc, base, canonical_path=""):
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{base}assets/img/logo-full.png">
<meta name="theme-color" content="#fffdf9">
<link rel="icon" type="image/png" href="{base}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="{base}assets/css/style.css">
{ga_snippet()}</head>
<body>
"""


def header(base, current=""):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    home = f"{base}index.html" if base else ""
    brand_href = home or "./"
    return f"""<header class="site-header" id="top">
  <div class="container nav">
    <a class="brand" href="{brand_href}" aria-label="로빈테크 홈">
      <img src="{base}assets/img/logo-mark.png" alt="" width="34" height="36">
      <span>RobinTech</span>
    </a>
    <nav class="nav-links" aria-label="주 메뉴">
      {link(f"{home}#services", "서비스", "services")}
      {link(f"{home}#pricing", "요금", "pricing")}
      {link(f"{base}cases/", "강의 · 컨설팅", "cases")}
      {link(f"{home}#about", "회사 소개", "about")}
      {link(f"{home}#contact", "문의", "contact")}
    </nav>
    <a class="btn btn-primary btn-sm nav-cta" href="{home}#contact">상담 신청</a>
    <button class="nav-toggle" type="button" aria-label="메뉴 열기" aria-expanded="false">{ICON_MENU}</button>
  </div>
</header>
"""


def footer(base):
    home = f"{base}index.html" if base else ""
    s = SITE
    tel_span = f"<span>전화 {s['tel']}</span>" if s["show_phone_contact"] else ""
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div>
        <div class="footer-brand"><img src="{base}assets/img/logo-mark.png" alt="" width="32" height="34"> RobinTech</div>
        <p style="margin-top:12px;max-width:320px">개발부터 운영까지 끝까지 책임지는 클라우드 · AI 소프트웨어 회사</p>
      </div>
      <div class="footer-links">
        <div><b>서비스</b>
          <a href="https://robin-cloud.com" target="_blank" rel="noopener">Robin Cloud</a>
          <a href="https://ax.robin-cloud.com" target="_blank" rel="noopener">ax 맞춤 개발</a>
          <a href="{base}cases/">강의 · 컨설팅</a>
        </div>
        <div><b>회사</b>
          <a href="{home}#about">회사 소개</a>
          <a href="{home}#contact">문의</a>
          <a href="{base}privacy/">개인정보처리방침</a>
          <a href="mailto:{s['email']}">{s['email']}</a>
        </div>
      </div>
    </div>
    <div class="biz">
      <span>상호 로빈테크(RobinTech)</span><span>대표 {s['ceo']}</span><span>사업자등록번호 {s['biz_no']}</span><br>
      <span>통신판매업신고 {s['mail_order_no']}</span><span>주소 {s['address']}</span><br>
      {tel_span}<span>이메일 {s['email']}</span>
    </div>
    <div class="copyright">© 2026 RobinTech. All rights reserved. · <a href="{base}privacy/" style="text-decoration:underline">개인정보처리방침</a></div>
  </div>
</footer>
<script src="{base}assets/js/main.js" defer></script>
</body>
</html>
"""


def case_card(c, base, heading="h3"):
    st = c["status"]
    status = f'<span class="status {st}">{STATUS_LABEL[st]}</span>' if st != "done" else ""
    return f"""<a class="case-card reveal" href="{base}cases/{c['slug']}/" data-cat="{c['category']}">
  <div class="case-thumb t-{c['theme']}">{status}
    <div><span class="client-name">{e(c['client'])}</span><span class="client-sub">{e(c['client_sub'])}</span></div>
  </div>
  <div class="case-meta">{e(c['client'])} · {e(c['industry'])} · {e(c['kind'])}</div>
  <{heading}>{e(c['title'])}</{heading}>
  <p class="summary">{e(c['summary'])}</p>
  <div class="dur">{e(c['duration'])} · {e(c['date'])}</div>
</a>"""


# ---------------------------------------------------------------- index
def build_index():
    base = ""
    featured = [c for c in CASES][:6]
    clients = []
    for c in CASES:
        if c["client"] not in clients and c["client"] != "AI 초격차 프로그램":
            clients.append(c["client"])
    client_row = "".join(f"<span>{e(n)}</span>" for n in clients)
    cards = "\n".join(case_card(c, base) for c in featured)
    phone_card = f"""      <a class="contact-card" href="tel:{SITE['tel'].replace('-', '')}">
        <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/></svg></span>
        <b>전화</b>
        <span class="v">{SITE['tel']}</span>
        <span>평일 10:00 – 18:00</span>
      </a>
""" if SITE["show_phone_contact"] else ""
    contact_cols = "" if SITE["show_phone_contact"] else " cols-2"

    body = f"""
<main>
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="pill"><span class="dot"></span> Robin Cloud · 서울 리전 운영 중</span>
      <h1>기업에 꼭 맞는 소프트웨어와 AI 에이전트,<br>구축부터 <em>클라우드 운영까지</em></h1>
      <p class="lead">로빈테크는 기업 맞춤형 소프트웨어와 AI 에이전트로 업무 시스템을 구축하고, 조직의 AX를 함께 만들어 갑니다. 완성된 서비스는 자체 클라우드 Robin Cloud에서 운영과 유지보수까지 책임집니다. 대기업 개발조직을 위한 AI 코딩 교육과 컨설팅도 함께합니다.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="#services">서비스 살펴보기</a>
        <a class="btn btn-ghost" href="cases/">강의 · 컨설팅 사례</a>
      </div>
      <div class="hero-stats">
        <div><b>1/10</b><span>일반 외주 대비 개발 비용</span></div>
        <div><b>월 10만원</b><span>운영 대행 기본 요금</span></div>
        <div><b>{len(CASES)}건</b><span>2026 기업 강의 · 컨설팅</span></div>
      </div>
    </div>
    <div class="hero-art">
      <img class="mascot" src="assets/img/logo-mark.png" alt="안경을 쓴 로빈 새 — 로빈테크 마스코트" width="431" height="458">
    </div>
  </div>
</section>

<section class="clients" aria-label="함께한 기업">
  <div class="container">
    <p>대기업 · 금융 · 연구 조직과 함께 AI 개발 역량을 만들어 왔습니다</p>
    <div class="client-row">{client_row}</div>
  </div>
</section>

<section class="section" id="services">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Services</span>
      <h2>개발과 운영, 한 팀이 끝까지</h2>
      <p>필요한 소프트웨어를 합리적인 비용으로 만들고, 만든 뒤의 배포 · 도메인 · 데이터베이스 · 모니터링 · 확장까지 로빈테크가 맡습니다. 고객은 비즈니스에만 집중하세요.</p>
    </div>
    <div class="services">
      <article class="service ax reveal">
        <span class="tag">맞춤형 소프트웨어 개발</span>
        <h3>ax</h3>
        <a class="url" href="https://ax.robin-cloud.com" target="_blank" rel="noopener">ax.robin-cloud.com ↗</a>
        <div class="badge-row"><span class="badge indigo">일반 외주 견적의 1/10</span></div>
        <p class="desc">업무에 꼭 맞는 소프트웨어와 AI 에이전트를 만듭니다. 기술 용어를 몰라도 괜찮아요. 필요한 것을 설명해 주시면 스펙과 견적을 제안하고, 승인하면 바로 개발을 시작합니다.</p>
        <div class="steps">
          <div><p style="margin:0"><b>의뢰</b><span>필요한 소프트웨어를 편하게 설명</span></p></div>
          <div><p style="margin:0"><b>스펙 검토 · 승인</b><span>요구사항 확인 후 스펙과 견적 제안</span></p></div>
          <div><p style="margin:0"><b>구현</b><span>AI 에이전트 탑재 · 커스텀, 진행 상황 주기 공유</span></p></div>
          <div><p style="margin:0"><b>딜리버리</b><span>Robin Cloud에 배포된 결과물 확인 · 인수</span></p></div>
          <div><p style="margin:0"><b>추가 요청</b><span>기능 추가 · 수정은 같은 프로젝트에서 언제든</span></p></div>
        </div>
        <ul>
          <li>OpenAI · Anthropic · Gemini · Qwen 등 모든 AI API 기반 워크플로 에이전트 탑재</li>
          <li>성서유니온 회원관리, 아쿠아벨리 스탬프 적립, 유앤아이환경기술 그룹웨어 운영 중</li>
        </ul>
        <div class="actions">
          <a class="btn btn-indigo" href="{SITE['consult_url']}" target="_blank" rel="noopener">개발 상담 신청</a>
          <a class="btn btn-ghost" href="#pricing">비용 보기</a>
        </div>
      </article>

      <article class="service reveal">
        <span class="tag">관리형 클라우드 · 운영 대행</span>
        <h3>Robin Cloud</h3>
        <a class="url" href="https://robin-cloud.com" target="_blank" rel="noopener">robin-cloud.com ↗</a>
        <div class="badge-row"><span class="badge orange">기본 월 10만원 · 운영 전부 대행</span><span class="badge">서울 리전 · 원화 결제</span></div>
        <p class="desc">GitHub에 푸시하면 서비스가 됩니다. 저장소를 연결하면 배포, 도메인과 인증서, 데이터베이스, 모니터링까지 Robin Cloud가 맡습니다. 서버를 몰라도 내 앱을 운영할 수 있습니다.</p>
        <div class="terminal" aria-hidden="true">
          <div>$ git push origin main</div>
          <div class="dim">→ GitHub Actions 빌드 · 장바구니 쿠폰 적용</div>
          <div class="ok">✓ 이미지 빌드 42초</div>
          <div class="ok">✓ 새 버전으로 교체 · 오토스케일링 활성</div>
          <div class="ok">✓ https://shop.example.co.kr</div>
        </div>
        <ul>
          <li>시크릿 없는 GitHub 배포 — 기본 브랜치에 푸시하면 자동으로 새 버전 교체</li>
          <li>프로젝트 전용 관리형 PostgreSQL, 파일 저장소</li>
          <li>내 도메인 연결과 HTTPS 인증서 자동 발급 · 갱신</li>
          <li>CPU · 메모리 지표, 로그 검색, 인시던트 모니터링</li>
          <li>운영 전부 대행 — 장애 대응과 확장까지 로빈테크가 책임</li>
        </ul>
        <div class="actions">
          <a class="btn btn-accent" href="https://robin-cloud.com" target="_blank" rel="noopener">Robin Cloud 시작하기</a>
          <a class="btn btn-ghost" href="#pricing">요금 보기</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section alt" id="pricing">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Pricing</span>
      <h2>개발은 1/10, 운영은 쓴 만큼</h2>
      <p>AI 에이전트 기반 개발 체계와 자체 클라우드로 비용 구조를 바꿨습니다. 개발비는 낮추고, 운영비는 서비스 규모에 맞춰 정직하게 받습니다.</p>
    </div>
    <div class="pricing">
      <article class="price-card featured reveal">
        <span class="ribbon">Robin Cloud 이용 시</span>
        <span class="kicker">ax · 맞춤형 소프트웨어 개발</span>
        <h3>일반 외주 견적의 1/10</h3>
        <div class="price-big"><b>1/10</b><span>개발 비용</span></div>
        <p class="price-note">일반적인 외주 개발 견적 기준으로, Robin Cloud에서 호스팅하는 조건으로 진행합니다.</p>
        <table class="compare">
          <thead><tr><th>일반 외주 견적</th><th>ax 진행 비용</th></tr></thead>
          <tbody>
            <tr><td><span class="strike">약 1,000만원</span></td><td class="now">약 100만원</td></tr>
            <tr><td><span class="strike">약 3,000만원</span></td><td class="now">약 300만원</td></tr>
          </tbody>
        </table>
        <ul class="fineprint" style="padding-left:18px;margin:0 0 24px">
          <li>요구사항 확인 후 스펙 문서와 견적을 먼저 제안합니다.</li>
          <li>Robin Cloud 이용이 조건입니다. 운영 비용은 오른쪽 요금이 적용됩니다.</li>
        </ul>
        <a class="btn btn-indigo" href="{SITE['consult_url']}" target="_blank" rel="noopener">내 프로젝트 견적 받기</a>
      </article>

      <article class="price-card reveal">
        <span class="kicker">Robin Cloud · 운영 전부 대행</span>
        <h3>기본 월 10만원</h3>
        <div class="price-big"><b>₩100,000</b><span>/ 월</span></div>
        <p class="price-note">배포 · 도메인 · 인증서 · 데이터베이스 · 모니터링 · 장애 대응까지 서비스 운영을 전부 대행합니다.</p>
        <dl class="tier">
          <dt>기본 요금</dt><dd>월 10만원 — 서비스 운영 전부 대행</dd>
          <dt>추가 사용</dt><dd>트래픽이 늘면 오토스케일링이 적용되고, 늘어난 서버는 실제 사용한 대수에 비례해 일할 과금</dd>
        </dl>
        <ul class="fineprint" style="padding-left:18px;margin:0 0 24px">
          <li>트래픽이 늘면 서버가 자동으로 늘고, 줄면 다시 줄어듭니다.</li>
          <li>추가 서버는 사용한 날만큼만 계산하므로 일시적인 트래픽 증가에도 부담이 적습니다.</li>
        </ul>
        <p class="fineprint" style="margin:-12px 0 24px">자세한 요금은 <a href="https://robin-cloud.com" target="_blank" rel="noopener" style="text-decoration:underline">robin-cloud.com 요금제</a>에서 확인하세요.</p>
        <a class="btn btn-accent" href="https://robin-cloud.com" target="_blank" rel="noopener">Robin Cloud 시작하기</a>
      </article>
    </div>
    <div class="combo reveal">
      <div>
        <b>예: 3,000만원 규모 시스템이라면</b>
        <p>개발 약 300만원 + 운영 기본 월 10만원으로 시작할 수 있습니다. 사용량이 늘어난 만큼만 일할로 추가됩니다.</p>
      </div>
      <a class="btn btn-accent" href="#contact">문의하기</a>
    </div>
  </div>
</section>

<section class="section" id="cases">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Lectures &amp; Consulting</span>
      <h2>기업 AI 개발 교육 · 컨설팅</h2>
      <p>삼성종합기술원, 코스콤, 현대자동차 ICT본부 등 연구 · 금융 · 제조 조직의 개발자와 임직원을 대상으로 Claude Code 기반 AI 코딩, 멀티 에이전트, RAG 실무 교육과 컨설팅을 진행합니다.</p>
    </div>
    <div class="case-grid">
{cards}
    </div>
    <div style="margin-top:40px"><a class="btn btn-ghost" href="cases/">전체 사례 보기 →</a></div>
  </div>
</section>

<section class="section alt" id="about">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">About</span>
      <h2>개발부터 운영까지 끝까지 책임지는 회사</h2>
    </div>
    <div class="about-grid">
      <div>
        <p>로빈테크는 2025년 서울 삼성동에서 시작한 클라우드 · AI 소프트웨어 회사입니다. 중소기업과 비영리 단체가 개발팀이나 운영 인력 없이도 자기 업무에 꼭 맞는 소프트웨어를 가질 수 있도록, 개발 · 호스팅 · 유지보수를 하나로 묶었습니다.</p>
        <p>AI 에이전트 기반 개발 체계로 개발 비용을 크게 낮추고, 쿠버네티스 기반 자체 클라우드 Robin Cloud로 운영을 자동화했습니다. 같은 경험을 바탕으로 대기업 개발조직의 AI 전환을 돕는 교육과 컨설팅도 진행합니다.</p>
        <div class="values">
          <div class="value"><i>🛠</i><p style="margin:0"><b>구축부터 운영까지 한 팀</b><span>납품 후에도 같은 팀이 운영하고 키웁니다.</span></p></div>
          <div class="value"><i>🤖</i><p style="margin:0"><b>AI 에이전트 네이티브</b><span>스펙부터 PR까지 에이전트와 함께 일하는 개발 체계.</span></p></div>
          <div class="value"><i>☁️</i><p style="margin:0"><b>자체 클라우드</b><span>배포 · DB · 도메인 · 모니터링을 한 콘솔에서.</span></p></div>
        </div>
      </div>
      <div class="ceo reveal">
        <div class="name">김석현</div>
        <div class="role">대표 · 서울대학교 전기컴퓨터공학 박사</div>
        <p style="font-size:15px;color:var(--ink-2)">아마존과 쿠팡에서 대규모 분산 시스템을 만들고, 여러 스타트업의 CTO와 엔지니어링 리더를 거쳤습니다. 2023년부터 AI 코딩 에이전트를 실무에 적용해 왔고, 그 경험을 로빈테크의 개발 체계와 기업 교육으로 이어가고 있습니다.</p>
        <ul class="timeline">
          <li><span>2025 –</span><p style="margin:0"><b>로빈테크 대표</b><small>Robin Cloud · AI 에이전트 서비스 개발 · 운영</small></p></li>
          <li><span>2026 –</span><p style="margin:0"><b>AX LABS AI · Cloud 컨설턴트</b><small>기업 AI 전환 교육 · 컨설팅</small></p></li>
          <li><span>2022 – 23</span><p style="margin:0"><b>CLASS101 Head of Foundation Engineering</b><small>커머스 · 코어 조직 15~20명 리드</small></p></li>
          <li><span>2021 – 22</span><p style="margin:0"><b>funNC CTO</b><small>22명 팀 구성, 커머스 시스템 리뉴얼</small></p></li>
          <li><span>2017 – 21</span><p style="margin:0"><b>쿠팡 Staff Software Engineer</b><small>프로모션 시스템 재구축 · 피크 동시 접속 약 2,000만</small></p></li>
          <li><span>2015 – 17</span><p style="margin:0"><b>Amazon SDE II (Seattle)</b><small>A/B 테스트 플랫폼 Weblab</small></p></li>
          <li><span>2013 – 15</span><p style="margin:0"><b>삼성전자 SW센터</b><small>모바일 딥러닝 · 빅데이터 플랫폼</small></p></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section" id="contact">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Contact</span>
      <h2>어떤 소프트웨어가 필요하신가요?</h2>
      <p>개발 의뢰, Robin Cloud 도입, 기업 강의 · 컨설팅 모두 편하게 문의하세요. 업무와 요구사항을 듣고 만들 수 있는 범위와 비용을 정리해 드립니다.</p>
    </div>
    <div class="contact-grid{contact_cols}">
      <a class="contact-card" href="{SITE['consult_url']}" target="_blank" rel="noopener">
        <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H8l-4 4z"/></svg></span>
        <b>온라인 상담 신청</b>
        <span class="v">상담 신청서 작성 →</span>
        <span>개발 의뢰는 신청서로 남겨 주시면 가장 빠르게 회신드립니다.</span>
      </a>
      <a class="contact-card" href="mailto:{SITE['email']}">
        <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></span>
        <b>이메일</b>
        <span class="v">{SITE['email']}</span>
        <span>강의 · 컨설팅 문의, 제안서 요청</span>
      </a>
{phone_card}    </div>
    <div class="contact-guide">
      <h3>문의하면 이렇게 진행돼요</h3>
      <ol>
        <li>상담 신청서나 이메일로 필요한 내용을 알려 주세요. 기술 용어는 몰라도 괜찮습니다.</li>
        <li>요구사항을 확인하고 만들 수 있는 범위, 스펙, 견적을 제안합니다.</li>
        <li>승인하면 개발을 시작하고, 진행 상황을 주기적으로 공유합니다.</li>
        <li>Robin Cloud에 배포된 결과물을 확인 · 인수하고, 이후 운영과 유지보수를 이어갑니다.</li>
      </ol>
      <p class="fineprint" style="margin:14px 0 0">방문 주소: {SITE['address']}</p>
    </div>
  </div>
</section>
</main>
"""
    html = head("로빈테크 RobinTech — 맞춤형 소프트웨어 개발과 운영, AI 교육",
                "로빈테크는 맞춤형 소프트웨어와 AI 에이전트를 일반 외주의 1/10 비용으로 만들고, 자체 클라우드 Robin Cloud에서 운영까지 책임집니다. 기업 AI 코딩 교육 · 컨설팅.",
                base) + header(base) + body + footer(base)
    (ROOT / "index.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- cases list
def build_case_list():
    base = "../"
    filters = "".join(
        f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>'
        for k, v in CATEGORIES)
    cards = "\n".join(case_card(c, base, "h2") for c in CASES)
    body = f"""
<main>
<section class="section" style="padding-top:72px">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">Lectures &amp; Consulting</span>
      <h1 style="font-size:clamp(32px,4.4vw,48px);font-weight:850">강의 · 컨설팅 사례</h1>
      <p>연구 · 금융 · 제조 · 교육 기업과 함께한 AI 코딩, 멀티 에이전트, RAG 교육과 컨설팅을 소개합니다. 카드를 누르면 커리큘럼과 실습 내용을 볼 수 있습니다.</p>
    </div>
    <div class="filters" role="group" aria-label="사례 분류">{filters}</div>
    <div class="case-grid" id="case-grid">
{cards}
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container" style="text-align:center">
    <h2 style="font-size:28px;font-weight:800">우리 조직에 맞는 AI 교육이 필요하신가요?</h2>
    <p style="color:var(--muted);margin:12px auto 24px;max-width:560px">조직의 개발 환경과 수준에 맞춰 강연, 1~3일 실습 과정, 팀 하네스 구축 컨설팅을 설계해 드립니다.</p>
    <a class="btn btn-primary" href="mailto:{SITE['email']}?subject={e('[강의 문의] ')}">강의 · 컨설팅 문의</a>
  </div>
</section>
</main>
"""
    html = head("강의 · 컨설팅 사례 — 로빈테크",
                "삼성종합기술원, 코스콤, 현대자동차 ICT본부, 멀티캠퍼스, 패스트캠퍼스 등 로빈테크의 기업 AI 개발 교육 · 컨설팅 사례.",
                base) + header(base, "cases") + body + footer(base)
    out = ROOT / "cases"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------- case detail
def build_case_detail(c, others):
    base = "../../"
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in c["facts"])
    overview = "".join(f"<p>{e(p)}</p>" for p in c["overview"])
    modules = "".join(
        f'<div class="module"><div class="m-head">{e(t)}</div><p>{e(d)}</p></div>' for t, d in c["modules"])
    labs = "".join(f"<li>{e(x)}</li>" for x in c["labs"])
    tech = "".join(f"<span>{e(x)}</span>" for x in c["tech"])
    outcomes = "".join(f"<li>{e(x)}</li>" for x in c["outcomes"])
    st = c["status"]
    status_line = f'<span class="status-line">{STATUS_LABEL[st]}</span>' if st != "done" else ""
    more = "\n".join(case_card(o, base) for o in others)

    body = f"""
<main>
<section class="case-hero">
  <div class="container">
    <div class="crumbs"><a href="{base}index.html">홈</a> / <a href="{base}cases/">강의 · 컨설팅</a></div>
    {status_line}
    <div class="client-big">{e(c['client'])}</div>
    <div style="font-size:14px;color:#c9bbca;margin-top:6px">{e(c['industry'])} · {e(c['kind'])} · {e(c['date'])}</div>
    <h1>{e(c['title'])}</h1>
    <p class="lead">{e(c['summary'])}</p>
  </div>
</section>
<div class="container case-body">
  <div>
    <dl class="facts">{facts}</dl>
    <article class="prose">
      <h2 id="overview">개요</h2>
      {overview}
      <h2 id="curriculum">커리큘럼</h2>
      <div class="modules">{modules}</div>
      <h2 id="labs">실습 · 사례</h2>
      <ul>{labs}</ul>
      <h2 id="tech">다룬 기술</h2>
      <div class="chips">{tech}</div>
      <h2 id="outcomes">결과물</h2>
      <ul>{outcomes}</ul>
    </article>
  </div>
  <aside class="aside">
    <nav class="toc" aria-label="목차"><b>목차</b>
      <a href="#overview">개요</a><a href="#curriculum">커리큘럼</a><a href="#labs">실습 · 사례</a><a href="#tech">다룬 기술</a><a href="#outcomes">결과물</a>
    </nav>
    <div class="cta-box">
      <b>비슷한 교육을 검토 중이신가요?</b>
      <p>조직의 개발 환경에 맞춰 과정을 설계해 드립니다.</p>
      <a class="btn btn-primary btn-sm" href="mailto:{SITE['email']}?subject={e('[강의 문의] ' + c['title'])}">문의하기</a>
    </div>
  </aside>
</div>
<section class="more-cases">
  <div class="container">
    <h2 style="font-size:24px;font-weight:800;margin-bottom:28px">다른 사례</h2>
    <div class="case-grid">
{more}
    </div>
  </div>
</section>
</main>
"""
    html = head(f"{c['title']} — {c['client']} | 로빈테크", c["summary"], base) + header(base, "cases") + body + footer(base)
    out = ROOT / "cases" / c["slug"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")


def build_privacy():
    base = "../"
    s = SITE
    body = f"""
<main>
<section class="section" style="padding-top:72px">
  <div class="container" style="max-width:820px">
    <span class="eyebrow">Privacy</span>
    <h1 style="font-size:clamp(30px,4vw,40px);font-weight:850;margin-bottom:12px">개인정보처리방침</h1>
    <p style="color:var(--muted)">시행일 2026년 11월 10일</p>
    <article class="prose" style="margin-top:40px">
      <p>로빈테크(이하 ‘회사’)는 이 홈페이지를 운영하면서 이용자의 개인정보를 「개인정보 보호법」 등 관련 법령에 따라 처리합니다. 이 방침은 회사 홈페이지에 적용됩니다. 상담 신청서(ax.robin-cloud.com)와 Robin Cloud 서비스(robin-cloud.com)에는 각 서비스의 개인정보처리방침이 적용됩니다.</p>

      <h2>1. 처리하는 개인정보 항목과 목적</h2>
      <ul>
        <li><b>이메일 문의</b> — 이메일 주소, 이름 · 회사명 등 문의자가 직접 적은 내용. 문의 확인과 회신에 이용합니다.</li>
        <li><b>방문 기록(자동 수집)</b> — 쿠키, 접속 일시, 방문한 페이지, 유입 경로, 브라우저 · 기기 · OS 정보, 대략적인 지역(국가 · 도시 단위). 방문 통계 분석과 홈페이지 개선에 이용합니다. 이 정보로 개인을 식별하지 않습니다.</li>
      </ul>

      <h2>2. 보유 및 이용 기간</h2>
      <ul>
        <li>이메일 문의: 문의 처리가 끝난 날부터 1년 동안 보관한 뒤 파기합니다.</li>
        <li>방문 기록: Google Analytics의 데이터 보존 설정에 따라 수집일로부터 최대 14개월 동안 보관된 뒤 자동 삭제됩니다.</li>
        <li>법령에서 보존 기간을 따로 정한 경우에는 그 기간 동안 보관합니다.</li>
      </ul>

      <h2>3. 웹 분석 도구(Google Analytics) 사용</h2>
      <p>회사는 방문 통계를 위해 Google LLC가 제공하는 Google Analytics 4를 사용합니다. Google Analytics는 쿠키를 이용해 위 1항의 방문 기록을 수집하며, 수집된 정보는 Google의 서버(미국 등 국외)에 저장 · 처리될 수 있습니다.</p>
      <ul>
        <li>수탁자 · 이전받는 자: Google LLC (문의: https://support.google.com/analytics)</li>
        <li>이전 항목: 1항의 방문 기록</li>
        <li>이전 시기 · 방법: 홈페이지 방문 시 네트워크를 통해 전송</li>
        <li>보유 기간: 2항의 방문 기록 보유 기간과 같음</li>
      </ul>
      <p>방문 기록 수집을 원하지 않으면 브라우저 설정에서 쿠키를 차단하거나, Google이 제공하는 <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener" style="text-decoration:underline">Google Analytics 차단 브라우저 부가기능</a>을 설치할 수 있습니다. 쿠키를 차단해도 홈페이지 이용에는 제한이 없습니다.</p>

      <h2>4. 제3자 제공</h2>
      <p>회사는 이용자의 개인정보를 제3자에게 제공하지 않습니다. 다만 법령에 근거가 있거나 수사기관이 법령에 정한 절차에 따라 요청하는 경우는 예외로 합니다.</p>

      <h2>5. 파기 절차와 방법</h2>
      <p>보유 기간이 끝나거나 처리 목적을 달성한 개인정보는 지체 없이 파기합니다. 전자 파일은 복구할 수 없는 방법으로 삭제하고, 종이 문서는 분쇄하거나 소각합니다.</p>

      <h2>6. 이용자의 권리</h2>
      <p>이용자는 언제든지 자신의 개인정보에 대한 열람, 정정, 삭제, 처리 정지를 요청할 수 있습니다. 아래 개인정보 보호책임자에게 이메일로 요청하면 지체 없이 조치하겠습니다.</p>

      <h2>7. 개인정보 보호책임자</h2>
      <ul>
        <li>성명: {s['ceo']} (대표)</li>
        <li>이메일: <a href="mailto:{s['email']}" style="text-decoration:underline">{s['email']}</a></li>
      </ul>
      <p>개인정보 침해에 관한 신고나 상담은 개인정보침해신고센터(국번 없이 118, privacy.kisa.or.kr), 개인정보분쟁조정위원회(1833-6972, www.kopico.go.kr)에도 할 수 있습니다.</p>

      <h2>8. 방침의 변경</h2>
      <p>이 방침의 내용이 바뀌면 시행 7일 전부터 홈페이지를 통해 알립니다.</p>
    </article>
  </div>
</section>
</main>
"""
    html = head("개인정보처리방침 — 로빈테크", "로빈테크 홈페이지 개인정보처리방침", base) + header(base) + body + footer(base)
    out = ROOT / "privacy"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")


def build_404():
    # GitHub Pages 404는 어떤 경로에서든 열리므로 절대 경로 사용
    base = "/"
    body = """
<main><section class="section" style="text-align:center">
  <div class="container">
    <h1 style="font-size:48px;font-weight:850">404</h1>
    <p style="color:var(--muted);margin:12px 0 28px">찾으시는 페이지가 없습니다.</p>
    <a class="btn btn-primary" href="/">홈으로</a>
  </div>
</section></main>
"""
    html = head("페이지를 찾을 수 없습니다 — 로빈테크", "로빈테크", base) + header(base) + body + footer(base)
    (ROOT / "404.html").write_text(html, encoding="utf-8")


def main():
    build_index()
    build_case_list()
    for i, c in enumerate(CASES):
        others = [CASES[(i + k) % len(CASES)] for k in (1, 2, 3)]
        build_case_detail(c, others)
    build_404()
    build_privacy()
    print(f"built index, cases list, {len(CASES)} case pages, privacy, 404")


if __name__ == "__main__":
    main()
