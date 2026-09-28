"""Een afvinklijst op één grote Koningsblauwe plaat, met een foto ernaast waar de verhuizer uit stapt. Voor #voorbereiding.

Pagina: /werkwijze/. Ronde 6, versie 3 (website/review/werkwijze-ronde-6/notitie-3.md).
De plaat is hetzelfde middel als de belkaart op /contact/: Koningsblauw dat naar Diepblauw zakt, een
zichtbare dikte onder de onderrand, een goudgeel tabje op de bovenrand en het huisje uit het logo in de
hoek. Het 3D-klembord hangt over de bovenrand. Sinds 28-09-2026 zit de foto verzonken in een dikke
Diepblauwe plaat en leunt de verhuizer eruit naar voren: zijn hoofd en zijn hand aan de kast komen boven
de rand uit (ontwerp 09 "Diepe plaat" uit _ontwerpen/lijstplaat-uit-de-foto.html). Alles staat stil.

Alle klassen staan onder b-lijstplaat-geel, zodat dit blok geen naam deelt met een ander blok op dezelfde pagina.

Opties: kopij_id (welk blok), grond = "wit" of "mist", foto (aan of uit), voorwerp (aan of uit).
Kopij: label, intro, lijstkop, lijst (een regel mag beginnen met een vette kop: "**Dozen op tijd.** uitleg"),
slot, en optioneel linktekst en link.

Samenvoeging 28-09-2026: dit is de versie van Tugche (origin/main 9dbb9a8) van het blok lijstplaat, de Goudgele
plaat waar de verhuizer uit leunt, met de klei-iconen die sinds 28-09-2026 overal de 3D-renders vervangen. Live
staat op /werkwijze/ lijstplaat (de Koningsblauwe plaat); dit blok staat daar als regel om te wisselen. Klassen
en css (css/blok/lijstplaat-geel.css) heten b-lijstplaat-geel, zodat de twee versies elkaar niet raken.
"""
import re

NAAM = "lijstplaat-geel"
CSS = True
JS = False

# Het 3D-klembord met de pen, over de bovenrand van de plaat: hetzelfde voorwerp en dezelfde opzet als de
# kanaalkaarten op /contact/ (img/contact-3d/). Het staat stil, de hoek zit in het beeld zelf.
# Sinds 28-09-2026 een klei-icoon (img/clay/, vierkant) in plaats van de 3D-render; hoogte vast in de css.
# Het klembord met de vinkjes en niet het formulier: dit is de afvinklijst, en het formulier staat op /werkwijze/
# al bij stap 1 van de trap erboven (samenvoeging 28-09-2026).
VOORWERP = ("/img/clay/klembord-240.webp", 240, 240)

# De foto in de huisvorm. Wat hier hoort is sinds 23-09-2026 veranderd, dus lees dit voor je hem
# vervangt.
#
# GEEN DOZEN MEER, EN GEEN NIEUWE BEELDEN. De oorspronkelijke opzet van dit blok vroeg om gestapelde
# verhuisdozen met het merk erop. Dat is die dag ook gemaakt en geplaatst (vijf rondes, het merk met
# het echte logobestand achteraf op blanco gegenereerde dozen), en meteen daarna zei de gebruiker:
# "change the image completely, add something more interesting than the box". Een ronde met vijf
# andere onderwerpen kreeg daarna: "nog niets gemarkeerd, dont make images for this section, use
# existing ones". Beide zijn zijn woorden en ze gaan voor de oorspronkelijke bedoeling: stuur hier
# niemand terug naar karton, en genereer hier niets nieuws.
#
# Wat er al bestaat is nagelopen op 23-09-2026, in de huisvorm en op de 264 px die de plaat
# werkelijk geeft: website/review/lijstplaat-bestaand-20260923/. Uitkomst in het kort: van de
# bruikbare kandidaten is alleen onze eigen dozenronde voor deze vorm gemaakt, en van vrijwel elk
# bestaand bestand in img/ is geen herkomst vastgelegd.
#
# EN DAARNA GING DE HUISVORM ERAF. Op die survey kwam: "none work, use image of workers working and
# remove the house form on the image". Dat heft de reden op waarom bijna alles afviel: de meeste
# kandidaten sneuvelden op de huisvorm en niet op het beeld. De vergelijking staat in
# website/review/lijstplaat-vorm-20260923/ (nu tegenover een liggend kader van 3:2, echt gebouwd in
# de browser, vier schermbreedtes).
#
# RONDE 2 DAAROP: "its better, but remove the border on the image and make the image larger, use
# different existing image". Dus ook de goudgele rand van .b-lijstplaat-geel__beeld::before gaat eraf.
# Let op wat dat betekent: die rand was het enige geel in de linkerkolom, bewust bewaard toen de
# huisvorm eraf ging. Zonder hem heeft de kolom zelf geen merkkleur meer; het geel in de sectie zit
# dan alleen nog in het tabje op de bovenrand van de plaat, de vinkjes in de lijst en het huisje in
# de sectielabel. De slagschaduw is meeverhuisd naar .b-lijstplaat-geel__beeld zelf, anders verdwijnt die
# met de ::before mee.
# Twee maten gemeten op 1440 (website/review/lijstplaat-vorm-20260923/): beeldkolom 24vw geeft een
# vak van 346x230 en kost geen hoogte, 30vw geeft 432x288 maar maakt de lijst smaller en de sectie
# 81 px hoger.
#
# RONDE 3: "houden toestand 4. use image made today, make it fully cover the empty space". Dus de
# grote variant (beeldkolom 30vw), een beeld van vandaag, en het beeld vult de kolom.
# Wat die lege ruimte was, gemeten voor er iets veranderde: op 1440 was de linkerkolom 343 px hoog
# (35 px lijstkop plus 288 px beeld) tegen 508 px voor de lijst ernaast, dus er stond 165 px kale
# blauwe plaat onder het beeld. Opgelost met align-items: stretch plus een flexkolom in plaats van
# met een vaste aspect-ratio, want een ratio klopt maar op één schermbreedte.
# De foto is versie 1 uit website/review/voorbereiding-ideeen-20260923/: een verhuizer die een smalle
# trap opmeet. Door ons gemaakt, dus met herkomst, en een staand onderwerp in een vak dat nu hoger is
# dan breed. Exporteren: node _werk/export-lijstplaat-trap.cjs
#
# Wat de huisvorm droeg, voor wie hem eraf haalt:
#  - .b-lijstplaat-geel__huis gaf met aspect-ratio 535.3/509.8 de HOOGTE van het beeldvak. Alleen de
#    clip-path weghalen laat een bijna vierkant vak achter dat nergens meer op slaat; kies bewust
#    een nieuwe verhouding.
#  - .b-lijstplaat-geel__beeld::before was het goudgele huis op 1.06 met de slagschaduw erop. Zonder
#    knipvorm wordt dat een goudgele rand om het beeld, en dat houdt het enige gele accent in deze
#    kolom vast. Haal je hem ook weg, dan is de kolom kleurloos.
#  - --huisvorm staat op .b-lijstplaat-geel en wordt door beide gebruikt. --huisje is iets ANDERS: dat is
#    het vage witte huis in de hoek van de plaat (.b-lijstplaat-geel__plaat::before) en dat hoort niet bij
#    het beeld; laat dat staan.
#  - het klembord hangt aan de PLAAT, niet aan het beeld, dus dat verschuift niet uit zichzelf. Wel
#    schuift het mee als de kolom korter wordt: gemeten 20 px omhoog bij 3:2.
#
# De dozenversie is niet weggegooid en blijft bruikbaar als hij erop terugkomt:
# _ai-beelden/archief/lijstplaat-dozen-20260923/ met master.png, de hoekpunten van beide doosvlakken,
# de lichtijking per doos en LEESMIJ.md. Opnieuw exporteren: node _werk/export-lijstplaat-dozen.cjs
#
# Wat nog wel geldt, want dat zit in het vak en niet in het onderwerp:
#  - eigen beeld, geen stockbeeld met onbekende mensen (design-notes A3), en geen header van een
#    andere pagina. Niet img/headers/kosten.webp (A3 wees die af), niet het oude inpakbeeld van de
#    home (dat was img/headers/werkwijze.webp, die bovenaan deze pagina staat), en niet de oude
#    header van /diensten/studentenverhuizing/ (twee onbekende mensen en een verzonnen merk).
#  - het onderwerp staat links van het midden en laag: de uitsnede begint op 25% links
#    (object-position in de CSS) en de huisvorm snijdt de bovenhoeken weg.
#  - gemeten op de gebouwde pagina loopt het huisje van 146 px (venster 360) tot 264 px (1600+).
#    Alles wat leesbaar moet zijn, moet op die maten de brandbook-ondergrenzen halen; een borstmerk
#    haalt dat nooit. Zie de tabel in het LEESMIJ hierboven.
#
# RONDE 4 (23-09-2026, zijn beeldinventaris): "img/voorbereiding-trap.webp: delete" en
# "img/voorbereiding-dozen.webp: keep". De dozenfoto blijft dus bestaan, maar hoort hier niet terug:
# dat is het onderwerp waarvan hij voor dit vak zei "add something more interesting than the box".
# In de plaats kwam versie 5 uit dezelfde ideeenronde: een verhuizer die kijkt of een kast door de
# deur past. Zelfde maat als de trapfoto, dus het vak verandert niet. Exporteren:
# node _werk/export-lijstplaat-kast.cjs
FOTO = ("/img/voorbereiding-kast.webp", 1200, 1030)

# RONDE 5 (28-09-2026): "de man op de foto moet realistischer, alsof hij eruit komt". De gebruiker koos
# ontwerp 09 "Diepe plaat" uit _ontwerpen/lijstplaat-uit-de-foto.html (vijftien ontwerpen, 00 = hoe het
# was). De verhuizer is met achtergrondverwijdering uit FOTO geknipt. Het bestand heeft PRECIES hetzelfde
# formaat als FOTO en de verhuizer staat op dezelfde pixels, zodat de twee beelden op elkaar vallen:
# binnen het kader zie je de foto, erbuiten alleen de verhuizer. Vervang je FOTO, maak dan ook deze
# uitsnede opnieuw op hetzelfde formaat, anders schuift hij los van zijn eigen foto.
# Bij de vingers van de opgeheven hand is de donkere rand van de kast met de hand weggehaald.
UITSNEDE = "/img/voorbereiding-kast-man.webp"

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
    # alt blijft leeg: de lijst ernaast zegt alles wat de foto laat zien, en de verhuizer is dezelfde foto.
    # De volgorde in het podium is de stapelvolgorde: de verhuizer met zijn slagschaduw onder de foto, de
    # foto op het kader geknipt, het glas (de schaduw van de verdieping) op de foto, en de verhuizer nog
    # een keer schoon bovenop, zodat hij voor de verdieping staat en niet erin.
    beeld = ""
    if opties.get("foto", True):
        uit = ctx.beeld(UITSNEDE, "", FOTO[1], FOTO[2], klasse=f"b-{NAAM}__uit")
        foto = ctx.beeld(FOTO[0], "", FOTO[1], FOTO[2], klasse=f"b-{NAAM}__foto")
        voor = ctx.beeld(UITSNEDE, "", FOTO[1], FOTO[2], klasse=f"b-{NAAM}__voor")
        beeld = (f'<span class="b-{NAAM}__beeld" aria-hidden="true"><span class="b-{NAAM}__kader"></span>'
                 f'<span class="b-{NAAM}__podium">{uit}{foto}<span class="b-{NAAM}__glas"></span>{voor}</span></span>')
    voorwerp = ""
    if opties.get("voorwerp", True):
        voorwerp = ctx.beeld(VOORWERP[0], "", VOORWERP[1], VOORWERP[2], klasse=f"b-{NAAM}__klembord", sizes="7.6rem",
                             srcset="/img/clay/klembord-144.webp 144w, /img/clay/klembord-240.webp 240w")
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
