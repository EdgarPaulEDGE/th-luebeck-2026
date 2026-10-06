"""Baut assets/collage/collage.jpg: die gewachsene Collage aus der IHK Kneipentalk Keynote als Basis,
neue Fotos werden randlos darübergesetzt.

Aufruf:  python3 werkzeuge/collage.py

Alle Kästen sind in Pixeln auf einer 1920 x 1080 Folie angegeben: (datei, links, oben, rechts, unten, fokus).
WICHTIG: Die Kästen liegen exakt auf den Kanten der Fotos in der Vorlage (mit Messraster abgelesen). Wer einen Kasten
verschiebt, lässt Reststreifen des alten Fotos stehen oder schneidet Nachbarn die Köpfe ab. Vor Änderungen
`python3 werkzeuge/collage.py --raster` aufrufen: das schreibt vier vergrößerte Viertel der Vorlage mit Koordinatennetz.
fokus = welcher Höhenanteil des neuen Fotos im Ausschnitt bleibt (0 oben, 1 unten). Statt fokus geht auch ein fester
Ausschnitt des Quellfotos als Tupel (links, oben, rechts, unten) in Anteilen.
Nicht überdecken: Günther in der Mitte, Urkunde unten links, Handschlag unten rechts, das Trio unten mittig (Doms Kopf!).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

HIER = Path(__file__).resolve().parent / "collage"
ZIEL = HIER.parent.parent / "assets/collage/collage.jpg"

EINSAETZE = [
    # Eigene Fotos 2025 und 2026
    ("18.jpg",                     0,   0,  345,  229, .40),                 # EDGE über Lübeck (statt Türfoto)
    ("16.jpg",                  1555,   0, 1920,  199, (0, .515, 1, .88)),   # unser IHK Kneipentalk: Querstreifen mit beiden und Leinwand
    ("15.jpg",                   190, 545,  368,  745, .30),                 # Forum Ehrenamt am Pult
    ("21.jpg",                     0, 592,  190,  745, .55),                 # Lübeck.Lokal auf dem Dach
    ("12.jpg",                  1255, 540, 1542,  680, .45),                 # Vortrag vor vollem Saal (endet über den Köpfen der Frauengruppe)
    ("19.jpg",                   385, 955,  656, 1080, .60),                 # Team vor dem Rathaus
    # Trio draußen aus dem Original. Muss VOR Roboter Gruppe und VfB Trikot stehen: die liegen oben links und rechts darüber,
    # in der Lücke dazwischen (x 893 bis 975) schaut Doms Kopf heraus, so wie in der Keynote Vorlage.
    ("20.jpg",                   656, 795, 1007, 1080, .5),
    # LinkedIn, Edgar und Emre
    ("li-guenther-vfb.jpg",     1387, 388, 1572,  540, .38),                 # Günther mit Emre im VfB Stadion
    ("li-vfb-gruppe.jpg",       1370, 230, 1572,  388, .45),
    ("li-vfb-stadion.jpg",      1542, 596, 1733,  733, .50),
    ("li-vfb-trikot.jpg",        975, 745, 1146,  900, .35),
    ("li-lachclash-gruppe.jpg",  290, 230,  528,  388, .50),
    ("li-lachclash-duo.jpg",     528, 281,  613,  395, .55),
    ("li-moin.jpg",              590, 572,  833,  713, .60),
    ("li-roboter-gruppe.jpg",    627, 713,  893,  850, .42),
    ("li-it4b.jpg",             1043, 520, 1147,  648, .45),
    ("li-fussball-team.jpg",     957,   0, 1150,  124, .50),
    ("li-fussball-bild.jpg",       0, 229,  172,  379, .45),
    ("li-anzug-trio.jpg",        161, 380,  378,  545, .0),
    ("li-workshop-selfie.jpg",   957, 124, 1152,  222, 1.0),
]

basis = Image.open(HIER / "basis.png").convert("RGB"); W, H = basis.size

if "--raster" in sys.argv:
    klein = basis.resize((1920, 1080), Image.LANCZOS)
    for name, (x0, y0) in {"A_oben_links": (0, 0), "B_oben_rechts": (960, 0), "C_unten_links": (0, 540), "D_unten_rechts": (960, 540)}.items():
        t = klein.crop((x0, y0, x0 + 960, y0 + 540)).resize((1920, 1080), Image.LANCZOS); d = ImageDraw.Draw(t)
        for g in range(0, 961, 40):
            d.line([(g * 2, 0), (g * 2, 1080)], fill=(255, 255, 0)); d.text((g * 2 + 3, 3), str(x0 + g), fill=(255, 255, 0))
        for g in range(0, 541, 40):
            d.line([(0, g * 2), (1920, g * 2)], fill=(0, 255, 255)); d.text((3, g * 2 + 2), str(y0 + g), fill=(0, 255, 255))
        t.save(HIER / f"raster_{name}.jpg", quality=80)
    print("Raster geschrieben nach", HIER); sys.exit()

for datei, l, o, r, u, fokus in EINSAETZE:
    kasten = (round(l / 1920 * W), round(o / 1080 * H), round(r / 1920 * W), round(u / 1080 * H))
    groesse = (kasten[2] - kasten[0], kasten[3] - kasten[1])
    foto = Image.open(HIER / "neu" / datei).convert("RGB")
    if isinstance(fokus, tuple):
        fw, fh = foto.size; foto = foto.crop((int(fokus[0] * fw), int(fokus[1] * fh), int(fokus[2] * fw), int(fokus[3] * fh))); fokus = .5
    basis.paste(ImageOps.fit(foto, groesse, Image.LANCZOS, centering=(.5, fokus)), kasten[:2])
ImageOps.fit(basis, (2560, 1440), Image.LANCZOS).save(ZIEL, quality=86, optimize=True)
print("gebaut:", ZIEL)
