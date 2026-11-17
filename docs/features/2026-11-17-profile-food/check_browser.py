#!/usr/bin/env python3
"""Browser checks for the food profile sample (Playwright + installed Google Chrome). Run from the repo root.

usage: python3 docs/features/2026-11-17-profile-food/check_browser.py page|gallery [--shots DIR]
  page     AC7 AC14 AC15 AC16 AC19 AC30 AC31 AC32; writes full-page screenshots for AC33/AC34
           to DIR (default /tmp/profile-food-shots): desktop-1440.png, mobile-390.png
  gallery  AC35 AC36 AC37 AC38 on /profile/
Serves the repository root on a free local port itself. Exit 0 only when every check passes.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
SLUG = "food-saebyeokmil"
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
KOREAN_FONT = re.compile(r"Pretendard|\bKR\b|Nanum|Gowun|Gothic A1|Hahmlet|Song Myung|Black Han Sans|Do Hyeon|Jua"
                         r"|Orbit|Sunflower|Gaegu|Dongle|Hi Melody|Gamja Flower|Poor Story|Stylish|Yeon Sung"
                         r"|Gugi|Dokdo|Single Day|Cute Font|Kirang Haerang|Bagel Fat One|Diphylleia", re.I)
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
fails = []


def fail(msg):
    fails.append(msg)


def serve():
    handler = partial(type("Quiet", (SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}),
                      directory=str(ROOT))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_port}"


def settle(target):
    """Wait for fonts, then scroll through once so lazy images and reveal effects run."""
    target.evaluate("""async () => {
      await document.fonts.ready;
      const h = () => document.documentElement.scrollHeight;
      for (let y = 0; y < h(); y += innerHeight / 2) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
      scrollTo(0, 0); await new Promise(r => setTimeout(r, 300));
    }""")


IN_VIEW = """el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
  if (!r.width || !r.height || s.visibility === 'hidden' || +s.opacity === 0) return false;
  if (r.top < 0 || r.left < 0 || r.bottom > innerHeight || r.right > innerWidth) return false;
  const t = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
  return !!t && (el === t || el.contains(t)); }"""


def mark_visible(target, label):  # AC7
    loc = target.get_by_text(MARK, exact=False)
    if not any(loc.nth(i).evaluate(IN_VIEW) for i in range(loc.count())):
        fail(f"AC7 sample notice not visible without scrolling at {label}")


def kakao(target):
    return target.get_by_role("link", name=re.compile("카카오톡.*주문")).or_(
        target.get_by_role("button", name=re.compile("카카오톡.*주문")))


def kakao_visible(target):
    loc = kakao(target)
    return any(loc.nth(i).evaluate(IN_VIEW) for i in range(loc.count()))


def no_overflow(target, label):  # AC31 AC32
    w = target.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    if w[0] > w[1]:
        fail(f"{label} horizontal overflow: scrollWidth {w[0]} > clientWidth {w[1]}")


def price_fonts(page, label):  # AC19: the digits of each price in a Korean face or a monospaced face
    texts = page.evaluate("""() => { let n = 0; const texts = [];
      const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), hosts = new Set();
      while (walk.nextNode()) { const t = walk.currentNode;
        if (/\\d[\\d,]*\\s?원/.test(t.nodeValue) && t.parentElement.getClientRects().length) hosts.add(t.parentElement); }
      for (const el of hosts) {  // a probe that inherits the element's font: all digits, then one span per character
        texts.push(el.textContent.replace(/\\s+/g, ' ').trim().slice(0, 60));
        const probe = document.createElement('span');
        probe.setAttribute('data-price-probe', String(n++));
        probe.style.cssText = 'position:absolute;left:-10000px;top:0;white-space:pre';
        const all = document.createElement('span');
        all.setAttribute('data-price-digits', '');
        all.textContent = '0123456789';
        probe.append(all);
        for (const c of '0123456789iM') { const s = document.createElement('span');
          s.setAttribute('data-price-char', ''); s.textContent = c; probe.append(s); }
        el.append(probe); }
      return texts; }""")
    if not texts:
        fail(f"AC19 no visible price (…원) found at {label}")
        return
    widths = page.evaluate("""() => [...document.querySelectorAll('[data-price-probe]')].map(p =>
      [...p.querySelectorAll('[data-price-char]')].map(s => s.getBoundingClientRect().width))""")
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
    for i, ws in enumerate(widths):
        node = cdp.send("DOM.querySelector", {"nodeId": root,
                                              "selector": f'[data-price-probe="{i}"] [data-price-digits]'})["nodeId"]
        fonts = cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]
        main = max(fonts, key=lambda f: f["glyphCount"])["familyName"] if fonts else None
        mono = bool(ws) and min(ws) > 0 and max(ws) <= min(ws) * 1.005
        if not main or not (KOREAN_FONT.search(main) or mono):
            fail(f"AC19 price digits rendered in {main!r}, neither Korean nor monospaced, at {label}: {texts[i]}")
    page.evaluate("document.querySelectorAll('[data-price-probe]').forEach(p => p.remove())")


def keep_all(page):  # AC16
    bad = page.evaluate("""() => [...document.querySelectorAll('p, li, dd')]
      .filter(e => /[가-힣]/.test(e.textContent) && getComputedStyle(e).wordBreak !== 'keep-all')
      .map(e => e.textContent.trim().slice(0, 40))""")
    for t in bad:
        fail(f"AC16 Korean text without word-break: keep-all: {t}")


def reduced_motion(page):  # AC30
    bad = page.evaluate("""() => {
      const out = [], secs = v => v.split(',').map(s => parseFloat(s) * (s.trim().endsWith('ms') ? 0.001 : 1));
      for (const a of document.getAnimations()) {
        const d = a.effect && a.effect.getComputedTiming().duration;
        if (typeof d === 'number' && d > 10) out.push('running animation ' + (a.animationName || a.transitionProperty || 'js') + ' ' + d + 'ms');
      }
      for (const el of document.querySelectorAll('*')) for (const pseudo of [null, '::before', '::after']) {
        const s = getComputedStyle(el, pseudo);
        if (s.animationName !== 'none' && secs(s.animationDuration).some(x => x > 0.01)) out.push('animation on ' + el.tagName + (pseudo || ''));
        if (s.transitionProperty !== 'none' && secs(s.transitionDuration).some(x => x > 0.01)) out.push('transition on ' + el.tagName + (pseudo || '') + ' ' + s.transitionDuration);
      }
      return [...new Set(out)].slice(0, 10); }""")
    for b in bad:
        fail(f"AC30 under prefers-reduced-motion: {b}")


def font_responses(page):  # AC19: a missing web font must not pass through a locally installed copy
    bad = []
    page.on("response", lambda r: any(h in r.url for h in FONT_HOSTS) and r.status != 200
            and bad.append(f"{r.status} {r.url}"))
    page.on("requestfailed", lambda r: any(h in r.url for h in FONT_HOSTS) and bad.append(f"failed {r.url}"))
    return bad


def check_page(browser, base, shots):
    url = f"{base}/profile/{SLUG}/"
    shots.mkdir(parents=True, exist_ok=True)
    for name in ("desktop-1440.png", "mobile-390.png"):
        (shots / name).unlink(missing_ok=True)
    for label, vp in (("1440px", DESKTOP), ("390px", MOBILE)):
        ctx = browser.new_context(viewport=vp)
        page = ctx.new_page()
        bad_fonts = font_responses(page)
        page.goto(url, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1500)  # let entrance effects finish before judging the first screen
        mark_visible(page, label)
        if vp is MOBILE:
            if not kakao_visible(page):
                fail("AC14 카카오톡 button not visible without scrolling at 390px")
            positions = page.evaluate("""async () => { const out = [], H = document.documentElement.scrollHeight;
              for (let y = 0; ; y += innerHeight / 2) { const t = Math.min(y, H - innerHeight); out.push(t);
                if (t >= H - innerHeight) break; } return out; }""")
            for y in positions:
                page.evaluate(f"scrollTo({{top: {y}, behavior: 'instant'}})")
                for _ in range(15):  # up to 1.5 s for a sticky bar that slides in
                    page.wait_for_timeout(100)
                    if kakao_visible(page):
                        break
                else:
                    fail(f"AC15 카카오톡 button not reachable at scroll {int(y)}px (390px)")
            page.evaluate("scrollTo(0, 0)")
        else:
            no_overflow(page, "AC31 1440px")
            keep_all(page)
        price_fonts(page, label)
        for b in bad_fonts:
            fail(f"AC19 web font request did not return 200 at {label}: {b}")
        settle(page)
        page.screenshot(path=str(shots / ("desktop-1440.png" if vp is DESKTOP else "mobile-390.png")),
                        full_page=True)
        ctx.close()
    # AC32: the page inside a width:390px iframe, as docs/profile-playbook.md §4 does it
    ctx = browser.new_context(viewport=DESKTOP)
    page = ctx.new_page()
    page.goto(f"{base}/profile/")
    page.set_content(f'<iframe src="{url}" style="width:390px;height:844px;border:0"></iframe>')
    frame = page.frame_locator("iframe")
    frame.locator("body").wait_for()
    inner = page.frames[1]
    inner.wait_for_load_state("networkidle")
    settle(inner)
    no_overflow(inner, "AC32 390px iframe")
    ctx.close()
    # AC30, at both widths (a mobile-only sticky bar may declare its own transition)
    for vp in (DESKTOP, MOBILE):
        ctx = browser.new_context(viewport=vp, reduced_motion="reduce")
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle")
        settle(page)
        reduced_motion(page)
        ctx.close()
    print(f"screenshots for AC33/AC34: {shots / 'desktop-1440.png'} {shots / 'mobile-390.png'}")


def check_gallery(browser, base):
    ctx = browser.new_context(viewport=DESKTOP)
    page = ctx.new_page()
    page.goto(f"{base}/profile/", wait_until="networkidle")
    page.click('.pf-filters button[data-filter="food"]')
    card = page.locator(f'a.pf-card[data-slug="{SLUG}"]')
    if not card.count() or not card.is_visible():
        fail("AC35 food filter does not show the new card")
        ctx.close()
        return
    if page.locator('.pf-empty[data-industry="food"]:visible').count():
        fail("AC35 food filter still shows a 준비 중 tile")
    card.click()
    viewer, iframe = page.locator("#pf-viewer"), page.locator("#pf-v-iframe")
    page.wait_for_timeout(300)
    if not viewer.is_visible() or not (iframe.get_attribute("src") or "").endswith(f"/profile/{SLUG}/"):
        fail("AC36 clicking the card does not open the preview with the sample")
    else:
        frame = page.frame_locator("#pf-v-iframe")
        try:
            frame.get_by_text(MARK, exact=False).first.wait_for(state="attached", timeout=10000)
        except Exception:
            fail("AC36 the sample did not load in the preview iframe")
    width = "document.getElementById('pf-v-iframe').getBoundingClientRect().width"
    for device, cond in (("mobile", "<= 400"), ("desktop", "> 600")):  # the width animates; wait for it
        page.click(f'button[data-device="{device}"]')
        try:
            page.wait_for_function(f"{width} {cond}", timeout=3000)
        except Exception:
            fail(f"AC37 {device} button does not switch the preview width ({page.evaluate(width)})")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    if viewer.is_visible():
        fail("AC38 Esc does not close the preview")
    ctx.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] not in ("page", "gallery"):
        raise SystemExit(__doc__)
    shots = Path(args[args.index("--shots") + 1]) if "--shots" in args else Path("/tmp/profile-food-shots")
    if not (ROOT / "profile" / SLUG / "index.html").is_file():
        print(f"FAIL profile/{SLUG}/index.html does not exist")
        sys.exit(1)
    httpd, base = serve()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        try:
            check_page(browser, base, shots) if args[0] == "page" else check_gallery(browser, base)
        except Exception as exc:  # a missing element or timeout is a failed check, not a crash
            fail(f"{args[0]}: {type(exc).__name__}: {str(exc).splitlines()[0]}")
        browser.close()
    httpd.shutdown()
    for f in fails:
        print("FAIL", f)
    print(f"{'PASS' if not fails else 'FAIL'}: {args[0]} ({len(fails)} failures)")
    sys.exit(1 if fails else 0)
