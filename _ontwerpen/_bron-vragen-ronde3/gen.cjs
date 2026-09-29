/* /contact/ #vragen, ronde 3 (29-09-2026). node gen.cjs -> ../vragen-contact-ronde3.html
   De gebruiker vond het blauwe paneel te druk en de sobere versie van referentie C (nu live, stijl="gesprek") te sober.
   Elk ontwerp hier gebruikt dezelfde markup als het live blok (vragen__in, __zij, __gesprek, __beller) plus een
   podium met een uitsnede, zodat de keuze een optie in vragen.py wordt en geen nieuw blok. Teksten komen letterlijk
   uit contact/index.html. Mensen: contact-uit (collega met headset, nergens op /contact/) en helpen-drie-uit
   (drie verhuizers, niet live op /contact/). Figuur links: de adviseur in de boog van #na-bericht staat rechts. */
const fs = require('fs');
const path = require('path');
const REPO = path.resolve(__dirname, '../..');
const PAG = fs.readFileSync(path.join(REPO, 'contact/index.html'), 'utf8');
const hash = n => PAG.match(new RegExp(`/css/min/${n}\\.min\\.css\\?v=([0-9a-f]+)`))[1];
const jsHash = PAG.match(/\/js\/site\.js\?v=([0-9a-f]+)/)[1];
const sprite = PAG.match(/<svg class="sprite"[\s\S]*?<\/svg>/)[0];
const SEC = PAG.match(/<section class="sectie[^"]*b-vragen--gesprek[\s\S]*?<\/section>/)[0];
const KOP = SEC.match(/<div class="kopgroep">[\s\S]*?<\/h2><\/div>/)[0];
const CHIP = SEC.match(/<span class="bereikbaar vragen__nu"[\s\S]*?<span class="bereikbaar__tekst"><\/span><\/span>/)[0];
const BELLER = SEC.match(/<p class="vragen__beller">[\s\S]*?<\/span><\/p>/)[0];
const VRAGEN = SEC.match(/<div class="vragen__gesprek" data-reveal>([\s\S]*?<\/details>)\s*<\/div>/)[1];

function maat(src) {
  const b = fs.readFileSync(path.join(REPO, src));
  const soort = b.toString('ascii', 12, 16);
  if (soort === 'VP8X') return [1 + b.readUIntLE(24, 3), 1 + b.readUIntLE(27, 3)];
  if (soort === 'VP8L') { const n = b.readUInt32LE(21); return [(n & 0x3fff) + 1, ((n >> 14) & 0x3fff) + 1]; }
  return [b.readUInt16LE(26) & 0x3fff, b.readUInt16LE(28) & 0x3fff];
}
const foto = src => { const [w, h] = maat(src); return `<img class="vragen__collega" src="${src}" alt="" width="${w}" height="${h}" loading="lazy" decoding="async">`; };
const COLLEGA = '/img/contact-uit.webp';
const TEAM = '/img/helpen-drie-uit.webp';

const sectie = (n, figuur) => {
  const id = `v${n}`;
  const kop = KOP.replace('id="vragen-kop"', `id="${id}-kop"`);
  const vragen = VRAGEN.replace(/id="vragen-(\d)"/g, `id="${id}-$1"`).replace(/name="vragen"/g, `name="${id}"`);
  const podium = `<div class="vragen__podium"><span class="vragen__staan" aria-hidden="true">${foto(figuur)}</span>${CHIP}</div>`;
  return `<section class="sectie sectie--wit b-vragen b-vragen--gesprek v z${n}" id="${id}" aria-labelledby="${id}-kop">
  <div class="wrap vragen__in">
    <div class="vragen__zij">
      ${kop}
      ${BELLER}
      ${podium}
    </div>
    <div class="vragen__gesprek" data-reveal>
      ${vragen}
    </div>
  </div>
</section>`;
};

const V = [
  ['01', 'Collega aan de lijn', 'Referentie C · .b-vragen__podium + .b-vragen__staan (het volledige blok)', COLLEGA,
   'Het blok zoals het bij referentie C echt staat: onder de belregel een schuin Koningsblauw paneel waar een collega met headset uit omhoog komt, "Nu bereikbaar" als gele pil op het paneel. De vragenkaarten en het gestippelde vel krijgen dikte (plaatrand), zoals de kaarten elders op /contact/. Kop en collega links, vragen rechts.'],
  ['02', 'Blauwe plaat met het team', 'Referentie C · .b-vragen__gesprek op donkere grond + podium', TEAM,
   'Het vel onder de vragen wordt een dikke Koningsblauwe plaat met witte stippen en een Diepblauwe zijkant; de witte kaarten liggen erop. Links drie verhuizers op een Goudgeel schuin paneel.'],
  ['03', 'Blauwe kaart met collega (ronde 2, ontwerp 10)', 'Referentie B · .sgdp-voorraad', COLLEGA,
   'Het ontwerp waarvan u op 28-09 zei "bu güzel aslında": een Koningsblauwe kaart met dikte, de vragen als regels erin, de collega steekt boven de kaart uit met "Nu bereikbaar" als gele pil. Nu gespiegeld: de collega links, omdat de adviseur in de boog erboven rechts staat.'],
  ['04', 'Blauwe kaart, vragen als witte kaarten', 'Referentie B · .sgdp-voorraad + referentie C · .b-vraag', COLLEGA,
   'Ontwerp 03 met de vragen als witte kaarten met een Diepblauwe plaatrand, het antwoord naast het beeldmerk, en de belregel met het beeldmerk in een schijf en het nummer met een gele streep.'],
  ['05', 'Gele kaart met het team', 'Referentie B · .sgdp-voorraad + referentie C · .b-vraag', TEAM,
   'Zelfde opzet als 04 op een Goudgele kaart met donkergele zijkant; de drie verhuizers staan erop en steken erboven uit. Kop en nummer in Diepblauw.'],
];

const css = fs.readFileSync(path.join(__dirname, 'var.css'), 'utf8');
const navl = ['00', ...V.map(v => v[0])].map(n => `<a href="#k${n}">${n}</a>`).join('');
const kap = (n, naam, bron, uitleg) => `<div class="vkap" id="k${n}"><div class="wrap"><span class="vkap__nr">${n}</span><div><b>${naam}</b><small>${bron}</small><p>${uitleg}</p></div><span class="vkap__maat" data-maat></span></div></div>`;
const ctx = `<div class="vctx" aria-hidden="true"><div class="wrap">Hierboven op /contact/: Diepblauwe band "Wat er gebeurt na uw bericht", adviseur in de witte boog rechts</div></div>`;
const live = SEC.replace('id="vragen"', 'id="v00"').replace('aria-labelledby="vragen-kop"', 'aria-labelledby="v00-kop"')
  .replace('id="vragen-kop"', 'id="v00-kop"').replace(/id="vragen-(\d)"/g, 'id="v00-$1"').replace(/name="vragen"/g, 'name="v00"');

const html = `<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.className+=' js'</script>
<title>Vragen over contact · ronde 3</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="/css/min/site.min.css?v=${hash('site')}">
<link rel="stylesheet" href="/css/min/vragen.min.css?v=${hash('vragen')}">
<style>
${css}
</style>
<script src="/js/site.js?v=${jsHash}" defer></script>
</head>
<body class="p-contact">
${sprite}
<nav class="vnav" aria-label="Ontwerpen"><div class="wrap"><b>/contact/ #vragen · ronde 3 · 5 ontwerpen</b><div class="vnav__links">${navl}</div></div></nav>
${kap('00', 'Nu live (te sober)', 'Referentie C · .b-vragen', 'Het blok dat nu op /contact/ staat, ter vergelijking.')}
${ctx}
${live}
${V.map(([n, naam, bron, fig, uitleg]) => kap(n, naam, bron, uitleg) + '\n' + ctx + '\n' + sectie(n, fig)).join('\n')}
<div class="vkap vkap--eind"><div class="wrap"><p>Alle teksten zijn letterlijk die van /contact/. Mensen en kleur zijn per ontwerp te wisselen (bijvoorbeeld 04 met het team, of 02 met de collega). Kies een nummer.</p></div></div>
<script>
(function(){
function meet(){document.querySelectorAll('[data-maat]').forEach(function(m){var s=m.closest('.vkap').nextElementSibling;while(s&&s.tagName!=='SECTION')s=s.nextElementSibling;if(!s)return;var h=Math.round(s.getBoundingClientRect().height);m.textContent='Blokhoogte '+h+' px';m.classList.toggle('is-hoog',h>730);});}
addEventListener('load',meet);addEventListener('resize',meet);document.addEventListener('toggle',meet,true);
})();
</script>
</body>
</html>
`;
fs.writeFileSync(path.join(REPO, '_ontwerpen/vragen-contact-ronde3.html'), html);
console.log('ok', html.length);
