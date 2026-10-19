#!/usr/bin/env python3
"""Regenera las fuentes, las capturas recortadas y (opcionalmente) la imagen para redes de dist/assets.

Solo hace falta si cambian las capturas de la App Store o la tipografía; el día a día es `python3 build.py`.
Requiere Pillow y fontTools:  pip install pillow fonttools

Uso:
  python3 tools/make_assets.py --shots "<carpeta 'para App Store'>" [--fonts <carpeta con los TTF de la app>] [--og]

La carpeta de capturas debe tener en/ es/ de/ fr/ con los nombres de la 1.0.1 (01_market, 03_team, 04_box, 05_table;
en francés 01_market, 02_team, 03_box, 04_table).
Pantallas sin captura de la App Store en su idioma (es/cups, fr/board): se enmarcan desde la captura cruda con tools/frame_raw.py
(fuentes en tools/raw-captures/; este script lo hace solo).

Tipografía: la de la app (Archivo y Barlow, licencia OFL), desde ../hoopline_gm/fonts. Se sirven como subconjunto latino en woff.
Capturas: 800 px de ancho (nítidas a 2x hasta ≈ 400 px), con el nombre `<idioma>-<pantalla>-800.webp`. El sufijo importa:
/assets/* se sirve con caché inmutable, así que un archivo nuevo necesita un nombre nuevo.
Recortes (se conserva la parte superior, donde está la información): market 72 %, box y table 76 %; el resto, completas.
"""
import argparse, os, subprocess, sys
from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--shots", required=True)
ap.add_argument("--fonts", default=os.path.join(HERE, "..", "..", "hoopline_gm", "fonts"))
ap.add_argument("--out", default=os.path.join(HERE, "..", "dist", "assets"))
ap.add_argument("--og", action="store_true", help="regenera también og.png (por defecto no se toca)")
a = ap.parse_args()
OUT = os.path.abspath(a.out)
os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True)
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)

# --- fuentes: subconjunto latino, formato woff
FONTS = {"Archivo-Bold.ttf": "archivo-700", "Archivo-SemiBold.ttf": "archivo-600", "Barlow-Regular.ttf": "barlow-400", "Barlow-SemiBold.ttf": "barlow-600"}
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
BOX, R, W = (134, 553, 1158, 2716), 128, 800
KEEP = {"market": 0.72, "box": 0.76, "table": 0.76}   # parte superior que se conserva (el resto lo tapa el degradado de la web)

def save(im, lang, k):
    """Recorta por abajo según KEEP y guarda como <idioma>-<pantalla>-800.webp."""
    keep = KEEP.get(k, 1.0)
    if keep < 1.0:
        im = im.crop((0, 0, im.width, round(im.height * keep)))
    im.save(os.path.join(OUT, "img", f"{lang}-{k}-{W}.webp"), quality=78, method=6)

for lang, m in FILES.items():
    for k, f in m.items():
        im = Image.open(os.path.join(a.shots, lang, f + ".png")).convert("RGB").crop(BOX)
        mask = Image.new("L", (im.width * 2, im.height * 2), 0)
        ImageDraw.Draw(mask).rounded_rectangle((2, 2, im.width * 2 - 3, im.height * 2 - 3), radius=R * 2, fill=255)
        im.putalpha(mask.resize(im.size, Image.LANCZOS))
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        save(im, lang, k)

# es/cups y fr/board: desde la captura cruda, con el marco de otra captura del mismo idioma
for lang, k, ref in (("es", "cups", "01_market"), ("fr", "board", "01_market")):
    raw = os.path.join(HERE, "raw-captures", f"{lang}-{k}.png")
    if os.path.exists(raw):
        tmp = os.path.join(OUT, "img", f"{lang}-{k}-{W}.webp")
        subprocess.run([sys.executable, os.path.join(HERE, "frame_raw.py"), raw, os.path.join(a.shots, lang, ref + ".png"), tmp], check=True)

# --- imagen para redes (1200x630): solo con --og
if a.og:
    Wd, Ht = 1200, 630
    base = Image.new("RGBA", (Wd, Ht), "#0D1014"); d = ImageDraw.Draw(base)
    F = lambda n, s: ImageFont.truetype(os.path.join(a.fonts, n), s)
    d.text((72, 64), "Hoopline GM", font=F("Archivo-Bold.ttf", 34), fill="#F2F5F8")
    d.text((72, 190), "Every bid", font=F("Archivo-Bold.ttf", 100), fill="#F2F5F8")
    d.text((72, 300), "in the open", font=F("Archivo-Bold.ttf", 100), fill="#F2F5F8")
    d.text((72, 452), "Draft, bid and build a basketball team.", font=F("Barlow-Regular.ttf", 32), fill="#C9D1DB")
    d.text((72, 494), "A manager game where nothing is hidden.", font=F("Barlow-Regular.ttf", 32), fill="#C9D1DB")
    ph = Image.open(os.path.join(OUT, "img", f"en-market-{W}.webp")).convert("RGBA"); pw = 380
    ph = ph.resize((pw, round(ph.height * pw / ph.width)), Image.LANCZOS)
    layer = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); layer.alpha_composite(ph, (770, 90))
    mask = np.full((Ht, Wd), 255, dtype=np.uint8)
    for y in range(420, Ht): mask[y, :] = int(255 * max(0, 1 - (y - 420) / 210))
    layer.putalpha(Image.fromarray(np.minimum(np.array(layer.split()[3]), mask)))
    base.alpha_composite(layer); base.convert("RGB").save(os.path.join(OUT, "og.png"), optimize=True)
print("assets en", OUT)
