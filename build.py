#!/usr/bin/env python3
"""Genera la landing de Hoopline GM (HTML/CSS estáticos, sin dependencias).

Uso:  python3 build.py
Salida: dist/   (se sube tal cual a Cloudflare Pages)

Para cambiar enlaces, URLs o textos, edita la sección CONFIG y COPY y vuelve a ejecutar.
"""
import html, os, json

# ----------------------------------------------------------------- CONFIG
SITE = "https://hooplinegm.com"
APP_STORE = "https://apps.apple.com/app/id6809042395"
APP_STORE_ID = "6809042395"
SUPABASE_URL = "https://qllwdtrmzlisyfaznoml.supabase.co"
SUPABASE_KEY = "sb_publishable_rIDDRy1qk65YFKYj_moGHA_Coha3u2C"  # clave pública, apta para el navegador
OPEN_APP_URL = "com.hooplinegm.app://login-callback/"

# Páginas legales publicadas en GitHub Pages (repo hoopline-gm-legal).
# La política de privacidad es la portada del repo; las condiciones, /terms.html.
# Soporte: de momento, el correo de contacto de las páginas legales (cámbialo si hay una página de soporte).
LEGAL_BASE = "https://viclop1.github.io/hoopline-gm-legal"
LEGAL = {
    "privacy": LEGAL_BASE + "/",
    "terms": LEGAL_BASE + "/terms.html",
    "support": LEGAL_BASE + "/support.html",
}

from legalnotice import LN, OWNER

LANGS = ["en", "es", "de", "fr"]
PATH = {"en": "/", "es": "/es/", "de": "/de/", "fr": "/fr/"}
NAME = {"en": "English", "es": "Español", "de": "Deutsch", "fr": "Français"}
OG_LOCALE = {"en": "en_US", "es": "es_ES", "de": "de_DE", "fr": "fr_FR"}

# ----------------------------------------------------------------- COPY
COPY = {
"en": dict(
    title="Hoopline GM – Basketball Manager & Draft",
    desc="Draft, bid and build a basketball team. A manager game where nothing is hidden.",
    h1="Every bid in the open",
    lead="Draft, bid and build a basketball team. A manager game where nothing is hidden.",
    store="Download on the App Store",
    android="The Android version is in testing.",
    open_title="Run a basketball club the way you would want the market to work: in the open.",
    pillars=[
        ("Every bid is public", "Bid in a live auction market where rivals bid back."),
        ("Every rule is written down", "Twelve teams, a fifteen-round snake draft and a salary cap you cannot talk your way around."),
        ("Every rating comes from real games", "Watch ratings move as the real season moves."),
    ],
    do_h="What you do",
    do=[
        "Draft fifteen players over a snake order you can see coming",
        "Bid in a live auction market where rivals bid back",
        "Finish in the top ten and play for the title: a play-in, then best-of-seven series to the Finals",
        "Search any player, star the ones you follow and get a notification when one goes up for auction",
        "Finish with a season report: your place, your best player, your badges",
    ],
    fair_h="Nothing on sale makes your five better",
    fair_p="Gems buy time and appearance: a refill of the energy meter, a jersey, a court, the name over the arena. Coins pay the salary cap, and coins cannot be bought with money. That is the whole point.",
    prem_h="Premium",
    prem_p="An optional monthly subscription raises the energy limit, so one sitting goes further, keeps up to three named tactics boards to switch between in one tap, and gives you the assistant’s suggestion for every game. It changes nothing about how good your squad can be.",
    feats=[
        ('board', 'Your tactics board, before every game', 'Style, defence, pace and who to feed, with your odds moving as you choose.', 'The tactics board with attacking style, defence, pace and focus player options'),
        ("team", "Your five, your call", "Set the court, rest tired starters or let Auto do it.", "The team screen with the starting five on the court and the bench below"),
        ('cups', 'Then take them into a cup', 'A ladder of cups against fictional clubs, from Bronze to Gold.', 'The cups screen with Bronze, Silver and Gold cups'),
    ],
    shots_h="Inside the app",
    shots=[
        ("box", "A box score for every game", "Points, rebounds and assists for everyone who played.", "The box score of a game with both teams’ players"),
        ("table", "Twelve teams. One title.", "22 league games, then the playoffs.", "The league standings with twelve teams"),
    ],
    market_alt="The market screen with live auctions, current bids and time left",
    faq_h="Questions",
    faq=[
        ("Is it free?", "Yes, you can play without paying. Optional purchases cover time and appearance, and none of them makes your squad better."),
        ("Which devices does it run on?", "On iPhone now. The Android version is in testing."),
        ("Is it connected to a real league?", "No. Hoopline GM is an independent game. All teams, arenas and competitions are fictional, and real players appear by name with publicly available statistics."),
    ],
    help_q="Need help?", help_a="Write to us by email",
    cta_h="Start your first draft",
    legal_links=("Privacy policy", "Terms of use", "Support"),
    notice="Hoopline GM is an independent basketball management game. It is not affiliated with, endorsed, sponsored or licensed by any professional basketball league, team, players’ association or player. Real players are referenced by name together with publicly available statistics as part of the game’s sports-related content and simulation mechanics. These references do not imply any endorsement, sponsorship, authorisation or affiliation. Statistics are not official league data. All teams, arenas and competitions in the game are fictional.",
    lang_label="Language",
    home_label="Hoopline GM, home",
),
"es": dict(
    title="Hoopline GM – Mánager de baloncesto y draft",
    desc="Draftea, puja y arma tu equipo de baloncesto. Un mánager sin trampas ocultas.",
    h1="Cada puja, a la vista",
    lead="Draftea, puja y arma tu equipo de baloncesto. Un mánager sin trampas ocultas.",
    store="Descargar en la App Store",
    android="La versión de Android está en pruebas.",
    open_title="Dirige un club de baloncesto con un mercado como debería ser: a la vista.",
    pillars=[
        ("Cada puja es pública", "Puja en un mercado de subastas en directo donde los rivales responden."),
        ("Cada regla está escrita", "Doce equipos, un draft en serpiente de quince rondas y un tope salarial que no se negocia."),
        ("Cada valoración sale de partidos reales", "Mira cómo cambian las valoraciones al ritmo de la temporada real."),
    ],
    do_h="Qué haces",
    do=[
        "Draftea quince jugadores con un orden en serpiente que ves venir",
        "Puja en un mercado de subastas en directo donde los rivales responden",
        "Acaba entre los diez primeros y juega por el título: play-in y series al mejor de siete hasta la final",
        "Busca cualquier jugador, marca con estrella a los que sigues y recibe un aviso cuando uno salga a subasta",
        "Cierra con el informe de temporada: tu puesto, tu mejor jugador, tus logros",
    ],
    fair_h="Nada de lo que se vende mejora tu quinteto",
    fair_p="Las gemas compran tiempo y aspecto: recargar la energía, una equipación, una pista, el nombre del pabellón. Las monedas pagan el tope salarial y no se compran con dinero. De eso se trata.",
    prem_h="Premium",
    prem_p="Una suscripción mensual opcional amplía el límite de energía para que cada sesión dé más de sí, guarda hasta tres pizarras tácticas con nombre para cambiar de una a otra de un toque y te da la sugerencia del ayudante en cada partido. No cambia en nada lo bueno que puede llegar a ser tu equipo.",
    feats=[
        ('board', 'Tu pizarra táctica, antes de cada partido', 'Estilo, defensa, ritmo y a quién buscar, con tus probabilidades moviéndose según eliges.', 'La pizarra táctica con estilo de ataque, defensa, ritmo y jugador clave'),
        ("team", "Tu quinteto, tu decisión", "Monta la pista, da descanso a los cansados o deja que lo haga Auto.", "La pantalla de equipo con el quinteto en la pista y el banquillo debajo"),
        ('cups', 'Después, a por una copa', 'Una escalera de copas contra clubes ficticios, de Bronce a Oro.', 'La pantalla de copas con copas de Bronce, Plata y Oro'),
    ],
    shots_h="Dentro de la app",
    shots=[
        ("box", "La estadística de cada partido", "Puntos, rebotes y asistencias de todos los que jugaron.", "La estadística de un partido con los jugadores de los dos equipos"),
        ("table", "Doce equipos. Un título.", "22 partidos de liga y, después, los playoffs.", "La clasificación de la liga con doce equipos"),
    ],
    market_alt="La pantalla del mercado con subastas en directo, pujas actuales y tiempo restante",
    faq_h="Preguntas",
    faq=[
        ("¿Es gratis?", "Sí, puedes jugar sin pagar. Las compras opcionales son de tiempo y aspecto, y ninguna mejora a tu equipo."),
        ("¿En qué dispositivos funciona?", "En iPhone ya. La versión de Android está en pruebas."),
        ("¿Está conectado a una liga real?", "No. Hoopline GM es un juego independiente. Todos los equipos, pabellones y competiciones son ficticios, y los jugadores reales aparecen por su nombre con estadísticas públicas."),
    ],
    help_q="¿Necesitas ayuda?", help_a="Escríbenos por correo",
    cta_h="Empieza tu primer draft",
    legal_links=("Política de privacidad", "Condiciones de uso", "Soporte"),
    notice="Hoopline GM es un juego independiente de gestión de baloncesto. No está afiliado, respaldado, patrocinado ni licenciado por ninguna liga, equipo, asociación de jugadores ni jugador de baloncesto profesional. Los jugadores reales se mencionan por su nombre junto con estadísticas públicas como parte del contenido deportivo del juego y de sus mecánicas de simulación. Estas menciones no implican respaldo, patrocinio, autorización ni afiliación alguna. Las estadísticas no son datos oficiales de ninguna liga. Todos los equipos, pabellones y competiciones del juego son ficticios.",
    lang_label="Idioma",
    home_label="Hoopline GM, inicio",
),
"de": dict(
    title="Hoopline GM – Basketball-Manager mit Draft",
    desc="Drafte, biete, bau dein Basketballteam. Manager-Spiel ohne versteckte Regeln.",
    h1="Jedes Gebot offen",
    lead="Drafte, biete, bau dein Basketballteam. Manager-Spiel ohne versteckte Regeln.",
    store="Laden im App Store",
    android="Die Android-Version ist in der Testphase.",
    open_title="Führe einen Basketballclub mit einem Markt, wie er sein sollte: offen.",
    pillars=[
        ("Jedes Gebot ist öffentlich", "Biete auf einem Live-Auktionsmarkt, auf dem die Rivalen mitbieten."),
        ("Jede Regel steht geschrieben", "Zwölf Teams, ein Snake-Draft über fünfzehn Runden und ein Gehaltslimit, das sich nicht verhandeln lässt."),
        ("Jede Wertung kommt aus echten Spielen", "Sieh zu, wie sich die Wertungen mit der echten Saison bewegen."),
    ],
    do_h="Was du machst",
    do=[
        "Drafte fünfzehn Spieler in einer Snake-Reihenfolge, die du kommen siehst",
        "Biete auf einem Live-Auktionsmarkt, auf dem die Rivalen mitbieten",
        "Schaff es unter die ersten zehn und spiel um den Titel: Play-in, dann Best-of-Seven-Serien bis zu den Finals",
        "Such jeden Spieler, markier die, denen du folgst, und werde benachrichtigt, wenn einer versteigert wird",
        "Zum Schluss der Saisonbericht: dein Platz, dein bester Spieler, deine Erfolge",
    ],
    fair_h="Nichts, was man kaufen kann, macht deine Fünf besser",
    fair_p="Gems kaufen Zeit und Aussehen: eine Energie-Aufladung, ein Trikot, ein Spielfeld, den Namen der Halle. Münzen bezahlen das Gehaltslimit und lassen sich nicht mit Geld kaufen. Genau darum geht es.",
    prem_h="Premium",
    prem_p="Ein optionales Monatsabo erhöht das Energielimit, damit eine Sitzung länger reicht, speichert bis zu drei Taktiktafeln mit Namen, zwischen denen du mit einem Tipp wechselst, und gibt dir den Vorschlag des Assistenten für jedes Spiel. An der Stärke deines Kaders ändert es nichts.",
    feats=[
        ('board', 'Deine Taktiktafel, vor jedem Spiel', 'Stil, Verteidigung, Tempo und wen du suchst, und deine Chancen bewegen sich mit jeder Wahl.', 'Die Taktiktafel mit Angriffsstil, Verteidigung, Tempo und Schlüsselspieler'),
        ("team", "Deine Fünf, deine Wahl", "Stell das Feld auf, gib den Müden Pause oder überlass es Auto.", "Der Team-Bildschirm mit der Startfünf auf dem Feld und der Bank darunter"),
        ('cups', 'Dann ab in den Pokal', 'Eine Leiter aus Pokalen gegen fiktive Klubs, von Bronze bis Gold.', 'Der Pokalbildschirm mit Bronze-, Silber- und Gold-Pokalen'),
    ],
    shots_h="In der App",
    shots=[
        ("box", "Ein Boxscore für jedes Spiel", "Punkte, Rebounds und Assists für alle, die gespielt haben.", "Der Boxscore eines Spiels mit den Spielern beider Teams"),
        ("table", "Zwölf Teams. Ein Titel.", "22 Ligaspiele, danach die Playoffs.", "Die Ligatabelle mit zwölf Teams"),
    ],
    market_alt="Der Marktbildschirm mit Live-Auktionen, aktuellen Geboten und Restzeit",
    faq_h="Fragen",
    faq=[
        ("Ist es kostenlos?", "Ja, du kannst ohne Bezahlung spielen. Optionale Käufe betreffen Zeit und Aussehen, und keiner macht dein Team besser."),
        ("Auf welchen Geräten läuft es?", "Auf dem iPhone. Die Android-Version ist in der Testphase."),
        ("Gehört es zu einer echten Liga?", "Nein. Hoopline GM ist ein unabhängiges Spiel. Alle Teams, Hallen und Wettbewerbe sind erfunden; echte Spieler erscheinen mit Namen und öffentlich verfügbaren Statistiken."),
    ],
    help_q="Brauchst du Hilfe?", help_a="Schreib uns per E-Mail",
    cta_h="Starte deinen ersten Draft",
    legal_links=("Datenschutzerklärung", "Nutzungsbedingungen", "Support"),
    notice="Hoopline GM ist ein unabhängiges Basketball-Managerspiel. Es ist mit keiner professionellen Basketballliga, keinem Team, keiner Spielervereinigung und keinem Spieler verbunden und wird von ihnen weder unterstützt, gesponsert noch lizenziert. Echte Spieler werden mit ihrem Namen und öffentlich verfügbaren Statistiken als Teil der sportlichen Spielinhalte und der Simulationsmechanik genannt. Diese Nennungen bedeuten keine Unterstützung, kein Sponsoring, keine Genehmigung und keine Verbindung. Die Statistiken sind keine offiziellen Ligadaten. Alle Teams, Hallen und Wettbewerbe im Spiel sind erfunden.",
    lang_label="Sprache",
    home_label="Hoopline GM, Startseite",
),
"fr": dict(
    title="Hoopline GM – Manager de basket et draft",
    desc="Draftez, enchérissez, bâtissez votre équipe de basket. Un manager transparent.",
    h1="Chaque enchère, à découvert",
    lead="Draftez, enchérissez, bâtissez votre équipe de basket. Un manager transparent.",
    store="Télécharger dans l’App Store",
    android="La version Android est en cours de test.",
    open_title="Dirigez un club de basket avec un marché comme il devrait être : à découvert.",
    pillars=[
        ("Chaque enchère est publique", "Enchérissez sur un marché en direct où les rivaux surenchérissent."),
        ("Chaque règle est écrite", "Douze équipes, une draft en serpentin de quinze tours et un plafond salarial qui ne se négocie pas."),
        ("Chaque note vient de vrais matchs", "Suivez l’évolution des notes au rythme de la vraie saison."),
    ],
    do_h="Ce que vous faites",
    do=[
        "Draftez quinze joueurs dans un ordre en serpentin que vous voyez venir",
        "Enchérissez sur un marché en direct où les rivaux surenchérissent",
        "Finissez dans les dix premiers et jouez le titre : un play-in, puis des séries au meilleur des sept jusqu’à la finale",
        "Cherchez n’importe quel joueur, suivez-le d’une étoile et soyez prévenu quand il est mis aux enchères",
        "Terminez par le bilan de saison : votre place, votre meilleur joueur, vos succès",
    ],
    fair_h="Rien à vendre ne rend votre cinq meilleur",
    fair_p="Les gemmes achètent du temps et du style : une recharge d’énergie, un maillot, un parquet, le nom de la salle. Les pièces paient le plafond salarial et ne s’achètent pas avec de l’argent. C’est tout le principe.",
    prem_h="Premium",
    prem_p="Un abonnement mensuel facultatif augmente la limite d’énergie pour que chaque session dure plus longtemps, garde jusqu’à trois tableaux tactiques nommés pour passer de l’un à l’autre d’un geste et vous donne la suggestion de l’adjoint à chaque match. Il ne change rien au niveau que votre effectif peut atteindre.",
    feats=[
        ('board', 'Votre tableau tactique, avant chaque match', 'Style, défense, rythme et qui servir, avec vos chances qui bougent selon vos choix.', 'Le tableau tactique avec style d’attaque, défense, rythme et joueur clé'),
        ("team", "Votre cinq, votre choix", "Composez le terrain, reposez les titulaires fatigués ou laissez Auto s’en charger.", "L’écran équipe avec le cinq de départ sur le terrain et le banc en dessous"),
        ('cups', 'Puis direction la coupe', 'Une échelle de coupes contre des clubs fictifs, de Bronze à Or.', 'L’écran des coupes avec les coupes Bronze, Argent et Or'),
    ],
    shots_h="Dans l’app",
    shots=[
        ("box", "La feuille de chaque match", "Points, rebonds et passes de tous ceux qui ont joué.", "La feuille de match avec les joueurs des deux équipes"),
        ("table", "Douze équipes. Un titre.", "22 matchs de championnat, puis les playoffs.", "Le classement de la ligue avec douze équipes"),
    ],
    market_alt="L’écran du marché avec des enchères en direct, les offres actuelles et le temps restant",
    faq_h="Questions",
    faq=[
        ("Est-ce gratuit ?", "Oui, vous pouvez jouer sans payer. Les achats facultatifs portent sur le temps et l’apparence, et aucun ne rend votre équipe meilleure."),
        ("Sur quels appareils ça fonctionne ?", "Sur iPhone dès maintenant. La version Android est en cours de test."),
        ("Est-ce lié à une vraie ligue ?", "Non. Hoopline GM est un jeu indépendant. Toutes les équipes, salles et compétitions sont fictives, et les vrais joueurs apparaissent avec leur nom et des statistiques publiques."),
    ],
    help_q="Besoin d’aide ?", help_a="Écrivez-nous par e-mail",
    cta_h="Lancez votre première draft",
    legal_links=("Politique de confidentialité", "Conditions d’utilisation", "Assistance"),
    notice="Hoopline GM est un jeu indépendant de gestion de basket. Il n’est affilié à aucune ligue, équipe, association de joueurs ni aucun joueur de basket professionnel, et n’est ni approuvé, ni sponsorisé, ni sous licence de leur part. Les vrais joueurs sont cités par leur nom avec des statistiques publiques dans le cadre du contenu sportif du jeu et de ses mécaniques de simulation. Ces mentions n’impliquent aucune approbation, aucun parrainage, aucune autorisation ni aucune affiliation. Les statistiques ne sont pas des données officielles d’une ligue. Toutes les équipes, salles et compétitions du jeu sont fictives.",
    lang_label="Langue",
    home_label="Hoopline GM, accueil",
),
}

# ----------------------------------------------------------------- helpers
e = html.escape
OUT = os.environ.get("HOOPLINE_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

# Aviso legal / Impressum: aprobado por el abogado el 08/10/2026 (contenido en legalnotice.py).
# HOOPLINE_LEGAL_LIVE=0 python3 build.py genera la web sin ellos.
LEGAL_PAGES_LIVE = os.environ.get("HOOPLINE_LEGAL_LIVE", "1") == "1"
LNPATH = {"en": "/legal/", "es": "/es/legal/", "de": "/de/legal/", "fr": "/fr/legal/"}

def w(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def alternates():
    s = ""
    for l in LANGS:
        s += f'<link rel="alternate" hreflang="{l}" href="{SITE}{PATH[l]}">\n'
    s += f'<link rel="alternate" hreflang="x-default" href="{SITE}/">\n'
    return s

def head_common(lang, title, desc, canonical, extra=""):
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0D1014">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/inter-display-800.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="/assets/fonts/inter-400.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/style.css">
{extra}'''

# ----------------------------------------------------------------- landing
def badge(lang, c):
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "assets", "img")
    name = f"app-store-badge-{lang}.png" if os.path.exists(os.path.join(here, f"app-store-badge-{lang}.png")) else "app-store-badge.png"
    return f'<a class="badge" href="{APP_STORE}"><img src="/assets/img/{name}" width="175" height="52" alt="{e(c["store"])}"></a>'


def landing(lang):
    c = COPY[lang]
    canonical = SITE + PATH[lang]
    ld = {
        "@context": "https://schema.org", "@type": "MobileApplication", "name": "Hoopline GM",
        "operatingSystem": "iOS", "applicationCategory": "GameApplication",
        "description": c["desc"], "url": canonical, "downloadUrl": APP_STORE, "inLanguage": lang,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
    }
    extra = f'''<link rel="canonical" href="{canonical}">
{alternates()}<meta name="apple-itunes-app" content="app-id={APP_STORE_ID}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Hoopline GM">
<meta property="og:title" content="{e(c["title"])}">
<meta property="og:description" content="{e(c["desc"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
'''
    switch = ""
    for l in LANGS:
        cur = ' aria-current="page"' if l == lang else ""
        switch += f'<a href="{PATH[l]}" hreflang="{l}" lang="{l}"{cur} aria-label="{NAME[l]}">{l.upper()}</a>'
    pillars = "".join(f'<li><h3>{e(t)}</h3><p>{e(p)}</p></li>' for t, p in c["pillars"])
    do = "".join(f"<li>{e(x)}</li>" for x in c["do"])
    shots = ""
    for key, title, text, alt in c["shots"]:
        shots += f'''<figure class="shot">
<img src="/assets/img/{lang}-{key}.webp" width="560" height="{{h}}" alt="{e(alt)}" loading="lazy" decoding="async">
<figcaption><strong>{e(title)}</strong><span>{e(text)}</span></figcaption>
</figure>'''.replace("{h}", "1183")
    feats = ""
    n = 0
    for key, title, text, alt in c["feats"]:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "assets", "img", f"{lang}-{key}.webp")):
            continue  # captura de ese idioma aún no disponible: el bloque se omite
        n += 1
        feats += f'''<article class="feat{" feat-r" if n % 2 == 0 else ""}">
<div class="feat-text"><h2>{e(title)}</h2><p>{e(text)}</p></div>
<div class="feat-phone"><img src="/assets/img/{lang}-{key}.webp" width="560" height="1183" alt="{e(alt)}" loading="lazy" decoding="async"></div>
</article>'''
    faq = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in c["faq"])
    faq += f'<details><summary>{e(c["help_q"])}</summary><p><a href="{LEGAL["support"]}">{e(c["help_a"])}</a></p></details>'
    lp, lt, ls = c["legal_links"]
    ln_link = ('<a href="' + LNPATH[lang] + '">' + e(LN[lang]["link"]) + '</a>') if LEGAL_PAGES_LIVE else ""
    return f'''<!doctype html>
<html lang="{lang}">
<head>
{head_common(lang, c["title"], c["desc"], canonical, extra)}</head>
<body>
<a class="skip" href="#main">{e({"en":"Skip to content","es":"Saltar al contenido","de":"Zum Inhalt springen","fr":"Aller au contenu"}[lang])}</a>
<header class="top wrap">
<a class="brand" href="{PATH[lang]}" aria-label="{e(c["home_label"])}">Hoopline GM</a>
<nav class="langs" aria-label="{e(c["lang_label"])}">{switch}</nav>
</header>
<main id="main">
<section class="hero wrap">
<div class="hero-text">
<h1>{e(c["h1"])}</h1>
<p class="lead">{e(c["lead"])}</p>
<p class="cta-row">{badge(lang, c)}</p>
<p class="note">{e(c["android"])}</p>
</div>
<div class="hero-phone"><img src="/assets/img/{lang}-market.webp" width="560" height="1183" alt="{e(c["market_alt"])}" fetchpriority="high" decoding="async"></div>
</section>

<section class="open wrap">
<h2>{e(c["open_title"])}</h2>
<ul class="pillars">{pillars}</ul>
</section>

<section class="do wrap">
<h2>{e(c["do_h"])}</h2>
<ul class="dolist">{do}</ul>
</section>

<section class="feats wrap">{feats}</section>

<div class="mid-cta wrap">{badge(lang, c)}</div>

<section class="fair">
<div class="wrap fair-in">
<h2>{e(c["fair_h"])}</h2>
<div class="fair-body">
<p>{e(c["fair_p"])}</p>
<h3>{e(c["prem_h"])}</h3>
<p>{e(c["prem_p"])}</p>
</div>
</div>
</section>

<section class="shots wrap" aria-labelledby="shots-h">
<h2 id="shots-h">{e(c["shots_h"])}</h2>
<div class="shot-row" tabindex="0" role="group" aria-labelledby="shots-h">{shots}</div>
</section>

<section class="faq wrap">
<h2>{e(c["faq_h"])}</h2>
<div class="faq-list">{faq}</div>
</section>

<section class="end wrap">
<h2>{e(c["cta_h"])}</h2>
<p class="cta-row">{badge(lang, c)}</p>
</section>
</main>
<footer class="foot wrap">
<nav class="foot-links" aria-label="Legal"><a href="{LEGAL["privacy"]}">{e(lp)}</a><a href="{LEGAL["terms"]}">{e(lt)}</a>{ln_link}<a href="{LEGAL["support"]}">{e(ls)}</a></nav>
<p class="notice">{e(c["notice"])}</p>
<p class="copy">© 2026 Hoopline GM</p>
</footer>
</body>
</html>
'''

for l in LANGS:
    w(("" if l == "en" else l + "/") + "index.html", landing(l))

# ----------------------------------------------------------------- /auth/confirm
AUTH_HEAD = head_common("en", "Hoopline GM", "Hoopline GM", SITE + "/auth/confirm/", '<meta name="robots" content="noindex, nofollow">\n<meta name="referrer" content="no-referrer">')
confirm_html = f'''<!doctype html>
<html lang="en">
<head>
{AUTH_HEAD}</head>
<body class="auth">
<header class="top wrap"><a class="brand" href="/">Hoopline GM</a></header>
<main class="auth-main wrap">
<div class="auth-card" id="card" aria-live="polite">
<h1 id="t"></h1>
<p id="p"></p>
<form id="pw" hidden>
<label for="pw1" id="pwl"></label>
<input id="pw1" name="password" type="password" autocomplete="new-password" minlength="6" required>
<label class="show"><input id="showpw" type="checkbox"> <span id="shl"></span></label>
<p class="err" id="pwerr" role="alert" hidden></p>
<button class="btn" type="submit" id="pwb"></button>
</form>
<p class="actions">
<button class="btn" type="button" id="go" hidden></button>
<a class="btn" id="open" href="{OPEN_APP_URL}" hidden></a>
</p>
<p class="note" id="n"></p>
</div>
</main>
<script src="/assets/confirm.js" defer></script>
</body>
</html>
'''
w("auth/confirm/index.html", confirm_html)

confirm_js = r'''(function () {
  "use strict";
  var SUPABASE_URL = "%(url)s";
  var SUPABASE_KEY = "%(key)s";
  var OPEN_APP_URL = "%(open)s";
  var TYPES = { email: 1, signup: 1, recovery: 1, email_change: 1, magiclink: 1, invite: 1 };

  var S = {
    en: {
      ready_email: ["Confirm your email", "Tap the button to finish creating your account."],
      ready_recovery: ["Choose a new password", "Tap the button to continue."],
      ready_email_change: ["Confirm your new email", "Tap the button to confirm the change."],
      ready_magiclink: ["Sign in to Hoopline GM", "Tap the button to continue."],
      btn_email: "Confirm email", btn_recovery: "Continue", btn_email_change: "Confirm change", btn_magiclink: "Continue",
      working: "One moment…",
      done_email: ["Email confirmed", "Your account is ready. Open Hoopline GM and sign in."],
      done_email_change: ["Email updated", "Your new email is active. Open Hoopline GM and sign in with it."],
      done_magiclink: ["You are verified", "Go back to Hoopline GM to keep playing."],
      done_recovery: ["Password updated", "Open Hoopline GM and sign in with your new password."],
      form_title: "Choose a new password", form_text: "Use at least 6 characters.", pw_label: "New password", show: "Show password", save: "Save password",
      open: "Open Hoopline GM", desktop: "Open Hoopline GM on your phone to continue.",
      err_title: "This link did not work", err_expired: "It has expired or was already used. Request a new one from the app.",
      err_generic: "Something went wrong. Try again, or request a new link from the app.",
      err_network: "No connection. Check your internet and try again.",
      missing_title: "This link is incomplete", missing_text: "Open the link from the email again, or request a new one from the app.",
      retry: "Try again",
      note_safe: "If you did not ask for this, you can close this page."
    },
    es: {
      ready_email: ["Confirma tu correo", "Pulsa el botón para terminar de crear tu cuenta."],
      ready_recovery: ["Elige una contraseña nueva", "Pulsa el botón para continuar."],
      ready_email_change: ["Confirma tu nuevo correo", "Pulsa el botón para confirmar el cambio."],
      ready_magiclink: ["Entra en Hoopline GM", "Pulsa el botón para continuar."],
      btn_email: "Confirmar correo", btn_recovery: "Continuar", btn_email_change: "Confirmar cambio", btn_magiclink: "Continuar",
      working: "Un momento…",
      done_email: ["Correo confirmado", "Tu cuenta está lista. Abre Hoopline GM e inicia sesión."],
      done_email_change: ["Correo actualizado", "Tu nuevo correo ya está activo. Abre Hoopline GM e inicia sesión con él."],
      done_magiclink: ["Verificado", "Vuelve a Hoopline GM para seguir jugando."],
      done_recovery: ["Contraseña actualizada", "Abre Hoopline GM e inicia sesión con tu nueva contraseña."],
      form_title: "Elige una contraseña nueva", form_text: "Usa al menos 6 caracteres.", pw_label: "Contraseña nueva", show: "Mostrar contraseña", save: "Guardar contraseña",
      open: "Abrir Hoopline GM", desktop: "Abre Hoopline GM en tu móvil para continuar.",
      err_title: "Este enlace no ha funcionado", err_expired: "Ha caducado o ya se usó. Pide uno nuevo desde la app.",
      err_generic: "Algo ha fallado. Inténtalo de nuevo o pide un enlace nuevo desde la app.",
      err_network: "Sin conexión. Revisa tu internet e inténtalo de nuevo.",
      missing_title: "El enlace está incompleto", missing_text: "Vuelve a abrir el enlace del correo o pide uno nuevo desde la app.",
      retry: "Intentar de nuevo",
      note_safe: "Si no lo has pedido tú, puedes cerrar esta página."
    },
    de: {
      ready_email: ["Bestätige deine E-Mail", "Tippe auf den Button, um dein Konto fertig einzurichten."],
      ready_recovery: ["Neues Passwort wählen", "Tippe auf den Button, um fortzufahren."],
      ready_email_change: ["Neue E-Mail bestätigen", "Tippe auf den Button, um die Änderung zu bestätigen."],
      ready_magiclink: ["Bei Hoopline GM anmelden", "Tippe auf den Button, um fortzufahren."],
      btn_email: "E-Mail bestätigen", btn_recovery: "Weiter", btn_email_change: "Änderung bestätigen", btn_magiclink: "Weiter",
      working: "Einen Moment …",
      done_email: ["E-Mail bestätigt", "Dein Konto ist bereit. Öffne Hoopline GM und melde dich an."],
      done_email_change: ["E-Mail aktualisiert", "Deine neue E-Mail ist aktiv. Öffne Hoopline GM und melde dich damit an."],
      done_magiclink: ["Verifiziert", "Geh zurück zu Hoopline GM, um weiterzuspielen."],
      done_recovery: ["Passwort aktualisiert", "Öffne Hoopline GM und melde dich mit deinem neuen Passwort an."],
      form_title: "Neues Passwort wählen", form_text: "Mindestens 6 Zeichen.", pw_label: "Neues Passwort", show: "Passwort anzeigen", save: "Passwort speichern",
      open: "Hoopline GM öffnen", desktop: "Öffne Hoopline GM auf deinem Handy, um fortzufahren.",
      err_title: "Dieser Link hat nicht funktioniert", err_expired: "Er ist abgelaufen oder wurde schon benutzt. Fordere in der App einen neuen an.",
      err_generic: "Etwas ist schiefgegangen. Versuch es noch einmal oder fordere in der App einen neuen Link an.",
      err_network: "Keine Verbindung. Prüfe dein Internet und versuch es noch einmal.",
      missing_title: "Der Link ist unvollständig", missing_text: "Öffne den Link aus der E-Mail noch einmal oder fordere in der App einen neuen an.",
      retry: "Noch einmal versuchen",
      note_safe: "Wenn du das nicht angefordert hast, kannst du diese Seite schließen."
    },
    fr: {
      ready_email: ["Confirmez votre e-mail", "Appuyez sur le bouton pour terminer la création de votre compte."],
      ready_recovery: ["Choisissez un nouveau mot de passe", "Appuyez sur le bouton pour continuer."],
      ready_email_change: ["Confirmez votre nouvel e-mail", "Appuyez sur le bouton pour confirmer le changement."],
      ready_magiclink: ["Connectez-vous à Hoopline GM", "Appuyez sur le bouton pour continuer."],
      btn_email: "Confirmer l’e-mail", btn_recovery: "Continuer", btn_email_change: "Confirmer le changement", btn_magiclink: "Continuer",
      working: "Un instant…",
      done_email: ["E-mail confirmé", "Votre compte est prêt. Ouvrez Hoopline GM et connectez-vous."],
      done_email_change: ["E-mail mis à jour", "Votre nouvel e-mail est actif. Ouvrez Hoopline GM et connectez-vous avec."],
      done_magiclink: ["Vérifié", "Retournez dans Hoopline GM pour continuer à jouer."],
      done_recovery: ["Mot de passe mis à jour", "Ouvrez Hoopline GM et connectez-vous avec votre nouveau mot de passe."],
      form_title: "Choisissez un nouveau mot de passe", form_text: "Au moins 6 caractères.", pw_label: "Nouveau mot de passe", show: "Afficher le mot de passe", save: "Enregistrer le mot de passe",
      open: "Ouvrir Hoopline GM", desktop: "Ouvrez Hoopline GM sur votre téléphone pour continuer.",
      err_title: "Ce lien n’a pas fonctionné", err_expired: "Il a expiré ou a déjà été utilisé. Demandez-en un nouveau depuis l’app.",
      err_generic: "Une erreur est survenue. Réessayez, ou demandez un nouveau lien depuis l’app.",
      err_network: "Pas de connexion. Vérifiez votre internet et réessayez.",
      missing_title: "Le lien est incomplet", missing_text: "Rouvrez le lien de l’e-mail ou demandez-en un nouveau depuis l’app.",
      retry: "Réessayer",
      note_safe: "Si vous n’êtes pas à l’origine de cette demande, vous pouvez fermer cette page."
    }
  };

  var qs = new URLSearchParams(location.search);
  var tokenHash = qs.get("token_hash");
  var type = qs.get("type") || "email";
  var lang = (qs.get("lang") || (navigator.language || "en")).slice(0, 2).toLowerCase();
  if (!S[lang]) lang = "en";
  var T = S[lang];
  document.documentElement.lang = lang;
  // El token no debe quedarse en la barra de direcciones ni en el historial.
  try { history.replaceState(null, "", location.pathname); } catch (e) {}

  var $ = function (id) { return document.getElementById(id); };
  var title = $("t"), text = $("p"), note = $("n"), go = $("go"), open = $("open"), form = $("pw");
  var access = null;
  var mobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

  function show(t, p, opts) {
    opts = opts || {};
    title.textContent = t; text.textContent = p;
    go.hidden = !opts.button; if (opts.button) go.textContent = opts.button;
    form.hidden = !opts.form;
    open.hidden = !opts.open; open.textContent = T.open;
    note.textContent = opts.note || "";
    if (opts.open && !mobile) { open.hidden = true; text.textContent = p + " " + T.desktop; }
  }
  function key(k) { return T[k + "_" + (type === "signup" ? "email" : type)] || T[k + "_email"]; }
  function btn() { return T["btn_" + (type === "signup" ? "email" : type)] || T.btn_email; }

  function fail(code, msg) {
    var text2 = code === "otp_expired" || code === "flow_state_expired" || /expired|invalid/i.test(msg || "") ? T.err_expired : T.err_generic;
    show(T.err_title, text2, { button: T.retry });
    go.onclick = function () { location.reload(); };
    // «Intentar de nuevo» solo tiene sentido si el enlace puede seguir valiendo; si ha caducado, se pide uno nuevo desde la app.
    if (text2 === T.err_expired) go.hidden = true;
  }

  if (!tokenHash || !TYPES[type]) {
    show(T.missing_title, T.missing_text);
  } else {
    show(key("ready")[0], key("ready")[1], { button: btn(), note: T.note_safe });
    go.onclick = verify;
  }

  function verify() {
    go.disabled = true; text.textContent = T.working;
    fetch(SUPABASE_URL + "/auth/v1/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json", apikey: SUPABASE_KEY },
      body: JSON.stringify({ type: type === "signup" ? "email" : type, token_hash: tokenHash })
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (b) { return { ok: r.ok, body: b }; });
    }).then(function (res) {
      go.disabled = false;
      if (!res.ok) { fail(res.body.error_code || res.body.code, res.body.msg || res.body.message); return; }
      if (type === "recovery") {
        access = res.body.access_token;
        show(T.form_title, T.form_text, { form: true });
        $("pwl").textContent = T.pw_label; $("shl").textContent = T.show; $("pwb").textContent = T.save;
        $("pw1").focus();
      } else {
        var d = T["done_" + (type === "signup" ? "email" : type)] || T.done_email;
        show(d[0], d[1], { open: true });
      }
    }).catch(function () {
      go.disabled = false;
      show(T.err_title, T.err_network, { button: T.retry });
      go.onclick = verify;
    });
  }

  $("showpw").addEventListener("change", function (ev) { $("pw1").type = ev.target.checked ? "text" : "password"; });
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var err = $("pwerr"); err.hidden = true;
    var b = $("pwb"); b.disabled = true;
    fetch(SUPABASE_URL + "/auth/v1/user", {
      method: "PUT",
      headers: { "Content-Type": "application/json", apikey: SUPABASE_KEY, Authorization: "Bearer " + access },
      body: JSON.stringify({ password: $("pw1").value })
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (body) { return { ok: r.ok, body: body }; });
    }).then(function (res) {
      b.disabled = false;
      if (res.ok) { access = null; var d = T.done_recovery; show(d[0], d[1], { open: true }); return; }
      err.textContent = res.body.msg || res.body.message || T.err_generic; err.hidden = false;
    }).catch(function () { b.disabled = false; err.textContent = T.err_network; err.hidden = false; });
  });
})();
''' % {"url": SUPABASE_URL, "key": SUPABASE_KEY, "open": OPEN_APP_URL}
w("assets/confirm.js", confirm_js)

# ----------------------------------------------------------------- Aviso legal / Impressum (solo si LEGAL_PAGES_LIVE)
def legal_page(lang):
    d = LN[lang]
    c = COPY[lang]
    canonical = SITE + LNPATH[lang]
    alts = ""
    for m in LANGS:
        alts += '<link rel="alternate" hreflang="' + m + '" href="' + SITE + LNPATH[m] + '">\n'
    alts += '<link rel="alternate" hreflang="x-default" href="' + SITE + LNPATH["en"] + '">\n'
    extra = '<link rel="canonical" href="' + canonical + '">\n' + alts
    switch = ""
    for l in LANGS:
        cur = ' aria-current="page"' if l == lang else ""
        switch += '<a href="' + LNPATH[l] + '" hreflang="' + l + '" lang="' + l + '"' + cur + ' aria-label="' + NAME[l] + '">' + l.upper() + '</a>'
    lp, lt, ls = c["legal_links"]
    privacy = '<a href="' + LEGAL["privacy"] + '">' + e(lp) + '</a>'
    terms = '<a href="' + LEGAL["terms"] + '">' + e(lt) + '</a>'
    mail = '<a href="mailto:' + OWNER["email"] + '">' + OWNER["email"] + '</a>'
    def fill(t):
        t = e(t)
        return t.replace("{notice}", e(c["notice"])).replace("{privacy}", privacy).replace("{terms}", terms).replace("{email}", mail)
    card = ""
    for k, v in d["card"]:
        val = v
        if v == OWNER["email"]:
            val = mail
        elif v == OWNER["site"]:
            val = '<a href="' + OWNER["site"] + '">' + OWNER["site"].replace("https://", "") + '</a>'
        else:
            val = e(v)
        card += '<div><dt>' + e(k) + '</dt><dd>' + val + '</dd></div>'
    body = ""
    for h, paras in d["sections"]:
        body += '<section><h2>' + e(h) + '</h2>' + "".join("<p>" + fill(p) + "</p>" for p in paras) + '</section>'
    skip = {"en": "Skip to content", "es": "Saltar al contenido", "de": "Zum Inhalt springen", "fr": "Aller au contenu"}[lang]
    return f'''<!doctype html>
<html lang="{lang}">
<head>
{head_common(lang, d["title"] + " · Hoopline GM", d["meta_desc"], canonical, extra)}</head>
<body>
<a class="skip" href="#main">{e(skip)}</a>
<header class="top wrap">
<a class="brand" href="{PATH[lang]}" aria-label="{e(c["home_label"])}">Hoopline GM</a>
<nav class="langs" aria-label="{e(c["lang_label"])}">{switch}</nav>
</header>
<main id="main" class="legal-doc wrap">
<h1>{e(d["title"])}</h1>
<p class="legal-intro">{e(d["intro"])}</p>
<dl class="legal-card">{card}</dl>
{body}
</main>
<footer class="foot wrap">
<nav class="foot-links" aria-label="Legal"><a href="{LEGAL["privacy"]}">{e(lp)}</a><a href="{LEGAL["terms"]}">{e(lt)}</a><a href="{LNPATH[lang]}">{e(d["link"])}</a><a href="{LEGAL["support"]}">{e(ls)}</a></nav>
<p class="copy">© 2026 Hoopline GM</p>
</footer>
</body>
</html>
'''

if LEGAL_PAGES_LIVE:
    for l in LANGS:
        w(LNPATH[l].strip("/") + "/index.html", legal_page(l))

# ----------------------------------------------------------------- 404, robots, sitemap, headers, favicon
w("404.html", f'''<!doctype html>
<html lang="en">
<head>
{head_common("en", "Hoopline GM", "Hoopline GM", SITE + "/", '<meta name="robots" content="noindex">')}</head>
<body class="auth">
<header class="top wrap"><a class="brand" href="/">Hoopline GM</a></header>
<main class="auth-main wrap"><div class="auth-card">
<h1>404</h1>
<p>This page does not exist. · Esta página no existe. · Diese Seite gibt es nicht. · Cette page n’existe pas.</p>
<p class="actions"><a class="btn" href="/">Hoopline GM</a></p>
</div></main>
</body>
</html>
''')
w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /auth/\n\nSitemap: {SITE}/sitemap.xml\n")
urls = ""
for l in LANGS:
    urls += f"<url><loc>{SITE}{PATH[l]}</loc>"
    for m in LANGS:
        urls += f'<xhtml:link rel="alternate" hreflang="{m}" href="{SITE}{PATH[m]}"/>'
    urls += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/></url>\n'
if LEGAL_PAGES_LIVE:
    for l in LANGS:
        urls += "<url><loc>" + SITE + LNPATH[l] + "</loc>"
        for m in LANGS:
            urls += '<xhtml:link rel="alternate" hreflang="' + m + '" href="' + SITE + LNPATH[m] + '"/>'
        urls += '<xhtml:link rel="alternate" hreflang="x-default" href="' + SITE + LNPATH["en"] + '"/></url>\n'
w("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
w("_headers", f"""/*
  X-Content-Type-Options: nosniff
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self' {SUPABASE_URL}; frame-ancestors 'none'; base-uri 'none'; form-action 'self'

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/auth/*
  Referrer-Policy: no-referrer
  Cache-Control: no-store
  X-Robots-Tag: noindex
""")
print("ok")
