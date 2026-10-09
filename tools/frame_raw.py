#!/usr/bin/env python3
"""Mete una captura 'cruda' (1206x2622, build de depuración) en el marco de móvil de las capturas de la App Store.

Uso: python3 frame_raw.py <captura_cruda.png> <captura_App_Store_de_referencia.png> <salida.webp>
La referencia aporta el marco, la isla y la barra de estado limpia (9:41); la captura cruda aporta la pantalla.
"""
import sys
from PIL import Image, ImageDraw
BOX, R, W = (134, 553, 1158, 2716), 128, 560
SX, SY, SW, SH = 28, 28, 968, 2107   # pantalla dentro del recorte del móvil
STRIP = 162                          # filas superiores (barra de estado) que se toman de la referencia
SR = 95                              # radio de las esquinas de la pantalla (medido en la referencia)

raw, ref, out = sys.argv[1:4]
T = Image.open(ref).convert("RGB").crop(BOX)
S = Image.open(raw).convert("RGB").resize((SW, SH), Image.LANCZOS)
S.paste(T.crop((SX, SY, SX + SW, SY + STRIP)), (0, 0))        # barra de estado limpia, sin la cinta DEBUG
m = Image.new("L", (SW * 4, SH * 4), 0)
ImageDraw.Draw(m).rounded_rectangle((4, 4, SW * 4 - 5, SH * 4 - 5), radius=SR * 4, fill=255)
m = m.resize((SW, SH), Image.LANCZOS)
T.paste(S, (SX, SY), m)
mask = Image.new("L", (T.width * 2, T.height * 2), 0)
ImageDraw.Draw(mask).rounded_rectangle((2, 2, T.width * 2 - 3, T.height * 2 - 3), radius=R * 2, fill=255)
T = T.convert("RGBA"); T.putalpha(mask.resize(T.size, Image.LANCZOS))
T = T.resize((W, round(T.height * W / T.width)), Image.LANCZOS)
T.save(out, quality=84, method=6); print(out, T.size)
