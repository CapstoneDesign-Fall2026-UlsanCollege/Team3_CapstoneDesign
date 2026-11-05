import { useEffect, useState } from "react";
const API = import.meta.env.PROD ? "" : "http://localhost:8000";
export type WorkTicket = { id: number; kind: string; title: string; customer: string; resource: string; starts_at: string | null; ends_at: string | null; notes: string; status: string; order_id: number | null; order_status: string | null };
type Table = { number: number; order_id: number | null; total: number };
async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, { ...options, credentials: "include" });
  const result = await response.json();
  if (!response.ok) throw new Error(typeof result.detail === "string" ? result.detail : "Check the fields and try again.");
  return result;
}
const money = (n: number) => `₩${n.toLocaleString("ko-KR")}`;
const statusLabel: Record<string, string> = { booked: "Waiting", in_progress: "In progress", ready: "Ready", completed: "Completed", cancelled: "Cancelled" };
export function TableBoard({ onSelect }: { onSelect: (number: number, orderId: number | null) => Promise<void> }) {
  const [tables, setTables] = useState<Table[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const load = () => request<Table[]>("/tables").then(result => { setTables(result); setError(""); }).catch(failure => setError(failure.message));
  useEffect(() => { void load(); const timer = setInterval(() => void load(), 10000); return () => clearInterval(timer); }, []);
  return <section><div className="section-heading"><div><p className="eyebrow">YOUR FLOOR</p><h2>Tables &amp; open bills</h2><p className="muted">Open a table to start an order. Occupied tables return to their saved bill.</p></div><button onClick={() => void load()}>Refresh tables</button></div>{error && <p role="alert">{error}</p>}<div className="table-board">{tables.map(table => <button disabled={busy} key={table.number} className={"floor-table " + (table.order_id ? "occupied" : "")} onClick={async () => { setBusy(true); try { await onSelect(table.number, table.order_id); } catch (failure) { setError(failure instanceof Error ? failure.message : "Could not open table."); } finally { setBusy(false); } }}><span className="table-symbol">▦</span><strong>Table {table.number}</strong><span>{table.order_id ? `Order #${table.order_id} · ${money(table.total)}` : "Available"}</span><small>{table.order_id ? "Resume bill →" : "Start order →"}</small></button>)}</div></section>;
}

export function WorkflowDesk({ features, onCheckout }: { features: string[]; onCheckout: (ticket: WorkTicket) => Promise<void> }) {
  const choices = [{ id: "appointment", feature: "appointments", label: "Appointments" }, { id: "walk_in", feature: "walk_ins", label: "Walk-ins" }, { id: "job", feature: "jobs", label: "Repair jobs" }].filter(item => features.includes(item.feature));
  const [kind, setKind] = useState(choices[0]?.id || "appointment");
  const [items, setItems] = useState<WorkTicket[]>([]);
  const [title, setTitle] = useState("");
  const [customer, setCustomer] = useState("");
  const [resource, setResource] = useState("");
  const [start, setStart] = useState("");
  const [duration, setDuration] = useState(30);
  const [notes, setNotes] = useState("");
  const [showClosed, setShowClosed] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const load = () => request<WorkTicket[]>("/owner/work").then(setItems).catch(failure => setError(failure.message));
  useEffect(() => { void load(); }, []);
  const changeStatus = async (item: WorkTicket, status: string) => {
    setBusy(true); setError("");
    try { await request(`/owner/work/${item.id}/status`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status }) }); await load(); }
    catch (failure) { setError(failure instanceof Error ? failure.message : "Could not update status."); }
    finally { setBusy(false); }
  };
  return <section><div className="section-heading"><div><p className="eyebrow">PEOPLE &amp; WORK</p><h2>{choices.find(item => item.id === kind)?.label}</h2><p className="muted">Manage your work, then connect it to a bill at checkout.</p></div><button onClick={() => void load()}>Refresh work</button></div><div className="category-tabs">{choices.map(item => <button aria-pressed={kind === item.id} className={kind === item.id ? "active" : ""} key={item.id} onClick={() => { setKind(item.id); setError(""); }}>{item.label}</button>)}</div>
    {error && <p role="alert" className="notice">{error} {error.includes("login") && <a href="/etalogin">Sign in as owner</a>}</p>}{message && <p role="status" className="notice">{message}</p>}
    <div className="work-layout"><form className="panel work-form" onSubmit={async event => { event.preventDefault(); setBusy(true); setError(""); setMessage(""); try { await request("/owner/work", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ kind, title, customer, resource: resource || "Any staff", starts_at: kind === "appointment" ? new Date(start).toISOString() : null, duration_minutes: duration, notes }) }); setTitle(""); setCustomer(""); setNotes(""); await load(); setMessage(kind === "appointment" ? "Appointment booked." : kind === "job" ? "Repair job created." : "Customer added to the queue."); } catch (failure) { setError(failure instanceof Error ? failure.message : "Could not save."); } finally { setBusy(false); } }}><h3>{kind === "appointment" ? "Book an appointment" : kind === "job" ? "New repair job" : "Add a walk-in"}</h3><label>{kind === "job" ? "Repair / device" : "Service"}<input required maxLength={120} value={title} onChange={event => setTitle(event.target.value)} placeholder={kind === "job" ? "Phone screen repair" : "Haircut"}/></label><label>Customer name<input required maxLength={120} value={customer} onChange={event => setCustomer(event.target.value)} /></label><label>Staff / resource<input maxLength={80} value={resource} onChange={event => setResource(event.target.value)} placeholder="Any staff" /></label>{kind === "appointment" && <><label>Appointment time (your local time)<input required type="datetime-local" value={start} onChange={event => setStart(event.target.value)}/></label><label>Duration (minutes)<input required type="number" min={5} max={480} step={5} value={duration} onChange={event => setDuration(Number(event.target.value))}/></label></>}<label>{kind === "job" ? "Fault, device details & customer instructions" : "Notes (optional)"}<textarea maxLength={1000} value={notes} onChange={event => setNotes(event.target.value)}/></label><button className="primary" disabled={busy} type="submit">{kind === "appointment" ? "Book appointment" : kind === "job" ? "Create repair job" : "Add to queue"}</button></form>
    <div><label className="inline-check"><input type="checkbox" checked={showClosed} onChange={event => setShowClosed(event.target.checked)}/>Show completed and cancelled</label><div className="work-cards">{items.filter(item => item.kind === kind && (showClosed || !["completed", "cancelled"].includes(item.status))).sort((a, b) => kind === "appointment" ? (a.starts_at || "").localeCompare(b.starts_at || "") : a.id - b.id).map(item => <article className="panel work-card" key={item.id}><div className="section-heading"><strong>#{item.id} · {item.customer}</strong><span className={"badge " + (item.status === "completed" ? "" : "open")}>{statusLabel[item.status]}</span></div><h3>{item.title}</h3><p className="muted">{item.resource}{item.starts_at && ` · ${new Date(item.starts_at).toLocaleString()} (${Math.round((Date.parse(item.ends_at!) - Date.parse(item.starts_at)) / 60000)} min)`}</p>{item.notes && <p className="work-notes">{item.notes}</p>}{item.order_id && <p>Bill #{item.order_id} · {item.order_status}</p>}<div className="row-actions">{item.status === "booked" && <button disabled={busy} onClick={() => void changeStatus(item, "in_progress")}>Start work</button>}{item.status === "in_progress" && <button disabled={busy} onClick={() => void changeStatus(item, "ready")}>Mark ready</button>}{!["completed", "cancelled"].includes(item.status) && <><button className="primary" disabled={busy} onClick={async () => { setBusy(true); try { await onCheckout(item); } catch (failure) { setError(failure instanceof Error ? failure.message : "Could not open checkout."); } finally { setBusy(false); } }}>{item.order_status === "open" ? "Resume bill" : "Checkout"}</button><button disabled={busy} onClick={() => void changeStatus(item, "cancelled")}>Cancel</button></>}</div></article>)}</div>{!items.some(item => item.kind === kind && (showClosed || !["completed", "cancelled"].includes(item.status))) && <p className="empty-state">{kind === "appointment" ? "No appointments yet. Book the first one." : kind === "job" ? "No repair jobs yet. Add a drop-off to get started." : "Your walk-in queue is clear."}</p>}</div></div>
  </section>;
}
