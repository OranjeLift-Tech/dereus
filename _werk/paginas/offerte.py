"""/offerte/: de kop, het offerteformulier (dereus-b4) en wat er na de aanvraag gebeurt."""
from kit import Pagina

PAGINA = Pagina(
    pad="/offerte/",
    kopij="offerte",
    header="transparant",
    body_klasse="p-offerte",
    # extra_css=("offerte-diepte",) is weg sinds 28-09-2026: dat bestand stijlde alleen nog stappen-na-aanvraag
    # en .p-offerte; het bestand zelf blijft staan. stappen-na-aanvraag laadt het nu zelf (AFHANKELIJK).
    extra_css=("logomotief",),                # het logo in de zijmarge in plaats van de randmotieven (Tugche, 28-09-2026)
    blokken=[
        ("kop", {}),
        # Sinds 28-09-2026 de opmaak van het formulier op de home: "make this the default styling for this form
        # in all pages". Dus dezelfde uitsnede als aanvraag.py, in plaats van het beeldmerk (merk=True): dat is
        # het negatieve logo, gemaakt voor het Diepblauwe paneel dat hier nu weg is.
        ("formulier", {"variant": "offerte", "beeld": "/img/verhuizer-doos-zijgreep-uit.webp"}),
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # de opzet van het offerteblok van referentie B, zoals /contact/ (zie _paneel in formulier.py): de lachende
        # verhuizer (uit img/over-verhuizer.webp) steekt boven de kaart uit, het blauwe paneel valt over zijn onderlichaam
        # ("formulier", {"variant": "offerte", "figuur": ("/img/offerte-figuur-uit.webp", 435, 752)}),
        # Sinds 28-09-2026 dezelfde Diepblauwe band met foto als "Na uw bericht" op /contact/ ("5. What happens
        # next: A: Navy band with photo"), als plaat in een witte sectie: deze pagina eindigt op de footer en
        # houdt zo een lichte band ervoor. Hiervoor stond hier ("stappen-na-aanvraag", {"kopij_id": "na-aanvraag"});
        # dat blok bestaat nog. De Google-pil gaat mee.
        # onder_beeld (28-09-2026): WhatsApp en de pil stonden "very off place"; nu een knoppenrij onder de foto.
        ("na-bericht", {"kopij_id": "na-aanvraag", "paneel": True, "grond": "wit", "google": True, "knoppen": None,
                        "onder_beeld": True}),
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # Zo gaat het verder op de Koningsblauwe band; de opmaak in css/blok/offerte-diepte.css komt mee
        # ("stappen-na-aanvraag", {"kopij_id": "na-aanvraag"}),
    ],
)
