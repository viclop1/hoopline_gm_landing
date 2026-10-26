# Hoopline GM website

Source of the website for **Hoopline GM**, a free basketball manager game for iOS: draft, bid in a live auction market and build a team. The site is a static landing page in four languages (English, Spanish, German, French), with legal notice pages and the page that confirms account emails.

- Website: [hooplinegm.com](https://hooplinegm.com)
- App Store: [apps.apple.com/app/id6809042395](https://apps.apple.com/app/id6809042395)

The Hoopline GM app source code is private.

## Stack

- Plain HTML and CSS, with one small script for the account confirmation page. No front-end framework and no runtime dependencies.
- `build.py` generates the pages. It uses only the Python standard library (Python 3).
- `tools/` contains optional helpers for images and checks. `make_assets.py` and `make_icons.py` need extra Python packages and are only run when the screenshots or icons change.

## Run locally

```sh
python3 build.py              # regenerates the pages in dist/
python3 tools/check_dist.py   # validates links, resources, image sizes, CSP and more
cd dist && python3 -m http.server 8000
```

Then open http://localhost:8000. The `_headers` file is a Cloudflare feature and is not applied by the local server.

Text, links and configuration live in the `CONFIG` and `COPY` sections of `build.py`. Styles are in `dist/assets/style.css`.

## Project structure

```
build.py            generates the pages, sitemap, robots.txt and _headers into dist/
legalnotice.py      legal notice texts in four languages, used by build.py
dist/               what gets published (committed)
  index.html          English home page (es/, de/, fr/ hold the other languages)
  <lang>/legal/       legal notice pages
  auth/confirm/       account email confirmation page
  assets/             style.css, confirm.js, fonts (woff2), images (WebP, SVG), hero clips, social images
  _headers            security and caching headers
  404.html, robots.txt, sitemap.xml, icons
emails/             HTML templates for the authentication emails (four languages per email) and their generator
tools/              make_assets.py, make_icons.py, check_dist.py
```

## Design and front-end notes

- On wide screens with scroll-driven animation support, the feature section is a sticky phone whose screen changes as the user scrolls. On narrow screens the same content is a horizontal scroll-snap carousel. Without support, or with reduced motion, it falls back to a plain layout.
- Animations respect `prefers-reduced-motion`.
- Images are WebP with explicit width and height. Fonts are self-hosted woff2.
- The hero can show a short muted looping clip per language (`dist/assets/video/<lang>-hero-v1.mp4`) over the still image.

## Deployment

The contents of `dist/` are served as static assets on Cloudflare. `dist/` is committed and a push to the repository deploys automatically, so what is in the repository is what is published; there is no build step on the server. Security headers and caching are configured in `dist/_headers`, which `build.py` writes.

Assets under `/assets/` are cached for a year as immutable, so a changed image, clip or social image gets a new file name, and the stylesheet link carries a content hash.

## SEO and special pages

- Each page has a canonical URL, `hreflang` alternates (including `x-default`), Open Graph and Twitter tags, and a per-language social image.
- The home pages include JSON-LD structured data (`MobileApplication`).
- `sitemap.xml` lists the public pages. `robots.txt` disallows `/auth/`.
- `/auth/confirm` is the page that account emails link to. It reads a one-time token from the link, removes it from the address bar and only confirms after the user presses a button, so email scanners that open links do not consume it. After a sign-up or email change it offers to open the app; for password recovery it shows a form to choose a new password. The page is `noindex`, served with `no-store` and `no-referrer`.
- `404.html` is also `noindex`.

## Security

- Content Security Policy that restricts scripts, styles, images and fonts to the site itself, plus `nosniff`, a restrictive `Permissions-Policy` and `frame-ancestors 'none'`. The only external connection allowed is the authentication service used by the confirmation page.
- No inline scripts or styles; `tools/check_dist.py` enforces this.

All rights reserved.
