---
name: deterministic-vs-llm
compatibility: claude-code-only
license: MIT
description: "Împarte un agent în pași și decide, pentru fiecare pas, ce face codul (determinist), ce face modelul (LLM) și unde se împletesc (hibrid), pe cinci criterii: repetabilitate, structură, cost, verificabilitate, risc. Merge pe un agent doar imaginat (mod plan) sau pe un agent deja construit, citit din folderul lui (mod audit). Scrie harta într-un fișier .md. Se declanșează cu /deterministic-vs-llm sau la formulări ca „ce las la LLM și ce scriu în cod”, „fă-mi harta agentului”, „care pași ar trebui să fie scripturi”, „auditează agentul ăsta”."
---

# Determinist sau LLM: harta pe pași a unui agent

Un agent bun are două părți care lucrează împreună. **Regizorul** e partea scrisă în cod:
face de fiecare dată exact același lucru, calculează, mută fișiere, decide ce urmează după
reguli fixe. **Vocea** e LLM-ul: înțelege limbaj liber, judecă, formulează. Nu decide
singur ce urmează și nu calculează nimic.

Skill-ul ăsta nu dă un verdict pe tot agentul („e bun pentru AI” sau „nu e”). Îl împarte
în pași și dă un verdict pe fiecare pas. Într-un agent real, cele două se împletesc.

## Reguli pentru tot parcursul

- Pui întrebările una câte una, câte una pe mesaj, și aștepți răspunsul. Nu anunți lista
  de pași dinainte.
- „Nu știu” e un răspuns valid. Îl notezi ca necunoscut și mergi mai departe. Nu completezi
  golurile cu presupuneri.
- NU INVENTA. Orice cifră pe care nu ți-a dat-o omul (volume, costuri) e marcată cu `*` ca
  estimare și spui din ce ai estimat-o.
- În modul audit nu modifici nimic în folderul agentului. Doar citești.
- Scrii în română, cu diacritice, fără liniuța lungă de dialog.

## Pasul 0. Alegi modul

Rulezi:

```
pwd; ls -A
```

- Dacă folderul curent are `CLAUDE.md` și cel puțin unul dintre `IDENTITY.md`,
  `.claude/skills/`, `scripts/`, e un agent construit. Propui **modul audit** pe acest
  folder și aștepți confirmarea.
- Altfel, întrebi: „Vrei să facem harta unui agent pe care încă nu l-ai construit (plan)
  sau a unui agent care există deja (audit)? Dacă există, spune-mi calea folderului lui.”

## Pasul 1a. Modul plan: afli ce face agentul

Întrebările, în ordine, câte una pe mesaj:

1. „Ce face agentul, într-o frază? Ce primește la început și ce predă la final?”
2. „Cât de des lucrează și pe cât material? De exemplu: 20 de emailuri pe zi, un articol
   pe săptămână, 300 de produse o dată pe lună.”
3. „Cine vede rezultatul înainte să ajungă la altcineva? Doar tu, un client, sau pleacă
   direct în public?”
4. „Dacă agentul greșește, ce se strică? Se poate repara ușor sau nu?”
5. „Cu ce lucrează: Gmail, Drive, un site, un serviciu cu cheie API, fișiere de pe
   calculator?”

## Pasul 1b. Modul audit: citești agentul

Citești, în ordinea asta:

1. `CLAUDE.md` și, dacă există, `IDENTITY.md`: ce face agentul și cum lucrează.
2. Fiecare `.claude/skills/*/SKILL.md`: descrierea din antet și pașii de lucru.
3. Folderul `scripts/` (sau orice fișiere `.py`, `.js`, `.sh`): numele fiecărui script și
   primele rânduri, ca să afli ce face.
4. `.mcp.json` și `.claude/settings.json`, dacă există: ce servicii sunt conectate și ce
   hooks rulează.
5. Folderul de memorie sau de lecții al agentului (`memorie/`, `MEMORY.md`), doar numele
   fișierelor și titlurile. Acolo se văd corecturile istorice: locurile unde modelul a
   greșit și s-a pus o regulă. Sunt indicii bune pentru pașii care ar trebui mutați în cod.

Din ce ai citit, reconstruiești fluxul agentului. Pentru întrebările 2-4 din modul plan
(volum, cine vede rezultatul, ce se strică), întrebi omul doar ce nu reiese din fișiere.

## Pasul 2. Împarți agentul în pași

Scrii o listă numerotată de 5-12 pași. Fiecare pas e un verb și un obiect, plus ce intră și
ce iese:

```
3. Clasifică emailul (intră: textul emailului; iese: una din etichetele urgent / normal / spam)
```

Un pas care face două lucruri diferite se sparge în doi. „Citește și răspunde” sunt doi
pași.

Arăți lista și întrebi: „Asta e fluxul? Lipsește ceva, e ceva în plus?” Nu treci mai
departe până nu confirmă.

## Pasul 3. Treci fiecare pas prin cele cinci criterii

| Criteriu | Întrebarea | Trage spre cod când... | Trage spre LLM când... |
|---|---|---|---|
| Repetabilitate | Aceeași intrare trebuie să dea mereu același rezultat? | da, rezultatul trebuie să fie identic de fiecare dată | variația e acceptabilă sau chiar dorită |
| Structură | Intrarea și ieșirea au formă fixă sau sunt limbaj liber? | formă fixă: numere, date, câmpuri, o listă închisă de valori | limbaj liber, texte scrise de oameni |
| Cost | De câte ori rulează pasul și pe cât text? | volum mare și sarcină simplă (codul nu consumă tokeni) | volum mic sau sarcină care chiar cere judecată |
| Verificabilitate | Poți verifica rezultatul cu o regulă? | da: există, are formatul corect, suma iese | nu, doar un om care citește își dă seama |
| Risc | Ce se strică dacă pasul greșește și se poate anula? | mult, ireversibil, cu bani, date sau trimiteri în afară | puțin și ușor de reparat |

Pentru fiecare pas notezi la fiecare criteriu: **C** (trage spre cod), **L** (trage spre
LLM) sau **?** (nu știm).

## Pasul 4. Dai verdictul pe fiecare pas

- **COD**: criteriile trag spre cod. Pasul devine script, formulă, filtru, apel API cu
  parametri ficși.
- **LLM**: limbaj liber, judecată, risc mic. Pasul rămâne în skill, cu instrucțiuni clare.
- **HIBRID**: le împletești și scrii explicit tiparul:
  - *LLM extrage, codul verifică*: modelul scoate datele din text liber, codul verifică
    forma (câmpurile există, data e validă, suma e număr).
  - *Codul decide, LLM formulează*: regizorul alege ce urmează după reguli, vocea scrie
    textul.
  - *LLM propune, omul aprobă*: modelul pregătește, un om confirmă înainte de efect.

Când criteriile se contrazic, decide riscul. Un pas cu risc mare nu rămâne la LLM singur,
oricât de bine ar merge modelul pe el.

Marchezi separat **aprobare umană** la orice pas care trimite ceva în afară, mișcă bani,
șterge sau publică.

## Pasul 5. Consum și securitate

**Consum.** Pentru pașii LLM și hibrizi estimezi câte apeluri la model înseamnă pe lună,
din răspunsul la întrebarea 2 (de exemplu „20 de emailuri pe zi, 3 pași LLM pe email:
aproximativ 1.800 de apeluri pe lună”). Marchezi estimarea cu `*`. Nu dai prețuri în bani
dacă omul nu ți-a spus ce plan sau ce model folosește.

**Securitate.** Notezi pașii care:

- folosesc o cheie API sau o parolă (cheia stă în Keychain sau în variabile de mediu,
  niciodată în prompt sau în fișierele agentului);
- trimit ceva în afară (email, postare, mesaj către client);
- șterg sau suprascriu date.

Pentru acești pași recomanzi o garanție în cod (un script care verifică, un hook care
blochează) sau aprobare umană. O limită scrisă doar în prompt e o rugăminte. O limită
verificată în cod e o garanție.

## Pasul 6. Scrii harta

Dacă în folderul curent există `arhitectura-mea.md` (template-ul de la atelier), completezi
acel fișier: înlocuiești comentariile `<!-- -->` și rândul de exemplu cu harta. Nu mai
întrebi unde salvezi.

Altfel, întrebi: „Unde salvez harta?” Propui `harta-<numele-agentului>.md` în folderul
curent. În modul audit, nu o salvezi în folderul agentului fără acordul omului.

Fișierul are exact structura asta:

```
# Harta determinist vs LLM: <numele agentului>

Data: <AAAA-LL-ZZ> · Mod: <plan / audit>

## Ce face agentul
<una-două fraze: ce primește, ce predă, cât de des>

## Pașii

| # | Pas | Intră → iese | Rep. | Str. | Cost | Verif. | Risc | Verdict | Cum se verifică |
|---|-----|--------------|------|------|------|--------|------|---------|-----------------|
| 1 | ... | ... | C | C | C | C | ? | COD | ... |

## Rezumat
<X pași COD, Y pași LLM, Z pași HIBRID. Pașii cu aprobare umană: ...>

## Consum și securitate
<estimarea de apeluri pe lună, marcată cu *; pașii sensibili și garanția recomandată>

## Recomandări
<cel mult trei, fiecare cu motivul. În modul audit: ce ar trebui mutat din LLM în cod
sau invers, față de cum e construit acum agentul.>

## Ce nu știm încă
<necunoscutele rămase și ce ar trebui aflat pentru fiecare>
```

## Pasul 7. Închidere

Spui în două propoziții unde e fișierul și care e cea mai importantă recomandare. Nu
modifici agentul și nu construiești scripturile, chiar dacă le-ai recomandat. Dacă omul
vrea să le construiască, e o sarcină separată.

## Semne după care recunoști un pas

**Semne de cod:** calcule și sume, date și ore, formatare, nume de fișiere, mutare și
copiere de fișiere, apeluri către un serviciu cu parametri cunoscuți, filtre pe reguli
exacte (expeditor, cuvânt anume, prag numeric), verificarea formatului, alegerea
următorului pas după o valoare fixă, rulare la oră fixă.

**Semne de LLM:** rezumat, rescriere într-un anumit ton, clasificare după criterii greu de
pus în reguli („e supărat clientul?”), extragere de informații din text scris liber,
alegeri editoriale, răspuns la întrebări neprevăzute, variante de text.

**Cele două capcane:**

- *LLM peste tot*: îi ceri modelului să numere, să calculeze, să respecte un format fix fără
  să verifice nimeni, sau să aplice o regulă de siguranță doar pentru că i-ai scris-o în
  prompt. Costă tokeni și greșește din când în când, fără să anunțe.
- *Cod peste tot*: scrii reguli fixe pentru limbaj natural („dacă emailul conține cuvântul
  «urgent»”). Merge până la prima formulare nouă, apoi se rupe.
