import { useState, type FormEvent } from "react";
import { apiRequest, jsonBody } from "./api";

export function PasswordReset({ initialEmail, onBack }: { initialEmail: string; onBack: (message: string) => void }) {
  const [email, setEmail] = useState(initialEmail);
  const [resetToken, setResetToken] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    if (resetToken && password !== confirmation) {
      setError("The passphrases do not match.");
      return;
    }
    setBusy(true);
    try {
      if (resetToken) {
        const result = await apiRequest<{ message: string }>("/auth/password/reset/confirm",
          jsonBody({ email, reset_token: resetToken, code, new_password: password }));
        onBack(result.message);
      } else {
        const result = await apiRequest<{ reset_token: string; message: string }>("/auth/password/reset/request", jsonBody({ email }));
        setResetToken(result.reset_token);
        setMessage(result.message);
      }
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : "Could not reset your passphrase. Try again.");
    } finally {
      setBusy(false);
    }
  }

  function restart() {
    setResetToken("");
    setCode("");
    setPassword("");
    setConfirmation("");
    setMessage("");
    setError("");
  }

  return <>
    <h1>Reset your passphrase</h1>
    {message && <p role="status">{message} Enter the six-digit code within five minutes.</p>}
    {error && <p className="setup-error" role="alert">{error}</p>}
    <form onSubmit={submit}>
      <label>Owner email address
        <input type="email" autoComplete="email" maxLength={254} value={email} onChange={event => setEmail(event.target.value)} readOnly={!!resetToken} required />
      </label>
      {resetToken && <>
        <label>Email verification code
          <input inputMode="numeric" autoComplete="one-time-code" pattern="[0-9]{6}" maxLength={6} value={code} onChange={event => setCode(event.target.value)} required />
        </label>
        <label>New passphrase
          <input type="password" autoComplete="new-password" minLength={14} maxLength={128} aria-describedby="reset-passphrase-hint" value={password} onChange={event => setPassword(event.target.value)} required />
        </label>
        <small id="reset-passphrase-hint">Use 14–128 characters.</small>
        <label>Confirm new passphrase
          <input type="password" autoComplete="new-password" minLength={14} maxLength={128} value={confirmation} onChange={event => setConfirmation(event.target.value)} required />
        </label>
      </>}
      <button className="setup-primary" type="submit" disabled={busy}>{resetToken ? "Reset passphrase" : "Email me a reset code"}</button>
      {resetToken && <button type="button" onClick={restart} disabled={busy}>Start over</button>}
      <button type="button" onClick={() => onBack("")} disabled={busy}>Back to sign in</button>
    </form>
  </>;
}
