# Publicarea prin Zernio

[adaptare locala] Skill-ul original se oprea la fisierele de pe disc. Aici caruselul
pleaca mai departe, pe contul omului, prin Zernio.

Publicarea nu face parte din sarcina implicita. O faci doar daca omul ti-a cerut-o.
„Fa-mi caruselul" se termina cu fisierele si cu raportul, nimic mai mult.

## Ordinea

**1. Verifici contul, inainte de orice.** `accounts_list`. Te uiti ce platforme sunt
legate si iei `account_id`-ul exact al contului pe care pleaca postarea. Daca
platforma ceruta nu apare in lista, te opresti aici si spui omului ca nu e conectata.
Nu improvizezi alta platforma si nu presupui ca s-a conectat intre timp. Nu iei
`account_id` din memorie, din seif sau dintr-o sesiune trecuta: se schimba cand omul
reconecteaza un cont.

**2. Incarci slide-urile.**

```
python3 scripts/incarca_media.py --dosar ../campanie/livrabile/carusel --json /tmp/media.json
```

Din dosar ia **doar fisierele `slide-*`** si le sorteaza natural, deci `slide-10` vine dupa
`slide-9`, nu dupa `slide-1`. Fundalurile stau in acelasi dosar si se cheama `fundal-*`:
fara filtru, caruselul ar fi plecat cu opt fundaluri brute in fata, fiindca `f` vine
inaintea lui `s`. Iti spune cate fisiere a ignorat. Alt prefix, cu `--tipar`; chiar tot,
cu `--toate`.

Le converteste in JPEG la calitate 92 (Instagram recomprima oricum, iar opt slide-uri scad
de la ~20 MB la ~3 MB) si se opreste singur in trei cazuri: peste 10 imagini, care e limita
unui carusel Instagram; rapoarte diferite intre slide-uri, fiindca Instagram ar decupa
singur; un fisier peste 8 MB. Iti da inapoi `media_urls`, gata de pus in `posts_create`.

Fisierele stau in stocarea temporara Zernio sapte zile. Deci incarci si publici in
aceeasi sesiune. Daca omul amana raspunsul o zi, reincarci, nu refolosesti adresele.

**3. Scrii textul postarii.** Nu e caruselul rescris. E ce vede omul in feed inainte
sa dea pe prima imagine: carligul din slide-ul 1 in propriile lui cuvinte, apoi
contextul, apoi indemnul. Hashtagurile la final, putine si reale.

Daca ai folosit fotografii de stoc, creditele intra in text sau in primul comentariu,
dupa ce s-a cerut in `photo-sourcing.md`. Nu le lasi doar in
`source/photo-credits.md`: acolo nu le vede nimeni.

**4. Te opresti si intrebi.** Intr-un singur mesaj ii arati:

- platforma si contul, cu numele afisat asa cum l-a intors `accounts_list`
- textul postarii, intreg
- lista slide-urilor in ordine, cu o descriere de cateva cuvinte fiecare
- daca pleaca acum sau ramane ciorna

Apoi astepti. Un da pe carusel nu e un da pe postare. Un „arata bine" pe imagini nu e
un da pe postare. Ai nevoie de un raspuns care spune limpede ca poate pleca.

**5. Publici.**

```
posts_create(
  content = "<textul>",
  platform = "instagram",
  account_id = "<de la accounts_list>",
  media_urls = "<lista virgula, din incarca_media.py>",
  publish_now = True
)
```

Fara `account_id` omul are mai multe conturi si unealta fie da eroare, fie nimereste
altundeva. Il pui mereu, chiar si cand e un singur cont pe platforma.

`is_draft = True` in loc de `publish_now` cand omul vrea sa se uite intai in Zernio.
Ciorna e raspunsul bun ori de cate ori nu esti sigur.

**6. Confirmi.** `posts_get` pe id-ul intors, si ii spui omului starea si adresa
postarii. Daca a esuat, ii spui de ce, nu reincerci la nesfarsit.

## Ce nu faci

Nu publici fara da. Nu publici pe alta platforma decat cea ceruta, nici „si pe
LinkedIn, ca tot era acolo". Nu stergi postari si nu raspunzi la comentarii: aia e
gura omului, nu a ta. Nu folosesti `media_generate_upload_link`, fiindca cere browser
si om, iar tu ai scriptul.

Nu publici din proprie initiativa un carusel care are o afirmatie ramasa `PENDING` in
`source/evidence-inventory.md`. Pe disc, o afirmatie nesustinuta e o problema de
corectat. Publicata, e o problema a omului.

**Dar semnalarea se face o singura data, si decizia e a lui.** Ii spui ce e `PENDING`
si ce risca, intr-un singur loc, la oprirea 3. Daca dupa aia cere publicarea, publici si
scrii in `publicare/postare.md` ce era nesustinut si ca a fost decizia lui, cu data. Nu
repeti avertismentul la fiecare mesaj si nu il transformi intr-un refuz pe ocolite.
Demonstratiile si testele de flux sunt exact cazul in care omul stie ce publica.
