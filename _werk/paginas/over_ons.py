"""/over-ons/: kop met de offertepil over de onderrand (zoals Brocken en De Kievit), het verhaal met het
huisvenster en de bevestigde feiten, de kernwaarden als gedrag (Koningsblauw met dakrand), reviews,
Den Haag met de kaart (Diepblauw met dakrand) en de contactband (licht, boven de footer).

Feiten (config.FEITEN): OPRICHTINGSJAAR, EIGENAAR, TEAM, RECHTSVORM en KVK verschijnen onder het verhaal zodra
ze bekend zijn; TEAM_BEELD vervangt het beeldmerk door een echte teamfoto. Tot die tijd blijven ze weg.
"""
from kit import Pagina

PAGINA = Pagina(
    pad="/over-ons/",
    kopij="over-ons",
    header="transparant",
    body_klasse="p-over-ons",
    feiten=("OPRICHTINGSJAAR", "EIGENAAR", "TEAM", "RECHTSVORM", "KVK", "TEAM_BEELD"),
    extra_css=("uitsnede",),                  # de gedeelde uitsnede-plaat van "Zo werken wij" en "Kennismaken?"
    blokken=[
        ("kop", {}),
        ("offertepil", {"variant": "los", "over_kop": True, "kopij": None}),
        ("over-ons", {"kopij_id": "verhaal", "feiten": True, "motto": False}),
        ("kernwaarden", {"kopij_id": "zo-werken-wij", "beeld": ("/img/dienst-particulier-uit.webp", 1080, 810, 215, 273, 673, 502), "compact": "krap"}),
        ("reviews", {}),
        ("werkgebied", {"kopij_id": "den-haag"}),
        ("contactband", {"kopij_id": "contact", "beeld": ("/img/verhuizer-twee-dozen-uit.webp", 407, 1200, 0, 0, 407, 1200), "compact": "krap"}),
    ],
)
