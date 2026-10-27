# De unde iei fotografia

> Fișier adăugat local pe 22 septembrie 2026, la cererea lui Dănuț. Nu face parte din
> skill-ul original.

Skill-ul cere fotografii reale și interzice înlocuirea unei persoane sau a unui client cu
imagine generată. Regula rămâne. Fișierul ăsta spune ce faci când, în practică, omul nu
trimite materialul.

## Ordinea surselor, de sus în jos

1. **Materialul omului.** Fotografiile lui, capturile lui. Singura sursă care dovedește
   ceva. Dacă povestea e despre atelierul lui, despre rezultatul lui sau despre mâinile
   lui, asta e singura sursă acceptabilă. Când lipsește, o ceri, cu listă scrisă, pe
   slide-uri, ca în `evidence-inventory.md`.
2. **Fotografie de stoc, luată de pe net.** Fotografie reală, dar a altcuiva. Merge pentru
   ilustrație, nu pentru dovadă. Vezi mai jos ce înseamnă asta. Se caută în cinci surse
   deodată, toate gratuite, și nu costă nimic. Nu treci mai departe după o singură
   căutare eșuată: reformulezi, ceri candidați și te uiți la ei.
3. **Imagine generată.** Când niciuna dintre surse nu are subiectul. Pentru fundal
   și atmosferă, niciodată pentru dovadă și niciodată în locul unei persoane reale.
   Costă credite, deci se spune cifra omului înainte.

**Când sari de la 2 la 3.** Regula practică, de pe 23 septembrie 2026: după două runde de
căutare, cu interogări reformulate, dacă subiectul tot nu iese, e semn că sursele nu îl au
și se generează. Subiectele tehnice cad des așa: un croasant tăiat cu straturile în
secțiune, o piesă anume, un obiect văzut dintr-un unghi anume. Nu insiști la infinit ca să
economisești șase credite, dar nici nu generezi din prima ce se găsea gratis.

Diferența contează și moral, nu doar bugetar. Pe o **poveste personală sau un studiu de
caz**, generarea e la fel de falsă ca stocul: locul nu e al omului. Pe o **postare utilă**,
care explică un proces și nu pretinde nimic despre nimeni, o imagine generată nu înșală pe
nimeni, și de multe ori arată exact lucrul pe care sursele nu îl au.

## Cum iei o fotografie de pe net

```bash
python3 scripts/cauta_foto.py "pottery wheel in a studio" \
  --iesire material-foto/04.jpg --vreau wheel,pottery --nu-vreau hand,person
```

Pentru tot setul deodată, un plan JSON cu o linie per slide:

```bash
python3 scripts/cauta_foto.py --plan plan-foto.json --dosar material-foto/
```

Scriptul caută în **cinci surse deodată**: Unsplash, Openverse, Wikimedia Commons, Pexels
și Pixabay. Rezultatele se intercalează, câte unul din fiecare sursă pe rând, ca să nu ocupe
una singură toate locurile. `--sursa unsplash`, `--sursa openverse`, `--sursa wikimedia`,
`--sursa pexels` sau `--sursa pixabay` o restrânge la una singură.

Pexels și Pixabay cer câte o cheie gratuită, ținută în seif ca `pexels-api-key` și
`pixabay-api-key`. Dacă lipsesc, sursele se sar în tăcere și căutarea merge mai departe cu
celelalte trei. Nu e eroare și nu te oprești pentru ea, dar dacă o căutare importantă iese
subțire, îi spui omului că două surse din cinci sunt stinse și cum se aprind.

Scoate din listă fotografiile Unsplash+, care vin cu filigran peste toată imaginea, iar din
Openverse și Wikimedia ia doar licențele `cc0`, `pdm` și `by`. Rămân afară `nc`, `nd` și
`sa`, pentru că punem text peste fotografie, ceea ce e o modificare, iar caruselul e pentru
o afacere.

Ce aduce fiecare sursă: Unsplash are calitate uniformă și fotografie profesionistă, dar
descrierile lui mint des. Openverse agregă Flickr, Wikimedia și altele, deci are subiecte
tehnice pe care Unsplash nu le are, secțiuni, unelte, scheme, cu prețul unei calități
neuniforme. Wikimedia Commons e sursa documentară, bună la obiecte, piese și scheme, slabă
la atmosferă. Pexels seamănă la gen cu Unsplash, dar are alt fond de imagini, deci merită
când Unsplash nu scoate nimic. Pixabay e cel mai divers și cel mai inegal, cu ilustrații și
vectori amestecate printre fotografii.

Creditele din ieșirea JSON conțin și sursa, și licența. Amândouă intră în
`source/photo-credits.md`.

## Trei lucruri pe care unealta nu le poate face în locul tău

1. **Te uiți la fotografii înainte să le folosești.** Filtrarea pe cuvinte e aproximativă:
   „nu vreau person" nu prinde o descriere care spune „woman". La prima rulare pe ceramică,
   o căutare de birou a întors un birou noaptea cu lumini colorate, iar „mâini pe roată" a
   întors o roată fără mâini.
2. **Verifici că fotografia nu se bate cu paleta stilului.** O găleată roșie într-o paletă
   caldă de lut sare în ochi. Tai cadrul sau schimbi fotografia.
3. **Scrii creditele.** Autorul și linkul, pentru fiecare fotografie folosită. Ieșirea
   scriptului ți le dă gata.

## Ce trebuie spus omului, negociat

O fotografie de stoc a unui atelier, pusă sub un text scris la persoana întâi („am deschis
în martie", „două roți și un cuptor"), e aceeași abatere ca o imagine generată: fotografia
e reală, locul nu e al lui. Stocul rezolvă estetica, nu dovada.

Deci, când folosești stoc pe un carusel de poveste personală sau de studiu de caz, spui
omului, în text, o dată, clar: fotografiile sunt ilustrative, nu sunt ale lui, iar caruselul
devine documentat abia când trimite materialul. Nu o strecori în subsolul unui fișier.

Pe slide-urile care poartă dovada, stocul nu are ce căuta deloc.
