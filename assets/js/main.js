(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  if (toggle && header) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
    });
    header.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () { header.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }
  var onScroll = function () { if (header) header.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  var filters = document.querySelectorAll('.filters button');
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      filters.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      document.querySelectorAll('#case-grid .case-card').forEach(function (card) {
        var show = f === 'all' || card.getAttribute('data-cat') === f;
        card.hidden = !show;
        if (show) card.classList.add('in');
      });
    });
  });
})();

/* GA4 전환 이벤트: 상담 신청 · 이메일 · Robin Cloud 시작 클릭 */
(function () {
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href]');
    if (!a || typeof window.gtag !== 'function') return;
    var href = a.getAttribute('href') || '';
    var name = null;
    if (href.indexOf('mailto:') === 0) name = 'contact_email';
    else if (href.indexOf('ax.robin-cloud.com') !== -1 && href.indexOf('#contact') !== -1) name = 'contact_form';
    else if (/^https:\/\/robin-cloud\.com/.test(href)) name = 'robin_cloud_start';
    if (!name) return;
    var section = a.closest('section[id], footer, header');
    window.gtag('event', name, {
      link_url: href.replace(/\?.*$/, ''),
      link_text: (a.textContent || '').trim().slice(0, 60),
      location: section ? (section.id || section.tagName.toLowerCase()) : 'page'
    });
  });
})();

/* 히어로 광고 영상: 소리 없이 자동 반복 재생, 버튼으로 소리 켜기 */
(function () {
  var fig = document.querySelector('.hero-video');
  if (!fig) return;
  var video = fig.querySelector('video');
  var btn = fig.querySelector('.video-sound');
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    video.removeAttribute('autoplay');
    video.pause();
    video.controls = true;
    if (btn) btn.hidden = true;
    return;
  }
  if (!btn) return;
  var setState = function (on) {
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    btn.querySelector('.ic').textContent = on ? '🔊' : '🔇';
    btn.querySelector('.lbl').textContent = on ? '소리 끄기' : '소리 켜기';
  };
  btn.addEventListener('click', function () {
    var turnOn = video.muted;
    video.muted = !turnOn;
    if (turnOn) {
      video.currentTime = 0;
      if (typeof window.gtag === 'function') window.gtag('event', 'ad_video_sound_on', { location: 'hero' });
    }
    var p = video.play();
    if (p && p.catch) p.catch(function () {});
    setState(turnOn);
  });
})();

/* 홈페이지 프로파일 갤러리: 업종 필터 + 미리보기 뷰어 (profile/index.html) */
(function () {
  var grid = document.getElementById('pf-grid');
  if (!grid) return;

  var chips = document.querySelectorAll('.pf-filters button');
  chips.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      chips.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
      grid.querySelectorAll('.pf-card').forEach(function (card) {
        var show = f === 'all' || card.getAttribute('data-industry') === f;
        card.hidden = !show;
        if (show) card.classList.add('in');
      });
    });
  });

  var viewer = document.getElementById('pf-viewer');
  var dataEl = document.getElementById('pf-data');
  if (!viewer || !dataEl) return;
  var data = {};
  try { data = JSON.parse(dataEl.textContent); } catch (err) { return; }

  var $ = function (id) { return document.getElementById(id); };
  var iframe = $('pf-v-iframe');
  var frame = viewer.querySelector('.pf-v-frame');
  var dialog = viewer.querySelector('.pf-v-dialog');
  var deviceBtns = viewer.querySelectorAll('[data-device]');
  var lastFocus = null;
  var current = null;

  var setDevice = function (d) {
    frame.setAttribute('data-device', d);
    deviceBtns.forEach(function (b) {
      if (b.tagName === 'BUTTON') b.setAttribute('aria-pressed', b.getAttribute('data-device') === d ? 'true' : 'false');
    });
  };
  deviceBtns.forEach(function (b) {
    if (b.tagName === 'BUTTON') b.addEventListener('click', function () { setDevice(b.getAttribute('data-device')); });
  });

  var open = function (slug, opener) {
    var p = data[slug];
    if (!p) return;
    current = slug;
    lastFocus = opener || document.activeElement;
    var url = new URL(slug + '/', location.href);
    $('pf-v-industry').textContent = p.industry;
    $('pf-v-title').textContent = p.title;
    $('pf-v-name').textContent = p.name + (p.demo ? ' · 가상 상호 샘플' : '');
    $('pf-v-summary').textContent = p.summary;
    $('pf-v-url').textContent = url.host + url.pathname;
    $('pf-v-newtab').href = url.href;
    var ul = $('pf-v-features'); ul.textContent = '';
    p.features.forEach(function (f) { var li = document.createElement('li'); li.textContent = f; ul.appendChild(li); });
    var pal = $('pf-v-palette'); pal.textContent = '';
    p.palette.forEach(function (c) {
      var s = document.createElement('span'), i = document.createElement('i');
      i.style.background = c; s.appendChild(i); s.appendChild(document.createTextNode(c)); pal.appendChild(s);
    });
    setDevice('desktop');
    iframe.src = url.href;
    viewer.hidden = false;
    document.documentElement.classList.add('pf-lock');
    if (location.hash !== '#' + slug) history.replaceState(null, '', '#' + slug);
    viewer.querySelector('.pf-v-close').focus();
    if (typeof window.gtag === 'function') window.gtag('event', 'profile_preview', { profile: slug });
  };

  var close = function () {
    if (viewer.hidden) return;
    viewer.hidden = true;
    iframe.src = 'about:blank';
    current = null;
    document.documentElement.classList.remove('pf-lock');
    history.replaceState(null, '', location.pathname + location.search);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };

  grid.addEventListener('click', function (ev) {
    var card = ev.target.closest('a.pf-card[data-slug]');
    if (!card || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button === 1) return;
    ev.preventDefault();
    open(card.getAttribute('data-slug'), card);
  });
  viewer.querySelectorAll('[data-close]').forEach(function (el) { el.addEventListener('click', close); });

  document.addEventListener('keydown', function (ev) {
    if (viewer.hidden) return;
    if (ev.key === 'Escape') { ev.preventDefault(); close(); return; }
    if (ev.key !== 'Tab') return;
    var f = Array.prototype.filter.call(
      dialog.querySelectorAll('button, a[href], iframe'),
      function (el) { return el.offsetParent !== null; }
    );
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (ev.shiftKey && document.activeElement === first) { ev.preventDefault(); last.focus(); }
    else if (!ev.shiftKey && document.activeElement === last) { ev.preventDefault(); first.focus(); }
  });

  var fromHash = function () {
    var slug = decodeURIComponent(location.hash.slice(1));
    if (slug && data[slug]) { if (slug !== current) open(slug); }
    else close();
  };
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();
