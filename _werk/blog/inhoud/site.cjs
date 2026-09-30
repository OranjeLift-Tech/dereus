// Vaste gegevens van de blog. Bedrijfsgegevens volgen _werk/config.py; wijzigt daar iets, zet het dan ook hier.
// Geen namen van medewerkers: die kent de site nog niet (FEITEN["EIGENAAR"] en ["TEAM"] zijn leeg).
// De mensen op de blogfoto's zijn modellen (Pexels), geen medewerkers; daarom staat er nergens een naam bij.
module.exports = {
  naam: 'Verhuisbedrijf De Reus',
  kort: 'De Reus',
  plaats: 'Den Haag',
  tel: '085 000 5647',
  telHref: '+31850005647',
  whatsapp: '31850005647',
  mail: 'info@verhuisbedrijfdereus.nl',
  score: '4,9',   // Google, altijd zonder aantal (config.py GOOGLE_SCORE)
  google: 'https://www.google.com/search?q=reviews+voor+verhuisbedrijf+de+reus',

  // Eén schrijver: het team. Het avatar is het beeldmerk, geen foto van een persoon.
  auteur: {
    naam: 'Team De Reus',
    kort: 'De Reus',
    rol: 'Verhuisadviseurs en verhuizers',
    bio: 'Hier schrijven de verhuisadviseurs en verhuizers van Verhuisbedrijf De Reus op wat zij elke week meemaken, van de eerste offerte tot de laatste doos. Heeft u een vraag over uw eigen verhuizing? Bel of app gerust, dan denken we met u mee.',
  },

  // Wie een tip geeft. Beeld = uitsnede in blog/img/team/ (model, geen medewerker).
  tippers: {
    verhuizer: { label: 'Tip van onze verhuizers', uit: 'daan-uit', wie: 'De verhuizers van De Reus' },
    inpakker: { label: 'Tip van onze inpakkers', uit: 'youssef-uit', wie: 'De verhuizers van De Reus' },
    adviseur: { label: 'Tip van uw verhuisadviseur', uit: 'sanne-uit', wie: 'Uw verhuisadviseur bij De Reus' },
  },

  // volgorde = volgorde van de tegels; het voorwerp staat op de gele schijf van de tegel.
  // kop = de foto achter de paginakop van een artikel: een van de koppen van de site zelf (img/headers/),
  // zodat een artikel er net zo uitziet als de andere pagina's; positie zoals op de pagina die hem ook gebruikt.
  onderwerpen: {
    alles: { naam: 'Alle artikelen', ding: 'plant', h: '5.6rem' },
    inpakken: { naam: 'Inpakken', ding: 'tape', h: '4.4rem', kop: { src: '/img/headers/werkwijze.webp', w: 1600, h: 900, positie: '50% 34%' } },
    planning: { naam: 'Planning', ding: 'wekker', h: '4.6rem', kop: { src: '/img/headers/offerte-bedankt.webp', w: 1600, h: 900, positie: '50% 50%' } },
    kosten: { naam: 'Kosten', ding: 'munten', h: '4.2rem', kop: { src: '/img/headers/kosten.webp', w: 1600, h: 900, positie: '50% 30%' } },
    gezin: { naam: 'Gezin & dieren', ding: 'hond', h: '5.3rem', kop: { src: '/img/headers/zakelijk.webp', w: 1448, h: 815, positie: '50% 35%' } },
    meubels: { naam: 'Meubels', ding: 'stoel', h: '5.5rem', kop: { src: '/img/headers/particulier.webp', w: 1448, h: 815, positie: '50% 45%' } },
    zakelijk: { naam: 'Zakelijk & opslag', ding: 'doos', h: '4.3rem', kop: { src: '/img/headers/opslag.webp', w: 1448, h: 815, positie: '50% 40%' } },
  },
};
