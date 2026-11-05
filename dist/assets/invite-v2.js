(function () {
  "use strict";
  var OPEN = "com.hooplinegm.app://invite/";
  var BADGES = {"en": {"as": "app-store-badge-en.svg", "asw": 156, "asa": "Download on the App Store", "gp": "google-play-badge-en.svg", "gpw": 175, "gpa": "Get it on Google Play"}, "es": {"as": "app-store-badge-es.svg", "asw": 156, "asa": "Descargar en la App Store", "gp": "google-play-badge-es.svg", "gpw": 175, "gpa": "Disponible en Google Play"}, "de": {"as": "app-store-badge-de.svg", "asw": 156, "asa": "Laden im App Store", "gp": "google-play-badge-de.svg", "gpw": 175, "gpa": "Jetzt bei Google Play"}, "fr": {"as": "app-store-badge-fr.svg", "asw": 164, "asa": "Télécharger dans l’App Store", "gp": "google-play-badge-fr.svg", "gpw": 175, "gpa": "Disponible sur Google Play"}};
  var S = {
    en: {
      title: "You have been invited to Hoopline GM",
      text: "The manager code of whoever invited you:",
      open: "Open in the app", copy: "Copy code", copied: "Code copied",
      note: "No app yet? Install it and write this code when you create your team. Already playing? Open it and write the code in More → Friends.",
      bad_title: "This link is missing its code",
      bad_text: "Ask whoever invited you to share it again from Hoopline GM, in More → Friends."
    },
    es: {
      title: "Te han invitado a Hoopline GM",
      text: "El código de mánager de quien te invita:",
      open: "Abrir en la app", copy: "Copiar código", copied: "Código copiado",
      note: "¿Aún no tienes la app? Instálala y escribe este código al crear tu equipo. ¿Ya juegas? Ábrela y escríbelo en Más → Amigos.",
      bad_title: "A este enlace le falta el código",
      bad_text: "Pide a quien te ha invitado que lo comparta otra vez desde Hoopline GM, en Más → Amigos."
    },
    fr: {
      title: "Vous êtes invité à Hoopline GM",
      text: "Le code de manager de la personne qui vous invite :",
      open: "Ouvrir dans l’app", copy: "Copier le code", copied: "Code copié",
      note: "Pas encore l’app ? Installez-la et saisissez ce code en créant votre équipe. Vous jouez déjà ? Ouvrez-la et saisissez le code dans Plus → Amis.",
      bad_title: "Il manque le code dans ce lien",
      bad_text: "Demandez à la personne qui vous a invité de le partager à nouveau depuis Hoopline GM, dans Plus → Amis."
    },
    de: {
      title: "Du wurdest zu Hoopline GM eingeladen",
      text: "Der Manager-Code der Person, die dich einlädt:",
      open: "In der App öffnen", copy: "Code kopieren", copied: "Code kopiert",
      note: "Noch keine App? Installiere sie und gib diesen Code ein, wenn du dein Team erstellst. Du spielst schon? Öffne sie und gib den Code unter Mehr → Freunde ein.",
      bad_title: "In diesem Link fehlt der Code",
      bad_text: "Bitte die Person, die dich eingeladen hat, ihn in Hoopline GM unter Mehr → Freunde noch einmal zu teilen."
    }
  };

  function $(id) { return document.getElementById(id); }

  var lang = "en";
  var prefs = navigator.languages || [navigator.language || "en"];
  for (var i = 0; i < prefs.length; i++) {
    var l = String(prefs[i] || "").slice(0, 2).toLowerCase();
    if (S[l]) { lang = l; break; }
  }
  var T = S[lang];
  document.documentElement.lang = lang;
  var b = BADGES[lang];
  $("as").src = "/assets/img/" + b.as; $("as").width = b.asw; $("as").alt = b.asa;
  $("gp").src = "/assets/img/" + b.gp; $("gp").width = b.gpw; $("gp").alt = b.gpa;

  // ?c=<code>, as the app shares it; the same rule as the app: with or without dashes, in any case.
  var raw = new URLSearchParams(location.search).get("c") || "";
  var compact = raw.toUpperCase().replace(/-/g, "");
  var code = /^HGM[A-Z0-9]{8}$/.test(compact)
    ? "HGM-" + compact.slice(3, 7) + "-" + compact.slice(7) : null;

  if (!code) {
    $("t").textContent = T.bad_title;
    $("p").textContent = T.bad_text;
    return;
  }
  document.title = T.title;
  $("t").textContent = T.title;
  $("p").textContent = T.text;
  $("code").textContent = code; $("code").hidden = false;
  var open = $("open");
  open.href = OPEN + code; open.textContent = T.open; open.hidden = false;
  $("n").textContent = T.note;
  var copy = $("copy");
  if (navigator.clipboard && navigator.clipboard.writeText) {
    copy.textContent = T.copy; copy.hidden = false;
    copy.onclick = function () {
      navigator.clipboard.writeText(code).then(function () { copy.textContent = T.copied; });
    };
  }
})();
