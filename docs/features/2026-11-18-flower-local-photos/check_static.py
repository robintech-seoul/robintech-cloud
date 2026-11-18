#!/usr/bin/env python3
"""Static checks for the flower sample's local photos (no browser, no network). Run from the repository root.

usage: python3 docs/features/2026-11-18-flower-local-photos/check_static.py <check> [<check> ...]
checks: photos page scope playbook current all
"Merge-base" is `git merge-base HEAD main`. Exit 0 when every named check passes; otherwise prints each
failure and exits 1.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[3]
REL = "profile/flower-bomgyeol"
SITE = ROOT / REL
IMG = SITE / "img"
SOURCES = IMG / "sources.txt"
FOOD_SOURCES = ROOT / "profile/food-saebyeokmil/img/sources.txt"
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
PRECONNECT = re.compile(r'^[ \t]*<link rel="preconnect" href="https://images\.unsplash\.com">[ \t]*\r?\n', re.M)
IMG_SRC = re.compile(r'(<img\b[^>]*?\bsrc=")[^"]*(")', re.I)
fails = []


def fail(msg):
    fails.append(msg)


def read(path):
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def git(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    return r.returncode, r.stdout


def merge_base():
    code, out = git("merge-base", "HEAD", "main")
    if code:
        fail("no merge-base between HEAD and main")
        return None
    return out.decode().strip()


def base_file(base, rel):
    code, out = git("show", f"{base}:{rel}")
    if code:
        fail(f"{rel} not found at merge-base {base[:8]}")
        return None
    return out


class Imgs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.srcs = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.srcs.append(dict(attrs).get("src") or "")


def img_srcs(html):
    p = Imgs()
    p.feed(html)
    return p.srcs


def image_files():
    return sorted(f for f in IMG.iterdir() if f.is_file() and f.name != "sources.txt"
                  and not f.name.startswith(".")) if IMG.is_dir() else []


def sources():
    """{file: (page URL, download URL)}; malformed lines are reported."""
    out = {}
    for ln in read(SOURCES).splitlines():
        if not ln.strip():
            continue
        parts = ln.split()
        if len(parts) != 3:
            fail(f"AC12 sources.txt line is not '<file> <page URL> <download URL>': {ln}")
            continue
        if parts[0] in out:
            fail(f"AC12 sources.txt lists {parts[0]} twice")
        out[parts[0]] = (parts[1], parts[2])
    return out


def photo_id(url):
    m = re.search(r"images\.unsplash\.com/(photo-[0-9]+-[0-9a-f]+)", url)
    return m.group(1) if m else None


def sips_size(path):
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True)
    w = re.search(r"pixelWidth:\s*(\d+)", r.stdout)
    h = re.search(r"pixelHeight:\s*(\d+)", r.stdout)
    return (int(w.group(1)), int(h.group(1))) if w and h else (None, None)


# --- checks -------------------------------------------------------------------------------------

def check_photos():  # AC8-AC14 AC16 AC18
    files = image_files()
    if not files:
        fail(f"AC8 {REL}/img/ has no image files")
    src = sources()
    total = 0
    for f in files:
        head = f.read_bytes()[:12]
        if not (f.suffix.lower() == ".jpg" and head[:3] == b"\xff\xd8\xff"
                or f.suffix.lower() == ".webp" and head[:4] == b"RIFF" and head[8:] == b"WEBP"):
            fail(f"AC8 not a JPEG named .jpg or a WebP named .webp: img/{f.name}")
        size = f.stat().st_size
        total += size
        if size > 500 * 1024:
            fail(f"AC10 larger than 500 KB: img/{f.name} ({size // 1024} KB)")
        w, _ = sips_size(f)
        if w is None or w > 2000:
            fail(f"AC9 wider than 2000 px or unreadable: img/{f.name} ({w})")
        if f.name in src:
            want = parse_qs(urlparse(src[f.name][1]).query).get("w", [None])[0]
            if want is None or str(w) != want:
                fail(f"AC16 img/{f.name} is {w} px wide, its download URL asks w={want}")
    if total > 3 * 1024 * 1024:
        fail(f"AC11 img/ totals {total / 1024 / 1024:.2f} MB > 3 MB")
    if sorted(src) != [f.name for f in files]:
        fail(f"AC12 sources.txt files {sorted(src)} != img/ files {[f.name for f in files]}")
    for name, (page_url, dl) in src.items():
        if page_url != "-" and not page_url.startswith("https://unsplash.com/photos/"):
            fail(f"AC12 page URL is neither an Unsplash photo page nor '-': {name} {page_url}")
        if not dl.startswith("https://images.unsplash.com/photo-"):
            fail(f"AC13 download URL not allowed: {name} {dl}")
    raw = read(SOURCES)
    if "plus.unsplash.com" in raw or "premium_photo" in raw:
        fail("AC14 sources.txt mentions plus.unsplash.com or premium_photo")
    food = read(FOOD_SOURCES)
    for name, (_, dl) in src.items():
        pid = photo_id(dl)
        if pid and pid in food:
            fail(f"AC18 photo {pid} ({name}) is also in food-saebyeokmil/img/sources.txt")


def check_page():  # AC4-AC7 AC15
    html, css = read(SITE / "index.html"), read(SITE / "style.css")
    for url in re.findall(r"https?://[^\s\"'()<>,]+", html + css):
        if urlparse(url).netloc not in FONT_HOSTS:
            fail(f"AC5 URL with a host that is not allowed: {url}")
    srcs = img_srcs(html)
    files = {f.name for f in image_files()}
    for s in srcs:
        m = re.fullmatch(r"img/([^/?#]+)", s)
        if not m or m.group(1) not in files:
            fail(f"AC6 <img> src is not img/<file> of an existing file: {s!r}")
    for name in sorted(files - {s.removeprefix("img/") for s in srcs}):
        fail(f"AC7 img/{name} is not used by any <img>")
    base = merge_base()
    old = base_file(base, f"{REL}/index.html") if base else None
    if old is None:
        return
    old = old.decode("utf-8")

    def norm(t):
        return IMG_SRC.sub(r"\1SRC\2", PRECONNECT.sub("", t))
    if norm(old) != norm(html):
        fail("AC4 index.html differs from the merge-base beyond the preconnect line and <img> src values")
    old_srcs, src = img_srcs(old), sources()
    if len(old_srcs) != len(srcs):
        fail(f"AC15 merge-base page has {len(old_srcs)} <img>, branch page has {len(srcs)}")
    for i, (was, now) in enumerate(zip(old_srcs, srcs), 1):
        dl = src.get(now.removeprefix("img/"), (None, None))[1]
        if dl != was:
            fail(f"AC15 <img> #{i} now {now!r} with download URL {dl!r}, merge-base src {was!r}")


def check_scope():  # AC1-AC3
    base = merge_base()
    if not base:
        return
    _, out = git("diff", "--name-only", base)
    _, new = git("ls-files", "--others", "--exclude-standard")
    for path in sorted(set((out + new).decode().split())):
        if not path.startswith((REL + "/", "docs/")):
            fail(f"AC1 file outside {REL}/ and docs/ changed: {path}")
    for ac, name in (("AC2", "style.css"), ("AC3", "thumb.jpg")):
        old = base_file(base, f"{REL}/{name}")
        path = SITE / name
        if old is not None and (not path.is_file() or path.read_bytes() != old):
            fail(f"{ac} {REL}/{name} differs from its merge-base version")


def check_playbook():  # AC26 AC28
    text = read(ROOT / "docs/profile-playbook.md")
    for ln in text.splitlines():
        if "flower-bomgyeol" in ln and re.search(r"예외|직접 링크|핫링크|hotlink", ln, re.I):
            fail(f"AC26 playbook still says flower-bomgyeol links its photos directly: {ln.strip()[:90]}")
    m = re.search(r"^- \*\*사진:\*\*.*?(?=^- \*\*|^#|\Z)", text, re.M | re.S)
    if not m or "sources.txt" not in m.group(0) or not re.search(r"페이지[^\n]*`-`|`-`[^\n]*페이지", m.group(0)):
        fail("AC28 the playbook photo rule does not say the sources.txt page URL may be `-`")


def check_current():  # AC27
    text = read(ROOT / "docs/current_system/profile-samples/component.md")
    m = re.search(r"^## Depends on\n.*?(?=^## |\Z)", text, re.M | re.S)
    if not m:
        fail("AC27 component.md has no '## Depends on' section")
    elif "flower-bomgyeol" in m.group(0):
        fail("AC27 component.md Depends on still names flower-bomgyeol as an exception")


CHECKS = {"photos": check_photos, "page": check_page, "scope": check_scope,
          "playbook": check_playbook, "current": check_current}

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
