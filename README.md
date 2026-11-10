# RobinTech 홈페이지

로빈테크 회사 홈페이지입니다. 빌드 도구 없이 쓰는 정적 사이트이고, GitHub Pages로 호스팅합니다.

## 구조

- `index.html`: 메인 페이지. 서비스(ax, Robin Cloud), 요금, 사례, 회사 소개, 문의 섹션이 있습니다.
- `cases/`: 강의·컨설팅 사례 목록(`cases/index.html`)과 사례별 상세 페이지(`cases/<slug>/index.html`)
- `assets/`: CSS, JS, 로고 이미지
- `scripts/cases.py`: 사례 데이터. 사례를 추가하거나 고칠 때 이 파일을 수정합니다.
- `scripts/build.py`: HTML 생성기. 외부 의존성이 없습니다.

## 수정하는 방법

`*.html` 파일은 생성 결과물이라 직접 고치지 않습니다. 사례는 `scripts/cases.py`에서, 그 밖의 문구·레이아웃·연락처는 `scripts/build.py`에서 고친 뒤 다시 생성합니다.

```bash
python3 scripts/build.py
python3 -m http.server 8000   # http://localhost:8000 에서 확인
```

## 배포 (GitHub Pages)

1. 저장소에서 Settings → Pages → Source를 `Deploy from a branch`, `main` / `(root)`로 설정합니다.
2. Custom domain에 도메인을 입력합니다. 저장소 루트에 `CNAME` 파일이 생깁니다.
3. DNS를 설정합니다.
   - apex 도메인: A 레코드 4개를 둡니다. `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www`: CNAME 레코드를 `<org>.github.io`로 둡니다.
4. 인증서가 발급되면 `Enforce HTTPS`를 켭니다.
