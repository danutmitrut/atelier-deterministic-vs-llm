# Tipurile de carusel, structura și layout-urile

> Fișier adăugat local pe 22 septembrie 2026. Vine din skill-ul `tipuri-carusel` al
> agentului, integrat aici. Versiunea de dinainte e în `arhiva-skilluri-proprii/`.

Skill-ul are deja trei tipuri de producție. Sunt aceleași trei, cu numele lor de aici:

| În skill | La noi | Ce duce povestea |
|---|---|---|
| Review / success story | **testimonial**, studiu de caz | cifrele și dovezile |
| Useful explainer | **postare utilă** | pașii și explicațiile |
| Personal story | **istorie personală** | fotografiile proprii |

## Întrebarea de la început, înainte de orice

**Nu începi niciun carusel fără să întrebi omul ce fel de carusel vrea.** Nici când brieful
pare limpede. Tipul schimbă structura, materialele cerute, cât se verifică și cum arată
setul; ghicit greșit, se pierde toată munca.

Întrebi o singură dată, la început, și pui totul în același mesaj, pentru că răspunsurile
împreună decid ce urmează. Vii cu o propunere, nu cu un chestionar gol: propunerea o scoți
din brief, dacă există, sau din chiar fraza cu care ți-a cerut omul caruselul. Răspunsul
lui e de un cuvânt.

> Înainte să încep, două lucruri.
>
> **1. Ce vrei să facă acest carusel?**
> - **să înveți publicul ceva**, explici un proces sau spargi o credință greșită;
> - **să arăți un rezultat**, al tău sau al unui client, cu cifre și dovezi;
> - **să spui o poveste**, cum ai ajuns aici și ce ai învățat.
>
> Din ce mi-ai spus îmi pare că e **[propunerea ta]**. Confirmi sau schimbi.
>
> **2. Ai materiale?** Fotografii sau capturi de ecran care să apară pe slide-uri.
> Dacă nu ai, îți spun exact ce mi-ar folosi, pe fiecare slide. Până atunci pot lucra cu
> imagini ilustrative, dar trebuie să știi că ele nu sunt ale tale și nu dovedesc nimic.

Te oprești și aștepți răspunsul. Nu deduci, nu presupui, nu începi „ca să nu pierdem timp".

Dacă brieful spune explicit tipul, tot întrebi, dar scurt: spui ce zice brieful și ceri
confirmarea. Dacă omul nu răspunde la a doua întrebare, o repeți o dată, pentru că fără ea
nu știi dacă faci un carusel documentat sau unul ilustrat.

### Când nu există brief, cererea a venit direct în chat

[adaptare locala] Atunci brieful ești tu. Pui cele două întrebări de mai sus, și în același
mesaj, într-o singură linie fiecare, ce îți lipsește ca să poți propune textul:

> **Ca să îți propun textul, îmi mai trebuie:** pentru cine e (cine citește și ce îl
> preocupă), ce vrei să facă după ce vede caruselul, și câte slide-uri. Dacă nu ai o
> preferință la număr, propun opt.

Trei linii, nu un interogatoriu. Ce nu îți spune nu inventezi: dacă nu ai aflat o cifră,
un preț sau o dată, textul propus lasă golul la vedere, `[cifra?]`, și îl întrebi o dată,
la confirmarea textului. Un preț plauzibil pus de tine e o minciună pe slide-ul omului.

Pe calea asta ai o oprire în plus, **confirmarea textului**, înainte de stil și de cost.
Arăți textul întreg, slide cu slide, cu rolul fiecăruia. Abia după da mergi la pixeli.

Tipul ales, răspunsul despre materiale și sursa imaginilor intră în raport și în capul
specificației. Nu rămân doar în conversație.

## Cât din aparatul de dovezi se aplică, pe fiecare tip

Poarta afirmațiilor, inventarul și consimțământul nu apasă la fel pe toate trei. Pe o
postare utilă care nu pretinde nimic despre nimeni, inventarul complet e ceremonie.

### Testimonial, studiu de caz

Aparatul complet, fără scutire. E tipul pentru care a fost scris skill-ul.

- inventar pe fiecare material, cu rolul lui în taxonomie;
- stare pe fiecare afirmație: `VERIFIED`, `SUPPORTED BUT INDIRECT`, `PENDING`, `EXCLUDE`;
- hook-ul numai pe afirmația cea mai tare care are dovadă vizibilă;
- consimțământ pe articole, separat, inclusiv pentru terții din capturi;
- capturile trec prin `scripts/pregateste_captura.py` înainte de orice.

### Istorie personală

Aparatul se aplică, dar mută greutatea pe materiale, nu pe cifre.

- afirmațiile sunt biografice și aproape toate ies `PENDING` dacă omul nu trimite nimic.
  Asta nu le face false, le face nedovedite, și se scrie așa;
- **aici mușcă cel mai tare regula fotografiei.** Un text la persoana întâi („am deschis în
  martie", „îl am și acum pe raftul de sus") sub imagini care nu sunt ale omului e o
  reprezentare falsă, fie că imaginile sunt generate, fie luate de pe net. Vezi
  `photo-sourcing.md`;
- ceri lista de materiale pe slide-uri înainte să faci orice. De obicei una sau două
  fotografii schimbă tot caruselul;
- consimțământul e scurt, pentru că subiectul e chiar omul care a comandat caruselul, dar
  se scrie: aprobarea celui care comandă nu se presupune.

### Postare utilă

Aparatul se aplică **doar afirmațiilor factuale care chiar apar pe slide-uri**: cifre,
prețuri, termene, promisiuni de rezultat, „studiile arată că".

- inventarul poate fi o singură linie: „niciun material cerut, nicio afirmație despre o
  persoană";
- consimțământ: niciun artefact, dacă nu apare nimeni și nimic al nimănui;
- ce rămâne valabil integral: nu inventezi cifre. Dacă o cifră nu e în brief și nu are
  sursă, nu apare pe slide.

Când tipul e postare utilă, spui în raport, într-o frază, că ai sărit inventarul și de ce.
Nu tăcut.

## Materialele omului

Răspunsul la a doua întrebare de mai sus dă varianta:

- **documentată**: omul pune fișierele în `../campanie/brief/materiale/`. Asta e varianta
  care dovedește ceva;
- **generică**: fără nume și fără cifre pe care nu le poate dovedi, iar imaginile sunt
  ilustrative și se spune asta.

## Stilul vizual

Tipul spune **ce fel de poveste** e. Stilul spune **cum arată**. O postare utilă a unui
service auto și una a unui profesor de engleză au aceeași structură și fundaluri complet
diferite.

```bash
python3 scripts/stiluri.py --alege "<o frază din brief, cu nișa>"
```

Șase stiluri, catalogul în `cunostinte/stiluri-carusel.md`, motorul în `randare-locala.md`.

- dacă brieful spune explicit stilul, îl respecți;
- dacă pickerul găsește unul, îl anunți în raport, cu motivul;
- dacă pickerul spune că se potrivesc mai multe, **nu alegi tu**: arăți exemplele din
  `resurse/exemple-stiluri/` și întrebi omul;
- dacă nu găsește nimic limpede, întrebi omul, cu trei variante și exemplele lor.

Stilul se alege **o dată** și rămâne același pe tot caruselul.

`style-library.md` din skill dă etichete de direcție artistică („corporate-report",
„documentary-portrait"). Sunt vocabular pentru discuția cu omul, nu stiluri executabile.
Executabile sunt cele șase.

## Structura, pe tipuri

Între 8 și 12 slide-uri. Sub 8 povestea nu prinde, peste 12 publicul se oprește.

**Postare utilă:** cârlig → problema recunoscută → de ce se întâmplă → promisiunea →
pașii, câte unul pe slide, cu cifra mare → ce se schimbă după → îndemn.

**Testimonial:** rezultatul în cifre → cine e clientul → problema lui → mecanismul folosit
→ prima dovadă → rezultatul principal → dovada de proces → ce urmează → îndemn.

**Istorie personală:** reperul de pornire („acum zece ani") → momentele, câte unul pe
slide, cu fotografie și două rânduri → ce ai învățat → privirea înainte → îndemn.

Harta de roluri din `templates/slide-architecture.md` e construită pentru testimonial. Pe
celelalte două tipuri o adaptezi la schema de mai sus, păstrând coloanele: rol, titlu,
dovadă, compoziție, stare.

## Rolul slide-ului și layout-ul

Un layout pe slide, altul decât cel de dinainte. Două slide-uri vecine nu au aceeași
compoziție. Unitatea vine din culori, fonturi și numerotare, nu din repetarea compoziției.

| Rol în poveste | Cum se compune | Compoziția (`--layout`) |
|---|---|---|
| copertă | `--eticheta --titlu1 --titlu2` | `foto-jos` |
| afirmație | `--titlu1 --titlu2 --text` | `panou` sau `citat` |
| pas numerotat | `--numar-mare 2 --titlu1 --text` | `foto-sus` |
| listă | `--titlu1 --lista "a\|b\|c"` | `panou` |
| cifră-rezultat | `--numar-mare "40.000" --titlu1 --text` | `foto-sus` |
| dovadă | `--titlu1 --text --dovada captura.png` | `dovada` |
| moment | `--eticheta "[ 2019 ]" --titlu1 --titlu2 --text` | `banda` |
| îndemn | `--titlu1 --titlu2 --text --logo` | `foto-jos` |

Numerotarea se pune pe fiecare slide: `--numar "03 / 12"`.

**Layout-ul e o decizie separată de rolul slide-ului.** Coloana a treia e punctul de
plecare, nu o lege: dacă două slide-uri vecine ar ieși la fel, schimbi unul. Singura
excepție e un lanț de slide-uri de dovadă într-un testimonial, unde arhitectura cere
dovezile una după alta, iar dovezile în sine arată complet diferit.

Două lucruri practice: `panou` și `dovada` nu folosesc fotografie, deci nu costă nicio
generare, iar `citat` cere o frază care merită centrată, nu orice text.

## Ce scrii în capul specificației

```markdown
Tip: [postare utilă | testimonial | istorie personală]
Stil: [aurora | hartie-editoriala | atelier | studio-cald | bloc-tipar | editorial-foto]
Variantă: [documentată, cu materialele din ... | generică, imagini ilustrative]
Număr de slide-uri:
Sursa imaginilor: [materialele omului | fotografii de pe net, ilustrative | generate]
```

Ultima linie e nouă și e obligatorie. Cine citește caruselul peste o lună trebuie să știe
din ce e făcut, fără să deschidă imaginile.
