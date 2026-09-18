"""Sjabloon dienstdetail: de losse dienstpagina's en de doelgroeppagina's. Allemaal concept tot config.PUBLICEER ze aanzet.

Een pagina erbij = één kopijbestand in website/content/ plus één regel in TABEL.
De blokken volgen de ##-blokken van het kopijbestand, in de volgorde van het bestand: het sjabloon kiest per
blok-id het bouwblok (zie BLOK). Vlak voor de offertepil komt altijd de rij met andere diensten.
Welke feiten een pagina gebruikt, leest het sjabloon uit de kopij ({NAAM}, als:, tenzij:, alleen-als:).
"""
import re

import config as cfg
import kopij as _kopij
from kit import Pagina

# pad, kopijbestand, dienst (merkicoon, ?dienst= en de voorkeuze in de offertepil), waar de pagina op wacht, en het feit
# dat bevestigd moet zijn voordat de pagina aan mag (None = geen voorwaarde). Aanzetten zonder dat feit is een bouwfout.
TABEL = [
    ("/diensten/particuliere-verhuizingen/", "diensten-particulier", "particulier", "Akkoord van de klant op de tekst", None),
    ("/diensten/zakelijke-verhuizingen/", "diensten-zakelijk", "zakelijk", "Zakelijk: avond, weekend en IT (open vraag 2.5)", None),
    ("/diensten/tijdelijke-opslag/", "diensten-opslag", "opslag", "Opslaglocatie, termijnen en verzekering (open vragen 1.6 en 2.4)", None),
    ("/diensten/internationale-verhuizingen/", "diensten-internationaal", "internationaal", "Landen (open vraag 5.1)", None),
    ("/diensten/studentenverhuizing/", "doelgroep-studenten", "particulier", "Bevestiging dat De Reus dit aanbiedt (open vraag 5.6)", "STUDENTEN_DIENST"),
    ("/diensten/seniorenverhuizing/", "doelgroep-senioren", "particulier", "Bevestiging dat De Reus dit aanbiedt (open vraag 5.6)", "SENIOREN_DIENST"),
    ("/diensten/spoedverhuizing/", "spoedverhuizing", "particulier", "Bevestiging dat De Reus dit aanbiedt (open vraag 5.6)", "SPOED_DIENST"),
]

# blok-id in de kopij -> bouwblok. Onbekende id's geven een bouwfout, zodat er nooit stil tekst wegvalt.
BLOK = {
    "wat": "watwijdoen", "keuze": "kaartenrij", "wanneer": "kaartenrij", "hoe": "kortestappen",
    "tips": "checklist", "waarom": "checklist", "vragen": "vragen",
    "landen": "plaatsenlijst",                  # bij internationaal: de landen waarvan de pagina live staat
}
_FEIT = re.compile(r"\{([A-Z][A-Z0-9_]+)\}|^(?:als|tenzij|alleen-als):\s*([A-Z][A-Z0-9_]+)", re.M)


def _feiten(doc):
    """De feiten uit config.FEITEN die in dit kopijbestand voorkomen, in volgorde van voorkomen."""
    tekst = doc.pad.read_text(encoding="utf-8")
    uit = []
    for a, b in _FEIT.findall(tekst):
        naam = a or b
        if naam in getattr(cfg, "FEITEN", {}) and naam not in uit:
            uit.append(naam)
    return tuple(uit)


def _pagina(pad, kopijnaam, dienst, wacht_op, vereist):
    if vereist and getattr(cfg, "PUBLICEER", {}).get(pad) and not getattr(cfg, "FEITEN", {}).get(vereist):
        raise _kopij.BouwFout(f"{pad} staat aan in config.PUBLICEER, maar het feit {vereist} is nog niet bevestigd "
                              f"(config.FEITEN). Zet eerst dat feit, of zet de pagina weer uit.")
    doc = _kopij.document(kopijnaam)
    kies = [s.strip() for s in (doc.h1.veld("verwant") if doc.h1 else "").split(",") if s.strip()]
    blokken = [("kop", {"icoon": dienst, "knop": True, "dienst": dienst})]
    grond = "wit"
    for b in doc.blokken:
        if b.niveau == 1 or b.id in ("offertepil", "reviews"):
            continue
        if b.id not in BLOK:
            raise _kopij.BouwFout(f"{doc.pad.name}: blok #{b.id} kent het sjabloon dienstdetail niet (wel: {', '.join(BLOK)})")
        opties = {"kopij_id": b.id}
        if BLOK[b.id] != "vragen":                  # vragen bepaalt zijn eigen ondergrond
            opties["grond"] = grond
            grond = "mist" if grond == "wit" else "wit"
        if BLOK[b.id] == "watwijdoen":
            opties["dienst"] = dienst
        if BLOK[b.id] == "plaatsenlijst":
            opties["soort"] = "landen"
        blokken.append((BLOK[b.id], opties))
    blokken.append(("verwant", {"kopij": None, "zonder": dienst if not kies else None, "kies": kies or None, "grond": "mist"}))
    blokken.append(("offertepil", {"variant": "los", "dienst": dienst}))
    return Pagina(pad=pad, kopij=kopijnaam, header="transparant", body_klasse="p-dienstdetail", concept=True,
                  wacht_op=wacht_op, feiten=_feiten(doc), blokken=blokken)


PAGINAS = [_pagina(*rij) for rij in TABEL]
