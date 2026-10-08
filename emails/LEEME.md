# Plantillas de email de Hoopline GM (Supabase), versión 2

Cada plantilla lleva los cuatro idiomas en un solo correo (EN arriba; ES, DE y FR debajo), porque Supabase solo admite UNA plantilla por tipo.
Cambios de la v2: enlace-propio ya lleva `https://hooplinegm.com` fijo (no usa tu Site URL) y la recuperación de contraseña apunta a
`/auth/confirm?...&type=recovery` (sin `next`). El francés pasa a "vous", como la ficha de App Store.

## Qué carpeta usar
- enlace-supabase/  →  botón con {{ .ConfirmationURL }}. Funciona ya con tu configuración actual.
- enlace-propio/    →  botón a hooplinegm.com/auth/confirm. **Úsala solo cuando la landing esté publicada** y la página responda.

## Dónde pegar cada una
Supabase → Authentication → Emails → Templates: HTML en "Message body", asunto en "Subject".
| Plantilla de Supabase | Archivo | Asunto |
|---|---|---|
| Confirm sign up | confirm_signup.html | Confirm your email · Confirma tu correo · Bestätige deine E-Mail · Confirmez votre e-mail |
| Reset password | recovery.html | Reset your password · Restablece tu contraseña · Passwort zurücksetzen · Réinitialisez votre mot de passe |
| Change email address | email_change.html | Confirm your new email · Confirma tu nuevo correo · Neue E-Mail bestätigen · Confirmez votre nouvel e-mail |
| Magic link | magic_link.html | Your sign-in link · Tu enlace de acceso · Dein Anmeldelink · Votre lien de connexion |
| Reauthentication | reauthentication.html | Your confirmation code · Tu código de confirmación · Dein Bestätigungscode · Votre code de confirmation |
