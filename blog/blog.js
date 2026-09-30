/* Verhuisbedrijf De Reus: verhuisblog. Losse onderdelen, elk start alleen als zijn markup er is.
   Kop, menu (lade) en snelbalk doet /js/site.js van de site; hier alleen wat de blog zelf heeft. */
(function () {
  'use strict';
  var $ = function (s, w) { return (w || document).querySelector(s); };
  var $$ = function (s, w) { return Array.prototype.slice.call((w || document).querySelectorAll(s)); };
  var opslag = {
    lees: function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    zet: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* privévenster: dan maar niet onthouden */ } }
  };

  /* ---- blogoverzicht: onderwerp-tegels + zoeken tonen de artikelen als groep ---- */
  var rij = $('[data-artikelrij]');
  if (rij) {
    var kaarten = $$('[data-onderwerp]', rij);
    var cta = $('.artikelrij__cta', rij);
    var tegels = $$('[data-filter]');
    var zoekveld = $('#zoekveld');
    var aantal = $('[data-aantal]'), leeg = $('[data-leeg]'), leegTerm = $('[data-leeg-term]');
    var uitgelicht = $('[data-uitgelicht-blok]'), filterbalk = $('[data-filterbalk]');
    var kopLabel = $('[data-kop-label]'), kopTitel = $('[data-kop-titel]');
    var kopStandaard = { label: kopLabel && kopLabel.textContent, titel: kopTitel && kopTitel.textContent };
    var status = { onderwerp: 'alles', term: '' };
    var normaal = function (s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    var naamVan = function (k) {
      var t = tegels.filter(function (t) { return t.dataset.filter === k; })[0];
      return t ? $('.tegel__naam', t).textContent : k;
    };

    var toon = function (schuif) {
      var term = normaal(status.term).trim(), n = 0;
      // zonder filter staat het uitgelichte artikel groot bovenaan; met filter gaat dat blok weg en staat de groep direct onder de tegels
      var standaard = status.onderwerp === 'alles' && !term;
      kaarten.forEach(function (li) {
        var past = (status.onderwerp === 'alles' || li.dataset.onderwerp === status.onderwerp) &&
          (!term || normaal(li.dataset.zoek).indexOf(term) > -1);
        li.hidden = !past || (standaard && li.hasAttribute('data-uitgelicht')); if (past) n++;
      });
      if (uitgelicht) uitgelicht.hidden = !standaard;
      rij.classList.toggle('is-gefilterd', !standaard);   // offertekaart achteraan, niet midden in de groep
      if (cta) cta.hidden = n === 0;
      if (kopLabel && kopTitel) {
        var onderwerp = status.onderwerp === 'alles' ? '' : naamVan(status.onderwerp);
        if (standaard) { kopLabel.textContent = kopStandaard.label; kopTitel.textContent = kopStandaard.titel; }
        else if (term) { kopLabel.textContent = onderwerp ? 'Zoeken in ' + onderwerp : 'Zoeken'; kopTitel.textContent = '“' + status.term.trim() + '”'; }
        else { kopLabel.textContent = 'Onderwerp'; kopTitel.textContent = onderwerp; }
      }
      if (filterbalk) filterbalk.classList.toggle('is-aan', !standaard);
      tegels.forEach(function (t) { t.setAttribute('aria-pressed', String(t.dataset.filter === status.onderwerp)); });
      if (aantal) aantal.textContent = n === 1 ? '1 artikel' : n + ' artikelen';
      if (leeg) { leeg.hidden = n > 0; if (leegTerm) leegTerm.textContent = status.term ? '“' + status.term + '”' : 'dit onderwerp'; }
      var url = new URL(location.href);
      if (status.onderwerp === 'alles') url.searchParams.delete('onderwerp'); else url.searchParams.set('onderwerp', status.onderwerp);
      if (term) url.searchParams.set('zoek', status.term); else url.searchParams.delete('zoek');
      history.replaceState(null, '', url);
      if (schuif) $('#artikelen').scrollIntoView({ block: 'start', behavior: schuif === 'direct' ? 'instant' : 'smooth' });
    };
    var kies = function (k) { status.onderwerp = k; toon(k !== 'alles'); };

    tegels.forEach(function (t) {
      t.addEventListener('click', function () { kies(t.dataset.filter === status.onderwerp ? 'alles' : t.dataset.filter); });
    });
    // onderwerp-labels op de kaarten filteren hier ter plekke, zonder de pagina opnieuw te laden
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="/blog/?onderwerp="]');
      if (!a || e.ctrlKey || e.metaKey || e.shiftKey || e.button) return;
      var k = new URL(a.href).searchParams.get('onderwerp');
      if (!tegels.some(function (t) { return t.dataset.filter === k; })) return;
      e.preventDefault(); status.term = ''; if (zoekveld) zoekveld.value = ''; kies(k);
    });
    var zoekform = $('[data-zoek]');
    if (zoekform) zoekform.addEventListener('submit', function (e) { e.preventDefault(); status.term = zoekveld.value; toon(true); });
    if (zoekveld) zoekveld.addEventListener('input', function () { status.term = zoekveld.value; toon(false); });
    $$('[data-zoekterm]').forEach(function (b) {
      b.addEventListener('click', function () { zoekveld.value = status.term = b.dataset.zoekterm; status.onderwerp = 'alles'; toon(true); });
    });
    $$('[data-alles]').forEach(function (b) {
      b.addEventListener('click', function () { status.onderwerp = 'alles'; status.term = ''; if (zoekveld) zoekveld.value = ''; toon(false); });
    });
    var q = new URLSearchParams(location.search);
    if (q.get('onderwerp') && tegels.some(function (t) { return t.dataset.filter === q.get('onderwerp'); })) status.onderwerp = q.get('onderwerp');
    if (q.get('zoek')) { status.term = q.get('zoek'); if (zoekveld) zoekveld.value = status.term; }
    if (status.onderwerp !== 'alles' || status.term) toon('direct');   // via een onderwerp-link binnengekomen: meteen naar de groep
  }

  /* ---- artikel: leesbalk ---- */
  var tekst = $('[data-tekst]');
  var balk = $('.leesbalk');
  if (tekst && balk) {
    var meet = function () {
      var r = tekst.getBoundingClientRect(), h = r.height - innerHeight * .6;
      var p = Math.min(1, Math.max(0, -r.top / (h > 0 ? h : 1)));
      balk.style.setProperty('--gelezen', p.toFixed(3));
    };
    meet();
    window.addEventListener('scroll', meet, { passive: true });
    window.addEventListener('resize', meet);
  }

  /* ---- artikel: inhoudsopgave volgt de kop die in beeld is ---- */
  var links = $$('[data-inhoud] a');
  if (links.length && 'IntersectionObserver' in window) {
    var koppen = links.map(function (a) { return document.getElementById(a.hash.slice(1)); }).filter(Boolean);
    var markeer = function () {
      var actief = null;
      koppen.forEach(function (k) { if (k.getBoundingClientRect().top < innerHeight * .35) actief = k; });
      if (!actief) actief = koppen[0];
      links.forEach(function (a) { a.classList.toggle('is-actief', a.hash.slice(1) === actief.id); });
    };
    var io = new IntersectionObserver(markeer, { rootMargin: '0px 0px -55% 0px' });
    koppen.forEach(function (k) { io.observe(k); });
    window.addEventListener('scroll', markeer, { passive: true });
    markeer();
  }

  /* ---- artikel: link kopiëren / delen ---- */
  $$('[data-kopieer]').forEach(function (b) {
    b.addEventListener('click', function () {
      var klaar = function () {
        b.classList.add('is-gekopieerd'); b.setAttribute('aria-label', 'Link gekopieerd');
        setTimeout(function () { b.classList.remove('is-gekopieerd'); b.setAttribute('aria-label', 'Kopieer de link'); }, 1800);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(klaar, klaar); else klaar();
    });
  });

  /* ---- afvinklijst: per bezoeker onthouden ---- */
  $$('[data-afvink]').forEach(function (lijst) {
    var sleutel = 'dereus-blog-afvink-' + lijst.dataset.afvink;
    var vakjes = $$('input[type=checkbox]', lijst), stand = $('[data-stand]', lijst);
    var bewaard = opslag.lees(sleutel) || [];
    vakjes.forEach(function (v, i) { v.checked = bewaard.indexOf(i) > -1; });
    var tel = function () {
      var aan = vakjes.filter(function (v) { return v.checked; }).length;
      if (stand) stand.textContent = aan + ' van ' + vakjes.length + ' klaar';
      opslag.zet(sleutel, vakjes.map(function (v, i) { return v.checked ? i : -1; }).filter(function (i) { return i > -1; }));
    };
    vakjes.forEach(function (v) { v.addEventListener('change', tel); });
    var wis = $('[data-wis]', lijst);
    if (wis) wis.addEventListener('click', function () { vakjes.forEach(function (v) { v.checked = false; }); tel(); });
    tel();
  });

  /* ---- dozenschatter: m2 x factor per inboedel + opslag per kamer en per bewoner, bandbreedte 0,9 tot 1,15 ---- */
  var schatter = $('[data-schatter]');
  if (schatter) {
    var FACTOR = { licht: .35, gemiddeld: .5, zwaar: .65 }, KAMER = { licht: 6, gemiddeld: 9, zwaar: 12 }, BEWONER = { licht: 3, gemiddeld: 5, zwaar: 7 };
    var getal = function (n, std) { var v = parseInt($('[name=' + n + ']', schatter).value, 10); return isNaN(v) || v < 0 ? std : v; };
    var reken = function () {
      var m2 = Math.min(getal('m2', 90), 600), kamers = Math.min(getal('kamers', 3), 20), bewoners = Math.min(getal('bewoners', 2), 12);
      var pak = $('[name=spullen]', schatter).value;
      var basis = m2 * FACTOR[pak] + kamers * KAMER[pak] + bewoners * BEWONER[pak];
      var min = Math.round(Math.max(5, basis * .9)), max = Math.round(Math.max(8, basis * 1.15)), ruw = (min + max) / 2;
      var advies = ruw >= 50 ? Math.round(ruw / 5) * 5 : Math.round(ruw);
      $('[data-getal]', schatter).textContent = advies + ' dozen';
      $('[data-bereik]', schatter).textContent = 'Reken op ' + min + ' tot ' + max + '.';
      $('[data-detail]', schatter).textContent = 'Waarvan ongeveer ' + Math.max(1, Math.round(advies * .25)) + ' boekendozen en ' + Math.max(1, Math.round(bewoners * 1.5)) + ' garderobedozen.';
    };
    schatter.addEventListener('input', reken);
    schatter.addEventListener('change', reken);
    reken();
  }
})();
