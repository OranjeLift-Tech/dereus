"""Sjabloon plaats: /werkgebied/<plaats>/. Allemaal concept tot config.PUBLICEER ze aanzet.

Een plaats erbij = één kopijbestand website/content/plaatsen/<slug>.md. Er hoeft hier niets bij.
De blokken volgen de ##-blokken van het kopijbestand (zie BLOK). In de kop van het bestand mag staan:
plaats: (de naam zoals hij in de offertepil komt, anders afgeleid van de slug) en richting: van of naar
(welk veld van de offertepil de plaatsnaam krijgt; standaard naar).
De feiten per plaats komen uit het onderzoek van dereus-e7; dit sjabloon verzint niets.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "blokken"))   # voor _b4

import _b4                                   # noqa: E402
import kopij as _kopij                       # noqa: E402
from kit import Pagina                       # noqa: E402

BLOK = {"verhuizen-in": "watwijdoen", "lokaal": "feitenkaart", "diensten": "verwant", "kaart": "plaatskaart", "vragen": "vragen"}


def _pagina(slug, kopijnaam):
    doc = _kopij.document(kopijnaam)
    naam = _b4.naam_van(doc, slug, "plaats")
    richting = "van" if (doc.h1.veld("richting") if doc.h1 else "") == "van" else "naar"
    blokken = [("kop", {"knop": True})]
    grond = "wit"
    for b in doc.blokken:
        if b.niveau == 1 or b.id == "offertepil":
            continue
        if b.id not in BLOK:
            raise _kopij.BouwFout(f"{doc.pad.name}: blok #{b.id} kent het sjabloon plaats niet (wel: {', '.join(BLOK)})")
        opties = {"kopij_id": b.id}
        if BLOK[b.id] != "vragen":
            opties["grond"] = grond
            grond = "mist" if grond == "wit" else "wit"
        if BLOK[b.id] == "verwant":
            opties["kies"] = "alle"
        if BLOK[b.id] == "plaatskaart":
            opties["slug"] = slug
        blokken.append((BLOK[b.id], opties))
    blokken.append(("offertepil", {"variant": "los", richting: naam}))
    return Pagina(pad=_b4.PLAATS_PAD.format(slug), kopij=kopijnaam, header="transparant", body_klasse="p-plaats", concept=True,
                  wacht_op="Bevestiging van het werkgebied door de klant (open vraag 1.3)", feiten=_b4.feiten_in(doc), blokken=blokken)


PAGINAS = [_pagina(slug, kopijnaam) for slug, kopijnaam in _b4.kopijbestanden("plaatsen")]
