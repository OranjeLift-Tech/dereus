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
        ("antwoord", {"chips": CHIPS, "beeld": ("/img/verhuisdozen-uit.webp", 562, 522)}),
        ("opbouw", {"voorwerpen": True}),                           # 3D-voorwerpen op gele schijven (css/blok/opbouw-3d.css)
        ("treden", {"kopij_id": "verhuizing", "figuren": True}),   # verhuizers op trede 1 en 2, beeldmerk op trede 3
        ("extradiensten", {"kopij_ids": EXTRA}),
        ("annuleren", {}),
        ("vragen", {"kopij_id": "vragen", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),   # hetzelfde blauwe paneel als op de home, /werkwijze/ en /contact/ (23-09-2026)
        ("offertepil", {"variant": "los"}),
    ],
)
