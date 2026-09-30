"""/ (home): hero met offertepil, diensten, waarom, werkwijze, reviews, over ons, werkgebied en vragen.

Banden (review dereus-70, D3): Mist, Wit, Koningsblauw met dakrand (werkwijze), Mist, Wit,
Diepblauw met dakrand (werkgebied), Mist. Nooit twee donkere banden naast elkaar, en licht voor de footer.
De beeldblokken, cijfers, aanvraag en contact uit main zijn opgenomen in de gedeelde bouwstraat.
"""
import config as cfg
import kit
from kit import Pagina


def _preload():
    """Het teambeeld is de LCP: preload de webp in de juiste maat (zelfde sizes als het blok hero)."""
    if not getattr(cfg, "HERO_TEAM", None):
        return None
    r = kit.responsief(cfg.HERO_TEAM)
    return {"href": r["webp"], "imagesrcset": r["srcset"], "imagesizes": kit.HERO_SIZES, "type": "image/webp"}

PAGINA = Pagina(
    pad="/",
    kopij="home",
    header="transparant",
    body_klasse="p-home",
    preload_beeld=_preload(),
    # "reviews-ster" (de gouden 3D-ster op de uitgelichte review) hoort bij het reviewblok "reviews"; zet hem terug
    # als dat blok hieronder weer aan gaat.
    blokken=[
        ("hero", {"kopij_id": "offerte"}),
        ("diensten", {}),
        # De cijfers als schuine actielijn (28-09-2026): "make this section into an action line, like a stripe that
        # is slanted and has icons by each line". Zelfde blok als #vertrouwen op /contact/. Het oude blok cijfers.py
        # blijft bestaan. Hier zonder "sectie": de cijferband telde niet mee in de motieftellers van style.css.
        # Sinds 29-09-2026 voor waarom: "in homepage - put the actionline a section higher". De grijze helft erachter
        # staat in actielijn.css (.sectie--mist + .b-actielijn), het gat erboven in diensten.css en eronder in waarom.css.
        ("actielijn", {"kopij_id": "cijfers"}),
        ("waarom", {}),
        # Zo werkt het: de stappen als kaarten met een verhuizer (steps-four-green uit ../section-library), zoals op
        # /werkwijze/, op de Koningsblauwe band uit de regel hierboven. Gekozen op 28-09-2026: "Home "Zo werkt het",
        # routeband or option A (28-09-2026): A on Koningsblauw" (website/review/zowerkthet-home-vergelijk-20260928/).
        # Daarvoor de routeband (intro-route-band); dat blok en zijn CSS blijven staan.
        ("stapkaarten", {"kopij_id": "werkwijze", "grond": "blauw"}),
        # het reviewblok van /werkwijze/ (scorepodium + rail) sinds 29-09-2026, opnieuw gezet op 30-09-2026 na afb212f
        # (Tugche: "home sayfasindaki Wat klanten over ons zeggen ... burasi yine eski ... duruyo").
        ("reviewrail", {"kopij_id": "reviews", "sectie": "mist", "accent": "over ons zeggen"}),
        # variant A (trio achter het donkere scorepaneel), aan door deze regel te wisselen met de regel erboven (en
        # "reviews-ster" terug in extra_css):
        # ("reviews", {}),
        # feiten: False sinds 28-09-2026, toen het KvK-nummer in config.FEITEN kwam: "Sterk waar het zwaar is" blijft zoals
        # goedgekeurd, zonder feitenrijen. Het KvK-nummer staat in de footer, op /contact/ en in de JSON-LD.
        ("over-ons", {"kopij_van": ("over-ons", "verhaal"), "feiten": False, "motto": False}),   # een kopie van /over-ons/ #verhaal
        # voorwerpen="echt": echte voorwerpen in de gele tegels (Tugche, 8971f9e), zonder de klei-iconen; opnieuw gezet
        # op 30-09-2026 na afb212f
        ("werkgebied", {"voorwerpen": "echt"}),
        # kopkaart: de sectiekop hoort in de belkaart. De headset verhuist mee naar de
        # rechterbovenhoek van die kaart ("hoek"); het gat dat "headset-huis" vulde bestaat
        # niet meer zodra de kop in de kaart staat.
        # Sinds 29-09-2026 de blauwe kaart met de collega, zoals op /contact/, /kosten/ en /werkwijze/ (Tugche: alle
        # vragenblokken zo); opnieuw gezet op 30-09-2026 na afb212f.
        ("vragen", {"stijl": "kaart"}),
        # Tot 29-09-2026 het blauwe paneel, aan door deze regel te wisselen met de regel erboven:
        # ("vragen", {"beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),
        ("aanvraag", {"kopij": None}),
        # homecontact ("Wilt u iets bespreken over uw verhuizing?") is eraf sinds 28-09-2026:
        # "remove from homepage as it sits right below the other form". Blok en CSS blijven bestaan.
    ],
)

# Klei-iconen op de naden, alleen vanaf 1100 px (blok naadiconen). De gebruiker plaatste ze zelf met de artifact
# placer op 1440: eerst op 28-09-2026, opnieuw op 29-09-2026 (export via dereus-2f, nu met een eigen dekking per icoon).
# Per blok: het id van de sectie en per icoon (naam, kant, x, y, dekking): x in px vanaf die kant van de pagina, y vanaf
# de bovenkant van de sectie, beide omgerekend uit de procenten van de export van 29-09-2026 op 1440, gemeten op de bouw
# van 13:23 (secties diensten 1258, waarom 904, werkwijze 832, reviews 1063, over-ons 941, werkgebied 1074 hoog).
NAADICONEN = {
    "diensten": ("diensten", [("particulier", "rechts", 77, 60, .52), ("dozen", "links", 78, 65, .48)]),
    # De ster boven #waarom en de vrachtwagen in #werkwijze gingen er eerder op 29-09-2026 af ("Dit mag u van ons
    # verwachten - remove the star clay artifact near this section.", "Zo werkt het - remove the truck clay icon near
    # the section"). In zijn export van diezelfde dag staan daar deze vier.
    # Zesde veld 1160: de verhuislift staat er pas vanaf 1160 px. Van 1100 tot 1140 lag hij op het eind van de intro
    # ("...Daarom zeggen"); de gebruiker op 29-09-2026: "12. Waarom verhuislift icon: hide below 1160".
    "waarom": ("waarom", [("verhuislift", "rechts", 109, 64, .53, 1160), ("vakman", "links", 76, 68, .48)]),
    "stapkaarten": ("werkwijze", [("woningontruiming", "links", 105, -30, .5), ("zakelijk", "rechts", 180, -35, .47)]),
    # sleutel reviewrail: zo heet het blok nu, de sectie blijft #reviews
    "reviewrail": ("reviews", [("telefoon", "links", 92, -84, .46)]),
    "over-ons": ("over-ons", [("verhuislift", "links", 66, -51, .47)]),
    "werkgebied": ("werkgebied", [("internationaal", "links", 82, -19, .52)]),
    # Het klembord hangt sinds 28-09-2026 aan de formulierkaart, op de rechterbovenhoek, met een hover:
    # "Vertel ons over uw verhuizing in homepage - make the artifact of the list next to the section be part of the section and have a hover effect."
    # Derde veld: de klasse van het element waar het in hangt; x en y vanaf die hoek (negatief is erbuiten).
    # De export van 29-09-2026 noemt nog een los klembord in #aanvraag (rechts 46, y 21, dekking 1): precies de plek van
    # 28-09-2026, die als concept in zijn placer bleef staan. Geen tweede klembord dus; het blijft alleen op de kaart.
    "aanvraag": ("aanvraag", [("klembord", "hoek", -14, -52)], "b-formulier__kaart"),
}
PAGINA.blokken = [("naadiconen", {"kopij": None, "blok": naam, "opties": opties, "plek": NAADICONEN[naam]})
                  if naam in NAADICONEN else (naam, opties) for naam, opties in PAGINA.blokken]
