"""Checks for docs/features/2026-11-18-gallery-industries/ (spec AC1-AC21).

Usage: python3 check.py data | gallery | playbook | scope | current | all | browser
`all` runs every check except `browser`; it needs no network and no browser.
`browser` drives the installed Google Chrome through Playwright and serves the repository
on a free local port itself. Exit 0 when every check passes, 1 otherwise.
"""
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import subprocess
import sys
import threading

ROOT = Path(__file__).resolve().parents[3]
NINE = [("law", "법무법인"), ("clinic", "병원 · 의원"), ("fitness", "필라테스"), ("beauty", "미용실"),
        ("interior", "인테리어"), ("crypto", "코인 · 가상자산"), ("invest", "투자자문"),
        ("food", "식당 · 카페"), ("flower", "꽃집 · 공방")]
OLD_LABELS = ["전문 서비스", "키즈 · 교육", "숙박 · 공간대여", "운동 · 피트니스", "뷰티 · 미용"]
OLD_KEYS = ["kids", "stay", "pro"]
SAMPLES = {"food-saebyeokmil": "food", "flower-bomgyeol": "flower", "clinic-neuru": "clinic",
           "clinic-byeotteul": "clinic", "clinic-bonui": "clinic"}
EMPTY = ["law", "fitness", "beauty", "interior", "crypto", "invest"]
COUNTS = {"clinic": "3", "food": "1", "flower": "1"}
DESC = "꽃집, 식당, 병원 등 업종별로 설계한 로빈테크 홈페이지 디자인 프로파일. 마음에 드는 디자인을 골라 우리 가게 홈페이지로 만들어 보세요."
fails = []


def fail(msg):
    fails.append(msg)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


class Gallery(HTMLParser):
    """Collects chips (data-filter, label, count), cards, data-* values and meta descriptions."""

    def __init__(self):
        super().__init__()
        self.chips, self.cards, self.empties, self.attrs, self.meta = [], {}, [], [], {}
        self.chip = None
        self.in_sup = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.attrs += [(k, v) for k, v in attrs if k in ("data-filter", "data-industry")]
        if tag == "meta" and (a.get("name") == "description" or a.get("property") == "og:description"):
            self.meta[a.get("name") or a.get("property")] = a.get("content", "")
        if tag == "button" and "data-filter" in a:
            self.chip = [a["data-filter"], "", ""]
        if tag == "sup" and self.chip:
            self.in_sup = True
        cls = a.get("class", "").split()
        if "pf-card" in cls and "pf-empty" in cls:
            self.empties.append(a.get("data-industry"))
        elif "pf-card" in cls and tag == "a":
            if a.get("data-slug") in self.cards:
                fail(f"AC11 two cards for {a.get('data-slug')}")
            self.cards[a.get("data-slug")] = a.get("data-industry")

    def handle_endtag(self, tag):
        if tag == "sup":
            self.in_sup = False
        if tag == "button" and self.chip:
            self.chips.append((self.chip[0], self.chip[1].strip(), self.chip[2].strip()))
            self.chip = None

    def handle_data(self, data):
        if self.chip:
            self.chip[2 if self.in_sup else 1] += data


def check_data():  # AC1
    sys.path.insert(0, str(ROOT / "scripts"))
    from profiles import INDUSTRIES
    if list(INDUSTRIES) != NINE:
        fail(f"AC1 INDUSTRIES is {INDUSTRIES}, expected {NINE}")


def check_gallery():  # AC3-AC13 (AC2: the task runs scripts/build.py first)
    text = (ROOT / "profile/index.html").read_text(encoding="utf-8")
    g = Gallery()
    g.feed(text)
    keys = [c[0] for c in g.chips]
    if keys != ["all"] + [k for k, _ in NINE]:
        fail(f"AC3 chips are {keys}")
    chips = {c[0]: c for c in g.chips}
    for k, label in NINE:
        if k in chips and chips[k][1] != label:
            fail(f"AC4 chip {k} shows {chips[k][1]!r}, expected {label!r}")
    if chips.get("all", ("", "", ""))[2] != "5":
        fail(f"AC5 all chip count is {chips.get('all', ('', '', ''))[2]!r}, expected '5'")
    for k, n in COUNTS.items():
        if k in chips and chips[k][2] != n:
            fail(f"AC6 chip {k} count is {chips[k][2]!r}, expected {n!r}")
    for k in EMPTY:
        if k in chips and chips[k][2]:
            fail(f"AC7 chip {k} shows a count {chips[k][2]!r}")
    if sorted(g.empties) != sorted(EMPTY):
        fail(f"AC8 준비 중 tiles are {g.empties}, expected one each for {EMPTY}")
    bad = sorted({f"{k}={v}" for k, v in g.attrs if v in OLD_KEYS})
    if bad:
        fail(f"AC9 removed keys still in attributes: {bad}")
    old = [s for s in OLD_LABELS if s in text]
    if old:
        fail(f"AC10 old labels in profile/index.html: {old}")
    if g.cards != SAMPLES:
        fail(f"AC11 cards are {g.cards}, expected {SAMPLES}")
    for name, ac in (("description", "AC12"), ("og:description", "AC13")):
        if g.meta.get(name) != DESC:
            fail(f"{ac} {name} is {g.meta.get(name)!r}, expected {DESC!r}")


def check_playbook():  # AC15-AC17
    text = (ROOT / "docs/profile-playbook.md").read_text(encoding="utf-8")
    sec = re.search(r"^## 3\..*?(?=^## |\Z)", text, re.M | re.S)
    line = re.search(r"^- \*\*업종 key:\*\*.*\(([^)]*)\)", sec.group(0) if sec else "", re.M)
    keys = [k.strip() for k in line.group(1).split(",")] if line else None
    if keys != [k for k, _ in NINE]:
        fail(f"AC15 §3 업종 key line lists {keys}")
    items = re.split(r"\n(?=- )|\n\s*\n", text)  # one bullet item or one paragraph
    for ac, words in (("AC16", ["fitness", "beauty", "프랜차이즈", "매장 찾기", "가맹 문의"]),
                      ("AC17", ["law", "invest", "crypto", "광고", "AC", "clinic"])):
        if not any(all(w in item for w in words) for item in items):
            fail(f"{ac} no single playbook item or paragraph holds all of {words}")


def check_scope():  # AC18 AC19
    base = git("merge-base", "main", "HEAD").strip()
    allowed = re.compile(r"^(scripts/profiles\.py|scripts/build\.py|profile/index\.html|docs/.*)$")
    out = [p for p in git("diff", "--name-only", base).split() if not allowed.match(p)]
    if out:
        fail(f"AC18 changed outside scope: {out}")
    lines = [l for l in git("diff", "-U0", base, "--", "scripts/build.py").splitlines()
             if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    other = [l for l in lines if not l[1:].startswith('    desc = "')]
    if other or len(lines) > 2:
        fail(f"AC19 scripts/build.py changes more than the gallery desc string: {other}")


def check_current():  # AC20
    for p in sorted((ROOT / "docs/current_system").rglob("*.md")):
        t = p.read_text(encoding="utf-8")
        hits = re.findall(r"\b(?:kids|stay|pro)\b", t) + [s for s in OLD_LABELS if s in t]
        if hits:
            fail(f"AC20 {p.relative_to(ROOT)} names {sorted(set(hits))}")


def check_browser():  # AC14
    from playwright.sync_api import sync_playwright
    handler = partial(type("Quiet", (SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}),
                      directory=str(ROOT))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{httpd.server_port}"
    shown_js = """() => [...document.querySelectorAll('#pf-grid .pf-card')]
        .filter(c => getComputedStyle(c).display !== 'none')
        .map(c => (c.classList.contains('pf-empty') ? 'empty:' : '') + (c.dataset.slug || c.dataset.industry))"""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.set_default_timeout(3000)
        page.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        page.goto(f"{base}/profile/", wait_until="domcontentloaded")
        for k, _ in NINE:
            chip = page.locator(f'.pf-filters button[data-filter="{k}"]')
            if chip.count() != 1:
                fail(f"AC14 no {k} chip on /profile/")
                continue
            chip.click()
            shown = sorted(page.evaluate(shown_js))
            want = sorted(s for s, i in SAMPLES.items() if i == k) or [f"empty:{k}"]
            if shown != want:
                fail(f"AC14 {k} chip shows {shown}, expected {want}")
        browser.close()
    httpd.shutdown()


CHECKS = {"data": check_data, "gallery": check_gallery, "playbook": check_playbook,
          "scope": check_scope, "current": check_current}

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "browser":
        check_browser()
    elif arg == "all":
        for f in CHECKS.values():
            f()
    elif arg in CHECKS:
        CHECKS[arg]()
    else:
        sys.exit(__doc__)
    for m in fails:
        print("FAIL", m)
    print("PASS" if not fails else f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)
