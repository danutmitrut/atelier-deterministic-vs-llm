---
name: genereaza-carusel
description: Produce slide-urile reale ale caruselului, ca imagini PNG, după specificația din carusel.md. Generează fundalul fiecărui slide prin kie.ai, apoi pune textul peste cu ImageMagick. Rulează după structura-carusel.
---

# genereaza-carusel

Adaptat din biblioteca de agenți: `nova-designer` (`img-carousel`, `img-compose-post`,
`img-brand-identity`), `nova-gpt-image` (`compune-text` și regulile despre cost) și
skill-ul `kie-image` al lui Dănuț.

## Uneltele, și doar astea

| Ce | Cu ce |
|---|---|
| Stilul și promptul lui | `python3 scripts/stiluri.py` (catalogul de stiluri) |
| Fundalul fiecărui slide | `python3 scripts/kie_generate.py` (kie.ai, GPT Image 2) |
| Textul de pe slide | `python3 scripts/compune_slide.py` (ImageMagick) |

**Nu folosești nicio altă unealtă de imagine**: nici Higgsfield, nici HeyGen, nici alte
MCP-uri sau skill-uri de generare care apar disponibile în sesiune. Dacă scripturile de
mai sus nu merg, te oprești și îi spui omului. Nu cauți altă cale.

Cheia kie.ai se citește singură din seif (`kie-api-key`). Nu o ceri, nu o afișezi, nu o
scrii în niciun fișier. Nu există `.env` în folderul ăsta și nu creezi unul.

## Pasul 1. Ce ai nevoie înainte

- `../campanie/livrabile/carusel.md`, făcut cu `tipuri-carusel` și `structura-carusel`.
  Dacă nu există, nu începi.
- `cunostinte/stiluri-carusel.md`: catalogul de stiluri și cum se alege.
- `cunostinte/reguli-carusel-brand.md`: ce rămâne fix, oricare ar fi stilul. Fișa completă
  de brand e `cunostinte/identitate-vizuala.md`. Dacă lipsesc, te oprești și ceri.
- **stilul ales**, scris în capul lui `carusel.md` de `tipuri-carusel`. Dacă nu e scris
  acolo, nu îl alegi tu pe fugă: te întorci la `tipuri-carusel`.

## Pasul 2. Stilul, arătat și confirmat

Înainte de orice generare, două lucruri, în ordine:

1. **Arăți exemplul.** `resurse/exemple-stiluri/<stil>.png` e cum arată stilul ales, gata
   făcut. Îl trimiți omului, cu o frază despre de ce stilul ăla.
   **Nu regenerezi niciodată exemplele din catalog**, sunt referința și ar costa degeaba.
2. **Spui costul.** „N slide-uri, în jur de N×6 credite, în jur de un minut pe imagine,
   toate pornite deodată." Aștepți confirmarea înainte să pornești setul.

Promptul de fundal îl scoate catalogul, nu îl scrii tu:

```bash
python3 scripts/stiluri.py --prompt <stil> --element "<elementul slide-ului, în engleză>"
```

Stilul rămâne identic pe toate slide-urile. Se schimbă doar `--element`, adică elementul
vizual al slide-ului respectiv. Consecvența vizuală între slide-uri e obligatorie.

Promptul e în engleză. Modelul răspunde mai bine, iar diferența se vede în rezultat.

## Pasul 2b. Capturile omului, dacă are

Slide-urile cu rolul **dovadă** se compun cu `--layout dovada --dovada <captura>`. Ca
`panou`, nu folosesc fotografie generată, deci nu le generezi fundal și nu coști credite
pe ele.

**Nicio captură nu ajunge pe slide așa cum a venit.** Trece prin:

```bash
python3 scripts/pregateste_captura.py captura.png pregatita.png \
  --zona "152,176,300,598:redactat, clienti terti" \
  --marcheaza "44,272,300,84" \
  --nota "56,268:37 de minute mai tarziu" \
  --decupaj "16,136,1068,644" --latime 900 --rama
```

- `--zona` acoperă ce nu se publică: nume de clienți, adrese, solduri, numere de telefon.
  Se poate repeta. Bară plină, nu blur și nu pixelare, pentru că pe text amândouă se
  pot inversa. Acoperirea e integrală, nu inițiale: „M. P." nu înseamnă anonim.
- `--marcheaza` și `--nota` arată ce trebuie citit pe captură. Nu acoperi cu nota chiar
  dovada la care se referă.
- `--decupaj` și `--latime` fac captura lizibilă pe telefon, `--rama` o transformă în
  obiect cu colțuri rotunjite și umbră.
- Coordonatele se dau raportat la imaginea originală, în pixeli sau în procente („12%").

Dacă omul nu a spus explicit ce are voie să apară din captură, întrebi înainte să compui.

## Fotografiile primite de la om, nu generate

Când omul trimite fotografii reale, nu le mai controlezi tonalitatea, cum o face promptul
la fundalurile generate. Un perete alb sub un titlu scris cu alb înseamnă slide ilizibil.

`compune_slide.py` măsoară singur zona în care cade textul, pe patru benzi, și pune un voal
în degrade dacă fondul e prea aproape de culoarea textului. Benzile contează separat: un
titlu așezat pe ceva închis trage media în jos și ascunde rândul de dedesubt, care stă pe
perete alb. Voalul e plin peste blocul de text și se stinge abia dincolo de el.

Nu se atinge de fundalurile generate, care stau oricum în tonalitatea cerută de prompt.
Dacă îl vrei oprit pe un slide anume, `--fara-scrim`.

Ce rămâne în sarcina ta, pentru că unealta nu le poate decide:

- o fotografie reală poate avea un obiect de o culoare care se bate cu paleta stilului;
  se taie din cadru sau se schimbă fotografia;
- o fotografie a atelierului altcuiva, pusă sub un text scris la persoana întâi, e aceeași
  abatere ca o imagine generată. Materialul trebuie să fie al omului.

## Pasul 3. Fundalurile

**Slide-urile cu `--layout panou` nu au nevoie de fundal**, sunt suprafață plată cu
tipografie. Le sari la generare și economisești câte o generare de fiecare. La compunere
le dai `-` în locul căii fundalului:

```bash
python3 scripts/compune_slide.py - ../campanie/livrabile/carusel/slide-5.png \
  --stil <stil> --layout panou --titlu1 "..." --titlu2 "..." --text "..." --numar "05 / 08"
```

`-` merge doar cu `--layout panou`. Pe orice alt layout scriptul se oprește și îți spune.

Pentru fiecare slide din `carusel.md` **care nu e `panou`**, în ordine:

```bash
PROMPT=$(python3 scripts/stiluri.py --prompt <stil> --element "<elementul slide-ului>")
python3 scripts/kie_generate.py "$PROMPT" \
  "../campanie/livrabile/carusel/fundal-<N>.png" --aspect 4:5
```

Formatul e vertical, 4:5, la fel ca al slide-urilor.

**Niciun text în prompt.** Generatoarele scriu prost, iar cu diacritice românești greșesc
aproape sigur: „ș" iese „s", „ț" iese „t". Textul se pune la pasul următor.

Fiecare generare durează în jur de un minut. Ca să nu aștepte sala câte un minut pe slide,
pornești toate generările deodată, fiecare în fundal, și aștepți să se termine toate.
Îi spui omului când începi și câte slide-uri urmează.

## Pasul 4. Textul peste

```bash
python3 scripts/compune_slide.py "../campanie/livrabile/carusel/fundal-<N>.png" \
  "../campanie/livrabile/carusel/slide-<N>.png" --stil <stil> --layout <layout> \
  --eticheta "// ..." --titlu1 "<primul rând>" --titlu2 "<al doilea rând>" \
  --text "<fraza secundară>" --numar "0<N> / 0<total>"
```

**`--layout` vine din `carusel.md`, slide cu slide.** El dă compoziția: `foto-jos`,
`foto-sus`, `banda`, `panou`, `citat`, `dovada`. Dacă îl uiți, toate slide-urile ies cu aceeași
așezare și caruselul arată turnat din șablon, care e exact reproșul de la care am pornit.

**`--stil` trebuie să fie același cu stilul fundalului.** El dă culorile textului, felul
umbrei și locul numărului. Dacă îl uiți, scrii cu paleta aurora peste un fundal deschis și
nu se mai citește nimic.

Fiecare slide are layout-ul lui, din `carusel.md`. Opțiunile care îl dau:
`--numar-mare` (cifra mare de fundal, pentru pași și rezultate), `--lista "a|b|c"`
(enumerare), `--foto a.png,b.png` (pozele sau capturile omului, ca un colaj înclinat),
`--logo` (doar pe ultimul slide). Două slide-uri vecine nu folosesc aceeași combinație.

Scriptul pune culorile, fonturile, linia și umbra de lizibilitate ale stilului ales.
Rupe singur textul pe rânduri, micșorează titlul dacă nu încape și așază blocul în
treimea de sus, acolo unde fundalul e curat.

**Citește ce-ți răspunde.** La fiecare slide scoate un JSON cu un câmp `avertisment`:

- `null`, textul a încăput cum trebuie, mergi mai departe;
- un mesaj (și un rând „ATENTIE" în consolă), textul e mai lung decât suportă layout-ul.
  Slide-ul se produce oricum, ca să nu stea campania, dar **nu îl treci ca reușit în
  tăcere**: îl treci în „Semnalări" și îi spui omului ce slide și ce text.
  Nu rescrii tu textul.
- eroare și oprire, textul nu încape nici micșorat. Atunci spui ce e prea lung și aștepți.

- textul îl copiezi exact din `copy.md` și din `carusel.md`, nu îl reformulezi
- `--eticheta`, `--titlu2` și `--text` sunt opționale, le lași deoparte dacă slide-ul nu le are
- pe ultimul slide adaugi `--logo`
- `scripts/compose_text.py` rămâne doar pentru cazuri speciale (un singur bloc de text)

## Pasul 5. Te uiți la fiecare slide

Deschizi fiecare `slide-<N>.png` și verifici cu ochii:

- diacriticele au virgulă la ș și ț, nu lipsesc
- textul nu iese din imagine și nu e tăiat
- se citește peste fundal (dacă nu, regenerezi fundalul cu zona de text mai curată)
- layout-ul diferă de cel al slide-ului dinainte, la propriu: altă compoziție, nu doar alt text
- slide-urile arată ca un set, nu ca imagini din carusele diferite

Un fundal ratat se regenerează **o singură dată**. Cel mai des se întâmplă ca elementul să
urce peste zona de text. Catalogul cere deja elementul în jumătatea opusă zonei de text,
deci la regenerare ceri explicit elementul mai mic și mai jos în `--element`, ori muți zona
liberă cu `--zona center` sau `--zona "lower half"` la `stiluri.py` (opțiunea e a promptului
de fundal, nu a compunerii). Dacă nici a doua oară nu iese, problema e în prompt, nu în
noroc. Te oprești și îi spui omului ce nu merge.

## Costul

Costul se spune **înainte**, la pasul 2, nu doar la final. O generare înseamnă în jur de
6 credite și 60-100 de secunde.

Sarcina primită acoperă un carusel, câte un fundal pe slide generat (fără `panou`), plus cel mult
o regenerare pe slide. Orice în plus (variante, alt stil, încă un carusel) cere aprobarea
omului. Scriptul raportează creditele consumate la fiecare generare,
le aduni și le treci în raport.

## Pasul 6. Livrarea

În `../campanie/livrabile/carusel/` rămân `slide-1.png` ... `slide-N.png`, în ordine.
Fundalurile fără text rămân și ele, nu le ștergi.

Adaugi la finalul `../campanie/livrabile/carusel.md`:

```markdown
## Imagini produse
| Slide | Fișier | Regenerat? |
|---|---|---|

Credite consumate: [total din rapoartele scriptului]
```

Îi trimiți omului calea folderului, numărul de slide-uri și creditele consumate.
