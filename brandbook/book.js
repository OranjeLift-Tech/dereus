/* Gedrag van het merkboek.
   Kleurcodes en contrastwaarden worden bij het laden uit tokens.css gelezen,
   zodat wat het boek toont nooit afwijkt van de tokens. Markeert ook het huidige
   hoofdstuk in de inhoudsopgave en telt de placeholders die nog open staan. */
(function () {
  var root = getComputedStyle(document.documentElement);
  function raw(name) { return root.getPropertyValue(name).trim(); }
  function token(name) { return raw(name).toUpperCase(); }
  function text(name) { return raw(name).replace(/^["']|["']$/g, '').trim(); }
  function rgb(hex) { return [1, 3, 5].map(function (i) { return parseInt(hex.slice(i, i + 2), 16); }); }
  function lin(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
  function lum(hex) { var c = rgb(hex).map(lin); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; }
  function ratio(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  function fmt(r) { return r.toFixed(2).replace('.', ','); }
  var WHITE = '#FFFFFF', INK = token('--ink') || '#0E1A33';
  var isHex = /^#[0-9A-F]{6}$/;

  // Kleurkaarten: <div class="swatch" data-token="--brand-primary"> met <dl class="codes">
  // CMYK en Pantone komen uit --brand-primary-cmyk en --brand-primary-pantone (als die bestaan).
  // Met <body data-web> (de webeditie) toont de kaart alleen HEX en RGB.
  var webOnly = document.body.hasAttribute('data-web');
  document.querySelectorAll('.swatch[data-token]').forEach(function (el) {
    var name = el.dataset.token, hex = token(name);
    if (!isHex.test(hex)) return;
    el.style.setProperty('--c', hex);
    var rows = [['HEX', hex], ['RGB', rgb(hex).join(' ')]];
    (webOnly ? [] : ['cmyk', 'pantone']).forEach(function (kind) {
      var v = raw(name + '-' + kind);
      if (v !== '') rows.push([kind === 'cmyk' ? 'CMYK' : 'Pantone', text(name + '-' + kind)]);
    });
    var dl = el.querySelector('.codes');
    if (dl) {
      dl.innerHTML = rows.map(function (r) {
        return '<dt>' + r[0] + '</dt><dd' + (r[1] ? '' : ' class="tbd"') + '>' + (r[1] || 'n.t.b.') + '</dd>';
      }).join('');
    }
    var chip = el.querySelector('.chip');
    if (chip) {
      // Alleen combinaties die minstens 3 : 1 halen; de rest is onleesbaar en hoort er niet te staan.
      chip.innerHTML = [[WHITE, 'met wit'], [INK, 'met inkt']].filter(function (p) { return ratio(p[0], hex) >= 3; }).map(function (p) {
        return '<span class="cr" style="color:' + p[0] + '">Aa <b>' + fmt(ratio(p[0], hex)) + '</b> ' + p[1] + '</span>';
      }).join('');
    }
  });

  // Contrasttabel: <tr data-fg="--white" data-bg="--brand-primary"> met 6 cellen
  function pill(ok) { return '<span class="cr-pill ' + (ok ? 'pass' : 'fail') + '">' + (ok ? 'Goed' : 'Onvoldoende') + '</span>'; }
  document.querySelectorAll('tr[data-fg]').forEach(function (tr) {
    var fg = token(tr.dataset.fg), bg = token(tr.dataset.bg);
    if (!isHex.test(fg) || !isHex.test(bg)) return;
    var r = ratio(fg, bg), td = tr.querySelectorAll('td');
    td[1].innerHTML = '<span class="sample" style="color:' + fg + ';background:' + bg + '">De Reus</span>';
    td[2].textContent = fmt(r) + ' : 1';
    td[3].innerHTML = pill(r >= 4.5);
    td[4].innerHTML = pill(r >= 3);
  });

  // Werkversie: tel de placeholders per bron. De balk verdwijnt als alles is ingevuld.
  var bar = document.querySelector('.bb-draft');
  if (bar) {
    var open = document.querySelectorAll('.ph, .todo'), bySrc = {};
    open.forEach(function (el) { var s = el.dataset.src || 'onbekend'; bySrc[s] = (bySrc[s] || 0) + 1; });
    if (open.length) {
      bar.textContent = 'Werkversie · ' + open.length + ' placeholders open · ' +
        Object.keys(bySrc).sort().map(function (s) { return s + ': ' + bySrc[s]; }).join(' · ');
      bar.hidden = false;
    }
  }

  // Huidig hoofdstuk in de inhoudsopgave
  var links = Array.prototype.slice.call(document.querySelectorAll('.bb-toc a[href^="#"]'));
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
  if (!('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var a = byId[e.target.id];
      if (!a) return;
      links.forEach(function (l) { l.removeAttribute('aria-current'); });
      a.setAttribute('aria-current', 'true');
      var list = a.closest('ol');
      if (list && list.scrollWidth > list.clientWidth) {
        list.scrollTo({ left: a.parentNode.offsetLeft - list.clientWidth / 2 + a.offsetWidth / 2, behavior: 'smooth' });
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  document.querySelectorAll('.chapter[id]').forEach(function (s) { io.observe(s); });
})();
