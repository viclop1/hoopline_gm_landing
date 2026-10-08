# -*- coding: utf-8 -*-
"""Aviso legal / Legal notice / Impressum / Mentions légales de hooplinegm.com.

Solo contenido: lo usan build.py (páginas web) y tools/make_legal_docx.py (borrador en Word para el abogado).
BORRADOR pendiente de revisión del abogado (consulta del 08/10/2026). Mientras LEGAL_PAGES_LIVE sea False en build.py
las páginas no se publican ni se enlazan.
"""

OWNER = {
    "name": "Víctor López Rodríguez",
    "nif": "05712011F",
    "address": "Calle de Valencia 5, escalera 2, 3.º A, 28945 Fuenlabrada (Madrid), Spain",
    "email": "hooplinegm@gmail.com",
    "site": "https://hooplinegm.com",
}

# Cada idioma: título de la página, texto del enlace del pie, introducción, tarjeta de datos (etiqueta, valor) y secciones (título, párrafos).
# Marcadores: {privacy} y {terms} se sustituyen por enlaces; {notice} por el aviso de independencia del idioma.
LN = {
    "en": {
        "title": "Legal notice",
        "link": "Legal notice",
        "meta_desc": "Legal notice of hooplinegm.com, the website of the game Hoopline GM.",
        "intro": "Information about the owner of this website, as required by Article 10 of Spanish Law 34/2002 on information society services (LSSI) and, for visitors in Germany, § 5 of the German Digital Services Act (DDG).",
        "card": [("Owner", OWNER["name"]), ("Tax ID (NIF)", OWNER["nif"]), ("Address", OWNER["address"]), ("Email", OWNER["email"]), ("Website", OWNER["site"])],
        "sections": [
            ("About this website", ["hooplinegm.com presents the mobile game Hoopline GM and hosts the page that confirms the emails the game sends (account confirmation and password recovery). The game itself is governed by the {terms} and the {privacy}."]),
            ("Independence", ["{notice}"]),
            ("Intellectual property", ["The name Hoopline GM and the original texts and graphic elements of this website belong to the owner or are used with the corresponding authorisation. Names, trademarks and other elements of third parties belong to their respective owners. Reproducing or using the original content of this website beyond the limits permitted by applicable law is prohibited without the corresponding authorisation."]),
            ("Links", ["This website links to services run by third parties (the App Store, and GitHub Pages for the legal texts). We are not responsible for their content."]),
            ("Complaints and disputes", ["If you have a complaint, write to {email}; we will reply within 30 days. We do not currently participate in any alternative dispute resolution scheme. Spanish law applies; the mandatory consumer protection of the country where you live is not affected. See section 12 of the {terms}."]),
            ("Privacy", ["How personal data is handled, including the technical data processed when you visit this website, is explained in the {privacy}."]),
        ],
    },
    "es": {
        "title": "Aviso legal",
        "link": "Aviso legal",
        "meta_desc": "Aviso legal de hooplinegm.com, la web del juego Hoopline GM.",
        "intro": "Información sobre el titular de esta web, conforme al artículo 10 de la Ley 34/2002 de servicios de la sociedad de la información y de comercio electrónico (LSSI) y, para las personas que la visitan desde Alemania, al § 5 de la ley alemana de servicios digitales (DDG).",
        "card": [("Titular", OWNER["name"]), ("NIF", OWNER["nif"]), ("Domicilio", OWNER["address"]), ("Correo electrónico", OWNER["email"]), ("Sitio web", OWNER["site"])],
        "sections": [
            ("Sobre esta web", ["hooplinegm.com presenta el juego para móviles Hoopline GM y aloja la página que confirma los correos que envía el juego (confirmación de cuenta y recuperación de contraseña). El juego se rige por las {terms} y la {privacy}."]),
            ("Independencia", ["{notice}"]),
            ("Propiedad intelectual", ["El nombre Hoopline GM y los textos y elementos gráficos originales de esta web pertenecen al titular o se utilizan con la correspondiente autorización. Los nombres, marcas y otros elementos de terceros pertenecen a sus respectivos titulares. Queda prohibida la reproducción o utilización de los contenidos originales de esta web fuera de los límites permitidos por la legislación aplicable sin la correspondiente autorización."]),
            ("Enlaces", ["Esta web enlaza a servicios de terceros (la App Store y GitHub Pages para los textos legales). No nos hacemos responsables de su contenido."]),
            ("Reclamaciones y litigios", ["Si tienes una reclamación, escríbenos a {email}; te responderemos en un máximo de 30 días. Actualmente no participamos en ningún sistema de resolución alternativa de litigios. Se aplica la ley española, sin perjuicio de la protección imperativa que te otorgue la ley del país donde vives. Consulta la sección 12 de las {terms}."]),
            ("Privacidad", ["En la {privacy} se explica cómo se tratan los datos personales, incluidos los datos técnicos que se procesan al visitar esta web."]),
        ],
    },
    "de": {
        "title": "Impressum",
        "link": "Impressum",
        "meta_desc": "Impressum von hooplinegm.com, der Website des Spiels Hoopline GM.",
        "intro": "Angaben gemäß § 5 DDG (Digitale-Dienste-Gesetz) und Artikel 10 des spanischen Gesetzes 34/2002 (LSSI).",
        "card": [("Anbieter", OWNER["name"]), ("Steuernummer (NIF)", OWNER["nif"]), ("Anschrift", OWNER["address"]), ("E-Mail", OWNER["email"]), ("Website", OWNER["site"])],
        "sections": [
            ("Über diese Website", ["hooplinegm.com stellt das Mobilspiel Hoopline GM vor und enthält die Seite, auf der die vom Spiel versendeten E-Mails bestätigt werden (Kontobestätigung und Zurücksetzen des Passworts). Für das Spiel selbst gelten die {terms} und die {privacy}."]),
            ("Unabhängigkeit", ["{notice}"]),
            ("Geistiges Eigentum", ["Der Name Hoopline GM sowie die originalen Texte und grafischen Elemente dieser Website gehören dem Anbieter oder werden mit entsprechender Erlaubnis verwendet. Namen, Marken und sonstige Elemente Dritter gehören ihren jeweiligen Inhabern. Die Vervielfältigung oder Nutzung der originalen Inhalte dieser Website über die gesetzlich zulässigen Grenzen hinaus ist ohne entsprechende Genehmigung untersagt."]),
            ("Links", ["Diese Website verlinkt auf Dienste Dritter (den App Store sowie GitHub Pages für die rechtlichen Texte). Für deren Inhalte sind wir nicht verantwortlich."]),
            ("Beschwerden und Streitigkeiten", ["Bei Beschwerden schreib uns an {email}; wir antworten innerhalb von 30 Tagen. Wir nehmen derzeit an keinem Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teil. Es gilt spanisches Recht; zwingende Verbraucherschutzvorschriften des Landes, in dem du wohnst, bleiben unberührt. Siehe Abschnitt 12 der {terms}."]),
            ("Datenschutz", ["Wie personenbezogene Daten verarbeitet werden, einschließlich der technischen Daten, die beim Besuch dieser Website anfallen, steht in der {privacy}."]),
        ],
    },
    "fr": {
        "title": "Mentions légales",
        "link": "Mentions légales",
        "meta_desc": "Mentions légales de hooplinegm.com, le site du jeu Hoopline GM.",
        "intro": "Informations sur l’éditeur de ce site, conformément à l’article 10 de la loi espagnole 34/2002 (LSSI) et, pour les visiteurs en Allemagne, au § 5 de la loi allemande sur les services numériques (DDG).",
        "card": [("Éditeur", OWNER["name"]), ("Numéro fiscal (NIF)", OWNER["nif"]), ("Adresse", OWNER["address"]), ("E-mail", OWNER["email"]), ("Site", OWNER["site"])],
        "sections": [
            ("À propos de ce site", ["hooplinegm.com présente le jeu mobile Hoopline GM et héberge la page qui confirme les e-mails envoyés par le jeu (confirmation de compte et récupération du mot de passe). Le jeu est régi par les {terms} et la {privacy}."]),
            ("Indépendance", ["{notice}"]),
            ("Propriété intellectuelle", ["Le nom Hoopline GM ainsi que les textes et éléments graphiques originaux de ce site appartiennent à l’éditeur ou sont utilisés avec l’autorisation correspondante. Les noms, marques et autres éléments de tiers appartiennent à leurs titulaires respectifs. La reproduction ou l’utilisation des contenus originaux de ce site au-delà des limites autorisées par la législation applicable est interdite sans autorisation préalable."]),
            ("Liens", ["Ce site renvoie vers des services tiers (l’App Store et GitHub Pages pour les textes juridiques). Nous ne sommes pas responsables de leur contenu."]),
            ("Réclamations et litiges", ["Pour toute réclamation, écrivez-nous à {email} ; nous répondrons sous 30 jours. Nous ne participons actuellement à aucun dispositif de règlement extrajudiciaire des litiges. Le droit espagnol s’applique, sans préjudice de la protection impérative dont vous bénéficiez selon la loi du pays où vous résidez. Voir l’article 12 des {terms}."]),
            ("Confidentialité", ["La {privacy} explique comment les données personnelles sont traitées, y compris les données techniques traitées lors de la visite de ce site."]),
        ],
    },
}

# Texto de ejemplo para la política de privacidad (solo en inglés, como la política). Pendiente de confirmar la retención real en Cloudflare.
PRIVACY_WEB_SECTION = {
    "heading": "Website (hooplinegm.com)",
    "paragraphs": [
        "This section covers the website hooplinegm.com, not the game. The website does not use cookies, analytics or advertising, and its fonts and images are served from the same domain.",
        "When you visit the website, technical data about the connection is processed to deliver the pages and to keep the service secure: your IP address, the date and time, the page requested, and technical details such as the browser and device type your browser sends. The website is delivered through Cloudflare, Inc., which provides our infrastructure and security services. Cloudflare may process technical information about visitors, including IP addresses and security-related event data, as necessary to provide and secure the service. Depending on the processing involved, Cloudflare may act on our behalf or as an independent controller for its own security and operational purposes. Further information is available in Cloudflare’s Privacy Policy (https://www.cloudflare.com/privacypolicy/).",
        "We use this data only to deliver the content, protect the website against abuse and keep it working. The legal basis is our legitimate interest in running and securing the website (Article 6(1)(f) GDPR).",
        "We have not enabled HTTP request log retention, Cloudflare Web Analytics or Logpush for this website. We therefore do not maintain a separate log of visitors or send website request logs to another service. Cloudflare may nevertheless process technical and security-related data as part of operating and protecting its network. Security Events available through Cloudflare may be retained for up to 31 days. For further information, please see Cloudflare’s Privacy Policy.",
        "The page https://hooplinegm.com/auth/confirm opens when you tap the link in a confirmation or password-recovery email. It sends the one-time code in the link to Supabase, our authentication provider, to confirm your account or to let you set a new password, and removes the code from the address bar. It does not keep any of this information itself and does not use cookies.",
    ],
}
