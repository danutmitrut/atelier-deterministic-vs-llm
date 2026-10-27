# Atelier BAAI, 27 octombrie 2026: determinist sau LLM

Materialele atelierului „Al treilea instrument: skill-ul care îți arată câți pași LLM și câți pași cod”, din comunitatea Business Architect AI.

## Ce e aici

| Ce | Unde | La ce folosește |
|---|---|---|
| Skill-ul `deterministic-vs-llm` | `deterministic-vs-llm/SKILL.md` | împarte un agent în pași și spune, pentru fiecare pas, ce face codul, ce face modelul și unde se împletesc |
| Template-ul hărții | `arhitectura-mea.md` | harta unui agent pe care vrei să-l construiești; o completează skill-ul |
| Agentul de carusele | `creator-carusele/` | un agent real, construit și folosit, ca studiu de caz: scripturile sunt partea deterministă, skill-ul editorial e partea LLM |

## 1. Descarci materialele

Pe pagina repo-ului apeși **Code**, apoi **Download ZIP**, și dezarhivezi. Sau, dacă ai git:

```
git clone https://github.com/danutmitrut/atelier-deterministic-vs-llm.git
```

## 2. Instalezi skill-ul

Deschizi terminalul în folderul descărcat (cel în care e acest README).

**Mac** (în Terminal):

```
mkdir -p ~/.claude/skills && cp -R deterministic-vs-llm ~/.claude/skills/
```

**Windows** (în PowerShell):

```
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null; Copy-Item -Recurse -Force deterministic-vs-llm "$env:USERPROFILE\.claude\skills\"
```

Verificare: pornești o sesiune nouă de Claude Code și scrii `/deterministic-vs-llm`. Skill-ul trebuie să apară în listă.

## 3. Faci harta agentului tău

1. Creezi un folder nou, de exemplu `arhitectura-mea`, și copiezi în el `arhitectura-mea.md`.
2. Deschizi Claude Code în acel folder.
3. Scrii `/deterministic-vs-llm`, alegi modul **plan** și răspunzi la întrebări.

Skill-ul completează `arhitectura-mea.md` cu pașii agentului, verdictul pe fiecare pas, consumul, securitatea și recomandările.

## 4. Te uiți în agentul de carusele

Deschizi folderul `creator-carusele/` în VS Code sau în Finder/Explorer și compari:

- `scripts/`: partea deterministă. Compunerea slide-urilor, căutarea fotografiilor cu filtrarea licențelor, redactarea capturilor, încărcarea.
- `.claude/skills/evidence-led-case-carousel/`: partea LLM. Inventarul dovezilor, arhitectura slide-urilor, textul.
- `memorie/`: corecturile primite de agent. Arată unde a greșit modelul și ce regulă s-a pus după aceea.

Poți rula și skill-ul în modul **audit** pe el: deschizi Claude Code în `creator-carusele/` și scrii `/deterministic-vs-llm`. Skill-ul doar citește, nu modifică nimic.

## Dacă vrei să folosești agentul de carusele

Pentru atelier nu e nevoie: e suficient să-l citești. Ca să facă și carusele, îi trebuie:

- **Python 3** și **ImageMagick**. Pe Mac: `brew install imagemagick`. Pe Windows: `winget install ImageMagick.ImageMagick`.
- Completezi `USER.md` (cine ești) și pui logo-ul tău în `resurse/logo.png`.
- **Opțional**, cheia **kie.ai**, pentru fundaluri generate, și cheia **Zernio**, pentru publicare. Pe Mac le pui în Keychain, cu serviciile `kie-api-key` și `zernio-api-key`. Pe Windows le pui în variabilele de mediu `KIE_API_KEY` și `ZERNIO_API_KEY`. Fără ele, agentul lucrează cu fotografii reale de pe net și nu publică.

Ce nu e inclus, intenționat: caruselele făcute pentru clienți, fotografiile personale, brandurile clienților și caruselele de referință ale altor autori. Lecțiile despre ele au rămas în `referinte/analiza-*.md`.
