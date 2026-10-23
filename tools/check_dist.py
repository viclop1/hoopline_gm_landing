#!/usr/bin/env python3
"""Comprueba dist/ antes de subirlo: enlaces y recursos locales, imágenes con tamaño y alt, CSP, hoja de estilos versionada,
fuentes precargadas y que las cuatro portadas tengan la misma estructura. Solo biblioteca estándar.

Uso:  python3 tools/check_dist.py      (sale con código 1 si hay errores)
"""
import hashlib, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dist"))
errors, warnings = [], []
def err(m): errors.append(m)

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.refs = []; s.imgs = []; s.inline = []; s.text = []; s.skip = 0; s.preload = []; s.css = []; s.ids = set(); s.hrefs = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs)
        if "id" in a: s.ids.add(a["id"])
        if tag == "img": s.imgs.append(a); s.refs.append(a.get("src"))
        if tag == "script":
            if a.get("src"): s.refs.append(a["src"])
            else:
                s.skip += 1
                if a.get("type") != "application/ld+json": s.inline.append("script")  # los datos estructurados no se ejecutan
        if tag == "style": s.inline.append("style"); s.skip += 1
        if tag == "link":
            if a.get("rel") == "preload": s.preload.append(a)
            if a.get("rel") == "stylesheet": s.css.append(a.get("href"))
            if a.get("href"): s.refs.append(a["href"])
        if tag == "a" and a.get("href"): s.hrefs.append(a["href"])
        if "style" in a: s.inline.append("atributo style")
        if any(k.startswith("on") for k in a): s.inline.append("manejador on*")
    def handle_endtag(s, tag):
        if tag in ("script", "style") and s.skip: s.skip -= 1
    def handle_data(s, d):
        if not s.skip: s.text.append(d)

def local(path, page_dir):
    path = path.split("#")[0].split("?")[0]
    if not path: return None
    if path.startswith("/"): p = os.path.join(ROOT, path.lstrip("/"))
    else: p = os.path.join(page_dir, path)
    if os.path.isdir(p): p = os.path.join(p, "index.html")
    return p

pages = []
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".html"): pages.append(os.path.join(dp, f))
css_path = os.path.join(ROOT, "assets", "style.css")
css = open(css_path, encoding="utf-8").read()
css_ver = hashlib.md5(open(css_path, "rb").read()).hexdigest()[:8]

for fn in re.findall(r'url\("(/assets/[^"]+)"\)', css):
    if not os.path.exists(os.path.join(ROOT, fn.lstrip("/"))): err(f"style.css: falta {fn}")

structure = {}
for pg in sorted(pages):
    rel = os.path.relpath(pg, ROOT); d = os.path.dirname(pg)
    p = P(); p.feed(open(pg, encoding="utf-8").read())
    for r in p.refs + p.hrefs:
        if not r or re.match(r"[a-z][a-z0-9+.-]*:", r) or r.startswith("#"): continue
        t = local(r, d)
        if t and not os.path.exists(t): err(f"{rel}: enlace o recurso roto {r}")
    for h in p.hrefs:
        if h.startswith("#") and h[1:] not in p.ids: err(f"{rel}: ancla {h} sin destino")
    if p.inline: err(f"{rel}: {sorted(set(p.inline))} en línea (el CSP lo bloquea)")
    for im in p.imgs:
        if "alt" not in im: err(f"{rel}: <img {im.get('src')}> sin alt")
        if not (im.get("width") and im.get("height")): err(f"{rel}: <img {im.get('src')}> sin width/height (provoca saltos de maquetación)")
    for c in p.css:
        if c.startswith("/assets/style.css"):
            if "v=" + css_ver not in c: err(f"{rel}: style.css con versión {c} (debería ser ?v={css_ver})")
    for a in p.preload:
        t = local(a.get("href", ""), d)
        if not t or not os.path.exists(t): err(f"{rel}: preload roto {a.get('href')}")
    text = " ".join("".join(p.text).split())
    if re.search(r"\bNBA\b", text) and not rel.startswith("legal") and "/legal/" not in rel:
        err(f"{rel}: aparece «NBA» en el texto visible")
    if rel in ("index.html", "es/index.html", "de/index.html", "fr/index.html"):
        structure[rel] = (len(p.imgs), [os.path.basename(i["src"]).split("-", 1)[1] for i in p.imgs])
if len(structure) == 4:
    ref = next(iter(structure.values()))
    for k, v in structure.items():
        if v != ref: err(f"{k}: las imágenes no coinciden con las de la portada en inglés ({v} frente a {ref})")

# recursos sin usar en dist/assets/img y fuentes
used = set()
for pg in pages:
    used |= set(re.findall(r'/assets/[^"\')\s]+', open(pg, encoding="utf-8").read()))
used |= set(re.findall(r'/assets/[^"\')\s]+', css))
for sub in ("img", "fonts"):
    for f in os.listdir(os.path.join(ROOT, "assets", sub)):
        if f"/assets/{sub}/{f}" not in used and not f.startswith(("og", "app-icon")):
            warnings.append(f"sin usar: assets/{sub}/{f}")

# _headers: la CSP debe seguir en 'self'
h = open(os.path.join(ROOT, "_headers"), encoding="utf-8").read()
if "unsafe-inline" in h or "unsafe-eval" in h: err("_headers: la CSP admite unsafe-inline/eval")

tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(os.path.join(ROOT, "assets")) for f in fs)
for w in warnings: print("aviso:", w)
for e_ in errors: print("ERROR:", e_)
print(f"{len(pages)} páginas, assets {tot // 1024} KB, hoja de estilos ?v={css_ver}: {'ERRORES: ' + str(len(errors)) if errors else 'todo en orden'}")
sys.exit(1 if errors else 0)
