/* Verhuisbedrijf De Reus · formulier (offerte en contact)
   1. invullen vanuit het adres: ?van=&naar=&datum=&dienst=
   2. vinkjes "nog onbekend" bij Naar en Wanneer
   3. adressuggesties van PDOK bij Van en Naar (een hulp, nooit een voorwaarde)
   4. foutoverzicht met aria-invalid
   5. verzenden via Web3Forms en doorsturen naar de bedanktpagina
   Zonder dit script werkt het formulier als gewone POST, met de controle van de browser. */
(function(){
  'use strict';
  var PDOK='https://api.pdok.nl/bzk/locatieserver/search/v3_1/suggest?fq=type:(woonplaats%20OR%20weg%20OR%20adres)&rows=6&q=';
  var WEB3FORMS='https://api.web3forms.com/submit';

  [].forEach.call(document.querySelectorAll('form[data-formulier]'),function(f){
    var foutlijst=f.querySelector('.b-formulier__foutlijst'),
        foutregels=foutlijst?foutlijst.querySelector('ul'):null,
        foutVersturen=f.querySelector('.b-formulier__fout'),
        knop=f.querySelector('button[type=submit]');
    f.noValidate=true;   /* pas hier: zonder script controleert de browser zelf */

    function veld(id){return f.querySelector('#f-'+id)}

    /* ---- 1. invullen vanuit het adres ---- */
    (function(){
      if(!('URLSearchParams' in window))return;
      var p=new URLSearchParams(location.search);
      ['van','naar'].forEach(function(n){
        var el=veld(n),w=(p.get(n)||'').trim();
        if(el&&w)el.value=w.slice(0,120);
      });
      var datum=veld('datum'),d=p.get('datum')||'';
      if(datum&&/^\d{4}-\d{2}-\d{2}$/.test(d))datum.value=d;
      var dienst=veld('dienst'),s=(p.get('dienst')||'').toLowerCase();
      if(dienst&&s)[].forEach.call(dienst.options,function(o){if(o.value===s)dienst.value=s});
    })();

    /* de vroegste datum is vandaag */
    (function(){
      var datum=veld('datum');if(!datum)return;
      var nu=new Date();
      datum.min=nu.getFullYear()+'-'+('0'+(nu.getMonth()+1)).slice(-2)+'-'+('0'+nu.getDate()).slice(-2);
    })();

    /* ---- 2. "nog onbekend": het veld leeg en uit, en andersom ---- */
    [].forEach.call(f.querySelectorAll('[data-onbekend-voor]'),function(vink){
      var doel=f.querySelector('#'+vink.getAttribute('data-onbekend-voor'));
      if(!doel)return;
      vink.addEventListener('change',function(){
        if(vink.checked){doel.value='';herstel(doel)}
        doel.disabled=vink.checked;
      });
      doel.addEventListener('input',function(){if(doel.value)vink.checked=false});
    });

    /* ---- 3. PDOK ---- */
    [].forEach.call(f.querySelectorAll('input[data-adres]'),function(el){
      var lijst=f.querySelector('#'+el.getAttribute('aria-controls')),timer=0,actief=-1;
      if(!lijst||!window.fetch)return;
      function sluit(){lijst.hidden=true;lijst.innerHTML='';actief=-1;el.setAttribute('aria-expanded','false');el.removeAttribute('aria-activedescendant')}
      function markeer(i){
        var items=lijst.children;
        [].forEach.call(items,function(li,j){li.setAttribute('aria-selected',i===j?'true':'false')});
        actief=i;
        if(i>-1){el.setAttribute('aria-activedescendant',items[i].id);items[i].scrollIntoView({block:'nearest'})}
        else el.removeAttribute('aria-activedescendant');
      }
      function kies(tekst){el.value=tekst;sluit();herstel(el)}
      function toon(namen){
        lijst.innerHTML='';
        namen.forEach(function(naam,i){
          var li=document.createElement('li');
          li.id=el.id+'-keuze-'+i;li.className='b-formulier__keuze';li.setAttribute('role','option');li.setAttribute('aria-selected','false');
          li.textContent=naam;
          /* mousedown: een klik komt pas na het verlaten van het veld, dan is de lijst al dicht */
          li.addEventListener('mousedown',function(e){e.preventDefault();kies(naam)});
          lijst.appendChild(li);
        });
        lijst.hidden=false;el.setAttribute('aria-expanded','true');actief=-1;
      }
      function haal(q,klaar){
        /* "2525ZJ336" vindt PDOK niet, "2525ZJ 336" wel */
        q=q.replace(/([1-9][0-9]{3})\s*([a-z]{2})\s*/i,'$1$2 ');
        fetch(PDOK+encodeURIComponent(q),{headers:{Accept:'application/json'}})
          .then(function(r){return r.json()})
          .then(function(j){klaar(((j&&j.response&&j.response.docs)||[]).map(function(d){return d.weergavenaam}).filter(Boolean))})
          .catch(function(){klaar(null)});   /* niet kunnen zoeken mag een aanvraag nooit tegenhouden */
      }
      el.addEventListener('input',function(){
        var q=el.value.trim();
        clearTimeout(timer);
        if(q.length<3){sluit();return}
        timer=setTimeout(function(){
          haal(q,function(namen){
            if(document.activeElement!==el||el.value.trim()!==q)return;   /* intussen verder getypt */
            if(!namen||!namen.length||(namen.length===1&&namen[0]===el.value)){sluit();return}
            toon(namen);
          });
        },220);
      });
      el.addEventListener('keydown',function(e){
        if(lijst.hidden)return;
        var n=lijst.children.length;
        if(e.key==='ArrowDown'){e.preventDefault();markeer((actief+1)%n)}
        else if(e.key==='ArrowUp'){e.preventDefault();markeer((actief-1+n)%n)}
        else if(e.key==='Enter'&&actief>-1){e.preventDefault();kies(lijst.children[actief].textContent)}
        else if(e.key==='Escape'){sluit()}
      });
      el.addEventListener('blur',function(){setTimeout(sluit,150)});
    });

    /* ---- 4. controle en foutoverzicht ---- */
    function melding(el){
      var v=el.validity;
      if(v.valueMissing)return el.getAttribute('data-fout')||'';
      if(v.typeMismatch||v.patternMismatch||v.rangeUnderflow||v.badInput)return el.getAttribute('data-fout-onjuist')||el.getAttribute('data-fout')||'';
      return el.validationMessage||'';
    }
    function labeltekst(el){var l=f.querySelector('label[for="'+el.id+'"]');return l?l.textContent.trim():''}
    function herstel(el){
      var li=document.getElementById(el.id+'-fout');
      if(li)li.parentNode.removeChild(li);
      el.removeAttribute('aria-invalid');
      var rest=(el.getAttribute('aria-describedby')||'').split(' ').filter(function(x){return x&&x!==el.id+'-fout'}).join(' ');
      if(rest)el.setAttribute('aria-describedby',rest);else el.removeAttribute('aria-describedby');
      if(foutlijst&&foutregels&&!foutregels.children.length)foutlijst.hidden=true;
    }
    function toonFouten(){
      var fout=[].filter.call(f.elements,function(el){return el.willValidate&&!el.checkValidity()});
      if(foutregels)foutregels.innerHTML='';
      [].forEach.call(f.querySelectorAll('[aria-invalid]'),herstel);
      if(!fout.length){if(foutlijst)foutlijst.hidden=true;return true}
      fout.forEach(function(el){
        var li=document.createElement('li'),a=document.createElement('a');
        li.id=el.id+'-fout';a.href='#'+el.id;
        a.textContent=melding(el)||labeltekst(el);
        a.addEventListener('click',function(e){e.preventDefault();el.focus()});
        li.appendChild(a);if(foutregels)foutregels.appendChild(li);
        el.setAttribute('aria-invalid','true');
        el.setAttribute('aria-describedby',((el.getAttribute('aria-describedby')||'')+' '+li.id).trim());
      });
      if(foutlijst){foutlijst.hidden=false;foutlijst.focus()}
      return false;
    }
    f.addEventListener('input',function(e){
      var el=e.target;
      if(el.getAttribute&&el.getAttribute('aria-invalid')&&el.checkValidity())herstel(el);
    });

    /* ---- 5. verzenden ---- */
    f.addEventListener('submit',function(e){
      e.preventDefault();
      if(foutVersturen)foutVersturen.hidden=true;
      if(!toonFouten())return;
      var oud=knop?knop.innerHTML:'';
      function mis(){
        if(knop){knop.disabled=false;knop.innerHTML=oud}
        if(foutVersturen){foutVersturen.hidden=false;foutVersturen.scrollIntoView({block:'nearest'})}
      }
      /* nog geen sleutel van Web3Forms: niet doen alsof het gelukt is, maar telefoon en e-mail tonen */
      if(f.hasAttribute('data-zonder-sleutel')){mis();return}
      if(knop){knop.disabled=true;if(f.getAttribute('data-bezig'))knop.textContent=f.getAttribute('data-bezig')}
      var d=new FormData(f);
      if(d.get('botcheck'))return;   /* honeypot: een robot krijgt niets te zien */
      d.delete('botcheck');d.delete('redirect');
      Array.from(d.keys()).forEach(function(k){if(!d.getAll(k).join('').trim())d.delete(k)});
      var mail=f.querySelector('input[type=email]');
      if(mail&&mail.value)d.append('replyto',mail.value);
      d.append('Pagina',document.title);
      fetch(WEB3FORMS,{method:'POST',headers:{Accept:'application/json'},body:d})
        .then(function(r){return r.json()})
        .then(function(res){
          if(!res||!res.success)return mis();
          location.href=f.getAttribute('data-bedankt')||'/';
        })
        .catch(mis);
    });
  });
})();
