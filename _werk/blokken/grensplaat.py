"""Zo gaat een verhuizing over de grens (/diensten/internationale-verhuizingen/ #over-de-grens), sinds 29-09-2026 op de
testlijn. Naar het patroon locations-plate-truck (De Bresser) uit ../section-library: een lichte band met een schuine
bovenrand, links de tekst met de belknop, rechts de vrachtwagen die boven de band uitsteekt en een witte plaat over de
wielen met de vier stappen, elk met een klei-icoon. Geclaimd als #7 in _werk/dienstsecties-register.md.

Kopij: dienstsecties-internationaal.md {#over-de-grens}, via kopij_van (de pagina leest diensten.md): label, intro en
vier ###-items. De bron per zin staat in dat bestand.
Opties: kopij_van=(document, blok-id).
"""

NAAM = "grensplaat"
CSS = True
JS = False

# klei-icoon per stap (img/clay/<naam>-144/240.webp), op de ###-titel
KLEI = {"Het gesprek": "headset", "De offerte": "formulier", "De reis": "dozen", "Aankomst": "montage"}
WAGEN = "/img/dienstsecties/vrachtwagen-uit"


def _klei(ctx, titel):
    n = KLEI.get(titel)
    if not n:
        raise ValueError(f"grensplaat: geen klei-icoon voor stap {titel!r}, zet er een in KLEI")
    return ctx.beeld(f"/img/clay/{n}-144.webp", "", 144, 144, klasse="gp__klei",
                     srcset=f"/img/clay/{n}-144.webp 144w, /img/clay/{n}-240.webp 240w",
                     sizes="(max-width: 560px) 3rem, 3.5rem")


def html(ctx, kopij, kopij_van=("dienstsecties-internationaal", "over-de-grens"), **opties):
    k = ctx.kopij_van(kopij_van[0]).blok(kopij_van[1])
    if len(k.items) != 4:
        raise ValueError(f"grensplaat: vier stappen, niet {len(k.items)}")
    stappen = "".join(f'''
          <li class="gp__stap"><div class="gp__kaart">{_klei(ctx, it.titel)}<h3>{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</div></li>'''
                      for it in k.items)
    wagen = ctx.beeld(f"{WAGEN}-1140.webp", "", 1140, 441, klasse="gp__wagen",
                      srcset=f"{WAGEN}-570.webp 570w, {WAGEN}-1140.webp 1140w",
                      sizes="(max-width: 900px) min(92vw, 36rem), min(52vw, 42rem)")
    return f'''<section class="sectie sectie--wit b-{NAAM}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="gp__band" aria-hidden="true"></div>
  <div class="wrap gp__raster">
    <div class="gp__tekst" data-reveal>
      {ctx.label(k.veld("label"))}<h2 id="{ctx.esc(k.id)}-kop">{ctx.inline(k.kop)}</h2><p class="intro">{ctx.inline(k.eis("intro"))}</p>
      <div class="knoppen">{ctx.belknop()}</div>
    </div>
    <div class="gp__beeld">
      {wagen}
      <div class="gp__plaat">
        <ol class="gp__stappen" role="list" data-reveal-groep>{stappen}
        </ol>
      </div>
    </div>
  </div>
</section>'''
