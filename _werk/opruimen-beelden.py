"""Beelden opruimen zonder dat het een eenrichtingsstraat wordt.

    python _werk/opruimen-beelden.py --lijst <bestand> --droog     tonen wat er zou gebeuren
    python _werk/opruimen-beelden.py --lijst <bestand>             verplaatsen naar het archief
    python _werk/opruimen-beelden.py --terug                       alles exact terugzetten

Verplaatsen, niet verwijderen. Alles gaat naar `_ai-beelden/archief/ongebruikt-20260922/` met
de mappenstructuur eronder intact, en `verplaatst.json` houdt van -> naar bij, met de maat en
een sha256 per bestand. `--terug` leest dat bestand en zet alles op zijn oude plek, en
weigert als de inhoud onderweg veranderd is.

DE LIJST IS DE GRENS. Het script raakt niets aan wat niet in de meegegeven lijst staat, en het
loopt geen mappen af op zoek naar meer. Mappen weigert het ook: een map meegeven is bijna altijd
een vergissing, en wie het echt bedoelt zegt dat met --mappen.

MAAR DE LIJST IS NIET HET LAATSTE WOORD. Voor elk pad in de lijst wordt opnieuw opgezocht waar
het vandaan verwezen wordt (zie beeldpaden.py), en daar hangt de uitkomst aan:

  in gebruik     verwezen vanuit de site of de bouwbron. Het script stopt, verplaatst niets en
                 noemt het bewijs. Alles of niets, want een halve opruiming is lastiger terug
                 te draaien dan geen.
  bronmateriaal  alleen verwezen vanuit een generator, een oude reviewronde of een
                 ontwerpvariant. Dat is werkmateriaal en gaat NIET mee; het wordt overgeslagen
                 en gemeld. Met --ook-bronmateriaal gaat het alsnog mee.
  ongebruikt     nergens vandaan verwezen. Dit is wat er verplaatst wordt.

Die tweede regel is er omdat een lijst die uit "grep de gebouwde pagina's" komt te ruim is: de
blokken bouwen hun paden met f-strings (`f"/img/kaart-{slug}.svg"`) en van de pagina's die de
build kan maken staan er nu tien in de wortel. Letterlijk zoeken mist daardoor onder meer alle
elf kaart-*.svg. Beter dat dit script weigert dan dat het de lijst gelooft.

--weg: echt verwijderen, alleen voor wat git niet kent
------------------------------------------------------
Bak 3 en 4 (reviewrondes, archief, kandidatenreeksen) staan in .gitignore. Verplaatsen levert
daar geen schijfruimte op en git kan het niet terughalen, dus daar is verwijderen echt
verwijderen. Daarvoor is `--weg`, en die stand is met opzet stug:

    python _werk/opruimen-beelden.py --lijst <bestand> --weg --droog
    python _werk/opruimen-beelden.py --lijst <bestand> --weg --ja

  * weigert elk pad dat git wel kent, want dat hoort verplaatst of gecommit te worden. Die
    grens gaat alleen open met --getrackt-toegestaan erbij, en die schakelaar werkt op zijn
    beurt alleen samen met --weg --ja. Voor een getrackt bestand IS git het vangnet: een
    `git checkout -- <pad>` haalt het terug, ook zonder archiefmap;
  * weigert elk pad uit de beschermde lijst hieronder, zonder ontsnapping;
  * weigert tekst: .md .py .cjs .mjs .txt .json en alles met "prompt" in de naam. Dat is het
    geheugen van een ronde, het weegt niets, en het is precies wat je mist als het weg is;
  * doet niets zonder --ja, en schrijft `verwijderd.json` als bewijsstuk achteraf.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import beeldpaden  # noqa: E402

WORTEL = beeldpaden.WORTEL
ARCHIEF = "_ai-beelden/archief/ongebruikt-20260922"
BOEKHOUDING = "verplaatst.json"
BEWIJSSTUK = "_werk/verwijderd-20260922.json"

# Nooit aanraken, in geen enkele stand, hoe de lijst er ook uitziet.
BESCHERMD = (
    "_ai-beelden/foto/",          # het bronmateriaal waar elke re-export uit komt
    "_ai-beelden/archief/",       # waar dit script zelf naartoe verplaatst
    "brandbook/",                 # de bron van het officiele logo
    # _voorbeeld/ ziet eruit als weggooibare voorvertoning, maar het is nu het enige bewijs dat
    # negen headerbeelden in gebruik zijn (img/headers/{delft,leiden,...}.svg). Valt die map weg,
    # dan zakken die negen naar ongebruikt terwijl img/headers/manifest.json ze nog aanwijst, en
    # sterft de eerstvolgende build op de BouwFout in kit.py:258.
    "_voorbeeld/",
    "_werk/",
    "css/",
    "js/",
    "fonts/",
)
# Rondes waar vandaag nog in gewerkt wordt.
BESCHERMDE_RONDES = (
    "drie-verhuizers-doos-20260922",
    "twee-verhuizers-20260922",
    "opruimen-beelden-20260922",
    "gezicht-test-20260922",
    "team-drie-20260922",
)
# De tekst van een ronde: wat er besloten is en waarom. Weegt niets, blijft staan.
TEKST_SUFFIX = (".md", ".py", ".cjs", ".mjs", ".js", ".txt", ".json", ".html", ".css")


def lees_lijst(bron):
    """De lijst paden: een tekstbestand met een pad per regel, of json, of - voor stdin.

    Json mag een lijst strings zijn, of een object {groep: [paden]}. In dat laatste geval
    houdt elke groep zijn eigen naam in verplaatst.json.
    """
    tekst = sys.stdin.read() if bron == "-" else Path(bron).read_text(encoding="utf-8")
    tekst = tekst.strip()
    if tekst.startswith(("[", "{")):
        data = json.loads(tekst)
        if isinstance(data, list):
            return {"beelden": [str(p) for p in data]}
        uit = {}
        for sleutel, waarde in data.items():
            if isinstance(waarde, list) and all(isinstance(p, str) for p in waarde):
                uit[sleutel] = waarde
        if not uit:
            raise SystemExit(f"{bron}: json zonder een lijst paden erin")
        return uit
    paden = []
    for regel in tekst.splitlines():
        regel = regel.split("#")[0].strip()
        if regel:
            paden.append(regel)
    return {"beelden": paden}


def normaliseer(ruw):
    """Een pad uit de lijst naar een repo-relatief pad, of een reden waarom niet."""
    schoon = ruw.strip().strip('"').replace("\\", "/").lstrip("/")
    if not schoon:
        return None, "lege regel"
    pad = (WORTEL / schoon).resolve()
    try:
        rel = pad.relative_to(WORTEL).as_posix()
    except ValueError:
        return None, "ligt buiten de repo"
    return rel, None


def beschermd(rel):
    """De reden waarom dit pad nooit weg mag, of None."""
    if any(rel == b.rstrip("/") or rel.startswith(b) for b in BESCHERMD):
        return f"beschermde map ({next(b for b in BESCHERMD if rel.startswith(b) or rel == b.rstrip('/'))})"
    for ronde in BESCHERMDE_RONDES:
        if ronde in rel.split("/"):
            return f"ronde {ronde} staat nog open"
    return None


def git_kent(paden):
    """Welke van deze paden git volgt. Een getrackt bestand hoort niet via --weg weg."""
    if not paden:
        return set()
    uit = set()
    for begin in range(0, len(paden), 500):
        brok = paden[begin:begin + 500]
        klaar = subprocess.run(["git", "ls-files", "--", *brok], cwd=WORTEL,
                               capture_output=True, text=True)
        uit.update(r.strip() for r in klaar.stdout.splitlines() if r.strip())
    return uit


def hash_van(pad):
    h = hashlib.sha256()
    with open(pad, "rb") as bestand:
        for blok in iter(lambda: bestand.read(1 << 20), b""):
            h.update(blok)
    return h.hexdigest()


def maat_van(pad):
    if pad.is_dir():
        return sum(p.stat().st_size for p in pad.rglob("*") if p.is_file())
    return pad.stat().st_size


def beoordeel(groepen, opties):
    """Per pad: wat ermee gebeurt en waarom. Verandert niets op schijf."""
    alle = [p for lijst in groepen.values() for p in lijst]
    genormaliseerd, fouten = [], []
    for ruw in alle:
        rel, reden = normaliseer(ruw)
        if reden:
            fouten.append((ruw, reden))
        else:
            genormaliseerd.append(rel)

    kaart = beeldpaden.scan(extra=[p for p in genormaliseerd
                                   if (WORTEL / p).is_file()
                                   and (WORTEL / p).suffix.lower() in beeldpaden.BEELD_SUFFIX])
    getrackt = git_kent(genormaliseerd) if opties.weg else set()

    uit = []
    for groep, lijst in groepen.items():
        for ruw in lijst:
            rel, reden = normaliseer(ruw)
            if reden:
                uit.append({"groep": groep, "pad": ruw, "doen": "weiger", "reden": reden})
                continue
            pad = WORTEL / rel
            regel = {"groep": groep, "pad": rel, "doen": "weiger", "reden": "", "bytes": 0}

            reden = beschermd(rel)
            if reden:
                regel["reden"] = reden
            elif not pad.exists():
                regel["reden"] = "bestaat niet"
            elif pad.is_dir() and not opties.mappen:
                regel["reden"] = "is een map (gebruik --mappen als dat de bedoeling is)"
            elif opties.weg and rel in getrackt and not opties.getrackt_toegestaan:
                regel["reden"] = "git volgt dit bestand; verplaatsen of committen, niet --weg"
            elif opties.weg and not pad.is_dir() and pad.suffix.lower() in TEKST_SUFFIX:
                regel["reden"] = "tekst van een ronde blijft staan"
            elif opties.weg and not pad.is_dir() and "prompt" in pad.name.lower():
                regel["reden"] = "prompt van een ronde blijft staan"
            else:
                gegevens = kaart.get(rel)
                klasse = gegevens["klasse"] if gegevens else "ongebruikt"
                regel["bytes"] = maat_van(pad)
                if klasse == "in gebruik":
                    regel["reden"] = "IN GEBRUIK: " + "; ".join(gegevens["bewijs"][:3])
                elif klasse == "bronmateriaal" and not opties.ook_bronmateriaal:
                    regel["doen"] = "sla over"
                    regel["reden"] = "bronmateriaal: " + "; ".join(gegevens["bewijs"][:2])
                else:
                    regel["doen"] = "weg" if opties.weg else "verplaats"
                    if gegevens and gegevens["bijna"]:
                        regel["reden"] = "let op: " + gegevens["bijna"][0]
            uit.append(regel)
    return uit, fouten


def toon(besluiten, opties):
    per = {"verplaats": [], "weg": [], "sla over": [], "weiger": []}
    for regel in besluiten:
        per[regel["doen"]].append(regel)

    for naam, kop in (("weiger", "GEWEIGERD, hier gebeurt niets mee"),
                      ("sla over", "OVERGESLAGEN, bronmateriaal blijft staan"),
                      ("verplaats", "VERPLAATSEN naar " + ARCHIEF),
                      ("weg", "VERWIJDEREN, niet terug te halen")):
        regels = per[naam]
        if not regels:
            continue
        totaal = sum(r.get("bytes", 0) for r in regels)
        print(f"{kop} ({len(regels)}, {beeldpaden.leesbaar(totaal)})")
        for regel in regels:
            groep = f"[{regel['groep']}] " if len(set(r["groep"] for r in besluiten)) > 1 else ""
            print(f"  {groep}{regel['pad']}")
            if regel.get("reden"):
                print(f"      {regel['reden']}")
        print()
    tegen = [r for r in per["weiger"] if r["reden"].startswith("IN GEBRUIK")]
    doen = per["verplaats"] + per["weg"]
    woord = "bestand" if len(doen) == 1 else "bestanden"
    print(f"Totaal: {len(doen)} {woord}, {beeldpaden.leesbaar(sum(r.get('bytes', 0) for r in doen))}"
          f"   overgeslagen {len(per['sla over'])}   geweigerd {len(per['weiger'])}")
    return tegen, doen


def verplaats(doen):
    doel_wortel = WORTEL / ARCHIEF
    boek = doel_wortel / BOEKHOUDING
    bestaand = json.loads(boek.read_text(encoding="utf-8")) if boek.exists() else {
        "gemaakt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "wortel": WORTEL.as_posix(), "groepen": {}}

    for regel in doen:
        bron = WORTEL / regel["pad"]
        doel = doel_wortel / regel["pad"]
        doel.parent.mkdir(parents=True, exist_ok=True)
        if doel.exists():
            print(f"  overgeslagen, staat al in het archief: {regel['pad']}")
            continue
        vinger = None if bron.is_dir() else hash_van(bron)
        shutil.move(str(bron), str(doel))
        bestaand["groepen"].setdefault(regel["groep"], []).append({
            "van": regel["pad"], "naar": (Path(ARCHIEF) / regel["pad"]).as_posix(),
            "bytes": regel["bytes"], "sha256": vinger,
            "op": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        print(f"  {regel['pad']}  ->  {ARCHIEF}/{regel['pad']}")

    boek.parent.mkdir(parents=True, exist_ok=True)
    boek.write_text(json.dumps(bestaand, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nBoekhouding: {ARCHIEF}/{BOEKHOUDING}")
    print(f"Terugzetten: python _werk/opruimen-beelden.py --terug")


def terug(groep):
    boek = WORTEL / ARCHIEF / BOEKHOUDING
    if not boek.exists():
        raise SystemExit(f"Geen boekhouding in {ARCHIEF}/{BOEKHOUDING}; er is niets te herstellen.")
    data = json.loads(boek.read_text(encoding="utf-8"))
    terugezet, over, mis = 0, {}, []
    for naam, regels in data.get("groepen", {}).items():
        if groep and naam != groep:
            over[naam] = regels
            continue
        for regel in regels:
            bron = WORTEL / regel["naar"]
            doel = WORTEL / regel["van"]
            if not bron.exists():
                mis.append(f"{regel['naar']} staat niet meer in het archief")
                over.setdefault(naam, []).append(regel)
                continue
            if doel.exists():
                mis.append(f"{regel['van']} staat er al; niet overschreven")
                over.setdefault(naam, []).append(regel)
                continue
            if regel.get("sha256") and bron.is_file() and hash_van(bron) != regel["sha256"]:
                mis.append(f"{regel['naar']} is onderweg veranderd; niet teruggezet")
                over.setdefault(naam, []).append(regel)
                continue
            doel.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(bron), str(doel))
            print(f"  {regel['naar']}  ->  {regel['van']}")
            terugezet += 1
    data["groepen"] = over
    boek.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{terugezet} teruggezet" + (f", {len(mis)} niet:" if mis else "."))
    for regel in mis:
        print("  " + regel)
    return 1 if mis else 0


def weg(doen):
    bewijs = WORTEL / BEWIJSSTUK
    eerder = json.loads(bewijs.read_text(encoding="utf-8")) if bewijs.exists() else []
    for regel in doen:
        pad = WORTEL / regel["pad"]
        vinger = None if pad.is_dir() else hash_van(pad)
        if pad.is_dir():
            shutil.rmtree(pad)
        else:
            pad.unlink()
        eerder.append({"pad": regel["pad"], "groep": regel["groep"], "bytes": regel["bytes"],
                       "sha256": vinger,
                       "op": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        print(f"  weg: {regel['pad']}")
    bewijs.write_text(json.dumps(eerder, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nBewijsstuk: {BEWIJSSTUK} ({len(eerder)} regels). Dit is niet terug te halen.")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--lijst", help="bestand met paden: een per regel, of json, of - voor stdin")
    p.add_argument("--droog", action="store_true", help="alleen tonen, niets aanraken")
    p.add_argument("--terug", action="store_true", help="alles uit verplaatst.json terugzetten")
    p.add_argument("--weg", action="store_true", help="echt verwijderen (alleen wat git niet kent)")
    p.add_argument("--ja", action="store_true", help="bevestiging die --weg nodig heeft")
    p.add_argument("--getrackt-toegestaan", action="store_true",
                   help="ook bestanden verwijderen die git volgt; alleen samen met --weg --ja")
    p.add_argument("--mappen", action="store_true", help="hele mappen toestaan, zoals _prof-*")
    p.add_argument("--groep", help="naam voor deze groep in verplaatst.json, of bij --terug: alleen deze")
    p.add_argument("--ook-bronmateriaal", action="store_true",
                   help="bronmateriaal toch meenemen in plaats van overslaan")
    opties = p.parse_args()

    if opties.getrackt_toegestaan and not (opties.weg and (opties.ja or opties.droog)):
        p.error("--getrackt-toegestaan werkt alleen samen met --weg --ja (of --weg --droog)")
    if opties.terug:
        return terug(opties.groep)
    if not opties.lijst:
        p.error("geef --lijst <bestand>, of --terug")

    groepen = lees_lijst(opties.lijst)
    if opties.groep and len(groepen) == 1:
        groepen = {opties.groep: next(iter(groepen.values()))}

    besluiten, _fouten = beoordeel(groepen, opties)
    tegen, doen = toon(besluiten, opties)

    if tegen:
        print(f"\nGESTOPT. {len(tegen)} pad(en) uit de lijst zijn in gebruik op de site of in de"
              " bouwbron. Er is niets aangeraakt. Haal ze uit de lijst, of laat zien waarom het"
              " bewijs hierboven niet klopt.")
        return 2
    if opties.droog:
        print("\nDroge run: er is niets aangeraakt.")
        return 0
    if not doen:
        print("\nNiets te doen.")
        return 0
    if opties.weg:
        if not opties.ja:
            print("\n--weg verwijdert echt en git kan dit niet terughalen. Voeg --ja toe.")
            return 2
        weg(doen)
    else:
        verplaats(doen)
    return 0


if __name__ == "__main__":
    sys.exit(main())
