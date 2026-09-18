/* Werkwijze-trap: treden komen omhoog zodra de trap in beeld is. Zonder JS blijft alles gewoon zichtbaar. */
(function () {
  'use strict';
  var trap = document.querySelector('.trap');
  if (!trap || !('IntersectionObserver' in window)) return;
  trap.setAttribute('data-zien', '');
  var io = new IntersectionObserver(function (items) {
    items.forEach(function (it) {
      if (it.isIntersecting) { trap.classList.add('is-zichtbaar'); io.disconnect(); }
    });
  }, { threshold: 0.2 });
  io.observe(trap);
})();
