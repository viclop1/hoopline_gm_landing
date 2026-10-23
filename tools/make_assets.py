#!/usr/bin/env python3
"""Regenera las fuentes, las capturas recortadas y (opcionalmente) la imagen para redes de dist/assets.

Solo hace falta si cambian las capturas de la App Store o la tipografía; el día a día es `python3 build.py`.
Requiere Pillow y fontTools:  pip install pillow fonttools

Uso:
  python3 tools/make_assets.py --shots "<carpeta 'para App Store'>" [--fonts <carpeta con los TTF de la app>] [--og]

La carpeta de capturas es la de la tienda de la 1.0.6: en/ es/ de/ fr/ con 01.png … 10.png (compuestos de 1320x2868; el mapa pantalla → número está en NUM).

Tipografía: la de la app (Archivo y Barlow, licencia OFL), desde ../hoopline_gm/fonts. Se sirven como subconjunto latino en woff2 (solo con --with-fonts; hace falta el módulo brotli: pip install brotli).
Capturas: 800 px de ancho (nítidas a 2x hasta ≈ 400 px), con el nombre `<idioma>-<pantalla>-800-<TAG>.webp`. El sufijo importa:
/assets/* se sirve con caché inmutable, así que un juego nuevo de capturas necesita un TAG nuevo.
Recortes (se conserva la parte superior, donde está la información): market 72 %, box y table 76 %; el resto, completas.
"""
import argparse, os, sys
from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--shots", required=True)
ap.add_argument("--fonts", default=os.path.join(HERE, "..", "..", "hoopline_gm", "fonts"))
ap.add_argument("--out", default=os.path.join(HERE, "..", "dist", "assets"))
ap.add_argument("--with-fonts", action="store_true", help="regenera las fuentes (por defecto no se tocan)")
ap.add_argument("--og", action="store_true", help="regenera también las imágenes para redes og-<idioma>-v2.png (por defecto no se tocan)")
a = ap.parse_args()
OUT = os.path.abspath(a.out)
os.makedirs(os.path.join(OUT, "fonts"), exist_ok=True)
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)

# --- fuentes: subconjunto latino, formato woff2 (solo con --with-fonts)
FONTS = {"Archivo-Bold.ttf": "archivo-700", "Archivo-SemiBold.ttf": "archivo-600", "Barlow-Regular.ttf": "barlow-400", "Barlow-SemiBold.ttf": "barlow-600"}
UNI = list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + [0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2026, 0x20AC, 0x2192, 0x2190, 0x2212, 0x2713, 0xD7, 0x192]
for src, name in (FONTS.items() if a.with_fonts else ()):
    o = subset.Options(); o.flavor = "woff2"; o.layout_features = ["*"]; o.name_IDs = [1, 2, 3, 4, 6]; o.notdef_outline = True
    f = TTFont(os.path.join(a.fonts, src)); s = subset.Subsetter(o); s.populate(unicodes=UNI); s.subset(f)
    f.flavor = "woff2"; f.save(os.path.join(OUT, "fonts", name + ".woff2"))

# --- capturas: recorte al móvil con esquinas redondeadas y transparencia
# Capturas de tienda de la 1.0.6 (Tienda/iOS/<idioma>/NN.png, 1320x2868, las 10 en los 4 idiomas): 01 mercado, 02 inicio, 03 equipo,
# 04 pizarra, 05 partido, 06 playoffs, 07 duelos, 08 copas, 09 clasificación, 10 informe de temporada.
NUM = {"market": 1, "team": 3, "board": 4, "box": 5, "playoffs": 6, "duels": 7, "cups": 8, "table": 9}
LANGS = ("en", "es", "de", "fr")
BOX, R, W = (130, 640, 1192, 2782), 130, 800        # el móvil dentro del compuesto (con su borde de 4 px)
TAG = "v106"                                        # cambia con cada juego de capturas: la caché de /assets es inmutable
KEEP = {"market": 0.72, "box": 0.76, "table": 0.76}   # parte superior que se conserva (el resto lo tapa el degradado de la web)

for lang in LANGS:
    for k, n in NUM.items():
        im = Image.open(os.path.join(a.shots, lang, f"{n:02d}.png")).convert("RGB").crop(BOX)
        mask = Image.new("L", (im.width * 2, im.height * 2), 0)
        ImageDraw.Draw(mask).rounded_rectangle((2, 2, im.width * 2 - 3, im.height * 2 - 3), radius=R * 2, fill=255)
        im.putalpha(mask.resize(im.size, Image.LANCZOS))
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        keep = KEEP.get(k, 1.0)
        if keep < 1.0:
            im = im.crop((0, 0, im.width, round(im.height * keep)))
        im.save(os.path.join(OUT, "img", f"{lang}-{k}-{W}-{TAG}.webp"), quality=78, method=6)

# --- imagen para redes (1200x630, una por idioma): solo con --og. Mismo escenario que la web: fondo ink, luz violeta, titular Archivo, móvil con degradado.
OG_TAG = "v2"
OG = {  # (titular en dos líneas, texto en dos líneas)
    "en": (("Every bid", "in the open"), ("Draft, bid and build a basketball team.", "A manager game where nothing is hidden.")),
    "es": (("Cada puja,", "a la vista"), ("Draftea, puja y arma tu equipo de baloncesto.", "Un mánager sin trampas ocultas.")),
    "de": (("Jedes Gebot", "offen"), ("Drafte, biete, bau dein Basketballteam.", "Manager-Spiel ohne versteckte Regeln.")),
    "fr": (("Chaque enchère,", "à découvert"), ("Draftez, enchérissez, bâtissez votre équipe", "de basket. Un manager transparent.")),
}
if a.og:
    Wd, Ht, MAXW = 1200, 630, 640
    F = lambda n, s: ImageFont.truetype(os.path.join(a.fonts, n), s)
    def fit(d, text, font, size, maxw):
        while d.textlength(text, font=F(font, size)) > maxw and size > 20: size -= 2
        return F(font, size)
    for lang, (h, lead) in OG.items():
        base = Image.new("RGBA", (Wd, Ht), "#0D1014"); d = ImageDraw.Draw(base)
        glow = Image.new("L", (Wd, Ht), 0); gd = ImageDraw.Draw(glow); gd.ellipse((700, 20, 1260, 620), fill=70)
        glow = glow.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(90))
        base.paste(Image.new("RGBA", (Wd, Ht), "#8B7BFF"), (0, 0), glow)
        d = ImageDraw.Draw(base)
        d.text((72, 64), "Hoopline GM", font=F("Archivo-Bold.ttf", 34), fill="#F2F5F8")
        hs = min(fit(d, t, "Archivo-Bold.ttf", 100, MAXW).size for t in h)
        d.text((72, 190), h[0], font=F("Archivo-Bold.ttf", hs), fill="#F2F5F8")
        d.text((72, 190 + round(hs * 1.1)), h[1], font=F("Archivo-Bold.ttf", hs), fill="#F2F5F8")
        ls = min(fit(d, t, "Barlow-Regular.ttf", 32, MAXW).size for t in lead)
        d.text((72, 452), lead[0], font=F("Barlow-Regular.ttf", ls), fill="#C9D1DB")
        d.text((72, 452 + round(ls * 1.3)), lead[1], font=F("Barlow-Regular.ttf", ls), fill="#C9D1DB")
        ph = Image.open(os.path.join(OUT, "img", f"{lang}-market-{W}-{TAG}.webp")).convert("RGBA"); pw = 380
        ph = ph.resize((pw, round(ph.height * pw / ph.width)), Image.LANCZOS)
        layer = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); layer.alpha_composite(ph, (770, 90))
        mask = np.full((Ht, Wd), 255, dtype=np.uint8)
        for y in range(420, Ht): mask[y, :] = int(255 * max(0, 1 - (y - 420) / 210))
        layer.putalpha(Image.fromarray(np.minimum(np.array(layer.split()[3]), mask)))
        base.alpha_composite(layer); base.convert("RGB").save(os.path.join(OUT, f"og-{lang}-{OG_TAG}.png"), optimize=True)
print("assets en", OUT)
