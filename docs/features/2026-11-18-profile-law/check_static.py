#!/usr/bin/env python3
"""Static checks for the two law-firm profile samples (no browser, no network). Run from the repository root.

usage: python3 docs/features/2026-11-18-profile-law/check_static.py <check> [<slug>]
  per sample (both when <slug> is left out): photos markers form ads flow assets sample register
  shared: name gallery current
  all: every check above, for every sample
slugs: law-ganeum law-goim
Exit 0 when every named check passes; otherwise prints each failure and exits 1.
The page contract these checks read is the "Fixed parameters" section of tasks.md in this folder.
"""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import colorsys
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unicodedata
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[3]
FEATURE = Path(__file__).resolve().parent
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
FEE = "상담 비용과 수임료는 상담 후 사건에 따라 안내드립니다."
OUTCOME = "사건의 결과는 사실관계와 증거에 따라 달라질 수 있습니다."

# AC91 (A) and AC103 (C): practice items, each a group of spellings counted once (spaces and middots ignored)
LITIGATION = (r"민사소송", r"형사(사건)?변호|형사사건", r"행정소송", r"가사소송", r"손해배상", r"이혼", r"상속",
              r"부동산분쟁", r"건설분쟁", r"노동(분쟁|사건)", r"의료분쟁", r"강제집행", r"보전처분|가압류|가처분",
              r"수사대응", r"고소대리")
ADVISORY = (r"회사설립|법인설립", r"지배구조", r"계약(서)?검토|계약자문", r"인사노무|노무", r"공정거래",
            r"개인정보|정보보호", r"투자|인수합병|M&A", r"지식재산|상표|특허", r"가맹|하도급", r"상사분쟁|기업분쟁",
            r"규제대응|인허가")
SAMPLES = {
    "law-ganeum": {
        "stem": "가늠", "name": "법무법인 가늠",
        "lawyers": ("남도윤", "문지후", "오세린", "신태오"),  # tasks.md Picks; the first is 대표변호사
        "ref": (r"selendy", r"\bgay\s*llp\b"),
        "vocab": LITIGATION,
    },
    "law-goim": {
        "stem": "고임", "name": "법무법인 고임",
        "lawyers": ("정다인", "백승우", "류하은", "임서하"),
        "ref": (r"kim\s*&\s*chang", r"kimchang", r"김\s*[·・ㆍ&]\s*장", r"김앤장", r"김\s*·\s*장\s*법률"),
        "vocab": ADVISORY,
    },
}
BANNED = {  # AC22-AC28, AC92 (A), AC105 (C): plain substrings of the page text (AC22 reading)
    "AC22": ("최고", "최초", "최상", "최대", "최다", "유일", "독보적", "1위", "1등", "No.1", "넘버원", "완벽", "100%",
             "100 %", "100％", "보장", "보증", "무조건", "확실", "승소", "승률", "성공률", "성공사례", "성공 사례",
             "해결사례", "석방", "결과 예측"),
    "AC23": ("전문", "전담", "특화"),
    "AC24": ("무료", "공짜", "할인", "최저", "원가", "후불", "환불", "견적", "쿠폰", "이벤트", "저렴", "염가",
             "성공보수"),
    "AC25": ("전관", "출신", "국제변호사"),
    "AC26": ("본사", "본점", "지점", "지사", "본부"),
    "AC27": ("사무장", "실장", "국장"),
    "AC28": ("후기", "리뷰", "별점", "평점", "만족도", "★", "감사 편지", "감사편지"),
}
BANNED_SAMPLE = {
    "law-ganeum": ("AC92", ("무죄", "무혐의", "혐의없음", "불기소", "기소유예", "집행유예", "선고유예", "감형", "감경",
                            "불구속", "선처", "기각")),
    "law-goim": ("AC105", ("고문사", "고객사", "파트너사", "자문 실적", "절세", "리스크 제로")),
}
SHIPPED_FACES = ("Cormorant Garamond", "Noto Serif KR", "IBM Plex Mono", "Gothic A1", "Gowun Dodum", "Noto Sans KR",
                 "Nanum Myeongjo", "Gowun Batang", "Hahmlet", "Song Myung")  # AC96
A_H1_FACES = ("Nanum Myeongjo", "Gowun Batang", "Hahmlet", "Song Myung")  # AC85
HOURS = r"\d{1,2}:\d{2}\s*[-–—~～〜]\s*\d{1,2}:\d{2}"
WEEKDAY = r"평일|월요일?\s*[-–—~～〜]\s*금요일?|월\s*[-–—~～〜·]\s*금"
LANG = re.compile(r"^(en|eng|english|jp|cn|日本語|中文)$", re.I)  # AC102
BLOCK = {"p", "li", "dd", "dt", "td", "th", "address", "div", "section", "article", "header", "footer", "ul", "ol",
         "h1", "h2", "h3", "h4", "h5", "h6", "button", "nav", "main", "aside", "figure", "figcaption", "tr", "table",
         "dl"}
fails = []


def fail(msg):
    fails.append(msg)


def read(path):
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"not UTF-8: {path.relative_to(ROOT)} ({exc.reason} at byte {exc.start})")
        return ""


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def flat(s):  # spaces and middots dropped, for term matching
    return re.sub(r"[\s·・ㆍ,/]+", "", s or "")


class Page(HTMLParser):
    """Collects text (with block breaks), headings, controls, ids, list items, images, refs, header and footer."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []            # visible text chunks; "\n" at block boundaries
        self.headings = []        # (level, text, offset)
        self.controls = []        # dict(tag, href, name, text, label, offset, in_header, in_first_section)
        self.ids = {}             # id -> text offset of its start tag
        self.item_ids = {}        # the same, for ids on h3-h6 and <article> only (AC90 targets)
        self.li = []              # text offsets of <li> start tags
        self.imgs, self.refs, self.links, self.scripts, self.metas, self.inputs = [], [], [], [], [], []
        self.forms, self.roles = 0, []
        self.title, self.attr_text = [], []
        self.footer_span = None   # (start, end) of the first <footer>
        self._stack = []
        self._skip = 0
        self._header = None       # None before the first <header>, then depth, then "done"
        self._section = None      # same for the first <section>
        self._footer = None

    def _offset(self):
        return sum(len(t) for t in self.text)

    def _track(self, attr, tag, want, start):
        state = getattr(self, attr)
        if tag != want:
            return
        if start:
            if state is None:
                setattr(self, attr, 1)
                return "open"
            if isinstance(state, int):
                setattr(self, attr, state + 1)
        elif isinstance(state, int):
            setattr(self, attr, state - 1 if state > 1 else "done")
            return "close" if state == 1 else None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        self.attr_text += [a[k] for k in ("aria-label", "title") if a.get(k)]
        if tag == "meta" and (a.get("name") == "description" or a.get("property", "").startswith("og:")):
            self.attr_text.append(a.get("content", ""))
        if tag in ("script", "style", "template", "title"):
            self._skip += 1
            if tag == "script" and a.get("src"):
                self.scripts.append(a["src"])
        self._track("_header", tag, "header", True)
        self._track("_section", tag, "section", True)
        if self._track("_footer", tag, "footer", True) == "open":
            self.footer_span = (self._offset(), None)
        if a.get("id"):
            self.ids.setdefault(a["id"], self._offset())
            if tag in ("h3", "h4", "h5", "h6", "article"):
                self.item_ids.setdefault(a["id"], self._offset())
        if a.get("role"):
            self.roles.append(a["role"])
        if tag == "form":
            self.forms += 1
        if tag in BLOCK:
            self.text.append("\n")
        elif tag in ("br", "a"):
            self.text.append(" ")
        if tag == "li":
            self.li.append(self._offset())
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
        elif tag == "input":
            self.inputs.append(a)
            if a.get("type") in ("submit", "button"):
                self.controls.append(self._control(tag, None, a.get("aria-label"), a.get("value", "")))
        if tag in ("a", "button"):
            self._stack.append({"kind": "control", "tag": tag, "href": a.get("href"), "label": a.get("aria-label"),
                                "buf": [], "offset": self._offset(), "in_header": isinstance(self._header, int),
                                "in_section": isinstance(self._section, int)})
        elif re.fullmatch(r"h[1-6]", tag):
            self._stack.append({"kind": "heading", "level": int(tag[1]), "buf": [], "offset": self._offset()})

    def _control(self, tag, href, label, txt, offset=None, in_header=False, in_section=False):
        return {"tag": tag, "href": href, "label": label or "", "text": txt, "name": label if label else txt,
                "offset": offset if offset is not None else self._offset(), "in_header": in_header,
                "in_section": in_section}

    def handle_endtag(self, tag):
        if tag in ("script", "style", "template", "title"):
            self._skip = max(0, self._skip - 1)
        if tag in BLOCK:
            self.text.append("\n")
        elif tag in ("br", "a"):
            self.text.append(" ")
        self._track("_header", tag, "header", False)
        self._track("_section", tag, "section", False)
        if self._track("_footer", tag, "footer", False) == "close":
            self.footer_span = (self.footer_span[0], self._offset())
        kind = {"a": "control", "button": "control"}.get(tag)
        if re.fullmatch(r"h[1-6]", tag):
            kind = "heading"
        if not kind:
            return
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i]["kind"] == kind:
                item = self._stack.pop(i)
                txt = norm("".join(item["buf"]))
                if kind == "control":
                    self.controls.append(self._control(item["tag"], item["href"], item["label"], txt, item["offset"],
                                                       item["in_header"], item["in_section"]))
                else:
                    self.headings.append((item["level"], txt, item["offset"]))
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

    def lines(self, start=0, end=None):
        return [norm(ln) for ln in self.full()[start:end].split("\n") if ln.strip()]

    def footer_lines(self):
        if not self.footer_span:
            return []
        return self.lines(self.footer_span[0], self.footer_span[1])

    def span(self, pattern, min_level=2):
        """(start, end) of the first heading of level >= min_level matching pattern, up to the next heading of the
        same or a higher level."""
        hs = sorted(self.headings, key=lambda h: h[2])
        for i, (lvl, txt, off) in enumerate(hs):
            if lvl >= min_level and re.search(pattern, txt):
                end = next((o for l, _, o in hs[i + 1:] if l <= lvl), len(self.full()))
                return off, end
        return None

    def section(self, pattern, min_level=2):
        s = self.span(pattern, min_level)
        return self.full()[s[0]:s[1]] if s else None


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


def sips_missing():
    if shutil.which("sips"):
        return False
    fail("sips not found: the image checks need macOS sips")
    return True


def sips_size(path):
    if sips_missing():
        return (None, None)
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True)
    w = re.search(r"pixelWidth:\s*(\d+)", r.stdout)
    h = re.search(r"pixelHeight:\s*(\d+)", r.stdout)
    return (int(w.group(1)), int(h.group(1))) if w and h else (None, None)


def mean_luma(path):  # AC116: ITU-R 601 luma over all pixels, decoded by sips to an uncompressed 24/32-bit BMP
    with tempfile.TemporaryDirectory() as tmp:
        bmp = Path(tmp) / "t.bmp"
        subprocess.run(["sips", "-s", "format", "bmp", str(path), "--out", str(bmp)], capture_output=True, check=True)
        d = bmp.read_bytes()
    off = struct.unpack_from("<I", d, 10)[0]
    w, h = struct.unpack_from("<ii", d, 18)
    bp = struct.unpack_from("<H", d, 28)[0] // 8
    if struct.unpack_from("<I", d, 30)[0] != 0 or bp not in (3, 4):
        raise ValueError("unexpected BMP format from sips")
    h, row, total = abs(h), (w * bp + 3) // 4 * 4, 0.0
    for y in range(h):
        r = d[off + y * row: off + y * row + w * bp]
        total += 0.299 * sum(r[2::bp]) + 0.587 * sum(r[1::bp]) + 0.114 * sum(r[0::bp])
    return total / (w * h)


def load_profiles():
    sys.path.insert(0, str(ROOT / "scripts"))
    from profiles import PROFILES  # noqa: E402
    return PROFILES


def entry(slug):
    hits = [p for p in load_profiles() if p.get("slug") == slug]
    return hits[0] if len(hits) == 1 else None


def accent_of(e):
    return (e.get("palette") or [""])[-1].lower()


def hsl(hexv):
    r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s, l


def fonts_loaded(s, family):  # anywhere in index.html or style.css: a link, an @import, a font stack, a comment
    html, css, _ = s.page()
    pat = re.escape(family).replace(r"\ ", r"[ +]")
    return bool(re.search(pat, html + css, re.I))


def css_content(css):  # strings in CSS content: declarations, read with the page text (AC22-AC28 AC92 AC105)
    return [m[1] for m in re.findall(r"content\s*:\s*([\"'])(.*?)\1", css)]


def law_text(p, css=""):  # AC22 reading: visible text, <title>, meta description/og: content, aria-label, alt, title,
    return norm(" ".join([p.full(), *p.title, *p.attr_text, *css_content(css)]))  # and CSS content: strings


# --- CSS: top-level rules, custom properties --------------------------------------------------------------

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


def custom_props(rules):
    props = {}
    for sel, body in rules:
        if any(x.strip() in (":root", "html") for x in sel.split(",")):
            for k, v in decls(body):
                if k.startswith("--"):
                    props[k] = v
    return props


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


def body_background(css):  # AC82 AC94 AC95: last background(-color) in a top-level `body` rule
    rules, bg = top_rules(css), None
    props = custom_props(rules)
    for sel, body in rules:
        if any(x.strip() == "body" for x in sel.split(",")):
            for k, v in decls(body):
                if k in ("background", "background-color"):
                    bg = v
    return bg, parse_color(resolve(bg, props)) if bg else None


def h1_family(css):  # AC85 AC108: first family of the last font-family/font declaration in a rule for `h1`
    rules, fam = top_rules(css), None
    props = custom_props(rules)
    for sel, body in rules:
        if any(re.search(r"(^|[\s>+~])h1([.:#\[][^\s]*)?$", x.strip()) for x in sel.split(",")):
            for k, v in decls(body):
                v = resolve(v, props)
                if k == "font-family":
                    fam = v
                elif k == "font":
                    while re.search(r"[a-z-]+\([^()]*\)", v):  # clamp(), min(), calc() … stand in as a size
                        v = re.sub(r"[a-z-]+\([^()]*\)", "0px", v)
                    m = re.search(r"[\d.]+(?:px|r?em|%|vw|vh|vmin|vmax|pt|ch)(?:\s*/\s*[\w.%-]+)?\s+(.+)$", v)
                    fam = m.group(1) if m else fam
    if fam is None:
        return None
    return fam.split(",")[0].strip().strip("'\"")


# --- shared checks ---------------------------------------------------------------------------------------

def check_name():  # AC13
    rec = read(FEATURE / "name-check.txt")
    lines = [ln.strip() for ln in rec.splitlines() if ln.strip() and not ln.startswith("#")]
    queries = []
    for i, ln in enumerate(lines):
        m = re.match(r"query:\s*(kakao-map|daum|kba|kba-control)\s+(.+)$", ln)
        if m:
            queries.append((m.group(1), flat(m.group(2).replace('"', ""))))
            if i + 1 >= len(lines) or not lines[i + 1].startswith("hits:"):
                fail(f"AC13 name-check.txt: '{ln}' is not followed by a 'hits:' line")
            elif m.group(1) != "kba-control":  # a hit that names the firm contradicts a 'no match' verdict
                for s in SAMPLES.values():
                    if flat("법무법인" + s["stem"]) in flat(lines[i + 1]):
                        fail(f"AC13 name-check.txt: a hit names {s['name']}: '{lines[i + 1]}'")
    if not any(e == "kba-control" for e, _ in queries):
        fail("AC13 name-check.txt: no 'query: kba-control <name>' line (a KBA search for a firm that exists)")
    for s in SAMPLES.values():
        st = s["stem"]
        wanted = [("kakao-map", q) for q in (f"법무법인{st}", f"{st}법률", f"{st}변호사", f"{st}법률사무소", st)]
        wanted += [("daum", f"법무법인{st}"), ("kba", st)]
        for engine, q in wanted:
            if (engine, q) not in queries:
                fail(f"AC13 name-check.txt: no 'query: {engine} {q}' line (spaces and quotes ignored)")
        if not re.search(rf"^verdict:\s*{re.escape(s['name'])}\s+no match\b", rec, re.M):
            fail(f"AC13 name-check.txt: no 'verdict: {s['name']} no match' line")


def check_gallery():  # AC69 AC74 AC107 (AC68 AC78 generated part)
    gallery = read(ROOT / "profile/index.html")
    if not re.search(r'data-filter="law"[^>]*>[^<]*<sup>2</sup>', gallery):
        fail("AC69 profile/index.html: the law filter chip does not show the count 2 (run python3 scripts/build.py)")
    for slug in SAMPLES:
        if f'data-slug="{slug}"' not in gallery:
            fail(f"AC68 profile/index.html has no card for {slug}")
    if re.search(r'class="pf-card pf-empty[^"]*" data-industry="law"', gallery):
        fail("AC78 profile/index.html still has the law 준비 중 tile")
    profiles = load_profiles()
    for slug in SAMPLES:
        e = entry(slug)
        a = accent_of(e) if e else ""
        if not re.fullmatch(r"#[0-9a-f]{6}", a):
            fail(f"AC74 {slug}: last palette entry is not a 6-digit hex: {a!r}")
            continue
        hue, sat, _ = hsl(a)
        if sat < 0.25:
            fail(f"AC107 {slug}: accent {a} has HSL saturation {sat:.2f} < 0.25")
        for other in profiles:
            if other.get("slug") == slug:
                continue
            b = accent_of(other)
            if not re.fullmatch(r"#[0-9a-f]{6}", b):
                fail(f"AC74 {other.get('slug')}: accent {b!r} is not a 6-digit hex")
                continue
            d = abs(hue - hsl(b)[0]) % 360
            d = min(d, 360 - d)
            if d < 25:
                fail(f"AC74 {slug}: accent {a} ({hue:.0f}°) is {d:.0f}° from {other.get('slug')} {b} "
                     f"({hsl(b)[0]:.0f}°), needs 25°")


def check_current():  # AC75
    comp = read(ROOT / "docs/current_system/profile-samples/component.md")
    src = next((ln for ln in comp.splitlines() if ln.startswith("**Source:**")), "")
    for slug in SAMPLES:
        if slug not in src:
            fail(f"AC75 the Source line of profile-samples/component.md does not list {slug}")


# --- per-sample checks -----------------------------------------------------------------------------------

def check_photos(s):  # AC52 AC55-AC60
    files = s.image_files()
    if not files:
        fail(f"AC55 {s.slug}: img/ has no image files")
    total = 0
    for f in files:
        if f.suffix.lower() not in (".jpg", ".webp"):
            fail(f"AC55 {s.slug}: not .jpg/.webp: img/{f.name}")
        size = f.stat().st_size
        total += size
        if size > 500 * 1024:
            fail(f"AC57 {s.slug}: larger than 500 KB: img/{f.name} ({size // 1024} KB)")
        w, _ = sips_size(f)
        if w is None or w > 2000:
            fail(f"AC56 {s.slug}: wider than 2000 px or unreadable: img/{f.name} ({w})")
    if total > 3 * 1024 * 1024:
        fail(f"AC58 {s.slug}: img/ totals {total / 1024 / 1024:.2f} MB > 3 MB")
    lines = s.source_lines()
    names = [ln[0] for ln in lines if ln]
    for ln in lines:
        if len(ln) != 3:
            fail(f"AC59 {s.slug}: sources.txt line is not '<file> <page URL> <download URL>': {' '.join(ln)}")
            continue
        _, page_url, dl = ln
        if page_url != "-" and not page_url.startswith(("https://unsplash.com/photos/", "https://www.pexels.com/photo/")):
            fail(f"AC59 {s.slug}: page URL is not an Unsplash/Pexels photo page or '-': {page_url}")
        if not dl.startswith(("https://images.unsplash.com/photo-", "https://images.pexels.com/photos/")):
            fail(f"AC60 {s.slug}: download URL not allowed: {dl}")
    if sorted(names) != [f.name for f in files] or len(set(names)) != len(names):
        fail(f"AC59 {s.slug}: sources.txt files {sorted(names)} != img/ files {[f.name for f in files]}")
    raw = s.sources.read_text(encoding="utf-8") if s.sources.is_file() else ""
    if "plus.unsplash.com" in raw or "premium_photo" in raw:
        fail(f"AC60 {s.slug}: sources.txt mentions plus.unsplash.com or premium_photo")
    taken = {}
    for path in sorted((ROOT / "profile").glob("*/img/sources.txt")):
        if path.parent.parent.name == s.slug:
            continue
        for ln in read(path).splitlines():
            pid = photo_id(ln)
            if pid:
                taken[pid] = str(path.relative_to(ROOT))
    for ln in lines:
        pid = photo_id(ln[-1]) if ln else None
        if pid and pid in taken:
            fail(f"AC52 {s.slug}: photo {pid} is also recorded in {taken[pid]}")


def check_markers(s):  # AC7 (text; visibility in check_browser.py) AC8 AC9 AC10 AC11 AC12 AC14 AC15
    _, _, p = s.page()
    if MARK not in norm(p.full()):
        fail(f"AC7 {s.slug}: page text lacks '{MARK}'")
    if "디자인 샘플" not in norm(" ".join(p.title)):
        fail(f"AC12 {s.slug}: <title> lacks '디자인 샘플'")
    foot = " ".join(p.footer_lines())
    if not p.footer_span:
        fail(f"AC8 AC11 {s.slug}: no <footer>")
    if MARK not in foot:
        fail(f"AC11 {s.slug}: footer lacks '{MARK}'")
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
        fail(f"AC14 {s.slug}: no address with '(가상 주소)' on the page")
    for ln in lines:
        if addr.search(ln) and "(가상 주소)" not in ln:
            fail(f"AC14 {s.slug}: address without '(가상 주소)': {ln[:80]}")
    text = p.full() + "\n" + " ".join(v for _, v in p.refs) + "\n" + " ".join(p.attr_text)
    phones = re.findall(r"(?<![\d-])(?:0\d{1,2}[-.\s]\d{3,4}|1[5-9]\d{2})[-.\s]\d{4}(?![\d-])", text)
    if "02-000-0000" not in phones:
        fail(f"AC15 {s.slug}: no phone number 02-000-0000 on the page")
    for ph in phones:
        if ph != "02-000-0000":
            fail(f"AC15 {s.slug}: phone number is not 02-000-0000: {ph}")
    for brn in re.findall(r"(?<![\d-])\d{3}[-.\s]\d{2}[-.\s]\d{5}(?![\d-])", text):
        if brn != "000-00-00000":
            fail(f"AC15 {s.slug}: business registration number is not 000-00-00000: {brn}")


def wordmark(p, stem):  # the first <a> in the first <header> whose text or aria-label holds the name stem
    return next((c for c in p.controls if c["in_header"] and c["tag"] == "a"
                 and (stem in c["text"] or stem in c["label"])), None)


def marked(name):  # AC18: the name, then within a title (대표, 광고책임, 구성원 변호사) and a few marks, 가상
    return re.compile(re.escape(name) + r"[^가-힣]{0,3}(?:대표변호사|광고책임변호사|구성원\s?변호사|변호사)?[^가-힣]{0,3}가상")


def check_form(s):  # AC16 AC17 AC18 (the fixed names) AC19 AC20 AC21
    _, _, p = s.page()
    name, stem, lawyers = s.info["name"], s.info["stem"], s.info["lawyers"]
    full_name = re.compile(r"법무법인\s?" + re.escape(stem))
    wm = wordmark(p, stem)
    places = {"<title>": norm(" ".join(p.title)), "footer": " ".join(p.footer_lines()),
              "header wordmark": (wm["text"] + " " + wm["label"]) if wm else ""}
    if not wm:
        fail(f"AC16 {s.slug}: no wordmark (an <a> in the first <header> whose text or aria-label contains '{stem}')")
    for where, txt in places.items():
        if txt and not full_name.search(txt):
            fail(f"AC16 {s.slug}: {where} does not name the firm as '{name}'")
        if re.search(r"법률\s?사무소|" + re.escape(stem) + r"\s?법률", txt):
            fail(f"AC16 {s.slug}: {where} names the firm in another form ('법률사무소' or '{stem} 법률')")
    team = p.span(r"구성원")
    listed = set()
    if not team:
        fail(f"AC17 {s.slug}: no h2-h6 heading '구성원'")
    else:
        listed = {n for ln in p.lines(*team) for n in lawyers if n in ln and "변호사" in ln}
        if len(listed) < 3:
            fail(f"AC17 {s.slug}: the 구성원 section lists {len(listed)} of the fixed lawyers with '변호사' "
                 f"({sorted(listed)}), needs 3")
    for ln in p.lines():
        clean = ln.replace(MARK, "").replace("(가상 주소)", "")
        for n in lawyers:
            for m in re.finditer(re.escape(n), clean):
                if not marked(n).match(clean, m.start()):
                    fail(f"AC18 {s.slug}: '{n}' has no '가상' marker right after the name: {ln[:80]}")
    foot = [ln.replace(MARK, "").replace("(가상 주소)", "") for ln in p.footer_lines()]
    for ac, label in (("AC19", "대표변호사"), ("AC20", "광고책임변호사")):
        pat = re.compile(r"(?<!광고책임)" + label + r"\s*[:：]?\s*(" + "|".join(map(re.escape, lawyers)) + ")")
        hit = [(ln, m) for ln in foot for m in pat.finditer(ln)]
        if not any(marked(m.group(1)).match(ln, m.start(1)) for ln, m in hit):
            fail(f"{ac} {s.slug}: footer has no '{label} <fixed lawyer name> (가상 …)'")
        elif ac == "AC20" and not any(m.group(1) in listed for _, m in hit):
            fail(f"AC20 {s.slug}: the 광고책임변호사 {hit[0][1].group(1)} is not one of the lawyers listed in 구성원")
    reg = re.compile(r"(등록\s*번호|등록|허가\s*번호|신고\s*번호|인가\s*번호)[\s:(#는은]*(?:제\s*)?(?:No\.?\s*)?"
                     r"([0-9][0-9\- ]*)")
    for ln in p.lines() + [norm(" ".join(p.title))] + p.attr_text:  # per block, as AC29; full-width digits folded
        for m in reg.finditer(unicodedata.normalize("NFKC", ln)):
            if re.search(r"[1-9]", m.group(2)):
                fail(f"AC21 {s.slug}: {m.group(1)} with a digit other than 0: {m.group(0)}")


def check_ads(s):  # AC22-AC31 AC36, and A: AC92, C: AC105
    _, css, p = s.page()
    text = law_text(p, css)
    lists = dict(BANNED)
    ac, words = BANNED_SAMPLE[s.slug]
    lists[ac] = words
    for ac, words in lists.items():
        for word in words:
            for m in re.finditer(re.escape(word), text):
                fail(f"{ac} {s.slug}: page text contains '{word}': …{text[max(0, m.start() - 20):m.end() + 20]}…")
    for ln in p.lines() + [norm(" ".join(p.title))] + p.attr_text:
        m = re.search(r"\d\s?(?:만\s?)?원|₩\s?\d|\d\s?KRW", unicodedata.normalize("NFKC", ln))
        if m:
            fail(f"AC29 {s.slug}: a price (a digit then '원' or '만원', ₩ or KRW): {ln[:80]}")
    consult = norm(p.section(r"상담\s?안내") or "")
    if FEE not in consult:
        fail(f"AC30 {s.slug}: the 상담 안내 section lacks the sentence '{FEE}'")
    if OUTCOME not in text:
        fail(f"AC31 {s.slug}: the page lacks the sentence '{OUTCOME}'")
    for m in re.finditer(r"사무소", text):
        if text[max(0, m.start() - 1):m.start()] not in ("주", "분"):
            fail(f"AC36 {s.slug}: an office not labelled 주사무소 or 분사무소: …{text[max(0, m.start() - 20):m.end() + 10]}…")
    if "주사무소" not in norm(p.section(r"오시는\s?길") or ""):
        fail(f"AC36 {s.slug}: the 오시는 길 section does not label the office 주사무소")


def check_flow(s):  # AC37-AC41 AC45 AC46 AC47 (stylesheet) AC61 AC62 AC77
    _, css, p = s.page()
    if not re.search(r"word-break\s*:\s*keep-all", css):
        fail(f"AC47 {s.slug}: style.css has no word-break: keep-all")

    def first(pattern):
        hits = [off for lvl, t, off in p.headings if lvl >= 2 and re.search(pattern, t)]
        return min(hits) if hits else None
    order = [("주요 업무분야", r"주요\s?업무\s?분야"), ("구성원", r"구성원"), ("상담 안내", r"상담\s?안내"),
             ("오시는 길", r"오시는\s?길")]
    offs = [first(pat) for _, pat in order]
    if None in offs or offs != sorted(offs):
        fail(f"AC45 {s.slug}: h2-h6 headings 주요 업무분야 < 구성원 < 상담 안내 < 오시는 길 not found in that order "
             f"(offsets {dict(zip([n for n, _ in order], offs))})")
    consult = p.span(r"상담\s?안내")
    lines = p.lines(*consult) if consult else []
    pairs = [(lines[i - 1] if i else "") + " " + ln for i, ln in enumerate(lines)]  # a <dt>/<dd> pair counts
    if not any(re.search(HOURS, ln) and re.search(WEEKDAY, pr) for ln, pr in zip(lines, pairs)):
        fail(f"AC46 {s.slug}: the 상담 안내 section has no line with weekday 상담 시간 (평일 or 월–금 and HH:MM–HH:MM)")
    if not any(re.search(r"휴무|쉽니다", pr) and re.search(r"공휴일|일요일|주말", pr)
               and not re.search(r"휴무\s?없|에도|없이", pr) for pr in pairs):
        fail(f"AC77 {s.slug}: the 상담 안내 section has no closed-days line (휴무 or 쉽니다 with 일요일, 주말 or 공휴일)")
    for ac, word in (("AC37", "상담 예약"), ("AC38", "전화"), ("AC39", "카카오톡"), ("AC40", "네이버 지도")):
        hits = [c for c in p.controls if word in (c["name"] or "")]
        if not hits:
            fail(f"{ac} {s.slug}: no link or button whose accessible name contains '{word}'")
        for c in hits:
            if c["href"] != "#":
                fail(f"AC41 {s.slug}: '{c['name']}' has href={c['href']!r}, not '#'")
    for img in p.imgs:
        if not img.get("alt", "").strip():
            fail(f"AC61 {s.slug}: <img> without alt: {img.get('src')}")
    levels = [lvl for lvl, _, _ in sorted(p.headings, key=lambda h: h[2])]
    if levels.count(1) != 1:
        fail(f"AC62 {s.slug}: expected exactly one <h1>, found {levels.count(1)}")
    prev = 1
    for lvl in levels:
        if lvl > prev + 1:
            fail(f"AC62 {s.slug}: heading level skipped: h{prev} -> h{lvl}")
        prev = lvl


def check_assets(s):  # AC1 (page files) AC2 AC49 AC51 AC53 AC54 AC71 (reference names)
    html, css, p = s.page()
    for name in ("index.html", "style.css"):
        if not (s.site / name).is_file():
            fail(f"AC1 missing profile/{s.slug}/{name}")
    local = [v for k, v in p.refs if k != "srcset"] + [u for k, v in p.refs if k == "srcset" for u in srcset_urls(v)]
    local += css_urls(css)
    for ref in local:
        if ref.startswith(("http://", "https://", "data:", "#", "mailto:")):
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
                fail(f"AC49 {s.slug}: external stylesheet not allowed: {href}")
    for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", css):
        u = urlparse(imp)
        if u.netloc and not font_host(u):
            fail(f"AC49 {s.slug}: external @import not allowed: {imp}")
    for src in p.scripts:
        if src.startswith(("http", "//")):
            fail(f"AC49 {s.slug}: external script: {src}")
    for url in re.findall(r"https?://[^\s\"'()<>,]+", html + css):
        if url.startswith("http://www.w3.org/"):  # an XML namespace (inline SVG), not a load
            continue
        if urlparse(url).netloc not in ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net"):
            fail(f"AC51 {s.slug}: URL with a host that is not allowed: {url}")
    for pat in s.info["ref"]:
        if re.search(pat, unescape(html) + css, re.I):
            fail(f"AC71 {s.slug}: the sample names its reference site ({pat})")
    for ref in (r.removeprefix("./") for r in image_refs(p, css)):
        path = (s.site / ref.split("?")[0].split("#")[0]).resolve()
        if not path.is_file() or s.site.resolve() not in path.parents:
            fail(f"AC53 {s.slug}: image path does not resolve inside the sample folder: {ref}")
        if re.search(r"\.(jpe?g|png|webp|avif|gif)$", ref.split("?")[0], re.I) and not ref.startswith("img/"):
            fail(f"AC54 {s.slug}: photo not in img/: {ref}")


def count_items(heads, groups):  # AC91 AC103: item headings (h3-h6 of the section) that name a listed item
    return [h for h in heads if any(re.search(g, flat(h)) for g in groups)]


def check_sample(s):  # A: AC82-AC85 AC90 AC91  C: AC94-AC96 AC98 AC101-AC104 AC106 AC108 AC110 AC111
    _, css, p = s.page()
    raw, rgb = body_background(css)
    practice = p.span(r"주요\s?업무\s?분야")
    heads = [t for lvl, t, o in p.headings if lvl > 2 and practice and practice[0] < o < practice[1]]
    items = count_items(heads, s.info["vocab"])
    if s.slug == "law-ganeum":
        if not rgb:
            fail(f"AC82 law-ganeum: no readable body background colour in style.css ({raw!r})")
        elif max(rgb) > 0x33:
            fail(f"AC82 law-ganeum: body background {rgb} has a channel above 0x33")
        if fonts_loaded(s, "Cormorant Garamond"):
            fail("AC83 law-ganeum loads (or names) Cormorant Garamond")
        if fonts_loaded(s, "Noto Serif KR"):
            fail("AC84 law-ganeum loads (or names) Noto Serif KR")
        fam = h1_family(css)
        if fam not in A_H1_FACES:
            fail(f"AC85 law-ganeum: first h1 font family is {fam!r}, not one of {A_H1_FACES}")
        targets = set()
        for c in p.controls:
            if (c["in_header"] or c["in_section"]) and (c["href"] or "").startswith("#") and len(c["href"]) > 1:
                off = p.item_ids.get(c["href"][1:])
                if practice and off is not None and practice[0] < off < practice[1]:
                    targets.add(c["href"])
        if len(targets) < 3:
            fail(f"AC90 law-ganeum: the first <section> or <header> links to {len(targets)} elements inside "
                 f"주요 업무분야 ({sorted(targets)}), needs 3")
        if len(items) < 4:
            fail(f"AC91 law-ganeum: the 주요 업무분야 section has {len(items)} item headings naming a 송무 · 형사 item, needs 4")
    else:
        if not rgb:
            fail(f"AC94 AC95 law-goim: no readable body background colour in style.css ({raw!r})")
        else:
            if min(rgb) < 0xD8 or max(rgb) > 0xEA:
                fail(f"AC94 law-goim: body background {rgb} has a channel outside 0xD8-0xEA")
            if rgb[2] < rgb[0]:
                fail(f"AC95 law-goim: body background {rgb} has blue < red")
        for face in SHIPPED_FACES:
            if fonts_loaded(s, face):
                fail(f"AC96 law-goim loads (or names) {face}")
        fam = h1_family(css)
        if not fam:
            fail("AC108 law-goim: no top-level rule for h1 sets font-family or font")
        elif fam.lower() in ("pretendard", "pretendard variable"):
            fail(f"AC108 law-goim: first h1 font family is {fam!r}")
        wm = wordmark(p, s.info["stem"])
        if not wm:
            fail("AC98 AC110 law-goim: no wordmark (an <a> in the first <header> containing '고임')")
        else:
            if re.search(r"[A-Za-z]", wm["text"]):
                fail(f"AC98 law-goim: wordmark text has a Latin letter: {wm['text']!r}")
            if re.search(r"[A-Za-z]", wm["name"]):
                fail(f"AC110 law-goim: wordmark accessible name has a Latin letter: {wm['name']!r}")
        if any(i.get("type", "").lower() == "search" for i in p.inputs) or "search" in p.roles:
            fail("AC101 law-goim has a search field (input type=search or role=search)")
        if p.forms:
            fail(f"AC111 law-goim has {p.forms} <form> element(s)")
        for c in p.controls:
            if LANG.match(norm(c["text"])) or LANG.match(norm(c["label"])):
                fail(f"AC102 law-goim: language switcher control: {c['name']!r}")
        if len(items) < 4:
            fail(f"AC103 law-goim: the 주요 업무분야 section has {len(items)} item headings naming a 기업 자문 item, needs 4")
        consult = p.span(r"상담\s?안내")
        prep = None
        if consult:
            hs = sorted(p.headings, key=lambda h: h[2])
            for i, (lvl, txt, off) in enumerate(hs):
                if lvl >= 3 and consult[0] < off < consult[1] and re.search(r"상담\s?전\s?준비", txt):
                    prep = (off, next((o for l, _, o in hs[i + 1:] if l <= lvl), len(p.full())))
                    break
        n = sum(1 for o in p.li if prep and prep[0] < o < prep[1])
        if n < 3:
            fail(f"AC104 law-goim: no h3-h6 '상담 전 준비' inside 상담 안내 followed by at least 3 <li> ({n})")
        team = p.span(r"구성원")
        known = {g for g in s.info["vocab"] if any(re.search(g, flat(h)) for h in heads)}
        if team:
            body = p.full()[team[0]:team[1]]
            spots = sorted((m.start(), n) for n in s.info["lawyers"] for m in re.finditer(re.escape(n), body))
            firsts, seen = [], set()
            for pos, n in spots:
                if n not in seen:
                    seen.add(n)
                    firsts.append((pos, n))
            for i, (pos, n) in enumerate(firsts):
                card = body[pos:firsts[i + 1][0] if i + 1 < len(firsts) else len(body)]
                line = next((ln for ln in card.split("\n") if "주요취급분야" in ln), "")
                hit = [g for g in known if re.search(g, flat(line))] or \
                    [h for h in heads if flat(h) and flat(h) in flat(line)]
                if not hit:
                    fail(f"AC106 law-goim: {n}'s card has no 주요취급분야 line naming a 주요 업무분야 item "
                         f"({norm(line)[:60]!r})")


def check_register(s):  # AC1 (thumb.jpg) AC3 AC4 (size) AC81, and C: AC116
    e = entry(s.slug)
    if not e:
        n = sum(1 for p in load_profiles() if p.get("slug") == s.slug)
        fail(f"AC3 expected one PROFILES entry for {s.slug}, found {n}")
    elif (e.get("industry"), e.get("status"), e.get("demo")) != ("law", "live", True):
        fail(f"AC3 {s.slug}: entry fields wrong: industry={e.get('industry')} status={e.get('status')} "
             f"demo={e.get('demo')}")
    thumb = s.site / "thumb.jpg"
    if thumb.is_file():
        data = thumb.read_bytes()
        if data[:2] != b"\xff\xd8" or data.rstrip(b"\x00\r\n")[-2:] != b"\xff\xd9":
            fail(f"AC4 {s.slug}: thumb.jpg is not a complete JPEG (no FFD8 start or FFD9 end); re-run profile_thumb.py")
        w, h = sips_size(thumb)
        if w != 1200 or h is None or abs(h * 16 - w * 10) > 16:
            fail(f"AC4 {s.slug}: thumb.jpg is {w}x{h}, not 1200 wide at 16:10")
        if s.slug == "law-goim" and not sips_missing():
            try:
                y = mean_luma(thumb)
            except (subprocess.CalledProcessError, ValueError, struct.error) as exc:
                fail(f"AC116 law-goim: thumb.jpg could not be decoded: {type(exc).__name__}")
            else:
                if y < 100:
                    fail(f"AC116 law-goim: thumb.jpg mean luma {y:.1f} < 100")
    else:
        fail(f"AC1 AC4 {s.slug}: thumb.jpg missing")
    a = accent_of(e) if e else None
    css = read(s.site / "style.css") if (s.site / "style.css").is_file() else ""
    if not a or a not in css.lower():
        fail(f"AC81 {s.slug}: style.css does not contain the PROFILES accent {a}")


PER_SAMPLE = {"photos": check_photos, "markers": check_markers, "form": check_form, "ads": check_ads,
              "flow": check_flow, "assets": check_assets, "sample": check_sample, "register": check_register}
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
    seen = []
    for f in fails:
        if f not in seen:
            seen.append(f)
            print("FAIL", f)
    print(f"{'PASS' if not fails else 'FAIL'}: {' '.join(args)} ({len(seen)} failures)")
    sys.exit(1 if fails else 0)
