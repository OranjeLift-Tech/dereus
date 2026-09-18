/* Verhuisbedrijf De Reus · dienstenpanelen: de wijzer in de index volgt het paneel dat in beeld is.
   Zonder dit script blijft de index een gewone lijst met ankers. */
(function(){
  'use strict';
  if(!('IntersectionObserver' in window))return;
  [].forEach.call(document.querySelectorAll('[data-b="dienstenpanelen"]'),function(blok){
    var index=blok.querySelector('.b-dienstenpanelen__index');
    if(!index)return;
    var wijzer=index.querySelector('.b-dienstenpanelen__wijzer'),
        links=[].slice.call(index.querySelectorAll('a[href^="#"]')),
        panelen=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))});
    if(!links.length||panelen.indexOf(null)>-1)return;

    function zet(i){
      if(wijzer)wijzer.style.setProperty('--i',i);
      links.forEach(function(a,j){
        a.classList.toggle('is-actief',i===j);
        if(i===j)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');
      });
    }
    var start=panelen.map(function(p){return '#'+p.id}).indexOf(location.hash);
    zet(start>-1?start:0);
    index.classList.add('is-actief');

    /* Een smalle band net boven het midden van het scherm. Raken meer panelen die band,
       dan wint het eerste in de volgorde van de pagina: dat blijft rustig bij omhoog scrollen. */
    var zichtbaar={};
    var io=new IntersectionObserver(function(items){
      items.forEach(function(it){zichtbaar[it.target.id]=it.isIntersecting});
      for(var i=0;i<panelen.length;i++){if(zichtbaar[panelen[i].id]){zet(i);return}}
    },{rootMargin:'-35% 0px -55% 0px'});
    panelen.forEach(function(p){io.observe(p)});

    links.forEach(function(a,i){a.addEventListener('click',function(){zet(i)})});
  });
})();
