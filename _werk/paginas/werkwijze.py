"""/werkwijze/: kop, de vijf stappen als trap, de voorbereiding op de Goudgele plaat, de verhuisdag (de ene blauwe band met
dakrand), na de verhuizing op de schuine gele band, reviews als rail, vragen op de Goudgele band en de offertepil.

Sinds 29-09-2026 de pagina van Tugche (origin/main 9dbb9a8, 28-09-2026), op verzoek: "revert changes to werkwijze and
contact to be the latest tugche changes". Haar blokken in haar volgorde; haar lijstplaat heet hier lijstplaat-geel,
omdat de samenvoeging van 28-09-2026 onze Koningsblauwe lijstplaat onder die naam liet staan. Onze versie van elke
sectie staat als commentaar onder de hare: terug door die twee te wisselen.

KLEI: de klei-iconen (img/clay/) in plaats van haar 3D-renders, zoals gekozen in de samenvoegreview van 28-09-2026
("with clay on 1, 2, 3 and 11"). False geeft haar renders terug in tijdlijn, lijstplaat-geel en naband."""
from kit import Pagina

KLEI = True

PAGINA = Pagina(
    pad="/werkwijze/",
    kopij="werkwijze",
    header="transparant",
    body_klasse="p-werkwijze",
    extra_css=("logomotief",),                # het logo in de zijmarge in plaats van de randmotieven (28-09-2026)
    # Onze had er ook "reviews-ster" bij, de 3D-ster op de uitgelichte review van het blok reviews.
    blokken=[
        ("kop", {}),
        # De tijdlijn als trap (css/blok/tijdlijn.css).
        ("tijdlijn", {"kopij_id": "stappen", "klei": KLEI}),
        # Onze: de vijf stappen als kaarten met een verhuizer die er bovenuit komt: steps-four-green uit
        # ../section-library, optie A uit website/review/zowerkthet-bibliotheek-20260928/ (28-09-2026).
        # ("stapkaarten", {"kopij_id": "stappen"}),
        # De Goudgele plaat waar de verhuizer uit leunt (ontwerp 09 "Diepe plaat").
        ("lijstplaat-geel", {"kopij_id": "voorbereiding", "grond": "wit", "klei": KLEI}),    # wit, zodat de dakrand erboven schoon aansluit
        # Onze: de Koningsblauwe plaat.
        # ("lijstplaat", {"kopij_id": "voorbereiding", "grond": "wit"}),
        ("verhuisdag", {}),
        # Diepblauwe kaart op een schuine gele band, nummer 03 uit _ontwerpen/na-de-verhuizing-varianten.html
        # (28-09-2026); verving het mozaiek (blok namozaiek, dat blijft bestaan)
        ("naband", {"kopij_id": "na-de-verhuizing", "klei": KLEI}),
        # Onze: mozaiek van vier tegels, versie 3 uit ronde 7 (23-09-2026); de foto is nationaal r4 versie 2
        # ("namozaiek", {"kopij_id": "na-de-verhuizing",
        #                "foto": ("/img/dienst-nationaal-v2-groot.webp", 1440, 1080),
        #                "foto_srcset": "/img/dienst-nationaal-v2.webp 720w, /img/dienst-nationaal-v2-groot.webp 1440w"}),
        # het reviewblok van referentie B (scorepodium + rail) in onze stijl (28-09-2026). Wit, tussen twee Mist-secties.
        ("reviewrail", {"kopij_id": "reviews", "accent": "in de praktijk"}),
        # Onze: variant A zoals de home (28-09-2026), met "reviews-ster" in extra_css hierboven.
        # ("reviews", {"sectie": "wit"}),
        # Goudgele band met foto-afdruk (ontwerp 07 uit _ontwerpen/vragen-referentie-ronde1.html, 28-09-2026), net als
        # /contact/. Afdruk woningontruiming: de bankscene staat al twee keer op deze pagina (verhuisdag).
        ("vragen", {"kopij_id": "vragen", "stijl": "geel", "afdruk": "woningontruiming"}),
        # Onze: kopkaart: de sectiekop hoort hier in de belkaart, niet erboven. foto: de verhuizer rechts in die
        # kaart. Hetzelfde blauwe paneel als op de home, /kosten/ en /contact/ (23-09-2026).
        # ("vragen", {"kopij_id": "vragen", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),
        # Zonder de verhuizer in de kopband, zoals bij Tugche (9dbb9a8). Die kwam er sitebreed bij na haar commit
        # (keuze van de gebruiker, 28-09-2026); op deze pagina op 29-09-2026 weer weg: "2. keep hers".
        ("offertepil", {"variant": "los", "beeld": None}),
        # Onze: met de verhuizer (FIGUUR in _werk/blokken/offertepil.py).
        # ("offertepil", {"variant": "los"}),
    ],
)
