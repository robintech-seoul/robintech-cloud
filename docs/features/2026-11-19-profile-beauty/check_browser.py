#!/usr/bin/env python3
"""Browser checks for the three hair-salon franchise profile samples (Playwright + installed Google Chrome). Run from
the repository root.

usage: python3 docs/features/2026-11-19-profile-beauty/check_browser.py page <slug> | gallery | trio | compare
       [--shots DIR]
  page <slug>  AC5 (thumb.jpg is the current first screen) AC8 AC9 AC35-AC38 AC41 AC62 AC63 AC84 AC85 AC86, and
               A (beauty-robinhair): AC97-AC99 AC104 AC105 AC107 AC112-AC115 AC118 AC119,
               B (beauty-robinsalon): AC120-AC124 AC129 AC132 AC133,
               C (beauty-robinhairsalon): AC140 AC142-AC144 AC147 AC148 AC152.
               Empties DIR/<slug>/ first, then writes full-page screenshots for the reviews (desktop-1440.png,
               mobile-390.png, and the same cut into 1200 px bands -NN.png) and summary.txt last.
  gallery      AC89 AC90 AC92 AC93 AC94 on /profile/
  trio         AC154 AC155: the h1 and wordmark faces of the three samples differ pairwise
  compare      evidence for the reviews, not a check: rewrites DIR/compare/ with first screens (1440x900 and 390x844)
               of the three beauty samples and the nine shipped samples, full pages (and bands) of the nine shipped
               samples, and of each reference site its first screen and full page at 1440 and its visible text
               (ref-<slug>.png, ref-<slug>-full.png and its -NN bands, ref-<slug>.txt; an HTTP error counts as no
               answer; the last good copy is kept when a site does not answer). summary.txt lists each local tree
               hash and each reference as ok, cached or unreachable. Exit 0 when every local screenshot was written.
DIR defaults to /tmp/profile-beauty-shots. Serves the repository root on a free local port itself.
The page clock is fixed at Sunday 2026-11-15 11:00 KST, so a "today" line cannot change between runs.
The page contract these checks read is the "Fixed parameters" section of tasks.md in this folder.
Adapted from docs/features/2026-11-18-profile-fitness/check_browser.py; AC numbers are this feature's spec.md.
"""
from datetime import datetime, timedelta, timezone
from functools import partial
from html import unescape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import base64
import re
import shutil
import subprocess
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
SAMPLES = {
    "beauty-robinhair": {"key": "A", "ref": "https://spokeandweal.com/"},
    "beauty-robinsalon": {"key": "B", "ref": "https://www.pschair.co.kr/"},
    "beauty-robinhairsalon": {"key": "C", "ref": "https://www.thelanesalon.com/"},
}
SHIPPED = ("flower-bomgyeol", "food-saebyeokmil", "clinic-neuru", "clinic-byeotteul", "clinic-bonui", "law-ganeum",
           "law-goim", "fitness-mideoum", "fitness-jjuuk")
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
CLOCK = datetime(2026, 11, 15, 11, 0, tzinfo=timezone(timedelta(hours=9)))  # a Sunday
KOREAN_FONT = re.compile(r"Pretendard|\bKR\b|Nanum|Gowun|Gothic A1|Hahmlet|Song Myung|Black Han Sans|Do Hyeon|Jua"
                         r"|Orbit|Sunflower|Gaegu|Dongle|Hi Melody|Gamja Flower|Poor Story|Stylish|Yeon Sung"
                         r"|Gugi|Dokdo|Single Day|Cute Font|Kirang Haerang|Bagel Fat One|Diphylleia", re.I)
C_FACES = ("Nanum Gothic", "Sunflower")  # AC148
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
THUMB_MAX_TILE = 40.0  # the same per 10x10-pixel tile of the 160x100 images (16 x 10 tiles), so a changed area shows
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
    .find(e => /(지점|매장)\\s?찾기/.test(e.textContent) && !e.closest('header')); const s = h && h.closest('section'); return s ? s.id : null; }"""

BRANCH_ENTRIES = """sid => { const s = document.getElementById(sid); if (!s) return [];
  return [...s.querySelectorAll('article[id]')].filter(a => { const h = a.querySelector('h3, h4, h5, h6');
    return h && /(^|\\s)([가-힣]{1,8})점$/.test(h.textContent.trim()) && !/(^|\\s)지점$/.test(h.textContent.trim()); })
    .map(a => a.id); }"""


def branch_links(page):  # links to the 지점 찾기 section (AC35-AC37 AC113 AC152)
    sid = page.evaluate(BRANCH_ID)
    if not sid:
        fail("AC22 no <section id> holding a '지점 찾기' or '매장 찾기' heading; the 지점 link checks cannot run")
        return None, None
    return sid, page.locator(f'a[href="#{sid}"]')


POSITIONS = """() => { const out = [], H = document.documentElement.scrollHeight;
  for (let y = 0; ; y += innerHeight / 2) { const t = Math.min(y, H - innerHeight); out.push(t);
    if (t >= H - innerHeight) break; } return out; }"""  # every half screen down to the end (AC37)

LAST_FOOTER_TEXT = """() => { const f = [...document.querySelectorAll('footer')].pop(); if (!f) return null;
  const pinned = e => { for (; e; e = e.parentElement) if (/fixed|sticky/.test(getComputedStyle(e).position)) return true;
    return false; };  // a bar inside <footer> is not the footer's last line
  return [f, ...f.querySelectorAll('*')].filter(e => e.getClientRects().length && !pinned(e)
    && [...e.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim())).pop() || null; }"""


def branch_link_everywhere(page, links):  # AC37, then AC38
    positions = page.evaluate(POSITIONS)
    for y in positions:
        page.evaluate(f"scrollTo({{top: {y}, behavior: 'instant'}})")
        for _ in range(15):  # up to 1.5 s for a bar that slides in
            if any_visible(links):
                break
            page.wait_for_timeout(100)
        else:
            fail(f"AC37 no link to the 지점 찾기 section on screen at scroll {int(y)}px of {int(positions[-1])}px (390px)")
    page.evaluate("scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")  # the page may have grown
    last = page.evaluate_handle(LAST_FOOTER_TEXT).as_element()
    for _ in range(15):  # up to 1.5 s, as for AC37, for a footer that fades or slides in
        if not last or last.evaluate(IN_VIEW):
            break
        page.wait_for_timeout(100)
    if not last:
        fail("AC38 no <footer> text to read at the end of the page (390px)")
    elif not last.evaluate(IN_VIEW):
        fail(f"AC38 the footer's last text line is covered or off screen at the end of the page (390px): "
             f"{last.evaluate('e => e.textContent.trim().slice(0, 40)')}")
    page.evaluate("scrollTo(0, 0)")


def no_overflow(target, label):  # AC85 AC86
    w = target.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    if w[0] > w[1]:
        fail(f"{label} horizontal overflow: scrollWidth {w[0]} > clientWidth {w[1]}")


def keep_all(page):  # AC41
    bad = page.evaluate("""() => [...document.querySelectorAll('p, li, dd, dt, td, th')]
      .filter(e => /[가-힣]/.test(e.textContent) && getComputedStyle(e).wordBreak !== 'keep-all')
      .map(e => e.textContent.trim().slice(0, 40))""")
    for t in bad:
        fail(f"AC41 Korean text without word-break: keep-all: {t}")


def digit_fonts(page, label):  # AC62: digits of hours and phone numbers in a Korean or monospaced face
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
        fail(f"AC62 no visible opening hours or phone number found at {label}")
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
            fail(f"AC62 digits rendered in {main!r}, neither Korean nor monospaced, at {label}: {texts[i]}")
    page.evaluate("document.querySelectorAll('[data-digit-probe]').forEach(p => p.remove())")
    cdp.detach()


def font_responses(page):  # AC63: every web font request returns 200
    bad = []
    page.on("response", lambda r: any(h in r.url for h in FONT_HOSTS) and r.status != 200
            and bad.append(f"{r.status} {r.url}"))
    page.on("requestfailed", lambda r: any(h in r.url for h in FONT_HOSTS) and bad.append(f"failed {r.url}"))
    return bad


def reduced_motion(page, label):  # AC84
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
        fail(f"AC84 under prefers-reduced-motion at {label}: {b}")


def first_family(target, selector_js):
    return target.evaluate(f"""() => [...document.querySelectorAll({selector_js!r})].map(e =>
      [e.textContent.trim().slice(0, 30), getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/^['"]|['"]$/g, '')])""")


def first_of(target, selector):  # computed first font family of the first element matching selector, or None
    return target.evaluate("""sel => { const e = document.querySelector(sel); if (!e) return null;
      return getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/^['"]|['"]$/g, ''); }""", selector)


def header_link(page, ac, word):  # AC114 AC115 AC132 AC133 AC142 AC143
    links = page.locator("header a")
    if not any(links.nth(i).evaluate(IN_VIEW) and word in links.nth(i).inner_text() for i in range(links.count())):
        fail(f"{ac} no visible link in the <header> whose text contains '{word}' at 1440px")


IN_BAR = """e => { if (e.closest('header')) return true;  // a header link or a fixed/sticky bar link is not the hero link
  for (let a = e; a; a = a.parentElement) { const p = getComputedStyle(a).position;  // a bar: under a quarter screen high
    if ((p === 'fixed' || p === 'sticky') && a.getBoundingClientRect().height < innerHeight / 4) return true; }
  return false; }"""


def web_font(page, selector, ac, what):  # AC63: the main rendered font is a loaded web font, not a local copy or a fallback
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
        if not main or not main.get("isCustomFont"):
            fail(f"{ac} the {what} renders in {main and main['familyName']!r}, not in a loaded web font "
                 f"(the requested face did not load)")
    finally:
        cdp.detach()


def hero_cta(page, sid, ac, words):  # AC113 AC152: a visible link outside every <header> to the 지점 찾기 section
    if not sid:
        fail(f"{ac} no 지점 찾기 section id; the hero link check cannot run")
        return
    cta = page.locator(f'a[href="#{sid}"]')
    for i in range(cta.count()):
        el = cta.nth(i)
        txt = el.inner_text()
        if not el.evaluate(IN_BAR) and all(w in txt for w in words) and el.evaluate(IN_VIEW):
            return
    fail(f"{ac} no visible link outside the <header> on the first screen to #{sid} whose text contains "
         f"{' and '.join(words)} (1440px)")


def boxes_overlap(a, b):  # [left, top, right, bottom]
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def box_of(target, selector):
    return target.evaluate("""sel => { const e = document.querySelector(sel); if (!e) return null;
      const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; }""", selector)


PHOTOS = """dir => { const out = [];  // first-screen photos from img/: an <img> (currentSrc) or an element's own background
  for (const el of document.body.querySelectorAll('*')) { const s = getComputedStyle(el);
    const src = el.tagName === 'IMG' ? (el.currentSrc || el.src) : (s.backgroundImage.match(/url\\(["']?([^"')]+)/) || [])[1];
    if (!src || !src.includes(dir) || s.visibility === 'hidden' || s.display === 'none') continue;
    const r = el.getBoundingClientRect();
    if (r.top < innerHeight && r.bottom > 0 && r.width > 0 && r.height > 0)
      out.push({tag: el.tagName, img: el.tagName === 'IMG', box: [r.left, r.top, r.right, r.bottom]}); }
  return out; }"""


# --- sample A ----------------------------------------------------------------------------------------------

def ital_families(slug):  # Google Fonts families whose family= value in index.html requests ital (AC107)
    html = (ROOT / "profile" / slug / "index.html").read_text(encoding="utf-8")
    out = set()
    for u in re.findall(r"https?://fonts\.googleapis\.com/css2?\?[^\"'\s)]+", unescape(html)):
        for fam in parse_qs(urlparse(u).query).get("family", []):
            name, _, axes = fam.partition(":")
            if "ital" in axes:
                out.add(name.replace("+", " ").strip().lower())
    return out


def a_first_screen(page, slug, sid):  # AC97-AC99 AC104 AC105 AC107 AC113-AC115
    header_link(page, "AC114", "지점")
    header_link(page, "AC115", "가맹")
    hero_cta(page, sid, "AC113", ("지점", "예약"))
    photos = page.evaluate(PHOTOS, f"/profile/{slug}/img/")
    W = page.evaluate("document.documentElement.clientWidth")
    full = [p for p in photos if p["box"][0] <= 1 and p["box"][2] >= W - 1]
    h1 = box_of(page, "h1")
    if not full:
        fail(f"AC97 no photo from img/ spans the full viewport width in the first screen at 1440px "
             f"(photos seen: {[[round(x) for x in p['box']] for p in photos][:4]})")
    elif not h1 or not any(boxes_overlap(h1, p["box"]) for p in full):
        fail(f"AC98 the h1 box {h1} does not overlap the full-bleed hero photo box {full[0]['box']}")
    if h1 and abs((h1[0] + h1[2]) / 2 - W / 2) > 24:
        fail(f"AC99 the h1 centre {(h1[0] + h1[2]) / 2:.0f}px is more than 24px from the viewport centre {W / 2:.0f}px")
    fam = first_of(page, "h1")
    if fam != "Nanum Myeongjo":
        fail(f"AC104 the h1's computed first font family is {fam!r}, not 'Nanum Myeongjo'")
    em = page.evaluate("""() => { const e = document.querySelector('h1 em'); if (!e) return null; const s = getComputedStyle(e);
      return [s.fontStyle, s.fontFamily.split(',')[0].trim().replace(/^['"]|['"]$/g, '')]; }""")
    if not em:
        fail("AC105 the h1 has no <em>")
        return
    if em[0] != "italic":
        fail(f"AC105 the h1 <em> has computed font-style {em[0]!r}, not 'italic'")
    ital = ital_families(slug)
    if em[1].lower() not in ital:
        fail(f"AC107 the h1 <em>'s first family {em[1]!r} is not requested with ital from Google Fonts ({sorted(ital)})")


def pills(page, sid, ac):  # AC112: the 네이버 예약 link of each branch entry is a pill
    ids = page.evaluate(BRANCH_ENTRIES, sid) if sid else []
    if len(ids) < 3:
        fail(f"{ac} found {len(ids)} branch entries (<article id> with an h3-h6 '<place>점') in the 지점 찾기 section")
    for bid in ids:
        r = page.evaluate("""bid => { const a = [...document.getElementById(bid).querySelectorAll('a')]
            .find(x => /네이버 예약/.test(x.getAttribute('aria-label') || x.textContent)); if (!a) return null;
          const b = a.getBoundingClientRect(), s = getComputedStyle(a);
          const px = v => v.endsWith('%') ? parseFloat(v) / 100 * b.height : parseFloat(v);
          return [Math.min(...[s.borderTopLeftRadius, s.borderTopRightRadius, s.borderBottomLeftRadius,
                               s.borderBottomRightRadius].map(v => px(v.split(' ').pop()))), b.height]; }""", bid)
        if not r:
            fail(f"{ac} branch {bid} has no 네이버 예약 link")
        elif r[0] < r[1] / 2 - 0.5:
            fail(f"{ac} branch {bid}: 네이버 예약 border-radius {r[0]:.1f}px is below half its height {r[1]:.1f}px")


def no_big_digits(page):  # AC118: no element whose own text has a digit above 24px, pseudo-elements included
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
        fail(f"AC118 a digit set above 24px: {b}")


def no_round_img(page):  # AC119: no <img> whose every corner radius is at least half its rendered width
    bad = page.evaluate("""() => [...document.querySelectorAll('img')].filter(i => i.getClientRects().length).map(i => {
        const b = i.getBoundingClientRect(), s = getComputedStyle(i);
        const px = v => { v = v.split(' ')[0]; return v.endsWith('%') ? parseFloat(v) / 100 * b.width : parseFloat(v); };
        const r = Math.min(...[s.borderTopLeftRadius, s.borderTopRightRadius, s.borderBottomLeftRadius,
                               s.borderBottomRightRadius].map(px));
        return [i.getAttribute('src'), r, b.width]; }).filter(([, r, w]) => w > 0 && r >= w / 2 - 0.5)""")
    for src, r, w in bad:
        fail(f"AC119 <img> {src} has border-radius {r:.1f}px, at least half its width {w:.1f}px")


# --- sample B ----------------------------------------------------------------------------------------------

BIG_WORDS = """() => { const out = [];  // first-screen elements whose own text is set at 160px or more (AC120)
  const own = e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('').trim();
  for (const e of document.body.querySelectorAll('*')) { const t = own(e); if (!t) continue;
    const s = getComputedStyle(e), r = e.getBoundingClientRect();
    if (parseFloat(s.fontSize) < 160 || !r.width || s.visibility === 'hidden' || s.display === 'none') continue;
    if (r.top >= innerHeight || r.bottom <= 0 || r.left >= innerWidth || r.right <= 0) continue;
    e.setAttribute('data-big-word', String(out.length));
    out.push({text: t, size: parseFloat(s.fontSize), box: [r.left, r.top, r.right, r.bottom],
              fam: s.fontFamily.split(',')[0].trim().replace(/^['"]|['"]$/g, '')}); }
  return out; }"""

PAINT_ORDER = """([x, y, n]) => {  // AC124: is a photo listed before the big word at (x, y)?
  const style = document.createElement('style');
  style.textContent = '*, *::before, *::after { pointer-events: auto !important; }';
  document.head.append(style);
  const stack = document.elementsFromPoint(x, y); style.remove();
  const word = document.querySelector(`[data-big-word="${n}"]`);
  const isPhoto = e => { const s = getComputedStyle(e);
    const src = e.tagName === 'IMG' ? (e.currentSrc || e.src) : (s.backgroundImage.match(/url\\(["']?([^"')]+)/) || [])[1];
    return !!src && src.includes('/img/'); };
  const wi = stack.findIndex(e => e === word || word.contains(e)), pi = stack.findIndex(e => isPhoto(e) && !e.contains(word));
  return [pi, wi, stack.slice(0, 6).map(e => e.tagName + (e.className ? '.' + e.className : ''))]; }"""


def b_first_screen(page, slug):  # AC120-AC124 AC132 AC133
    header_link(page, "AC132", "지점")
    header_link(page, "AC133", "가맹")
    words = page.evaluate(BIG_WORDS)
    if not words:
        fail("AC120 no first-screen element whose own text is set at 160px or more (1440px)")
        return
    photos = page.evaluate(PHOTOS, f"/profile/{slug}/img/")
    for n, w in enumerate(words):
        if not re.search(r"[가-힣]", w["text"]) or re.search(r"[A-Za-z]", w["text"]):
            fail(f"AC121 the {w['size']:.0f}px text {w['text']!r} needs a Hangul syllable and no Latin letter")
        if w["fam"] != "Song Myung":
            fail(f"AC122 the {w['size']:.0f}px text {w['text']!r} has computed first family {w['fam']!r}, not 'Song Myung'")
        over = [(p, [max(w["box"][0], p["box"][0]), max(w["box"][1], p["box"][1]),
                     min(w["box"][2], p["box"][2]), min(w["box"][3], p["box"][3])])
                for p in photos if boxes_overlap(w["box"], p["box"])]
        if not over:
            fail(f"AC123 the {w['size']:.0f}px text {w['text']!r} overlaps no photo from img/ (1440px)")
            continue
        _, o = max(over, key=lambda x: (x[1][2] - x[1][0]) * (x[1][3] - x[1][1]))
        vw, vh = page.evaluate("[document.documentElement.clientWidth, innerHeight]")
        o = [max(o[0], 0), max(o[1], 0), min(o[2], vw), min(o[3], vh)]
        pi, wi, top = page.evaluate(PAINT_ORDER, [(o[0] + o[2]) / 2, (o[1] + o[3]) / 2, n])
        if pi < 0 or wi < 0 or pi > wi:
            fail(f"AC124 at the centre of the overlap, the photo is not listed before the {w['text']!r} element "
                 f"(photo {pi}, word {wi}; top of stack {top})")


def style_strip(page):  # AC129: the visible 스타일 cards share a top edge within 4px
    tops = page.evaluate("""() => { const h = [...document.querySelectorAll('h2, h3, h4, h5, h6')]
        .find(e => /스타일/.test(e.textContent) && !e.closest('header')); const s = h && h.closest('section');
      if (!s) return null; s.scrollIntoView({block: 'start', behavior: 'instant'});
      return [...s.querySelectorAll('article')].map(a => a.getBoundingClientRect())
        .filter(r => r.width > 0 && r.height > 0 && r.right > 0 && r.left < innerWidth).map(r => r.top); }""")
    page.evaluate("scrollTo({top: 0, behavior: 'instant'})")
    page.wait_for_timeout(300)
    if not tops:
        fail("AC129 no visible <article> card in a <section> with a 스타일 heading (1440px)")
    elif max(tops) - min(tops) > 4:
        fail(f"AC129 the visible 스타일 cards' top edges spread {max(tops) - min(tops):.1f}px (> 4px): {tops}")


# --- sample C ----------------------------------------------------------------------------------------------

def c_first_screen(page, slug, sid):  # AC140 AC142-AC144 AC147 AC148 AC152
    rows = page.evaluate("""() => [...document.querySelectorAll('header nav a')].map(a => { const s = getComputedStyle(a);
        return [a.textContent.trim().slice(0, 20), s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing),
                parseFloat(s.fontSize)]; })""")
    if not rows:
        fail("AC140 no <a> inside a <nav> in the <header>")
    for txt, ls, fs in rows:
        if ls < 0.1 * fs - 0.01:
            fail(f"AC140 header nav link {txt!r}: letter-spacing {ls:.2f}px < 0.1 x font-size {fs:.1f}px")
    header_link(page, "AC142", "지점")
    header_link(page, "AC143", "가맹")
    hero_cta(page, sid, "AC152", ("지점",))
    tall = [p for p in page.evaluate(PHOTOS, f"/profile/{slug}/img/") if p["img"]
            and (p["box"][3] - p["box"][1]) >= 1.4 * (p["box"][2] - p["box"][0])]
    pairs = [(a, b) for i, a in enumerate(tall) for b in tall[i + 1:]
             if abs(a["box"][1] - b["box"][1]) <= 8 and not boxes_overlap(a["box"], b["box"])]
    if not pairs:
        fail(f"AC144 no two first-screen <img> from img/ side by side, each at least 1.4x as tall as wide, tops within "
             f"8px, not overlapping (tall ones seen: {[[round(x) for x in p['box']] for p in tall][:4]})")
    h1 = box_of(page, "h1")
    for a, b in pairs:
        for p in (a, b):
            if h1 and boxes_overlap(h1, p["box"]):
                fail(f"AC147 the h1 box {[round(x) for x in h1]} overlaps the tall photo {[round(x) for x in p['box']]}")
    for txt, fam in first_family(page, "h1, h2"):
        if fam not in C_FACES:
            fail(f"AC148 heading {txt!r}: computed first font family {fam!r} is not one of {C_FACES}")


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


def check_page(browser, base, slug, shots):
    url = f"{base}/profile/{slug}/"
    key = SAMPLES[slug]["key"]
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
        sid, links = guard("AC22", branch_links, page) or (None, None)
        if links is not None and not guard("AC35 AC36", any_visible, links):
            fail(f"{'AC35' if vp is DESKTOP else 'AC36'} no link to the 지점 찾기 section visible without scrolling "
                 f"at {label}")
        if vp is DESKTOP:
            tdiff = guard("AC5", thumb_fresh, page, base, slug)
            guard("AC41", keep_all, page)
            if key == "A":
                guard("AC97-AC115", a_first_screen, page, slug, sid)
                guard("AC112", pills, page, sid, "AC112")
                guard("AC118", no_big_digits, page)
                guard("AC119", no_round_img, page)
            elif key == "B":
                guard("AC120-AC133", b_first_screen, page, slug)
                guard("AC129", style_strip, page)
            else:
                guard("AC140-AC152", c_first_screen, page, slug, sid)
        elif links is not None:
            guard("AC37 AC38", branch_link_everywhere, page, links)
        guard("AC62", digit_fonts, page, label)
        if vp is DESKTOP:
            for sel, what in (("h1", "h1"), ("header a.wordmark", "wordmark"), (".display-word", "display word")):
                guard("AC63", web_font, page, sel, "AC63", what)
        guard("settle", settle, page)
        if vp is DESKTOP:
            guard("AC85", no_overflow, page, "AC85 1440px")  # after the scroll-through, on the full page
        name = "desktop-1440.png" if vp is DESKTOP else "mobile-390.png"
        heights[name] = guard("screenshots", bands, page, out / name, vp["width"])
        for b in bad_fonts:  # read last, so font files fetched during the scroll-through count too
            fail(f"AC63 web font request did not return 200 at {label}: {b}")
        ctx.close()

    def iframe_390():  # AC86: inside a width:390px iframe, as playbook §4 does it
        ctx, page = new_page(browser, DESKTOP)
        page.goto(f"{base}/profile/")
        page.set_content(f'<iframe src="{url}" style="width:390px;height:844px;border:0"></iframe>')
        page.frame_locator("iframe").locator("body").wait_for()
        inner = page.frames[1]
        inner.wait_for_load_state("networkidle")
        inner.wait_for_timeout(1500)
        settle(inner)
        no_overflow(inner, "AC86 390px iframe")
        ctx.close()
    guard("AC86", iframe_390)

    def motion(label, vp):  # AC84
        ctx, page = new_page(browser, vp, reduced_motion="reduce")
        page.goto(url, wait_until="networkidle")
        settle(page)
        reduced_motion(page, label)
        ctx.close()
    for label, vp in (("1440px", DESKTOP), ("390px", MOBILE)):
        guard(f"AC84 {label}", motion, label, vp)
    tree, dirty = tree_state(slug)
    lines = [f"slug {slug}", f"head {git('rev-parse', 'HEAD') or 'unknown'}", f"site tree {tree}",
             f"site working tree {dirty}", *(f"height {k} {v}" for k, v in heights.items()),
             f"thumb difference {tdiff}" if tdiff is not None else "thumb difference n/a",
             *(f"FAIL {f}" for f in fails), f"result {'PASS' if not fails else 'FAIL'}"]
    (out / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"screenshots for the reviews: {out}/desktop-1440*.png {out}/mobile-390*.png, summary {out / 'summary.txt'}")


def check_gallery(browser, base):  # AC89 AC90 AC92 AC93 AC94
    ctx, page = new_page(browser, DESKTOP)
    page.goto(f"{base}/profile/", wait_until="networkidle")
    page.click('.pf-filters button[data-filter="beauty"]')
    page.wait_for_timeout(300)
    shown = page.locator('a.pf-card[data-industry="beauty"]:visible')
    slugs = sorted(shown.nth(i).get_attribute("data-slug") for i in range(shown.count()))
    if slugs != sorted(SAMPLES):
        fail(f"AC89 beauty filter shows cards {slugs}, expected {sorted(SAMPLES)}")
    if page.locator('.pf-empty[data-industry="beauty"]:visible').count():
        fail("AC90 beauty filter still shows a 준비 중 tile")
    width = "document.getElementById('pf-v-iframe').getBoundingClientRect().width"
    for slug in SAMPLES:  # each card from a fresh load of /profile/, as a visitor arrives
        if slug not in slugs:
            continue
        page.goto(f"{base}/profile/", wait_until="networkidle")
        page.click('.pf-filters button[data-filter="beauty"]')
        page.wait_for_timeout(300)
        viewer, iframe = page.locator("#pf-viewer"), page.locator("#pf-v-iframe")
        page.locator(f'a.pf-card[data-slug="{slug}"]').click()
        page.wait_for_timeout(300)
        if not viewer.is_visible() or not (iframe.get_attribute("src") or "").endswith(f"/profile/{slug}/"):
            fail(f"AC92 clicking the {slug} card does not open the preview with that sample")
            continue
        try:  # the loaded document is this sample's page (slug match, not a name stem: 로빈헤어 is in 로빈헤어살롱)
            page.frame_locator("#pf-v-iframe").locator("header a.wordmark").first.wait_for(state="attached",
                                                                                            timeout=10000)
            next(f for f in page.frames if f.url.rstrip("/").endswith(f"/profile/{slug}"))
        except Exception:
            fail(f"AC92 {slug}: the preview iframe does not show that sample's page")
        for device, cond in (("mobile", "<= 400"), ("desktop", "> 600")):  # the width animates; wait for it
            page.click(f'button[data-device="{device}"]')
            try:
                page.wait_for_function(f"{width} {cond}", timeout=3000)
            except Exception:
                fail(f"AC93 {slug}: {device} button does not switch the preview width ({page.evaluate(width)})")
        page.keyboard.press("Escape")
        try:
            page.wait_for_function("document.getElementById('pf-viewer').hidden", timeout=3000)
        except Exception:
            fail(f"AC94 {slug}: Esc does not close the preview")
    ctx.close()


def check_trio(browser, base):  # AC154 AC155: h1 faces and wordmark faces differ pairwise across the three samples
    faces = {}
    for slug in SAMPLES:
        if not (ROOT / "profile" / slug / "index.html").is_file():
            fail(f"AC154 AC155 profile/{slug}/index.html does not exist")
            continue
        ctx, page = new_page(browser, DESKTOP)
        page.goto(f"{base}/profile/{slug}/", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        faces[slug] = (first_of(page, "h1"), first_of(page, "header a.wordmark"))
        ctx.close()
    for i, (ac, what) in enumerate((("AC154", "h1"), ("AC155", "header wordmark"))):
        got = {slug: f[i] for slug, f in faces.items()}
        for slug, fam in got.items():
            if not fam:
                fail(f"{ac} {slug}: no {what} to read a font family from")
        named = [f.lower() for f in got.values() if f]
        if len(set(named)) != len(named):
            fail(f"{ac} two samples share the {what}'s first font family: {got}")
    print("faces (h1, wordmark):", faces)


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
            if slug not in SAMPLES:  # the beauty samples' full pages are in <slug>/ from `page`
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
    shots = Path("/tmp/profile-beauty-shots")
    if "--shots" in args:
        i = args.index("--shots")
        if i + 1 >= len(args):
            raise SystemExit(__doc__)
        shots = Path(args[i + 1]).resolve()
        if shots == ROOT or ROOT in shots.parents:  # `page` empties DIR/<slug>/; never inside the repository
            raise SystemExit(f"--shots must be outside the repository: {shots}")
        del args[i:i + 2]
    if not args or args[0] not in ("page", "gallery", "trio", "compare") or \
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
