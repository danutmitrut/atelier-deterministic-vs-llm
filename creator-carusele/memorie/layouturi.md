# Layout-urile se diversifică, uniformitatea nu mai e un argument

Decizie de la Dănuț, 22 septembrie 2026, pornind de la o observație venită din afară pe
caruselul atelierului de ceramică.

Am livrat opt slide-uri `editorial-foto` cu blocul de text în același loc pe toate, și am
apărat asta în specificație ca fiind intenționată: stilul e un tratament tipografic fix,
de copertă de revistă, iar `cunostinte/stiluri-carusel.md` spune că unitatea vine din
culori, fonturi și numerotare. Argumentul nu a ținut. Răspunsul a fost, textual,
„nu mai facem nicio uniformitate".

**Ce înseamnă pentru mine:** nu mai invoc uniformitatea stilului ca motiv pentru care
slide-urile arată la fel. Unitatea o dau culorile, fonturile și numerotarea. Ritmul îl dă
alternanța de layout-uri.

**Starea uneltei, actualizată în aceeași zi:** motorul a fost modificat, limitarea nu mai
există. `compune_slide.py` primește `--layout` cu șase compoziții reale (`foto-sus`,
`foto-jos`, `banda`, `panou`, `citat`, `dovada`) plus `auto`, iar
`stiluri.py --prompt ... --layout` scoate un prompt de fundal potrivit layout-ului, ca
subiectul fotografiei să stea în jumătatea opusă textului. `panou` și `dovada` nu folosesc
deloc fotografie, deci nu le generezi fundal și nu plătești credite pe ele.

Tot atunci a intrat și voalul automat: pe fotografie, motorul măsoară fondul pe patru benzi
sub text și pune singur un strat dacă literele s-ar pierde. Nu întuneci tu imaginea
dinainte, ai strica fotografia degeaba.

**Regula pe care o aplic de acum:** aleg layout-ul pe fiecare slide, nu pe carusel, și nu
las două slide-uri vecine cu același layout. Excepția e un lanț de slide-uri de dovadă,
unde arhitectura cere dovezile una după alta. Ritmul verificat pe setul de ceramică e
`foto-jos | banda | citat | foto-sus | panou | banda | foto-sus | foto-jos`. Layout-ul îl
scriu în specificație, pe linia `Layout:` a fiecărui slide, înainte să generez fundalurile,
pentru că el decide și promptul fundalului.

**Și verific potrivirea stil-layout pe aceeași linie**, tot înainte de generări. Un stil cu
cerneală închisă peste `citat` dă text invizibil, iar fundalul generat pentru el e bani
aruncați. Pe 22 septembrie am plătit 6 credite pe un fundal care a ajuns la coș, fiindcă am
descoperit incompatibilitatea abia la compunere. Lista e în `cunostinte/stiluri-carusel.md`.
