# 3D-voorwerpen voor de contactkaarten

De telefoon, envelop, het klembord en de verhuisdoos in `img/contact-3d/` zijn renders uit three.js (geen AI-beeld).
Eén lichtbron linksboven, fysieke materialen, transparante achtergrond, het echte logo als opdruk op de doos.

Opnieuw maken:

1. `npm i three@0.186.0` in deze map (node_modules staat niet in de repo).
2. `node render.cjs` schrijft `uit/<naam>.png` (1000 x 1000). Het script gebruikt playwright uit de npx-cache en de
   geïnstalleerde Chrome; pas het pad bovenin aan als dat verandert.
3. `node export.cjs` snijdt bij op de alfa en schrijft `img/contact-3d/<naam>.webp` (400 px hoog).

Verandert een maat, werk dan `VOORWERP` in `_werk/blokken/contactkaarten.py` bij. Vormgeving staat onderaan
`css/blok/contactkaarten.css`.

## Vertrouwensrij (reviewkaart, schild, headset, klok)

Zelfde opzet, eigen bestanden: `scene-vertrouwen.html` met `score`, `schild`, `headset` en `klok`.

1. `node render2.cjs scene-vertrouwen.html score schild headset klok` schrijft `uit/<naam>.png` en een controleblad
   `uit/blad-scene-vertrouwen.png`. De Google-G komt uit de sprite in `contact/index.html`, dus in de echte kleuren.
2. `node export2.cjs score schild headset klok` schrijft `img/contact-3d/<naam>.webp` (320 px hoog).

Maten staan in `VOORWERP` in `_werk/blokken/vertrouwensrij.py`; vormgeving onderaan `css/blok/vertrouwensrij.css`.
