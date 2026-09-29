"""Zo pakken we het aan (/diensten/zakelijke-verhuizingen/ #hoe), sinds 29-09-2026 op de testlijn. Naar het patroon
branch-route-stops (De Bresser) uit ../section-library: de kop met twee knoppen links, rechts een verhuizer die met
zijn hoofd boven het fotokader uitkomt, en over de onderrand van de foto een witte strook met de stappen als haltes
op een gestippelde route. Elke halte heeft een speld en een klei-icoon op de route. Geclaimd als #3 in
_werk/dienstsecties-register.md.

Kopij: diensten-zakelijk.md {#hoe} (label, intro, vier ###-stappen met een alinea), via kopij_van, want de pagina
leest diensten.md. De knoptekst komt uit {#kop} van hetzelfde document, de link naar /werkwijze/ uit home.md
{#werkwijze} (linktekst, link). Opties: kopij_van=(document, blok-id), offerte (href van de offerteknop).
De foto: verhuisdag-dragen-stoep met zijn uitsnede op dezelfde doos (live op de home, #waarom), alt leeg; hij
illustreert de verhuisdag en zegt niet wie het is. Niet dienst-nationaal-v2: in die uitsnede zweeft de tweede man uit
de bus, dus daar kan het kader niet laag genoeg voor een hoofd erboven.
"""
NAAM = "routestops"
CSS = True
JS = False

# klei-icoon per stap (img/clay/<naam>-144/240.webp), in de volgorde van de kopij
KLEI = {"Kennismaking": "telefoon", "Het verhuisplan": "formulier", "De verhuisdag": "nationaal", "Weer aan het werk": "zakelijk"}
FOTO = ("/img/verhuisdag-dragen-stoep.webp", 1400, 1050)
UIT = ("/img/verhuisdag-dragen-stoep-uit.webp", 1400, 1050)


def _klei(ctx, titel):
    n = KLEI.get(titel)
    if not n:
        raise ValueError(f"routestops: geen klei-icoon voor stap {titel!r}, zet er een in KLEI")
    return ctx.beeld(f"/img/clay/{n}-144.webp", "", 144, 144, klasse="rstop__klei",
                     srcset=f"/img/clay/{n}-144.webp 144w, /img/clay/{n}-240.webp 240w",
                     sizes="(max-width: 560px) 3rem, 3.5rem")


def html(ctx, kopij, kopij_van=("diensten-zakelijk", "hoe"), offerte="/offerte/", **opties):
    doc = ctx.kopij_van(kopij_van[0])
    k = doc.blok(kopij_van[1])
    if not 3 <= len(k.items) <= 5:
        raise ValueError(f"routestops: 3 tot 5 stappen, niet {len(k.items)}")
    haltes = "".join(f'''
          <li class="rstop__halte"><span class="rstop__speld" aria-hidden="true"></span>{_klei(ctx, it.titel)}<h3>{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</li>'''
                     for it in k.items)
    werk = ctx.kopij_van("home").blok("werkwijze")
    knoppen = ctx.knop(doc.blok("kop").veld("knop"), offerte)
    if ctx.live(werk.veld("link")):
        knoppen += ctx.knop(werk.veld("linktekst"), werk.veld("link"), soort="link")
    fsrc, fb, fh = FOTO
    usrc, ub, uh = UIT
    return f'''<section class="sectie sectie--mist b-{NAAM}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap rstop__raster">
    <div class="rstop__kop" data-reveal>{ctx.label(k.veld("label"))}<h2 id="{ctx.esc(k.id)}-kop">{ctx.inline(k.kop)}</h2>{f'<p class="intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""}
      <div class="rstop__knoppen">{knoppen}</div>
    </div>
    <div class="rstop__fig" aria-hidden="true">{ctx.beeld(fsrc, "", fb, fh, klasse="rstop__foto")}{ctx.beeld(usrc, "", ub, uh, klasse="rstop__uit")}</div>
    <div class="rstop__strook" data-reveal>
      <ol class="rstop__lijst" role="list" data-reveal-groep>{haltes}
      </ol>
    </div>
  </div>
</section>'''
