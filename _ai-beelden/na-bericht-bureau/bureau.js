// Na uw bericht (/contact/): de klantenservice met haar bureau, zonder kamer erachter (zoals referentie A).
// Uitvoer: img/contact-klantenservice-bureau-uit.webp (1060 x 690, alfa).
// Bron: de vrouw uit img/contact-klantenservice-uit.webp, en uit img/contact-klantenservice-foto.webp
// een veelhoek met het bureau, de kop, het toetsenbord, de telefoon en het scherm (zelfde 1200x800-raster).
const foto = await laad('/img/contact-klantenservice-foto.webp');
const uit = await laad('/img/contact-klantenservice-uit.webp');
const W = 1200, H = 800;
// y 522 = achterrand van het bureau (onder de vensterbank); 1051-1066 = linkerrand van het scherm
const P = [[382,640],[505,522],[986,522],[986,497],[1051,492],[1066,62],[1200,86],[1200,800],[382,800]];
const [m, mx] = doek(W, H);
mx.fillStyle = '#000'; mx.beginPath(); P.forEach(([x,y],i)=> i?mx.lineTo(x,y):mx.moveTo(x,y)); mx.closePath(); mx.fill();
const [pf, px] = doek(W, H);
px.drawImage(foto, 0, 0); px.globalCompositeOperation = 'destination-in'; px.filter = 'blur(0.6px)'; px.drawImage(m, 0, 0); px.filter = 'none';
const [c, x] = doek(W, H);
x.drawImage(uit, 0, 0);
x.drawImage(pf, 0, 0);
// de uitsnede houdt links onder een grijze vlek over (armleuning van de stoel): alles wat daar licht is weg
const blok = x.getImageData(0, 660, 230, 140), d = blok.data;
let weg = 0;
for (let i = 0; i < d.length; i += 4) {
  const l = 0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2];
  if (d[i+3] && l > 70) { d[i+3] = 0; weg++; }
}
x.putImageData(blok, 0, 0 + 660);
// uitsnede: kruin op y 50, onderkant door het bureaufront
const X0 = 140, Y0 = 40, BW = 1060, BH = 690;
const [o, ox] = doek(BW, BH);
ox.drawImage(c, X0, Y0, BW, BH, 0, 0, BW, BH);
bewaar('contact-klantenservice-bureau-uit.webp', o, 'image/webp', 0.9);
const [v, vx] = doek(BW * 2 + 40, BH);
vx.fillStyle = '#0B2352'; vx.fillRect(0, 0, BW, BH);
for (let i = 0; i < BW; i += 20) for (let j = 0; j < BH; j += 20) { vx.fillStyle = ((i + j) / 20) % 2 ? '#ccc' : '#fff'; vx.fillRect(BW + 40 + i, j, 20, 20); }
vx.drawImage(o, 0, 0); vx.drawImage(o, BW + 40, 0);
bewaar('bureau-voorbeeld.png', v);
return { weg };
