"""/werkwijze/: kop, de drie stappen als trap van kaarten, de voorbereiding, de verhuisdag (de blauwe band met dakrand),
na de verhuizing, reviews, vragen over de werkwijze en de offertepil."""
from kit import Pagina

PAGINA = Pagina(
    pad="/werkwijze/",
    kopij="werkwijze",
    header="transparant",
    body_klasse="p-werkwijze",
    # "reviews-ster" (de 3D-ster op de uitgelichte review) hoort bij het reviewblok "reviews"; zet hem terug
    # als dat blok hieronder weer aan gaat.
    extra_css=("logomotief",),                # het logo in de zijmarge in plaats van de randmotieven (Tugche, 28-09-2026)
    blokken=[
        ("kop", {}),
        # De drie stappen als trap van drie kaarten met een medewerker erachter, boven een Goudgele band (29-09-2026:
        # de klant wilde drie stappen in plaats van vijf, in de opzet van het blok "Bel ons, videobel ons of kom
        # langs" van referentie B; css/blok/stappentrap.css).
        ("stappentrap", {"kopij_id": "stappen"}),
        # De stappen als kaarten met een verhuizer die er bovenuit komt: steps-four-green uit ../section-library,
        # optie A uit website/review/zowerkthet-bibliotheek-20260928/ (28-09-2026), aan door deze regel te
        # wisselen met de regel erboven. Werkt ook met drie stappen.
        # ("stapkaarten", {"kopij_id": "stappen"}),
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # de tijdlijn als trap (css/blok/tijdlijn.css)
        # ("tijdlijn", {"kopij_id": "stappen"}),
        ("lijstplaat", {"kopij_id": "voorbereiding", "grond": "wit", "plaat": "geel"}),   # wit, zodat de dakrand erboven schoon aansluit; Goudgele plaat (29-09-2026): de pagina werd te blauw
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # de Goudgele plaat waar de verhuizer uit leunt (ontwerp 09 "Diepe plaat"), met de klei-iconen van hier
        # ("lijstplaat-geel", {"kopij_id": "voorbereiding", "grond": "wit"}),
        ("verhuisdag", {}),                         # blauw; "grond": "geel" (29-09-2026) teruggedraaid, stond de klant niet
        # Diepblauwe kaart op een schuine gele band, nummer 03 uit _ontwerpen/na-de-verhuizing-varianten.html, met de
        # 3D-telefoon en -ster op een gele schijf (Tugche, 28-09-2026; na de samenvoeging op 29-09-2026 teruggezet,
        # de klant koos dit blok)
        ("naband", {"kopij_id": "na-de-verhuizing"}),
        # mozaiek van vier tegels, versie 3 uit ronde 7 (23-09-2026), aan door deze regels te wisselen met de regel erboven:
        # ("namozaiek", {"kopij_id": "na-de-verhuizing",
        #                "foto": ("/img/dienst-nationaal-v2-groot.webp", 1440, 1080),
        #                "foto_srcset": "/img/dienst-nationaal-v2.webp 720w, /img/dienst-nationaal-v2-groot.webp 1440w"}),
        # het reviewblok van referentie B (scorepodium + rail) in onze stijl; weer aan op 29-09-2026, de klant
        # koos dit blok (Tugche)
        ("reviewrail", {"kopij_id": "reviews", "accent": "in de praktijk"}),
        # variant A zoals de home (28-09-2026), aan door deze regel te wisselen met de regel erboven (en
        # "reviews-ster" terug in extra_css):
        # ("reviews", {"sectie": "wit"}),
        # kopkaart: de sectiekop hoort hier in de belkaart, niet erboven. foto: de verhuizer
        # rechts in die kaart. Beide opties staan alleen op deze pagina aan.
        ("vragen", {"kopij_id": "vragen", "stijl": "kaart"}),   # de blauwe kaart met de collega, zoals op /contact/ (29-09-2026)
        # tot 29-09-2026: ("vragen", {"kopij_id": "vragen", "beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),
        # Tugche (origin/main 9dbb9a8, 28-09-2026), aan door deze regel te wisselen met de regel erboven:
        # Goudgele band met foto-afdruk (ontwerp 07 uit _ontwerpen/vragen-referentie-ronde1.html). Afdruk
        # woningontruiming: de bankscene staat al twee keer op deze pagina (verhuisdag).
        # ("vragen", {"kopij_id": "vragen", "stijl": "geel", "afdruk": "woningontruiming"}),
        ("offertepil", {"variant": "los"}),
    ],
)
