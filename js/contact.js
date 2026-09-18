/* Contact: lopende klok + dagbalk (Nederlandse tijd) en de medewerker die uit het scherm komt. */
(function () {
  'use strict';
  var rustig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Klok en dagbalk. Altijd Nederlandse tijd, ook voor bezoekers in het buitenland. */
  var klok = document.querySelector('[data-klok]');
  if (klok) {
    var uur = klok.querySelector('.klok__uur'), min = klok.querySelector('.klok__min'), sec = klok.querySelector('.klok__sec');
    var boog = klok.querySelector('.klok__open');
    var tijd = document.querySelector('[data-kloktijd]');
    var balk = document.querySelector('.dagbalk');
    var fmt = new Intl.DateTimeFormat('nl-NL', { timeZone: 'Europe/Amsterdam', hour: '2-digit', minute: '2-digit', second: '2-digit', weekday: 'short', hour12: false });

    function nu() {
      var d = {};
      fmt.formatToParts(new Date()).forEach(function (p) { d[p.type] = p.value; });
      return { u: +d.hour % 24, m: +d.minute, s: +d.second, zondag: d.weekday.toLowerCase().indexOf('zo') === 0 };
    }
    // Draaien via CSS (draaipunt staat in contact-plus.css). De hoek loopt altijd op, zodat een wijzer
    // bij 60 seconden niet terugzwiept.
    function draai(el, graden) {
      if (!el) return;
      var vorige = el._hoek;
      if (vorige != null) { while (graden < vorige - 1) graden += 360; }
      el._hoek = graden;
      el.style.transform = 'rotate(' + graden + 'deg)';
    }

    function tik() {
      var t = nu();
      var van = t.zondag ? 9 : 8, tot = t.zondag ? 17 : 20;
      draai(uur, (t.u % 12) * 30 + t.m * 0.5);
      draai(min, t.m * 6 + t.s * 0.1);
      draai(sec, t.s * 6);
      if (tijd) tijd.firstChild.nodeValue = ('0' + t.u).slice(-2) + '.' + ('0' + t.m).slice(-2);
      if (balk) {
        balk.style.setProperty('--van', van);
        balk.style.setProperty('--tot', tot);
        balk.style.setProperty('--nu', (t.u + t.m / 60).toFixed(2));
      }
      // gele boog op de wijzerplaat: de uren waarop we vandaag bereikbaar zijn (12-uurs klok)
      if (boog && !boog.getAttribute('d')) {
        var r = 40, uren = Math.min(tot - van, 11.99);
        var a0 = (van % 12) * 30 - 90, a1 = a0 + uren * 30;
        var p = function (a) { var k = a * Math.PI / 180; return (50 + r * Math.cos(k)).toFixed(2) + ' ' + (50 + r * Math.sin(k)).toFixed(2); };
        boog.setAttribute('d', 'M' + p(a0) + ' A' + r + ' ' + r + ' 0 ' + (uren * 30 > 180 ? 1 : 0) + ' 1 ' + p(a1));
      }
    }
    tik();
    if (!rustig) setInterval(tik, 1000); else setInterval(tik, 30000);
  }

  /* 2. Uit het scherm: foto en uitsnede bewegen tegen elkaar in als de muis beweegt. */
  var foto = document.querySelector('[data-uitscherm]');
  if (foto && !rustig && window.matchMedia('(hover: hover)').matches) {
    var vak = foto.closest('.gluur') || foto, bezig = false, mx = 0, my = 0;
    vak.addEventListener('pointermove', function (e) {
      var r = vak.getBoundingClientRect();
      mx = ((e.clientX - r.left) / r.width - 0.5) * 2;
      my = ((e.clientY - r.top) / r.height - 0.5) * 2;
      if (bezig) return;
      bezig = true;
      requestAnimationFrame(function () {
        foto.style.setProperty('--mx', mx.toFixed(3));
        foto.style.setProperty('--my', my.toFixed(3));
        bezig = false;
      });
    });
    vak.addEventListener('pointerleave', function () {
      foto.style.setProperty('--mx', 0); foto.style.setProperty('--my', 0);
    });
  }
})();
