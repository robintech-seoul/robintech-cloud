#!/usr/bin/env python3
"""Static checks for the three clinic profile samples (no browser, no network). Run from the repository root.

usage: python3 docs/features/2026-11-18-profile-clinic/check_static.py <check> [<slug>]
  per sample (all three when <slug> is left out): photos markers flow law assets sample register
  shared: name gallery current
  all: every check above, for every sample
slugs: clinic-neuru clinic-byeotteul clinic-bonui
Exit 0 when every named check passes; otherwise prints each failure and exits 1.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[3]
FEATURE = Path(__file__).resolve().parent
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
SAMPLES = {  # slug: clinic name, name stem, words naming its reference site (AC50)
    "clinic-neuru": {"name": "느루치과", "stem": "느루", "ref": [r"studio\s*dental", r"studiodental"]},
    "clinic-byeotteul": {"name": "볕뜰가정의학과의원", "stem": "볕뜰", "ref": [r"\bTia\b", r"asktia"]},
    "clinic-bonui": {"name": "보늬피부과", "stem": "보늬", "ref": [r"ever\s*/?\s*body", r"everbody"]},
}
OTHER_SOURCES = ("profile/flower-bomgyeol/img/sources.txt", "profile/food-saebyeokmil/img/sources.txt")
NAME_SUFFIXES = ("의원", "치과", "내과", "가정의학과", "피부과", "클리닉")
BANNED = ("최고", "최초", "최상", "유일", "1위", "1등", "No.1", "최첨단", "독보적", "완벽", "영구적", "완치", "100%",
          "100 %", "100％", "보장", "보증", "부작용 없", "부작용이 없", "부작용 걱정", "무통", "통증 없", "아프지 않", "안 아픈",
          "전문병원", "할인", "특가", "반값", "이벤트", "후기", "리뷰", "체험담", "평점", "별점", "만족도", "★", "전후 사진",
          "비포", "애프터")
BANNED_BONUI = ("동안 피부", "동안 시술", "젊어지", "효과 보장", "확실한 효과", "즉각적", "드라마틱", "극적인")
BONUI_SENTENCE = "시술 결과와 부작용은 개인에 따라 다를 수 있으며, 진료 상담 후 결정합니다."
DENTAL = ("일반진료", "스케일링", "신경치료", "보존치료", "잇몸치료", "충치치료", "발치", "임플란트", "교정", "미백",
          "레진", "크라운", "보철", "구강검진", "틀니", "불소", "실란트", "소아진료", "치주")
EVERYDAY = ("감기", "독감", "만성질환", "고혈압", "당뇨", "고지혈증", "예방접종", "건강검진", "소화기", "장염", "알레르기",
            "비염", "천식", "갑상선", "골다공증", "금연", "비만", "상처", "두통", "수면", "피로")
PRACTITIONER = re.compile(r"(?<![가-힣])([가-힣]{2,4}) (대표 ?원장|부원장|원장)(?:님)?(?![가-힣])")
NOT_A_NAME = ("의료진", "진료진", "담당", "소개", "대표", "공동", "우리", "병원", "의원", "치과", "피부과", "여성", "남성",
              "전문의", "진료", "모든")
HOURS = r"\d{1,2}:\d{2}\s*[-–—~～〜]\s*\d{1,2}:\d{2}"
BLOCK = {"p", "li", "dd", "dt", "td", "th", "address", "div", "section", "article", "header", "footer",
         "h1", "h2", "h3", "h4", "h5", "h6", "button", "nav", "main", "aside", "figure", "figcaption", "tr", "table"}
fails = []


def fail(msg):
    fails.append(msg)


def read(path):
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


class Page(HTMLParser):
    """Collects headings, links/buttons with accessible names, images, refs, block text lines."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []            # visible text chunks; "\n" at block boundaries
        self.headings = []        # (level, text, text_offset), document order
        self.controls = []        # dict(tag, href, name)
        self.imgs, self.refs, self.links, self.scripts, self.metas, self.footer = [], [], [], [], [], []
        self.title, self.attr_text = [], []  # <title> text; aria-label, title and meta description/og: content
        self.body_at = None       # text offset at <body>
        self.header_at = None     # text offset at the first <header>
        self._stack = []
        self._skip = 0

    def _offset(self):
        return sum(len(t) for t in self.text)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        self.attr_text += [a[k] for k in ("aria-label", "title") if a.get(k)]
        if tag == "meta" and (a.get("name") == "description" or a.get("property", "").startswith("og:")):
            self.attr_text.append(a.get("content", ""))
        if tag in ("script", "style", "template", "title"):
            self._skip += 1
            if tag == "script" and a.get("src"):
                self.scripts.append(a["src"])
        if tag == "body" and self.body_at is None:
            self.body_at = self._offset()
        if tag == "header" and self.header_at is None:
            self.header_at = self._offset()
        if tag in BLOCK:
            self.text.append("\n")
        elif tag in ("br", "a"):
            self.text.append(" ")
        for k in ("src", "srcset", "href", "poster"):
            if k in a:
                self.refs.append((k, a[k]))
        if tag == "img":
            self.imgs.append(a)
            self._add(a.get("alt", ""))
        elif tag == "link":
            self.links.append(a)
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "input" and a.get("type") in ("submit", "button"):
            self.controls.append({"tag": tag, "href": None, "name": a.get("aria-label") or a.get("value", "")})
        if tag in ("a", "button"):
            self._stack.append({"kind": "control", "tag": tag, "href": a.get("href"),
                                "label": a.get("aria-label"), "buf": []})
        elif re.fullmatch(r"h[1-6]", tag):
            self._stack.append({"kind": "heading", "level": int(tag[1]), "buf": [], "offset": self._offset()})
        elif tag == "footer":
            self._stack.append({"kind": "footer", "buf": []})

    def handle_endtag(self, tag):
        if tag in ("script", "style", "template", "title"):
            self._skip = max(0, self._skip - 1)
        if tag in BLOCK:
            self.text.append("\n")
        elif tag in ("br", "a"):
            self.text.append(" ")
        kind = {"a": "control", "button": "control", "footer": "footer"}.get(tag)
        if re.fullmatch(r"h[1-6]", tag):
            kind = "heading"
        if not kind:
            return
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i]["kind"] == kind:
                item = self._stack.pop(i)
                txt = re.sub(r"\s+", " ", "".join(item["buf"])).strip()
                if kind == "control":
                    self.controls.append({"tag": item["tag"], "href": item["href"],
                                          "name": item["label"] if item["label"] else txt})
                elif kind == "heading":
                    self.headings.append((item["level"], txt, item["offset"]))
                else:
                    self.footer.append(txt)
                break

    def _add(self, data):
        self.text.append(data)
        for item in self._stack:
            item["buf"].append(data)

    def handle_data(self, data):
        if self.lasttag == "title" and self._skip:
            self.title.append(data)
        if not self._skip:
            self._add(data)

    def full(self):
        return "".join(self.text)

    def lines(self):
        return [re.sub(r"\s+", " ", ln).strip() for ln in self.full().split("\n") if ln.strip()]

    def section(self, pattern):
        """Text of the first h2-h6 heading matching pattern up to the next heading of the same or a higher level."""
        hs = sorted(self.headings, key=lambda h: h[2])
        for i, (lvl, txt, off) in enumerate(hs):
            if lvl >= 2 and re.search(pattern, txt):
                end = next((o for l, _, o in hs[i + 1:] if l <= lvl), len(self.full()))
                return self.full()[off:end]
        return None


class Sample:
    def __init__(self, slug):
        self.slug = slug
        self.info = SAMPLES[slug]
        self.site = ROOT / "profile" / slug
        self.img = self.site / "img"
        self.sources = self.img / "sources.txt"
        self._page = None

    def page(self):
        if self._page is None:
            html = read(self.site / "index.html")
            p = Page()
            p.feed(html)
            self._page = (html, read(self.site / "style.css"), p)
        return self._page

    def image_files(self):
        return sorted(f for f in self.img.iterdir() if f.is_file() and f.name != "sources.txt"
                      and not f.name.startswith(".")) if self.img.is_dir() else []

    def source_lines(self):
        return [ln.split() for ln in read(self.sources).splitlines() if ln.strip()]


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def nospace(s):
    return re.sub(r"\s+", "", s or "")


def css_urls(css):
    out = [u.strip("'\" ") for u in re.findall(r"url\(([^)]*)\)", css)]
    out += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", css)
    return out


def srcset_urls(v):
    return [part.strip().split()[0] for part in v.split(",") if part.strip()]


def image_refs(p, css):
    refs = []
    for k, v in p.refs:
        if k in ("src", "poster"):
            refs.append(v)
        elif k == "srcset":
            refs += srcset_urls(v)
    refs += css_urls(css)
    return [r for r in refs if r and not r.startswith(("data:", "#", "http://", "https://", "//"))]


def photo_id(url):
    m = re.search(r"images\.unsplash\.com/(photo-[0-9]+-[0-9a-f]+)", url) or \
        re.search(r"images\.pexels\.com/photos/([0-9]+)/", url)
    return m.group(1) if m else None


def sips_size(path):
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True)
    w = re.search(r"pixelWidth:\s*(\d+)", r.stdout)
    h = re.search(r"pixelHeight:\s*(\d+)", r.stdout)
    return (int(w.group(1)), int(h.group(1))) if w and h else (None, None)


def load_profiles():
    sys.path.insert(0, str(ROOT / "scripts"))
    from profiles import PROFILES  # noqa: E402
    return PROFILES


def entry(slug):
    hits = [p for p in load_profiles() if p.get("slug") == slug]
    return hits[0] if len(hits) == 1 else None


def accent(slug):
    e = entry(slug)
    return (e.get("palette") or [""])[-1].lower() if e else None


def fonts_loaded(s, family):
    html, css, _ = s.page()
    pat = re.escape(family).replace(r"\ ", r"[ +]")
    return bool(re.search(pat, html + css, re.I))


# --- CSS: top-level rules, custom properties, body background (AC70 AC71) -----------------------

def top_rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    rules, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            break
        sel = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        if not sel.split(";")[-1].strip().startswith("@"):
            rules.append((sel.split(";")[-1].strip(), css[j + 1:k - 1]))
        i = k
    return rules


def decls(body):
    out = []
    for part in body.split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out.append((k.strip().lower(), v.strip()))
    return out


def resolve(value, props, depth=0):
    if depth > 10:
        return value
    m = re.search(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)", value)
    if not m:
        return value
    rep = props.get(m.group(1), m.group(2) or "")
    return resolve(value[:m.start()] + rep + value[m.end():], props, depth + 1)


def parse_color(value):
    v = value.strip().lower()
    m = re.search(r"#([0-9a-f]{6}|[0-9a-f]{3})\b", v)
    if m:
        h = m.group(1)
        h = "".join(c * 2 for c in h) if len(h) == 3 else h
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.search(r"rgba?\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)", v)
    if m:
        return tuple(int(x) for x in m.groups())
    if re.search(r"(^|\s)white(\s|$)", v):
        return (255, 255, 255)
    return None


def body_background(css):
    props, bg = {}, None
    rules = top_rules(css)
    for sel, body in rules:
        if any(s.strip() in (":root", "html") for s in sel.split(",")):
            for k, v in decls(body):
                if k.startswith("--"):
                    props[k] = v
    for sel, body in rules:
        if any(s.strip() == "body" for s in sel.split(",")):
            for k, v in decls(body):
                if k in ("background", "background-color"):
                    bg = v
    return (bg, parse_color(resolve(bg, props)) if bg else None)


# --- shared checks ------------------------------------------------------------------------------

def check_name():  # AC11
    rec = read(FEATURE / "name-check.txt")
    lines = [ln.strip() for ln in rec.splitlines() if ln.strip() and not ln.startswith("#")]
    queries = []
    for i, ln in enumerate(lines):
        m = re.match(r"query:\s*(kakao-map|daum)\s+(.+)$", ln)
        if m:
            queries.append((m.group(1), nospace(m.group(2))))
            if i + 1 >= len(lines) or not lines[i + 1].startswith("hits:"):
                fail(f"AC11 name-check.txt: '{ln}' is not followed by a 'hits:' line")
    for s in SAMPLES.values():
        wanted = {s["stem"] + suf for suf in NAME_SUFFIXES} | {s["name"]}
        for engine in ("kakao-map", "daum"):
            for q in sorted(wanted):
                if (engine, q) not in queries:
                    fail(f"AC11 name-check.txt: no 'query: {engine} {q}' line")
        if not re.search(rf"^verdict:\s*{re.escape(s['name'])}\s+no match\b", rec, re.M):
            fail(f"AC11 name-check.txt: no 'verdict: {s['name']} no match' line")


def check_gallery():  # AC46 AC53 (AC44 AC45 generated part)
    gallery = read(ROOT / "profile/index.html")
    if not re.search(r'data-filter="clinic"[^>]*>[^<]*<sup>3</sup>', gallery):
        fail("AC46 profile/index.html: the clinic filter chip does not show the count 3 (run python3 scripts/build.py)")
    for slug in SAMPLES:
        if f'data-slug="{slug}"' not in gallery:
            fail(f"AC44 profile/index.html has no card for {slug}")
    if re.search(r'class="pf-card pf-empty[^"]*" data-industry="clinic"', gallery):
        fail("AC45 profile/index.html still has the clinic 준비 중 tile")
    accents = {slug: accent(slug) for slug in SAMPLES}
    shipped = [(e.get("palette") or [""])[-1].lower() for e in load_profiles()
               if e.get("industry") != "clinic" and e.get("status") == "live"]
    for slug, a in accents.items():
        if not a or not re.fullmatch(r"#[0-9a-f]{6}", a):
            fail(f"AC53 {slug}: last palette entry is not a 6-digit hex: {a!r}")
            continue
        others = [x for s2, x in accents.items() if s2 != slug] + shipped
        if a in others:
            fail(f"AC53 {slug}: accent {a} is also used by another sample")


def check_current():  # AC84
    comp = read(ROOT / "docs/current_system/profile-samples/component.md")
    src = next((ln for ln in comp.splitlines() if ln.startswith("**Source:**")), "")
    for slug in SAMPLES:
        if slug not in src:
            fail(f"AC84 the Source line of profile-samples/component.md does not list {slug}")


# --- per-sample checks --------------------------------------------------------------------------

def check_photos(s):  # AC24 AC57-AC62
    files = s.image_files()
    if not files:
        fail(f"AC57 {s.slug}: img/ has no image files")
    total = 0
    for f in files:
        if f.suffix.lower() not in (".jpg", ".webp"):
            fail(f"AC57 {s.slug}: not .jpg/.webp: img/{f.name}")
        size = f.stat().st_size
        total += size
        if size > 500 * 1024:
            fail(f"AC59 {s.slug}: larger than 500 KB: img/{f.name} ({size // 1024} KB)")
        w, _ = sips_size(f)
        if w is None or w > 2000:
            fail(f"AC58 {s.slug}: wider than 2000 px or unreadable: img/{f.name} ({w})")
    if total > 3 * 1024 * 1024:
        fail(f"AC60 {s.slug}: img/ totals {total / 1024 / 1024:.2f} MB > 3 MB")
    lines = s.source_lines()
    names = [ln[0] for ln in lines if ln]
    for ln in lines:
        if len(ln) != 3:
            fail(f"AC61 {s.slug}: sources.txt line is not '<file> <page URL> <download URL>': {' '.join(ln)}")
            continue
        _, page_url, dl = ln
        if page_url != "-" and not page_url.startswith(("https://unsplash.com/photos/", "https://www.pexels.com/photo/")):
            fail(f"AC61 {s.slug}: page URL is not an Unsplash/Pexels photo page or '-': {page_url}")
        if not dl.startswith(("https://images.unsplash.com/photo-", "https://images.pexels.com/photos/")):
            fail(f"AC62 {s.slug}: download URL not allowed: {dl}")
    if sorted(names) != [f.name for f in files] or len(set(names)) != len(names):
        fail(f"AC61 {s.slug}: sources.txt files {sorted(names)} != img/ files {[f.name for f in files]}")
    raw = read(s.sources) if s.sources.is_file() else ""
    if "plus.unsplash.com" in raw or "premium_photo" in raw:
        fail(f"AC62 {s.slug}: sources.txt mentions plus.unsplash.com or premium_photo")
    others = {p: (ROOT / p) for p in OTHER_SOURCES}
    others.update({f"profile/{o}/img/sources.txt": ROOT / "profile" / o / "img" / "sources.txt"
                   for o in SAMPLES if o != s.slug})
    taken = {}
    for label, path in others.items():
        if path.is_file():
            for ln in path.read_text(encoding="utf-8").splitlines():
                pid = photo_id(ln)
                if pid:
                    taken[pid] = label
    for ln in lines:
        pid = photo_id(ln[-1]) if ln else None
        if pid and pid in taken:
            fail(f"AC24 {s.slug}: photo {pid} is also recorded in {taken[pid]}")


def check_markers(s):  # AC7 (text; visibility in check_browser.py) AC8 AC9 AC10 AC12 AC13 AC86 AC87
    _, _, p = s.page()
    if MARK not in norm(p.full()):
        fail(f"AC7 {s.slug}: page text lacks '{MARK}'")
    if "디자인 샘플" not in norm(" ".join(p.title)):
        fail(f"AC87 {s.slug}: <title> lacks '디자인 샘플'")
    foot = " ".join(p.footer)
    if MARK not in norm(foot):
        fail(f"AC86 {s.slug}: footer lacks '{MARK}'")
    if "Website by RobinTech" not in foot:
        fail(f"AC8 {s.slug}: footer lacks 'Website by RobinTech'")
    credit = foot.split("Photos:", 1)[1] if "Photos:" in foot else ""
    raw = s.sources.read_text(encoding="utf-8") if s.sources.is_file() else ""
    if not credit:
        fail(f"AC9 {s.slug}: footer has no 'Photos:' credit")
    for host, name in (("images.unsplash.com", "Unsplash"), ("images.pexels.com", "Pexels")):
        if host in raw and name not in credit:
            fail(f"AC9 {s.slug}: a {name} photo is used but the footer's 'Photos:' credit does not name {name}")
    if not any(m.get("name") == "robots" and m.get("content") == "noindex" for m in p.metas):
        fail(f'AC10 {s.slug}: no <meta name="robots" content="noindex">')
    addr = re.compile(r"[가-힣0-9]*[가-힣0-9](?<!으)(?:로|길)\s?\d+(?:-\d+)?"
                      r"(?![\d%A-Za-z가-힣~:.-]|,\d|\s?(?:원|분|시|개|인|일|명|번|미터|층|m(?![A-Za-z])))")
    lines = p.lines()
    if not any("(가상 주소)" in ln for ln in lines):
        fail(f"AC12 {s.slug}: no address with '(가상 주소)' on the page")
    for ln in lines:
        if addr.search(ln) and "(가상 주소)" not in ln:
            fail(f"AC12 {s.slug}: address without '(가상 주소)': {ln[:80]}")
    text = p.full() + "\n" + " ".join(v for _, v in p.refs)
    phones = re.findall(r"(?<![\d-])(?:0\d{1,2}[-.\s]\d{3,4}|1[5-9]\d{2})[-.\s]\d{4}(?![\d-])", text)
    if "02-000-0000" not in phones:
        fail(f"AC13 {s.slug}: no phone number 02-000-0000 on the page")
    for ph in phones:
        if ph != "02-000-0000":
            fail(f"AC13 {s.slug}: phone number is not 02-000-0000: {ph}")
    for brn in re.findall(r"(?<![\d-])\d{3}[-.\s]\d{2}[-.\s]\d{5}(?![\d-])", text):
        if brn != "000-00-00000":
            fail(f"AC13 {s.slug}: business registration number is not 000-00-00000: {brn}")


def check_flow(s):  # AC17 (stylesheet) AC18 AC19 AC20 AC32-AC38
    _, css, p = s.page()
    if not re.search(r"word-break\s*:\s*keep-all", css):
        fail(f"AC17 {s.slug}: style.css has no word-break: keep-all")

    def first(pattern):
        hits = [off for lvl, t, off in p.headings if lvl >= 2 and re.search(pattern, t)]
        return min(hits) if hits else None
    order = [("진료 안내", r"진료\s?안내"), ("의료진", r"의료진"), ("진료시간", r"진료\s?시간"), ("오시는 길", r"오시는\s?길")]
    offs = [first(pat) for _, pat in order]
    if None in offs or offs != sorted(offs):
        fail(f"AC18 {s.slug}: h2-h6 headings 진료 안내 < 의료진 < 진료시간 < 오시는 길 not found in that order "
             f"(offsets {dict(zip([n for n, _ in order], offs))})")
    hours = p.section(r"진료\s?시간") or ""
    if not re.search(r"점심[\s\S]{0,40}?" + HOURS, hours):
        fail(f"AC19 {s.slug}: the 진료시간 section shows no 점심시간 with its hours (점심 … HH:MM–HH:MM)")
    for word in ("휴진", "일요일", "공휴일"):
        if word not in hours:
            fail(f"AC20 {s.slug}: the 진료시간 section lacks '{word}'")
    for ac, word in (("AC32", "네이버 예약"), ("AC33", "전화"), ("AC34", "카카오톡"), ("AC35", "네이버 지도")):
        hits = [c for c in p.controls if word in (c["name"] or "")]
        if not hits:
            fail(f"{ac} {s.slug}: no link or button whose accessible name contains '{word}'")
        for c in hits:
            if c["href"] != "#":
                fail(f"AC36 {s.slug}: '{c['name']}' has href={c['href']!r}, not '#'")
    for img in p.imgs:
        if not img.get("alt", "").strip():
            fail(f"AC37 {s.slug}: <img> without alt: {img.get('src')}")
    levels = [lvl for lvl, _, _ in sorted(p.headings, key=lambda h: h[2])]
    if levels.count(1) != 1:
        fail(f"AC38 {s.slug}: expected exactly one <h1>, found {levels.count(1)}")
    prev = 1
    for lvl in levels:
        if lvl > prev + 1:
            fail(f"AC38 {s.slug}: heading level skipped: h{prev} -> h{lvl}")
        prev = lvl


def check_law(s):  # AC25 AC29 AC30
    _, _, p = s.page()
    text = law_text(p)
    for word in BANNED:
        if word in text:
            i = text.index(word)
            fail(f"AC25 {s.slug}: page text contains '{word}': …{text[max(0, i - 20):i + 20]}…")
    for ln in p.lines():
        for m in PRACTITIONER.finditer(ln):
            if m.group(1) in NOT_A_NAME or m.group(1).endswith("과"):
                continue
            if "가상" not in ln.replace("(가상 주소)", ""):
                fail(f"AC29 {s.slug}: practitioner '{m.group(0)}' has no '가상' marker on its line: {ln[:80]}")
    for m in re.finditer(r"(면허\s*번호|면허|의료기관\s*(?:번호|기호)|요양기관\s*(?:번호|기호))\s*[:：]?\s*(?:제\s*)?"
                         r"(?:No\.?\s*)?([0-9][0-9\- ]*)", text):
        if re.search(r"[1-9]", m.group(2)):
            fail(f"AC30 {s.slug}: {m.group(1)} with a digit other than 0: {m.group(0)}")


def check_assets(s):  # AC1 (page files) AC2 AC21 AC23 AC50 (reference names) AC55 AC56
    html, css, p = s.page()
    for name in ("index.html", "style.css"):
        if not (s.site / name).is_file():
            fail(f"AC1 missing profile/{s.slug}/{name}")
    local = [v for k, v in p.refs if k != "srcset"] + [u for k, v in p.refs if k == "srcset" for u in srcset_urls(v)]
    local += css_urls(css)
    for ref in local:
        if ref.startswith(("http://", "https://", "data:", "#", "mailto:", "tel:")):
            continue
        if ref.startswith("/") or "../" in ref or "assets/" in ref:
            fail(f"AC2 {s.slug}: reference leaves the sample folder: {ref}")
    if "../" in html + css or re.search(r"\bassets/", html + css):
        fail(f"AC2 {s.slug}: index.html or style.css contains '../' or 'assets/'")

    def font_host(u):
        return u.netloc == "fonts.googleapis.com" or (u.netloc == "cdn.jsdelivr.net" and "pretendard" in u.path.lower())
    for link in p.links:
        href = link.get("href", "")
        if "stylesheet" in link.get("rel", "") and href.startswith(("http", "//")):
            if not font_host(urlparse(href if not href.startswith("//") else "https:" + href)):
                fail(f"AC21 {s.slug}: external stylesheet not allowed: {href}")
    for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", css):
        u = urlparse(imp)
        if u.netloc and not font_host(u):
            fail(f"AC21 {s.slug}: external @import not allowed: {imp}")
    for src in p.scripts:
        if src.startswith(("http", "//")):
            fail(f"AC21 {s.slug}: external script: {src}")
    for url in re.findall(r"https?://[^\s\"'()<>,]+", html + css):
        if url.startswith("http://www.w3.org/"):  # an XML namespace (inline SVG), not a load
            continue
        if urlparse(url).netloc not in ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net"):
            fail(f"AC23 {s.slug}: URL with a host that is not allowed: {url}")
    for pat in s.info["ref"]:
        if re.search(pat, html + css, re.I if pat[0] != "\\" else 0):
            fail(f"AC50 {s.slug}: the sample names its reference site ({pat})")
    for ref in (r.removeprefix("./") for r in image_refs(p, css)):
        path = (s.site / ref.split("?")[0].split("#")[0]).resolve()
        if not path.is_file() or s.site.resolve() not in path.parents:
            fail(f"AC55 {s.slug}: image path does not resolve inside the sample folder: {ref}")
        if re.search(r"\.(jpe?g|png|webp|avif|gif)$", ref.split("?")[0], re.I) and not ref.startswith("img/"):
            fail(f"AC56 {s.slug}: photo not in img/: {ref}")


def law_text(p):  # AC25 AC81: visible text, <title>, meta description/og: content, aria-label and title attributes
    return norm(" ".join([p.full(), *p.title, *p.attr_text]))


def count_terms(text, vocab):
    flat = nospace(text)
    return sorted({t for t in vocab if t in flat})


def check_sample(s):  # A: AC67-AC69  B: AC70-AC76  D: AC79 AC81 AC82
    _, css, p = s.page()
    if s.slug == "clinic-neuru":
        if fonts_loaded(s, "Cormorant Garamond"):
            fail("AC67 clinic-neuru loads Cormorant Garamond")
        items = count_terms(p.section(r"진료\s?안내") or "", DENTAL)
        if len(items) < 4:
            fail(f"AC68 clinic-neuru: the 진료 안내 section names {len(items)} dental items {items}, needs 4")
        team = p.section(r"의료진") or ""
        names = [m for ln in team.split("\n") for m in PRACTITIONER.findall(norm(ln))
                 if m[0] not in NOT_A_NAME and not m[0].endswith("과")]
        if not names or not re.search(r"치과|치의", team):
            fail("AC69 clinic-neuru: the 의료진 section names no dentist ('<이름> 대표원장|원장|부원장' and '치과')")
    elif s.slug == "clinic-byeotteul":
        raw, rgb = body_background(css)
        if not rgb:
            fail(f"AC70 AC71 clinic-byeotteul: no readable body background colour in style.css ({raw!r})")
        else:
            if rgb[2] < rgb[0]:
                fail(f"AC70 clinic-byeotteul: body background {rgb} has blue < red (cream)")
            if min(rgb) < 0xF0:
                fail(f"AC71 clinic-byeotteul: body background {rgb} has a channel below 0xF0")
        if fonts_loaded(s, "IBM Plex Mono"):
            fail("AC72 clinic-byeotteul loads IBM Plex Mono")
        if fonts_loaded(s, "Cormorant Garamond"):
            fail("AC73 clinic-byeotteul loads Cormorant Garamond")
        if p.header_at is None or "휴진" not in p.full()[p.body_at or 0:p.header_at]:
            fail("AC74 clinic-byeotteul: no text with '휴진' in <body> before the first <header>")
        bad = re.compile(r"로그인|회원\s?가입|가입|보험|네트워크|log\s?in|sign\s?(up|in)|insurance|network", re.I)
        for c in p.controls:
            if bad.search(c["name"] or ""):
                fail(f"AC75 clinic-byeotteul: login, sign-up or insurance control: {c['name']}")
        items = count_terms(p.section(r"진료\s?안내") or "", EVERYDAY)
        if len(items) < 4:
            fail(f"AC76 clinic-byeotteul: the 진료 안내 section names {len(items)} everyday items {items}, needs 4")
    elif s.slug == "clinic-bonui":
        if fonts_loaded(s, "Cormorant Garamond"):
            fail("AC79 clinic-bonui loads Cormorant Garamond")
        text = law_text(p)
        for word in BANNED_BONUI:
            if word in text:
                fail(f"AC81 clinic-bonui: page text contains '{word}'")
        if BONUI_SENTENCE not in norm(p.section(r"진료\s?안내") or ""):
            fail(f"AC82 clinic-bonui: the 진료 안내 section lacks the sentence '{BONUI_SENTENCE}'")


def check_register(s):  # AC1 (thumb.jpg) AC3 AC4 AC54
    e = entry(s.slug)
    if not e:
        n = sum(1 for p in load_profiles() if p.get("slug") == s.slug)
        fail(f"AC3 expected one PROFILES entry for {s.slug}, found {n}")
    elif (e.get("industry"), e.get("status"), e.get("demo")) != ("clinic", "live", True):
        fail(f"AC3 {s.slug}: entry fields wrong: industry={e.get('industry')} status={e.get('status')} "
             f"demo={e.get('demo')}")
    thumb = s.site / "thumb.jpg"
    if thumb.is_file():
        w, h = sips_size(thumb)
        if w != 1200 or h is None or abs(h * 16 - w * 10) > 16:
            fail(f"AC4 {s.slug}: thumb.jpg is {w}x{h}, not 1200 wide at 16:10")
    else:
        fail(f"AC1 AC4 {s.slug}: thumb.jpg missing")
    a = accent(s.slug)
    css = (s.site / "style.css").read_text(encoding="utf-8") if (s.site / "style.css").is_file() else ""
    if not a or a not in css.lower():
        fail(f"AC54 {s.slug}: style.css does not contain the PROFILES accent {a}")


PER_SAMPLE = {"photos": check_photos, "markers": check_markers, "flow": check_flow, "law": check_law,
              "assets": check_assets, "sample": check_sample, "register": check_register}
SHARED = {"name": check_name, "gallery": check_gallery, "current": check_current}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] not in (*PER_SAMPLE, *SHARED, "all") or len(args) > 2 or \
            (len(args) == 2 and (args[1] not in SAMPLES or args[0] not in PER_SAMPLE)):
        raise SystemExit(__doc__)
    slugs = [args[1]] if len(args) == 2 else list(SAMPLES)
    names = [*PER_SAMPLE, *SHARED] if args[0] == "all" else [args[0]]
    samples = [Sample(slug) for slug in slugs]
    for n in names:
        if n in SHARED:
            SHARED[n]()
        else:
            for s in samples:
                PER_SAMPLE[n](s)
    seen = set()
    for f in fails:
        if f not in seen:
            seen.add(f)
            print("FAIL", f)
    print(f"{'PASS' if not fails else 'FAIL'}: {' '.join(args)} ({len(seen)} failures)")
    sys.exit(1 if fails else 0)
