#!/usr/bin/env python3
"""Browser checks for the three clinic profile samples (Playwright + installed Google Chrome). Run from the repo root.

usage: python3 docs/features/2026-11-18-profile-clinic/check_browser.py page <slug> | gallery | compare [--shots DIR]
  page <slug>  AC4 (thumb.jpg is the current first screen) AC7 AC14 AC15 AC16 AC17 AC22 AC39 AC40 AC41, and
               A: AC63-AC66, D: AC77 AC78 AC80. Empties DIR/<slug>/ first, then writes full-page screenshots for
               AC42/AC43 (desktop-1440.png, mobile-390.png, and the same cut into 1200 px bands -NN.png) and
               summary.txt last.
  gallery      AC44 AC45 AC47 AC48 AC49 on /profile/
  compare      evidence for AC50-AC52, not a check: rewrites DIR/compare/ with first screens (1440x900 and 390x844) of
               the three clinic samples, flower-bomgyeol and food-saebyeokmil, full pages (and bands) of the last two,
               and of each reference site its first screen and full page at 1440 and its visible text (ref-<slug>.png,
               ref-<slug>-full.png and its -NN bands, ref-<slug>.txt; an HTTP error counts as no answer;
               the last good copy is kept when a site does not answer). summary.txt lists each local tree hash and each
               reference as ok, cached or unreachable. Exit 0 when every local screenshot was written.
DIR defaults to /tmp/profile-clinic-shots. Serves the repository root on a free local port itself.
The page clock is fixed at Sunday 2026-11-15 11:00 KST, so a "today" line cannot change between runs.
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
    "clinic-neuru": {"name": "느루치과", "stem": "느루", "ref": "https://www.studiodental.com/"},
    "clinic-byeotteul": {"name": "볕뜰가정의학과의원", "stem": "볕뜰", "ref": "https://www.asktia.com/"},
    "clinic-bonui": {"name": "보늬피부과", "stem": "보늬", "ref": "https://www.everbody.com/"},
}
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
CLOCK = datetime(2026, 11, 15, 11, 0, tzinfo=timezone(timedelta(hours=9)))  # a Sunday
KOREAN_FONT = re.compile(r"Pretendard|\bKR\b|Nanum|Gowun|Gothic A1|Hahmlet|Song Myung|Black Han Sans|Do Hyeon|Jua"
                         r"|Orbit|Sunflower|Gaegu|Dongle|Hi Melody|Gamja Flower|Poor Story|Stylish|Yeon Sung"
                         r"|Gugi|Dokdo|Single Day|Cute Font|Kirang Haerang|Bagel Fat One|Diphylleia", re.I)
SANS_FONT = re.compile(r"Pretendard|Sans|Gothic|Dodum|SUIT|Inter\b|Spoqa|NanumSquare|Nanum Square|system-ui"
                       r"|-apple-system|BlinkMacSystemFont|Apple SD Gothic|Malgun", re.I)
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
HOURS = r"\d{1,2}:\d{2}\s*[-–—~～〜]\s*\d{1,2}:\d{2}"
WEEKDAY = r"평일|오늘|요일|[월화수목금토]\s*[-–—~～〜]\s*[월화수목금토일]"  # AC16: the range is the weekday or today's hours
THUMB_MAX_DIFF = 15.0  # mean absolute RGB difference (0-255) at 160x100 between thumb.jpg and a fresh first screen
fails = []


def fail(msg):
    fails.append(msg)


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
      for (let y = 0; y < h(); y += innerHeight / 2) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
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


def hours_visible(page, label):  # AC16: the smallest element whose text holds a time range, beside a weekday word, in view
    ok = page.evaluate(f"""() => {{ const re = /{HOURS}/, day = /{WEEKDAY}/, inView = {IN_VIEW};
      const t = e => e.textContent.replace(/\\s+/g, ' ');
      const els = [...document.body.querySelectorAll('*')].filter(e => re.test(t(e))
        && ![...e.children].some(c => re.test(t(c))) && (day.test(t(e)) || day.test(t(e.parentElement))));
      return els.some(inView); }}""")
    if not ok:
        fail(f"AC16 no 진료시간 time range (HH:MM–HH:MM beside 평일, 오늘, 요일 or a weekday range) visible without scrolling at {label}")


def no_overflow(target, label):  # AC40 AC41
    w = target.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    if w[0] > w[1]:
        fail(f"{label} horizontal overflow: scrollWidth {w[0]} > clientWidth {w[1]}")


def keep_all(page):  # AC17
    bad = page.evaluate("""() => [...document.querySelectorAll('p, li, dd, dt, td, th')]
      .filter(e => /[가-힣]/.test(e.textContent) && getComputedStyle(e).wordBreak !== 'keep-all')
      .map(e => e.textContent.trim().slice(0, 40))""")
    for t in bad:
        fail(f"AC17 Korean text without word-break: keep-all: {t}")


def digit_fonts(page, label):  # AC22: digits of hours, phone numbers and prices in a Korean or monospaced face
    texts = page.evaluate("""() => { let n = 0; const texts = [], re = /\\d{1,2}:\\d{2}|0\\d{1,2}-\\d{3,4}-\\d{4}|\\d[\\d,]*\\s?원/;
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
        fail(f"AC22 no visible hours, phone number or price found at {label}")
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
            fail(f"AC22 digits rendered in {main!r}, neither Korean nor monospaced, at {label}: {texts[i]}")
    page.evaluate("document.querySelectorAll('[data-digit-probe]').forEach(p => p.remove())")
    cdp.detach()


def font_responses(page):  # AC22: every web font request returns 200
    bad = []
    page.on("response", lambda r: any(h in r.url for h in FONT_HOSTS) and r.status != 200
            and bad.append(f"{r.status} {r.url}"))
    page.on("requestfailed", lambda r: any(h in r.url for h in FONT_HOSTS) and bad.append(f"failed {r.url}"))
    return bad


def reduced_motion(page, label):  # AC39
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
        fail(f"AC39 under prefers-reduced-motion at {label}: {b}")


HERO = """() => { const vis = [...document.images].map(i => [i, i.getBoundingClientRect()])
    .filter(([i, r]) => r.width > 0 && r.height > 0 && r.top < innerHeight && r.bottom > 0
      && getComputedStyle(i).visibility !== 'hidden')
    .map(([i, r]) => [i, Math.max(0, Math.min(r.bottom, innerHeight) - Math.max(r.top, 0)) * r.width]);
  vis.sort((a, b) => b[1] - a[1]); return vis.length ? vis[0][0] : null; }"""


def hero_photo(page):
    h = page.evaluate_handle(HERO)
    return h.as_element()


def full_width(page, hero, ac):  # AC63
    r = hero.evaluate("i => { const r = i.getBoundingClientRect(); return [r.left, r.right, document.documentElement.clientWidth]; }")
    if r[0] > 1 or r[1] < r[2] - 1:
        fail(f"{ac} hero photo does not span the viewport width at 1440px (left {r[0]:.0f}, right {r[1]:.0f}, width {r[2]})")


OVERLAY = """img => {
  const out = [], r = img.getBoundingClientRect(), area = r.width * r.height;
  const anc = new Set(); for (let e = img; e; e = e.parentElement) anc.add(e);
  const rgba = s => [...s.matchAll(/rgba?\\(([^)]*)\\)/g)].map(m => m[1].split(/[\\s,\\/]+/).filter(Boolean).map(Number))
    .map(v => [v[0], v[1], v[2], v.length > 3 ? v[3] : 1]);
  const opacity = el => { let o = 1; for (let e = el; e; e = e.parentElement) o *= +getComputedStyle(e).opacity; return o; };
  const fx = s => (s.match(/brightness\\(([\\d.]+)(%?)\\)/) || []);
  for (const e of anc) { const f = fx(getComputedStyle(e).filter); if (f.length && +f[1] / (f[2] ? 100 : 1) < 0.8)
    out.push('filter ' + getComputedStyle(e).filter + ' on ' + e.tagName); }
  if (opacity(img) < 0.7) out.push('photo opacity ' + opacity(img).toFixed(2));
  const style = document.createElement('style');
  style.textContent = '*, *::before, *::after { pointer-events: auto !important; }';
  document.head.append(style);
  const stack = (x, y) => document.elementsFromPoint(x, y);
  for (const el of document.body.querySelectorAll('*')) {
    if (el === img) continue;
    for (const pseudo of [null, '::before', '::after']) {
      if (pseudo === null && anc.has(el)) continue;
      const s = getComputedStyle(el, pseudo);
      if (pseudo && (s.content === 'none' || s.content === 'normal')) continue;
      if (s.display === 'none' || s.visibility === 'hidden') continue;
      const b = el.getBoundingClientRect();
      const ix = Math.max(0, Math.min(b.right, r.right) - Math.max(b.left, r.left));
      const iy = Math.max(0, Math.min(b.bottom, r.bottom) - Math.max(b.top, r.top));
      if (ix * iy < 0.1 * area) continue;
      if (pseudo) {  // a pseudo-element is measured by its own box, not its parent's
        const px = k => parseFloat(s[k]) || 0;
        const pw = px('width') + px('paddingLeft') + px('paddingRight');
        const ph = px('height') + px('paddingTop') + px('paddingBottom');
        if (pw * ph < 0.1 * area) continue;
      } else {  // painted above the photo at the centre of the overlap?
        const cx = Math.max(b.left, r.left) + ix / 2, cy = Math.max(b.top, r.top) + iy / 2, st = stack(cx, cy);
        if (st.indexOf(el) < 0 || st.indexOf(img) >= 0 && st.indexOf(el) > st.indexOf(img)) continue;
      }
      const o = opacity(el);
      const paint = s.backgroundColor + ' ' + s.backgroundImage + ' ' + (/inset/.test(s.boxShadow) ? s.boxShadow : '');
      const unparsed = /(oklab|oklch|lab|lch|hsl|hwb|color)\\(/.test(paint);
      if (unparsed) out.push('colour not in rgb()/rgba() on ' + el.tagName + (pseudo || ''));
      for (const [R, G, B, A] of rgba(paint))
        if (A * o > 0.3 && Math.max(R, G, B) <= 0x80) out.push('dark ' + [R, G, B, A].join(',') + ' over the photo on ' + el.tagName + (el.className ? '.' + el.className : '') + (pseudo || ''));
    }
  }
  style.remove();
  return [...new Set(out)].slice(0, 10); }"""


def no_dark_overlay(hero, ac):  # AC64 AC80
    for b in hero.evaluate(OVERLAY):
        fail(f"{ac} hero overlay: {b}")


def dark_headline(page):  # AC65
    bad = page.evaluate("""() => { const h = document.querySelector('h1'); if (!h) return ['no h1'];
      return [h, ...h.querySelectorAll('*')].filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim()))
        .map(e => getComputedStyle(e).color).filter(c => { const v = c.match(/[\\d.]+/g).map(Number);
          return Math.max(v[0], v[1], v[2]) > 0x40; }); }""")
    for c in bad:
        fail(f"AC65 hero headline (h1) colour is not dark: {c}")


WORDMARK = """stem => { const header = document.querySelector('header'); if (!header) return null;
  const w = document.createTreeWalker(header, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) if (w.currentNode.nodeValue.includes(stem)) { const el = w.currentNode.parentElement;
    return el.closest('a') && header.contains(el.closest('a')) ? el.closest('a') : el; }
  return null; }"""


def wordmark(page, stem, ac):
    h = page.evaluate_handle(WORDMARK, stem).as_element()
    if not h:
        fail(f"{ac} no wordmark: no text containing '{stem}' inside the first <header>")
    return h


def wordmark_left(wm):  # AC66
    left = wm.evaluate("e => e.getBoundingClientRect().left")
    if left > 1440 / 4:
        fail(f"AC66 wordmark left edge at {left:.0f}px, not within the left quarter (360px) at 1440px")


def wordmark_type(page, wm):  # AC77 AC78
    info = wm.evaluate("""e => [e, ...e.querySelectorAll('*')]
      .filter(x => [...x.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim()))
      .map(x => { const s = getComputedStyle(x); return [s.letterSpacing, parseFloat(s.fontSize), s.fontFamily]; })""")
    for ls, size, family in info:
        px = 0.0 if ls == "normal" else float(re.sub(r"px$", "", ls))
        if px > 0.05 * size + 1e-6:
            fail(f"AC77 wordmark letter-spacing {ls} is more than 0.05em of {size}px")
        first = family.split(",")[0].strip().strip("'\"")
        if not SANS_FONT.search(first) or first.lower() == "serif":
            fail(f"AC78 wordmark's first font family {first!r} is not on the sans list")
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    wm.evaluate("e => e.setAttribute('data-wordmark-probe', '')")
    root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
    node = cdp.send("DOM.querySelector", {"nodeId": root, "selector": "[data-wordmark-probe]"})["nodeId"]
    fonts = cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]
    wm.evaluate("e => e.removeAttribute('data-wordmark-probe')")
    cdp.detach()
    main = max(fonts, key=lambda f: f["glyphCount"])["familyName"] if fonts else ""
    if fonts and not SANS_FONT.search(main):
        fail(f"AC78 wordmark renders in {main!r}, not a face on the sans list")


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


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


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
        hours_visible(page, label)
        if vp is DESKTOP:
            tdiff = thumb_fresh(page, base, slug)
            no_overflow(page, "AC40 1440px")
            keep_all(page)
            if slug in ("clinic-neuru", "clinic-bonui"):
                hero = hero_photo(page)
                if not hero:
                    fail(f"{'AC63' if slug == 'clinic-neuru' else 'AC80'} no hero photo (<img>) on the first screen")
                elif slug == "clinic-neuru":
                    full_width(page, hero, "AC63")
                    no_dark_overlay(hero, "AC64")
                else:
                    no_dark_overlay(hero, "AC80")
                wm = wordmark(page, info["stem"], "AC66" if slug == "clinic-neuru" else "AC77 AC78")
                if wm and slug == "clinic-neuru":
                    wordmark_left(wm)
                elif wm:
                    wordmark_type(page, wm)
            if slug == "clinic-neuru":
                dark_headline(page)
        else:
            for word, ac in (("네이버 예약", "AC14"), ("전화", "AC14")):
                if not any_visible(control(page, word)):
                    fail(f"{ac} '{word}' button not visible without scrolling at 390px")
            positions = page.evaluate("""() => { const out = [], H = document.documentElement.scrollHeight;
              for (let y = 0; ; y += innerHeight / 2) { const t = Math.min(y, H - innerHeight); out.push(t);
                if (t >= H - innerHeight) break; } return out; }""")
            for y in positions:
                page.evaluate(f"scrollTo({{top: {y}, behavior: 'instant'}})")
                for word in ("네이버 예약", "전화"):
                    for _ in range(15):  # up to 1.5 s for a sticky bar that slides in
                        if any_visible(control(page, word)):
                            break
                        page.wait_for_timeout(100)
                    else:
                        fail(f"AC15 '{word}' button not reachable at scroll {int(y)}px (390px)")
            page.evaluate("scrollTo(0, 0)")
        digit_fonts(page, label)
        for b in bad_fonts:
            fail(f"AC22 web font request did not return 200 at {label}: {b}")
        settle(page)
        name = "desktop-1440.png" if vp is DESKTOP else "mobile-390.png"
        heights[name] = bands(page, out / name, vp["width"])
        ctx.close()
    ctx, page = new_page(browser, DESKTOP)  # AC41: inside a width:390px iframe, as playbook §4 does it
    page.goto(f"{base}/profile/")
    page.set_content(f'<iframe src="{url}" style="width:390px;height:844px;border:0"></iframe>')
    page.frame_locator("iframe").locator("body").wait_for()
    inner = page.frames[1]
    inner.wait_for_load_state("networkidle")
    settle(inner)
    no_overflow(inner, "AC41 390px iframe")
    ctx.close()
    for label, vp in (("1440px", DESKTOP), ("390px", MOBILE)):  # AC39
        ctx, page = new_page(browser, vp, reduced_motion="reduce")
        page.goto(url, wait_until="networkidle")
        settle(page)
        reduced_motion(page, label)
        ctx.close()
    tree, dirty = tree_state(slug)
    lines = [f"slug {slug}", f"head {git('rev-parse', 'HEAD')}", f"site tree {tree}", f"site working tree {dirty}",
             *(f"height {k} {v}" for k, v in heights.items()),
             f"thumb difference {tdiff:.1f}" if tdiff is not None else "thumb difference n/a",
             *(f"FAIL {f}" for f in fails), f"result {'PASS' if not fails else 'FAIL'}"]
    (out / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"screenshots for AC42/AC43: {out}/desktop-1440*.png {out}/mobile-390*.png, summary {out / 'summary.txt'}")


def check_gallery(browser, base):
    ctx, page = new_page(browser, DESKTOP)
    page.goto(f"{base}/profile/", wait_until="networkidle")
    page.click('.pf-filters button[data-filter="clinic"]')
    page.wait_for_timeout(300)
    shown = page.locator('a.pf-card[data-industry="clinic"]:visible')
    slugs = sorted(shown.nth(i).get_attribute("data-slug") for i in range(shown.count()))
    if slugs != sorted(SAMPLES):
        fail(f"AC44 clinic filter shows cards {slugs}, expected {sorted(SAMPLES)}")
    if page.locator('.pf-empty[data-industry="clinic"]:visible').count():
        fail("AC45 clinic filter still shows a 준비 중 tile")
    width = "document.getElementById('pf-v-iframe').getBoundingClientRect().width"
    for slug, info in SAMPLES.items():  # each card from a fresh load of /profile/, as a visitor arrives
        if slug not in slugs:
            continue
        page.goto(f"{base}/profile/", wait_until="networkidle")
        page.click('.pf-filters button[data-filter="clinic"]')
        page.wait_for_timeout(300)
        viewer, iframe = page.locator("#pf-viewer"), page.locator("#pf-v-iframe")
        page.locator(f'a.pf-card[data-slug="{slug}"]').click()
        page.wait_for_timeout(300)
        if not viewer.is_visible() or not (iframe.get_attribute("src") or "").endswith(f"/profile/{slug}/"):
            fail(f"AC47 clicking the {slug} card does not open the preview with that sample")
            continue
        try:
            page.frame_locator("#pf-v-iframe").get_by_text(info["stem"]).first.wait_for(state="attached", timeout=10000)
        except Exception:
            fail(f"AC47 {slug}: the preview iframe does not show {info['stem']}")
        for device, cond in (("mobile", "<= 400"), ("desktop", "> 600")):  # the width animates; wait for it
            page.click(f'button[data-device="{device}"]')
            try:
                page.wait_for_function(f"{width} {cond}", timeout=3000)
            except Exception:
                fail(f"AC48 {slug}: {device} button does not switch the preview width ({page.evaluate(width)})")
        page.keyboard.press("Escape")
        try:
            page.wait_for_function("document.getElementById('pf-viewer').hidden", timeout=3000)
        except Exception:
            fail(f"AC49 {slug}: Esc does not close the preview")
    ctx.close()


def tree_state(slug):
    tree = git("rev-parse", f"HEAD:profile/{slug}") or "none"
    return tree, "dirty" if git("status", "--porcelain", "--", f"profile/{slug}") else "clean"


def compare(browser, base, shots):
    out = shots / "compare"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.iterdir():  # keep the last good reference files; they are replaced only when a site answers
        if f.is_file() and not f.name.startswith("ref-"):
            f.unlink()
    notes = []
    for slug in [*SAMPLES, "flower-bomgyeol", "food-saebyeokmil"]:
        if not (ROOT / "profile" / slug / "index.html").is_file():
            fail(f"compare: profile/{slug}/index.html does not exist")
            notes.append(f"local {slug} missing")
            continue
        for label, vp in (("1440", DESKTOP), ("390", MOBILE)):
            ctx, page = new_page(browser, vp)
            page.goto(f"{base}/profile/{slug}/", wait_until="networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(out / f"{slug}-{label}.png"))
            if slug not in SAMPLES:  # the clinic samples' full pages are in <slug>/ from `page`
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
            page.screenshot(path=str(out / f"ref-{slug}.png"))
            for f in out.glob(f"ref-{slug}-full*.png"):
                f.unlink()
            settle(page)
            bands(page, out / f"ref-{slug}-full.png", DESKTOP["width"])
            (out / f"ref-{slug}.txt").write_text(page.evaluate("document.body.innerText"), encoding="utf-8")
            notes.append(f"reference {slug} {info['ref']} ok {datetime.now().date()}")
        except Exception as exc:
            have = (out / f"ref-{slug}.png").is_file() and (out / f"ref-{slug}.txt").is_file()
            when = datetime.fromtimestamp((out / f"ref-{slug}.png").stat().st_mtime).date() if have else ""
            notes.append(f"reference {slug} {info['ref']} {'cached ' + str(when) if have else 'unreachable'}: "
                         f"{type(exc).__name__}: {str(exc).splitlines()[0]}")
        ctx.close()
    (out / "summary.txt").write_text("\n".join([f"head {git('rev-parse', 'HEAD')}", *notes]) + "\n", encoding="utf-8")
    print("\n".join(notes))
    print(f"compare shots: {out}")


if __name__ == "__main__":
    args = sys.argv[1:]
    shots = Path(args[args.index("--shots") + 1]) if "--shots" in args else Path("/tmp/profile-clinic-shots")
    if "--shots" in args:
        del args[args.index("--shots"):args.index("--shots") + 2]
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
            fail(f"{args[0]}: {type(exc).__name__}: {str(exc).splitlines()[0]}")
        browser.close()
    httpd.shutdown()
    for f in fails:
        print("FAIL", f)
    print(f"{'PASS' if not fails else 'FAIL'}: {' '.join(args)} ({len(fails)} failures)")
    sys.exit(1 if fails else 0)
