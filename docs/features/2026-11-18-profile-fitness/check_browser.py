#!/usr/bin/env python3
"""Browser checks for the two Pilates franchise profile samples (Playwright + installed Google Chrome). Run from the
repository root.

usage: python3 docs/features/2026-11-18-profile-fitness/check_browser.py page <slug> | gallery | compare [--shots DIR]
  page <slug>  AC5 (thumb.jpg is the current first screen) AC8 AC9 AC33-AC36 AC39 AC55 AC56 AC67 AC76 AC77, and
               D (fitness-mideoum): AC90 AC91 AC94 AC95 AC96 AC99 AC105, B (fitness-jjuuk): AC109 AC113 AC116-AC120.
               Empties DIR/<slug>/ first, then writes full-page screenshots for the reviews (desktop-1440.png,
               mobile-390.png, and the same cut into 1200 px bands -NN.png) and summary.txt last.
  gallery      AC80 AC81 AC83 AC84 AC85 on /profile/
  compare      evidence for the reviews, not a check: rewrites DIR/compare/ with first screens (1440x900 and 390x844)
               of the two fitness samples and the seven shipped samples, full pages (and bands) of the seven shipped
               samples, and of each reference site its first screen and full page at 1440 and its visible text
               (ref-<slug>.png, ref-<slug>-full.png and its -NN bands, ref-<slug>.txt; an HTTP error counts as no
               answer; the last good copy is kept when a site does not answer). summary.txt lists each local tree
               hash and each reference as ok, cached or unreachable. Exit 0 when every local screenshot was written.
DIR defaults to /tmp/profile-fitness-shots. Serves the repository root on a free local port itself.
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
    "fitness-mideoum": {"stem": "미더움", "ref": "https://rebornpilates.com/"},
    "fitness-jjuuk": {"stem": "쭈욱", "ref": "https://scoutstudios.com.au/"},
}
SHIPPED = ("flower-bomgyeol", "food-saebyeokmil", "clinic-neuru", "clinic-byeotteul", "clinic-bonui", "law-ganeum",
           "law-goim")
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
CLOCK = datetime(2026, 11, 15, 11, 0, tzinfo=timezone(timedelta(hours=9)))  # a Sunday
KOREAN_FONT = re.compile(r"Pretendard|\bKR\b|Nanum|Gowun|Gothic A1|Hahmlet|Song Myung|Black Han Sans|Do Hyeon|Jua"
                         r"|Orbit|Sunflower|Gaegu|Dongle|Hi Melody|Gamja Flower|Poor Story|Stylish|Yeon Sung"
                         r"|Gugi|Dokdo|Single Day|Cute Font|Kirang Haerang|Bagel Fat One|Diphylleia", re.I)
D_H2_FACES = ("Gowun Batang", "Song Myung")  # AC99
SERIF_FONT = re.compile(r"serif|Myeongjo|Myungjo|Batang|Hahmlet|Song Myung|Garamond|Cormorant|Times|Georgia|Mincho"
                        r"|Diphylleia|Baskerville|Playfair|Lora|Merriweather|Libre Caslon|Spectral", re.I)
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
THUMB_MAX_DIFF = 15.0  # mean absolute RGB difference (0-255) at 160x100 between thumb.jpg and a fresh first screen
fails = []


def fail(msg):
    fails.append(msg)


def guard(label, fn, *args):  # a check that throws is one failure; the remaining checks and summary.txt still run
    try:
        return fn(*args)
    except Exception as exc:
        fail(f"{label}: {type(exc).__name__}: {(str(exc).splitlines() or [''])[0]}")
        return None


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
      for (let y = 0; y < Math.min(h(), 30000); y += innerHeight / 2) {
        scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 120)); }
      scrollTo({top: 0, behavior: 'instant'});
      for (let i = 0; i < 20 && scrollY !== 0; i++) await new Promise(r => setTimeout(r, 50));
      await new Promise(r => setTimeout(r, 300));
    }""")


IN_VIEW = """el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
  let o = 1; for (let e = el; e; e = e.parentElement) o *= +getComputedStyle(e).opacity;
  if (!r.width || !r.height || s.visibility === 'hidden' || o <= 0.5) return false;
  if (r.top < 0 || r.left < 0 || r.bottom > innerHeight || r.right > innerWidth) return false;
  const style = document.createElement('style');  // a pointer-events:none layer still covers what is under it
  style.textContent = '*, *::before, *::after { pointer-events: auto !important; }';
  document.head.append(style);
  const rects = [...el.getClientRects()].filter(q => q.width && q.height);  // each line box of a wrapped inline
  const stacks = (rects.length ? rects : [r]).map(q => document.elementsFromPoint(q.left + q.width / 2, q.top + q.height / 2));
  style.remove();
  const fill = c => { if (c.backgroundImage !== 'none') return 1; const v = c.backgroundColor;  // alpha of any colour syntax
    if (v === 'transparent') return 0; const m = v.match(/\\(([^)]*)\\)/); if (!m) return 1;
    const parts = m[1].split(/[\\s,\\/]+/).filter(Boolean);
    const a = /^rgba?\\(/.test(v) ? parts[3] : m[1].includes('/') ? parts[parts.length - 1] : undefined;
    return a === undefined ? 1 : a.endsWith('%') ? parseFloat(a) / 100 : +a; };
  const paints = e => {  // the paint that was hit: an ancestor of el only through its ::before/::after
    let o = 1; for (let x = e; x; x = x.parentElement) o *= +getComputedStyle(x).opacity;
    const own = getComputedStyle(e), parts = e.contains(el) ? [] : [[own, 1]];
    for (const ps of ['::before', '::after']) { const c = getComputedStyle(e, ps);
      if (c.content !== 'none' && c.content !== 'normal' && c.display !== 'none') parts.push([c, +c.opacity]); }
    return own.visibility !== 'hidden' && parts.some(([c, po]) => fill(c) * po * o > 0.5); };
  const shows = stack => { for (const t of stack) { if (el === t || el.contains(t)) return true; if (paints(t)) return false; }
    return false; };
  return stacks.some(shows); }"""


def any_visible(loc):
    return any(loc.nth(i).evaluate(IN_VIEW) for i in range(loc.count()))


BRANCH_ID = """() => { const h = [...document.querySelectorAll('h2, h3, h4, h5, h6')]
    .find(e => /지점\\s?찾기/.test(e.textContent) && !e.closest('header')); const s = h && h.closest('section'); return s ? s.id : null; }"""

BRANCH_ENTRIES = """sid => { const s = document.getElementById(sid); if (!s) return [];
  return [...s.querySelectorAll('article[id]')].filter(a => { const h = a.querySelector('h3, h4, h5, h6');
    return h && /(^|\\s)([가-힣]{1,8})점$/.test(h.textContent.trim()) && !/(^|\\s)지점$/.test(h.textContent.trim()); })
    .map(a => a.id); }"""


def branch_links(page):  # links to the 지점 찾기 section (AC33-AC35 AC94)
    sid = page.evaluate(BRANCH_ID)
    if not sid:
        fail("AC20 no <section id> holding a '지점 찾기' heading; the 지점 link checks cannot run")
        return None, None
    return sid, page.locator(f'a[href="#{sid}"]')


POSITIONS = """() => { const out = [], H = document.documentElement.scrollHeight;
  for (let y = 0; ; y += innerHeight / 2) { const t = Math.min(y, H - innerHeight); out.push(t);
    if (t >= H - innerHeight) break; } return out; }"""  # every half screen down to the end (AC35)

LAST_FOOTER_TEXT = """() => { const f = [...document.querySelectorAll('footer')].pop(); if (!f) return null;
  const pinned = e => { for (; e; e = e.parentElement) if (/fixed|sticky/.test(getComputedStyle(e).position)) return true;
    return false; };  // a bar inside <footer> is not the footer's last line
  return [f, ...f.querySelectorAll('*')].filter(e => e.getClientRects().length && !pinned(e)
    && [...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim())).pop() || null; }"""


def branch_link_everywhere(page, links):  # AC35, then AC36
    positions = page.evaluate(POSITIONS)
    for y in positions:
        page.evaluate(f"scrollTo({{top: {y}, behavior: 'instant'}})")
        for _ in range(15):  # up to 1.5 s for a bar that slides in
            if any_visible(links):
                break
            page.wait_for_timeout(100)
        else:
            fail(f"AC35 no link to the 지점 찾기 section on screen at scroll {int(y)}px of {int(positions[-1])}px (390px)")
    page.evaluate("scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")  # the page may have grown
    page.wait_for_timeout(200)
    last = page.evaluate_handle(LAST_FOOTER_TEXT).as_element()
    if not last:
        fail("AC36 no <footer> text to read at the end of the page (390px)")
    elif not last.evaluate(IN_VIEW):
        fail(f"AC36 the footer's last text line is covered or off screen at the end of the page (390px): "
             f"{last.evaluate('e => e.textContent.trim().slice(0, 40)')}")
    page.evaluate("scrollTo(0, 0)")


def no_overflow(target, label):  # AC76 AC77
    w = target.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    if w[0] > w[1]:
        fail(f"{label} horizontal overflow: scrollWidth {w[0]} > clientWidth {w[1]}")


def keep_all(page):  # AC39
    bad = page.evaluate("""() => [...document.querySelectorAll('p, li, dd, dt, td, th')]
      .filter(e => /[가-힣]/.test(e.textContent) && getComputedStyle(e).wordBreak !== 'keep-all')
      .map(e => e.textContent.trim().slice(0, 40))""")
    for t in bad:
        fail(f"AC39 Korean text without word-break: keep-all: {t}")


def main_font(page, handle):
    """The platform font that renders most glyphs of the element and its descendants (CDP), None when none."""
    cdp = page.context.new_cdp_session(page)
    cdp.send("DOM.enable")
    cdp.send("CSS.enable")
    handle.evaluate("e => [e, ...e.querySelectorAll('*')].forEach(x => x.setAttribute('data-font-probe', ''))")
    root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
    nodes = cdp.send("DOM.querySelectorAll", {"nodeId": root, "selector": "[data-font-probe]"})["nodeIds"]
    count = {}
    for node in nodes:
        for f in cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]:
            count[f["familyName"]] = count.get(f["familyName"], 0) + f["glyphCount"]
    handle.evaluate("e => [e, ...e.querySelectorAll('*')].forEach(x => x.removeAttribute('data-font-probe'))")
    cdp.detach()
    return max(count, key=count.get) if count else None


def digit_fonts(page, label):  # AC55: digits of hours and phone numbers in a Korean or monospaced face
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
        fail(f"AC55 no visible opening hours or phone number found at {label}")
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
            fail(f"AC55 digits rendered in {main!r}, neither Korean nor monospaced, at {label}: {texts[i]}")
    page.evaluate("document.querySelectorAll('[data-digit-probe]').forEach(p => p.remove())")
    cdp.detach()


def font_responses(page):  # AC56: every web font request returns 200
    bad = []
    page.on("response", lambda r: any(h in r.url for h in FONT_HOSTS) and r.status != 200
            and bad.append(f"{r.status} {r.url}"))
    page.on("requestfailed", lambda r: any(h in r.url for h in FONT_HOSTS) and bad.append(f"failed {r.url}"))
    return bad


def reduced_motion(page, label):  # AC67
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
        fail(f"AC67 under prefers-reduced-motion at {label}: {b}")


def first_family(target, selector_js):
    return target.evaluate(f"""() => [...document.querySelectorAll({selector_js!r})].map(e =>
      [e.textContent.trim().slice(0, 30), getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/^['"]|['"]$/g, '')])""")


# --- sample D ----------------------------------------------------------------------------------------------

FULL_BLEED = """dir => { const W = document.documentElement.clientWidth, out = [];
  for (const el of document.body.querySelectorAll('*')) { const s = getComputedStyle(el);
    const src = el.tagName === 'IMG' ? (el.currentSrc || el.src) : (s.backgroundImage.match(/url\\(["']?([^"')]+)/) || [])[1];
    if (!src || !src.includes(dir) || s.visibility === 'hidden' || s.display === 'none') continue;
    const r = el.getBoundingClientRect();
    if (r.top < innerHeight && r.bottom > 0 && r.height > 0) {
      out.push([el.tagName, Math.round(r.left), Math.round(r.right), W]);
      if (r.left <= 1 && r.right >= W - 1) return [true, out, [r.left, r.top, r.right, r.bottom]]; } }
  return [false, out, null]; }"""


def d_first_screen(page, slug, sid):  # AC90 AC91 AC94 AC95 AC96
    header_links = page.locator("header a")
    for ac, word in (("AC90", "지점"), ("AC91", "가맹")):
        if not any(header_links.nth(i).evaluate(IN_VIEW) and word in header_links.nth(i).inner_text()
                   for i in range(header_links.count())):
            fail(f"{ac} no visible link in the <header> whose text contains '{word}' at 1440px")
    if sid:
        cta = page.locator(f'a[href="#{sid}"]')
        ok = False
        for i in range(cta.count()):
            el = cta.nth(i)
            txt = el.inner_text()
            inside = el.evaluate("e => !!e.closest('header')")
            if not inside and "지점" in txt and re.search(r"상담|예약", txt) and el.evaluate(IN_VIEW):
                ok = True
        if not ok:
            fail("AC94 no visible link outside the <header> on the first screen to the 지점 찾기 section whose text "
                 "contains 지점 and 상담 or 예약 (1440px)")
    ok, seen, box = page.evaluate(FULL_BLEED, f"/profile/{slug}/img/")
    if not ok:
        fail(f"AC95 no photo from img/ spans the full viewport width in the first screen at 1440px (photos seen: {seen[:4]})")
        return
    h = page.evaluate("() => { const r = document.querySelector('h1').getBoundingClientRect(); "
                      "return [r.left, r.top, r.right, r.bottom]; }")
    if not (h[0] < box[2] and h[2] > box[0] and h[1] < box[3] and h[3] > box[1]):
        fail(f"AC96 the h1 box {[round(x) for x in h]} does not overlap the hero photo box {[round(x) for x in box]}")


def d_h2_faces(page):  # AC99
    rows = first_family(page, "h2")
    if not rows:
        fail("AC99 no <h2> on the page")
    for txt, fam in rows:
        if fam not in D_H2_FACES:
            fail(f"AC99 h2 {txt!r}: computed first font family {fam!r} is not one of {D_H2_FACES}")


def no_big_digits(page):  # AC105: no element whose own text has a digit above 24px, pseudo-elements included
    bad = page.evaluate("""() => { const out = [];
      const own = e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('');
      for (const e of document.body.querySelectorAll('*')) {
        const t = own(e), sz = parseFloat(getComputedStyle(e).fontSize);
        if (/\\d/.test(t) && sz > 24 && e.getClientRects().length) out.push(t.trim().slice(0, 20) + ' at ' + sz + 'px');
        for (const ps of ['::before', '::after']) { const c = getComputedStyle(e, ps);
          if (c.content === 'none' || c.content === 'normal' || c.display === 'none') continue;
          if ((/\\d/.test(c.content) || /counter/.test(c.content)) && parseFloat(c.fontSize) > 24)
            out.push(ps + ' ' + c.content.slice(0, 20) + ' at ' + c.fontSize); } }
      return out.slice(0, 10); }""")
    for b in bad:
        fail(f"AC105 a digit set above 24px: {b}")


# --- sample B ----------------------------------------------------------------------------------------------

GREEN_BAND = """() => { const W = document.documentElement.clientWidth;
  const g2 = document.createElement('canvas').getContext('2d', {willReadFrequently: true});
  const hsl = c => { g2.clearRect(0, 0, 1, 1); g2.fillStyle = '#000'; g2.fillStyle = c; g2.fillRect(0, 0, 1, 1);
    const v = g2.getImageData(0, 0, 1, 1).data; if (v[3] < 253) return null;  // any colour syntax, as painted
    const [r, g, b] = [v[0], v[1], v[2]].map(x => x / 255), mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2;
    let h = 0; const d = mx - mn;
    if (d) h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
    return [(h * 60 + 360) % 360, l]; };
  for (const el of [document.body, ...document.body.querySelectorAll('*')]) { const r = el.getBoundingClientRect();
    if (r.width < W - 1 || r.height <= 0 || r.top >= innerHeight || r.bottom <= 0) continue;
    const c = hsl(getComputedStyle(el).backgroundColor);
    if (c && c[0] >= 100 && c[0] <= 160 && c[1] <= 0.30) return null; }
  return 'none'; }"""


def b_first_screen(page, slug):  # AC109 AC113 AC116 AC117 AC118 AC119 AC120
    if page.evaluate(GREEN_BAND):
        fail("AC109 no element as wide as the viewport with a deep-green background (hue 100-160, lightness <= 0.30) "
             "in the first screen at 1440px")
    wm = page.locator("header a.wordmark").first
    if not page.locator("header a.wordmark").count():
        fail('AC113 no <a class="wordmark"> in the <header>')
    else:
        fam = wm.evaluate("e => getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/^['\"]|['\"]$/g, '')")
        rendered = main_font(page, wm.element_handle())
        for what, name in (("computed first font family", fam), ("rendered font", rendered)):
            if not name or re.match(r"pretendard", name, re.I):
                fail(f"AC113 the wordmark's {what} is {name!r}")
        pat = re.compile(re.escape(fam).replace(r"\ ", r"[ +]"), re.I)
        for other in sorted((ROOT / "profile").glob("*/")):
            if other.name == slug:
                continue
            for f in ("index.html", "style.css"):
                p = other / f
                if p.is_file() and pat.search(p.read_text(encoding="utf-8", errors="replace")):
                    fail(f"AC113 the wordmark face {fam!r} is also named in profile/{other.name}/{f}")
    for txt, fam in first_family(page, "h1, h2"):
        if serif(fam):
            fail(f"AC116 heading {txt!r}: computed first font family {fam!r} is a serif face")
    if page.locator("h1").count():
        main = main_font(page, page.locator("h1").first.element_handle())
        if not main or serif(main):
            fail(f"AC116 the h1 renders in {main!r}, a serif face or no font could be read")


def b_branches(page, slug, sid):  # AC117 AC118 AC119 AC120
    ids = page.evaluate(BRANCH_ENTRIES, sid) if sid else []
    if len(ids) < 3:
        fail(f"AC117 AC119 found {len(ids)} branch entries (<article id> with an h3-h6 '<place>점') in the 지점 찾기 section")
    for bid in ids:
        r = page.evaluate("""bid => { const a = [...document.getElementById(bid).querySelectorAll('a')]
            .find(x => /네이버 예약/.test(x.getAttribute('aria-label') || x.textContent)); if (!a) return null;
          const b = a.getBoundingClientRect(), s = getComputedStyle(a);
          const px = v => v.endsWith('%') ? parseFloat(v) / 100 * b.height : parseFloat(v);
          return [Math.min(...[s.borderTopLeftRadius, s.borderTopRightRadius, s.borderBottomLeftRadius,
                               s.borderBottomRightRadius].map(v => px(v.split(' ').pop()))), b.height]; }""", bid)
        if not r:
            fail(f"AC117 branch {bid} has no 네이버 예약 link")
        elif r[0] < r[1] / 2 - 0.5:
            fail(f"AC117 branch {bid}: 네이버 예약 border-radius {r[0]:.1f}px is below half its height {r[1]:.1f}px")
    menu = page.locator("header button, header summary").filter(has_text="지점")
    shown = [menu.nth(i) for i in range(menu.count()) if menu.nth(i).evaluate(IN_VIEW)]
    if not shown:
        fail("AC118 no visible <button> or <summary> in the <header> whose text contains '지점' at 1440px")
        return
    for bid in ids:  # the panel is closed on load (the thumbnail does not show it)
        links = page.locator(f'header a[href="#{bid}"]')
        if any(links.nth(i).evaluate(IN_VIEW) for i in range(links.count())):
            fail(f"AC119 the header link to #{bid} is visible before the 지점 menu is opened (panel open on load)")
    shown[0].click()
    page.wait_for_timeout(600)
    for bid in ids:
        links = page.locator(f'header a[href="#{bid}"]')
        vis = [links.nth(i) for i in range(links.count()) if links.nth(i).evaluate(IN_VIEW)]
        if not vis:
            fail(f"AC119 after opening the 지점 menu, no visible link in the <header> to #{bid}")
            continue
        ok = vis[0].evaluate("""(a, dir) => [...a.querySelectorAll('img')].some(i => (i.currentSrc || i.src).includes(dir)
            && i.complete && i.naturalWidth > 0 && i.getBoundingClientRect().width > 0)""", f"/profile/{slug}/img/")
        if not ok:
            fail(f"AC120 the 지점 menu link to #{bid} shows no loaded photo from img/")
    page.evaluate("document.fonts.ready")  # fonts the open panel requested finish before the reload (AC56)
    page.wait_for_load_state("networkidle")
    page.reload(wait_until="networkidle")  # the menu closed again before the screenshots
    page.wait_for_timeout(1500)


def thumb_fresh(page, base, slug):  # AC5: thumb.jpg shows the current first screen (profile_thumb.py was re-run)
    if not (ROOT / "profile" / slug / "thumb.jpg").is_file():
        fail("AC5 thumb.jpg missing")
        return None
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
        fail(f"AC5 thumb.jpg differs from the current first screen (mean difference {diff:.1f} > {THUMB_MAX_DIFF}); "
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


def tree_state(slug):
    tree = git("rev-parse", f"HEAD:profile/{slug}") or "none"
    status = git("status", "--porcelain", "--", f"profile/{slug}")
    return tree, "unknown" if status is None else "dirty" if status else "clean"


def check_page(browser, base, slug, shots):
    url = f"{base}/profile/{slug}/"
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
        if not guard("AC8 AC9", any_visible, page.get_by_text(MARK, exact=False)):
            fail(f"{'AC8' if vp is DESKTOP else 'AC9'} sample notice not visible without scrolling at {label}")
        sid, links = guard("AC20", branch_links, page) or (None, None)
        if links is not None and not guard("AC33 AC34", any_visible, links):
            fail(f"{'AC33' if vp is DESKTOP else 'AC34'} no link to the 지점 찾기 section visible without scrolling "
                 f"at {label}")
        if vp is DESKTOP:
            tdiff = guard("AC5", thumb_fresh, page, base, slug)
            guard("AC39", keep_all, page)
            if slug == "fitness-mideoum":
                guard("AC90-AC96", d_first_screen, page, slug, sid)
                guard("AC99", d_h2_faces, page)
                guard("AC105", no_big_digits, page)
            else:
                guard("AC109 AC113 AC116", b_first_screen, page, slug)
                guard("AC117-AC120", b_branches, page, slug, sid)
        elif links is not None:
            guard("AC35 AC36", branch_link_everywhere, page, links)
        guard("AC55", digit_fonts, page, label)
        guard("settle", settle, page)
        if vp is DESKTOP:
            guard("AC76", no_overflow, page, "AC76 1440px")  # after the scroll-through, on the full page
        name = "desktop-1440.png" if vp is DESKTOP else "mobile-390.png"
        heights[name] = guard("screenshots", bands, page, out / name, vp["width"])
        for b in bad_fonts:  # read last, so font files fetched during the scroll-through count too
            fail(f"AC56 web font request did not return 200 at {label}: {b}")
        ctx.close()
    def iframe_390():  # AC77: inside a width:390px iframe, as playbook §4 does it
        ctx, page = new_page(browser, DESKTOP)
        page.goto(f"{base}/profile/")
        page.set_content(f'<iframe src="{url}" style="width:390px;height:844px;border:0"></iframe>')
        page.frame_locator("iframe").locator("body").wait_for()
        inner = page.frames[1]
        inner.wait_for_load_state("networkidle")
        inner.wait_for_timeout(1500)
        settle(inner)
        no_overflow(inner, "AC77 390px iframe")
        ctx.close()
    guard("AC77", iframe_390)

    def motion(label, vp):  # AC67
        ctx, page = new_page(browser, vp, reduced_motion="reduce")
        page.goto(url, wait_until="networkidle")
        settle(page)
        reduced_motion(page, label)
        ctx.close()
    for label, vp in (("1440px", DESKTOP), ("390px", MOBILE)):
        guard(f"AC67 {label}", motion, label, vp)
    tree, dirty = tree_state(slug)
    lines = [f"slug {slug}", f"head {git('rev-parse', 'HEAD') or 'unknown'}", f"site tree {tree}",
             f"site working tree {dirty}", *(f"height {k} {v}" for k, v in heights.items()),
             f"thumb difference {tdiff:.1f}" if tdiff is not None else "thumb difference n/a",
             *(f"FAIL {f}" for f in fails), f"result {'PASS' if not fails else 'FAIL'}"]
    (out / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"screenshots for the reviews: {out}/desktop-1440*.png {out}/mobile-390*.png, summary {out / 'summary.txt'}")


def check_gallery(browser, base):
    ctx, page = new_page(browser, DESKTOP)
    page.goto(f"{base}/profile/", wait_until="networkidle")
    page.click('.pf-filters button[data-filter="fitness"]')
    page.wait_for_timeout(300)
    shown = page.locator('a.pf-card[data-industry="fitness"]:visible')
    slugs = sorted(shown.nth(i).get_attribute("data-slug") for i in range(shown.count()))
    if slugs != sorted(SAMPLES):
        fail(f"AC80 fitness filter shows cards {slugs}, expected {sorted(SAMPLES)}")
    if page.locator('.pf-empty[data-industry="fitness"]:visible').count():
        fail("AC81 fitness filter still shows a 준비 중 tile")
    width = "document.getElementById('pf-v-iframe').getBoundingClientRect().width"
    for slug, info in SAMPLES.items():  # each card from a fresh load of /profile/, as a visitor arrives
        if slug not in slugs:
            continue
        page.goto(f"{base}/profile/", wait_until="networkidle")
        page.click('.pf-filters button[data-filter="fitness"]')
        page.wait_for_timeout(300)
        viewer, iframe = page.locator("#pf-viewer"), page.locator("#pf-v-iframe")
        page.locator(f'a.pf-card[data-slug="{slug}"]').click()
        page.wait_for_timeout(300)
        if not viewer.is_visible() or not (iframe.get_attribute("src") or "").endswith(f"/profile/{slug}/"):
            fail(f"AC83 clicking the {slug} card does not open the preview with that sample")
            continue
        try:
            page.frame_locator("#pf-v-iframe").get_by_text(info["stem"]).first.wait_for(state="attached", timeout=10000)
        except Exception:
            fail(f"AC83 {slug}: the preview iframe does not show {info['stem']}")
        for device, cond in (("mobile", "<= 400"), ("desktop", "> 600")):  # the width animates; wait for it
            page.click(f'button[data-device="{device}"]')
            try:
                page.wait_for_function(f"{width} {cond}", timeout=3000)
            except Exception:
                fail(f"AC84 {slug}: {device} button does not switch the preview width ({page.evaluate(width)})")
        page.keyboard.press("Escape")
        try:
            page.wait_for_function("document.getElementById('pf-viewer').hidden", timeout=3000)
        except Exception:
            fail(f"AC85 {slug}: Esc does not close the preview")
    ctx.close()


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
            if slug not in SAMPLES:  # the fitness samples' full pages are in <slug>/ from `page`
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
            for f in out.glob(f"tmp-ref-{slug}*"):
                f.unlink()
            have = all((out / f"ref-{slug}{x}").is_file() for x in (".png", ".txt", "-full.png", "-full-01.png"))
            when = datetime.fromtimestamp((out / f"ref-{slug}.png").stat().st_mtime).date() if have else ""
            notes.append(f"reference {slug} {info['ref']} {'cached ' + str(when) if have else 'unreachable'}: "
                         f"{type(exc).__name__}: {(str(exc).splitlines() or [''])[0]}")
        ctx.close()
    (out / "summary.txt").write_text("\n".join([f"head {git('rev-parse', 'HEAD') or 'unknown'}", *notes]) + "\n",
                                     encoding="utf-8")
    print("\n".join(notes))
    print(f"compare shots: {out}")


if __name__ == "__main__":
    args = sys.argv[1:]
    shots = Path("/tmp/profile-fitness-shots")
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
