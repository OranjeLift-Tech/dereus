/* Eén stap tegelijk. Lopende hoogteanimaties worden vanaf hun actuele maat voortgezet. */
(function () {
  'use strict';
  var rustig = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-werkwijze]').forEach(function (blok) {
    var lagen = [].slice.call(blok.querySelectorAll('[data-stap-beeld]'));
    var gekozen = 0;
    var stappen = [].map.call(blok.querySelectorAll('.werkwijze__stap'), function (details) {
      return { details: details, knop: details.querySelector('summary'), inhoud: details.querySelector('.werkwijze__antwoord'),
        binnen: details.querySelector('.werkwijze__antwoord-in'), open: details.open, animatie: null };
    });
    if (!stappen.length) return;
    blok.classList.add('is-verrijkt');

    function beeld(index) {
      gekozen = index;
      var laag = lagen[index], foto = laag && laag.querySelector('img');
      if (!foto) return;
      // Het desktopbeeld is op mobiel verborgen; laad de gekozen foto ook dan voor een latere resize.
      foto.loading = 'eager';
      function wissel() {
        if (gekozen !== index) return;
        lagen.forEach(function (el, i) { el.classList.toggle('is-actief', i === index); });
      }
      if (foto.complete && foto.naturalWidth) wissel();
      else if (foto.decode) foto.decode().then(wissel).catch(function () {});
      else foto.addEventListener('load', wissel, { once: true });
    }

    function zet(stap, open, direct) {
      var hoogte = stap.details.open ? stap.inhoud.getBoundingClientRect().height : 0;
      if (stap.animatie) { stap.animatie.cancel(); stap.animatie = null; }
      stap.open = open;
      stap.knop.setAttribute('aria-expanded', String(open));
      stap.details.classList.toggle('is-sluitend', !open);
      function klaar() {
        stap.details.open = open;
        stap.inhoud.style.height = '';
        stap.details.classList.remove('is-sluitend');
        stap.animatie = null;
      }
      if (direct || rustig.matches || !stap.inhoud.animate) { klaar(); return; }
      stap.details.open = true;
      var doel = open ? stap.binnen.getBoundingClientRect().height : 0;
      stap.inhoud.style.height = doel + 'px';
      var animatie = stap.inhoud.animate([{ height: hoogte + 'px' }, { height: doel + 'px' }],
        { duration: 280, easing: 'cubic-bezier(.22,.61,.36,1)' });
      stap.animatie = animatie;
      animatie.onfinish = function () { if (stap.animatie === animatie) klaar(); };
    }

    function kies(index, open, direct) {
      stappen.forEach(function (stap, i) {
        var gewenst = i === index && open;
        if (stap.open !== gewenst || direct) zet(stap, gewenst, direct);
      });
      if (open) beeld(index);
    }
    stappen.forEach(function (stap, index) {
      stap.knop.setAttribute('aria-expanded', String(stap.open));
      stap.knop.addEventListener('click', function (event) {
        event.preventDefault();
        kies(index, !stap.open, false);
      });
      stap.knop.addEventListener('keydown', function (event) {
        var doel = event.key === 'ArrowDown' ? (index + 1) % stappen.length :
          event.key === 'ArrowUp' ? (index - 1 + stappen.length) % stappen.length :
          event.key === 'Home' ? 0 : event.key === 'End' ? stappen.length - 1 : -1;
        if (doel > -1) { event.preventDefault(); stappen[doel].knop.focus(); }
      });
    });
    function anker() {
      var index = stappen.findIndex(function (stap) { return '#' + stap.details.parentElement.id === location.hash; });
      if (index > -1) kies(index, true, true);
    }
    window.addEventListener('hashchange', anker);
    anker();
    function stopAnimaties() {
      stappen.forEach(function (stap) { if (stap.animatie) zet(stap, stap.open, true); });
    }
    window.addEventListener('resize', stopAnimaties);
    if (rustig.addEventListener) rustig.addEventListener('change', stopAnimaties);
  });
})();
