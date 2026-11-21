#!/usr/bin/env python3
"""Static checks for the three invest profile samples (no browser, no network). Run from the repository root.

usage: python3 docs/features/2026-11-21-profile-invest/check_static.py <check> [<slug>]
  per sample (all three when <slug> is left out): markers structure copy a11y assets photos sample register
  shared: gallery three current
  all: every check above, for every sample
slugs: invest-robinfamilyoffice (B) invest-robinwealth (C) invest-robincapital (D)
Exit 0 when every named check passes; otherwise prints each failure and exits 1.
The page contract these checks read is the "Fixed parameters" section of tasks.md in this folder.
AC numbers are this feature's spec.md.
"""
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import colorsys
import json
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
FICTION = "가상의 업체이며 금융투자업자가 아닙니다. 투자 권유가 아니며 실제 자문 · 운용 · 상담을 제공하지 않습니다."  # AC31 AC32
RISK = "투자에는 원금 손실 위험이 있으며, 손실은 투자자에게 귀속됩니다."  # AC57
PE_NOTE = "저희가 운용하는 기관전용 사모펀드는 개인의 출자를 받지 않습니다."  # AC77
READ_NOTE = "계약을 체결하기 전에 설명서와 약관을 읽어 보시기 바랍니다."  # AC81
SAMPLES = {
    "invest-robinfamilyoffice": {
        "key": "B", "kind": "자문", "name": "로빈패밀리오피스", "ac": "AC128", "photos": (2, "AC149"),
        "families": ("AC163", ["Gowun Batang", "Grandiflora One"]), "title": "크림 헤더와 짙은 초록 패널의 패밀리오피스",
        "palette": ["#f3eee2", "#18261e", "#123524", "#e3cf8e"], "body": ("#f3eee2", "#18261e", "AC129"),
        "faces": ("chiswick", "inter"), "order": "AC161", "service": None, "contact": ("AC162", "상담"),
        "hex": ("AC165", ("#002a3a", "#06262d", "#bba984", "#806a4d", "#84744d", "#ceb28a", "#f3f1ec", "#3b5542", "#914124")),
        "own": {"AC167": ("세대째", "대대로", "대를 이어", "유서 깊", "전통의", "역사와 전통", "창립", "설립 이래", "명문가", "재벌")}},
    "invest-robinwealth": {
        "key": "C", "kind": "자문", "name": "로빈자산관리", "ac": "AC168", "photos": (1, "AC187"),
        "families": ("AC200", []), "title": "계단처럼 놓은 색 블록 둘과 밝은 실내 사진의 자산관리",
        "palette": ["#fdfbf8", "#211a16", "#efe6dc", "#a6462b"], "body": ("#fdfbf8", "#211a16", "AC169"),
        "faces": ("pjtsans",), "order": "AC198", "service": None, "contact": ("AC199", "상담"),
        "hex": ("AC201", ("#5050a7", "#60b6f6", "#4e3b98", "#5ca1e6", "#4e3f9b", "#5c9de3", "#1b1c52", "#fa4a1f", "#f78230",
                          "#f5ab71", "#f9e49e", "#f6deb7", "#ffdbff")),
        "own": {"AC203": ("인수합병", "M&A", "구조조정", "기업 매각", "자금 조달", "상장 주관")}},
    "invest-robincapital": {
        "key": "D", "kind": "PE", "name": "로빈캐피탈", "ac": "AC204", "photos": (0, "AC235"),
        "families": ("AC236", ["Orbit"]), "title": "보라 지면에 등고선과 분홍 알약을 둔 사모펀드 운용사",
        "palette": ["#230a47", "#f4effc", "#fbf9ff", "#ff6685"], "body": ("#230a47", "#f4effc", "AC205"),
        "faces": ("f37bolton", "bolton"), "order": "AC233", "service": ("AC234", "투자 분야"), "contact": ("AC234", "기업 문의"),
        "hex": ("AC239", ("#160535", "#1a0838", "#1c0a44", "#29155e", "#2a0f6a", "#6021d8", "#b99fff", "#ded7ff", "#ff0078", "#ba0050")),
        "own": {"AC240": ("뉴스레터", "구독", "소식 받기", "보도자료")}},
}
SECTIONS = {  # kind: (AC, pattern of the section's own <h2>)
    "services": ("AC28", r"하는 일|서비스|투자 분야"), "steps": ("AC29", r"절차|과정|방식"), "contact": ("AC30", r"문의|상담")}
ACTIONS = (("AC36", "카카오톡"), ("AC37", "전화"), ("AC38", "네이버 예약"), ("AC39", "네이버 지도"))
# Listed words. A word with a space also matches without it. A word with a Latin letter matches in any case; a word
# made only of Latin capitals and digits matches as a whole word.
ENTRY = {  # AC52-AC55 AC69 AC116: read on the whole page text
    "AC52": ("App Store", "Google Play", "앱스토어", "플레이스토어", "앱 다운로드", "앱 설치", "APK"),
    "AC53": ("계좌번호", "가상계좌", "입금", "송금", "납입", "이체", "계좌 개설", "비대면 개설", "결제", "카드 등록"),
    "AC54": ("케이뱅크", "카카오뱅크", "토스", "농협", "신한", "국민은행", "우리은행", "하나은행", "기업은행", "미래에셋", "한국투자증권",
             "삼성증권", "키움", "페이팔", "Visa", "Mastercard"),
    "AC55": ("로그인", "회원가입", "가입하기", "시작하기", "투자하기", "청약하기", "출자 신청", "포털", "Portal", "Login", "Log in",
             "Sign up", "Get started"),
    "AC69": ("삼성전자", "코스피", "코스닥", "나스닥", "다우", "S&P", "니프티", "비트코인", "ETF"),
    "AC116": ("Asset Management", "Investment Management", "Investment Advisory", "Investment Adviser", "Securities",
              "Investment Trust", "Financial Investment"),
}
RULES = {  # AC60-AC68: read on the page text with the AC31 and AC57 sentences taken out (spec, Acceptance criteria preamble)
    "AC60": ("수익", "원금 보장", "원금 보전", "원금 보호", "손실 보전", "손실 없", "이익 보장", "무위험", "안전한 투자", "안정적", "이율",
             "이자율", "배당", "복리", "불로소득", "패시브 인컴", "IRR", "MOIC", "TVPI", "DPI", "APY", "배수", "초과 성과", "알파"),
    "AC61": ("최고", "최초", "최대", "최다", "최저", "유일", "독보적", "압도적", "1위", "1등", "No.1", "넘버원", "선도", "선두", "리딩",
             "완벽", "보장", "보증", "무조건", "확실", "반드시", "틀림없"),
    "AC62": ("업계 평균", "타사", "경쟁사", "은행보다", "예금보다", "시장 대비", "벤치마크", "지수 대비"),
    "AC63": ("추천 종목", "종목 추천", "추천주", "매수 추천", "매도 추천", "급등", "테마주", "대박", "저점 매수", "목표가", "시그널",
             "주식 방송", "종목 상담", "무료 체험", "유료 회원", "정회원", "VIP", "수익 인증", "리딩방"),
    "AC64": ("등록 완료", "정식 등록", "등록 업체", "인가", "인허가", "허가", "신고 수리", "신고 완료", "라이선스", "금융위원회",
             "금융감독원", "금융당국", "금융투자협회", "제도권", "합법", "심의필", "심사필", "준법감시인", "예금자 보호"),
    "AC65": ("AUM", "운용자산", "운용 자산", "운용 규모", "수탁고", "약정액", "약정 총액", "펀드 규모", "누적", "실적", "트랙레코드",
             "트랙 레코드", "Track Record", "투자 건수", "성과보수", "성과 보수", "후기", "리뷰", "별점", "평점", "만족도", "★", "수상",
             "어워드", "Award", "고객 수", "가입자", "회원 수", "파트너사", "고객사", "출자자 명단"),
    "AC66": ("무료", "공짜", "할인", "이벤트", "선착순", "마감 임박", "프로모션", "쿠폰", "특가", "사은품", "캐시백", "혜택", "수수료 면제",
             "지금 투자", "지금 가입", "소액으로"),
    "AC67": ("호 펀드", "1호", "2호", "3호", "신규 펀드", "펀드 출시", "펀드 가입", "판매 중", "모집 중", "모집 기간", "청약", "최소 가입",
             "최소 투자", "가입 금액", "환매", "만기"),
    "AC68": ("KKR", "블랙스톤", "Blackstone", "칼라일", "Carlyle", "베인", "Bain", "TPG", "CVC", "EQT", "MBK", "IMM", "한앤컴퍼니",
             "스틱", "STIC", "어피니티", "Affinity", "글렌우드", "버데인", "Verdane", "록펠러", "Rockefeller", "Farther", "PJT",
             "타임폴리오", "국민연금", "사학연금", "공무원연금", "교직원공제회", "한국투자공사", "산업은행"),
}
BY_KIND = {  # the 업태 blocks
    "PE": {"AC78": ("개인 투자자", "개인 고객", "개인 출자", "일반 투자자", "누구나", "소액", "재테크", "노후", "자산관리 상담")},
    "자문": {"AC82": ("공동 운용", "합동 운용", "모아서 운용", "펀드처럼"),
           "AC83": ("사모펀드", "출자", "블라인드", "프로젝트 펀드", "비상장 주식 추천", "공모주")},
}
RESERVED = ("금융투자", "증권", "파생", "선물", "집합투자", "투자신탁", "자산운용", "투자자문", "투자일임", "신탁")  # AC115
SLUG_WORDS = ("asset", "advisory", "securities", "trust")  # AC116
EMAIL = re.compile(r"[\w.+-]+@((?:[\w-]+\.)+[A-Za-z]{2,})")
CLOSED = r"휴무|휴관|쉽니다|쉬어요|쉬는 날|쉼"  # AC46
CLOSED_DAY = r"공휴일|일요일|주말|토요일|월요일|화요일|수요일|목요일|금요일"
HOURS = r"\d{1,2}:\d{2}\s*[-–—~～〜]\s*\d{1,2}:\d{2}"  # AC45
UNITS = r"(?:[천백십]\s*)?(?:원|만|억|조|달러|유로|명|건|배|개국|개사|곳|년|호)"
FIGURE = re.compile(rf"\d\s*%|\d\s*{UNITS}|[₩￦$€]\s*\d|\d\s*[₩￦$€]|\d[xX]|[xX]\d|\d\s*\+|\d{{1,3}}(?:,\d{{3}})+")  # AC73
UNIT_FIRST = re.compile(rf"\s*(?:%|{UNITS})")  # AC73: the unit of a number in the block before
NOT_COUNTED = re.compile(r"02-000-0000|000-00-00000|\d{1,2}:\d{2}")  # AC73: three kinds of digit
SYSTEM_COLORS = set("""accentcolor accentcolortext activetext buttonborder buttonface buttontext canvas canvastext field
fieldtext graytext highlight highlighttext linktext mark marktext selecteditem selecteditemtext visitedtext activeborder
activecaption appworkspace buttonhighlight buttonshadow captiontext inactiveborder inactivecaption inactivecaptiontext
infobackground infotext menu menutext scrollbar threeddarkshadow threedface threedhighlight threedlightshadow threedshadow
window windowframe windowtext""".split())
GREY_NAMES = {"black", "white", "gray", "grey", "silver", "dimgray", "dimgrey", "darkgray", "darkgrey", "lightgray",
              "lightgrey", "gainsboro", "whitesmoke"}  # exact greys: no hue to judge
COLOR_NAMES = set("""aliceblue antiquewhite aqua aquamarine azure beige bisque blanchedalmond blue blueviolet brown
    burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod
    darkgreen darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen darkslateblue
    darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dodgerblue firebrick floralwhite
    forestgreen fuchsia ghostwhite gold goldenrod green greenyellow honeydew hotpink indianred indigo ivory khaki
    lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan lightgoldenrodyellow lightgreen
    lightpink lightsalmon lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime
    limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen
    mediumslateblue mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin
    navajowhite navy oldlace olive olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise
    palevioletred papayawhip peachpuff peru pink plum powderblue purple rebeccapurple red rosybrown royalblue
    saddlebrown salmon sandybrown seagreen seashell sienna skyblue slateblue slategray slategrey snow springgreen
    steelblue tan teal thistle tomato turquoise violet wheat yellow yellowgreen""".split())
# Every CSS colour name that is not an exact grey; AC221 and AC249 need hex or rgb() instead
BLOCK = {"p", "li", "dd", "dt", "td", "th", "address", "div", "section", "article", "header", "footer", "ul", "ol",
         "h1", "h2", "h3", "h4", "h5", "h6", "nav", "main", "aside", "figure", "figcaption", "tr", "table", "dl",
         "details", "summary", "blockquote", "body"}
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

    def own(self):  # the element's own text: its direct text nodes
        return norm(" ".join(k for k in self.kids if isinstance(k, str)))

    def text(self, breaks=False, skip=None):  # text; "\n" at block boundaries when breaks is set; skip(node) leaves a subtree out
        out = []

        def walk(n):
            for k in n.kids:
                if isinstance(k, str):
                    out.append(re.sub(r"\s+", " ", k) if breaks else k)  # a line break in the source is a space, not a block
                elif k.tag in SKIP or (skip and skip(k)):
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

    def name(self):  # accessible name: aria-label, else text
        return norm(self.attrs.get("aria-label") or self.text())


class Dom(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.cur, self.n, self.title, self.doc_title = self.root, 0, [], []
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
            if self.cur.up(lambda n: n.tag == "svg") is None:
                self.doc_title.append(data)  # the page's <title>, not an inline SVG <title>
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
            fail(f"AC86 {self.slug}: img/sources.txt missing")
            return []
        return [ln.split() for ln in read(self.sources).splitlines() if ln.strip()]


def headings(d):
    return list(d.root.iter("h1", "h2", "h3", "h4", "h5", "h6"))


def own_h2(sec):  # the <h2> elements whose nearest <section> is sec
    return [h for h in sec.iter("h2") if h.up(lambda n: n.tag == "section") is sec]


def section(d, kind, slug, quiet=False):
    """The one <section id> whose own <h2> matches the pattern of `kind`. The contact section is the one match of
    /문의|상담/ among the sections that match neither the service nor the steps pattern, so '상담 과정' is the steps
    section. None, with a failure, when there is none or more than one."""
    def hits(k):
        return [s for s in d.root.iter("section") if s.attrs.get("id")
                and any(re.search(SECTIONS[k][1], norm(h.text())) for h in own_h2(s))]
    got = hits(kind)
    if kind == "contact":
        other = hits("services") + hits("steps")
        got = [s for s in got if s not in other]
    if len(got) == 1:
        return got[0]
    if not quiet:
        ac, pat = SECTIONS[kind]
        fail(f"{ac} {slug}: expected exactly one <section id> whose own <h2> matches /{pat}/"
             f"{' and neither the service nor the steps pattern' if kind == 'contact' else ''}, found {len(got)} "
             f"{[('#' + s.attrs['id'], norm(own_h2(s)[0].text())) for s in got]}")
    return None


def header(d):
    return next(d.root.iter("header"), None)


def wordmark(d):  # the <a class="wordmark"> in the first <header>
    h = header(d)
    return next((a for a in h.iter("a") if "wordmark" in a.classes()), None) if h else None


def footer(d):
    fs = [f for f in d.root.iter("footer") if not f.up(lambda n: n.tag == "article")]
    return fs[-1] if fs else None


def inline_css(html):  # the CSS inside <style> elements and style="" attributes of index.html
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)
                     + ["[style]{%s}" % unescape(v) for v in re.findall(r"\sstyle\s*=\s*\"([^\"]*)\"", html, re.I)]
                     + ["[style]{%s}" % unescape(v) for v in re.findall(r"\sstyle\s*=\s*'([^']*)'", html, re.I)]
                     + ["body{%s}" % unescape(a or b)  # the style="" of <body> is a rule whose subject is body
                        for a, b in re.findall(r"<body\b[^>]*?\sstyle\s*=\s*(?:\"([^\"]*)\"|'([^']*)')", html, re.I)])


def uncomment(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def css_urls(css):
    out = [u.strip("'\" ") for u in re.findall(r"url\(([^)]*)\)", uncomment(css))]
    out += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", css)
    return out


def css_unescape(t):  # "\2605" and "\C218 \C775" are the characters they name
    t = re.sub(r"\\([0-9a-fA-F]{1,6})\s?", lambda m: chr(int(m.group(1), 16)) if int(m.group(1), 16) < 0x110000 else "", t)
    return re.sub(r"\\(.)", r"\1", t)


def css_content_values(css):  # the whole value of every CSS content: declaration
    return re.findall(r"(?<![\w-])content\s*:\s*((?:\"[^\"]*\"|'[^']*'|[^;}\"'])*)", uncomment(css))


def css_content(css):  # the text a CSS content: declaration draws, read with the page text: every string of the value
    out = []  # joined, escapes decoded, and a counter() read as a digit
    for value in css_content_values(css):
        parts = re.findall(r"\"([^\"]*)\"|'([^']*)'|(counters?\([^)]*\))", value)
        out.append(norm("".join("1" if c else css_unescape(a or b) for a, b, c in parts)))
    return [t for t in out if t]


def attr_texts(d):  # aria-label, title and alt attributes, meta description and og: content
    out = []
    for n in d.root.iter():
        out += [n.attrs[k] for k in ("aria-label", "title", "alt") if n.attrs.get(k)]
        key = (n.attrs.get("name") or n.attrs.get("property") or "").lower()
        if n.tag == "meta" and (key in ("description", "keywords") or key.startswith(("og:", "twitter:"))):
            out.append(n.attrs.get("content", ""))
    return out


def lines(node, skip=None):  # the text of a node, one entry per block
    return [norm(ln) for ln in node.text(breaks=True, skip=skip).split("\n") if ln.strip()]


def blocks(d, css, skip=None):  # the page text, one entry per block
    return lines(d.root, skip) + [norm(" ".join(d.title))] + [norm(t) for t in attr_texts(d)] + css_content(css)


def page_text(d, css):
    return norm(" ".join(blocks(d, css)))


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


def pseudo_positions(css):  # (selectors, value) of every `position` declared for a ::before/::after, in a rule nested in it too
    out = []

    def walk(s, chain):
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
            walk(s[j + 1:k - 1], chain + [norm(head[cut:])])
            i = k
        if any(re.search(r"::?(?:before|after)\b", c, re.I) for c in chain):
            out.extend((" { ".join(chain), v) for k, v in decls("".join(own)) if k == "position")
    walk(uncomment(css), [])
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


def body_overrides(css, names):  # (selector, value, colour) of every rule, at any nesting, whose subject is `body`
    rules = flat_rules(css)
    props = custom_props(top_rules(css))
    out = []
    for sel, body in rules:
        if any(re.search(r"(?:^|[\s>+~])body(?:[.:#\[][^\s>+~]*)?$", x.strip()) for x in sel.split(",")):
            out += [(sel, v, one_color(resolve(v, props))) for k, v in decls(body) if k in names]
    return out


def colors_in(value):
    """The colours written in one CSS value or SVG colour attribute: ([((r, g, b), alpha)], [problem]). Reads #hex and
    rgb()/rgba() with plain numbers. hsl(), a saturated colour name or a malformed colour is a problem (fail closed)."""
    found, bad = [], []
    v = re.sub(r"url\([^)]*\)", " ", value.lower())
    for m in re.finditer(r"rgba?\(([^)]*)\)", v):
        parts = [p for p in re.split(r"[\s,/]+", m.group(1).strip()) if p]
        if len(parts) not in (3, 4) or not all(re.fullmatch(r"\d*\.?\d+", p) for p in parts):
            bad.append(f"{m.group(0)} (write rgb() with plain numbers)")
            continue
        found.append((tuple(int(float(p)) for p in parts[:3]), float(parts[3]) if len(parts) == 4 else 1.0))
    v = re.sub(r"rgba?\([^)]*\)", " ", v)
    if re.search(r"\b(?:hsla?|hwb|lab|lch|oklab|oklch|color|color-mix)\(", v):
        bad.append(f"{value.strip()[:50]} (write every colour as #hex or rgb())")
    for m in re.finditer(r"#([0-9a-f]+)\b", v):
        h = m.group(1)
        if len(h) not in (3, 4, 6, 8):
            bad.append(f"{m.group(0)} (not a hex colour)")
            continue
        h = "".join(c * 2 for c in h) if len(h) in (3, 4) else h
        found.append((hex_rgb(h[:6]), int(h[6:8], 16) / 255 if len(h) == 8 else 1.0))
    for word in re.findall(r"(?<![\w-])[a-z]+(?![\w(-])", re.sub(r"#[0-9a-f]+", " ", v)):
        if word in COLOR_NAMES:
            bad.append(f"the colour name '{word}' (write every colour as #hex or rgb())")
    return found, bad


def all_colors(css):  # every colour in every declaration value of the CSS, var() definitions included: [(selector, rgb, alpha)]
    found, bad, rules = [], [], flat_rules(css)
    defined = {k for _, body in rules for k, _ in decls(body) if k.startswith("--")}
    for sel, body in rules:
        for k, raw in decls(body):
            if k in ("content", "font-family", "font", "animation", "animation-name", "transition", "grid-area",
                     "grid-template-areas") or raw.startswith(("'", '"')):
                continue
            got, problems = colors_in(raw)
            for name in re.findall(r"var\(\s*(--[\w-]+)", raw):  # a colour the check cannot read (fail closed)
                if name.lower() not in defined:
                    problems.append(f"var({name}) that no rule defines")
            if k.startswith("--") or re.search(r"color|background|border|outline|shadow|fill|stroke|decoration|column-rule", k):
                for word in re.findall(r"(?<![\w-])[a-z]+(?![\w(-])", raw.lower()):
                    if word in SYSTEM_COLORS:
                        problems.append(f"the system colour '{word}' (write every colour as #hex or rgb())")
            found += [(sel, rgb, a) for rgb, a in got]
            bad += [f"'{sel}' {k}: {p}" for p in problems]
    return found, bad


def background_colors(css):
    """Every colour in every background, background-color and background-image value, at any nesting, var()
    resolved from every rule that defines the property (each definition is read). Returns
    ([(selector, (r, g, b), alpha)], [problem]). A token that is not a hex colour, an rgb()/rgba() with plain
    numbers, a number, a url() or a known keyword is a problem (fail closed)."""
    rules, defs, found, bad = flat_rules(css), {}, [], []
    for _, body in rules:
        for k, v in decls(body):
            if k.startswith("--"):
                defs.setdefault(k, []).append(v)
    for sel, body in rules:
        for k, raw in decls(body):
            if k not in ("background", "background-color", "background-image"):
                continue
            readings = resolve_all(raw, defs)
            if readings is None:
                bad.append(f"'{sel}' {k}: {raw} (a var() that no rule defines, or one the check cannot resolve)")
                continue
            for v in (r.lower() for r in readings):
                got, problems = colors_in(v)
                found += [(sel, rgb, a) for rgb, a in got]
                bad += [f"'{sel}' {k}: {p}" for p in problems]
                v = re.sub(r"url\([^)]*\)|rgba?\([^)]*\)|#[0-9a-f]+", " ", v)
                v = re.sub(r"-?\d*\.?\d+(?:deg|turn|rad|px|em|rem|vw|vh|vmin|vmax|%)?", " ", v)
                for word in re.findall(r"[a-z][a-z-]*", v):
                    if word not in BG_WORDS and word not in GREY_NAMES and word not in COLOR_NAMES:  # colors_in reports a saturated name
                        bad.append(f"'{sel}' {k}: '{word}' (write every background colour as #hex or rgb())")
    return found, bad


def spread(rgb):
    return max(rgb) - min(rgb)


def hue(rgb):  # HSL hue in degrees
    return colorsys.rgb_to_hls(*(c / 255 for c in rgb))[0] * 360


def lightness(rgb):
    return (max(rgb) + min(rgb)) / 510


def google_families(html, css):  # families requested from fonts.googleapis.com (link or @import)
    fams = []
    for u in re.findall(r"(?:https?:)?//fonts\.googleapis\.com[^\"'\s)]*", unescape(html) + "\n" + css):
        if urlparse(u).path in ("", "/"):  # a preconnect hint, not a request for a family
            continue
        got = parse_qs(urlparse(u).query).get("family", []) if re.search(r"\.com/css2?\?", u) else []
        fams += [fam.split(":")[0].replace("+", " ").strip() for fam in got] or [u]  # /icon, /earlyaccess …: listed as is
    return fams


# --- files -------------------------------------------------------------------------------------------------

def sips_size(path):
    if not shutil.which("sips"):
        fail("sips not found: the thumbnail check needs macOS sips")
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


# --- the word lists ----------------------------------------------------------------------------------------

def fold(t):  # full-width forms, invisible characters, typographic apostrophes and Latin accents folded
    t = "".join(c for c in unicodedata.normalize("NFKC", t) if unicodedata.category(c) not in ("Cf", "Mn"))
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    return unicodedata.normalize("NFC", re.sub(r"([A-Za-z])[\u0300-\u036f]+", r"\1", unicodedata.normalize("NFD", t)))


def word_hits(word, text):  # the matches of one listed word in `text` (already folded)
    if re.fullmatch(r"[A-Z0-9]+", word):  # APY, BTC, ICO …: a whole word, any case
        return list(re.finditer(rf"(?<![A-Za-z0-9]){word}(?![A-Za-z0-9])", text, re.I))
    out = []
    for w in dict.fromkeys((word, word.replace(" ", ""))):  # '원금 보장' and '원금보장'
        out += list(re.finditer(re.escape(w), text, re.I if re.search(r"[A-Za-z]", w) else 0))
    return out


def around(t, m):
    return f"…{t[max(0, m.start() - 20):m.end() + 20]}…"


def banned_words(label, text, lists):
    text = fold(text)
    for ac, words in lists.items():
        for word in words:
            for m in word_hits(word, text):
                fail(f"{ac} {label}: the text contains '{m.group(0)}' (listed word '{word}'): {around(text, m)}")


def figures(label, parts, ac="AC73"):  # AC73: digit forms, per block, and a number block followed by its unit
    prev = ""
    for ln in parts:
        folded = NOT_COUNTED.sub("□", unicodedata.normalize("NFKC", ln))
        m = FIGURE.search(folded)
        if m:
            fail(f"{ac} {label}: '{m.group(0)}' reads as an amount, a rate, a count or a year: {ln[:80]}")
        elif re.fullmatch(r"[\d.,\s]*\d[\d.,\s]*", prev) and UNIT_FIRST.match(folded):
            fail(f"{ac} {label}: the number '{prev.strip()}' is followed by a block that starts with a unit: {ln[:80]}")
        prev = folded


def word_lists(label, text, info):  # AC52-AC55 AC60-AC69 AC116, the 업태 lists and the sample's own list
    text = fold(text)
    banned_words(label, text, {**ENTRY, **BY_KIND[info["kind"]], **info["own"]})
    banned_words(label, text.replace(fold(FICTION), " ").replace(fold(RISK), " "), RULES)


def reserved_names(label, text):  # AC115: 로빈 followed, in the same word or in the next, by a word of 자본시장법 제38조
    for m in re.finditer(r"로빈\S*(?:\s+\S+)?", fold(text)):
        for w in RESERVED:
            if w in m.group(0):
                fail(f"AC115 {label}: 로빈 is followed by the reserved word '{w}': {m.group(0)}")


def photo_id(url):
    m = re.search(r"images\.unsplash\.com/(photo-[0-9]+-[0-9a-f]+)", url, re.I) or \
        re.search(r"images\.pexels\.com/photos/([0-9]+)/", url)
    return m.group(1).lower() if m else None


def mean_luma(path):  # AC190: mean Rec. 709 luma (0-1) of the gamma-encoded pixels, read from a 64x64 copy made by sips
    if not shutil.which("sips"):
        fail("sips not found: the image checks need macOS sips")
        return None
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "small.bmp"
        subprocess.run(["sips", "-z", "64", "64", "-s", "format", "bmp", str(path), "--out", str(out)], capture_output=True)
        data = out.read_bytes() if out.is_file() else b""
    if data[:2] != b"BM":
        return None
    off, w = int.from_bytes(data[10:14], "little"), int.from_bytes(data[18:22], "little", signed=True)
    h, step = abs(int.from_bytes(data[22:26], "little", signed=True)), int.from_bytes(data[28:30], "little") // 8
    row = (w * step + 3) // 4 * 4
    if step not in (3, 4) or w <= 0 or h <= 0 or len(data) < off + row * h:
        return None
    total = 0.0
    for y in range(h):
        for x in range(w):
            b, g, r = data[off + y * row + x * step:off + y * row + x * step + 3]
            total += 0.2126 * r + 0.7152 * g + 0.0722 * b
    return total / (w * h * 255)


def first_part(d, slug):  # elements before the service section in document order (the first section, header included)
    svc = section(d, "services", slug, quiet=True)
    return [n for n in d.root.iter() if svc is None or n.order < svc.order]


def attr_up(n, name):  # an SVG presentation attribute, on the element or inherited from an ancestor up to its <svg>
    while n is not None:
        if name in n.attrs:
            return n.attrs[name].strip().lower()
        if n.tag == "svg":
            return None
        n = n.parent
    return None


# --- shared checks -----------------------------------------------------------------------------------------

def check_gallery():  # AC3 AC114 (no other invest entry) and the generated part of AC111
    gallery = read(ROOT / "profile/index.html")
    profiles = load_profiles()
    count = sum(1 for p in profiles if p.get("industry") == "invest")
    if count != len(SAMPLES) or not re.search(rf'data-filter="invest"[^>]*>[^<]*<sup>{count}</sup>', gallery):
        fail(f"AC111 profile/index.html: the invest filter chip does not show the count {len(SAMPLES)} "
             f"(PROFILES has {count} invest entries; run python3 scripts/build.py)")
    for slug in SAMPLES:
        if f'data-slug="{slug}"' not in gallery:
            fail(f"AC111 profile/index.html has no card for {slug}")
    if re.search(r'class="pf-card pf-empty[^"]*" data-industry="invest"', gallery):
        fail("AC111 profile/index.html still has the invest 준비 중 tile")
    m = re.search(r'<script type="application/json" id="pf-data">(.*?)</script>', gallery, re.S)
    data = json.loads(m.group(1).replace("<\\/", "</")) if m else {}
    for p in profiles:
        if p.get("slug") in SAMPLES and any(data.get(p["slug"], {}).get(k) != p.get(k) for k in ("title", "name", "summary", "features", "palette")):
            fail(f"AC111 profile/index.html: the card data of {p['slug']} is not that of PROFILES (run python3 scripts/build.py)")
    others = [p.get("slug") for p in profiles if p.get("industry") == "invest" and p.get("slug") not in SAMPLES]
    if others:
        fail(f"AC3 AC114 PROFILES has invest entries for other slugs: {others}")


def check_three():  # AC19 AC114 AC241 AC248
    got = {slug: entry(slug) for slug in SAMPLES}
    names = [e.get("name") for e in got.values() if e]
    if len(names) != len(SAMPLES) or len(set(names)) != len(names):
        fail(f"AC19 the invest samples need three different PROFILES names, found {names}")
    if names != [info["name"] for info in SAMPLES.values()]:
        fail(f"AC114 the three invest entries are named {names}, expected {[info['name'] for info in SAMPLES.values()]}")
    seen = {}
    for slug, e in got.items():
        for hexv in {str(x).lower() for x in (e or {}).get("palette") or []}:
            if hexv in seen:
                fail(f"AC241 the palette hex {hexv} is in the palettes of {seen[hexv]} and {slug}")
            seen[hexv] = slug
    dark = []
    for slug in SAMPLES:
        css = read(ROOT / "profile" / slug / "style.css")
        every = css + "\n" + inline_css(read(ROOT / "profile" / slug / "index.html"))
        raw, rgb = body_decl(css, ("background", "background-color"))
        if rgb is None:
            fail(f"AC248 {slug}: the body background in style.css is {raw!r}; the check needs one hex or rgb() colour")
        elif lightness(rgb) < 0.2 or any(c is None or lightness(c) < 0.2 for _, _, c in body_overrides(every, ("background", "background-color"))):
            dark.append(slug)
    if dark != ["invest-robincapital"]:
        fail(f"AC248 the samples whose body background has an HSL lightness below 0.2 are {dark}, expected only invest-robincapital")


def check_current():  # AC113 (the list; last_reconciled is the reconcile task's git command)
    comp = read(ROOT / "docs/current_system/profile-samples/component.md")
    src = next((ln for ln in comp.splitlines() if ln.startswith("**Source:**")), "")
    listed = set(re.findall(r"`([a-z0-9-]+)`", src))
    for slug in SAMPLES:
        if slug not in listed:
            fail(f"AC113 the Source line of profile-samples/component.md does not list `{slug}`")


# --- per-sample checks -------------------------------------------------------------------------------------

def check_markers(s):  # AC8 (text; visibility in check_browser.py) AC13-AC16 AC18 AC20 AC22-AC24 AC57 AC81
    html, css, d = s.page()
    slug = s.slug
    if MARK not in norm(d.root.text()):
        fail(f"AC8 {slug}: page text lacks '{MARK}'")
    if "디자인 샘플" not in norm(" ".join(d.doc_title)):
        fail(f"AC16 {slug}: <title> lacks '디자인 샘플'")
    desc = [m.attrs.get("content", "") for m in d.root.iter("meta") if m.attrs.get("name") == "description"]
    if len(desc) != 1 or "디자인 샘플" not in desc[0]:
        fail(f"AC16 {slug}: expected one meta description whose content contains '디자인 샘플', found {desc}")
    og = [m.attrs.get("content", "") for m in d.root.iter("meta") if m.attrs.get("property") == "og:title"]
    if len(og) != 1 or "디자인 샘플" not in og[0]:
        fail(f"AC16 {slug}: expected one og:title whose content contains '디자인 샘플', found {og}")
    ft = footer(d)
    foot = norm(ft.text()) if ft else ""
    if not ft:
        fail(f"AC13 AC14 AC57 {slug}: no <footer>")
    if MARK not in foot:
        fail(f"AC13 {slug}: footer lacks '{MARK}'")
    if "Website by RobinTech" not in foot:
        fail(f"AC14 {slug}: footer lacks 'Website by RobinTech'")
    if RISK not in foot:
        fail(f"AC57 {slug}: footer lacks the sentence '{RISK}'")
    if s.info["kind"] == "자문" and READ_NOTE not in foot:
        fail(f"AC81 {slug}: footer lacks the sentence '{READ_NOTE}'")
    if not any(m.attrs.get("name") == "robots" and m.attrs.get("content") == "noindex" for m in d.root.iter("meta")):
        fail(f'AC15 {slug}: no <meta name="robots" content="noindex">')
    wm = wordmark(d)
    if not wm:
        fail(f'AC18 {slug}: no <a class="wordmark"> in the first <header>')
    elif wm.name() != s.info["name"] or squash(wm.text()) != s.info["name"] or next(wm.iter("img", "svg"), None) is not None:
        fail(f"AC18 {slug}: the wordmark must be the live text {s.info['name']!r} with that accessible name and no <img> "
             f"or <svg> (name {wm.name()!r}, text {norm(wm.text())!r})")
    if wm and sum(1 for k in wm.kids if not isinstance(k, str)) > 1 and not wm.attrs.get("aria-label"):
        fail(f"AC18 {slug}: a wordmark set in more than one child element needs aria-label={s.info['name']!r}; "
             f"a browser may join the parts with a space")
    addr = re.compile(r"[가-힣0-9]*[가-힣0-9](?<!으)(?:로|길)\s?\d+(?:-\d+)?"
                      r"(?![\d%A-Za-z가-힣~:.-]|,\d|\s?(?:원|분|시|개|인|일|명|번|미터|층|m(?![A-Za-z])))"
                      r"|[가-힣]+동\d*가\s?\d+|\d+(?:-\d+)?\s?번지"
                      r"|[가-힣]+[구군시]\s[가-힣0-9]+동\s?\d+(?:-\d+)?(?![\d가-힣A-Za-z%:.])")  # road-name, 동N가, 번지 and 구 동 lot addresses
    page_lines = lines(d.root)
    if not any("(가상 주소)" in ln for ln in page_lines):
        fail(f"AC20 {slug}: no address with '(가상 주소)' on the page")
    for ln in page_lines:
        if addr.search(ln) and "(가상 주소)" not in ln:
            fail(f"AC20 {slug}: address without '(가상 주소)': {ln[:80]}")
    text = d.root.text(breaks=True) + "\n" + " ".join(attr_texts(d)) + "\n" + " ".join(css_content(css + "\n" + inline_css(html)))
    text = re.sub("[\u2010-\u2015\u2212]", "-", unicodedata.normalize("NFKC", text))  # full-width digits and every dash folded
    phones = re.findall(r"(?<![\d-])(?:0\d{1,3}[-.\s]\d{3,4}|1[5-9]\d{2})[-.\s]\d{4}(?![\d-])", text)
    phones += re.findall(r"\(?0\d{1,3}\)\s?\d{3,4}[-.\s]?\d{4}|\+82[\d\s().-]{7,}", text)
    phones += re.findall(r"(?<![\d-])0(?:2|1[016-9]|[3-6]\d|70|50\d)\d{7,8}(?![\d-])", text)
    for ph in phones:
        if ph != "02-000-0000":
            fail(f"AC22 {slug}: phone number is not 02-000-0000: {ph}")
    brns = re.findall(r"(?<![\d-])\d{3}[-.\s]\d{2}[-.\s]\d{5}(?![\d-])", text)
    if "사업자등록번호" in text and not brns:
        fail(f"AC23 {slug}: '사업자등록번호' without a number 000-00-00000")
    for brn in brns:
        if brn != "000-00-00000":
            fail(f"AC23 {slug}: business registration number is not 000-00-00000: {brn}")
    reg = re.compile(r"(등록\s*번호|등록|허가\s*번호|신고\s*번호|인가\s*번호|인증\s*번호|면허\s*번호|면허)[\s:(\[#는은\-–—]*(?:제\s*)?"
                     r"(?:No\.?\s*)?([0-9][0-9\-]*)")
    for ln in blocks(d, css):  # per block; full-width digits folded
        folded = unicodedata.normalize("NFKC", ln)
        for m in re.finditer(r"(?<!사업자)(?<!사업자 )등록\s*번호|면허\s*번호|허가\s*번호|신고\s*번호|인가\s*번호|인증\s*번호"
                             r"|통신판매업?\s*(?:등록|신고)|제\s*[0-9][0-9\-\s]*(?:[가-힣]+\s*-\s*[0-9][0-9\-\s]*)?호"
                             r"|(?i:(?:registration|licen[cs]e|certificate|certification)\s*(?:no\b\.?|number|#))", folded):
            fail(f"AC24 {slug}: a registration or certificate number other than 사업자등록번호: {m.group(0)} in {ln[:60]}")
        for m in reg.finditer(folded):
            if re.search(r"[1-9]", m.group(2)):
                fail(f"AC24 {slug}: {m.group(1)} with a digit other than 0: {m.group(0)}")
        for m in re.finditer(r"심의\s*번호|심의\s*필", folded):
            fail(f"AC24 {slug}: a review number: {m.group(0)} in {ln[:60]}")


def check_structure(s):  # AC28-AC31 AC36-AC40 AC45-AC51 AC102 AC125
    html, _, d = s.page()
    slug = s.slug
    svc, steps, con = (section(d, k, slug) for k in ("services", "steps", "contact"))
    if svc and max(len(list(svc.iter("li"))), len(list(svc.iter("h3")))) < 3:
        fail(f"AC28 {slug}: the service section names fewer than three things (<li> or <h3> items)")
    if steps and not any(sum(1 for k in ol.kids if isinstance(k, Node) and k.tag == "li") >= 3 for ol in steps.iter("ol")):
        fail(f"AC29 {slug}: the steps section has no <ol> with at least three <li> steps")
    tags = sorted({n.tag for n in d.root.iter("form", "input", "select", "textarea", "button")})
    if tags:
        fail(f"AC48 {slug}: the page has {tags} elements")
    if next(d.root.iter("script"), None) is not None:
        fail(f"AC49 {slug}: the page has a <script> element")
    for n in d.root.iter():
        for k, v in n.attrs.items():
            if re.fullmatch(r"on[a-z]+", k):
                fail(f"AC49 {slug}: an inline event handler: <{n.tag} {k}=…>")
            if v.strip().lower().startswith("javascript:"):
                fail(f"AC49 {slug}: a javascript: URL in <{n.tag} {k}=…>")
    for f in sorted(s.site.rglob("*")) if s.site.is_dir() else []:
        if f.is_file() and f.suffix.lower() in (".js", ".mjs"):
            fail(f"AC49 {slug}: a script file in the folder: {f.relative_to(s.site)}")
    ids = {n.attrs["id"] for n in d.root.iter() if n.attrs.get("id")}
    for a in d.root.iter("a"):
        href = a.attrs.get("href")
        if href is None or not (href == "#" or (href.startswith("#") and href[1:] in ids)):
            fail(f"AC50 {slug}: the link {a.name()[:30]!r} has href={href!r}; it must be '#' or '#<id of an element on the page>'")
    tags = sorted({n.tag for n in d.root.iter("iframe", "embed", "object", "video", "audio")})
    if tags:
        fail(f"AC51 {slug}: the page has {tags} elements")
    tags = sorted({n.tag for n in d.root.iter("details", "summary", "dialog")})
    if tags:
        fail(f"AC125 {slug}: the page has {tags} elements")
    h = header(d)
    navs = [list(nav.iter("a")) for nav in h.iter("nav")] if h else []
    if not any(len(n) >= 3 and all(a.attrs.get("href", "").startswith("#") and re.search(r"[가-힣]", norm(a.text())) for a in n)
               for n in navs):
        fail(f"AC102 {slug}: the <header> has no <nav> with at least three links, each with an href starting with '#' "
             f"and a text with a Hangul syllable")
    if not con:
        return
    links = list(con.iter("a"))
    for ac, word in ACTIONS:
        if not any(word in a.name() for a in links):
            fail(f"{ac} {slug}: the contact section has no link whose accessible name contains '{word}'")
    for a in links:
        hit = [w for _, w in ACTIONS if w in a.name()]
        if len(hit) > 1:
            fail(f"AC40 {slug}: one link names several actions {hit}: '{a.name()}'")
    ls = lines(con)
    if FICTION not in norm(con.text()):
        fail(f"AC31 {slug}: the contact section lacks the sentence '{FICTION}'")
    if not any(re.search(HOURS, ln) for ln in ls):
        fail(f"AC45 {slug}: the contact section shows no 상담 hours as HH:MM–HH:MM")
    labels = [ls[i - 1] if i and len(ls[i - 1]) <= 12 and not re.search(r"\d:\d", ls[i - 1]) else "" for i in range(len(ls))]

    def closed(ln, lb):
        no = r"휴무일?\s*:?\s*없|에도|없이|문의"  # judged in the blocks that make the match: a label only when it is needed
        if re.search(CLOSED, ln) and re.search(CLOSED_DAY, ln):
            return not re.search(no, ln)
        hit = (re.search(CLOSED, lb) and re.search(CLOSED_DAY, ln)) or (re.search(CLOSED_DAY, lb) and re.search(CLOSED, ln))
        return hit and not re.search(no, lb + " " + ln)
    if not any(closed(ln, lb) for ln, lb in zip(ls, labels)):
        fail(f"AC46 {slug}: the contact section has no closed-days line ({CLOSED} with a day, in one block or split "
             f"over a label of at most 12 characters and the next block)")
    if not any("(가상 주소)" in ln for ln in ls):
        fail(f"AC47 {slug}: the contact section shows no address with '(가상 주소)'")
    if not any("02-000-0000" in ln for ln in ls):
        fail(f"AC47 {slug}: the contact section does not show 02-000-0000")


def check_copy(s):  # AC25 AC26 AC52-AC55 AC60-AC69 AC73 AC115 AC116, AC78 (PE) or AC82 AC83 (자문), AC167 AC203 AC240
    html, css, d = s.page()
    slug = s.slug
    css = css + "\n" + inline_css(html)  # content: strings of <style> and style="" count as page text too
    if any(re.search(r"\b(?:attr|var)\(", re.sub(r"\"[^\"]*\"|'[^']*'", "", v)) for v in css_content_values(css)):
        fail(f"AC60-AC69 {slug}: a CSS content: uses attr() or var(); the check cannot read that text, write the string")
    text = fold(page_text(d, css))
    word_lists(slug, text, s.info)
    reserved_names(slug, text)
    figures(slug, blocks(d, css))
    for m in EMAIL.finditer(text):
        if m.group(1).lower() != "example.com":
            fail(f"AC25 {slug}: an e-mail address outside example.com: {m.group(0)}")
    for m in re.finditer(r"(?<![\w.+-])@[A-Za-z0-9_.가-힣]{2,}", text):
        fail(f"AC26 {slug}: a social handle: {m.group(0)}")
    for m in re.finditer(r"(?<![A-Za-z0-9@.-])((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})(?![A-Za-z0-9@-])", text, re.I):
        if m.group(1).lower() != "example.com" and not re.search(r"\.(?:jpe?g|png|webp|gif|svg|css|html?|txt|js)$", m.group(1), re.I):
            fail(f"AC26 {slug}: a domain name: {m.group(1)}")


def check_a11y(s):  # AC33 AC34 (stylesheet) AC94 AC95 (the block; its effect in check_browser.py) AC118 (stylesheet)
    html, css, d = s.page()
    if not re.search(r"word-break\s*:\s*keep-all", uncomment(css)):
        fail(f"AC34 {s.slug}: style.css has no word-break: keep-all")
    if not re.search(r"@media[^{]*prefers-reduced-motion\s*:\s*reduce", uncomment(css)):
        fail(f"AC95 {s.slug}: style.css has no @media (prefers-reduced-motion: reduce) block")
    for sel, v in pseudo_positions(css + "\n" + inline_css(html)):  # a bar drawn as ::before/::after is not counted in the browser
        if re.sub(r"!\s*important", "", v, flags=re.I).strip().lower() not in ("absolute", "relative", "static"):
            fail(f"AC118 {s.slug}: the rule '{sel}' sets position: {v} on a ::before/::after; "
                 f"only absolute, relative and static are read (a fixed or sticky bar is an element)")
    html_tag = next(d.root.iter("html"), None)
    if html_tag is None or html_tag.attrs.get("lang") != "ko":
        fail(f'AC94 {s.slug}: <html> does not have lang="ko"')
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
        fail(f"AC33 {s.slug}: the <h1> has no Hangul syllable: {h1[0]!r}")


def check_assets(s):  # AC1 (page files) AC2 AC56 AC85 AC89 AC93 AC99 AC120 (the link) AC122 AC127, AC149 / AC187 / AC235 (the <img>), AC163 / AC200 / AC236 (families)
    html, css, d = s.page()
    slug = s.slug
    for name in ("index.html", "style.css"):
        if not (s.site / name).is_file():
            fail(f"AC1 missing profile/{slug}/{name}")
    want_img = s.info["photos"][0] > 0
    for f in sorted(s.site.rglob("*")):
        rel = f.relative_to(s.site)
        if f.is_file() and not any(part.startswith(".") for part in rel.parts) and str(rel) not in ("index.html", "style.css", "thumb.jpg") \
                and not (want_img and len(rel.parts) == 2 and rel.parts[0] == "img"):
            fail(f"AC1 {slug}: a file other than index.html, style.css, thumb.jpg{' and the files of img/' if want_img else ''} "
                 f"in the folder: {rel}")
    all_css = css + "\n" + inline_css(html)
    refs = []
    for n in d.root.iter():
        refs += [n.attrs[k] for k in ("src", "href", "poster", "data") if k in n.attrs]
        refs += [part.strip().split()[0] for part in n.attrs.get("srcset", "").split(",") if part.strip()]
    for ref in refs + css_urls(all_css):
        if ref.lower().startswith(("http://", "https://", "//", "data:", "#")):
            continue
        if ref.startswith("/") or "../" in ref or "assets/" in ref:
            fail(f"AC2 {slug}: reference leaves the sample folder: {ref}")
    if "../" in html + css or re.search(r"\bassets/", html + css):
        fail(f"AC2 {slug}: index.html or style.css contains '../' or 'assets/'")

    def font_host(u):
        return u.netloc == "fonts.googleapis.com" or (u.netloc == "cdn.jsdelivr.net" and pretendard(u.path))

    def pretendard(path):  # the Pretendard package itself, not any jsDelivr path with the word in it
        return path.lower().startswith(("/gh/orioncactus/pretendard@", "/npm/pretendard@"))
    for link in d.root.iter("link"):
        href = link.attrs.get("href", "")
        if "stylesheet" in link.attrs.get("rel", "").lower() and href.lower().startswith(("http", "//")):
            if not font_host(urlparse(href if not href.startswith("//") else "https:" + href)):
                fail(f"AC99 {slug}: external stylesheet not allowed: {href}")
    for url in re.findall(r"(?:https?:)?//cdn\.jsdelivr\.net/[^\s\"'()<>,]+", html + css):
        if not pretendard(urlparse(url if not url.startswith("//") else "https:" + url).path):
            fail(f"AC99 {slug}: a cdn.jsdelivr.net load that is not Pretendard: {url}")
    for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", all_css):
        u = urlparse(imp)
        if u.netloc and not font_host(u):
            fail(f"AC99 {slug}: external @import not allowed: {imp}")
    if re.search(r"@font-face", all_css, re.I):
        fail(f"AC99 {slug}: an @font-face rule; fonts come only from the Google Fonts and Pretendard stylesheets")
    for url in re.findall(r"(?i)https?://[^\s\"'()<>,]+|(?<![\w:/])//[\w-]+(?:\.[\w-]+)+[^\s\"'()<>,]*", unescape(html) + "\n" + uncomment(all_css)):
        if url.lower().startswith("http://www.w3.org/"):  # an XML namespace (inline SVG), not a load
            continue
        if urlparse(url if not url.startswith("//") else "https:" + url).netloc.lower() not in ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net"):
            fail(f"AC56 {slug}: URL with a host that is not allowed: {url}")
    if not any("stylesheet" in ln.attrs.get("rel", "").lower() and font_host(urlparse(ln.attrs.get("href", "")))
               and urlparse(ln.attrs.get("href", "")).netloc == "cdn.jsdelivr.net" for ln in d.root.iter("link")):
        fail(f"AC120 {slug}: index.html has no <link rel=\"stylesheet\"> to Pretendard on cdn.jsdelivr.net; the body face would be a fallback")
    ac, want = s.info["families"]
    fams = sorted(set(google_families(html, css)))
    if fams != want:
        fail(f"{ac} {slug}: fonts.googleapis.com is asked for {fams}, expected exactly {want}")
    for f in sorted(s.site.rglob("*")) if s.site.is_dir() else []:
        if f.is_file() and f.suffix.lower() in (".svg", ".png", ".gif"):
            fail(f"AC122 {slug}: a picture file in the folder; pictures that are not photos are CSS and inline <svg>: {f.relative_to(s.site)}")
    if re.search(r"(?<![\w-])data\s*:", html + css, re.I):
        fail(f"AC122 {slug}: a data: URL (a picture is an inline <svg> element or CSS; text and colours inside a data: URL are not read)")
    if next(d.root.iter("picture", "source"), None) is not None:
        fail(f"AC89 {slug}: the page has a <picture> or <source> element; a photo is one <img>")
    for img in d.root.iter("img"):
        if not img.attrs.get("src", "").startswith("img/") or "alt" not in img.attrs:
            fail(f"AC89 {slug}: an <img> needs a src that starts with img/ and an alt attribute: src={img.attrs.get('src')!r}")
    local = [u for u in css_urls(all_css) if u and not u.startswith(("http://", "https://", "//", "data:", "#"))]
    if local:
        fail(f"AC89 {slug}: a CSS url() points at a local file; a photo is an <img> element: {local[:3]}")
    photo_markup(s, d)
    fonts = [v for k, v in (kv for _, body in flat_rules(all_css) for kv in decls(body)) if k in ("font-family", "font") or k.startswith("--")]
    fonts += [n.attrs["font-family"] for n in d.root.iter() if n.attrs.get("font-family")]  # an SVG presentation attribute
    fonts += re.findall(r"(?:https?:)?//fonts\.(?:googleapis|gstatic)\.com[^\"'\s)]*", unescape(html) + "\n" + all_css)
    for word in s.info["faces"]:
        if any(re.search(rf"(?<![a-z0-9]){word}(?![a-z0-9])", v.lower().replace("+", " ")) for v in fonts):
            fail(f"AC127 {slug}: a font-family value or a font URL names a typeface of the reference ('{word}', any case)")


def check_photos(s):  # the files of img/: AC86 AC87 AC88 AC124, the file count of AC149 / AC187, AC190 (C), and no img/ in D (AC85 AC235)
    slug = s.slug
    want, ac = s.info["photos"]
    files = s.image_files()
    if want == 0:
        if not (s.site / "index.html").is_file():
            fail(f"missing file: profile/{slug}/index.html (photos not run)")
        if s.img.exists():
            fail(f"AC85 {ac} {slug}: a sample with no photo has no img/ folder")
        return
    if len(files) != want:
        fail(f"{ac} {slug}: img/ holds {len(files)} image file(s), needs exactly {want}")
    for sub in (f for f in s.img.rglob("*") if f.is_dir()) if s.img.is_dir() else []:
        fail(f"AC88 {slug}: img/ holds a folder, whose files no photo check reads: {sub.relative_to(s.site)}")
    total = 0
    for f in files:
        head = f.read_bytes()[:12]
        if f.suffix.lower() not in (".jpg", ".jpeg", ".webp") or not (head[:2] == b"\xff\xd8" or (head[:4] == b"RIFF" and head[8:12] == b"WEBP")):
            fail(f"AC88 {slug}: not a JPEG or WebP file: img/{f.name}")
        size = f.stat().st_size
        total += size
        if size > 500 * 1024:
            fail(f"AC88 {slug}: larger than 500 KB: img/{f.name} ({size // 1024} KB)")
        w, _ = sips_size(f)
        if w is None or w > 2000:
            fail(f"AC88 {slug}: wider than 2000 px or unreadable: img/{f.name} ({w})")
    if total > 3 * 1024 * 1024:
        fail(f"AC88 {slug}: img/ totals {total / 1024 / 1024:.2f} MB > 3 MB")
    rows = s.source_lines()
    names = [ln[0] for ln in rows if ln]
    for ln in rows:
        if len(ln) != 3:
            fail(f"AC86 {slug}: sources.txt line is not '<file> <page URL or -> <download URL>': {' '.join(ln)}")
            continue
        _, page_url, dl = ln
        if page_url != "-" and not page_url.startswith(("https://unsplash.com/photos/", "https://www.pexels.com/photo/")):
            fail(f"AC86 {slug}: page URL is not an Unsplash/Pexels photo page or '-': {page_url}")
        if urlparse(dl).scheme != "https" or urlparse(dl).netloc not in ("images.unsplash.com", "images.pexels.com"):
            fail(f"AC87 {slug}: the downloaded URL's host is not images.unsplash.com or images.pexels.com: {dl}")
    if sorted(names) != [f.name for f in files] or len(set(names)) != len(names):
        fail(f"AC86 {slug}: sources.txt files {sorted(names)} != img/ files {[f.name for f in files]}")
    raw = read(s.sources) if s.sources.is_file() else ""
    if "plus.unsplash.com" in raw or "premium_photo" in raw:
        fail(f"AC87 {slug}: sources.txt mentions plus.unsplash.com or premium_photo")
    taken = {}
    for path in sorted((ROOT / "profile").glob("*/img/sources.txt")):
        if path.parent.parent.name == slug:
            continue
        for ln in read(path).splitlines():
            pid = photo_id(ln)
            if pid:
                taken[pid] = str(path.relative_to(ROOT))
    own = []
    for ln in rows:
        pid = photo_id(ln[-1]) if ln else None
        if ln and not pid:
            fail(f"AC124 {slug}: no photo ID can be read from the downloaded URL, so it cannot be compared: {ln[-1]}")
        if pid and (pid in taken or pid in own):
            fail(f"AC124 {slug}: photo {pid} is also recorded in {taken.get(pid, 'this sources.txt')}")
        own.append(pid)
    if s.info["key"] == "C" and files:
        luma = mean_luma(files[0])
        if luma is None or luma < 0.55:
            fail(f"AC190 {slug}: the photo img/{files[0].name} has a mean luminance of {luma if luma is None else round(luma, 3)}, below 0.55")


def photo_markup(s, d):  # the page side of the photos: AC85 AC93, and AC149 / AC187 / AC235
    slug = s.slug
    want, ac = s.info["photos"]
    imgs = list(d.root.iter("img"))
    ft = footer(d)
    foot = norm(ft.text()) if ft else ""
    if want == 0:
        if imgs:
            fail(f"AC85 {ac} {slug}: a sample with no photo has no <img> element (found {len(imgs)})")
        if "Photos:" in foot:
            fail(f"AC93 {slug}: the footer has a 'Photos:' credit, and the sample has no photo")
        return
    first = {n.order for n in first_part(d, slug)}
    if len(imgs) != want or any(i.attrs.get("alt") != "" or i.order not in first for i in imgs):
        fail(f"{ac} {slug}: the page needs exactly {want} <img>, each with alt=\"\" and before the service section (found {len(imgs)})")
    used = {i.attrs.get("src", "") for i in imgs}
    for f in s.image_files():
        if f"img/{f.name}" not in used:
            fail(f"{ac} {slug}: img/{f.name} is not the src of an <img>")
    raw = read(s.sources) if s.sources.is_file() else ""
    credit = foot.split("Photos:", 1)[1] if "Photos:" in foot else ""
    if not credit:
        fail(f"AC93 {slug}: footer has no 'Photos:' credit")
    for host, name in (("images.unsplash.com", "Unsplash"), ("images.pexels.com", "Pexels")):
        if (host in raw) != (name in credit):
            fail(f"AC93 {slug}: the footer's 'Photos:' credit {'does not name' if host in raw else 'names'} {name}, and "
                 f"sources.txt {'has a' if host in raw else 'has no'} {host} URL")


def check_sample_b(s, html, css, d):  # AC140 AC142 AC166
    slug = s.slug
    svgs = [n for n in first_part(d, slug) if n.tag == "svg" and header(d) is not None and n.up(lambda x: x is header(d)) is None]
    if len(svgs) != 1 or svgs[0].attrs.get("aria-hidden") != "true":
        fail(f'AC140 {slug}: the first section, the <header> aside, needs exactly one inline <svg aria-hidden="true"> (the pattern), found {len(svgs)}')
    else:
        for n in svgs[0].iter():
            if n.tag in ("g", "defs", "title", "desc"):
                continue
            d_attr = n.attrs.get("d", "")
            if n.tag == "line" or (n.tag in ("path", "polyline") and attr_up(n, "fill") == "none"
                                   and not re.search(r"[A-Za-z]", re.sub(r"[MLHVZmlhvz]", "", d_attr))):
                continue
            fail(f"AC140 {slug}: the pattern holds a <{n.tag}> that is not a <line>, nor a <path> or <polyline> with "
                 f"fill=\"none\" (on it or on the <svg>) and only M, L, H, V and Z commands: {d_attr[:40]!r}")
    h1 = next(d.root.iter("h1"), None)
    if h1 is not None:
        kids = [k for k in h1.kids if isinstance(k, Node)]
        texts = [norm(k.text()) for k in kids]
        if [k.tag for k in kids] != ["span", "em"] or h1.own() or any(not re.search(r"[가-힣]", t) or re.search(r"[A-Za-z]", t) for t in texts):
            fail(f"AC142 {slug}: the <h1> needs exactly one child <span> then one child <em> and no text outside them, each "
                 f"with a Hangul syllable and no Latin letter (children {[k.tag for k in kids]}, own text {h1.own()!r})")
    found, bad = background_colors(css + "\n" + inline_css(html))
    for b in bad:
        fail(f"AC166 {slug}: a background value the check cannot read: {b}")
    for sel, rgb, _ in found:
        if lightness(rgb) < 0.3 and spread(rgb) > 0x18 and not 135 <= hue(rgb) <= 165:
            fail(f"AC166 {slug}: '{sel}' paints the dark background #{'%02x%02x%02x' % rgb} (hue {hue(rgb):.0f}°); a dark "
                 f"saturated background needs a hue from 135° to 165°")


def check_sample_c(s, html, css, d):  # AC173 (the two hex values) AC183 (markup) AC197 (markup) AC202
    slug = s.slug
    for h in ("#b5533a", "#8f3a24"):
        if h not in css.lower():
            fail(f"AC173 {slug}: style.css does not contain {h}")
    h1 = next(d.root.iter("h1"), None)
    if h1 is not None:
        kids = [k for k in h1.kids if isinstance(k, Node)]
        if [k.tag for k in kids] != ["span"] * 3 or h1.own() or any(not norm(k.text()) for k in kids):
            fail(f"AC183 {slug}: the <h1> needs exactly three child <span> elements with text and no text outside them "
                 f"(children {[k.tag for k in kids]}, own text {h1.own()!r})")
    svc = section(d, "services", slug, quiet=True)
    if svc and not any(sum(1 for k in ul.kids if isinstance(k, Node) and k.tag == "li") >= 4 for ul in svc.iter("ul")):
        fail(f"AC197 {slug}: the service section has no <ul> with at least four <li>")
    found, bad = all_colors(css + "\n" + inline_css(html))
    for b in bad:
        fail(f"AC202 {slug}: a colour the check cannot read: {b}")
    for sel, rgb, _ in found:
        if spread(rgb) > 0x30 and not 5 <= hue(rgb) <= 40:
            fail(f"AC202 {slug}: '{sel}' uses #{'%02x%02x%02x' % rgb} (hue {hue(rgb):.0f}°); a colour with a channel spread "
                 f"above 0x30 needs a hue from 5° to 40°")


def check_sample_d(s, html, css, d):  # AC214 AC237, AC239 (inline SVG)
    slug = s.slug
    svgs = [n for n in first_part(d, slug) if n.tag == "svg" and n.attrs.get("aria-hidden") == "true" and n.up(lambda x: x.tag == "a") is None]
    if len(svgs) != 1:
        fail(f'AC213 AC214 {slug}: the first section needs exactly one inline <svg aria-hidden="true"> outside a link (the contours), found {len(svgs)}')
    else:
        paths = list(svgs[0].iter("path"))
        bad = sorted({n.tag for n in svgs[0].iter("text", "line", "rect", "polyline", "image")})
        if len(paths) < 8 or bad:
            fail(f"AC214 {slug}: the contours need at least eight <path> and no <text>, <line>, <rect>, <polyline> or <image> "
                 f"(found {len(paths)} <path>, {bad})")
        for p in paths:
            if attr_up(p, "fill") != "none" or attr_up(p, "stroke") in (None, "", "none") or not re.search(r"[CSQTAcsqta]", p.attrs.get("d", "")):
                fail(f"AC214 {slug}: a contour <path> needs fill=\"none\" and a stroke (on it or on the <svg>) and a curve "
                     f"command in its path data: {p.attrs.get('d', '')[:40]!r}")
    found, bad = all_colors(css + "\n" + inline_css(html))
    for svg in d.root.iter("svg"):
        for n in [svg, *svg.iter()]:
            for k in ("fill", "stroke", "stop-color", "flood-color", "lighting-color", "color"):
                if k in n.attrs:
                    got, problems = colors_in(n.attrs[k])
                    found += [(f"<{n.tag} {k}>", rgb, a) for rgb, a in got]
                    bad += [f"<{n.tag} {k}>: {p}" for p in problems]
    for b in bad:
        fail(f"AC237 {slug}: a colour the check cannot read: {b}")
    for sel, rgb, _ in found:
        if spread(rgb) > 0x30 and rgb != (0xFF, 0x66, 0x85) and not 240 <= hue(rgb) <= 285:
            fail(f"AC237 {slug}: '{sel}' uses #{'%02x%02x%02x' % rgb} (hue {hue(rgb):.0f}°); a colour with a channel spread "
                 f"above 0x30 is #ff6685 or has a hue from 240° to 285°")
    ac, hexes = s.info["hex"]
    for hexv in hexes:
        if hexv in unescape(html).lower():
            fail(f"{ac} {slug}: index.html contains {hexv}")


def check_sample(s):  # AC129 / AC169 / AC205, AC161 / AC198 / AC233, AC162 / AC199 / AC234, AC165 / AC201 / AC239, then per sample
    html, css, d = s.page()
    slug = s.slug
    want_bg, want_fg, ac = s.info["body"]
    for names, want, what in ((("background", "background-color"), want_bg, "background"), (("color",), want_fg, "text")):
        raw, rgb = body_decl(css, names)
        if rgb != hex_rgb(want):
            fail(f"{ac} {slug}: the body {what} colour in style.css is {raw!r}, expected {want} "
                 f"(a top-level body rule; hex or rgb(), var() from :root)")
        for sel, v, c in body_overrides(css + "\n" + inline_css(html), names):
            if c != hex_rgb(want):
                fail(f"{ac} {slug}: the rule '{sel}' sets the body {what} colour to {v!r}, expected {want} in every rule")
    ac, hexes = s.info["hex"]
    for hexv in hexes:
        if hexv in (css + "\n" + inline_css(html)).lower():
            fail(f"{ac} {slug}: style.css contains {hexv}")
    svc, steps, con = (section(d, k, slug, quiet=True) for k in ("services", "steps", "contact"))
    for sec, key in ((svc, "service"), (con, "contact")):
        if s.info[key]:
            ac, word = s.info[key]
            if not sec or not any(word in norm(h.text()) for h in own_h2(sec)):
                fail(f"{ac} {slug}: the {key} section's heading does not contain '{word}'")
    order = [svc, steps, con]
    if s.info["key"] == "C":
        order.insert(0, next((n for n in d.root.iter("p") if "statement" in n.classes()), None))
    if any(x is None for x in order) or [x.order for x in order] != sorted(x.order for x in order):
        fail(f"{s.info['order']} {slug}: the order must be {'the statement (<p class=\"statement\">), ' if s.info['key'] == 'C' else ''}"
             f"the service section, the steps section, the contact section")
    {"B": check_sample_b, "C": check_sample_c, "D": check_sample_d}[s.info["key"]](s, html, css, d)


def check_register(s):  # AC1 (thumb.jpg) AC3 AC4 AC5 (size) AC17 AC76 AC105 AC114-AC116 AC123 AC241, AC128 / AC168 / AC204
    slug, info = s.slug, s.info
    e = entry(slug)
    profiles = load_profiles()
    if not e:
        fail(f"AC3 expected one PROFILES entry for {slug}, found {sum(1 for x in profiles if x.get('slug') == slug)}")
    else:
        if (e.get("industry"), e.get("status"), e.get("demo")) != ("invest", "live", True):
            fail(f"AC3 {slug}: entry fields wrong: industry={e.get('industry')} status={e.get('status')} "
                 f"demo={e.get('demo')}")
        if not re.fullmatch(r"로빈[가-힣]+", str(e.get("name", ""))):
            fail(f"AC17 {slug}: PROFILES name {e.get('name')!r} is not 로빈 followed by Hangul syllables only")
        if e.get("name") != info["name"]:
            fail(f"AC114 {slug}: PROFILES name is {e.get('name')!r}, expected {info['name']!r}")
        if [str(x).lower() for x in e.get("palette") or []] != info["palette"] or e.get("title") != info["title"]:
            fail(f"{info['ac']} {slug}: PROFILES palette and title are {e.get('palette')} {e.get('title')!r}, expected "
                 f"{info['palette']} {info['title']!r}")
        a = accent_of(e)
        for other in profiles:
            if other is not e and a in {str(x).lower() for x in other.get("palette") or []}:
                fail(f"AC105 {slug}: the accent {a} is also in the palette of {other.get('slug')}")
            if other is not e and other.get("industry") == "invest":
                shared = {str(x).lower() for x in e.get("palette") or []} & {str(x).lower() for x in other.get("palette") or []}
                if shared:
                    fail(f"AC241 {slug}: palette hex {sorted(shared)} is also in the palette of {other.get('slug')}")
        card = [str(e.get(k, "")) for k in ("title", "summary")] + [str(x) for x in e.get("features") or []]
        label = f"{slug} PROFILES entry (AC76)"
        word_lists(label, norm(" ".join(card)), info)
        figures(label, card, "AC76 AC73")
        for part in [str(e.get("name", "")), *card]:
            reserved_names(label, part)
        css = read(s.site / "style.css") if (s.site / "style.css").is_file() else ""
        if not a or a not in css.lower():
            fail(f"AC123 {slug}: style.css does not contain the PROFILES accent {a}")
    if not re.fullmatch(r"invest-robin[a-z]+", slug):
        fail(f"AC4 {slug}: slug is not 'invest-robin' and lowercase ASCII letters")
    for word in SLUG_WORDS:
        if word in slug[len("invest-robin"):]:
            fail(f"AC116 {slug}: the slug holds '{word}' after invest-robin")
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


PER_SAMPLE = {"markers": check_markers, "structure": check_structure, "copy": check_copy, "a11y": check_a11y,
              "assets": check_assets, "photos": check_photos, "sample": check_sample, "register": check_register}
SHARED = {"gallery": check_gallery, "three": check_three, "current": check_current}

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
            try:
                SHARED[n]()
            except Exception as exc:
                fail(f"{n}: the check stopped: {type(exc).__name__}: {exc}")
        else:
            for s in samples:
                if not (s.site / "index.html").is_file() and n not in ("register", "photos"):
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
