#!/usr/bin/env python3
"""Catalogul de stiluri vizuale pentru carusele.

Un stil inseamna doua lucruri, tinute impreuna ca sa nu se desincronizeze:

1. `prompt`  — sablonul trimis la kie.ai pentru fundal, cu {ELEMENT}, {ZONA} si {CONTRA}
2. `paleta`  — culorile cu care `compune_slide.py` scrie textul PESTE fundalul ala

Textul NU e desenat de model niciodata. Modelul face doar fundalul.

Folosire:
  python3 scripts/stiluri.py --lista
  python3 scripts/stiluri.py --alege "campanie pentru un service auto din Cluj"
  python3 scripts/stiluri.py --prompt atelier --element "o cheie fixa pe un banc de lucru"
"""
import argparse
import re
import sys

STILURI = {
    "aurora": {
        "eticheta": "Aurora",
        "cand": "tehnologie, AI, software, automatizari; brandul Personality AI Architect",
        "prompt": (
            "cinematic abstract background, near-black center #06070A, large soft glowing "
            "aurora lights: vivid teal #4ECDC4 glow top left, rich lavender purple #C084FC "
            "glow top right, warm copper orange #E08A5E glow at the bottom, {ELEMENT} kept in the {CONTRA} of the frame, "
            "depth, subtle bokeh, premium, high contrast, {CADRU}, no text, no letters, no logo, no robots, no cyberpunk "
            "city, no circuit brain"
        ),
        "element_implicit": "a delicate network of fine luminous connected nodes and "
                            "particles floating in the light",
        "cadru": {
            "zona": "large clean dark empty area in the {ZONA} for text",
            "plin": "the light fills the whole frame, balanced, nothing cropped at the edges",
        },
        "paleta": {
            "titlu1": "#FFFFFF",
            "titlu2": ("#F0A070", "#C084FC"),  # doua culori = gradient
            "text": "#D5D7DB",
            "eticheta": "#F0A070",
            "numar": "#4ECDC4",
            "umbra": "negru",
        },
        "cuvinte": r"\b(agen[tț]|inteligen[tț][aă]|tehnolog|software|automatiz|digital|"
                   r"programare|saas|chatbot|robo)\w*|\bai\b",
    },
    "hartie-editoriala": {
        "eticheta": "Hârtie editorială",
        "cand": "educație, cursuri, meditații, scriere, consultanță, mentorat",
        "prompt": (
            "editorial print background, warm off-white paper #F4F0E6 with fine paper "
            "grain, {ELEMENT} kept in the {CONTRA} of the frame, rendered as a restrained ink and gouache illustration in "
            "brick red #8C3A2B and deep ink #1A1A18, {CADRU}, soft natural shadow, magazine quality, calm, no text, no letters, "
            "no logo, no gradients, no glow, no neon"
        ),
        "element_implicit": "a single open book and a fountain pen seen from above",
        "cadru": {
            "zona": "generous empty paper in the {ZONA} for text",
            "plin": "the illustration is centred and fills the frame, even paper margins around it",
        },
        # sigla vine ca patrat bleumarin cu accent turcoaz, strain de cerneala si hartie
        "logo_mono": "#1A1A18",
        "paleta": {
            "titlu1": "#1A1A18",
            "titlu2": "#8C3A2B",
            "text": "#4A4A45",
            "eticheta": "#8C3A2B",
            "numar": "#8C8B84",
            "umbra": "alb",
        },
        "cuvinte": r"\b(curs|lec[tț]i|profesor|medita[tț]i|[iî]nv[aă][tț]|educa[tț]i|"
                   r"englez|limb[aă]|scriere|carte|mentorat|consultan[tț])\w*",
    },
    "atelier": {
        "eticheta": "Atelier",
        "cand": "service auto, meserii, construcții, instalații, reparații, utilaje",
        "prompt": (
            "industrial workshop background, dark brushed concrete and steel, cool grey "
            "#23262A, {ELEMENT} kept in the {CONTRA} of the frame, lit by a hard directional work light, safety orange "
            "#FF6A2B accent light on one edge, fine dust in the air, honest and sturdy, "
            "{CADRU}, no text, no letters, "
            "no logo, no neon, no cyberpunk"
        ),
        "element_implicit": "a set of well-used hand tools arranged on a workbench",
        "cadru": {
            "zona": "large clean dark empty area in the {ZONA} for text",
            "plin": "the scene is centred and fills the whole frame, no empty corners",
        },
        "paleta": {
            "titlu1": "#F5F5F3",
            "titlu2": "#FF6A2B",
            "text": "#C9C9C4",
            "eticheta": "#FF6A2B",
            "numar": "#9AA0A6",
            "umbra": "negru",
        },
        "cuvinte": r"\b(service|auto|mecanic|instala[tț]|construc[tț]i|t[aâ]mpl|"
                   r"repara[tț]i|utilaj|montaj|vulcaniz|caroser|anvelop)\w*",
    },
    "studio-cald": {
        "eticheta": "Studio cald",
        "cand": "wellness, nutriție, terapie, cosmetică, yoga, îngrijire personală",
        "prompt": (
            "warm studio background, sand and terracotta tones #E8DCCB, soft daylight "
            "from one side, {ELEMENT} on a plain surface in the {CONTRA} of the frame, gentle natural shadow, calm and "
            "tactile, film photography feel, {CADRU}, "
            "no text, no letters, no logo, no glow, no neon, no gradients"
        ),
        "element_implicit": "a ceramic cup and a few dried leaves",
        "cadru": {
            "zona": "generous empty area in the {ZONA} for text",
            "plin": "the scene is centred and fills the frame, calm and even composition",
        },
        "paleta": {
            "titlu1": "#2B211C",
            "titlu2": "#B4573A",
            "text": "#5A4C44",
            "eticheta": "#B4573A",
            "numar": "#9C8B80",
            "umbra": "alb",
        },
        "cuvinte": r"\b(wellness|nutri[tț]i|terapi|masaj|yoga|cosmetic|spa|[iî]ngrijire|"
                   r"s[aă]n[aă]tate|relaxare|medita[tț]ie ghidat)\w*",
    },
    "bloc-tipar": {
        "eticheta": "Bloc tipar",
        "cand": "evenimente, lansări, promoții, anunțuri, înscrieri cu termen",
        "prompt": (
            "flat two-color print poster background, deep blue #14294F and cream #FFF7E8, "
            "{ELEMENT} as a bold simplified cut-paper silhouette kept entirely in the "
            "bottom third of the frame, screen print texture, slight misregistration, "
            "high contrast, {CADRU}, no text, no letters, no logo, no photo realism, no gradients"
        ),
        "element_implicit": "a megaphone and three diagonal rays",
        "cadru": {
            "zona": "the {ZONA} is a big empty flat deep blue area for text, nothing in it",
            "plin": "the silhouette is centred and fills the frame, flat colour around it",
        },
        "paleta": {
            "titlu1": "#FFF7E8",
            "titlu2": "#FFD447",
            "text": "#D9E2F0",
            "eticheta": "#FFD447",
            "numar": "#FFD447",
            "umbra": "negru",
            # elementul sta jos, deci numarul slide-ului urca in coltul din dreapta sus
            "numar_pozitie": "sus",
        },
        "cuvinte": r"\b(eveniment|lansare|workshop|webinar|promo[tț]i|reducere|anun[tț]|"
                   r"[iî]nscrier|concurs|ofert[aă]|termen)\w*",
    },
    # Dupa caruselele de referinta din `referinte/postare-utila/`: fotografie calda pe tot
    # cadrul, titlu urias cu antiqua alba peste ea, subtitlu sans bold caps sub el.
    # Se ia tratamentul tipografic si fotografic, nu pozele si nu oamenii din ele.
    "editorial-foto": {
        "eticheta": "Editorial foto",
        "cand": "poveste personală de brand, opinie, lucruri în care crezi; look de revistă",
        "prompt": (
            "warm editorial photograph, soft natural window light from one side, "
            "{ELEMENT} kept in the {CONTRA} of the frame, textured plaster wall in warm "
            "taupe #6E5E50, clay red and dusty rose accents, deep soft shadows, shallow "
            "depth of field, fine film grain, muted warm palette, magazine cover feel, "
            "{CADRU}, no text, no letters, "
            "no logo, no faces, no recognizable people, no neon, no gradients"
        ),
        "element_implicit": "a wooden chair with a linen dress draped over it",
        "cadru": {
            "zona": "large calm uncluttered area in the {ZONA} for text",
            "plin": "the scene fills the whole frame, centred, rich texture and depth",
        },
        "zona_implicita": "lower half",
        "paleta": {
            "titlu1": "#FFFFFF",
            "titlu2": "#F7F1E8",
            "text": "#EDE1D2",
            "eticheta": "#E8C87E",
            "numar": "#F0E7DA",
            "umbra": "negru",
            "numar_pozitie": "jos-dreapta",
        },
        # suprafata plata pentru layout-urile `banda` si `panou`, plus culorile textului
        # pe ea: pe crem, textul alb ar disparea
        # logo-ul original e un patrat bleumarin cu accent turcoaz, strain de paleta
        # calda: pe stilul asta il decupam de pe fundal si il turnam intr-o culoare.
        "logo_mono": "#F7F1E8",
        "culoare_panou": "#E9DED0",
        "paleta_panou": {
            "titlu1": "#2E241D",
            "titlu2": "#6B5646",
            "text": "#6B5646",
            "eticheta": "#A5753C",
            "numar": "#6B5646",
            "umbra": "fara",
            "numar_pozitie": "jos-dreapta",
        },
        "tipografie": {
            "numar": {"font": "InstrumentSans-Regular.ttf", "scara": 0.95, "pastila": True},
            "titlu1": {"font": "PlayfairDisplay-Black.ttf", "caps": True},
            "titlu2": {"caps": True, "scara": 0.52},
            "text": {"caps": True, "scara": 0.80},
            "linie": False,
            "pozitie": "jos",
        },
        "cuvinte": r"\b(brand personal|poveste|editorial|revist[aă]|opinie|manifest|"
                   r"credin[tț]|valori)\w*",
    },
}

IMPLICIT = "aurora"

# Aurora se verifica ultima: „ai" prinde si verbul romanesc, deci lasa intai
# stilurile cu cuvinte specifice de nisa.
ORDINE = ["atelier", "hartie-editoriala", "studio-cald", "bloc-tipar", "editorial-foto", "aurora"]


def alege(brief):
    """Intoarce (id_stil, motiv). Daca nimic nu se potriveste, intoarce (None, None).

    Cand se potrivesc mai multe stiluri, il intoarce pe primul din ORDINE, dar spune in
    motiv si care sunt celelalte: „atelier de fotografie cu inscrieri" e si eveniment, si
    mestesug, iar alegerea aia o face omul, nu ordinea din lista.
    """
    t = brief.lower()
    gasite = []
    for sid in ORDINE:
        m = re.search(STILURI[sid]["cuvinte"], t)
        if m:
            gasite.append((sid, m.group(0)))
    if not gasite:
        return None, None
    sid, cuvant = gasite[0]
    motiv = "„" + cuvant + "” din brief"
    if len(gasite) > 1:
        altele = ", ".join(f"{s} („{c}”)" for s, c in gasite[1:])
        motiv += f"; se potrivesc și {altele}, deci arată exemplele și întreabă omul"
    return sid, motiv


# Unde sta elementul, ca sa nu urce peste text: partea opusa zonei lasate libere.
# Fara asta modelul pune obiectul in mijloc si frazele de sub titlu cad peste el.
CONTRA_ZONA = {
    "upper half": "lower half",
    "lower half": "upper half",
    "center": "bottom third",
}


# Fiecare layout vrea alt fel de fotografie. `banda` taie imaginea la 58% din inaltime si
# pune textul pe o suprafata plata dedesubt, `citat` o intuneca si scrie peste ea: amandoua
# vor cadru plin, nu spatiu gol. `panou` nu foloseste fotografie deloc.
CADRU_PENTRU_LAYOUT = {
    "foto-sus": ("zona", "upper half"),
    "foto-jos": ("zona", "lower half"),
    "banda": ("plin", None),
    "citat": ("plin", None),
    "auto": None,
}


def prompt_pentru(sid, element=None, zona=None, layout=None):
    s = STILURI[sid]
    fel = "zona"
    if layout and layout != "auto":
        if layout in ("panou", "dovada"):
            raise ValueError(f"layout-ul `{layout}` nu foloseste fotografie generata: "
                             "nu generezi fundal pentru el")
        fel, zona_layout = CADRU_PENTRU_LAYOUT[layout]
        zona = zona or zona_layout
    # la stilurile care isi aseaza textul jos, zona libera e jos, nu sus
    zona = zona or s.get("zona_implicita", "upper half")
    cadru = s["cadru"][fel].format(ZONA=zona)
    return s["prompt"].format(
        ELEMENT=element or s["element_implicit"], ZONA=zona, CADRU=cadru,
        CONTRA=CONTRA_ZONA.get(zona, "lower half") if fel == "zona" else "middle"
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lista", action="store_true")
    p.add_argument("--alege", metavar="BRIEF")
    p.add_argument("--prompt", metavar="STIL")
    p.add_argument("--element", default=None)
    # textul se aseaza in jumatatea de sus, deci acolo ceri loc gol.
    # Fara --zona, fiecare stil foloseste zona lui implicita.
    p.add_argument("--zona", default=None,
                   choices=["upper half", "center", "lower half"])
    p.add_argument("--layout", default=None,
                   choices=["auto", "foto-sus", "foto-jos", "banda", "citat", "panou", "dovada"],
                   help="layout-ul slide-ului; el decide daca fotografia lasa loc gol "
                        "sau umple cadrul")
    a = p.parse_args()

    if a.lista:
        for sid, s in STILURI.items():
            print(f"{sid:20} {s['eticheta']:22} {s['cand']}")
        return
    if a.alege:
        sid, motiv = alege(a.alege)
        if sid:
            print(f"{sid}\t{motiv}")
        else:
            print("niciun stil nu se potriveste clar; intreaba omul, "
                  "cu trei variante din --lista")
            sys.exit(2)
        return
    if a.prompt:
        if a.prompt not in STILURI:
            sys.exit(f"stil necunoscut: {a.prompt}")
        try:
            print(prompt_pentru(a.prompt, a.element, a.zona, a.layout))
        except ValueError as e:
            sys.exit(str(e))
        return
    p.print_help()


if __name__ == "__main__":
    main()
