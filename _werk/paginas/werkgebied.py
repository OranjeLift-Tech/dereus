"""/werkgebied/: de hub boven de plaatspagina's. Concept tot config.PUBLICEER["/werkgebied/"] aan staat.

Kopij: werkgebied.md. De blokken volgen het bestand: #plaatsen wordt de lijst met plaatsen die al live staan (het blok
vervalt als er geen enkele aan staat), de overige tekstblokken worden een tekstblok met het passende merkicoon.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "blokken"))   # voor _b4

import _b4                                   # noqa: E402
import kopij as _kopij                       # noqa: E402
from kit import Pagina                       # noqa: E402

ICOON = {"den-haag": "particulier", "nederland": "nationaal", "internationaal": "internationaal"}


def _blokken(doc):
    blokken = [("kop", {"knop": True})]
    grond = "wit"
    for b in doc.blokken:
        if b.niveau == 1 or b.id == "offertepil":
            continue
        if b.id == "vragen":
            blokken.append(("vragen", {"kopij_id": "vragen"}))
            continue
        naam = "plaatsenlijst" if b.id == "plaatsen" else "watwijdoen"
        opties = {"kopij_id": b.id, "grond": grond}
        if b.id in ICOON:
            opties["dienst"] = ICOON[b.id]
        blokken.append((naam, opties))
        grond = "mist" if grond == "wit" else "wit"
    blokken.append(("offertepil", {"variant": "los"}))
    return blokken


_doc = _kopij.document("werkgebied")
PAGINAS = [Pagina(pad="/werkgebied/", kopij="werkgebied", header="transparant", body_klasse="p-werkgebied", concept=True,
                  wacht_op="Bevestiging van het werkgebied door de klant (open vraag 1.3)", feiten=_b4.feiten_in(_doc),
                  blokken=_blokken(_doc))] if _doc.blokken else []
