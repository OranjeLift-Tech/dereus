// Haalt een egaal groen scherm (#00FF00) uit een foto: zachte randen, geen groene weerschijn.
import sharp from 'sharp';
export async function groenWeg(bron) {
  const { data, info } = await sharp(bron).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i], g = data[i + 1], b = data[i + 2];
    const groen = g - Math.max(r, b);
    if (groen > 60) data[i + 3] = 0;
    else if (groen > 20) data[i + 3] = Math.round(255 * (60 - groen) / 40);
    if (groen > 0) data[i + 1] = Math.max(r, b);
  }
  return sharp(data, { raw: info }).trim({ threshold: 1 });
}
