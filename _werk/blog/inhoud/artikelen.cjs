// De artikelen van de blog. Nieuwste eerst; het eerste artikel met uitgelicht: true staat groot bovenaan.
// tekst(h) geeft de HTML van het artikel. h2-koppen krijgen vanzelf een id en komen in de inhoudsopgave.
// De bouwstenen (h.tip, h.stappen, h.tabel, ...) staan in bouw-blog.cjs.
//
// Huisregels van de site gelden ook hier (website/content/kosten.md, werkwijze.md):
// - "u", geen "je"; geen gedachtestreepjes.
// - Geen bedragen, geen vaste eindprijs, geen "volledig verzekerd", geen "zonder verrassingen".
// - Geen feiten die in _werk/config.py FEITEN nog None zijn (opslaglocatie en -termijn, avond en weekend,
//   dozen ophalen). Wat de site wel zegt: offerte gratis en vrijblijvend, binnen 24 uur gebeld, één vaste
//   verhuisadviseur, geen voorrijkosten, betalen op de verhuisdag, all-in of regieprijs.
module.exports = [
  {
    slug: 'verhuisdozen-inpakken',
    uitgelicht: true,
    titel: 'Verhuisdozen inpakken zoals een verhuizer het doet',
    kort: 'Zwaar onder, licht boven, en nooit een doos die u zelf niet kunt tillen. De vuistregels van onze verhuizers, plus een schatter voor het aantal dozen.',
    lead: 'Een goed ingepakte doos valt op de verhuisdag niemand op: hij gaat de wagen in, komt er heel weer uit en staat in de goede kamer. Zo pakken onze verhuizers het aan.',
    onderwerp: 'inpakken', datum: '2026-09-24', leestijd: 8,
    foto: 'verhuisdozen-inpakken', alt: 'Verhuizer draagt een stapel verhuisdozen door een lichte kamer',
    zoek: 'dozen verhuisdozen tape etiket breekbaar servies eerste nacht',
    kopdingen: { 'zwaar-onder-licht-boven': { ding: 'dozen', h: '15rem' } },   // twee De Reus-dozen gestapeld (img/contact-echt), voorwerp op een goudgele schijf rechts van de kop van deel 02
    tekst: (h) => `
<p class="intro">Onze verhuizers tillen elke week heel wat dozen. De meeste zijn prima, een paar scheuren open op de trap. Het verschil zit bijna nooit in de doos zelf, maar in hoe hij gevuld is. Hieronder leest u hoe wij het doen, zodat uw dozen heel aankomen.</p>

<h2>Begin met de juiste dozen</h2>
<p>Gebruik geen dozen van de supermarkt. Die zijn gemaakt voor één rit met lichte spullen en zakken in zodra er boeken in gaan. Verhuisdozen hebben dubbelgolf karton en handgrepen, en ze zijn allemaal even groot. Daardoor staan ze recht en stevig gestapeld in de wagen.</p>
${h.tabelmet(['Doos', 'Inhoud', 'Maximaal', 'Waarvoor'], [
  ['Boekendoos', '35 liter', '15 kg', 'Boeken, papieren, blikken, gereedschap'],
  ['Verhuisdoos', '50 liter', '20 kg', 'Keukenspullen, speelgoed, schoenen, decoratie'],
  ['Serviesdoos', '45 liter, met vakken', '15 kg', 'Borden, glazen, kopjes'],
  ['Garderobedoos', '100 liter, met stang', '12 kg', 'Kleding die aan de hanger blijft'],
], { ding: 'tape', h: '5.2rem', label: 'Hoeveel dozen?', tekst: 'Twijfelt u hoeveel dozen u nodig heeft en waar u ze vandaan haalt? Vraag het bij uw offerte. Uw verhuisadviseur denkt met u mee.', knop: 'Offerte aanvragen' })}

<h2>Zwaar onder, licht boven</h2>
<p>Dit is de gouden regel. Zware spullen gaan in kleine dozen, lichte spullen in grote. Een grote doos vol boeken weegt al snel dertig kilo, en daar scheurt elke bodem van.</p>
${h.stappen([
  ['Plak de bodem kruislings dicht', 'Eén strook tape in het midden is niet genoeg. Plak een kruis en daarna een strook langs beide randen, dan draagt de bodem ook de zware dozen.'],
  ['Zware spullen onderin', 'Boeken, borden en blikken gaan plat op de bodem. Zo ligt het gewicht laag en kantelt de doos niet in uw armen.'],
  ['Vul elk gat op', 'Een doos die rammelt, gaat kapot. Prop kranten, theedoeken of handdoeken in elke lege hoek.'],
  ['Niet boller dan de rand', 'De deksel moet plat sluiten. Een bolle doos kunt u niet stapelen en hij drukt de doos eronder in.'],
  ['Til hem op voor u hem dichtplakt', 'Kunt u hem niet makkelijk dragen, haal er dan iets uit. Wij tillen hem ook, maar uw rug telt mee als u zelf nog iets verplaatst.'],
  ['Schrijf op twee zijkanten', 'Tape over de naad, en daarna de kamer en de inhoud op twee zijkanten. Niet op de deksel: die ziet niemand meer als de dozen gestapeld staan.'],
])}
${h.tip('verhuizer', 'Twijfelt u of een doos te zwaar is? Til hem tot kniehoogte en tel tot drie. Voelt dat al zwaar, dan is hij op de trap echt te zwaar. Maak er dan twee dozen van.')}

<h2>Breekbaar: vullen tot niets meer schuift</h2>
<p>Borden zet u op hun kant, als in een afwasrek. Plat gestapeld drukken ze op elkaar en breekt de onderste bij de eerste drempel. Glazen gaan met de opening naar beneden, elk in een eigen vel papier.</p>
${h.fotomet('mok-inpakken', 'Handen pakken een mok in, in een doos vol opvulmateriaal', 'Elk kopje in een eigen vel, en de lege ruimte vol opvulmateriaal. Schud de doos zachtjes: hoort u iets, dan moet er meer in.', { etiket: 'Breekbaar &uarr;', label: 'Op de doos', tekst: '<p>Gebruik voor breekbare spullen de kleinere dozen en schrijf er in grote letters BREEKBAAR op, met een pijl naar boven. Dan weten de verhuizers dat die doos bovenop hoort, en niet onder een stapel boeken.</p>' })}
${h.citaat('Een doos die rammelt, is een doos die breekt. Schud elke doos met breekbare spullen even voor u hem dichtplakt.', 'De verhuizers van De Reus')}

<h2>Etiketten die de verhuizers echt lezen</h2>
<p>Op de verhuisdag hebben de verhuizers per doos een paar seconden. Zet op elke doos in welke kamer hij hoort, dan zetten wij hem meteen op de goede plek. Een goed etiket heeft:</p>
<ul>
  <li>de kamer in het nieuwe huis, in hoofdletters: SLAAPKAMER 2, niet ‘boven’;</li>
  <li>een korte inhoud, zodat u later weet wat u zoekt;</li>
  <li>BREEKBAAR en een pijl naar boven, als dat nodig is;</li>
  <li>een nummer, zodat u kunt nagaan of alles er is.</li>
</ul>
<p>Handig: geef elke kamer een eigen kleur tape. Plak een stukje van die kleur op de deur van de kamer in het nieuwe huis, dan hoeft niemand te zoeken.</p>
${h.afvink('inpakken-laatste-check', 'Laatste check voor de verhuisdag', [
  'Alle dozen kruislings dichtgeplakt',
  'Kamer en inhoud op twee zijkanten geschreven',
  'Breekbare dozen gemarkeerd, met een pijl naar boven',
  'Geen doos zwaarder dan u zelf kunt tillen',
  'Eerste-nachtdoos apart gezet, die gaat met u mee',
  'Lades leeg of dichtgeplakt, boekenkasten leeg',
  'Snoeren en schroefjes per meubel in een zakje, vastgeplakt aan het meubel',
])}

<h2>De eerste-nachtdoos</h2>
<p>Pak één doos in die u zelf in de auto meeneemt: toiletpapier, een waterkoker, koffie of thee, opladers, medicijnen, een handdoek, schoon beddengoed en een schaar om de andere dozen open te maken. Paspoorten, sleutels en andere waardevolle spullen houdt u ook zelf bij de hand.</p>

<h2>Hoeveel dozen heeft u nodig?</h2>
<p>Een ruwe schatting: iemand alleen in een appartement komt uit op 25 tot 35 dozen, een gezin in een eengezinswoning op 60 tot 90. Vul hieronder uw eigen huis in voor een schatting op maat.</p>
${h.schatter()}
<p>Neem liever een paar dozen te veel dan te weinig. Een halve kamer die op de verhuisdag nog ingepakt moet worden, kost meer tijd dan een lege doos.</p>
${h.aanbod({ titel: 'Liever laten inpakken?', tekst: 'U kunt alles zelf inpakken en ons alleen het zware werk laten doen, of wij pakken voor u in. En weer uit, als u dat wilt. U wijst aan wat mee moet, wij doen de rest.', knop: 'Offerte aanvragen' })}

<h2>Veelgestelde vragen over inpakken</h2>
${h.vragen([
  ['Hoe lang van tevoren begin ik met inpakken?', 'Begin twee tot drie weken van tevoren met alles wat u niet dagelijks gebruikt: boeken, decoratie, kleding van het andere seizoen. De keuken en de badkamer volgen in de laatste week.'],
  ['Mogen kasten gevuld blijven?', 'Ladekasten met kleding mogen soms dicht, als ze goed zijn afgeplakt en de kast stevig is. Boekenkasten en vitrinekasten moeten altijd leeg. Twijfelt u, vraag het dan aan uw verhuisadviseur.'],
  ['Wat neem ik beter zelf mee?', 'Geld, sieraden, paspoorten, sleutels, belangrijke papieren en medicijnen. Gasflessen, verf en brandbare vloeistoffen meldt u vooraf: stoffen die niet gemeld zijn, nemen wij niet mee.'],
  ['Pakken jullie ook voor mij in?', 'Ja. U kunt alles zelf inpakken en ons alleen het zware werk laten doen, of wij pakken voor u in. U bespreekt het met uw verhuisadviseur, dan staat het in de offerte.'],
])}`,
  },

  {
    slug: 'verhuischecklist',
    titel: 'Verhuischecklist: acht weken tot de sleutel',
    kort: 'Wat regelt u wanneer? Van huur opzeggen en adreswijzigingen tot de laatste meterstanden. Een planning die u gewoon kunt afvinken.',
    lead: 'De meeste verhuisstress komt van dingen die op het laatste moment opduiken. Met deze planning heeft u alles op tijd geregeld, week voor week.',
    onderwerp: 'planning', datum: '2026-09-18', leestijd: 6,
    foto: 'verhuischecklist', alt: 'Vrouw leunt vermoeid op een verhuisdoos tussen stapels dozen',
    zoek: 'checklist planning lijst weken adreswijziging meterstanden parkeervergunning ontheffing',
    tekst: (h) => `
<p class="intro">Onze verhuisadviseurs zien het vaak: de verhuizing zelf gaat goed, maar de internetaansluiting is vergeten of de oude huur loopt een maand te lang door. Met deze lijst overkomt u dat niet. Vink af wat klaar is; uw browser onthoudt het.</p>

<h2>Acht tot zes weken van tevoren</h2>
${h.afvink('checklist-acht', 'Acht tot zes weken', [
  'Huur opzeggen of de overdrachtsdatum vastleggen',
  'Offertes van verhuizers aanvragen en er één kiezen',
  'Vrij nemen voor de verhuisdag en de dag erna',
  'Internet, energie en verzekeringen verhuizen of opzeggen',
  'Beginnen met opruimen: wat gaat er niet mee?',
])}

<h2>Vier weken van tevoren</h2>
${h.afvink('checklist-vier', 'Vier weken', [
  'Adreswijziging doorgeven aan de gemeente (dat kan vier weken vooraf)',
  'Post laten doorsturen naar het nieuwe adres',
  'School, huisarts, tandarts en werkgever inlichten',
  'Dozen regelen en beginnen met inpakken',
  'Parkeerplek of ontheffing voor de verhuiswagen aanvragen',
])}
${h.tip('adviseur', 'Vraag de ontheffing voor de verhuiswagen zo vroeg mogelijk aan. In sommige gemeenten duurt het een paar weken, en zonder ontheffing staat de wagen soms een straat verderop. Dat kost op de verhuisdag uren.')}

<h2>De laatste week</h2>
${h.afvink('checklist-week', 'De laatste week', [
  'Koelkast en vriezer leegmaken en ontdooien',
  'Eerste-nachtdoos inpakken',
  'Kasten leegmaken en lades dichtplakken',
  'Gas laten afkoppelen door een installateur',
  'Waardevolle spullen en papieren apart leggen',
  'Opladers, sleutels en medicijnen in één tas',
])}

<h2>Op de verhuisdag</h2>
${h.afvink('checklist-dag', 'De verhuisdag', [
  'Meterstanden noteren en fotograferen, in het oude én het nieuwe huis',
  'Een laatste ronde door alle kasten, de zolder en de schuur',
  'Kinderen en huisdieren bij iemand onderbrengen',
  'Sleutels overdragen',
])}
<p>Wat er op de verhuisdag zelf gebeurt, van aankomst tot uitladen en opbouwen, leest u op <a href="/werkwijze/">onze werkwijze</a>. Liever op papier? Print deze pagina: de navigatie en de knoppen vallen weg, alleen de lijsten blijven over.</p>`,
  },

  {
    slug: 'wat-kost-een-verhuizing',
    titel: 'Wat kost een verhuizing? Zo komt de prijs tot stand',
    kort: 'All-in of regieprijs, verhuislift of trap, wel of niet inpakken. Waar het bedrag uit bestaat en waar u zelf op kunt besparen.',
    lead: 'Een verhuizing kost geen vast bedrag, maar de opbouw is wel altijd hetzelfde. Kent u die, dan kunt u offertes vergelijken en ziet u waar u kunt besparen.',
    onderwerp: 'kosten', datum: '2026-09-12', leestijd: 6,
    foto: 'wat-kost-een-verhuizing', alt: 'Stel rekent aan de keukentafel met een rekenmachine en papieren',
    zoek: 'kosten prijs tarief offerte besparen verhuislift all-in regieprijs voorrijkosten',
    tekst: (h) => `
<p class="intro">De vraag die wij het vaakst krijgen: wat kost het? Het eerlijke antwoord is dat het afhangt van hoeveel spullen u heeft, de afstand, hoe bereikbaar beide adressen zijn en wat u zelf doet. Daarom krijgt u bij De Reus altijd een offerte op maat, gratis en vrijblijvend.</p>

<h2>Waar de prijs uit bestaat</h2>
${h.stappen([
  ['Hoeveel er mee moet', 'Een studio is sneller verhuisd dan een eengezinswoning. Het volume bepaalt hoe groot de wagen moet zijn en hoeveel verhuizers er meegaan.'],
  ['De afstand', 'Binnen Den Haag of naar de andere kant van het land. Binnen de stad telt vooral de tijd, verder weg komen er rijuren bij.'],
  ['De bereikbaarheid', 'Een smalle trap, een hoge verdieping of weinig ruimte om te parkeren kost meer tijd.'],
  ['Wat u zelf doet', 'Pakt u zelf in, of doen wij dat? Moeten meubels uit elkaar en weer in elkaar?'],
  ['Extra diensten', 'Zoals een verhuislift of tijdelijke opslag.'],
])}

<h2>All-in prijs of regieprijs?</h2>
${h.tabel(['Soort prijs', 'Wat u betaalt'], [
  ['All-in prijs', 'Eén vast bedrag voor de verhuizing zoals die in de offerte staat.'],
  ['Regieprijs', 'De tijd die de verhuizing werkelijk kost.'],
])}
<p>U betaalt geen voorrijkosten: u betaalt voor de verhuizing zelf, niet voor de rit naar uw adres. En u betaalt op de verhuisdag, tenzij we samen iets anders afspreken.</p>
${h.tip('adviseur', 'Meld vooraf alles wat mee moet, ook de zolder, de schuur en die ene kast die niet uit elkaar kan. Hoe vollediger uw informatie, hoe beter de offerte past. Moet er op de verhuisdag meer mee dan afgesproken, dan wordt dat als meerwerk verrekend.')}

<h2>Wat kost per woning de meeste tijd?</h2>
${h.tabel(['Woning', 'Waar de tijd in zit'], [
  ['Studio of appartement', 'Weinig volume, maar vaak een trap of een smal portiek. Of er een lift is en hoe hoog u woont, bepaalt hoeveel tijd het dragen kost.'],
  ['Eengezinswoning', 'Meer kamers, meer dozen en vaak meubels die uit elkaar moeten. Het inpakken en de montage wegen hier zwaarder mee.'],
  ['Groot huis of kantoor', 'Veel volume en vaak meerdere verdiepingen. Een goede planning vooraf en de bereikbaarheid voor de deur maken hier het verschil.'],
])}

<h2>Zo bespaart u echt</h2>
<ul>
  <li><strong>Ruim vooraf op.</strong> Alles wat niet mee hoeft, scheelt tijd en ruimte in de wagen.</li>
  <li><strong>Pak zelf in</strong>, en laat alleen het zware werk aan ons over.</li>
  <li><strong>Zorg dat de wagen voor de deur kan staan.</strong> Elke meter lopen kost tijd. Vraag op tijd een ontheffing aan.</li>
  <li><strong>Vergelijk offertes op wat erin staat.</strong> Een lage prijs zonder montage, verhuislift of parkeerplek wordt op de verhuisdag vaak alsnog duurder.</li>
</ul>
<p>Alles over de prijsopbouw, ook voor opslag, een verhuislift, montage en woningontruiming, leest u op <a href="/kosten/">wat kost een verhuisbedrijf</a>.</p>`,
  },

  {
    slug: 'verhuizen-met-kinderen',
    titel: 'Verhuizen met kinderen: zo blijft het rustig in huis',
    kort: 'Kinderen merken alles van een verhuizing. Met een paar vaste afspraken voelen ze zich sneller thuis in het nieuwe huis.',
    lead: 'Voor kinderen is een verhuizing groot nieuws, ook als ze er blij mee zijn. Een beetje voorbereiding scheelt veel tranen, bij hen en bij u.',
    onderwerp: 'gezin', datum: '2026-09-05', leestijd: 5,
    foto: 'verhuizen-met-kinderen', alt: 'Moeder, vader en kind dragen samen dozen een nieuwe keuken in',
    zoek: 'kinderen gezin kinderkamer school verhuisdag',
    tekst: (h) => `
<p class="intro">Wij verhuizen veel gezinnen, en de kinderen die weten wat er gebeurt, vinden de dag het leukst. Ze mogen helpen, ze weten waar hun spullen blijven en ze slapen de eerste nacht in hun eigen bed.</p>

<h2>Vertel het op tijd</h2>
<p>Jonge kinderen hebben weinig aan ‘over drie maanden’. Vertel het ongeveer een maand van tevoren en maak het concreet: laat foto’s van het nieuwe huis zien, of ga er een keer kijken, ook als het nog leeg is.</p>

<h2>Laat ze zelf een doos inpakken</h2>
<p>Geef elk kind een eigen doos voor de liefste spullen. Laat ze hem versieren en er hun naam op schrijven. Die doos gaat als laatste de wagen in en komt er als eerste weer uit.</p>
${h.citaat('Die doos gaat als laatste de wagen in, en komt er als eerste weer uit.', 'De verhuizers van De Reus')}
${h.tip('verhuizer', 'Laat u ons de meubels weer opbouwen? Begin dan met de kinderkamer: bed, kast, de doos met knuffels. Dan hebben de kinderen een plek die al af is, terwijl de rest nog in dozen staat.')}

<h2>De verhuisdag zelf</h2>
<ul>
  <li>Laat jonge kinderen die dag logeren bij opa en oma of bij vrienden.</li>
  <li>Oudere kinderen kunnen helpen: dozen tellen, de kamers aanwijzen, de verhuizers de weg wijzen.</li>
  <li>Houd de gewone dingen vast: op dezelfde tijd eten, hetzelfde ritueel voor het slapengaan.</li>
</ul>

<h2>De eerste weken</h2>
<p>Richt de kinderkamer zoveel mogelijk in zoals de oude. Nieuw mag later. Loop samen een rondje door de buurt: waar is de speeltuin, waar is de school, waar is de bakker?</p>`,
  },

  {
    slug: 'verhuizen-met-huisdieren',
    titel: 'Verhuizen met uw hond of kat zonder gedoe',
    kort: 'Een open voordeur, vreemde mensen en overal dozen. Zo houdt u uw huisdier rustig en veilig op de verhuisdag.',
    lead: 'Voor een hond of kat is de verhuisdag vooral onrustig: open deuren, zware stappen en een huis dat leeg raakt. Met deze tips blijft uw dier kalm.',
    onderwerp: 'gezin', datum: '2026-08-28', leestijd: 5,
    foto: 'verhuizen-met-huisdieren', alt: 'Stel knuffelt met hun witte hond tussen de verhuisdozen',
    zoek: 'hond kat huisdieren dier chip',
    tekst: (h) => `
<p class="intro">Onze verhuizers zijn dol op dieren, maar op de verhuisdag komen ze ze liever niet tegen. Niet omdat ze in de weg lopen, maar omdat een open voordeur voor een kat een uitnodiging is. Dieren verhuizen wij zelf niet, dus regel voor die dag een goede plek.</p>

<h2>Voor de verhuizing</h2>
<ul>
  <li>Zet de reismand of bench een week van tevoren al open neer, met een deken erin.</li>
  <li>Houd voer, riemen en het vaste speeltje apart, in een eigen tas.</li>
  <li>Geef het nieuwe adres door aan de chipregistratie en de dierenarts.</li>
</ul>

<h2>Op de verhuisdag</h2>
<p>De beste plek voor uw huisdier is die dag niet thuis. Laat een hond logeren bij iemand die hij kent. Een kat kan de hele dag in één lege kamer met de deur dicht, met water, voer en de kattenbak.</p>
${h.citaat('Een open voordeur is voor een kat een uitnodiging. Geef uw dier die dag een eigen, rustige plek.', 'De verhuizers van De Reus')}
${h.tip('inpakker', 'Hang een briefje op de deur van de kamer waar uw kat zit. Wij slaan die kamer dan over tot het allerlaatst. Dan hoeft de deur maar één keer open.')}

<h2>In het nieuwe huis</h2>
<p>Laat een kat de eerste week binnen. Begin met één kamer en maak het huis stukje bij beetje groter. Een hond heeft baat bij een lange wandeling door de nieuwe buurt, zodat hij de geuren leert kennen.</p>`,
  },

  {
    slug: 'bank-de-trap-af',
    titel: 'Een bank de trap af: waarom u dat beter niet zelf doet',
    kort: 'Een bank is groot, zwaar en past bijna nooit recht door een trapgat. Zo pakken wij zware meubels aan, en wanneer een verhuislift slimmer is.',
    lead: 'Een bank, een kast of een wasmachine: bij zware meubels gaat het vaakst iets mis. Met uw rug, of met een kras in de nieuwe muur.',
    onderwerp: 'meubels', datum: '2026-08-21', leestijd: 4,
    foto: 'bank-de-trap-af', alt: 'Twee verhuizers dragen een groene bank een huis in',
    zoek: 'bank meubels trap verhuislift zwaar kast wasmachine piano',
    tekst: (h) => `
<p class="intro">Onze verhuizers tillen elke week banken. Het gewicht is zelden het probleem, de vorm wel. Een bank past alleen door een smalle trap als u weet hoe hij gedraaid moet worden.</p>

<h2>Meten voor u tilt</h2>
<p>Meet de breedte van de trap, van de deuren en van de draai op de overloop. Meet de bank op zijn smalste punt, meestal de diepte. Past het op papier niet, dan past het in het echt ook niet, hoe hard u ook duwt.</p>
${h.citaat('Past het op papier niet, dan past het in het echt ook niet. Hoe hard u ook duwt.', 'De verhuizers van De Reus')}

<h2>Zo gaat een bank de trap af</h2>
${h.stappen([
  ['Kussens en poten eraf', 'Alles wat los kan, gaat los. Een bank zonder poten is vaak net die paar centimeter smaller.'],
  ['Rechtop, niet plat', 'Een bank gaat meestal rechtop door een trapgat, met de zitting naar de muur.'],
  ['De sterkste onderaan', 'Wie onderaan staat, draagt het gewicht. Wie bovenaan staat, stuurt en zegt wanneer er gestopt wordt.'],
  ['Dekens om de hoeken', 'Zo blijft de bank heel, en de muur ook.'],
])}
${h.tip('verhuizer', 'Onze regel: moet een meubel drie keer gedraaid worden, dan stoppen we en kijken we naar de verhuislift. Dat is sneller dan een kapotte trapleuning en een kras in uw nieuwe behang.')}

<h2>Wanneer een verhuislift?</h2>
<p>Vanaf de tweede verdieping zonder lift, bij smalle trappen en bij meubels die niet uit elkaar kunnen, is een verhuislift sneller en veiliger. De lift zet alles via het raam of het balkon direct bij de wagen. Of een lift nodig is, bekijkt uw verhuisadviseur samen met u; het staat dan in de offerte. Meer leest u bij <a href="/diensten/#verhuislift">verhuizen met de verhuislift</a>.</p>`,
  },

  {
    slug: 'kantoorverhuizing-zonder-stilstand',
    titel: 'Kantoorverhuizing: zo ligt uw bedrijf geen dag stil',
    kort: 'Vrijdag de deur dicht, maandag gewoon aan het werk. Zo plant u een kantoorverhuizing zonder dat er een dag werk verloren gaat.',
    lead: 'Een kantoor verhuizen is vooral plannen. Als iedereen weet wat er van hem verwacht wordt, staat maandagochtend elke computer weer aan.',
    onderwerp: 'zakelijk', datum: '2026-08-14', leestijd: 6,
    pop: { maat: { z: 1.76, x: 0, y: 42 }, zij: [0, 30] },   // rechts 30 %: de kop van de man valt er helemaal in, de vrouw rechts (kop afgesneden in de foto) blijft weg
    foto: 'kantoorverhuizing-in-een-weekend', alt: 'Twee collega’s plakken een label op een doos met het opschrift office',
    zoek: 'kantoor zakelijk bedrijf werkplek it archief weekend',
    tekst: (h) => `
<p class="intro">Bij een kantoorverhuizing telt elk uur dat er niet gewerkt kan worden. Daarom begint een goede zakelijke verhuizing met een plan dat vooraf met iedereen gedeeld is. Wanneer de verhuizing het best past, bespreekt u met uw verhuisadviseur.</p>

<h2>Begin met een plattegrond</h2>
<p>Geef elke werkplek in het nieuwe pand een nummer. Hetzelfde nummer komt op de dozen, het bureau, de stoel en de computer. Zo weet iedereen, ook wie het pand nog nooit heeft gezien, waar alles hoort.</p>
${h.citaat('Vrijdag de deur dicht, maandag gewoon aan het werk.', 'Uw verhuisadviseur bij De Reus')}

<h2>Een draaiboek voor één weekend</h2>
${h.stappen([
  ['Vrijdagmiddag: inpakken', 'Iedereen pakt zijn eigen bureau in, één of twee dozen per persoon, met het nummer van de nieuwe werkplek erop.'],
  ['Vrijdagavond: IT koppelt af', 'Computers en schermen worden losgekoppeld en per werkplek in een krat gezet.'],
  ['De verhuizing', 'Meubels, kratten en dozen gaan in één of meer ritten naar het nieuwe pand, meteen op hun plek.'],
  ['Aansluiten en testen', 'IT sluit alles aan en test elke werkplek, zodat maandagochtend iedereen kan beginnen.'],
])}
${h.tip('adviseur', 'Laat elke medewerker één doos inpakken met een label met zijn werkplek. Zo zet het team maandagochtend niet eerst een uur dozen rond.')}

<h2>Archief en opslag</h2>
<p>Niet alles hoeft mee naar het nieuwe pand. Een oud archief of meubels voor later kunnen tijdelijk in de opslag. Omdat wij de verhuizing en de opslag samen regelen, staat alles in één offerte. Meer over <a href="/diensten/#zakelijk">zakelijke verhuizingen</a>.</p>`,
  },

  {
    slug: 'opslag-tijdens-verbouwing',
    titel: 'Tijdelijk opslaan tijdens een verbouwing: zo werkt het',
    kort: 'Een nieuwe keuken, een nieuwe vloer of een huis dat nog niet klaar is. Zo slaat u uw spullen een paar weken of maanden op.',
    lead: 'Tussen twee huizen in, of midden in een verbouwing: soms moeten uw spullen even ergens anders staan. Zo gaat opslag bij De Reus.',
    onderwerp: 'zakelijk', datum: '2026-08-07', leestijd: 5,
    foto: 'opslag-tijdens-verbouwing', alt: 'Stel stapelt verhuisdozen tot aan het plafond',
    banden: ['opslag', 'kantoor', 'vast', 'doos'],   // 30-09: eigen foto sneed de armen af; eerste band = sitefoto opslag
    zoek: 'opslag verbouwing bewaren tijdelijk nieuwbouw',
    tekst: (h) => `
<p class="intro">Een verbouwing loopt bijna altijd uit, en een nieuw huis is niet altijd op tijd klaar. Opslag geeft u die ruimte: uw spullen staan ergens anders, en u hoeft niet op een matras tussen de dozen te slapen.</p>

<h2>Wanneer opslag handig is</h2>
<ul>
  <li><strong>De data sluiten niet aan.</strong> U moet uit uw oude huis, maar de sleutel van het nieuwe huis komt pas later.</li>
  <li><strong>U gaat verbouwen of schilderen.</strong> Een lege kamer werkt makkelijker.</li>
  <li><strong>U woont tijdelijk kleiner</strong>, bijvoorbeeld tussen twee huizen in of bij familie.</li>
  <li><strong>Nieuwbouw is nog niet klaar.</strong> Loopt de oplevering uit, dan hoeft uw verhuizing niet te wachten.</li>
</ul>

<h2>Zo werkt het</h2>
${h.stappen([
  ['Wij pakken in, als u dat wilt', 'Net als bij een gewone verhuizing. Zo is alles goed beschermd tot het weer naar uw nieuwe adres gaat.'],
  ['Wij halen uw spullen op', 'Met dezelfde verhuizers en dezelfde zorg als op een verhuisdag.'],
  ['Uw spullen gaan in de opslag', 'Tot het werk klaar is of de sleutel er is.'],
  ['Wij brengen alles naar uw nieuwe adres', 'Wanneer u zover bent. Eén aanspreekpunt: uw verhuisadviseur.'],
])}

<h2>Wat mag er wel en niet in?</h2>
<p>Meubels, dozen, fietsen en witgoed mogen gewoon mee. Eten, planten, verf en brandbare spullen niet. Maak de koelkast en de wasmachine van tevoren schoon en droog, anders ruikt het na drie maanden niet fris.</p>
${h.tabel(['Mag in de opslag', 'Mag niet in de opslag'], [
  ['Meubels en dozen', 'Eten'],
  ['Fietsen', 'Planten'],
  ['Witgoed, schoon en droog', 'Verf en brandbare spullen'],
])}
${h.tip('inpakker', 'Maak een lijst van wat in welke doos zit, en neem er een foto van. Dan weet u precies waar uw winterjassen staan, ook als ze een paar maanden in de opslag staan.')}

<h2>Wat kost het?</h2>
<p>Dat hangt af van hoeveel u opslaat en hoe lang. Omdat wij de verhuizing en de opslag samen regelen, staat alles in één offerte. Meer leest u bij <a href="/kosten/#opslag">wat kost opslag van uw inboedel</a>.</p>`,
  },

  {
    slug: 'breekbaar-inpakken',
    titel: 'Servies, glas en spiegels: breekbaar inpakken in vijf stappen',
    kort: 'Borden op hun kant, glazen met de opening naar beneden en spiegels tussen twee platen karton. Zo komt alles heel aan.',
    lead: 'Er gaat bij een verhuizing zelden veel kapot, maar als het gebeurt, is het bijna altijd servies of glas. Met deze vijf stappen voorkomt u dat.',
    onderwerp: 'inpakken', datum: '2026-08-01', leestijd: 5,
    foto: 'breekbaar-inpakken', alt: 'Vrouw pakt kleding en spullen in, tussen open verhuisdozen',
    zoek: 'breekbaar servies glas spiegel schilderij kunst inpakken',
    tekst: (h) => `
<p class="intro">Breekbaar inpakken is geen kunst, maar het kost wel tijd. Neem er een avond voor, zet een film aan en doe het goed: wat stevig ingepakt is, komt heel aan.</p>

<h2>Vijf stappen voor servies en glas</h2>
${h.stappen([
  ['Een laag proppen op de bodem', 'Zo staat niets direct op het karton, en vangt de bodem de klappen op.'],
  ['Borden op hun kant', 'Elk bord in een vel papier, rechtop naast elkaar, als in een afwasrek.'],
  ['Glazen ondersteboven', 'Met de opening naar beneden, elk in een eigen vel. Stop ook papier in het glas.'],
  ['Opvullen tot niets meer schuift', 'Schud zachtjes aan de doos. Hoort u iets, dan moet er meer papier in.'],
  ['Markeren', 'BREEKBAAR in grote letters, een pijl naar boven, en nooit iets zwaars bovenop.'],
])}
${h.tip('inpakker', 'Gebruik geen kranten voor wit servies: de inkt geeft af. Blanco inpakpapier kost weinig en scheelt u een middag afwassen in het nieuwe huis.')}

<h2>Spiegels en schilderijen</h2>
<p>Plak een kruis van tape over het glas; breekt het toch, dan blijven de scherven op hun plek. Zet de spiegel tussen twee platen karton, en vervoer hem rechtop, nooit plat.</p>
${h.citaat('Een spiegel gaat rechtop de wagen in, tussen twee platen karton. Nooit plat.', 'De verhuizers van De Reus')}

<h2>Wat u beter aan ons overlaat</h2>
<ul>
  <li>Kunst en antiek.</li>
  <li>Grote spiegels en glazen tafelbladen.</li>
  <li>Lampen van glas en kroonluchters.</li>
</ul>
<p>Noem ze in uw aanvraag. Dan houden wij er in de offerte en op de verhuisdag rekening mee.</p>`,
  },
];
