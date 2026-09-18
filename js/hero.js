/* Snelle offerte in de hero: zet van/naar/datum door naar het offerteformulier en spring erheen. */
(function () {
  var snel = document.querySelector('[data-snelofferte]');
  if (!snel) return;
  var koppel = { van: 'o-woonplaats', naar: 'o-toekomst', datum: 'o-datum' };
  snel.addEventListener('submit', function (e) {
    e.preventDefault();
    Object.keys(koppel).forEach(function (naam) {
      var bron = snel.elements[naam], doel = document.getElementById(koppel[naam]);
      if (bron && doel && bron.value) doel.value = bron.value;
    });
    var offerte = document.getElementById('offerte');
    if (offerte) offerte.scrollIntoView({ block: 'start' });
    var naamveld = document.getElementById('o-naam');
    if (naamveld) setTimeout(function () { naamveld.focus({ preventScroll: true }); }, 500);
  });
})();
