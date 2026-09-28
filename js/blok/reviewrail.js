/* Reviews als rail (blok reviewrail, /werkwijze/ #reviews), naar reviews.js van referentie B: de knoppen, de
   voortgangsbalk en "Lees verder" onder een lange review. Zonder JS scrollt de rail gewoon en staat elke tekst
   er helemaal. Geen foto's en geen tekenende ring: de site staat stil, alleen de rail schuift op een klik. */
(function () {
  'use strict';
  var rails = document.querySelectorAll('.b-reviewrail__rail');
  if (!rails.length) return;
  var rustig = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  var teller = 0;

  [].forEach.call(rails, function (rail) {
    var lijst = rail.querySelector('.b-reviewrail__kaarten');
    var nav = rail.querySelector('.b-reviewrail__nav');
    if (!lijst || !nav) return;
    rail.classList.add('b-reviewrail__rail--js');

    // "Lees verder" onder elke tekst; verborgen zolang de tekst in zes regels past.
    var knoppen = [];
    [].forEach.call(lijst.querySelectorAll('.b-reviewrail__tekst'), function (t) {
      var p = t.querySelector('p');
      if (!p) return;
      t.id = t.id || ('reviewrail-tekst-' + (++teller));
      var k = document.createElement('button');
      k.type = 'button'; k.className = 'b-reviewrail__lees'; k.textContent = 'Lees verder'; k.hidden = true;
      k.setAttribute('aria-expanded', 'false'); k.setAttribute('aria-controls', t.id);
      t.parentNode.insertBefore(k, t.nextSibling);
      k.addEventListener('click', function () {
        var open = t.classList.toggle('is-open');
        k.setAttribute('aria-expanded', open ? 'true' : 'false');
        k.textContent = open ? 'Minder tonen' : 'Lees verder';
        if (!open) k.hidden = p.scrollHeight <= p.clientHeight + 2;
        stand();
      });
      knoppen.push([t, p, k]);
    });
    function meetTeksten() {
      knoppen.forEach(function (x) { if (!x[0].classList.contains('is-open')) x[2].hidden = x[1].scrollHeight <= x[1].clientHeight + 2; });
    }

    var terug = nav.querySelector('.b-reviewrail__knop--terug');
    var verder = nav.querySelector('.b-reviewrail__knop--verder');
    var balk = nav.querySelector('.b-reviewrail__voortgang i');

    // Eén kaart per klik: de breedte van een kaart plus de ruimte ertussen.
    function stap() {
      var k = lijst.querySelector('.b-reviewrail__kaart');
      var gap = parseFloat(getComputedStyle(lijst).columnGap) || 16;
      return k ? k.getBoundingClientRect().width + gap : lijst.clientWidth * .8;
    }
    function schuif(richting, knop) {
      if (knop.getAttribute('aria-disabled') === 'true') return;
      lijst.scrollBy({ left: richting * stap(), behavior: rustig ? 'auto' : 'smooth' });
    }
    terug.addEventListener('click', function () { schuif(-1, terug); });
    verder.addEventListener('click', function () { schuif(1, verder); });

    var wacht = false;
    function stand() {
      wacht = false;
      var max = lijst.scrollWidth - lijst.clientWidth;
      nav.hidden = max <= 4;
      terug.setAttribute('aria-disabled', lijst.scrollLeft <= 4 ? 'true' : 'false');
      verder.setAttribute('aria-disabled', lijst.scrollLeft >= max - 4 ? 'true' : 'false');
      var deel = Math.min(1, lijst.clientWidth / Math.max(1, lijst.scrollWidth));
      balk.style.width = (deel * 100) + '%';
      balk.style.transform = 'translateX(' + (lijst.scrollLeft / Math.max(1, lijst.clientWidth) * 100) + '%)';
    }
    function later() { if (!wacht) { wacht = true; requestAnimationFrame(stand); } }
    lijst.addEventListener('scroll', later, { passive: true });
    window.addEventListener('resize', function () { meetTeksten(); later(); }, { passive: true });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { meetTeksten(); stand(); });
    meetTeksten(); stand();
  });
})();
