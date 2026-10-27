# Arhitectura caruselului. Atelierul de ceramică

Structură după `templates/slide-architecture.md`. De aprobat înainte de pixeli.

## Marginea sursei
- Sursa principală: `brief-om.md`, plus `brief-uri.md` și `copy.md`
- Materiale: **zero**
- Goluri de acces: niciunul tehnic. Golul e că nu s-a cerut nimic.
- Stare consimțământ: implicit, fără artefact. Vezi `consent/consimtamant.md`.

## Tipul caruselului
- Tip ales: **Personal story**
- De ce: povestea e a unei persoane, la persoana întâi, cu cronologie (birou, subsol,
  martie 2024, acum)
- Public: oameni de birou, 28-45, care se tem că nu au talent
- Acțiune dorită: mesaj în privat

## Strategia vizuală

Aici se rupe. Skill-ul dă cinci tehnici pentru personal story:

| Tehnica | Ce cere | Avem? |
|---|---|---|
| dominant editorial photo | fotografie reală, cu drepturi | nu |
| personal timeline | fotografii din momente diferite | nu |
| collage + texture | fotografii, fragmente, obiecte | nu |
| behind-the-scenes proof | atelierul real | nu |
| one quote/thought per slide | doar text | **da** |

Patru din cinci cer materiale. Rămâne una singură, care e un carusel tipografic.

## Poarta hook-ului
- Hook: „Primul vas mi-a ieșit strâmb. Îl am și acum, pe raftul de sus."
- Stare: `PENDING`
- Verdict: **nu se schimbă hook-ul, se cere fotografia.** E cea mai bună frază din campanie
  și cea mai ieftină dovadă din tot proiectul. Obiectul există și e la doi metri de ea.

## Două drumuri

### Drumul A, recomandat: se cer fotografiile, apoi se face caruselul

Șapte fotografii, lista e în `evidence-inventory.md`. Cu primele trei se poate începe.
Textul Copywriterului rămâne neatins, nu are nimic de reparat.

| # | Rol | Titlu | Material | Compoziție |
|---|---|---|---|---|
| 01 | Hook | Primul vas mi-a ieșit strâmb | **foto: vasul strâmb pe raft** | dominant editorial photo |
| 02 | Înainte | Zece ani am lucrat la birou | textură sau obiect neutru | bandă tipografică |
| 03 | Mecanism | Mâinile învață înaintea capului | **foto: mâinile ei pe roată** | crop strâns |
| 04 | Momentul | Am deschis în martie | **foto: atelierul, două roți, cuptorul** | plan larg |
| 05 | Afirmație | Lutul nu iartă graba | **foto: forma prăbușită** sau panou | contrast |
| 06 | Ce faci | Ce faci într-o sâmbătă | **foto: raftul cu vase la uscat** | bandă |
| 07 | Oferta | Opt locuri pe serie | **foto: vase ale cursanților** | dovada că iese |
| 08 | Îndemn | Vino sâmbătă și fă-ți un vas | **foto: o cană terminată** | curat |

Slide-ul 7 câștigă cel mai mult: vasele unor oameni de birou care au dus un vas până la
capăt sunt exact dovada de care are nevoie cineva speriat că nu are talent. Opt căni
generate nu dovedesc nimic.

### Drumul B, dacă nu vin fotografiile: carusel care nu pretinde

Se păstrează textul, se schimbă contractul vizual. Nicio imagine nu mai pretinde că e
atelierul ei:

- tipografie pe suprafețe plate (`panou`), în paleta lutului;
- texturi abstracte, nu scene: lut, ipsos, pânză de in, fără roată, fără raft, fără atelier;
- nicio mână, niciun obiect care să pară al ei;
- în caption, o frază scurtă: fotografiile vin din serii viitoare.

Drumul B e cinstit, dar e un carusel mai slab. Nu pentru că arată mai prost, ci pentru că
nu dovedește nimic într-o campanie construită pe „o să-ți iasă prost și e în regulă".

## Ce am de spus despre caruselul deja livrat

Caruselul din `campanie/livrabile/carusel/` e bine făcut ca obiect vizual. Layout-urile
sunt variate, textul se citește, diacriticele sunt corecte, ritmul e bun. Prin poarta
skill-ului ăsta trece totuși cu două semnalări:

1. **E un drum A cu materiale de drum B.** Are contractul vizual al unui carusel
   documentat (fotografii de atelier, mâini, vase, praf în lumină) și materialele unui
   carusel tipografic (niciuna). Diferența o suportă cititorul.
2. **Un element cerut de Director a căzut fără să fie semnalat ca abatere.** Brieful cere
   opt elemente vizuale, unul pe slide, între care „o formă de lut prăbușită pe capul
   roții" pentru slide-ul 5. Slide-ul 5 a devenit `panou` și nu are nicio imagine.
   Decizia de layout e bună; lipsa e consemnată în specificație, dar nu ca abatere de la
   brieful Directorului. QC-ul din skill cere exact linia asta.

## QC
- [x] afirmațiile trecute prin poartă: 10, din care 5 `PENDING`
- [x] artefact de consimțământ: scris, cu ce lipsește
- [ ] dovezi vizibile: **niciuna**
- [ ] materiale reale acolo unde povestea depinde de o persoană reală: **nu**
- [x] abaterile de la brief, numite
