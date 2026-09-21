"""/offerte/: de kop, het offerteformulier (dereus-b4) en wat er na de aanvraag gebeurt."""
from kit import Pagina

PAGINA = Pagina(
    pad="/offerte/",
    kopij="offerte",
    header="transparant",
    body_klasse="p-offerte",
    extra_css=("offerte-diepte",),            # de pagina in lagen: plaat, paneel ervoor, verzonken velden
    blokken=[
        ("kop", {}),
        ("formulier", {"variant": "offerte", "merk": True}),   # beeldmerk onder de belknop, loopt mee in de zijkolom
        ("stappen-na-aanvraag", {"kopij_id": "na-aanvraag"}),
    ],
)
