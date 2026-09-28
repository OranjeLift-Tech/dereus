"""/over-ons/: kop met de offertepil over de onderrand (zoals Brocken en referentie A), het verhaal met de
verhuizers op twee platen en drie feitenkaarten (about-address-team, sinds 28-09-2026), de kernwaarden als
gedrag (Koningsblauw met dakrand: een uitgelichte waarde met de verhuizers die uit de foto stappen, de
overige als rijen ernaast), reviews, Den Haag met de kaart (Diepblauw met dakrand) en het grote offerteformulier
van de home (blok aanvraag, sinds 28-09-2026; daarvoor de offertekaart "Kennismaken?").

Feiten (config.FEITEN): OPRICHTINGSJAAR, EIGENAAR, TEAM, RECHTSVORM en KVK verschijnen onder het verhaal zodra
ze bekend zijn. Tot die tijd blijven ze weg. TEAM_BEELD leest het verhaal sinds 28-09-2026 niet meer.
"""
from kit import Pagina

PAGINA = Pagina(
    pad="/over-ons/",
    kopij="over-ons",
    header="transparant",
    body_klasse="p-over-ons",
    feiten=("OPRICHTINGSJAAR", "EIGENAAR", "TEAM", "RECHTSVORM", "KVK"),
    extra_css=("reviews-ster",),   # de 3D-ster op de uitgelichte review
    blokken=[
        ("kop", {}),
        ("offertepil", {"variant": "los", "over_kop": True, "kopij": None}),
        ("over-ons", {"kopij_id": "verhaal", "feiten": True, "motto": False}),
        ("kernwaarden", {"kopij_id": "zo-werken-wij", "foto": "particulier-v2", "compact": "krap"}),
        ("reviews", {}),
        ("werkgebied", {"kopij_id": "den-haag", "regels_van": ("home", "werkgebied"), "alineas": False}),   # keuze A (28-09-2026): de drie regels van de home
        # Sinds 28-09-2026 het grote formulier van de home, zoals home.py het aanroept. De gebruiker: "replace the small
        # form in /over-ons/ with the big one from homepage". Hiervoor stond hier ("offertepil", {"variant": "los",
        # "kopij_id": "contact"}), "Kennismaken?"; die kopij in over-ons.md blijft staan, ongebruikt.
        ("aanvraag", {"kopij": None}),
    ],
)
