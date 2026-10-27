# `posts_create` întoarce „publishing", nu „published"

**23 septembrie 2026, prima publicare reală prin Zernio.** Caruselul de ceramică, opt
slide-uri, pe Instagram.

`posts_create` cu `publish_now=True` a răspuns pe loc cu „✅ Published" și cu id-ul
postării. Dar `posts_get` pe acel id a întors `Status: publishing`, și a rămas acolo la
două verificări consecutive. Abia după circa patruzeci de secunde a trecut pe `published`.

Mesajul de succes al lui `posts_create` înseamnă „Zernio a acceptat-o și a predat-o mai
departe", nu „e pe profil". Instagram procesează caruselul în partea lui, și cu cât sunt
mai multe imagini, cu atât durează.

## Cum aplic

Nu raportez „publicat" pe baza răspunsului de la `posts_create`. Verific cu `posts_get`
până statusul e `published`, și abia atunci îi spun omului că e live.

Dacă la prima verificare e `publishing`, îi spun starea reală („a plecat, Instagram o
procesează") și aștept, nu interoghez la nesfârșit. Un `sleep` scurt în fundal, apoi încă
o verificare, e de ajuns pentru un carusel de opt imagini.

Un status care rămâne `publishing` mult peste un minut, sau care trece pe `failed`, se
spune omului cu motivul, nu se reîncearcă la nesfârșit. Așa zice și
`references/publicare-zernio.md`.

## Ce a mai ieșit bine de știut

`incarca_media.py` scoate din PNG-uri de 2 la 3 MB niște JPEG-uri de circa 500 KB. Limita
Instagram e 8 MB **per imagine**, deci un carusel obișnuit e pe la 9% din plafon. Mărimea
nu e o problemă reală la stilurile noastre, dar se verifică cu `validate_media`, nu se
presupune. Legat de [[semnalarile-din-raport]]: o cifră verificată se dă cu cifra, nu cu
„încape lejer".
