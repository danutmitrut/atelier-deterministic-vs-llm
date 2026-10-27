# Catalogul de stiluri de carusel

Un carusel nu arată la fel pentru orice nișă. Un service auto și un profesor de engleză nu
au aceeași greutate vizuală, iar dacă le dai același fundal se vede că e turnat din șablon.

Catalogul ăsta ține șase stiluri. Fiecare e două lucruri legate între ele: **promptul de
fundal** pentru kie.ai și **paleta cu care se scrie textul peste el**. Amândouă stau în
`scripts/stiluri.py`, ca să nu se desincronizeze niciodată.

Adaptat ca metodă din `fantastic-posters` (skill-ul primit ca referință, analiza în
`referinte/analiza-fantastic-posters.md`). De acolo am luat ideea de catalog cu picker și
regulile de mai jos. Ce n-am luat: textul desenat de model. La noi textul rămâne compus
local, pentru diacritice.

## Cele șase stiluri

| Stil | Când îl folosești | Cum arată |
|---|---|---|
| `aurora` | tehnologie, AI, software, automatizări, produse digitale | fundal aproape negru, lumini teal, lavender și copper |
| `hartie-editoriala` | educație, cursuri, meditații, scriere, consultanță, mentorat | hârtie caldă, ilustrație în tuș cărămiziu, liniște de revistă |
| `atelier` | service auto, meserii, construcții, instalații, reparații | beton și oțel, lumină de lucru dură, accent portocaliu de siguranță |
| `studio-cald` | wellness, nutriție, terapie, cosmetică, yoga | nisip și teracotă, lumină naturală laterală, textură |
| `bloc-tipar` | evenimente, lansări, promoții, anunțuri cu termen | două culori plate, siluetă decupată, textură de serigrafie |
| `editorial-foto` | poveste personală de brand, opinie, manifest; look de revistă | fotografie caldă pe tot cadrul, titlu uriaș cu antiqua peste ea |

Exemplele, cu text peste ele, sunt în `resurse/exemple-stiluri/`:
`toate-cu-text.png` le arată pe primele cinci una lângă alta, iar `editorial-foto.png`
și `editorial-foto-cu-text.png` arată stilul al șaselea, adăugat pe 22 septembrie 2026.

## Cum alegi

```bash
python3 scripts/stiluri.py --alege "campanie pentru un service auto din Cluj"
# atelier	„service” din brief
```

Pickerul se uită după cuvintele nișei din brief. Dacă nu găsește nimic limpede, **iese cu
eroare și atunci întrebi omul**, cu trei variante din `--lista`. Nu alegi în tăcere și nu
cazi automat pe aurora.

Dacă brieful spune explicit stilul, îl respecți, chiar dacă pickerul ar fi zis altceva.

## Cum generezi fundalul

```bash
python3 scripts/stiluri.py --prompt atelier --element "a brake disc and a torque wrench"
```

Iese promptul complet, pe care îl dai lui `kie_generate.py`. `--element` e singurul lucru
care se schimbă de la un slide la altul: elementul vizual al slide-ului respectiv, scris în
engleză, scurt. Restul promptului ține stilul.

Dacă nu dai `--element`, se folosește elementul implicit al stilului. Bun pentru copertă,
prea repetitiv pentru douăsprezece slide-uri.

Zona liberă pentru text e, implicit, jumătatea de sus, pentru că acolo se așază textul.
La `editorial-foto` e jumătatea de jos, pentru că acolo stă titlul, ca pe o copertă de
revistă. Fiecare stil își știe zona, `--zona` o schimbă doar dacă ai nevoie.

## Cum compui textul

```bash
python3 scripts/compune_slide.py fundal.png slide-1.png --stil atelier \
    --eticheta "// cum alegi" --titlu1 "Trei greșeli" --titlu2 "care te costă clienți" \
    --numar "01 / 12"
```

**`--stil` e obligatoriu să fie același cu cel al fundalului.** El decide culorile textului,
felul umbrei (neagră pe fundal închis, halou deschis pe fundal deschis) și unde stă numărul
slide-ului. Dacă îl uiți, slide-ul iese cu paleta aurora peste un fundal deschis și nu se
citește nimic.

## Trei reguli, luate din skill-ul de referință

**1. Arată exemplul înainte să generezi.** Când ai ales stilul, arată-i omului
`resurse/exemple-stiluri/<stil>.png` și spune într-o frază de ce ăla. Nu regenera niciodată
exemplele din catalog: sunt referința, și costă credite degeaba.

**2. Spune costul înainte, nu după.** O generare kie.ai înseamnă în jur de 6 credite și
între 60 și 100 de secunde. Înainte să pornești un set, spui câte imagini sunt și cât face,
și aștepți confirmarea. La un carusel de 12 slide-uri sunt ~72 de credite.

**3. La editarea cu imagine de referință, promptul scurt bate specificația lungă.** Dacă
pornești de la un slide gata făcut ca să ții unitatea setului, scrie **doar ce se schimbă**.
Nu repeta ce se vede deja în referință: modelul derivează cu cât îi spui mai mult.

## Când elementul intră peste text

Se întâmplă: modelul umple zona pe care i-ai cerut-o goală. Atunci ai o singură regenerare
pe slide, și în ea ceri explicit elementul mai jos sau mai mic. Dacă nici a doua oară nu
iese, muți textul (`--zona`) sau schimbi elementul, nu arunci stilul.

## Layout-urile, adică de ce nu arată toate slide-urile la fel

Stilul dă lumea vizuală, layout-ul dă compoziția. Fără layout-uri, un carusel de opt
slide-uri e același slide de opt ori, cu alt text. Se alege cu `--layout`:

| Layout | Ce e | Când îl folosești |
|---|---|---|
| `foto-jos` | text în josul fotografiei | copertă și îndemn final |
| `foto-sus` | text în susul fotografiei | momente, pași, cifre mari |
| `banda` | fotografia sus, o bandă plină jos cu textul pe ea | momente povestite, informații practice |
| `panou` | fără fotografie, suprafață plată și tipografie mare | afirmații tari, respiro între imagini |
| `citat` | fotografie întunecată, text centrat peste ea | fraza care se ține minte |
| `dovada` | text scurt sus, captura pregătită dedesubt, întreagă și dreaptă | capturi, cifre dovedite |
| `auto` | asezarea implicită a stilului | când nu te gândești la compoziție |

**Regula:** două slide-uri vecine nu au voie să aibă același layout. Unitatea vine din
culori, fonturi și numerotare, nu din repetarea compoziției. Singura excepție e un lanț de
slide-uri de dovadă, unde arhitectura cere dovezile una după alta, iar capturile arată
oricum diferit între ele.

**`dovada` cere `--dovada <captura>` și nu merge cu alt layout.** Captura trece întâi prin
`pregateste_captura.py`, niciodată direct pe slide. Ca și `panou`, nu folosește fotografie,
deci nu costă nicio generare.

**Stilurile cu cerneală închisă pe hârtie deschisă (`hartie-editoriala`, `studio-cald`) nu
merg cu `citat`.** Layout-ul întunecă fotografia cu 38%, stilul scrie cu cerneală închisă
peste ea, și textul dispare. Același lucru pe `foto-sus` peste o fotografie deja
întunecată. Verifici potrivirea stil-layout **înainte** să generezi fundalul, altminteri
plătești o generare pentru un slide pe care îl schimbi oricum. S-a întâmplat pe 22
septembrie: 6 credite pe un fundal care a ajuns la coș.

Nu întuneci tu fotografia și nu adaugi tu un strat peste ea. `compune_slide.py` pune singur
un voal sub text când fondul se apropie prea tare de culoarea literelor, măsurat pe patru
benzi. Dacă chiar nu îl vrei, `--fara-scrim`.

**`panou` și `dovada` nu folosesc fotografia deloc**, deci slide-urile alea nu costă nicio
generare. La un carusel de opt slide-uri cu două panouri, plătești șase fundaluri, nu opt.
Și înainte să plătești vreunul, vezi dacă nu îl rezolvă o fotografie reală de pe net, cu
`cauta_foto.py`. Aia e gratis și arată a lucru adevărat.

Un ritm care funcționează, pe opt slide-uri:

```
1 foto-jos   2 banda   3 citat   4 foto-sus
5 panou      6 banda   7 foto-sus (cu --numar-mare)   8 foto-jos (cu --logo)
```

Pe `banda` și pe `panou` textul e scris cu paleta închisă a stilului, pe suprafața deschisă,
și titlul e proiectat mai mic, pentru că zona e mai mică. Nu e o micșorare de avarie.

## `editorial-foto`, stilul de copertă de revistă

E singurul stil cu tipografie proprie și cu textul așezat jos, nu sus. Vine din caruselele
de referință (`referinte/postare-utila/`), din care am luat **tratamentul**,
nu pozele și nu oamenii din ele:

- titlul, cu majuscule, în Playfair Display Black, o antiqua grea de afiș;
- al doilea rând, tot majuscule, în Instrument Sans Bold, mai mic, sub el;
- fraza secundară, majuscule mici, fără linia de accent;
- numărul slide-ului într-o pastilă cu contur, jos-dreapta;
- fundalul e fotografie caldă, cu obiecte, **fără fețe și fără oameni recognoscibili**.

Se potrivește la poveste personală de brand, opinie, manifest. Nu îl folosi la pași
numerotați și la liste: titlul mare mănâncă tot slide-ul. Acolo rămân celelalte stiluri.

Pentru că titlul e cu majuscule și cu o literă lată, **ține-l până în 3-4 cuvinte**.
„Blogul meu" merge, „Cum îți dai seama că frânele cer ajutor" nu.

## Ce nu se schimbă, oricare ar fi stilul

Formatul e vertical, 4:5. Textul e compus local, niciodată desenat de model. Fonturile sunt
Instrument Sans, JetBrains Mono și, doar la `editorial-foto`, Playfair Display Black, toate
din `resurse/fonturi/`. Logoul apare doar pe ultimul slide, prin `--logo`. Un singur mesaj
pe slide, numerotare pe fiecare, îndemn pe ultimul.
