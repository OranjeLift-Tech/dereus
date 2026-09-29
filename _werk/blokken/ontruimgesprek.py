"""Ontruimgesprek: het eerste gesprek met de verhuisadviseur, op /diensten/woningontruiming/ (#gesprek). Links de kop,
de alinea's en de knoppen; rechts de adviseur met headset voor een goudgele wijzerplaat, het hoofd boven het kader uit;
over de onderkant van de foto een kaart met drie ###-items, elk met een klei-icoon.
Bron: section-library/reply-dial-choices. Testlijn test/diensten-paginas, dereus-ce, 29-09-2026.

Kopij: een ##-blok met label, kaartlabel, kaartkop, knop, alinea's, en ###-items met icoon: (een naam uit img/clay/)
en een alinea. Opties: kopij_van=(document, id), en dan geeft de pagina "kopij": None mee; sectie (standaard "diep").
Vormgeving: css/blok/ontruimgesprek.css.
"""

NAAM = "ontruimgesprek"
CSS = True
JS = False

# De verhuisadviseur die terugbelt (zelfde paar als homecontact op de home en na-bericht op de bedanktpagina's): de foto
# en de uitsnede die er pixel op pixel op ligt, allebei 1200x800. De foto draagt de alt, de uitsnede is een laag erop.
# De uitsnede heeft lichtere breedtes (_werk/beeldvarianten.py); even groot getekend blijven ze op de foto liggen.
FOTO = ("/img/contact-klantenservice-foto.webp", 1200, 800, "Verhuisadviseur van De Reus aan de telefoon met een klant")
UIT = ("/img/contact-klantenservice-uit.webp", "/img/contact-klantenservice-uit-680.webp 680w, "
       "/img/contact-klantenservice-uit-900.webp 900w, /img/contact-klantenservice-uit.webp 1200w")
MATEN = "(max-width: 899.98px) min(100vw, 40rem), 44vw"


def _klei(naam):
    # 3,25 rem op het scherm, 2,9 rem op een telefoon (ontruimgesprek.css); 144 dekt 2x, 240 een telefoon op 3x
    return (f'<img class="b-{NAAM}__klei" src="/img/clay/{naam}-144.webp" srcset="/img/clay/{naam}-144.webp 144w, '
            f'/img/clay/{naam}-240.webp 240w" sizes="(max-width: 559.98px) 2.9rem, 3.25rem" alt="" width="144" height="144" '
            f'loading="lazy" decoding="async">')


def html(ctx, kopij, sectie="diep", **opties) -> str:
    k = kopij
    if opties.get("kopij_van"):
        document, kid = opties["kopij_van"]
        k = ctx.kopij_van(document).blok(kid)
    sid = ctx.esc(k.id)
    src, fb, fh, alt = FOTO
    keuzes = "".join(f'''
          <li>{_klei(it.veld("icoon") or "dozen")}<div><strong>{ctx.inline(it.titel)}</strong>{ctx.alineas(it.tekst)}</div></li>'''
                     for it in k.items)
    # Een hoofdactie: het formulier staat verderop op de pagina. Een belknop kreeg hier van contactlinks() een
    # WhatsApp-knop erbij, drie knoppen op twee regels naast een rustige kop; het formulier (#aanvraag) heeft zijn belknop.
    knoppen = ctx.knop(k.veld("knop") or "Offerte aanvragen", "#aanvraag")
    return f'''<section class="b-{NAAM} sectie sectie--{sectie}" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap b-{NAAM}__raster">
        <div class="b-{NAAM}__tekst" data-reveal>
          {ctx.kopgroep(k)}
          {ctx.alineas(k.tekst)}
          <div class="knoppen">{knoppen}</div>
        </div>
        <figure class="b-{NAAM}__beeld" data-reveal>
          <span class="b-{NAAM}__schijf" aria-hidden="true"></span>
          <div class="b-{NAAM}__kader">
            <div class="b-{NAAM}__vak">{ctx.beeld(src, alt, fb, fh)}</div>
            <span class="b-{NAAM}__uit" aria-hidden="true">{ctx.beeld(UIT[0], "", fb, fh, srcset=UIT[1], sizes=MATEN)}</span>
          </div>
        </figure>
        <div class="b-{NAAM}__kaart" data-reveal>
          <div class="b-{NAAM}__kaartkop">{ctx.label(k.veld("kaartlabel"))}<h3>{ctx.inline(k.veld("kaartkop"))}</h3></div>
          <ul class="b-{NAAM}__keuzes" role="list" data-reveal-groep>{keuzes}
          </ul>
        </div>
      </div>
    </section>'''
