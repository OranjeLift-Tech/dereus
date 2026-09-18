"""/kosten/: vraag vooraf. Kop, direct antwoord met ankerchips, prijsopbouw, traptreden, vier extra diensten,
annuleren, vragen over de prijs en de offertepil."""
from kit import Pagina

EXTRA = ["opslag", "verhuislift", "montage", "woningontruiming"]
CHIPS = ["opbouw", "verhuizing"] + EXTRA + ["annuleren", "vragen"]

PAGINA = Pagina(
    pad="/kosten/",
    kopij="kosten",
    header="transparant",
    body_klasse="p-kosten",
    blokken=[
        ("kop", {}),
        ("antwoord", {"chips": CHIPS}),
        ("opbouw", {}),
        ("treden", {"kopij_id": "verhuizing"}),
        ("extradiensten", {"kopij_ids": EXTRA}),
        ("annuleren", {}),
        ("vragen", {"kopij_id": "vragen"}),
        ("offertepil", {"variant": "los"}),
    ],
)
