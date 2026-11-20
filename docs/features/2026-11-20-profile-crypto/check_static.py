#!/usr/bin/env python3
"""Static checks for the three crypto profile samples (no browser, no network). Run from the repository root.

usage: python3 docs/features/2026-11-20-profile-crypto/check_static.py <check> [<slug>]
  per sample (all three when <slug> is left out): markers structure copy a11y assets sample register
  shared: gallery three current
  all: every check above, for every sample
slugs: crypto-robincoin (A) crypto-robincustody (B) crypto-robinchain (D)
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
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
FICTION = "가상의 업체이며 가상자산사업자가 아닙니다. 실제 거래 · 보관 · 상담을 제공하지 않습니다."  # AC31
RISK = "가상자산은 가격 변동이 커서 원금의 전부 또는 일부를 잃을 수 있습니다."  # AC58
EXAMPLE = "예시 화면 · 실제 시세가 아닙니다"  # AC77
SAMPLES = {
    "crypto-robincoin": {
        "key": "A", "name": "로빈코인", "ac": "AC150", "families": [], "title": "흰 바탕에 파란 패널과 예시 화면을 둔 거래소",
        "palette": ["#ffffff", "#0c1222", "#eef2f7", "#0a69c7"], "body": ("#ffffff", "#0c1222", "AC151"),
        "ref": ("coinbase", "코인베이스"), "faces": ("coinbasedisplay", "coinbasesans"),
        "hex": ("AC191", ("#0052ff", "#2d60ef", "#001767")), "contact": ("AC189", "고객센터")},
    "crypto-robincustody": {
        "key": "B", "name": "로빈커스터디", "ac": "AC193", "families": ["Noto Sans KR", "Noto Serif KR"],
        "title": "살구색 지면과 흰 알약 헤더의 수탁 서비스",
        "palette": ["#f5c08a", "#2a1d14", "#fffdf9", "#7b2338"], "body": ("#f5c08a", "#2a1d14", "AC194"),
        "ref": ("copper", "코퍼"), "faces": ("regola", "richmond"),
        "hex": ("AC222", ("#fdbda4", "#222426")), "contact": ("AC223", "도입")},
    "crypto-robinchain": {
        "key": "D", "name": "로빈체인", "ac": "AC224", "families": ["Gasoek One"], "title": "검정 지면에 라임 한 색을 쓴 웹3 개발사",
        "palette": ["#07090a", "#f2f5ee", "#161a1c", "#a9ef2c"], "body": ("#07090a", "#f2f5ee", "AC225"),
        "ref": ("kaia", "카이아"), "faces": ("owners-wide", "owners wide", "manrope"),
        "hex": ("AC250", ("#bff009",)), "contact": None},
}
B_SATURATED = ((0xF5, 0xC0, 0x8A), (0x7B, 0x23, 0x38))  # AC221
SECTIONS = {  # kind: (AC, pattern of the section's own <h2>)
    "services": ("AC28", r"서비스|하는 일"), "steps": ("AC29", r"절차|과정|이용 방법"), "contact": ("AC30", r"문의|상담")}
ACTIONS = (("AC35", "카카오톡"), ("AC36", "전화"), ("AC37", "네이버 예약"), ("AC38", "네이버 지도"))
ENTRY_WORDS = ("로그인", "회원가입", "가입하기", "시작하기")  # AC56
# Listed words (spec AC53-AC70). A word with a space also matches without it. A word with a Latin letter matches in
# any case; a word made only of Latin capitals and digits matches as a whole word.
BANNED = {
    "AC53": ("App Store", "Google Play", "앱스토어", "플레이스토어", "앱 다운로드", "APK"),
    "AC54": ("지갑 연결", "지갑 연동하기", "Connect Wallet", "시드 문구", "복구 문구", "니모닉", "개인키 입력", "입금 주소",
             "입금하기", "출금하기", "계좌번호", "가상계좌", "실명계좌"),
    "AC55": ("케이뱅크", "카카오뱅크", "토스", "농협", "신한", "국민은행", "우리은행", "하나은행", "기업은행", "페이팔", "Visa",
             "Mastercard"),
    "AC61": ("수익", "원금 보장", "원금 보전", "원금 보호", "손실 보전", "손실 없", "무위험", "이율", "배당", "APY", "APR", "복리",
             "불로소득", "패시브 인컴"),
    "AC62": ("스테이킹", "예치 상품", "예치 서비스", "렌딩", "대여 서비스", "레버리지", "마진", "선물 거래", "무기한", "옵션 거래",
             "파생", "채굴", "마이닝", "노드 분양", "락업 상품"),
    "AC63": ("매수 추천", "추천 종목", "추천 코인", "유망 코인", "급등", "떡상", "대박", "저점 매수", "지금 사", "목표가", "리딩",
             "시그널", "시세 예측", "가격 전망", "수익 인증"),
    "AC64": ("최고", "최초", "최대", "최다", "최저", "유일", "독보적", "압도적", "1위", "1등", "No.1", "넘버원", "업계 선두", "완벽",
             "보장", "보증", "무조건", "확실"),
    "AC65": ("해킹 불가", "해킹 걱정 없", "무사고", "사고 없", "안전 자산", "안전 보장", "절대 안전", "보험 가입", "보상 한도",
             "예금자 보호"),
    "AC66": ("신고 수리", "신고 완료", "사업자 신고", "신고필", "ISMS", "인증 획득", "인허가", "정식 인가", "인가 완료", "정식 허가",
             "허가 완료", "라이선스", "금융위원회", "금융감독원", "금융정보분석원", "FIU", "금융당국", "제도권", "합법"),
    "AC67": ("후기", "리뷰", "별점", "평점", "만족도", "★", "수상", "어워드", "Award", "누적", "가입자", "회원 수", "이용자 수",
             "거래액", "거래대금", "거래량", "수탁고", "예치금 규모", "운용 자산", "AUM", "TVL", "다운로드 수", "파트너사", "투자사",
             "고객사"),
    "AC68": ("무료", "공짜", "할인", "이벤트", "선착순", "마감 임박", "프로모션", "쿠폰", "특가", "사은품", "에어드랍", "에어드롭",
             "리워드", "캐시백", "추천인", "수수료 면제", "혜택"),
    "AC69": ("업비트", "빗썸", "코인원", "코빗", "고팍스", "바이낸스", "코인베이스", "크라켄", "바이비트", "메타마스크", "팬텀",
             "카이아", "클레이튼", "Upbit", "Bithumb", "Coinone", "Korbit", "Gopax", "Binance", "Coinbase", "Kraken",
             "Bybit", "OKX", "MetaMask", "Phantom", "Kaia", "Klaytn", "Uniswap", "DAXA"),
    "AC70": ("비트코인", "이더리움", "리플", "솔라나", "테더", "도지", "에이다", "바이낸스코인", "Bitcoin", "Ethereum", "Ripple",
             "Solana", "Tether", "Dogecoin", "BTC", "ETH", "XRP", "SOL", "USDT", "USDC", "BNB", "DOGE", "ADA", "TRX"),
}
BANNED_BY_KEY = {  # the 업태 blocks and the per-sample lists
    "A": {"AC85": ("신규 상장", "상장 예정", "거래지원 개시", "원화 마켓 오픈", "거래 대회", "트레이딩 대회", "입금 이벤트"),
          "AC190": ("거래하기", "거래 시작", "지금 거래", "계정 만들기", "계좌 개설", "본인 인증", "인증하기", "간편 가입", "KYC",
                    "가입하기", "시작하기")},
    "B": {},
    "D": {"AC95": ("토큰 세일", "토큰 판매", "ICO", "IDO", "IEO", "프리세일", "화이트리스트", "민팅", "토큰 분배", "토크노믹스", "백서",
                   "로드맵 상장", "거버넌스 토큰", "재단 물량"),
          "AC97": ("앱 실행", "포털 열기", "브리지", "스왑", "Launch App", "Open App", "Bridge", "Swap"),
          "AC251": ("재단", "그랜트", "생태계 기금")},
}
EXAMPLE_BANNED = {"AC82": ("평가손익", "손익", "평가 금액"),  # in the text of an example block
                  "AC167": ("잔고", "보유", "총 자산", "내 자산", "자산 현황", "포트폴리오", "입금", "출금")}
INTEREST_OK = ("개발사", "운영사", "회사")  # AC61: 이자 only as the ending of these three words
EMAIL = re.compile(r"[\w.+-]+@((?:[\w-]+\.)+[A-Za-z]{2,})")
CLOSED = r"휴무|휴관|쉽니다|쉬어요|쉬는 날|쉼"  # AC45
CLOSED_DAY = r"공휴일|일요일|주말|토요일|월요일|화요일|수요일|목요일|금요일"
HOURS = r"\d{1,2}:\d{2}\s*[-–—~～〜]\s*\d{1,2}:\d{2}"  # AC44
FIGURE = re.compile(r"\d\s*%|\d\s*(?:[천백십]\s*)?(?:원|만|억|조|달러|명|건|배|개국)|[₩￦$]\s*\d|\d\s*[₩￦$]|\d{1,3}(?:,\d{3})+")  # AC74
UNIT_FIRST = re.compile(r"\s*(?:%|(?:[천백십]\s*)?(?:원|만|억|조|달러|명|건|배|개국)(?![가-힣]))")  # AC74: the unit of a number in the block before
NOT_COUNTED = re.compile(r"02-000-0000|000-00-00000|\d{1,2}:\d{2}|(?:웹|web)\s?3", re.I)  # AC74: four kinds of digit
SHAPES = ("path", "rect", "line", "polygon", "polyline", "circle", "ellipse")
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
                    out.append(k)
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
        self._page = None

    def page(self):
        if self._page is None:
            html = read(self.site / "index.html")
            self._page = (html, read(self.site / "style.css"), Dom(html))
        return self._page


def headings(d):
    return list(d.root.iter("h1", "h2", "h3", "h4", "h5", "h6"))


def own_h2(sec):  # the <h2> elements whose nearest <section> is sec
    return [h for h in sec.iter("h2") if h.up(lambda n: n.tag == "section") is sec]


def section(d, kind, slug, quiet=False):
    """The one <section id> whose own <h2> matches the pattern of `kind`. None, with a failure, when there is none
    or more than one (a heading such as '상담 절차' matches both the steps and the contact pattern)."""
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


def footer(d):
    fs = [f for f in d.root.iter("footer") if not f.up(lambda n: n.tag == "article")]
    return fs[-1] if fs else None


def is_example(n):
    return isinstance(n, Node) and "data-example" in n.attrs


def example_blocks(d):  # elements with data-example, outermost first in document order
    return [n for n in d.root.iter() if is_example(n)]


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


def css_content(css):  # strings in CSS content: declarations, read with the page text
    return [m[1] for m in re.findall(r"content\s*:\s*([\"'])(.*?)\1", uncomment(css))]


def attr_texts(d):  # aria-label, title and alt attributes, meta description and og: content
    out = []
    for n in d.root.iter():
        out += [n.attrs[k] for k in ("aria-label", "title", "alt") if n.attrs.get(k)]
        if n.tag == "meta" and (n.attrs.get("name") == "description" or n.attrs.get("property", "").startswith("og:")):
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
    found, bad = [], []
    for sel, body in flat_rules(css):
        for k, raw in decls(body):
            if k in ("content", "font-family", "font", "animation", "animation-name", "transition", "grid-area",
                     "grid-template-areas") or raw.startswith(("'", '"')):
                continue
            got, problems = colors_in(raw)
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
    t = re.sub("[\u00ad\u200b-\u200d\u2060\ufeff]", "", unicodedata.normalize("NFKC", t))
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


def interest(label, text):  # AC61: 이자, except as the ending of 개발사이자, 운영사이자 and 회사이자
    for m in re.finditer("이자", text):
        before, after = text[:m.start()], text[m.end():m.end() + 1]
        if not (before.endswith(INTEREST_OK) and not re.match(r"[가-힣]", after)):
            fail(f"AC61 {label}: the text contains 이자 outside 개발사이자, 운영사이자 and 회사이자: {around(text, m)}")


def figures(label, parts, ac="AC74 AC77"):  # AC74: digit forms, per block, and a number block followed by its unit
    prev = ""
    for ln in parts:
        folded = NOT_COUNTED.sub("□", unicodedata.normalize("NFKC", ln))
        m = FIGURE.search(folded)
        if m:
            fail(f"{ac} {label}: '{m.group(0)}' reads as a price, a rate or a count outside an example block: {ln[:80]}")
        elif re.fullmatch(r"[\d.,\s]*\d[\d.,\s]*", prev) and UNIT_FIRST.match(folded):
            fail(f"{ac} {label}: the number '{prev.strip()}' is followed by a block that starts with a unit: {ln[:80]}")
        prev = folded


def wallet_shaped(label, text):  # AC51
    for pat, what in ((r"0x[0-9a-fA-F]{8,}", "0x and eight or more hexadecimal characters"),
                      (r"bc1[0-9A-Za-z]{20,}", "bc1 and twenty or more characters")):
        for m in re.finditer(pat, text):
            fail(f"AC51 {label}: a wallet-address-shaped string ({what}): {m.group(0)[:40]}")
    for m in re.finditer(r"[0-9A-Za-z]{26,}", text):
        if re.search(r"\d", m.group(0)) and re.search(r"[A-Za-z]", m.group(0)):
            fail(f"AC51 {label}: an unbroken run of 26 or more letters and digits: {m.group(0)[:40]}")


# --- shared checks -----------------------------------------------------------------------------------------

def check_gallery():  # AC3 (no other crypto entry) and the generated part of AC137 AC138 AC139
    gallery = read(ROOT / "profile/index.html")
    profiles = load_profiles()
    count = sum(1 for p in profiles if p.get("industry") == "crypto")
    if count != len(SAMPLES) or not re.search(rf'data-filter="crypto"[^>]*>[^<]*<sup>{count}</sup>', gallery):
        fail(f"AC139 profile/index.html: the crypto filter chip does not show the count {len(SAMPLES)} "
             f"(PROFILES has {count} crypto entries; run python3 scripts/build.py)")
    for slug in SAMPLES:
        if f'data-slug="{slug}"' not in gallery:
            fail(f"AC137 profile/index.html has no card for {slug}")
    if re.search(r'class="pf-card pf-empty[^"]*" data-industry="crypto"', gallery):
        fail("AC138 profile/index.html still has the crypto 준비 중 tile")
    m = re.search(r'<script type="application/json" id="pf-data">(.*?)</script>', gallery, re.S)
    data = json.loads(m.group(1).replace("<\\/", "</")) if m else {}
    for p in profiles:
        if p.get("slug") in SAMPLES and any(data.get(p["slug"], {}).get(k) != p.get(k) for k in ("title", "name", "summary", "features", "palette")):
            fail(f"AC6 profile/index.html: the card data of {p['slug']} is not that of PROFILES (run python3 scripts/build.py)")
    others = [p.get("slug") for p in profiles if p.get("industry") == "crypto" and p.get("slug") not in SAMPLES]
    if others:
        fail(f"AC3 PROFILES has crypto entries for other slugs: {others}")


def check_three():  # AC19 AC128
    names = [entry(slug).get("name") for slug in SAMPLES if entry(slug)]
    if len(names) != len(SAMPLES) or len(set(names)) != len(names):
        fail(f"AC19 the crypto samples need three different PROFILES names, found {names}")
    dark = []
    for slug in SAMPLES:
        css = read(ROOT / "profile" / slug / "style.css")
        every = css + "\n" + inline_css(read(ROOT / "profile" / slug / "index.html"))
        raw, rgb = body_decl(css, ("background", "background-color"))
        if rgb is None:
            fail(f"AC128 {slug}: the body background in style.css is {raw!r}; the check needs one hex or rgb() colour")
        elif lightness(rgb) < 0.2 or any(c is None or lightness(c) < 0.2 for _, _, c in body_overrides(every, ("background", "background-color"))):
            dark.append(slug)
    if len(dark) > 1:
        fail(f"AC128 more than one crypto sample has a body background with HSL lightness below 0.2: {dark}")


def check_current():  # AC143
    comp = read(ROOT / "docs/current_system/profile-samples/component.md")
    src = next((ln for ln in comp.splitlines() if ln.startswith("**Source:**")), "")
    listed = set(re.findall(r"`([a-z0-9-]+)`", src))
    for slug in SAMPLES:
        if slug not in listed:
            fail(f"AC143 the Source line of profile-samples/component.md does not list `{slug}`")
    if "every sample keeps them" in comp:
        fail("AC143 profile-samples/component.md still says every sample keeps photos in img/; the crypto samples have none")


# --- per-sample checks -------------------------------------------------------------------------------------

def check_markers(s):  # AC8 (text; visibility in check_browser.py) AC13-AC16 AC18 AC20 AC22-AC24 AC58 AC145 AC146 AC256 AC257
    html, css, d = s.page()
    slug = s.slug
    if MARK not in norm(d.root.text()):
        fail(f"AC8 {slug}: page text lacks '{MARK}'")
    if "디자인 샘플" not in norm(" ".join(d.doc_title)):
        fail(f"AC16 {slug}: <title> lacks '디자인 샘플'")
    desc = [m.attrs.get("content", "") for m in d.root.iter("meta") if m.attrs.get("name") == "description"]
    if len(desc) != 1 or "디자인 샘플" not in desc[0]:
        fail(f"AC145 {slug}: expected one meta description whose content contains '디자인 샘플', found {desc}")
    for m in d.root.iter("meta"):
        if m.attrs.get("property") in ("og:title", "og:description") and "디자인 샘플" not in m.attrs.get("content", ""):
            fail(f"AC146 {slug}: {m.attrs['property']} content lacks '디자인 샘플': {m.attrs.get('content', '')!r}")
    ft = footer(d)
    foot = norm(ft.text()) if ft else ""
    if not ft:
        fail(f"AC13 AC14 AC58 {slug}: no <footer>")
    if MARK not in foot:
        fail(f"AC13 {slug}: footer lacks '{MARK}'")
    if "Website by RobinTech" not in foot:
        fail(f"AC14 {slug}: footer lacks 'Website by RobinTech'")
    if RISK not in foot:
        fail(f"AC58 {slug}: footer lacks the sentence '{RISK}'")
    if not any(m.attrs.get("name") == "robots" and m.attrs.get("content") == "noindex" for m in d.root.iter("meta")):
        fail(f'AC15 {slug}: no <meta name="robots" content="noindex">')
    wm = wordmark(d)
    if not wm:
        fail(f'AC18 AC256 AC257 {slug}: no <a class="wordmark"> in the first <header>')
    else:
        if not wm.name().startswith("로빈"):
            fail(f"AC18 {slug}: the wordmark's accessible name {wm.name()!r} does not start with 로빈")
        if wm.name() != s.info["name"]:
            fail(f"AC256 {slug}: the wordmark's accessible name is {wm.name()!r}, not {s.info['name']!r}")
        if squash(wm.text()) != s.info["name"] or next(wm.iter("img", "text"), None) is not None:
            fail(f"AC257 {slug}: the wordmark must be the live text {s.info['name']!r} with no <img> and no SVG <text> "
                 f"(text {norm(wm.text())!r})")
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
    phones = re.findall(r"(?<![\d-])(?:0\d{1,2}[-.\s]\d{3,4}|1[5-9]\d{2})[-.\s]\d{4}(?![\d-])", text)
    phones += re.findall(r"\(?0\d{1,2}\)\s?\d{3,4}[-.\s]?\d{4}|\+82[\d\s().-]{7,}", text)
    phones += re.findall(r"(?<![\d-])0(?:2|1[016-9]|[3-6]\d|70)\d{7,8}(?![\d-])", text)
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


def check_structure(s):  # AC28-AC31 AC35-AC39 AC44-AC50 AC56 AC78 AC255
    html, _, d = s.page()
    slug = s.slug
    svc, steps, con = (section(d, k, slug) for k in ("services", "steps", "contact"))
    if svc and max(len(list(svc.iter("li"))), len(list(svc.iter("h3")))) < 3:
        fail(f"AC28 {slug}: the service section names fewer than three things (<li> or <h3> items)")
    if steps and not any(sum(1 for k in ol.kids if isinstance(k, Node) and k.tag == "li") >= 3 for ol in steps.iter("ol")):
        fail(f"AC29 {slug}: the steps section has no <ol> with at least three <li> steps")
    tags = sorted({n.tag for n in d.root.iter("form", "input", "select", "textarea", "button")})
    if tags:
        fail(f"AC47 {slug}: the page has {tags} elements")
    if next(d.root.iter("script"), None) is not None:
        fail(f"AC48 {slug}: the page has a <script> element")
    for n in d.root.iter():
        for k, v in n.attrs.items():
            if re.fullmatch(r"on[a-z]+", k):
                fail(f"AC48 {slug}: an inline event handler: <{n.tag} {k}=…>")
            if v.strip().lower().startswith("javascript:"):
                fail(f"AC48 {slug}: a javascript: URL in <{n.tag} {k}=…>")
    for f in sorted(s.site.rglob("*")) if s.site.is_dir() else []:
        if f.is_file() and f.suffix.lower() in (".js", ".mjs"):
            fail(f"AC48 {slug}: a script file in the folder: {f.relative_to(s.site)}")
    ids = {n.attrs["id"] for n in d.root.iter() if n.attrs.get("id")}
    for a in d.root.iter("a"):
        href = a.attrs.get("href")
        if href is None or not (href == "#" or (href.startswith("#") and href[1:] in ids)):
            fail(f"AC49 {slug}: the link {a.name()[:30]!r} has href={href!r}; it must be '#' or '#<id of an element on the page>'")
    tags = sorted({n.tag for n in d.root.iter("iframe", "embed", "object", "video", "audio")})
    if tags:
        fail(f"AC50 {slug}: the page has {tags} elements")
    h = header(d)
    for word in ENTRY_WORDS:  # by accessible name, so an icon link labelled 로그인 counts
        hits = [a for a in d.root.iter("a") if word in squash(a.name()) or word in squash(a.text())]
        if s.info["key"] != "A":
            if hits:
                fail(f"AC56 {slug}: a link says '{word}'; only the 거래소 sample may show it")
        elif word in ("로그인", "회원가입") and (len(hits) != 1 or h is None or hits[0].up(lambda n: n is h) is None
                                             or squash(hits[0].name()) != word):
            fail(f"AC56 {slug}: '{word}' is in {len(hits)} links ({[a.name()[:20] for a in hits]}); the <header> holds "
                 f"exactly one link whose accessible name is '{word}', and no other link holds the word")
    if s.info["key"] != "A" and example_blocks(d):
        fail(f"AC78 {slug}: a sample whose 업태 is not 거래소 has an element with data-example")
    navs = [list(nav.iter("a")) for nav in h.iter("nav")] if h else []
    good = [n for n in navs if len(n) >= 4 and all(a.attrs.get("href", "").startswith("#") for a in n)
            and all(re.search(r"[가-힣]", norm(a.text())) and not re.search(r"[A-Za-z]", norm(a.text())) for a in n)]
    if not good:
        fail(f"AC255 {slug}: the <header> has no <nav> with at least four links, each with an href starting with '#' "
             f"and a text with a Hangul syllable and no Latin letter")
    if not con:
        return
    links = list(con.iter("a"))
    for ac, word in ACTIONS:
        if not any(word in a.name() for a in links):
            fail(f"{ac} {slug}: the contact section has no link whose accessible name contains '{word}'")
    for a in links:
        hit = [w for _, w in ACTIONS if w in a.name()]
        if len(hit) > 1:
            fail(f"AC39 {slug}: one link names several actions {hit}: '{a.name()}'")
    ls = lines(con)
    if FICTION not in norm(con.text()):
        fail(f"AC31 {slug}: the contact section lacks the sentence '{FICTION}'")
    if not any(re.search(HOURS, ln) for ln in ls):
        fail(f"AC44 {slug}: the contact section shows no 상담 hours as HH:MM–HH:MM")
    labels = [ls[i - 1] if i and len(ls[i - 1]) <= 12 and not re.search(r"\d:\d", ls[i - 1]) else "" for i in range(len(ls))]

    def closed(ln, lb):
        no = r"휴무일?\s*:?\s*없|에도|없이|문의"  # judged in the blocks that make the match: a label only when it is needed
        if re.search(CLOSED, ln) and re.search(CLOSED_DAY, ln):
            return not re.search(no, ln)
        hit = (re.search(CLOSED, lb) and re.search(CLOSED_DAY, ln)) or (re.search(CLOSED_DAY, lb) and re.search(CLOSED, ln))
        return hit and not re.search(no, lb + " " + ln)
    if not any(closed(ln, lb) for ln, lb in zip(ls, labels)):
        fail(f"AC45 {slug}: the contact section has no closed-days line ({CLOSED} with a day, in one block or split "
             f"over a label of at most 12 characters and the next block)")
    if not any("(가상 주소)" in ln for ln in ls):
        fail(f"AC46 {slug}: the contact section shows no address with '(가상 주소)'")
    if not any("02-000-0000" in ln for ln in ls):
        fail(f"AC46 {slug}: the contact section does not show 02-000-0000")


def check_copy(s):  # AC25 AC26 AC51 AC53-AC55 AC61-AC70 AC74 AC77 (listed words and digit forms), and AC85 AC190 / AC95 AC97 AC251
    html, css, d = s.page()
    slug = s.slug
    css = css + "\n" + inline_css(html)  # content: strings of <style> and style="" count as page text too
    if re.search(r"content\s*:[^;{}]*\battr\(", uncomment(css)):
        fail(f"AC61-AC70 {slug}: a CSS content: uses attr(); the check cannot read that text, write the string")
    text = fold(page_text(d, css))
    banned_words(slug, text, {**BANNED, **BANNED_BY_KEY[s.info["key"]]})
    interest(slug, text)
    figures(slug, blocks(d, css, skip=is_example))
    for m in EMAIL.finditer(text):
        if m.group(1).lower() != "example.com":
            fail(f"AC25 {slug}: an e-mail address outside example.com: {m.group(0)}")
    for m in re.finditer(r"(?<![\w.+-])@[A-Za-z0-9_.가-힣]{2,}", text):
        fail(f"AC26 {slug}: a social handle: {m.group(0)}")
    for m in re.finditer(r"(?<![\w@.-])((?:[A-Za-z0-9-]+\.)+(?:com|net|org|kr|io|me|co|xyz|fund|finance|app|dev|shop|cloud|ai|network|exchange|ly|gg|biz|info|site|online|link|page|club|pro|money|capital|trade|market|world|global|tech|cc|tv|us|uk|jp|eu))\b", text, re.I):
        if m.group(1).lower() != "example.com":
            fail(f"AC26 {slug}: a domain name: {m.group(1)}")
    markup = re.sub(r"https?://[^\s\"'()<>]+|url\([^)]*\)", " ", unescape(html) + "\n" + css)  # font and image URLs aside
    markup = re.sub(r"\s(?:d|points|viewBox|transform|gradientTransform)\s*=\s*(\"[^\"]*\"|'[^']*')", " ", markup)  # SVG geometry aside
    wallet_shaped(slug, markup)
    wallet_shaped(slug, text)  # an address split over <wbr> or <span> still reads as one


def check_a11y(s):  # AC33 AC34 (stylesheet) AC129 AC130 AC149 (stylesheet)
    html, css, d = s.page()
    if not re.search(r"word-break\s*:\s*keep-all", css):
        fail(f"AC34 {s.slug}: style.css has no word-break: keep-all")
    for sel, v in pseudo_positions(css + "\n" + inline_css(html)):  # a bar drawn as ::before/::after is not counted in the browser
        if re.sub(r"!\s*important", "", v, flags=re.I).strip().lower() not in ("absolute", "relative", "static"):
            fail(f"AC149 {s.slug}: the rule '{sel}' sets position: {v} on a ::before/::after; "
                 f"only absolute, relative and static are read (a fixed or sticky bar is an element)")
    for img in d.root.iter("img"):
        if not img.attrs.get("alt", "").strip():
            fail(f"AC129 {s.slug}: <img> without alt: {img.attrs.get('src')}")
    for svg in d.root.iter("svg"):
        named = svg.attrs.get("aria-label", "").strip() or any(k.tag == "title" and norm(k.text()) for k in svg.kids if isinstance(k, Node))
        if svg.attrs.get("aria-hidden") != "true" and not (svg.attrs.get("role") == "img" and named):
            fail(f'AC129 {s.slug}: an inline <svg> has neither aria-hidden="true" nor role="img" with an aria-label or <title>')
    hs = headings(d)
    levels = [int(h.tag[1]) for h in hs]
    if levels.count(1) != 1:
        fail(f"AC130 {s.slug}: expected exactly one <h1>, found {levels.count(1)}")
    prev = 1
    for lvl in levels:
        if lvl > prev + 1:
            fail(f"AC130 {s.slug}: heading level skipped: h{prev} -> h{lvl}")
        prev = lvl
    h1 = [norm(h.text()) for h in hs if h.tag == "h1"]
    if h1 and not re.search(r"[가-힣]", h1[0]):
        fail(f"AC33 {s.slug}: the <h1> has no Hangul syllable: {h1[0]!r}")


def check_assets(s):  # AC1 (page files) AC2 AC57 AC98 AC102-AC117 AC124 AC252 AC262
    html, css, d = s.page()
    slug = s.slug
    for name in ("index.html", "style.css"):
        if not (s.site / name).is_file():
            fail(f"AC1 missing profile/{slug}/{name}")
    for f in sorted(s.site.rglob("*")):
        rel = f.relative_to(s.site)
        if f.is_file() and not any(part.startswith(".") for part in rel.parts) and str(rel) not in ("index.html", "style.css", "thumb.jpg"):
            fail(f"AC1 {slug}: a file other than index.html, style.css and thumb.jpg in the folder: {rel}")
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
        return u.netloc == "fonts.googleapis.com" or (u.netloc == "cdn.jsdelivr.net" and "pretendard" in u.path.lower())
    for link in d.root.iter("link"):
        href = link.attrs.get("href", "")
        if "stylesheet" in link.attrs.get("rel", "").lower() and href.lower().startswith(("http", "//")):
            if not font_host(urlparse(href if not href.startswith("//") else "https:" + href)):
                fail(f"AC98 {slug}: external stylesheet not allowed: {href}")
    for url in re.findall(r"(?:https?:)?//cdn\.jsdelivr\.net/[^\s\"'()<>,]+", html + css):
        if "pretendard" not in url.lower():
            fail(f"AC98 {slug}: a cdn.jsdelivr.net load that is not Pretendard: {url}")
    for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", all_css):
        u = urlparse(imp)
        if u.netloc and not font_host(u):
            fail(f"AC98 {slug}: external @import not allowed: {imp}")
    for url in re.findall(r"(?i)https?://[^\s\"'()<>,]+|(?<![\w:/])//[\w-]+(?:\.[\w-]+)+[^\s\"'()<>,]*", unescape(html) + "\n" + uncomment(all_css)):
        if url.lower().startswith("http://www.w3.org/"):  # an XML namespace (inline SVG), not a load
            continue
        if urlparse(url if not url.startswith("//") else "https:" + url).netloc.lower() not in ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net"):
            fail(f"AC57 {slug}: URL with a host that is not allowed: {url}")
    if not any("stylesheet" in ln.attrs.get("rel", "").lower() and font_host(urlparse(ln.attrs.get("href", "")))
               and urlparse(ln.attrs.get("href", "")).netloc == "cdn.jsdelivr.net" for ln in d.root.iter("link")):
        fail(f"AC101 {slug}: index.html has no <link rel=\"stylesheet\"> to Pretendard on cdn.jsdelivr.net; the body face would be a fallback")
    fams = sorted(set(google_families(html, css)))
    if fams != s.info["families"]:
        fail(f"AC252 {slug}: fonts.googleapis.com is asked for {fams}, expected exactly {s.info['families']}")
    for f in sorted(s.site.rglob("*")) if s.site.is_dir() else []:
        if f.is_file() and f.suffix.lower() in (".svg", ".png", ".gif"):
            fail(f"AC102 {slug}: a picture file in the folder; pictures are CSS and inline <svg>: {f.relative_to(s.site)}")
    if re.search(r"(?<![\w-])data\s*:", html + css, re.I):
        fail(f"AC103 {slug}: a data: URL (a picture is an inline <svg> element or CSS; text and colours inside a data: URL are not read)")
    # No crypto sample uses a photo (AC262), so AC104-AC116 hold with nothing to check once these four pass.
    if next(d.root.iter("img", "picture", "source"), None) is not None:
        fail(f"AC262 AC104 AC115 AC116 {slug}: the page has an <img>, <picture> or <source> element")
    if (s.site / "img").exists():
        fail(f"AC262 AC105 AC106 AC107 AC108 AC109 AC110 AC111 AC112 AC113 AC114 {slug}: the sample has an img/ folder")
    local = [u for u in css_urls(all_css) if u and not u.startswith(("http://", "https://", "//", "data:", "#"))]
    if local:
        fail(f"AC104 {slug}: a CSS url() points at a local file, and the sample has no img/: {local[:3]}")
    ft = footer(d)
    if ft is not None and "Photos:" in norm(ft.text()):
        fail(f"AC106 {slug}: the footer has a 'Photos:' credit, and the sample has no photo")
    both = (unescape(html) + css).lower()
    for word in s.info["ref"]:
        if word in both:
            fail(f"AC117 {slug}: index.html or style.css names the reference site ('{word}', any case)")
    for word in s.info["faces"]:
        if word in both:
            fail(f"AC124 {slug}: index.html or style.css names a typeface of the reference ('{word}', any case)")


def rows_of(block, ac, slug, what, want):  # AC170: the <li> rows of an example list
    rows = [li for li in block.iter("li")]
    if len(rows) < want:
        fail(f"{ac} {slug}: {what} holds {len(rows)} <li> rows, needs at least {want}")
    names = []
    for li in rows:
        t = norm(li.text())
        nm = next((m for m in (re.fullmatch(r"예시 자산 ([A-Z])", n.own()) for n in li.iter()) if m), None)
        prices = [n for n in li.iter() if re.fullmatch(r"\d[\d,]*원", n.own())]
        changes = [n for n in li.iter() if n.own().endswith("%")]
        if not nm or len(prices) != 1 or len(changes) != 1:
            fail(f"{ac} {slug}: a row of {what} needs one element whose own text is '예시 자산' plus one Latin capital, one whose own "
                 f"text is a price ending in 원 and one change figure: {t[:50]!r}")
        names.append(nm.group(1) if nm else "?")
    return names


def check_sample_a(s, html, css, d):  # AC80 AC82-AC84 AC159 AC162 AC164 AC167-AC172 AC175 AC187-AC189
    slug = s.slug
    for h in ("#3f9cf0", "#06357a"):
        if h not in css.lower():
            fail(f"AC162 {slug}: style.css does not contain {h}")
    marked = example_blocks(d)
    for b in marked:
        if EXAMPLE not in norm(b.text()):
            fail(f"AC77 {slug}: an element with data-example lacks the text '{EXAMPLE}'")
        if b.up(is_example) is not None:
            fail(f"AC159 {slug}: an example block is nested in another example block")
    if len(marked) != 2:
        fail(f"AC159 {slug}: expected exactly two example blocks (elements with data-example), found {len(marked)}")
        return
    panel, card = marked
    for b, what in ((panel, "the panel"), (card, "the asset card")):
        t = norm(b.text())
        latin = [n.own() for n in [b, *b.iter()] if re.search(r"[A-Za-z]", n.own()) and not re.fullmatch(r"예시 자산 [A-Z]", n.own())]
        if latin:
            fail(f"AC80 {slug}: {what} has a Latin letter outside an asset name; an asset name is an element whose own "
                 f"text is '예시 자산' plus one Latin capital: {latin[:5]}")
        banned_words(f"{slug} {what}", t, EXAMPLE_BANNED)
        after = next((k for k in b.parent.kids[b.parent.kids.index(b) + 1:] if isinstance(k, Node)), None)
        if RISK not in t and not (after is not None and RISK in norm(after.text())):
            fail(f"AC83 {slug}: the sentence '{RISK}' is neither inside {what} nor in the element directly after it")
        if not re.search(r"\d원", t):
            fail(f"AC84 {slug}: {what} has no price written as static text")
        if next(b.iter("a"), None) is not None or any("tabindex" in n.attrs for n in [b, *b.iter()]):
            fail(f"AC175 {slug}: {what} holds an <a> or an element with tabindex")
        changes = [n.own() for n in b.iter() if n.own().endswith("%")]
        for c in changes:
            if not c.startswith(("+", "\u2212")):
                fail(f"AC171 {slug}: a change figure of {what} does not start with + or − (U+2212): {c!r}")
        if not any(c.startswith("+") for c in changes) or not any(c.startswith("\u2212") for c in changes):
            fail(f"AC172 {slug}: {what} needs at least one change figure starting with + and one starting with − (found {changes})")
    phones = [n for n in panel.iter() if "phone" in n.classes()]
    if len(phones) != 1:
        fail(f'AC163 {slug}: the panel needs exactly one element with class "phone", found {len(phones)}')
        return
    phone = phones[0]
    first = next((ln for ln in lines(phone)), "")
    if first != EXAMPLE:
        fail(f"AC164 {slug}: the first text inside the phone is {first[:40]!r}, not '{EXAMPLE}'")
    svgs = list(phone.iter("svg"))
    polys = [p for v in svgs for p in v.iter("polyline")]
    if len(svgs) != 1 or svgs[0].attrs.get("aria-hidden") != "true" or len(polys) != 1:
        fail(f'AC168 {slug}: the phone needs exactly one inline <svg aria-hidden="true"> that holds exactly one <polyline> '
             f"(found {len(svgs)} svg, {len(polys)} polyline)")
    else:
        nums = [float(x) for x in re.findall(r"-?\d*\.?\d+", polys[0].attrs.get("points", ""))]
        ys = nums[1::2]
        ups, downs = any(b < a for a, b in zip(ys, ys[1:])), any(b > a for a, b in zip(ys, ys[1:]))
        if len(nums) % 2 or len(ys) < 3 or not ups or not downs or ys[-1] <= min(ys):
            fail(f"AC169 {slug}: the price line must go up at least once and down at least once and must not end at its "
                 f"highest point (the smallest y); y values {ys}")
    rows_of(phone, "AC170", slug, "the phone", 3)
    names = rows_of(card, "AC187", slug, "the asset card", 4)
    if names != [chr(ord("A") + i) for i in range(len(names))]:
        fail(f"AC187 {slug}: the asset card's rows are named {names}; they must run in letter order from 예시 자산 A")
    svc, steps, con = (section(d, k, slug, quiet=True) for k in ("services", "steps", "contact"))
    ol = next(steps.iter("ol"), None) if steps else None
    if not (svc and ol is not None and con and svc.order < ol.order < card.order < con.order):
        fail(f"AC188 {slug}: the order must be service section, the steps <ol> (in the dark panel), the asset card, "
             f"contact section")


def check_sample_b(s, html, css, d):  # AC205 AC209 AC213 AC216 (markup) AC221
    slug = s.slug
    h = header(d)
    for a in h.iter("a") if h else []:
        if not re.search(r"[가-힣]", norm(a.text())):
            fail(f"AC205 {slug}: a header link has no visible text with a Hangul syllable: {a.name()[:30]!r}")
    h1 = next(d.root.iter("h1"), None)
    ems = list(h1.iter("em")) if h1 is not None else []
    if not 1 <= len(ems) <= 2:
        fail(f"AC208 {slug}: the <h1> needs one or two <em>, found {len(ems)}")
    elif any(not re.search(r"[가-힣]", norm(e.text())) for e in ems) or \
            len(squash(h1.text())) <= sum(len(squash(e.text())) for e in ems):
        fail(f"AC209 {slug}: each <em> needs a Hangul syllable and the <h1> needs text outside every <em>: {norm(h1.text())!r}")
    cards = [n for n in d.root.iter() if "word-card" in n.classes()]
    if len(cards) != 3:
        fail(f'AC216 {slug}: expected exactly three elements with class "word-card", found {len(cards)}')
    for c in cards:
        terms = [n for n in c.iter() if "term" in n.classes()]
        if len(terms) != 1 or len(list(c.iter("p"))) != 1 or not re.fullmatch(r"[가-힣]+(?: [가-힣]+)*", norm(terms[0].text()) if terms else ""):
            fail(f'AC216 {slug}: a word card needs one element with class "term" (Hangul syllables and spaces only) and '
                 f"one <p>: {norm(c.text())[:40]!r}")
    for svg in d.root.iter("svg"):
        bad = sorted({n.tag for n in svg.iter("ellipse", "text")})
        if bad:
            fail(f"AC213 {slug}: an inline <svg> holds {bad}")
    found, bad = background_colors(css + "\n" + inline_css(html))
    for b in bad:
        fail(f"AC221 {slug}: a background value the check cannot read: {b}")
    for sel, rgb, alpha in found:
        if spread(rgb) > 0x30 and (rgb not in B_SATURATED or alpha < 1):
            fail(f"AC221 {slug}: '{sel}' paints a saturated background #{'%02x%02x%02x' % rgb} at alpha {alpha:.2f}; "
                 f"only #f5c08a and #7b2338 at full opacity are allowed")


def check_sample_d(s, html, css, d):  # AC231 (markup) AC241 (no <text>) AC246 (three <li>) AC248 AC249
    slug = s.slug
    h1 = next(d.root.iter("h1"), None)
    if h1 is not None:
        kids = [k for k in h1.kids if isinstance(k, Node)]
        if [k.tag for k in kids] != ["span"] * 3 or h1.own() or any(not norm(k.text()) for k in kids):
            fail(f"AC231 {slug}: the <h1> needs exactly three child <span> elements with text and no text outside them "
                 f"(children {[k.tag for k in kids]}, own text {h1.own()!r})")
    if next((t for v in d.root.iter("svg") for t in v.iter("text")), None) is not None:
        fail(f"AC241 {slug}: an inline <svg> holds a <text> element")
    svc, steps, con = (section(d, k, slug, quiet=True) for k in ("services", "steps", "contact"))
    if not (svc and steps and con and svc.order < steps.order < con.order):
        fail(f"AC248 {slug}: the order must be service section, the band (steps section), contact section")
    if steps:
        ols = list(steps.iter("ol"))
        n = sum(1 for k in ols[0].kids if isinstance(k, Node) and k.tag == "li") if len(ols) == 1 else -1
        if n != 3:
            fail(f"AC246 {slug}: the band needs one <ol> with exactly three <li> cards (found {len(ols)} <ol>, {n} <li>)")
    found, bad = all_colors(css + "\n" + inline_css(html))
    for svg in d.root.iter("svg"):
        for n in [svg, *svg.iter()]:
            for k in ("fill", "stroke", "stop-color", "flood-color", "lighting-color", "color"):
                if k in n.attrs:
                    got, problems = colors_in(n.attrs[k])
                    found += [(f"<{n.tag} {k}>", rgb, a) for rgb, a in got]
                    bad += [f"<{n.tag} {k}>: {p}" for p in problems]
    for b in bad:
        fail(f"AC249 {slug}: a colour the check cannot read: {b}")
    for sel, rgb, _ in found:
        if spread(rgb) > 0x30 and not 74 <= hue(rgb) <= 90:
            fail(f"AC249 {slug}: '{sel}' uses #{'%02x%02x%02x' % rgb} (hue {hue(rgb):.0f}°); a colour with a channel spread "
                 f"above 0x30 needs a hue from 74° to 90°")


def check_sample(s):  # the per-sample static criteria; AC151/AC194/AC225, AC191/AC222/AC250, AC189/AC223 for all
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
        if hexv in css.lower():
            fail(f"{ac} {slug}: style.css contains {hexv}")
    if s.info["contact"]:
        ac, word = s.info["contact"]
        con = section(d, "contact", slug, quiet=True)
        if not con or not any(word in norm(h.text()) for h in own_h2(con)):
            fail(f"{ac} {slug}: the contact section's heading does not contain '{word}'")
    {"A": check_sample_a, "B": check_sample_b, "D": check_sample_d}[s.info["key"]](s, html, css, d)


def check_register(s):  # AC1 (thumb.jpg) AC3 AC4 AC5 (size) AC17 AC76 AC121 AC122 AC150 AC193 AC224
    slug, info = s.slug, s.info
    e = entry(slug)
    profiles = load_profiles()
    if not e:
        fail(f"AC3 expected one PROFILES entry for {slug}, found {sum(1 for x in profiles if x.get('slug') == slug)}")
    else:
        if (e.get("industry"), e.get("status"), e.get("demo")) != ("crypto", "live", True):
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
                fail(f"AC121 {slug}: accent {a} is also the accent of {other.get('slug')}")
            if other is not e and other.get("industry") == "crypto":
                shared = {str(x).lower() for x in e.get("palette") or []} & {str(x).lower() for x in other.get("palette") or []}
                if shared:
                    fail(f"AC121 {slug}: palette hex {sorted(shared)} is also in the palette of {other.get('slug')}")
        card = [str(e.get(k, "")) for k in ("title", "summary")] + [str(x) for x in e.get("features") or []]
        label = f"{slug} PROFILES entry (AC76)"
        if e.get("title") != info["title"]:
            fail(f"AC76 {slug}: PROFILES title is {e.get('title')!r}, expected {info['title']!r} (spec A15)")
        joined = fold(norm(" ".join(card)))
        banned_words(label, joined, {**BANNED, **BANNED_BY_KEY[info["key"]]})  # AC53-AC55, AC61-AC70 and the sample's own lists
        interest(label, joined)
        figures(label, card, "AC74")
        css = read(s.site / "style.css") if (s.site / "style.css").is_file() else ""
        if not a or a not in css.lower():
            fail(f"AC122 {slug}: style.css does not contain the PROFILES accent {a}")
    if not re.fullmatch(r"crypto-robin[a-z]+", slug):
        fail(f"AC4 {slug}: slug is not 'crypto-robin' and lowercase ASCII letters")
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
              "assets": check_assets, "sample": check_sample, "register": check_register}
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
                if not (s.site / "index.html").is_file() and n != "register":
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
