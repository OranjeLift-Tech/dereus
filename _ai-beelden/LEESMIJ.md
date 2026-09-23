# Een beeldronde starten

Alles wat een ronde nodig heeft staat in `_ai-beelden/gereedschap/`. Schrijf één json-bestand met de
scenes en draai één commando; de map, de beelden en de reviewpagina komen daaruit.

## Het commando

```bash
node _ai-beelden/gereedschap/ronde.mjs <ronde.json>           # hele ronde
node _ai-beelden/gereedschap/ronde.mjs <ronde.json> 2 4       # alleen versie 2 en 4 opnieuw
node _ai-beelden/gereedschap/ronde.mjs <ronde.json> --pagina  # alleen de pagina herbouwen
node _ai-beelden/gereedschap/ronde.mjs <ronde.json> --prompts # alleen prompts.md schrijven
```

Het schrijft naar `website/review/<naam>-<datum>/` en eindigt met het pad naar `index.html` op één
regel. Die regel geef je aan de gebruiker. Die map staat in `.gitignore`.

## Het rondebestand

```json
{
  "naam": "drie-verhuizers-doos",
  "titel": "Drie verhuizers met een doos",
  "ratio": "1:1",
  "cast": ["mannen/man-18.png", "mannen/man-01.png"],
  "versies": [
    { "nr": 1, "naam": "Bank de stoep af", "scene": "Two movers carry a sofa ..." }
  ]
}
```

Optioneel: `lead`, `datum`, `grootte` (2K), `eenheid` (Versie of Kandidaat), `extra` (regels achter
de merkregels aan), en `lagen` en `crop` voor de reviewpagina. Met `lagen` toont de pagina per vak
het eerste bestand dat bestaat, bijvoorbeeld eerst `versie-{nr}-merk.png` en anders `versie-{nr}.png`.

## Twee regels zitten ingebakken

**Het merk gaat nooit in het prompt.** Het model tekent een logo na in plaats van het te plaatsen, en
elke ronde die om een borstteken vroeg kreeg een vervormd huisje met een onleesbaar regeltje eronder
terug. Vragen om een kleiner huisje helpt niet; de borst leeg vragen wel. `MERK` in
`gereedschap/gemini.mjs` vraagt daarom een egaal blauwe polo en blanco dozen. Het echte beeldmerk
komt er naderhand op met `gereedschap/merk-op-doos.py` (zie `MERK-OP-DOOS.md`).

**Alle versies van één ronde krijgen dezelfde cast.** Er overleeft er maar één. Wisselen de gezichten
per versie, dan kiest de gebruiker tussen mensen in plaats van tussen composities. `cast` wordt één
keer geladen en aan elke versie meegegeven.

De gezichten komen uit `~/.claude/skills/foto-verbeteren/assets/gezichten/`. **Lees daar eerst
`GEZICHTEN.md`**: het is een schaarse voorraad die tussen parallelle rondes gedeeld wordt.

## Wat het kost

Ongeveer **27 seconden**, ongeacht of het één beeld is of vijf: de beelden gaan parallel, met een dak
van vijf tegelijk. Gemeten op 22-09-2026: één beeld 27 s, drie tegelijk 28 s. Achter elkaar zou vijf
beelden ruim twee minuten kosten. Bij een tijdelijke fout (429, 5xx) volgen twee herkansingen met
4 en 8 seconden ertussen; een blijvende fout stopt meteen en de andere beelden lopen door.

Dit raakt geen gedeelde bestanden en mag naast andere sessies draaien. **Draai `_werk/build.py` niet**
terwijl anderen werken.

## De sleutel

Uit `GEMINI_API_KEY` of `~/.gemini_api_key`. Nooit in de repo, nooit printen.

## Taalverdeling in deze map

Node met sharp voor genereren en uitsnijden, Python met numpy en PIL voor compositie en perspectief
(`merk-op-doos.py`). Dat is een keuze en geen ongeluk: de projectieve warp en de luminantiekaart zijn
in numpy een paar regels en met de hand in node een bron van subtiele fouten.

## De oudere generatoren

De `*-gen.mjs` in deze map horen bij afgeronde rondes en draaien nog los, elk met hun eigen kopie van
de sleutel, de modelnaam en de herkansing. Ze zijn nog niet omgezet naar `gereedschap/gemini.mjs`.
Begin een nieuwe ronde met `ronde.mjs`; pas een oude alleen aan als je hem echt nodig hebt.
