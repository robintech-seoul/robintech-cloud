#!/usr/bin/env python3
"""Static checks for the three hair-salon franchise profile samples (no browser, no network). Run from the repository
root.

usage: python3 docs/features/2026-11-19-profile-beauty/check_static.py <check> [<slug>]
  per sample (all three when <slug> is left out): photos markers franchise ads flow assets sample register
  shared: gallery current
  all: every check above, for every sample
slugs: beauty-robinhair (A) beauty-robinsalon (B) beauty-robinhairsalon (C)
Exit 0 when every named check passes; otherwise prints each failure and exits 1.
The page contract these checks read is the "Fixed parameters" section of tasks.md in this folder.
Adapted from docs/features/2026-11-18-profile-fitness/check_static.py; AC numbers are this feature's spec.md.
"""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import colorsys
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
FEATURE = Path(__file__).resolve().parent
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
NOT_RECRUITING = "가상의 가맹 안내이며 실제 가맹점을 모집하지 않습니다."  # AC42
SAMPLES = {
    "beauty-robinhair": {"key": "A", "ref": (r"spoke", r"weal", r"스포크")},
    "beauty-robinsalon": {"key": "B", "ref": (r"박승철", r"pschair", r"park\s*seung", r"\bstage\b")},
    "beauty-robinhairsalon": {"key": "C", "ref": (r"the\s*lane", r"thelane", r"더\s*레인")},
}
BANNED = {  # plain substrings of the whitespace-collapsed page text (tasks.md Fixed parameters, "Page text")
    "AC43": ("수익률", "순수익", "순이익", "월매출", "연매출", "매출액", "예상 매출", "예상매출", "예상 수익", "예상수익",
             "투자금 회수", "원금", "손익분기", "대박", "소자본"),
    "AC46": ("최고", "최초", "최대", "최다", "유일", "독보적", "1위", "1등", "넘버원", "업계 선두", "완벽", "보장",
             "보증", "무조건"),
    "AC47": ("수상", "어워드", "선정", "100대", "공식 인증", "인증 받은"),
    "AC48": ("후기", "리뷰", "별점", "평점", "만족도", "★", "성공 사례", "성공사례", "점주 인터뷰", "고객 인터뷰"),
    "AC50": ("치료", "완치", "탈모 개선", "탈모개선", "탈모 예방", "탈모예방", "발모", "육모", "모발 재생", "모발재생",
             "두피 재생", "처방", "의학", "메디컬", "피부과", "효능", "효과", "탈모", "진단", "염증"),
    "AC51": ("무료", "공짜", "할인", "이벤트", "선착순", "마감 임박", "프로모션", "쿠폰"),
    "AC52": ("가맹점사업자피해보상보험", "피해보상보험", "공제조합 가입", "지급보증", "공제계약", "가맹금 예치"),
    "AC53": ("특허", "상표등록", "상표 등록", "®", "™", "저작권 등록", "공정거래위원회", "공정위", "등록 완료"),
    "AC54": ("원장님", "대표 원장", "대표원장", "수석 디자이너", "스타 디자이너", "경력", "년차", "년 차"),
    "AC160": ("천연", "유기농", "무독성", "무자극", "저자극", "무암모니아", "암모니아 없", "무손상", "손상 없", "친환경",
              "무첨가"),
}
BANNED_CI = {"AC46": ("No.1",), "AC47": ("Award",),  # case-insensitive
             "AC49": ("비포", "애프터", "before", "after", "전후 사진", "시술 전후"),
             "AC161": ("K18", "올라플렉스", "Olaplex", "밀본", "Milbon", "로레알", "L'Oreal", "L'Oréal", "웰라", "Wella",
                       "아베다", "Aveda", "다이슨", "Dyson", "케라스타즈", "Kerastase", "Kérastase", "슈바르츠코프",
                       "Schwarzkopf", "아모스", "미쟝센")}
ALT_BANNED = ("디자이너", "원장", "스타일리스트", "직원", "점주", "대표 원장", "대표원장", "우리 팀", "미용사", "실장")  # AC159
EMAIL = re.compile(r"[\w.+-]+@((?:[\w-]+\.)+[A-Za-z]{2,})")  # AC59: only @example.com
CLOSED = r"휴무|휴관|쉽니다|쉬어요|쉬는 날|쉼"  # AC40
CLOSED_DAY = r"공휴일|일요일|주말|토요일|월요일|화요일|수요일|목요일|금요일"
HOURS = r"\d{1,2}:\d{2}\s*[-–—~～〜]\s*\d{1,2}:\d{2}"
WEEKDAY = r"평일|월요일?\s*[-–—~～〜]\s*금요일?|월\s*[-–—~～〜·]\s*금|화요일?\s*[-–—~～〜]\s*금요일?|화\s*[-–—~～〜·]\s*금"
BRANCH = re.compile(r"(?:^|\s)([가-힣]{1,8})점$")  # AC23: the last word of a branch heading, a place name then 점
CONTROL_WORDS = ("네이버 예약", "카카오톡", "전화", "네이버 지도")  # AC26-AC29 AC32
BLOCK = {"p", "li", "dd", "dt", "td", "th", "address", "div", "section", "article", "header", "footer", "ul", "ol",
         "h1", "h2", "h3", "h4", "h5", "h6", "button", "nav", "main", "aside", "figure", "figcaption", "tr", "table",
         "dl", "details", "summary"}
CAPTURE = ("display-word",)  # class names whose element text the parser keeps (AC121)
A_BANNED_FACES = ("Instrument Serif", "Inter", "Noto Serif KR", "Cormorant Garamond", "Hahmlet", "Gowun Batang")
A_BANNED_HEX = ("#faf7f2", "#0a0a0a", "#f2ede3", "#c2a176", "#83643a")  # AC110
B_BANNED_HEX = ("#635595", "#5f518e", "#686199")  # AC136
C_BANNED_HEX = ("#5d564b", "#837e73", "#f4f3f2", "#754e36")  # AC151
fails = []


def fail(msg):
    fails.append(msg)


def read(path):
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
        return ""
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        fail(f"not UTF-8: {path.relative_to(ROOT)} ({exc.reason} at byte {exc.start})")
        return ""


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


class Page(HTMLParser):
    """Collects text (with block breaks), headings, controls, articles, ids, images, refs, header, nav and footer."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []            # visible text chunks; "\n" at block boundaries
        self.headings = []        # (level, text, offset, innermost open <section> as [id, start, end] or None)
        self.controls = []        # dict(tag, href, label, text, name, offset, in_header, in_nav, cls)
        self.articles = []        # (id, start offset, end offset)
        self.ids = {}             # id -> text offset of its start tag
        self.captured = []        # (class, text, offset) for elements whose class is in CAPTURE
        self.imgs = []            # (attrs, offset)
        self.img_refs = []        # src/srcset of <img> and <source>, poster of <video> (AC65)
        self.refs, self.links, self.scripts, self.metas = [], [], [], []
        self.forms, self.fields = 0, []
        self.title, self.attr_text = [], []
        self.footer_span = None   # (start, end) of the last <footer> outside every <article>
        self._footers = []        # stack of [start, inside an <article>]
        self._stack = []
        self._skip = 0
        self._header = None       # None before the first <header>, then depth, then "done"
        self._nav = 0             # depth of <nav> inside the first <header>
        self._sections = []       # stack of open <section> elements as [id ("" when none), start, end]
        self._articles = []       # stack of [id, start]
        self._cap = []            # stack of [class, buf, offset, depth-tag]

    def _offset(self):
        return sum(len(t) for t in self.text)

    def _track(self, attr, tag, want, start):
        state = getattr(self, attr)
        if tag != want:
            return None
        if start:
            if state is None:
                setattr(self, attr, 1)
                return "open"
            if isinstance(state, int):
                setattr(self, attr, state + 1)
        elif isinstance(state, int):
            setattr(self, attr, state - 1 if state > 1 else "done")
            return "close" if state == 1 else None
        return None

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
        if tag == "footer":
            self._footers.append([self._offset(), bool(self._articles)])
        if tag == "nav" and isinstance(self._header, int):
            self._nav += 1
        if tag == "section":
            self._sections.append([a.get("id", ""), self._offset(), None])
        if tag == "article":
            self._articles.append([a.get("id", ""), self._offset()])
        if a.get("id"):
            self.ids.setdefault(a["id"], self._offset())
        if tag == "form":
            self.forms += 1
        if tag in ("input", "select", "textarea"):
            self.fields.append(tag)
        if tag in BLOCK:
            self.text.append("\n")
        elif tag in ("br", "a"):
            self.text.append(" ")
        for k in ("src", "srcset", "href", "poster"):
            if k in a:
                self.refs.append((k, a[k]))
                if (tag in ("img", "source") and k in ("src", "srcset")) or (tag == "video" and k == "poster"):
                    self.img_refs.append((k, a[k]))
        classes = a.get("class", "").split()
        for c in CAPTURE:
            if c in classes:
                self._cap.append([c, [], self._offset(), tag])
        if tag == "img":
            self.imgs.append((a, self._offset()))
            self._add(a.get("alt", ""))
        elif tag == "link":
            self.links.append(a)
        elif tag == "meta":
            self.metas.append(a)
        if tag in ("a", "button", "summary"):
            self._stack.append({"kind": "control", "tag": tag, "href": a.get("href"), "label": a.get("aria-label"),
                                "cls": classes, "buf": [], "offset": self._offset(),
                                "in_header": isinstance(self._header, int), "in_nav": self._nav > 0})
        elif re.fullmatch(r"h[1-6]", tag):
            self._stack.append({"kind": "heading", "level": int(tag[1]), "buf": [], "offset": self._offset(),
                                "section": self._sections[-1] if self._sections else None})

    def handle_endtag(self, tag):
        if tag in ("script", "style", "template", "title"):
            self._skip = max(0, self._skip - 1)
        if tag in BLOCK:
            self.text.append("\n")
        elif tag in ("br", "a"):
            self.text.append(" ")
        self._track("_header", tag, "header", False)
        if tag == "footer" and self._footers:
            start, in_article = self._footers.pop()
            if not in_article:
                self.footer_span = (start, self._offset())
        if tag == "nav" and self._nav:
            self._nav -= 1
        if tag == "section" and self._sections:
            self._sections.pop()[2] = self._offset()
        if tag == "article" and self._articles:
            aid, start = self._articles.pop()
            self.articles.append((aid, start, self._offset()))
        for i in range(len(self._cap) - 1, -1, -1):
            if self._cap[i][3] == tag:
                c, buf, off, _ = self._cap.pop(i)
                self.captured.append((c, norm("".join(buf)), off))
                break
        kind = "control" if tag in ("a", "button", "summary") else "heading" if re.fullmatch(r"h[1-6]", tag) else None
        if not kind:
            return
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i]["kind"] == kind:
                item = self._stack.pop(i)
                txt = norm("".join(item["buf"]))
                if kind == "control":
                    label = item["label"] or ""
                    self.controls.append({"tag": item["tag"], "href": item["href"], "label": label, "text": txt,
                                          "name": label if label else txt, "offset": item["offset"],
                                          "in_header": item["in_header"], "in_nav": item["in_nav"],
                                          "cls": item["cls"]})
                else:
                    self.headings.append((item["level"], txt, item["offset"], item["section"]))
                break

    def _add(self, data):
        self.text.append(data)
        for item in self._stack:
            item["buf"].append(data)
        for cap in self._cap:
            cap[1].append(data)

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
        if not self.footer_span or self.footer_span[1] is None:
            return []
        return self.lines(self.footer_span[0], self.footer_span[1])

    def heading(self, pattern, min_level=2):
        """The first heading of level >= min_level whose text matches pattern, with its span (start, end) up to the
        next heading of the same or a higher level or the end of its innermost <section>, whichever comes first.
        "section" is the id of that <section> ("" or None when it has none)."""
        hs = sorted(self.headings, key=lambda h: h[2])
        for i, (lvl, txt, off, sec) in enumerate(hs):
            if lvl >= min_level and re.search(pattern, txt):
                end = next((o for l, _, o, _ in hs[i + 1:] if l <= lvl), len(self.full()))
                if sec and sec[2] is not None:
                    end = min(end, sec[2])
                return {"level": lvl, "text": txt, "start": off, "end": end, "section": sec[0] if sec else None,
                        "in_section": sec is not None}
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
            p.close()
            self._page = (html, read(self.site / "style.css"), p)
        return self._page

    def image_files(self):
        return sorted(f for f in self.img.iterdir() if f.is_file() and f.name != "sources.txt"
                      and not f.name.startswith(".")) if self.img.is_dir() else []

    def source_lines(self):
        if not self.sources.is_file():
            fail(f"AC70 {self.slug}: img/sources.txt missing")
            return []
        return [ln.split() for ln in read(self.sources).splitlines() if ln.strip()]


def inline_css(html):  # the CSS inside <style> elements and style="" attributes of index.html
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)
                     + [unescape(v) for v in re.findall(r"\sstyle\s*=\s*\"([^\"]*)\"", html, re.I)]
                     + [unescape(v) for v in re.findall(r"\sstyle\s*=\s*'([^']*)'", html, re.I)])


def uncomment(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def css_urls(css):
    out = [u.strip("'\" ") for u in re.findall(r"url\(([^)]*)\)", uncomment(css))]
    out += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", css)
    return out


def srcset_urls(v):
    return [part.strip().split()[0] for part in v.split(",") if part.strip()]


def image_refs(p, css):
    refs = []
    for k, v in p.img_refs:
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


def mean_luma(path):  # AC101 AC153: ITU-R 601 luma over all pixels, decoded by sips to an uncompressed 24/32-bit BMP
    with tempfile.TemporaryDirectory() as tmp:
        bmp = Path(tmp) / "t.bmp"
        subprocess.run(["sips", "-s", "format", "bmp", str(path), "--out", str(bmp)], capture_output=True, check=True)
        d = bmp.read_bytes()  # OSError when sips wrote nothing
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
    try:
        from profiles import PROFILES  # noqa: E402
    except Exception as exc:  # a broken profiles.py is a failure, not a traceback
        fail(f"AC3 scripts/profiles.py does not import: {type(exc).__name__}: {exc}")
        return []
    return PROFILES


def entry(slug):
    hits = [p for p in load_profiles() if p.get("slug") == slug]
    return hits[0] if len(hits) == 1 else None


def accent_of(e):
    return str((e.get("palette") or [""])[-1]).lower()


def hsl(hexv):
    r, g, b = (int(hexv[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s, l


def hsl_rgb(rgb):
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in rgb))
    return h * 360, s, l


def css_content(css):  # strings in CSS content: declarations, read with the page text
    return [m[1] for m in re.findall(r"content\s*:\s*([\"'])(.*?)\1", uncomment(css))]


def page_text(p, css=""):  # visible text, <title>, meta description/og: content, aria-label, alt, title, CSS content:
    return norm(" ".join([p.full(), *p.title, *p.attr_text, *css_content(css)]))


def blocks(p, css=""):  # the same text, one entry per block (AC21 AC44 AC45)
    return p.lines() + [norm(" ".join(p.title))] + [norm(t) for t in p.attr_text] + css_content(css)


def script_strings(html):  # inline <script> string literals holding Hangul or markup, tags stripped: page text a script may add
    out = []
    for body in re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S | re.I):
        for m in re.finditer(r"\"((?:[^\"\\\n]|\\.)*)\"|'((?:[^'\\\n]|\\.)*)'|`((?:[^`\\]|\\.)*)`", body):
            t = next(g for g in m.groups() if g is not None)
            if re.search(r"[가-힣<@₩￦\s]", t) and t not in ("beforebegin", "afterbegin", "beforeend", "afterend"):
                out.append(norm(unescape(re.sub(r"<[^>]+>", " ", t))))
    return [t for t in out if t]


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


def body_decl(css, names):  # the last of the named declarations in a top-level `body` rule, var() resolved
    rules, val = top_rules(css), None
    props = custom_props(rules)
    for sel, body in rules:
        if any(x.strip() == "body" for x in sel.split(",")):
            for k, v in decls(body):
                if k in names:
                    val = v
    return val, parse_color(resolve(val, props)) if val else None


def css_families(css, html=""):
    """Every font-family value, and the family part of every font shorthand, at any nesting (@media included) in
    style.css and in <style> and style="" of index.html, var() resolved from :root or html."""
    props = custom_props(top_rules(css))
    text = uncomment(css + "\n" + inline_css(html))
    out = [resolve(v.strip(), props) for v in re.findall(r"(?<![\w-])font-family\s*:\s*((?:[^;}\"]|\"[^\"]*\")+)", text)]
    for v in re.findall(r"(?<![\w-])font\s*:\s*([^;}]+)", text):
        m = re.search(r"\d[\w.%]*(?:\s*/\s*[\w.%]+)?\s+(.+)$", resolve(v.strip(), props))
        if m:
            out.append(m.group(1))
    return out


def loaded_families(html, css):  # families requested from Google Fonts (link or @import) and from font stacks
    fams = []
    for u in re.findall(r"https?://fonts\.googleapis\.com/css2?\?[^\"'\s)]+", unescape(html) + css):
        for fam in parse_qs(urlparse(u).query).get("family", []):
            fams.append(fam.split(":")[0].replace("+", " "))
    for stack in css_families(css, html):
        fams += [f.strip().strip("'\"") for f in stack.split(",")]
    return fams


def rgb_of(hexv):
    return tuple(int(hexv[i:i + 2], 16) for i in (1, 3, 5))


def achromatic(hexv):  # AC75: largest RGB channel minus the smallest is at most 0x18
    c = rgb_of(hexv)
    return max(c) - min(c) <= 0x18


def families_lower(html, css):  # exact family tokens (tasks.md Fixed parameters, "Faces")
    return {f.strip().strip("'\"").lower() for f in loaded_families(html, css) if f.strip()}


def ital_families(html):  # Google Fonts families whose family= value requests ital (AC107)
    out = set()
    for u in re.findall(r"https?://fonts\.googleapis\.com/css2?\?[^\"'\s)]+", unescape(html)):
        for fam in parse_qs(urlparse(u).query).get("family", []):
            name, _, axes = fam.partition(":")
            if "ital" in axes:
                out.add(name.replace("+", " ").strip().lower())
    return out


def flat_rules(css):  # (selector, body) of every innermost rule, at any nesting (@media included)
    return [(sel.strip().split(";")[-1].strip(), body)
            for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", uncomment(css))]


def h1_em_texts(html):  # AC106: the text of every <em> inside the <h1>
    out = []
    for h1 in re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.S | re.I):
        for em in re.findall(r"<em\b[^>]*>(.*?)</em>", h1, re.S | re.I):
            out.append(norm(unescape(re.sub(r"<[^>]+>", "", em))))
    return out


# --- branch and section helpers ---------------------------------------------------------------------------

def branch_section(p):  # AC22: the 지점 찾기 / 매장 찾기 heading and its span
    return p.heading(r"(지점|매장)\s?찾기")


def franchise_section(p):  # AC24: the 가맹 문의 / 가맹 안내 heading and its span
    return p.heading(r"가맹\s?(문의|안내)")


def branches(p):
    """Branch entries: <article id> elements inside the 지점 찾기 section whose first h3-h6 heading ends in a
    place name followed by 점. Returns [(id, start, end, name)]."""
    sec = branch_section(p)
    if not sec:
        return []
    out = []
    for aid, start, end in sorted(p.articles, key=lambda a: a[1]):
        if not (sec["start"] < start < sec["end"]):
            continue
        hs = sorted((h for h in p.headings if h[0] >= 3 and start <= h[2] < end), key=lambda h: h[2])
        m = BRANCH.search(hs[0][1]) if hs else None
        if m and m.group(1) not in ("지", "본", "매"):
            out.append((aid, start, end, m.group(0).strip()))
    return out


def stray_articles(p, entries):  # <article> elements in the 지점 찾기 section that branches() did not take
    sec = branch_section(p)
    if not sec:
        return []
    taken = {e[1] for e in entries}
    inner = [(a, st, en) for a, st, en in p.articles if sec["start"] < st < sec["end"]]
    return [(a, st) for a, st, en in inner if st not in taken
            and not any(t < st < e for _, t, e in inner if t in taken)]  # an article nested in a branch entry is part of it


def controls_in(p, start, end):
    return [c for c in p.controls if start <= c["offset"] < end]


def wordmark(p):  # the <a class="wordmark"> in the first <header>
    return next((c for c in p.controls if c["in_header"] and c["tag"] == "a" and "wordmark" in c["cls"]), None)


def nav_hangul_only(p, ac, slug):  # AC131 AC141
    nav = [c for c in p.controls if c["in_nav"] and c["tag"] == "a"]
    if not nav:
        fail(f"{ac} {slug}: no <a> inside a <nav> in the first <header>")
    for c in nav:
        if not re.search(r"[가-힣]", c["text"]) or re.search(r"[A-Za-z]", c["text"]):
            fail(f"{ac} {slug}: header nav link text is not Hangul-only: {c['text']!r}")


def wordmark_no_latin(p, ac, slug):  # AC116 AC134 AC149
    wm = wordmark(p)
    if not wm:
        fail(f'{ac} {slug}: no <a class="wordmark"> in the first <header>')
    elif re.search(r"[A-Za-z]", wm["name"]):
        fail(f"{ac} {slug}: the wordmark's accessible name {wm['name']!r} has a Latin letter")


def banned_hex(css, hexes, ac, slug):
    for hexv in hexes:
        if hexv in css.lower():
            fail(f"{ac} {slug}: style.css contains {hexv}")


def banned_faces(html, css, faces, ac, slug):
    have = families_lower(html, css)
    for face in faces:
        if face.lower() in have:
            fail(f"{ac} {slug} loads or names the family {face}")


# --- shared checks ---------------------------------------------------------------------------------------

def check_gallery():  # AC3 (no other beauty entry) AC17 AC75 AC76 AC91 AC157, and the generated part of AC89 AC90
    gallery = read(ROOT / "profile/index.html")
    if not re.search(rf'data-filter="beauty"[^>]*>[^<]*<sup>{len(SAMPLES)}</sup>', gallery):
        fail(f"AC91 profile/index.html: the beauty filter chip does not show the count {len(SAMPLES)} "
             f"(run python3 scripts/build.py)")
    for slug in SAMPLES:
        if f'data-slug="{slug}"' not in gallery:
            fail(f"AC89 profile/index.html has no card for {slug}")
    if re.search(r'class="pf-card pf-empty[^"]*" data-industry="beauty"', gallery):
        fail("AC90 profile/index.html still has the beauty 준비 중 tile")
    profiles = load_profiles()
    others = [p.get("slug") for p in profiles if p.get("industry") == "beauty" and p.get("slug") not in SAMPLES]
    if others:
        fail(f"AC3 PROFILES has beauty entries for other slugs: {others}")
    names = [entry(slug).get("name") for slug in SAMPLES if entry(slug)]
    if len(set(names)) != len(names):
        fail(f"AC17 two beauty samples share a PROFILES name: {names}")
    seen = {}
    for slug in SAMPLES:
        e = entry(slug)
        for hexv in (str(h).lower() for h in ((e or {}).get("palette") or [])):
            if hexv in seen and seen[hexv] != slug:
                fail(f"AC157 {hexv} is in the palette of both {seen[hexv]} and {slug}")
            seen.setdefault(hexv, slug)
    for slug in SAMPLES:
        e = entry(slug)
        a = accent_of(e) if e else ""
        if not re.fullmatch(r"#[0-9a-f]{6}", a):
            fail(f"AC75 {slug}: last palette entry is not a 6-digit hex: {a!r}")
            continue
        if achromatic(a):
            continue  # AC76: an achromatic accent is exempt and is not compared with any hue
        hue, sat, _ = hsl(a)
        if sat < 0.25:
            fail(f"AC75 {slug}: accent {a} is chromatic (channel spread above 0x18) with HSL saturation "
                 f"{sat:.2f} < 0.25")
        for other in profiles:
            if other.get("slug") == slug:
                continue
            b = accent_of(other)
            if not re.fullmatch(r"#[0-9a-f]{6}", b):
                fail(f"AC76 {other.get('slug')}: accent {b!r} is not a 6-digit hex")
                continue
            if achromatic(b):
                continue
            d = abs(hue - hsl(b)[0]) % 360
            d = min(d, 360 - d)
            if d < 25:
                fail(f"AC76 {slug}: accent {a} ({hue:.0f}°) is {d:.0f}° from {other.get('slug')} {b} "
                     f"({hsl(b)[0]:.0f}°), needs 25°")


def check_current():  # AC95
    comp = read(ROOT / "docs/current_system/profile-samples/component.md")
    src = next((ln for ln in comp.splitlines() if ln.startswith("**Source:**")), "")
    listed = set(re.findall(r"`([a-z0-9-]+)`", src))
    for slug in SAMPLES:
        if slug not in listed:
            fail(f"AC95 the Source line of profile-samples/component.md does not list `{slug}`")


# --- per-sample checks -----------------------------------------------------------------------------------

def check_photos(s):  # AC64 AC66-AC71
    files = s.image_files()
    if not files:
        fail(f"AC66 {s.slug}: img/ has no image files")
    for d in (f for f in s.img.rglob("*") if f.is_dir()) if s.img.is_dir() else []:
        fail(f"AC66 {s.slug}: img/ holds a folder, whose files no photo check reads: {d.relative_to(s.site)}")
    total = 0
    for f in files:
        if f.suffix.lower() not in (".jpg", ".webp"):
            fail(f"AC66 {s.slug}: not .jpg/.webp: img/{f.name}")
        size = f.stat().st_size
        total += size
        if size > 500 * 1024:
            fail(f"AC68 {s.slug}: larger than 500 KB: img/{f.name} ({size // 1024} KB)")
        w, _ = sips_size(f)
        if w is None or w > 2000:
            fail(f"AC67 {s.slug}: wider than 2000 px or unreadable: img/{f.name} ({w})")
    if total > 3 * 1024 * 1024:
        fail(f"AC69 {s.slug}: img/ totals {total / 1024 / 1024:.2f} MB > 3 MB")
    lines = s.source_lines()
    names = [ln[0] for ln in lines if ln]
    for ln in lines:
        if len(ln) != 3:
            fail(f"AC70 {s.slug}: sources.txt line is not '<file> <page URL> <download URL>': {' '.join(ln)}")
            continue
        _, page_url, dl = ln
        if page_url != "-" and not page_url.startswith(("https://unsplash.com/photos/", "https://www.pexels.com/photo/")):
            fail(f"AC70 {s.slug}: page URL is not an Unsplash/Pexels photo page or '-': {page_url}")
        if not dl.startswith(("https://images.unsplash.com/photo-", "https://images.pexels.com/photos/")):
            fail(f"AC71 {s.slug}: download URL not allowed: {dl}")
    if sorted(names) != [f.name for f in files] or len(set(names)) != len(names):
        fail(f"AC70 {s.slug}: sources.txt files {sorted(names)} != img/ files {[f.name for f in files]}")
    raw = read(s.sources) if s.sources.is_file() else ""
    if "plus.unsplash.com" in raw or "premium_photo" in raw:
        fail(f"AC71 {s.slug}: sources.txt mentions plus.unsplash.com or premium_photo")
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
            fail(f"AC64 {s.slug}: photo {pid} is also recorded in {taken[pid]}")


def check_markers(s):  # AC8 (text; visibility in check_browser.py) AC10-AC14 AC16 AC18-AC21
    _, css, p = s.page()
    if MARK not in norm(p.full()):
        fail(f"AC8 {s.slug}: page text lacks '{MARK}'")
    if "디자인 샘플" not in norm(" ".join(p.title)):
        fail(f"AC14 {s.slug}: <title> lacks '디자인 샘플'")
    foot = " ".join(p.footer_lines())
    if not p.footer_span:
        fail(f"AC10 AC11 {s.slug}: no <footer>")
    if MARK not in foot:
        fail(f"AC10 {s.slug}: footer lacks '{MARK}'")
    if "Website by RobinTech" not in foot:
        fail(f"AC11 {s.slug}: footer lacks 'Website by RobinTech'")
    credit = foot.split("Photos:", 1)[1] if "Photos:" in foot else ""
    raw = read(s.sources) if s.sources.is_file() else ""
    if not credit:
        fail(f"AC12 {s.slug}: footer has no 'Photos:' credit")
    for host, name in (("images.unsplash.com", "Unsplash"), ("images.pexels.com", "Pexels")):
        if host in raw and name not in credit:
            fail(f"AC12 {s.slug}: a {name} photo is used but the footer's 'Photos:' credit does not name {name}")
    if not any(m.get("name") == "robots" and m.get("content") == "noindex" for m in p.metas):
        fail(f'AC13 {s.slug}: no <meta name="robots" content="noindex">')
    wm = wordmark(p)
    if not wm:
        fail(f'AC16 {s.slug}: no <a class="wordmark"> in the first <header>')
    elif not wm["name"].startswith("로빈"):
        fail(f"AC16 {s.slug}: the wordmark's accessible name {wm['name']!r} does not start with 로빈")
    addr = re.compile(r"[가-힣0-9]*[가-힣0-9](?<!으)(?:로|길)\s?\d+(?:-\d+)?"
                      r"(?![\d%A-Za-z가-힣~:.-]|,\d|\s?(?:원|분|시|개|인|일|명|번|미터|층|m(?![A-Za-z])))"
                      r"|[가-힣]+동\d*가\s?\d+|\d+(?:-\d+)?\s?번지")  # road-name, 동N가 and 번지 addresses
    lines = p.lines()
    if not any("(가상 주소)" in ln for ln in lines):
        fail(f"AC18 {s.slug}: no address with '(가상 주소)' on the page")
    for ln in lines:
        if addr.search(ln) and "(가상 주소)" not in ln:
            fail(f"AC18 {s.slug}: address without '(가상 주소)': {ln[:80]}")
    text = p.full() + "\n" + " ".join(v for _, v in p.refs) + "\n" + " ".join(p.attr_text)
    phones = re.findall(r"(?<![\d-])(?:0\d{1,2}[-.\s]\d{3,4}|1[5-9]\d{2})[-.\s]\d{4}(?![\d-])", text)
    if "02-000-0000" not in phones:
        fail(f"AC19 {s.slug}: no phone number 02-000-0000 on the page")
    phones += re.findall(r"\(0\d{1,2}\)\s?\d{3,4}[-.\s]\d{4}|\+82[\d\s().-]{7,}", text)
    for ph in phones:
        if ph != "02-000-0000":
            fail(f"AC19 {s.slug}: phone number is not 02-000-0000: {ph}")
    for k, v in p.refs:
        if v.lower().startswith("tel:") and re.sub(r"\D", "", v) != "0200000000":
            fail(f"AC19 {s.slug}: tel: link is not 02-000-0000: {v}")
    brns = re.findall(r"(?<![\d-])\d{3}[-.\s]\d{2}[-.\s]\d{5}(?![\d-])", text)
    if "사업자등록번호" in text and not brns:
        fail(f"AC20 {s.slug}: '사업자등록번호' without a number 000-00-00000")
    for brn in brns:
        if brn != "000-00-00000":
            fail(f"AC20 {s.slug}: business registration number is not 000-00-00000: {brn}")
    reg = re.compile(r"(등록\s*번호|등록|허가\s*번호|신고\s*번호|인가\s*번호)[\s:(\[#는은\-–—]*(?:제\s*)?(?:No\.?\s*)?"
                     r"([0-9][0-9\-]*)")
    for ln in blocks(p, css):  # per block; full-width digits folded
        for m in reg.finditer(unicodedata.normalize("NFKC", ln)):
            if re.search(r"[1-9]", m.group(2)):
                fail(f"AC21 {s.slug}: {m.group(1)} with a digit other than 0: {m.group(0)}")
        for m in re.finditer(r"제\s*([0-9][0-9\-]*)\s*호", unicodedata.normalize("NFKC", ln)):
            if re.search(r"[1-9]", m.group(1)):
                fail(f"AC21 {s.slug}: a 제…호 number with a digit other than 0: {m.group(0)}")


def check_franchise(s):  # AC22-AC32 AC39 AC40 AC42
    _, _, p = s.page()
    bsec, fsec = branch_section(p), franchise_section(p)
    if not bsec:
        fail(f"AC22 {s.slug}: no h2-h6 heading containing '지점 찾기' or '매장 찾기'")
    if not fsec:
        fail(f"AC24 {s.slug}: no h2-h6 heading containing '가맹 문의' or '가맹 안내'")
    if bsec and fsec and not bsec["start"] < fsec["start"]:
        fail(f"AC25 {s.slug}: the 지점 찾기 section does not come before the 가맹 section")
    if bsec and not bsec["section"]:
        fail(f"AC22 {s.slug}: the 지점 찾기 heading is not directly inside a <section id> (the link target)")
    if fsec and not fsec["in_section"]:
        fail(f"AC24 {s.slug}: the 가맹 heading is not inside a <section> (its span ends with that section)")
    entries = branches(p)
    for aid, start in stray_articles(p, entries):
        fail(f"AC23 {s.slug}: an <article> in the 지점 찾기 section (id={aid!r}) is not a branch entry: its first "
             f"h3-h6 does not end in '<place>점', so its controls, address and hours are not checked")
    if len(entries) < 3:
        fail(f"AC23 {s.slug}: the 지점 찾기 section has {len(entries)} branch entries (<article id> with an h3-h6 "
             f"ending '<place>점'), needs 3")
    for aid, start, end, name in entries:
        if not aid:
            fail(f"AC23 {s.slug}: branch entry {name} has no id")
        ctl = controls_in(p, start, end)
        for ac, word in zip(("AC26", "AC27", "AC28", "AC29"), CONTROL_WORDS):
            if not any(word in c["name"] and c["tag"] == "a" for c in ctl):
                fail(f"{ac} {s.slug}: branch {name} has no link whose accessible name contains '{word}'")
        for c in ctl:
            if c["tag"] == "a" and sum(w in c["name"] for w in CONTROL_WORDS) > 1:
                fail(f"AC26 {s.slug}: branch {name}: one link names several of {CONTROL_WORDS}: '{c['name']}'")
            if any(w in c["name"] for w in CONTROL_WORDS) and c["href"] != "#":
                fail(f"AC32 {s.slug}: branch {name}: '{c['name']}' ({c['tag']}) has href={c['href']!r}, not '#'")
        lines = p.lines(start, end)
        if not any("(가상 주소)" in ln for ln in lines):
            fail(f"AC30 {s.slug}: branch {name} shows no address with '(가상 주소)'")
        if not any("02-000-0000" in ln for ln in lines):
            fail(f"AC30 {s.slug}: branch {name} does not show 02-000-0000")
        pairs = [(lines[i - 1] if i else "") + " " + ln for i, ln in enumerate(lines)]  # a <dt>/<dd> pair counts
        labels = [lines[i - 1] if i and len(lines[i - 1]) <= 12 and not re.search(r"\d:\d", lines[i - 1]) else ""
                  for i in range(len(lines))]  # a short label block before this one (<dt>, <th>)
        if not any(re.search(HOURS, ln) and re.search(WEEKDAY, pr) for ln, pr in zip(lines, pairs)):
            fail(f"AC39 {s.slug}: branch {name} has no weekday hours line (평일, 월–금 or 화–금 and HH:MM–HH:MM)")

        def closed(ln, lb):
            hit = (re.search(CLOSED, ln) and re.search(CLOSED_DAY, ln)) or (re.search(CLOSED, lb) and re.search(
                CLOSED_DAY, ln)) or (re.search(CLOSED_DAY, lb) and re.search(CLOSED, ln))
            return hit and not re.search(r"휴무일?\s*:?\s*없|에도|없이|문의", lb + " " + ln)
        if not any(closed(ln, lb) for ln, lb in zip(lines, labels)):
            fail(f"AC40 {s.slug}: branch {name} has no closed-days line ({CLOSED} with a day, in one block or "
                 f"split over a label of at most 12 characters and the next block)")
    if fsec:
        ctl = controls_in(p, fsec["start"], fsec["end"])
        if not any("가맹" in c["name"] and c["tag"] == "a" for c in ctl):
            fail(f"AC31 {s.slug}: the 가맹 section has no link whose accessible name contains '가맹'")
        for c in ctl:
            if ("가맹" in c["name"] and c["href"] != "#") or (c["tag"] == "a" and not (c["href"] or "").startswith("#")):
                fail(f"AC32 {s.slug}: 가맹 section: '{c['name']}' ({c['tag']}) has href={c['href']!r}, not '#'")
        if NOT_RECRUITING not in norm(p.full()[fsec["start"]:fsec["end"]]):
            fail(f"AC42 {s.slug}: the 가맹 section lacks the sentence '{NOT_RECRUITING}'")


def fold(t):  # for the case-insensitive lists: typographic apostrophes and Latin accents folded (L’Oréal -> L'Oreal)
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    return unicodedata.normalize("NFC", re.sub(r"([A-Za-z])[\u0300-\u036f]+", r"\1", unicodedata.normalize("NFD", t)))


def check_ads(s):  # AC43-AC54 AC59 AC159 AC160 AC161 AC164
    html, css, p = s.page()
    scripts = script_strings(html)
    text = norm(page_text(p, css) + " " + " ".join(scripts))
    for ac, words in BANNED.items():
        for word in words:
            for m in re.finditer(re.escape(word), text):
                fail(f"{ac} {s.slug}: page text contains '{word}': …{text[max(0, m.start() - 20):m.end() + 20]}…")
    folded_text = fold(text)
    for ac, words in BANNED_CI.items():
        for word in words:
            for m in re.finditer(re.escape(fold(word)), folded_text, re.I):
                fail(f"{ac} {s.slug}: page text contains '{m.group(0)}' (case-insensitive '{word}'): "
                     f"…{folded_text[max(0, m.start() - 20):m.end() + 20]}…")
    for m in EMAIL.finditer(text + " " + " ".join(v for _, v in p.refs if v.lower().startswith("mailto:"))):
        if m.group(1).lower() != "example.com":
            fail(f"AC59 {s.slug}: an e-mail address outside example.com: {m.group(0)}")
    for m in re.finditer(r"(?<![\w.+-])@[A-Za-z0-9_.가-힣]{2,}", text):
        fail(f"AC164 {s.slug}: a social handle: {m.group(0)}")
    for m in re.finditer(r"(?<![\w@.-])((?:[A-Za-z0-9-]+\.)+(?:com|net|org|kr|io|me|co|shop|cloud))\b", text, re.I):
        if m.group(1).lower() != "example.com":
            fail(f"AC164 {s.slug}: a domain name: {m.group(1)}")
    for ln in blocks(p, css) + scripts:
        folded = unicodedata.normalize("NFKC", ln)
        m = re.search(r"\d\s*(?:호점|개 지점|개지점|개 매장|개매장|개점|곳|명|(?:[천백십]\s*)?(?:억|만|원))|[₩￦]\s*\d"
                      r"|\d\s*KRW|\d{1,3}(?:,\d{3})+", folded)
        if m:
            fail(f"AC44 {s.slug}: a digit followed by '{m.group(0)}' (a count or a money figure): {ln[:80]}")
        m = re.search(r"\d\s*%", folded)
        if m:
            fail(f"AC45 {s.slug}: a digit followed by %: {ln[:80]}")
    for img, _ in p.imgs:
        alt = img.get("alt", "")
        for word in ALT_BANNED:
            if word in alt:
                fail(f"AC159 {s.slug}: alt contains '{word}': {alt[:80]!r}")


def check_flow(s):  # AC33 AC34 AC41 (stylesheet) AC79 AC82 AC83
    _, css, p = s.page()
    if p.forms:
        fail(f"AC33 {s.slug}: {p.forms} <form> element(s)")
    if p.fields:
        fail(f"AC34 {s.slug}: form fields {sorted(set(p.fields))}")
    if not re.search(r"word-break\s*:\s*keep-all", css):
        fail(f"AC41 {s.slug}: style.css has no word-break: keep-all")
    for img, _ in p.imgs:
        if not img.get("alt", "").strip():
            fail(f"AC82 {s.slug}: <img> without alt: {img.get('src')}")
    hs = sorted(p.headings, key=lambda h: h[2])
    levels = [h[0] for h in hs]
    if levels.count(1) != 1:
        fail(f"AC83 {s.slug}: expected exactly one <h1>, found {levels.count(1)}")
    prev = 1
    for lvl in levels:
        if lvl > prev + 1:
            fail(f"AC83 {s.slug}: heading level skipped: h{prev} -> h{lvl}")
        prev = lvl
    h1 = [t for l, t, _, _ in hs if l == 1]
    if h1 and not re.search(r"[가-힣]", h1[0]):
        fail(f"AC79 {s.slug}: the <h1> has no Hangul syllable: {h1[0]!r}")


def exact_case(base, rel):  # every path part matches a directory entry exactly, case included
    cur = base
    for part in Path(rel).parts:
        if part == ".":
            continue
        if not cur.is_dir() or part not in {f.name for f in cur.iterdir()}:
            return False
        cur = cur / part
    return True


def check_assets(s):  # AC1 (page files) AC2 AC60 AC61 AC65 AC72 (reference names)
    html, css, p = s.page()
    for name in ("index.html", "style.css"):
        if not (s.site / name).is_file():
            fail(f"AC1 missing profile/{s.slug}/{name}")
    local = [v for k, v in p.refs if k != "srcset"] + [u for k, v in p.refs if k == "srcset" for u in srcset_urls(v)]
    local += css_urls(css) + css_urls(inline_css(html))
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
                fail(f"AC60 {s.slug}: external stylesheet not allowed: {href}")
    for url in re.findall(r"(?:https?:)?//cdn\.jsdelivr\.net/[^\s\"'()<>,]+", html + css):
        if "pretendard" not in url.lower():
            fail(f"AC60 {s.slug}: a cdn.jsdelivr.net load that is not Pretendard: {url}")
    for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", css + "\n" + inline_css(html)):
        u = urlparse(imp)
        if u.netloc and not font_host(u):
            fail(f"AC60 {s.slug}: external @import not allowed: {imp}")
    for src in p.scripts:
        if src.startswith(("http", "//")):
            fail(f"AC60 {s.slug}: external script: {src}")
    for url in re.findall(r"https?://[^\s\"'()<>,]+", html + css):
        if url.startswith("http://www.w3.org/"):  # an XML namespace (inline SVG), not a load
            continue
        if urlparse(url).netloc not in ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net"):
            fail(f"AC61 {s.slug}: URL with a host that is not allowed: {url}")
    for pat in s.info["ref"]:
        if re.search(pat, unescape(html) + css, re.I):
            fail(f"AC72 {s.slug}: the sample names its reference site ({pat})")
    for ref in (r.removeprefix("./") for r in image_refs(p, css + "\n" + inline_css(html))):
        path = (s.site / ref.split("?")[0].split("#")[0]).resolve()
        if re.search(r"\.(jpe?g|png|webp|avif|gif|svg)$", ref.split("?")[0], re.I) and not ref.startswith("img/"):
            fail(f"AC65 {s.slug}: image not in img/: {ref}")
        elif not path.is_file() or s.img.resolve() not in path.parents:
            fail(f"AC65 {s.slug}: image path does not resolve to a file in img/: {ref}")
        elif not exact_case(s.site, ref.split("?")[0].split("#")[0]):
            fail(f"AC65 {s.slug}: image path differs in letter case from the file (GitHub Pages is case-sensitive): {ref}")


def check_sample_a(s, html, css, p):  # AC102 AC103 AC106 AC107 (static part) AC108-AC110 AC116
    slug = s.slug
    raw, rgb = body_decl(css, ("background", "background-color"))
    if not rgb:
        fail(f"AC102 {slug}: no readable body background colour in style.css ({raw!r})")
    else:
        if hsl_rgb(rgb)[2] > 0.15:
            fail(f"AC102 {slug}: body background {rgb} has HSL lightness {hsl_rgb(rgb)[2]:.3f} > 0.15")
        if rgb[0] - rgb[2] < 0x04:
            fail(f"AC103 {slug}: body background {rgb} has red only {rgb[0] - rgb[2]} above blue (< 0x04)")
    ems = h1_em_texts(html)
    if not ems:
        fail(f"AC106 {slug}: the <h1> has no <em>")
    for t in ems:
        if not re.search(r"[A-Za-z]", t) or re.search(r"[가-힣]", t):
            fail(f"AC106 {slug}: the <h1> <em> text {t!r} needs a Latin letter and no Hangul syllable")
    ital = ital_families(html)
    if not ital:
        fail(f"AC107 {slug}: no fonts.googleapis.com URL in index.html requests ital for a family")
    props = custom_props(top_rules(css))
    em_rules = [(sel, v) for sel, body in flat_rules(css + "\n" + inline_css(html)) for k, v in decls(body)
                if k == "font-family" and any(re.search(r"\bh1\b.*(^|[\s>+~])em(?![\w-])[^\s>+~]*$", part.strip())
                                             for part in sel.split(","))]
    if not em_rules:
        fail(f"AC107 {slug}: no CSS rule with an `em` selector sets font-family")
    for sel, v in em_rules:
        first = resolve(v, props).split(",")[0].strip().strip("'\"").lower()
        if first not in ital:
            fail(f"AC107 {slug}: rule '{sel}' sets first family {first!r}, which no Google Fonts URL requests with ital "
                 f"({sorted(ital)})")
    banned_faces(html, css, ("Instrument Serif", "Inter"), "AC108", slug)
    banned_faces(html, css, ("Noto Serif KR", "Cormorant Garamond", "Hahmlet", "Gowun Batang"), "AC109", slug)
    banned_hex(css, A_BANNED_HEX, "AC110", slug)
    wordmark_no_latin(p, "AC116", slug)


def check_sample_b(s, html, css, p):  # AC121 AC127 AC128 AC131 AC134-AC137
    slug = s.slug
    words = [t for c, t, _ in p.captured if c == "display-word"]
    if len(words) != 1:
        fail(f"AC121 {slug}: expected one element with class display-word, found {len(words)}")
    for t in words:
        if not re.search(r"[가-힣]", t) or re.search(r"[A-Za-z]", t):
            fail(f"AC121 {slug}: the display word {t!r} needs a Hangul syllable and no Latin letter")
    sec = p.heading(r"스타일")
    if not sec:
        fail(f"AC127 {slug}: no h2-h6 heading containing '스타일'")
    else:
        if not sec["in_section"]:
            fail(f"AC127 {slug}: the 스타일 heading is not inside a <section> (its span ends with that section)")
        cards = [a for a in p.articles if sec["start"] < a[1] < sec["end"]]
        if len(cards) < 4:
            fail(f"AC127 {slug}: the 스타일 section has {len(cards)} cards (<article>), needs 4")
        for aid, start, end in cards:
            imgs = [i for i, off in p.imgs if start <= off < end]
            if not any(i.get("src", "").removeprefix("./").startswith("img/") for i in imgs):
                fail(f"AC127 {slug}: style card at {aid or start} has no <img> from img/")
            hs = sorted((h for h in p.headings if h[0] >= 3 and start <= h[2] < end), key=lambda h: h[2])
            if not hs or not re.search(r"[가-힣]", hs[0][1]):
                fail(f"AC128 {slug}: style card at {aid or start} has no h3-h6 style name with a Hangul syllable")
    nav_hangul_only(p, "AC131", slug)
    wordmark_no_latin(p, "AC134", slug)
    banned_faces(html, css, ("Roboto",), "AC135", slug)
    banned_hex(css, B_BANNED_HEX, "AC136", slug)
    raw, rgb = body_decl(css, ("background", "background-color"))
    if not rgb:
        fail(f"AC137 {slug}: no readable body background colour in style.css ({raw!r})")
    elif min(rgb) < 0xF8 or max(rgb) - min(rgb) > 0x04:
        fail(f"AC137 {slug}: body background {rgb} needs every channel >= 0xF8 and a spread <= 0x04")


def check_sample_c(s, html, css, p):  # AC138 AC139 AC141 AC149 AC151
    slug = s.slug
    raw, rgb = body_decl(css, ("background", "background-color"))
    if not rgb:
        fail(f"AC138 {slug}: no readable body background colour in style.css ({raw!r})")
    else:
        if min(rgb) < 0xDC or max(rgb) > 0xF2:
            fail(f"AC138 {slug}: body background {rgb} has a channel outside 0xDC-0xF2")
        if not 0x04 <= rgb[0] - rgb[2] <= 0x14:
            fail(f"AC139 {slug}: body background {rgb} has red {rgb[0] - rgb[2]} above blue, needs 0x04-0x14")
    nav_hangul_only(p, "AC141", slug)
    wordmark_no_latin(p, "AC149", slug)
    banned_hex(css, C_BANNED_HEX, "AC151", slug)


def check_sample(s):
    html, css, p = s.page()
    {"A": check_sample_a, "B": check_sample_b, "C": check_sample_c}[s.info["key"]](s, html, css, p)


def check_register(s):  # AC1 (thumb.jpg) AC3 AC4 AC5 (size) AC15 AC77 AC101 AC111 AC153
    e = entry(s.slug)
    if not e:
        n = sum(1 for x in load_profiles() if x.get("slug") == s.slug)
        fail(f"AC3 expected one PROFILES entry for {s.slug}, found {n}")
    else:
        if (e.get("industry"), e.get("status"), e.get("demo")) != ("beauty", "live", True):
            fail(f"AC3 {s.slug}: entry fields wrong: industry={e.get('industry')} status={e.get('status')} "
                 f"demo={e.get('demo')}")
        if not str(e.get("name", "")).startswith("로빈"):
            fail(f"AC15 {s.slug}: PROFILES name {e.get('name')!r} does not start with 로빈")
    if not re.fullmatch(r"beauty-robin[a-z]+", s.slug):
        fail(f"AC4 {s.slug}: slug is not 'beauty-robin' and lowercase ASCII letters")
    thumb = s.site / "thumb.jpg"
    if thumb.is_file():
        data = thumb.read_bytes()
        if data[:2] != b"\xff\xd8" or data.rstrip(b"\x00\r\n")[-2:] != b"\xff\xd9":
            fail(f"AC5 {s.slug}: thumb.jpg is not a complete JPEG (no FFD8 start or FFD9 end); re-run profile_thumb.py")
        w, h = sips_size(thumb)
        if w != 1200 or h is None or abs(h * 16 - w * 10) > 16:
            fail(f"AC5 {s.slug}: thumb.jpg is {w}x{h}, not 1200 wide at 16:10")
        if s.info["key"] in ("A", "C") and not sips_missing():
            try:
                y = mean_luma(thumb)
            except (subprocess.CalledProcessError, ValueError, struct.error, OSError) as exc:
                fail(f"AC101 AC153 {s.slug}: thumb.jpg could not be decoded: {type(exc).__name__}")
            else:
                if s.info["key"] == "A" and y >= 100:
                    fail(f"AC101 {s.slug}: thumb.jpg mean luma {y:.1f} is not below 100")
                if s.info["key"] == "C" and y < 100:
                    fail(f"AC153 {s.slug}: thumb.jpg mean luma {y:.1f} < 100")
    else:
        fail(f"AC1 AC5 {s.slug}: thumb.jpg missing")
    a = accent_of(e) if e else None
    css = read(s.site / "style.css") if (s.site / "style.css").is_file() else ""
    if not a or a not in css.lower():
        fail(f"AC77 {s.slug}: style.css does not contain the PROFILES accent {a}")
    if s.info["key"] == "A" and (not a or not re.fullmatch(r"#[0-9a-f]{6}", a) or achromatic(a)):
        fail(f"AC111 {s.slug}: accent {a!r} is not chromatic (channel spread must be above 0x18)")


PER_SAMPLE = {"photos": check_photos, "markers": check_markers, "franchise": check_franchise, "ads": check_ads,
              "flow": check_flow, "assets": check_assets, "sample": check_sample, "register": check_register}
SHARED = {"gallery": check_gallery, "current": check_current}

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
