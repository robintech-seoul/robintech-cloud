"""홈페이지 제작 프로파일(업종별 디자인 샘플) 데이터.

수정 후 `python3 scripts/build.py` 로 profile/index.html 을 다시 생성합니다.

프로파일 하나를 올리는 방법
1. `profile/<slug>/` 폴더에 샘플 사이트를 만듭니다. 이 폴더는 build.py 가 건드리지 않습니다.
   다른 사이트로 옮겨도 동작하도록 CSS·이미지·폰트를 폴더 안에서 상대 경로로 씁니다
   (사이트 공용 style.css, 헤더, 푸터를 쓰지 않습니다).
2. 갤러리 카드용 썸네일 `profile/<slug>/thumb.jpg` (16:10, 가로 1200px 권장)를 둡니다.
   `python3 scripts/profile_thumb.py <slug>` 로 데스크톱 화면을 찍어 만들 수 있습니다.
3. 아래 PROFILES 에 dict 하나를 추가합니다.

필드
- slug: 폴더 이름. URL 은 /profile/<slug>/
- industry: INDUSTRIES 의 key (갤러리 필터)
- name: 샘플 속 상호 (가상 상호)
- title: 카드 제목 — 디자인 콘셉트를 한 줄로
- summary: 미리보기 패널 설명
- features: 포함 기능 (예약, 지도, 메뉴판 등)
- palette: 카드 아래 색상 칩 (hex 3~4개)
- status: live(공개) | draft(준비 중: 카드만 보이고 열리지 않음)
- demo: True 면 '가상 상호 샘플' 표시
"""

# (key, 라벨) — 필터 칩 순서. 프로파일이 없는 업종도 '준비 중' 타일로 보여 줍니다.
INDUSTRIES = [
    ("food", "식당 · 카페"),
    ("flower", "꽃집 · 공방"),
    ("clinic", "병원 · 의원"),
    ("beauty", "뷰티 · 미용"),
    ("kids", "키즈 · 교육"),
    ("fitness", "운동 · 피트니스"),
    ("stay", "숙박 · 공간대여"),
    ("pro", "전문 서비스"),
]

PROFILES = [
    {
        "slug": "flower-bomgyeol",
        "industry": "flower",
        "name": "봄결 플라워",
        "title": "계절을 담는 동네 꽃집",
        "summary": "따뜻한 크림 톤과 세리프 서체로 꽃집의 감성을 살린 한 페이지 홈페이지. 시그니처 꽃다발, 정기구독, 카카오톡 주문과 오시는 길까지 손님이 찾는 정보를 한 화면 흐름에 담았습니다.",
        "features": ["상품 소개", "정기구독 안내", "카카오톡 주문", "네이버 지도", "모바일 최적화"],
        "palette": ["#f7f1e8", "#5d6b4f", "#d98c7a", "#2f2a24"],
        "status": "live",
        "demo": True,
    },
]
