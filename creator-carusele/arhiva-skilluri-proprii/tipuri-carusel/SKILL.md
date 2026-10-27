---
name: tipuri-carusel
description: Stabilește tipul caruselului (postare utilă, testimonial sau istorie personală) și stilul vizual potrivit nișei, cere materialele omului când e nevoie și dă structura de slide-uri și layout-urile. Rulează primul, înaintea structurii și a generării.
---

# tipuri-carusel

Primul pas la orice cerere de carusel. Dacă sari peste el, ies douăsprezece slide-uri care
arată la fel și nu spun nimic. Analiza caruselelor reale e în `referinte/analiza-tipuri.md`.

## Pasul 1. Ce tip de carusel e

| Tip | Când îl folosești | Ce duce povestea |
|---|---|---|
| **postare utilă** | înveți publicul ceva, explici un proces, spargi o credință greșită | pașii și explicațiile |
| **testimonial** (studiu de caz) | arăți rezultatul unui client și cum s-a ajuns la el | cifrele și dovezile |
| **istorie personală** | construiești apropiere, spui o poveste din viața ta | pozele proprii |

Tipul vine din brief. Dacă brieful nu îl spune, îl deduci din text și **anunți ce ai ales**,
în raportul tău. Nu îl alegi în tăcere.

## Pasul 2. Materialele omului

La **testimonial** și la **istorie personală** întrebi omul înainte să începi:

> Facem varianta generică, doar cu imagini generate, sau varianta personalizată, cu
> materialele tale? La cea personalizată am nevoie de poze sau capturi de ecran.

- **generică**: totul generat, fără nume și fără cifre pe care nu le poți dovedi;
- **personalizată**: omul pune fișierele în `../campanie/brief/materiale/`, iar tu le așezi
  în slide-uri cu opțiunea `--foto`.

Nu inventezi niciodată dovezi: nici capturi, nici cifre, nici citate de la clienți.
Dacă o cifră nu e în brief, nu apare pe slide.

## Pasul 3. Stilul vizual

Tipul spune **ce fel de poveste** e. Stilul spune **cum arată**. Sunt lucruri diferite:
o postare utilă a unui service auto și una a unui profesor de engleză au aceeași structură
și fundaluri complet diferite.

```bash
python3 scripts/stiluri.py --alege "<o frază din brief, cu nișa>"
```

Șase stiluri, în `cunostinte/stiluri-carusel.md`: `aurora`, `hartie-editoriala`,
`atelier`, `studio-cald`, `bloc-tipar`, `editorial-foto`.

`editorial-foto` e stilul de copertă de revistă, luat din caruselele de referință: cere
titluri de 3-4 cuvinte și nu merge la pași numerotați sau liste.

- dacă brieful spune explicit stilul, îl respecți;
- dacă pickerul găsește unul, îl anunți în raport, cu motivul;
- dacă pickerul spune că se potrivesc mai multe, **nu alegi tu**: arăți exemplele celor
  găsite și întrebi omul;
- dacă nu găsește nimic limpede, **întrebi omul**, cu trei variante și
  cu exemplele lor din `resurse/exemple-stiluri/`. Nu cazi automat pe aurora.

Stilul se alege **o dată** și rămâne același pe tot caruselul.

## Pasul 4. Structura, pe tipuri

Între 8 și 12 slide-uri. Sub 8 povestea nu prinde, peste 12 publicul se oprește.

**Postare utilă:** cârlig → problema recunoscută → de ce se întâmplă → promisiunea →
pașii (câte unul pe slide, cu cifra mare) → ce se schimbă după → îndemn.

**Testimonial:** rezultatul în cifre → cine e clientul → problema lui →
mecanismul folosit → pașii aplicați (cu dovezi) → rezultatele → ce urmează → îndemn.

**Istorie personală:** reperul de pornire („acum 10 ani”) → momentele, câte unul pe slide,
cu poze și două rânduri de text → ce ai învățat → privirea înainte → îndemn.

## Pasul 5. Layout-urile

Un layout pe slide, altul decât cel de dinainte. Două slide-uri consecutive nu au aceeași
compoziție. Unitatea vine din culori, fonturi și numerotare, nu din repetarea compoziției.

| Rol în poveste | Cum se compune | Compoziția (`--layout`) |
|---|---|---|
| copertă | `--eticheta --titlu1 --titlu2` | `foto-jos` |
| afirmație | `--titlu1 --titlu2 --text` | `panou` sau `citat` |
| pas numerotat | `--numar-mare 2 --titlu1 --text` | `foto-sus` |
| listă | `--titlu1 --lista "a|b|c"` | `panou` |
| cifră-rezultat | `--numar-mare "40.000" --titlu1 --text` | `foto-sus` |
| dovadă | `--titlu1 --text --dovada captura.png` | `dovada` |
| moment | `--eticheta "[ 2019 ]" --titlu1 --titlu2 --text` | `banda` |
| îndemn | `--titlu1 --titlu2 --text --logo` | `foto-jos` |

Numerotarea se pune pe fiecare slide: `--numar "03 / 12"`.

**Layout-ul e o decizie separată de rolul slide-ului.** Coloana a treia e punctul de
plecare, nu o lege: dacă două slide-uri vecine ar ieși cu aceeași compoziție, schimbi unul.
Catalogul de layout-uri și un ritm gata făcut pe opt slide-uri sunt în
`cunostinte/stiluri-carusel.md`.

Ține minte două lucruri practice: `panou` nu folosește fotografie, deci nu costă nicio
generare, iar `citat` cere o frază care merită centrată, nu orice text.

Rolul **dovadă** e singurul care cere materialul omului. Captura nu se pune pe slide
așa cum a venit: trece întâi prin `scripts/pregateste_captura.py`, care acoperă ce nu se
publică, marchează ce trebuie citit și pune rama. Vezi `genereaza-carusel`.

## Pasul 6. Ce predai mai departe

Scrii în capul fișierului `../campanie/livrabile/carusel.md`:

```markdown
Tip: [postare utilă | testimonial | istorie personală]
Stil: [aurora | hartie-editoriala | atelier | studio-cald | bloc-tipar]
Variantă: [generică | personalizată, cu materialele din ../campanie/brief/materiale/]
Număr de slide-uri: 
```

Stilul scris acolo e cel cu care lucrează `genereaza-carusel`, și la fundal, și la text.

Apoi treci la `structura-carusel`, care detaliază fiecare slide, și la `genereaza-carusel`,
care le produce.
