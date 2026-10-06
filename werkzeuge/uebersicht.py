"""Baut Kontaktbögen aus den Prüfbildern: je Bogen 6 Folien (3 x 2), Folie groß genug zum Lesen."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ordner = Path(sys.argv[1]); ziel = Path(sys.argv[2]); ziel.mkdir(parents=True, exist_ok=True)
bilder = sorted(ordner.glob("folie-*.png"))
B, H, sp = 760, 428, 3
for start in range(0, len(bilder), 6):
    teil = bilder[start:start + 6]
    bogen = Image.new("RGB", (sp * B + (sp + 1) * 10, 2 * (H + 28) + 10), "white")
    d = ImageDraw.Draw(bogen)
    for i, f in enumerate(teil):
        im = Image.open(f).convert("RGB").resize((B, H))
        x, y = 10 + (i % sp) * (B + 10), 10 + (i // sp) * (H + 28)
        bogen.paste(im, (x, y + 18)); d.text((x, y + 2), f.stem, fill="black")
    bogen.save(ziel / f"bogen-{start // 6 + 1}.jpg", quality=85)
print(len(bilder), "Folien")
