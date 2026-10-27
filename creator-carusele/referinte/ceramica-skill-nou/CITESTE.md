# Atelierul de ceramică, rulat cap-coadă cu skill-ul nou

Adăugat pe 22 septembrie 2026. E singura rulare completă a
`evidence-led-case-carousel` pe motorul din `scripts/`. Celelalte dosare din
`referinte/` sunt caruselele de referință, adică munca altcuiva, bună de studiat ca
tratament vizual. Ăsta e al tău, deci îl citești altfel: ca model al propriilor tale
livrabile.

**Citește avertismentul de mai jos înainte să copiezi ceva de aici.** Exemplul are o
scăpare pe care a recunoscut-o singur, în propria lui specificație.

## Ce e aici

| Fișier | Ce arată |
|---|---|
| `specificatie/evidence-inventory.md` | inventarul dovezilor pe un caz fără niciun material, cu afirmațiile trecute prin poartă |
| `specificatie/slide-architecture.md` | arhitectura, cu două drumuri: A cu materiale cerute, B fără |
| `specificatie/consimtamant.md` | artefactul de consimțământ pe articole, inclusiv ce lipsește |
| `specificatie/CREDITE.md` | creditele foto, autor și link pentru fiecare imagine |
| `contact-sheet.jpg` | cele opt slide-uri într-o pagină, ca să se vadă ritmul |
| `slide-uri/` | slide-urile, la 1024 px, ca să verifici lizibilitatea |

## Ce merită copiat

**Felul în care se scrie specificația.** `slide-architecture.md` e modelul: marginea
sursei, tipul, strategia vizuală cu tabelul tehnicilor și coloana „Avem?", poarta
hook-ului cu un verdict, tabelul rol-titlu-material-compoziție, apoi QC-ul cu bifele
puse cinstit, inclusiv cele nebifate. Observă că fișierul își critică propriul rezultat
la secțiunea „Ce am de spus despre caruselul deja livrat". Aia e purtarea corectă, nu o
scăpare de politețe.

**Cele două drumuri.** Când materialul lipsește, nu alegi în tăcere. Pui drumul A, cel
documentat, lângă drumul B, cel care nu pretinde nimic, spui care e mai slab și de ce,
și îl lași pe om să aleagă.

**Ritmul layout-urilor.** Verificat pe slide-urile de aici, în ordine:

```
1 foto-jos   2 banda   3 citat   4 foto-sus
5 panou      6 banda   7 foto-sus   8 foto-jos
```

Niciun vecin nu repetă compoziția. Stilul e `editorial-foto` pe tot setul, deci unitatea
vine din paletă, din tipografie și din pastila cu numărul, nu din așezare. Slide-ul 5 e
`panou`, fără fotografie, și face exact ce trebuie: e respiro între imagini, pe afirmația
cea mai tare din carusel.

**Creditele.** `CREDITE.md` e formatul: slide, rol, autor cu link, fotografie cu link.

## Ce NU se copiază

**Sursa imaginilor.** Toate cele șapte fotografii sunt de pe Unsplash. Nu sunt ale Anei.
Caruselul ăsta are contractul vizual al unui carusel documentat, atelier, mâini pe roată,
raft cu vase, și materialele unui carusel tipografic, adică niciunul. Diferența o suportă
cititorul, iar specificația o numește ea însăși abatere.

A fost o decizie de demonstrație, luată ca să se vadă cum arată drumul A dacă ar exista
materialele. Într-o campanie reală, o fotografie a atelierului altcuiva pusă sub textul
„am deschis în martie" e aceeași abatere ca o imagine generată: fotografia e reală, locul
nu e al omului.

Deci: dacă ajungi în aceeași situație, nu tragi concluzia „merge și cu stoc". Ceri
materialul, cu listă pe slide-uri, ca în `evidence-inventory.md`. Dacă omul tot vrea să
vadă caruselul întâi, îi spui o dată, în text, limpede, că fotografiile sunt ilustrative
și că devine documentat abia când trimite materialul. Regula întreagă e în
`references/photo-sourcing.md` din skill.

**Și nu copiezi conținutul.** Nici textele, nici Ana Crețu, nici cifrele. Doar felul de
a lucra.
