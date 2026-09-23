#!/usr/bin/env python3
"""Bouwt de reviewpagina van een beeldronde: N vakken, een keuzeknop per vak en een notitieveld.

    python _ai-beelden/gereedschap/rondepagina.py website/review/<naam>-<datum> \
        --titel "Drie verhuizers met een doos" --aantal 5

De vorm komt van de ronde die dereus-54 op 22-09-2026 bouwde
(website/review/drie-verhuizers-doos-20260922/index.html). Die logica stond in de ronde-map zelf en
ging daarmee verloren zodra de ronde afliep. Hier staat hij één keer, zodat elke volgende ronde
dezelfde pagina krijgt en er geen tweede stijl ontstaat.

Waarom niet in website/review/maak-index.py: die map staat in .gitignore en het script is niet
getrackt. Gereedschap dat elke ronde nodig heeft moet een kloon overleven, dus staat het hier.
maak-index.py blijft de bouwer van de overzichtspagina website/review/index.html; dat is een andere
pagina met een andere vraag.

De pagina zoekt de bestanden zelf op in de browser en blijft leeg waar er nog niets staat. Daardoor
kun je hem openen zodra de ronde start en hoeft de generator niet te wachten met schrijven.

Deze pagina is een lokaal bestand in website/review/. Nooit een claude.ai-link.
"""
import argparse
import html
import json
import pathlib
import sys

HIER = pathlib.Path(__file__).resolve().parent
SJABLOON = HIER / "rondepagina.css"


def e(t):
    return html.escape(str(t if t is not None else ""), quote=True)


CSS = """
:root {
  --grond:#EFF0F4; --vlak:#FFFFFF; --inkt:#121726; --zacht:#5A6376; --lijn:#D6DAE3;
  --blauw:#1746A2; --geel:#FFCC33; --podium:#14161B; --goed:#1B7F45; --let:#A8452F;
  --gutter:clamp(16px,4vw,40px);
  --display:"Archivo","Segoe UI",system-ui,sans-serif;
  --body:"IBM Plex Sans","Segoe UI",system-ui,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --grond:#0F1218; --vlak:#171B22; --inkt:#E7EAF1; --zacht:#98A1B3; --lijn:#262C38;
    --blauw:#7BA2EE; --goed:#4FB77B; --let:#E08268;
  }
}
:root[data-theme="dark"] {
  --grond:#0F1218; --vlak:#171B22; --inkt:#E7EAF1; --zacht:#98A1B3; --lijn:#262C38;
  --blauw:#7BA2EE; --goed:#4FB77B; --let:#E08268;
}
*,*::before,*::after { box-sizing:border-box; }
body {
  margin:0; background:var(--grond); color:var(--inkt); overflow-x:hidden;
  font:400 15.5px/1.6 var(--body); -webkit-font-smoothing:antialiased;
}
.wrap { max-width:1500px; margin-inline:auto; padding-inline:var(--gutter); padding-block:clamp(24px,5vw,44px) 64px; }
.eyebrow { font:500 11.5px/1 var(--mono); letter-spacing:.14em; text-transform:uppercase; color:var(--zacht); margin:0 0 14px; }
h1 { font:700 clamp(26px,3.2vw,40px)/1.08 var(--display); letter-spacing:-.022em; margin:0 0 12px; text-wrap:balance; }
.lead { margin:0; max-width:64ch; color:var(--zacht); }
.lead b { color:var(--inkt); font-weight:600; }

.balk {
  display:flex; flex-wrap:wrap; align-items:center; gap:10px 18px;
  margin-top:clamp(20px,3vw,28px); padding-bottom:16px; border-bottom:1px solid var(--lijn);
}
.stand { font:500 13px/1.4 var(--mono); color:var(--zacht); flex:1 1 14rem; min-width:0; margin:0; }
.stand b { color:var(--inkt); }
.groepje { display:flex; align-items:center; gap:6px; }
.groepje .kop { font:500 11.5px/1 var(--mono); letter-spacing:.1em; text-transform:uppercase; color:var(--zacht); margin-right:2px; }
.mini {
  font:500 13px/1 var(--mono); padding:8px 11px; border-radius:3px; cursor:pointer;
  border:1px solid var(--lijn); background:var(--vlak); color:var(--zacht);
}
.mini:hover { border-color:var(--blauw); color:var(--blauw); }
.mini[aria-pressed="true"] { background:var(--blauw); border-color:var(--blauw); color:#FFF; }
.mini:disabled { opacity:.5; cursor:default; }

.rooster { display:grid; gap:14px; margin-top:20px; grid-template-columns:repeat(var(--kol,3),minmax(0,1fr)); }
@media (max-width:1100px) { .rooster { grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media (max-width:680px)  { .rooster { grid-template-columns:minmax(0,1fr); } }

.kaart {
  min-width:0; background:var(--vlak); border:1px solid var(--lijn); border-radius:4px;
  padding:12px; display:flex; flex-direction:column; gap:10px;
}
.kaart[data-gemarkeerd="ja"] { border-color:var(--geel); box-shadow:0 0 0 2px rgb(255 204 51 / .35); }
.kaartkop { display:flex; align-items:baseline; justify-content:space-between; gap:10px; }
.kaartkop .nr { font:600 15px/1.2 var(--display); }
.kaartkop .bron { font:500 11px/1.3 var(--mono); letter-spacing:.06em; text-transform:uppercase; color:var(--zacht); text-align:right; }
.kaartkop .bron.klaar { color:var(--goed); }
.kaartkop .bron.ruw { color:#A07714; }

/* Geen vaste verhouding: het beeld bepaalt zijn eigen hoogte, alleen het wachtvak heeft een maat nodig. */
.vak {
  position:relative; display:block; background:var(--podium);
  border-radius:3px; overflow:hidden; text-decoration:none;
}
.vak img { display:block; width:100%; height:auto; }
.vak .volle {
  position:absolute; right:8px; bottom:8px; font:400 11px/1 var(--mono); color:#C9CEDA;
  background:rgb(10 12 16 / .65); padding:5px 8px; border-radius:3px; opacity:0; transition:opacity .15s;
}
.vak:hover .volle, .vak:focus-visible .volle { opacity:1; }
.vak.wacht { aspect-ratio:var(--verhouding,3/2); display:grid; place-items:center; padding:16px; text-align:center; cursor:default; }
.vak.wacht .volle { display:none; }
.vak.wacht .leegtekst { font:400 13px/1.5 var(--mono); color:#8A93A5; max-width:28ch; }

.croprij { display:grid; gap:5px; }
.croplabel { margin:0; font:500 11px/1 var(--mono); letter-spacing:.08em; text-transform:uppercase; color:var(--zacht); }
.cropvak {
  position:relative; display:block; min-height:96px; border-radius:3px; overflow:hidden;
  background:var(--podium); text-decoration:none;
}
.cropvak img { display:block; width:100%; height:auto; max-height:260px; object-fit:contain; }
.cropvak.wacht {
  display:grid; place-items:center; background:transparent; border:1px dashed var(--lijn);
  padding:12px; text-align:center; cursor:default;
}
.cropvak.wacht .leegtekst { font:400 12px/1.5 var(--mono); color:var(--zacht); max-width:30ch; }

.knop {
  font:600 14px/1 var(--display); padding:11px 14px; border-radius:3px; cursor:pointer;
  border:1px solid var(--blauw); background:var(--blauw); color:#FFF; width:100%;
}
.knop:hover { filter:brightness(1.08); }
.knop.al { background:var(--geel); border-color:var(--geel); color:#14161B; }
.knop.uit { background:transparent; border-color:var(--lijn); color:var(--zacht); }
.knop.uit:hover { border-color:var(--blauw); color:var(--blauw); filter:none; }

textarea {
  width:100%; max-width:100%; min-height:72px; resize:vertical; padding:9px 10px;
  font:400 14px/1.5 var(--body); color:var(--inkt); background:var(--grond);
  border:1px solid var(--lijn); border-radius:3px;
}
textarea:focus-visible { outline:2px solid var(--blauw); outline-offset:1px; }
.bewaard { font:400 11px/1.2 var(--mono); color:var(--goed); min-height:13px; margin:-4px 0 0; }

.uitkomst {
  margin-top:clamp(26px,4vw,34px); padding-top:20px; border-top:1px solid var(--lijn);
  display:flex; flex-wrap:wrap; align-items:center; gap:12px 16px;
}
.uitkomst .knop { width:auto; }
.uitleg { font-size:13.5px; color:var(--zacht); flex:1 1 18rem; min-width:0; margin:0; overflow-wrap:anywhere; white-space:pre-line; }
.uitleg b { color:var(--inkt); font-weight:600; }

footer { margin-top:40px; padding-top:18px; border-top:1px solid var(--lijn); font-size:13px; color:var(--zacht); }
footer p { margin:0 0 7px; }
footer code { font:400 12.5px/1.5 var(--mono); background:var(--vlak); border:1px solid var(--lijn); padding:2px 6px; border-radius:3px; overflow-wrap:anywhere; }
@media (prefers-reduced-motion: reduce) { * { transition:none !important; } }
"""


SCRIPT = """
const NRS = __NRS__;
const SLEUTEL = "__SLEUTEL__";
const LAGEN = __LAGEN__;          // per versie op volgorde: het eerste bestand dat bestaat wint
const CROP = __CROP__;            // {patroon, label} of null
const EENHEID = "__EENHEID__";    // "Versie" of "Kandidaat"

const vul = (patroon, nr) => patroon.replace(/\\{nr\\}/g, nr);

let staat = { gemarkeerd: [], notities: {} };
try {
  const rauw = localStorage.getItem(SLEUTEL);
  if (rauw) {
    const g = JSON.parse(rauw);
    if (Array.isArray(g.gemarkeerd)) staat.gemarkeerd = g.gemarkeerd.map(Number);
    if (g.notities && typeof g.notities === "object") staat.notities = g.notities;
  }
} catch (e) { /* privevenster of geblokkeerde opslag: de pagina werkt verder gewoon */ }

function bewaar() {
  try { localStorage.setItem(SLEUTEL, JSON.stringify(staat)); return true; } catch (e) { return false; }
}

const rooster = document.getElementById("rooster");
const kaarten = new Map();

NRS.forEach((nr) => {
  const kaart = document.createElement("article");
  kaart.className = "kaart";
  kaart.dataset.nr = String(nr);
  kaart.innerHTML =
    '<div class="kaartkop"><span class="nr">' + EENHEID + ' ' + nr + '</span><span class="bron"></span></div>' +
    '<a class="vak wacht" target="_blank" rel="noopener"><span class="leegtekst"></span>' +
    '<span class="volle">volle resolutie</span></a>' +
    (CROP ? '<div class="croprij"><p class="croplabel">' + CROP.label + '</p>' +
      '<a class="cropvak wacht" target="_blank" rel="noopener"><span class="leegtekst"></span></a></div>' : '') +
    '<button class="knop uit" type="button">Deze houden</button>' +
    '<textarea placeholder="Notitie bij ' + EENHEID.toLowerCase() + ' ' + nr + '"></textarea>' +
    '<p class="bewaard"></p>';
  rooster.append(kaart);

  const knop = kaart.querySelector(".knop");
  const veld = kaart.querySelector("textarea");
  const melding = kaart.querySelector(".bewaard");

  knop.addEventListener("click", () => {
    const i = staat.gemarkeerd.indexOf(nr);
    if (i === -1) staat.gemarkeerd.push(nr); else staat.gemarkeerd.splice(i, 1);
    staat.gemarkeerd.sort((a, b) => a - b);
    const ok = bewaar();
    tekenKaart(nr);
    tekenUitkomst();
    melding.textContent = ok ? "" : "Deze browser bewaart niets, noem het nummer even in het gesprek.";
  });

  let klok;
  veld.addEventListener("input", () => {
    staat.notities[nr] = veld.value;
    clearTimeout(klok);
    klok = setTimeout(() => {
      const ok = bewaar();
      melding.textContent = ok ? "notitie bewaard" : "niet bewaard, deze browser blokkeert opslag";
      tekenUitkomst();
      if (ok) setTimeout(() => { melding.textContent = ""; }, 2000);
    }, 400);
  });

  veld.value = staat.notities[nr] || "";
  kaarten.set(nr, kaart);
  tekenKaart(nr);
});

function tekenKaart(nr) {
  const kaart = kaarten.get(nr);
  const aan = staat.gemarkeerd.includes(nr);
  const knop = kaart.querySelector(".knop");
  kaart.dataset.gemarkeerd = aan ? "ja" : "nee";
  knop.className = "knop " + (aan ? "al" : "uit");
  knop.textContent = aan ? "Gemarkeerd \\u2713" : "Deze houden";
}

// Zoekt per versie het beste bestand dat er is. Geen onerror-ketting in de opmaak: een losse probe
// houdt het vak leeg zolang er niets staat, in plaats van een kapot plaatje te laten zien.
function probeer(pad, verval) {
  return new Promise((klaar) => {
    const im = new Image();
    im.onload = () => klaar(true);
    im.onerror = () => klaar(false);
    im.src = verval ? pad + "?t=" + verval : pad;
  });
}

function zetBeeld(vak, pad, alt, verval) {
  vak.classList.remove("wacht");
  vak.href = pad;
  let im = vak.querySelector("img");
  if (!im) { im = document.createElement("img"); vak.prepend(im); }
  im.src = verval ? pad + "?t=" + verval : pad;
  im.alt = alt;
  im.loading = "lazy";
  vak.querySelector(".leegtekst").textContent = "";
}

function zetLeeg(vak, tekst) {
  vak.classList.add("wacht");
  vak.removeAttribute("href");
  const im = vak.querySelector("img");
  if (im) im.remove();
  vak.querySelector(".leegtekst").textContent = tekst;
}

async function laad(verval) {
  let gevonden = 0, af = 0, crops = 0;
  for (const nr of NRS) {
    const kaart = kaarten.get(nr);
    const vak = kaart.querySelector(".vak");
    const bronvak = kaart.querySelector(".bron");
    let bron = null;
    for (const laag of LAGEN) {
      const pad = vul(laag.patroon, nr);
      if (await probeer(pad, verval)) { bron = { ...laag, pad }; break; }
    }
    if (bron) {
      gevonden++;
      if (bron.klasse === "klaar") af++;
      zetBeeld(vak, bron.pad, EENHEID + " " + nr + ", " + bron.label, verval);
      bronvak.textContent = bron.label;
      bronvak.className = "bron " + (bron.klasse || "");
    } else {
      zetLeeg(vak, vul(LAGEN[LAGEN.length - 1].patroon, nr) + " is er nog niet");
      bronvak.textContent = "wacht op het beeld";
      bronvak.className = "bron";
    }

    if (CROP) {
      const cropvak = kaart.querySelector(".cropvak");
      const cropPad = vul(CROP.patroon, nr);
      if (await probeer(cropPad, verval)) {
        crops++;
        zetBeeld(cropvak, cropPad, "Uitsnede bij " + EENHEID.toLowerCase() + " " + nr, verval);
      } else {
        zetLeeg(cropvak, "uitsnede volgt");
      }
    }
  }
  const meer = LAGEN.length > 1 ? ", waarvan <b>" + af + "</b> afgewerkt" : "";
  const crop = CROP ? ", en <b>" + crops + "</b> uitsnede" + (crops === 1 ? "" : "s") : "";
  document.getElementById("stand").innerHTML =
    "<b>" + gevonden + " van de " + NRS.length + "</b> beelden staan er" + meer + crop + ".";
}

function tekenUitkomst() {
  const t = document.getElementById("uitkomsttekst");
  if (!staat.gemarkeerd.length) { t.textContent = "Nog niets gemarkeerd."; return; }
  const n = Object.values(staat.notities).filter((v) => v && v.trim()).length;
  t.innerHTML = "Gemarkeerd: " + EENHEID.toLowerCase() + " <b>" + staat.gemarkeerd.join(" en ") + "</b>" +
    (n ? ", met " + n + " notitie" + (n === 1 ? "" : "s") : "") + ".";
}

document.getElementById("kopieer").addEventListener("click", (ev) => {
  const regels = [staat.gemarkeerd.length
    ? "__TITEL__: houden " + EENHEID.toLowerCase() + " " + staat.gemarkeerd.join(" en ")
    : "__TITEL__: nog niets gemarkeerd"];
  NRS.forEach((nr) => {
    const n = (staat.notities[nr] || "").trim();
    if (n) regels.push(EENHEID + " " + nr + ": " + n);
  });
  const tekst = regels.join("\\n");
  const knop = ev.currentTarget;
  const klaar = () => {
    knop.textContent = "Gekopieerd \\u2713";
    setTimeout(() => { knop.textContent = "Uitkomst kopieren"; }, 1800);
  };
  const terugval = () => { document.getElementById("uitkomsttekst").textContent = tekst; };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(tekst).then(klaar, terugval);
  } else {
    terugval();
  }
});

const kolknoppen = document.querySelectorAll("[data-kol]");
kolknoppen.forEach((knop) => {
  knop.addEventListener("click", () => {
    kolknoppen.forEach((k) => k.setAttribute("aria-pressed", String(k === knop)));
    rooster.style.setProperty("--kol", knop.dataset.kol);
    try { localStorage.setItem(SLEUTEL + "-kolommen", knop.dataset.kol); } catch (e) {}
  });
});
try {
  const kol = localStorage.getItem(SLEUTEL + "-kolommen");
  if (kol) {
    rooster.style.setProperty("--kol", kol);
    kolknoppen.forEach((k) => k.setAttribute("aria-pressed", String(k.dataset.kol === kol)));
  }
} catch (e) {}

document.getElementById("ververs").addEventListener("click", (ev) => {
  const knop = ev.currentTarget;
  knop.disabled = true;
  knop.textContent = "Zoeken\\u2026";
  laad(Date.now()).then(() => { knop.disabled = false; knop.textContent = "Opnieuw laden"; });
});

tekenUitkomst();
laad(0);
"""


def bouw(titel, lead, sleutel, nrs, lagen, crop, eenheid, datum, verhouding, voet):
    """Geeft de HTML van de reviewpagina terug."""
    script = (SCRIPT
              .replace("__NRS__", json.dumps(nrs))
              .replace("__SLEUTEL__", sleutel)
              .replace("__LAGEN__", json.dumps(lagen, ensure_ascii=False))
              .replace("__CROP__", json.dumps(crop, ensure_ascii=False) if crop else "null")
              .replace("__EENHEID__", eenheid)
              .replace("__TITEL__", titel.replace('"', "'")))
    voetregels = "\n".join(f"    <p>{r}</p>" for r in voet)
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(titel)} &middot; beeldkeuze</title>
<style>
:root {{ --verhouding:{verhouding}; }}
{CSS}</style>
</head>
<body>
<div class="wrap">
  <p class="eyebrow">De Reus &middot; beeldronde {e(datum)}</p>
  <h1>{e(titel)}</h1>
  <p class="lead">{lead}</p>

  <div class="balk">
    <p class="stand" id="stand">Beelden worden gezocht&hellip;</p>
    <div class="groepje">
      <span class="kop">breedte</span>
      <button class="mini" type="button" data-kol="1" aria-pressed="false">1</button>
      <button class="mini" type="button" data-kol="3" aria-pressed="true">3</button>
      <button class="mini" type="button" data-kol="5" aria-pressed="false">5</button>
    </div>
    <button class="mini" type="button" id="ververs">Opnieuw laden</button>
  </div>

  <div class="rooster" id="rooster"></div>

  <div class="uitkomst">
    <button class="knop" type="button" id="kopieer">Uitkomst kopieren</button>
    <p class="uitleg" id="uitkomsttekst">Nog niets gemarkeerd.</p>
  </div>

  <footer>
{voetregels}
    <p>Landen er beelden terwijl deze pagina openstaat, druk dan op <b>Opnieuw laden</b>: hij zoekt de
       bestanden opnieuw op, langs de browsercache heen. Deze map staat in <code>.gitignore</code>, er gaat
       hiervan niets naar de repo.</p>
  </footer>
</div>

<script>
{script}</script>
</body>
</html>
"""


def schrijf(map_, titel, aantal=None, lead="", sleutel=None, lagen=None, crop=None,
            eenheid="Versie", datum=None, verhouding="3/2", voet=None, nrs=None):
    """Schrijft index.html in `map_` en geeft het pad terug.

    `nrs` is de lijst versienummers. Laat hem weg en het wordt 1..aantal. Een vervolgronde houdt
    de nummers van de ronde ervoor (bijvoorbeeld [2, 4, 5]), zodat de gebruiker zijn eigen keuze
    terugziet in plaats van een nieuwe telling.
    """
    nrs = [int(n) for n in nrs] if nrs else list(range(1, (aantal or 5) + 1))
    map_ = pathlib.Path(map_)
    map_.mkdir(parents=True, exist_ok=True)
    naam = map_.name
    sleutel = sleutel or f"dereus-{naam}"
    datum = datum or (naam.rsplit("-", 1)[-1] if naam.rsplit("-", 1)[-1].isdigit() else "")
    if len(datum) == 8:
        datum = f"{datum[6:8]}-{datum[4:6]}-{datum[0:4]}"
    lagen = lagen or [{"patroon": "versie-{nr}.png", "label": "ruw uit de generator", "klasse": "ruw"}]
    voet = voet or [
        "De pagina zoekt per vak zelf het beste bestand dat er is en blijft leeg zolang er niets staat, "
        "in plaats van een kapot plaatje te tonen."
    ]
    if not lead:
        lead = (f"{len(nrs)} versies van hetzelfde tafereel. Markeer wat u wilt houden en zet er een notitie bij; "
                f"de keuze blijft in deze browser bewaard.")
    doel = map_ / "index.html"
    doel.write_text(bouw(titel, lead, sleutel, nrs, lagen, crop, eenheid, datum, verhouding, voet),
                    encoding="utf-8")
    return doel


def main():
    p = argparse.ArgumentParser(description="Bouwt de reviewpagina van een beeldronde.")
    p.add_argument("map", help="de ronde-map, bijvoorbeeld website/review/dozen-20260922")
    p.add_argument("--titel", required=True)
    p.add_argument("--aantal", type=int, default=5)
    p.add_argument("--nrs", default="", help="losse versienummers, bijvoorbeeld 2,4,5; leeg = 1 t/m --aantal")
    p.add_argument("--lead", default="")
    p.add_argument("--eenheid", default="Versie", help="Versie of Kandidaat")
    p.add_argument("--verhouding", default="3/2", help="verhouding van het wachtvak, bijvoorbeeld 1/1")
    p.add_argument("--lagen", default="", help="JSON-lijst met {patroon,label,klasse}; leeg = alleen versie-{nr}.png")
    p.add_argument("--crop", default="", help="JSON met {patroon,label}; leeg = geen uitsnedevak")
    args = p.parse_args()
    doel = schrijf(
        args.map, args.titel, args.aantal, lead=args.lead, eenheid=args.eenheid,
        verhouding=args.verhouding,
        nrs=[int(n) for n in args.nrs.replace(",", " ").split()] if args.nrs else None,
        lagen=json.loads(args.lagen) if args.lagen else None,
        crop=json.loads(args.crop) if args.crop else None,
    )
    print(doel.resolve().as_posix())


if __name__ == "__main__":
    sys.exit(main())
