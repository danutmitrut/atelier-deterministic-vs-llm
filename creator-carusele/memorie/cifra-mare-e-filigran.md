# `--numar-mare` e filigran, nu mesaj

**23 septembrie 2026, caruselul „Drumul meu”, slide-ul 7.** Am pus `--numar-mare 6` cu
titlul „agenți AI”. Cifra a ieșit abia vizibilă, în colțul din dreapta sus, iar titlul
spunea doar „agenți AI”, fără câți.

Nu e bug. În `scripts/compune_slide.py`, blocul `if a.numar_mare` desenează cifra ca fundal
discret, la 12% opacitate, în dreapta sus. Pe un panou gol se vede, pe o fotografie
aglomerată dispare.

## Cum aplic

Când cifra e chiar mesajul slide-ului („6 agenți”, „40.000 de lei”), o pun în `--titlu1`,
nu în `--numar-mare`. `--numar-mare` rămâne pentru numărul pasului, unde e decor.
Și verific slide-ul la rezoluție întreagă, nu doar pe foaia de contact, unde filigranul
nu se vede deloc.
