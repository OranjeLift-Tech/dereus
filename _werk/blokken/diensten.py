"""Diensten op de home: acht fotokaarten met de bestaande dienstlinks en kopij."""
NAAM = "diensten"
CSS = True
JS = False

FOTOS = {
    "particulier": "particulier", "zakelijk": "zakelijk", "nationaal": "nationaal",
    "internationaal": "internationaal", "verhuislift": "verhuislift", "opslag": "opslag",
    "montage": "handyman", "woningontruiming": "woningontruiming",
}


def html(ctx, kopij, **opties):
    k = kopij
    tegels = []
    for it in k.items:
        sleutel = it.id
        link = it.veld("link") or f"/diensten/#{sleutel}"
        titel = ctx.inline(it.titel)
        foto = FOTOS.get(sleutel)
        beeld = ctx.beeld(f"/img/dienst-{foto}.webp", "", 720, 540, klasse="dtegel__foto") if foto else ""
        tegels.append(f'''<li class="dtegel">
        <div class="dtegel__beeld">{beeld}<span class="dtegel__icoon">{ctx.dienst_icoon(sleutel)}</span></div>
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
    {ctx.belregel(k.veld("belregel"))}
  </div>
</section>'''
