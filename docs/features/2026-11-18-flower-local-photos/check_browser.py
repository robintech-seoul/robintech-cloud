#!/usr/bin/env python3
"""Browser checks for the flower sample's local photos (Playwright + installed Google Chrome). Run from the repo root.

usage: python3 docs/features/2026-11-18-flower-local-photos/check_browser.py page|gallery|compare [--shots DIR]
  page     AC19 AC20 AC21: local server and web fonts only
  gallery  AC22 AC23 on /profile/
  compare  AC17, and the AC24/AC25 screenshots; needs images.unsplash.com. Writes to DIR
           (default /tmp/flower-local-photos-shots): {before,after}-{1440,390}.png, side-{1440,390}.png,
           side-{1440,390}-NN.png (1200 px tall bands of the side-by-side) and summary.txt.
           "before" is the merge-base page (git merge-base HEAD main), still loading its photos from Unsplash.
Serves the repository root on a free local port itself. Exit 0 only when every check passes.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
REL = "profile/flower-bomgyeol"
SOURCES = ROOT / REL / "img/sources.txt"
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
VIEWPORTS = {1440: {"width": 1440, "height": 900}, 390: {"width": 390, "height": 844}}
BAND = 1200
N_IMG = 9  # spec Assumptions: the page has nine <img>
fails = []


def fail(msg):
    fails.append(msg)


def serve(directory):
    handler = partial(type("Quiet", (SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}),
                      directory=str(directory))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_port}"


def settle(target):
    """Scroll to the end in half-screen steps so lazy images start; ends at the bottom."""
    target.evaluate("""async () => {
      await document.fonts.ready;
      const h = () => document.documentElement.scrollHeight;
      for (let y = 0; y < h(); y += innerHeight / 2) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
      scrollTo(0, h()); await new Promise(r => setTimeout(r, 300));
    }""")


def images_loaded(target, ac, label):
    """Wait up to 20 s for every <img> to finish; fail each one without a natural width, or a wrong count."""
    n = target.evaluate("document.images.length")
    if n != N_IMG:
        fail(f"{ac} page has {n} <img> at {label}, expected {N_IMG}")
        return False
    try:
        target.wait_for_function("[...document.images].every(i => i.complete)", timeout=20000)
    except Exception:
        pass
    bad = target.evaluate("[...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src)")
    for src in bad:
        fail(f"{ac} image did not load at {label}: {src}")
    return not bad


def check_page(browser, base):
    url = f"{base}/profile/flower-bomgyeol/"
    ctx = browser.new_context(viewport=VIEWPORTS[1440])
    page = ctx.new_page()
    local = urlparse(base).netloc
    foreign = []
    page.on("request", lambda r: urlparse(r.url).scheme in ("http", "https")
            and urlparse(r.url).netloc != local and urlparse(r.url).hostname not in FONT_HOSTS
            and foreign.append(r.url))
    page.goto(url, wait_until="networkidle")
    settle(page)
    images_loaded(page, "AC19", "1440px")
    page.wait_for_load_state("networkidle")
    for u in sorted(set(foreign)):
        fail(f"AC21 request to a host that is not allowed: {u}")
    ctx.close()
    # AC20: the page inside a width:390px iframe, as docs/profile-playbook.md §4 does it
    ctx = browser.new_context(viewport=VIEWPORTS[1440])
    page = ctx.new_page()
    page.goto(f"{base}/profile/")
    page.set_content(f'<iframe src="{url}" style="width:390px;height:844px;border:0"></iframe>')
    page.frame_locator("iframe").locator("body").wait_for()
    inner = page.frames[1]
    inner.wait_for_load_state("networkidle")
    settle(inner)
    images_loaded(inner, "AC20", "390px iframe")
    ctx.close()


def check_gallery(browser, base):
    ctx = browser.new_context(viewport=VIEWPORTS[1440])
    page = ctx.new_page()
    page.goto(f"{base}/profile/", wait_until="networkidle")
    page.click('.pf-filters button[data-filter="flower"]')
    card = page.locator('a.pf-card[data-slug="flower-bomgyeol"]')
    if not card.count() or not card.is_visible():
        fail("AC22 flower filter does not show the flower-bomgyeol card")
        ctx.close()
        return
    thumb = card.locator("img")
    thumb.scroll_into_view_if_needed()
    try:
        thumb.evaluate("i => i.complete || new Promise(r => { i.onload = r; i.onerror = r; setTimeout(r, 15000); })")
    except Exception:
        pass
    if not thumb.evaluate("i => i.complete && i.naturalWidth > 0"):
        fail("AC22 the flower card's thumbnail did not load")
    card.click()
    viewer, iframe = page.locator("#pf-viewer"), page.locator("#pf-v-iframe")
    page.wait_for_timeout(300)
    if not viewer.is_visible() or not (iframe.get_attribute("src") or "").endswith("/profile/flower-bomgyeol/"):
        fail("AC23 clicking the card does not open the preview with the sample")
    else:
        try:
            page.frame_locator("#pf-v-iframe").get_by_text(MARK, exact=False).first.wait_for(
                state="attached", timeout=10000)
        except Exception:
            fail("AC23 the sample did not load in the preview iframe")
    ctx.close()


def sips_size(path):
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True)
    w = re.search(r"pixelWidth:\s*(\d+)", r.stdout)
    h = re.search(r"pixelHeight:\s*(\d+)", r.stdout)
    return (int(w.group(1)), int(h.group(1))) if w and h else (None, None)


def shoot(browser, url, width, path):
    """Full-page screenshot at scroll 0 after every image loaded. Both pages are shot alike: reduced motion,
    no transitions, and the fixed header pinned to the top, so the capture shows it once, in its top state."""
    ctx = browser.new_context(viewport=VIEWPORTS[width], reduced_motion="reduce")
    page = ctx.new_page()
    page.goto(url, wait_until="networkidle")
    settle(page)
    ok = images_loaded(page, "AC24" if width == 1440 else "AC25", f"{width}px {path.stem}")
    page.add_style_tag(content="*, *::before, *::after { transition: none !important; animation: none !important; }"
                               " html { scroll-behavior: auto !important; } .top { position: absolute !important; }")
    page.evaluate("async () => { scrollTo({top: 0, behavior: 'instant'}); dispatchEvent(new Event('scroll'));"
                  " await document.fonts.ready; }")
    page.wait_for_function("scrollY === 0 && !document.getElementById('top').classList.contains('solid')",
                           timeout=5000)
    page.wait_for_load_state("networkidle")
    info = page.evaluate("""() => ({height: document.documentElement.scrollHeight,
      natural: [...document.images].map(i => `${i.naturalWidth}x${i.naturalHeight}`),
      imgs: [...document.images].map(i => { const r = i.getBoundingClientRect();
        return `${i.alt} | natural ${i.naturalWidth}x${i.naturalHeight} | box ${Math.round(r.width)}x${Math.round(r.height)}`
          + ` at y ${Math.round(r.top + scrollY)}`; })})""")
    if ok:
        page.screenshot(path=str(path), full_page=True)
    ctx.close()
    return ok, info


def side_by_side(browser, shots_url, shots, width):
    a, b = f"before-{width}.png", f"after-{width}.png"
    (wa, ha), (wb, hb) = sips_size(shots / a), sips_size(shots / b)
    gap, label = 24, 40
    total_w, total_h = wa + wb + gap, max(ha, hb) + label
    ctx = browser.new_context(viewport={"width": total_w, "height": 900})
    page = ctx.new_page()
    page.goto(f"{shots_url}/")
    page.set_content(f"""<style>body{{margin:0;background:#777;font:bold 24px sans-serif;color:#fff}}
      .row{{display:flex;gap:{gap}px;align-items:flex-start}} .c{{width:{wa}px}} .c+.c{{width:{wb}px}}
      .l{{height:{label}px;line-height:{label}px;padding-left:8px}} img{{display:block}}</style>
      <div class="row"><div class="c"><div class="l">merge-base</div><img src="{a}"></div>
      <div class="c"><div class="l">branch</div><img src="{b}"></div></div>""")
    page.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth)")
    page.screenshot(path=str(shots / f"side-{width}.png"), full_page=True)
    n = 0
    for y in range(0, total_h, BAND):
        n += 1
        page.screenshot(path=str(shots / f"side-{width}-{n:02d}.png"), full_page=True,
                        clip={"x": 0, "y": y, "width": total_w, "height": min(BAND, total_h - y)})
    ctx.close()
    return n


def check_compare(browser, base, shots):
    lines = [ln.split() for ln in SOURCES.read_text(encoding="utf-8").splitlines() if ln.strip()]
    # AC17: the height each download URL serves, read by the browser, against the local file
    ctx = browser.new_context()
    page = ctx.new_page()
    served = page.evaluate("""urls => Promise.all(urls.map(u => new Promise(r => { const i = new Image();
      i.onload = () => r([i.naturalWidth, i.naturalHeight]); i.onerror = () => r(null);
      setTimeout(() => r(null), 15000); i.src = u; })))""",
                           [ln[-1] for ln in lines])
    ctx.close()
    for ln, got in zip(lines, served):
        name = ln[0]
        w, h = sips_size(ROOT / REL / "img" / name)
        if got is None:
            fail(f"AC17 download URL of {name} did not load: {ln[-1]}")
        elif h != got[1]:
            fail(f"AC17 img/{name} is {h} px high, its download URL serves {got[1]} px")
    # AC24 AC25: before (merge-base, hotlinking Unsplash) and after screenshots, then side by side
    r = subprocess.run(["git", "merge-base", "HEAD", "main"], cwd=ROOT, capture_output=True, text=True)
    mb = r.stdout.strip()
    if r.returncode or not mb:
        fail("no merge-base between HEAD and main")
        return
    shots.mkdir(parents=True, exist_ok=True)
    for old in [*shots.glob("*.png"), shots / "summary.txt"]:
        old.unlink(missing_ok=True)
    tree = subprocess.run(["git", "rev-parse", f"HEAD:{REL}"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", REL], cwd=ROOT, capture_output=True,
                           text=True).stdout.strip()
    summary = [f"merge-base {mb}", f"site tree {tree}", f"site working tree {'dirty' if dirty else 'clean'}"]
    with tempfile.TemporaryDirectory() as tmp:
        site = Path(tmp) / REL
        site.mkdir(parents=True)
        for name in ("index.html", "style.css"):
            out = subprocess.run(["git", "show", f"{mb}:{REL}/{name}"], cwd=ROOT, capture_output=True)
            if out.returncode:
                fail(f"git show {mb[:8]}:{REL}/{name} failed")
                return
            (site / name).write_bytes(out.stdout)
        before_httpd, before = serve(tmp)
        shots_httpd, shots_url = serve(shots)
        try:
            for width in (1440, 390):
                ok_a, info_a = shoot(browser, f"{before}/{REL}/", width, shots / f"before-{width}.png")
                ok_b, info_b = shoot(browser, f"{base}/{REL}/", width, shots / f"after-{width}.png")
                summary.append(f"\n{width}px page height: before {info_a['height']}, after {info_b['height']}")
                if info_a["natural"] != info_b["natural"]:
                    fail(f"AC{24 if width == 1440 else 25} natural image sizes differ at {width}px:"
                         f" before {info_a['natural']}, after {info_b['natural']}")
                for i, (x, y) in enumerate(zip(info_a["imgs"], info_b["imgs"]), 1):
                    summary.append(f"  #{i} before {x}\n     after  {y}")
                if ok_a and ok_b:
                    summary.append(f"  side-{width}.png + {side_by_side(browser, shots_url, shots, width)} bands")
        finally:
            before_httpd.shutdown()
            shots_httpd.shutdown()
    shots_summary.extend(summary)
    print(f"screenshots for AC24/AC25 in {shots}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] not in ("page", "gallery", "compare"):
        raise SystemExit(__doc__)
    shots = Path(args[args.index("--shots") + 1]) if "--shots" in args else Path("/tmp/flower-local-photos-shots")
    shots_summary = []
    if args[0] != "gallery" and not SOURCES.is_file():  # nothing to check before the photos exist; no network
        print(f"FAIL {REL}/img/sources.txt does not exist")
        sys.exit(1)
    httpd, base = serve(ROOT)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        try:
            {"page": check_page, "gallery": check_gallery}.get(args[0], lambda b, u: check_compare(b, u, shots))(
                browser, base)
        except Exception as exc:  # a missing element or timeout is a failed check, not a crash
            fail(f"{args[0]}: {type(exc).__name__}: {str(exc).splitlines()[0]}")
        browser.close()
    httpd.shutdown()
    for f in fails:
        print("FAIL", f)
    print(f"{'PASS' if not fails else 'FAIL'}: {args[0]} ({len(fails)} failures)")
    if shots_summary:  # written last, so it names the result of the run that made the shots
        result = ["result PASS"] if not fails else ["result FAIL"] + [f"  {f}" for f in fails]
        (shots / "summary.txt").write_text("\n".join(shots_summary + [""] + result) + "\n", encoding="utf-8")
    sys.exit(1 if fails else 0)
