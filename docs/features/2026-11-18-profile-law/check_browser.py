#!/usr/bin/env python3
"""Browser checks for the two law-firm profile samples (Playwright + installed Google Chrome). Run from the repo root.

usage: python3 docs/features/2026-11-18-profile-law/check_browser.py page <slug> | gallery | compare [--shots DIR]
  page <slug>  AC4 (thumb.jpg is the current first screen) AC7 AC42 AC43 AC44 AC47 AC50 AC63 AC64 AC65 AC119, and
               A (law-ganeum): AC85 AC86 AC87 AC88 AC89 AC93, C (law-goim): AC97 AC99 AC100 AC108 AC112. Empties DIR/<slug>/
               first, then writes full-page screenshots for AC66/AC67 (desktop-1440.png, mobile-390.png, and the
               same cut into 1200 px bands -NN.png) and summary.txt last.
  gallery      AC68 AC70 AC78 AC79 AC80 on /profile/
  compare      evidence for AC71-AC73 and AC113-AC117, not a check: rewrites DIR/compare/ with first screens
               (1440x900 and 390x844) of the two law samples, flower-bomgyeol, food-saebyeokmil and the three clinic
               samples, full pages (and bands) of the five shipped samples, and of each reference site its first
               screen and full page at 1440 and its visible text (ref-<slug>.png, ref-<slug>-full.png and its -NN
               bands, ref-<slug>.txt; an HTTP error counts as no answer; the last good copy is kept when a site does
               not answer). summary.txt lists each local tree hash and each reference as ok, cached or unreachable.
               Exit 0 when every local screenshot was written.
DIR defaults to /tmp/profile-law-shots. Serves the repository root on a free local port itself.
The page clock is fixed at Sunday 2026-11-15 11:00 KST, so a "today" line cannot change between runs.
The page contract these checks read is the "Fixed parameters" section of tasks.md in this folder.
"""
from datetime import datetime, timedelta, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import base64
import re
import shutil
import subprocess
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
SAMPLES = {
    "law-ganeum": {"name": "법무법인 가늠", "stem": "가늠", "ref": "https://www.selendygay.com/"},
    "law-goim": {"name": "법무법인 고임", "stem": "고임", "ref": "https://www.kimchang.com/"},
}
SHIPPED = ("flower-bomgyeol", "food-saebyeokmil", "clinic-neuru", "clinic-byeotteul", "clinic-bonui")
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
NOTICE = MARK.removeprefix("로빈테크 ")  # AC119: the short notice, a part of MARK, so the full line counts too
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
CLOCK = datetime(2026, 11, 15, 11, 0, tzinfo=timezone(timedelta(hours=9)))  # a Sunday
KOREAN_FONT = re.compile(r"Pretendard|\bKR\b|Nanum|Gowun|Gothic A1|Hahmlet|Song Myung|Black Han Sans|Do Hyeon|Jua"
                         r"|Orbit|Sunflower|Gaegu|Dongle|Hi Melody|Gamja Flower|Poor Story|Stylish|Yeon Sung"
                         r"|Gugi|Dokdo|Single Day|Cute Font|Kirang Haerang|Bagel Fat One|Diphylleia", re.I)
A_H1_FACES = ("Nanum Myeongjo", "Gowun Batang", "Hahmlet", "Song Myung")  # AC85
SERIF_FONT = re.compile(r"serif|Myeongjo|Batang|Hahmlet|Song Myung|Garamond|Cormorant|Times|Georgia|Mincho"
                        r"|Diphylleia|Baskerville|Playfair|Lora|Merriweather|Libre Caslon|Spectral", re.I)
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
CONTROLS = ("상담 예약", "전화")  # AC42-AC44
THUMB_MAX_DIFF = 15.0  # mean absolute RGB difference (0-255) at 160x100 between thumb.jpg and a fresh first screen
fails = []


def fail(msg):
    fails.append(msg)


def serif(name):
    return bool(SERIF_FONT.search(name or "")) and not re.search(r"sans", name or "", re.I)


def serve():
    handler = partial(type("Quiet", (SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}),
                      directory=str(ROOT))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_port}"


def new_page(browser, vp, **kw):
    ctx = browser.new_context(viewport=vp, timezone_id="Asia/Seoul", **kw)
    page = ctx.new_page()
    page.clock.set_fixed_time(CLOCK)
    return ctx, page


def settle(target):
    """Wait for fonts, then scroll through once so lazy images and reveal effects run."""
    target.evaluate("""async () => {
      await document.fonts.ready;
      const h = () => document.documentElement.scrollHeight;
      for (let y = 0; y < Math.min(h(), 30000); y += innerHeight / 2) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
      scrollTo(0, 0); await new Promise(r => setTimeout(r, 300));
    }""")


IN_VIEW = """el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
  let o = 1; for (let e = el; e; e = e.parentElement) o *= +getComputedStyle(e).opacity;
  if (!r.width || !r.height || s.visibility === 'hidden' || o <= 0.5) return false;
  if (r.top < 0 || r.left < 0 || r.bottom > innerHeight || r.right > innerWidth) return false;
  const style = document.createElement('style');  // a pointer-events:none layer still covers what is under it
  style.textContent = '*, *::before, *::after { pointer-events: auto !important; }';
  document.head.append(style);
  const stack = document.elementsFromPoint(r.left + r.width / 2, r.top + r.height / 2);
  style.remove();
  const fill = c => { if (c.backgroundImage !== 'none') return 1; const m = c.backgroundColor.match(/rgba?\\(([^)]*)\\)/);
    return m ? +(m[1].split(/[\\s,\\/]+/).filter(Boolean)[3] ?? 1) : 0; };
  const paints = e => {  // the paint that was hit: an ancestor of el only through its ::before/::after
    let o = 1; for (let x = e; x; x = x.parentElement) o *= +getComputedStyle(x).opacity;
    const own = getComputedStyle(e), parts = e.contains(el) ? [] : [[own, 1]];
    for (const ps of ['::before', '::after']) { const c = getComputedStyle(e, ps);
      if (c.content !== 'none' && c.content !== 'normal' && c.display !== 'none') parts.push([c, +c.opacity]); }
    return own.visibility !== 'hidden' && parts.some(([c, po]) => fill(c) * po * o > 0.5); };
  for (const t of stack) { if (el === t || el.contains(t)) return true; if (paints(t)) return false; }
  return false; }"""


def any_visible(loc):
    return any(loc.nth(i).evaluate(IN_VIEW) for i in range(loc.count()))


def control(page, word):
    name = re.compile(re.escape(word))
    return page.get_by_role("link", name=name).or_(page.get_by_role("button", name=name))


POSITIONS = """() => { const out = [], H = document.documentElement.scrollHeight;
  for (let y = 0; ; y += innerHeight / 2) { const t = Math.min(y, H - innerHeight); out.push(t);
    if (t >= H - innerHeight) break; } return out; }"""  # every half screen down to the end (AC44 AC119)

LAST_FOOTER_TEXT = """() => { const f = [...document.querySelectorAll('footer')].pop(); if (!f) return null;
  const pinned = e => { for (; e; e = e.parentElement) if (/fixed|sticky/.test(getComputedStyle(e).position)) return true;
    return false; };  // a bar inside <footer> is not the footer's last line
  return [f, ...f.querySelectorAll('*')].filter(e => e.getClientRects().length && !pinned(e)
    && [...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim())).pop() || null; }"""


def notice_everywhere(page, label):  # AC119: the notice on screen at every scroll position; the footer's end uncovered
    loc = page.get_by_text(NOTICE, exact=False)
    positions = page.evaluate(POSITIONS)
    for y in positions:
        page.evaluate(f"scrollTo({{top: {y}, behavior: 'instant'}})")
        for _ in range(15):  # up to 1.5 s for a sticky bar that slides in
            if any_visible(loc):
                break
            page.wait_for_timeout(100)
        else:
            fail(f"AC119 sample notice '{NOTICE}' not visible at scroll {int(y)}px of {int(positions[-1])}px ({label})")
    page.evaluate("scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")  # the page may have grown
    page.wait_for_timeout(200)
    last = page.evaluate_handle(LAST_FOOTER_TEXT).as_element()
    if not last:
        fail(f"AC119 no <footer> text to read at the end of the page ({label})")
    elif not last.evaluate(IN_VIEW):
        fail(f"AC119 the footer's last text line is covered or off screen at the end of the page ({label}): "
             f"{last.evaluate('e => e.textContent.trim().slice(0, 40)')}")
    page.evaluate("scrollTo(0, 0)")


def no_overflow(target, label):  # AC64 AC65
    w = target.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    if w[0] > w[1]:
        fail(f"{label} horizontal overflow: scrollWidth {w[0]} > clientWidth {w[1]}")


def keep_all(page):  # AC47
    bad = page.evaluate("""() => [...document.querySelectorAll('p, li, dd, dt, td, th')]
      .filter(e => /[가-힣]/.test(e.textContent) && getComputedStyle(e).wordBreak !== 'keep-all')
      .map(e => e.textContent.trim().slice(0, 40))""")
    for t in bad:
        fail(f"AC47 Korean text without word-break: keep-all: {t}")


def main_font(page, handle):  # the platform font that renders most glyphs of the element (CDP)
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    handle.evaluate("e => e.setAttribute('data-font-probe', '')")
    root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
    node = cdp.send("DOM.querySelector", {"nodeId": root, "selector": "[data-font-probe]"})["nodeId"]
    fonts = cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]
    handle.evaluate("e => e.removeAttribute('data-font-probe')")
    cdp.detach()
    return max(fonts, key=lambda f: f["glyphCount"])["familyName"] if fonts else None


def digit_fonts(page, label):  # AC50: digits of hours and phone numbers in a Korean or monospaced face
    texts = page.evaluate("""() => { let n = 0; const texts = [], re = /\\d{1,2}:\\d{2}|0\\d{1,2}-\\d{3,4}-\\d{4}/;
      const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), hosts = new Set();
      while (walk.nextNode()) { const t = walk.currentNode;
        if (re.test(t.nodeValue) && t.parentElement.getClientRects().length) hosts.add(t.parentElement); }
      for (const el of hosts) {
        texts.push(el.textContent.replace(/\\s+/g, ' ').trim().slice(0, 60));
        const probe = document.createElement('span');
        probe.setAttribute('data-digit-probe', String(n++));
        probe.style.cssText = 'position:absolute;left:-10000px;top:0;white-space:pre';
        const all = document.createElement('span');
        all.setAttribute('data-digit-all', '');
        all.textContent = '0123456789';
        probe.append(all);
        for (const c of '0123456789iM') { const s = document.createElement('span');
          s.setAttribute('data-digit-char', ''); s.textContent = c; probe.append(s); }
        el.append(probe); }
      return texts; }""")
    if not texts:
        fail(f"AC50 no visible 상담 시간 or phone number found at {label}")
        return
    widths = page.evaluate("""n => [...Array(n).keys()].map(i => [...document.querySelector(`[data-digit-probe="${i}"]`)
      .querySelectorAll('[data-digit-char]')].map(s => s.getBoundingClientRect().width))""", len(texts))
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
    for i, ws in enumerate(widths):
        node = cdp.send("DOM.querySelector", {"nodeId": root,
                                              "selector": f'[data-digit-probe="{i}"] [data-digit-all]'})["nodeId"]
        fonts = cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]
        main = max(fonts, key=lambda f: f["glyphCount"])["familyName"] if fonts else None
        mono = bool(ws) and min(ws) > 0 and max(ws) <= min(ws) * 1.005
        if not main or not (KOREAN_FONT.search(main) or mono):
            fail(f"AC50 digits rendered in {main!r}, neither Korean nor monospaced, at {label}: {texts[i]}")
    page.evaluate("document.querySelectorAll('[data-digit-probe]').forEach(p => p.remove())")
    cdp.detach()


def font_responses(page):  # AC50: every web font request returns 200
    bad = []
    page.on("response", lambda r: any(h in r.url for h in FONT_HOSTS) and r.status != 200
            and bad.append(f"{r.status} {r.url}"))
    page.on("requestfailed", lambda r: any(h in r.url for h in FONT_HOSTS) and bad.append(f"failed {r.url}"))
    return bad


def reduced_motion(page, label):  # AC63
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
        fail(f"AC63 under prefers-reduced-motion at {label}: {b}")


WORDMARK = """stem => { const header = document.querySelector('header'); if (!header) return null;
  const w = document.createTreeWalker(header, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) if (w.currentNode.nodeValue.includes(stem)) { const el = w.currentNode.parentElement;
    return el.closest('a') && header.contains(el.closest('a')) ? el.closest('a') : el; }
  return null; }"""


def wordmark_a(page, stem):  # AC86 AC87
    wm = page.evaluate_handle(WORDMARK, stem).as_element()
    if not wm:
        fail(f"AC86 AC87 no wordmark: no text containing '{stem}' inside the first <header>")
        return
    left = wm.evaluate("e => e.getBoundingClientRect().left")
    if left > 1440 / 4:
        fail(f"AC86 wordmark left edge at {left:.0f}px, not within the left quarter (360px) at 1440px")
    info = wm.evaluate("""e => [e, ...e.querySelectorAll('*')]
      .filter(x => [...x.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim()))
      .map(x => { const s = getComputedStyle(x); return [s.letterSpacing, parseFloat(s.fontSize)]; })""")
    for ls, size in info:
        px = 0.0 if ls == "normal" else float(re.sub(r"px$", "", ls))
        if px > 0.05 * size + 1e-6:
            fail(f"AC87 wordmark letter-spacing {ls} is more than 0.05em of {size}px")


def no_wide_image(page):  # AC88: no <img>/<video> or url() background in the first screen wider than 60% of it
    bad = page.evaluate("""() => { const out = [], W = document.documentElement.clientWidth;
      for (const el of [document.documentElement, document.body, ...document.body.querySelectorAll('*')])
        for (const ps of [null, '::before', '::after']) {
        const s = getComputedStyle(el, ps);
        if (ps && (s.content === 'none' || s.content === 'normal')) continue;
        const media = !ps && ['IMG', 'VIDEO', 'PICTURE', 'svg'].includes(el.tagName) || /url\\(/.test(s.backgroundImage);
        if (!media || s.display === 'none' || s.visibility === 'hidden') continue;
        const r = el.getBoundingClientRect();
        const w = ps ? (parseFloat(s.width) || r.width) : r.width;
        if (r.top < innerHeight && r.bottom > 0 && w > 0.6 * W)
          out.push(el.tagName + (el.className ? '.' + el.className : '') + (ps || '') + ' ' + Math.round(w) + 'px'); }
      return out.slice(0, 10); }""")
    for b in bad:
        fail(f"AC88 image in the first screen wider than 60% of the viewport: {b}")


def no_big_number(page):  # AC89: no element whose own text is a number set larger than the h1
    bad = page.evaluate("""() => { const h = document.querySelector('h1'); if (!h) return ['no h1'];
      const own = e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('').trim();
      const size = e => parseFloat(getComputedStyle(e).fontSize);
      const h1 = Math.max(...[h, ...h.querySelectorAll('*')].filter(e => own(e)).map(size));
      const num = /^[\\d.,:+%~–\\-\\s]*\\d[\\d.,:+%~–\\-\\s]*(건|명|년|억|만|%|원|회|개|위|배|\\+)?$/;
      const out = [...document.body.querySelectorAll('*')].filter(e => num.test(own(e)) && size(e) > h1)
        .map(e => own(e) + ' at ' + size(e) + 'px (h1 ' + h1 + 'px)');
      for (const e of document.body.querySelectorAll('*')) for (const ps of ['::before', '::after']) {
        const c = getComputedStyle(e, ps), t = (c.content.match(/^["'](.*)["']$/) || [])[1];
        if (t && num.test(t.trim()) && parseFloat(c.fontSize) > h1) out.push(t + ' (' + ps + ') at ' + c.fontSize); }
      return out.slice(0, 10); }""")
    for b in bad:
        fail(f"AC89 a number set larger than the h1: {b}")


def h1_family(page):  # the first family of the h1's computed font-family (the cascade, unlike check_static.py)
    return page.locator("h1").first.evaluate(
        "e => getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/^['\"]|['\"]$/g, '')")


def h1_a_face(page):  # AC85, computed
    fam = h1_family(page)
    if fam not in A_H1_FACES:
        fail(f"AC85 the h1's computed first font family {fam!r} is not one of {A_H1_FACES}")


def h1_not_serif(page):  # AC97, and AC108 computed and rendered
    h = page.locator("h1").first
    fam = h1_family(page)
    if serif(fam):
        fail(f"AC97 the h1's first font family {fam!r} is a serif face")
    if re.match(r"pretendard", fam, re.I):
        fail(f"AC108 the h1's computed first font family is {fam!r}")
    main = main_font(page, h.element_handle())
    if main and serif(main):
        fail(f"AC97 the h1 renders in {main!r}, a serif face")
    if main and re.match(r"pretendard", main, re.I):
        fail(f"AC108 the h1 renders in {main!r}")


def vertical_text(page):  # AC99
    ok = page.evaluate(f"""() => {{ const inView = {IN_VIEW};
      return [...document.body.querySelectorAll('*')].some(e => getComputedStyle(e).writingMode === 'vertical-rl'
        && [...e.childNodes].some(n => n.nodeType === 3 && /[가-힣]/.test(n.nodeValue)) && inView(e)); }}""")
    if not ok:
        fail("AC99 no visible Korean text with writing-mode: vertical-rl in the first screen at 1440px")


FULL_BLEED = """dir => { const W = document.documentElement.clientWidth, out = [];
  for (const el of document.body.querySelectorAll('*')) { const s = getComputedStyle(el);
    const src = el.tagName === 'IMG' ? (el.currentSrc || el.src) : (s.backgroundImage.match(/url\\(["']?([^"')]+)/) || [])[1];
    if (!src || !src.includes(dir) || s.visibility === 'hidden' || s.display === 'none') continue;
    const r = el.getBoundingClientRect();
    if (r.top < innerHeight && r.bottom > 0 && r.height > 0) {
      out.push([el.tagName, Math.round(r.left), Math.round(r.right), W]);
      if (r.left <= 1 && r.right >= W - 1) return [true, out]; } }
  return [false, out]; }"""


def full_bleed(target, slug, ac, label):  # AC100 AC112
    ok, seen = target.evaluate(FULL_BLEED, f"/profile/{slug}/img/")
    if not ok:
        fail(f"{ac} no photo from img/ spans the full viewport width in the first screen at {label} "
             f"(photos seen: {seen[:4]})")


def thumb_fresh(page, base, slug):  # AC4: thumb.jpg shows the current first screen (profile_thumb.py was re-run)
    if not (ROOT / "profile" / slug / "thumb.jpg").is_file():
        fail("AC4 thumb.jpg missing")
        return
    shot = base64.b64encode(page.screenshot()).decode()
    ctx = page.context.browser.new_context()
    p = ctx.new_page()
    p.goto(f"{base}/profile/")
    diff = p.evaluate("""async ([a, b]) => {
      const load = src => new Promise((ok, no) => { const i = new Image(); i.onload = () => ok(i); i.onerror = no; i.src = src; });
      const px = img => { const c = document.createElement('canvas'); c.width = 160; c.height = 100;
        const g = c.getContext('2d'); g.drawImage(img, 0, 0, 160, 100); return g.getImageData(0, 0, 160, 100).data; };
      const [x, y] = [px(await load(a)), px(await load(b))]; let s = 0, n = 0;
      for (let i = 0; i < x.length; i += 4) { for (let k = 0; k < 3; k++) s += Math.abs(x[i + k] - y[i + k]); n += 3; }
      return s / n; }""", [f"{base}/profile/{slug}/thumb.jpg?{datetime.now().timestamp()}", f"data:image/png;base64,{shot}"])
    ctx.close()
    if diff > THUMB_MAX_DIFF:
        fail(f"AC4 thumb.jpg differs from the current first screen (mean difference {diff:.1f} > {THUMB_MAX_DIFF}); "
             f"re-run python3 scripts/profile_thumb.py {slug}")
    return diff


def bands(page, path, width):
    h = page.evaluate("document.documentElement.scrollHeight")
    page.screenshot(path=str(path), full_page=True)
    for n, y in enumerate(range(0, h, 1200), 1):
        page.screenshot(path=str(path.with_name(f"{path.stem}-{n:02d}.png")), full_page=True,
                        clip={"x": 0, "y": y, "width": width, "height": min(1200, h - y)})
    return h


def git(*args):  # None when git fails, so a failed call never reads as a clean tree
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def check_page(browser, base, slug, shots):
    info, url = SAMPLES[slug], f"{base}/profile/{slug}/"
    out = shots / slug
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    heights, tdiff = {}, None
    for label, vp in (("1440px", DESKTOP), ("390px", MOBILE)):
        ctx, page = new_page(browser, vp)
        bad_fonts = font_responses(page)
        page.goto(url, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1500)  # let entrance effects finish before judging the first screen
        if not any_visible(page.get_by_text(MARK, exact=False)):
            fail(f"AC7 sample notice not visible without scrolling at {label}")
        for word in CONTROLS:
            if not any_visible(control(page, word)):
                fail(f"{'AC42' if vp is DESKTOP else 'AC43'} '{word}' control not visible without scrolling at {label}")
        if vp is DESKTOP:
            tdiff = thumb_fresh(page, base, slug)
            no_overflow(page, "AC64 1440px")
            keep_all(page)
            if slug == "law-ganeum":
                h1_a_face(page)
                wordmark_a(page, info["stem"])
                no_wide_image(page)
                no_big_number(page)
            else:
                h1_not_serif(page)
                vertical_text(page)
                full_bleed(page, slug, "AC100", "1440px")
        else:
            if slug == "law-ganeum" and not any_visible(page.get_by_text("02-000-0000", exact=False)):
                fail("AC93 the phone number 02-000-0000 is not visible without scrolling at 390px")
            positions = page.evaluate(POSITIONS)
            for y in positions:
                page.evaluate(f"scrollTo({{top: {y}, behavior: 'instant'}})")
                for word in CONTROLS:
                    for _ in range(15):  # up to 1.5 s for a sticky bar that slides in
                        if any_visible(control(page, word)):
                            break
                        page.wait_for_timeout(100)
                    else:
                        fail(f"AC44 '{word}' control not reachable at scroll {int(y)}px (390px)")
            page.evaluate("scrollTo(0, 0)")
        notice_everywhere(page, label)
        digit_fonts(page, label)
        settle(page)
        name = "desktop-1440.png" if vp is DESKTOP else "mobile-390.png"
        heights[name] = bands(page, out / name, vp["width"])
        for b in bad_fonts:  # read last, so font files fetched during the scroll-through count too
            fail(f"AC50 web font request did not return 200 at {label}: {b}")
        ctx.close()
    ctx, page = new_page(browser, DESKTOP)  # AC65 AC112: inside a width:390px iframe, as playbook §4 does it
    page.goto(f"{base}/profile/")
    page.set_content(f'<iframe src="{url}" style="width:390px;height:844px;border:0"></iframe>')
    page.frame_locator("iframe").locator("body").wait_for()
    inner = page.frames[1]
    inner.wait_for_load_state("networkidle")
    inner.wait_for_timeout(1500)
    if slug == "law-goim":
        full_bleed(inner, slug, "AC112", "390px (iframe)")
    settle(inner)
    no_overflow(inner, "AC65 390px iframe")
    ctx.close()
    for label, vp in (("1440px", DESKTOP), ("390px", MOBILE)):  # AC63
        ctx, page = new_page(browser, vp, reduced_motion="reduce")
        page.goto(url, wait_until="networkidle")
        settle(page)
        reduced_motion(page, label)
        ctx.close()
    tree, dirty = tree_state(slug)
    lines = [f"slug {slug}", f"head {git('rev-parse', 'HEAD') or 'unknown'}", f"site tree {tree}", f"site working tree {dirty}",
             *(f"height {k} {v}" for k, v in heights.items()),
             f"thumb difference {tdiff:.1f}" if tdiff is not None else "thumb difference n/a",
             *(f"FAIL {f}" for f in fails), f"result {'PASS' if not fails else 'FAIL'}"]
    (out / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"screenshots for AC66/AC67: {out}/desktop-1440*.png {out}/mobile-390*.png, summary {out / 'summary.txt'}")


def check_gallery(browser, base):
    ctx, page = new_page(browser, DESKTOP)
    page.goto(f"{base}/profile/", wait_until="networkidle")
    page.click('.pf-filters button[data-filter="law"]')
    page.wait_for_timeout(300)
    shown = page.locator('a.pf-card[data-industry="law"]:visible')
    slugs = sorted(shown.nth(i).get_attribute("data-slug") for i in range(shown.count()))
    if slugs != sorted(SAMPLES):
        fail(f"AC68 law filter shows cards {slugs}, expected {sorted(SAMPLES)}")
    if page.locator('.pf-empty[data-industry="law"]:visible').count():
        fail("AC78 law filter still shows a 준비 중 tile")
    width = "document.getElementById('pf-v-iframe').getBoundingClientRect().width"
    for slug, info in SAMPLES.items():  # each card from a fresh load of /profile/, as a visitor arrives
        if slug not in slugs:
            continue
        page.goto(f"{base}/profile/", wait_until="networkidle")
        page.click('.pf-filters button[data-filter="law"]')
        page.wait_for_timeout(300)
        viewer, iframe = page.locator("#pf-viewer"), page.locator("#pf-v-iframe")
        page.locator(f'a.pf-card[data-slug="{slug}"]').click()
        page.wait_for_timeout(300)
        if not viewer.is_visible() or not (iframe.get_attribute("src") or "").endswith(f"/profile/{slug}/"):
            fail(f"AC70 clicking the {slug} card does not open the preview with that sample")
            continue
        try:
            page.frame_locator("#pf-v-iframe").get_by_text(info["stem"]).first.wait_for(state="attached", timeout=10000)
        except Exception:
            fail(f"AC70 {slug}: the preview iframe does not show {info['stem']}")
        for device, cond in (("mobile", "<= 400"), ("desktop", "> 600")):  # the width animates; wait for it
            page.click(f'button[data-device="{device}"]')
            try:
                page.wait_for_function(f"{width} {cond}", timeout=3000)
            except Exception:
                fail(f"AC79 {slug}: {device} button does not switch the preview width ({page.evaluate(width)})")
        page.keyboard.press("Escape")
        try:
            page.wait_for_function("document.getElementById('pf-viewer').hidden", timeout=3000)
        except Exception:
            fail(f"AC80 {slug}: Esc does not close the preview")
    ctx.close()


def tree_state(slug):
    tree = git("rev-parse", f"HEAD:profile/{slug}") or "none"
    status = git("status", "--porcelain", "--", f"profile/{slug}")
    return tree, "unknown" if status is None else "dirty" if status else "clean"


def compare(browser, base, shots):
    out = shots / "compare"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.iterdir():  # keep the last good reference files; they are replaced only when a site answers
        if f.is_file() and not f.name.startswith("ref-"):
            f.unlink()
    notes = []
    for slug in [*SAMPLES, *SHIPPED]:
        if not (ROOT / "profile" / slug / "index.html").is_file():
            fail(f"compare: profile/{slug}/index.html does not exist")
            notes.append(f"local {slug} missing")
            continue
        for label, vp in (("1440", DESKTOP), ("390", MOBILE)):
            ctx, page = new_page(browser, vp)
            page.goto(f"{base}/profile/{slug}/", wait_until="networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(out / f"{slug}-{label}.png"))
            if slug not in SAMPLES:  # the law samples' full pages are in <slug>/ from `page`
                settle(page)
                bands(page, out / f"{slug}-{label}-full.png", vp["width"])
            ctx.close()
        tree, state = tree_state(slug)
        notes.append(f"local {slug} tree {tree} {state}")
    for slug, info in SAMPLES.items():
        ctx = browser.new_context(viewport=DESKTOP)
        page = ctx.new_page()
        try:
            resp = page.goto(info["ref"], wait_until="load", timeout=45000)
            if resp is None or resp.status >= 400:  # an error or challenge page is not a good copy
                raise RuntimeError(f"HTTP {resp.status if resp else 'no response'}")
            page.wait_for_timeout(4000)
            page.screenshot(path=str(out / f"tmp-ref-{slug}.png"))  # tmp- files are swapped in only when all succeed
            settle(page)
            bands(page, out / f"tmp-ref-{slug}-full.png", DESKTOP["width"])
            (out / f"tmp-ref-{slug}.txt").write_text(page.evaluate("document.body.innerText"), encoding="utf-8")
            for f in out.glob(f"ref-{slug}-full*.png"):
                f.unlink()
            for f in sorted(out.glob(f"tmp-ref-{slug}*")):
                f.replace(out / f.name.removeprefix("tmp-"))
            notes.append(f"reference {slug} {info['ref']} ok {datetime.now().date()}")
        except Exception as exc:
            have = all((out / f"ref-{slug}{x}").is_file() for x in (".png", ".txt", "-full.png", "-full-01.png"))
            when = datetime.fromtimestamp((out / f"ref-{slug}.png").stat().st_mtime).date() if have else ""
            notes.append(f"reference {slug} {info['ref']} {'cached ' + str(when) if have else 'unreachable'}: "
                         f"{type(exc).__name__}: {(str(exc).splitlines() or [''])[0]}")
        ctx.close()
    (out / "summary.txt").write_text("\n".join([f"head {git('rev-parse', 'HEAD') or 'unknown'}", *notes]) + "\n", encoding="utf-8")
    print("\n".join(notes))
    print(f"compare shots: {out}")


if __name__ == "__main__":
    args = sys.argv[1:]
    shots = Path("/tmp/profile-law-shots")
    if "--shots" in args:
        i = args.index("--shots")
        if i + 1 >= len(args):
            raise SystemExit(__doc__)
        shots = Path(args[i + 1]).resolve()
        if shots == ROOT or ROOT in shots.parents:  # `page` empties DIR/<slug>/; never inside the repository
            raise SystemExit(f"--shots must be outside the repository: {shots}")
        del args[i:i + 2]
    if not args or args[0] not in ("page", "gallery", "compare") or \
            (args[0] == "page" and (len(args) != 2 or args[1] not in SAMPLES)) or (args[0] != "page" and len(args) != 1):
        raise SystemExit(__doc__)
    if args[0] == "page" and not (ROOT / "profile" / args[1] / "index.html").is_file():
        print(f"FAIL profile/{args[1]}/index.html does not exist")
        sys.exit(1)
    httpd, base = serve()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome")
        try:
            if args[0] == "page":
                check_page(browser, base, args[1], shots)
            elif args[0] == "gallery":
                check_gallery(browser, base)
            else:
                compare(browser, base, shots)
        except Exception as exc:  # a missing element or timeout is a failed check, not a crash
            fail(f"{args[0]}: {type(exc).__name__}: {(str(exc).splitlines() or [''])[0]}")
        browser.close()
    httpd.shutdown()
    for f in fails:
        print("FAIL", f)
    print(f"{'PASS' if not fails else 'FAIL'}: {' '.join(args)} ({len(fails)} failures)")
    sys.exit(1 if fails else 0)
