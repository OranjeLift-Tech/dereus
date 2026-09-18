"""Sjabloon land: /diensten/internationale-verhuizingen/<land>/. Allemaal concept tot config.PUBLICEER ze aanzet.

Een land erbij = één kopijbestand website/content/landen/<slug>.md. Er hoeft hier niets bij.
De blokken volgen de ##-blokken van het kopijbestand (zie BLOK). In de kop van het bestand mag staan:
land: (de naam, anders afgeleid van de slug). De feiten per land (afstand, route, papieren) komen uit het
onderzoek van dereus-e7; dit sjabloon verzint niets.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "blokken"))   # voor _b4

import _b4                                   # noqa: E402
import kopij as _kopij                       # noqa: E402
from kit import Pagina                       # noqa: E402

DIENST = "internationaal"
BLOK = {"wat": "watwijdoen", "hoe": "kortestappen", "reis": "feitenkaart", "tips": "checklist", "vragen": "vragen"}


def _pagina(slug, kopijnaam):
    doc = _kopij.document(kopijnaam)
    blokken = [("kop", {"icoon": DIENST, "knop": True, "dienst": DIENST})]
    grond = "wit"
    for b in doc.blokken:
        if b.niveau == 1 or b.id in ("offertepil", "andere-landen"):
            continue
        if b.id not in BLOK:
            raise _kopij.BouwFout(f"{doc.pad.name}: blok #{b.id} kent het sjabloon land niet (wel: {', '.join(BLOK)})")
        opties = {"kopij_id": b.id}
        if BLOK[b.id] != "vragen":
            opties["grond"] = grond
            grond = "mist" if grond == "wit" else "wit"
        if BLOK[b.id] == "watwijdoen":
            opties["dienst"] = DIENST
        blokken.append((BLOK[b.id], opties))
    if doc.heeft("andere-landen"):            # kop boven de andere landen; alleen landen die live staan krijgen een kaartje
        blokken.append(("plaatsenlijst", {"kopij_id": "andere-landen", "soort": "landen", "grond": "mist"}))
    blokken.append(("offertepil", {"variant": "los", "dienst": DIENST}))
    return Pagina(pad=_b4.LAND_PAD.format(slug), kopij=kopijnaam, header="transparant", body_klasse="p-land", concept=True,
                  wacht_op="Bevestiging van de landen door de klant (open vraag 5.1)", feiten=_b4.feiten_in(doc), blokken=blokken)


PAGINAS = [_pagina(slug, kopijnaam) for slug, kopijnaam in _b4.kopijbestanden("landen")]
