#!/usr/bin/env python3
"""Static checks for the food profile sample (no browser). Run from the repository root.

usage: python3 docs/features/2026-11-17-profile-food/check_static.py <check> [<check> ...]
checks: name photos markers flow assets register playbook all
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
SLUG = "food-saebyeokmil"
SITE = ROOT / "profile" / SLUG
IMG = SITE / "img"
SOURCES = IMG / "sources.txt"
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
BLOCK = {"p", "li", "dd", "dt", "td", "th", "address", "div", "section", "article", "header", "footer",
         "h1", "h2", "h3", "h4", "h5", "h6", "button", "nav", "main", "aside", "figure", "figcaption"}
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
        self.text = []            # (offset-ordered) visible text chunks; "\n" at block boundaries
        self.headings = []        # (level, text, text_offset)
        self.controls = []        # dict(tag, href, label, text)
        self.imgs = []            # attrs dicts
        self.refs = []            # (attr, value) for src/srcset/href/poster
        self.links = []           # <link> attrs
        self.scripts = []         # <script src>
        self.metas = []
        self.footer = []
        self._stack = []          # open controls / headings / footer capture
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag in ("script", "style", "template"):
            self._skip += 1
            if tag == "script" and a.get("src"):
                self.scripts.append(a["src"])
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
        if tag in ("a", "button"):
            self._stack.append({"kind": "control", "tag": tag, "href": a.get("href"),
                                "label": a.get("aria-label"), "buf": []})
        elif re.fullmatch(r"h[1-6]", tag):
            self._stack.append({"kind": "heading", "level": int(tag[1]), "buf": [],
                                "offset": sum(len(t) for t in self.text)})
        elif tag == "footer":
            self._stack.append({"kind": "footer", "buf": []})

    def handle_endtag(self, tag):
        if tag in ("script", "style", "template"):
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
        if not self._skip:
            self._add(data)

    def lines(self):
        return [re.sub(r"\s+", " ", ln).strip() for ln in "".join(self.text).split("\n") if ln.strip()]

    def full(self):
        return "".join(self.text)


def page():
    html = read(SITE / "index.html")
    p = Page()
    p.feed(html)
    return html, read(SITE / "style.css"), p


def css_urls(css):
    out = [u.strip("'\" ") for u in re.findall(r"url\(([^)]*)\)", css)]
    out += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", css)
    return out


def srcset_urls(v):
    return [part.strip().split()[0] for part in v.split(",") if part.strip()]


def image_refs(p, css):
    """Local paths referenced as images: src, srcset, CSS url()."""
    refs = []
    for k, v in p.refs:
        if k == "src" or k == "poster":
            refs.append(v)
        elif k == "srcset":
            refs += srcset_urls(v)
    refs += css_urls(css)
    return [r for r in refs if r and not r.startswith(("data:", "#", "http://", "https://", "//"))]


def image_files():
    return sorted(f for f in IMG.iterdir() if f.is_file() and f.name != "sources.txt"
                  and not f.name.startswith(".")) if IMG.is_dir() else []


def sources_lines():
    return [ln.split() for ln in read(SOURCES).splitlines() if ln.strip()]


def photo_id(url):
    m = re.search(r"images\.unsplash\.com/(photo-[0-9]+-[0-9a-f]+)", url) or \
        re.search(r"images\.pexels\.com/photos/([0-9]+)/", url)
    return m.group(1) if m else None


def sips_size(path):
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True)
    w = re.search(r"pixelWidth:\s*(\d+)", r.stdout)
    h = re.search(r"pixelHeight:\s*(\d+)", r.stdout)
    return (int(w.group(1)), int(h.group(1))) if w and h else (None, None)


# --- checks -------------------------------------------------------------------------------------

def check_name():  # AC11
    rec = read(FEATURE / "name-check.txt")
    queries = [ln for ln in rec.splitlines() if ln.startswith("query:")]
    for word in ("빵집", "베이커리", "카페"):
        if not any("새벽밀" in q and word in q for q in queries):
            fail(f"AC11 name-check.txt: no 'query:' line with 새벽밀 and {word}")
    if not re.search(r"^verdict: no match\b", rec, re.M):
        fail("AC11 name-check.txt: no 'verdict: no match' line")


def check_photos():  # AC21 AC22 AC44-AC49
    files = image_files()
    if not files:
        fail("AC44 img/ has no image files")
    total = 0
    for f in files:
        if f.suffix.lower() not in (".jpg", ".webp"):
            fail(f"AC44 not .jpg/.webp: img/{f.name}")
        size = f.stat().st_size
        total += size
        if size > 500 * 1024:
            fail(f"AC46 larger than 500 KB: img/{f.name} ({size // 1024} KB)")
        w, _ = sips_size(f)
        if w is None or w > 2000:
            fail(f"AC45 wider than 2000 px or unreadable: img/{f.name} ({w})")
    if total > 3 * 1024 * 1024:
        fail(f"AC47 img/ totals {total / 1024 / 1024:.2f} MB > 3 MB")
    lines = sources_lines()
    names = [ln[0] for ln in lines if ln]
    for ln in lines:
        if len(ln) != 3:
            fail(f"AC48 sources.txt line is not '<file> <page URL> <download URL>': {' '.join(ln)}")
            continue
        name, page_url, dl = ln
        if not page_url.startswith(("https://unsplash.com/photos/", "https://www.pexels.com/photo/")):
            fail(f"AC48 page URL is not an Unsplash/Pexels photo page: {page_url}")
        if not dl.startswith(("https://images.unsplash.com/photo-", "https://images.pexels.com/photos/")):
            fail(f"AC49 download URL not allowed: {dl}")
    if sorted(names) != [f.name for f in files] or len(set(names)) != len(names):
        fail(f"AC48 sources.txt files {sorted(names)} != img/ files {[f.name for f in files]}")
    raw = read(SOURCES)
    if "plus.unsplash.com" in raw or "premium_photo" in raw:
        fail("AC21 sources.txt mentions plus.unsplash.com or premium_photo")
    flower = read(ROOT / "profile/flower-bomgyeol/index.html")
    for ln in lines:
        pid = photo_id(ln[-1]) if ln else None
        if pid and pid in flower:
            fail(f"AC22 photo {pid} is also used by flower-bomgyeol")


def check_markers():  # AC7 (text present; visibility in check_browser.py) AC8 AC9 AC10 AC12 AC13
    html, _, p = page()
    if MARK not in re.sub(r"\s+", " ", p.full()):
        fail(f"AC7 page text lacks '{MARK}'")
    foot = " ".join(p.footer)
    if "Website by RobinTech" not in foot:
        fail("AC8 footer lacks 'Website by RobinTech'")
    credit = foot.split("Photos:", 1)[1] if "Photos:" in foot else ""
    for host, name in (("images.unsplash.com", "Unsplash"), ("images.pexels.com", "Pexels")):
        if host in read(SOURCES) and name not in credit:
            fail(f"AC9 a {name} photo is used but the footer's 'Photos:' credit does not name {name}")
    if not any(m.get("name") == "robots" and m.get("content") == "noindex" for m in p.metas):
        fail('AC10 no <meta name="robots" content="noindex">')
    addr = re.compile(r"[가-힣0-9]*[가-힣0-9](?<!으)(?:로|길)\s?\d+(?:-\d+)?"
                      r"(?![\d%A-Za-z가-힣~:.-]|,\d|\s?(?:원|분|시|개|인|일|명|번))")
    lines = p.lines()
    if not any("(가상 주소)" in ln for ln in lines):
        fail("AC12 no address with '(가상 주소)' on the page")
    for ln in lines:
        if addr.search(ln) and "(가상 주소)" not in ln:
            fail(f"AC12 address without '(가상 주소)': {ln[:80]}")
    text = p.full() + "\n" + " ".join(v for _, v in p.refs)
    phones = re.findall(r"(?<![\d-])0\d{1,2}[-.\s]\d{3,4}[-.\s]\d{4}(?![\d-])", text)
    if "02-000-0000" not in phones:
        fail("AC13 no phone number 02-000-0000 on the page")
    for ph in phones:
        if ph != "02-000-0000":
            fail(f"AC13 phone number is not 02-000-0000: {ph}")
    for brn in re.findall(r"(?<![\d-])\d{3}-\d{2}-\d{5}(?![\d-])", text):
        if brn != "000-00-00000":
            fail(f"AC13 business registration number is not 000-00-00000: {brn}")


def check_flow():  # AC16 AC17 AC23-AC29
    _, css, p = page()
    if not re.search(r"word-break\s*:\s*keep-all", css):
        fail("AC16 style.css has no word-break: keep-all")
    full = p.full()

    def first(pattern):
        hits = [off for lvl, t, off in p.headings if re.search(pattern, t) and lvl >= 2]
        return min(hits) if hits else None
    menu, hours, visit = first(r"메뉴"), first(r"영업\s?시간"), first(r"오시는\s?길")
    if None in (menu, hours, visit) or not menu < hours < visit:
        fail(f"AC17 headings 메뉴 < 영업시간 < 오시는 길 not found in order (offsets {menu}, {hours}, {visit})")
    else:
        mb, hb = full[menu:hours], full[hours:visit]
        for word in ("빵", "케이크", "음료"):
            if word not in mb:
                fail(f"AC17 menu section lacks '{word}'")
        if not re.search(r"\d[\d,]*\s?원", mb):
            fail("AC17 menu section shows no price (…원)")
        if "휴무" not in hb:
            fail("AC17 hours section lacks closed days (휴무)")
    for ac, word in (("AC23", "카카오톡"), ("AC24", "네이버 예약"), ("AC25", "네이버 지도"), ("AC26", "전화")):
        hits = [c for c in p.controls if word in (c["name"] or "")]
        if not hits:
            fail(f"{ac} no link or button whose accessible name contains '{word}'")
        for c in hits:
            if c["href"] != "#":
                fail(f"AC27 '{c['name']}' has href={c['href']!r}, not '#'")
    for img in p.imgs:
        if not img.get("alt", "").strip():
            fail(f"AC28 <img> without alt: {img.get('src')}")
    levels = [lvl for lvl, _, _ in p.headings]
    if levels.count(1) != 1:
        fail(f"AC29 expected exactly one <h1>, found {levels.count(1)}")
    prev = 1
    for lvl in levels:
        if lvl > prev + 1:
            fail(f"AC29 heading level skipped: h{prev} -> h{lvl}")
        prev = lvl


def check_assets():  # AC1 (page files; thumb.jpg in register) AC2 AC18 AC20 AC39 AC42 AC43
    html, css, p = page()
    for name in ("index.html", "style.css"):
        if not (SITE / name).is_file():
            fail(f"AC1 missing profile/{SLUG}/{name}")
    local = [v for k, v in p.refs if k != "srcset"] + [u for k, v in p.refs if k == "srcset" for u in srcset_urls(v)]
    local += css_urls(css)
    for ref in local:
        if ref.startswith(("http://", "https://", "data:", "#", "mailto:", "tel:")):
            continue
        if ref.startswith("/") or "../" in ref or "assets/" in ref:
            fail(f"AC2 reference leaves the sample folder: {ref}")
    if "../" in html + css or re.search(r"\bassets/", html + css):
        fail("AC2 index.html or style.css contains '../' or 'assets/'")
    for link in p.links:
        if "stylesheet" in link.get("rel", "") and link.get("href", "").startswith(("http", "//")):
            u = urlparse(link["href"] if not link["href"].startswith("//") else "https:" + link["href"])
            if not (u.netloc == "fonts.googleapis.com" or
                    (u.netloc == "cdn.jsdelivr.net" and "pretendard" in u.path.lower())):
                fail(f"AC18 external stylesheet not allowed: {link['href']}")
    for imp in re.findall(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", css):
        u = urlparse(imp)
        if u.netloc and not (u.netloc == "fonts.googleapis.com" or
                             (u.netloc == "cdn.jsdelivr.net" and "pretendard" in u.path.lower())):
            fail(f"AC18 external @import not allowed: {imp}")
    for src in p.scripts:
        if src.startswith(("http", "//")):
            fail(f"AC18 external script: {src}")
    for url in re.findall(r"https?://[^\s\"'()<>,]+", html + css):
        if urlparse(url).netloc not in ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net"):
            fail(f"AC20 URL with a host that is not allowed: {url}")
    if re.search(r"tartine", html + css, re.I):
        fail("AC39 the sample mentions Tartine")
    for ref in (r.removeprefix("./") for r in image_refs(p, css)):
        path = (SITE / ref.split("?")[0].split("#")[0]).resolve()
        if not path.is_file() or SITE.resolve() not in path.parents:
            fail(f"AC42 image path does not resolve inside the sample folder: {ref}")
        if re.search(r"\.(jpe?g|png|webp|avif|gif)$", ref.split("?")[0], re.I) and not ref.startswith("img/"):
            fail(f"AC43 photo not in img/: {ref}")


def check_register():  # AC1 (thumb.jpg) AC3 AC4 AC5 AC35 (generated part)
    sys.path.insert(0, str(ROOT / "scripts"))
    from profiles import PROFILES  # noqa: E402
    hits = [p for p in PROFILES if p.get("slug") == SLUG]
    if len(hits) != 1:
        fail(f"AC3 expected one PROFILES entry for {SLUG}, found {len(hits)}")
    elif (hits[0].get("industry"), hits[0].get("status"), hits[0].get("demo")) != ("food", "live", True):
        fail(f"AC3 entry fields wrong: industry={hits[0].get('industry')} status={hits[0].get('status')} "
             f"demo={hits[0].get('demo')}")
    thumb = SITE / "thumb.jpg"
    if thumb.is_file():
        w, h = sips_size(thumb)
        if w != 1200 or h is None or abs(h * 16 - w * 10) > 16:
            fail(f"AC4 thumb.jpg is {w}x{h}, not 1200 wide at 16:10")
    else:
        fail("AC1 AC4 thumb.jpg missing")
    gallery = read(ROOT / "profile/index.html")
    if f'data-slug="{SLUG}"' not in gallery:
        fail("AC35 profile/index.html has no card for the sample (run python3 scripts/build.py)")
    if re.search(r'class="pf-card pf-empty[^"]*" data-industry="food"', gallery):
        fail("AC35 profile/index.html still has the food 준비 중 tile")


def check_playbook():  # AC50-AC53
    pb = read(ROOT / "docs/profile-playbook.md")
    m = re.search(r"^## 3\..*?(?=^## 4\.)", pb, re.S | re.M)
    sec = m.group(0) if m else ""
    if not sec:
        fail("AC50 playbook §3 not found")
    bullets = re.findall(r"^- .*(?:\n[ \t]+\S.*)*", sec, re.M)  # a bullet with its wrapped lines
    photo = [b for b in bullets if "**사진:**" in b]
    if not photo or "profile/<slug>/img/" not in photo[0] or "상대 경로" not in photo[0]:
        fail("AC50 §3 photo rule does not say photos go into profile/<slug>/img/ by relative path")
    if photo and "images.unsplash.com" in photo[0]:
        fail("AC50 §3 photo rule still mentions linking images.unsplash.com")
    folder = [b for b in bullets if "**폴더:**" in b]
    if not folder or "img/" not in folder[0] or "sources.txt" not in folder[0]:
        fail("AC51 §3 folder rule does not list img/ with img/sources.txt")
    if not any("flower-bomgyeol" in b and ("직접 링크" in b or "핫링크" in b)
               for b in re.findall(r"^\s*- .*(?:\n[ \t]+\S.*)*|^\S.*", pb, re.M)):
        fail("AC52 playbook does not say flower-bomgyeol still links its photos directly")
    font = [re.sub(r"\s+", " ", b) for b in bullets if "**글꼴:**" in b]
    if (not font or "가격" not in font[0] or "한글 서체" not in font[0]
            or not ("모노" in font[0] or "고정폭" in font[0]) or "숫자는 한글 서체로" in font[0]):
        fail("AC53 §3 font rule does not allow prices and numbers in a Korean or monospaced (모노) face")


CHECKS = {"name": check_name, "photos": check_photos, "markers": check_markers, "flow": check_flow,
          "assets": check_assets, "register": check_register, "playbook": check_playbook}

if __name__ == "__main__":
    names = sys.argv[1:]
    if not names or any(n not in CHECKS and n != "all" for n in names):
        raise SystemExit(__doc__)
    if "all" in names:
        names = list(CHECKS)
    for n in names:
        CHECKS[n]()
    for f in fails:
        print("FAIL", f)
    print(f"{'PASS' if not fails else 'FAIL'}: {' '.join(names)} ({len(fails)} failures)")
    sys.exit(1 if fails else 0)
