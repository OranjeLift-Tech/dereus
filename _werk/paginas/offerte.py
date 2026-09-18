"""/offerte/: de kop, het offerteformulier (dereus-b4) en wat er na de aanvraag gebeurt."""
from kit import Pagina

PAGINA = Pagina(
    pad="/offerte/",
    kopij="offerte",
    header="transparant",
    body_klasse="p-offerte",
    blokken=[
        ("kop", {}),
        ("formulier", {"variant": "offerte"}),
        ("stappen-na-aanvraag", {"kopij_id": "na-aanvraag"}),
    ],
)
