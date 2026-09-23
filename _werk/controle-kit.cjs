/* Gereedschap voor de controlescripts: zachte asserts, een eigen server, een gedeelde browser.

   Zacht asserten is waar het om gaat. Met node:assert stopt een sweep bij de eerste fout, dus
   een run levert precies een foutregel op: herstellen, alles opnieuw, volgende foutregel. Bij
   controle-layout kwam de sweep op 22-09-2026 niet verder dan breedte 1100, waardoor 768, 390
   en 320 die run ongezien bleven. De wikkel hieronder vangt de AssertionError, schrijft hem op
   met de eenheid waarin hij viel, en laat de sweep doorlopen. Een run geeft dan de hele lijst.
   De afsluitcode blijft 1 zodra er iets rood is, dus als poort blijft de controle even streng.

   Wat niet zacht is: een echte fout (een selector die er niet is, een timeout, een TypeError).
   Die stopt de eenheid waarin hij valt. Vandaar omhul(): die zet er een hek omheen, zodat de
   volgende route of breedte gewoon aan de beurt komt.

   Gebruik in een controlescript:

     const kit = require('./controle-kit.cjs');
     const { assert, eenheid, omhul, meld, rapport } = kit.zacht('layout');
*/
const echt = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');

const WORTEL = path.resolve(__dirname, '..');

// De repo heeft geen package.json en geen node_modules; zie de notitie verification-toolchain.
const PLAYWRIGHT_BEKEND = 'C:/users/arnas/git_repos/tandartsvanschiedam/node_modules/playwright';

/* Zo lang mag een enkele locator- of navigatiestap duren. Playwright staat standaard op 30s en
   dat is hier alleen maar wachten: een selector die niet bestaat is meteen fout, niet traag. */
const GEDULD = 8000;
const GEDULD_NAVIGATIE = 20000;

/* Waar het eigen bericht staat: assert.ok(waarde, bericht), assert.equal(a, b, bericht). */
const BERICHT_OP = { ok: 1, fail: 1, equal: 2, notEqual: 2, deepEqual: 2, notDeepEqual: 2, strictEqual: 2, match: 2, doesNotMatch: 2 };
const METHODEN = Object.keys(BERICHT_OP);

function toon(waarde) {
  if (typeof waarde === 'string') return waarde.length > 120 ? `${waarde.slice(0, 117)}...` : waarde;
  let tekst;
  try {
    tekst = JSON.stringify(waarde);
  } catch {
    tekst = String(waarde);
  }
  if (tekst === undefined) tekst = String(waarde);
  return tekst.length > 160 ? `${tekst.slice(0, 157)}...` : tekst;
}

/* Uit welke regel van welk controlescript de fout komt. Zonder dat staat er in het rapport
   een uitslag zonder vindplaats, en juist die regel is waar je gaat kijken. */
function plek(fout) {
  const regel = String(fout.stack || '').split('\n')
    .find(r => /controle-[a-z-]+\.cjs:\d+/.test(r) && !r.includes('controle-kit.cjs'));
  const gevonden = regel && regel.match(/(controle-[a-z-]+\.cjs:\d+)/);
  return gevonden ? ` [${gevonden[1]}]` : '';
}

function zacht(naam) {
  const fouten = [];
  let huidige = naam;
  let eenheden = 0;

  /* Veel asserts in deze scripts hebben geen eigen bericht; dan zegt node alleen "Expected
     values to be strictly equal". Daarom altijd de gemeten waarde erbij, en de vindplaats. */
  const bericht = (methode, fout, args) => {
    const eigen = args[BERICHT_OP[methode]];
    const tekst = typeof eigen === 'string' && eigen ? eigen : null;
    const waarden = methode === 'ok' || methode === 'fail'
      ? (tekst ? '' : 'waarde was niet waar')
      : `kreeg ${toon(fout.actual)}${tekst ? '' : `, verwacht ${toon(fout.expected)}`}`;
    return [tekst, waarden].filter(Boolean).join(', ') + plek(fout);
  };

  /* Een assert die zijn eenheid vasthoudt in plaats van hem op te zoeken. Nodig zodra er
     routes naast elkaar lopen: met een gedeelde "huidige eenheid" krijgt een fout dan het
     etiket van de route die toevallig net begon. */
  const gebonden = label => {
    const set = {};
    for (const methode of METHODEN) {
      set[methode] = (...args) => {
        try {
          echt[methode](...args);
        } catch (fout) {
          if (!(fout instanceof echt.AssertionError)) throw fout;
          fouten.push({ eenheid: label ?? huidige, bericht: bericht(methode, fout, args) });
        }
      };
    }
    return set;
  };

  const assert = gebonden(null);   // volgt de lopende eenheid

  /* De eenheid is wat er in de foutregel voor staat: "1100 /contact/", "globe-error", "390px
     motion=reduce". Alles wat daarna misgaat hangt eraan, tot de volgende eenheid. */
  const eenheid = label => { huidige = label ? `${naam} ${label}` : naam; eenheden++; };
  const fout = tekst => fouten.push({ eenheid: huidige, bericht: tekst });
  const meld = regel => console.log(`[${naam}] ${regel}`);

  /* Een hek om een route, een breedte of een scenario: valt er iets hards om, dan is die eenheid
     afgebroken en gaat de sweep door met de volgende. */
  const omhul = async (label, werk) => {
    eenheid(label);
    const eigen = huidige;
    try {
      await werk(gebonden(eigen));
      return true;
    } catch (e) {
      fouten.push({ eenheid: eigen, bericht: `afgebroken: ${String(e.message || e).split('\n')[0]}` });
      return false;
    }
  };

  const rapport = () => {
    if (!fouten.length) {
      console.log(`[${naam}] akkoord (${eenheden} eenheden)`);
    } else {
      console.log(`[${naam}] ${fouten.length} ${fouten.length === 1 ? 'fout' : 'fouten'} in ${eenheden} eenheden:`);
      for (const f of fouten) console.log(`  ${f.eenheid}  ${f.bericht}`);
    }
    return { naam, eenheden, fouten };
  };

  return { assert, eenheid, fout, meld, omhul, rapport, fouten };
}

/* Playwright: uit het argument, anders uit de omgeving, anders het bekende pad op deze machine,
   anders naast dit project. Scheelt het pad per commando meegeven. */
function pak(pad) {
  const kandidaten = [pad, process.env.CONTROLE_PLAYWRIGHT, PLAYWRIGHT_BEKEND, 'playwright'].filter(Boolean);
  const misgelopen = [];
  for (const kandidaat of kandidaten) {
    try {
      return require(kandidaat);
    } catch (e) {
      misgelopen.push(`${kandidaat}: ${e.code || e.message}`);
    }
  }
  throw new Error(`Playwright niet gevonden. Geprobeerd:\n  ${misgelopen.join('\n  ')}\n` +
    'Geef het pad mee als eerste argument of zet CONTROLE_PLAYWRIGHT.');
}

async function browser(pad) {
  return pak(pad).chromium.launch({ channel: 'msedge', headless: true });
}

/* Elke pagina krijgt hetzelfde korte geduld, zodat een verdwenen selector meteen opvalt in
   plaats van dertig seconden te kosten. */
function temmen(pagina) {
  pagina.setDefaultTimeout(GEDULD);
  pagina.setDefaultNavigationTimeout(GEDULD_NAVIGATIE);
  return pagina;
}

/* Een handvol dingen tegelijk, met een vaste ploeg werkers. De 27 headers achter elkaar
   afgaan duurt vijf keer zo lang als nodig; met drie tabbladen is het wachten op het netwerk
   van de een de rekentijd van de ander. De werker krijgt zijn eigen nummer, zodat de aanroeper
   per werker een pagina kan openen in plaats van per taak. */
async function parallel(taken, ploeg, werk) {
  const rij = [...taken];
  let volgende = 0;
  await Promise.all(Array.from({ length: Math.max(1, Math.min(ploeg, rij.length)) }, (_, werker) => (async () => {
    while (volgende < rij.length) {
      const index = volgende++;
      await werk(rij[index], werker, index);
    }
  })()));
}

const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.webmanifest': 'application/manifest+json',
  '.svg': 'image/svg+xml', '.webp': 'image/webp', '.avif': 'image/avif', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.ico': 'image/x-icon', '.gif': 'image/gif',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8', '.pdf': 'application/pdf',
};

/* Eigen server op een vrije poort. Dat scheelt per run het handmatige python -m http.server,
   en een vrije poort kan niet botsen met de server van een andere sessie. Zelfde gedrag als
   build.py --serve: een map wordt zijn index.html, een misser wordt 404.html met status 404. */
function server(wortel = WORTEL) {
  return new Promise((klaar, mis) => {
    const app = http.createServer((verzoek, antwoord) => {
      let pad;
      try {
        pad = decodeURIComponent(new URL(verzoek.url, 'http://127.0.0.1').pathname);
      } catch {
        pad = '/';
      }
      let bestand = path.join(wortel, pad);
      if (!path.resolve(bestand).startsWith(wortel)) bestand = path.join(wortel, '404.html');
      if (fs.existsSync(bestand) && fs.statSync(bestand).isDirectory()) bestand = path.join(bestand, 'index.html');
      const gevonden = fs.existsSync(bestand) && fs.statSync(bestand).isFile();
      const uit = gevonden ? bestand : path.join(wortel, '404.html');
      if (!fs.existsSync(uit)) {
        antwoord.writeHead(404, { 'Content-Type': 'text/plain' });
        antwoord.end('404');
        return;
      }
      const inhoud = fs.readFileSync(uit);
      antwoord.writeHead(gevonden ? 200 : 404, {
        'Content-Type': MIME[path.extname(uit).toLowerCase()] || 'application/octet-stream',
        'Content-Length': inhoud.length,
        'Cache-Control': 'no-store',
      });
      antwoord.end(verzoek.method === 'HEAD' ? undefined : inhoud);
    });
    app.on('error', mis);
    app.listen(0, '127.0.0.1', () => klaar({
      url: `http://127.0.0.1:${app.address().port}`,
      sluit: () => new Promise(gedaan => { app.closeAllConnections?.(); app.close(gedaan); }),
    }));
  });
}

/* Wat een controlescript nodig heeft om zowel los als onder de runner te draaien: een basis-url
   (eigen server als er geen meegegeven is) en een browser (de gedeelde als die er is). */
async function opzet({ basis, browser: gedeeld, playwright } = {}) {
  const eigenServer = basis ? null : await server();
  const eigenBrowser = gedeeld ? null : await browser(playwright);
  return {
    basis: basis || eigenServer.url,
    browser: gedeeld || eigenBrowser,
    async op() {
      if (eigenBrowser) await eigenBrowser.close();
      if (eigenServer) await eigenServer.sluit();
    },
  };
}

/* Los draaien: node _werk/controle-<naam>.cjs [pad-naar-playwright] [basis-url]. Beide mogen weg. */
function argumenten(argv = process.argv.slice(2)) {
  const los = argv.filter(a => !a.startsWith('--'));
  return {
    playwright: los.find(a => !a.startsWith('http')) || null,
    basis: los.find(a => a.startsWith('http')) || null,
    snel: argv.includes('--snel'),
  };
}

module.exports = { zacht, pak, browser, server, opzet, temmen, parallel, argumenten, WORTEL, GEDULD };
