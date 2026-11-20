#!/usr/bin/env python3
"""Browser checks for the three crypto profile samples (Playwright + installed Google Chrome). Run from the
repository root.

usage: python3 docs/features/2026-11-20-profile-crypto/check_browser.py page <slug> | thumb <slug> | gallery | trio
       | compare [--shots DIR]
  page <slug>  AC8-AC10 AC12 AC31 AC32 AC34 AC40-AC43 AC58-AC60 AC99-AC101 AC131-AC134 AC147-AC149 AC253 AC254 AC260, and
               A (crypto-robincoin): AC79 AC83 AC152-AC158 AC160 AC161 AC163-AC166 AC173-AC175 AC177-AC186,
               B (crypto-robincustody): AC195-AC204 AC206-AC208 AC210-AC220 AC261,
               D (crypto-robinchain): AC226-AC240 AC242-AC247.
               Empties DIR/<slug>/ first, then writes full-page screenshots for the reviews (desktop-1440.png,
               mobile-390.png, and the same cut into 1200 px bands -NN.png) and summary.txt last.
  thumb <slug> AC5: thumb.jpg shows the sample's current 1440x900 first screen
  gallery      AC137 AC138 AC140 AC141 AC142 on /profile/
  trio         AC125 AC126 AC258 AC259 AC263: faces, wordmark centres and wordmark sizes differ pairwise
  compare      evidence for the reviews, not a check: rewrites DIR/compare/ with first screens (1440x900 and 390x844)
               of the three crypto samples and the fifteen shipped samples, full pages (and bands) of the fifteen
               shipped samples, the three thumb.jpg files, and of each reference site its first screen and full page
               at 1440 and its visible text (ref-<slug>.png, ref-<slug>-full.png and its -NN bands, ref-<slug>.txt; an
               HTTP error counts as no answer; the last good copy is kept when a site does not answer). summary.txt
               lists each local tree hash and each reference as ok, cached or unreachable. Exit 0 when every local
               screenshot was written.
DIR defaults to /tmp/profile-crypto-shots. Serves the repository root on a free local port itself and stops the
server when it ends.
The page contract these checks read is the "Fixed parameters" section of tasks.md in this folder.
AC numbers are this feature's spec.md.
"""
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import base64
import os
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
PRETENDARD = ("Pretendard Variable", "Pretendard")
SAMPLES = {
    "crypto-robincoin": {"key": "A", "ref": "https://www.coinbase.com/", "h1": PRETENDARD, "wm": PRETENDARD},
    "crypto-robincustody": {"key": "B", "ref": "https://copper.co/", "h1": ("Noto Sans KR", "Noto Serif KR"),
                            "wm": ("Noto Serif KR",)},
    "crypto-robinchain": {"key": "D", "ref": "https://www.kaia.io/", "h1": ("Gasoek One",), "wm": ("Gasoek One",)},
}
SHIPPED = ("flower-bomgyeol", "food-saebyeokmil", "clinic-neuru", "clinic-byeotteul", "clinic-bonui", "law-ganeum",
           "law-goim", "fitness-mideoum", "fitness-jjuuk", "beauty-robinhair", "beauty-robinsalon",
           "beauty-robinhairsalon", "interior-robininterior", "interior-robindesign", "interior-robinhome")
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
MARK_TAIL = "디자인 샘플 · 상호와 정보는 가상입니다"  # AC12
FICTION = "가상의 업체이며 가상자산사업자가 아닙니다. 실제 거래 · 보관 · 상담을 제공하지 않습니다."  # AC31 AC32
RISK = "가상자산은 가격 변동이 커서 원금의 전부 또는 일부를 잃을 수 있습니다."  # AC58
EXAMPLE = "예시 화면 · 실제 시세가 아닙니다"
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
KOREAN_FONT = re.compile(r"Pretendard|\bKR\b|Nanum|Gowun|Gothic A1|Hahmlet|Gasoek", re.I)
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
DEADLINE = 900  # seconds one run may take before it is a failure
THUMB_MAX_TILE = 40.0  # the same per 10x10-pixel tile of the 160x100 images (16 x 10 tiles), so a changed area shows
THUMB_MAX_DIFF = 15.0  # mean absolute RGB difference (0-255) at 160x100 between thumb.jpg and a fresh first screen
WHITE, INK_A, GREY_A, BLUE, RED = (255, 255, 255), (12, 18, 34), (238, 242, 247), (10, 105, 199), (200, 50, 60)
APRICOT, INK_B, PAPER, WINE = (245, 192, 138), (42, 29, 20), (255, 253, 249), (123, 35, 56)
PAGE_D, TEXT_D, CARD_D, LIME = (7, 9, 10), (242, 245, 238), (22, 26, 28), (169, 239, 44)
SVC, STEPS, CONTACT = "서비스|하는 일", "절차|과정|이용 방법", "문의|상담"
fails = []


def fail(msg):
    fails.append(msg)


def guard(label, fn, *args):  # a check that throws is one failure; the remaining checks and summary.txt still run
    try:
        return fn(*args)
    except Exception as exc:
        fail(f"{label}: the check stopped: {type(exc).__name__}: {(str(exc).splitlines() or [''])[0]}")
        return None


def serve():
    handler = partial(type("Quiet", (SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}),
                      directory=str(ROOT))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)  # port 0: a free port, so no clash with another server
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_port}"


def new_page(browser, vp, **kw):
    ctx = browser.new_context(viewport=vp, timezone_id="Asia/Seoul", **kw)
    return ctx, ctx.new_page()


def settle(target):
    """Wait for fonts, then scroll through once so reveal effects run."""
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

UNDER_BAR = """el => { const r = el.getBoundingClientRect();  // does a fixed or sticky element overlap any part of it?
  return [...document.body.querySelectorAll('*')].some(e => { if (e.contains(el) || !/fixed|sticky/.test(getComputedStyle(e).position)) return false;
    const b = e.getBoundingClientRect(); if (!b.width || !b.height || getComputedStyle(e).visibility === 'hidden') return false;
    return Math.min(r.right, b.right) - Math.max(r.left, b.left) > 1 && Math.min(r.bottom, b.bottom) - Math.max(r.top, b.top) > 1; }); }"""

# Helpers every page script below can call: installed once per page by lib().
LIB = """() => { window.__c = {
  inView: __IN_VIEW__,
  underBar: __UNDER_BAR__,
  rgba: v => { const m = (v || '').match(/^rgba?\\(([^)]+)\\)$/); if (!m) return null;
    const p = m[1].split(/[\\s,\\/]+/).filter(Boolean).map(parseFloat); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; },
  box: e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; },
  ext: e => { const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let b = null;  // the extent of the rendered text:
    for (let n; (n = w.nextNode());) { if (!n.nodeValue.trim()) continue;  // the union of the text nodes' line boxes, so
      const g = document.createRange(); g.selectNodeContents(n);  // neither the element's box nor a mark beside the text widens it
      for (const r of g.getClientRects()) { if (!r.width || !r.height) continue;
        b = b ? [Math.min(b[0], r.left), Math.min(b[1], r.top), Math.max(b[2], r.right), Math.max(b[3], r.bottom)] : [r.left, r.top, r.right, r.bottom]; } }
    return b || [0, 0, 0, 0]; },
  fam: e => getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/^['"]|['"]$/g, ''),
  own: e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('').replace(/\\s+/g, ' ').trim(),
  shown: e => { const s = getComputedStyle(e), r = e.getBoundingClientRect();
    return e.getClientRects().length > 0 && r.width > 1 && r.height > 1 && s.visibility !== 'hidden'; },
  uncut: e => { const r = e.getBoundingClientRect();  // not cut off by an ancestor that clips its overflow
    for (let a = e.parentElement; a; a = a.parentElement) { const s = getComputedStyle(a);
      if (s.overflowX === 'visible' && s.overflowY === 'visible') continue; const b = a.getBoundingClientRect();
      if (r.left < b.left - 1 || r.right > b.right + 1 || r.top < b.top - 1 || r.bottom > b.bottom + 1) return false; }
    return true; },
  plain: e => { const t = getComputedStyle(e);  // drawn as written: nothing that can hide or shrink the glyphs while
    if (t.webkitTextFillColor !== t.color) return false;  // the computed colour and font-size stay the same
    for (let a = e; a; a = a.parentElement) { const s = getComputedStyle(a);
      if (s.filter !== 'none' || s.transform !== 'none' || +s.zoom !== 1 || (s.scale && s.scale !== 'none')
          || (s.maskImage || s.webkitMaskImage || 'none') !== 'none' || s.mixBlendMode !== 'normal') return false; }
    return true; },
  whole: e => { const c = window.__c, x = c.ext(e), b = c.box(e), s = getComputedStyle(e);  // the text is all there: not cut by an
    if (!c.uncut(e) || x[2] - x[0] < 1 || x[0] < -1 || x[2] > innerWidth + 1) return false;  // overflow box, not pushed off the side
    const clips = s.overflowX !== 'visible' || s.overflowY !== 'visible';
    return !clips || (x[0] >= b[0] - 2 && x[2] <= b[2] + 2 && x[1] >= b[1] - 2 && x[3] <= b[3] + 2 && e.scrollWidth <= e.clientWidth + 1); },
  pinned: e => { for (; e; e = e.parentElement) if (/fixed|sticky/.test(getComputedStyle(e).position)) return true; return false; },
  sec: pat => { const re = new RegExp(pat); const hit = [...document.querySelectorAll('section[id]')].filter(s =>
      [...s.querySelectorAll('h2')].some(h => h.closest('section') === s && re.test(h.textContent)));
    return hit.length === 1 ? hit[0] : null; },
  radius: e => { const s = getComputedStyle(e), h = e.getBoundingClientRect().height;
    return [s.borderTopLeftRadius, s.borderTopRightRadius, s.borderBottomLeftRadius, s.borderBottomRightRadius]
      .map(v => { const p = v.split(' ')[0]; return p.endsWith('%') ? parseFloat(p) / 100 * h : parseFloat(p); }); },
  bg: el => { const layers = [], c = window.__c;  // the colour behind el: translucent layers composited down to the first opaque one
    for (let e = el; e; e = e.parentElement) for (const ps of ['::before', '::after']) { const s = getComputedStyle(e, ps);  // a painted
      if (s.content === 'none' || s.content === 'normal' || s.display === 'none') continue;  // ::before/::after of el or of an ancestor
      const k = c.rgba(s.backgroundColor);  // may lie under or over the text: not judged
      if (s.backgroundImage !== 'none' || !k || k[3] > 0)
        return {err: 'a background on ' + e.tagName.toLowerCase() + ps + ' of the element or of an ancestor'}; }
    for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e);
      if (s.backgroundImage !== 'none') return {err: 'a CSS background-image on <' + e.tagName.toLowerCase() + '> behind it'};
      const c = window.__c.rgba(s.backgroundColor); if (!c) return {err: 'unreadable background ' + s.backgroundColor};
      if (c[3] > 0) { layers.push(c); if (c[3] >= 1) break; } }
    let base = [255, 255, 255];
    for (const c of layers.reverse()) base = [0, 1, 2].map(i => c[i] * c[3] + base[i] * (1 - c[3]));
    return {c: base}; },
  bgAt: (x, y, skipPinned) => { for (const e of document.elementsFromPoint(x, y)) {  // the topmost painted background at a point
      if (skipPinned && window.__c.pinned(e)) continue; const s = getComputedStyle(e);
      if (s.backgroundImage !== 'none') return 'image ' + s.backgroundImage.slice(0, 30);
      const c = window.__c.rgba(s.backgroundColor); if (c && c[3] > 0) return c; }
    return null; },
  ratio: (fg, bg) => { const lum = v => { const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * f(v[0]) + 0.7152 * f(v[1]) + 0.0722 * f(v[2]); };
    const l1 = lum(fg), l2 = lum(bg); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); },
  contrast: e => { const c = window.__c, s = getComputedStyle(e), fg = c.rgba(s.color), bg = c.bg(e);  // {ratio} or {err}
    let o = 1; for (let x = e; x; x = x.parentElement) o *= +getComputedStyle(x).opacity;
    if (!fg || bg.err) return {err: bg.err || 'unreadable colour ' + s.color};
    const a = fg[3] * o, mix = [0, 1, 2].map(i => fg[i] * a + bg.c[i] * (1 - a));
    return {ratio: c.ratio(mix, bg.c), fg: mix.map(Math.round), bg: bg.c.map(Math.round)}; },
  info: e => { if (!e) return null; const s = getComputedStyle(e), c = window.__c;
    return {box: c.box(e), ext: c.ext(e), fs: parseFloat(s.fontSize), fam: c.fam(e), weight: +s.fontWeight, color: c.rgba(s.color),
      bg: c.rgba(s.backgroundColor), bgImage: s.backgroundImage, style: s.fontStyle, display: s.display, position: s.position,
      href: e.getAttribute && e.getAttribute('href'), text: e.textContent.replace(/\\s+/g, ' ').trim().slice(0, 40),
      shown: c.shown(e), radius: c.radius(e)}; },
  withText: (root, t) => [root, ...root.querySelectorAll('*')].filter(e => window.__c.own(e).includes(t)),
  first: () => { const c = window.__c, svc = c.sec('__SVC__'); if (!svc) return null;  // the first section, the <header> and bars aside
    return [...document.body.querySelectorAll('*')].filter(e => (svc.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_PRECEDING)
      && !e.contains(svc) && !e.closest('header') && !c.pinned(e)); },
  cover: () => { const c = window.__c, iv = [];  // px of viewport height under fixed elements and stuck sticky elements
    for (const e of document.body.querySelectorAll('*')) { const s = getComputedStyle(e);
      if (!/fixed|sticky/.test(s.position) || !c.shown(e)) continue; const r = e.getBoundingClientRect();
      let pin = s.position === 'fixed'; const t = parseFloat(s.top), b = parseFloat(s.bottom);
      if (!pin) pin = (!isNaN(t) && Math.abs(r.top - t) <= 1) || (!isNaN(b) && Math.abs(innerHeight - r.bottom - b) <= 1);
      const top = Math.max(0, r.top), bot = Math.min(innerHeight, r.bottom); if (pin && bot > top) iv.push([top, bot]); }
    iv.sort((a, b) => a[0] - b[0]); let sum = 0, end = -1;
    for (const [a, b] of iv) { if (b <= end) continue; sum += b - Math.max(a, end); end = b; }
    return sum; },
}; }""".replace("__IN_VIEW__", IN_VIEW).replace("__UNDER_BAR__", UNDER_BAR).replace("__SVC__", SVC)


def lib(target):
    target.evaluate(LIB)


def info(target, selector):  # box, text extent, font and colours of the first element matching selector, or None
    return target.evaluate("sel => window.__c.info(document.querySelector(sel))", selector)


def rgb(c):  # [r, g, b, a] -> (r, g, b) when opaque, else None
    return tuple(round(x) for x in c[:3]) if c and not isinstance(c, str) and c[3] >= 0.999 else None


def hexs(c):
    return "#%02x%02x%02x" % tuple(c)


def rnd(box):
    return [round(x) for x in box]


def want_color(ac, what, got, *want):  # got: [r, g, b, a] from the page
    if rgb(got) not in want:
        fail(f"{ac} {what} is {got}, expected {' or '.join(hexs(w) for w in want)}")


def want_face(ac, what, got, *faces):
    if got not in faces:
        fail(f"{ac} {what} has computed first font family {got!r}, not {' or '.join(repr(f) for f in faces)}")


def is_pill(x):  # border-radius at least half the rendered height
    return min(x["radius"]) >= (x["box"][3] - x["box"][1]) / 2 - 0.5


def want_pill(ac, what, x):
    if not is_pill(x):
        fail(f"{ac} {what} has a border-radius of {min(x['radius']):.1f}px, below half its height {x['box'][3] - x['box'][1]:.0f}px")


def inside_viewport(box, W, H):
    return box[0] >= -0.5 and box[1] >= -0.5 and box[2] <= W + 0.5 and box[3] <= H + 0.5


def size(page):
    return page.evaluate("[document.documentElement.clientWidth, innerHeight]")


def section_id(page, pat):
    return page.evaluate("pat => { const s = window.__c.sec(pat); return s ? s.id : null; }", pat)


# --- common checks -----------------------------------------------------------------------------------------

EVERYWHERE = """async ([kind, arg]) => { const c = window.__c;  // scroll positions (every 40 px) at which none is on screen
  const els = kind === 'text' ? c.withText(document.body, arg)
    : [...document.querySelectorAll('a[href="#' + arg + '"]')].filter(a => /문의|상담/.test(a.textContent));
  const H = document.documentElement.scrollHeight, miss = [];
  for (let y = 0; ; y += 40) { const t = Math.max(0, Math.min(y, H - innerHeight)); scrollTo({top: t, behavior: 'instant'});
    let ok = false;
    for (let i = 0; i < 15 && !ok; i++) { await new Promise(r => requestAnimationFrame(() => r())); ok = els.some(e => c.inView(e) && c.whole(e) && (kind !== 'text' || c.plain(e)));
      if (!ok) await new Promise(r => setTimeout(r, 100)); }  // up to 1.5 s for a bar that slides in
    if (!ok) miss.push(t); if (t >= H - innerHeight) break; }
  const solid = e => { for (let x = e; x; x = x.parentElement) { const s = getComputedStyle(x), k = c.rgba(s.backgroundColor);
      if (k && k[3] >= 0.999) return true; if (/fixed|sticky/.test(s.position)) return false; } return false; };  // AC12
  const bare = els.filter(e => c.inView(e) && c.pinned(e) && !solid(e)).length;
  const end = els.filter(e => c.inView(e) && (kind !== 'text' || c.plain(e))).map(e => parseFloat(getComputedStyle(e).fontSize));
  scrollTo({top: 0, behavior: 'instant'}); await new Promise(r => requestAnimationFrame(() => r()));
  return {n: els.length, miss, bare, top: els.filter(e => c.inView(e) && (kind !== 'text' || c.plain(e))).map(e => parseFloat(getComputedStyle(e).fontSize)), end}; }"""

LAST_FOOTER_TEXT = """() => { const f = [...document.querySelectorAll('footer')].pop(); if (!f) return null;
  return [f, ...f.querySelectorAll('*')].filter(e => e.getClientRects().length && !window.__c.pinned(e) && window.__c.own(e)).pop() || null; }"""


def marker(page, vp, label):  # AC8 AC9 AC10, then AC12 AC147
    ac = "AC8" if vp is DESKTOP else "AC9"
    sizes = page.evaluate("""t => window.__c.withText(document.body, t).filter(e => window.__c.inView(e) && window.__c.whole(e) && window.__c.plain(e))
        .map(e => [parseFloat(getComputedStyle(e).fontSize), parseFloat(getComputedStyle(document.body).fontSize)])""", MARK)
    if not sizes:
        fail(f"{ac} the sample marker '{MARK}' is not visible without scrolling at {label}")
    elif not any(fs >= body and fs >= 14 for fs, body in sizes):
        fail(f"AC10 the first-screen sample marker is set at {sizes[0][0]}px, below the body size {sizes[0][1]}px or 14px, at {label}")
    r = page.evaluate(EVERYWHERE, ["text", MARK_TAIL])
    if r["miss"]:
        fail(f"AC12 no element with '{MARK_TAIL}' is on screen at scroll {r['miss'][:5]} px ({len(r['miss'])} positions) at {label}")
    if r["bare"]:
        fail(f"AC12 the marker that stays on screen has no opaque background colour on itself or between it and its fixed or "
             f"sticky ancestor at {label}: what scrolls under it shows through the text")
    for where, got in (("scroll position 0", r["top"]), ("the end of the page", r["end"])):
        if not got or max(got) < 14:
            fail(f"AC147 the marker that stays on screen is set at {got}px at {where}, below 14px, at {label}")


def sentence_first_screen(page, label):  # AC32 AC148, A and B
    sizes = page.evaluate("t => window.__c.withText(document.body, t).filter(e => window.__c.inView(e) && window.__c.whole(e) && window.__c.plain(e)).map(e => parseFloat(getComputedStyle(e).fontSize))", FICTION)
    if not sizes:
        fail(f"AC32 the sentence '{FICTION}' is not visible without scrolling at {label}")
    elif max(sizes) < 14:
        fail(f"AC148 the first-screen sentence of AC32 is set at {max(sizes)}px, below 14px, at {label}")


def sentences(page, label):  # AC31 (visible in the contact section, 14 px) AC58 (visible in the footer) AC59 AC60
    r = page.evaluate("""async ([fiction, risk, pat]) => { const c = window.__c, out = {};
      const seen = async e => { e.scrollIntoView({block: 'center', behavior: 'instant'});
        for (let i = 0; i < 15; i++) { await new Promise(r => requestAnimationFrame(() => r())); if (c.inView(e) && c.whole(e) && c.plain(e)) return true;
          await new Promise(r => setTimeout(r, 100)); } return false; };
      const con = c.sec(pat), foot = [...document.querySelectorAll('footer')].pop();
      out.fiction = []; for (const e of con ? c.withText(con, fiction) : []) if (await seen(e)) out.fiction.push(parseFloat(getComputedStyle(e).fontSize));
      out.foot = false; for (const e of foot ? c.withText(foot, risk) : []) if (await seen(e)) out.foot = true;
      out.risk = c.withText(document.body, risk).filter(c.shown).map(e => [parseFloat(getComputedStyle(e).fontSize), c.contrast(e)]);
      scrollTo({top: 0, behavior: 'instant'}); return out; }""", [FICTION, RISK, CONTACT])
    if not r["fiction"]:
        fail(f"AC31 the sentence '{FICTION}' is not visible in the contact section at {label}")
    elif max(r["fiction"]) < 14:
        fail(f"AC31 the sentence '{FICTION}' in the contact section is set at {max(r['fiction'])}px, below 14px, at {label}")
    if not r["foot"]:
        fail(f"AC58 the sentence '{RISK}' is not visible in the footer at {label}")
    for fs, con in r["risk"]:
        if fs < 13:
            fail(f"AC59 the sentence of AC58 is set at {fs}px, below 13px, at {label}")
        if con.get("err") or con["ratio"] < 4.5:
            fail(f"AC60 the sentence of AC58 has a contrast of {con.get('err') or round(con['ratio'], 2)} (text {con.get('fg')} on "
                 f"{con.get('bg')}), below 4.5:1, at {label}")


def contact_link(page, vp, sid, label):  # AC40 AC41, and at 390 AC42 AC43
    seen = page.evaluate("""sid => [...document.querySelectorAll('a[href="#' + sid + '"]')]
        .filter(a => /문의|상담/.test(a.textContent)).some(window.__c.inView)""", sid)
    if not seen:
        fail(f"{'AC40' if vp is DESKTOP else 'AC41'} no link to the contact section whose text contains 문의 or 상담 is "
             f"visible without scrolling at {label}")
    if vp is DESKTOP:
        return
    r = page.evaluate(EVERYWHERE, ["link", sid])
    if r["miss"]:
        fail(f"AC42 no 문의 · 상담 link to the contact section is on screen at scroll {r['miss'][:5]} px "
             f"({len(r['miss'])} positions) at 390px")
    page.evaluate("scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    last = page.evaluate_handle(LAST_FOOTER_TEXT).as_element()
    for _ in range(15):  # up to 1.5 s for a footer that fades or slides in
        if not last or last.evaluate(IN_VIEW):
            break
        page.wait_for_timeout(100)
    if not last:
        fail("AC43 no <footer> text to read at the end of the page (390px)")
    elif not last.evaluate(IN_VIEW) or last.evaluate(UNDER_BAR):
        fail(f"AC43 the footer's last text line is covered or off screen at the end of the page (390px): "
             f"{last.evaluate('e => e.textContent.trim().slice(0, 40)')}")
    page.evaluate("scrollTo(0, 0)")


def bars(page):  # AC149, at 390
    r = page.evaluate("""async () => { const out = [], H = document.documentElement.scrollHeight;
      for (const y of [0, Math.max(0, (H - innerHeight) / 2)]) { scrollTo({top: y, behavior: 'instant'});
        await new Promise(r => setTimeout(r, 400)); out.push([Math.round(y), window.__c.cover()]); }
      scrollTo({top: 0, behavior: 'instant'}); return out; }""")
    for y, px in r:
        if px > 220:
            fail(f"AC149 fixed and sticky elements cover {px:.0f}px of the 390px screen's height at scroll {y}px, above 220px")


def no_overflow(target, label):  # AC133 AC134
    w = target.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    if w[0] > w[1]:
        fail(f"{label} horizontal overflow: scrollWidth {w[0]} > clientWidth {w[1]}")
    wide = target.evaluate("""() => { const W = document.documentElement.clientWidth, out = [];  // overflow-x on <html>/<body> hides it, not removes it
      for (const e of document.body.querySelectorAll('*')) { const r = e.getBoundingClientRect();
        if (r.width < 1 || r.height < 1 || r.right <= W + 1 || getComputedStyle(e).visibility === 'hidden') continue;
        let cut = false;
        for (let a = e.parentElement; a && a !== document.body; a = a.parentElement)
          if (getComputedStyle(a).overflowX !== 'visible' && a.getBoundingClientRect().right <= W + 1) { cut = true; break; }
        if (!cut) out.push('<' + e.tagName.toLowerCase() + (e.className && e.className.baseVal === undefined ? '.' + e.className : '') + '> to ' + Math.round(r.right) + 'px'); }
      return out.slice(0, 5); }""")
    if wide:
        fail(f"{label} elements reach past the right edge of the {w[1]}px page (overflow-x on html or body only hides them): {wide}")


def keep_all(page, label):  # AC34, both widths
    bad = page.evaluate("""() => [...document.querySelectorAll('p, li, dd, dt, td, th, h1, h2, h3')]
      .filter(e => /[가-힣]/.test(e.textContent) && getComputedStyle(e).wordBreak !== 'keep-all')
      .map(e => e.textContent.trim().slice(0, 40))""")
    for t in bad[:8]:
        fail(f"AC34 Korean text without word-break: keep-all at {label}: {t}")


def digit_fonts(page, label):  # AC100: digits of hours, phone numbers and example figures in a Korean or monospaced face
    texts = page.evaluate("""() => { let n = 0; const texts = [], re = /\\d{1,2}:\\d{2}|0\\d{1,2}-\\d{3,4}-\\d{4}|\\d\\s*원|\\d\\s*%/;
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
        fail(f"AC100 no visible 상담 hours or phone number found at {label}")
        return
    widths = page.evaluate("""n => [...Array(n).keys()].map(i => [...document.querySelector(`[data-digit-probe="${i}"]`)
      .querySelectorAll('[data-digit-char]')].map(s => s.getBoundingClientRect().width))""", len(texts))
    cdp = page.context.new_cdp_session(page)
    try:
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
                fail(f"AC100 digits rendered in {main!r}, neither Korean nor monospaced, at {label}: {texts[i]}")
    finally:
        page.evaluate("document.querySelectorAll('[data-digit-probe]').forEach(p => p.remove())")
        cdp.detach()


def font_responses(page):  # AC99: every web font request returns 200
    bad = []
    page.on("response", lambda r: any(h in r.url for h in FONT_HOSTS) and r.status != 200
            and bad.append(f"{r.status} {r.url}"))
    page.on("requestfailed", lambda r: any(h in r.url for h in FONT_HOSTS) and bad.append(f"failed {r.url}"))
    return bad


def web_font(page, selector, what, faces):  # AC99: the text renders in the sample's faces, loaded as web fonts
    cdp = page.context.new_cdp_session(page)
    try:
        cdp.send("DOM.enable")
        cdp.send("CSS.enable")
        root = cdp.send("DOM.getDocument", {"depth": -1})["root"]["nodeId"]
        nodes = cdp.send("DOM.querySelectorAll", {"nodeId": root, "selector": f"{selector}, {selector} *"})["nodeIds"]
        fonts = [f for n in nodes for f in cdp.send("CSS.getPlatformFontsForNode", {"nodeId": n})["fonts"] if f["glyphCount"]]
        bad = sorted({f["familyName"] + ("" if f.get("isCustomFont") else " (not a web font)") for f in fonts
                      if not f.get("isCustomFont") or not f["familyName"].startswith(faces)})
        if not fonts or bad:
            fail(f"AC99 the {what} renders in {bad or 'no font'}, not only in the loaded web font {' / '.join(faces)} "
                 f"(a face did not load, a fallback drew some of the text, or a copy installed on the machine was used)")
    finally:
        cdp.detach()


def reduced_motion(page, label):  # AC131
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
        fail(f"AC131 under prefers-reduced-motion at {label}: {b}")


def faces(page, label):  # AC101 AC253 AC254
    fam = page.evaluate("window.__c.fam(document.body)")
    want_face("AC101", f"the <body> at {label}", fam, *PRETENDARD)
    loaded = page.evaluate("[...document.fonts].map(f => f.family.replace(/^['\"]|['\"]$/g, ''))")
    if fam in PRETENDARD and fam not in loaded:  # the name of a copy installed on this machine: a visitor gets a fallback
        fail(f"AC101 the <body> family {fam!r} is not a family the linked stylesheets define at {label} "
             f"(they define {sorted(set(loaded))[:6]}); start the stack with the loaded name")
    bad = page.evaluate("""() => [...document.body.querySelectorAll('*')].filter(e => window.__c.fam(e) === 'Gasoek One'
        && getComputedStyle(e).fontWeight !== '400' && e.getClientRects().length)
      .map(e => e.tagName.toLowerCase() + ' ' + e.textContent.trim().slice(0, 20) + ' at weight ' + getComputedStyle(e).fontWeight).slice(0, 10)""")
    for b in bad:
        fail(f"AC253 an element in Gasoek One is not font-weight 400 at {label}: {b}")
    rows = page.evaluate("""pat => { const s = window.__c.sec(pat); if (!s) return null; const out = [];
      const walk = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
      while (walk.nextNode()) { const t = walk.currentNode;
        if (/\\d{1,2}:\\d{2}|0\\d{1,2}-\\d{3,4}-\\d{4}/.test(t.nodeValue) && t.parentElement.getClientRects().length)
          out.push([t.nodeValue.trim().slice(0, 40), window.__c.fam(t.parentElement)]); }
      return out; }""", CONTACT)
    if not rows:
        fail(f"AC254 no visible 상담 hours or phone number in the contact section at {label}")
    for text, fam in rows or []:
        if fam not in PRETENDARD or fam not in loaded:
            fail(f"AC254 {text!r} in the contact section has computed first family {fam!r}, not a loaded Pretendard, at {label}")


def contrast(page, label):  # AC132, on the whole page
    bad = page.evaluate("""() => { const c = window.__c, out = [];
      for (const e of document.body.querySelectorAll('*')) {
        if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(e.tagName) || e.closest('svg') || !c.own(e) || !c.shown(e)) continue;
        let o = 1; for (let x = e; x; x = x.parentElement) o *= +getComputedStyle(x).opacity;
        if (o === 0) continue;
        const r = c.contrast(e), fs = parseFloat(getComputedStyle(e).fontSize), need = fs >= 24 ? 3 : 4.5;
        const tag = e.tagName.toLowerCase() + ' ' + JSON.stringify(c.own(e).slice(0, 24));
        if (r.err) out.push(tag + ': cannot judge, ' + r.err);
        else if (r.ratio < need) out.push(tag + ': contrast ' + r.ratio.toFixed(2) + ':1 below ' + need + ':1 (text ' + r.fg + ' on ' + r.bg + ', ' + fs + 'px)');
      }
      return out.slice(0, 15); }""")
    for b in bad:
        fail(f"AC132 at {label}: {b}")


def h1_side(page, key):  # AC260
    W, _ = size(page)
    h1 = info(page, "h1")
    if not h1:
        fail("AC260 no <h1>")
        return
    centre = (h1["ext"][0] + h1["ext"][2]) / 2
    if (centre <= W / 2) if key == "A" else (centre >= W / 2):
        fail(f"AC260 the <h1> text's horizontal centre is at {centre:.0f}px; it must be in the "
             f"{'right' if key == 'A' else 'left'} half of the {W}px viewport")


FIRST_LINKS = """() => { const c = window.__c, f = c.first(); if (!f) return null;
  return f.filter(e => e.tagName === 'A' && c.shown(e) && !e.closest('[data-example]')).map(c.info); }"""
FIRST_SVGS = """inLinks => { const c = window.__c, f = c.first(); if (!f) return null;  // B counts an <svg> inside a link too (AC211); D does not (AC239)
  return f.filter(e => e.tagName.toLowerCase() === 'svg' && e.getAttribute('aria-hidden') === 'true' && (inLinks || !e.closest('a')) && !e.closest('[data-example]'))
    .map(e => ({box: c.box(e), shown: c.shown(e)})); }"""


def first_links(page, ac):
    links = page.evaluate(FIRST_LINKS)
    if links is None:
        fail(f"{ac} no single service section, so the first section cannot be read")
    return links


def h1_on_load(page, ac, min_fs, label):  # the <h1> is at least min_fs, fully inside the viewport and not under a bar
    W, H = size(page)
    h1 = info(page, "h1")
    ok = h1 and page.locator("h1").first.evaluate(IN_VIEW) and not page.locator("h1").first.evaluate(UNDER_BAR)
    if not h1 or h1["fs"] < min_fs or not inside_viewport(h1["box"], W, H) or not ok:
        fail(f"{ac} at {label} the <h1> must be set at {min_fs}px or more (is {h1 and h1['fs']}px), lie fully inside the "
             f"viewport on load and not be covered by a fixed or sticky element (box {h1 and rnd(h1['box'])})")


def stacked(boxes):  # one column: each box starts at or below the bottom of the one before
    return all(b[1] >= a[3] - 1 for a, b in zip(boxes, boxes[1:]))


# --- sample A ----------------------------------------------------------------------------------------------

A_BLOCKS = """() => { const c = window.__c;
  return [...document.querySelectorAll('[data-example]')].map(b => { const phones = [...b.querySelectorAll('.phone')];
    const notes = c.withText(b, %r);
    return {box: c.box(b), radius: c.radius(b), bg: c.rgba(getComputedStyle(b).backgroundColor), bgImage: getComputedStyle(b).backgroundImage,
      imgs: b.querySelectorAll('img').length, phones: phones.map(c.info),
      risk: [...c.withText(b, %r), ...(b.nextElementSibling ? c.withText(b.nextElementSibling, %r) : [])].filter(e => c.shown(e) && c.whole(e) && c.plain(e)).length,
      notes: notes.map(n => ({box: c.box(n), fs: parseFloat(getComputedStyle(n).fontSize), seen: c.inView(n) && c.whole(n) && c.plain(n), whole: c.whole(n) && c.plain(n), inPhone: !!n.closest('.phone')})),
      changes: [b, ...b.querySelectorAll('*')].filter(e => c.own(e).endsWith('%%')).map(e => [c.own(e), c.rgba(getComputedStyle(e).color)]),
      digits: [b, ...b.querySelectorAll('*')].filter(e => /\\d/.test(c.own(e)) && c.shown(e))
        .map(e => [c.own(e).slice(0, 20), c.fam(e), getComputedStyle(e).fontVariantNumeric]),
      pointers: [b, ...b.querySelectorAll('*')].filter(e => getComputedStyle(e).cursor === 'pointer' || e.tagName === 'A' || e.hasAttribute('tabindex'))
        .map(e => e.tagName.toLowerCase() + ' ' + e.textContent.trim().slice(0, 20)),
      band: (() => { for (let e = b.parentElement; e; e = e.parentElement) { const r = c.box(e), g = c.rgba(getComputedStyle(e).backgroundColor);
        if (g && g[3] >= 1 && r[0] <= 1 && r[2] >= document.documentElement.clientWidth - 1) return g; } return null; })()}; }); }""" % (EXAMPLE, RISK, RISK)

A_PHONE_TOP = """() => { const c = window.__c, p = document.querySelector('[data-example] .phone'); if (!p) return null;
  const els = [...p.querySelectorAll('*')].filter(e => c.own(e) && c.shown(e));
  const sizes = els.map(e => parseFloat(getComputedStyle(e).fontSize)), max = Math.max(...sizes);
  const top = els.filter((e, i) => sizes[i] === max);
  return {count: top.length, text: c.own(top[0]), before: els.indexOf(top[0]) > 0 ? c.own(els[els.indexOf(top[0]) - 1]) : null, fs: max}; }"""

A_DARK = """pat => { const c = window.__c, s = c.sec(pat), ol = s && s.querySelector('ol'); if (!ol) return null;
  for (let e = ol.parentElement; e && e !== document.body; e = e.parentElement) { const g = c.rgba(getComputedStyle(e).backgroundColor);
    if (g && g[3] >= 1 && g.slice(0, 3).join() === '12,18,34' && Math.min(...c.radius(e)) >= 32)
      return {box: c.box(e), examples: e.querySelectorAll('[data-example]').length, svgs: e.querySelectorAll('svg').length,
        digit: /\\d/.test(e.textContent)}; }
  return {none: true}; }"""


def a_blocks(page, label):  # AC79 AC83 (displayed) AC164 (size), both widths
    blocks = page.evaluate(A_BLOCKS)
    for i, b in enumerate(blocks):
        what = "the panel" if i == 0 else "the asset card"
        ok = [n for n in b["notes"] if n["whole"] and n["fs"] >= 12 and n["box"][0] >= b["box"][0] - 1 and n["box"][2] <= b["box"][2] + 1
              and n["box"][1] >= b["box"][1] - 1 and n["box"][3] <= b["box"][3] + 1]
        if not ok:
            fail(f"AC79 the text '{EXAMPLE}' of {what} is not set at 12px or more inside the block's box at {label} "
                 f"(found {[(n['fs'], rnd(n['box'])) for n in b['notes']]}, block {rnd(b['box'])})")
        if not b["risk"]:
            fail(f"AC83 the sentence '{RISK}' is not displayed, uncut by an overflow box, inside {what} or in the element "
                 f"directly after it at {label}")
    if blocks and not any(n["inPhone"] and n["whole"] and n["fs"] >= 13 for n in blocks[0]["notes"]):
        fail(f"AC164 the text '{EXAMPLE}' inside the phone is not set at 13px or more at {label}")
    return blocks


def a_desktop(page, sid):  # AC152-AC157 AC160 AC161 AC163 AC165 AC166 AC173-AC175 AC177-AC181 AC184-AC186
    W, H = size(page)
    head, wm, h1 = (info(page, s) for s in ("header", "header a.wordmark", "h1"))
    if not head or not wm or not h1:
        fail("AC152-AC181 a <header>, its a.wordmark or the <h1> is missing")
        return
    if not rgb(head["bg"]) or min(rgb(head["bg"])) < 0xF8 or head["box"][0] > 1 or head["box"][2] < W - 1:
        fail(f"AC152 the <header> (background {head['bg']}, box {rnd(head['box'])}) must be opaque with every channel at "
             f"least 0xF8 and span the full viewport width")
    if wm["ext"][0] > 64:
        fail(f"AC153 the wordmark text's left edge is at {wm['ext'][0]:.0f}px, more than 64px from the left")
    want_face("AC154", "the header wordmark", wm["fam"], *PRETENDARD)
    if not 23 <= wm["fs"] <= 25 or wm["weight"] < 700:
        fail(f"AC154 the header wordmark is set at {wm['fs']}px, weight {wm['weight']}; it needs 23-25px and 700 or more")
    links = page.evaluate("[...document.querySelectorAll('header a')].filter(window.__c.shown).map(window.__c.info)")
    pills = []
    for word in ("로그인", "회원가입"):
        hit = [x for x in links if x["text"] == word]
        if len(hit) != 1 or hit[0]["href"] != "#":
            fail(f"AC155 the <header> needs exactly one link with the text '{word}' and href '#' (found {len(hit)})")
            continue
        want_color("AC155", f"the '{word}' link's background", hit[0]["bg"], GREY_A)
        want_color("AC155", f"the '{word}' link's colour", hit[0]["color"], INK_A)
        pills.append((word, hit[0]))
    ask = [x for x in links if x["href"] == f"#{sid}" and "문의" in x["text"] and rgb(x["bg"]) == BLUE and rgb(x["color"]) == WHITE]
    if not ask:
        fail(f"AC156 the <header> has no link to #{sid} whose text contains 문의 with the background #0a69c7 and the colour #ffffff")
    else:
        if any(x["box"][2] > ask[0]["box"][2] + 0.5 for x in links):
            fail(f"AC156 a header link has its right edge further right than the 문의 link ({ask[0]['box'][2]:.0f}px)")
        pills.append(("문의", ask[0]))
    for word, x in pills:
        want_pill("AC157", f"the header '{word}' link", x)
    blocks = page.evaluate(A_BLOCKS)
    if len(blocks) != 2:
        fail(f"AC159 expected two example blocks, found {len(blocks)}; the panel and asset card checks did not run")
        return
    panel, card = blocks
    b = panel["box"]
    if not inside_viewport(b, W, H) or b[0] > 144 or not 480 <= b[2] - b[0] <= 660 or not 480 <= b[3] - b[1] <= 720:
        fail(f"AC160 the panel {rnd(b)} must lie inside the viewport, start within 144px of the left edge and be "
             f"480-660px wide and 480-720px high")
    if min(panel["radius"]) < 32 or "linear-gradient" not in panel["bgImage"] or panel["imgs"]:
        fail(f"AC161 the panel needs a border-radius of 32px or more (is {min(panel['radius'])}), a linear-gradient "
             f"background-image ({panel['bgImage'][:40]}) and no <img>")
    if len(panel["phones"]) != 1:
        fail(f'AC163 the panel needs exactly one element with class "phone", found {len(panel["phones"])}')
    else:
        p = panel["phones"][0]
        pb = p["box"]
        if min(p["radius"][:2]) < 28 or not rgb(p["bg"]) or min(rgb(p["bg"])) < 0xF4 or not 280 <= pb[2] - pb[0] <= 400 \
                or pb[0] < b[0] or pb[2] > b[2] or pb[1] < b[1] + 24:
            fail(f"AC163 the phone (box {rnd(pb)}, top radii {p['radius'][:2]}, background {p['bg']}) needs top corners of "
                 f"28px or more, an opaque background with every channel at least 0xF4, a width of 280-400px, both side "
                 f"edges inside the panel {rnd(b)} and a top edge 24px or more below the panel's")
        if not any(n["inPhone"] and n["seen"] for n in panel["notes"]):
            fail(f"AC165 the text '{EXAMPLE}' inside the phone is not visible without scrolling at 1440px")
        top = page.evaluate(A_PHONE_TOP)
        if not top or top["count"] != 1 or not re.fullmatch(r"\d[\d,]*원", top["text"]) or top["before"] != "예시 자산 A":
            fail(f"AC166 the largest text in the phone must be one element whose own text is a number and 원, directly "
                 f"after '예시 자산 A' (found {top})")
    for blk, what in ((panel, "the panel"), (card, "the asset card")):
        for text, colour in blk["changes"]:
            want = RED if text.startswith("+") else BLUE
            if rgb(colour) != want:
                fail(f"AC173 the change figure {text!r} of {what} has the colour {colour}, expected {hexs(want)}")
        for text, fam, variant in blk["digits"]:
            if fam not in PRETENDARD or "tabular-nums" not in variant:
                fail(f"AC174 {text!r} in {what} has first family {fam!r} and font-variant-numeric {variant!r}; it needs "
                     f"Pretendard and tabular-nums")
        for t in blk["pointers"]:
            fail(f"AC175 {what} holds a link, a tabindex or a pointer cursor: {t}")
    if h1["ext"][0] < b[2] + 40 or not inside_viewport(h1["box"], W, H):
        fail(f"AC177 the <h1> (text from {h1['ext'][0]:.0f}px, box {rnd(h1['box'])}) must start 40px or more right of the "
             f"panel ({b[2]:.0f}px) and lie fully inside the viewport")
    want_face("AC178", "the <h1>", h1["fam"], *PRETENDARD)
    want_color("AC178", "the <h1>'s colour", h1["color"], INK_A)
    if not 56 <= h1["fs"] <= 80 or not 600 <= h1["weight"] <= 800:
        fail(f"AC178 the <h1> is set at {h1['fs']}px, weight {h1['weight']}; it needs 56-80px and 600-800")
    lines = (h1["box"][3] - h1["box"][1]) / h1["fs"]
    if not 1.9 <= lines <= 2.9:
        fail(f"AC179 the <h1> box is {lines:.2f} x its font-size high, not 1.9-2.9 (two lines)")
    svc = section_id(page, SVC)
    links = first_links(page, "AC180") or []
    got = sorted((x["text"], x["href"]) for x in links)
    if got != sorted([("고객센터 문의", f"#{sid}"), ("서비스 보기", f"#{svc}")]):
        fail(f"AC180 the first section must hold exactly two links outside the bars and the panel: '고객센터 문의' to "
             f"#{sid} and '서비스 보기' to #{svc} (found {got})")
    for x in (x for x in links if x["text"] == "고객센터 문의"):
        want_color("AC181", "the '고객센터 문의' link's background", x["bg"], BLUE)
        want_color("AC181", "the '고객센터 문의' link's colour", x["color"], WHITE)
        want_pill("AC181", "the '고객센터 문의' link", x)
    dark = page.evaluate(A_DARK, STEPS)
    if not dark or dark.get("none"):
        fail("AC184 no element with the background #0c1222 and a border-radius of 32px or more holds the <ol> of the steps section")
    else:
        if dark["box"][0] < 24 or W - dark["box"][2] < 24:
            fail(f"AC184 the dark panel {rnd(dark['box'])} needs a gap of 24px or more to each side of the viewport")
        if dark["examples"] or dark["svgs"] or dark["digit"]:
            fail(f"AC185 the dark panel holds an example block ({dark['examples']}), an <svg> ({dark['svgs']}) or a digit "
                 f"in its text ({dark['digit']})")
    if rgb(card["bg"]) != WHITE or min(card["radius"]) < 24 or rgb(card["band"]) != GREY_A:
        fail(f"AC186 the asset card needs the background #ffffff (is {card['bg']}), a border-radius of 24px or more (is "
             f"{min(card['radius'])}) and a full-width band behind it with the background #eef2f7 (is {card['band']})")


def a_mobile(page, sid):  # AC158 AC182 AC183
    seen = page.evaluate("""sid => [...document.querySelectorAll('header a[href="#' + sid + '"]')]
        .filter(a => /문의/.test(a.textContent)).some(window.__c.inView)""", sid)
    if not seen:
        fail("AC158 the header 문의 link is not visible without scrolling at 390px")
    h1_on_load(page, "AC182", 32, "390px")
    h1 = info(page, "h1")
    blocks = page.evaluate(A_BLOCKS)
    if not blocks or not h1 or len(blocks[0]["phones"]) != 1:
        fail("AC183 the panel, its phone or the <h1> is missing at 390px")
        return
    b, p = blocks[0]["box"], blocks[0]["phones"][0]["box"]
    if b[1] < h1["box"][3] - 0.5 or b[1] > 720 or b[2] - b[0] < 300 or p[2] - p[0] < 240:
        fail(f"AC183 at 390px the panel {rnd(b)} must come below the <h1> (bottom {h1['box'][3]:.0f}px), start at most "
             f"720px down, be 300px wide or more and hold a phone 240px wide or more (is {p[2] - p[0]:.0f}px)")


# --- sample B ----------------------------------------------------------------------------------------------

NO_BG_IMAGE = """() => { const c = window.__c, out = [];
  for (const e of [document.documentElement, document.body, ...document.body.querySelectorAll('*')]) { const r = c.box(e);
    if (!c.shown(e) || r[1] >= innerHeight || r[3] <= 0 || r[0] >= innerWidth || r[2] <= 0) continue;
    for (const ps of [null, '::before', '::after']) if (getComputedStyle(e, ps).backgroundImage !== 'none'
        && (!ps || getComputedStyle(e, ps).content !== 'none'))
      out.push(e.tagName.toLowerCase() + (ps || '') + ' ' + getComputedStyle(e, ps).backgroundImage.slice(0, 40)); }
  return out.slice(0, 6); }"""

B_DRAWING = """() => { const c = window.__c, f = c.first(); if (!f) return null;
  const svg = f.find(e => e.tagName.toLowerCase() === 'svg' && e.getAttribute('aria-hidden') === 'true'); if (!svg) return null;
  return {shapes: [...svg.querySelectorAll('path, rect, line, polygon, polyline, circle')].map(e => { const s = getComputedStyle(e);
      return {tag: e.tagName.toLowerCase(), fill: s.fill, stroke: s.stroke, w: e.getBoundingClientRect().width}; }),
    bad: [...svg.querySelectorAll('ellipse, text')].map(e => e.tagName.toLowerCase())}; }"""


def b_common(page, label):  # AC195 AC196, both widths
    W, H = size(page)
    for t in page.evaluate(NO_BG_IMAGE):
        fail(f"AC195 an element with a background-image is on the first screen at {label}: {t}")
    r = page.evaluate("""pat => { const c = window.__c, s = c.sec(pat), W = document.documentElement.clientWidth, H = innerHeight;
      return {top: s ? c.box(s)[1] : null, pts: [[4, H / 2], [W - 4, H / 2], [4, H - 4], [W - 4, H - 4]].map(p => c.bgAt(p[0], p[1], true))}; }""", SVC)
    if r["top"] is None or r["top"] < H - 0.5:
        fail(f"AC196 the first section ends at {r['top']}px, above the bottom of the {H}px viewport, at {label}")
    if any(rgb(p) != APRICOT for p in r["pts"]):
        fail(f"AC196 the background behind the first section is not #f5c08a at both side edges of the first screen at "
             f"{label} (found {r['pts']})")


def b_desktop(page, sid):  # AC197-AC203 AC206-AC208 AC210-AC213 AC216-AC220 AC261
    W, H = size(page)
    head, wm, nav, h1 = (info(page, s) for s in ("header", "header a.wordmark", "header nav", "h1"))
    if not head or not wm or not nav or not h1:
        fail("AC197-AC210 a <header>, its a.wordmark, its <nav> or the <h1> is missing")
        return
    hb = head["box"]
    if not rgb(head["bg"]) or min(rgb(head["bg"])) < 0xF8 or not is_pill(head) or not 60 <= hb[3] - hb[1] <= 88:
        fail(f"AC197 the <header> (background {head['bg']}, radius {min(head['radius']):.0f}px, height {hb[3] - hb[1]:.0f}px) "
             f"must be opaque with every channel at least 0xF8, have a border-radius of half its height or more and be "
             f"60-88px high")
    if hb[0] < 40 or W - hb[2] < 40 or abs(hb[0] - (W - hb[2])) > 4:
        fail(f"AC198 the <header> {rnd(hb)} needs a gap of 40px or more to each side at 1440px, the two within 4px")
    pts = page.evaluate("b => [window.__c.bgAt((b[0] + b[2]) / 2, b[1] - 6, false), window.__c.bgAt((b[0] + b[2]) / 2, b[3] + 6, false)]", hb)
    if any(rgb(p) != APRICOT for p in pts):
        fail(f"AC199 the background 6px above and 6px below the <header>, at its horizontal centre, is {pts}, not #f5c08a")
    centre = (wm["ext"][0] + wm["ext"][2]) / 2
    if abs(centre - W / 2) > 24:
        fail(f"AC200 the wordmark text's centre is at {centre:.0f}px, more than 24px from {W / 2:.0f}px")
    want_face("AC201", "the header wordmark", wm["fam"], "Noto Serif KR")
    if wm["weight"] != 700 or not 28 <= wm["fs"] <= 32:
        fail(f"AC201 the header wordmark is set at {wm['fs']}px, weight {wm['weight']}; it needs 28-32px and 700")
    if nav["box"][2] > wm["ext"][0]:
        fail(f"AC202 the header <nav>'s right edge ({nav['box'][2]:.0f}px) is not left of the wordmark ({wm['ext'][0]:.0f}px)")
    links = page.evaluate("[...document.querySelectorAll('header a')].filter(window.__c.shown).map(window.__c.info)")
    ask = [x for x in links if x["href"] == f"#{sid}" and "도입 문의" in x["text"]]
    if not ask:
        fail(f"AC203 the <header> has no link to #{sid} whose text contains '도입 문의'")
    else:
        x = ask[0]
        if x["box"][0] < wm["ext"][2]:
            fail(f"AC203 the header 도입 문의 link ({x['box'][0]:.0f}px) is not right of the wordmark ({wm['ext'][2]:.0f}px)")
        want_color("AC203", "the header 도입 문의 link's background", x["bg"], WINE)
        want_color("AC203", "the header 도입 문의 link's colour", x["color"], PAPER)
        want_pill("AC203", "the header 도입 문의 link", x)
    if h1["ext"][0] > 144 or h1["ext"][2] > 800 or not inside_viewport(h1["box"], W, H):
        fail(f"AC206 the <h1> text runs from {h1['ext'][0]:.0f}px to {h1['ext'][2]:.0f}px (box {rnd(h1['box'])}); it must "
             f"start within 144px of the left edge, end at most 800px from it and lie fully inside the viewport")
    want_face("AC207", "the <h1>", h1["fam"], "Noto Sans KR")
    want_color("AC207", "the <h1>'s colour", h1["color"], INK_B)
    if h1["weight"] != 300 or not 52 <= h1["fs"] <= 76:
        fail(f"AC207 the <h1> is set at {h1['fs']}px, weight {h1['weight']}; it needs 52-76px and 300")
    ems = page.evaluate("[...document.querySelectorAll('h1 em')].map(window.__c.info)")
    if not 1 <= len(ems) <= 2 or any(e["fam"] != "Noto Serif KR" or e["weight"] != 700 or e["style"] != "normal"
                                     or e["fs"] != h1["fs"] for e in ems):
        fail(f"AC208 the <h1> needs one or two <em> in Noto Serif KR, weight 700, font-style normal, at the <h1>'s size "
             f"(found {[(e['fam'], e['weight'], e['style'], e['fs']) for e in ems]})")
    lines = (h1["box"][3] - h1["box"][1]) / h1["fs"]
    if not 1.9 <= lines <= 3.9:
        fail(f"AC261 the <h1> box is {lines:.2f} x its font-size high, not 1.9-3.9 (two or three lines)")
    links = first_links(page, "AC210") or []
    if len(links) != 1 or "도입 문의" not in links[0]["text"] or links[0]["href"] != f"#{sid}":
        fail(f"AC210 the first section must hold exactly one link outside the bars, with '도입 문의' in its text and the "
             f"href #{sid} (found {[(x['text'], x['href']) for x in links]})")
    else:
        want_color("AC210", "the first-section 도입 문의 link's background", links[0]["bg"], INK_B)
        want_color("AC210", "the first-section 도입 문의 link's colour", links[0]["color"], PAPER)
        want_pill("AC210", "the first-section 도입 문의 link", links[0])
    svgs = page.evaluate(FIRST_SVGS, True) or []
    if len(svgs) != 1:
        fail(f'AC211 the first section needs exactly one inline <svg aria-hidden="true">, found {len(svgs)}')
    else:
        d = svgs[0]["box"]
        if d[0] < W / 2 or not 360 <= d[2] - d[0] <= 560 or not inside_viewport(d, W, H):
            fail(f"AC211 the drawing {rnd(d)} must start at or right of {W / 2:.0f}px, be 360-560px wide and lie fully "
                 f"inside the viewport")
        dr = page.evaluate(B_DRAWING)
        shapes = dr["shapes"]
        if len(shapes) < 6:
            fail(f"AC212 the drawing holds {len(shapes)} shape elements, needs six or more")
        for s in shapes:
            if s["fill"] != "none" and s["w"] > 16:
                fail(f"AC212 a <{s['tag']}> of the drawing is filled ({s['fill']}) and {s['w']:.0f}px wide; a filled shape is "
                     f"at most 16px wide")
            if s["stroke"] != "none" and s["stroke"] != "rgb(42, 29, 20)":
                fail(f"AC212 a <{s['tag']}> of the drawing has the stroke {s['stroke']}, not #2a1d14")
            if s["tag"] == "circle" and s["w"] > 16:
                fail(f"AC213 the drawing holds a <circle> {s['w']:.0f}px wide, above 16px")
        if dr["bad"]:
            fail(f"AC213 the drawing holds {sorted(set(dr['bad']))}")
    cards = page.evaluate("""() => [...document.querySelectorAll('.word-card')].map(k => { const c = window.__c, t = k.querySelector('.term');
      return {box: c.box(k), term: t ? c.info(t) : null}; })""")
    if len(cards) != 3 or any(not k["term"] for k in cards):
        fail(f'AC216 expected three elements with class "word-card", each with a "term" (found {len(cards)})')
    else:
        for k in cards:
            if k["term"]["fs"] < 40:
                fail(f"AC216 the word-card term {k['term']['text']!r} is set at {k['term']['fs']}px, below 40px at 1440px")
            if k["term"]["fam"] != "Noto Serif KR" or k["term"]["weight"] != 700:
                fail(f"AC217 the word-card term {k['term']['text']!r} is in {k['term']['fam']!r} at weight "
                     f"{k['term']['weight']}, not Noto Serif KR 700")
        tops = [k["box"][1] for k in cards]
        if max(tops) - min(tops) > 4:
            fail(f"AC218 the word cards' top edges spread more than 4px at 1440px: {rnd(tops)}")
    dashed = page.evaluate("""() => [...document.body.querySelectorAll('*')].filter(e => { const s = getComputedStyle(e);
      return s.borderTopStyle === 'dashed' && parseFloat(s.borderTopWidth) > 0 && e.getBoundingClientRect().width >= 900 && window.__c.shown(e); }).length""")
    if dashed < 2:
        fail(f"AC220 {dashed} elements 900px wide or wider have a dashed top border at 1440px, needs two or more")


def big_digits(page, label):  # AC219
    bad = page.evaluate("""() => [...document.body.querySelectorAll('*')].filter(e => /\\d/.test(window.__c.own(e))
        && parseFloat(getComputedStyle(e).fontSize) > 24 && e.getClientRects().length)
      .map(e => window.__c.own(e).slice(0, 20) + ' at ' + getComputedStyle(e).fontSize).slice(0, 8)""")
    for b in bad:
        fail(f"AC219 a digit set above 24px at {label}: {b}")


def b_mobile(page, sid):  # AC198 (390) AC204 AC214 AC215 AC218 (390)
    W, H = size(page)
    head = info(page, "header")
    if not head or head["box"][0] < 12 or W - head["box"][2] < 12:
        fail(f"AC198 the <header> {head and rnd(head['box'])} needs a gap of 12px or more to each side at 390px")
    seen = page.evaluate("""sid => [...document.querySelectorAll('header a[href="#' + sid + '"]')]
        .filter(a => /도입 문의/.test(a.textContent)).some(window.__c.inView)""", sid)
    if not seen:
        fail("AC204 the header 도입 문의 link is not visible without scrolling at 390px")
    h1_on_load(page, "AC214", 30, "390px")
    h1 = info(page, "h1")
    svgs = [s for s in (page.evaluate(FIRST_SVGS, True) or []) if s["shown"]]
    if not h1 or len(svgs) != 1 or svgs[0]["box"][1] < h1["box"][3] - 0.5 or svgs[0]["box"][2] - svgs[0]["box"][0] < 200:
        fail(f"AC215 at 390px the drawing must be displayed below the <h1> and be 200px wide or more "
             f"(found {[rnd(s['box']) for s in svgs]}, <h1> bottom {h1 and round(h1['box'][3])})")
    cards = page.evaluate("[...document.querySelectorAll('.word-card')].map(window.__c.box)")
    if len(cards) != 3 or not stacked(cards):
        fail(f"AC218 at 390px the three word cards do not stack in one column: {[rnd(b) for b in cards]}")


# --- sample D ----------------------------------------------------------------------------------------------

D_HEADER = """() => { const h = document.querySelector('header'); if (!h) return null; const s = getComputedStyle(h), r = h.getBoundingClientRect();
  return {position: s.position, bg: s.backgroundColor, filter: (s.backdropFilter && s.backdropFilter !== 'none') ? s.backdropFilter : (s.webkitBackdropFilter || 'none'),
    radius: window.__c.radius(h).join(), width: Math.round(r.width), height: Math.round(r.height)}; }"""

D_CARDS = """pat => { const c = window.__c, s = c.sec(pat); if (!s) return null;
  const hit = [...s.querySelectorAll('*')].filter(e => { const g = c.rgba(getComputedStyle(e).backgroundColor);
    return g && g[3] >= 1 && g.slice(0, 3).join() === '22,26,28' && Math.min(...c.radius(e)) >= 20 && c.shown(e); });
  return hit.filter(e => !hit.some(o => o !== e && o.contains(e))).map(c.box); }"""

D_BAND = """pat => { const c = window.__c, s = c.sec(pat); if (!s) return null;
  return {box: c.box(s), bg: c.rgba(getComputedStyle(s).backgroundColor), radius: c.radius(s),
    colours: [...new Set([s, ...s.querySelectorAll('*')].filter(e => c.own(e) && c.shown(e)).map(e => getComputedStyle(e).color))],
    cards: [...s.querySelectorAll('ol > li')].map(c.box)}; }"""


def d_header(page, label):  # AC226 AC227, at 1440
    a = page.evaluate(D_HEADER)
    if not a:
        fail("AC226 no <header>")
        return
    col = page.evaluate("v => window.__c.rgba(v)", a["bg"])
    if "blur" not in a["filter"] or not col or not 0.75 <= col[3] <= 0.92 or max(col[:3]) > 0x30:
        fail(f"AC226 the <header> needs a backdrop-filter with blur (is {a['filter']!r}) and a background with an alpha "
             f"from 0.75 to 0.92 and every channel at most 0x30 (is {a['bg']})")
    page.evaluate("scrollTo({top: 1200, behavior: 'instant'})")
    page.wait_for_timeout(600)
    b = page.evaluate(D_HEADER)
    y = page.evaluate("scrollY")
    page.evaluate("scrollTo({top: 0, behavior: 'instant'})")
    page.wait_for_timeout(200)
    if a["position"] not in ("fixed", "sticky") or a != b or y < 1200:
        fail(f"AC227 the <header> must be fixed or sticky and keep its background, backdrop-filter, border-radius, width "
             f"and height at scroll 1200px (scroll 0: {a}; scroll {y:.0f}: {b})")


def d_desktop(page, sid):  # AC228-AC240 AC243-AC246
    W, H = size(page)
    head, wm, h1 = (info(page, s) for s in ("header", "header a.wordmark", "h1"))
    if not head or not wm or not h1:
        fail("AC228-AC240 a <header>, its a.wordmark or the <h1> is missing")
        return
    hb = head["box"]
    if not is_pill(head) or hb[0] < 120 or W - hb[2] < 120 or abs(hb[0] - (W - hb[2])) > 4:
        fail(f"AC228 the <header> {rnd(hb)} (radius {min(head['radius']):.0f}px) needs a border-radius of half its height or "
             f"more and a gap of 120px or more to each side at 1440px, the two within 4px")
    if not 150 <= wm["ext"][0] <= 260:
        fail(f"AC229 the wordmark text's left edge is at {wm['ext'][0]:.0f}px, not 150-260px from the left")
    want_face("AC230", "the header wordmark", wm["fam"], "Gasoek One")
    want_color("AC230", "the header wordmark's colour", wm["color"], LIME)
    if not 35 <= wm["fs"] <= 38:
        fail(f"AC230 the header wordmark is set at {wm['fs']}px at 1440px, not 35-38px")
    d_spans(page, "1440px")
    want_face("AC234", "the <h1>", h1["fam"], "Gasoek One")
    if not 60 <= h1["fs"] <= 84:
        fail(f"AC234 the <h1> is set at {h1['fs']}px at 1440px, not 60-84px")
    if h1["ext"][0] > 200:
        fail(f"AC235 the <h1> text's left edge is at {h1['ext'][0]:.0f}px, more than 200px from the left")
    h1_on_load(page, "AC235", 0, "1440px")
    svc = section_id(page, SVC)
    links = first_links(page, "AC236") or []
    if len(links) != 2 or "프로젝트 문의" not in links[0]["text"] or links[0]["href"] != f"#{sid}" \
            or links[1]["text"] != "서비스 보기" or links[1]["href"] != f"#{svc}":
        fail(f"AC236 the first section must hold exactly two links outside the bars: first one with '프로젝트 문의' to "
             f"#{sid}, then '서비스 보기' to #{svc} (found {[(x['text'], x['href']) for x in links]})")
    else:
        for x, bg, fg, what in ((links[0], LIME, PAGE_D, "프로젝트 문의"), (links[1], CARD_D, TEXT_D, "서비스 보기")):
            want_color("AC237", f"the '{what}' link's background", x["bg"], bg)
            want_color("AC237", f"the '{what}' link's colour", x["color"], fg)
            want_pill("AC237", f"the '{what}' link", x)
        if abs(links[0]["box"][1] - links[1]["box"][1]) > 4 or min(links[0]["box"][1], links[1]["box"][1]) < h1["box"][3] - 0.5:
            fail(f"AC238 the two links' top edges ({links[0]['box'][1]:.0f}px, {links[1]['box'][1]:.0f}px) must lie within "
                 f"4px of each other and below the <h1> ({h1['box'][3]:.0f}px)")
    svgs = page.evaluate(FIRST_SVGS, False) or []
    if len(svgs) != 1:
        fail(f'AC239 the first section needs exactly one inline <svg aria-hidden="true"> outside a link, found {len(svgs)}')
    else:
        o = svgs[0]["box"]
        if o[0] < W / 2 or not 300 <= o[2] - o[0] <= 560 or not inside_viewport(o, W, H):
            fail(f"AC239 the object {rnd(o)} must start at or right of {W / 2:.0f}px, be 300-560px wide and lie fully "
                 f"inside the viewport")
        lit = page.evaluate("""() => { const svg = window.__c.first().find(e => e.tagName.toLowerCase() === 'svg' && e.getAttribute('aria-hidden') === 'true' && !e.closest('a'));
          return [svg, svg.parentElement].map(e => getComputedStyle(e).filter + ' | ' + getComputedStyle(e).backgroundImage); }""")
        if not any(re.search(r"drop-shadow|blur", t.split(" | ")[0]) or "radial-gradient" in t.split(" | ")[1] for t in lit):
            fail(f"AC240 neither the object nor its parent has a filter with drop-shadow or blur, or a radial-gradient "
                 f"background-image (found {lit})")
    cards = page.evaluate(D_CARDS, SVC) or []
    if len(cards) < 4:
        fail(f"AC243 the service section holds {len(cards)} cards with the background #161a1c and a border-radius of 20px "
             f"or more, needs four or more")
    else:
        widths = [b[2] - b[0] for b in cards]
        if max(widths) - min(widths) < 80:
            fail(f"AC244 the widest and the narrowest service card differ by {max(widths) - min(widths):.0f}px at 1440px, below 80px")
    band = page.evaluate(D_BAND, STEPS)
    if not band:
        fail("AC245 no single steps section (the band)")
    else:
        if rgb(band["bg"]) != LIME or min(band["radius"]) < 32 or band["box"][2] - band["box"][0] < 0.9 * W \
                or band["colours"] != ["rgb(7, 9, 10)"]:
            fail(f"AC245 the band needs the background #a9ef2c (is {band['bg']}), a border-radius of 32px or more (is "
                 f"{min(band['radius'])}), a width of 90 % of the viewport or more (is {band['box'][2] - band['box'][0]:.0f}px) "
                 f"and text only in #07090a (is {band['colours']})")
        c = band["cards"]
        ok = len(c) == 3 and all(b[0] >= a[2] - 1 for a, b in zip(c, c[1:])) \
            and all(abs(c[i][1] - c[j][1]) >= 16 for i in range(3) for j in range(i + 1, 3))
        if not ok:
            fail(f"AC246 the band's <ol> needs exactly three <li> cards side by side with top edges 16px or more apart "
                 f"pairwise at 1440px (found {[rnd(b) for b in c]})")


def d_spans(page, label):  # AC231 AC232 AC233
    spans = page.evaluate("""() => { const h = document.querySelector('h1'); if (!h) return null;
      return {own: window.__c.own(h), kids: [...h.children].map(k => ({tag: k.tagName.toLowerCase(), ...window.__c.info(k)}))}; }""")
    if not spans or spans["own"] or [k["tag"] for k in spans["kids"]] != ["span"] * 3 or any(k["display"] != "block" for k in spans["kids"]):
        fail(f"AC231 the <h1> needs exactly three child <span> elements with display block and no text outside them at {label}")
        return
    for k in spans["kids"]:
        if (k["box"][3] - k["box"][1]) > 1.5 * k["fs"]:
            fail(f"AC232 the <h1> line {k['text']!r} is {(k['box'][3] - k['box'][1]) / k['fs']:.2f} x its font-size high at "
                 f"{label}, above 1.5 (it wraps)")
    got = [rgb(k["color"]) for k in spans["kids"]]
    if got != [TEXT_D, LIME, TEXT_D]:
        fail(f"AC233 the three <h1> lines have the colours {got} at {label}, expected #f2f5ee, #a9ef2c, #f2f5ee")


def d_mobile(page):  # AC228 (390) AC230 (390) AC232 AC234 AC235 (390) AC242 AC244 AC247
    W, H = size(page)
    head, wm, h1 = (info(page, s) for s in ("header", "header a.wordmark", "h1"))
    if not head or head["box"][0] < 12 or W - head["box"][2] < 12:
        fail(f"AC228 the <header> {head and rnd(head['box'])} needs a gap of 12px or more to each side at 390px")
    if not wm or not 30 <= wm["fs"] <= 34:
        fail(f"AC230 the header wordmark is set at {wm and wm['fs']}px at 390px, not 30-34px")
    d_spans(page, "390px")
    if not h1 or h1["fs"] < 30:
        fail(f"AC234 the <h1> is set at {h1 and h1['fs']}px at 390px, below 30px")
    h1_on_load(page, "AC235", 0, "390px")
    svgs = [s for s in (page.evaluate(FIRST_SVGS, False) or []) if s["shown"]]
    if len(svgs) != 1 or svgs[0]["box"][2] - svgs[0]["box"][0] < 160:
        fail(f"AC242 at 390px the object must be displayed and be 160px wide or more (found {[rnd(s['box']) for s in svgs]})")
    cards = page.evaluate(D_CARDS, SVC) or []
    if len(cards) < 4 or not stacked(cards):
        fail(f"AC244 at 390px the service cards do not stack in one column: {[rnd(b) for b in cards]}")
    band = page.evaluate(D_BAND, STEPS)
    if not band or len(band["cards"]) != 3 or not stacked(band["cards"]):
        fail(f"AC247 at 390px the band's three cards do not stack in one column: {band and [rnd(b) for b in band['cards']]}")


# --- commands ----------------------------------------------------------------------------------------------

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
        for sel, what, want in (("h1", "<h1>", SAMPLES[slug]["h1"]), ("header a.wordmark", "header wordmark", SAMPLES[slug]["wm"])):
            guard("AC99", web_font, page, sel, what, want)  # first: the measurements below need the real faces
        sid = guard("AC30", section_id, page, CONTACT)
        if not sid:
            fail(f"AC30 no single <section id> whose own <h2> contains 문의 or 상담 at {label}; the contact link checks did not run")
        if key == "A":
            guard(f"sample A at {label}", a_blocks, page, label)
            guard(f"sample A at {label}", a_desktop if vp is DESKTOP else a_mobile, page, sid)
        elif key == "B":
            guard(f"sample B at {label}", b_common, page, label)
            guard(f"sample B at {label}", b_desktop if vp is DESKTOP else b_mobile, page, sid)
            guard("AC219", big_digits, page, label)
        else:
            if vp is DESKTOP:
                guard("sample D at 1440px", d_desktop, page, sid)
                guard("AC226 AC227", d_header, page, label)
            else:
                guard("sample D at 390px", d_mobile, page)
        if vp is DESKTOP:
            guard("AC260", h1_side, page, key)
        guard("AC34", keep_all, page, label)
        if key in ("A", "B"):
            guard("AC32 AC148", sentence_first_screen, page, label)
        guard("AC8-AC12 AC147", marker, page, vp, label)
        if sid:
            guard("AC40-AC43", contact_link, page, vp, sid, label)
        if vp is MOBILE:
            guard("AC149", bars, page)
        guard("AC31 AC58-AC60", sentences, page, label)
        guard("AC100", digit_fonts, page, label)
        guard("AC101 AC253 AC254", faces, page, label)
        guard("settle", settle, page)
        if vp is DESKTOP:
            guard("AC133", no_overflow, page, "AC133 1440px")  # after the scroll-through, on the full page
        name = "desktop-1440.png" if vp is DESKTOP else "mobile-390.png"
        heights[name] = guard("screenshots", bands, page, out / name, vp["width"])
        guard("AC132", contrast, page, label)
        for b in bad_fonts:  # read last, so font files fetched during the scroll-through count too
            fail(f"AC99 web font request did not return 200 at {label}: {b}")
        ctx.close()

    def iframe_390():  # AC134: inside a width:390px iframe, as playbook §4 does it
        ctx, page = new_page(browser, DESKTOP)
        page.goto(f"{base}/profile/")
        page.set_content(f'<iframe src="{url}" style="width:390px;height:844px;border:0"></iframe>')
        page.frame_locator("iframe").locator("body").wait_for()
        inner = page.frames[1]
        inner.wait_for_load_state("networkidle")
        inner.wait_for_timeout(1500)
        settle(inner)
        no_overflow(inner, "AC134 390px iframe")
        ctx.close()
    guard("AC134", iframe_390)

    def motion(label, vp):  # AC131
        ctx, page = new_page(browser, vp, reduced_motion="reduce")
        page.goto(url, wait_until="networkidle")
        settle(page)
        reduced_motion(page, label)
        ctx.close()
    for label, vp in (("1440px", DESKTOP), ("390px", MOBILE)):
        guard(f"AC131 {label}", motion, label, vp)
    tree, dirty = tree_state(slug)
    lines = [f"slug {slug}", f"head {git('rev-parse', 'HEAD') or 'unknown'}", f"site tree {tree}",
             f"site working tree {dirty}", *(f"height {k} {v}" for k, v in heights.items()),
             *(f"FAIL {f}" for f in fails), f"result {'PASS' if not fails else 'FAIL'}"]
    (out / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"screenshots for the reviews: {out}/desktop-1440*.png {out}/mobile-390*.png, summary {out / 'summary.txt'}")


def check_gallery(browser, base):  # AC137 AC138 AC140 AC141 AC142
    ctx, page = new_page(browser, DESKTOP)
    page.goto(f"{base}/profile/", wait_until="networkidle")
    page.click('.pf-filters button[data-filter="crypto"]')
    page.wait_for_timeout(300)
    shown = page.locator('a.pf-card[data-industry="crypto"]:visible')
    slugs = sorted(shown.nth(i).get_attribute("data-slug") for i in range(shown.count()))
    if slugs != sorted(SAMPLES):
        fail(f"AC137 the crypto filter shows cards {slugs}, expected {sorted(SAMPLES)}")
    if page.locator('.pf-empty[data-industry="crypto"]:visible').count():
        fail("AC138 the crypto filter still shows a 준비 중 tile")
    width = "document.getElementById('pf-v-iframe').getBoundingClientRect().width"
    for slug in SAMPLES:  # each card from a fresh load of /profile/, as a visitor arrives
        if slug not in slugs:
            continue
        page.goto(f"{base}/profile/", wait_until="networkidle")
        page.click('.pf-filters button[data-filter="crypto"]')
        page.wait_for_timeout(300)
        viewer, iframe = page.locator("#pf-viewer"), page.locator("#pf-v-iframe")
        page.locator(f'a.pf-card[data-slug="{slug}"]').click()
        page.wait_for_timeout(300)
        if not viewer.is_visible() or not (iframe.get_attribute("src") or "").endswith(f"/profile/{slug}/"):
            fail(f"AC140 clicking the {slug} card does not open the preview with that sample")
            continue
        try:  # the loaded document is this sample's page (matched by slug)
            page.frame_locator("#pf-v-iframe").locator("header a.wordmark").first.wait_for(state="attached",
                                                                                            timeout=10000)
            next(f for f in page.frames if f.url.rstrip("/").endswith(f"/profile/{slug}"))
        except Exception:
            fail(f"AC140 {slug}: the preview iframe does not show that sample's page")
        for device, cond in (("mobile", "<= 400"), ("desktop", "> 600")):  # the width animates; wait for it
            page.click(f'button[data-device="{device}"]')
            try:
                page.wait_for_function(f"{width} {cond}", timeout=3000)
            except Exception:
                fail(f"AC141 {slug}: the {device} button does not switch the preview width ({page.evaluate(width)})")
        page.keyboard.press("Escape")
        try:
            page.wait_for_function("document.getElementById('pf-viewer').hidden", timeout=3000)
        except Exception:
            fail(f"AC142 {slug}: Esc does not close the preview")
    ctx.close()


def check_trio(browser, base):  # AC125 AC126 AC258 AC259 AC263
    got = {}
    for slug in SAMPLES:
        if not (ROOT / "profile" / slug / "index.html").is_file():
            fail(f"AC125 AC126 AC258 AC259 AC263 profile/{slug}/index.html does not exist")
            continue
        got[slug] = {}
        for label, vp in (("1440", DESKTOP), ("390", MOBILE)):
            ctx, page = new_page(browser, vp)
            page.goto(f"{base}/profile/{slug}/", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(500)
            lib(page)
            got[slug][label] = (info(page, "h1"), info(page, "header a.wordmark"))
            ctx.close()
        if not all(x for pair in got[slug].values() for x in pair):
            fail(f"AC125 AC126 AC258 AC259 AC263 {slug}: no <h1> or no header a.wordmark to read")
            del got[slug]
    slugs = list(got)
    if len(slugs) < len(SAMPLES):
        return
    pairs = [(a, b) for i, a in enumerate(slugs) for b in slugs[i + 1:]]
    for ac, what, idx in (("AC125", "<h1>", 0), ("AC126", "header wordmark", 1)):
        fams = {s: got[s]["1440"][idx]["fam"] for s in slugs}
        if len({f.lower() for f in fams.values()}) != len(fams):
            fail(f"{ac} two samples share the {what}'s first font family: {fams}")
    for a, b in pairs:
        wa, wb = got[a]["1440"][1], got[b]["1440"][1]
        ca, cb = ((w["ext"][0] + w["ext"][2]) / 2 for w in (wa, wb))
        if abs(ca - cb) < 60:
            fail(f"AC258 the wordmark text centres of {a} ({ca:.0f}px) and {b} ({cb:.0f}px) are less than 60px apart at 1440px")
        if abs(wa["fs"] - wb["fs"]) < 3:
            fail(f"AC259 the wordmark sizes of {a} ({wa['fs']}px) and {b} ({wb['fs']}px) differ by less than 3px at 1440px")
        ma, mb = got[a]["390"][1], got[b]["390"][1]
        if abs(ma["fs"] - mb["fs"]) < 2:
            fail(f"AC263 the wordmark sizes of {a} ({ma['fs']}px) and {b} ({mb['fs']}px) differ by less than 2px at 390px")
    for s in slugs:
        w, m = got[s]["1440"][1], got[s]["390"][1]
        print(f"{s}: h1 {got[s]['1440'][0]['fam']}, wordmark {w['fam']} {w['fs']}px centre {(w['ext'][0] + w['ext'][2]) / 2:.0f}px at 1440, {m['fs']}px at 390")


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
            if slug not in SAMPLES:  # the crypto samples' full pages are in <slug>/ from `page`
                settle(page)
                bands(page, out / f"{slug}-{label}-full.png", vp["width"])
            ctx.close()
        thumb = ROOT / "profile" / slug / "thumb.jpg"
        if slug in SAMPLES and thumb.is_file():
            shutil.copyfile(thumb, out / f"{slug}-thumb.jpg")
        tree, state = tree_state(slug)
        notes.append(f"local {slug} tree {tree} {state}")
    for slug, meta in SAMPLES.items():
        ctx = browser.new_context(viewport=DESKTOP)
        page = ctx.new_page()
        try:
            resp = page.goto(meta["ref"], wait_until="load", timeout=45000)
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
            notes.append(f"reference {slug} {meta['ref']} ok {datetime.now().date()}")
        except Exception as exc:
            for f in out.glob(f"tmp-ref-{slug}*"):
                f.unlink()
            have = all((out / f"ref-{slug}{x}").is_file() for x in (".png", ".txt", "-full.png", "-full-01.png"))
            when = datetime.fromtimestamp((out / f"ref-{slug}.png").stat().st_mtime).date() if have else ""
            notes.append(f"reference {slug} {meta['ref']} {'cached ' + str(when) if have else 'unreachable'}: "
                         f"{type(exc).__name__}: {(str(exc).splitlines() or [''])[0]}")
        ctx.close()
    (out / "summary.txt").write_text("\n".join([f"head {git('rev-parse', 'HEAD') or 'unknown'}", *notes]) + "\n",
                                     encoding="utf-8")
    print("\n".join(notes))
    print(f"compare shots: {out}")


if __name__ == "__main__":
    args = sys.argv[1:]
    shots = Path("/tmp/profile-crypto-shots")
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
    def give_up():  # a browser that never answers is a failure, not a wait
        print(f"FAIL {' '.join(args)}: no result after {DEADLINE} s; the browser did not answer")
        print(f"FAIL: {' '.join(args)} (1 failures)", flush=True)
        os._exit(1)
    watchdog = threading.Timer(DEADLINE, give_up)
    watchdog.daemon = True
    watchdog.start()
    httpd, base = serve()
    try:
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
            for f in fails:  # the verdict first: closing Chrome can wait minutes on a helper process that holds its pipes
                print("FAIL", f)
            print(f"{'PASS' if not fails else 'FAIL'}: {' '.join(args)} ({len(fails)} failures)", flush=True)
            httpd.shutdown()
            httpd.server_close()
            sys.stdout.flush()
            os._exit(1 if fails else 0)  # no browser.close(): the driver ends Chrome when this process is gone
    finally:
        httpd.shutdown()
        httpd.server_close()
