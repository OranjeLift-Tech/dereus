/* De hele controleketen in een commando: eigen server, een browser, alle checks, een lijst.

     node _werk/controle.cjs                  alles
     node _werk/controle.cjs layout headers   alleen deze
     node _werk/controle.cjs --snel           twee breedtes in plaats van vijf, voor tussendoor
     node _werk/controle.cjs --serie          achter elkaar in plaats van tegelijk
     node _werk/controle.cjs --basis http://127.0.0.1:8012    tegen een server die al draait
     node _werk/controle.cjs --playwright <pad>               ander Playwright dan het bekende

   Wat dit vervangt: vijf losse commando's, vijf browserstarts, zelf een server opstarten op een
   poort die niet botst, en het Playwright-pad per keer intypen. De checks draaien tegelijk op
   een gedeelde browser en elke regel draagt de naam van de check die hem schreef.

   De afsluitcode is 1 zodra een check een fout meldt. controle-beelden.py telt daar niet in mee:
   die rapporteert (zie de kop van dat bestand) en hangt niet aan de build.

   Het vangnet is de uitzondering daarop: dat is dezelfde python, maar met --vangnet, en die
   telt wel mee. Het is het net onder de opruimronde van de beelden, en de enige vraag die
   het stelt is of elk opgevraagd pad nog op een bestaand bestand uitkomt. Wie beelden
   verplaatst draait dit erna; komt er FOUT uit, dan zet
   python _werk/opruimen-beelden.py --terug alles op zijn plek. */
const { spawn } = require('node:child_process');
const path = require('node:path');
const kit = require('./controle-kit.cjs');

const CHECKS = {
  layout: './controle-layout.cjs',
  headers: './controle-headers.cjs',
  wereld: './controle-wereld.cjs',
  werkwijze: './controle-werkwijze.cjs',
};
/* streng: de afsluitcode van de python telt mee in die van de runner. */
const PYTHON_CHECKS = {
  beelden: { bestand: 'controle-beelden.py', args: [], streng: false },
  vangnet: { bestand: 'controle-beelden.py', args: ['--vangnet'], streng: true },
};

function pythonCheck(naam, opdracht) {
  return new Promise(klaar => {
    const regels = [];
    const proces = spawn('python', [path.join(__dirname, opdracht.bestand), ...opdracht.args], { cwd: kit.WORTEL });
    const lees = brok => regels.push(...String(brok).split(/\r?\n/).filter(Boolean));
    proces.stdout.on('data', lees);
    proces.stderr.on('data', lees);
    proces.on('close', code => {
      // Bij beelden is de laatste regel de telling per soort; het vangnet zegt het in zijn
      // GOED/FOUT-regel. Allebei precies wat er in de samenvatting hoort.
      const uitslag = (opdracht.streng
        ? regels.find(r => /^(GOED|FOUT)/.test(r))
        : regels[regels.length - 1]) || 'geen uitslag';
      console.log(`[${naam}] ${uitslag.trim()}`);
      const fouten = [];
      if (opdracht.streng && code !== 0) {
        // De ingesprongen regels onder FOUT zijn de vindplaatsen; die horen in het rapport.
        const details = regels.filter(r => /^\s+\S/.test(r)).map(r => r.trim());
        for (const regel of details.length ? details : [uitslag.trim()]) fouten.push({ eenheid: naam, bericht: regel });
        // Zonder deze regels staat er straks alleen "2 fouten" en moet je de check opnieuw
        // draaien om te zien welk bestand het was.
        for (const f of fouten) console.log(`  ${f.bericht}`);
      }
      // Wat de check geteld heeft, zodat de samenvatting een getal draagt en geen regelaantal.
      const geteld = (regels.find(r => /^\s*Vangnet: (\d+)/.test(r)) || '').match(/(\d+)/);
      klaar({ naam, eenheden: geteld ? Number(geteld[1]) : regels.length, fouten, rapporteert: fouten.length ? undefined : uitslag.trim() });
    });
    proces.on('error', e => klaar({ naam, eenheden: 0, fouten: [{ eenheid: naam, bericht: `python startte niet: ${e.message}` }] }));
  });
}

(async () => {
  const argv = process.argv.slice(2);
  const gevraagd = argv.filter(a => !a.startsWith('--') && !a.startsWith('http'));
  const onbekend = gevraagd.filter(n => !CHECKS[n] && !PYTHON_CHECKS[n]);
  if (onbekend.length) {
    console.error(`Onbekende check: ${onbekend.join(', ')}. Keuze: ${[...Object.keys(CHECKS), ...Object.keys(PYTHON_CHECKS)].join(', ')}`);
    process.exit(2);
  }
  const draaien = gevraagd.length ? gevraagd : [...Object.keys(CHECKS), ...Object.keys(PYTHON_CHECKS)];
  const snel = argv.includes('--snel');
  const serie = argv.includes('--serie');
  const basis = argv.find(a => a.startsWith('http')) || (argv.includes('--basis') ? argv[argv.indexOf('--basis') + 1] : null);
  const playwright = argv.includes('--playwright') ? argv[argv.indexOf('--playwright') + 1] : null;

  const begin = Date.now();
  const omgeving = await kit.opzet({ basis, playwright });
  console.log(`Controle op ${omgeving.basis}${snel ? ' (snel)' : ''}: ${draaien.join(', ')}\n`);

  const taken = draaien.map(naam => async () => {
    if (PYTHON_CHECKS[naam]) return pythonCheck(naam, PYTHON_CHECKS[naam]);
    try {
      return await require(CHECKS[naam]).draai({ browser: omgeving.browser, basis: omgeving.basis, snel });
    } catch (e) {
      console.log(`[${naam}] afgebroken: ${e.message}`);
      return { naam, eenheden: 0, fouten: [{ eenheid: naam, bericht: `afgebroken: ${e.message}` }] };
    }
  });

  let uitslagen;
  try {
    if (serie) {
      uitslagen = [];
      for (const taak of taken) uitslagen.push(await taak());
    } else {
      uitslagen = await Promise.all(taken.map(taak => taak()));
    }
  } finally {
    await omgeving.op();
  }

  const seconden = ((Date.now() - begin) / 1000).toFixed(0);
  const fouten = uitslagen.reduce((som, u) => som + u.fouten.length, 0);
  console.log(`\nSamenvatting (${seconden}s)`);
  for (const u of uitslagen) {
    const staat = u.rapporteert ? u.rapporteert
      : u.fouten.length ? `${u.fouten.length} fout${u.fouten.length === 1 ? '' : 'en'} in ${u.eenheden} eenheden`
        : `akkoord (${u.eenheden} eenheden)`;
    console.log(`  ${u.naam.padEnd(10)} ${staat}`);
  }
  process.exitCode = fouten ? 1 : 0;
})().catch(error => { console.error(error); process.exitCode = 1; });
