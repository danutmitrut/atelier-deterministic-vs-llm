# Skill-urile proprii ale agentului, scoase din uz pe 22 septembrie 2026

Cele trei skill-uri de aici au fost skill-urile active ale creatorului de carusele de pe
16 septembrie până pe 22 septembrie 2026: `tipuri-carusel`, `structura-carusel`,
`genereaza-carusel`. Au fost mutate aici la cererea lui Dănuț, ca să ia locul lor
`evidence-led-case-carousel`, skill-ul de referință.

**Nu sunt șterse și nu sunt depășite.** Partea lor de execuție, adică stilurile,
layout-urile, promptul de fundal, compunerea textului și pregătirea capturilor, e singura
care există: skill-ul de referință se oprește înaintea pixelilor. De aceea execuția a fost
rezumată în `.claude/skills/evidence-led-case-carousel/references/randare-locala.md`, iar
versiunea completă a rămas aici.

Ca să se întoarcă în uz:

    cp -R arhiva-skilluri-proprii/{tipuri-carusel,structura-carusel,genereaza-carusel} .claude/skills/

Ce conțin și nu se găsește nicăieri altundeva:

- `tipuri-carusel`: cele trei tipuri de carusel, alegerea stilului, tabelul rolurilor de
  slide cu layout-ul potrivit fiecăruia, regula vecinilor;
- `structura-carusel`: forma fișierului `carusel.md`, limitele de text măsurate pe
  slide-uri reale, linia `Layout:` obligatorie pe fiecare slide;
- `genereaza-carusel`: promptul de fundal pe layout, compunerea, pregătirea capturilor,
  voalul automat, verificarea finală cu ochii.
