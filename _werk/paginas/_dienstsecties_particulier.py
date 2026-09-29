"""De twee extra secties van /diensten/particuliere-verhuizingen/ (testlijn test/diensten-paginas). Bouwt: dereus-28.

Alleen dereus-28 bewerkt dit bestand; elke dienstpagina heeft een eigen bestand, zodat de vier sessies die de
secties bouwen elkaars regels niet raken. dienstpaginas.py zet SECTIES tussen het paneel van de dienst en de reviews,
in deze volgorde. Een regel is (blok, opties), net als in dienstpaginas._blokken(). Hooguit twee regels.

Patroon eerst laten vastleggen in _werk/dienstsecties-register.md (bijgehouden door dereus-37), dan pas bouwen.
Kopij: de pagina leest website/content/diensten.md; een blok met eigen kopij neemt {"kopij": None, "kopij_van":
(document, blok-id)} en leest die zelf via ctx.kopij_van(document).blok(blok-id), zoals blok actielijn.
"""
SECTIES = [
    # 1 in het register: nieuw patroon policy-card-folder-seal (/section), de verzekering als poliskaart op een map
    ("polis", {"kopij": None}),
    # 2 in het register: vacancy-detail-card (Solar Green), de voorbereiding van /werkwijze/ als kaart met drie kolommen
    ("voorbereidkaart", {"kopij": None, "kopij_van": ("werkwijze", "voorbereiding")}),
]
