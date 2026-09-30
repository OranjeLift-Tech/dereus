# Beeldbronnen

Alle foto's komen van Pexels (Pexels-licentie: gratis te gebruiken, ook commercieel, naamsvermelding niet verplicht). Opgehaald op 30-09-2026 via `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?w=1400` (hero en team op w=2600).

| Bestand in assets/img | Pexels-id | Pagina |
|---|---|---|
| blog/verhuisdozen-inpakken | 7203789 | https://www.pexels.com/photo/7203789/ |
| blog/verhuischecklist | 7464466 | https://www.pexels.com/photo/7464466/ |
| blog/wat-kost-een-verhuizing | 6964363 | https://www.pexels.com/photo/6964363/ |
| blog/verhuizen-met-kinderen | 7415053 | https://www.pexels.com/photo/7415053/ |
| blog/verhuizen-met-huisdieren | 5495050 | https://www.pexels.com/photo/5495050/ |
| blog/bank-de-trap-af | 7464406 | https://www.pexels.com/photo/7464406/ |
| blog/kantoorverhuizing-in-een-weekend | 7217852 | https://www.pexels.com/photo/7217852/ |
| blog/opslag-tijdens-verbouwing | 7203783 | https://www.pexels.com/photo/7203783/ |
| blog/breekbaar-inpakken | 7203815 | https://www.pexels.com/photo/7203815/ |
| blog/verhuizers-kop, team/daan*, team/youssef* | 7464703 | https://www.pexels.com/photo/7464703/ |
| blog/verhuizer-bus | 7843960 | https://www.pexels.com/photo/7843960/ |
| blog/verhuizer-wagen | 6699421 | https://www.pexels.com/photo/6699421/ |
| team/sanne* | 3791617 | https://www.pexels.com/photo/3791617/ |
| sfeer/bus-straat | 5025669 | https://www.pexels.com/photo/5025669/ |
| sfeer/mok-inpakken | 7464407 | https://www.pexels.com/photo/7464407/ |
| voorwerp/plant | 12684656 | https://www.pexels.com/photo/12684656/ |
| voorwerp/tape | 5691615 | https://www.pexels.com/photo/5691615/ |
| voorwerp/wekker | 18911015 | https://www.pexels.com/photo/18911015/ |
| voorwerp/rekenmachine | 7580753 | https://www.pexels.com/photo/7580753/ | (niet meer in gebruik sinds 30-09-2026)
| voorwerp/munten | Unsplash OApHds2yEGQ (Ibrahim Rifath) | zelfde uitsnede als img/contact-echt/munten-*, zie img/LICENTIES.md |
| voorwerp/hond | 18956761 | https://www.pexels.com/photo/18956761/ |
| voorwerp/stoel | 963486 | https://www.pexels.com/photo/963486/ |
| voorwerp/doos | 5025503 | https://www.pexels.com/photo/5025503/ |

De mensen op de foto's zijn modellen, geen medewerkers. Vervang de teamfoto's en auteurs door echte medewerkers voor livegang.

## Beeldstraat

`uit.cjs` knipt het onderwerp uit (`@imgly/background-removal-node`, model medium), `poets.cjs` ruimt resten op (raamglas, losse lijntjes, half doorzichtige dozen), `beelden.cjs` schrijft alles als webp naar `assets/img/`. Ze draaiden in een tijdelijke map met `npm install @imgly/background-removal-node` en daarna `npm install-scripts approve onnxruntime-node sharp` + `npm rebuild onnxruntime-node sharp`; de paden bovenin `beelden.cjs` wijzen nog naar die map. Na een nieuwe uitsnede de omtrek meten en in `inhoud/beeldmaten.json` zetten (r, s, cx: verhouding, bovenkant onderwerp, midden van de bovenkant).
