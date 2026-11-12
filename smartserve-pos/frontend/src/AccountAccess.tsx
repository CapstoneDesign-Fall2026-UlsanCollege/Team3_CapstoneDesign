import { useEffect, useRef, useState, type ReactNode } from "react";
import { apiRequest, jsonBody, type AccountSession } from "./api";

export function AccountAccess({ children }: { children: (session: AccountSession) => ReactNode }) {
  const [session, setSession] = useState<AccountSession | null>(null);
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [recovery, setRecovery] = useState<string[]>([]);
  const [saved, setSaved] = useState(false);
  const [resendAt, setResendAt] = useState(0);
  const [clock, setClock] = useState(Date.now());
  const [invitation, setInvitation] = useState(() => window.location.pathname === "/activate" ? window.location.hash.slice(1) : "");
  const activity = useRef(Date.now());
  const refresh = () => apiRequest<AccountSession>("/auth/session").then(setSession).catch(() => { setSession({ authenticated: false }); setError("Could not check your session. Refresh to retry."); });
  useEffect(() => {
    if (invitation) history.replaceState(null, "", "/activate");
    void refresh();
    const expired = () => { setSession({ authenticated: false }); setError("Your session ended. Please sign in again."); setPassword(""); setCode(""); };
    window.addEventListener("smartserve:session-expired", expired);
    return () => window.removeEventListener("smartserve:session-expired", expired);
  }, []);
  useEffect(() => {
    const touch = () => { activity.current = Date.now(); };
    window.addEventListener("pointerdown", touch); window.addEventListener("keydown", touch);
    const timer = window.setInterval(() => {
      setClock(Date.now());
      const idle = session?.user?.role === "platform_admin" ? 15 * 60000 : 30 * 60000;
      if (session?.authenticated && Date.now() - activity.current >= idle) {
        void apiRequest("/auth/logout", { method: "POST" }).finally(() => { setSession({ authenticated: false }); setError("Signed out after inactivity."); });
      }
    }, 1000);
    return () => { clearInterval(timer); window.removeEventListener("pointerdown", touch); window.removeEventListener("keydown", touch); };
  }, [session?.authenticated, session?.user?.role]);
  const challenge = session?.challenge === "verify_email";
  if (!session) return <main className="auth-page"><p role="status">Checking your secure session…</p></main>;
  if (session.authenticated && !recovery.length) return <>{children(session)}</>;
  return <main className="auth-page"><a className="setup-brand" href="/"><span>S</span> SmartServe</a><section className="auth-card">
    <p className="setup-kicker">YOUR BUSINESS, PROTECTED</p><h1>{recovery.length ? "Keep your recovery codes safe." : challenge ? "Check your email." : invitation ? "Your invitation to SmartServe." : "Sign in to SmartServe"}</h1>
    <p className="muted">{recovery.length ? "Save these one-use codes offline. You will need your passphrase as well if email is unavailable." : challenge ? `Enter the code sent to ${session.user?.email}. It expires in five minutes.` : invitation ? "Choose a private passphrase. Admins and owners verify their email before entering the workspace." : "Sign in to the workspace your account is authorized to use."}</p>
    {error && <p className="setup-error" role="alert">{error}</p>}{message && <p className="notice" role="status">{message}</p>}
    {recovery.length ? <><div className="recovery-codes">{recovery.map(value => <code key={value}>{value}</code>)}</div><button onClick={() => { const blob = new Blob(["SmartServe one-use recovery codes\nKeep offline and private.\n\n" + recovery.join("\n")], { type: "text/plain" }); const url = URL.createObjectURL(blob); const link = document.createElement("a"); link.href = url; link.download = "smartserve-recovery-codes.txt"; link.click(); URL.revokeObjectURL(url); }}>Download recovery codes</button><label className="inline-check"><input type="checkbox" checked={saved} onChange={event => setSaved(event.target.checked)}/>I have saved my recovery codes privately</label><button className="setup-primary" disabled={!saved} onClick={() => window.location.assign("/")}>Enter my workspace →</button></> : <form onSubmit={async event => { event.preventDefault(); setBusy(true); setError(""); setMessage(""); try {
      if (challenge) {
        const result = await apiRequest<{ recovery_codes: string[] }>("/auth/mfa/verify", jsonBody({ code }));
        setCode(""); if (result.recovery_codes?.length) setRecovery(result.recovery_codes); await refresh();
      } else {
        const result = await apiRequest<{ authenticated: boolean; email_sent: boolean; challenge?: string }>(invitation ? "/auth/activate" : "/auth/login", jsonBody(invitation ? { token: invitation, name, password } : { email, password }));
        setPassword(""); setInvitation(""); await refresh();
        if (result.challenge) { setResendAt(Date.now() + 60000); if (!result.email_sent) setError("The email could not be delivered. Authorize the Gmail sender, resend, or use a saved recovery code."); }
      }
    } catch (failure) { setError(failure instanceof Error ? failure.message : "Could not sign in."); } finally { setBusy(false); } }}>
      {challenge ? <label>Email code or one-use recovery code<input autoComplete="one-time-code" value={code} maxLength={100} onChange={event => setCode(event.target.value)} required autoFocus/></label> : <>{invitation ? <label>Your name<input maxLength={120} value={name} onChange={event => setName(event.target.value)} autoComplete="name" required/></label> : <label>Email address<input type="email" maxLength={254} value={email} onChange={event => setEmail(event.target.value)} autoComplete="username" required/></label>}<label>Passphrase<input aria-label="Passphrase" type="password" minLength={invitation ? 14 : 1} maxLength={128} value={password} onChange={event => setPassword(event.target.value)} autoComplete={invitation ? "new-password" : "current-password"} required/>{invitation && <small>Use 14–128 characters. A long, unique passphrase is best.</small>}</label></>}
      <button className="setup-primary" disabled={busy} type="submit">{busy ? "Verifying…" : challenge ? "Verify & sign in" : invitation ? "Activate my account" : "Sign in"}</button>
      {challenge && <><button type="button" disabled={busy || clock < resendAt} onClick={async () => { setBusy(true); setError(""); try { await apiRequest("/auth/mfa/resend", { method: "POST" }); setResendAt(Date.now() + 60000); setMessage("A new code was sent. The previous code no longer works."); } catch (failure) { setError(failure instanceof Error ? failure.message : "Could not resend."); } finally { setBusy(false); } }}>{clock < resendAt ? `Resend in ${Math.ceil((resendAt - clock) / 1000)}s` : "Resend email code"}</button><button type="button" disabled={busy} onClick={async () => { await apiRequest("/auth/logout", { method: "POST" }); window.location.assign("/"); }}>Use a different account</button></>}
    </form>}
    <p className="auth-footnote">Accounts are invitation-only. No public administrator registration. Never share a passphrase, email code or recovery code.</p>
  </section></main>;
}
