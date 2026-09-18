/* Verhuisbedrijf De Reus · site scripts */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Mobiel menu: lade van rechts, focus blijft in de lade */
  var knop = document.getElementById('menuknop');
  var lade = document.getElementById('lade');
  var paneel = lade && lade.querySelector('.lade__paneel');
  var vorige = null;
  function zetLade(open) {
    if (!lade) return;
    lade.classList.toggle('is-open', open);
    lade.setAttribute('aria-hidden', open ? 'false' : 'true');
    document.body.classList.toggle('lade-open', open);
    knop.setAttribute('aria-expanded', String(open));
    if (open) {
      vorige = document.activeElement;
      lade.querySelector('.lade__sluit').focus();
    } else if (vorige) {
      vorige.focus(); vorige = null;
    }
  }
  if (knop && lade) {
    knop.addEventListener('click', function () { zetLade(true); });
    lade.querySelector('.lade__sluit').addEventListener('click', function () { zetLade(false); });
    lade.querySelector('.lade__scrim').addEventListener('click', function () { zetLade(false); });
    lade.addEventListener('click', function (e) { if (e.target.closest('a')) { vorige = null; zetLade(false); } });
    document.addEventListener('keydown', function (e) {
      if (!lade.classList.contains('is-open')) return;
      if (e.key === 'Escape') { zetLade(false); return; }
      if (e.key !== 'Tab') return;
      var f = paneel.querySelectorAll('a, button');
      var eerste = f[0], laatste = f[f.length - 1];
      if (e.shiftKey && document.activeElement === eerste) { e.preventDefault(); laatste.focus(); }
      else if (!e.shiftKey && document.activeElement === laatste) { e.preventDefault(); eerste.focus(); }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1023 && lade.classList.contains('is-open')) zetLade(false);
    });
  }

  /* 2. Header: transparant over de hero, vaste lichte balk zodra de utilitybalk uit beeld is */
  var header = document.querySelector('.header');
  var utility = document.querySelector('.utility');
  var utilityH = 0;
  function meet() {
    utilityH = utility ? utility.offsetHeight : 0;
    document.documentElement.style.setProperty('--dr-utility-h', utilityH + 'px');
  }
  function scrol() { header.classList.toggle('is-vast', window.scrollY > utilityH); }
  meet();
  window.addEventListener('resize', function () { meet(); scrol(); });
  window.addEventListener('scroll', scrol, { passive: true });
  scrol();

  /* 3. Actief menu-item bij scrollen */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"], .lade__nav a[href^="#"]'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (items) {
      items.forEach(function (it) {
        if (!it.isIntersecting) return;
        links.forEach(function (a) {
          if (a.getAttribute('href') === '#' + it.target.id) a.setAttribute('aria-current', 'true');
          else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ['over-ons', 'diensten', 'werkwijze', 'contact'].forEach(function (id) {
      var el = document.getElementById(id); if (el) io.observe(el);
    });

  }

  /* 5. Formulieren: controle met duidelijke foutmelding (merkboek 7.3) */
  function geldig(input) {
    var v = input.value.trim();
    if (input.required && !v) return false;
    if (v && input.type === 'email') return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
    if (v && input.type === 'tel') return v.replace(/[^\d]/g, '').length >= 10;
    return true;
  }
  function toon(input, ok) {
    var fout = input.getAttribute('aria-describedby') && document.getElementById(input.getAttribute('aria-describedby'));
    input.setAttribute('aria-invalid', String(!ok));
    if (fout) fout.hidden = ok;
  }
  document.querySelectorAll('form.formulier').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      var eerste = null;
      form.querySelectorAll('input, textarea').forEach(function (inp) {
        var ok = geldig(inp);
        toon(inp, ok);
        if (!ok && !eerste) eerste = inp;
      });
      if (eerste) { e.preventDefault(); eerste.focus(); return; }
      var m = form.querySelector('.melding');
      if (!m) { m = document.createElement('p'); m.className = 'melding'; m.setAttribute('role', 'status'); form.appendChild(m); }
      m.textContent = '✓ Bedankt! Uw e-mailprogramma opent met de aanvraag. Verstuur die mail, dan belt uw verhuisadviseur u binnen 24 uur.';
    });
    form.addEventListener('input', function (e) {
      if (e.target.getAttribute('aria-invalid') === 'true') toon(e.target, geldig(e.target));
    });
  });

  /* 6. Contact: nu bereikbaar? Tijden in Nederlandse tijd, ook als de bezoeker in het buitenland zit */
  var status = document.querySelector('.bereikbaar');
  if (status && window.Intl) {
    try {
      var delen = {};
      new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Amsterdam', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
        .formatToParts(new Date()).forEach(function (d) { delen[d.type] = d.value; });
      var dag = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(delen.weekday);
      var nu = parseInt(delen.hour, 10) * 60 + parseInt(delen.minute, 10);
      var zondag = dag === 0;
      var open = zondag ? 9 * 60 : 8 * 60, dicht = zondag ? 17 * 60 : 20 * 60;
      var isOpen = nu >= open && nu < dicht;
      var tekst = status.querySelector('.bereikbaar__tekst');
      if (isOpen) {
        tekst.textContent = 'Nu bereikbaar, tot ' + (zondag ? '17.00' : '20.00') + ' uur';
      } else {
        var morgenZondag = nu >= dicht && dag === 6;
        var vanaf = nu < open ? (zondag ? '09.00' : '08.00') : (morgenZondag ? '09.00' : '08.00');
        tekst.textContent = 'Nu gesloten, ' + (nu < open ? 'vandaag' : 'morgen') + ' weer bereikbaar vanaf ' + vanaf + ' uur';
        status.classList.add('is-dicht');
      }
      status.hidden = false;
      var rij = document.querySelector('.openingstijden [data-dagen="' + (zondag ? '0' : '1-6') + '"]');
      if (rij) rij.classList.add('is-vandaag');
    } catch (e) { /* zonder status is de pagina ook compleet */ }
  }
})();
