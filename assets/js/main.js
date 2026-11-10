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
