/* Veelgestelde vragen: het blauwe paneel naast de vragen groeit niet mee als er een vraag opengaat.
   Optie A uit website/review/vragen-beweging-20260928/ (dereus-d8, 28-09-2026: "Veelgestelde vragen - reduce the
   movement when clicking on the questions"), gekozen op 29-09-2026: "6. FAQ: A". Het raster rekt het paneel tot de
   hoogte van de vragenlijst, dus met elk antwoord groeide het mee: de vraagtekens werden groter en de verhuizer zakte
   mee. Bij de eerste klik op een vraag, zolang er nog niets open staat, krijgt het paneel de hoogte die het in rust had
   (--paneel-rust) en .is-vast op de sectie; die houdt het. Alleen de lijst beweegt nog. Verandert de breedte, dan laat
   het los en meet het bij de volgende klik opnieuw. Zonder JavaScript blijft alles zoals het was. De opmaak staat in
   css/blok/vragen.css; onder 900px is het paneel een kaart boven de lijst en doet dit niets. */
(function () {
  'use strict';
  var breed = window.matchMedia('(min-width: 900px)');
  var secties = document.querySelectorAll('.b-vragen--paneel');
  if (!secties.length) return;
  secties.forEach(function (sectie) {
    var paneel = sectie.querySelector('.vragen__kop');
    if (!paneel) return;
    // capture: de klik komt hier voor de details opengaat, dus de gemeten hoogte is die in rust
    sectie.addEventListener('click', function (e) {
      if (!breed.matches || sectie.classList.contains('is-vast')) return;
      if (!e.target.closest || !e.target.closest('.vraag > summary')) return;
      if (sectie.querySelector('.vraag[open]')) return;   // er staat al iets open: dit is niet de ruststand
      sectie.style.setProperty('--paneel-rust', paneel.getBoundingClientRect().height + 'px');
      sectie.classList.add('is-vast');
    }, true);
  });
  var vorige = window.innerWidth;
  window.addEventListener('resize', function () {
    if (window.innerWidth === vorige) return;            // alleen de breedte; de adresbalk op de telefoon telt niet
    vorige = window.innerWidth;
    secties.forEach(function (sectie) {
      sectie.classList.remove('is-vast');
      sectie.style.removeProperty('--paneel-rust');
    });
  });
})();
