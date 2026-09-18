"""Hulpfuncties van dereus-b4 voor de sjablonen plaats, land en werkgebied (geen blok: de naam begint met _).

Een plaats of land erbij is één kopijbestand: website/content/plaatsen/<slug>.md of landen/<slug>.md.
De onderzoeksbestanden van dereus-e7 (<slug>-feiten.md) en bestanden die met _ beginnen tellen niet mee.
"""
import re

import config as cfg
import kopij as _kopij

# De diensten met een eigen pagina. Zolang die pagina uit staat, blijft de link het anker op /diensten/.
DIENST_PAGINA = {
    "particulier": "/diensten/particuliere-verhuizingen/",
    "zakelijk": "/diensten/zakelijke-verhuizingen/",
    "opslag": "/diensten/tijdelijke-opslag/",
    "internationaal": "/diensten/internationale-verhuizingen/",
}
# Doelgroeppagina's: geen menu-item. Staan ze live, dan linkt het paneel Particulier op /diensten/ ernaar.
DOELGROEPEN = [("/diensten/studentenverhuizing/", "doelgroep-studenten"), ("/diensten/seniorenverhuizing/", "doelgroep-senioren"),
               ("/diensten/spoedverhuizing/", "spoedverhuizing")]
PLAATS_PAD = "/werkgebied/{}/"
LAND_PAD = "/diensten/internationale-verhuizingen/{}/"
_FEIT = re.compile(r"\{([A-Z][A-Z0-9_]+)\}|^(?:als|tenzij|alleen-als):\s*([A-Z][A-Z0-9_]+)", re.M)


def dienst_href(ctx, sleutel):
    """De eigen pagina van een dienst als die live is, anders het anker op /diensten/."""
    anker = f"/diensten/#{sleutel}"
    return ctx.href(DIENST_PAGINA[sleutel], anker) if sleutel in DIENST_PAGINA else anker


def schakel(ctx, href):
    """Een link uit de kopij naar /diensten/#<dienst> wordt de eigen pagina zodra die live is."""
    if href.startswith("/diensten/#"):
        return dienst_href(ctx, href.split("#", 1)[1])
    return href


def kopijbestanden(map_naam):
    """[(slug, kopijnaam)] voor elk kopijbestand in website/content/<map_naam>/, op alfabet."""
    map_ = _kopij.MAP / map_naam
    if not map_.exists():
        return []
    return [(p.stem, f"{map_naam}/{p.stem}") for p in sorted(map_.glob("*.md"))
            if not p.stem.endswith("-feiten") and not p.stem.startswith("_")]


def naam_van(doc, slug, veld):
    """De naam van de plaats of het land: het veld in de kop (plaats: of land:), anders afgeleid van de slug."""
    gegeven = doc.h1.veld(veld) if doc.h1 else ""
    return gegeven or " ".join(w.capitalize() for w in slug.split("-"))


def feiten_in(doc):
    """De namen uit config.FEITEN die in dit kopijbestand voorkomen ({NAAM}, als:, tenzij:, alleen-als:)."""
    if not doc.pad.exists():
        return ()
    uit = []
    for a, b in _FEIT.findall(doc.pad.read_text(encoding="utf-8")):
        naam = a or b
        if naam in getattr(cfg, "FEITEN", {}) and naam not in uit:
            uit.append(naam)
    return tuple(uit)


def plaatsen():
    """[(slug, naam, pad)] van alle plaatspagina's waarvoor kopij bestaat."""
    uit = []
    for slug, kopijnaam in kopijbestanden("plaatsen"):
        uit.append((slug, naam_van(_kopij.document(kopijnaam), slug, "plaats"), PLAATS_PAD.format(slug)))
    return uit


def landen():
    uit = []
    for slug, kopijnaam in kopijbestanden("landen"):
        uit.append((slug, naam_van(_kopij.document(kopijnaam), slug, "land"), LAND_PAD.format(slug)))
    return uit
