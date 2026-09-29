// Na uw bericht (/contact/): de klantenservice aan haar bureau, zonder kamer, voor de lichte boog (optie beeld="boog").
// Uitvoer: img/contact-klantenservice-boog-uit.webp (850 x 730, alfa).
// Zelfde opbouw als ../na-bericht-bureau/bureau.js: de vrouw uit img/contact-klantenservice-uit.webp, en uit
// img/contact-klantenservice-foto.webp (zelfde 1200x800-raster) het bureau met schrijfblok en kop. Het scherm,
// het toetsenbord en de telefoon vallen weg: het beeld houdt rechts van de kop op, zodat alles in de boog past.
const foto = await laad('/img/contact-klantenservice-foto.webp');
const uit = await laad('/img/contact-klantenservice-uit.webp');
const W = 1200, H = 800;
// y 522 = achterrand van het bureau (onder de vensterbank); x 945 = net rechts van de kop, voor het toetsenbord
const R = 945;
const P = [[382,640],[505,522],[R,522],[R,800],[382,800]];
const [m, mx] = doek(W, H);
mx.fillStyle = '#000'; mx.beginPath(); P.forEach(([x,y],i)=> i?mx.lineTo(x,y):mx.moveTo(x,y)); mx.closePath(); mx.fill();
const [pf, px] = doek(W, H);
px.drawImage(foto, 0, 0); px.globalCompositeOperation = 'destination-in'; px.filter = 'blur(0.6px)'; px.drawImage(m, 0, 0); px.filter = 'none';
const [c, x] = doek(W, H);
x.drawImage(uit, 0, 0);
x.drawImage(pf, 0, 0);
// de uitsnede houdt links onder een grijze vlek over (zitting van de stoel): alles wat daar licht is weg
const blok = x.getImageData(0, 660, 230, 140), d = blok.data;
let weg = 0;
for (let i = 0; i < d.length; i += 4) {
  const l = 0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2];
  if (d[i+3] && l > 70) { d[i+3] = 0; weg++; }
}
x.putImageData(blok, 0, 660);
// rechts van x R niets meer (resten van het toetsenbord of de kamer)
x.clearRect(R, 0, W - R, H);
// uitsnede: 40 px lucht links van haar rug, kruin op y 50, onderkant door het bureaufront
const X0 = 95, Y0 = 0, BW = R - X0, BH = 730;
const [o, ox] = doek(BW, BH);
ox.drawImage(c, X0, Y0, BW, BH, 0, 0, BW, BH);
// onder haar rug blijft een halfdoorzichtige donkere waas van de stoel over: op de witte boog een vlek
const waas = ox.getImageData(0, 695, 90, BH - 695), e = waas.data;
for (let i = 0; i < e.length; i += 4) if (e[i+3] < 130) { e[i+3] = 0; weg++; }
ox.putImageData(waas, 0, 695);
bewaar('contact-klantenservice-boog-uit.webp', o, 'image/webp', 0.9);
// voorbeeld: op Diepblauw in een witte boog, en op een dambord
const [v, vx] = doek(BW * 2 + 40, BH);
vx.fillStyle = '#0B2352'; vx.fillRect(0, 0, BW, BH);
vx.fillStyle = '#fff'; vx.beginPath(); vx.moveTo(0, BH); vx.lineTo(0, BW / 2); vx.arc(BW / 2, BW / 2, BW / 2, Math.PI, 0); vx.lineTo(BW, BH); vx.closePath(); vx.fill();
for (let i = 0; i < BW; i += 20) for (let j = 0; j < BH; j += 20) { vx.fillStyle = ((i + j) / 20) % 2 ? '#ccc' : '#fff'; vx.fillRect(BW + 40 + i, j, 20, 20); }
vx.drawImage(o, 0, 0); vx.drawImage(o, BW + 40, 0);
bewaar('boog-voorbeeld.png', v);
return { weg, breed: BW, hoog: BH };
