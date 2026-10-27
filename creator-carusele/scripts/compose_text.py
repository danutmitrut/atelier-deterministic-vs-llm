#!/usr/bin/env python3
"""
Pune text peste o imagine, cu ImageMagick.

Există separat de generare dintr-un motiv practic: generatoarele de imagini
scriu prost textul, iar cu diacritice românești greșesc aproape sigur. Un „ș"
iese „s", un „ț" iese „t". Textul care trebuie citit corect se pune aici, după
generare, nu se cere modelului.

Folosire:
  python3 compose_text.py <sursa> <output> --text "Textul tău" [optiuni]

Opțiuni:
  --position top|center|bottom   unde stă textul, implicit bottom
  --font NUME_SAU_CALE           implicit caută un font de sistem cu diacritice
  --size N                       mărimea literei în puncte, implicit 10% din înălțime
  --color CULOARE                implicit white
  --band                         bandă închisă sub text, pentru lizibilitate
  --band-opacity 0..1            implicit 0.55
  --margin N                     distanța față de margine, implicit 5% din înălțime
  --width-ratio 0..1             cât din lățime ocupă textul, implicit 0.8

Scriptul scrie doar pe disc. Nu trimite imaginea nicăieri: publicarea e a Publisher-ului,
după aprobarea omului.
"""

import argparse
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Fonturi de sistem care randează corect ș și ț cu virgulă, nu cu sedilă.
# Ordinea contează: primul găsit câștigă.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def log(msg):
    print(msg, file=sys.stderr)


def die(msg, hint=None):
    log(f"EROARE: {msg}")
    if hint:
        log(f"   {hint}")
    sys.exit(1)


def find_magick():
    """ImageMagick 7 se cheamă magick, versiunea 6 se cheamă convert."""
    for binary in ("magick", "convert"):
        try:
            subprocess.run([binary, "-version"], capture_output=True, timeout=10, check=True)
            return binary
        except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            continue
    die(
        "ImageMagick nu e instalat.",
        "Pe Mac: brew install imagemagick. Pe Windows: winget install ImageMagick.ImageMagick",
    )


def resolve_font(requested):
    """Acceptă o cale către fișierul de font sau un nume cunoscut de ImageMagick."""
    if requested:
        if os.path.exists(requested):
            return requested
        # Nu e cale, deci lăsăm ImageMagick să caute numele în lista lui.
        return requested

    for candidate in FONT_CANDIDATES:
        if os.path.exists(candidate):
            return candidate

    die(
        "Nu găsesc niciun font de sistem pentru text.",
        "Dă-mi unul explicit cu --font, de exemplu --font /calea/catre/font.ttf",
    )


def image_dimensions(magick, path):
    out = subprocess.run(
        [magick, "identify", "-format", "%w %h", path] if magick == "magick"
        else ["identify", "-format", "%w %h", path],
        capture_output=True, text=True, timeout=30,
    )
    if out.returncode != 0:
        die(f"Nu pot citi imaginea {path}: {out.stderr.strip()}")
    width, height = out.stdout.split()
    return int(width), int(height)


def run(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        die(f"ImageMagick a eșuat: {out.stderr.strip()[:400]}")
    return out


def compose(args):
    magick = find_magick()
    if not os.path.exists(args.source):
        die(f"Imaginea sursă nu există: {args.source}")

    width, height = image_dimensions(magick, args.source)
    font = resolve_font(args.font)
    point_size = args.size or max(16, int(height * 0.10))
    margin = args.margin if args.margin is not None else int(height * 0.05)
    text_width = int(width * args.width_ratio)

    log(f"-> Compun text peste {args.source} ({width}x{height})")
    log(f"   font: {font}, mărime: {point_size}px")

    # Padding vertical obligatoriu, nu decorativ: ImageMagick calculează înălțimea
    # rândului fără să lase loc virgulei de sub ș, ț, Ș și Ț, iar fără spațiul ăsta
    # diacriticele românești ies tăiate la bază.
    padding_y = max(int(point_size * 0.3), 8)
    padding_x = int(point_size * 0.6) if args.band else padding_y

    with tempfile.TemporaryDirectory() as tmp:
        layer = os.path.join(tmp, "text.png")

        # caption: face wrap automat la lățimea dată, spre deosebire de annotate.
        run([
            magick, "-background", "none", "-fill", args.color,
            "-font", font, "-pointsize", str(point_size),
            "-gravity", "center",
            "-size", f"{text_width}x",
            f"caption:{args.text}",
            "-bordercolor", "none", "-border", f"{padding_x}x{padding_y}",
            layer,
        ])

        if args.band:
            # Banda se desenează ca dreptunghi separat, sub tot layerul. Varianta
            # cu -border colorat dădea două nuanțe, fiindcă bordura semitransparentă
            # se aduna peste fundalul semitransparent al textului.
            layer_width, layer_height = image_dimensions(magick, layer)
            banded = os.path.join(tmp, "text-band.png")
            run([
                magick, "-size", f"{layer_width}x{layer_height}",
                f"xc:rgba(0,0,0,{args.band_opacity})",
                layer, "-composite", banded,
            ])
            layer = banded

        gravity = {"top": "north", "center": "center", "bottom": "south"}[args.position]
        offset = f"+0+{margin}" if args.position != "center" else "+0+0"

        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        run([
            magick, args.source, layer,
            "-gravity", gravity, "-geometry", offset,
            "-composite", args.output,
        ])

    size_kb = os.path.getsize(args.output) // 1024
    log(f"   gata: {args.output} ({size_kb} KB)")
    return {"output_path": args.output, "size_bytes": os.path.getsize(args.output), "font": font}


def main():
    parser = argparse.ArgumentParser(description="Pune text peste o imagine, cu diacritice corecte.")
    parser.add_argument("source", help="Imaginea peste care scrii")
    parser.add_argument("output", help="Unde salvezi rezultatul")
    parser.add_argument("--text", required=True, help="Textul de pus")
    parser.add_argument("--position", default="bottom", choices=["top", "center", "bottom"])
    parser.add_argument("--font", default=None, help="Cale către font sau nume cunoscut ImageMagick")
    parser.add_argument("--size", type=int, default=None, help="Mărimea literei în puncte")
    parser.add_argument("--color", default="white")
    parser.add_argument("--band", action="store_true", help="Bandă închisă sub text")
    parser.add_argument("--band-opacity", type=float, default=0.55)
    parser.add_argument("--margin", type=int, default=None)
    parser.add_argument("--width-ratio", type=float, default=0.8)
    args = parser.parse_args()

    result = compose(args)

    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
