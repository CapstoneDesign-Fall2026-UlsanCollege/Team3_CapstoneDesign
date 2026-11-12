import { AccountSecurity } from "./AccountSecurity";
import { useEffect, useState } from "react";
import { apiRequest, jsonBody, type AccountSession } from "./api";
import type { BusinessProfile } from "./Onboarding";

export function Reauthentication() {
  const [password, setPassword] = useState(""); const [code, setCode] = useState("");
  const [message, setMessage] = useState(""); const [busy, setBusy] = useState(false);
  return <details className="panel reauthentication"><summary>Verify sensitive actions</summary><p className="muted">Invitations and access changes require verification within the last ten minutes.</p><button disabled={busy} onClick={async () => { setBusy(true); try { await apiRequest("/auth/mfa/resend", { method: "POST" }); setMessage("Verification code sent to your registered email."); } catch (failure) { setMessage(String(failure instanceof Error ? failure.message : failure)); } finally { setBusy(false); } }}>Send verification email</button><form onSubmit={async event => { event.preventDefault(); setBusy(true); try { await apiRequest("/auth/reauth", jsonBody({ password, code })); setPassword(""); setCode(""); setMessage("Verified. Retry the sensitive action now."); } catch (failure) { setMessage(failure instanceof Error ? failure.message : "Could not verify."); } finally { setBusy(false); } }}><label>Current passphrase<input type="password" autoComplete="current-password" value={password} onChange={event => setPassword(event.target.value)} required/></label><label>Email verification code<input autoComplete="one-time-code" value={code} onChange={event => setCode(event.target.value)} required/></label><button className="primary" disabled={busy}>Verify sensitive actions</button></form>{message && <p role="status">{message}</p>}</details>;
}

type Business = {
  id: string;
  name: string;
  active: boolean;
  owners: { email: string; activated: boolean }[];
  delete_at: number | null;
};
export function PlatformConsole({ session }: { session: AccountSession }) {
  const [businesses, setBusinesses] = useState<Business[]>([]); const [businessName, setBusinessName] = useState("");
  const [email, setEmail] = useState(""); const [ownerName, setOwnerName] = useState(""); const [store, setStore] = useState("");
  const [message, setMessage] = useState(""); const [busy, setBusy] = useState(false);
  const load = () => apiRequest<Business[]>("/platform/businesses").then(setBusinesses).catch(failure => setMessage(failure.message));
  useEffect(() => { void load(); }, []);
  const openBusiness = async (business: Business, setup: boolean) => {
    setBusy(true); try { await apiRequest("/auth/switch-business", jsonBody({ store_id: business.id })); window.location.assign(setup ? "/setup" : "/"); } catch (failure) { setMessage(failure instanceof Error ? failure.message : "Could not open business."); setBusy(false); }
  };
  const changeAccess = async (business: Business, action: "stop" | "resume" | "archive") => {
    if (action === "archive" && !window.confirm(`Archive ${business.name}? POS access stops now. The workspace and its sales history will be permanently deleted after 30 days unless restored.`)) return;
    setBusy(true);
    setMessage("");
    try {
      const path = "/platform/businesses/" + business.id;
      if (action === "archive") {
        await apiRequest(path, { method: "DELETE" });
        setMessage("Business archived. You can restore it within 30 days.");
      } else {
        await apiRequest(path + "/access", { ...jsonBody({ active: action === "resume" }), method: "PATCH" });
        setMessage(action === "resume" ? "Business access restored." : "Business POS access stopped.");
      }
      await load();
    } catch (failure) {
      setMessage(failure instanceof Error ? failure.message : "Could not update business access.");
    } finally {
      setBusy(false);
    }
  };
  return <main className="app-shell platform-console"><header><div><p className="eyebrow">SMARTSERVE PLATFORM · ADMINISTRATOR ONLY</p><h1>Your business platform</h1><p className="muted">Signed in as {session.user?.email}</p></div><button onClick={async () => { await apiRequest("/auth/logout", { method: "POST" }); window.location.assign("/"); }}>Sign out</button></header><p className="notice">Only your platform-admin account can create businesses or change presets and workflows. Each business has isolated POS data.</p>{message && <p role="status" className="notice">{message}</p>}
    <div className="management-grid"><form className="panel management-form" onSubmit={async event => { event.preventDefault(); setBusy(true); try { const created = await apiRequest<Business>("/platform/businesses", jsonBody({ name: businessName })); setBusinessName(""); setStore(created.id); await load(); setMessage("Business created. Configure its profile, then invite the owner."); } catch (failure) { setMessage(failure instanceof Error ? failure.message : "Could not create business."); } finally { setBusy(false); } }}><h2>Create a business</h2><label>Business account name<input required maxLength={120} value={businessName} onChange={event => setBusinessName(event.target.value)} /></label><button disabled={busy} className="primary">Create business</button></form>
    <form className="panel management-form" onSubmit={async event => { event.preventDefault(); setBusy(true); try { const result = await apiRequest<{ message: string }>("/platform/invitations", jsonBody({ email, name: ownerName, store_id: store, role: "owner", require_mfa: true })); setEmail(""); setOwnerName(""); setMessage(result.message); await load(); } catch (failure) { setMessage(failure instanceof Error ? failure.message : "Could not invite owner."); } finally { setBusy(false); } }}><h2>Invite a business owner</h2><label>Business<select aria-label="Business" required value={store} onChange={event => setStore(event.target.value)}><option value="">Choose a business</option>{businesses.filter(item => item.active).map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label><label>Owner name<input required maxLength={120} value={ownerName} onChange={event => setOwnerName(event.target.value)}/></label><label>Owner email<input required type="email" value={email} onChange={event => setEmail(event.target.value)}/></label><p className="muted">The owner receives an activation email for the selected business.</p><button disabled={busy} className="primary">Email owner invitation</button></form></div>
    <section className="business-account-list">
      <h2>Your businesses</h2>
      {businesses.map(item => <article className="panel business-account" key={item.id}>
        <div>
          <h3>{item.name}</h3>
          <p>{item.delete_at ? "Archived" : item.active ? "Active" : "Stopped"}</p>
          {item.delete_at && <p>Permanent deletion after {new Date(item.delete_at * 1000).toLocaleString()}.</p>}
          {item.owners.length ? <ul>{item.owners.map(owner => <li key={owner.email}>
            {owner.email} · {owner.activated ? "Passphrase set" : "Awaiting activation"}
          </li>)}</ul> : <p>No owner assigned</p>}
        </div>
        <div className="row-actions">
          {item.active && <>
            <button disabled={busy} onClick={() => void openBusiness(item, false)}>Open workspace</button>
            <button className="primary" disabled={busy} onClick={() => void openBusiness(item, true)}>Configure setup</button>
            <button disabled={busy} onClick={() => void changeAccess(item, "stop")}>Stop POS access</button>
          </>}
          {!item.active && <button disabled={busy || Boolean(item.delete_at && item.delete_at * 1000 <= Date.now())}
            onClick={() => void changeAccess(item, "resume")}>{item.delete_at ? "Restore business" : "Resume POS access"}</button>}
          {item.id !== "legacy" && !item.delete_at && <button className="danger" disabled={busy}
            onClick={() => void changeAccess(item, "archive")}>Delete business</button>}
        </div>
      </article>)}
    </section><Reauthentication/><AccountSecurity/>
  </main>;
}

type Member = { id: string; name: string; email: string; role: string; active: boolean; mfa_enabled: boolean };
export function BusinessAccountSettings({ session, profile, onChanged }: { session: AccountSession; profile: BusinessProfile; onChanged: (value: BusinessProfile) => void }) {
  const [name, setName] = useState(profile.name); const [address, setAddress] = useState(profile.address); const [phone, setPhone] = useState(profile.phone); const [footer, setFooter] = useState(profile.receipt_footer);
  const [members, setMembers] = useState<Member[]>([]); const [email, setEmail] = useState(""); const [staffName, setStaffName] = useState(""); const [requireMfa, setRequireMfa] = useState(true);
  const [activation, setActivation] = useState(""); const [message, setMessage] = useState(""); const [busy, setBusy] = useState(false);
  const load = () => apiRequest<Member[]>("/owner/staff").then(setMembers).catch(failure => setMessage(failure.message));
  useEffect(() => { void load(); }, []);
  return <section className="account-settings"><div className="management-grid"><form className="panel management-form" onSubmit={async event => { event.preventDefault(); setBusy(true); try { const value = await apiRequest<BusinessProfile>("/owner/settings", { ...jsonBody({ name, address, phone, receipt_footer: footer }), method: "PUT" }); onChanged(value); setMessage("Business details saved."); } catch (failure) { setMessage(failure instanceof Error ? failure.message : "Could not save details."); } finally { setBusy(false); } }}><h3>Business details</h3><p className="muted">Business presets and workflow changes are managed by the platform administrator.</p><label>Business display name<input required maxLength={120} value={name} onChange={event => setName(event.target.value)}/></label><label>Address<input maxLength={300} value={address} onChange={event => setAddress(event.target.value)}/></label><label>Phone<input maxLength={40} value={phone} onChange={event => setPhone(event.target.value)}/></label><label>Receipt footer<input maxLength={300} value={footer} onChange={event => setFooter(event.target.value)}/></label><button disabled={busy} className="primary">Save business details</button></form>
    <form className="panel management-form" onSubmit={async event => { event.preventDefault(); setBusy(true); setActivation(""); try { const result = await apiRequest<{ activation_url: string | null; message: string }>("/owner/staff/invitations", jsonBody({ name: staffName, email, store_id: session.store_id, role: "cashier", require_mfa: requireMfa })); setActivation(result.activation_url || ""); setMessage(result.message); await load(); } catch (failure) { setMessage(failure instanceof Error ? failure.message : "Could not invite cashier."); } finally { setBusy(false); } }}><h3>Invite a cashier</h3><label>Staff name<input required value={staffName} maxLength={120} onChange={event => setStaffName(event.target.value)}/></label><label>Staff email<input required type="email" value={email} onChange={event => setEmail(event.target.value)}/></label><label className="inline-check"><input type="checkbox" checked={requireMfa} onChange={event => setRequireMfa(event.target.checked)}/>Require email verification for this cashier</label><button disabled={busy} className="primary">Create private staff invitation</button></form></div>{message && <p role="status" className="notice">{message}</p>}{activation && <section className="panel private-invitation"><h3>Private one-use staff invitation</h3><p>No email has been sent. Share only with the named staff member.</p><textarea readOnly aria-label="Private staff activation link" value={activation}/><button onClick={() => void navigator.clipboard.writeText(activation)}>Copy private link</button></section>}
    <section className="panel"><h3>Business accounts</h3>{members.map(item => <div className="management-row" key={item.id}><div><strong>{item.name}</strong><small>{item.email} · {item.role} · {item.active ? "Active" : "Disabled"}</small></div>{item.role === "cashier" && <button disabled={busy} onClick={async () => { setBusy(true); try { await apiRequest(`/owner/staff/${item.id}/access`, { ...jsonBody({ active: !item.active }), method: "PUT" }); await load(); setMessage("Staff access updated. Existing staff sessions were revoked."); } catch (failure) { setMessage(failure instanceof Error ? failure.message : "Could not update access."); } finally { setBusy(false); } }}>{item.active ? "Disable access" : "Enable access"}</button>}</div>)}</section><Reauthentication/>
  </section>;
}
