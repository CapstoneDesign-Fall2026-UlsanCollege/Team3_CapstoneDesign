# Secure accounts and Gmail authorization

This branch replaces the shared demo login with individual, invitation-only accounts. The Render site is not protected by these changes until this branch is deployed with the required secrets. Never deploy with test mode enabled.

## Roles

| Role | Access |
|---|---|
| Platform administrator | Creates businesses, runs setup/presets, selects business workspaces, assigns owners, and reads platform audit events |
| Owner | Own business sales, catalog, stock, everyday details, staff invitations/access, and operational tools |
| Cashier | Own business checkout, orders, stock availability, tables, appointments/queue/jobs enabled by the administrator |

Setup APIs are restricted to the platform administrator. No API or public signup can create another platform administrator. A database constraint permits one platform administrator. Owner and cashier identities cannot select a business without a membership. Sessions are bound to a server-selected business namespace, not a browser-supplied business header or query parameter.

PostgreSQL uses separate `store_<id>` schemas for each business. Local SQLite uses separate database files. The original store remains in the existing database as the `legacy` business; it is not assigned to an arbitrary account. The platform administrator can select it and invite its owner. Back up the database before migrating production.

## Two-factor authentication and sessions

Everyone signs in at the app's home page. The configured platform administrator can create and switch businesses. From the platform console, select a business and use **Email owner invitation**. The owner receives a one-use activation link, sets a passphrase, and verifies their email. New business invitations require a separate email for each workspace. To resend a pending owner invitation, submit the same email and business again.

Admins and owners must enter a passphrase plus a code delivered to their registered email. Owners can require email codes for cashiers (enabled by default in the staff invitation UI). Codes expire after five minutes, are bound to a session and purpose, accept at most five guesses, and work once. Resending is limited and invalidates the prior code. Ten random recovery codes are displayed once after first verification; each is usable once with the correct passphrase.

Passwords use Argon2id. Cookies are opaque, HttpOnly, SameSite=Strict, host-only, and Secure in production. Session tokens and invitations are stored as hashes. Server-side expiry, idle limits, revocation, CSRF checks, origin checks, role checks, and audit events are enforced. Switching businesses rotates the token without refreshing the original MFA time or absolute expiry. Invitations/access changes require verification in the last ten minutes. Password changes revoke earlier sessions.

Email codes are not phishing-resistant. Protect the sending Gmail account and every owner's inbox with Google's/account-provider MFA. Never reuse the Google password as the SmartServe passphrase. No claim of a production security audit, regulatory certification, or protection against every attack is made.

## Gmail API on Render Free

Render Free blocks SMTP ports 25, 465 and 587. This deployment sends via the Gmail HTTPS API, not an app password. Only the sending Google account authorizes OAuth; owners and cashiers only receive emails and do not grant inbox access.

1. In [Google Cloud Console](https://console.cloud.google.com/), create/select a project and enable the **Gmail API**.
2. Configure **Google Auth Platform** branding/audience/data access. During testing, add the sender account as a test user.
3. Create an **OAuth client ID → Desktop app** and download its client JSON into a private location outside Git. Do not upload it to chat or commit it.
4. From the repository root, run:

```powershell
uv run --with-requirements smartserve-pos/backend/requirements-admin.txt python smartserve-pos/backend/manage_security.py configure-gmail-api --client-secrets "C:\private\google-client.json" --email "YOUR_ADMIN_GMAIL"
```

The helper opens your normal browser. Select the exact sender/admin account and approve send-only Gmail permission plus identity/email verification. PKCE and Google's verified ID token bind the authorization to the requested account. It does not request inbox-read permission. It saves a protected `.smartserve-local/security-config.json` and does not print refresh/access tokens.

Google apps left in **Testing** issue Gmail refresh tokens that generally expire after seven days. Before relying on this for ongoing sign-in, follow Google's production/publishing and sensitive-scope verification requirements as applicable; do not treat a temporary test authorization as permanent mail delivery. Do not grant broader Gmail scopes to bypass verification.

## Local activation

After Gmail authorization, create your one-use private activation link:

```powershell
uv run --with-requirements smartserve-pos/backend/requirements.txt python smartserve-pos/backend/manage_security.py bootstrap-admin --output "D:\private\smartserve-admin-activation.txt"
```

Use the same `DATABASE_URL` as the local server. Open the link privately, choose your own passphrase, verify the email code, and save recovery codes offline. Bootstrap refuses to replace an existing administrator or escalate a business account. Link files expire after 24 hours and are not passwords.

## Render configuration and first admin

Export protected environment values (never a repository file):

```powershell
uv run --with-requirements smartserve-pos/backend/requirements.txt python smartserve-pos/backend/manage_security.py export-render-env --origin "https://YOUR-SERVICE.onrender.com" --output "D:\private\render-security.env"
```

Import these values into the existing Render service's protected environment settings before deployment. Keep the existing database URL. The required names are:

- `SMARTSERVE_ENV=production`
- `SMARTSERVE_AUTH_SECRET` (persistent random value, at least 32 characters)
- `SMARTSERVE_PLATFORM_ADMIN_EMAIL` (the sole admin email)
- `SMARTSERVE_BOOTSTRAP_ADMIN=true`
- `SMARTSERVE_PUBLIC_ORIGIN` (the service's HTTPS origin)
- `MAIL_PROVIDER=gmail_api`
- `GMAIL_SENDER`, `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`

Render is also detected as production automatically. Missing production authentication secrets prevent startup. On first properly configured startup, the server emails a one-use activation link only to the configured admin. No Render shell is required. It never auto-reassigns an existing admin. An unactivated, expired invitation can be reissued to that same address on a later restart; once a passphrase is set, automatic account creation stays closed.

Remove obsolete `SMARTSERVE_OWNER_USERNAME`, `SMARTSERVE_OWNER_PASSWORD`, `SMARTSERVE_OWNER_PASSWORD_SHA256` and `SMARTSERVE_SESSION_SECRET` settings. They no longer authenticate anyone. Old shared-owner cookies are ignored. Users must sign in using their individual accounts.

## Tests and operating limits

Install `backend/requirements-dev.txt` for the backend suite. `verify_business.py` provisions an isolated administrator, sends to an ephemeral **test-only** outbox, and exercises the actual login, MFA, owner invitation, staff invitation, setup and checkout screens. Outboxes are refused outside explicit test mode; no HTTP endpoint exposes a test code. `test_security.py` tests isolation, replay/guess limits, revocation, CSRF, role escalation attempts, recovery, and private bootstrap. Gmail HTTPS requests are tested with mocks; actual Google authorization and delivery require your credentials and consent.

Identity migrations currently use additive tables. Future domain-column migrations must be applied to every business schema, not only `public`. The app uses one database role; schema isolation does not replace database backups, restricted database/network access, patching, monitoring, or a dedicated production security review. Google authorization secrets, administrator activation files, recovery codes and test outboxes must stay outside version control and shared artifacts.

References: [Google sending guide](https://developers.google.com/workspace/gmail/api/guides/sending), [Google OAuth](https://developers.google.com/identity/protocols/oauth2/), [Render Free limitations](https://render.com/docs/free), [OWASP MFA](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html), [OWASP sessions](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).
