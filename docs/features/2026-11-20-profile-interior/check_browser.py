#!/usr/bin/env python3
"""Browser checks for the three interior profile samples (Playwright + installed Google Chrome). Run from the
repository root.

usage: python3 docs/features/2026-11-20-profile-interior/check_browser.py page <slug> | thumb <slug> | gallery | trio
       | compare [--shots DIR]
  page <slug>  AC8-AC10 AC29 AC51 (the two notices are visible) AC42-AC45 AC49 AC70 AC71 AC95-AC97 AC198-AC201, and
               A (interior-robininterior): AC110-AC112 AC114-AC119 AC121 AC123 AC124 AC126 AC127 AC129 AC130 AC134 AC135,
               B (interior-robindesign): AC140-AC143 AC145-AC147 AC149-AC152 AC154-AC159 AC162 AC163,
               C (interior-robinhome): AC171-AC180 AC182-AC186 AC188-AC190.
               Empties DIR/<slug>/ first, then writes full-page screenshots for the reviews (desktop-1440.png,
               mobile-390.png, and the same cut into 1200 px bands -NN.png) and summary.txt last.
  thumb <slug> AC5: thumb.jpg shows the sample's current 1440x900 first screen
  gallery      AC100 AC101 AC103 AC104 AC105 on /profile/
  trio         AC90 AC91: the h1 and wordmark faces of the three samples differ pairwise
  compare      evidence for the reviews, not a check: rewrites DIR/compare/ with first screens (1440x900 and 390x844)
               of the three interior samples and the twelve shipped samples, full pages (and bands) of the twelve
               shipped samples, and of each reference site its first screen and full page at 1440 and its visible text
               (ref-<slug>.png, ref-<slug>-full.png and its -NN bands, ref-<slug>.txt; an HTTP error counts as no
               answer; the last good copy is kept when a site does not answer). summary.txt lists each local tree
               hash and each reference as ok, cached or unreachable. Exit 0 when every local screenshot was written.
DIR defaults to /tmp/profile-interior-shots. Serves the repository root on a free local port itself.
The page clock is fixed at Sunday 2026-11-15 11:00 KST, so a "today" line cannot change between runs.
The page contract these checks read is the "Fixed parameters" section of tasks.md in this folder.
Adapted from docs/features/2026-11-19-profile-beauty/check_browser.py; AC numbers are this feature's spec.md.
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

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("FAIL the Python package playwright is not installed (see preflight(browser) in tasks.md)")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[3]
SAMPLES = {
    "interior-robininterior": {"key": "A", "face": "Do Hyeon", "ref": "https://apartmentary.com/"},
    "interior-robindesign": {"key": "B", "face": "Black Han Sans", "ref": "https://www.studioashby.com/"},
    "interior-robinhome": {"key": "C", "face": "Diphylleia", "ref": "https://studio-mcgee.com/"},
}
SHIPPED = ("flower-bomgyeol", "food-saebyeokmil", "clinic-neuru", "clinic-byeotteul", "clinic-bonui", "law-ganeum",
           "law-goim", "fitness-mideoum", "fitness-jjuuk", "beauty-robinhair", "beauty-robinsalon",
           "beauty-robinhairsalon")
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
NOTICES = (("AC29", "예시 사진이며 실제 시공 사례가 아닙니다."), ("AC51", "가상의 업체이며 실제 견적 · 상담을 받지 않습니다."))
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
CLOCK = datetime(2026, 11, 15, 11, 0, tzinfo=timezone(timedelta(hours=9)))  # a Sunday
KOREAN_FONT = re.compile(r"Pretendard|\bKR\b|Nanum|Gowun|Gothic A1|Hahmlet|Song Myung|Black Han Sans|Do Hyeon|Jua"
                         r"|Orbit|Sunflower|Gaegu|Dongle|Hi Melody|Gamja Flower|Poor Story|Stylish|Yeon Sung"
                         r"|Gugi|Dokdo|Single Day|Cute Font|Kirang Haerang|Bagel Fat One|Diphylleia", re.I)
DISPLAY_FACES = ("Do Hyeon", "Black Han Sans", "Diphylleia")  # AC198
BODY_FACES = ("Pretendard Variable", "Pretendard")  # AC199 AC200
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
THUMB_MAX_TILE = 40.0  # the same per 10x10-pixel tile of the 160x100 images (16 x 10 tiles), so a changed area shows
THUMB_MAX_DIFF = 15.0  # mean absolute RGB difference (0-255) at 160x100 between thumb.jpg and a fresh first screen
INK_A, PAGE_B, INK_B, PINK, TEAL, LILAC = (22, 24, 27), (248, 241, 251), (27, 20, 48), (238, 104, 174), (11, 95, 101), (222, 177, 241)
PAGE_C, CREAM, INK_C, SAND = (42, 63, 99), (240, 234, 223), (28, 36, 51), (210, 169, 106)
fails = []


def fail(msg):
    fails.append(msg)


def guard(label, fn, *args):  # a check that throws is one failure; the remaining checks and summary.txt still run
    try:
        return fn(*args)
    except Exception as exc:
        fail(f"{label}: {type(exc).__name__}: {(str(exc).splitlines() or [''])[0]}")
        return None


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

# Helpers every page script below can call: installed once per page by lib().
LIB = """() => { window.__c = {
  rgba: v => { const m = (v || '').match(/^rgba?\\(([^)]+)\\)$/); if (!m) return null;
    const p = m[1].split(/[\\s,\\/]+/).filter(Boolean).map(parseFloat); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; },
  box: e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; },
  ext: e => { const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let b = null;  // the extent of the rendered text:
    for (let n; (n = w.nextNode());) { if (!n.nodeValue.trim()) continue;  // the union of the text nodes' line boxes, so
      const g = document.createRange(); g.selectNodeContents(n);  // neither the element's box nor a block child's widens it
      for (const r of g.getClientRects()) { if (!r.width || !r.height) continue;
        b = b ? [Math.min(b[0], r.left), Math.min(b[1], r.top), Math.max(b[2], r.right), Math.max(b[3], r.bottom)] : [r.left, r.top, r.right, r.bottom]; } }
    return b || [0, 0, 0, 0]; },
  fam: e => getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/^['"]|['"]$/g, ''),
  own: e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('').trim(),
  shown: e => { const s = getComputedStyle(e), r = e.getBoundingClientRect();
    return e.getClientRects().length > 0 && r.width > 1 && r.height > 1 && s.visibility !== 'hidden'; },
  pinned: e => { for (; e; e = e.parentElement) if (/fixed|sticky/.test(getComputedStyle(e).position)) return true; return false; },
  sec: re => { const hit = [...document.querySelectorAll('section[id]')].filter(s =>
      [...s.querySelectorAll('h2')].some(h => h.closest('section') === s && re.test(h.textContent)));
    return hit.length === 1 ? hit[0] : null; },
  bg: el => { const layers = [];  // the colour behind el: translucent layers composited down to the first opaque one
    for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e);
      if (s.backgroundImage !== 'none') return {err: 'a CSS background-image on <' + e.tagName.toLowerCase() + '> behind it'};
      const c = window.__c.rgba(s.backgroundColor); if (!c) return {err: 'unreadable background ' + s.backgroundColor};
      if (c[3] > 0) { layers.push(c); if (c[3] >= 1) break; } }
    let base = [255, 255, 255];
    for (const c of layers.reverse()) base = [0, 1, 2].map(i => c[i] * c[3] + base[i] * (1 - c[3]));
    return {c: base}; },
  info: e => { if (!e) return null; const s = getComputedStyle(e), c = window.__c;
    return {box: c.box(e), ext: c.ext(e), fs: parseFloat(s.fontSize), fam: c.fam(e), color: c.rgba(s.color),
      bg: c.rgba(s.backgroundColor), bgImage: s.backgroundImage, ls: s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing),
      align: s.textAlign, style: s.fontStyle, text: e.textContent.replace(/\\s+/g, ' ').trim().slice(0, 40),
      radius: [s.borderTopLeftRadius, s.borderTopRightRadius, s.borderBottomLeftRadius, s.borderBottomRightRadius]
        .map(v => { const p = v.split(' ')[0]; return p.endsWith('%') ? parseFloat(p) / 100 * e.getBoundingClientRect().height : parseFloat(p); })}; },
}; }"""


def lib(target):
    target.evaluate(LIB)


def info(target, selector):  # box, text extent, font and colours of the first element matching selector, or None
    return target.evaluate("sel => window.__c.info(document.querySelector(sel))", selector)


def rgb(c):  # [r, g, b, a] -> (r, g, b) when opaque, else None
    return tuple(round(x) for x in c[:3]) if c and c[3] >= 0.999 else None


def hexs(c):
    return "#%02x%02x%02x" % tuple(c)


def want_color(ac, what, got, *want):  # got: [r, g, b, a] from the page
    if rgb(got) not in want:
        fail(f"{ac} {what} is {got}, expected {' or '.join(hexs(w) for w in want)}")


def want_face(ac, what, got, face):
    if got != face:
        fail(f"{ac} {what} has computed first font family {got!r}, not {face!r}")


CONTACT_ID = "() => { const s = window.__c.sec(/문의|상담/); return s ? s.id : null; }"
EXAMPLE_ID = "() => { const s = window.__c.sec(/예시/); return s ? s.id : null; }"


def contact_links(page):  # links to the contact section whose text contains 견적 or 상담 (AC42-AC44)
    sid = page.evaluate(CONTACT_ID)
    if not sid:
        fail("AC32 no single <section id> whose own <h2> contains 문의 or 상담; the contact link checks cannot run")
        return None, None
    return sid, page.locator(f'a[href="#{sid}"]').filter(has_text=re.compile("견적|상담"))


POSITIONS = """() => { const out = [], H = document.documentElement.scrollHeight;
  for (let y = 0; ; y += 40) { const t = Math.min(y, H - innerHeight); out.push(t);
    if (t >= H - innerHeight) break; } return out; }"""  # every 40 px down to the end (AC44): a bar is taller than that

LAST_FOOTER_TEXT = """() => { const f = [...document.querySelectorAll('footer')].pop(); if (!f) return null;
  const pinned = e => { for (; e; e = e.parentElement) if (/fixed|sticky/.test(getComputedStyle(e).position)) return true;
    return false; };  // a bar inside <footer> is not the footer's last line
  return [f, ...f.querySelectorAll('*')].filter(e => e.getClientRects().length && !pinned(e)
    && [...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim())).pop() || null; }"""


UNDER_BAR = """el => { const r = el.getBoundingClientRect();  // does a fixed or sticky element overlap any part of the line?
  return [...document.body.querySelectorAll('*')].some(e => { if (e.contains(el) || !/fixed|sticky/.test(getComputedStyle(e).position)) return false;
    const b = e.getBoundingClientRect(); if (!b.width || !b.height || getComputedStyle(e).visibility === 'hidden') return false;
    return Math.min(r.right, b.right) - Math.max(r.left, b.left) > 1 && Math.min(r.bottom, b.bottom) - Math.max(r.top, b.top) > 1; }); }"""


def contact_link_everywhere(page, links):  # AC44, then AC45
    positions = page.evaluate(POSITIONS)
    for y in positions:
        page.evaluate(f"scrollTo({{top: {y}, behavior: 'instant'}})")
        for _ in range(15):  # up to 1.5 s for a bar that slides in
            if any_visible(links):
                break
            page.wait_for_timeout(100)
        else:
            fail(f"AC44 no 견적 · 상담 link to the contact section on screen at scroll {int(y)}px of {int(positions[-1])}px (390px)")
    page.evaluate("scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")  # the page may have grown
    last = page.evaluate_handle(LAST_FOOTER_TEXT).as_element()
    for _ in range(15):  # up to 1.5 s for a footer that fades or slides in
        if not last or last.evaluate(IN_VIEW):
            break
        page.wait_for_timeout(100)
    if not last:
        fail("AC45 no <footer> text to read at the end of the page (390px)")
    elif not last.evaluate(IN_VIEW) or last.evaluate(UNDER_BAR):
        fail(f"AC45 the footer's last text line is covered or off screen at the end of the page (390px): "
             f"{last.evaluate('e => e.textContent.trim().slice(0, 40)')}")
    page.evaluate("scrollTo(0, 0)")


def notices_shown(page, label):  # AC29 AC51: each sentence is on screen once scrolled to, not hidden or covered
    for ac, text in NOTICES:
        loc = page.get_by_text(text, exact=False)
        seen = False
        for i in range(loc.count()):
            loc.nth(i).evaluate("e => e.scrollIntoView({block: 'center', behavior: 'instant'})")
            for _ in range(15):  # up to 1.5 s for a block that fades in
                if loc.nth(i).evaluate(IN_VIEW):
                    seen = True
                    break
                page.wait_for_timeout(100)
        if not seen:
            fail(f"{ac} the sentence '{text}' is not visible on the page at {label}")
    page.evaluate("scrollTo(0, 0)")


def notice_size(page, ac, label):  # AC8 AC9 AC10
    loc = page.get_by_text(MARK, exact=False)
    seen = [loc.nth(i) for i in range(loc.count()) if loc.nth(i).evaluate(IN_VIEW)]
    if not seen:
        fail(f"{ac} sample notice not visible without scrolling at {label}")
        return
    sizes = [el.evaluate("e => [parseFloat(getComputedStyle(e).fontSize), parseFloat(getComputedStyle(document.body).fontSize)]")
             for el in seen]
    if not any(fs >= body and fs >= 14 for fs, body in sizes):
        fail(f"AC10 the first-screen sample notice is set at {sizes[0][0]}px, below the body size {sizes[0][1]}px or "
             f"14px, at {label}")


def no_overflow(target, label):  # AC96 AC97
    w = target.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    if w[0] > w[1]:
        fail(f"{label} horizontal overflow: scrollWidth {w[0]} > clientWidth {w[1]}")


def keep_all(page):  # AC49
    bad = page.evaluate("""() => [...document.querySelectorAll('p, li, dd, dt, td, th')]
      .filter(e => /[가-힣]/.test(e.textContent) && getComputedStyle(e).wordBreak !== 'keep-all')
      .map(e => e.textContent.trim().slice(0, 40))""")
    for t in bad:
        fail(f"AC49 Korean text without word-break: keep-all: {t}")


def digit_fonts(page, label):  # AC70: digits of hours and phone numbers in a Korean or monospaced face
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
        fail(f"AC70 no visible 상담 hours or phone number found at {label}")
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
            fail(f"AC70 digits rendered in {main!r}, neither Korean nor monospaced, at {label}: {texts[i]}")
    page.evaluate("document.querySelectorAll('[data-digit-probe]').forEach(p => p.remove())")
    cdp.detach()


def font_responses(page):  # AC71: every web font request returns 200
    bad = []
    page.on("response", lambda r: any(h in r.url for h in FONT_HOSTS) and r.status != 200
            and bad.append(f"{r.status} {r.url}"))
    page.on("requestfailed", lambda r: any(h in r.url for h in FONT_HOSTS) and bad.append(f"failed {r.url}"))
    return bad


def reduced_motion(page, label):  # AC95
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
        fail(f"AC95 under prefers-reduced-motion at {label}: {b}")


def contact_faces(page, label):  # AC200: the hours and the phone number of the contact section are set in Pretendard
    rows = page.evaluate("""() => { const s = window.__c.sec(/문의|상담/); if (!s) return null; const out = [];
      const walk = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
      while (walk.nextNode()) { const t = walk.currentNode;
        if (/\\d{1,2}:\\d{2}|0\\d{1,2}-\\d{3,4}-\\d{4}/.test(t.nodeValue) && t.parentElement.getClientRects().length)
          out.push([t.nodeValue.trim().slice(0, 40), window.__c.fam(t.parentElement)]); }
      return out; }""")
    if not rows:
        fail(f"AC200 no visible 상담 hours or phone number in the contact section at {label}")
    for text, fam in rows or []:
        if fam not in BODY_FACES:
            fail(f"AC200 {text!r} in the contact section has computed first family {fam!r}, not Pretendard, at {label}")


def faces(page, label):  # AC198 AC199
    fam = page.evaluate("window.__c.fam(document.body)")
    if fam not in BODY_FACES:
        fail(f"AC199 the <body>'s computed first family is {fam!r}, not Pretendard, at {label}")
    bad = page.evaluate("""faces => [...document.body.querySelectorAll('*')].filter(e => faces.includes(window.__c.fam(e))
        && getComputedStyle(e).fontWeight !== '400' && e.getClientRects().length)
      .map(e => e.tagName.toLowerCase() + ' ' + e.textContent.trim().slice(0, 20) + ' at weight ' + getComputedStyle(e).fontWeight).slice(0, 10)""",
                        list(DISPLAY_FACES))
    for b in bad:
        fail(f"AC198 an element in a one-weight display face is not font-weight 400 at {label}: {b}")


def contrast(page, label):  # AC201, on the whole page with every <details> opened
    bad = page.evaluate("""() => { const c = window.__c, out = [];
      document.querySelectorAll('details').forEach(d => { d.open = true; });
      const doc = r => [r.left + scrollX, r.top + scrollY, r.right + scrollX, r.bottom + scrollY];
      const imgs = [...document.images].filter(c.shown).map(i => doc(i.getBoundingClientRect()));
      const lum = v => { const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; };
        return 0.2126 * f(v[0]) + 0.7152 * f(v[1]) + 0.0722 * f(v[2]); };
      for (const e of document.body.querySelectorAll('*')) {
        if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(e.tagName) || !c.own(e) || !c.shown(e)) continue;
        let o = 1; for (let x = e; x; x = x.parentElement) o *= +getComputedStyle(x).opacity;
        if (o === 0) continue;
        const r = doc(e.getBoundingClientRect()), tag = e.tagName.toLowerCase() + ' ' + JSON.stringify(c.own(e).slice(0, 24));
        if (!c.pinned(e) && imgs.some(i => r[0] < i[2] && r[2] > i[0] && r[1] < i[3] && r[3] > i[1])) continue;  // text on a photo: AC98 AC99
        const s = getComputedStyle(e), fg = c.rgba(s.color), bg = c.bg(e);
        if (!fg || bg.err) { out.push(tag + ': cannot judge, ' + (bg.err || 'unreadable colour ' + s.color)); continue; }
        const a = fg[3] * o, mix = [0, 1, 2].map(i => fg[i] * a + bg.c[i] * (1 - a));
        const l1 = lum(mix), l2 = lum(bg.c), ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
        const need = parseFloat(s.fontSize) >= 24 ? 3 : 4.5;
        if (ratio < need) out.push(tag + ': contrast ' + ratio.toFixed(2) + ':1 below ' + need + ':1 (text ' + mix.map(Math.round) + ' on ' + bg.c.map(Math.round) + ', ' + s.fontSize + ')');
      }
      return out.slice(0, 15); }""")
    for b in bad:
        fail(f"AC201 at {label}: {b}")


IN_BAR = """e => { if (e.closest('header')) return true;  // a header link or a fixed/sticky bar link is not the hero link
  for (let a = e; a; a = a.parentElement) { const p = getComputedStyle(a).position;  // a bar: under a quarter screen high
    if ((p === 'fixed' || p === 'sticky') && a.getBoundingClientRect().height < innerHeight / 4) return true; }
  return false; }"""


def web_font(page, selector, ac, what, face):  # AC71: the main rendered font is the sample's face, loaded as a web font
    cdp = page.context.new_cdp_session(page)
    try:
        cdp.send("DOM.enable")
        cdp.send("CSS.enable")
        root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
        node = cdp.send("DOM.querySelector", {"nodeId": root, "selector": selector})["nodeId"]
        if not node:
            return
        fonts = cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node})["fonts"]
        main = max(fonts, key=lambda f: f["glyphCount"]) if fonts else None
        if not main or not main.get("isCustomFont") or main["familyName"] != face:
            fail(f"{ac} the {what} renders in {main and main['familyName']!r}, not in the loaded web font {face!r} "
                 f"(the requested face did not load, or a fallback drew the text)")
    finally:
        cdp.detach()


def boxes_overlap(a, b):  # [left, top, right, bottom]
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def no_big_digits(page):  # AC135: no element whose own text has a digit above 24px, pseudo-elements included
    bad = page.evaluate("""() => { const out = [];
      const own = e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('');
      for (const e of document.body.querySelectorAll('*')) {
        const t = own(e), sz = parseFloat(getComputedStyle(e).fontSize);
        if (/\\d/.test(t) && sz > 24 && e.getClientRects().length) out.push(t.trim().slice(0, 20) + ' at ' + sz + 'px');
        for (const ps of ['::before', '::after']) { const c = getComputedStyle(e, ps);
          if (c.content === 'none' || c.content === 'normal' || c.display === 'none') continue;
          if ((/\\d/.test(c.content) || /counter/.test(c.content)) && parseFloat(c.fontSize) > 24)
            out.push(ps + ' ' + c.content.slice(0, 20) + ' at ' + c.fontSize); }
        if (e.tagName === 'LI' && e.getClientRects().length && getComputedStyle(e).display === 'list-item'
            && /decimal/.test(getComputedStyle(e).listStyleType)
            && !['none', '""', "''"].includes(getComputedStyle(e, '::marker').content) && parseFloat(getComputedStyle(e, '::marker').fontSize) > 24)
          out.push('::marker of ' + own(e).trim().slice(0, 20) + ' at ' + getComputedStyle(e, '::marker').fontSize); }
      return out.slice(0, 10); }""")
    for b in bad:
        fail(f"AC135 a digit set above 24px: {b}")


OVER_PHOTO = """([box, skip]) => { const c = window.__c, out = [];  // elements with their own text that overlap the photo box
  for (const e of document.body.querySelectorAll('*')) { if (!c.own(e) || !c.shown(e) || c.pinned(e)) continue;
    if (skip && e.closest(skip)) continue; const r = c.box(e);
    if (r[0] < box[2] && r[2] > box[0] && r[1] < box[3] && r[3] > box[1]) out.push(e.tagName.toLowerCase() + ' ' + c.own(e).slice(0, 24)); }
  return out.slice(0, 6); }"""

CARDS = """re => { const s = window.__c.sec(new RegExp(re)); if (!s) return null;
  return [...s.querySelectorAll('figure')].map(f => window.__c.box(f)); }"""


def first_img(page, slug, ac):
    r = page.evaluate("""() => { const i = document.querySelector('img'); if (!i) return null;
      return {src: i.currentSrc || i.src, box: window.__c.box(i), radius: window.__c.info(i).radius}; }""")
    if not r or f"/profile/{slug}/img/" not in r["src"]:
        fail(f"{ac} the first <img> of the page is not from the sample's img/ ({r and r['src']})")
        return None
    return r


def card_row(page, ac, n):  # the <figure> cards of the example section share a top edge within 4px
    boxes = page.evaluate(CARDS, "예시")
    if not boxes or len(boxes) != n:
        fail(f"{ac} expected {n} <figure> cards in the example section, found {len(boxes or [])}")
    elif max(b[1] for b in boxes) - min(b[1] for b in boxes) > 4:
        fail(f"{ac} the cards' top edges spread more than 4px: {[round(b[1]) for b in boxes]}")


def card_stack(page, ac, n, per_row):  # at 390: one column (per_row 1) or rows of two (per_row 2)
    boxes = page.evaluate(CARDS, "예시")
    if not boxes or len(boxes) != n:
        fail(f"{ac} expected {n} <figure> cards in the example section, found {len(boxes or [])} (390px)")
        return
    rows = [boxes[i:i + per_row] for i in range(0, n, per_row)]
    ok = all(max(b[1] for b in row) - min(b[1] for b in row) <= 4 for row in rows)
    ok = ok and all(min(b[1] for b in rows[i + 1]) >= max(b[3] for b in rows[i]) - 1 for i in range(len(rows) - 1))
    ok = ok and all(row[i + 1][0] >= row[i][2] - 1 for row in rows for i in range(len(row) - 1))
    if not ok:
        fail(f"{ac} at 390px the {n} cards do not form rows of {per_row}: {[[round(x) for x in b] for b in boxes]}")


def link_in(page, scope, sid, ac, what):  # the visible links to the contact section, with 견적 or 상담, in scope
    r = page.evaluate("""([scope, sid]) => [...document.querySelectorAll(scope + ' a[href="#' + sid + '"]')]
        .filter(x => /견적|상담/.test(x.textContent) && window.__c.shown(x)).map(x => window.__c.info(x))""", [scope, sid])
    if not r:
        fail(f"{ac} {what} holds no visible link to #{sid} whose text contains 견적 or 상담")
    return r


# --- sample A ----------------------------------------------------------------------------------------------

def a_desktop(page, slug, sid):  # AC110-AC112 AC114-AC116 AC118 AC119 AC121 AC123 AC124 AC126 AC127 AC129 AC134 AC135
    W = page.evaluate("document.documentElement.clientWidth")
    head, wm, nav, h1 = (info(page, s) for s in ("header", "header a.wordmark", "header nav", "h1"))
    if not head or not wm or not nav or not h1:
        fail(f"AC110-AC127 a <header>, its a.wordmark, its <nav> or the <h1> is missing")
        return
    if not rgb(head["bg"]) or min(rgb(head["bg"])) < 0xF8:
        fail(f"AC110 the <header> background {head['bg']} has a channel below 0xF8 or is not opaque")
    if wm["box"][0] > 144:
        fail(f"AC111 the wordmark's left edge is at {wm['box'][0]:.0f}px, more than 144px from the left")
    want_face("AC112", "the header wordmark", wm["fam"], "Do Hyeon")
    if not 20 <= wm["fs"] <= 26:
        fail(f"AC112 the header wordmark is set at {wm['fs']}px, not 20-26px")
    if abs((nav["box"][0] + nav["box"][2]) / 2 - W / 2) > 144:
        fail(f"AC114 the header <nav> centre is at {(nav['box'][0] + nav['box'][2]) / 2:.0f}px, more than 144px from {W / 2:.0f}px")
    pills = page.evaluate("""sid => [...document.querySelectorAll('header a[href="#' + sid + '"]')]
        .filter(x => /상담/.test(x.textContent) && window.__c.shown(x)).map(x => window.__c.info(x))""", sid) if sid else []
    pill = next((x for x in pills if 0.75 * W <= x["box"][2] <= W), None)  # a nav link may say 상담 too
    if not pills:
        fail("AC115 the <header> holds no visible link to the contact section whose text contains 상담")
    elif not pill:
        fail(f"AC115 no header 상담 link has its right edge in the right quarter (right edges: "
             f"{[round(x['box'][2]) for x in pills]})")
    else:
        if min(pill["radius"]) < (pill["box"][3] - pill["box"][1]) / 2 - 0.5:
            fail(f"AC116 the header 상담 link's border-radius {min(pill['radius']):.1f}px is below half its height")
        want_color("AC116", "the header 상담 link's background", pill["bg"], INK_A)
    photo = first_img(page, slug, "AC118")
    if photo:
        b = photo["box"]
        if b[0] > 1 or b[2] < W - 1 or abs(b[1] - head["box"][3]) > 2:
            fail(f"AC118 the first photo {[round(x) for x in b]} does not span the viewport width directly under the "
                 f"<header> (bottom {head['box'][3]:.0f}px)")
        if not 450 <= b[3] - b[1] <= 612:
            fail(f"AC119 the first photo is {b[3] - b[1]:.0f}px high, not 450-612px")
        eid = page.evaluate(EXAMPLE_ID)
        inside = page.evaluate("""box => [...document.querySelectorAll('a')].filter(a => { if (!window.__c.shown(a)) return false;
            const r = window.__c.box(a); return r[0] >= box[0] - 1 && r[2] <= box[2] + 1 && r[1] >= box[1] - 1 && r[3] <= box[3] + 1; })
          .map(a => [a.getAttribute('href'), a.textContent.trim(), a.classList.contains('hero-caption'),
                     a.getBoundingClientRect().height, parseFloat(getComputedStyle(a).fontSize)])""", b)
        if len(inside) != 1 or not inside[0][2] or inside[0][0] != f"#{eid}" or "예시" not in inside[0][1]:
            fail(f"AC121 expected one link inside the first photo, the a.hero-caption to #{eid} with 예시 in its text; "
                 f"found {[x[:2] for x in inside]}")
        elif inside[0][3] > 1.8 * inside[0][4]:
            fail(f"AC123 the caption box is {inside[0][3]:.0f}px high, more than 1.8 x its font-size {inside[0][4]}px")
        for t in page.evaluate(OVER_PHOTO, [b, ".hero-caption"]):
            fail(f"AC124 an element with its own text overlaps the first photo: {t}")
        if h1["box"][1] < b[3] - 0.5 or h1["box"][1] > 840:
            fail(f"AC126 the <h1> top is at {h1['box'][1]:.0f}px; it must be below the photo ({b[3]:.0f}px) and at most 840px")
    want_face("AC127", "the <h1>", h1["fam"], "Do Hyeon")
    card_row(page, "AC129", 3)
    foot = page.evaluate("() => { const f = [...document.querySelectorAll('footer')].pop(); return f ? window.__c.info(f) : null; }")
    want_color("AC134", "the <footer> background", foot and foot["bg"], INK_A)
    no_big_digits(page)


def a_mobile(page, sid):  # AC117 AC130
    pill = page.locator(f'header a[href="#{sid}"]').filter(has_text="상담") if sid else None
    if pill is None or not any_visible(pill):
        fail("AC117 the header 상담 link is not visible without scrolling at 390px")
    card_stack(page, "AC130", 3, 1)


# --- sample B ----------------------------------------------------------------------------------------------

def b_blocks(page, ac):
    n = page.evaluate("[document.querySelectorAll('.wordmark-block').length, document.querySelectorAll('.headline-block').length]")
    if n != [1, 1]:
        fail(f'{ac} expected one element with class "wordmark-block" and one with class "headline-block", found {n}')
        return None, None
    return info(page, ".wordmark-block"), info(page, ".headline-block")


def b_desktop(page, slug, sid):  # AC140-AC143 AC145-AC147 AC149-AC152 AC157-AC159 AC162
    W, H = page.evaluate("[document.documentElement.clientWidth, innerHeight]")
    for t in page.evaluate("""() => { const c = window.__c, out = [];
        for (const e of [document.documentElement, document.body, ...document.body.querySelectorAll('*')]) { const r = c.box(e);
          if (!c.shown(e) || r[1] >= innerHeight || r[3] <= 0 || r[0] >= innerWidth || r[2] <= 0) continue;
          if (e.tagName === 'IMG') out.push('<img> ' + e.getAttribute('src'));
          for (const ps of [null, '::before', '::after']) if (getComputedStyle(e, ps).backgroundImage !== 'none'
              && (!ps || getComputedStyle(e, ps).content !== 'none'))
            out.push(e.tagName.toLowerCase() + (ps || '') + ' background-image ' + getComputedStyle(e, ps).backgroundImage.slice(0, 40)); }
        return out.slice(0, 6); }"""):
        fail(f"AC140 the first screen is not free of photos and background images: {t}")
    wb, hb = b_blocks(page, "AC141")
    if not wb:
        return
    a, b = wb["box"], hb["box"]
    for name, x in (("wordmark", a), ("headline", b)):
        if not 0.4 * W <= x[2] - x[0] <= 0.6 * W:
            fail(f"AC141 the {name} block is {x[2] - x[0]:.0f}px wide, not 40-60 % of {W}px")
        if min(x[3], H) - max(x[1], 0) < 720:
            fail(f"AC142 the {name} block shows {min(x[3], H) - max(x[1], 0):.0f}px of its height in the viewport, below 720px")
    if boxes_overlap(a, b) or min(a[0], b[0]) > 1 or max(a[2], b[2]) < W - 1 or abs(a[1] - b[1]) > 4:
        fail(f"AC141 the two blocks do not sit side by side across the full width: {[round(x) for x in a]} {[round(x) for x in b]}")
    want_color("AC143", "the wordmark block's background", wb["bg"], PINK)
    want_color("AC143", "the headline block's background", hb["bg"], TEAL)
    wm = info(page, "header a.wordmark")
    if not wm:
        fail("AC144 no a.wordmark in the <header>")
    else:
        ext = wm["ext"]
        if wm["fs"] < 180 or ext[3] - ext[1] < 1.8 * wm["fs"] or ext[2] - ext[0] < 0.7 * (a[2] - a[0]):
            fail(f"AC145 the wordmark is set at {wm['fs']}px with rendered text {ext[2] - ext[0]:.0f}x{ext[3] - ext[1]:.0f}px; "
                 f"it needs 180px or more, text at least 1.8 x that high and at least {0.7 * (a[2] - a[0]):.0f}px wide")
        want_face("AC146", "the wordmark", wm["fam"], "Black Han Sans")
        want_color("AC146", "the wordmark's colour", wm["color"], INK_B)
        if wm["ls"] > 0.05 * wm["fs"]:
            fail(f"AC147 the wordmark's letter-spacing {wm['ls']}px is above 0.05 x its font-size")
    h1 = page.evaluate("() => { const h = document.querySelector('h1'); return h && h.closest('.headline-block') "
                       "&& !h.querySelector('a.wordmark') && !h.closest('a.wordmark') ? window.__c.info(h) : null; }")
    if not h1:
        fail("AC149 the <h1> is not inside the headline block, or it is the wordmark")
    else:
        want_face("AC149", "the <h1>", h1["fam"], "Black Han Sans")
        want_color("AC149", "the <h1>'s colour", h1["color"], PAGE_B)
    ctas = link_in(page, ".headline-block", sid, "AC150", "the headline block") if sid else None
    if ctas and not any(rgb(c["bg"]) == PINK and rgb(c["color"]) == INK_B for c in ctas):  # one such link is enough
        want_color("AC150", "the headline block link's background", ctas[0]["bg"], PINK)
        want_color("AC150", "the headline block link's colour", ctas[0]["color"], INK_B)
    nav = page.locator("header nav a")
    if nav.count() < 4 or not all(nav.nth(i).evaluate(IN_VIEW) for i in range(nav.count())):
        fail(f"AC151 the header <nav> needs at least four links, all visible on the first screen (found {nav.count()})")
    doc = page.evaluate("document.documentElement.scrollHeight")
    cover = page.evaluate("""() => [...document.body.querySelectorAll('*')].filter(e => getComputedStyle(e).position === 'fixed' && window.__c.shown(e))
      .map(e => { const r = window.__c.box(e); return Math.max(0, Math.min(r[2], innerWidth) - Math.max(r[0], 0)) * Math.max(0, Math.min(r[3], innerHeight) - Math.max(r[1], 0)) / (innerWidth * innerHeight); })""")
    if any(c > 0.5 for c in cover) or doc <= 1800:
        fail(f"AC152 a fixed element covers more than half the viewport ({[round(c, 2) for c in cover]}) or the document is only {doc}px tall")
    band = page.evaluate("""([w, lilac]) => { const c = window.__c; for (const s of document.querySelectorAll('section')) {
        const r = c.box(s), bg = c.rgba(getComputedStyle(s).backgroundColor);
        if (r[0] > 1 || r[2] < w - 1 || !bg || bg[3] < 1 || bg.slice(0, 3).join() !== lilac.join()) continue;
        if (s.querySelectorAll('p').length !== 1 || s.querySelector('img')) continue;
        return c.info(s.querySelector('p')); } return null; }""", [W, list(LILAC)])
    if not band:
        fail("AC157 no full-width <section> with the background #deb1f1 that holds exactly one <p> and no <img>")
    else:
        ext = band["ext"]
        if band["align"] != "center" or abs((ext[0] + ext[2]) / 2 - W / 2) > 24:
            fail(f"AC158 the band paragraph is not centred (text-align {band['align']}, text centre {(ext[0] + ext[2]) / 2:.0f}px)")
        want_color("AC158", "the band paragraph's colour", band["color"], INK_B)
    feat = page.evaluate("""() => { const c = window.__c, s = c.sec(/예시/), p = s && s.querySelector('.feature-panel');
      const f = p && p.closest('.feature'), imgs = f ? [...f.querySelectorAll('img')] : [];
      return p && f ? {panel: c.info(p), imgs: imgs.map(c.box)} : null; }""")
    if not feat or len(feat["imgs"]) != 1:
        fail('AC159 the example section needs a .feature that holds a .feature-panel and exactly one <img>')
    else:
        p, i = feat["panel"]["box"], feat["imgs"][0]
        if rgb(feat["panel"]["bg"]) not in (TEAL, PINK) or feat["panel"]["bgImage"] != "none":
            fail(f"AC159 the feature panel's background is {feat['panel']['bg']} (image {feat['panel']['bgImage'][:30]}), not #0b5f65 or #ee68ae")
        if abs(p[1] - i[1]) > 4 or boxes_overlap(p, i) or min(p[2] - p[0], i[2] - i[0]) < 0.35 * W:
            fail(f"AC159 the feature panel and its photo are not side by side, each at least 35 % of the width: "
                 f"{[round(x) for x in p]} {[round(x) for x in i]}")
    card_row(page, "AC162", 4)


def b_mobile(page):  # AC154 AC155 AC156 AC163
    W, H = page.evaluate("[document.documentElement.clientWidth, innerHeight]")
    wb, hb = b_blocks(page, "AC154")
    if wb:
        a, b = wb["box"], hb["box"]
        above = page.evaluate("""([mark, top]) => [...document.body.querySelectorAll('*')].filter(e => window.__c.own(e) && window.__c.shown(e)
            && !window.__c.pinned(e) && window.__c.box(e)[3] <= top + 1 && !e.textContent.includes(mark)).map(e => window.__c.own(e).slice(0, 20))""", [MARK, a[1]])
        if a[0] > 1 or a[2] < W - 1 or above:
            fail(f"AC154 at 390px the wordmark block is not the full-width first block (box {[round(x) for x in a]}, text above it: {above[:3]})")
        if b[0] > 1 or b[2] < W - 1 or abs(b[1] - a[3]) > 1:
            fail(f"AC154 at 390px the headline block is not full-width directly below the wordmark block: {[round(x) for x in b]}")
        wm = info(page, "header a.wordmark")
        if not wm or wm["fs"] < 90 or a[3] - a[1] > 420:
            fail(f"AC155 at 390px the wordmark is set at {wm and wm['fs']}px (needs 90px or more) in a block {a[3] - a[1]:.0f}px high (at most 420px)")
    h1 = page.locator("h1").first
    box = info(page, "h1")
    if not box or box["box"][1] < 0 or box["box"][3] > H or not h1.evaluate(IN_VIEW) or h1.evaluate(UNDER_BAR):
        fail(f"AC156 at 390px the <h1> is not fully inside the first screen and uncovered (box {box and [round(x) for x in box['box']]})")
    card_stack(page, "AC163", 4, 2)


# --- sample C ----------------------------------------------------------------------------------------------

def c_desktop(page, slug, sid):  # AC171-AC180 AC182-AC186 AC188 AC190
    W, H = page.evaluate("[document.documentElement.clientWidth, innerHeight]")
    head, wm, h1 = (info(page, s) for s in ("header", "header a.wordmark", "h1"))
    if not head or not wm or not h1:
        fail("AC171-AC185 a <header>, its a.wordmark or the <h1> is missing")
        return
    if head["bg"] is None or (head["bg"][3] != 0 and rgb(head["bg"]) != PAGE_C):
        fail(f"AC171 the <header> background is {head['bg']}, neither #2a3f63 nor transparent")
    photo = first_img(page, slug, "AC172")
    if photo:
        b = photo["box"]
        left, right = b[0], W - b[2]
        if b[1] < 0 or b[3] > H or b[2] - b[0] < 1150 or left < 40 or right < 40 or abs(left - right) > 4:
            fail(f"AC172 the first photo {[round(x) for x in b]} must lie inside the first screen, be 1150px wide or "
                 f"more and keep equal side gaps of 40px or more")
        if b[1] < head["box"][3] + 16:
            fail(f"AC173 the first photo's top ({b[1]:.0f}px) is less than 16px below the <header> ({head['box'][3]:.0f}px)")
        if b[2] - b[0] < 1.8 * (b[3] - b[1]) or max(photo["radius"]) > 4:
            fail(f"AC174 the first photo is {b[2] - b[0]:.0f}x{b[3] - b[1]:.0f}px with radius {max(photo['radius'])}px; it "
                 f"needs a width of 1.8 x its height or more and a radius of at most 4px")
        for t in page.evaluate(OVER_PHOTO, [b, None]):
            fail(f"AC175 an element with its own text overlaps the first photo: {t}")
        hb, ext = h1["box"], h1["ext"]
        if hb[1] < b[3] + 16 or hb[1] < 0 or hb[3] > H or abs((ext[0] + ext[2]) / 2 - W / 2) > 24:
            fail(f"AC176 the <h1> (box {[round(x) for x in hb]}, text centre {(ext[0] + ext[2]) / 2:.0f}px) must start 16px "
                 f"or more below the photo ({b[3]:.0f}px), lie inside the first screen and be centred")
    behind = page.evaluate("window.__c.bg(document.querySelector('h1'))")
    if behind.get("err") or tuple(round(x) for x in behind["c"]) != PAGE_C:
        fail(f"AC177 the background behind the <h1> is {behind}, not #2a3f63")
    if h1["box"][3] - h1["box"][1] > 1.6 * h1["fs"]:
        fail(f"AC178 the <h1> box is {h1['box'][3] - h1['box'][1]:.0f}px high, more than 1.6 x its font-size {h1['fs']}px (one line)")
    want_face("AC179", "the <h1>", h1["fam"], "Diphylleia")
    want_color("AC179", "the <h1>'s colour", h1["color"], CREAM)
    ems = page.evaluate("[...document.querySelectorAll('h1 em')].map(e => window.__c.info(e))")
    if len(ems) != 1 or ems[0]["style"] != "normal" or rgb(ems[0]["color"]) != SAND:
        fail(f"AC180 the <h1> needs exactly one <em> with font-style normal and the colour #d2a96a "
             f"(found {[(e['style'], e['color']) for e in ems]})")
    hero = page.locator(f'a[href="#{sid}"]').filter(has_text=re.compile("견적|상담")) if sid else None
    if hero is None or not any(not hero.nth(i).evaluate(IN_BAR) and hero.nth(i).evaluate(IN_VIEW) for i in range(hero.count())):
        fail("AC182 no 견적 · 상담 link to the contact section is fully visible on the first screen outside the <header> and outside every fixed or sticky bar")
    head_link = page.locator(f'header a[href="#{sid}"]').filter(has_text=re.compile("견적|상담")) if sid else None
    if head_link is None or not any_visible(head_link):
        fail("AC183 the <header> shows no 견적 · 상담 link to the contact section")
    if abs((wm["box"][0] + wm["box"][2]) / 2 - W / 2) > 24:
        fail(f"AC184 the header wordmark's centre is at {(wm['box'][0] + wm['box'][2]) / 2:.0f}px, more than 24px from {W / 2:.0f}px")
    want_face("AC185", "the header wordmark", wm["fam"], "Diphylleia")
    if not 30 <= wm["fs"] <= 44 or wm["ls"] > 0.05 * wm["fs"]:
        fail(f"AC185 the header wordmark is set at {wm['fs']}px with letter-spacing {wm['ls']}px; it needs 30-44px and at most 0.05 x that")
    ex = page.evaluate("""() => { const s = window.__c.sec(/예시/); return s ? {bg: window.__c.rgba(getComputedStyle(s).backgroundColor),
        caps: [...s.querySelectorAll('figcaption')].map(f => window.__c.rgba(getComputedStyle(f).color))} : null; }""")
    if not ex or rgb(ex["bg"]) != CREAM or not ex["caps"] or any(rgb(c) != INK_C for c in ex["caps"]):
        fail(f"AC186 the example section needs the background #f0eadf and caption colour #1c2433 (found {ex})")
    card_row(page, "AC188", 3)
    for t in page.evaluate("""() => { const c = window.__c, out = [];
        for (const e of document.body.querySelectorAll('*')) { if (c.fam(e) !== 'Diphylleia' || !e.getClientRects().length) continue;
          if (/\\d/.test(c.own(e))) out.push(e.tagName.toLowerCase() + ' ' + c.own(e).slice(0, 20));
          for (const ps of ['::before', '::after']) { const s = getComputedStyle(e, ps);
            if (s.content !== 'none' && s.content !== 'normal' && (/\\d/.test(s.content) || /counter/.test(s.content))) out.push(e.tagName.toLowerCase() + ps + ' ' + s.content.slice(0, 20)); }
          if (e.tagName === 'LI' && getComputedStyle(e).display === 'list-item' && /decimal/.test(getComputedStyle(e).listStyleType)) out.push('li marker ' + c.own(e).slice(0, 20)); }
        return out.slice(0, 6); }"""):
        fail(f"AC190 a digit is set in Diphylleia: {t}")


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
        const g = c.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(img, 0, 0, 160, 100); return g.getImageData(0, 0, 160, 100).data; };
      const [x, y] = [px(await load(a)), px(await load(b))]; let s = 0, n = 0; const tiles = new Array(160).fill(0);
      for (let i = 0; i < x.length; i += 4) { const q = i / 4, t = Math.floor((q % 160) / 10) + 16 * Math.floor(q / 1600);
        for (let k = 0; k < 3; k++) { const d = Math.abs(x[i + k] - y[i + k]); s += d; tiles[t] += d; } n += 3; }
      return [s / n, Math.max(...tiles) / 300]; }""", [f"{base}/profile/{slug}/thumb.jpg?{datetime.now().timestamp()}", f"data:image/png;base64,{shot}"])
    ctx.close()
    diff, tile = diff
    if diff > THUMB_MAX_DIFF or tile > THUMB_MAX_TILE:
        fail(f"AC5 thumb.jpg differs from the current first screen (mean difference {diff:.1f}, limit {THUMB_MAX_DIFF}; "
             f"largest 10x10 tile {tile:.1f}, limit {THUMB_MAX_TILE}); re-run python3 scripts/profile_thumb.py {slug}")
    return f"{diff:.1f} (largest tile {tile:.1f})"


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


def check_thumb(browser, base, slug):  # AC5
    ctx, page = new_page(browser, DESKTOP)
    page.goto(f"{base}/profile/{slug}/", wait_until="networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(1500)
    print(f"thumb difference {thumb_fresh(page, base, slug)}")
    ctx.close()


def check_page(browser, base, slug, shots):
    url = f"{base}/profile/{slug}/"
    key = SAMPLES[slug]["key"]
    out = shots / slug
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    heights = {}
    for label, vp in (("1440px", DESKTOP), ("390px", MOBILE)):
        ctx, page = new_page(browser, vp)
        bad_fonts = font_responses(page)
        page.goto(url, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1500)  # let entrance effects finish before judging the first screen
        lib(page)
        for sel, what in (("h1", "h1"), ("header a.wordmark", "wordmark")):  # first: the measurements below need the real faces
            guard("AC71", web_font, page, sel, "AC71", what, SAMPLES[slug]["face"])
        guard("AC8 AC9 AC10", notice_size, page, "AC8" if vp is DESKTOP else "AC9", label)
        sid, links = guard("AC32", contact_links, page) or (None, None)
        if links is not None and not guard("AC42 AC43", any_visible, links):
            fail(f"{'AC42' if vp is DESKTOP else 'AC43'} no 견적 · 상담 link to the contact section visible without "
                 f"scrolling at {label}")
        if vp is DESKTOP:
            guard("AC49", keep_all, page)
            guard(f"sample {key} at 1440px", {"A": a_desktop, "B": b_desktop, "C": c_desktop}[key], page, slug, sid)
        else:
            if key == "A":
                guard("AC117 AC130", a_mobile, page, sid)
            elif key == "B":
                guard("AC154-AC163", b_mobile, page)
            else:
                guard("AC189", card_stack, page, "AC189", 3, 1)
            if links is not None:
                guard("AC44 AC45", contact_link_everywhere, page, links)
        guard("AC29 AC51", notices_shown, page, label)
        guard("AC70", digit_fonts, page, label)
        guard("AC200", contact_faces, page, label)
        guard("AC198 AC199", faces, page, label)
        guard("settle", settle, page)
        if vp is DESKTOP:
            guard("AC96", no_overflow, page, "AC96 1440px")  # after the scroll-through, on the full page
        name = "desktop-1440.png" if vp is DESKTOP else "mobile-390.png"
        heights[name] = guard("screenshots", bands, page, out / name, vp["width"])
        guard("AC201", contrast, page, label)  # last: it opens every <details>
        for b in bad_fonts:  # read last, so font files fetched during the scroll-through count too
            fail(f"AC71 web font request did not return 200 at {label}: {b}")
        ctx.close()

    def iframe_390():  # AC97: inside a width:390px iframe, as playbook §4 does it
        ctx, page = new_page(browser, DESKTOP)
        page.goto(f"{base}/profile/")
        page.set_content(f'<iframe src="{url}" style="width:390px;height:844px;border:0"></iframe>')
        page.frame_locator("iframe").locator("body").wait_for()
        inner = page.frames[1]
        inner.wait_for_load_state("networkidle")
        inner.wait_for_timeout(1500)
        settle(inner)
        no_overflow(inner, "AC97 390px iframe")
        ctx.close()
    guard("AC97", iframe_390)

    def motion(label, vp):  # AC95
        ctx, page = new_page(browser, vp, reduced_motion="reduce")
        page.goto(url, wait_until="networkidle")
        settle(page)
        reduced_motion(page, label)
        ctx.close()
    for label, vp in (("1440px", DESKTOP), ("390px", MOBILE)):
        guard(f"AC95 {label}", motion, label, vp)
    tree, dirty = tree_state(slug)
    lines = [f"slug {slug}", f"head {git('rev-parse', 'HEAD') or 'unknown'}", f"site tree {tree}",
             f"site working tree {dirty}", *(f"height {k} {v}" for k, v in heights.items()),
             *(f"FAIL {f}" for f in fails), f"result {'PASS' if not fails else 'FAIL'}"]
    (out / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"screenshots for the reviews: {out}/desktop-1440*.png {out}/mobile-390*.png, summary {out / 'summary.txt'}")


def check_gallery(browser, base):  # AC100 AC101 AC103 AC104 AC105
    ctx, page = new_page(browser, DESKTOP)
    page.goto(f"{base}/profile/", wait_until="networkidle")
    page.click('.pf-filters button[data-filter="interior"]')
    page.wait_for_timeout(300)
    shown = page.locator('a.pf-card[data-industry="interior"]:visible')
    slugs = sorted(shown.nth(i).get_attribute("data-slug") for i in range(shown.count()))
    if slugs != sorted(SAMPLES):
        fail(f"AC100 interior filter shows cards {slugs}, expected {sorted(SAMPLES)}")
    if page.locator('.pf-empty[data-industry="interior"]:visible').count():
        fail("AC101 interior filter still shows a 준비 중 tile")
    width = "document.getElementById('pf-v-iframe').getBoundingClientRect().width"
    for slug in SAMPLES:  # each card from a fresh load of /profile/, as a visitor arrives
        if slug not in slugs:
            continue
        page.goto(f"{base}/profile/", wait_until="networkidle")
        page.click('.pf-filters button[data-filter="interior"]')
        page.wait_for_timeout(300)
        viewer, iframe = page.locator("#pf-viewer"), page.locator("#pf-v-iframe")
        page.locator(f'a.pf-card[data-slug="{slug}"]').click()
        page.wait_for_timeout(300)
        if not viewer.is_visible() or not (iframe.get_attribute("src") or "").endswith(f"/profile/{slug}/"):
            fail(f"AC103 clicking the {slug} card does not open the preview with that sample")
            continue
        try:  # the loaded document is this sample's page (matched by slug)
            page.frame_locator("#pf-v-iframe").locator("header a.wordmark").first.wait_for(state="attached",
                                                                                            timeout=10000)
            next(f for f in page.frames if f.url.rstrip("/").endswith(f"/profile/{slug}"))
        except Exception:
            fail(f"AC103 {slug}: the preview iframe does not show that sample's page")
        for device, cond in (("mobile", "<= 400"), ("desktop", "> 600")):  # the width animates; wait for it
            page.click(f'button[data-device="{device}"]')
            try:
                page.wait_for_function(f"{width} {cond}", timeout=3000)
            except Exception:
                fail(f"AC104 {slug}: {device} button does not switch the preview width ({page.evaluate(width)})")
        page.keyboard.press("Escape")
        try:
            page.wait_for_function("document.getElementById('pf-viewer').hidden", timeout=3000)
        except Exception:
            fail(f"AC105 {slug}: Esc does not close the preview")
    ctx.close()


def first_of(target, selector):  # computed first font family of the first element matching selector, or None
    return target.evaluate("""sel => { const e = document.querySelector(sel); if (!e) return null;
      return getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/^['"]|['"]$/g, ''); }""", selector)



def check_trio(browser, base):  # AC90 AC91: h1 faces and wordmark faces differ pairwise across the three samples
    got = {}
    for slug in SAMPLES:
        if not (ROOT / "profile" / slug / "index.html").is_file():
            fail(f"AC90 AC91 profile/{slug}/index.html does not exist")
            continue
        ctx, page = new_page(browser, DESKTOP)
        page.goto(f"{base}/profile/{slug}/", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        got[slug] = (first_of(page, "h1"), first_of(page, "header a.wordmark"))
        ctx.close()
    for i, (ac, what) in enumerate((("AC90", "h1"), ("AC91", "header wordmark"))):
        fams = {slug: f[i] for slug, f in got.items()}
        for slug, fam in fams.items():
            if not fam:
                fail(f"{ac} {slug}: no {what} to read a font family from")
        named = [f.lower() for f in fams.values() if f]
        if len(set(named)) != len(named):
            fail(f"{ac} two samples share the {what}'s first font family: {fams}")
    print("faces (h1, wordmark):", got)


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
            if slug not in SAMPLES:  # the interior samples' full pages are in <slug>/ from `page`
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
    shots = Path("/tmp/profile-interior-shots")
    if "--shots" in args:
        i = args.index("--shots")
        if i + 1 >= len(args):
            raise SystemExit(__doc__)
        shots = Path(args[i + 1]).resolve()
        if shots == ROOT or ROOT in shots.parents:  # `page` empties DIR/<slug>/; never inside the repository
            raise SystemExit(f"--shots must be outside the repository: {shots}")
        del args[i:i + 2]
    per_slug = ("page", "thumb")
    if not args or args[0] not in (*per_slug, "gallery", "trio", "compare") or \
            (args[0] in per_slug and (len(args) != 2 or args[1] not in SAMPLES)) or (args[0] not in per_slug and len(args) != 1):
        raise SystemExit(__doc__)
    if args[0] in per_slug and not (ROOT / "profile" / args[1] / "index.html").is_file():
        print(f"FAIL profile/{args[1]}/index.html does not exist")
        print(f"FAIL: {' '.join(args)} (1 failures)")
        sys.exit(1)
    httpd, base = serve()
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(channel="chrome")
        except Exception as exc:
            print(f"FAIL Google Chrome did not start: {(str(exc).splitlines() or [''])[0]}")
            sys.exit(1)
        try:
            if args[0] == "page":
                check_page(browser, base, args[1], shots)
            elif args[0] == "thumb":
                check_thumb(browser, base, args[1])
            elif args[0] == "gallery":
                check_gallery(browser, base)
            elif args[0] == "trio":
                check_trio(browser, base)
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
