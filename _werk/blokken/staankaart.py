"""Staankaart: plek op straat en de vergunning voor de verhuislift, op /diensten/verhuislift/ (#ruimte-op-straat).
Een warme kaart met links de kop, twee alinea's en de knop; rechts een verhuizer met een doos op de schouder, de voeten
op de onderrand van de kaart en het hoofd erboven, en over zijn onderbenen een wit plaatje met een klei-icoon.
Bron: section-library/pay-after-stock-figure. Testlijn test/diensten-paginas, dereus-3e, 29-09-2026.

Kopij: een ##-blok met label, badge (de tekst op het plaatje), knop en twee alinea's. Opties: kopij_van=(document, id),
en dan geeft de pagina "kopij": None mee; sectie (standaard "mist"); icoon (standaard "klembord", uit img/clay/).
Vormgeving: css/blok/staankaart.css.
"""

NAAM = "staankaart"
CSS = True
JS = False

# Dezelfde verhuizer als in de blokken reviewrail en vragen: een live uitsnede, geen nieuw beeld. De uitsnede heeft
# geen lege rand (van de doos tot de zolen). Een laag op de kaart, dus alt leeg.
FIGUUR = ("/img/verhuizer-doos-schouder-uit.webp", 489, 1200)


def _klei(naam):
    # 2,75 rem op het plaatje, 2,5 rem op een telefoon (staankaart.css); 144 dekt ook een telefoon op 3x
    return (f'<img class="b-{NAAM}__klei" src="/img/clay/{naam}-144.webp" alt="" width="144" height="144" '
            f'loading="lazy" decoding="async">')


def html(ctx, kopij, sectie="mist", icoon="klembord", **opties) -> str:
    k = kopij
    if opties.get("kopij_van"):
        document, kid = opties["kopij_van"]
        k = ctx.kopij_van(document).blok(kid)
    sid = ctx.esc(k.id)
    src, fb, fh = FIGUUR
    plaat = (f'<p class="b-{NAAM}__plaat">{_klei(icoon)}<span>{ctx.inline(k.veld("badge"))}</span></p>'
             if k.veld("badge") else "")
    # Een hoofdactie: het formulier staat onderaan deze pagina (#aanvraag).
    knop = ctx.knop(k.veld("knop") or "Offerte aanvragen", "#aanvraag")
    return f'''<section class="b-{NAAM} sectie sectie--{sectie}" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap">
        <div class="b-{NAAM}__kaart" data-reveal>
          <div class="b-{NAAM}__tekst">
            {ctx.kopgroep(k)}
            <div class="b-{NAAM}__alineas">{ctx.alineas(k.tekst)}</div>
            <div class="knoppen">{knop}</div>
          </div>
          <div class="b-{NAAM}__beeld">
            <span class="b-{NAAM}__figuur" aria-hidden="true"><img src="{src}" alt="" width="{fb}" height="{fh}" loading="lazy" decoding="async"></span>
            {plaat}
          </div>
        </div>
      </div>
    </section>'''
