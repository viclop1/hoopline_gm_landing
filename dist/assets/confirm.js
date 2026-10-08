(function () {
  "use strict";
  var SUPABASE_URL = "https://qllwdtrmzlisyfaznoml.supabase.co";
  var SUPABASE_KEY = "sb_publishable_rIDDRy1qk65YFKYj_moGHA_Coha3u2C";
  var OPEN_APP_URL = "com.hooplinegm.app://login-callback/";
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
