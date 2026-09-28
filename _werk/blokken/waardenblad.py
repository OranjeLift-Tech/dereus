"""Zo werken wij als blad (/over-ons/ #zo-werken-wij), sinds 28-09-2026. Naar het patroon contact-direct-location
(Solar Green) uit ../section-library: een blad van Lucht naar goud met de kop, de intro en de offerteknop, een vakman
die boven de bovenrand van het blad uitkomt, en daaronder de waarden als witte kaarten op een Koningsblauwe voet.
De keuze van de gebruiker uit website/review/zowerkenwij-20260928/: versie 5, met in ronde 2 "make the icons pop out
of the block and make the blocks be more compact, less empty space" en in ronde 3 "less text" ("Take r3 onto
/over-ons/"). Hiervoor stond hier blok kernwaarden (Koningsblauwe band met rijen); dat blok en zijn CSS blijven staan.

Het klei-icoon van elke kaart steekt --uit boven de kaart uit. De kolommen zijn zo breed als de tekst lang is
(gewicht (lengte / gemiddelde) ** 0.6), zodat de vijf kaarten op 1440 even hoog zijn zonder lege strook onderin.
Kopij: over-ons.md {#zo-werken-wij}: label, intro, knop, en per waarde een ###-titel met een alinea.
De vakman: dienst-montage-v2-uit (live op de home en /diensten/), alt leeg; hij illustreert en zegt niet wie het is.
"""
import re

NAAM = "waardenblad"
CSS = True
JS = False

# klei-iconen per waarde-id (img/clay/<naam>-144/240.webp); niet de vijf van "Sterk waar het zwaar is" op deze pagina
KLEI = {"sterk": "trap", "zorgvuldig": "dozen", "betrouwbaar": "klembord", "eerlijk": "formulier", "betrokken": "headset"}
MAN = ("/img/dienst-montage-v2-uit.webp", 1080, 810)


def _klei(ctx, it):
    n = KLEI.get(it.id)
    if not n:
        raise ValueError(f"waardenblad: geen klei-icoon voor waarde {it.id!r}, zet er een in KLEI")
    return ctx.beeld(f"/img/clay/{n}-144.webp", "", 144, 144, klasse="wb__klei",
                     srcset=f"/img/clay/{n}-144.webp 144w, /img/clay/{n}-240.webp 240w",
                     sizes="(max-width: 560px) 3.75rem, 4.75rem")


def html(ctx, kopij, sectie="lucht", **opties):
    k = kopij
    if not 3 <= len(k.items) <= 6:
        raise ValueError(f"waardenblad: 3 tot 6 waarden, niet {len(k.items)}")
    kaarten, lengtes = [], []
    for it in k.items:
        tekst = ctx.alineas(it.tekst)
        lengtes.append(len(re.sub(r"<[^>]+>", "", tekst)))
        kaarten.append(f'''
      <li class="wb__item"><div class="wb__kaart">{_klei(ctx, it)}<h3>{ctx.inline(it.titel)}</h3>{tekst}</div></li>''')
    gem = sum(lengtes) / len(lengtes)
    kolommen = " ".join(f"minmax(0,{(n / gem) ** 0.6:.2f}fr)" for n in lengtes)
    knop = ctx.knop(k.veld("knop"), "/offerte/", klasse="wb__knop") if k.veld("knop") else ""
    msrc, mb, mh = MAN
    return f'''<section class="sectie sectie--{sectie} b-{NAAM}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="wb__blad" data-reveal>
      <div class="wb__kop">{ctx.label(k.veld("label"))}<h2 id="{ctx.esc(k.id)}-kop">{ctx.inline(k.kop)}</h2>{f'<p class="intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""}{knop}</div>
      <div class="wb__fig" aria-hidden="true">{ctx.beeld(msrc, "", mb, mh)}</div>
    </div>
    <ul class="wb__kaarten" role="list" style="--wb-kolommen:{kolommen}" data-reveal-groep>{"".join(kaarten)}
    </ul>
  </div>
</section>'''
