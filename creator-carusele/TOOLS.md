# Uneltele tale

Stabilite 16 septembrie 2026, completate pe 22 septembrie. Doar astea, nimic altceva.

| Unealtă | Pentru ce | Cum |
|---|---|---|
| `scripts/stiluri.py` | catalogul de stiluri, promptul de fundal pe stil și pe layout | local |
| `scripts/cauta_foto.py` | fotografii reale de pe net, când omul nu trimite material | cinci surse gratuite deodată, vezi mai jos |
| `scripts/kie_generate.py` | fundalul fiecărui slide, când nu merge o fotografie reală | kie.ai, modelul GPT Image 2, format 4:5 |
| `scripts/compune_slide.py` | textul slide-ului: etichetă, titlu, text, listă, cifră mare, număr, logo | ImageMagick |
| `scripts/pregateste_captura.py` | capturile omului, înainte să intre pe slide: acoperă datele care nu se publică, marchează dovada, decupează, pune ramă | ImageMagick |
| `scripts/compose_text.py` | un singur bloc de text, pentru cazuri speciale | ImageMagick |
| `scripts/incarca_media.py` | urcă slide-urile în stocarea Zernio și îți dă adresele publice | API-ul Zernio, cheia din seif |
| MCP `zernio` | publicarea propriu-zisă, după da-ul omului | plugin global, vezi mai jos |

**Căutarea de fotografii are cinci surse, și se caută în toate deodată.** Rezultatele
se intercalează, câte unul din fiecare sursă pe rând, ca să nu ocupe una singură toate
locurile. `--sursa` o restrânge la una anume, când știi că celelalte nu au subiectul.

| Sursă | Cheie | Ce aduce | Slăbiciunea |
|---|---|---|---|
| Unsplash | nu | fotografie profesionistă, calitate uniformă | descrierile mint des; caută cuvinte, nu înțelesuri |
| Openverse | nu | agregă Flickr, Wikimedia și altele; are subiecte tehnice pe care Unsplash nu le are, secțiuni, unelte, scheme | calitate neuniformă, multe fotografii amatoricești |
| Wikimedia Commons | nu | obiecte, locuri, piese, scheme, tot ce e documentar | rar ceva cu atmosferă; multe cadre plate, pe fundal alb |
| Pexels | da, `pexels-api-key` | apropiat de Unsplash ca gen, dar alt fond de imagini | aceeași problemă de descriere |
| Pixabay | da, `pixabay-api-key` | cel mai divers, inclusiv ilustrații și vectori | calitatea cea mai inegală dintre toate |

**Sursele cu cheie se sar în tăcere dacă nu e cheia în seif.** Nu e eroare, căutarea merge
mai departe cu celelalte trei. Cheile sunt gratuite, se iau de pe pexels.com/api și
pixabay.com/api/docs și se pun cu `cheie-set pexels-api-key`, respectiv
`cheie-set pixabay-api-key`. Le pune omul, nu tu.

**Din Openverse și Wikimedia intră doar licențele `cc0`, `pdm` și `by`.** Rămân afară
`nc`, `nd` și `sa`. Motivul e concret: pe un carusel punem text peste fotografie, ceea ce e
o modificare, iar caruselul e pentru o afacere. `nd` interzice modificarea, `nc` interzice
uzul comercial, iar `sa` ar obliga caruselul tău să poarte aceeași licență. Filtrul e în
script, nu se ocolește din linia de comandă. Unsplash, Pexels și Pixabay au licențe proprii,
permisive, care acoperă și modificarea, și uzul comercial.

Creditele întorc acum și sursa, și licența. Amândouă intră în `photo-credits.md`.

**Nicio căutare nu se ia de bună fără să te uiți la fotografii.** Toate sursele întorc
altceva decât scrie în descriere, destul de des cât să fie regulă, nu excepție: o
căutare după miezul unui croasant a adus faguri de miere, una după o mașină de tuns a
adus un telefon mobil, iar o căutare după unt a adus brânză cu busuioc. Ceri candidați
cu `--candidati`, faci o foaie de contact și alegi cu ochii.

**Capturile nu ajung niciodată pe un slide direct.** Trec întâi prin
`pregateste_captura.py`. Motivul e că o captură primită de la om conține aproape
întotdeauna ceva ce nu are voie să fie publicat: numele unui client, o adresă, un
sold, numărul de telefon al cuiva. Acoperirea e bară plină. Nu există blur și nu
există pixelare, pentru că pe text amândouă se pot inversa.

Cheia kie.ai se citește singură din seif (`kie-api-key`), cheia Zernio la fel
(`zernio-api-key`). Nu le ceri, nu le afișezi, nu le scrii nicăieri. Nu există și nu
creezi `.env`.

## Zernio

MCP-ul Zernio vine din pluginul global `zernio@zernio`, e pornit la nivel de cont și
îl vezi în orice sesiune. Nu are `.mcp.json` în folderul tău și nu îi faci unul: ar
fi a doua conexiune la același server, cu alt nume și cu o autorizare separată.

Uneltele pe care le folosești, în ordine:

| Unealtă | Pentru ce |
|---|---|
| `accounts_list` | ce conturi sunt legate și care e `account_id`-ul fiecăruia |
| `validate_media` | verifică o adresă de imagine și limita platformei, înainte să postezi |
| `posts_create` | ciorna sau postarea, cu `media_urls` lista de la `incarca_media.py` |
| `posts_get` | starea postării, după ce ai trimis-o |

Ce **nu** folosești din Zernio: `media_generate_upload_link` (îți dă o adresă pe care
ar trebui s-o deschidă omul în browser și să tragă fișierele de mână, iar tu ai deja
`incarca_media.py`), `posts_bulk_upload_posts`, `posts_cross_post` și tot ce ține de
inbox, comentarii, analytics sau ștergere. Nu ștergi postări și nu răspunzi la
comentarii în locul omului.

`account_id` se citește de fiecare dată cu `accounts_list`, nu din memorie și nu din
seif. Identificatorii se schimbă când omul reconectează un cont, iar o postare plecată
pe contul greșit nu se ia înapoi.

## Resursele brandului

`resurse/fonturi/` (Instrument Sans, JetBrains Mono și Playfair Display Black, folosit
doar de stilul `editorial-foto`) și `resurse/logo.png`, pe care îl pui tu (nu e inclus).
Logo-ul îl pune `compune_slide.py --logo`.

## Ce nu folosești

Higgsfield, HeyGen, orice alt MCP sau skill de generare de imagini sau video.
Din Zernio, doar cele patru unelte de mai sus, și numai după da-ul omului.

## Folderul comun

Contează doar când lucrezi la campania flotei. Citești din `../campanie/brief/`,
`../campanie/strategie/` și `../campanie/livrabile/`. Scrii doar
`../campanie/livrabile/carusel.md` și imaginile din `../campanie/livrabile/carusel/`.
Nu scrii niciodată în folderul altui agent.

**Pe cale directă nu atingi folderul campaniei.** Livrabilele merg în `iesiri/<nume-scurt>/`,
la tine, cu aceeași structură pe care o cere skill-ul: `source/`, `consent/`, `carusel/`.
Dacă folderul `../campanie/` nici nu există, nu e o eroare, înseamnă doar că agentul rulează
în afara flotei.

## Ce nu atingi

Nimic din afara folderului flotei (folderul care conține acest agent și `campanie/`).
