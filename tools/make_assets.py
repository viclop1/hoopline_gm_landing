#!/usr/bin/env python3
"""Regenera las fuentes, las capturas recortadas y la imagen para redes de dist/assets.

Solo hace falta si cambian las capturas de la App Store o la tipografía; el día a día es `python3 build.py`.
Requiere Pillow y fontTools:  pip install pillow fonttools

Uso:
  python3 tools/make_assets.py --shots "<carpeta 'para App Store'>" [--fonts <carpeta con Inter *.otf>]

La carpeta de capturas debe tener en/ es/ de/ fr/ con los nombres de la 1.0.1 (01_market, 03_team, 04_box, 05_table;
en francés 01_market, 02_team, 03_box, 04_table). Las fuentes son Inter (licencia OFL): Inter-Regular, Inter-SemiBold, InterDisplay-ExtraBold.
"""
import argparse, os
from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--shots", required=True)
ap.add_argument("--fonts", default="/usr/share/fonts/opentype/inter/")
ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dist", "assets"))
a = ap.parse_args()
OUT = os.path.abspath(a.out)
os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True)
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)

# --- fuentes: subconjunto latino, formato woff
FONTS = {"InterDisplay-ExtraBold.otf": "inter-display-800", "Inter-Regular.otf": "inter-400", "Inter-SemiBold.otf": "inter-600"}
UNI = list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + [0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x20AC, 0x2192, 0x2190, 0x2212, 0x2713, 0xD7, 0x192]
for src, name in FONTS.items():
    o = subset.Options(); o.flavor = "woff"; o.layout_features = ["*"]; o.name_IDs = [1, 2, 3, 4, 6]; o.notdef_outline = True
    f = TTFont(os.path.join(a.fonts, src)); s = subset.Subsetter(o); s.populate(unicodes=UNI); s.subset(f)
    f.flavor = "woff"; f.save(os.path.join(OUT, "fonts", name + ".woff"))

# --- capturas: recorte al móvil con esquinas redondeadas y transparencia
FILES = {l: {"market": "01_market", "team": "03_team", "box": "04_box", "table": "05_table"} for l in ("en", "es", "de")}
FILES["fr"] = {"market": "01_market", "team": "02_team", "box": "03_box", "table": "04_table"}
# pantallas de los bloques por función: no todos los idiomas tienen ambas (falta es/cups y fr/board en la carpeta de la App Store)
FILES["en"].update({"board": "02_board", "cups": "06_cups"})
FILES["es"].update({"board": "02_board"})
FILES["de"].update({"board": "02_board", "cups": "06_cups"})
FILES["fr"].update({"cups": "05_cups"})
BOX, R, W = (134, 553, 1158, 2716), 128, 560
for lang, m in FILES.items():
    for k, f in m.items():
        im = Image.open(os.path.join(a.shots, lang, f + ".png")).convert("RGB").crop(BOX)
        mask = Image.new("L", (im.width * 2, im.height * 2), 0)
        ImageDraw.Draw(mask).rounded_rectangle((2, 2, im.width * 2 - 3, im.height * 2 - 3), radius=R * 2, fill=255)
        im.putalpha(mask.resize(im.size, Image.LANCZOS))
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        im.save(os.path.join(OUT, "img", f"{lang}-{k}.webp"), quality=84, method=6)

# --- imagen para redes (1200x630)
Wd, Ht = 1200, 630
base = Image.new("RGBA", (Wd, Ht), "#0D1014"); d = ImageDraw.Draw(base)
F = lambda n, s: ImageFont.truetype(os.path.join(a.fonts, n), s)
d.text((72, 64), "Hoopline GM", font=F("InterDisplay-ExtraBold.otf", 34), fill="#F2F5F8")
d.text((72, 190), "Every bid", font=F("InterDisplay-ExtraBold.otf", 100), fill="#F2F5F8")
d.text((72, 300), "in the open", font=F("InterDisplay-ExtraBold.otf", 100), fill="#F2F5F8")
d.text((72, 452), "Draft, bid and build a basketball team.", font=F("Inter-Regular.otf", 30), fill="#C9D1DB")
d.text((72, 494), "A manager game where nothing is hidden.", font=F("Inter-Regular.otf", 30), fill="#C9D1DB")
ph = Image.open(os.path.join(OUT, "img", "en-market.webp")).convert("RGBA"); pw = 380
ph = ph.resize((pw, round(ph.height * pw / ph.width)), Image.LANCZOS)
layer = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); layer.alpha_composite(ph, (770, 90))
mask = np.full((Ht, Wd), 255, dtype=np.uint8)
for y in range(420, Ht): mask[y, :] = int(255 * max(0, 1 - (y - 420) / 210))
layer.putalpha(Image.fromarray(np.minimum(np.array(layer.split()[3]), mask)))
base.alpha_composite(layer); base.convert("RGB").save(os.path.join(OUT, "og.png"), optimize=True)
print("assets en", OUT)
