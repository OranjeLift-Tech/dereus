"""Diensten op de home: acht fotokaarten met de bestaande dienstlinks en kopij."""
import re

NAAM = "diensten"
CSS = True
JS = False

FOTOS = {
    "particulier": "particulier-v2", "zakelijk": "zakelijk-v2", "nationaal": "nationaal-v2",
    "internationaal": "internationaal-v2b", "verhuislift": "verhuislift", "opslag": "opslag-v2",
    "montage": "montage-v2", "woningontruiming": "woningontruiming-v2",
}

# Uitstap-effect: hoe ver de fotolaag boven het kader uitsteekt (pop) en waar het kader
# begint, gemeten over die laag (knip). De uitsnede zonder achtergrond wordt niet afgeknipt, dus
# alles wat boven de kaderlijn zit komt boven de kaart uit. Berekend uit het alfamasker door
# _ai-beelden/diensten-uit-export.cjs; niet met de hand aanpassen. De oude montage (de 3D-boor)
# staat er bewust niet bij: daar was geen persoon om uit te laten stappen.
UITSTAP = {
    "particulier": ("67.4%", "40.27%"),
    # particulier-v2 (23-09-2026, variant A uit website/review/dienst-particulier-v1-20260923/): de alfa begint op
    # 21,98% van de hoogte (drempel 45, zoals de export), dus pop (0,2198 + 0,11) / (1 - 0,2198) en knip pop / (1 + pop).
    "particulier-v2": ("42.3%", "29.71%"),
    "zakelijk": ("36.9%", "26.93%"),
    # zakelijk-v2 (23-09-2026, versie 2 uit website/review/dienst-zakelijk-wit-r3-20260923/): de alfa begint net als bij
    # zakelijk op 18,89% van de hoogte en het masker valt voor 99,6% samen, dus dezelfde pop en knip als zakelijk.
    "zakelijk-v2": ("36.9%", "26.93%"),
    "nationaal": ("14.2%", "12.47%"),
    # nationaal-v2 (23-09-2026, versie 2 uit website/review/dienst-nationaal-r4-20260923/): de alfa begint op
    # 26,42% van de hoogte (drempel 45), dus pop (0,2642 + 0,11) / (1 - 0,2642) en knip pop / (1 + pop).
    "nationaal-v2": ("50.9%", "33.71%"),
    "internationaal": ("40.9%", "29.04%"),
    # internationaal-v2b (23-09-2026, variant B uit website/review/dienst-internationaal-v1-20260923/): de alfa begint
    # op 7,28% van de hoogte (drempel 45), dus pop (0,0728 + 0,11) / (1 - 0,0728) en knip pop / (1 + pop).
    "internationaal-v2b": ("19.7%", "16.47%"),
    "verhuislift": ("43.2%", "30.15%"),
    "opslag": ("50.1%", "33.38%"),
    # opslag-v2 (23-09-2026, ander gezicht, zelfde uitsnede): de bovenkant van de persoon zakt van 26,05% naar
    # 26,54% (korter haar), verder is de alfa gelijk, dus dezelfde pop en knip als opslag.
    "opslag-v2": ("50.1%", "33.38%"),
    # montage-v2 (23-09-2026, versie 3 uit website/review/handyman-ronde-r7-20260923/): de alfa begint op 3,33% van
    # de hoogte (drempel 45), dus pop (0,0333 + 0,11) / (1 - 0,0333) en knip pop / (1 + pop).
    "montage-v2": ("14.8%", "12.91%"),
    "woningontruiming": ("22.2%", "18.14%"),
    # woningontruiming-v2 (23-09-2026, versie 1 uit website/review/dienst-woningontruiming-wit-r2-20260923/): het
    # alfamasker is gelijk aan dat van woningontruiming, dus dezelfde pop en knip.
    "woningontruiming-v2": ("22.2%", "18.14%"),
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
