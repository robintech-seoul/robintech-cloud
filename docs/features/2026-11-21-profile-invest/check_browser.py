#!/usr/bin/env python3
"""Browser checks for the three invest profile samples (Playwright + installed Google Chrome). Run from the
repository root.

usage: python3 docs/features/2026-11-21-profile-invest/check_browser.py page <slug> | thumb <slug> | gallery | trio
       | compare [--shots DIR]
  page <slug>  AC8-AC10 AC12 AC18 AC31 AC32 AC34 AC41-AC47 AC57-AC59 AC81 AC95 AC96 AC98 AC101 AC117-AC121, and
               B (invest-robinfamilyoffice): AC130-AC139 AC141 AC143-AC146 AC148 AC150-AC154 AC156-AC160 AC164,
               C (invest-robinwealth): AC170-AC186 AC188 AC189 AC192-AC197,
               D (invest-robincapital): AC77 AC206-AC213 AC216-AC226 AC228-AC232 AC236.
               Empties DIR/<slug>/ first, then writes full-page screenshots for the reviews (desktop-1440.png,
               mobile-390.png, and the same cut into 1200 px bands -NN.png), the page as a width:390px iframe shows
               it from top to end (iframe-390-NN.png, AC97), crops of the header wordmark and of the <h1> at both
               widths (wordmark-1440.png, h1-390.png ...) and summary.txt last.
  thumb <slug> AC5: thumb.jpg shows the sample's current 1440x900 first screen
  gallery      AC111 on /profile/
  trio         AC242-AC247: faces, wordmark positions and sizes, and <h1> positions across the three samples
  compare      evidence for the reviews, not a check: rewrites DIR/compare/ with first screens (1440x900 and 390x844)
               of the three invest samples and the eighteen shipped samples, the thumb.jpg files, the G1 screenshots
               of the references (ref-g1-<slug>-1440.jpg, -390.jpg, copied from .git/robintech-dev/keep/), a live copy
               of each reference home page when it answers (ref-<slug>.png, ref-<slug>.txt; the last good copy is
               kept), and the sheets sheet-*.png that set them side by side. summary.txt lists each local tree hash
               and each reference, and ends with result PASS|FAIL. Exit 0 when every local screenshot and every
               sheet was written and the invest samples rendered in their web fonts.
DIR defaults to /tmp/profile-invest-shots. Serves the repository root on a free local port itself and stops the
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
    "invest-robinfamilyoffice": {"key": "B", "g1": "B", "ref": "https://www.rockco.com/",
                                 "h1": ("Grandiflora One", "Gowun Batang"), "wm": ("Gowun Batang",), "name": "로빈패밀리오피스"},
    "invest-robinwealth": {"key": "C", "g1": "C", "ref": "https://www.pjtpartners.com/", "h1": PRETENDARD, "wm": PRETENDARD, "name": "로빈자산관리"},
    "invest-robincapital": {"key": "D", "g1": "D", "ref": "https://hgcapital.com/", "h1": ("Orbit",), "wm": ("Orbit",), "name": "로빈캐피탈"},
}
SHIPPED = ("flower-bomgyeol", "food-saebyeokmil", "clinic-neuru", "clinic-byeotteul", "clinic-bonui", "law-ganeum",
           "law-goim", "fitness-mideoum", "fitness-jjuuk", "beauty-robinhair", "beauty-robinsalon",
           "beauty-robinhairsalon", "interior-robininterior", "interior-robindesign", "interior-robinhome",
           "crypto-robincoin", "crypto-robincustody", "crypto-robinchain")
SIX = ("food-saebyeokmil", "clinic-bonui", "crypto-robincoin", "law-ganeum", "crypto-robinchain", "interior-robinhome")  # AC250
MARK = "로빈테크 디자인 샘플 · 상호와 정보는 가상입니다"
MARK_TAIL = "디자인 샘플 · 상호와 정보는 가상입니다"  # AC12
FICTION = "가상의 업체이며 금융투자업자가 아닙니다. 투자 권유가 아니며 실제 자문 · 운용 · 상담을 제공하지 않습니다."  # AC31 AC32
RISK = "투자에는 원금 손실 위험이 있으며, 손실은 투자자에게 귀속됩니다."  # AC57
PE_NOTE = "저희가 운용하는 기관전용 사모펀드는 개인의 출자를 받지 않습니다."  # AC77
READ_NOTE = "계약을 체결하기 전에 설명서와 약관을 읽어 보시기 바랍니다."  # AC81
ASK = "상담 문의"
DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net")
DEADLINE = 900  # seconds one run may take before it is a failure
THUMB_MAX_TILE = 40.0  # the same per 10x10-pixel tile of the 160x100 images (16 x 10 tiles), so a changed area shows
THUMB_MAX_DIFF = 15.0  # mean absolute RGB difference (0-255) at 160x100 between thumb.jpg and a fresh first screen
WHITE = (255, 255, 255)
CREAM, INK_B, GREEN, STRAW = (0xF3, 0xEE, 0xE2), (0x18, 0x26, 0x1E), (0x12, 0x35, 0x24), (0xE3, 0xCF, 0x8E)
PAGE_C, INK_C, STOPS_C = (0xFD, 0xFB, 0xF8), (0x21, 0x1A, 0x16), {(181, 83, 58), (143, 58, 36)}
VIOLET, TEXT_D, SHEET, PALE, STRIP_D, PINK = (0x23, 0x0A, 0x47), (0xF4, 0xEF, 0xFC), (0xFB, 0xF9, 0xFF), (0xEC, 0xE6, 0xFB), (0x16, 0x06, 0x2E), (0xFF, 0x66, 0x85)
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
  const lines = e => { const out = [], w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);  // each line box of the rendered text: a
    for (let n; (n = w.nextNode());) { if (!n.nodeValue.trim()) continue; const g = document.createRange(); g.selectNodeContents(n);  // block has one client rect
      for (const q of g.getClientRects()) if (q.width && q.height) out.push(q); }  // whatever its line count, so the text nodes are read
    return out.length ? out : [...e.getClientRects()].filter(q => q.width && q.height); };
  const rects = lines(el);
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
    if (own.visibility === 'hidden') return false;
    if (!e.contains(el) && o > 0.5 && (/^(IMG|VIDEO|CANVAS)$/.test(e.tagName)  // a picture has no background and covers all the same
        || (e instanceof SVGGeometryElement && own.fill !== 'none' && +own.fillOpacity * o > 0.5))) return true;
    return parts.some(([c, po]) => fill(c) * po * o > 0.5); };
  const shows = stack => { for (const t of stack) { if (el === t || el.contains(t)) return true; if (paints(t)) return false; }
    return false; };
  return stacks.every(shows); }"""

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
  sec: kind => { const pats = {services: /하는 일|서비스|투자 분야/, steps: /절차|과정|방식/, contact: /문의|상담/};  // as section() in check_static.py
    const hits = k => [...document.querySelectorAll('section[id]')].filter(s =>
      [...s.querySelectorAll('h2')].some(h => h.closest('section') === s && pats[k].test(h.textContent)));
    let hit = hits(kind); if (kind === 'contact') { const other = [...hits('services'), ...hits('steps')]; hit = hit.filter(s => !other.includes(s)); }
    return hit.length === 1 ? hit[0] : null; },
  radius: e => { const s = getComputedStyle(e), h = e.getBoundingClientRect().height;
    return [s.borderTopLeftRadius, s.borderTopRightRadius, s.borderBottomLeftRadius, s.borderBottomRightRadius]
      .map(v => { const p = v.split(' ')[0]; return p.endsWith('%') ? parseFloat(p) / 100 * h : parseFloat(p); }); },
  bg: el => { const layers = [], c = window.__c;  // the colour(s) behind el: translucent layers composited down to the first opaque one
    for (let e = el; e; e = e.parentElement) for (const ps of ['::before', '::after']) { const s = getComputedStyle(e, ps);  // a painted
      if (s.content === 'none' || s.content === 'normal' || s.display === 'none') continue;  // ::before/::after of el or of an ancestor
      const k = c.rgba(s.backgroundColor);  // may lie under or over the text: not judged
      if (s.backgroundImage !== 'none' || !k || k[3] > 0)
        return {err: 'a background on ' + e.tagName.toLowerCase() + ps + ' of the element or of an ancestor'}; }
    let bases = null, owner = null;
    for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e);
      if (s.backgroundImage !== 'none') { const g = s.backgroundImage, cols = (g.match(/rgba?\\([^)]*\\)/g) || []).map(c.rgba);  // one linear-gradient
        if (!/^linear-gradient\\(/.test(g) || g.indexOf('gradient(', 16) >= 0 || /url\\(/.test(g) || cols.length < 2 || cols.some(k => !k || k[3] < 1))  // of opaque colours is judged at each stop
          return {err: 'a CSS background-image on <' + e.tagName.toLowerCase() + '> behind it that is not one linear-gradient of opaque rgb() colours'};
        bases = cols.map(k => k.slice(0, 3)); owner = e; break; }
      const k = c.rgba(s.backgroundColor); if (!k) return {err: 'unreadable background ' + s.backgroundColor};
      if (k[3] > 0) { layers.push(k); if (k[3] >= 1) { owner = e; break; } } }
    const cs = (bases || [[255, 255, 255]]).map(b => { let base = b;
      for (const k of [...layers].reverse()) base = [0, 1, 2].map(i => k[i] * k[3] + base[i] * (1 - k[3])); return base; });
    return {c: cs[0], cs, owner}; },
  stackAt: (x, y) => { const style = document.createElement('style');  // the elements at a point, top first; a pointer-events:none
    style.textContent = '*, *::before, *::after { pointer-events: auto !important; }';  // layer is painted all the same
    document.head.append(style); const out = document.elementsFromPoint(x, y); style.remove(); return out; },
  under: el => { const c = window.__c, y0 = scrollY, free = !c.pinned(el);  // null, or what is painted at the text by an element that is
    el.scrollIntoView({block: 'center', behavior: 'instant'});  // not el, not inside it and not an ancestor: bg() did not read it
    const lines = e => { const out = [], w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);  // each line box of the rendered text: a
    for (let n; (n = w.nextNode());) { if (!n.nodeValue.trim()) continue; const g = document.createRange(); g.selectNodeContents(n);  // block has one client rect
      for (const q of g.getClientRects()) if (q.width && q.height) out.push(q); }  // whatever its line count, so the text nodes are read
    return out.length ? out : [...e.getClientRects()].filter(q => q.width && q.height); };
    const rects = lines(el); let err = null;
    for (const q of rects) { const x = q.left + q.width / 2, y = q.top + q.height / 2;
      if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) continue;
      for (const t of c.stackAt(x, y)) { if (t !== el && el.contains(t)) continue; const s = getComputedStyle(t), k = c.rgba(s.backgroundColor);
        const painted = s.backgroundImage !== 'none' || !k || k[3] > 0;
        if (t === document.body || t === document.documentElement) continue;  // their background is the canvas, under a z-index below 0
        if (t.contains(el)) { if (s.backgroundImage !== 'none' || (k && k[3] >= 1)) break; continue; }
        if (free && c.pinned(t)) continue;  // a bar passes over the page; AC44 and the screenshots cover that
        if (s.visibility === 'hidden') continue;
        if (painted || /^(IMG|VIDEO|CANVAS)$/.test(t.tagName) || (t instanceof SVGGeometryElement && s.fill !== 'none')) {
          err = 'a <' + t.tagName.toLowerCase() + '> that is not an ancestor of the text is painted over or under it'; break; } }
      if (err) break; }
    scrollTo({top: y0, behavior: 'instant'}); return err; },
  bgAt: (x, y, skipPinned) => { const st = window.__c.stackAt(x, y), root = e => e === document.body || e === document.documentElement;
    for (const e of [...st.filter(e => !root(e)), ...st.filter(root)]) {  // the topmost painted background at a point; the <body> and <html>
      if (skipPinned && window.__c.pinned(e)) continue; const s = getComputedStyle(e);  // backgrounds are the canvas, painted under everything
      if (s.backgroundImage !== 'none') return 'image ' + s.backgroundImage.slice(0, 30);
      const c = window.__c.rgba(s.backgroundColor); if (c && c[3] > 0) return c; }
    return null; },
  ratio: (fg, bg) => { const lum = v => { const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * f(v[0]) + 0.7152 * f(v[1]) + 0.0722 * f(v[2]); };
    const l1 = lum(fg), l2 = lum(bg); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); },
  lum: v => { const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(v[0]) + 0.7152 * f(v[1]) + 0.0722 * f(v[2]); },
  contrast: e => { const c = window.__c, s = getComputedStyle(e), fg = c.rgba(s.color), bg = c.bg(e);  // {ratio} or {err}
    let o = 1; for (let x = e; x; x = x.parentElement) o *= +getComputedStyle(x).opacity;
    if (!fg || bg.err) return {err: bg.err || 'unreadable colour ' + s.color};
    const x = c.ext(e);  // text over a photo is not judged: the <img> is painted over the background that was read
    for (const img of document.images) { if (!c.shown(img) || (bg.owner && !bg.owner.contains(img))) continue; const r = c.box(img);
      if (Math.min(x[2], r[2]) - Math.max(x[0], r[0]) > 1 && Math.min(x[3], r[3]) - Math.max(x[1], r[1]) > 1) return {err: 'the text lies over an <img>'}; }
    const u = c.under(e); if (u) return {err: u};
    const a = fg[3] * o; let worst = null;
    for (const b of bg.cs) { const mix = [0, 1, 2].map(i => fg[i] * a + b[i] * (1 - a)), r = c.ratio(mix, b);
      if (!worst || r < worst.ratio) worst = {ratio: r, fg: mix.map(Math.round), bg: b.map(Math.round)}; }
    if (bg.cs.length > 1) { const L = bg.cs.map(c.lum), f = c.lum(worst.fg);
      if (f > Math.min(...L) && f < Math.max(...L)) return {err: 'the text colour lies between the ends of the gradient behind it'}; }
    return worst; },
  info: e => { if (!e) return null; const s = getComputedStyle(e), c = window.__c;
    return {box: c.box(e), ext: c.ext(e), fs: parseFloat(s.fontSize), fam: c.fam(e), weight: +s.fontWeight, color: c.rgba(s.color),
      bg: c.rgba(s.backgroundColor), bgImage: s.backgroundImage, style: s.fontStyle, display: s.display, position: s.position,
      href: e.getAttribute && e.getAttribute('href'), text: e.textContent.replace(/\\s+/g, ' ').trim().slice(0, 40),
      shown: c.shown(e), radius: c.radius(e), own: c.own(e), name: ((e.getAttribute && e.getAttribute('aria-label')) || e.textContent).replace(/\\s+/g, ' ').trim(), opacity: +s.opacity, ls: parseFloat(s.letterSpacing) || 0, filter: s.filter, cursor: s.cursor,
      border: ['Top', 'Right', 'Bottom', 'Left'].map(k => [s['border' + k + 'Style'], parseFloat(s['border' + k + 'Width']), c.rgba(s['border' + k + 'Color'])])}; },
  withText: (root, t) => [root, ...root.querySelectorAll('*')].filter(e => window.__c.own(e).includes(t)),
  first: () => { const c = window.__c, svc = c.sec('services'); if (!svc) return null;  // the first section, the <header> and bars aside
    return [...document.body.querySelectorAll('*')].filter(e => (svc.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_PRECEDING)
      && !e.contains(svc) && !e.closest('header') && !c.pinned(e)); },
  firstAll: () => { const c = window.__c, svc = c.sec('services'); if (!svc) return null;  // the same, the <header> included
    return [...document.body.querySelectorAll('*')].filter(e => (svc.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_PRECEDING) && !e.contains(svc)); },
  bars: () => { const c = window.__c, out = [];  // the bars: outermost fixed elements and stuck sticky elements, with the side they are pinned to
    for (const e of document.body.querySelectorAll('*')) { const s = getComputedStyle(e);
      if (!/fixed|sticky/.test(s.position) || !c.shown(e) || out.some(o => o.el.contains(e))) continue; const r = e.getBoundingClientRect();
      let pin = s.position === 'fixed'; const t = parseFloat(s.top), b = parseFloat(s.bottom);
      if (!pin) pin = (!isNaN(t) && Math.abs(r.top - t) <= 1) || (!isNaN(b) && Math.abs(innerHeight - r.bottom - b) <= 1);
      if (pin && r.bottom > 0 && r.top < innerHeight) out.push({el: e, side: (r.top + r.bottom) / 2 < innerHeight / 2 ? 'top' : 'bottom'}); }
    return out; },
  barInfo: () => { const c = window.__c; return c.bars().map(b => ({side: b.side, tag: b.el.tagName.toLowerCase(), ...c.info(b.el),
      marker: c.withText(b.el, '__MARK_TAIL__').filter(c.shown).length > 0,
      links: [b.el, ...b.el.querySelectorAll('a')].filter(a => a.tagName === 'A' && c.shown(a)).map(c.info)})); },
  behind: e => { for (; e; e = e.parentElement) { const g = window.__c.rgba(getComputedStyle(e).backgroundColor); if (g && g[3] > 0) return g; } return null; },
  solid: (x, min) => x.border.every(b => b[0] === 'solid' && b[1] >= min),
  cover: () => { const c = window.__c, iv = [];  // px of viewport height under fixed elements and stuck sticky elements
    for (const e of document.body.querySelectorAll('*')) { const s = getComputedStyle(e);
      if (!/fixed|sticky/.test(s.position) || !c.shown(e)) continue; const r = e.getBoundingClientRect();
      let pin = s.position === 'fixed'; const t = parseFloat(s.top), b = parseFloat(s.bottom);
      if (!pin) pin = (!isNaN(t) && Math.abs(r.top - t) <= 1) || (!isNaN(b) && Math.abs(innerHeight - r.bottom - b) <= 1);
      const top = Math.max(0, r.top), bot = Math.min(innerHeight, r.bottom); if (pin && bot > top) iv.push([top, bot]); }
    iv.sort((a, b) => a[0] - b[0]); let sum = 0, end = -1;
    for (const [a, b] of iv) { if (b <= end) continue; sum += b - Math.max(a, end); end = b; }
    return sum; },
}; }""".replace("__IN_VIEW__", IN_VIEW).replace("__UNDER_BAR__", UNDER_BAR).replace("__MARK_TAIL__", MARK_TAIL)


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


def section_id(page, kind):
    return page.evaluate("kind => { const s = window.__c.sec(kind); return s ? s.id : null; }", kind)


def within(inner, outer, tol=1.0):  # box inside box
    return inner[0] >= outer[0] - tol and inner[1] >= outer[1] - tol and inner[2] <= outer[2] + tol and inner[3] <= outer[3] + tol


def wide(box):
    return box[2] - box[0]


def high(box):
    return box[3] - box[1]


def clear(c):  # a computed background colour that paints nothing
    return not c or c[3] == 0


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

LAST_FOOTER_TEXT = """() => { const f = [...document.querySelectorAll('footer')].filter(f => !f.closest('article')).pop(); if (!f) return null;
  return [f, ...f.querySelectorAll('*')].filter(e => e.getClientRects().length && !window.__c.pinned(e) && window.__c.own(e)).pop() || null; }"""



def marker(page, vp, label):  # AC8 AC9 AC10, then AC12 AC117
    ac = "AC8" if vp is DESKTOP else "AC9"
    sizes = page.evaluate("""t => window.__c.withText(document.body, t).filter(e => window.__c.inView(e) && window.__c.whole(e) && window.__c.plain(e))
        .map(e => [parseFloat(getComputedStyle(e).fontSize), parseFloat(getComputedStyle(document.body).fontSize)])""", MARK)
    if not sizes:
        fail(f"{ac} the sample marker '{MARK}' is not visible without scrolling at {label}")
    elif not any(fs >= body and fs >= 14 for fs, body in sizes):
        fail(f"AC10 the first-screen sample marker is set at {sizes[0][0]}px, below the body size {sizes[0][1]}px or 14px, at {label}")
    body = page.evaluate("parseFloat(getComputedStyle(document.body).fontSize)")
    r = page.evaluate(EVERYWHERE, ["text", MARK_TAIL])
    if r["miss"]:
        fail(f"AC12 no element with '{MARK_TAIL}' is on screen at scroll {r['miss'][:5]} px ({len(r['miss'])} positions) at {label}")
    if r["bare"]:
        fail(f"AC12 the marker that stays on screen has no opaque background colour on itself or between it and its fixed or "
             f"sticky ancestor at {label}: what scrolls under it shows through the text")
    for where, got in (("scroll position 0", r["top"]), ("the end of the page", r["end"])):
        if not got or max(got) < max(14, body):
            fail(f"AC117 the marker that stays on screen is set at {got}px at {where}, below 14px or the body size {body}px, at {label}")


def sentence_first_screen(page, label):  # AC32
    sizes = page.evaluate("t => window.__c.withText(document.body, t).filter(e => window.__c.inView(e) && window.__c.whole(e) && window.__c.plain(e)).map(e => parseFloat(getComputedStyle(e).fontSize))", FICTION)
    if not sizes:
        fail(f"AC32 the sentence '{FICTION}' is not visible without scrolling at {label}")
    elif max(sizes) < 13:
        fail(f"AC32 the first-screen sentence is set at {max(sizes)}px, below 13px, at {label}")


def sentences(page, key, label):  # AC31 and AC77 (visible in the contact section, 14 px) AC57 and AC81 (visible in the footer) AC58 AC59, AC45-AC47 as displayed
    r = page.evaluate("""async ([notes, risk, read]) => { const c = window.__c, out = {notes: []};
      const seen = async e => { e.scrollIntoView({block: 'center', behavior: 'instant'});
        for (let i = 0; i < 15; i++) { await new Promise(r => requestAnimationFrame(() => r())); if (c.inView(e) && c.whole(e) && c.plain(e)) return true;
          await new Promise(r => setTimeout(r, 100)); } return false; };
      const con = c.sec('contact'), foot = [...document.querySelectorAll('footer')].filter(f => !f.closest('article')).pop();
      for (const t of notes) { const got = []; for (const e of con ? c.withText(con, t) : []) if (await seen(e)) got.push(parseFloat(getComputedStyle(e).fontSize)); out.notes.push(got); }
      out.foot = false; for (const e of foot ? c.withText(foot, risk) : []) if (await seen(e)) out.foot = true;
      out.read = []; for (const e of foot ? c.withText(foot, read) : []) if (await seen(e)) out.read.push(parseFloat(getComputedStyle(e).fontSize));
      out.contact = con ? con.innerText : null;  // innerText leaves out what is not displayed
      out.risk = c.withText(document.body, risk).filter(c.shown).map(e => [parseFloat(getComputedStyle(e).fontSize), c.contrast(e)]);
      scrollTo({top: 0, behavior: 'instant'}); return out; }""", [[FICTION, PE_NOTE] if key == "D" else [FICTION], RISK, READ_NOTE])
    for (ac, text), got in zip((("AC31", FICTION), ("AC77", PE_NOTE)), r["notes"]):
        if not got:
            fail(f"{ac} the sentence '{text}' is not visible in the contact section at {label}")
        elif max(got) < 14:
            fail(f"{ac} the sentence '{text}' in the contact section is set at {max(got)}px, below 14px, at {label}")
    if not r["foot"]:
        fail(f"AC57 the sentence '{RISK}' is not visible in the footer at {label}")
    if key != "D":
        if not r["read"]:
            fail(f"AC81 the sentence '{READ_NOTE}' is not visible in the footer at {label}")
        elif max(r["read"]) < 13:
            fail(f"AC81 the sentence '{READ_NOTE}' is set at {max(r['read'])}px, below 13px, at {label}")
    shown = r["contact"] or ""
    for ac, what, pat in (("AC45", "the 상담 hours as digits", r"\d{1,2}:\d{2}"), ("AC46", "the closed days", r"휴무|휴관|쉽니다|쉬어요|쉬는 날|쉼"),
                          ("AC47", "an address with '(가상 주소)'", r"\(가상 주소\)"), ("AC47", "the phone number 02-000-0000", r"02-000-0000")):
        if not re.search(pat, shown):
            fail(f"{ac} the contact section does not display {what} at {label}")
    for fs, con in r["risk"]:
        if fs < 13:
            fail(f"AC58 the sentence of AC57 is set at {fs}px, below 13px, at {label}")
        if con.get("err") or con["ratio"] < 4.5:
            fail(f"AC59 the sentence of AC57 has a contrast of {con.get('err') or round(con['ratio'], 2)} (text {con.get('fg')} on "
                 f"{con.get('bg')}), below 4.5:1, at {label}")


def contact_link(page, vp, sid, label):  # AC41 AC42, and at 390 AC43 AC44
    seen = page.evaluate("""sid => [...document.querySelectorAll('a[href="#' + sid + '"]')]
        .filter(a => /문의|상담/.test(a.textContent)).some(window.__c.inView)""", sid)
    if not seen:
        fail(f"{'AC41' if vp is DESKTOP else 'AC42'} no link to the contact section whose text contains 문의 or 상담 is "
             f"visible without scrolling at {label}")
    if vp is DESKTOP:
        return
    r = page.evaluate(EVERYWHERE, ["link", sid])
    if r["miss"]:
        fail(f"AC43 no 문의 · 상담 link to the contact section is on screen at scroll {r['miss'][:5]} px "
             f"({len(r['miss'])} positions) at 390px")
    page.evaluate("scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    last = page.evaluate_handle(LAST_FOOTER_TEXT).as_element()
    for _ in range(15):  # up to 1.5 s for a footer that fades or slides in
        if not last or last.evaluate(IN_VIEW):
            break
        page.wait_for_timeout(100)
    if not last:
        fail("AC44 no <footer> text to read at the end of the page (390px)")
    elif not last.evaluate(IN_VIEW) or last.evaluate(UNDER_BAR):
        fail(f"AC44 the footer's last text line is covered or off screen at the end of the page (390px): "
             f"{last.evaluate('e => e.textContent.trim().slice(0, 40)')}")
    page.evaluate("scrollTo(0, 0)")


def bars_cover(page):  # AC118, at 390
    r = page.evaluate("""async () => { const out = [], H = document.documentElement.scrollHeight;
      for (const y of [0, Math.max(0, (H - innerHeight) / 2)]) { scrollTo({top: y, behavior: 'instant'});
        await new Promise(r => setTimeout(r, 400)); out.push([Math.round(y), window.__c.cover()]); }
      scrollTo({top: 0, behavior: 'instant'}); return out; }""")
    for y, px in r:
        if px > 220:
            fail(f"AC118 fixed and sticky elements cover {px:.0f}px of the 390px screen's height at scroll {y}px, above 220px")


def no_overflow(target, label):  # AC96
    w = target.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    if w[0] > w[1]:
        fail(f"{label} horizontal overflow: scrollWidth {w[0]} > clientWidth {w[1]}")
    out = target.evaluate("""() => { const W = document.documentElement.clientWidth, out = [];  // overflow-x on <html>/<body> hides it, not removes it
      for (const e of document.body.querySelectorAll('*')) { const r = e.getBoundingClientRect();
        if (r.width < 1 || r.height < 1 || r.right <= W + 1 || getComputedStyle(e).visibility === 'hidden') continue;
        let cut = false;
        for (let a = e.parentElement; a && a !== document.body; a = a.parentElement)
          if (getComputedStyle(a).overflowX !== 'visible' && a.getBoundingClientRect().right <= W + 1) { cut = true; break; }
        if (!cut) out.push('<' + e.tagName.toLowerCase() + (e.className && e.className.baseVal === undefined ? '.' + e.className : '') + '> to ' + Math.round(r.right) + 'px'); }
      return out.slice(0, 5); }""")
    if out:
        fail(f"{label} elements reach past the right edge of the {w[1]}px page (overflow-x on html or body only hides them): {out}")


def keep_all(page, label):  # AC34, both widths
    bad = page.evaluate("""() => [...document.querySelectorAll('p, li, dd, dt, td, th, h1, h2, h3')]
      .filter(e => /[가-힣]/.test(e.textContent) && getComputedStyle(e).wordBreak !== 'keep-all')
      .map(e => e.textContent.trim().slice(0, 40))""")
    for t in bad[:8]:
        fail(f"AC34 Korean text without word-break: keep-all at {label}: {t}")


def font_responses(page):  # AC119: every web font request returns 200
    bad = []
    page.on("response", lambda r: any(h in r.url for h in FONT_HOSTS) and r.status != 200
            and bad.append(f"{r.status} {r.url}"))
    page.on("requestfailed", lambda r: any(h in r.url for h in FONT_HOSTS) and bad.append(f"failed {r.url}"))
    return bad


def web_font(page, selector, what, faces):  # AC119: the text renders in the sample's faces, loaded as web fonts
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
            fail(f"AC119 the {what} renders in {bad or 'no font'}, not only in the loaded web font {' / '.join(faces)} "
                 f"(a face did not load, a fallback drew some of the text, or a copy installed on the machine was used)")
    finally:
        cdp.detach()


def wordmark_name(page, slug, label):  # AC18: the accessible name Chrome computes (block children are joined with a space)
    cdp = page.context.new_cdp_session(page)
    try:
        cdp.send("DOM.enable")
        cdp.send("Accessibility.enable")
        root = cdp.send("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
        node = cdp.send("DOM.querySelector", {"nodeId": root, "selector": "header a.wordmark"})["nodeId"]
        nodes = cdp.send("Accessibility.getPartialAXTree", {"nodeId": node, "fetchRelatives": False})["nodes"] if node else []
        got = next((n.get("name", {}).get("value") for n in nodes if not n.get("ignored")), None)
        if got != SAMPLES[slug]["name"]:
            fail(f"AC18 the accessible name of the header wordmark is {got!r}, not {SAMPLES[slug]['name']!r}, at {label} "
                 f"(a name set in two block lines needs aria-label)")
    finally:
        cdp.detach()


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


DISPLAY_FACES = {"B": ("AC164", {"Grandiflora One": (400,), "Gowun Batang": (400, 700)}), "C": ("", {}),
                 "D": ("AC236", {"Orbit": (400,)})}


def faces(page, key, big, label):  # AC120 AC121 AC164 (B) AC236 (D)
    fam = page.evaluate("window.__c.fam(document.body)")
    want_face("AC120", f"the <body> at {label}", fam, *PRETENDARD)
    loaded = page.evaluate("[...document.fonts].map(f => f.family.replace(/^['\"]|['\"]$/g, ''))")
    if fam in PRETENDARD and fam not in loaded:  # the name of a copy installed on this machine: a visitor gets a fallback
        fail(f"AC120 the <body> family {fam!r} is not a family the linked stylesheets define at {label} "
             f"(they define {sorted(set(loaded))[:6]}); start the stack with the loaded name")
    rows = page.evaluate("""() => { const s = window.__c.sec('contact'); if (!s) return null; const out = [];
      const walk = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
      while (walk.nextNode()) { const t = walk.currentNode;
        if (/\\d{1,2}:\\d{2}|0\\d{1,2}-\\d{3,4}-\\d{4}/.test(t.nodeValue) && t.parentElement.getClientRects().length)
          out.push([t.nodeValue.trim().slice(0, 40), window.__c.fam(t.parentElement)]); }
      return out; }""")
    if not rows:
        fail(f"AC121 no visible 상담 hours or phone number in the contact section at {label}")
    for text, f in rows or []:
        if f not in PRETENDARD or f not in loaded:
            fail(f"AC121 {text!r} in the contact section has computed first family {f!r}, not a loaded Pretendard, at {label}")
    ac, want = DISPLAY_FACES[key]
    used = page.evaluate("""fams => [...document.body.querySelectorAll('*')].filter(e => fams.includes(window.__c.fam(e)) && e.getClientRects().length)
      .map(e => [window.__c.fam(e), +getComputedStyle(e).fontWeight, window.__c.own(e).slice(0, 24), e.tagName.toLowerCase()])""", list(want))
    for f, weight, own, tag in used:
        if weight not in want[f]:
            fail(f"{ac} a <{tag}> in {f} has font-weight {weight}, not {' or '.join(map(str, want[f]))}, at {label}: {own!r}")
        if re.search(r"\d", own):
            fail(f"{ac} a <{tag}> in {f} has a digit in its own text at {label}: {own!r}")


def contrast(page, label):  # AC98, on the whole page
    bad = page.evaluate("""() => { const c = window.__c, out = [];
      for (const e of document.body.querySelectorAll('*')) {
        if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE'].includes(e.tagName) || e.closest('svg') || !c.own(e) || !c.shown(e)) continue;
        let o = 1; for (let x = e; x; x = x.parentElement) o *= +getComputedStyle(x).opacity;
        if (o === 0) continue;
        const r = c.contrast(e), fs = parseFloat(getComputedStyle(e).fontSize), need = fs >= 24 && e.closest('h1, h2, h3, h4, h5, h6') ? 3 : 4.5;
        const tag = e.tagName.toLowerCase() + ' ' + JSON.stringify(c.own(e).slice(0, 24));
        if (r.err) out.push(tag + ': cannot judge, ' + r.err);
        else if (r.ratio < need) out.push(tag + ': contrast ' + r.ratio.toFixed(2) + ':1 below ' + need + ':1 (text ' + r.fg + ' on ' + r.bg + ', ' + fs + 'px)');
      }
      return out.slice(0, 15); }""")
    for b in bad:
        fail(f"AC98 at {label}: {b}")


FOCUS_SIG = """e => { const s = getComputedStyle(e); return [s.outlineStyle, s.outlineWidth, s.outlineColor, s.boxShadow, s.backgroundColor,
  s.borderTopColor, s.borderBottomColor, s.borderBottomWidth, s.textDecorationLine, s.color].join('|'); }"""


def focus_ring(page, label):  # AC101: every displayed link and focusable element shows an indicator on keyboard focus
    n = page.evaluate("""sig => { const f = new Function('return ' + sig)(); window.__focus = new Map(); let n = 0;
      for (const e of document.querySelectorAll('a[href], [tabindex]')) if (e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden'
          && e.getAttribute('tabindex') !== '-1') { window.__focus.set(e, {before: f(e), hit: false}); n++; }
      document.activeElement && document.activeElement.blur(); scrollTo(0, 0); return n; }""", FOCUS_SIG)
    bad = []
    for _ in range(n + 3):
        page.keyboard.press("Tab")
        r = page.evaluate("""sig => { const f = new Function('return ' + sig)(), e = document.activeElement, m = window.__focus.get(e); if (!m) return null;
          m.hit = true; const s = getComputedStyle(e), ring = s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 1
            && (window.__c.rgba(s.outlineColor) || [0, 0, 0, 1])[3] > 0;
          return {ok: e.matches(':focus-visible') && (ring || f(e) !== m.before), text: e.textContent.trim().slice(0, 24)}; }""", FOCUS_SIG)
        if r and not r["ok"]:
            bad.append(r["text"])
    missed = page.evaluate("[...window.__focus].filter(([e, m]) => !m.hit).map(([e]) => e.textContent.trim().slice(0, 24))")
    page.evaluate("document.activeElement && document.activeElement.blur(); scrollTo(0, 0)")
    for t in dict.fromkeys(bad):
        fail(f"AC101 the link {t!r} shows no focus indicator (an outline, or a change of colour, border or shadow) on keyboard focus at {label}")
    if missed:
        fail(f"AC101 displayed links the Tab key does not reach at {label}: {missed[:6]}")


FIRST_LINKS = """() => { const c = window.__c, f = c.first(); if (!f) return null;
  return f.filter(e => e.tagName === 'A' && c.shown(e)).map(c.info); }"""


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


def strip(page, ac, bg, fg, label):  # the strip: the bar pinned to the top that holds the AC12 marker
    W, _ = size(page)
    tops = [b for b in page.evaluate("window.__c.barInfo()") if b["side"] == "top" and b["marker"]]
    if len(tops) != 1:
        fail(f"{ac} expected one bar pinned to the top of the viewport that holds the sample marker at {label}, found {len(tops)}")
        return
    b = tops[0]
    if b["box"][0] > 0.5 or b["box"][2] < W - 0.5 or b["box"][1] > 0.5 or rgb(b["bg"]) != bg or (fg and rgb(b["color"]) != fg):
        fail(f"{ac} the strip (box {rnd(b['box'])}, background {b['bg']}, colour {b['color']}) must sit at the top edge, span the "
             f"full width and have the background {hexs(bg)}{' and the text colour ' + hexs(fg) if fg else ''} at {label}")


def bottom_bars(page):
    return [b for b in page.evaluate("window.__c.barInfo()") if b["side"] == "bottom"]


def link_is(x, text, sid):
    return x["text"] == text and x["href"] == f"#{sid}"


def says(x, text):  # by its text or by its accessible name, so an icon link labelled with the text counts too
    return text in (x["text"], x["name"])


# --- sample B ----------------------------------------------------------------------------------------------

B_PARTS = """() => { const c = window.__c, h1 = document.querySelector('h1'), out = {panel: null}; if (!h1) return null;
  let p = null; for (let e = h1.parentElement; e && e !== document.body; e = e.parentElement) { const g = c.rgba(getComputedStyle(e).backgroundColor);
    if (g && g[3] >= 1 && g.slice(0, 3).join() === '18,53,36') { p = e; break; } }
  const imgs = [...document.images];
  out.frames = imgs.map(i => ({...c.info(i), inFirst: (c.firstAll() || []).includes(i)}));
  if (imgs.length === 2) { const a = c.box(imgs[0]), b = c.box(imgs[1]);
    const o = [Math.max(a[0], b[0]), Math.max(a[1], b[1]), Math.min(a[2], b[2]), Math.min(a[3], b[3])]; out.overlap = o;
    out.frontOnTop = o[2] > o[0] && o[3] > o[1] && c.stackAt((o[0] + o[2]) / 2, (o[1] + o[3]) / 2)[0] === imgs[1]; }
  const sp = h1.querySelector(':scope > span');
  if (sp) { const g = document.createRange(); g.selectNodeContents(sp); out.spanLines = new Set([...g.getClientRects()].filter(r => r.width && r.height).map(r => Math.round(r.top))).size; }
  out.span = c.info(sp); out.em = c.info(h1.querySelector(':scope > em')); out.h1 = c.info(h1);
  if (!p) return out;
  out.panel = {box: c.box(p),
    svgs: [...p.querySelectorAll('svg')].map(v => ({hidden: v.getAttribute('aria-hidden'), box: c.box(v), opacity: +getComputedStyle(v).opacity})),
    rules: [...p.querySelectorAll('[aria-hidden="true"]')].filter(e => !e.closest('svg') && !e.textContent.trim() && e.getClientRects().length)
      .map(e => ({box: c.box(e), bg: c.rgba(getComputedStyle(e).backgroundColor)}))};
  return out; }"""

B_COLUMNS = """() => { const c = window.__c, s = c.sec('services'); if (!s) return null; const uls = [...s.querySelectorAll('ul')];
  return {behind: c.behind(s), uls: uls.length, cols: uls.length === 1 ? [...uls[0].children].map(li => ({tag: li.tagName.toLowerCase(), box: c.box(li),
    heads: li.querySelectorAll('h3, h4').length, ps: li.querySelectorAll('p').length})) : []}; }"""


def b_common(page, vp, label):  # AC130 AC133 AC134 AC135 AC145 AC160, both widths
    W, _ = size(page)
    strip(page, "AC130", STRAW, INK_B, label)
    wm = info(page, "header a.wordmark")
    if not wm:
        fail(f"AC133-AC135 no header a.wordmark at {label}")
    else:
        centre = (wm["ext"][0] + wm["ext"][2]) / 2
        if abs(centre - W / 2) > 24:
            fail(f"AC133 the wordmark text's centre is at {centre:.0f}px, more than 24px from {W / 2:.0f}px, at {label}")
        want_face("AC134", f"the header wordmark at {label}", wm["fam"], "Gowun Batang")
        want_color("AC134", f"the header wordmark's colour at {label}", wm["color"], GREEN)
        lo, hi = (20, 24) if vp is DESKTOP else (16, 19)
        if wm["weight"] != 700 or not lo <= wm["fs"] <= hi:
            fail(f"AC134 the header wordmark is set at {wm['fs']}px, weight {wm['weight']}, at {label}; it needs {lo}-{hi}px and 700")
        if wm["ls"] < 0.25 * wm["fs"] - 0.01:
            fail(f"AC135 the header wordmark's letter-spacing is {wm['ls']}px, below 0.25 x its font-size {wm['fs']}px, at {label}")
    p = page.evaluate(B_PARTS)
    span, em = (p or {}).get("span"), (p or {}).get("em")
    if not span or not em:
        fail(f"AC145 the <h1> has no child <span> or no child <em> at {label}")
    elif em["fam"] != "Gowun Batang" or em["weight"] != 400 or em["style"] != "italic" or rgb(em["color"]) != STRAW \
            or em["display"] != "block" or em["fs"] < 1.6 * span["fs"] - 0.01:
        fail(f"AC145 the <em> of the <h1> ({em['fam']!r}, weight {em['weight']}, {em['style']}, colour {em['color']}, display "
             f"{em['display']}, {em['fs']}px beside a {span['fs']}px <span>) needs Gowun Batang, 400, italic, #e3cf8e, display "
             f"block and 1.6 x the <span>'s size or more, at {label}")
    cols = page.evaluate(B_COLUMNS)
    if not cols:
        fail(f"AC160 no single service section at {label}")
        return
    boxes = [k["box"] for k in cols["cols"]]
    if rgb(cols["behind"]) != CREAM or cols["uls"] != 1 or len(boxes) != 3 or any(k["tag"] != "li" or k["heads"] != 1 or k["ps"] != 1 for k in cols["cols"]):
        fail(f"AC160 the service section needs the background #f3eee2 behind it (is {cols['behind']}) and one <ul> of exactly "
             f"three <li>, each with one heading and one <p> (found {cols['uls']} <ul>, {[(k['tag'], k['heads'], k['ps']) for k in cols['cols']]}) at {label}")
    elif vp is DESKTOP:
        row = sorted(boxes)
        if max(b[1] for b in boxes) - min(b[1] for b in boxes) > 4 or any(b[0] < a[2] - 1 for a, b in zip(row, row[1:])):
            fail(f"AC160 the three service columns must share a top edge within 4px and not overlap in width at 1440px: {[rnd(b) for b in boxes]}")
    elif not stacked(boxes):
        fail(f"AC160 the three service columns do not stack in one column at 390px: {[rnd(b) for b in boxes]}")


def b_desktop(page, sid):  # AC131 AC132 AC136-AC139 AC141 AC143 AC144 AC146 AC148 AC150-AC154
    W, H = size(page)
    head, wm, nav = (info(page, s) for s in ("header", "header a.wordmark", "header nav"))
    p = page.evaluate(B_PARTS)
    if not head or not wm or not nav or not p:
        fail("AC131-AC154 a <header>, its a.wordmark, its <nav> or the <h1> is missing")
        return
    hb = head["box"]
    if hb[0] > 0.5 or hb[2] < W - 0.5 or rgb(head["bg"]) != CREAM or not 110 <= high(hb) <= 180 or head["position"] in ("fixed", "sticky"):
        fail(f"AC131 the <header> (box {rnd(hb)}, background {head['bg']}, position {head['position']}) must span the full "
             f"width, have the background #f3eee2, be 110-180px tall and not be fixed or sticky")
    if wm["ext"][3] > nav["box"][1] + 0.5 or nav["box"][0] > 64:
        fail(f"AC132 the wordmark's bottom edge ({wm['ext'][3]:.0f}px) must be above the <nav>'s top edge ({nav['box'][1]:.0f}px), "
             f"and the <nav>'s left edge ({nav['box'][0]:.0f}px) within 64px of the left")
    links = page.evaluate("[...document.querySelectorAll('header a')].map(window.__c.info)")
    ask = [x for x in links if says(x, ASK)]
    if len(ask) != 1 or not link_is(ask[0], ASK, sid) or not ask[0]["shown"]:
        fail(f"AC136 the <header> needs exactly one link with the text '{ASK}' (by text or accessible name), to #{sid} and "
             f"displayed at 1440px (found {len(ask)})")
    else:
        x = ask[0]
        if not clear(x["bg"]) or any(b[0] != "solid" or b[1] < 1 or rgb(b[2]) != GREEN for b in x["border"]) or max(x["radius"]) > 0 \
                or W - x["box"][2] > 64 or x["box"][2] > W or x["box"][1] >= nav["box"][1]:
            fail(f"AC136 the '{ASK}' link (background {x['bg']}, borders {x['border']}, radius {x['radius']}, box {rnd(x['box'])}) "
                 f"needs a transparent background, four solid #123524 borders of 1px or more, no radius, its right edge "
                 f"within 64px of the right and its top edge above the <nav>'s ({nav['box'][1]:.0f}px)")
    panel = p["panel"]
    if not panel:
        fail("AC137 no ancestor of the <h1> has the background #123524 (the panel); AC138-AC153 did not run")
        return
    pb = panel["box"]
    if pb[0] > 0.5 or pb[2] < W - 0.5 or abs(pb[1] - hb[3]) > 2:
        fail(f"AC137 the panel {rnd(pb)} must span the full width and start within 2px of the <header>'s bottom ({hb[3]:.0f}px)")
    if not 680 <= pb[3] <= 840:
        fail(f"AC138 the panel's bottom edge is {pb[3]:.0f}px from the top, not 680-840px")
    svgs = panel["svgs"]
    if len(svgs) != 1 or svgs[0]["hidden"] != "true" or wide(svgs[0]["box"]) < 0.9 * wide(pb) or high(svgs[0]["box"]) < 0.9 * high(pb) \
            or not 0.04 <= svgs[0]["opacity"] <= 0.2:
        fail(f"AC139 the panel needs exactly one inline <svg aria-hidden=\"true\">, at least 90 % as wide and as tall as the "
             f"panel, with an opacity of 0.04-0.2 (found {[(s['hidden'], rnd(s['box']), s['opacity']) for s in svgs]}, panel {rnd(pb)})")
    h1, span = p["h1"], p["span"]
    if not within(h1["box"], pb) or not inside_viewport(h1["box"], W, H) or not 48 <= h1["ext"][0] <= 160 or h1["ext"][2] > 700:
        fail(f"AC141 the <h1> (box {rnd(h1['box'])}, text {h1['ext'][0]:.0f}-{h1['ext'][2]:.0f}px) must lie inside the panel and the "
             f"viewport, start 48-160px from the left and end at most 700px from it")
    if span:
        if span["fam"] != "Grandiflora One" or span["weight"] != 400 or rgb(span["color"]) != CREAM or not 38 <= span["fs"] <= 52:
            fail(f"AC143 the <span> of the <h1> ({span['fam']!r}, weight {span['weight']}, colour {span['color']}, {span['fs']}px) "
                 f"needs Grandiflora One, 400, #f3eee2 and 38-52px")
        if not 3.0 <= high(span["box"]) / span["fs"] <= 7.0 or p.get("spanLines") not in (3, 4):
            fail(f"AC144 the <span> of the <h1> is {high(span['box']) / span['fs']:.2f} x its font-size tall in {p.get('spanLines')} line(s), "
                 f"not 3.0-7.0 in three or four lines")
    rules = [r for r in panel["rules"] if wide(r["box"]) <= 3 and high(r["box"]) >= 120 and rgb(r["bg"]) == STRAW]
    if len(rules) != 1 or not 8 <= h1["ext"][0] - rules[0]["box"][2] <= 40 or abs(rules[0]["box"][1] - h1["ext"][1]) > 24:
        fail(f"AC146 the panel needs exactly one rule (aria-hidden, no text, at most 3px wide, 120px tall or more, #e3cf8e), "
             f"8-40px left of the <h1> text ({h1['ext'][0]:.0f}px) and within 24px of its top ({h1['ext'][1]:.0f}px) "
             f"(found {[rnd(r['box']) for r in panel['rules']]})")
    links = first_links(page, "AC148")
    if links:
        fail(f"AC148 the first section holds a link outside the header and the bars: {[x['text'] for x in links]}")
    fr = p["frames"]
    if len(fr) != 2 or not all(f["inFirst"] for f in fr):
        fail(f"AC149 the page needs exactly two <img>, both before the service section (found {len(fr)}); AC150-AC154 did not run")
        return
    back, front, o = fr[0]["box"], fr[1]["box"], p["overlap"]
    for f, what in zip(fr, ("back", "front")):
        if "grayscale(1)" not in f["filter"] or max(f["radius"]) > 0:
            fail(f"AC150 the {what} frame has the filter {f['filter']!r} and radius {f['radius']}; it needs grayscale(1) and no radius")
        if wide(f["box"]) < 320 or high(f["box"]) < 380 or f["box"][0] < 640:
            fail(f"AC151 the {what} frame {rnd(f['box'])} must be 320px wide and 380px tall or more and start 640px or more from the left")
    if o[2] - o[0] < 80 or o[3] - o[1] < 200 or front[0] > back[0] - 80 or front[1] < back[1] + 40 or not p["frontOnTop"]:
        fail(f"AC152 the frames (back {rnd(back)}, front {rnd(front)}) must overlap by 80px in width and 200px in height or more, "
             f"the front one starting 80px or more left of and 40px or more below the back one, and lying on top at the "
             f"centre of the overlap (on top: {p['frontOnTop']})")
    if not pb[1] <= back[1] <= pb[3] or front[3] < pb[3] + 24 or front[3] > H + 0.5:
        fail(f"AC153 the back frame's top ({back[1]:.0f}px) must be inside the panel ({pb[1]:.0f}-{pb[3]:.0f}px), and the front "
             f"frame's bottom ({front[3]:.0f}px) 24px or more below the panel's and inside the {H}px viewport")
    if front[0] < h1["ext"][2] + 24:
        fail(f"AC154 the front frame's left edge ({front[0]:.0f}px) is less than 24px right of the <h1> text ({h1['ext'][2]:.0f}px)")


def b_mobile(page, sid):  # AC156-AC159, AC148 at 390
    W, H = size(page)
    links = first_links(page, "AC148")
    if links:
        fail(f"AC148 at 390px the first section holds a link outside the header and the bars: {[x['text'] for x in links]}")
    head = info(page, "header")
    navs = page.evaluate("[...document.querySelectorAll('header nav a')].filter(window.__c.inView).map(window.__c.box)")
    row = max((sum(1 for b in navs if abs(b[1] - a[1]) <= 4) for a in navs), default=0)
    asks = page.evaluate("t => [...document.querySelectorAll('header a')].filter(a => [a.textContent.trim(), a.getAttribute('aria-label')].includes(t) && a.getClientRects().length).length", ASK)
    if not head or high(head["box"]) > 130 or row < 3 or asks:
        fail(f"AC156 at 390px the <header> must be at most 130px tall (is {head and round(high(head['box']))}px), show three or "
             f"more <nav> links in one row (shows {row}) and not display its '{ASK}' link (displayed: {asks})")
    bars = bottom_bars(page)
    if len(bars) != 1 or rgb(bars[0]["bg"]) is None or len(bars[0]["links"]) != 1 or not link_is(bars[0]["links"][0], ASK, sid):
        fail(f"AC157 at 390px one bar is pinned to the bottom, with an opaque background colour and exactly one link, "
             f"'{ASK}' to #{sid} (found {[(b['tag'], b['bg'], [(x['text'], x['href']) for x in b['links']]) for b in bars]})")
    p = page.evaluate(B_PARTS)
    if not p or not p["span"] or p["span"]["fs"] < 26:
        fail(f"AC158 the <span> of the <h1> is set at {p and p['span'] and p['span']['fs']}px at 390px, below 26px")
    h1_on_load(page, "AC158", 0, "390px")
    fr = (p or {}).get("frames") or []
    if len(fr) != 2 or not bars:
        fail("AC159 two <img> frames and the bottom bar are needed at 390px")
        return
    o, top = p["overlap"], min(fr, key=lambda f: f["box"][1])["box"]
    seen = min(top[3], bars[0]["box"][1]) - top[1]
    if any(not f["shown"] or f["box"][1] < p["h1"]["box"][3] - 0.5 or wide(f["box"]) < 200 for f in fr) or o[2] - o[0] < 40 or o[3] - o[1] < 40 \
            or top[1] > 660 or seen < 100:
        fail(f"AC159 at 390px both frames ({[rnd(f['box']) for f in fr]}) must be displayed below the <h1> (bottom "
             f"{p['h1']['box'][3]:.0f}px), be 200px wide or more and overlap by 40px or more each way; the higher one starts at most "
             f"660px down and shows 100px or more above the bottom bar (shows {seen:.0f}px)")


# --- sample C ----------------------------------------------------------------------------------------------

C_PARTS = """() => { const c = window.__c, out = {};
  const blocks = [...document.body.querySelectorAll('*')].filter(e => c.shown(e) && getComputedStyle(e).backgroundImage.startsWith('linear-gradient'));
  blocks.sort((a, b) => a.getBoundingClientRect().width - b.getBoundingClientRect().width);
  const stops = e => (getComputedStyle(e).backgroundImage.match(/rgba?\\([^)]*\\)/g) || []).map(c.rgba);
  out.blocks = blocks.map(e => ({box: c.box(e), stops: stops(e), image: getComputedStyle(e).backgroundImage}));
  const wm = document.querySelector('header a.wordmark'), nav = document.querySelector('header nav'), h1 = document.querySelector('h1');
  const img = document.images.length === 1 ? document.images[0] : null, head = document.querySelector('header');
  out.head = c.info(head); out.wm = c.info(wm); out.nav = c.info(nav); out.h1 = c.info(h1); out.img = c.info(img); out.imgs = document.images.length;
  out.navLinks = nav ? [...nav.querySelectorAll('a')].map(a => ({...c.info(a), seen: c.inView(a)})) : [];
  out.spans = h1 ? {own: c.own(h1), kids: [...h1.children].map(k => ({tag: k.tagName.toLowerCase(), ...c.info(k)}))} : null;
  if (blocks.length === 2) { const [n, w] = blocks;
    out.narrow = {hasWm: !!wm && n.contains(wm), texts: [n, ...n.querySelectorAll('*')].filter(e => c.own(e) && c.shown(e) && !(wm && wm.contains(e))).map(e => c.own(e).slice(0, 20)),
      links: [...n.querySelectorAll('a')].filter(a => a !== wm).length};
    out.wide = {hasNav: !!nav && w.contains(nav), hasH1: !!h1 && w.contains(h1),
      notes: c.withText(w, '__FICTION__').filter(c.shown).map(c.info),
      links: [...w.querySelectorAll('a')].filter(a => c.shown(a) && !(nav && nav.contains(a))).length};
    const bars = c.bars().map(b => b.el);
    out.onPhoto = !img ? null : [...document.body.querySelectorAll('*')].filter(e => { if (!c.own(e) || !c.shown(e) || e.closest('svg')) return false;
        if (n.contains(e) || w.contains(e) || bars.some(b => b.contains(e))) return false; const x = c.ext(e), r = c.box(img);
        return Math.min(x[2], r[2]) - Math.max(x[0], r[0]) > 1 && Math.min(x[3], r[3]) - Math.max(x[1], r[1]) > 1; }).map(e => c.own(e).slice(0, 24)); }
  const st = document.querySelector('p.statement'), svc = c.sec('services');
  out.statement = st ? {...c.info(st), behind: c.behind(st), lines: new Set([...(() => { const g = document.createRange(); g.selectNodeContents(st); return g.getClientRects(); })()].map(r => Math.round(r.top))).size,
    placed: !!img && !!svc && !!(img.compareDocumentPosition(st) & Node.DOCUMENT_POSITION_FOLLOWING) && !!(st.compareDocumentPosition(svc) & Node.DOCUMENT_POSITION_FOLLOWING)} : null;
  out.list = svc ? [...svc.querySelectorAll('ul')].map(u => [...u.children].filter(k => k.tagName === 'LI').map(c.info)) : [];
  return out; }""".replace("__FICTION__", FICTION)


def c_common(page, vp, sid, label):  # AC170-AC173 AC179 AC180 AC186 AC188 AC189 AC196, both widths; returns the parts
    W, H = size(page)
    p = page.evaluate(C_PARTS)
    bars = page.evaluate("window.__c.barInfo()")
    if [b for b in bars if b["side"] == "top"] or not p["head"] or not clear(p["head"]["bg"]) or p["head"]["bgImage"] != "none":
        fail(f"AC170 no bar may be pinned to the top (found {[b['tag'] for b in bars if b['side'] == 'top']}) and the <header>'s "
             f"background must be transparent (is {p['head'] and p['head']['bg']}) at {label}")
    low = [b for b in bars if b["side"] == "bottom"]
    bar = low[0] if len(low) == 1 else None
    if not bar or bar["box"][0] > 0.5 or bar["box"][2] < W - 0.5 or rgb(bar["bg"]) != INK_C or not bar["marker"] \
            or len(bar["links"]) != 1 or not link_is(bar["links"][0], ASK, sid):
        fail(f"AC171 one bar is pinned to the bottom at {label}: full width, background #211a16, holding the sample marker and "
             f"exactly one link, '{ASK}' to #{sid} (found {[(b['tag'], rnd(b['box']), b['bg'], b['marker'], [(x['text'], x['href']) for x in b['links']]) for b in low]})")
    limit = 72 if vp is DESKTOP else 120
    if bar and high(bar["box"]) > limit:
        fail(f"AC172 the bottom bar is {high(bar['box']):.0f}px tall at {label}, above {limit}px")
    if len(p["blocks"]) != 2:
        fail(f"{'AC173' if vp is DESKTOP else 'AC192'} expected exactly two displayed elements with a linear-gradient "
             f"background-image (the blocks) at {label}, found {len(p['blocks'])}; the block checks did not run")
        return None
    for b in p["blocks"] if vp is DESKTOP else []:
        if any(not s or s[3] < 1 for s in b["stops"]) or {tuple(round(v) for v in s[:3]) for s in b["stops"] if s} != STOPS_C:
            fail(f"AC173 a block's gradient is {b['image'][:80]} at {label}; its colour stops must be rgb(181, 83, 58) and rgb(143, 58, 36) only")
    narrow, wideb = (b["box"] for b in p["blocks"])
    wm = p["wm"]
    if not wm:
        fail(f"AC179 no header a.wordmark at {label}")
    else:
        lo, hi = (38, 46) if vp is DESKTOP else (20, 23)
        if wm["fam"] not in PRETENDARD or wm["weight"] < 700 or rgb(wm["color"]) != WHITE or not lo <= wm["fs"] <= hi:
            fail(f"AC179 the header wordmark ({wm['fam']!r}, weight {wm['weight']}, colour {wm['color']}, {wm['fs']}px) needs "
                 f"Pretendard, 700 or more, #ffffff and {lo}-{hi}px at {label}")
        if not 1.9 <= high(wm["box"]) / wm["fs"] <= 2.7:
            fail(f"AC180 the header wordmark's box is {high(wm['box']) / wm['fs']:.2f} x its font-size tall at {label}, not 1.9-2.7 (two lines)")
    notes = [n for n in p["wide"]["notes"] if rgb(n["color"]) == WHITE and p["h1"] and n["box"][1] >= p["h1"]["box"][3] - 0.5 and within(n["box"], wideb)]
    if not notes or p["wide"]["links"]:
        fail(f"AC186 the wide block must hold the sentence of AC32 below the <h1> in #ffffff, and no link outside the <nav> "
             f"(sentence found: {len(notes)}, links outside the <nav>: {p['wide']['links']}) at {label}")
    img = p["img"]
    if not img:
        fail(f"AC187 the page needs exactly one <img> (found {p['imgs']}); AC188 AC189 did not run at {label}")
    else:
        ib = img["box"]
        if ib[0] > 0.5 or ib[2] < W - 0.5 or ib[1] > 4 or (bar and ib[3] < bar["box"][1] - 0.5) or not within(narrow, ib) or not within(wideb, ib):
            fail(f"AC188 the photo {rnd(ib)} must span the full width, start at most 4px down, reach the bottom bar's top edge "
                 f"({bar and round(bar['box'][1])}px) and hold both blocks ({rnd(narrow)}, {rnd(wideb)}) at {label}")
        if p["onPhoto"]:
            fail(f"AC189 text lies on the photo outside the two blocks and the bars at {label}: {p['onPhoto'][:5]}")
    st = p["statement"]
    need = 30 if vp is DESKTOP else 20
    if not st or not st["placed"] or st["lines"] < 2 or st["fs"] < need or rgb(st["behind"]) != PAGE_C:
        fail(f"AC196 the statement (<p class=\"statement\">) must come after the photo and before the service section, run over "
             f"two lines or more at {need}px or more on #fdfbf8 at {label} (found {st and (st['placed'], st['lines'], st['fs'], st['behind'])})")
    return p, narrow, wideb, bar


def c_desktop(page, sid, parts):  # AC174-AC178 AC181-AC185 AC197
    W, H = size(page)
    p, narrow, wideb, _ = parts
    if abs(narrow[0]) > 0.5 or abs(narrow[1]) > 0.5 or not 380 <= wide(narrow) <= 480 or not 250 <= high(narrow) <= 340:
        fail(f"AC174 the narrow block {rnd(narrow)} must start at the top left corner and be 380-480px wide and 250-340px tall")
    if abs(wideb[1]) > 0.5 or abs(wideb[0] - narrow[2]) > 2 or abs(wideb[2] - W) > 0.5:
        fail(f"AC175 the wide block {rnd(wideb)} must start at the top edge, within 2px of the narrow block's right edge "
             f"({narrow[2]:.0f}px), and end at the right edge of the viewport")
    if not 370 <= high(wideb) <= 480 or high(wideb) < high(narrow) + 80:
        fail(f"AC176 the wide block is {high(wideb):.0f}px tall; it needs 370-480px and 80px or more above the narrow block's {high(narrow):.0f}px")
    if not p["narrow"]["hasWm"] or p["narrow"]["texts"] or p["narrow"]["links"]:
        fail(f"AC177 the narrow block must hold the header wordmark and no other text or link (wordmark inside: "
             f"{p['narrow']['hasWm']}, other text {p['narrow']['texts']}, other links {p['narrow']['links']})")
    wm, nav, h1 = p["wm"], p["nav"], p["h1"]
    if wm:
        centre = (wm["ext"][1] + wm["ext"][3]) / 2
        if wm["ext"][0] > 64 or not 160 <= centre <= 300:
            fail(f"AC178 the wordmark text starts {wm['ext'][0]:.0f}px from the left with its vertical centre at {centre:.0f}px; "
                 f"it needs at most 64px and 160-300px")
    links = p["navLinks"]
    if not nav or not p["wide"]["hasNav"] or not within(nav["box"], wideb) or W - nav["box"][2] > 64 or nav["box"][1] > 100 \
            or len(links) < 4 or not link_is(links[-1], ASK, sid):
        fail(f"AC181 the <nav> (box {nav and rnd(nav['box'])}) must lie inside the wide block, end within 64px of the right edge, "
             f"start at most 100px down and hold four or more links, the last one '{ASK}' to #{sid} "
             f"(links {[(x['text'], x['href']) for x in links]})")
    for x in links:
        if rgb(x["color"]) != WHITE or not clear(x["bg"]) or any(b[0] != "none" and b[1] > 0 for b in x["border"]):
            fail(f"AC182 the <nav> link {x['text']!r} (colour {x['color']}, background {x['bg']}) needs #ffffff, a transparent "
                 f"background and no border")
    sp = p["spans"]
    if not sp or sp["own"] or [k["tag"] for k in sp["kids"]] != ["span"] * 3 or any(k["display"] != "block" for k in sp["kids"]):
        fail("AC183 the <h1> needs exactly three child <span> elements with display block and no text outside them")
    else:
        for k in sp["kids"]:
            if high(k["box"]) > 1.5 * k["fs"]:
                fail(f"AC183 the <h1> line {k['text']!r} is {high(k['box']) / k['fs']:.2f} x its font-size tall, above 1.5 (it wraps)")
    if h1:
        if h1["fam"] not in PRETENDARD or not 400 <= h1["weight"] <= 500 or rgb(h1["color"]) != WHITE or not 44 <= h1["fs"] <= 60:
            fail(f"AC184 the <h1> ({h1['fam']!r}, weight {h1['weight']}, colour {h1['color']}, {h1['fs']}px) needs Pretendard, "
                 f"400-500, #ffffff and 44-60px")
        if not p["wide"]["hasH1"] or not within(h1["box"], wideb) or not 40 <= h1["ext"][0] - wideb[0] <= 120 or (nav and h1["box"][1] < nav["box"][3] - 0.5):
            fail(f"AC185 the <h1> (box {rnd(h1['box'])}, text from {h1['ext'][0]:.0f}px) must lie inside the wide block, start "
                 f"40-120px right of its left edge ({wideb[0]:.0f}px) and below the <nav> ({nav and round(nav['box'][3])}px)")
    lists = [u for u in p["list"] if len(u) >= 4]
    if not lists or any(wide(li["box"]) < 0.6 * W or not any(b[0] == "solid" and b[1] >= 1 for b in (li["border"][0], li["border"][2])) for li in lists[0]):
        fail(f"AC197 the service section needs a <ul> of four or more <li>, each 60 % of the viewport wide or more with a "
             f"solid top or bottom border (found {[[round(wide(li['box'])) for li in u] for u in p['list']]})")


def c_mobile(page, sid, parts):  # AC192-AC195
    W, H = size(page)
    p, narrow, wideb, bar = parts
    if abs(narrow[0]) > 0.5 or abs(narrow[1]) > 0.5 or not 100 <= wide(narrow) <= 140 or not 170 <= high(narrow) <= 240 \
            or abs(wideb[0] - narrow[2]) > 2 or abs(wideb[2] - W) > 0.5 or abs(wideb[1]) > 0.5 or high(wideb) < high(narrow) + 60 or wideb[3] > 500:
        fail(f"AC192 at 390px the narrow block {rnd(narrow)} must sit at the top left, 100-140px wide and 170-240px tall; the wide "
             f"block {rnd(wideb)} runs from its right edge to the right edge of the viewport from the top, is 60px or more "
             f"taller and ends at most 500px down")
    h1 = p["h1"]
    if not h1 or h1["fs"] < 22 or not within(h1["box"], wideb) or not inside_viewport(h1["box"], W, H):
        fail(f"AC193 at 390px the <h1> ({h1 and h1['fs']}px, box {h1 and rnd(h1['box'])}) must be set at 22px or more and lie "
             f"inside the wide block and the viewport")
    seen = [x for x in p["navLinks"] if x["seen"] and within(x["box"], wideb) and h1 and x["box"][3] <= h1["box"][1] + 0.5]
    asks = [x for x in seen if link_is(x, ASK, sid)]
    row = max((sum(1 for b in seen if abs(b["box"][1] - a["box"][1]) <= 4) for a in asks), default=0)  # the row of the 상담 문의 link
    if row < 3:
        fail(f"AC194 at 390px three or more <nav> links, '{ASK}' among them, must be visible in one row inside the wide block "
             f"above the <h1> (visible: {[x['text'] for x in seen]})")
    img = p["img"]
    if img and bar:
        free = min(img["box"][3], bar["box"][1]) - max(wideb[3], img["box"][1])
        if free < 220:
            fail(f"AC195 at 390px {free:.0f}px of the photo shows between the wide block ({wideb[3]:.0f}px) and the bottom bar "
                 f"({bar['box'][1]:.0f}px), below 220px")


# --- sample D ----------------------------------------------------------------------------------------------

D_PARTS = """() => { const c = window.__c, out = {}, svc = c.sec('services'), con = c.sec('contact');
  const head = document.querySelector('header'), wm = document.querySelector('header a.wordmark'), nav = document.querySelector('header nav'), h1 = document.querySelector('h1');
  out.head = c.info(head); out.wm = c.info(wm); out.nav = c.info(nav); out.h1 = c.info(h1);
  out.navLinks = nav ? [...nav.querySelectorAll('a')].map(c.info) : [];
  out.headLinks = head ? [...head.querySelectorAll('a')].filter(a => a !== wm && !(nav && nav.contains(a))).map(c.info) : [];
  out.behindWm = wm ? (() => { const x = c.ext(wm); return c.bgAt((x[0] + x[2]) / 2, (x[1] + x[3]) / 2, false); })() : null;
  out.rightOfWm = head && wm ? [...head.querySelectorAll('*')].filter(e => c.shown(e) && !e.contains(wm) && !wm.contains(e) && c.box(e)[0] >= c.ext(wm)[2] - 0.5)
    .map(e => e.tagName.toLowerCase() + ' ' + e.textContent.trim().slice(0, 16)) : [];
  out.svgs = (c.firstAll() || []).filter(e => e.tagName.toLowerCase() === 'svg' && e.getAttribute('aria-hidden') === 'true' && !e.closest('a')).map(e => ({box: c.box(e), shown: c.shown(e)}));
  let sheet = null; for (let e = svc; e && e !== document.body; e = e.parentElement) { const g = c.rgba(getComputedStyle(e).backgroundColor);
    if (g && g[3] >= 1 && g.slice(0, 3).join() === '251,249,255') { sheet = e; break; } }
  if (sheet) { const b = c.box(sheet); out.sheet = {box: b, radius: c.radius(sheet), docTop: b[1] + scrollY, above: c.bgAt((b[0] + b[2]) / 2, b[1] - 6, true),
      tags: [...sheet.querySelectorAll('ul.tags > li')].map(t => ({...c.info(t), link: !!(t.closest('a') || t.querySelector('a'))})),
      cards: [...sheet.querySelectorAll('.card')].map(k => ({...c.info(k), heads: k.querySelectorAll('h3, h4').length, ps: k.querySelectorAll('p').length}))}; }
  if (con) { const names = ['카카오톡', '전화', '네이버 예약', '네이버 지도'];
    const links = names.map(n => [...con.querySelectorAll('a')].find(a => (a.getAttribute('aria-label') || a.textContent).includes(n))).filter(Boolean);
    out.contact = {box: c.box(con), bg: c.rgba(getComputedStyle(con).backgroundColor), color: c.rgba(getComputedStyle(con).color),
      links: links.map(a => ({...c.info(a), li: a.closest('li') ? c.info(a.closest('li')) : null})),
      oneList: links.length === 4 && links.every(a => a.closest('li') && a.closest('li').parentElement === links[0].closest('li').parentElement)}; }
  return out; }"""


def d_common(page, vp, sid, label):  # AC206-AC209 AC213 AC216-AC222 AC226 AC228 AC229, both widths; returns the parts
    W, H = size(page)
    big = vp is DESKTOP
    strip(page, "AC206", STRIP_D, None, label)
    p = page.evaluate(D_PARTS)
    head, wm, h1 = p["head"], p["wm"], p["h1"]
    if not head or not wm or not h1:
        fail(f"AC207-AC220 a <header>, its a.wordmark or the <h1> is missing at {label}")
        return p
    if big and (not clear(head["bg"]) or head["bgImage"] != "none" or head["position"] in ("fixed", "sticky") or rgb(p["behindWm"]) != VIOLET):
        fail(f"AC207 the <header> (background {head['bg']}, position {head['position']}) must be transparent and not fixed or "
             f"sticky, with #230a47 behind the wordmark (is {p['behindWm']}) at {label}")
    centre = (wm["ext"][1] + wm["ext"][3]) / 2
    if wm["ext"][0] > 64 or centre > 120:
        fail(f"AC208 the wordmark text starts {wm['ext'][0]:.0f}px from the left with its vertical centre at {centre:.0f}px at "
             f"{label}; it needs at most 64px and at most 120px")
    lo, hi = (28, 32) if big else (26, 29)
    if wm["fam"] != "Orbit" or wm["weight"] != 400 or rgb(wm["color"]) != TEXT_D or high(wm["box"]) > 1.6 * wm["fs"] or not lo <= wm["fs"] <= hi:
        fail(f"AC209 the header wordmark ({wm['fam']!r}, weight {wm['weight']}, colour {wm['color']}, {wm['fs']}px, box "
             f"{high(wm['box']) / wm['fs']:.2f} x) needs Orbit, 400, #f4effc, a box at most 1.6 x its font-size tall and {lo}-{hi}px at {label}")
    svgs = p["svgs"]
    need = (1300, 560) if big else (370, 480)
    if len(svgs) != 1 or not svgs[0]["shown"] or wide(svgs[0]["box"]) < need[0] or high(svgs[0]["box"]) < need[1]:
        fail(f"AC213 the first section needs exactly one inline <svg aria-hidden=\"true\"> outside a link (the contours), "
             f"{need[0]}px wide and {need[1]}px tall or more at {label} (found {[rnd(s['box']) for s in svgs]})")
    sheet = p.get("sheet")
    if abs((h1["ext"][0] + h1["ext"][2]) / 2 - W / 2) > 24 or (sheet and h1["box"][3] > sheet["box"][1] + 0.5):
        fail(f"AC216 the <h1> text's centre ({(h1['ext'][0] + h1['ext'][2]) / 2:.0f}px) must be within 24px of {W / 2:.0f}px and the "
             f"<h1> (bottom {h1['box'][3]:.0f}px) above the sheet ({sheet and round(sheet['box'][1])}px) at {label}")
    h1_on_load(page, "AC216", 0, label)
    if h1["fam"] != "Orbit" or h1["weight"] != 400 or rgb(h1["color"]) != TEXT_D or not ((56 <= h1["fs"] <= 80) if big else h1["fs"] >= 28):
        fail(f"AC217 the <h1> ({h1['fam']!r}, weight {h1['weight']}, colour {h1['color']}, {h1['fs']}px) needs Orbit, 400, #f4effc "
             f"and {'56-80px' if big else '28px or more'} at {label}")
    limit = 1.5 if big else 2.9
    if high(h1["box"]) > limit * h1["fs"]:
        fail(f"AC218 the <h1> box is {high(h1['box']) / h1['fs']:.2f} x its font-size tall at {label}, above {limit}")
    svc = section_id(page, "services")
    links = [x for x in (first_links(page, "AC219") or []) if not sheet or x["box"][3] <= sheet["box"][1] + 0.5]
    if len(links) != 1 or links[0]["text"] != "투자 분야 보기" or links[0]["href"] != f"#{svc}":
        fail(f"AC219 the first section must hold, above the sheet, exactly one link outside the header "
             f"and the bars: '투자 분야 보기' to #{svc} (found {[(x['text'], x['href']) for x in links]}) at {label}")
    else:
        x = links[0]
        if (not clear(x["bg"]) or any(b[0] != "solid" or b[1] < 1 for b in x["border"]) or not is_pill(x) or rgb(x["color"]) != TEXT_D):
            fail(f"AC219 the outline pill (background {x['bg']}, borders {x['border']}, radius {min(x['radius']):.0f}px, colour "
                 f"{x['color']}) needs a transparent background, four solid borders of 1px or more, a pill radius and #f4effc at {label}")
        gap = x["box"][1] - h1["box"][3]
        if not -0.5 <= gap <= 64 or abs((x["box"][0] + x["box"][2]) / 2 - W / 2) > 24:
            fail(f"AC220 the outline pill {rnd(x['box'])} must start below the <h1> ({h1['box'][3]:.0f}px), at most 64px from it, "
                 f"with its centre within 24px of {W / 2:.0f}px at {label}")
    if not sheet:
        fail(f"AC221 no element with the background #fbf9ff holds the service section (the sheet) at {label}; AC221-AC226 did not run")
    else:
        sb = sheet["box"]
        left, right = sb[0], W - sb[2]
        lo, hi = (8, 40) if big else (4, 16)
        if min(sheet["radius"][:2]) < 12 or not lo <= left <= hi or not lo <= right <= hi or (big and abs(left - right) > 4):
            fail(f"AC221 the sheet (top radii {sheet['radius'][:2]}, side gaps {left:.0f}px and {right:.0f}px) needs top corners of "
                 f"12px or more and a gap of {lo}-{hi}px to each side{', the two within 4px' if big else ''} at {label}")
        lo, hi = (600, 780) if big else (540, 740)
        if not lo <= sb[1] <= hi or rgb(sheet["above"]) != VIOLET:
            fail(f"AC222 the sheet's top edge is {sb[1]:.0f}px from the top at {label} (needs {lo}-{hi}px), with {sheet['above']} "
                 f"6px above it (needs #230a47)")
        tags, cards = sheet["tags"], sheet["cards"]
        ok = len(cards) >= 3 and all(min(k["radius"]) >= 12 and k["heads"] == 1 and k["ps"] == 1 for k in cards) \
            and (not tags or all(k["box"][1] >= max(t["box"][3] for t in tags) - 0.5 for k in cards))
        if ok and big:
            ok = max(sum(1 for b in cards if abs(b["box"][1] - a["box"][1]) <= 4) for a in cards) >= 3
        elif ok:
            ok = stacked([k["box"] for k in cards])
        if not ok:
            fail(f"AC226 the sheet needs three or more cards (class \"card\") below the tags, each with a radius of 12px or more, "
                 f"one heading and one <p>; {'three or more side by side' if big else 'stacked in one column'} at {label} "
                 f"(found {[(rnd(k['box']), min(k['radius']), k['heads'], k['ps']) for k in cards]})")
    con = p.get("contact")
    if not con:
        fail(f"AC228 no single contact section at {label}")
    else:
        if big and (rgb(con["bg"]) != PALE or rgb(con["color"]) != VIOLET or con["box"][0] > 0.5 or con["box"][2] < W - 0.5):
            fail(f"AC228 the contact section (background {con['bg']}, colour {con['color']}, box {rnd(con['box'])}) needs "
                 f"#ece6fb, #230a47 and the full viewport width")
        need = 28 if big else 20
        if not con["oneList"] or any(x["fs"] < need or (big and wide(x["box"]) < 0.5 * W) or not x["li"]
                                     or not any(b[0] == "solid" and b[1] >= 1 for b in (x["li"]["border"][0], x["li"]["border"][2])) for x in con["links"]):
            fail(f"AC229 the four contact links must be items of one list, each at {need}px or more"
                 f"{', 50 % of the viewport wide or more' if big else ''}, in an <li> with a solid top or bottom border at {label} "
                 f"(one list: {con['oneList']}, {[(x['text'], x['fs'], round(wide(x['box']))) for x in con['links']]})")
    return p


def d_desktop(page, sid, p):  # AC210-AC212 AC223-AC225
    W, H = size(page)
    nav, sheet = p["nav"], p.get("sheet")
    if not nav or not clear(nav["bg"]) or any(b[0] != "solid" or b[1] < 1 for b in nav["border"]) or not is_pill(nav) \
            or len(p["navLinks"]) < 3 or any(rgb(x["color"]) != TEXT_D for x in p["navLinks"]):
        fail(f"AC210 the nav pill (background {nav and nav['bg']}, borders {nav and nav['border']}) needs a transparent "
             f"background, four solid borders of 1px or more, a pill radius and three or more links in #f4effc")
    pink = [x for x in p["headLinks"] if says(x, "기업 문의")]
    if len(pink) != 1 or not link_is(pink[0], "기업 문의", sid) or rgb(pink[0]["bg"]) != PINK or rgb(pink[0]["color"]) != VIOLET or not is_pill(pink[0]):
        fail(f"AC211 the <header> needs exactly one link outside the nav pill with the text '기업 문의', to #{sid}, with the "
             f"background #ff6685, the colour #230a47 and a pill radius (found {[(x['text'], x['href'], x['bg'], x['color']) for x in p['headLinks']]})")
    elif nav:
        x, gap = pink[0]["box"], pink[0]["box"][0] - nav["box"][2]
        if W - x[2] > 64 or x[2] > W or not 0 <= gap <= 24 or abs((x[1] + x[3]) / 2 - (nav["box"][1] + nav["box"][3]) / 2) > 6:
            fail(f"AC212 the pink pill {rnd(x)} must end within 64px of the right edge, with the nav pill {rnd(nav['box'])} ending "
                 f"0-24px left of it and their vertical centres within 6px")
    if not sheet:
        return
    page.evaluate("scrollTo({top: 600, behavior: 'instant'})")
    page.wait_for_timeout(600)
    after = page.evaluate(D_PARTS).get("sheet")
    y = page.evaluate("scrollY")
    page.evaluate("scrollTo({top: 0, behavior: 'instant'})")
    page.wait_for_timeout(200)
    if not after or y < 600 or abs(after["docTop"] - sheet["docTop"]) > 0.5:
        fail(f"AC223 the sheet's top edge moves in the document on scroll: {sheet['docTop']:.0f}px at scroll 0, "
             f"{after and round(after['docTop'])}px at scroll {y:.0f}")
    tags = sheet["tags"]
    if len(tags) < 4:
        fail(f"AC224 the sheet needs a <ul class=\"tags\"> of four or more <li> (found {len(tags)})")
    for t in tags:
        if not re.fullmatch(r"[가-힣]+(?: [가-힣]+)*", t["own"]) or any(b[0] != "solid" or b[1] <= 0 for b in t["border"]) or not is_pill(t) \
                or t["link"] or t["cursor"] == "pointer":
            fail(f"AC224 the tag {t['text']!r} needs own text of Hangul syllables and spaces only, four solid borders, a pill "
                 f"radius, no <a> and no pointer cursor (borders {t['border']}, link {t['link']}, cursor {t['cursor']})")
        if not 0 <= t["box"][1] < H:
            fail(f"AC225 the tag {t['text']!r} starts {t['box'][1]:.0f}px down, outside the {H}px viewport on load")


def d_mobile(page, sid, p):  # AC230-AC232
    W, H = size(page)
    if (p["nav"] and p["nav"]["shown"]) or any(x["shown"] for x in p["headLinks"]) or p["rightOfWm"]:
        fail(f"AC230 at 390px the nav pill and the pink pill of the <header> must not be displayed, and nothing may stand right "
             f"of the wordmark in the <header> (found {p['rightOfWm'][:4]})")
    low = bottom_bars(page)
    if len(low) != 1 or low[0]["tag"] != "a" or not link_is(low[0], "기업 문의", sid) or rgb(low[0]["bg"]) != PINK \
            or rgb(low[0]["color"]) != VIOLET or not is_pill(low[0]):
        fail(f"AC231 at 390px exactly one element is pinned to the bottom: a link '기업 문의' to #{sid} with the background "
             f"#ff6685, the colour #230a47 and a pill radius (found {[(b['tag'], b['text'], b['href'], b['bg']) for b in low]})")
        return
    b = low[0]["box"]
    if wide(b) > 200 or high(b) > 56 or not 12 <= H - b[3] <= 28:
        fail(f"AC231 the floating link {rnd(b)} must be at most 200px wide and 56px tall, with its bottom edge 12-28px above "
             f"the bottom of the {H}px viewport")
    sheet = p.get("sheet")
    if sheet and b[1] - max(sheet["box"][1], 0) < 60:
        fail(f"AC232 at 390px {b[1] - sheet['box'][1]:.0f}px of the sheet (top {sheet['box'][1]:.0f}px) shows above the floating link "
             f"(top {b[1]:.0f}px), below 60px")


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


def iframe_shots(page, inner, out):  # AC97: the 390x844 iframe at every 600 px down to the end, bars in place
    h = inner.evaluate("document.documentElement.scrollHeight")
    for n, y in enumerate([*range(0, max(h - 844, 0), 600), max(h - 844, 0)], 1):
        inner.evaluate("y => scrollTo({top: y, behavior: 'instant'})", y)
        inner.wait_for_timeout(300)
        page.screenshot(path=str(out / f"iframe-390-{n:02d}.png"), clip={"x": 0, "y": 0, "width": 390, "height": 844})
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


def crops(page, out, name):  # the wordmark and the <h1> as drawn at deviceScaleFactor 1, for the reviews
    for sel, what in (("header a.wordmark", "wordmark"), ("h1", "h1")):
        box = page.evaluate("""sel => { const e = document.querySelector(sel); if (!e) return null; scrollTo(0, 0); const x = window.__c.ext(e);
          return {x: Math.max(0, x[0] - 16), y: Math.max(0, x[1] - 12), width: Math.min(innerWidth, x[2] + 16) - Math.max(0, x[0] - 16), height: x[3] - x[1] + 24}; }""", sel)
        if box and box["width"] > 1 and box["height"] > 1:
            page.screenshot(path=str(out / f"{what}-{name}.png"), clip=box)


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
            guard("AC119", web_font, page, sel, what, want)  # first: the measurements below need the real faces
        sid = guard("AC30", section_id, page, "contact")
        if not sid:
            fail(f"AC30 no single contact <section id> at {label}; the contact link checks did not run")
        big = vp is DESKTOP
        if key == "B":
            guard(f"sample B at {label}", b_common, page, vp, label)
            guard(f"sample B at {label}", b_desktop if big else b_mobile, page, sid)
        elif key == "C":
            parts = guard(f"sample C at {label}", c_common, page, vp, sid, label)
            if parts:
                guard(f"sample C at {label}", c_desktop if big else c_mobile, page, sid, parts)
        else:
            parts = guard(f"sample D at {label}", d_common, page, vp, sid, label)
            if parts:
                guard(f"sample D at {label}", d_desktop if big else d_mobile, page, sid, parts)
        guard("AC18", wordmark_name, page, slug, label)
        guard("AC34", keep_all, page, label)
        guard("AC32", sentence_first_screen, page, label)
        guard("AC8-AC12 AC117", marker, page, vp, label)
        if sid:
            guard("AC41-AC44", contact_link, page, vp, sid, label)
        if not big:
            guard("AC118", bars_cover, page)
        guard("AC31 AC45-AC47 AC57-AC59 AC77 AC81", sentences, page, key, label)
        guard("AC120 AC121 AC164 AC236", faces, page, key, big, label)
        guard("AC101", focus_ring, page, label)
        name = "1440" if big else "390"
        guard("crops", crops, page, out, name)
        guard("AC96", no_overflow, page, f"AC96 {label}")
        guard("settle", settle, page)
        guard("AC96", no_overflow, page, f"AC96 {label}")  # again after the scroll-through, on the full page
        shot = "desktop-1440.png" if big else "mobile-390.png"
        heights[shot] = guard("screenshots", bands, page, out / shot, vp["width"])
        guard("AC98", contrast, page, label)
        for b in bad_fonts:  # read last, so font files fetched during the scroll-through count too
            fail(f"AC119 web font request did not return 200 at {label}: {b}")
        ctx.close()

    def iframe_390():  # AC96 again inside a width:390px iframe, as playbook §4 does it
        ctx, page = new_page(browser, DESKTOP)
        page.goto(f"{base}/profile/")
        page.set_content(f'<body style="margin:0"><iframe src="{url}" style="display:block;width:390px;height:844px;border:0"></iframe>')
        page.frame_locator("iframe").locator("body").wait_for()
        inner = page.frames[1]
        inner.wait_for_load_state("networkidle")
        inner.wait_for_timeout(1500)
        settle(inner)
        no_overflow(inner, "AC96 390px iframe")
        heights["iframe-390"] = guard("screenshots", iframe_shots, page, inner, out)
        ctx.close()
    guard("AC96", iframe_390)

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
    print(f"screenshots for the reviews: {out}/desktop-1440*.png {out}/mobile-390*.png {out}/iframe-390-*.png, summary {out / 'summary.txt'}")


def check_gallery(browser, base):  # AC111
    ctx, page = new_page(browser, DESKTOP)
    page.goto(f"{base}/profile/", wait_until="networkidle")
    page.click('.pf-filters button[data-filter="invest"]')
    page.wait_for_timeout(300)
    shown = page.locator('a.pf-card[data-industry="invest"]:visible')
    slugs = sorted(shown.nth(i).get_attribute("data-slug") for i in range(shown.count()))
    if slugs != sorted(SAMPLES):
        fail(f"AC111 the invest filter shows cards {slugs}, expected {sorted(SAMPLES)}")
    if page.locator('.pf-empty[data-industry="invest"]:visible').count():
        fail("AC111 the invest filter still shows a 준비 중 tile")
    width = "document.getElementById('pf-v-iframe').getBoundingClientRect().width"
    for slug in SAMPLES:  # each card from a fresh load of /profile/, as a visitor arrives
        if slug not in slugs:
            continue
        page.goto(f"{base}/profile/", wait_until="networkidle")
        page.click('.pf-filters button[data-filter="invest"]')
        page.wait_for_timeout(300)
        viewer, iframe = page.locator("#pf-viewer"), page.locator("#pf-v-iframe")
        page.locator(f'a.pf-card[data-slug="{slug}"]').click()
        page.wait_for_timeout(300)
        if not viewer.is_visible() or not (iframe.get_attribute("src") or "").endswith(f"/profile/{slug}/"):
            fail(f"AC111 clicking the {slug} card does not open the preview with that sample")
            continue
        try:  # the loaded document is this sample's page (matched by slug)
            page.frame_locator("#pf-v-iframe").locator("header a.wordmark").first.wait_for(state="attached",
                                                                                            timeout=10000)
            next(f for f in page.frames if f.url.rstrip("/").endswith(f"/profile/{slug}"))
        except Exception:
            fail(f"AC111 {slug}: the preview iframe does not show that sample's page")
        for device, cond in (("mobile", "<= 400"), ("desktop", "> 600")):  # the width animates; wait for it
            page.click(f'button[data-device="{device}"]')
            try:
                page.wait_for_function(f"{width} {cond}", timeout=3000)
            except Exception:
                fail(f"AC111 {slug}: the {device} button does not switch the preview width ({page.evaluate(width)})")
        page.keyboard.press("Escape")
        try:
            page.wait_for_function("document.getElementById('pf-viewer').hidden", timeout=3000)
        except Exception:
            fail(f"AC111 {slug}: Esc does not close the preview")
    ctx.close()



def real_faces(page, slug, bad_fonts, label):  # AC119 where a measurement or a crop needs the real faces
    for sel, what, want in (("h1", "<h1>", SAMPLES[slug]["h1"]), ("header a.wordmark", "header wordmark", SAMPLES[slug]["wm"])):
        guard(f"AC119 {label}", web_font, page, sel, f"{what} ({label})", want)
    for b in bad_fonts:
        fail(f"AC119 {label}: a web font request did not succeed: {b}")


def check_trio(browser, base):  # AC242-AC247
    got = {}
    for slug in SAMPLES:
        if not (ROOT / "profile" / slug / "index.html").is_file():
            fail(f"AC242-AC247 profile/{slug}/index.html does not exist")
            continue
        got[slug] = {}
        for label, vp in (("1440", DESKTOP), ("390", MOBILE)):
            ctx, page = new_page(browser, vp)
            bad_fonts = font_responses(page)
            page.goto(f"{base}/profile/{slug}/", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(500)
            lib(page)
            real_faces(page, slug, bad_fonts, f"trio {slug} at {label}px")
            got[slug][label] = (info(page, "h1"), info(page, "header a.wordmark"))
            ctx.close()
        if not all(x for pair in got[slug].values() for x in pair):
            fail(f"AC242-AC247 {slug}: no <h1> or no header a.wordmark to read")
            del got[slug]
    if len(got) < len(SAMPLES):
        return
    b, c, d = (got[s] for s in SAMPLES)

    def cx(x):
        return (x["ext"][0] + x["ext"][2]) / 2

    def cy(x):
        return (x["ext"][1] + x["ext"][3]) / 2
    for what, idx in (("<h1>", 0), ("header wordmark", 1)):
        fams = {s: got[s]["1440"][idx]["fam"] for s in got}
        if len({f.lower() for f in fams.values()}) != len(fams):
            fail(f"AC242 two samples share the {what}'s first font family: {fams}")
    wb, wc, wd = b["1440"][1], c["1440"][1], d["1440"][1]
    if cx(wb) - max(cx(wc), cx(wd)) < 300:
        fail(f"AC243 at 1440px the wordmark centre of B ({cx(wb):.0f}px) is less than 300px right of C's ({cx(wc):.0f}px) or D's ({cx(wd):.0f}px)")
    if cy(wc) - cy(wd) < 90:
        fail(f"AC244 at 1440px the wordmark of C (vertical centre {cy(wc):.0f}px) is less than 90px further down than D's ({cy(wd):.0f}px)")
    sizes = {"B": wb["fs"], "C": wc["fs"], "D": wd["fs"]}
    if min(abs(sizes[x] - sizes[y]) for x, y in (("B", "C"), ("B", "D"), ("C", "D"))) < 4:
        fail(f"AC245 at 1440px two wordmark sizes differ by less than 4px: {sizes}")
    mb, mc, md = b["390"][1], c["390"][1], d["390"][1]
    if cx(mb) - max(cx(mc), cx(md)) < 60 or abs(mc["fs"] - md["fs"]) < 3:
        fail(f"AC246 at 390px the wordmark centre of B ({cx(mb):.0f}px) must be 60px or more right of C's ({cx(mc):.0f}px) and D's "
             f"({cx(md):.0f}px), and the sizes of C ({mc['fs']}px) and D ({md['fs']}px) 3px or more apart")
    hb, hc, hd = b["1440"][0], c["1440"][0], d["1440"][0]
    W = DESKTOP["width"]
    if hb["ext"][2] > W / 2 or cx(hc) <= W / 2 or abs(cx(hd) - W / 2) > 24:
        fail(f"AC247 at 1440px the <h1> of B must lie wholly left of {W / 2:.0f}px (ends at {hb['ext'][2]:.0f}px), the centre of C's "
             f"right of it ({cx(hc):.0f}px) and the centre of D's within 24px of it ({cx(hd):.0f}px)")
    for s in got:
        h, w, m = got[s]["1440"][0], got[s]["1440"][1], got[s]["390"][1]
        print(f"{s}: h1 {h['fam']} text {h['ext'][0]:.0f}-{h['ext'][2]:.0f}px; wordmark {w['fam']} {w['fs']}px centre "
              f"({cx(w):.0f}, {cy(w):.0f}) at 1440, {m['fs']}px centre {cx(m):.0f}px at 390")


SHEET = """<!doctype html><meta charset="utf-8"><style>body{margin:0;padding:16px;background:#888;font:14px sans-serif;display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start}
figure{margin:0;background:#fff;padding:6px}figcaption{padding:4px 2px 0;color:#000}img{display:block;width:%dpx;height:auto}</style>%s"""


def sheet(browser, shots_base, out, name, items, width, per_row):  # one PNG that sets the named files of `out` side by side
    have = [(f, cap) for f, cap in items if (out / f).is_file()]
    if len(have) < len(items):
        fail(f"compare: {name} lacks {[f for f, _ in items if not (out / f).is_file()]}")
    if not have:
        return
    figs = "".join(f'<figure><img src="{shots_base}/compare/{f}"><figcaption>{cap}</figcaption></figure>' for f, cap in have)
    ctx, page = new_page(browser, {"width": 32 + per_row * (width + 28), "height": 600})
    page.set_content(SHEET % (width, figs), wait_until="load")
    page.wait_for_timeout(200)
    page.screenshot(path=str(out / name), full_page=True)
    ctx.close()


def compare(browser, base, shots):
    out = shots / "compare"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.iterdir():  # keep the last good live reference files; they are replaced only when a site answers
        if f.is_file() and (not f.name.startswith("ref-") or f.name.startswith("ref-g1-")):
            f.unlink()
    notes = []
    before = len(fails)
    for slug in [*SAMPLES, *SHIPPED]:
        if not (ROOT / "profile" / slug / "index.html").is_file():
            fail(f"compare: profile/{slug}/index.html does not exist")
            notes.append(f"local {slug} missing")
            continue
        for label, vp in (("1440", DESKTOP), ("390", MOBILE)):
            ctx, page = new_page(browser, vp)
            bad_fonts = font_responses(page)
            page.goto(f"{base}/profile/{slug}/", wait_until="networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(out / f"{slug}-{label}.png"))
            if slug in SAMPLES:
                lib(page)
                real_faces(page, slug, bad_fonts, f"compare {slug} at {label}px")
                x = page.evaluate("(() => { const e = document.querySelector('header a.wordmark'); if (!e) return null; const x = window.__c.ext(e);"
                                  " return {x: Math.max(0, x[0] - 16), y: Math.max(0, x[1] - 12), width: x[2] - x[0] + 32, height: x[3] - x[1] + 24}; })()")
                if x and x["width"] > 33:
                    page.screenshot(path=str(out / f"{slug}-wordmark-{label}.png"), clip=x)
            ctx.close()
        thumb = ROOT / "profile" / slug / "thumb.jpg"
        if thumb.is_file():
            shutil.copyfile(thumb, out / f"{slug}-thumb.jpg")
        tree, state = tree_state(slug)
        notes.append(f"local {slug} tree {tree} {state}")
    keep = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir") or ROOT / ".git") / "robintech-dev" / "keep"
    for slug, meta in SAMPLES.items():
        got = []
        for src, dst in ((f"ref-g1-invest-{meta['g1']}.jpg", f"ref-g1-{slug}-1440.jpg"), (f"ref-g1-invest-{meta['g1']}-390.jpg", f"ref-g1-{slug}-390.jpg")):
            if (keep / src).is_file():
                shutil.copyfile(keep / src, out / dst)
                got.append(dst)
        notes.append(f"reference-g1 {slug} {'ok ' + ' '.join(got) if len(got) == 2 else 'missing (' + str(keep) + ')'}")
        ctx = browser.new_context(viewport=DESKTOP)
        page = ctx.new_page()
        try:
            resp = page.goto(meta["ref"], wait_until="load", timeout=45000)
            if resp is None or resp.status >= 400:  # an error or challenge page is not a good copy
                raise RuntimeError(f"HTTP {resp.status if resp else 'no response'}")
            page.wait_for_timeout(4000)
            page.screenshot(path=str(out / f"tmp-ref-{slug}.png"))  # tmp- files are swapped in only when both succeed
            (out / f"tmp-ref-{slug}.txt").write_text(page.evaluate("document.body.innerText"), encoding="utf-8")
            for f in sorted(out.glob(f"tmp-ref-{slug}*")):
                f.replace(out / f.name.removeprefix("tmp-"))
            notes.append(f"reference {slug} {meta['ref']} ok {datetime.now().date()}")
        except Exception as exc:
            for f in out.glob(f"tmp-ref-{slug}*"):
                f.unlink()
            have = all((out / f"ref-{slug}{x}").is_file() for x in (".png", ".txt"))
            when = datetime.fromtimestamp((out / f"ref-{slug}.png").stat().st_mtime).date() if have else ""
            notes.append(f"reference {slug} {meta['ref']} {'cached ' + str(when) if have else 'unreachable'}: "
                         f"{type(exc).__name__}: {(str(exc).splitlines() or [''])[0]}")
        ctx.close()
    handler = partial(type("Quiet", (SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}), directory=str(shots))
    files = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=files.serve_forever, daemon=True).start()
    fb = f"http://127.0.0.1:{files.server_port}"
    try:
        every = [*SAMPLES, *SHIPPED]
        sheet(browser, fb, out, "sheet-all-1440.png", [(f"{s}-1440.png", s) for s in every], 440, 4)
        sheet(browser, fb, out, "sheet-all-390.png", [(f"{s}-390.png", s) for s in every], 240, 7)
        sheet(browser, fb, out, "sheet-thumbs.png", [(f"{s}-thumb.jpg", s) for s in every], 440, 4)
        sheet(browser, fb, out, "sheet-six-390.png", [(f"{s}-390.png", s) for s in [*SAMPLES, *SIX]], 300, 5)
        sheet(browser, fb, out, "sheet-trio-1440.png", [(f"{s}-1440.png", s) for s in SAMPLES], 960, 2)
        sheet(browser, fb, out, "sheet-trio-390.png", [(f"{s}-390.png", s) for s in SAMPLES], 390, 3)
        sheet(browser, fb, out, "sheet-trio-thumbs.png", [(f"{s}-thumb.jpg", s) for s in SAMPLES], 600, 3)
        for label in ("1440", "390"):
            for s in SAMPLES:  # at their own size: 1 CSS px is 1 image px
                if not (out / f"{s}-wordmark-{label}.png").is_file():
                    fail(f"compare: no wordmark crop of {s} at {label}")
        for s in SAMPLES:
            if (out / f"ref-g1-{s}-1440.jpg").is_file():
                sheet(browser, fb, out, f"sheet-ref-{s}-1440.png", [(f"{s}-1440.png", s), (f"ref-g1-{s}-1440.jpg", "reference (G1 screenshot)")], 960, 2)
                sheet(browser, fb, out, f"sheet-ref-{s}-390.png", [(f"{s}-390.png", s), (f"ref-g1-{s}-390.jpg", "reference (G1 screenshot)")], 390, 2)
    finally:
        files.shutdown()
        files.server_close()
    notes.append(f"result {'PASS' if len(fails) == before else 'FAIL'}")  # last: a run with a missing shot or sheet is not evidence
    (out / "summary.txt").write_text("\n".join([f"head {git('rev-parse', 'HEAD') or 'unknown'}", *notes]) + "\n",
                                     encoding="utf-8")
    print("\n".join(notes))
    print(f"compare shots: {out}")


if __name__ == "__main__":
    args = sys.argv[1:]
    shots = Path("/tmp/profile-invest-shots")
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
