import type { ReactNode } from "react";
import { apiFetch } from "./api";
import { useState } from "react";
const API = import.meta.env.PROD ? "" : "http://localhost:8000";
export type BusinessProfile = { name: string; business_type: string; currency: string; operation_mode: string; features: string[]; order_types: string[]; address: string; phone: string; logo_url: string; receipt_footer: string; table_count: number; onboarding_complete: boolean };
export type BusinessSetupInput = Pick<BusinessProfile, "name" | "business_type" | "operation_mode" | "features" | "address" | "phone" | "logo_url" | "receipt_footer" | "table_count"> & { catalog_action: string };
export const businessLabels: Record<string, string> = { cafe: "Café", restaurant: "Restaurant", bakery: "Bakery & desserts", retail: "Retail shop", grocery: "Grocery & convenience", barbershop: "Barbershop", beauty: "Salon & beauty", repair: "Repair & workshop", services: "Professional services", custom: "Custom setup" };
export const orderLabels: Record<string, string> = { dine_in: "Table service", takeaway: "Takeaway", in_store: "In store", pickup: "Pickup", service: "Service" };
export const defaultBusiness: BusinessProfile = { name: "SmartServe POS", business_type: "cafe", currency: "KRW", operation_mode: "both", features: ["checkout", "inventory", "tables"], order_types: ["dine_in", "takeaway"], address: "", phone: "", logo_url: "", receipt_footer: "Thank you for your visit!", table_count: 8, onboarding_complete: false };
const descriptions: Record<string, string> = { cafe: "Coffee, quick orders & a place to stay", restaurant: "Meals, open tables & takeaway orders", bakery: "Fresh bakes, sweet treats & counter sales", retail: "Products, stock & a fast checkout", grocery: "Daily essentials & pickup orders", barbershop: "Walk-ins, appointments & grooming", beauty: "Appointments, treatments & beauty products", repair: "Drop-offs, repair jobs & collection", services: "Consultations, bookings & service sales", custom: "Start with a blank canvas. Make it your own." };
const icons: Record<string, string> = { cafe: "☕", restaurant: "🍽", bakery: "◒", retail: "▣", grocery: "◈", barbershop: "✂", beauty: "✧", repair: "⚙", services: "◇", custom: "+" };
const featureLabels: Record<string, string> = { checkout: "Checkout", inventory: "Stock & inventory", tables: "Tables & open bills", appointments: "Appointments", walk_ins: "Walk-in queue", jobs: "Repair jobs" };
function modesFor(type: string): { id: string; title: string; detail: string }[] {
  if (["cafe", "restaurant", "bakery"].includes(type)) return [{ id: "takeaway", title: "Takeaway only", detail: "Quick counter sales, without tables" }, { id: "tables", title: "Table service only", detail: "Assign tables and hold open bills" }, { id: "both", title: "Takeaway + tables", detail: "Both workflows in one place" }];
  if (["retail", "grocery"].includes(type)) return [{ id: "in_store", title: "In-store sales", detail: "Sell products over the counter" }, { id: "pickup", title: "Pickup orders", detail: "Save orders ready for collection" }, { id: "both", title: "In store + pickup", detail: "One catalog for both order types" }];
  if (["barbershop", "beauty"].includes(type)) return [{ id: "walk_ins", title: "Walk-ins only", detail: "Manage a queue and service checkout" }, { id: "appointments", title: "Appointments only", detail: "Book staff and prevent overlapping times" }, { id: "both", title: "Walk-ins + appointments", detail: "Manage bookings and your queue together" }];
  if (type === "repair") return [{ id: "immediate", title: "While-you-wait service", detail: "Take payment for immediate work" }, { id: "jobs", title: "Repair jobs", detail: "Track drop-off, work, ready and collection" }, { id: "both", title: "Immediate service + jobs", detail: "Quick checkout and a job board" }];
  if (type === "services") return [{ id: "immediate", title: "Immediate service", detail: "Fixed-price services and checkout" }, { id: "appointments", title: "By appointment", detail: "Schedule time with your customers" }, { id: "both", title: "Both", detail: "Scheduled work and immediate service" }];
  return [{ id: "custom", title: "Build my own workflow", detail: "Choose the tools your business actually needs" }];
}
function featuresFor(type: string, mode: string) {
  return ["checkout", "inventory", ...(["cafe", "restaurant", "bakery"].includes(type) && mode !== "takeaway" ? ["tables"] : []), ...(["barbershop", "beauty", "services"].includes(type) && ["appointments", "both"].includes(mode) ? ["appointments"] : []), ...(["barbershop", "beauty"].includes(type) && ["walk_ins", "both"].includes(mode) ? ["walk_ins"] : []), ...(type === "repair" && ["jobs", "both"].includes(mode) ? ["jobs"] : [])];
}
export function BusinessSetup({ profile, onChanged, onClose, onSave, ownerFields, reauthentication }: { profile: BusinessProfile; onChanged: (profile: BusinessProfile) => Promise<void>; onClose?: () => void; onSave?: (setup: BusinessSetupInput) => Promise<BusinessProfile>; ownerFields?: ReactNode; reauthentication?: ReactNode }) {
  const [step, setStep] = useState(0);
  const [type, setType] = useState(profile.onboarding_complete ? profile.business_type : "");
  const [mode, setMode] = useState(profile.operation_mode);
  const [name, setName] = useState(profile.name === "SmartServe POS" ? "" : profile.name);
  const [address, setAddress] = useState(profile.address);
  const [phone, setPhone] = useState(profile.phone);
  const [logo, setLogo] = useState(profile.logo_url);
  const [footer, setFooter] = useState(profile.receipt_footer);
  const [tables, setTables] = useState(profile.table_count);
  const [customFeatures, setCustomFeatures] = useState(profile.features);
  const [catalog, setCatalog] = useState("keep");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);
  const features = type === "custom" ? customFeatures : featuresFor(type, mode);
  const titles = ["Your business", "Your workflow", "Details & review"];
  const next = () => { setError(""); if (step === 0 && !type) return setError("Choose a business to continue."); setStep(value => Math.min(2, value + 1)); };
  const save = async () => {
    if (!name.trim()) { setError("Enter your business name."); return; }
    setBusy(true); setError("");
    try {
      const payload: BusinessSetupInput = { name: name.trim(), business_type: type, operation_mode: mode, features, address, phone, logo_url: logo, receipt_footer: footer, table_count: tables, catalog_action: catalog };
      let savedProfile: BusinessProfile;
      if (onSave) savedProfile = await onSave(payload);
      else {
        const response = await apiFetch(`${API}/owner/business/setup`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
        const result = await response.json();
        if (!response.ok) throw new Error(typeof result.detail === "string" ? result.detail : "Check your profile details and logo URL, then try again.");
        savedProfile = result.profile;
      }
      await onChanged(savedProfile); setDone(true);
    } catch (failure) { setError(failure instanceof Error ? failure.message : "Could not save setup."); }
    finally { setBusy(false); }
  };
  return <main className="setup-shell">
    <aside className="setup-sidebar"><a href="/" className="setup-brand"><span>S</span> SmartServe</a><div><p className="setup-kicker">MADE FOR THE WAY YOU WORK</p><h1>Your business.<br/>Your kind of POS.</h1><p>Three simple steps to a workspace that feels like yours.</p></div><ol aria-label="Setup steps">{titles.map((title, index) => <li aria-current={index === step ? "step" : undefined} className={index === step ? "current" : index < step ? "finished" : ""} key={title}><span>{index < step ? "✓" : String(index + 1).padStart(2, "0")}</span>{title}</li>)}</ol><small>One store · editable by your platform admin<br/>Your sales history stays yours.</small></aside>
    <section className="setup-content"><div className="setup-topline"><span>SETUP / {String(step + 1).padStart(2, "0")} OF 03</span>{onClose && <button type="button" disabled={busy} onClick={onClose}>Back to workspace</button>}</div>
      {done ? <div className="setup-success"><div className="success-mark">✓</div><p className="setup-kicker">YOU’RE ALL SET</p><h2>{name}, ready for business.</h2><p>Your profile and workflows are saved. Start selling or make the catalog your own.</p><a className="setup-primary" href="/">Open my POS →</a></div> : <>
      <div className="setup-heading"><p className="setup-kicker">{["LET’S START WITH YOU", "MAKE IT FIT", "MAKE IT YOURS"][step]}</p><h2>{["What kind of business are you building?", "How do you serve your customers?", "Make it yours. Then you’re ready."][step]}</h2><p>{["Pick a starting point. You can change your profile later.", "We’ll show the tools that match the way you work.", "Add your business details, choose your catalog, and review everything here."][step]}</p></div>
      {error && <p className="setup-error" role="alert">{error}</p>}
      {error && reauthentication}
      {step === 0 && <div className="business-choice-grid">{Object.entries(businessLabels).map(([id, label]) => <button className={"business-choice " + (type === id ? "selected" : "")} aria-pressed={type === id} key={id} onClick={() => { setType(id); setMode(modesFor(id)[0].id); if (id === "custom") setCatalog("empty"); }}><span className="business-choice-icon">{icons[id]}</span><strong>{label}</strong><small>{descriptions[id]}</small><span className="choice-check" aria-hidden="true">{type === id ? "✓" : ""}</span></button>)}</div>}
      {step === 1 && <><div className="workflow-choices">{modesFor(type).map(option => <button className={"workflow-choice " + (mode === option.id ? "selected" : "")} aria-pressed={mode === option.id} key={option.id} onClick={() => setMode(option.id)}><span className="choice-radio"/><span><strong>{option.title}</strong><small>{option.detail}</small></span></button>)}</div>{type === "custom" && <fieldset className="custom-features"><legend>Choose your tools</legend>{Object.entries(featureLabels).map(([id, label]) => <label key={id}><input type="checkbox" checked={customFeatures.includes(id)} disabled={id === "checkout"} onChange={event => setCustomFeatures(current => event.target.checked ? [...current, id] : current.filter(value => value !== id))}/>{label}</label>)}</fieldset>}{features.includes("tables") && <label className="setup-table-count">How many tables?<input type="number" min={1} max={50} value={tables} onChange={event => setTables(Math.max(1, Math.min(50, Number(event.target.value) || 1)))}/></label>}<div className="setup-tool-strip">YOUR WORKSPACE{features.map(feature => <span key={feature}>{featureLabels[feature]}</span>)}</div></>}
      {step === 2 && <div className="setup-final-layout">
        <div className="profile-fields">
          <label>Business name<input required maxLength={120} value={name} onChange={event => setName(event.target.value)} placeholder="e.g. Sunday Coffee or The Local Barber" autoComplete="organization" /></label>
          {ownerFields}
          <label>Business address<input maxLength={300} value={address} onChange={event => setAddress(event.target.value)} placeholder="Street, city" autoComplete="street-address" /></label>
          <div className="form-pair"><label>Phone (optional)<input type="tel" maxLength={40} value={phone} onChange={event => setPhone(event.target.value)} autoComplete="tel" /></label><label>Currency<input value="KRW · South Korean won" readOnly/><small>Current checkout currency</small></label></div>
          <label>Logo image URL (optional)<input type="url" maxLength={2048} value={logo} onChange={event => setLogo(event.target.value)} placeholder="https://example.com/logo.png" /></label>
          <label>Receipt message<input maxLength={300} value={footer} onChange={event => setFooter(event.target.value)} /></label>
        </div>
        <div className="setup-final-options">
          <section className="setup-catalog" aria-labelledby="setup-catalog-title">
            <h3 id="setup-catalog-title">Choose your starting catalog</h3>
            <div className="workflow-choices">{[
              { id: "keep", title: "Keep my current catalog", detail: "Keep existing products, services and stock." },
              ...(type !== "custom" ? [{ id: "samples", title: "Start with editable sample items", detail: "Try items for this business. Review sample prices and stock before selling." }] : []),
              { id: "empty", title: "Start with an empty catalog", detail: "Add your own products and services." }
            ].map(option => <button key={option.id} className={"workflow-choice " + (catalog === option.id ? "selected" : "")} aria-pressed={catalog === option.id} onClick={() => setCatalog(option.id)}><span className="choice-radio"/><span><strong>{option.title}</strong><small>{option.detail}</small></span></button>)}</div>
            <p className="muted">Changing catalogs archives existing items and preserves sales history and stock.</p>
          </section>
          <section className="setup-review" aria-label="Setup summary">
            <p className="setup-kicker">YOUR WORKSPACE AT A GLANCE</p>
            <h3>{name.trim() || "Your business"}</h3>
            <p>{businessLabels[type]} · {modesFor(type).find(option => option.id === mode)?.title}</p>
            <div className="review-tools">{features.map(feature => <span key={feature}>✓ {featureLabels[feature]}</span>)}</div>
            <p>{features.includes("tables") ? tables + " tables · " : ""}KRW · {catalog === "keep" ? "Keep current items" : catalog === "samples" ? "Editable sample items" : "Empty catalog"}</p>
            <small>Payments are simulated. Settle open bills before changing an existing setup.</small>
          </section>
        </div>
      </div>}
      <footer className="setup-footer"><button disabled={busy || step === 0} onClick={() => { setError(""); setStep(value => value - 1); }}>← Back</button><span>{step + 1} of 3</span>{step < 2 ? <button className="setup-primary" onClick={next}>Continue →</button> : <button className="setup-primary" disabled={busy} onClick={() => void save()}>{busy ? "Creating your workspace…" : "Create my workspace →"}</button>}</footer>
      </>}
    </section>
  </main>;
}
