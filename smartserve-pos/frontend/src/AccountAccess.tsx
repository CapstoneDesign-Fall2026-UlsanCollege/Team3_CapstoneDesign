import { useEffect, useRef, useState, type ReactNode } from "react";
import { apiRequest, jsonBody, type AccountSession } from "./api";

import { PasswordReset } from "./PasswordReset";

export function AccountAccess({ children }: { children: (session: AccountSession) => ReactNode }) {
  const [session, setSession] = useState<AccountSession | null>(null);
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [businessName, setBusinessName] = useState("");
  const [signupSubmitted, setSignupSubmitted] = useState(false);
  const [password, setPassword] = useState("");
  const [resetting, setResetting] = useState(false);
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
  async function requestSignup() {
    setBusy(true); setError(""); setMessage("");
    try {
      const result = await apiRequest<{ message: string }>("/auth/register", jsonBody({ email, business_name: businessName.trim() }));
      setSignupSubmitted(true);
      setResendAt(Date.now() + 60000);
      setMessage(result.message);
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : "Could not request an account.");
    } finally { setBusy(false); }
  }
  const challenge = session?.challenge === "verify_email";
  const registering = window.location.pathname.replace(/\/+$/, "") === "/register" && !challenge;
  if (!session) return <main className="auth-page"><p role="status">Checking your secure session…</p></main>;
  if (session.authenticated && !recovery.length) return <>{children(session)}</>;
  return <main className="auth-page"><a className="setup-brand" href="/"><span>S</span> SmartServe</a><section className="auth-card">
    {resetting ? <PasswordReset initialEmail={email} onBack={result => { setResetting(false); setMessage(result); }} /> : <>
    <p className="setup-kicker">YOUR BUSINESS, PROTECTED</p><h1>{recovery.length ? "Keep your recovery codes safe." : challenge ? "Check your email." : invitation ? "Activate your SmartServe account" : registering ? (signupSubmitted ? "Check your inbox" : "Create your business") : "Welcome back."}</h1>
    <p className="muted">{recovery.length ? "Save these one-use codes offline. You will need your passphrase as well if email is unavailable." : challenge ? `Enter the code sent to ${session.user?.email}. It expires in five minutes.` : invitation ? "Choose a private passphrase to activate your account." : registering ? (signupSubmitted ? "Open the latest signup link within 30 minutes. If it hasn’t arrived, check Spam or resend below." : "Use your email address to create an owner account and set up your own workspace.") : "Sign in to the workspace your account is authorized to use."}</p>
    {error && <p className="setup-error" role="alert">{error}</p>}{message && <p className="notice" role="status">{message}</p>}
    {recovery.length ? <><div className="recovery-codes">{recovery.map(value => <code key={value}>{value}</code>)}</div><button onClick={() => { const blob = new Blob(["SmartServe one-use recovery codes\nKeep offline and private.\n\n" + recovery.join("\n")], { type: "text/plain" }); const url = URL.createObjectURL(blob); const link = document.createElement("a"); link.href = url; link.download = "smartserve-recovery-codes.txt"; link.click(); URL.revokeObjectURL(url); }}>Download recovery codes</button><label className="inline-check"><input type="checkbox" checked={saved} onChange={event => setSaved(event.target.checked)}/>I have saved my recovery codes privately</label><button className="setup-primary" disabled={!saved} onClick={() => window.location.replace("/login")}>Enter my workspace →</button></> : registering ? (signupSubmitted ?
      <div className="signup-next">
        <p><strong>Email address</strong><br/>{email}</p>
        <button className="setup-primary" type="button" disabled={busy || clock < resendAt} onClick={() => void requestSignup()}>
          {clock < resendAt ? `Resend in ${Math.ceil((resendAt - clock) / 1000)}s` : "Resend signup link"}
        </button>
        <button type="button" disabled={busy} onClick={() => { setSignupSubmitted(false); setMessage(""); setError(""); }}>Change email address</button>
      </div> :
      <form onSubmit={event => { event.preventDefault(); void requestSignup(); }}>
        <label>Business name<input maxLength={120} autoComplete="organization" value={businessName} onChange={event => setBusinessName(event.target.value)} required/></label>
        <label>Email address<input type="email" maxLength={254} autoComplete="email" value={email} onChange={event => setEmail(event.target.value)} required/></label>
        <button className="setup-primary" disabled={busy}>Email me a signup link</button>
      </form>) : <form onSubmit={async event => { event.preventDefault(); setBusy(true); setError(""); setMessage(""); try {
      if (challenge) {
        const result = await apiRequest<{ recovery_codes: string[] }>("/auth/mfa/verify", jsonBody({ code }));
        setCode(""); if (result.recovery_codes?.length) setRecovery(result.recovery_codes); await refresh();
      } else {
        const result = await apiRequest<{ authenticated: boolean; email_sent: boolean; challenge?: string }>(invitation ? "/auth/activate" : "/auth/login", jsonBody(invitation ? { token: invitation, name, password } : { email, password }));
        setPassword(""); setInvitation(""); await refresh();
        if (result.challenge) { setResendAt(Date.now() + 60000); if (!result.email_sent) setError("The email could not be delivered. Try resending it or use a saved recovery code."); }
      }
    } catch (failure) { setError(failure instanceof Error ? failure.message : "Could not sign in."); } finally { setBusy(false); } }}>
      {challenge ? <label>Email code or one-use recovery code<input autoComplete="one-time-code" value={code} maxLength={100} onChange={event => setCode(event.target.value)} required autoFocus/></label> : <>{invitation ? <label>Your name<input maxLength={120} value={name} onChange={event => setName(event.target.value)} autoComplete="name" required/></label> : <label>Email address<input type="email" maxLength={254} value={email} onChange={event => setEmail(event.target.value)} autoComplete="username" required/></label>}<label>Passphrase<input aria-label="Passphrase" type="password" minLength={invitation ? 14 : 1} maxLength={128} value={password} onChange={event => setPassword(event.target.value)} autoComplete={invitation ? "new-password" : "current-password"} required/>{invitation && <small>Use 14–128 characters. A long, unique passphrase is best.</small>}</label></>}
      <button className="setup-primary" disabled={busy} type="submit">{busy ? "Verifying…" : challenge ? "Verify & sign in" : invitation ? "Activate my account" : "Sign in"}</button>
      {challenge && <><button type="button" disabled={busy || clock < resendAt} onClick={async () => { setBusy(true); setError(""); try { await apiRequest("/auth/mfa/resend", { method: "POST" }); setResendAt(Date.now() + 60000); setMessage("A new code was sent. The previous code no longer works."); } catch (failure) { setError(failure instanceof Error ? failure.message : "Could not resend."); } finally { setBusy(false); } }}>{clock < resendAt ? `Resend in ${Math.ceil((resendAt - clock) / 1000)}s` : "Resend email code"}</button><button type="button" disabled={busy} onClick={async () => { await apiRequest("/auth/logout", { method: "POST" }); window.location.assign("/login"); }}>Use a different account</button></>}
    </form>}
    {!challenge && !invitation && !recovery.length && <p className="auth-footnote">{registering ? <a href="/login">Sign in to an existing account</a> : <a href="/register">Create your own business</a>}</p>}
    {!challenge && !invitation && !recovery.length && !registering && <button type="button" disabled={busy} onClick={() => { setPassword(""); setError(""); setMessage(""); setResetting(true); }}>Forgot password?</button>}
    </>}
  </section></main>;
}
