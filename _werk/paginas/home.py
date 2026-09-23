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
        ("cijfers", {}),
        ("werkwijze", {}),
        ("reviews", {}),
        ("over-ons", {"kopij_van": ("over-ons", "verhaal"), "feiten": True, "motto": False}),   # een kopie van /over-ons/ #verhaal
        ("werkgebied", {}),
        # kopkaart: de sectiekop hoort in de belkaart. De headset verhuist mee naar de
        # rechterbovenhoek van die kaart ("hoek"); het gat dat "headset-huis" vulde bestaat
        # niet meer zodra de kop in de kaart staat.
        ("vragen", {"beeld": "headset-hoek", "kopkaart": True, "stijl": "paneel"}),
        ("aanvraag", {"kopij": None}),
        ("homecontact", {"kopij_id": "contact"}),
    ],
)
