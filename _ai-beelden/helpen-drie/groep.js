// Drie verhuizers voor "Zo helpen wij u snel": de adviseur (met het echte borstmerk) vooraan in het midden,
// de man met de dozen en de blonde man met de deken uit img/team/team-hero-1600.webp er iets achter.
// Eenheden = pixels van de adviseur (640x954, lichaam gecentreerd op x 320, kruin y 0, voeten y 953).
const adv = await laad('/_tmp/adviseur-merk.png');
const team = await laad('/img/team/team-hero-1600.webp');
const TW = team.width, TH = team.height;

// losknippen: per rij de grens tegen de middelste man (gemeten 28-09-2026)
const [tc, tx] = doek(TW, TH); tx.drawImage(team, 0, 0);
const src = tx.getImageData(0, 0, TW, TH);
const knip = (inRij) => {
  const [c, x] = doek(TW, TH); const out = x.createImageData(TW, TH);
  for (let y = 0; y < TH; y++) for (let xx = 0; xx < TW; xx++) if (inRij(xx, y)) {
    const i = (y * TW + xx) * 4; for (let k = 0; k < 4; k++) out.data[i+k] = src.data[i+k];
  }
  x.putImageData(out, 0, 0); return c;
};
// man met de dozen: boven de dozen tot 565, dan de rechterrand van de bovenste en onderste doos, eronder tot 610
const doosRand = y => y < 655 ? 596 + (y - 400) * 14 / 255 : 648 + (y - 655) * 12 / 270;
const zwart = knip((xx, y) => y < 398 ? xx < 565 : y < 925 ? xx <= doosRand(y) + 1 : xx < 610);
// blonde man: hij staat voor de middelste man; de grens ligt achter de adviseur, dus hoeft niet op de pixel
const blond = knip((xx, y) => y < 400 ? xx >= 1075 : y < 560 ? xx >= 1062 : y < 900 ? xx >= 1028 : xx >= 1015);

// plaatsing
const S = 0.5225;                 // team-hero naar adviseur, x 0,95: zij staan iets verder naar achteren
const VOET = 928;                 // hun voetlijn iets hoger dan die van de adviseur (953)
const HC = Math.round(954 * 0.62); // alleen kruin tot onder de heup: de rest ligt achter het blauwe paneel
const X0 = 333, WC = 685;
const [g, gx] = doek(WC, HC);
const zet = (laag, hoofdX, doelX) => {
  // hoofdX = x van het hoofdmidden in team-hero, doelX = waar dat moet komen
  const l = doelX - hoofdX * S, t = VOET - TH * S;
  return [laag, l, t, TW * S, TH * S];
};
const achter = [zet(zwart, 240, X0 - 198), zet(blond, 1250, X0 + 164)];
const [ac, ax] = doek(WC, HC);
ax.filter = 'brightness(0.94) saturate(0.9)';   // hun polo's zijn feller dan die van de adviseur (2,87,181 tegen 21,79,160)
for (const [laag, l, t, w, h] of achter) ax.drawImage(laag, l, t, w, h);
ax.filter = 'none';
// slagschaduw van de adviseur op de twee achter hem
const [sc, sx] = doek(WC, HC);
sx.filter = 'blur(14px)'; sx.drawImage(adv, X0 - 320 + 10, 8);
sx.filter = 'none'; sx.globalCompositeOperation = 'source-in'; sx.fillStyle = 'rgba(8,24,60,.42)'; sx.fillRect(0, 0, WC, HC);
ax.globalCompositeOperation = 'source-atop'; ax.drawImage(sc, 0, 0); ax.globalCompositeOperation = 'source-over';
gx.drawImage(ac, 0, 0);
gx.drawImage(adv, X0 - 320, 0);
bewaar('groep.png', g);
bewaar('groep.webp', g, 'image/webp', 0.9);

// voorbeeld op een paneel, zoals op de site: wit met de blauwe schuine rand over de heup
const [pc, px] = doek(WC + 40, HC + 60);
px.fillStyle = '#fff'; px.fillRect(0, 0, pc.width, pc.height);
px.drawImage(g, 20, 20);
const heup = 20 + Math.round(954 / 2.05);
px.fillStyle = '#1746A2'; px.beginPath(); px.moveTo(0, heup); px.lineTo(pc.width * .58, heup); px.lineTo(pc.width, heup - 60); px.lineTo(pc.width, pc.height); px.lineTo(0, pc.height); px.fill();
bewaar('groep-voorbeeld.png', pc);
return { WC, HC, hoogteFactor: +(2.05 * HC / 954).toFixed(4) };
