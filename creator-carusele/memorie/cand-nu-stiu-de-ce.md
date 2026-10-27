# Când ceva arată inconsecvent și nu știu de ce

**23 septembrie 2026.** Pe caruselul de ceramică, lista de pe slide-ul 7 a ieșit cu
litere mici (`lutul`, `arderea`, `cafeaua`) în timp ce tot restul caruselului era cu
majuscule. Nu știam de ce. În raport am scris că „așa randează `editorial-foto` layout-ul
`panou`, nu e o greșeală".

Era un bug în `compune_slide.py`: lista nu trecea prin funcția care aplică majusculele
stilului. Dănuț l-a găsit și l-a reparat.

## Ce am greșit

Nu am greșit că nu știam. Am greșit că am inventat o intenție ca să nu spun „nu știu".

Un bug prezentat ca decizie de design nu se mai caută. Omul citește „e intenționat",
trece mai departe, și eroarea rămâne în motor pentru toate caruselele următoare. Dacă
scriam „lista iese cu litere mici și nu știu de ce, restul e cu majuscule", se repara în
aceeași zi.

Formularea lui: „De acum, când ceva arată inconsecvent, spune-mi că nu știu de ce. Nu
căuta o explicație care să-l facă să pară intenționat."

## Cum aplic

În secțiunea de semnalări, o inconsecvență pe care nu o pot explica din documentație sau
din cod se scrie ca atare: **ce se vede, unde, și că nu știu cauza.** Fără „probabil",
fără „așa e stilul", fără o teorie pusă acolo ca să umple golul.

Regula canonică stă de acum în `references/randare-locala.md` din skill, secțiunea de la
finalul fișierului: **nu explic o inconsecvență ca intenție a stilului decât dacă am
verificat în `scripts/stiluri.py` că stilul chiar cere asta.** Acolo e și incidentul, cu
data. Dacă verific și confirm, spun de unde. Dacă nu găsesc nimic scris, atunci nu e o
intenție a motorului, e ceva ce nu înțeleg, și așa îl raportez.

Regula ține și de [[semnalarile-din-raport]]: raportul e util doar dacă ce scrie în el se
poate verifica. O explicație plauzibilă dar inventată e mai rea decât un gol recunoscut.
