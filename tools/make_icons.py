#!/usr/bin/env python3
"""Genera los iconos de la web (favicon.ico, favicon-32.png, icon-192.png, apple-touch-icon.png) desde tools/app-icon-1024.png.

Uso:  python3 tools/make_icons.py        (requiere Pillow)
Para cambiar el icono: sustituye tools/app-icon-1024.png por el nuevo (1024x1024) y vuelve a ejecutarlo.
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "dist")
src = Image.open(os.path.join(HERE, "app-icon-1024.png")).convert("RGB")

def rounded(size, radius_ratio=0.22):
    im = src.resize((size, size), Image.LANCZOS).convert("RGBA")
    s = 4
    mask = Image.new("L", (size * s, size * s), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size * s - 1, size * s - 1), radius=int(size * s * radius_ratio), fill=255)
    im.putalpha(mask.resize((size, size), Image.LANCZOS))
    return im

rounded(32).save(os.path.join(OUT, "favicon-32.png"), optimize=True)
rounded(192).save(os.path.join(OUT, "icon-192.png"), optimize=True)
# iOS aplica sus propias esquinas: cuadrado y opaco
src.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
rounded(48).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("iconos ok")
