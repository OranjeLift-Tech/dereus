/* Verhuisbedrijf De Reus - site scripts
 * Vervangt de Wix-runtime, die buiten Wix alleen fouten geeft. */
(function () {
  'use strict';

  /* 1. Scherpe afbeeldingen
   * De HTML bevat kleine, wazige placeholders (w_49, blur_2). Wix wisselt die
   * normaal via JS om. Hier: blur eruit en de maat afstemmen op het scherm. */
  function imageInfo(img) {
    var wrap = img.closest('wow-image[data-image-info]');
    if (!wrap) return null;
    try { return { box: wrap, data: JSON.parse(wrap.getAttribute('data-image-info')) }; } catch (e) { return null; }
  }

  function sharpenImages() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    document.querySelectorAll('img[src*="static.wixstatic.com/media/"]').forEach(function (img) {
      var src = img.getAttribute('src');
      var m = src.match(/\/(fill|fit)\/w_(\d+),h_(\d+)([^/]*)\//);
      if (!m) return;

      // Afbeeldingen met Wix-data: URL opbouwen zoals Wix dat doet,
      // inclusief de aparte uitsnede voor mobiel (sourceSets).
      var info = imageInfo(img);
      if (info && info.data.imageData && info.data.imageData.displayMode === 'fill') {
        var d = info.data.imageData;
        var crop = d.crop;
        (info.data.sourceSets || []).forEach(function (s) {
          if (s.mediaQuery && window.matchMedia(s.mediaQuery).matches && s.crop) crop = s.crop;
        });
        var r = info.box.getBoundingClientRect();
        if (r.width && r.height) {
          var W = Math.ceil(r.width * dpr), H = Math.ceil(r.height * dpr);
          var cropPart = crop ? 'crop/x_' + crop.x + ',y_' + crop.y + ',w_' + crop.width + ',h_' + crop.height + '/' : '';
          var url = 'https://static.wixstatic.com/media/' + d.uri + '/v1/' + cropPart +
            'fill/w_' + W + ',h_' + H + m[4].replace(/,blur_\d+/, '') + '/' + src.split('/').pop();
          if (url !== src) img.setAttribute('src', url);
          return;
        }
      }

      var w = +m[2], h = +m[3];
      var shown = img.getBoundingClientRect().width || img.parentElement.getBoundingClientRect().width;
      var k = Math.max(1, Math.ceil((shown * dpr) / w * 10) / 10);
      var params = m[4].replace(/,blur_\d+/, '');
      var next = src.replace(m[0], '/' + m[1] + '/w_' + Math.round(w * k) + ',h_' + Math.round(h * k) + params + '/');
      if (next !== src) img.setAttribute('src', next);
    });
  }

  /* 2. Menu-ankers (Home, Over ons, Diensten, Werkwijze, Contact, Offerte aanvragen) */
  var anchors = {
    SCROLL_TO_TOP: null,
    'anchors-mjj6dcf9': 'comp-miw17n40', // Over ons
    'anchors-mjj6csct': 'comp-miyob6cm', // Diensten
    'anchors-mjj6dpfc': 'comp-mj5w5r6z', // Werkwijze
    'anchors-mjj6dy97': 'comp-mj8s1xg3', // Contact
    'anchors-mjj6dtls': 'comp-mj5zpanx'  // Offerte aanvragen
  };

  document.addEventListener('click', function (e) {
    var link = e.target.closest('[data-anchor]');
    if (!link) return;
    var key = link.getAttribute('data-anchor');
    if (!(key in anchors)) return;
    e.preventDefault();
    closeMenu();
    var target = anchors[key] && document.getElementById(anchors[key]);
    var top = target ? target.getBoundingClientRect().top + window.scrollY : 0;
    window.scrollTo({ top: top, behavior: 'smooth' });
  });

  /* 3. Hamburgermenu (mobiel) */
  var OPEN = 'HamburgerOverlay547129737--isMenuOpen';
  var overlay = document.querySelector('[data-hook="hamburger-overlay-root"]');
  var openBtn = document.querySelector('.wixui-hamburger-open-button');

  function setMenu(open) {
    if (!overlay) return;
    overlay.classList.toggle(OPEN, open);
    overlay.setAttribute('data-visible', open ? 'true' : 'false');
    overlay.querySelectorAll('[aria-hidden]').forEach(function (el) {
      el.setAttribute('aria-hidden', open ? 'false' : 'true');
    });
    if (openBtn) openBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.documentElement.style.overflow = open ? 'hidden' : '';
  }
  function closeMenu() { setMenu(false); }

  if (openBtn) openBtn.addEventListener('click', function () { setMenu(true); });
  document.querySelectorAll('.wixui-hamburger-close-button').forEach(function (btn) {
    btn.addEventListener('click', closeMenu);
  });
  if (overlay) overlay.addEventListener('click', function (e) {
    if (e.target.getAttribute('data-hook') === 'hamburger-overlay-dialog') closeMenu();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });

  /* 4. Entree-animaties
   * In de CSS staan animaties op "paused" tot data-motion-enter="done".
   * Wix start ze bij het in beeld scrollen; dat doen we hier ook. */
  function startMotion(el) {
    el.style.animationPlayState = 'running';
    el.addEventListener('animationend', function () {
      el.setAttribute('data-motion-enter', 'done');
      el.style.animationPlayState = '';
    }, { once: true });
  }

  var waiting = Array.prototype.filter.call(document.querySelectorAll('[id^="comp-"]'), function (el) {
    var cs = getComputedStyle(el);
    return cs.animationName !== 'none' && cs.animationPlayState.indexOf('paused') !== -1;
  });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        startMotion(entry.target);
      });
    }, { threshold: 0.1 });
    waiting.forEach(function (el) { io.observe(el); });
  } else {
    waiting.forEach(function (el) { el.setAttribute('data-motion-enter', 'done'); });
  }

  // <picture><source> (aparte mobiele uitsnede): zelfde placeholder, zelfde fix
  function sharpenSources() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    document.querySelectorAll('picture source[srcset*="static.wixstatic.com/media/"]').forEach(function (s) {
      var box = s.closest('wow-image') || s.parentElement;
      var r = box.getBoundingClientRect();
      if (!r.width || !r.height) return;
      var W = Math.ceil(r.width * dpr), H = Math.ceil(r.height * dpr);
      var set = s.getAttribute('srcset');
      var next = set.replace(/\/(fill|fit)\/w_\d+,h_\d+([^/]*)\//, function (all, mode, params) {
        return '/' + mode + '/w_' + W + ',h_' + H + params.replace(/,blur_\d+/, '') + '/';
      });
      if (next !== set) s.setAttribute('srcset', next);
    });
  }

  sharpenSources();
  sharpenImages();
  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(function () { sharpenSources(); sharpenImages(); }, 200); });
})();
