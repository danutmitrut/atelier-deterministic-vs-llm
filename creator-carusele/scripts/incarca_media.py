#!/usr/bin/env python3
"""
Incarca slide-urile in stocarea Zernio si intoarce adresele publice.

Usage:
    python3 incarca_media.py slide-1.png slide-2.png ...
    python3 incarca_media.py --dosar ../campanie/livrabile/carusel
    python3 incarca_media.py --dosar carusel/ --png          # pastreaza PNG-ul

Scriptul face doar incarcarea. NU publica nimic. Publicarea se face pe urma,
prin unealta `posts_create` din MCP-ul Zernio, si numai dupa ce omul a spus da.

De ce exista scriptul: unealta `media_generate_upload_link` din MCP intoarce o
adresa pe care omul trebuie s-o deschida in browser si sa traga fisierele de
mana. API-ul Zernio are insa si calea programatica, in trei pasi:
`POST /v1/media/presign`, un `PUT` al fisierului la adresa semnata, apoi
`publicUrl` merge direct in `media_urls`.

Cheia se ia din seif (serviciul „zernio-api-key"). Nu se afiseaza, nu se scrie
nicaieri, nu exista .env.

Implicit convertim in JPEG la calitate 92: Instagram recomprima oricum, iar un
set de opt slide-uri scade de la ~20 MB la ~3 MB, deci incarcarea se vede
terminata in cateva secunde, nu in doua minute. Cu `--png` pastram originalul.

Fisierele stau in stocarea temporara Zernio si se sterg singure dupa 7 zile.
Adresa semnata de incarcare e valabila o ora.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

BASE = "https://zernio.com/api/v1"
LIMITA_INSTAGRAM = 8 * 1024 * 1024


def cheie():
    k = os.environ.get("ZERNIO_API_KEY", "")
    if k:
        return k
    r = subprocess.run(
        ["security", "find-generic-password", "-a", os.environ.get("USER", ""),
         "-s", "zernio-api-key", "-w"],
        capture_output=True, text=True,
    )
    k = r.stdout.strip()
    if not k:
        sys.exit("nu gasesc `zernio-api-key` in seif. Omul o pune cu: cheie-set zernio-api-key")
    return k


def curl(*args):
    r = subprocess.run(["curl", "-s", "--max-time", "300", *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl a esuat: {r.stderr.strip()}")
    return r.stdout


def presign(fisier, tip, marime, k):
    corp = json.dumps({"filename": os.path.basename(fisier),
                       "contentType": tip, "size": marime})
    raspuns = curl("-X", "POST", f"{BASE}/media/presign",
                   "-H", f"Authorization: Bearer {k}",
                   "-H", "Content-Type: application/json",
                   "-d", corp)
    try:
        d = json.loads(raspuns)
    except json.JSONDecodeError:
        raise RuntimeError(f"raspuns neasteptat de la presign: {raspuns[:200]}")
    if "uploadUrl" not in d:
        raise RuntimeError(f"presign fara uploadUrl: {raspuns[:200]}")
    return d


def urca(cale, adresa, tip):
    cod = curl("-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT", adresa,
               "-H", f"Content-Type: {tip}", "--data-binary", "@" + cale).strip()
    if cod != "200":
        raise RuntimeError(f"incarcarea a raspuns {cod}, nu 200")


def in_jpeg(cale, tmp):
    iesire = os.path.join(tmp, os.path.splitext(os.path.basename(cale))[0] + ".jpg")
    subprocess.run(["magick", cale, "-quality", "92", "-strip", iesire], check=True)
    return iesire


def main():
    p = argparse.ArgumentParser()
    p.add_argument("fisiere", nargs="*", help="slide-urile, in ordinea din carusel")
    p.add_argument("--dosar", help="ia din dosar doar fisierele `slide-*`, sortate natural")
    p.add_argument("--tipar", default="slide-", help="prefixul cautat in --dosar (implicit `slide-`)")
    p.add_argument("--toate", action="store_true",
                   help="in --dosar, ia orice imagine, nu doar `slide-*`")
    p.add_argument("--png", action="store_true", help="incarca PNG-ul original, fara conversie")
    p.add_argument("--json", help="scrie rezultatul si intr-un fisier")
    a = p.parse_args()

    cai = list(a.fisiere)
    if a.dosar:
        # Dosarul de livrabile tine si fundalurile langa slide-uri, iar `fundal-1.png`
        # vine inaintea lui `slide-1.png` la sortare. Fara filtru, caruselul ar pleca
        # cu opt fundaluri brute in fata. De asta luam implicit doar `slide-*`.
        toate = [f for f in os.listdir(a.dosar) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        alese = toate if a.toate else [f for f in toate if f.startswith(a.tipar)]
        if not alese:
            sys.exit(f"in {a.dosar} nu e niciun fisier `{a.tipar}*`. "
                     f"Am gasit: {', '.join(sorted(toate)[:8]) or 'nicio imagine'}. "
                     "Foloseste --tipar <prefix> sau --toate.")
        ignorate = len(toate) - len(alese)
        if ignorate:
            print(f"  ({ignorate} fisiere ignorate, nu incep cu `{a.tipar}`)", file=sys.stderr)
        # sortare naturala: slide-10 dupa slide-9, nu inaintea lui slide-2
        def cheie_sort(f):
            return [int(t) if t.isdigit() else t.lower()
                    for t in re.split(r"(\d+)", f)]
        cai += [os.path.join(a.dosar, f) for f in sorted(alese, key=cheie_sort)]
    if not cai:
        sys.exit("nu mi-ai dat niciun fisier")
    for c in cai:
        if not os.path.exists(c):
            sys.exit(f"nu gasesc {c}")
    if len(cai) > 10:
        sys.exit(f"{len(cai)} imagini. Un carusel Instagram ia cel mult 10. "
                 "Taie setul sau incarca-l pe bucati.")

    # Instagram cere acelasi raport pe tot caruselul. Daca slide-urile nu au
    # aceeasi forma, Instagram decupeaza singur si se pierde text de pe margine.
    forme = set()
    for c in cai:
        lat, inalt = subprocess.run(["magick", "identify", "-format", "%w %h", c],
                                    capture_output=True, text=True).stdout.split()
        forme.add(round(int(lat) / int(inalt), 3))
    if len(forme) > 1:
        sys.exit(f"slide-urile nu au acelasi raport ({sorted(forme)}). "
                 "Instagram ar decupa singur. Recompune-le pe aceeasi dimensiune.")

    k = cheie()
    rezultat = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, c in enumerate(cai, 1):
            sursa, tip = (c, "image/png") if a.png else (in_jpeg(c, tmp), "image/jpeg")
            if not a.png and c.lower().endswith((".jpg", ".jpeg")):
                sursa, tip = c, "image/jpeg"
            marime = os.path.getsize(sursa)
            if marime > LIMITA_INSTAGRAM:
                sys.exit(f"{c} are {marime/1048576:.1f} MB, peste limita Instagram de 8 MB")
            d = presign(sursa, tip, marime, k)
            urca(sursa, d["uploadUrl"], tip)
            rezultat.append({"slide": i, "sursa": c, "octeti": marime,
                             "adresa": d["publicUrl"]})
            print(f"  {i}. {os.path.basename(c)} -> {marime/1024:.0f} KB  urcat", file=sys.stderr)

    iesire = {
        "media_urls": ",".join(r["adresa"] for r in rezultat),
        "slide_uri": rezultat,
        "atentie": "fisierele se sterg singure din stocarea Zernio dupa 7 zile; "
                   "publica in aceeasi sesiune, nu peste o saptamana",
    }
    text = json.dumps(iesire, indent=2, ensure_ascii=False)
    if a.json:
        open(a.json, "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
