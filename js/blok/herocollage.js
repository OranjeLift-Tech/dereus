/* Bewegende collage in de hero van de home (_werk/blokken/herocollage.py). Beeld 2 tot 4 staan in een <template>
   en worden pas na het load-event ingezet en geladen, dus ze vechten nooit om bandbreedte met het teambeeld (de LCP) of met beeld 1. De beweging start als
   alle vier gedecodeerd zijn. Met prefers-reduced-motion of Save-Data blijft beeld 1 staan en worden de andere
   nooit opgehaald. Buiten beeld of in een verborgen tab staat de beweging stil; de knop zet hem stil tot hij
   opnieuw wordt ingedrukt. */
(function () {
  'use strict';
  var c = document.querySelector('[data-collage]');
  var knop = document.querySelector('.collage__knop');
  if (!c) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (navigator.connection && navigator.connection.saveData) return;
  var stil = false, inBeeld = true;
  function zet() { c.classList.toggle('pauze', stil || !inBeeld || document.hidden); }
  function start() {
    // beeld 2 tot 4 staan in een <template>: niet geladen en geen img in de pagina tot ze hier worden ingezet
    var sjablonen = c.querySelectorAll('template');
    for (var t = 0; t < sjablonen.length; t++) sjablonen[t].parentNode.replaceChild(sjablonen[t].content.cloneNode(true), sjablonen[t]);
    var klaar = Array.prototype.map.call(c.querySelectorAll('img'), function (img) {
      return img.decode ? img.decode().catch(function () {}) : null;
    });
    Promise.all(klaar).then(function () {
      c.classList.add('speelt');
      if (knop) knop.hidden = false;
    });
  }
  if (document.readyState === 'complete') start();
  else window.addEventListener('load', start, { once: true });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (e) { inBeeld = e[0].isIntersecting; zet(); }).observe(c);
  }
  document.addEventListener('visibilitychange', zet);
  if (knop) knop.addEventListener('click', function () {
    stil = !stil;
    knop.setAttribute('aria-pressed', String(stil));
    zet();
  });
})();
