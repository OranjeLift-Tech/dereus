"""Een afvinklijst op één grote Koningsblauwe plaat, met een foto in de huisvorm ernaast. Voor #voorbereiding.

Pagina: /werkwijze/. Ronde 6, versie 3 (website/review/werkwijze-ronde-6/notitie-3.md).
De plaat is hetzelfde middel als de belkaart op /contact/: Koningsblauw dat naar Diepblauw zakt, een
zichtbare dikte onder de onderrand, een goudgeel tabje op de bovenrand en het huisje uit het logo in de
hoek. Het 3D-klembord hangt over de bovenrand. De foto in de lijst is in de huisvorm uit het logo geknipt
met een goudgeel huis er net iets omheen, hetzelfde diepte-idee als de panelen op /diensten/, maar met
één laag: er stapt hier geen uitsnede uit het huis. Alles staat stil.

Alle klassen staan onder b-lijstplaat, zodat dit blok geen naam deelt met een ander blok op dezelfde pagina.

Opties: kopij_id (welk blok), grond = "wit" of "mist", foto (aan of uit), voorwerp (aan of uit).
Kopij: label, intro, lijstkop, lijst (een regel mag beginnen met een vette kop: "**Dozen op tijd.** uitleg"),
slot, en optioneel linktekst en link.
"""
import re

NAAM = "lijstplaat"
CSS = True
JS = False

# Het 3D-klembord met de pen, over de bovenrand van de plaat: hetzelfde voorwerp en dezelfde opzet als de
# kanaalkaarten op /contact/ (img/contact-3d/). Het staat stil, de hoek zit in het beeld zelf.
VOORWERP = ("/img/contact-3d/formulier.webp", 346, 400)

# De foto in de huisvorm: gestapelde, ingepakte verhuisdozen van De Reus, met het merkteken op de voorste
# doos. Dat is precies waar deze sectie over gaat, en het is een eigen foto met eigen dozen, geen stockbeeld
# met onbekende mensen (design-notes A3). Niet img/headers/kosten.webp: A3 heeft die al afgewezen. Niet
# img/verwachten-inpakken.webp: dat is dezelfde foto als img/headers/werkwijze.webp, die bovenaan deze
# pagina staat. De uitsnede begint links (object-position in de CSS), daar staat het merkteken.
FOTO = ("/img/headers/studenten.webp", 720, 405)

_VET = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")


def _punt(ctx, regel):
    """Eén afvinkregel: een goudgele schijf met een haakje, daarnaast de tekst. Een regel die met een vette
    kop begint houdt die kop binnen dezelfde span, anders valt de zin op een schermlezer uit elkaar."""
    m = _VET.match(regel)
    kern = f"<b>{ctx.inline(m.group(1))}</b> {ctx.inline(m.group(2))}" if m else ctx.inline(regel)
    return f'<li>{ctx.icoon("check")}<span>{kern}</span></li>'


def html(ctx, kopij, **opties) -> str:
    k = kopij
    grond = "mist" if opties.get("grond") == "mist" else "wit"
    punten = "".join(_punt(ctx, r) for r in k.lijst)
    lijstkop = f'<h3 class="b-{NAAM}__lijstkop">{ctx.inline(k.veld("lijstkop"))}</h3>' if k.veld("lijstkop") else ""
    # De slotregel is een tipvak: een doorschijnend vlak op de plaat met een goudgele kantlijn, dezelfde
    # vorm als het tipvak in de panelen op /diensten/.
    slot = f'<p class="b-{NAAM}__slot">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
    link = ""
    if k.veld("link"):
        link = (f'<p class="b-{NAAM}__acties">'
                f'{ctx.knop(k.veld("linktekst"), k.veld("link"), soort="link", klasse=f"b-{NAAM}__link")}</p>')
    # alt blijft leeg: de lijst ernaast zegt alles wat de foto laat zien, en het goudgele huis eromheen is sier
    beeld = ""
    if opties.get("foto", True):
        foto = ctx.beeld(FOTO[0], "", FOTO[1], FOTO[2], klasse=f"b-{NAAM}__foto")
        beeld = (f'<span class="b-{NAAM}__beeld" aria-hidden="true">'
                 f'<span class="b-{NAAM}__huis">{foto}</span></span>')
    voorwerp = ""
    if opties.get("voorwerp", True):
        voorwerp = ctx.beeld(VOORWERP[0], "", VOORWERP[1], VOORWERP[2], klasse=f"b-{NAAM}__klembord")
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        {ctx.kopgroep(k, klasse=f"b-{NAAM}__kop")}
        <div class="b-{NAAM}__plaat" data-reveal>
          {voorwerp}
          <div class="b-{NAAM}__in">
            <div class="b-{NAAM}__zij">{lijstkop}{beeld}</div>
            <ul class="b-{NAAM}__lijst" data-reveal-groep>{punten}</ul>
          </div>
          {slot}{link}
        </div>
      </div>
    </section>'''
