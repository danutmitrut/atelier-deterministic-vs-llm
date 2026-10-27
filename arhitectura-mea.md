# Arhitectura mea: <numele agentului>

<!--
Template pentru atelierul BAAI din 27 octombrie 2026.

Cum îl folosești:
1. Pui fișierul ăsta într-un folder gol, de exemplu `~/agenti/arhitectura-mea/`.
2. Deschizi Claude Code în acel folder și scrii `/deterministic-vs-llm`.
3. Alegi modul plan și răspunzi la întrebări. Skill-ul completează fișierul ăsta.

Poți să-l completezi și de mână: urmezi întrebările din fiecare secțiune.
Comentariile ca acesta nu se văd când deschizi fișierul ca document. Le poți lăsa.
-->

Data: <AAAA-LL-ZZ> · Mod: plan

## Ce face agentul

<!--
Una-două fraze. Răspunsurile la:
- Ce face agentul? Ce primește la început și ce predă la final?
- Cât de des lucrează și pe cât material? (de exemplu: 20 de emailuri pe zi)
- Cine vede rezultatul înainte să ajungă la altcineva?
- Ce se strică dacă greșește? Se poate repara ușor?
- Cu ce lucrează: Gmail, Drive, un site, un serviciu cu cheie API, fișiere de pe calculator?
-->

## Pașii

<!--
5-12 pași. Fiecare pas e un verb și un obiect, plus ce intră și ce iese.
Un pas care face două lucruri se sparge în doi: „citește și răspunde” sunt doi pași.

Pentru fiecare criteriu scrii C (trage spre cod), L (trage spre LLM) sau ? (nu știu încă):
- Rep. (repetabilitate): trebuie să iasă mereu exact la fel? Da = C.
- Str. (structură): date fixe (numere, date, o listă de valori) = C; text liber = L.
- Cost: rulează des, pe mult material, și sarcina e simplă = C.
- Verif. (verificabilitate): rezultatul se verifică cu o regulă = C; doar citind = L.
- Risc: greșeala strică mult sau nu se poate anula = C.

Verdictul: COD, LLM sau HIBRID. La HIBRID scrii și tiparul:
- LLM extrage, codul verifică
- codul decide, LLM formulează
- LLM propune, omul aprobă
Adaugi „+ aprobare umană” la orice pas care trimite ceva în afară, mișcă bani, șterge sau publică.

Primul rând e un exemplu din agentul de carusele. Îl ștergi când scrii pașii tăi.
-->

| # | Pas | Intră → iese | Rep. | Str. | Cost | Verif. | Risc | Verdict | Cum se verifică |
|---|-----|--------------|------|------|------|--------|------|---------|-----------------|
| ex. | Caută fotografiile | descrierea slide-ului → fotografie plus credite | L | C | C | C | C | HIBRID: LLM formulează căutarea, codul filtrează licențele | scriptul păstrează doar licențele permise și scrie creditele |
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |
| 4 | | | | | | | | | |
| 5 | | | | | | | | | |

## Rezumat

<!--
Câți pași COD, câți LLM, câți HIBRID. Care pași au aprobare umană.
-->

## Consum și securitate

<!--
Consum: câte apeluri la model înseamnă pe lună. Exemplu: 20 de emailuri pe zi,
3 pași LLM pe email, aproximativ 1.800 de apeluri pe lună. Marchezi cu * ce e estimat.

Securitate: pașii care folosesc o cheie API sau o parolă, care trimit ceva în afară,
care șterg sau suprascriu date. Pentru fiecare: ce garanție are (un script care verifică,
un hook care blochează, aprobarea ta).
Cheile stau în Keychain sau în variabile de mediu, niciodată în prompt sau în fișierele agentului.
-->

## Recomandări

<!--
Cel mult trei, fiecare cu motivul. Ce ar trebui să fie script de la început,
unde e nevoie de aprobarea ta, ce ar trebui verificat în cod.
-->

## Ce nu știu încă

<!--
Necunoscutele rămase și ce ar trebui aflat pentru fiecare înainte de construcție.
-->
