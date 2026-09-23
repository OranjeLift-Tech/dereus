"""Diensten op de home: acht fotokaarten met de bestaande dienstlinks en kopij."""
import re

NAAM = "diensten"
CSS = True
JS = False

FOTOS = {
    "particulier": "particulier", "zakelijk": "zakelijk", "nationaal": "nationaal",
    "internationaal": "internationaal", "verhuislift": "verhuislift", "opslag": "opslag-v2",
    "montage": "montage", "woningontruiming": "woningontruiming",
}

# Uitstap-effect: hoe ver de fotolaag boven het kader uitsteekt (pop) en waar het kader
# begint, gemeten over die laag (knip). De uitsnede zonder achtergrond wordt niet afgeknipt, dus
# alles wat boven de kaderlijn zit komt boven de kaart uit. Berekend uit het alfamasker door
# _ai-beelden/diensten-uit-export.cjs; niet met de hand aanpassen. Montage staat er bewust niet
# bij: dat beeld is een 3D-boor op een achtergrond, zonder persoon om uit te laten stappen.
UITSTAP = {
    "particulier": ("67.4%", "40.27%"),
    "zakelijk": ("36.9%", "26.93%"),
    "nationaal": ("14.2%", "12.47%"),
    "internationaal": ("40.9%", "29.04%"),
    "verhuislift": ("43.2%", "30.15%"),
    "opslag": ("50.1%", "33.38%"),
    # opslag-v2 (23-09-2026, ander gezicht, zelfde uitsnede): de bovenkant van de persoon zakt van 26,05% naar
    # 26,54% (korter haar), verder is de alfa gelijk, dus dezelfde pop en knip als opslag.
    "opslag-v2": ("50.1%", "33.38%"),
    "woningontruiming": ("22.2%", "18.14%"),
}


def hulp(ctx, tekst):
    """De regel onder de tegels als twee blokken: bellen en WhatsApp naast de vraag."""
    cfg = ctx.cfg
    vraag = re.split(r"\bBel\b", ctx.inline(tekst or ""), maxsplit=1)[0].strip().rstrip(".")
    vraagregel = f'<p class="dhulp__vraag">{vraag}</p>' if vraag else ""
    # De WhatsApp-link volgt direct op de tel-link en draagt data-whatsapp-business,
    # zodat ctx.contactlinks er niet nog een tweede achteraan plakt.
    return f'''<div class="dhulp">{vraagregel}<a class="dhulp__blok dhulp__bel" href="{cfg.TELHREF}">\
{ctx.icoon("telefoon")}<span>Bel {cfg.TEL}</span></a><a class="dhulp__blok dhulp__wa" href="{cfg.WHATSAPP}" \
data-whatsapp-business aria-label="Contact met {ctx.esc(cfg.NAAM)} via WhatsApp" title="Contact via WhatsApp">\
{ctx.icoon("whatsapp-wit")}<span>WhatsApp</span></a></div>'''


def html(ctx, kopij, **opties):
    k = kopij
    tegels = []
    for it in k.items:
        sleutel = it.id
        link = it.veld("link") or f"/diensten/#{sleutel}"
        titel = ctx.inline(it.titel)
        foto = FOTOS.get(sleutel)
        beeld = uit = stijl = ""
        if foto:
            beeld = ctx.beeld(f"/img/dienst-{foto}.webp", "", 720, 540, klasse="dtegel__foto")
            if foto in UITSTAP:
                pop, knip = UITSTAP[foto]
                stijl = f' style="--pop:{pop};--knip:{knip}"'
                uit = f'<span class="dtegel__uit">{ctx.beeld(f"/img/dienst-{foto}-uit.webp", "", 1080, 810)}</span>'
        tegels.append(f'''<li class="dtegel"{stijl}>
        <div class="dtegel__beeld"><span class="dtegel__laag">{beeld}{uit}</span><span class="dtegel__icoon">{ctx.dienst_icoon(sleutel, inline=True)}</span></div>
        <div class="dtegel__inhoud">
        <h3 class="dtegel__titel"><a href="{ctx.esc(link)}">{titel}</a></h3>
        <p class="dtegel__tekst">{ctx.inline(it.veld("tekst"))}</p>
        <span class="dtegel__pijl" aria-hidden="true">{ctx.icoon("pijl")}</span>
        </div>
      </li>''')
    alle = ctx.knop(k.veld("linktekst", "Bekijk alle diensten"), "/diensten/", soort="link")
    return f'''<section class="sectie sectie--mist b-diensten" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="kopbalk">{ctx.kopgroep(k)}<div class="kopbalk__eind">{alle}</div></div>
    <ul class="dtegels" role="list" data-reveal-groep>
      {"".join(tegels)}
    </ul>
    {hulp(ctx, k.veld("belregel"))}
  </div>
</section>'''
