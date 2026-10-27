#!/usr/bin/env python3
"""Pregateste o captura de ecran ca sa poata intra pe un slide de carusel.

Face patru lucruri, in ordinea asta, si toate coordonatele se dau raportat la
imaginea ORIGINALA, nu la ce a iesit dupa pasul dinainte:

  1. acopera zonele cu date pe care nu ai voie sa le publici („--zona")
  2. marcheaza si adnoteaza dovada, ca sa se vada ce trebuie citit („--marcheaza", „--nota")
  3. decupeaza, ca sa se citeasca pe telefon fara zoom („--decupaj")
  4. pune rama rotunjita si umbra, ca sa stea pe slide ca un obiect („--rama")

Acoperirea e bara plina, opaca. Nu exista optiune de blur si nici de pixelare:
pe text, amandoua se pot inversa si nu sunt redactare, sunt doar aparenta ei.

Coordonatele se dau „x,y,latime,inaltime", fie in pixeli, fie in procente din
latimea si inaltimea imaginii, cu procentele scrise ca „12%".

Exemple:
  # acopera numele platitorului si numele firmei, pune rama
  python3 scripts/pregateste_captura.py transfer.png transfer-ok.png \\
      --zona "56,398,420,34:redactat" --rama

  # marcheaza suma, adnoteaza, decupeaza pe jumatatea de sus
  python3 scripts/pregateste_captura.py transfer.png dovada.png \\
      --marcheaza "50,280,300,60" --nota "56,240:suma incasata" \\
      --decupaj "0,0,100%,60%" --latime 900 --rama
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

AICI = os.path.dirname(os.path.abspath(__file__))
RESURSE = os.path.join(AICI, "..", "resurse")
FONT_MONO = os.path.join(RESURSE, "fonturi", "JetBrainsMono-Medium.ttf")
FONT_BOLD = os.path.join(RESURSE, "fonturi", "InstrumentSans-Bold.ttf")


def magick(*args):
    rezultat = subprocess.run(["magick", *map(str, args)], capture_output=True, text=True)
    if rezultat.returncode != 0:
        sys.exit("magick a esuat: " + (rezultat.stderr.strip() or " ".join(map(str, args))))
    return rezultat.stdout.strip()


def masura(cale):
    return [int(v) for v in magick("identify", "-format", "%w %h", cale).split()]


def numar(valoare, referinta, unde):
    """„120" sau „12%" devin pixeli. Procentul se raporteaza la latura data."""
    valoare = valoare.strip()
    try:
        if valoare.endswith("%"):
            return int(round(float(valoare[:-1]) / 100.0 * referinta))
        return int(round(float(valoare)))
    except ValueError:
        sys.exit(f"valoare neinteleasa in {unde}: „{valoare}”")


def dreptunghi(spec, lat, inalt, unde):
    """„x,y,w,h" sau „x,y,w,h:eticheta" devine (x, y, w, h, eticheta)."""
    eticheta = None
    if ":" in spec:
        spec, eticheta = spec.split(":", 1)
    parti = spec.split(",")
    if len(parti) != 4:
        sys.exit(f"{unde} cere patru valori „x,y,latime,inaltime”, am primit „{spec}”")
    x = numar(parti[0], lat, unde)
    y = numar(parti[1], inalt, unde)
    w = numar(parti[2], lat, unde)
    h = numar(parti[3], inalt, unde)
    if w <= 0 or h <= 0:
        sys.exit(f"{unde} are latime sau inaltime zero: „{spec}”")
    return x, y, w, h, (eticheta.strip() if eticheta else None)


def punct(spec, lat, inalt, unde):
    """„x,y:text" devine (x, y, text)."""
    if ":" not in spec:
        sys.exit(f"{unde} cere „x,y:text”, am primit „{spec}”")
    coord, text = spec.split(":", 1)
    parti = coord.split(",")
    if len(parti) != 2:
        sys.exit(f"{unde} cere „x,y:text”, am primit „{spec}”")
    return numar(parti[0], lat, unde), numar(parti[1], inalt, unde), text.strip()


def main():
    p = argparse.ArgumentParser(
        description="Redacteaza, adnoteaza si incadreaza o captura pentru slide.")
    p.add_argument("intrare", help="captura originala")
    p.add_argument("iesire", help="fisierul de scris")
    p.add_argument("--zona", action="append", default=[], metavar="X,Y,W,H[:eticheta]",
                   help="acopera zona cu o bara plina; se poate repeta")
    p.add_argument("--marcheaza", action="append", default=[], metavar="X,Y,W,H",
                   help="contur colorat in jurul dovezii; se poate repeta")
    p.add_argument("--nota", action="append", default=[], metavar="X,Y:text",
                   help="eticheta scrisa peste captura; se poate repeta")
    p.add_argument("--decupaj", metavar="X,Y,W,H", help="decupeaza zona asta")
    p.add_argument("--latime", type=int, help="latimea finala, in pixeli")
    p.add_argument("--rama", action="store_true", help="colturi rotunjite si umbra")
    p.add_argument("--culoare-bara", default="#14181D", help="culoarea barelor de acoperire")
    p.add_argument("--culoare-accent", default="#E4002B", help="culoarea conturului si a notelor")
    a = p.parse_args()

    if not os.path.exists(a.intrare):
        sys.exit(f"nu gasesc captura: {a.intrare}")
    if not (a.zona or a.marcheaza or a.nota or a.decupaj or a.latime or a.rama):
        sys.exit("nu ai cerut nicio operatie: pune macar --zona, --decupaj sau --rama")

    tmp = tempfile.mkdtemp(prefix="captura-")
    lucru = os.path.join(tmp, "lucru.png")
    magick(a.intrare, "-alpha", "on", lucru)
    lat, inalt = masura(lucru)

    acoperite = []
    for spec in a.zona:
        x, y, w, h, eticheta = dreptunghi(spec, lat, inalt, "--zona")
        magick(lucru, "-fill", a.culoare_bara,
               "-draw", f"rectangle {x},{y} {x + w},{y + h}", lucru)
        if eticheta:
            # eticheta sta in bara, cu corp cat incape, ca sa se vada ca e
            # redactare intentionata, nu o pata aparuta din greseala
            pad_x = max(4, int(w * 0.03))
            util = max(1, w - 2 * pad_x)
            corp = max(11, min(int(h * 0.52),
                               int(util / (0.62 * max(len(eticheta), 1)))))
            magick(lucru, "-font", FONT_MONO, "-pointsize", corp, "-fill", "#FFFFFF",
                   "-gravity", "northwest",
                   "-annotate", f"+{x + pad_x}+{y + (h - corp) // 2}",
                   eticheta, lucru)
        acoperite.append({"x": x, "y": y, "latime": w, "inaltime": h, "eticheta": eticheta})

    for spec in a.marcheaza:
        x, y, w, h, _ = dreptunghi(spec, lat, inalt, "--marcheaza")
        gros = max(2, int(min(lat, inalt) * 0.005))
        magick(lucru, "-fill", "none", "-stroke", a.culoare_accent, "-strokewidth", gros,
               "-draw", f"roundrectangle {x},{y} {x + w},{y + h} 6,6", lucru)

    for spec in a.nota:
        x, y, text = punct(spec, lat, inalt, "--nota")
        corp = max(14, int(min(lat, inalt) * 0.028))
        pad = int(corp * 0.5)
        w = int(len(text) * corp * 0.62) + pad * 2
        h = corp + pad * 2
        magick(lucru, "-fill", a.culoare_accent,
               "-draw", f"roundrectangle {x},{y} {x + w},{y + h} 5,5", lucru)
        magick(lucru, "-font", FONT_BOLD, "-pointsize", corp, "-fill", "#FFFFFF",
               "-gravity", "northwest", "-annotate", f"+{x + pad}+{y + pad}", text, lucru)

    if a.decupaj:
        x, y, w, h, _ = dreptunghi(a.decupaj, lat, inalt, "--decupaj")
        if x + w > lat or y + h > inalt:
            sys.exit(f"--decupaj iese din imagine: captura are {lat}x{inalt}")
        magick(lucru, "-crop", f"{w}x{h}+{x}+{y}", "+repage", lucru)
        lat, inalt = masura(lucru)

    if a.latime and a.latime != lat:
        magick(lucru, "-resize", f"{a.latime}x", lucru)
        lat, inalt = masura(lucru)

    if a.rama:
        raza = max(8, int(min(lat, inalt) * 0.03))
        masca = os.path.join(tmp, "masca.png")
        magick("-size", f"{lat}x{inalt}", "xc:black", "-fill", "white",
               "-draw", f"roundrectangle 0,0 {lat - 1},{inalt - 1} {raza},{raza}",
               "-alpha", "off", masca)
        magick(lucru, masca, "-alpha", "off", "-compose", "copy_opacity", "-composite", lucru)
        magick(lucru, "(", "+clone", "-background", "black",
               "-shadow", "55x14+0+8", ")", "+swap", "-background", "none",
               "-layers", "merge", "+repage", lucru)

    # „-strip" scoate metadatele originale: o captura redactata nu are ce sa
    # mai care din fisierul de la care a plecat
    magick(lucru, "-strip", a.iesire)
    lat_f, inalt_f = masura(a.iesire)
    print(json.dumps({"output_path": os.path.abspath(a.iesire),
                      "dimensiune": f"{lat_f}x{inalt_f}",
                      "zone_acoperite": acoperite,
                      "size_bytes": os.path.getsize(a.iesire)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
