#!/usr/bin/env python3
"""Cauta pe Unsplash si Openverse o fotografie potrivita pentru un slide si o descarca.

Se foloseste cand povestea cere o fotografie reala si omul nu a trimis materialul
lui. Nu inlocuieste materialul omului: daca povestea e despre atelierul lui, o
fotografie de stoc arata atelierul altcuiva. Vezi avertismentul de la final.

Doua surse, cautate impreuna, castiga cea mai potrivita indiferent de unde vine:

  unsplash   fotografie profesionista, calitate uniforma, descrieri inselatoare
  openverse  agrega Flickr, Wikimedia si altele; acopera subiecte tehnice pe care
             Unsplash nu le are (sectiuni, scheme, unelte), calitate neuniforma

Filtreaza fotografiile Unsplash+, care vin cu filigran peste toata imaginea. Din
Openverse ia doar licentele care permit si uz comercial, si modificare: cc0, pdm
si by. Lasa afara nc (fara comercial), nd (fara modificari) si sa (obliga lucrarea
ta sa poarte aceeasi licenta), fiindca pe un carusel punem text peste fotografie,
ceea ce e o modificare, iar caruselul e pentru o afacere.

Ordoneaza rezultatele dupa cuvintele cerute si cele interzise, descarca prima
potrivire si scrie creditele, care sunt obligatorii.

Exemple:
  # o singura cautare
  python3 scripts/cauta_foto.py "pottery wheel studio" --iesire foto/atelier.jpg \\
      --vreau wheel,pottery --nu-vreau hand,person

  # mai multi candidati, ca sa alegi cu ochii
  python3 scripts/cauta_foto.py "office desk daylight" --candidati 4 --iesire /tmp/birou

  # mai multe cautari deodata, dintr-un fisier JSON
  python3 scripts/cauta_foto.py --plan plan-foto.json --dosar material-primit/

  # doar o sursa, cand stii ca cealalta nu are subiectul
  python3 scripts/cauta_foto.py "croissant cross section" --sursa openverse --iesire /tmp/c.jpg
"""
import argparse
import json
import os
import subprocess
import sys

API = "https://unsplash.com/napi/search/photos"
OPENVERSE = "https://api.openverse.org/v1/images/"
PEXELS = "https://api.pexels.com/v1/search"
PIXABAY = "https://pixabay.com/api/"
COMMONS = "https://commons.wikimedia.org/w/api.php"
AGENT = "creator-carusele/1.0"
# licentele care permit si uz comercial, si modificare; vezi docstring
LICENTE = "cc0,pdm,by"


def curl(url, iesire=None, agent=None):
    # Unsplash: fara User-Agent, cu unul raspunde cu pagina de verificare anti-bot
    # Openverse: invers, cere un User-Agent ca sa raspunda
    cmd = ["curl", "-sL", "--max-time", "60", url]
    if agent:
        cmd += ["-H", f"User-Agent: {agent}"]
    if iesire:
        r = subprocess.run(cmd + ["-o", iesire])
        if r.returncode != 0:
            sys.exit(f"descarcarea a esuat: {url}")
        return None
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        sys.exit(f"cautarea a esuat: {url}")
    return r.stdout


def cauta_unsplash(text, pe_pagina=20):
    import urllib.parse
    brut = curl(f"{API}?query={urllib.parse.quote(text)}&per_page={pe_pagina}")
    try:
        d = json.loads(brut)
    except json.JSONDecodeError:
        sys.exit("Unsplash a raspuns cu altceva decat JSON, probabil verificare anti-bot")
    iesire = []
    # „plus" sunt fotografiile Unsplash+, cu filigran peste toata imaginea
    for r in d.get("results", []):
        if r.get("plus"):
            continue
        iesire.append({
            "sursa": "unsplash", "id": r["id"],
            "autor": r["user"]["name"],
            "profil": f"https://unsplash.com/@{r['user']['username']}",
            "pagina": r["links"]["html"],
            "descriere": r.get("alt_description"),
            "licenta": "Unsplash License",
            # raw + parametri: Unsplash redimensioneaza el, nu descarcam 20 MB
            "descarcare": r["urls"]["raw"],
            "redimensioneaza_singur": False,
        })
    return iesire


def cauta_openverse(text, pe_pagina=20):
    import urllib.parse
    url = (f"{OPENVERSE}?q={urllib.parse.quote(text)}"
           f"&license={LICENTE}&page_size={pe_pagina}")
    brut = curl(url, agent=AGENT)
    try:
        d = json.loads(brut)
    except json.JSONDecodeError:
        print("Openverse nu a raspuns cu JSON; continui doar cu Unsplash", file=sys.stderr)
        return []
    iesire = []
    for r in d.get("results", []):
        if not r.get("url"):
            continue
        descriere = " ".join(filter(None, [
            r.get("title"),
            " ".join(e.get("name", "") for e in (r.get("tags") or [])[:8]),
        ]))
        iesire.append({
            "sursa": f"openverse/{r.get('source')}", "id": r["id"],
            "autor": r.get("creator") or "autor necunoscut",
            "profil": r.get("creator_url") or r.get("foreign_landing_url"),
            "pagina": r.get("foreign_landing_url"),
            "descriere": descriere.strip() or None,
            "licenta": f"CC {(r.get('license') or '').upper()} {r.get('license_version') or ''}".strip(),
            "descarcare": r["url"],
            "redimensioneaza_singur": True,
        })
    return iesire


def cheie(nume):
    """Citeste o cheie din Keychain. Lipsa ei nu e eroare: sursa se sare in tacere."""
    r = subprocess.run(["cheie", nume], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def cauta_pexels(text, pe_pagina=20):
    k = cheie("pexels-api-key")
    if not k:
        return []
    import urllib.parse
    url = f"{PEXELS}?query={urllib.parse.quote(text)}&per_page={pe_pagina}"
    r = subprocess.run(["curl", "-sL", "--max-time", "60", url,
                        "-H", f"Authorization: {k}"], capture_output=True)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return []
    return [{
        "sursa": "pexels", "id": f"px{f['id']}",
        "autor": f.get("photographer") or "autor necunoscut",
        "profil": f.get("photographer_url"),
        "pagina": f.get("url"),
        "descriere": f.get("alt") or None,
        "licenta": "Pexels License",
        "descarcare": (f.get("src") or {}).get("large2x") or (f.get("src") or {}).get("original"),
        "redimensioneaza_singur": True,
    } for f in d.get("photos", []) if (f.get("src") or {}).get("original")]


def cauta_pixabay(text, pe_pagina=20):
    k = cheie("pixabay-api-key")
    if not k:
        return []
    import urllib.parse
    url = (f"{PIXABAY}?key={k}&q={urllib.parse.quote(text)}"
           f"&image_type=photo&per_page={pe_pagina}&safesearch=true")
    brut = curl(url)
    try:
        d = json.loads(brut)
    except json.JSONDecodeError:
        return []
    return [{
        "sursa": "pixabay", "id": f"pb{h['id']}",
        "autor": h.get("user") or "autor necunoscut",
        "profil": f"https://pixabay.com/users/{h.get('user')}-{h.get('user_id')}/",
        "pagina": h.get("pageURL"),
        "descriere": (h.get("tags") or "").replace(",", " ") or None,
        "licenta": "Pixabay Content License",
        "descarcare": h.get("largeImageURL"),
        "redimensioneaza_singur": True,
    } for h in d.get("hits", []) if h.get("largeImageURL")]


def cauta_commons(text, pe_pagina=20):
    """Wikimedia Commons. Are subiecte enciclopedice pe care bancile de stoc nu le au,
    dar cele mai multe fisiere sunt BY-SA, care nu ne convine. Filtram pe licenta."""
    import re
    import urllib.parse
    url = (f"{COMMONS}?action=query&generator=search"
           f"&gsrsearch={urllib.parse.quote('filetype:bitmap ' + text)}"
           f"&gsrnamespace=6&gsrlimit={pe_pagina}&prop=imageinfo"
           f"&iiprop=url|extmetadata&iiurlwidth=1600&format=json")
    brut = curl(url, agent=AGENT)
    try:
        d = json.loads(brut)
    except json.JSONDecodeError:
        return []
    iesire = []
    for _, v in ((d.get("query") or {}).get("pages") or {}).items():
        ii = (v.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata") or {}
        lic = ((em.get("LicenseShortName") or {}).get("value") or "").strip()
        l = lic.lower()
        # acceptam doar domeniu public, CC0 si CC BY curat; fara sa, nc, nd
        curata = ("cc0" in l or "public domain" in l
                  or (l.startswith("cc by") and not any(x in l for x in ("-sa", "-nc", "-nd"))))
        if not curata or not ii.get("thumburl"):
            continue
        autor = re.sub("<[^>]+>", "", (em.get("Artist") or {}).get("value") or "").strip()
        iesire.append({
            "sursa": "wikimedia", "id": v.get("title"),
            "autor": autor or "autor necunoscut",
            "profil": ii.get("descriptionurl"),
            "pagina": ii.get("descriptionurl"),
            "descriere": (v.get("title") or "").replace("File:", "").rsplit(".", 1)[0],
            "licenta": lic,
            "descarcare": ii["thumburl"],
            "redimensioneaza_singur": True,
        })
    return iesire


SURSE = {"unsplash": cauta_unsplash, "openverse": cauta_openverse,
         "pexels": cauta_pexels, "pixabay": cauta_pixabay, "wikimedia": cauta_commons}


def cauta(text, sursa="toate", pe_pagina=20):
    nume = list(SURSE) if sursa == "toate" else [sursa]
    pe_sursa = []
    for n in nume:
        try:
            r = SURSE[n](text, pe_pagina)
        except SystemExit:
            raise
        except Exception as e:
            print(f"sursa {n} a picat ({e}); continui cu celelalte", file=sys.stderr)
            r = []
        if r:
            pe_sursa.append(r)
    # Intercalam: cate unul din fiecare sursa, pe rand. Fara asta, sursa care raspunde
    # prima ocupa toate locurile cand scorurile sunt egale, fiindca sortarea e stabila,
    # iar celelalte surse nu se vad niciodata.
    from itertools import zip_longest
    return [r for grup in zip_longest(*pe_sursa) for r in grup if r is not None]


def scor(rezultat, vreau, nu_vreau):
    t = (rezultat.get("descriere") or "").lower()
    return sum(2 for c in vreau if c in t) - sum(3 for c in nu_vreau if c in t)


def credit(r, cale, rol=None):
    return {"rol": rol, "fisier": cale, "sursa": r["sursa"], "id": r["id"],
            "autor": r["autor"], "profil": r["profil"],
            "foto": r["pagina"], "licenta": r["licenta"],
            "descriere": r["descriere"]}


def ia(text, vreau, nu_vreau, cale, latime, ocolite, sursa="toate"):
    gasite = [r for r in cauta(text, sursa) if r["id"] not in ocolite]
    if not gasite:
        return None
    gasite.sort(key=lambda r: scor(r, vreau, nu_vreau), reverse=True)
    r = gasite[0]
    os.makedirs(os.path.dirname(os.path.abspath(cale)), exist_ok=True)
    if r["redimensioneaza_singur"]:
        # Openverse da fisierul asa cum e; il aducem la latimea ceruta cu magick
        curl(r["descarcare"], cale, agent=AGENT)
        subprocess.run(["magick", cale, "-auto-orient", "-resize", f"{latime}x{latime*3}>",
                        "-quality", "85", cale],
                       capture_output=True)
    else:
        curl(r["descarcare"] + f"&w={latime}&q=85&fm=jpg", cale)
    ocolite.add(r["id"])
    return r


def main():
    p = argparse.ArgumentParser(description="Cauta si descarca fotografii din cinci surse gratuite deodata.")
    p.add_argument("cautare", nargs="?", help="ce cauti, in engleza")
    p.add_argument("--iesire", help="fisierul de scris, sau prefixul cand ceri candidati")
    p.add_argument("--vreau", default="", help="cuvinte care cresc scorul, separate prin virgula")
    p.add_argument("--nu-vreau", default="", help="cuvinte care scad scorul")
    p.add_argument("--candidati", type=int, default=1,
                   help="cate variante descarci, ca sa alegi cu ochii")
    p.add_argument("--latime", type=int, default=1600, help="latimea descarcata")
    p.add_argument("--plan", help="fisier JSON cu mai multe cautari deodata")
    p.add_argument("--dosar", default=".", help="unde scrie fisierele planului")
    p.add_argument("--sursa", choices=["toate"] + list(SURSE), default="toate",
                   help="unde cauta; implicit in toate si castiga cea mai potrivita. "
                        "pexels si pixabay cer cate o cheie in Keychain si se sar daca lipseste")
    a = p.parse_args()

    vreau = [c.strip().lower() for c in a.vreau.split(",") if c.strip()]
    nu_vreau = [c.strip().lower() for c in a.nu_vreau.split(",") if c.strip()]
    ocolite, credite = set(), []

    if a.plan:
        # planul e o lista de {"nume", "cautare", "vreau", "nu_vreau", "rol"}
        for cerere in json.load(open(a.plan, encoding="utf-8")):
            nume = cerere["nume"]
            if not os.path.splitext(nume)[1]:
                nume += ".jpg"
            cale = os.path.join(a.dosar, nume)
            r = ia(cerere["cautare"],
                   [c.lower() for c in cerere.get("vreau", [])],
                   [c.lower() for c in cerere.get("nu_vreau", [])],
                   cale, a.latime, ocolite, a.sursa)
            if r is None:
                print(f"NIMIC pentru „{cerere['cautare']}”", file=sys.stderr)
                continue
            credite.append(credit(r, cale, cerere.get("rol")))
    else:
        if not a.cautare or not a.iesire:
            sys.exit("fara --plan, trebuie sa dai si cautarea, si --iesire")
        for i in range(a.candidati):
            cale = a.iesire if a.candidati == 1 else f"{a.iesire}-{i + 1}.jpg"
            r = ia(a.cautare, vreau, nu_vreau, cale, a.latime, ocolite, a.sursa)
            if r is None:
                break
            credite.append(credit(r, cale))

    if not credite:
        sys.exit("nu am gasit nicio fotografie potrivita in sursele cerute")
    print(json.dumps({"fotografii": credite,
                      "atentie": "creditele sunt obligatorii la publicare; o fotografie "
                                 "de stoc nu e materialul omului"},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
