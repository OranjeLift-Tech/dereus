/* Wisselend woord in de H1 van de home: "Sterk in verhuizen", dan inpakken, sjouwen, opbouwen en ontruimen.
   De woorden staan in data-woorden; zonder script blijft het eerste woord staan. Elke 2,6 s gaat het oude
   woord weg (0,25 s) en komt het nieuwe (0,25 s), zie hero.css. Na twee rondes blijft het op het eerste
   woord staan, zodat de kop niet eindeloos beweegt (WCAG 2.2.2). Bij prefers-reduced-motion wisselt er niets.
   Een schermlezer hoort steeds het eerste woord: de wisselende woorden zijn aria-hidden. */
(function () {
  'use strict';
  var em = document.querySelector('.hero__wissel[data-woorden]');
  var rustig = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!em || rustig.matches) return;
  var lijst = em.getAttribute('data-woorden').split('|');
  if (lijst.length < 2) return;
  var vast = document.createElement('span');
  vast.className = 'vh';
  vast.textContent = lijst[0];
  var stapel = document.createElement('span');
  stapel.className = 'hero__woorden';
  stapel.setAttribute('aria-hidden', 'true');
  var woorden = lijst.map(function (tekst, n) {
    var s = document.createElement('span');
    s.className = 'hero__woord' + (n ? '' : ' is-actief');
    s.textContent = tekst;
    stapel.appendChild(s);
    return s;
  });
  em.textContent = '';
  em.appendChild(vast);
  em.appendChild(stapel);
  var nu = 0, stappen = lijst.length * 2;
  function stap() {
    if (rustig.matches) return;
    if (document.hidden) { setTimeout(stap, 2600); return; }
    var oud = woorden[nu];
    nu = (nu + 1) % woorden.length;
    var nieuw = woorden[nu];
    oud.classList.remove('is-actief');
    oud.classList.add('is-weg');
    nieuw.classList.remove('is-weg');
    nieuw.classList.add('is-actief');
    // de andere woorden zakken onzichtbaar terug naar onder, klaar om van onder binnen te komen
    woorden.forEach(function (w) { if (w !== oud && w !== nieuw) w.classList.remove('is-weg'); });
    if (--stappen > 0) setTimeout(stap, 2600);
  }
  setTimeout(stap, 2600);
})();
