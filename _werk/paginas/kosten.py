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
    extra_css=("kosten-diepte", "opbouw-3d"),             # de pagina in lagen: platen met dikte, de trap op de Diepblauwe band
    blokken=[
        ("kop", {}),
        ("antwoord", {"chips": CHIPS}),
        ("opbouw", {"voorwerpen": True}),                           # 3D-voorwerpen op gele schijven (css/blok/opbouw-3d.css)
        ("treden", {"kopij_id": "verhuizing", "figuren": True}),   # verhuizers op trede 1 en 2, beeldmerk op trede 3
        ("extradiensten", {"kopij_ids": EXTRA}),
        ("annuleren", {}),
        ("vragen", {"kopij_id": "vragen", "open": 1}),             # gesprek op de telefoon: de eerste vraag staat open
        ("offertepil", {"variant": "los"}),
    ],
)
