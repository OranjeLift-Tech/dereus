/* Werkwijze-trap: een echte asfaltweg slingert van links naar het nieuwe huis,
   om en om boven en onder de treden door. De weg wordt uitgerekend uit de plek van de kaarten,
   dus hij klopt bij elke schermbreedte. Onder 1100 px (treden onder elkaar) is er geen weg. */
(function () {
  'use strict';
  var trap = document.querySelector('.trap');
  if (!trap || !document.createElementNS) return;
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'trap__weg');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('focusable', 'false');
  svg.innerHTML =
    '<defs>' +
      // echte asfaltfoto als tegel
      '<pattern id="trap-asfalt" patternUnits="userSpaceOnUse" width="96" height="96"><image href="img/asfalt.webp" width="96" height="96"/></pattern>' +
      '<filter id="trap-wegschaduw" x="-10%" y="-20%" width="120%" height="140%"><feGaussianBlur stdDeviation="10"/></filter>' +
      // rafelige rand: asfalt houdt nooit in een strakke lijn op
      '<filter id="trap-rafel" x="-10%" y="-20%" width="120%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="5" xChannelSelector="R" yChannelSelector="G"/></filter>' +
      // vlekken en reparatievakken: grote, zachte donkere en lichte plekken over het wegdek
      '<filter id="trap-vlekken" x="-10%" y="-20%" width="120%" height="140%">' +
        '<feTurbulence type="fractalNoise" baseFrequency=".008 .02" numOctaves="3" seed="11" result="n"/>' +
        '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  .55 0 0 0 -.2" result="donker"/>' +
        '<feComposite in="donker" in2="SourceGraphic" operator="in" result="d2"/>' +
        '<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 -.7 0 0 .38" result="licht"/>' +
        '<feComposite in="licht" in2="SourceGraphic" operator="in" result="l2"/>' +
        '<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="d2"/><feMergeNode in="l2"/></feMerge>' +
      '</filter>' +
      // versleten belijning: verf met gaatjes en vage randen
      '<filter id="trap-sleet" x="-10%" y="-20%" width="120%" height="140%">' +
        '<feTurbulence type="fractalNoise" baseFrequency=".45" numOctaves="2" seed="5" result="n"/>' +
        '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  3.2 0 0 0 -1.05" result="gaten"/>' +
        '<feComposite in="SourceGraphic" in2="gaten" operator="in"/><feGaussianBlur stdDeviation=".35"/>' +
      '</filter>' +
      '<filter id="trap-zacht" x="-10%" y="-20%" width="120%" height="140%"><feGaussianBlur stdDeviation="3.2"/></filter>' +
    '</defs>' +
    '<path class="weg weg--schaduw" filter="url(#trap-wegschaduw)"/>' +
    '<g filter="url(#trap-rafel)"><path class="weg weg--berm"/><path class="weg weg--asfalt" stroke="url(#trap-asfalt)"/></g>' +
    '<g filter="url(#trap-sleet)"><path class="weg weg--kant"/></g>' +                                  // kantstrepen ...
    '<g filter="url(#trap-vlekken)"><path class="weg weg--kantvul" stroke="url(#trap-asfalt)"/></g>' +   // ... met het wegdek ertussen
    '<g filter="url(#trap-zacht)"><path class="weg weg--spoor"/><path class="weg weg--midden"/></g>' +
    '<g filter="url(#trap-sleet)"><path class="weg weg--streep"/></g>';
  trap.appendChild(svg);   // achteraan, zodat :nth-child van de treden blijft kloppen; z-index legt hem erachter
  trap.classList.add('trap--weg');
  var paden = svg.querySelectorAll('.weg');

  // vloeiende lijn door de punten (Catmull-Rom naar bezier)
  function lijn(p) {
    var d = 'M' + p[0][0].toFixed(1) + ' ' + p[0][1].toFixed(1);
    for (var i = 0; i < p.length - 1; i++) {
      var a = p[i - 1] || p[i], b = p[i], c = p[i + 1], e = p[i + 2] || c, t = 0.19;
      d += ' C' + (b[0] + (c[0] - a[0]) * t).toFixed(1) + ' ' + (b[1] + (c[1] - a[1]) * t).toFixed(1) + ' ' +
        (c[0] - (e[0] - b[0]) * t).toFixed(1) + ' ' + (c[1] - (e[1] - b[1]) * t).toFixed(1) + ' ' + c[0].toFixed(1) + ' ' + c[1].toFixed(1);
    }
    return d;
  }

  function teken() {
    var kaarten = trap.querySelectorAll('.trap__trede');
    if (window.innerWidth <= 1100 || kaarten.length < 5) { svg.style.display = 'none'; return; }
    svg.style.display = '';
    // maten uit de layout (offset*), niet uit het beeld: zo telt de opkomst-animatie van de treden niet mee
    var o = { left: trap.getBoundingClientRect().left, width: trap.offsetWidth, height: trap.offsetHeight };
    var r = [].map.call(kaarten, function (k) {
      return { x: k.offsetLeft + k.offsetWidth / 2, boven: k.offsetTop, onder: k.offsetTop + k.offsetHeight };
    });
    // voordeur: midden onder de foto, meegerekend met de schaal en lift van het huis
    var huis = trap.querySelector('.trap__huis'), vorm = trap.querySelector('.trap__huisvorm');
    var cs = getComputedStyle(huis), oor = cs.transformOrigin.split(' ').map(parseFloat);
    var m = cs.transform && cs.transform !== 'none' && window.DOMMatrix ? new DOMMatrix(cs.transform) : null;
    var px = huis.offsetWidth / 2 - oor[0], py = vorm.offsetHeight - oor[1];
    var deur = m ? [huis.offsetLeft + oor[0] + m.a * px + m.c * py + m.e, huis.offsetTop + oor[1] + m.b * px + m.d * py + m.f]
                 : [huis.offsetLeft + huis.offsetWidth / 2, huis.offsetTop + vorm.offsetHeight];
    var punten = [
      [-o.left - 80, r[0].boven + 120],          // komt links het beeld in
      [r[0].x, r[0].boven - 58],                 // boven trede 1
      [r[1].x, r[1].onder + 40],                 // onder trede 2
      [r[2].x, r[2].boven - 58],                 // boven trede 3
      [r[3].x, r[3].onder + 52],                 // onder trede 4
      [r[4].x + 30, r[4].onder + 56],            // onder trede 5
      [deur[0] - 8, deur[1] + 70],               // draait omhoog naar de voordeur
      [deur[0], deur[1] - 6]                     // eindigt op de stoep, achter het huis langs
    ];
    svg.setAttribute('viewBox', '0 0 ' + o.width + ' ' + o.height);
    svg.setAttribute('width', o.width);
    svg.setAttribute('height', o.height);
    var d = lijn(punten);
    [].forEach.call(paden, function (p) { p.setAttribute('d', d); });
  }

  var wacht;
  window.addEventListener('resize', function () { clearTimeout(wacht); wacht = setTimeout(teken, 120); });
  window.addEventListener('load', teken);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(teken);
  teken();
})();
