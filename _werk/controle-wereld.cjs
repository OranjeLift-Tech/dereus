/* Browsercontrole van kaartladen, terugval en toetsenbordfocus, met lokale CDN/API-mocks.
   Gebruik: node _werk/controle-wereld.cjs <pad-naar-playwright> [basis-url] */
const { chromium } = require(process.argv[2] || 'playwright');
const assert = require('node:assert/strict');
const base = process.argv[3] || 'http://127.0.0.1:8765';

function bibliotheekMock() {
  const state = window.kaartControle = { maps: [], layers: [], removed: 0 };
  function emitter(target = {}) {
    const events = {};
    target.on = (name, fn) => { (events[name] ||= []).push(fn); return target; };
    target.once = (name, fn) => {
      const once = (...args) => { events[name] = events[name].filter(f => f !== once); fn(...args); };
      return target.on(name, once);
    };
    target.emit = name => [...(events[name] || [])].forEach(fn => fn({ type: name }));
    return target;
  }
  function map(container) {
    const canvas = document.createElement('canvas');
    canvas.className = 'maplibregl-canvas'; canvas.tabIndex = 0; container.append(canvas);
    const instance = emitter({
      touchZoomRotate: { disableRotation() {} }, attributionControl: { setPosition() {} },
      addControl() {}, resize() {}, invalidateSize() {}, setView() {}, flyTo() {}, jumpTo() {},
      getZoom: () => 15, getCenter: () => ({ lng: 4, lat: 52 }),
      remove() { state.removed++; container.remove(); }
    });
    state.maps.push(instance); return instance;
  }
  window.maplibregl = {
    Map: function (options) { return map(options.container); },
    NavigationControl: function () {}, AttributionControl: function () {},
    Marker: function () { this.setLngLat = () => this; this.addTo = () => this; }
  };
  window.L = {
    Browser: { mobile: false }, map, control: { zoom: () => ({ addTo() {} }) },
    tileLayer() { const layer = emitter({ addTo() {} }); state.layers.push(layer); return layer; },
    divIcon: options => options, marker: () => ({ addTo() {} })
  };
}

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  let checks = 0;
  try {
    for (const scenario of ['globe-success', 'globe-error', 'globe-timeout-retry', 'leaflet-success', 'leaflet-error', 'cdn-error']) {
      const page = await browser.newPage({ reducedMotion: 'reduce' });
      const errors = [], requests = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.addInitScript(leaflet => {
        Object.defineProperty(window, 'WebGL2RenderingContext', { configurable: true, value: leaflet ? undefined : function () {} });
        const getContext = HTMLCanvasElement.prototype.getContext;
        HTMLCanvasElement.prototype.getContext = function (kind, ...args) {
          return kind === 'webgl2' ? {} : getContext.call(this, kind, ...args);
        };
      }, scenario.startsWith('leaflet'));
      await page.route(/https:\/\/(cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com)\//, async route => {
        requests.push(route.request().url());
        if (scenario === 'cdn-error') return route.abort();
        const css = route.request().url().endsWith('.css');
        return route.fulfill({ contentType: css ? 'text/css' : 'application/javascript', body: css ? '/* local map test */' : `(${bibliotheekMock.toString()})();` });
      });
      await page.goto(base, { waitUntil: 'networkidle' });
      assert.equal(requests.length, 0, `${scenario}: no CDN requests before consent`);
      if (scenario.includes('timeout')) await page.clock.install();
      const start = page.locator('[data-wereld-start]');
      await start.scrollIntoViewIfNeeded();
      await start.focus(); await page.keyboard.press('Enter');
      if (scenario === 'cdn-error') {
        await page.waitForFunction(() => !document.querySelector('[data-wereld-start]').disabled);
      } else {
        await page.waitForFunction(() => window.kaartControle?.maps.length);
        assert.equal(await page.locator('.wereld__terugval').isVisible(), true, `${scenario}: fallback while loading`);
        assert.equal(await page.locator('.wereld__kaart').isVisible(), false, `${scenario}: pending controls hidden`);
        assert.equal(await start.isEnabled(), false);
        if (scenario.includes('timeout')) {
          await page.clock.fastForward(15001);
          assert.equal(await start.isEnabled(), true, 'timeout permits retry');
          await page.evaluate(() => window.kaartControle.maps[0].emit('load'));
          assert.equal(await page.locator('.wereld.is-kaart').count(), 0, 'stale load cannot replace fallback');
          await start.focus(); await page.keyboard.press('Enter');
          await page.waitForFunction(() => window.kaartControle.maps.length === 2);
          await page.evaluate(() => window.kaartControle.maps[1].emit('load'));
        } else if (scenario === 'globe-error') {
          await page.evaluate(() => window.kaartControle.maps[0].emit('error'));
        } else if (scenario.startsWith('leaflet')) {
          await page.evaluate(success => {
            if (success) window.kaartControle.layers[0].emit('tileload');
            window.kaartControle.layers[0].emit('load');
          }, scenario.endsWith('success'));
        } else await page.evaluate(() => window.kaartControle.maps[0].emit('load'));
      }
      const success = scenario.endsWith('success') || scenario.endsWith('retry');
      if (success) {
        assert.equal(await page.locator('.wereld__terugval').isVisible(), false);
        assert.equal(await page.locator('.wereld__kaart').getAttribute('role'), 'region');
        assert.equal(await page.locator('.wereld__knop').first().evaluate(el => el === document.activeElement), true, `${scenario}: keyboard focus transferred`);
        assert.match(await page.locator('[data-wereld-melding]').textContent(), /kaart geladen/);
        const canvas = page.locator('.maplibregl-canvas');
        await canvas.focus();
        assert.notEqual(await canvas.evaluate(el => getComputedStyle(el).outlineStyle), 'none', 'visible map focus');
      } else {
        assert.equal(await page.locator('.wereld__terugval').isVisible(), true);
        assert.equal(await start.isEnabled(), true);
        assert.equal(await page.locator('.wereld__kaart').count(), 0, `${scenario}: failed map removed`);
        assert.match(await page.locator('[data-wereld-melding]').textContent(), /niet beschikbaar/);
        assert.equal(await start.evaluate(el => el === document.activeElement), true, `${scenario}: retry focus restored`);
      }
      assert.equal(await page.locator('[data-wereld]').getAttribute('aria-busy'), null);
      assert.deepEqual(errors, [], `${scenario}: no browser errors`);
      console.log(`${scenario}: akkoord`); checks++;
      await page.close();
    }
    console.log(`${checks} kaartscenario's gecontroleerd met lokale bibliotheekmocks.`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
