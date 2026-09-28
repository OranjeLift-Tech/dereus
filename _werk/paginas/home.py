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
    extra_css=("reviews-ster",),              # de gouden 3D-ster op de uitgelichte review, alleen hier
    blokken=[
        ("hero", {"kopij_id": "offerte"}),
        ("diensten", {}),
        ("waarom", {}),
        # De cijfers als schuine actielijn (28-09-2026): "make this section into an action line, like a stripe that
        # is slanted and has icons by each line". Zelfde blok als #vertrouwen op /contact/. Het oude blok cijfers.py
        # blijft bestaan. Hier zonder "sectie": de cijferband telde niet mee in de motieftellers van style.css.
        ("actielijn", {"kopij_id": "cijfers"}),
        # Zo werkt het: de stappen als kaarten met een verhuizer (steps-four-green uit ../section-library), zoals op
        # /werkwijze/, op de Koningsblauwe band uit de regel hierboven. Gekozen op 28-09-2026: "Home "Zo werkt het",
        # routeband or option A (28-09-2026): A on Koningsblauw" (website/review/zowerkthet-home-vergelijk-20260928/).
        # Daarvoor de routeband (intro-route-band); dat blok en zijn CSS blijven staan.
        ("stapkaarten", {"kopij_id": "werkwijze", "grond": "blauw"}),
        ("reviews", {}),
        ("over-ons", {"kopij_van": ("over-ons", "verhaal"), "feiten": True, "motto": False}),   # een kopie van /over-ons/ #verhaal
        ("werkgebied", {}),
        # kopkaart: de sectiekop hoort in de belkaart. De headset verhuist mee naar de
        # rechterbovenhoek van die kaart ("hoek"); het gat dat "headset-huis" vulde bestaat
        # niet meer zodra de kop in de kaart staat.
        ("vragen", {"beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),
        ("aanvraag", {"kopij": None}),
        # homecontact ("Wilt u iets bespreken over uw verhuizing?") is eraf sinds 28-09-2026:
        # "remove from homepage as it sits right below the other form". Blok en CSS blijven bestaan.
    ],
)

# Klei-iconen op de naden, alleen vanaf 1100 px (blok naadiconen). De gebruiker plaatste ze zelf met de artifact
# placer op 1440 (28-09-2026). Per blok: het id van de sectie en per icoon (naam, kant, x, y) in px, gemeten uit
# zijn export op de home van 15:41: x vanaf die kant van de pagina, y vanaf de bovenkant van de sectie.
NAADICONEN = {
    "diensten": ("diensten", [("particulier", "rechts", 77, 60), ("dozen", "links", 33, 68)]),
    # Ster in plaats van het schild (28-09-2026, "sure replace"): het schild stond al op de kaart "Standaard verzekerd".
    "waarom": ("waarom", [("ster", "links", 70, -52)]),
    "stapkaarten": ("werkwijze", [("nationaal", "rechts", 50, 148)]),
    "reviews": ("reviews", [("telefoon", "links", 22, 19)]),
    "over-ons": ("over-ons", [("verhuislift", "links", 66, -58)]),
    "werkgebied": ("werkgebied", [("internationaal", "links", 82, -18)]),
    "aanvraag": ("aanvraag", [("klembord", "rechts", 46, 21)]),
}
PAGINA.blokken = [("naadiconen", {"kopij": None, "blok": naam, "opties": opties, "plek": NAADICONEN[naam]})
                  if naam in NAADICONEN else (naam, opties) for naam, opties in PAGINA.blokken]
