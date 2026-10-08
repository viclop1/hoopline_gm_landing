import os, sys, json

OUT = sys.argv[1]
BG, SURF, ACC, TXT, MUT, LINE = "#0D1014", "#151A21", "#8B7BFF", "#F2F5F8", "#9AA4B2", "#232B35"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

# ---- link per template: "supabase" = {{ .ConfirmationURL }}, "own" = hooplinegm.com/auth/confirm
def link(kind, mode):
    if kind == "reauthentication": return None
    if mode == "supabase": return "{{ .ConfirmationURL }}"
    t = {"confirm_signup": "email", "magic_link": "email", "recovery": "recovery", "email_change": "email_change", "invite": "invite"}[kind]
    return "https://hooplinegm.com/auth/confirm?token_hash={{ .TokenHash }}&type=" + t

# ---- copy
T = {
"confirm_signup": {
  "subject": "Confirm your email · Confirma tu correo · Bestätige deine E-Mail · Confirmez votre e-mail",
  "en": dict(h="Confirm your email", p="Welcome to Hoopline GM. One tap and your team is ready: confirm your email to start building your roster.", b="Confirm email", n="Didn't create an account? Ignore this email, nothing will happen."),
  "es": dict(h="Confirma tu correo", p="Te damos la bienvenida a Hoopline GM. Confirma tu correo para empezar a montar tu plantilla.", b="Confirmar correo", n="¿No has creado una cuenta? Ignora este mensaje, no pasará nada."),
  "de": dict(h="Bestätige deine E-Mail", p="Willkommen bei Hoopline GM. Bestätige deine E-Mail-Adresse, um dein Team aufzubauen.", b="E-Mail bestätigen", n="Du hast kein Konto erstellt? Ignoriere diese Nachricht, es passiert nichts."),
  "fr": dict(h="Confirmez votre e-mail", p="Bienvenue sur Hoopline GM. Confirmez votre adresse e-mail pour commencer à construire votre équipe.", b="Confirmer l'e-mail", n="Vous n'avez pas créé de compte ? Ignorez ce message, il ne se passera rien."),
  "pre": "Confirm your email to start playing Hoopline GM",
},
"recovery": {
  "subject": "Reset your password · Restablece tu contraseña · Passwort zurücksetzen · Réinitialisez votre mot de passe",
  "en": dict(h="Reset your password", p="We received a request to reset the password of your Hoopline GM account. Tap the button to choose a new one.", b="Choose a new password", n="Didn't ask for this? Ignore this email and your password stays the same."),
  "es": dict(h="Restablece tu contraseña", p="Hemos recibido una solicitud para restablecer la contraseña de tu cuenta de Hoopline GM. Pulsa el botón para elegir una nueva.", b="Elegir nueva contraseña", n="¿No lo has pedido tú? Ignora este mensaje y tu contraseña seguirá igual."),
  "de": dict(h="Passwort zurücksetzen", p="Wir haben eine Anfrage erhalten, das Passwort deines Hoopline-GM-Kontos zurückzusetzen. Tippe auf den Button, um ein neues zu wählen.", b="Neues Passwort wählen", n="Nicht von dir? Ignoriere diese Nachricht, dein Passwort bleibt unverändert."),
  "fr": dict(h="Réinitialisez votre mot de passe", p="Nous avons reçu une demande de réinitialisation du mot de passe de votre compte Hoopline GM. Appuyez sur le bouton pour en choisir un nouveau.", b="Choisir un nouveau mot de passe", n="Ce n'est pas vous ? Ignorez ce message, votre mot de passe ne change pas."),
  "pre": "Choose a new password for your Hoopline GM account",
},
"email_change": {
  "subject": "Confirm your new email · Confirma tu nuevo correo · Neue E-Mail bestätigen · Confirmez votre nouvel e-mail",
  "en": dict(h="Confirm your new email", p="You asked to change the email of your Hoopline GM account from {{ .Email }} to {{ .NewEmail }}. Confirm the change to finish.", b="Confirm change", n="Didn't request this? Ignore this email and your account stays as it is."),
  "es": dict(h="Confirma tu nuevo correo", p="Has pedido cambiar el correo de tu cuenta de Hoopline GM de {{ .Email }} a {{ .NewEmail }}. Confirma el cambio para terminar.", b="Confirmar cambio", n="¿No lo has pedido tú? Ignora este mensaje y tu cuenta seguirá igual."),
  "de": dict(h="Neue E-Mail bestätigen", p="Du möchtest die E-Mail-Adresse deines Hoopline-GM-Kontos von {{ .Email }} auf {{ .NewEmail }} ändern. Bestätige die Änderung, um sie abzuschließen.", b="Änderung bestätigen", n="Nicht von dir? Ignoriere diese Nachricht, dein Konto bleibt unverändert."),
  "fr": dict(h="Confirmez votre nouvel e-mail", p="Vous avez demandé à changer l'e-mail de votre compte Hoopline GM de {{ .Email }} vers {{ .NewEmail }}. Confirmez le changement pour terminer.", b="Confirmer le changement", n="Ce n'est pas vous ? Ignorez ce message, votre compte ne change pas."),
  "pre": "Confirm the new email for your Hoopline GM account",
},
"magic_link": {
  "subject": "Your sign-in link · Tu enlace de acceso · Dein Anmeldelink · Votre lien de connexion",
  "en": dict(h="Sign in to Hoopline GM", p="Tap the button to sign in. The link works once and expires soon.", b="Sign in", n="Didn't try to sign in? Ignore this email."),
  "es": dict(h="Entra en Hoopline GM", p="Pulsa el botón para iniciar sesión. El enlace funciona una sola vez y caduca pronto.", b="Iniciar sesión", n="¿No has intentado entrar? Ignora este mensaje."),
  "de": dict(h="Bei Hoopline GM anmelden", p="Tippe auf den Button, um dich anzumelden. Der Link funktioniert nur einmal und läuft bald ab.", b="Anmelden", n="Du wolltest dich nicht anmelden? Ignoriere diese Nachricht."),
  "fr": dict(h="Connectez-vous à Hoopline GM", p="Appuyez sur le bouton pour vous connecter. Le lien ne fonctionne qu'une fois et expire bientôt.", b="Se connecter", n="Vous n'avez pas essayé de vous connecter ? Ignorez ce message."),
  "pre": "Your one-time sign-in link for Hoopline GM",
},
"reauthentication": {
  "subject": "Your confirmation code · Tu código de confirmación · Dein Bestätigungscode · Votre code de confirmation",
  "en": dict(h="Your confirmation code", p="Enter this code in Hoopline GM to confirm it's you.", b="", n="Didn't request a code? Ignore this email."),
  "es": dict(h="Tu código de confirmación", p="Introduce este código en Hoopline GM para confirmar que eres tú.", b="", n="¿No has pedido un código? Ignora este mensaje."),
  "de": dict(h="Dein Bestätigungscode", p="Gib diesen Code in Hoopline GM ein, um zu bestätigen, dass du es bist.", b="", n="Keinen Code angefordert? Ignoriere diese Nachricht."),
  "fr": dict(h="Votre code de confirmation", p="Saisissez ce code dans Hoopline GM pour confirmer que c'est bien vous.", b="", n="Vous n'avez pas demandé de code ? Ignorez ce message."),
  "pre": "Your Hoopline GM confirmation code",
},
}
FALLBACK = {"en": "Button not working? Copy this link into your browser:", "es": "¿No funciona el botón? Copia este enlace en tu navegador:", "de": "Button funktioniert nicht? Kopiere diesen Link in deinen Browser:", "fr": "Le bouton ne fonctionne pas ? Copie ce lien dans ton navigateur :"}
FOOT = {"en": "Sent by Hoopline GM · hooplinegm.com", "es": "Enviado por Hoopline GM · hooplinegm.com", "de": "Gesendet von Hoopline GM · hooplinegm.com", "fr": "Envoyé par Hoopline GM · hooplinegm.com"}

def code_box():
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:24px 0 8px;"><tr><td bgcolor="{BG}" style="background:{BG};border:1px solid {LINE};border-radius:12px;padding:16px 28px;font-family:'SF Mono',Menlo,Consolas,monospace;font-size:32px;letter-spacing:8px;font-weight:700;color:{TXT};">{{{{ .Token }}}}</td></tr></table>'''

def button(href, label):
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:26px 0 6px;"><tr><td align="center" bgcolor="{ACC}" style="background:{ACC};border-radius:12px;"><a href="{href}" target="_blank" style="display:inline-block;padding:15px 30px;font-family:{FONT};font-size:16px;font-weight:700;line-height:20px;color:{BG};text-decoration:none;border-radius:12px;">{label}</a></td></tr></table>'''

def main_block(kind, lang, href):
    c = T[kind][lang]
    s = f'<h1 style="margin:0 0 12px;font-family:{FONT};font-size:26px;line-height:32px;font-weight:700;color:{TXT};letter-spacing:-0.3px;">{c["h"]}</h1>'
    s += f'<p style="margin:0;font-family:{FONT};font-size:16px;line-height:25px;color:#C9D1DB;">{c["p"]}</p>'
    s += button(href, c["b"]) if href else code_box()
    s += f'<p style="margin:14px 0 0;font-family:{FONT};font-size:13px;line-height:20px;color:{MUT};">{c["n"]}</p>'
    return s

def small_block(kind, lang, href):
    c = T[kind][lang]
    s = f'<p style="margin:0 0 4px;font-family:{FONT};font-size:11px;letter-spacing:1.5px;font-weight:700;color:{ACC};">{lang.upper()}</p>'
    s += f'<p style="margin:0;font-family:{FONT};font-size:14px;line-height:22px;color:#C9D1DB;"><strong style="color:{TXT};">{c["h"]}.</strong> {c["p"]}'
    if href: s += f' <a href="{href}" target="_blank" style="color:{ACC};font-weight:700;text-decoration:none;white-space:nowrap;">{c["b"]} &rarr;</a>'
    s += f'</p>'
    s += f'<p style="margin:4px 0 0;font-family:{FONT};font-size:12px;line-height:18px;color:{MUT};">{c["n"]}</p>'
    return s

def page(kind, langs, href, title):
    pre = T[kind]["pre"]
    first, rest = langs[0], langs[1:]
    body = main_block(kind, first, href)
    if href:
        body += f'<p style="margin:18px 0 0;font-family:{FONT};font-size:12px;line-height:18px;color:{MUT};">{FALLBACK[first]}<br><a href="{href}" target="_blank" style="color:{ACC};word-break:break-all;">{href}</a></p>'
    for l in rest:
        body += f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:26px 0 0;"><tr><td style="border-top:1px solid {LINE};padding-top:20px;">{small_block(kind, l, href)}</td></tr></table>'
    foot = FOOT[first] if len(langs) == 1 else "Hoopline GM · hooplinegm.com"
    return f'''<!DOCTYPE html>
<html lang="{first}" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark light">
<meta name="supported-color-schemes" content="dark light">
<title>{title}</title>
</head>
<body style="margin:0;padding:0;background:{BG};" bgcolor="{BG}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:{BG};font-size:1px;line-height:1px;">{pre}&#8199;&#847;&#8199;&#847;&#8199;&#847;&#8199;&#847;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="{BG}" style="background:{BG};">
<tr><td align="center" style="padding:32px 16px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:520px;">
    <tr><td style="padding:0 4px 20px;font-family:{FONT};font-size:15px;font-weight:800;letter-spacing:3px;color:{TXT};">HOOPLINE <span style="color:{ACC};">GM</span></td></tr>
    <tr><td bgcolor="{SURF}" style="background:{SURF};border:1px solid {LINE};border-radius:20px;padding:34px 30px;">
      {body}
    </td></tr>
    <tr><td style="padding:20px 8px 0;font-family:{FONT};font-size:12px;line-height:18px;color:{MUT};text-align:center;">{foot}</td></tr>
  </table>
</td></tr>
</table>
</body>
</html>
'''

def subj_for(kind, lang):
    parts = T[kind]["subject"].split(" · ")
    return parts[["en","es","de","fr"].index(lang)]

os.makedirs(OUT, exist_ok=True)
manifest = {}
for mode in ("supabase", "own"):
    d = os.path.join(OUT, "enlace-supabase" if mode == "supabase" else "enlace-propio")
    os.makedirs(d, exist_ok=True)
    for kind in T:
        href = link(kind, mode)
        html = page(kind, ["en","es","de","fr"], href, subj_for(kind, "en"))
        open(os.path.join(d, f"{kind}.html"), "w").write(html)
        manifest[f"{mode}/{kind}"] = T[kind]["subject"]
json.dump(manifest, open(os.path.join(OUT, "subjects.json"), "w"), ensure_ascii=False, indent=1)
print("ok", len(manifest))
