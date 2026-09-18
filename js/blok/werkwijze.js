/* De weg volgt de fototreden. De inhoud en trap blijven zonder JavaScript zichtbaar. */
(function () {
  'use strict';
  var traps = document.querySelectorAll('.verhuistrap');
  if (!traps.length || !document.createElementNS) return;
  var ns = 'http://www.w3.org/2000/svg';

  [].forEach.call(traps, function (trap, index) {
    var svg = document.createElementNS(ns, 'svg');
    var patternId = 'verhuistrap-asfalt-' + index;
    svg.setAttribute('class', 'verhuistrap__weg');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    svg.innerHTML = '<defs><pattern id="' + patternId + '" patternUnits="userSpaceOnUse" width="96" height="96"><image href="/img/asfalt.webp" width="96" height="96"/></pattern></defs>' +
      '<path class="verhuistrap__wegrand"/>' +
      '<path class="verhuistrap__asfalt" stroke="url(#' + patternId + ')"/>' +
      '<path class="verhuistrap__wegstreep"/>';
    trap.appendChild(svg);

    function draw() {
      if (window.innerWidth <= 1100) return;
      var steps = trap.querySelectorAll('.verhuistrap__trede');
      var house = trap.querySelector('.verhuistrap__huisvorm');
      if (steps.length !== 5 || !house) return;
      var rect = trap.getBoundingClientRect();
      var cards = [].map.call(steps, function (step) {
        var r = step.getBoundingClientRect();
        return { x: r.left - rect.left + r.width / 2, top: r.top - rect.top, bottom: r.bottom - rect.top };
      });
      var door = house.getBoundingClientRect();
      var doorX = door.left - rect.left + door.width / 2;
      var doorY = door.bottom - rect.top;
      var points = [
        [-rect.left - 30, cards[0].top + 70],
        [cards[0].x, cards[0].top - 34],
        [cards[1].x, cards[1].bottom + 30],
        [cards[2].x, cards[2].top - 34],
        [cards[3].x, cards[3].bottom + 35],
        [cards[4].x, cards[4].bottom + 36],
        [doorX - 10, doorY + 42],
        [doorX, doorY - 8]
      ];
      var d = 'M' + points[0].join(' ');
      for (var i = 0; i < points.length - 1; i++) {
        var a = points[i - 1] || points[i], b = points[i], c = points[i + 1], e = points[i + 2] || c;
        d += ' C' + (b[0] + (c[0] - a[0]) * .19) + ' ' + (b[1] + (c[1] - a[1]) * .19) +
          ' ' + (c[0] - (e[0] - b[0]) * .19) + ' ' + (c[1] - (e[1] - b[1]) * .19) + ' ' + c.join(' ');
      }
      svg.setAttribute('viewBox', '0 0 ' + rect.width + ' ' + rect.height);
      [].forEach.call(svg.querySelectorAll('path'), function (path) { path.setAttribute('d', d); });
    }

    var frame;
    function schedule() {
      window.cancelAnimationFrame(frame);
      frame = window.requestAnimationFrame(draw);
    }
    window.addEventListener('resize', schedule, { passive: true });
    if ('ResizeObserver' in window) new ResizeObserver(schedule).observe(trap);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(schedule);
    schedule();
  });
})();
