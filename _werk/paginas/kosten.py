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
    # de pagina in lagen: platen met dikte, de trap op de Diepblauwe band; opbouw-balie is de gele band van #opbouw
    # (tot 29-09-2026 stond hier "opbouw-3d", voor de gele schijven hieronder)
    extra_css=("kosten-diepte", "opbouw-balie"),
    blokken=[
        ("kop", {}),
        ("antwoord", {"chips": CHIPS, "beeld": ("/img/verhuisdozen-uit.webp", 562, 522)}),
        # de verhuizers achter de prijsbalie op een gele band (29-09-2026, ontwerp 05 uit
        # _ontwerpen/prijsopbouw-referentie-varianten-2.html; css/blok/opbouw-balie.css)
        ("opbouw", {"stijl": "balie"}),
        # tot 29-09-2026: 3D-voorwerpen op gele schijven (css/blok/opbouw-3d.css, dan "opbouw-3d" in extra_css) en
        # all-in en regie als fotoduo (onderaan css/blok/kosten-diepte.css):
        # ("opbouw", {"voorwerpen": True, "duo": "foto"}),
        ("treden", {"kopij_id": "verhuizing", "figuren": True}),   # verhuizers op trede 1 en 2, beeldmerk op trede 3
        # lijst met wisselende foto (29-09-2026); zonder "stijl" komen de vier platen met klei-iconen terug
        ("extradiensten", {"kopij_ids": EXTRA, "stijl": "lijst"}),
        ("annuleren", {}),
        ("vragen", {"kopij_id": "vragen", "stijl": "kaart"}),   # de blauwe kaart met de collega, zoals op /contact/ (29-09-2026)
        # tot 29-09-2026: ("vragen", {"kopij_id": "vragen", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),
        # de twee-dozen-verhuizer staat hier al op de treden, dus in de offertekaart een andere uitsnede
        ("offertepil", {"variant": "los", "beeld": ("/img/verhuizer-doos-zijgreep-uit.webp", 489, 1200)}),
    ],
)
