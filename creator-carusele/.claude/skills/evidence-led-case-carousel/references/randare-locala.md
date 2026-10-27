# Randarea, pe mașina asta

> Fișier adăugat local pe 22 septembrie 2026. Nu face parte din skill-ul original.
> Skill-ul trimite la `carousel-builder`, care nu există aici. Randorul aprobat e setul de
> scripturi din `scripts/`. Versiunea completă a instrucțiunilor e în
> `arhiva-skilluri-proprii/genereaza-carusel/SKILL.md`.

## Uneltele

| Unealtă | Pentru ce |
|---|---|
| `scripts/stiluri.py` | catalogul de stiluri, promptul de fundal pe stil și pe layout |
| `scripts/cauta_foto.py` | fotografii reale de pe net, când omul nu trimite material |
| `scripts/kie_generate.py` | fundal generat, kie.ai, 4:5, 6 credite pe imagine |
| `scripts/compune_slide.py` | textul peste fundal, layout-urile, numerotarea, logo-ul |
| `scripts/pregateste_captura.py` | capturile omului: redactare, marcaj, decupaj, ramă |

Cheia kie.ai se citește singură din Keychain, serviciul `kie-api-key`. **Nu Infisical**,
cum spune `provider-access-check.md`: Infisical nu e instalat aici, iar regula locală e că
toate cheile stau în Keychain. Higgsfield nu există pe mașina asta.

## Cele șase stiluri

`aurora`, `hartie-editoriala`, `atelier`, `studio-cald`, `bloc-tipar`, `editorial-foto`.
Catalogul cu palete, tipografie și exemple gata făcute e în
`cunostinte/stiluri-carusel.md`. Alegerea automată:

```bash
python3 scripts/stiluri.py --alege "descrierea campaniei"
```

Dacă pickerul semnalează că se potrivesc mai multe, arăți exemplele și întrebi omul.
Stilurile cu cerneală închisă pe hârtie deschisă (`hartie-editoriala`, `studio-cald`) nu
merg cu layout-ul `citat`, care întunecă fotografia, și nici peste fotografii întunecate.

## Cele șapte layout-uri

| Layout | Ce face | Fundal |
|---|---|---|
| `foto-jos` | fotografia sus, textul intră de jos | da |
| `foto-sus` | textul în capul cadrului, fotografia dedesubt | da |
| `banda` | fotografia se oprește la 58%, textul pe o bandă plată | da |
| `citat` | fotografia întunecată, textul centrat sus | da |
| `panou` | fără fotografie, doar tipografie | nu |
| `dovada` | text sus, captura pregătită dedesubt, întreagă și dreaptă | nu |
| `auto` | alege după stil | da |

**Layout-ul se alege pe fiecare slide, nu pe carusel, și nu se repetă la două slide-uri
vecine.** Excepția e un lanț de slide-uri de dovadă, unde arhitectura cere dovezile una
după alta și dovezile în sine arată diferit.

## Ordinea de lucru

```bash
# 1. promptul de fundal, pentru layout-ul slide-ului
PROMPT=$(python3 scripts/stiluri.py --prompt <stil> --element "<elementul>" --layout <layout>)

# 2. fundalul: generat...
python3 scripts/kie_generate.py "$PROMPT" carusel/fundal-1.png --aspect 4:5
# ...sau o fotografie reală, vezi references/photo-sourcing.md
python3 scripts/cauta_foto.py "<cautare>" --iesire carusel/fundal-1.jpg

# 3. capturile omului, înainte să intre pe slide
python3 scripts/pregateste_captura.py captura.png pregatita.png \
  --zona "152,176,300,598:redactat" --decupaj "16,136,1068,644" --latime 900 --rama

# 4. compunerea
python3 scripts/compune_slide.py carusel/fundal-1.png carusel/slide-1.png \
  --stil <stil> --layout <layout> --titlu1 "..." --titlu2 "..." --text "..." --numar "01 / 08"

# slide fără fotografie
python3 scripts/compune_slide.py - carusel/slide-5.png --stil <stil> --layout panou ...

# slide de dovadă
python3 scripts/compune_slide.py - carusel/slide-4.png --stil <stil> --layout dovada \
  --dovada pregatita.png --titlu1 "..." --text "..."
```

## Ce face motorul singur

- **rupe textul pe rânduri și îl micșorează** dacă nu încape; dacă titlul a fost micșorat
  cu peste 14% sau blocul trece de 78% din zonă, scoate `avertisment` în JSON. Avertismentul
  se duce mai departe omului, nu se ascunde.
- **pune un voal sub text pe fotografii**, când fondul e prea aproape de culoarea textului.
  Măsoară pe patru benzi, nu pe medie. Se oprește cu `--fara-scrim`.
- **scrie textul local**, cu fonturile din `resurse/fonturi/`. Modelul de imagine nu
  desenează niciodată text: ș și ț ar ieși cu sedilă, nu cu virgulă.

## Două opriri obligatorii

1. **Stilul**, după ce îi arăți omului exemplul gata făcut din `resurse/exemple-stiluri/`.
2. **Costul**, înainte să pornești setul de generări. 6 credite pe imagine. Slide-urile
   `panou` și `dovada` nu costă nimic, nici fotografiile de pe net.

## La final

Deschizi fiecare slide și te uiți: diacriticele cu virgulă, textul netăiat, dovada lizibilă
fără zoom, niciun layout repetat la vecini, redactările chiar aplicate pe fișierele care
intră în carusel.

**Când ceva arată inconsecvent, nu îl explici ca intenție a stilului decât dacă ai
verificat în `scripts/stiluri.py` că stilul chiar cere asta.** Altfel îl raportezi ca
nelămurire, cu cuvintele tale: „pe slide-ul 7 lista iese cu litere mici, restul
caruselului e cu majuscule, nu știu de ce". O nelămurire spusă se repară. Una îmbrăcată în
„așa randează motorul" rămâne în carusel și devine problema omului, în fața publicului lui.

S-a întâmplat pe 23 septembrie 2026: lista de pe `panou` ieșea cu minuscule pe
`editorial-foto`, iar raportul a numit-o comportament al stilului. Era un bug în
`compune_slide.py`, punctele de listă nu treceau prin funcția care aplică majusculele.
Reparat în aceeași zi. Nu tu trebuie să ghicești unde e buba, dar tu trebuie să spui că
o vezi.
