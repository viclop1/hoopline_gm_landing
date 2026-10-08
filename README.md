# hoopline_gm_landing

Web de [hooplinegm.com](https://hooplinegm.com): landing de Hoopline GM en cuatro idiomas (EN, ES, DE, FR), página de confirmación de correo
(`/auth/confirm`) y plantillas de correo de Supabase. HTML y CSS estáticos, **sin dependencias**.

## Estructura
```
build.py              genera las páginas HTML en dist/ (Python estándar, sin instalar nada)
dist/                 lo que se publica (se sube tal cual a Cloudflare)
  assets/style.css      estilos (a mano)
  assets/confirm.js     lógica de /auth/confirm (a mano; la genera build.py con la URL y la clave de Supabase)
  assets/fonts, img     fuentes Inter y capturas recortadas (las genera tools/make_assets.py)
  _headers              cabeceras de seguridad de Cloudflare
emails/               plantillas de correo de Supabase (enlace-supabase / enlace-propio) y su generador
tools/make_assets.py  regenera fuentes, capturas y la imagen para redes (solo si cambian las capturas)
```

## Día a día
1. Edita textos, enlaces o configuración en `build.py` (secciones CONFIG y COPY) o los estilos en `dist/assets/style.css`.
2. `python3 build.py`
3. Para verlo en local: `cd dist && python3 -m http.server 8000` y abre http://localhost:8000
4. Publica el contenido de `dist/` (ver abajo).

`build.py` reescribe los `index.html`, `404.html`, `auth/confirm/index.html`, `assets/confirm.js`, `robots.txt`, `sitemap.xml`, `_headers`.
No toca `assets/style.css`, `fonts` ni `img`.

## Publicación (Cloudflare, proyecto `hooplinegm`)
- **Ahora:** subida manual del contenido de `dist/` (Assets directory `/`, HTML handling `auto-trailing-slash`, Not found handling `404-page`).
  Dominio en Settings → Domains & Routes.
- **Despliegue automático desde este repo (opcional):** conectar el repo en el proyecto de Cloudflare, sin comando de build y con `dist` como
  carpeta de assets. Como `dist/` va en el repo, cada `git push` publicaría. Hazlo solo si quieres ese flujo.

## /auth/confirm
Confirma con `POST {SUPABASE_URL}/auth/v1/verify` (`token_hash` y `type`) con la clave pública, sin librerías. Registro y cambio de correo: confirma y
ofrece abrir la app (`com.hooplinegm.app://login-callback/`, solo en móvil). Recuperar contraseña: formulario en la propia web (`PUT /auth/v1/user`).
Hay que pulsar un botón antes de confirmar (los escáneres de correo no gastan el enlace) y el token se quita de la barra de direcciones.
La clave `sb_publishable_…` es pública por diseño; **nunca** pongas aquí la secret ni la `service_role`.
Site URL y Redirect URLs de Supabase no cambian (`com.hooplinegm.app://login-callback/`).

## Correos de Supabase
`python3 emails/build_emails.py emails` regenera `emails/enlace-supabase/` y `emails/enlace-propio/` (más `subjects.json`). Detalle y dónde pegar cada una en `emails/LEEME.md`.
Con `enlace-propio` el botón va a `https://hooplinegm.com/auth/confirm?token_hash=…&type=…`.

## Reglas de contenido (abogado)
Sin "NBA", sin logos ni nombres de franquicias, sin jugadores reales como reclamo, capturas solo de pantallas funcionales, y el aviso de independencia
en el pie. Los textos salen de `aso-listing.md` (Project APP NBA) y están revisados; los textos nuevos en FR y DE son de Claude y no los ha revisado una persona nativa.

## Pendiente
- Soporte: el pie enlaza a `mailto:hooplinegm@gmail.com`; confirmar si debe haber una página de soporte (`LEGAL["support"]` y `help_a` en `build.py`).
- Aviso legal / Impressum: consultarlo con el abogado (hay versión en alemán).
- ~~Favicon~~ hecho: icono de la app. Para cambiarlo, sustituye `tools/app-icon-1024.png` y ejecuta `python3 tools/make_icons.py`.
- Los textos y capturas son de la 1.0.1: comprobar que está aprobada en App Store.
