/* Contact: het adres op een wereldbol (zelfde aanpak als de locatiekaart van De Bresser).
 * De bol draait even, draait naar Europa en vliegt dan naar het hoofdkantoor in Den Haag.
 * Zonder WebGL: platte Leaflet-kaart. Bij een laadfout blijft de lokale kaart staan.
 * Esri-tegels werken zonder sleutel. */
(function () {
  'use strict';
  var paneel = document.querySelector('[data-wereld]');
  if (!paneel) return;

  var LAT = parseFloat(paneel.getAttribute('data-lat')), LNG = parseFloat(paneel.getAttribute('data-lng'));
  var ESRI = 'https://server.arcgisonline.com/ArcGIS/rest/services/';
  var MAPLIBRE = 'https://cdn.jsdelivr.net/npm/maplibre-gl@5.24.0/dist/';
  var LEAFLET = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/';
  var ATTR = 'Kaart &copy; Esri, HERE, Garmin, &copy; OpenStreetMap-bijdragers';
  var ZOOM = 15.5;
  var rustig = window.matchMedia('(prefers-reduced-motion: reduce)');
  var poging = 0, wachttijd = null, geladen = false, opruimen = null, toetsenbord = false;
  var ICON = {
    huis: '<svg class="ic" aria-hidden="true"><use href="#i-pin"/></svg>',
    pin: '<svg class="ic" aria-hidden="true"><use href="#i-pin"/></svg>',
    wereld: '<svg class="ic" aria-hidden="true"><use href="#i-wereld"/></svg>'
  };

  function laadBibliotheek(css, js, aanwezig, ok, mis) {
    var mijn = poging, klaar = 0, afgehandeld = false;
    var l = document.createElement('link'), s;
    function fout() {
      if (afgehandeld || mijn !== poging) return;
      afgehandeld = true; l.remove(); if (s) s.remove(); mis();
    }
    function volgende() {
      if (afgehandeld || mijn !== poging) return;
      klaar++;
      if (klaar === 2) { afgehandeld = true; try { ok(); } catch (e) { herstel(); } }
    }
    l.rel = 'stylesheet'; l.href = css; l.onload = volgende; l.onerror = fout;
    document.head.appendChild(l);
    if (aanwezig) volgende();
    else {
      s = document.createElement('script'); s.src = js; s.onload = volgende; s.onerror = fout;
      document.head.appendChild(s);
    }
  }

  function maakKaart() {
    var box = document.createElement('div');
    box.className = 'wereld__kaart';
    box.setAttribute('role', 'region');
    box.setAttribute('aria-label', 'Kaart met het hoofdkantoor van De Reus aan de Lau Mazirellaan in Den Haag');
    paneel.insertBefore(box, paneel.firstChild);
    return box;
  }
  /* De pin is een echte link naar de routeplanner: wie op het kantoor klikt, kan er ook heen. */
  function routeLink() { var a = paneel.querySelector('.wereld__route'); return a ? a.href : ''; }
  function maakPin() {
    var href = routeLink(), el = document.createElement(href ? 'a' : 'div');
    el.className = 'wereld__marker';
    if (href) {
      el.href = href; el.target = '_blank'; el.rel = 'noopener';
      el.setAttribute('aria-label', 'Route plannen naar De Reus, Lau Mazirellaan 336 in Den Haag (opent in een nieuw tabblad)');
    }
    el.innerHTML = '<span class="wereld__pin">' + ICON.huis + '</span>';
    return el;
  }
  function knoppen(lijst) {
    var tools = document.createElement('div');
    tools.className = 'wereld__tools';
    lijst.forEach(function (k) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'wereld__knop';
      b.innerHTML = k[0] + k[1];
      b.addEventListener('click', k[2]);
      tools.appendChild(b);
    });
    paneel.appendChild(tools);
  }

  /* ---- wereldbol (MapLibre, globe-projectie) ---- */
  function bouwBol() {
    var ml = window.maplibregl, box = maakKaart(), map;
    var mijn = poging, zien = null;
    var START = { center: [-30, 28], zoom: 0.7 };
    try {
      map = new ml.Map({
        container: box,
        style: {
          version: 8,
          projection: { type: 'globe' },
          sky: {
            'sky-color': '#0F2D6B', 'horizon-color': '#1746A2', 'fog-color': '#E8EEF8',
            'sky-horizon-blend': 0.6, 'horizon-fog-blend': 0.6, 'fog-ground-blend': 0.8,
            'atmosphere-blend': ['interpolate', ['linear'], ['zoom'], 0, 1, 4, 0.8, 6, 0]
          },
          sources: {
            beeld: { type: 'raster', tileSize: 256, maxzoom: 19, tiles: [ESRI + 'World_Imagery/MapServer/tile/{z}/{y}/{x}'], attribution: ATTR },
            straat: { type: 'raster', tileSize: 256, maxzoom: 19, tiles: [ESRI + 'World_Street_Map/MapServer/tile/{z}/{y}/{x}'] }
          },
          layers: [
            { id: 'ruimte', type: 'background', paint: { 'background-color': '#0F2D6B' } },
            /* van ver satellietbeeld, dichterbij de straatkaart */
            { id: 'beeld', type: 'raster', source: 'beeld', maxzoom: 9, paint: { 'raster-opacity': ['interpolate', ['linear'], ['zoom'], 6, 1, 8, 0] } },
            { id: 'straat', type: 'raster', source: 'straat', minzoom: 5.5, paint: { 'raster-opacity': ['interpolate', ['linear'], ['zoom'], 6, 0, 8, 1] } }
          ]
        },
        center: START.center, zoom: START.zoom,
        attributionControl: false,
        scrollZoom: false, dragRotate: false, pitchWithRotate: false, touchPitch: false,
        dragPan: !window.matchMedia('(pointer: coarse)').matches,
        fadeDuration: 0
      });
    } catch (e) { box.remove(); startPlat(); return; }
    map.touchZoomRotate.disableRotation();
    map.addControl(new ml.NavigationControl({ showCompass: false }), 'top-right');
    map.addControl(new ml.AttributionControl({ compact: true }), 'top-right');

    var pin = maakPin();
    new ml.Marker({ element: pin, anchor: 'bottom' }).setLngLat([LNG, LAT]).addTo(map);
    function opZoom() { pin.classList.toggle('is-ver', map.getZoom() < 6); }
    map.on('zoom', opZoom);

    var draai = null, beurt = 0;
    function stop() { beurt++; if (draai) { cancelAnimationFrame(draai); draai = null; } }
    function vergroot() { map.resize(); }
    opruimen = function () {
      stop(); if (zien) zien.disconnect();
      window.removeEventListener('resize', vergroot); map.remove();
    };
    map.on('error', function () { if (mijn === poging && !geladen) herstel(); });
    /* pin boven het adreskaartje houden */
    function ruimte() { var info = paneel.querySelector('.wereld__info'); return { top: 40, bottom: (info ? info.offsetHeight : 0) + 12, left: 0, right: 0 }; }
    function naarAdres(duur) {
      map.flyTo({ center: [LNG, LAT], zoom: ZOOM, curve: 1.6, padding: ruimte(), duration: rustig.matches ? 0 : duur, essential: false });
    }
    function rondje() {
      stop();
      var mijn = beurt;
      map.jumpTo(START); opZoom();
      if (rustig.matches) { setTimeout(function () { if (mijn === beurt) naarAdres(0); }, 800); return; }
      var t0 = performance.now(), vorig = t0;
      (function stap(nu) {
        if (mijn !== beurt) return;
        var c = map.getCenter();
        map.setCenter([c.lng + (nu - vorig) * 0.035, c.lat]);
        vorig = nu;
        if (nu - t0 < 1600) { draai = requestAnimationFrame(stap); return; }
        draai = null;
        map.flyTo({ center: [5, 51.5], zoom: 3, duration: 1800, essential: false });
        map.once('moveend', function () { if (mijn === beurt) naarAdres(3200); });
      })(t0);
    }
    ['mousedown', 'touchstart'].forEach(function (ev) { box.addEventListener(ev, stop, { passive: true }); });
    knoppen([
      [ICON.pin, 'Den Haag', function () { stop(); naarAdres(1600); }],
      [ICON.wereld, 'Wereldbeeld', rondje]
    ]);
    map.once('load', function () {
      if (mijn !== poging) return;
      gereed();
      map.resize();
      if (!('IntersectionObserver' in window)) return naarAdres(0);
      zien = new IntersectionObserver(function (items) {
        if (!items[0].isIntersecting) return;
        zien.disconnect();
        rondje();
      }, { threshold: 0.45 });
      zien.observe(box);
    });
    window.addEventListener('resize', vergroot);
  }

  /* ---- platte kaart (Leaflet) ---- */
  function bouwPlat() {
    var L = window.L, box = maakKaart();
    var mijn = poging, tegelsGeladen = 0;
    var map = L.map(box, { scrollWheelZoom: false, zoomControl: false, dragging: !L.Browser.mobile, tap: false });
    opruimen = function () { map.remove(); };
    L.control.zoom({ position: 'topright' }).addTo(map);
    var tegels = L.tileLayer(ESRI + 'World_Street_Map/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19, attribution: ATTR });
    tegels.on('tileload', function () { tegelsGeladen++; });
    tegels.once('load', function () {
      if (mijn !== poging) return;
      if (tegelsGeladen) gereed(); else herstel();
    });
    tegels.addTo(map);
    var icoon = L.divIcon({ className: 'wereld__marker', html: '<span class="wereld__pin">' + ICON.huis + '</span>', iconSize: [40, 40], iconAnchor: [20, 46] });
    L.marker([LAT, LNG], { icon: icoon, keyboard: false }).addTo(map)
      .on('click', function () { var h = routeLink(); if (h) window.open(h, '_blank', 'noopener'); });
    map.setView([LAT, LNG], 15);
    map.attributionControl.setPosition('topright');
    knoppen([[ICON.pin, 'Den Haag', function () { map.flyTo([LAT, LNG], 15, { duration: rustig.matches ? 0 : 0.9 }); }]]);
    setTimeout(function () { if (mijn === poging) { map.invalidateSize(); map.setView([LAT, LNG], 15); } }, 60);
  }
  function startPlat() {
    laadBibliotheek(LEAFLET + 'leaflet.min.css', LEAFLET + 'leaflet.min.js', window.L && window.L.map, bouwPlat, herstel);
  }

  function heeftWebGL() {
    try { return !!(window.WebGL2RenderingContext && document.createElement('canvas').getContext('webgl2')); }
    catch (e) { return false; }
  }
  function start() {
    if (!heeftWebGL()) return startPlat();
    laadBibliotheek(MAPLIBRE + 'maplibre-gl.css', MAPLIBRE + 'maplibre-gl.js', window.maplibregl, bouwBol, startPlat);
  }

  /* De bezoeker opent de interactieve kaart. De lokale kaart en het adres blijven als terugval. */
  var startKnop = paneel.querySelector('[data-wereld-start]');
  var melding = paneel.querySelector('[data-wereld-melding]');
  function gereed() {
    if (geladen) return;
    geladen = true; clearTimeout(wachttijd);
    paneel.classList.add('is-kaart');
    paneel.removeAttribute('aria-busy');
    if (melding) { melding.classList.add('vh'); melding.textContent = 'Interactieve kaart geladen. U kunt inzoomen of de routeplanner openen.'; }
    if (toetsenbord && (document.activeElement === startKnop || document.activeElement === document.body)) {
      var knop = paneel.querySelector('.wereld__knop');
      if (knop) knop.focus();
    }
  }
  function herstel() {
    poging++; clearTimeout(wachttijd); geladen = false;
    if (opruimen) { var schoon = opruimen; opruimen = null; schoon(); }
    paneel.querySelectorAll('.wereld__kaart,.wereld__tools').forEach(function (el) { el.remove(); });
    paneel.classList.remove('is-kaart');
    paneel.removeAttribute('aria-busy');
    if (startKnop) { startKnop.disabled = false; startKnop.textContent = 'Opnieuw proberen'; }
    if (melding) { melding.classList.remove('vh'); melding.textContent = 'De interactieve kaart is nu niet beschikbaar. U kunt wel de routeplanner openen.'; }
    if (toetsenbord && document.activeElement === document.body && startKnop) startKnop.focus();
  }
  function openKaart(metToetsenbord) {
    if (!startKnop || startKnop.disabled) return;
    poging++; geladen = false; toetsenbord = metToetsenbord;
    startKnop.disabled = true;
    paneel.setAttribute('aria-busy', 'true');
    if (melding) { melding.classList.add('vh'); melding.textContent = 'Kaart laden'; }
    wachttijd = setTimeout(herstel, 15000);
    start();
  }
  if (startKnop) startKnop.addEventListener('click', function (e) { openKaart(e.detail === 0); });
  /* ook een klik op de getekende kaart zelf opent de echte kaart */
  var terugval = paneel.querySelector('.wereld__terugval');
  if (terugval && startKnop) terugval.addEventListener('click', function () { openKaart(false); });
})();
