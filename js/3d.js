/* Verhuisbedrijf De Reus · diepte (hoort bij css/3d.css). Geen beweging: alleen vaste 3D-lagen. */
(function () {
  'use strict';
  document.querySelectorAll('.laag[data-diepte]').forEach(function (el) {
    el.style.setProperty('--z', el.getAttribute('data-diepte') + 'px');
  });
})();
