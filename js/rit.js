/* Werkwijze-rit: de vrachtwagen rijdt van het oude naar het nieuwe huis terwijl je scrollt. */
(function () {
  'use strict';
  var rit = document.querySelector('[data-rit]');
  if (!rit || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var stil;
  function zet() {
    var r = rit.getBoundingClientRect();
    var vh = window.innerHeight;
    // 0 als de strook onderin het beeld verschijnt, 1 als hij bovenin bijna weg is
    var p = (vh - r.top) / (vh + r.height * 0.4);
    p = Math.min(1, Math.max(0, p));
    rit.style.setProperty('--p', p.toFixed(4));
  }
  function scroll() {
    rit.classList.add('is-rijdend');
    clearTimeout(stil);
    stil = setTimeout(function () { rit.classList.remove('is-rijdend'); }, 180);
    requestAnimationFrame(zet);
  }
  window.addEventListener('scroll', scroll, { passive: true });
  window.addEventListener('resize', zet);
  zet();
})();
