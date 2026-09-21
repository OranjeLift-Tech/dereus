// Maakt img/footer-verhuiswagen.svg uit de merkboek-mockup (brandbook/assets/mockups/verhuiswagen.svg):
// zonder decor en vloer, strak uitgesneden en met een schaduw die op het diepblauw van de footer past.
// Gebruik: node _werk/footer-wagen.cjs
const fs = require("fs");
const path = require("path");

const WORTEL = path.join(__dirname, "..");
const BRON = path.join(WORTEL, "brandbook/assets/mockups/verhuiswagen.svg");
const DOEL = path.join(WORTEL, "img/footer-verhuiswagen.svg");
const VIEWBOX = "150 30 1450 680";

let svg = fs.readFileSync(BRON, "utf8").replace(/\r\n/g, "\n");

function vervang(van, naar) {
  const n = svg.split(van).length - 1;
  if (n !== 1) throw new Error(`Verwacht 1 keer, gevonden ${n}: ${van.slice(0, 70)}`);
  svg = svg.replace(van, naar);
}

svg = svg.replace(/^<\?xml[^>]*\?>\n/, "");
svg = svg.replace(/<svg [^>]*>/, `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="${VIEWBOX}">`);
svg = svg.replace(/<title[\s\S]*?<\/title>\n?/, "").replace(/<desc[\s\S]*?<\/desc>\n?/, "");
vervang('<rect width="1750" height="750" fill="url(#decor)"/>\n', "");
vervang('<rect y="684.5" width="1750" height="65.5" fill="#E1E5EC"/>\n', "");
vervang('<ellipse cx="825" cy="801" rx="720" ry="15" fill="#0E1A33" opacity=".22" filter="url(#zacht)"/>',
        '<ellipse cx="825" cy="801" rx="720" ry="15" fill="#000" opacity=".5" filter="url(#zacht)"/>');
svg = svg.split('ry="7" fill="#0E1A33" opacity=".35"/>').join('ry="7" fill="#000" opacity=".45"/>');

fs.writeFileSync(DOEL, svg.trim() + "\n", "utf8");
console.log("geschreven:", path.relative(WORTEL, DOEL), Math.round(svg.length / 1024) + " kB");
