"""De twee extra secties van /diensten/verhuislift/ (testlijn test/diensten-paginas). Bouwt: dereus-3e.

Alleen dereus-3e bewerkt dit bestand; elke dienstpagina heeft een eigen bestand, zodat de vier sessies die de
secties bouwen elkaars regels niet raken. dienstpaginas.py zet SECTIES tussen het paneel van de dienst en de reviews,
in deze volgorde. Een regel is (blok, opties), net als in dienstpaginas._blokken(). Hooguit twee regels.

Patroon eerst laten vastleggen in _werk/dienstsecties-register.md (bijgehouden door dereus-37), dan pas bouwen.
Kopij: de pagina leest website/content/diensten.md; een blok met eigen kopij neemt {"kopij": None, "kopij_van":
(document, blok-id)} en leest die zelf via ctx.kopij_van(document).blok(blok-id), zoals blok actielijn.
"""
SECTIES = [
    # 9: wat u vooraf meldt, drie tegels met klei-iconen (section-library/sustainability-tree-band)
    ("meldtegels", {"kopij": None, "kopij_van": ("dienstsecties-verhuislift", "vooraf-melden")}),
    # 10: plek op straat en de vergunning, met een verhuizer die boven de kaart uitsteekt (section-library/pay-after-stock-figure)
    ("staankaart", {"kopij": None, "kopij_van": ("dienstsecties-verhuislift", "ruimte-op-straat")}),
]
