#!/usr/bin/env python3
"""Static checks for the three interior profile samples (no browser, no network). Run from the repository root.

usage: python3 docs/features/2026-11-20-profile-interior/check_static.py <check> [<slug>]
  per sample (all three when <slug> is left out): photos markers structure copy a11y assets sample register
  shared: gallery current
  all: every check above, for every sample
slugs: interior-robininterior (A) interior-robindesign (B) interior-robinhome (C)
Exit 0 when every named check passes; otherwise prints each failure and exits 1.
The page contract these checks read is the "Fixed parameters" section of tasks.md in this folder.
Adapted from docs/features/2026-11-19-profile-beauty/check_static.py; AC numbers are this feature's spec.md.
"""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import re
import runpy
import shutil
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
EXAMPLE_NOTE = "예시 사진이며 실제 시공 사례가 아닙니다."  # AC29
FICTION = "가상의 업체이며 실제 견적 · 상담을 받지 않습니다."  # AC51
SAMPLES = {
    "interior-robininterior": {
        "key": "A", "name": "로빈인테리어", "face": "Do Hyeon", "ac": "AC108",
        "palette": ["#f5f5f3", "#16181b", "#e3e2de", "#c8371f"], "body": ("#f5f5f3", "#16181b", "AC109"),
        "ref": (r"apartmentary", r"아파트멘터리"), "words": ("AC136", ("decimal", "spoqa")), "hex": None},
    "interior-robindesign": {
        "key": "B", "name": "로빈디자인", "face": "Black Han Sans", "ac": "AC138",
        "palette": ["#0b5f65", "#f8f1fb", "#deb1f1", "#ee68ae"], "body": ("#f8f1fb", "#1b1430", "AC139"),
        "ref": (r"studio\s*ashby", r"studioashby", r"애쉬비", r"애시비"),
        "words": ("AC167", ("beaux", "allrounder", "matter")),
        "hex": ("AC166", ("#633b2f", "#b19e18", "#e87308", "#45519f", "#f9f3f0"))},
    "interior-robinhome": {
        "key": "C", "name": "로빈홈", "face": "Diphylleia", "ac": "AC169",
        "palette": ["#2a3f63", "#f0eadf", "#1c2433", "#d2a96a"], "body": ("#2a3f63", "#f0eadf", "AC170"),
        "ref": (r"mcgee", r"studio-mcgee", r"맥기"), "words": ("AC192", ("ftbureau", "jost", "schibsted")),
        "hex": ("AC191", ("#484d49", "#f9f7f4"))},
}
B_SATURATED = ((0xEE, 0x68, 0xAE), (0x0B, 0x5F, 0x65), (0xDE, 0xB1, 0xF1))  # AC165
SECTIONS = {  # kind: (AC, pattern of the section's own <h2>)
    "services": ("AC28", r"서비스|시공 범위|작업 범위"), "example": ("AC29 AC30", r"예시"),
    "process": ("AC31", r"절차|과정"), "contact": ("AC32", r"문의|상담"), "faq": ("AC131", r"자주 묻는 질문")}
ACTIONS = (("AC33", "견적"), ("AC34", "카카오톡"), ("AC35", "전화"), ("AC36", "네이버 예약"), ("AC37", "네이버 지도"))
BANNED = {  # plain substrings of the whitespace-collapsed page text (tasks.md Fixed parameters, "Page text")
    "AC27": ("가맹", "프랜차이즈", "지점 찾기", "매장 찾기", "직영점"),
    "AC52": ("최고", "최초", "최대", "최다", "유일", "독보적", "1위", "1등", "넘버원", "업계 선두", "완벽", "보장", "보증",
             "무조건"),
    "AC53": ("수상", "어워드", "100대", "우수 업체", "인증", "공식 파트너", "협회", "면허 보유", "등록 업체"),
    "AC54": ("후기", "리뷰", "별점", "평점", "만족도", "★", "추천지수", "NPS", "고객 인터뷰"),
    "AC56": ("무료", "공짜", "할인", "이벤트", "선착순", "마감 임박", "프로모션", "쿠폰", "특가", "사은품"),
    "AC57": ("무상", "평생", "하자 없", "무하자", "책임 시공"),
    "AC62": ("친환경", "무독성", "무해", "항균", "유해물질 없", "E0", "새집증후군"),
}
BANNED_CI = {  # case-insensitive substrings
    "AC52": ("No.1",), "AC53": ("Award",), "AC55": ("비포", "애프터", "Before", "After", "전후 사진", "시공 전후"),
    "AC60": ("한샘", "리바트", "Z:IN", "KCC", "영림", "이케아", "IKEA", "까사미아", "일룸", "오늘의집", "집닥", "숨고",
             "아파트멘터리", "삼성", "비스포크", "벤자민무어", "던에드워드", "구정마루", "동화자연마루", "그로헤", "콜러",
             "아메리칸스탠다드", "허먼밀러", "프리츠한센", "루이스폴센", "비트라", "USM"),
    "AC61": ("래미안", "힐스테이트", "푸르지오", "아이파크", "e편한세상", "롯데캐슬", "더샵", "타워팰리스", "아크로", "디에이치",
             "센트레빌", "위브", "SK뷰", "트리마제"),
}
BANNED_WORD = {"AC60": ("LG", "LX")}  # whole words, any case
ALT_BANNED = ("디자이너", "대표", "실장", "직원", "고객", "우리 팀", "시공 사례", "시공 현장", "완공")  # AC67
NOT_HEADING = ("시공 사례", "시공사례", "포트폴리오", "portfolio", "projects")  # AC30, in headings and nav links
C_NOT_HEADING = ("쇼핑", "스토어", "블로그", "매거진", "shop", "blog", "read")  # AC193
EMAIL = re.compile(r"[\w.+-]+@((?:[\w-]+\.)+[A-Za-z]{2,})")
CLOSED = r"휴무|휴관|쉽니다|쉬어요|쉬는 날|쉼"  # AC47
CLOSED_DAY = r"공휴일|일요일|주말|토요일|월요일|화요일|수요일|목요일|금요일"
HOURS = r"\d{1,2}:\d{2}\s*[-–—~～〜]\s*\d{1,2}:\d{2}"  # AC46
BLOCK = {"p", "li", "dd", "dt", "td", "th", "address", "div", "section", "article", "header", "footer", "ul", "ol",
         "h1", "h2", "h3", "h4", "h5", "h6", "button", "nav", "main", "aside", "figure", "figcaption", "tr", "table",
         "dl", "details", "summary", "blockquote", "body"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SKIP = {"script", "style", "template", "title"}
BG_WORDS = {"none", "transparent", "no-repeat", "repeat", "repeat-x", "repeat-y", "space", "round", "center", "top",
            "left", "right", "bottom", "cover", "contain", "auto", "fixed", "scroll", "local", "border-box",
            "padding-box", "content-box", "inherit", "initial", "unset", "linear-gradient", "radial-gradient",
            "conic-gradient", "repeating-linear-gradient", "repeating-radial-gradient", "to", "at", "circle", "ellipse",
            "closest-side", "farthest-side", "closest-corner", "farthest-corner", "from", "important"}
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


def squash(s):
    return re.sub(r"\s+", "", s or "")


# --- a small DOM -------------------------------------------------------------------------------------------

class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.kids, self.order = tag, attrs, parent, [], 0

    def iter(self, *tags):  # descendants in document order
        for k in self.kids:
            if isinstance(k, Node):
                if not tags or k.tag in tags:
                    yield k
                yield from k.iter(*tags)

    def classes(self):
        return self.attrs.get("class", "").split()

    def up(self, pred):  # the nearest ancestor (not self) for which pred holds
        n = self.parent
        while n is not None and not pred(n):
            n = n.parent
        return n

    def text(self, breaks=False):  # text with image alt; "\n" at block boundaries when breaks is set
        out = []

        def walk(n):
            for k in n.kids:
                if isinstance(k, str):
                    out.append(k)
                elif k.tag in SKIP:
                    continue
                else:
                    mark = "\n" if breaks and k.tag in BLOCK else " " if k.tag in ("br", "a") else ""
                    out.append(mark)
                    if k.tag == "img":
                        out.append(" " + k.attrs.get("alt", "") + " ")
                    walk(k)
                    out.append(mark)
        walk(self)
        return "".join(out)

    def name(self):  # accessible name: aria-label, else text with image alt
        return norm(self.attrs.get("aria-label") or self.text())


class Dom(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.cur, self.n, self.title = self.root, 0, []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: (v or "") for k, v in attrs}, self.cur)
        self.n += 1
        node.order = self.n
        self.cur.kids.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.cur = self.cur.parent

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        if self.cur.tag == "title":
            self.title.append(data)
        self.cur.kids.append(data)


class Sample:
    def __init__(self, slug):
        self.slug, self.info = slug, SAMPLES[slug]
        self.site = ROOT / "profile" / slug
        self.img = self.site / "img"
        self.sources = self.img / "sources.txt"
        self._page = None

    def page(self):
        if self._page is None:
            html = read(self.site / "index.html")
            self._page = (html, read(self.site / "style.css"), Dom(html))
        return self._page

    def image_files(self):
        return sorted(f for f in self.img.iterdir() if f.is_file() and f.name != "sources.txt"
                      and not f.name.startswith(".")) if self.img.is_dir() else []

    def source_lines(self):
        if not self.sources.is_file():
            fail(f"AC78 {self.slug}: img/sources.txt missing")
            return []
        return [ln.split() for ln in read(self.sources).splitlines() if ln.strip()]


def headings(d):
    return list(d.root.iter("h1", "h2", "h3", "h4", "h5", "h6"))


def own_h2(sec):  # the <h2> elements whose nearest <section> is sec
    return [h for h in sec.iter("h2") if h.up(lambda n: n.tag == "section") is sec]


def section(d, kind, slug, quiet=False):
    """The one <section id> whose own <h2> matches the pattern of `kind`. None, with a failure, when there is none
    or more than one (a heading such as '상담 절차' matches both the process and the contact pattern)."""
    ac, pat = SECTIONS[kind]
    hits = [s for s in d.root.iter("section") if s.attrs.get("id") and any(re.search(pat, norm(h.text())) for h in own_h2(s))]
    if len(hits) == 1:
        return hits[0]
    if not quiet:
        got = [f"#{s.attrs['id']} '{norm(own_h2(s)[0].text())}'" for s in hits]
        fail(f"{ac} {slug}: expected exactly one <section id> whose own <h2> matches /{pat}/, found {len(hits)} {got}")
    return None


def header(d):
    return next(d.root.iter("header"), None)


def wordmark(d):  # the <a class="wordmark"> in the first <header>
    h = header(d)
    return next((a for a in h.iter("a") if "wordmark" in a.classes()), None) if h else None


def nav_links(d):  # every <a> inside a <nav> in the first <header>
    h = header(d)
    return [a for nav in h.iter("nav") for a in nav.iter("a")] if h else []


def footer(d):
    fs = [f for f in d.root.iter("footer") if not f.up(lambda n: n.tag == "article")]
    return fs[-1] if fs else None


def inline_css(html):  # the CSS inside <style> elements and style="" attributes of index.html
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)
                     + ["[style]{%s}" % unescape(v) for v in re.findall(r"\sstyle\s*=\s*\"([^\"]*)\"", html, re.I)]
                     + ["[style]{%s}" % unescape(v) for v in re.findall(r"\sstyle\s*=\s*'([^']*)'", html, re.I)])


def uncomment(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def css_urls(css):
    out = [u.strip("'\" ") for u in re.findall(r"url\(([^)]*)\)", uncomment(css))]
    out += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", css)
    return out


def srcset_urls(v):
    return [part.strip().split()[0] for part in v.split(",") if part.strip()]


def css_content(css):  # strings in CSS content: declarations, read with the page text
    return [m[1] for m in re.findall(r"content\s*:\s*([\"'])(.*?)\1", uncomment(css))]


def attr_texts(d):  # aria-label, title and alt attributes, meta description and og: content
    out = []
    for n in d.root.iter():
        out += [n.attrs[k] for k in ("aria-label", "title") if n.attrs.get(k)]
        if n.tag == "meta" and (n.attrs.get("name") == "description" or n.attrs.get("property", "").startswith("og:")):
            out.append(n.attrs.get("content", ""))
    return out


def lines(node):  # the text of a node, one entry per block
    return [norm(ln) for ln in node.text(breaks=True).split("\n") if ln.strip()]


def blocks(d, css):  # the page text, one entry per block
    return lines(d.root) + [norm(" ".join(d.title))] + [norm(t) for t in attr_texts(d)] + css_content(css)


def page_text(d, css):
    return norm(" ".join(blocks(d, css)))


def script_strings(html):  # inline <script> string literals a script may put on the page
    out = []
    for body in re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S | re.I):
        for m in re.finditer(r"\"((?:[^\"\\\n]|\\.)*)\"|'((?:[^'\\\n]|\\.)*)'|`((?:[^`\\]|\\.)*)`", body):
            t = next(g for g in m.groups() if g is not None)
            if re.search(r"[가-힣<@₩￦\s]", t) and t not in ("beforebegin", "afterbegin", "beforeend", "afterend"):
                out.append(norm(unescape(re.sub(r"<[^>]+>", " ", t))))
    return [t for t in out if t]


# --- CSS ---------------------------------------------------------------------------------------------------

def top_rules(css):
    css = uncomment(css)
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


def flat_rules(css):  # (selector, own declarations) of every rule at any nesting (@media and CSS nesting included)
    out = []

    def walk(s):
        own, i = [], 0
        while True:
            j = s.find("{", i)
            if j < 0:
                own.append(s[i:])
                break
            head = s[i:j]
            cut = head.rfind(";") + 1
            own.append(head[:cut])
            depth, k = 1, j + 1
            while k < len(s) and depth:
                depth += {"{": 1, "}": -1}.get(s[k], 0)
                k += 1
            out.append((head[cut:].strip(), walk(s[j + 1:k - 1])))
            i = k
        return "".join(own)
    walk(uncomment(css))
    return out


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


def resolve_all(value, defs):  # every reading of a value whose var()s may be defined in several rules; None: undefined var
    done, todo = [], [value]
    for _ in range(200):
        if not todo:
            return done
        v = todo.pop()
        m = re.search(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)", v)
        if not m:
            done.append(v)
            continue
        reps = list(defs.get(m.group(1), [])) + ([m.group(2)] if m.group(2) else [])
        if not reps:
            return None
        todo += [v[:m.start()] + r + v[m.end():] for r in reps]
    return None  # too many readings or a cycle


def hex_rgb(h):  # '#abc' or '#aabbcc' -> (r, g, b)
    h = h.lstrip("#")
    h = "".join(c * 2 for c in h) if len(h) == 3 else h
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def one_color(value):  # a declaration value that is one opaque colour, as (r, g, b); else None
    v = value.strip().lower().replace("!important", "").strip()
    if re.fullmatch(r"#(?:[0-9a-f]{3}|[0-9a-f]{6})", v):
        return hex_rgb(v)
    m = re.fullmatch(r"rgb\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)\s*\)", v)
    return tuple(int(x) for x in m.groups()) if m else None


def body_decl(css, names):  # the last of the named declarations in a top-level `body` rule, var() resolved
    rules, val = top_rules(css), None
    props = custom_props(rules)
    for sel, body in rules:
        if any(x.strip() == "body" for x in sel.split(",")):
            for k, v in decls(body):
                if k in names:
                    val = v
    return val, one_color(resolve(val, props)) if val else None


def background_colors(css):
    """Every colour in every background, background-color and background-image value, at any nesting, var()
    resolved from every rule that defines the property (each definition is read). Returns ([(selector, (r, g, b), alpha)], [problem]). A token that is not a hex
    colour, an rgb()/rgba() with plain numbers, a number, a url() or a known keyword is a problem (fail closed)."""
    rules, defs, found, bad = flat_rules(css), {}, [], []
    for _, body in rules:
        for k, v in decls(body):
            if k.startswith("--"):
                defs.setdefault(k, []).append(v)
    values = []
    for sel, body in rules:
        for k, raw in decls(body):
            if k not in ("background", "background-color", "background-image"):
                continue
            readings = resolve_all(raw, defs)
            if readings is None:
                bad.append(f"'{sel}' {k}: {raw} (a var() that no rule defines, or one the check cannot resolve)")
                continue
            values += [(sel, k, r.lower()) for r in readings]
    for sel, k, v in values:
        if True:
            v = re.sub(r"url\([^)]*\)", " ", v)
            for m in re.finditer(r"rgba?\(([^)]*)\)", v):
                parts = [p for p in re.split(r"[\s,/]+", m.group(1).strip()) if p]
                if len(parts) not in (3, 4) or not all(re.fullmatch(r"\d*\.?\d+", p) for p in parts):
                    bad.append(f"'{sel}' {k}: {m.group(0)} (write rgb() with plain numbers)")
                    continue
                found.append((sel, tuple(int(float(p)) for p in parts[:3]), float(parts[3]) if len(parts) == 4 else 1.0))
            v = re.sub(r"rgba?\([^)]*\)", " ", v)
            for m in re.finditer(r"#([0-9a-f]+)", v):
                h = m.group(1)
                if len(h) not in (3, 4, 6, 8):
                    bad.append(f"'{sel}' {k}: {m.group(0)} (not a hex colour)")
                    continue
                h = "".join(c * 2 for c in h) if len(h) in (3, 4) else h
                found.append((sel, hex_rgb(h[:6]), int(h[6:8], 16) / 255 if len(h) == 8 else 1.0))
            v = re.sub(r"#[0-9a-f]+", " ", v)
            v = re.sub(r"-?\d*\.?\d+(?:deg|turn|rad|px|em|rem|vw|vh|vmin|vmax|%)?", " ", v)
            for word in re.findall(r"[a-z][a-z-]*", v):
                if word not in BG_WORDS:
                    bad.append(f"'{sel}' {k}: '{word}' (write every background colour as #hex or rgb())")
    return found, bad


def google_families(html, css):  # families requested from fonts.googleapis.com (link or @import)
    fams = []
    for u in re.findall(r"(?:https?:)?//fonts\.googleapis\.com[^\"'\s)]*", unescape(html) + "\n" + css):
        if urlparse(u).path in ("", "/"):  # a preconnect hint, not a request for a family
            continue
        got = parse_qs(urlparse(u).query).get("family", []) if re.search(r"\.com/css2?\?", u) else []
        fams += [fam.split(":")[0].replace("+", " ").strip() for fam in got] or [u]  # /icon, /earlyaccess …: listed as is
    return fams


# --- files -------------------------------------------------------------------------------------------------

def photo_id(url):
    m = re.search(r"images\.unsplash\.com/(photo-[0-9]+-[0-9a-f]+)", url, re.I) or \
        re.search(r"images\.pexels\.com/photos/([0-9]+)/", url)
    return m.group(1).lower() if m else None


def sips_size(path):
    if not shutil.which("sips"):
        fail("sips not found: the image checks need macOS sips")
        return (None, None)
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True)
    w = re.search(r"pixelWidth:\s*(\d+)", r.stdout)
    h = re.search(r"pixelHeight:\s*(\d+)", r.stdout)
    return (int(w.group(1)), int(h.group(1))) if w and h else (None, None)


_profiles = None


def load_profiles():
    global _profiles
    if _profiles is None:
        try:  # run_path reads the file as it is now: no stale __pycache__ copy
            _profiles = runpy.run_path(str(ROOT / "scripts/profiles.py"))["PROFILES"]
        except Exception as exc:  # a broken profiles.py is a failure, not a traceback
            fail(f"AC3 scripts/profiles.py does not load: {type(exc).__name__}: {exc}")
            _profiles = []
    return _profiles


def entry(slug):
    hits = [p for p in load_profiles() if p.get("slug") == slug]
    return hits[0] if len(hits) == 1 else None


def accent_of(e):
    return str((e.get("palette") or [""])[-1]).lower()


def exact_case(base, rel):  # every path part matches a directory entry exactly, case included
    cur = base
    for part in Path(rel).parts:
        if part == ".":
            continue
        if not cur.is_dir() or part not in {f.name for f in cur.iterdir()}:
            return False
        cur = cur / part
    return True


# --- shared checks -----------------------------------------------------------------------------------------

def check_gallery():  # AC3 (no other interior entry) AC19 AC102, and the generated part of AC100 AC101
    gallery = read(ROOT / "profile/index.html")
    profiles = load_profiles()
    count = sum(1 for p in profiles if p.get("industry") == "interior")
    if count != len(SAMPLES) or not re.search(rf'data-filter="interior"[^>]*>[^<]*<sup>{count}</sup>', gallery):
        fail(f"AC102 profile/index.html: the interior filter chip does not show the count {len(SAMPLES)} "
             f"(PROFILES has {count} interior entries; run python3 scripts/build.py)")
    for slug in SAMPLES:
        if f'data-slug="{slug}"' not in gallery:
            fail(f"AC100 profile/index.html has no card for {slug}")
    if re.search(r'class="pf-card pf-empty[^"]*" data-industry="interior"', gallery):
        fail("AC101 profile/index.html still has the interior 준비 중 tile")
    others = [p.get("slug") for p in profiles if p.get("industry") == "interior" and p.get("slug") not in SAMPLES]
    if others:
        fail(f"AC3 PROFILES has interior entries for other slugs: {others}")
    names = [entry(slug).get("name") for slug in SAMPLES if entry(slug)]
    if len(set(names)) != len(names):
        fail(f"AC19 two interior samples share a PROFILES name: {names}")


def check_current():  # AC106
    comp = read(ROOT / "docs/current_system/profile-samples/component.md")
    src = next((ln for ln in comp.splitlines() if ln.startswith("**Source:**")), "")
    listed = set(re.findall(r"`([a-z0-9-]+)`", src))
    for slug in SAMPLES:
        if slug not in listed:
            fail(f"AC106 the Source line of profile-samples/component.md does not list `{slug}`")


# --- per-sample checks -------------------------------------------------------------------------------------

def check_photos(s):  # AC72 AC74-AC79 AC202
    files = s.image_files()
    if not files:
        fail(f"AC74 {s.slug}: img/ has no image files")
    if len(files) > 6:
        fail(f"AC202 {s.slug}: img/ holds {len(files)} image files, more than six")
    for d in (f for f in s.img.rglob("*") if f.is_dir()) if s.img.is_dir() else []:
        fail(f"AC74 {s.slug}: img/ holds a folder, whose files no photo check reads: {d.relative_to(s.site)}")
    total = 0
    for f in files:
        if f.suffix.lower() not in (".jpg", ".webp"):
            fail(f"AC74 {s.slug}: not .jpg/.webp: img/{f.name}")
        size = f.stat().st_size
        total += size
        if size > 500 * 1024:
            fail(f"AC76 {s.slug}: larger than 500 KB: img/{f.name} ({size // 1024} KB)")
        w, _ = sips_size(f)
        if w is None or w > 2000:
            fail(f"AC75 {s.slug}: wider than 2000 px or unreadable: img/{f.name} ({w})")
    if total > 3 * 1024 * 1024:
        fail(f"AC77 {s.slug}: img/ totals {total / 1024 / 1024:.2f} MB > 3 MB")
    rows = s.source_lines()
    names = [ln[0] for ln in rows if ln]
    for ln in rows:
        if len(ln) != 3:
            fail(f"AC78 {s.slug}: sources.txt line is not '<file> <page URL> <download URL>': {' '.join(ln)}")
            continue
        _, page_url, dl = ln
        if page_url != "-" and not page_url.startswith(("https://unsplash.com/photos/", "https://www.pexels.com/photo/")):
            fail(f"AC78 {s.slug}: page URL is not an Unsplash/Pexels photo page or '-': {page_url}")
        if not dl.startswith(("https://images.unsplash.com/photo-", "https://images.pexels.com/photos/")):
            fail(f"AC79 {s.slug}: download URL not allowed: {dl}")
    if sorted(names) != [f.name for f in files] or len(set(names)) != len(names):
        fail(f"AC78 {s.slug}: sources.txt files {sorted(names)} != img/ files {[f.name for f in files]}")
    raw = read(s.sources) if s.sources.is_file() else ""
    if "plus.unsplash.com" in raw or "premium_photo" in raw:
        fail(f"AC79 {s.slug}: sources.txt mentions plus.unsplash.com or premium_photo")
    taken = {}
    for path in sorted((ROOT / "profile").glob("*/img/sources.txt")):
        if path.parent.parent.name == s.slug:
            continue
        for ln in read(path).splitlines():
            pid = photo_id(ln)
            if pid:
                taken[pid] = str(path.relative_to(ROOT))
    for ln in rows:
        pid = photo_id(ln[-1]) if ln else None
        if ln and not pid:
            fail(f"AC72 {s.slug}: no photo ID can be read from the download URL, so it cannot be compared: {ln[-1]}")
        if pid and pid in taken:
            fail(f"AC72 {s.slug}: photo {pid} is also recorded in {taken[pid]}")


def check_markers(s):  # AC8 (text; visibility in check_browser.py) AC12-AC16 AC18 AC20 AC22-AC24 AC196
    _, css, d = s.page()
    slug = s.slug
    if MARK not in norm(d.root.text()):
        fail(f"AC8 {slug}: page text lacks '{MARK}'")
    if "디자인 샘플" not in norm(" ".join(d.title)):
        fail(f"AC16 {slug}: <title> lacks '디자인 샘플'")
    ft = footer(d)
    foot = norm(ft.text()) if ft else ""
    if not ft:
        fail(f"AC12 AC13 {slug}: no <footer>")
    if MARK not in foot:
        fail(f"AC12 {slug}: footer lacks '{MARK}'")
    if "Website by RobinTech" not in foot:
        fail(f"AC13 {slug}: footer lacks 'Website by RobinTech'")
    credit = foot.split("Photos:", 1)[1] if "Photos:" in foot else ""
    raw = read(s.sources) if s.sources.is_file() else ""
    if not credit:
        fail(f"AC14 {slug}: footer has no 'Photos:' credit")
    for host, name in (("images.unsplash.com", "Unsplash"), ("images.pexels.com", "Pexels")):
        if host in raw and name not in credit:
            fail(f"AC14 {slug}: a {name} photo is used but the footer's 'Photos:' credit does not name {name}")
    if not any(m.attrs.get("name") == "robots" and m.attrs.get("content") == "noindex" for m in d.root.iter("meta")):
        fail(f'AC15 {slug}: no <meta name="robots" content="noindex">')
    wm = wordmark(d)
    if not wm:
        fail(f'AC18 {slug}: no <a class="wordmark"> in the first <header>')
    else:
        if not wm.name().startswith("로빈"):
            fail(f"AC18 {slug}: the wordmark's accessible name {wm.name()!r} does not start with 로빈")
        if re.search(r"[A-Za-z]", wm.name()):
            fail(f"AC196 {slug}: the wordmark's accessible name {wm.name()!r} has a Latin letter")
    addr = re.compile(r"[가-힣0-9]*[가-힣0-9](?<!으)(?:로|길)\s?\d+(?:-\d+)?"
                      r"(?![\d%A-Za-z가-힣~:.-]|,\d|\s?(?:원|분|시|개|인|일|명|번|미터|층|m(?![A-Za-z])))"
                      r"|[가-힣]+동\d*가\s?\d+|\d+(?:-\d+)?\s?번지")  # road-name, 동N가 and 번지 addresses
    page_lines = lines(d.root)
    if not any("(가상 주소)" in ln for ln in page_lines):
        fail(f"AC20 {slug}: no address with '(가상 주소)' on the page")
    for ln in page_lines:
        if addr.search(ln) and "(가상 주소)" not in ln:
            fail(f"AC20 {slug}: address without '(가상 주소)': {ln[:80]}")
    refs = [n.attrs[k] for n in d.root.iter() for k in ("href", "src") if k in n.attrs]
    text = d.root.text(breaks=True) + "\n" + " ".join(refs) + "\n" + " ".join(attr_texts(d))
    phones = re.findall(r"(?<![\d-])(?:0\d{1,2}[-.\s]\d{3,4}|1[5-9]\d{2})[-.\s]\d{4}(?![\d-])", text)
    phones += re.findall(r"\(0\d{1,2}\)\s?\d{3,4}[-.\s]\d{4}|\+82[\d\s().-]{7,}", text)
    for ph in phones:
        if ph != "02-000-0000":
            fail(f"AC22 {slug}: phone number is not 02-000-0000: {ph}")
    for v in refs:
        if v.lower().startswith("tel:") and re.sub(r"\D", "", v) != "020000000":
            fail(f"AC22 {slug}: tel: link is not 02-000-0000: {v}")
    brns = re.findall(r"(?<![\d-])\d{3}[-.\s]\d{2}[-.\s]\d{5}(?![\d-])", text)
    if "사업자등록번호" in text and not brns:
        fail(f"AC23 {slug}: '사업자등록번호' without a number 000-00-00000")
    for brn in brns:
        if brn != "000-00-00000":
            fail(f"AC23 {slug}: business registration number is not 000-00-00000: {brn}")
    reg = re.compile(r"(등록\s*번호|등록|허가\s*번호|신고\s*번호|인가\s*번호|면허\s*번호|면허)[\s:(\[#는은\-–—]*(?:제\s*)?"
                     r"(?:No\.?\s*)?([0-9][0-9\-]*)")
    for ln in blocks(d, css):  # per block; full-width digits folded
        folded = unicodedata.normalize("NFKC", ln)
        for m in re.finditer(r"(?<!사업자)(?<!사업자 )등록\s*번호|면허\s*번호|허가\s*번호|신고\s*번호|인가\s*번호"
                             r"|(?:공사업|건설업|통신판매업?)\s*(?:등록|신고|면허)|제\s*[0-9][0-9가-힣\-\s]{0,25}호", folded):
            fail(f"AC24 {slug}: a registration number other than 사업자등록번호: {m.group(0)} in {ln[:60]}")
        for m in reg.finditer(folded):
            if re.search(r"[1-9]", m.group(2)):
                fail(f"AC24 {slug}: {m.group(1)} with a digit other than 0: {m.group(0)}")
        for m in re.finditer(r"제\s*([0-9][0-9\-]*)\s*호", folded):
            if re.search(r"[1-9]", m.group(1)):
                fail(f"AC24 {slug}: a 제…호 number with a digit other than 0: {m.group(0)}")


def check_structure(s):  # AC28-AC41 AC46-AC48 AC51 AC195
    _, _, d = s.page()
    slug = s.slug
    svc, ex, proc, con = (section(d, k, slug) for k in ("services", "example", "process", "contact"))
    if svc and max(len(list(svc.iter("li"))), len(list(svc.iter("h3")))) < 3:
        fail(f"AC28 {slug}: the service section names fewer than three kinds of work (<li> or <h3> items)")
    holders = [x for x in d.root.iter("section") if EXAMPLE_NOTE in norm(x.text())]
    if norm(d.root.text()).count(EXAMPLE_NOTE) != 1 or len(holders) != 1 or (ex is not None and holders[0] is not ex):
        fail(f"AC29 {slug}: the sentence '{EXAMPLE_NOTE}' must appear once on the page, inside the example section "
             f"and inside no other or nested <section> (found in {len(holders)} sections)")
    if ex:
        n = sum(1 for i in ex.iter("img") if i.attrs.get("src", "").removeprefix("./").startswith("img/"))
        if n < 3:
            fail(f"AC29 {slug}: the example section has {n} <img> from img/, needs 3")
    marked = [("heading", h) for h in headings(d)] + [("nav link", a) for nav in d.root.iter("nav") for a in nav.iter("a")]
    for what, n in marked:
        for word in NOT_HEADING:
            if word in norm(n.text()).lower():
                fail(f"AC30 {slug}: a {what} contains '{word}': {norm(n.text())[:40]!r}")
    if proc and not any(sum(1 for k in ol.kids if isinstance(k, Node) and k.tag == "li") >= 4 for ol in proc.iter("ol")):
        fail(f"AC31 {slug}: the process section has no <ol> with at least four <li> steps")
    if next(d.root.iter("form"), None) is not None:
        fail(f"AC40 {slug}: the page has a <form> element")
    fields = sorted({n.tag for n in d.root.iter("input", "select", "textarea")})
    if fields:
        fail(f"AC41 {slug}: form fields {fields}")
    nav = nav_links(d)
    if not nav:
        fail(f"AC195 {slug}: no <a> inside a <nav> in the first <header>")
    for a in nav:
        t = norm(a.text())
        if not re.search(r"[가-힣]", t) or re.search(r"[A-Za-z]", t):
            fail(f"AC195 {slug}: header nav link text needs a Hangul syllable and no Latin letter: {t!r}")
    if not con:
        return
    ctl = [n for n in con.iter("a", "button")]
    for ac, word in ACTIONS:
        if not any(word in c.name() and c.tag == "a" for c in ctl):
            fail(f"{ac} {slug}: the contact section has no link whose accessible name contains '{word}'")
    for c in ctl:
        hit = [w for _, w in ACTIONS if w in c.name()]
        if len(hit) > 1:
            fail(f"AC38 {slug}: one control names several actions {hit}: '{c.name()}'")
        if hit and (c.tag != "a" or c.attrs.get("href") != "#"):
            fail(f"AC39 {slug}: '{c.name()}' (<{c.tag}>) has href={c.attrs.get('href')!r}, not '#'")
    ls = lines(con)
    if not any(re.search(HOURS, ln) for ln in ls):
        fail(f"AC46 {slug}: the contact section shows no 상담 hours as HH:MM–HH:MM")
    labels = [ls[i - 1] if i and len(ls[i - 1]) <= 12 and not re.search(r"\d:\d", ls[i - 1]) else "" for i in range(len(ls))]

    def closed(ln, lb):
        no = r"휴무일?\s*:?\s*없|에도|없이|문의"  # judged in the blocks that make the match: a label only when it is needed
        if re.search(CLOSED, ln) and re.search(CLOSED_DAY, ln):
            return not re.search(no, ln)
        hit = (re.search(CLOSED, lb) and re.search(CLOSED_DAY, ln)) or (re.search(CLOSED_DAY, lb) and re.search(CLOSED, ln))
        return hit and not re.search(no, lb + " " + ln)
    if not any(closed(ln, lb) for ln, lb in zip(ls, labels)):
        fail(f"AC47 {slug}: the contact section has no closed-days line ({CLOSED} with a day, in one block or split "
             f"over a label of at most 12 characters and the next block)")
    if not any("(가상 주소)" in ln for ln in ls):
        fail(f"AC48 {slug}: the contact section shows no address with '(가상 주소)'")
    if not any("02-000-0000" in ln for ln in ls):
        fail(f"AC48 {slug}: the contact section does not show 02-000-0000")
    if FICTION not in norm(con.text()):
        fail(f"AC51 {slug}: the contact section lacks the sentence '{FICTION}'")


def fold(t):  # typographic apostrophes and Latin accents folded
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    return unicodedata.normalize("NFC", re.sub(r"([A-Za-z])[\u0300-\u036f]+", r"\1", unicodedata.normalize("NFD", t)))


def banned_copy(slug, text, parts):  # AC27 AC52-AC62: listed words in `text`, digit forms per block in `parts`
    def around(t, m):
        return f"…{t[max(0, m.start() - 20):m.end() + 20]}…"
    for ac, words in BANNED.items():
        for word in (w for x in words for w in dict.fromkeys((x, x.replace(" ", "")))):  # '책임 시공' and '책임시공'
            for m in re.finditer(re.escape(word), text):
                fail(f"{ac} {slug}: page text contains '{word}': {around(text, m)}")
    folded_text = fold(text)
    for ac, words in BANNED_CI.items():
        for word in (w for x in words for w in dict.fromkeys((x, x.replace(" ", "")))):
            for m in re.finditer(re.escape(fold(word)), folded_text, re.I):
                fail(f"{ac} {slug}: page text contains '{m.group(0)}' (case-insensitive '{word}'): {around(folded_text, m)}")
    for ac, words in BANNED_WORD.items():
        for word in words:
            for m in re.finditer(rf"(?<![A-Za-z0-9]){word}(?![A-Za-z0-9])", folded_text, re.I):
                fail(f"{ac} {slug}: page text contains the word '{m.group(0)}': {around(folded_text, m)}")
    for ln in parts:
        folded = unicodedata.normalize("NFKC", ln)
        m = re.search(r"\d(?:평|건|세대|가구|곳|명|년|개월|주|일)|\d\s*(?:[천백십]\s*)?(?:억|만|원)|[₩￦]\s*\d|\d\s*KRW"
                      r"|\d{1,3}(?:,\d{3})+", folded)
        if m:
            fail(f"AC58 {slug}: '{m.group(0)}' reads as an area, a count, a period or a money figure: {ln[:80]}")
        if re.search(r"\d\s*%", folded):
            fail(f"AC59 {slug}: a digit followed by %: {ln[:80]}")


def check_copy(s):  # AC25 AC26 AC27 AC52-AC62 (listed words and digit forms) AC67
    html, css, d = s.page()
    slug = s.slug
    scripts = script_strings(html)
    css = css + "\n" + inline_css(html)  # content: strings of <style> and style="" count as page text too
    if re.search(r"content\s*:[^;{}]*\battr\(", uncomment(css)):
        fail(f"AC27 AC52-AC62 {slug}: a CSS content: uses attr(); the check cannot read that text, write the string")
    text = norm(page_text(d, css) + " " + " ".join(scripts))
    banned_copy(slug, text, blocks(d, css) + scripts)
    mailto = [n.attrs["href"] for n in d.root.iter("a") if n.attrs.get("href", "").lower().startswith("mailto:")]
    for m in EMAIL.finditer(text + " " + " ".join(mailto)):
        if m.group(1).lower() != "example.com":
            fail(f"AC25 {slug}: an e-mail address outside example.com: {m.group(0)}")
    for m in re.finditer(r"(?<![\w.+-])@[A-Za-z0-9_.가-힣]{2,}", text):
        fail(f"AC26 {slug}: a social handle: {m.group(0)}")
    for m in re.finditer(r"(?<![\w@.-])((?:[A-Za-z0-9-]+\.)+(?:com|net|org|kr|io|me|co|shop|cloud))\b", text, re.I):
        if m.group(1).lower() != "example.com":
            fail(f"AC26 {slug}: a domain name: {m.group(1)}")
    for img in d.root.iter("img"):
        alt = img.attrs.get("alt", "")
        for word in (w for x in ALT_BANNED for w in dict.fromkeys((x, x.replace(" ", "")))):
            if word in alt:
                fail(f"AC67 {slug}: alt contains '{word}': {alt[:80]!r}")


def check_a11y(s):  # AC49 (stylesheet) AC50 AC93 AC94
    _, css, d = s.page()
    if not re.search(r"word-break\s*:\s*keep-all", css):
        fail(f"AC49 {s.slug}: style.css has no word-break: keep-all")
    for img in d.root.iter("img"):
        if not img.attrs.get("alt", "").strip():
            fail(f"AC93 {s.slug}: <img> without alt: {img.attrs.get('src')}")
    hs = headings(d)
    levels = [int(h.tag[1]) for h in hs]
    if levels.count(1) != 1:
        fail(f"AC94 {s.slug}: expected exactly one <h1>, found {levels.count(1)}")
    prev = 1
    for lvl in levels:
        if lvl > prev + 1:
            fail(f"AC94 {s.slug}: heading level skipped: h{prev} -> h{lvl}")
        prev = lvl
    h1 = [norm(h.text()) for h in hs if h.tag == "h1"]
    if h1 and not re.search(r"[가-힣]", h1[0]):
        fail(f"AC50 {s.slug}: the <h1> has no Hangul syllable: {h1[0]!r}")


def check_assets(s):  # AC1 (page files) AC2 AC68 AC69 AC73 AC82 (reference names) AC197
    html, css, d = s.page()
    slug = s.slug
    for name in ("index.html", "style.css"):
        if not (s.site / name).is_file():
            fail(f"AC1 missing profile/{slug}/{name}")
    all_css = css + "\n" + inline_css(html)
    refs = []
    for n in d.root.iter():
        for k in ("src", "href", "poster"):
            if k in n.attrs:
                refs.append(n.attrs[k])
        if "srcset" in n.attrs:
            refs += srcset_urls(n.attrs["srcset"])
    for ref in refs + css_urls(all_css):
        if ref.startswith(("http://", "https://", "data:", "#", "mailto:", "tel:")):
            continue
        if ref.startswith("/") or "../" in ref or "assets/" in ref:
            fail(f"AC2 {slug}: reference leaves the sample folder: {ref}")
    if "../" in html + css or re.search(r"\bassets/", html + css):
        fail(f"AC2 {slug}: index.html or style.css contains '../' or 'assets/'")

    def font_host(u):
        return u.netloc == "fonts.googleapis.com" or (u.netloc == "cdn.jsdelivr.net" and "pretendard" in u.path.lower())
    for link in d.root.iter("link"):
        href = link.attrs.get("href", "")
        if "stylesheet" in link.attrs.get("rel", "") and href.startswith(("http", "//")):
            if not font_host(urlparse(href if not href.startswith("//") else "https:" + href)):
                fail(f"AC68 {slug}: external stylesheet not allowed: {href}")
    for url in re.findall(r"(?:https?:)?//cdn\.jsdelivr\.net/[^\s\"'()<>,]+", html + css):
        if "pretendard" not in url.lower():
            fail(f"AC68 {slug}: a cdn.jsdelivr.net load that is not Pretendard: {url}")
    for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", all_css):
        u = urlparse(imp)
        if u.netloc and not font_host(u):
            fail(f"AC68 {slug}: external @import not allowed: {imp}")
    for sc in d.root.iter("script"):
        if sc.attrs.get("src", "").startswith(("http", "//")):
            fail(f"AC68 {slug}: external script: {sc.attrs['src']}")
        elif "src" in sc.attrs:  # the copy checks (AC27 AC52-AC62) read inline scripts only
            fail(f"AC27 AC52-AC62 {slug}: a <script src> file ({sc.attrs['src']}); scripts are inline (tasks.md, Images)")
    for url in re.findall(r"https?://[^\s\"'()<>,]+", html + css):
        if url.startswith("http://www.w3.org/"):  # an XML namespace (inline SVG), not a load
            continue
        if urlparse(url).netloc not in ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net"):
            fail(f"AC69 {slug}: URL with a host that is not allowed: {url}")
    for pat in s.info["ref"]:
        if re.search(pat, unescape(html) + css, re.I):
            fail(f"AC82 {slug}: the sample names its reference site ({pat})")
    fams = sorted(set(google_families(html, css)))
    if fams != [s.info["face"]]:
        fail(f"AC197 {slug}: fonts.googleapis.com is asked for {fams}, expected only ['{s.info['face']}']")
    img_refs = []
    for n in d.root.iter("img", "source", "video"):
        img_refs += [n.attrs[k] for k in ("src", "poster") if k in n.attrs]
        img_refs += srcset_urls(n.attrs.get("srcset", ""))
    img_refs = [r for r in img_refs + [u for u in css_urls(all_css)]
                if r and not r.startswith(("data:", "#", "http://", "https://", "//"))]
    for ref in (r.removeprefix("./") for r in img_refs):
        rel = ref.split("?")[0].split("#")[0]
        path = (s.site / rel).resolve()
        if not ref.startswith("img/"):
            fail(f"AC73 {slug}: image not in img/: {ref}")
        elif not path.is_file() or s.img.resolve() not in path.parents:
            fail(f"AC73 {slug}: image path does not resolve to a file in img/: {ref}")
        elif not exact_case(s.site, rel):
            fail(f"AC73 {slug}: image path differs in letter case from the file (GitHub Pages is case-sensitive): {ref}")


def cards(sec, ac, slug, want):  # <figure> cards of a section: `want` of them, each one <img> and a Hangul <figcaption>
    figs = list(sec.iter("figure"))
    if len(figs) != want:
        fail(f"{ac} {slug}: the example section holds {len(figs)} <figure> cards, needs exactly {want}")
    for f in figs:
        caps = list(f.iter("figcaption"))
        if len(list(f.iter("img"))) != 1 or len(caps) != 1 or not re.search(r"[가-힣]", norm(caps[0].text())):
            fail(f"{ac} {slug}: a card needs exactly one <img> and one <figcaption> with a Hangul syllable: "
                 f"{norm(f.text())[:40]!r}")


def header_nav(d, ac, slug):  # a <nav> in the <header> with at least four links to '#…'
    h = header(d)
    navs = [[a for a in nav.iter("a")] for nav in h.iter("nav")] if h else []
    if not any(len(n) >= 4 and all(a.attrs.get("href", "").startswith("#") for a in n) for n in navs):
        fail(f"{ac} {slug}: the <header> has no <nav> with at least four links, each with an href starting with '#'")


def check_sample_a(s, html, css, d):  # AC113 AC120 AC121 AC122 (static parts) AC128 AC131 AC132
    slug = s.slug
    header_nav(d, "AC113", slug)
    ex = section(d, "example", slug, quiet=True)
    first = next(d.root.iter("img"), None)
    if first is None or first.parent is None:
        fail(f"AC120 {slug}: no <img> on the page")
    else:
        holder = first.parent
        if len(list(holder.iter("img"))) != 1 or next(holder.iter("button"), None) is not None:
            fail(f"AC120 {slug}: the element holding the first <img> (<{holder.tag}>) needs exactly one <img> and no "
                 f"<button>")
        caps = [a for a in holder.iter("a") if "hero-caption" in a.classes()]
        if len(caps) != 1:
            fail(f'AC121 {slug}: expected one <a class="hero-caption"> beside the first <img>, found {len(caps)}')
        for a in caps:
            t = norm(a.text())
            if not ex or a.attrs.get("href") != "#" + ex.attrs["id"] or "예시" not in t:
                fail(f"AC121 {slug}: the caption needs href='#<example section id>' and '예시' in its text: {t!r}")
            if not re.search(r"[가-힣]", t) or re.search(r"[0-9A-Za-z]", unicodedata.normalize("NFKC", t)):
                fail(f"AC122 {slug}: the caption needs a Hangul syllable, no digit and no Latin letter: {t!r}")
    if ex:
        cards(ex, "AC128", slug, 3)
    else:
        fail(f"AC128 {slug}: no example section, so its cards were not checked")
    faq, proc, con = (section(d, k, slug, quiet=(k != "faq")) for k in ("faq", "process", "contact"))
    if faq:
        det = list(faq.iter("details"))
        if len(det) < 4:
            fail(f"AC131 {slug}: the FAQ section has {len(det)} <details>, needs 4")
        for x in det:
            sm = next(x.iter("summary"), None)
            if sm is None or not re.search(r"[가-힣]", norm(sm.text())):
                fail(f"AC131 {slug}: a <details> has no <summary> with a Hangul syllable")
        if not (proc and con and proc.order < faq.order < con.order):
            fail(f"AC132 {slug}: the order must be process section, FAQ section, contact section")


def check_sample_b(s, html, css, d):  # AC144 AC151 (static part) AC160 AC161 AC164 AC165
    slug = s.slug
    wm, h = wordmark(d), header(d)
    if wm is None:
        fail(f'AC144 {slug}: no <a class="wordmark"> in the first <header>')
    if wm is not None:
        if squash(wm.name()) != "로빈디자인" or squash(wm.text()) != "로빈디자인":
            fail(f"AC144 {slug}: the wordmark must be live text 로빈디자인 with that accessible name "
                 f"(text {norm(wm.text())!r}, name {wm.name()!r})")
        if next(wm.iter("img"), None) is not None:
            fail(f"AC144 {slug}: the wordmark holds an <img>; it must be live text")
        if wm.up(lambda n: "wordmark-block" in n.classes()) is None:
            fail(f'AC144 {slug}: the wordmark is not inside an element with class "wordmark-block"')
        kin = set(id(x) for x in wm.iter()) | {id(wm)}
        n = wm.parent
        while n is not None:
            kin.add(id(n))
            n = n.parent
        for x in h.iter():
            if id(x) not in kin and "로빈디자인" in (squash(x.text()), squash(x.attrs.get("aria-label", "")),
                                                  squash(x.attrs.get("alt", ""))):
                fail(f"AC144 {slug}: the <header> holds a second element named 로빈디자인 (<{x.tag}>)")
    header_nav(d, "AC151", slug)
    ex = section(d, "example", slug, quiet=True)
    if not ex:
        fail(f"AC160 AC161 AC164 {slug}: no example section, so its feature, tiles and photo count were not checked")
    if ex:
        panels = [n for n in ex.iter() if "feature-panel" in n.classes()]
        if len(panels) != 1:
            fail(f'AC159 AC160 {slug}: expected one element with class "feature-panel" in the example section, found '
                 f"{len(panels)}")
        for p in panels:
            hs = [x for x in p.iter("h3", "h4", "h5", "h6")]
            if len(hs) != 1 or not re.search(r"[가-힣]", norm(hs[0].text())) or len(list(p.iter("p"))) != 1:
                fail(f"AC160 {slug}: the feature panel needs one heading with a Hangul syllable and one <p>")
        cards(ex, "AC161", slug, 4)
        n = len(list(ex.iter("img")))
        if n != 5:
            fail(f"AC164 {slug}: the example section holds {n} <img>, needs exactly five")
    found, bad = background_colors(css + "\n" + inline_css(html))
    for b in bad:
        fail(f"AC165 {slug}: a background value the check cannot read: {b}")
    for sel, rgb, alpha in found:
        if max(rgb) - min(rgb) > 0x30 and (rgb not in B_SATURATED or alpha < 1):
            fail(f"AC165 {slug}: '{sel}' paints a saturated background #{'%02x%02x%02x' % rgb} at alpha {alpha:.2f}; "
                 f"only #ee68ae, #0b5f65 and #deb1f1 at full opacity are allowed")


def check_sample_c(s, html, css, d):  # AC180 AC181 (static parts) AC187 AC193
    slug = s.slug
    h1 = next(d.root.iter("h1"), None)
    ems = list(h1.iter("em")) if h1 is not None else []
    if len(ems) != 1:
        fail(f"AC180 {slug}: the <h1> needs exactly one <em>, found {len(ems)}")
    else:
        inner, whole = squash(ems[0].text()), squash(h1.text())
        if not re.search(r"[가-힣]", inner) or len(whole) <= len(inner):
            fail(f"AC181 {slug}: the <em> needs a Hangul syllable and the <h1> needs text outside it: {norm(h1.text())!r}")
    ex = section(d, "example", slug, quiet=True)
    if ex:
        cards(ex, "AC187", slug, 3)
    else:
        fail(f"AC187 {slug}: no example section, so its cards were not checked")
    for what, n in [("heading", x) for x in headings(d)] + [("nav link", a) for nav in d.root.iter("nav") for a in nav.iter("a")]:
        for word in C_NOT_HEADING:
            if word in norm(n.text()).lower():
                fail(f"AC193 {slug}: a {what} contains '{word}': {norm(n.text())[:40]!r}")


def check_sample(s):  # the per-sample static criteria; AC109/AC139/AC170, AC136/AC167/AC192, AC166/AC191 for all
    html, css, d = s.page()
    slug = s.slug
    want_bg, want_fg, ac = s.info["body"]
    for names, want, what in ((("background", "background-color"), want_bg, "background"), (("color",), want_fg, "text")):
        raw, rgb = body_decl(css, names)
        if rgb != hex_rgb(want):
            fail(f"{ac} {slug}: the body {what} colour in style.css is {raw!r}, expected {want} "
                 f"(a top-level body rule; hex or rgb(), var() from :root)")
    ac, words = s.info["words"]
    for w in words:
        if w in (html + css).lower():
            fail(f"{ac} {slug}: index.html or style.css contains '{w}' (any case)")
    if s.info["hex"]:
        ac, hexes = s.info["hex"]
        for hexv in hexes:
            if hexv in css.lower():
                fail(f"{ac} {slug}: style.css contains {hexv}")
    {"A": check_sample_a, "B": check_sample_b, "C": check_sample_c}[s.info["key"]](s, html, css, d)


def check_register(s):  # AC1 (thumb.jpg) AC3 AC4 AC5 (size) AC17 AC86 AC87 AC108 AC138 AC169; AC203 (AC27 AC52-AC62 on the card text)
    slug, info = s.slug, s.info
    e = entry(slug)
    profiles = load_profiles()
    if not e:
        fail(f"AC3 expected one PROFILES entry for {slug}, found {sum(1 for x in profiles if x.get('slug') == slug)}")
    else:
        if (e.get("industry"), e.get("status"), e.get("demo")) != ("interior", "live", True):
            fail(f"AC3 {slug}: entry fields wrong: industry={e.get('industry')} status={e.get('status')} "
                 f"demo={e.get('demo')}")
        if not re.fullmatch(r"로빈[가-힣]+", str(e.get("name", ""))):
            fail(f"AC17 {slug}: PROFILES name {e.get('name')!r} is not 로빈 followed by Hangul syllables only")
        if e.get("name") != info["name"] or [str(x).lower() for x in e.get("palette") or []] != info["palette"]:
            fail(f"{info['ac']} {slug}: PROFILES name and palette are {e.get('name')!r} {e.get('palette')}, expected "
                 f"{info['name']!r} {info['palette']}")
        a = accent_of(e)
        for other in profiles:
            if other is not e and accent_of(other) == a:
                fail(f"AC86 {slug}: accent {a} is also the accent of {other.get('slug')}")
            if other is not e and other.get("industry") == "interior":
                shared = {str(x).lower() for x in e.get("palette") or []} & {str(x).lower() for x in other.get("palette") or []}
                if shared:
                    fail(f"AC86 {slug}: palette hex {sorted(shared)} is also in the palette of {other.get('slug')}")
        card = [str(e.get(k, "")) for k in ("title", "summary")] + [str(x) for x in e.get("features") or []]
        banned_copy(f"AC203 {slug} PROFILES entry", norm(" ".join(card)), card)  # the gallery card text
        css = read(s.site / "style.css") if (s.site / "style.css").is_file() else ""
        if not a or a not in css.lower():
            fail(f"AC87 {slug}: style.css does not contain the PROFILES accent {a}")
    if not re.fullmatch(r"interior-robin[a-z]+", slug):
        fail(f"AC4 {slug}: slug is not 'interior-robin' and lowercase ASCII letters")
    thumb = s.site / "thumb.jpg"
    if thumb.is_file():
        data = thumb.read_bytes()
        if data[:2] != b"\xff\xd8" or data.rstrip(b"\x00\r\n")[-2:] != b"\xff\xd9":
            fail(f"AC5 {slug}: thumb.jpg is not a complete JPEG (no FFD8 start or FFD9 end); re-run profile_thumb.py")
        w, h = sips_size(thumb)
        if w != 1200 or h is None or abs(h * 16 - w * 10) > 16:
            fail(f"AC5 {slug}: thumb.jpg is {w}x{h}, not 1200 wide at 16:10")
    else:
        fail(f"AC1 AC5 {slug}: thumb.jpg missing")


PER_SAMPLE = {"photos": check_photos, "markers": check_markers, "structure": check_structure, "copy": check_copy,
              "a11y": check_a11y, "assets": check_assets, "sample": check_sample, "register": check_register}
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
                if not (s.site / "index.html").is_file() and n not in ("photos", "register"):
                    fail(f"missing file: profile/{s.slug}/index.html ({n} not run)")
                    continue
                try:
                    PER_SAMPLE[n](s)
                except Exception as exc:  # a page the check cannot read is a failure, not a traceback
                    fail(f"{n} {s.slug}: the check stopped: {type(exc).__name__}: {exc}")
    seen = []
    for f in fails:
        if f not in seen:
            seen.append(f)
            print("FAIL", f)
    print(f"{'PASS' if not fails else 'FAIL'}: {' '.join(args)} ({len(seen)} failures)")
    sys.exit(1 if fails else 0)
