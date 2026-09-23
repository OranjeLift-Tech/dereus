"""dienst-montage.webp (720x540) en dienst-montage-uit.webp (1080x810): de 3D-boor uit kosten-3d op een
achtergrond in merkblauw, als vervanging van dienst-handyman (door de gebruiker op "delete" gezet).
Foto en uitsnede liggen pixel voor pixel op dezelfde plek, zoals bij de andere dienstfoto's."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

WORTEL = Path(__file__).resolve().parent.parent
UIT = Path(sys.argv[1]) if len(sys.argv) > 1 else WORTEL / "img"
W, H = 1080, 810
render = Image.open(WORTEL / "img/kosten-3d/boor.webp").convert("RGBA")
bb = render.getbbox()
render = render.crop(bb)
# de render beslaat 64% van de breedte en staat met zijn onderkant op 90% van de hoogte, midden
rb = round(W * .64); rh = round(render.height * rb / render.width)
render = render.resize((rb, rh), Image.LANCZOS)
x = (W - rb) // 2; y = round(H * .90) - rh

# achtergrond: primary-100 boven naar primary-200 onder, met een zachte vloer
def mix(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
boven, onder = (0xE6, 0xEF, 0xFF), (0xB9, 0xD0, 0xF7)
grond = Image.new("RGB", (W, H))
d = ImageDraw.Draw(grond)
for yy in range(H):
    d.line([(0, yy), (W, yy)], fill=mix(boven, onder, (yy / H) ** 1.4))
schaduw = Image.new("L", (W, H), 0)
ImageDraw.Draw(schaduw).ellipse([x + rb * .08, y + rh - 34, x + rb * .92, y + rh + 30], fill=120)
schaduw = schaduw.filter(ImageFilter.GaussianBlur(22))
grond.paste((11, 35, 82), (0, 0), schaduw.point(lambda v: round(v * .55)))

foto = grond.convert("RGBA")
foto.alpha_composite(render, (x, y))
foto.convert("RGB").resize((720, 540), Image.LANCZOS).save(UIT / "dienst-montage.webp", quality=86, method=6)

uit = Image.new("RGBA", (W, H), (0, 0, 0, 0))
uit.alpha_composite(render, (x, y))
uit.save(UIT / "dienst-montage-uit.webp", quality=90, method=6)
print("render", rb, "x", rh, "op", x, y)
