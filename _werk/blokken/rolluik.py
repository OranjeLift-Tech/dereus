"""Rolluik: hoe opslag bij een verhuizing gaat, op /diensten/tijdelijke-opslag/ (#zo-werkt-opslag). Links een
opslagdeur met het rolluik half dicht en de verhuisadviseur in de opening, een wit naamplaatje over zijn benen;
rechts de kop, drie stappen (###-items) op een stippellijn en de knop met een belregel.
Bron: section-library/door-shutter-steps (nieuw, /section; wacht op zijn akkoord voor de catalogus).
Testlijn test/diensten-paginas, dereus-3e, 29-09-2026.

Kopij: een ##-blok met label, intro, naamplaat, naamplaat-sub, knop, belregel, en ###-items met icoon: (een naam uit
img/clay/) en een alinea. Opties: kopij_van=(document, id), en dan geeft de pagina "kopij": None mee; sectie
(standaard "wit"); icoon (het icoon op het naamplaatje, standaard "headset").
Vormgeving: css/blok/rolluik.css.
"""

NAAM = "rolluik"
CSS = True
JS = False

# De verhuisadviseur van de offertestappen (blok stappentrap): een live uitsnede tot de dijen, geen lege rand.
# Een laag in de deur; het naamplaatje zegt wie hij is, dus alt leeg.
FIGUUR = ("/img/offerte-figuur-uit.webp", 435, 752)

# Stapelende dozen achter de adviseur, als lijntekening op lage dekking (rolluik.css)
DOZEN = ('<svg class="b-rolluik__dozen" viewBox="0 0 120 100" preserveAspectRatio="xMinYMax meet" aria-hidden="true" '
         'focusable="false"><path d="M4 98V62h40v36zm40 0V62h36v36zM14 62V30h38v32zm8-32V4h30v26zM4 80h40M44 80h36M14 46h38M22 17h30"/></svg>')


def _klei(naam, klasse, maten):
    # 144 dekt 2x op het scherm, 240 een telefoon op 3x
    return (f'<img class="b-{NAAM}__{klasse}" src="/img/clay/{naam}-144.webp" srcset="/img/clay/{naam}-144.webp 144w, '
            f'/img/clay/{naam}-240.webp 240w" sizes="{maten}" alt="" width="144" height="144" loading="lazy" decoding="async">')


def html(ctx, kopij, sectie="wit", icoon="headset", **opties) -> str:
    k = kopij
    if opties.get("kopij_van"):
        document, kid = opties["kopij_van"]
        k = ctx.kopij_van(document).blok(kid)
    sid = ctx.esc(k.id)
    src, fb, fh = FIGUUR
    # de schijf is 4 rem, 3,25 rem op een telefoon (rolluik.css)
    stappen = "".join(f'''
          <li class="b-{NAAM}__stap">{_klei(it.veld("icoon") or "dozen", "klei", "(max-width: 559.98px) 3.25rem, 4rem")}<div class="b-{NAAM}__staptekst"><span class="b-{NAAM}__nr">Stap {i}</span><h3>{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</div></li>'''
                      for i, it in enumerate(k.items, 1))
    plaat = ""
    if k.veld("naamplaat"):
        plaat = (f'<p class="b-{NAAM}__plaat">{_klei(icoon, "plaatklei", "3rem")}'
                 f'<span><b>{ctx.inline(k.veld("naamplaat"))}</b> {ctx.inline(k.veld("naamplaat-sub"))}</span></p>')
    # Een hoofdactie naar het formulier onderaan de pagina, en het nummer als tekst ernaast. Zonder WhatsApp-knop:
    # die zou een derde element op de regel zijn, en het formulier heeft zijn eigen belknop.
    acties = ctx.knop(k.veld("knop") or "Offerte aanvragen", "#aanvraag") + ctx.belregel(k.veld("belregel"), whatsapp=False)
    return f'''<section class="b-{NAAM} sectie sectie--{sectie}" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap b-{NAAM}__raster">
        <div class="b-{NAAM}__kop" data-reveal>
          {ctx.kopgroep(k)}
        </div>
        <div class="b-{NAAM}__deur">
          <span class="b-{NAAM}__rail" aria-hidden="true"></span>
          <span class="b-{NAAM}__luik" aria-hidden="true"></span>
          <div class="b-{NAAM}__opening" aria-hidden="true">
            {DOZEN}
            <span class="b-{NAAM}__figuur"><img src="{src}" alt="" width="{fb}" height="{fh}" loading="lazy" decoding="async"></span>
          </div>
          {plaat}
        </div>
        <ol class="b-{NAAM}__stappen" role="list" data-reveal-groep>{stappen}
        </ol>
        <div class="b-{NAAM}__acties" data-reveal>{acties}</div>
      </div>
    </section>'''
