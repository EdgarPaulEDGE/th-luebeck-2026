"""Rechnet eine Logodatei in eine weiße Silhouette um und trägt sie in assets/logos/referenzen.json ein.

Aufruf:  python3 werkzeuge/logo_weiss.py <kennung> "<Anzeigename>" <g|k> <quelldatei>
         python3 werkzeuge/logo_weiss.py --entfernen <kennung> [<kennung> ...]
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image

ORDNER = Path(__file__).resolve().parent.parent
LISTE = ORDNER / "assets/logos/referenzen.json"


def laden(pfad):
    if pfad.lower().endswith(".svg"):
        # Quick Look rendert SVG auf weißem Grund, weiße Füllungen würden verschwinden: vorher schwarz färben
        tmp = tempfile.mkdtemp(); kopie = os.path.join(tmp, "l.svg")
        roh = open(pfad, encoding="utf8", errors="ignore").read()
        roh = re.sub(r"#fff(?:fff)?\b|\bwhite\b|rgb\(255, ?255, ?255\)", "#000000", roh, flags=re.I)
        open(kopie, "w", encoding="utf8").write(roh)
        subprocess.run(["qlmanage", "-t", "-s", "1400", "-o", tmp, kopie], capture_output=True, timeout=60)
        return Image.open(os.path.join(tmp, "l.svg.png")).convert("RGBA")
    return Image.open(pfad).convert("RGBA")


def weiss(im):
    im.thumbnail((1400, 1400))
    a = np.asarray(im).astype(np.float32); rgb, al = a[..., :3], a[..., 3] / 255
    lum = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 255
    if (al < 0.1).mean() > 0.05:                      # echter transparenter Grund
        deck = al > 0.5
        hell = lum[deck].mean() if deck.any() else 1
        tinte = al if hell > 0.72 else al * np.clip((1 - lum) * 2.4, 0, 1)
    else:                                             # deckender Grund: Farbabstand zur Eckfarbe
        ecken = np.concatenate([rgb[:6, :6].reshape(-1, 3), rgb[:6, -6:].reshape(-1, 3), rgb[-6:, :6].reshape(-1, 3), rgb[-6:, -6:].reshape(-1, 3)])
        tinte = np.clip((np.linalg.norm(rgb - np.median(ecken, axis=0), axis=2) - 18) / 110, 0, 1)
    aus = np.zeros(a.shape, np.uint8); aus[..., :3] = 255; aus[..., 3] = (tinte * 255).astype(np.uint8)
    bild = Image.fromarray(aus, "RGBA")
    bild = bild.crop(bild.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox()); bild.thumbnail((640, 240))
    return bild


liste = json.loads(LISTE.read_text(encoding="utf8"))
if sys.argv[1] == "--entfernen":
    for k in sys.argv[2:]:
        liste = [l for l in liste if l["id"] != k]; (ORDNER / f"assets/logos/ref-{k}.png").unlink(missing_ok=True); print("entfernt", k)
else:
    kennung, name, klasse, quelle = sys.argv[1:5]
    b = weiss(laden(quelle)); b.save(ORDNER / f"assets/logos/ref-{kennung}.png", optimize=True)
    liste = [l for l in liste if l["id"] != kennung] + [dict(id=kennung, name=name, klasse=klasse, w=b.width, h=b.height)]
    print("ok", kennung, b.size)
LISTE.write_text(json.dumps(liste, ensure_ascii=False), encoding="utf8")
