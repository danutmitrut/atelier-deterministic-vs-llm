---
name: structura-carusel
description: Construiește caruselul campaniei din textul Copywriterului și brieful Directorului: slide-urile, ce stă pe fiecare, regulile vizuale aplicate. Rulează când primești sarcina de carusel.
---

# structura-carusel

Adaptat din biblioteca de agenți (`nova-designer`, skill-urile `img-carousel` și
`img-compose-post`, plus regulile din `GUARDRAILS.md`).

Aici produci **specificația caruselului**. Imaginile le produci după, cu `genereaza-carusel`,
direct din specificația asta. De aceea trebuie să fie atât de exactă încât imaginile să
poată fi produse din ea fără nicio întrebare în plus.

## Pasul 1. Ce citești

1. secțiunea „Brief. Creator de carusele" din `../campanie/strategie/brief-uri.md`
2. `../campanie/livrabile/copy.md`, secțiunea de carusel
3. regulile vizuale ale brandului din `cunostinte/`

**Textul vine înaintea vizualului.** Dacă `copy.md` nu există, nu începi.
Textul dictează compoziția, nu invers.

**Brandul vine înaintea oricărei decizii vizuale.** Dacă regulile vizuale lipsesc,
te oprești și ceri. Un carusel corect ca formă și străin ca identitate e exact eroarea
arătată pe scenă ca exemplu negativ.

## Pasul 2. Structura

- **Slide 1, coperta**: titlul principal și un element vizual puternic. Fără text dens.
- **Slide-urile din mijloc**: un singur punct pe slide, text mai mic, mult spațiu liber.
- **Ultimul slide**: un singur îndemn, clar, plus semnătura brandului.

**Fiecare slide primește un layout, scris în specificație.** Layout-ul e compoziția
(`foto-jos`, `foto-sus`, `banda`, `panou`, `citat`), separată de rolul slide-ului în
poveste. Catalogul și ritmul recomandat sunt în `cunostinte/stiluri-carusel.md`.
Două slide-uri vecine cu același layout sunt o greșeală, nu o alegere.

Limite:
- maximum 10 slide-uri, recomandat 5-7
- același font, aceeași paletă, același stil de fundal pe toate slide-urile
- un slide cu peste 50 de cuvinte e semnalat, nu predat ca atare

## Pasul 3. Dimensiunile

Formatul e vertical, 4:5, ca în caruselele de referință. Ocupă mai mult ecran în feed
decât pătratul și merge pe Instagram, Facebook și LinkedIn. Pătratul îl folosești doar
dacă brieful îl cere explicit.

## Pasul 4. Textul pe imagine sau în caption

**Pe imagine** când slide-ul are titlu sau când îndemnul trebuie să se vadă în imagine.
Un slide are loc pentru: o etichetă scurtă, un titlu în două bucăți (prima albă, a doua
colorată) și cel mult o frază sub el. Cu cât mai puțin text, cu atât arată mai bine la cameră.

Măsurile care ies bine la compunere, verificate pe slide-uri reale:

- titlul, până în 7-8 cuvinte cu tot cu al doilea rând; peste, scriptul îl micșorează și
  semnalează;
- fraza secundară, un singur rând, până în vreo 60 de caractere. Pe copertă mai ales: acolo
  fraza lungă cade peste elementul din imagine;
- lista, 3-4 puncte de câte 2-4 cuvinte.
**În caption** când imaginea vorbește singură.

Dacă textul e prea lung pentru a sta pe slide, nu îl tai tu. Propui mutarea în caption
și îi spui omului ce nu încape.

## Pasul 5. Fișierul

Scrie în `../campanie/livrabile/carusel.md`:

```markdown
# Carusel, [campania]

Tip: [postare utilă | testimonial | istorie personală]
Variantă: [generică | personalizată]
Platformă și format: [ex: Instagram și LinkedIn, 4:5]
Număr de slide-uri: 
Reguli vizuale aplicate: [ce fișier, ce culori, ce fonturi]

## Slide 1. Copertă
Rol: copertă
Layout: foto-jos
Etichetă: [// două-trei cuvinte, opțional]
Titlu, rândul alb: 
Titlu, rândul în gradient: [opțional]
Text secundar: [o frază, opțional]
Element vizual: [ce apare în lumina din jurul textului]

## Slide 2
Rol: [afirmație | moment | pas | listă | cifră | dovadă]
Layout: [altul decât la slide-ul anterior]
...

## Caption
[din copy.md, neschimbat]

## Semnalări
[slide-uri prea încărcate, text mutat în caption, orice abatere de la brief]
```

## Pasul 6. Mai departe

Treci direct la `genereaza-carusel`. Dacă ai semnalări care schimbă ce se generează
(text care nu încape, format diferit), le spui întâi omului și aștepți.
