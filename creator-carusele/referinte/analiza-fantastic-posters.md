# Analiză: skill-ul „fantastic-posters", primit ca referință

Sursa: `github.com/robonuggets/fantastic-posters`, v0.2, licență MIT.
Analizat pe 21 septembrie 2026, pentru integrare în Creatorul de carusele.

## Ce e, de fapt

Un generator de **afișe**, nu de carusele. O imagine pe rulare, cu textul desenat de model.

| Piesă | Ce face |
|---|---|
| `styles.js` | 33 de șabloane de prompt, câte unul pe stil, plus un auto-picker pe expresii regulate |
| `generate.js` | CLI pe Node: `node generate.js "<brief>"`, cu `--style`, `--n`, `--refs`, `--logo`, `--brief`, `--batch`, `--template`, `--size`, `--quality`, `--palette` |
| `examples/` | câte un render de referință pentru fiecare stil, 608×1088 |
| două skill-uri | `fantastic-posters` (33 stiluri) și `quality-posters` (31, versiunea veche) |

Modelul e tot **GPT Image 2**, ca la noi, dar prin **Fal** (`FAL_KEY` obligatoriu).
`KIE_KEY` apare în cod doar pentru urcarea imaginilor de referință, nu pentru generare.

Calitatea exemplelor e reală. Tipografia ține, compozițiile sunt curate, iar catalogul de
stiluri e muncă serioasă, nu o listă de adjective.

## Ce nu e

Nu are noțiunea de **set**: nici structură de slide-uri, nici fir narativ, nici numerotare,
nici unitate între imagini. Fluxul lui se termină cu un pas manual, în Canva („Magic /
Smart Layers"), ca omul să separe textul de fundal și să-l editeze.

Pentru linia demoului nostru, unde caruselul pleacă din `copy.md` și ajunge la Publisher
fără mâini umane, pasul din Canva e exact ce nu vrem.

## Unde se bate cap în cap cu ce avem

**1. Textul.** La ei textul îl desenează modelul, și ăsta e tot rostul skill-ului. La noi
textul se compune local cu ImageMagick, tocmai ca să avem ș și ț cu virgulă. Documentația
lor spune singură că peste ~6 cuvinte în titlu apar greșeli de literă. Pe un carusel de 12
slide-uri în română, fiecare slide e o șansă de greșeală, iar pe scenă nu ai când
regenerezi. **Asta e obiecția principală.**

**2. Unitatea setului.** Fiecare generare e independentă, deci 12 imagini din același stil
tot derivă în culoare și în tipografie. Noi ținem unitatea din fundal identic + strat de
text identic.

**3. Furnizorul.** Generarea merge doar pe Fal. Noi avem kie.ai și cheia în Keychain.
Prompturile sunt însă independente de furnizor, deci catalogul de stiluri se poate muta pe
kie fără să-l rescrii.

**4. Cele două skill-uri gemene.** `fantastic-posters` și `quality-posters` au descrieri și
declanșatoare aproape identice. Dacă le instalezi pe amândouă, agentul nu știe pe care să-l
ia. Se instalează unul singur.

Ce nu e problemă: formatul (`--size=1024x1280` ne dă 4:5), costul (medium ~0,04 $ pe
imagine, adică ~0,50 $ pe carusel) și licența (MIT, se poate adapta).

## Ce merită luat, chiar dacă nu instalăm nimic

| Ce | De ce contează la noi |
|---|---|
| **Catalogul de stiluri cu picker** | Creatorul nostru are un singur look, „aurora". Pentru ziua 3, cu profesor de engleză și service auto, aurora e greșit pe amândouă. Aceeași problemă pe care tocmai am rezolvat-o la Web Designer |
| **„Arată exemplul înainte să generezi, nu regenera catalogul"** | Costă zero, dă omului o alegere și e un moment bun pe scenă |
| **Estimare de cost și confirmare înainte de generare** | Noi raportăm creditele abia după. La 12 slide-uri, confirmarea dinainte e corectă |
| **Modul `--template`**: primul slide devine referință pentru următoarele | E cea mai bună idee din tot repo-ul pentru problema unității unui carusel generat |
| **„Trust the reference"**: la editare cu referință, promptul scurt care spune doar ce se schimbă bate specificația lungă | Contraintuitiv și util. Noi n-avem regula asta scrisă nicăieri |
| **Protocolul de logo**: logo ca referință separată, cu clauza „nu-l redesena, nu-l recolora" | Util dacă vreodată trimitem logoul clientului la model. Acum îl compunem local, ceea ce e mai sigur |

## Trei feluri de a integra

### 1. Minimal, doar regulile. Recomandat pentru intensiv

Nu instalăm nimic. Scriem în skill-urile existente trei reguli luate de la ei: arată
exemplul înainte de generare, confirmă costul înainte de generare, la editarea cu referință
scrie promptul scurt. Zero dependențe noi, zero risc pe scenă, o jumătate de oră de lucru.

### 2. Catalog de stiluri pentru carusele

Construim un catalog propriu, după modelul lor, dar pentru fundaluri de carusel și pe
kie.ai: „aurora" (ce avem) plus 3-4 stiluri pentru alte nișe, fiecare cu promptul lui și cu
un exemplu generat o singură dată. Creatorul alege stilul după domeniul campaniei și îl
arată înainte să genereze. Textul rămâne compus local.

Rezolvă problema reală din ziua 3: două demonstrații pe nișe diferite care nu au voie să
arate la fel. Cost: o jumătate de zi și câteva credite pentru exemple.

### 3. Instalare ca unealtă separată, în afara flotei

Repo-ul clonat undeva, cu cheia Fal, pentru afișe adevărate: coperte de lecție, materiale
de curs, postere pentru comunitate. Nu intră în demo. Se poate face oricând, nu acum.

## Testul care decide dacă textul poate veni vreodată de la model

O singură generare, pe kie, cu un titlu în română plin de diacritice, de exemplu
„Ședințe săptămânale · Înscrie-te acum". Dacă ș, ț, î și ă ies corect și constant, se poate
discuta despre text desenat de model la coperte. Dacă nu, rămâne definitiv compunerea
locală, și punem asta în scris în skill, ca să nu se mai redeschidă discuția.

Costă un credit și cinci minute.

## Verdict

Skill-ul e bun, dar e pentru altă meserie. Nu se integrează ca atare în Creatorul de
carusele, pentru că își pune valoarea exact acolo unde noi am ales deliberat altceva:
textul desenat de model.

Ce se integrează sunt metoda și trei reguli. Varianta 1 acum, varianta 2 dacă mai avem
timp înainte de intensiv, varianta 3 după.
