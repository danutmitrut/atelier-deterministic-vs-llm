# Ghid de lucru: harta determinist vs LLM

Atelier BAAI, 27 octombrie 2026

## Scop

La finalul atelierului ai două lucruri:

1. **`arhitectura-mea.md`**: harta unui agent pe care vrei să-l construiești. Pentru fiecare pas al agentului scrie ce face un script, ce face modelul și unde se împart.
2. **Comparația cu un agent real**: ce ai prevăzut la fel ca agentul de carusele, construit și folosit, și ce ai decide altfel după ce l-ai văzut.

## Precondiții

- Claude Code funcțional, în VS Code sau în terminal.
- O idee de agent pe care ai vrea să-l construiești în lunile următoare. O frază e suficientă: „un agent care îmi sortează emailurile de la clienți”, „un agent care face oferte din cererile primite pe site”.
- Materialele atelierului: https://github.com/danutmitrut/atelier-deterministic-vs-llm

## Partea 1: pregătirea

### Pasul 1. Descarci materialele

1. Deschizi linkul repo-ului în browser.
2. Apeși butonul verde **Code**, apoi **Download ZIP**.
3. Dezarhivezi fișierul. Se creează folderul `atelier-deterministic-vs-llm-main`.

Criteriu de succes: în folder vezi `README.md`, `GHID.md`, `arhitectura-mea.md`, folderul `deterministic-vs-llm` și folderul `creator-carusele`.

### Pasul 2. Instalezi skill-ul

Deschizi terminalul în folderul dezarhivat. În VS Code: **File > Open Folder**, alegi folderul, apoi **Terminal > New Terminal**.

**Mac:**

```
mkdir -p ~/.claude/skills && cp -R deterministic-vs-llm ~/.claude/skills/
```

**Windows** (terminalul trebuie să fie PowerShell, nu Command Prompt):

```
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null; Copy-Item -Recurse -Force deterministic-vs-llm "$env:USERPROFILE\.claude\skills\"
```

Criteriu de succes: într-o sesiune nouă de Claude Code scrii `/deter` și în listă apare `deterministic-vs-llm`.

### Pasul 3. Pregătești folderul hărții

1. Creezi un folder nou, separat de materiale, de exemplu `Documente/arhitectura-mea`.
2. Copiezi în el fișierul `arhitectura-mea.md` din materiale.
3. Deschizi folderul nou în VS Code (**File > Open Folder**).

Criteriu de succes: folderul deschis conține doar `arhitectura-mea.md`.

## Partea 2: cum se citește harta

Înainte să o faci, afli ce vei primi. Harta e un tabel. Fiecare rând e un pas al agentului. Coloanele din mijloc sunt cinci întrebări puse acelui pas:

| Criteriul | Întrebarea | Trage spre cod când... |
|---|---|---|
| Repetabilitate | Trebuie să iasă mereu exact la fel? | da, rezultatul trebuie să fie identic de fiecare dată |
| Structură | Lucrează cu date fixe sau cu text liber? | date fixe: numere, date, o listă închisă de valori |
| Cost | De câte ori rulează și pe cât material? | des, pe mult material, iar sarcina e simplă |
| Verificabilitate | Pot verifica rezultatul cu o regulă, fără să-l citesc? | da: există, are formatul corect, suma iese |
| Risc | Ce se strică dacă greșește și se poate repara? | mult, ireversibil, cu bani, date sau trimiteri în afară |

În fiecare celulă scrie **C** (criteriul trage spre cod), **L** (trage spre LLM) sau **?** (nu se știe încă).

Din aceste răspunsuri iese verdictul pasului:

- **COD**: pasul devine script. Exemplu: textul pus pe o imagine, la pixel, cu diacritice corecte.
- **LLM**: pasul rămâne la model. Exemplu: o conversație cu omul, în limbaj liber.
- **HIBRID**: se împart, după unul din trei tipare:
  - *LLM extrage, codul verifică.* Modelul scoate datele din text, scriptul verifică forma lor.
  - *Codul decide, LLM formulează.* Scriptul alege ce urmează, modelul scrie textul.
  - *LLM propune, omul aprobă.* Modelul pregătește, tu confirmi înainte de efect.

Ultima coloană, **„Cum se verifică”**, spune cine prinde greșeala la acel pas.

Trei reguli de reținut:

1. **Decizia se ia pe pas, nu pe agent.** Același agent are pași de cod, pași de LLM și pași hibrizi. Într-un agent real, cei mai mulți pași sunt hibrizi.
2. **Când criteriile se contrazic, decide riscul.** Un pas care publică, trimite ceva în afară, mișcă bani sau șterge nu rămâne la LLM singur.
3. **Dacă la un pas nu poți scrie cum se verifică, acolo te va surprinde agentul.** O limită scrisă doar în prompt e o rugăminte. O limită verificată în cod e o garanție.

## Partea 3, exercițiul 1: harta agentului tău

### Pasul 4. Pornești skill-ul

1. Deschizi Claude Code în folderul hărții.
2. Scrii `/deterministic-vs-llm` și apeși Enter.

Ce se întâmplă: skill-ul vede că folderul nu conține un agent și te întreabă dacă faci un **plan** (agent încă neconstruit) sau un **audit** (agent existent). Răspunzi „plan”.

### Pasul 5. Răspunzi la cele cinci întrebări

Skill-ul pune întrebările una câte una și așteaptă răspunsul. Răspunzi concret, cu cifre unde le ai. „Nu știu” e un răspuns acceptat: skill-ul îl notează și nu inventează în locul tău.

Model de răspunsuri, pentru un agent care face carusele de LinkedIn din articole:

| Întrebarea | Răspuns-model |
|---|---|
| Ce face agentul, ce primește, ce predă? | „Primește un articol lung de pe blogul meu și predă 8 slide-uri PNG plus textul postării.” |
| Cât de des, pe cât material? | „Două articole pe săptămână.” |
| Cine vede rezultatul înainte? | „Doar eu. Public eu, după ce mă uit.” |
| Ce se strică dacă greșește? | „O cifră sau un citat greșit apare public sub numele meu.” |
| Cu ce lucrează? | „Fișiere de pe calculator, un generator de imagini, o aplicație de publicare.” |

Tu răspunzi pentru agentul tău, nu pentru cel din model.

### Pasul 6. Verifici lista de pași

Skill-ul propune între 5 și 12 pași, fiecare cu ce intră și ce iese, și te întreabă dacă lista e corectă. Nu merge mai departe fără confirmarea ta.

Citești lista cu trei întrebări:

1. **Lipsește vreun pas?** Cel mai des lipsesc verificările: „verific că cifrele de pe slide există în articol”, „verific că emailul are destinatarul corect”.
2. **Face vreun pas două lucruri?** „Citește și răspunde” sunt doi pași. Îi ceri să-i despartă.
3. **E vreun pas inventat**, pe care agentul tău nu l-ar face? Îi ceri să-l scoată.

Criteriu de succes: lista confirmată descrie ce ar face agentul tău, de la început până la final.

### Pasul 7. Citești harta

Skill-ul completează `arhitectura-mea.md`. Îl deschizi în preview: `Cmd + Shift + V` pe Mac, `Ctrl + Shift + V` pe Windows.

Treci prin hartă în ordinea asta:

1. **Rezumatul**: câți pași de cod, câți de LLM, câți hibrizi.
2. **Un pas cu verdict COD.** Te întrebi: îl lăsam modelului dacă nu aveam harta?
3. **Un pas HIBRID.** Citești tiparul: cine face ce?
4. **Coloana „Cum se verifică”** pe pașii cu risc mare. Fiecare are o verificare în cod sau aprobarea ta?
5. **Consum și securitate**: câte apeluri la model pe lună și ce pași folosesc chei sau trimit ceva în afară.

Dacă un verdict ți se pare greșit, îi spui skill-ului de ce, de exemplu: „pasul 4 lucrează cu sume, nu poate fi LLM”. Skill-ul corectează harta.

Criteriu de succes: fiecare rând din tabel are verdict, iar fiecare pas cu risc mare are completată coloana „Cum se verifică”.

## Partea 4, exercițiul 2: comparația cu agentul real

### Pasul 8. Faci harta agentului de carusele

1. Deschizi Claude Code în folderul `creator-carusele` din materiale.
2. Scrii `/deterministic-vs-llm`. Skill-ul recunoaște un agent construit și propune modul **audit**. Confirmi.
3. Skill-ul citește fișierele agentului și propune pașii. Îi confirmi.
4. Când te întreabă unde salvează harta, îi dai folderul hărții tale: `harta-creator-carusele.md` lângă `arhitectura-mea.md`.

În modul audit, skill-ul doar citește, nu modifică nimic în agent.

### Pasul 9. Compari cele două hărți

Le deschizi una lângă alta și răspunzi la trei întrebări:

1. **Ce pași seamănă?** Căutare, scriere de text, generare de imagini, publicare. Au primit același verdict la tine și la agentul de carusele?
2. **Ce a pus agentul de carusele în cod, iar tu ai lăsat la LLM?** Exemple de acolo: filtrarea licențelor la fotografii, redactarea datelor sensibile de pe capturi, textul pus pe imagine.
3. **Ce verificare îți lipsește?** Uită-te în `creator-carusele/memorie/`. Fiecare fișier e o greșeală pe care modelul a făcut-o deja o dată. Există în agentul tău un pas unde s-ar putea întâmpla ceva asemănător?

Adaugi la finalul fișierului `arhitectura-mea.md` o secțiune nouă, `## Ce am luat din agentul de carusele`, cu răspunsurile.

## Criterii de validare

Ai terminat atelierul corect dacă:

- `arhitectura-mea.md` are tabelul completat pentru agentul tău, fără rândul de exemplu;
- fiecare pas cu risc mare are o verificare în cod sau aprobarea ta;
- secțiunea „Ce nu știu încă” spune ce trebuie aflat înainte de construcție;
- secțiunea „Ce am luat din agentul de carusele” are cel puțin o schimbare pe care o faci în harta ta.

## Cazuri-limită

- **`/deterministic-vs-llm` nu apare în listă.** Ai instalat skill-ul după ce ai pornit sesiunea. Pornești o sesiune nouă. Dacă tot nu apare, verifici că există fișierul `~/.claude/skills/deterministic-vs-llm/SKILL.md` (pe Windows, `%USERPROFILE%\.claude\skills\deterministic-vs-llm\SKILL.md`).
- **Skill-ul a scris harta în alt fișier decât `arhitectura-mea.md`.** Folderul deschis în Claude Code nu era cel cu template-ul. Deschizi folderul corect și pornești din nou.
- **Nu ai încă o idee de agent.** Faci harta agentului din modelul de răspunsuri (carusele din articole). Exercițiul 2 iese chiar mai clar, pentru că agentul real face același lucru.
- **Ai deja un agent construit** (de exemplu butler-inbox, de la atelierul din 12 octombrie). Îl poți trece prin modul audit, ca exercițiu suplimentar.

## Ce să nu faci

- Nu ceri skill-ului să construiască agentul. Harta e planul. Construcția e un pas separat.
- Nu accepți lista de pași fără să o citești. O hartă pe pași greșiți dă verdicte greșite.
- Nu completezi cifrele de volum din imaginație. Dacă nu știi, spui „nu știu”, iar skill-ul trece necunoscuta la final.
- Nu lași la LLM un pas care publică, plătește sau șterge doar pentru că „merge bine de obicei”.
