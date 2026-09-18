/* Verhuisbedrijf De Reus: kernscript (header, menu, lade, bereikbaarheid, onthullen).
   Vanilla, defer. Blokscripts staan in js/blok/. */
(function () {
  'use strict';
  var doc = document;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Header: transparant bovenaan, licht na scrollen. De inhoud houdt een vaste bovenruimte. */
  var header = doc.querySelector('[data-header]');
  function scrol() {
    if (!header) return;
    header.classList.toggle('is-vast', window.scrollY > 24);
  }
  scrol();
  window.addEventListener('scroll', scrol, { passive: true });

  /* 2. Submenu's: klik of toets op de knop naast Diensten en Over ons; Escape sluit */
  var subs = [].slice.call(doc.querySelectorAll('.nav__item--sub'));
  function sluitSubs(behalve) {
    subs.forEach(function (li) {
      if (li === behalve) return;
      li.classList.remove('is-open');
      var k = li.querySelector('.nav__open'); if (k) k.setAttribute('aria-expanded', 'false');
    });
  }
  subs.forEach(function (li) {
    var knop = li.querySelector('.nav__open');
    if (!knop) return;
    var hoverTimer;
    function zetSub(open) {
      clearTimeout(hoverTimer);
      if (open) sluitSubs(li);
      li.classList.toggle('is-open', open);
      knop.setAttribute('aria-expanded', String(open));
    }
    knop.addEventListener('click', function () {
      zetSub(!li.classList.contains('is-open'));
    });
    li.addEventListener('mouseenter', function () {
      if (matchMedia('(hover: hover)').matches) zetSub(true);
    });
    li.addEventListener('mouseleave', function () {
      if (!li.contains(doc.activeElement)) hoverTimer = setTimeout(function () { zetSub(false); }, 140);
    });
    li.addEventListener('focusout', function (e) {
      if (!li.contains(e.relatedTarget)) zetSub(false);
    });
  });
  doc.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = subs.filter(function (li) { return li.classList.contains('is-open'); })[0];
    if (open) { sluitSubs(); var k = open.querySelector('.nav__open'); if (k) k.focus(); }
  });
  doc.addEventListener('click', function (e) { if (!e.target.closest('.nav__item--sub')) sluitSubs(); });

  /* 3. Lade (mobiel menu): focus blijft in de lade, Escape en de scrim sluiten, focus terug naar de knop */
  var menuKnop = doc.querySelector('.header__menu');
  var lade = doc.getElementById('lade');
  var paneel = lade && lade.querySelector('.lade__paneel');
  var vorige = null, timer = null;
  var achterLade = [];
  function focusbaar() {
    return [].slice.call(paneel.querySelectorAll('a[href], button, summary, [tabindex]:not([tabindex="-1"])'))
      .filter(function (el) { return el.offsetParent !== null; });
  }
  function zetLade(open) {
    if (!lade) return;
    clearTimeout(timer);
    if (open) {
      vorige = doc.activeElement;
      achterLade = [].slice.call(doc.body.children).filter(function (el) {
        return el !== lade && !el.inert && !/^(SCRIPT|STYLE|SVG)$/.test(el.tagName);
      });
      achterLade.forEach(function (el) { el.inert = true; });
      lade.hidden = false;
      requestAnimationFrame(function () { requestAnimationFrame(function () { lade.classList.add('is-open'); }); });
      doc.body.classList.add('lade-open');
      menuKnop.setAttribute('aria-expanded', 'true');
      var eerste = lade.querySelector('.lade__sluit'); if (eerste) eerste.focus();
    } else {
      achterLade.forEach(function (el) { el.inert = false; });
      achterLade = [];
      lade.classList.remove('is-open');
      doc.body.classList.remove('lade-open');
      menuKnop.setAttribute('aria-expanded', 'false');
      timer = setTimeout(function () { lade.hidden = true; }, reduce ? 0 : 360);
      if (vorige && vorige.focus) vorige.focus();
      vorige = null;
    }
  }
  if (menuKnop && lade) {
    menuKnop.addEventListener('click', function () { zetLade(true); });
    [].forEach.call(lade.querySelectorAll('[data-lade-sluit]'), function (el) { el.addEventListener('click', function () { zetLade(false); }); });
    lade.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]');
      if (a) zetLade(false);
    });
    doc.addEventListener('keydown', function (e) {
      if (!doc.body.classList.contains('lade-open')) return;
      if (e.key === 'Escape') { zetLade(false); return; }
      if (e.key !== 'Tab') return;
      var f = focusbaar(); if (!f.length) return;
      var eerste = f[0], laatste = f[f.length - 1];
      if (e.shiftKey && (doc.activeElement === eerste || !paneel.contains(doc.activeElement))) { e.preventDefault(); laatste.focus(); }
      else if (!e.shiftKey && (doc.activeElement === laatste || !paneel.contains(doc.activeElement))) { e.preventDefault(); eerste.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth >= 1100 && !lade.hidden) zetLade(false); });
  }

  /* 4. Bereikbaar: open of dicht in Nederlandse tijd, ook als de bezoeker in het buitenland zit.
     Tijden: ma t/m za 08.00 tot 20.00, zo 09.00 tot 17.00 (config.TIJDEN). */
  var statussen = doc.querySelectorAll('[data-bereikbaar]');
  if (statussen.length && window.Intl) {
    try {
      var d = {};
      new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Amsterdam', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
        .formatToParts(new Date()).forEach(function (p) { d[p.type] = p.value; });
      var dag = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(d.weekday);
      var nu = parseInt(d.hour, 10) * 60 + parseInt(d.minute, 10);
      var opent = function (dg) { return dg === 0 ? 9 * 60 : 8 * 60; };
      var sluit = function (dg) { return dg === 0 ? 17 * 60 : 20 * 60; };
      var tijd = function (min) { return (min < 600 ? '0' : '') + Math.floor(min / 60) + '.' + ('0' + min % 60).slice(-2); };
      var isOpen = nu >= opent(dag) && nu < sluit(dag);
      [].forEach.call(statussen, function (el) {
        var tekst = el.querySelector('.bereikbaar__tekst');
        if (!tekst) return;
        if (isOpen) {
          tekst.textContent = el.getAttribute('data-open') || 'Nu bereikbaar';
        } else {
          var morgen = nu >= sluit(dag);
          var volgende = morgen ? (dag + 1) % 7 : dag;
          var zin = (el.getAttribute('data-morgen') || 'Morgen weer bereikbaar vanaf {tijd} uur').replace('{tijd}', tijd(opent(volgende)));
          if (!morgen) zin = zin.replace(/^Morgen/, 'Vandaag');
          tekst.textContent = (el.getAttribute('data-dicht') || 'Nu gesloten') + ', ' + zin.charAt(0).toLowerCase() + zin.slice(1);
          el.classList.add('is-dicht');
        }
        el.hidden = false;
      });
      var rij = doc.querySelectorAll('[data-dagen="' + (dag === 0 ? '0' : '1-6') + '"]');
      [].forEach.call(rij, function (r) { r.classList.add('is-vandaag'); });
    } catch (e) { /* zonder status is de pagina ook compleet */ }
  }

  /* 5. Onthullen bij scrollen. Drempel 0 voor losse blokken en groepen (een lange groep op een telefoon
     haalt nooit 12 % zichtbaarheid), terugval zonder IntersectionObserver, alles zichtbaar bij afdrukken. */
  var los = doc.querySelectorAll('[data-reveal]'), groepen = doc.querySelectorAll('[data-reveal-groep]');
  function allesAan() {
    [].forEach.call(los, function (e) { e.classList.add('in'); });
    [].forEach.call(groepen, function (g) { [].forEach.call(g.children, function (k) { k.classList.add('in'); }); });
  }
  window.addEventListener('beforeprint', allesAan);
  if (!('IntersectionObserver' in window) || reduce) { allesAan(); }
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
    }, { threshold: 0, rootMargin: '0px 0px -8% 0px' });
    [].forEach.call(los, function (e) { io.observe(e); });
    var ioG = new IntersectionObserver(function (es) {
      es.forEach(function (x) {
        if (!x.isIntersecting) return;
        [].forEach.call(x.target.children, function (k, i) { k.style.transitionDelay = Math.min(i * 70, 560) + 'ms'; k.classList.add('in'); });
        ioG.unobserve(x.target);
      });
    }, { threshold: 0, rootMargin: '0px 0px -6% 0px' });
    [].forEach.call(groepen, function (g) { ioG.observe(g); });
  }

  /* De zwevende placeholder maakt plaats voor formulieren en de interactieve kaart. */
  var whatsapp = doc.querySelector('.whatsapp');
  if (whatsapp) {
    var whatsappFrame = null;
    var mobieleBalk = doc.querySelector('.mcta');
    var vrijeVlaken = [].slice.call(doc.querySelectorAll('form, [data-wereld]'));
    function ruimteVoorContact() {
      whatsappFrame = null;
      var balkHoogte = mobieleBalk ? mobieleBalk.getBoundingClientRect().height : 0;
      if (balkHoogte) whatsapp.style.bottom = (balkHoogte + 12) + 'px';
      else whatsapp.style.removeProperty('bottom');
      var knop = whatsapp.getBoundingClientRect();
      var bedekt = vrijeVlaken.some(function (el) {
        var vak = el.getBoundingClientRect();
        return vak.width > 0 && vak.height > 0 && vak.left < knop.right && vak.right > knop.left && vak.top < knop.bottom && vak.bottom > knop.top;
      });
      whatsapp.classList.toggle('is-bedekt', bedekt);
    }
    function planContactRuimte() { if (whatsappFrame === null) whatsappFrame = requestAnimationFrame(ruimteVoorContact); }
    window.addEventListener('scroll', planContactRuimte, { passive: true });
    window.addEventListener('resize', planContactRuimte);
    window.addEventListener('load', planContactRuimte);
    doc.addEventListener('focusin', planContactRuimte);
    if ('ResizeObserver' in window) {
      var contactMaten = new ResizeObserver(planContactRuimte);
      vrijeVlaken.forEach(function (el) { contactMaten.observe(el); });
      if (mobieleBalk) contactMaten.observe(mobieleBalk);
    }
    planContactRuimte();
  }

  /* 6. Binnenkomst via een anker (/diensten/#opslag): het doel direct tonen, ook als het nog verborgen is */
  if (location.hash) {
    try {
      var doel = doc.querySelector(location.hash);
      if (doel) { var r = doel.closest('[data-reveal]'); if (r) r.classList.add('in'); }
    } catch (e) { /* ongeldig anker */ }
  }
})();
