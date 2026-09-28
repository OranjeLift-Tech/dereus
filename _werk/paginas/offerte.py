"""/offerte/: de kop, het offerteformulier (dereus-b4) en wat er na de aanvraag gebeurt."""
from kit import Pagina

PAGINA = Pagina(
    pad="/offerte/",
    kopij="offerte",
    header="transparant",
    body_klasse="p-offerte",
    extra_css=("offerte-diepte",              # de grond onder het formulier en Zo gaat het verder
               "logomotief"),                 # het logo in de zijmarge in plaats van de randmotieven (28-09-2026)
    blokken=[
        ("kop", {}),
        # sinds 28-09-2026 de opzet van het offerteblok van referentie B, zoals /contact/ (zie _paneel in formulier.py):
        # de lachende verhuizer (uit img/over-verhuizer.webp) steekt boven de kaart uit, het blauwe paneel valt over
        # zijn onderlichaam; bewust een ander gezicht dan de man met de steekwagen bij Zo gaat het verder
        ("formulier", {"variant": "offerte", "figuur": ("/img/offerte-figuur-uit.webp", 435, 752)}),
        ("stappen-na-aanvraag", {"kopij_id": "na-aanvraag"}),
    ],
)
