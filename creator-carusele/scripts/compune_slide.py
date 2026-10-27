#!/usr/bin/env python3
"""Compune un slide de carusel peste un fundal, in formula vizuala „aurora".

Blocuri disponibile: eticheta, titlu pe doua randuri (al doilea cu gradient), text
secundar, lista de puncte, cifra mare de fundal, poze proprii asezate ca un colaj,
numarul slide-ului si logo-ul. Din combinatia lor ies layout-urile diferite cerute
pentru carusel. Textul se rupe singur pe randuri si se micsoreaza daca nu incape.

Totul se face local cu ImageMagick, fara cost.

Exemple:
  # copertă
  python3 scripts/compune_slide.py fundal.png slide-1.png \
      --eticheta "// cum vinzi" --titlu1 "Cum vinzi de" --titlu2 "40.000 de euro" --numar "01 / 12"

  # pas numerotat, cu listă
  python3 scripts/compune_slide.py fundal.png slide-4.png --numar-mare 2 \
      --titlu1 "Separă ce poți controla" --lista "Reach-ul|Algoritmul|Viteza de creștere"

  # dovadă, cu poze proprii
  python3 scripts/compune_slide.py fundal.png slide-9.png --titlu1 "Rezultatele" \
      --text "În primele 6 luni" --foto captura1.png,captura2.png,captura3.png
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stiluri import STILURI  # noqa: E402  catalogul de stiluri, sursa culorilor

AICI = os.path.dirname(os.path.abspath(__file__))
RESURSE = os.path.join(AICI, "..", "resurse")
FONT_TITLU = os.path.join(RESURSE, "fonturi", "InstrumentSans-Bold.ttf")
FONT_TEXT = os.path.join(RESURSE, "fonturi", "InstrumentSans-Regular.ttf")
FONT_MONO = os.path.join(RESURSE, "fonturi", "JetBrainsMono-Medium.ttf")
LOGO = os.path.join(RESURSE, "logo.png")

# Culorile nu mai stau aici: vin din stilul ales, din `stiluri.py`.


def magick(*args):
    rezultat = subprocess.run(["magick", *args], capture_output=True, text=True)
    if rezultat.returncode != 0:
        sys.exit(f"eroare ImageMagick: {rezultat.stderr.strip()}")
    return rezultat.stdout


# cat din inaltimea slide-ului tine textul la layout-ul `dovada`. Restul e al capturii.
ZONA_TEXT_DOVADA = 0.38


def inaltime(cale):
    return int(magick("identify", "-format", "%h", cale))


def bloc_text(out, text, font, marime, latime, culoare=None, gradient=None,
              aliniere=None):
    """Randeaza text cu rupere pe randuri, pe fundal transparent, taiat la inaltimea reala.

    `aliniere` se da doar cand textul trebuie centrat: pus si cand nu trebuie, `-gravity`
    schimba subtil randarea si strica potrivirea cu slide-urile facute inainte.
    """
    masca = out + ".masca.png"
    grav = ["-gravity", aliniere] if aliniere else []
    magick("-background", "black", "-fill", "white", "-font", font,
           "-pointsize", str(marime), "-size", f"{latime}x",
           "-interline-spacing", str(int(marime * -0.08)),
           *grav, f"caption:{text}", masca)
    h = inaltime(masca)
    if gradient:
        # gradientul se intinde doar cat textul, ca sa ajunga la a doua culoare si la titluri scurte
        cutie = magick(masca, "-format", "%@", "info:")  # ex: 610x120+2+18
        lat_reala = int(cutie.split("x")[0]) + int(cutie.split("+")[1])
        umplere = ["-size", f"{max(lat_reala, 1)}x{h}", "-define", "gradient:direction=east",
                   f"gradient:{gradient[0]}-{gradient[1]}", "-background", gradient[1],
                   "-extent", f"{latime}x{h}"]
    else:
        umplere = ["-size", f"{latime}x{h}", f"xc:{culoare}"]
    # PNG32 obligatoriu: altfel PNG-ul se salveaza in tonuri de gri si culoarea se pierde
    magick(*umplere, masca, "-alpha", "off", "-compose", "copy_opacity", "-composite", "PNG32:" + out)
    os.remove(masca)
    return h


def main():
    p = argparse.ArgumentParser()
    p.add_argument("fundal")
    p.add_argument("output")
    p.add_argument("--titlu1", required=True)
    p.add_argument("--titlu2", default="")
    p.add_argument("--eticheta", default="")
    p.add_argument("--text", default="")
    p.add_argument("--lista", default="", help="puncte scurte, separate prin |")
    p.add_argument("--numar-mare", dest="numar_mare", default="",
                   help="cifra sau numarul mare din fundal, ex: 2 sau 40.000")
    p.add_argument("--foto", default="",
                   help="una pana la trei imagini proprii, separate prin virgula")
    p.add_argument("--numar", default="", help="numarul slide-ului, ex: 03 / 12")
    p.add_argument("--dovada", metavar="CAPTURA",
                   help="o captura pregatita cu pregateste_captura.py, asezata dreapta "
                        "sub text, nedecupata si neinclinata; cere --layout dovada")
    p.add_argument("--fara-scrim", action="store_true",
                   help="nu pune voalul automat sub text pe fotografii")
    p.add_argument("--logo", action="store_true", help="pune logo-ul mic, dreapta jos")
    p.add_argument("--format", default="4:5", choices=["4:5", "1:1"],
                   help="formatul slide-ului; 4:5 e cel folosit in carusele")
    p.add_argument("--layout", default="auto",
                   choices=["auto", "foto-sus", "foto-jos", "banda", "panou", "citat", "dovada"],
                   help="compozitia slide-ului; alterneaza-le, doua slide-uri vecine "
                        "nu au voie sa aiba acelasi layout")
    p.add_argument("--stil", default="aurora", choices=list(STILURI),
                   help="stilul vizual; da culorile textului, vezi scripts/stiluri.py")
    p.add_argument("--brand", metavar="JSON",
                   help="fisa vizuala a brandului, peste stil: paleta, fonturi, logo. "
                        "Cand se bate cu stilul, castiga brandul")
    a = p.parse_args()

    stil = STILURI[a.stil]
    if a.brand:
        # catalogul ramane independent de brand; fisa brandului doar suprascrie cheile
        # pe care le numeste (paleta_panou, culoare_panou, tipografie, logo_fisier...)
        with open(a.brand, encoding="utf-8") as fb:
            stil = {**stil, **json.load(fb)}
    # tipografia stilului: ce font, ce marime si daca titlul e cu majuscule.
    # Stilurile care nu o definesc raman pe formula initiala, cu Instrument Sans.
    tipo = stil.get("tipografie", {})

    # Layout-ul da compozitia, nu culorile. „auto" ia asezarea implicita a stilului.
    layout = a.layout
    if layout == "auto":
        layout = "foto-jos" if tipo.get("pozitie") == "jos" else "foto-sus"
    PE_PANOU = layout in ("banda", "panou", "dovada")

    # pe suprafata plata, deschisa, textul nu poate ramane alb: stilul da o a doua paleta
    pal = stil.get("paleta_panou", stil["paleta"]) if PE_PANOU else stil["paleta"]
    CULOARE_PANOU = stil.get("culoare_panou", "#EFE4D4")

    def font_stil(cheie, implicit):
        nume = tipo.get(cheie, {}).get("font")
        return os.path.join(RESURSE, "fonturi", nume) if nume else implicit

    def scris(cheie, text):
        return text.upper() if tipo.get(cheie, {}).get("caps") else text

    def scara(cheie):
        return tipo.get(cheie, {}).get("scara", 1.0)

    C_TITLU, C_TEXT = pal["titlu1"], pal["text"]
    C_ETICHETA, C_NUMAR = pal["eticheta"], pal["numar"]
    t2 = pal["titlu2"]
    GRADIENT_TITLU = t2 if isinstance(t2, tuple) else None
    C_TITLU2 = None if GRADIENT_TITLU else t2
    # linia de sub titlu: gradient la stilurile cu gradient, plina la celelalte
    LINIE = GRADIENT_TITLU or (t2, t2)
    UMBRA_ALBA = pal["umbra"] == "alb"
    FARA_UMBRA = pal["umbra"] == "fara"
    NUMAR_SUS = pal.get("numar_pozitie") == "sus"
    # numarul in dreapta jos se bate cap in cap cu logoul, care sta tot acolo.
    # Pe slide-ul cu logo numarul trece in stanga.
    NUMAR_DREAPTA = pal.get("numar_pozitie") == "jos-dreapta" and not a.logo

    tmp = tempfile.mkdtemp(prefix="slide-")
    # la `panou` nu exista fundal: se da „-" in locul caii si latimea e cea standard
    fara_fundal = a.fundal == "-"
    if fara_fundal and layout not in ("panou", "dovada"):
        sys.exit('fara fundal („-") se poate doar cu --layout panou sau dovada')
    if a.dovada and layout != "dovada":
        sys.exit("--dovada merge doar cu --layout dovada")
    if layout == "dovada" and not a.dovada:
        sys.exit("--layout dovada cere --dovada <captura>")
    if a.dovada and not os.path.exists(a.dovada):
        sys.exit(f"nu gasesc captura: {a.dovada}")
    lat = 1024 if fara_fundal else int(magick("identify", "-format", "%w", a.fundal))
    s = lat / 1024  # toate masurile sunt gandite pe latimea de 1024 px
    inalt = lat if a.format == "1:1" else int(lat * 5 / 4)
    marg = int(84 * s)
    lat_text = lat - 2 * marg

    # fundalul adus la formatul cerut, taiat din centru.
    # „panou" nu foloseste deloc fotografia: e o suprafata plata, deci un slide fara cost
    # de generare. „banda" taie fotografia sus si umple restul cu suprafata plata.
    baza = os.path.join(tmp, "baza.png")
    # cat din cadru ia fotografia la `banda`; un brand cu text mai lung o poate scadea
    inalt_foto = int(inalt * stil.get("banda_foto", 0.58))
    if layout in ("panou", "dovada"):
        magick("-size", f"{lat}x{inalt}", f"xc:{CULOARE_PANOU}", baza)
    elif layout == "banda":
        magick(a.fundal, "-resize", f"{lat}x{inalt_foto}^", "-gravity", "center",
               "-extent", f"{lat}x{inalt_foto}", "-background", CULOARE_PANOU,
               "-gravity", "north", "-extent", f"{lat}x{inalt}", baza)
    else:
        magick(a.fundal, "-resize", f"{lat}x{inalt}^", "-gravity", "center",
               "-extent", f"{lat}x{inalt}", baza)
        if layout == "citat":
            # citatul cere liniste sub el: fotografia se intuneca uniform
            magick(baza, "-fill", "black", "-colorize", "38%", baza)

    fotografii = [f.strip() for f in a.foto.split(",") if f.strip()]

    # cifra mare de fundal, discreta, in dreapta sus
    if a.numar_mare:
        c = os.path.join(tmp, "cifra.png")
        # cifrele lungi („40.000") se rup pe randuri si ies din cadru daca nu le micsorezi
        marime_cifra = int(420 * s * min(1.0, 2.4 / max(1, len(a.numar_mare))))
        bloc_text(c, a.numar_mare, font_stil("titlu1", FONT_TITLU), marime_cifra, lat,
                  culoare=C_TITLU)
        magick(c, "-trim", "+repage", "-channel", "A", "-evaluate", "multiply", "0.12",
               "+channel", "PNG32:" + c)
        lat_cifra = int(magick("identify", "-format", "%w", c))
        if lat_cifra > lat * 0.85:
            magick(c, "-resize", f"{int(lat * 0.85)}x", "PNG32:" + c)
        magick(baza, c, "-gravity", "northeast", "-geometry", f"+{int(30 * s)}+{int(60 * s)}",
               "-compose", "over", "-composite", baza)

    # zona de text: de sus pana deasupra numarului si a logo-ului.
    # cand slide-ul are poze, textul sta in treimea de sus.
    y0 = marg
    if layout == "banda":
        # textul traieste in banda de jos, sub fotografie
        y0 = inalt_foto + int(52 * s)
        disponibil = inalt - y0 - int(130 * s)
    elif layout == "dovada":
        # textul sta sus, captura dedesubt. Zona de text e fixa, ca dovada sa aiba
        # intotdeauna acelasi loc, indiferent cat de scurt e titlul
        disponibil = int(inalt * ZONA_TEXT_DOVADA) - marg
    elif fotografii:
        disponibil = int(inalt * 0.40) - marg
    else:
        disponibil = inalt - marg - int(160 * s)
    # cat ocupa textul pe un slide care arata bine. Peste prag slide-ul iese incarcat:
    # il producem oricum, dar cu semnalare, ca sa nu cada o campanie dintr-un rand in plus.
    prag_confortabil = int(disponibil * 0.78)

    # la citat textul se centreaza, la restul ramane aliniat la stanga
    ALIN = "north" if layout == "citat" else None
    # banda de jos e o caseta, nu o coperta: titlul e proiectat mai mic acolo, nu
    # micsorat de bucla de incadrare, ca sa nu iasa avertisment la fiecare slide
    F_LAYOUT = {"banda": 0.80, "dovada": 0.68}.get(layout, 1.0)
    if layout == "banda" and tipo.get("linie", True):
        # stilurile care trag o linie de accent sub titlu mai pierd un rand din banda,
        # care e oricum strimta. Titlul se proiecteaza mai mic, nu se micsoreaza la final.
        F_LAYOUT *= 0.88
    if layout == "dovada" and a.eticheta:
        # zona de text la `dovada` e fixa, ca dovada sa cada mereu in acelasi loc.
        # Eticheta mananca un rand din ea, deci titlul se proiecteaza mai mic de la
        # inceput, nu micsorat de urgenta la final.
        F_LAYOUT *= 0.85

    def construieste(f):
        blocuri = []  # (cale, spatiu_dupa)
        if a.eticheta:
            c = os.path.join(tmp, "eticheta.png")
            bloc_text(c, a.eticheta.upper(), FONT_MONO, int(32 * s), lat_text,
                      culoare=C_ETICHETA, aliniere=ALIN)
            blocuri.append((c, int(22 * s)))
        c = os.path.join(tmp, "titlu1.png")
        bloc_text(c, scris("titlu1", a.titlu1), font_stil("titlu1", FONT_TITLU),
                  int(104 * s * f * F_LAYOUT * scara("titlu1")), lat_text, culoare=C_TITLU,
                  aliniere=ALIN)
        blocuri.append((c, int(4 * s) if a.titlu2 else int(40 * s)))
        if a.titlu2:
            c = os.path.join(tmp, "titlu2.png")
            bloc_text(c, scris("titlu2", a.titlu2), font_stil("titlu2", FONT_TITLU),
                      int(104 * s * f * F_LAYOUT * scara("titlu2")), lat_text,
                      culoare=C_TITLU2, gradient=GRADIENT_TITLU, aliniere=ALIN)
            blocuri.append((c, int(34 * s)))
        if (a.text or a.lista) and tipo.get("linie", True) and layout != "citat":
            c = os.path.join(tmp, "linie.png")
            magick("-size", f"{int(200 * s)}x{max(4, int(6 * s))}", "-define",
                   "gradient:direction=east",
                   f"gradient:{LINIE[0]}-{LINIE[1]}", "PNG32:" + c)
            blocuri.append((c, int(28 * s)))
        if a.text:
            c = os.path.join(tmp, "text.png")
            bloc_text(c, scris("text", a.text), font_stil("text", FONT_TEXT),
                      int(38 * s * max(f, 0.85) * F_LAYOUT * scara("text")), lat_text,
                      culoare=C_TEXT, aliniere=ALIN)
            blocuri.append((c, int(20 * s) if a.lista else 0))
        if a.lista:
            # punctele urmeaza tipografia stilului, exact ca `--text`: aceleasi
            # majuscule, acelasi font, aceeasi scara. Altfel, pe un stil cu
            # `caps`, lista iese cu litere mici langa un carusel scris integral
            # cu majuscule, si se vede ca inconsecventa.
            for i, punct in enumerate(x.strip() for x in a.lista.split("|") if x.strip()):
                c = os.path.join(tmp, f"punct-{i}.png")
                bloc_text(c, "—  " + scris("text", punct), font_stil("text", FONT_TEXT),
                          int(40 * s * max(f, 0.85) * F_LAYOUT * scara("text")),
                          lat_text, culoare=C_TITLU)
                blocuri.append((c, int(16 * s)))
        return blocuri, sum(inaltime(c) + d for c, d in blocuri)

    # titlul se micsoreaza pana cand totul incape confortabil. Daca nici la jumatate
    # nu incape, mai avem zona intreaga, dar slide-ul pleaca cu semnalare.
    f = 1.0
    blocuri, total = construieste(f)
    while total > prag_confortabil and f > 0.5:
        f -= 0.07
        blocuri, total = construieste(f)
    if total > disponibil:
        sys.exit("textul nu incape pe slide nici micsorat: scurteaza-l sau scoate poze")
    # doua semnale de text prea lung: titlul a trebuit micsorat simtitor, sau blocul
    # depaseste pragul confortabil. Slide-ul pleaca oricum, dar semnalarea intra in JSON
    # si agentul o duce mai departe Orchestratorului.
    avertisment = None
    if f < 0.86 or total > prag_confortabil:
        avertisment = (
            f"titlu micsorat la {int(f * 100)}%, textul ocupa {int(total / disponibil * 100)}% "
            "din zona slide-ului: scurteaza titlul sau muta o parte in caption"
        )
        print("ATENTIE: " + avertisment, file=sys.stderr)

    # textul sta in treimea de sus, nu centrat: promptul de fundal cere zona curata sus
    # („large clean empty area in the upper half"), iar centrarea il aseza exact peste
    # obiectul din mijlocul imaginii. Nu lipit de margine, ca sa respire.
    # Fiecare layout isi aseaza altfel blocul pe verticala. De aici vine, in mare parte,
    # diferenta dintre doua slide-uri vecine.
    liber = max(0, disponibil - total)
    if layout == "foto-jos" and not fotografii:
        y = y0 + liber            # la baza cadrului, ca pe o coperta de revista
    elif layout == "dovada":
        y = y0                    # lipit de sus, captura are nevoie de tot restul
    elif layout in ("banda", "panou", "citat"):
        y = y0 + liber // 2       # centrat in suprafata lui
    else:
        y = y0 + int(liber * 0.28)
    straturi = os.path.join(tmp, "text-strat.png")
    magick("-size", f"{lat}x{inalt}", "xc:none", "PNG32:" + straturi)
    y_text_sus = y
    for c, dupa in blocuri:
        magick(straturi, c, "-geometry", f"+{marg}+{y}", "-compose", "over", "-composite",
               "PNG32:" + straturi)
        y += inaltime(c) + dupa
    y_text_jos = y

    # Plasa pentru fotografiile primite de la om. Pe fundalurile generate tonalitatea o
    # cere promptul, deci textul cade mereu pe ceva potrivit. Pe o fotografie reala nu
    # controlezi nimic: un perete alb sub text alb inseamna slide ilizibil. Masuram zona
    # in care chiar sta textul si, daca e prea aproape de culoarea lui, punem un voal in
    # degrade dinspre marginea de langa text. Pragurile sunt alese ca sa nu se atinga de
    # fundalurile generate, care stau la 0,28-0,36.
    scrim = None
    if not PE_PANOU and layout != "citat" and not fara_fundal and not a.fara_scrim:
        sus = max(0, y_text_sus - int(24 * s))
        jos = min(inalt, y_text_jos + int(24 * s))
        if jos - sus > 40:
            # masuram pe benzi, nu pe tot blocul: un titlu asezat pe ceva inchis
            # trage media in jos si ascunde randul de dedesubt, care sta pe perete alb.
            # Conteaza banda cea mai defavorabila, nu media lor.
            n_benzi = 4
            h_banda = max(1, (jos - sus) // n_benzi)
            medii = [float(magick(baza, "-crop", f"{lat}x{h_banda}+0+{sus + i * h_banda}",
                                  "+repage", "-colorspace", "Gray",
                                  "-format", "%[fx:mean]", "info:"))
                     for i in range(n_benzi)]
            medie = max(medii) if not UMBRA_ALBA else min(medii)
            spre_jos = y_text_sus > inalt // 2
            if UMBRA_ALBA:
                # text inchis, cu halou alb: cade pe fotografii intunecate
                nevoie, culoare = 0.36 - medie, "white"
            else:
                # text deschis, cu umbra neagra: cade pe fotografii luminoase
                nevoie, culoare = medie - 0.45, "black"
            if nevoie > 0:
                # cat trebuie stins ca textul sa aiba contrast, nu cat arata bine un degrade
                if UMBRA_ALBA:
                    opac = 1 - (1 - 0.62) / max(0.05, 1 - medie)
                else:
                    opac = 1 - 0.42 / max(0.05, medie)
                opac = min(0.72, max(0.25, opac))
                # voalul e plin peste blocul de text si se stinge abia dincolo de el:
                # un degrade pornit din marginea cadrului lasa tocmai randul de jos,
                # textul secundar, fara acoperire
                estompare = int(160 * s)
                plin = (inalt - sus) if spre_jos else jos
                plin = max(0, min(inalt, plin))
                est = min(estompare, inalt - plin)
                scrim = os.path.join(tmp, "voal.png")
                bucati = [os.path.join(tmp, "voal-plin.png"),
                          os.path.join(tmp, "voal-est.png")]
                magick("-size", f"{lat}x{max(1, plin)}", f"xc:{culoare}", bucati[0])
                magick("-size", f"{lat}x{max(1, est)}", f"gradient:{culoare}-none", bucati[1])
                if spre_jos:
                    magick(bucati[1], "-rotate", "180", bucati[1])
                    magick(bucati[1], bucati[0], "-append", scrim)
                else:
                    magick(bucati[0], bucati[1], "-append", scrim)
                magick(scrim, "-alpha", "set", "-channel", "A", "-evaluate", "multiply",
                       str(opac), "+channel", "PNG32:" + scrim)
                magick(baza, scrim, "-gravity", "south" if spre_jos else "north",
                       "-compose", "over", "-composite", baza)

    # pe fundalurile deschise umbra e un halou deschis, nu una neagra
    culoare_umbra = "white" if UMBRA_ALBA else "black"
    opacitate_umbra = "0.70" if UMBRA_ALBA else "0.55"

    if a.numar:
        c = os.path.join(tmp, "numar.png")
        bloc_text(c, a.numar, font_stil("numar", FONT_MONO),
                  int(30 * s * scara("numar")), lat_text, culoare=C_NUMAR)
        magick(c, "-trim", "+repage", "PNG32:" + c)
        # pastila din caruselele de referinta: contur rotunjit in jurul numarului
        if tipo.get("numar", {}).get("pastila"):
            pad_x, pad_y = int(30 * s), int(16 * s)
            magick(c, "-bordercolor", "none", "-border", f"{pad_x}x{pad_y}", "PNG32:" + c)
            w_p = int(magick("identify", "-format", "%w", c))
            h_p = int(magick("identify", "-format", "%h", c))
            gros = max(2, int(2.5 * s))
            magick(c, "-fill", "none", "-stroke", C_NUMAR, "-strokewidth", str(gros),
                   "-draw", f"roundrectangle {gros},{gros} {w_p - gros},{h_p - gros}"
                            f" {h_p // 2},{h_p // 2}", "PNG32:" + c)
        # rama transparenta: fara ea haloul numarului s-ar taia la marginea taieturii
        b = max(6, int(14 * s))
        magick(c, "-bordercolor", "none", "-border", str(b), "PNG32:" + c)
        # numarul e mono subtire peste coltul cel mai incarcat al fundalului. Umbra generala
        # nu-i ajunge: primeste un halou al lui, pus de doua ori, altfel se pierde peste
        # o piulita sau peste o umbra din poza.
        w_n = int(magick("identify", "-format", "%w", c))
        h_n = int(magick("identify", "-format", "%h", c))
        cu = os.path.join(tmp, "numar-umbra.png")
        magick(c, "-alpha", "extract", "-blur", f"0x{max(2, int(6 * s))}", "-level", "0,45%",
               "(", "-size", f"{w_n}x{h_n}", f"xc:{culoare_umbra}", ")", "+swap",
               "-alpha", "off", "-compose", "copy_opacity", "-composite", "PNG32:" + cu)
        # pe crem, haloul ar fi o pata murdara in jurul pastilei
        straturi_numar = (c,) if FARA_UMBRA else (cu, cu, c)
        if NUMAR_SUS:
            gravitatie = "northeast"
            geometrie = f"+{marg - b}+{int(marg * 0.95) - b}"
        else:
            # jos, in stanga (implicit) sau in dreapta, dupa stil
            gravitatie = "northeast" if NUMAR_DREAPTA else "northwest"
            geometrie = f"+{marg - b}+{inalt - int(104 * s) - b}"
        for strat in straturi_numar:
            magick(straturi, strat, "-gravity", gravitatie, "-geometry", geometrie,
                   "-compose", "over", "-composite", "PNG32:" + straturi)

    # umbra discreta sub text, ca sa se citeasca peste orice fundal.
    # Pe o suprafata plata nu are ce sa faca: textul are deja contrast.
    umbra = os.path.join(tmp, "umbra.png")
    magick(straturi, "-alpha", "extract", "-blur", f"0x{int(18 * s)}", "-level", "0,60%",
           "(", "-size", f"{lat}x{inalt}", f"xc:{culoare_umbra}", ")", "+swap", "-alpha", "off",
           "-compose", "copy_opacity", "-composite", "-channel", "A", "-evaluate",
           "multiply", opacitate_umbra, "+channel", "PNG32:" + umbra)
    if FARA_UMBRA:
        magick(baza, straturi, "-compose", "over", "-composite", a.output)
    else:
        magick(baza, umbra, "-compose", "over", "-composite", straturi, "-compose", "over",
               "-composite", a.output)

    # pozele proprii, ca un colaj usor inclinat, in partea de jos
    if fotografii:
        n = min(len(fotografii), 3)
        lat_foto = int((lat - 2 * marg) / (1.6 if n == 1 else 2.15 if n == 2 else 2.9))
        inalt_foto = int(lat_foto * 1.25)
        centru_y = int(inalt * 0.68)
        pas = int((lat - 2 * marg - lat_foto) / max(1, n - 1)) if n > 1 else 0
        for i, cale in enumerate(fotografii[:3]):
            if not os.path.exists(cale):
                sys.exit(f"poza lipseste: {cale}")
            c = os.path.join(tmp, f"foto-{i}.png")
            magick(cale, "-resize", f"{lat_foto}x{inalt_foto}^", "-gravity", "center",
                   "-extent", f"{lat_foto}x{inalt_foto}",
                   "-bordercolor", "white", "-border", str(max(4, int(10 * s))),
                   "-background", "none", "-rotate", str(-4 + i * 4),
                   "PNG32:" + c)
            x = marg + i * pas
            y_foto = centru_y - inaltime(c) // 2 + (int(14 * s) if i % 2 else 0)
            magick(a.output, "(", c, "-background", "black", "-shadow", "45x18+0+10", ")",
                   "-geometry", f"+{x - int(20 * s)}+{y_foto + int(10 * s)}", "-compose", "over",
                   "-composite", c, "-geometry", f"+{x}+{y_foto}", "-compose", "over",
                   "-composite", a.output)

    # captura-dovada: intreaga, dreapta, cat de mare incape. Nu se decupeaza si nu se
    # inclina aici, pentru ca tot ce trebuie citit pe ea a fost decis la pregatire.
    if a.dovada:
        sus = int(inalt * ZONA_TEXT_DOVADA)
        jos = inalt - int(150 * s)
        zona_l, zona_i = lat - 2 * marg, jos - sus
        d = os.path.join(tmp, "dovada.png")
        magick(a.dovada, "-background", "none", "-resize", f"{zona_l}x{zona_i}",
               "PNG32:" + d)
        d_l, d_i = int(magick("identify", "-format", "%w", d)), inaltime(d)
        magick(a.output, d, "-gravity", "northwest",
               "-geometry", f"+{(lat - d_l) // 2}+{sus + (zona_i - d_i) // 2}",
               "-compose", "over", "-composite", a.output)

    if a.logo:
        m = int(90 * s)
        mono = stil.get("logo_mono")
        logo_brand = stil.get("logo_fisier")
        if logo_brand:
            # logo-ul brandului, de obicei un nume scris, lat, nu patrat: se asaza in
            # coltul din dreapta jos, pe aceeasi linie cu numarul, in interiorul marginii
            cale_logo = os.path.join(RESURSE, logo_brand)
            lat_logo = int(stil.get("logo_latime", 260) * s)
            sigla = os.path.join(tmp, "logo-brand.png")
            magick(cale_logo, "-resize", f"{lat_logo}x", "PNG32:" + sigla)
            h_logo = inaltime(sigla)
            magick(a.output, sigla, "-gravity", "northeast",
                   "-geometry", f"+{marg}+{inalt - int(104 * s) + int(18 * s) - h_logo // 2}",
                   "-compose", "over", "-composite", a.output)
        elif mono:
            # se scoate fundalul patrat al siglei si se toarna semnul intr-o
            # singura culoare din paleta, cu o umbra moale sub el ca sa tina
            # si pe fotografiile deschise.
            sigla = os.path.join(tmp, "logo-mono.png")
            magick(LOGO, "-fuzz", "22%", "-transparent", "srgb(46,55,62)",
                   "-fill", mono, "-colorize", "100", "-resize", f"{m}x{m}", sigla)
            magick(a.output,
                   "(", sigla, "-background", "black", "-shadow", "55x10+0+0", ")",
                   "-gravity", "southeast", "-geometry", f"+{int(46 * s)}+{int(40 * s)}",
                   "-composite",
                   sigla, "-gravity", "southeast",
                   "-geometry", f"+{int(50 * s)}+{int(44 * s)}", "-composite", a.output)
        else:
            magick(a.output, "(", LOGO, "-resize", f"{m}x{m}", ")", "-gravity", "southeast",
                   "-geometry", f"+{int(50 * s)}+{int(44 * s)}", "-composite", a.output)

    print(json.dumps({"output_path": os.path.abspath(a.output),
                      "size_bytes": os.path.getsize(a.output),
                      "avertisment": avertisment}, ensure_ascii=False))


if __name__ == "__main__":
    main()
