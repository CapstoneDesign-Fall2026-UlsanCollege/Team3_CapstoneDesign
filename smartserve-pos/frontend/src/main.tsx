import { StrictMode, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { OwnerManagement } from "./OwnerManagement";
import "./styles.css";

const API = "http://localhost:8000";
type MenuItem = { id: number; name: string; price: number };
type CartLine = MenuItem & { quantity: number };
type InventoryItem = { id: number; name: string; unit: string; stock_quantity: number; reorder_level: number; low_stock: boolean };
type Order = { id: number; order_type: string; status: string; total: number; created_at: string; paid_at?: string | null; trashed_at?: string | null; delete_after?: string | null; items: { name: string; quantity: number; unit_price: number }[]; payment_method?: string; simulated_reference?: string };
type Dashboard = { date: string; paid_orders: number; sales_total: number; recent_sales: Order[] };
type Tab = "cashier" | "orders" | "inventory" | "owner";
type Theme = "white" | "dark" | "code";

const won = (value: number) => new Intl.NumberFormat("ko-KR", { style: "currency", currency: "KRW", maximumFractionDigits: 0 }).format(value);
const koreaDate = (value = new Date()) => new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Seoul", year: "numeric", month: "2-digit", day: "2-digit" }).format(value);
const dateTime = (value?: string | null) => value ? new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Seoul", year: "numeric", month: "short", day: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false }).format(new Date(value)) : "—";
async function readData<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${API}${endpoint}`);
  if (!response.ok) throw new Error("Could not load data. Please refresh and try again.");
  return response.json();
}

function App() {
  const [theme, setTheme] = useState<Theme>(() => {
    try { const saved = localStorage.getItem("smartserve.theme"); return saved === "dark" || saved === "code" ? saved : "white"; }
    catch { return "white"; }
  });
  const [themeMenuOpen, setThemeMenuOpen] = useState(false);
  const themePanel = useRef<HTMLElement | null>(null);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem("smartserve.theme", theme); } catch { /* Theme still works without storage. */ }
  }, [theme]);
  useEffect(() => {
    if (!themeMenuOpen) return;
    const closeOutside = (event: PointerEvent) => { if (!themePanel.current?.contains(event.target as Node)) setThemeMenuOpen(false); };
    document.addEventListener("pointerdown", closeOutside);
    return () => document.removeEventListener("pointerdown", closeOutside);
  }, [themeMenuOpen]);
  const [tab, setTab] = useState<Tab>("cashier");
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [cart, setCart] = useState<CartLine[]>([]);
  const [orderType, setOrderType] = useState("dine_in");
  const [receipt, setReceipt] = useState<Order | null>(null);
  const [message, setMessage] = useState("");
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [salesDate, setSalesDate] = useState(koreaDate);
  const [salesLoading, setSalesLoading] = useState(false);
  const [salesError, setSalesError] = useState("");
  const [salesRefresh, setSalesRefresh] = useState(0);
  const salesRequest = useRef(0);
  const [orderDate, setOrderDate] = useState("");
  const [orders, setOrders] = useState<Order[]>([]);
  const [ordersTrash, setOrdersTrash] = useState(false);
  const [monthOpen, setMonthOpen] = useState<Record<string, boolean>>({});
  const [orderFilter, setOrderFilter] = useState("all");
  const [savedOrder, setSavedOrder] = useState<Order | null>(null);
  const paying = useRef(false);
  const [busy, setBusy] = useState(false);
  const [pendingOrder, setPendingOrder] = useState<number | null>(() => {
    const saved = Number(sessionStorage.getItem("smartserve.pendingOrder"));
    return Number.isSafeInteger(saved) && saved > 0 ? saved : null;
  });
  const total = useMemo(() => cart.reduce((sum, line) => sum + line.price * line.quantity, 0), [cart]);

  useEffect(() => { void loadMenu().catch(() => setMessage("Could not load the menu. Check the connection and refresh.")); }, []);
  useEffect(() => {
    if (tab !== "owner") return;
    const requestId = ++salesRequest.current;
    setSalesLoading(true); setSalesError(""); setDashboard(null);
    void readData<Dashboard>(`/dashboard/sales?selected_date=${salesDate}`).then(result => {
      if (requestId === salesRequest.current) setDashboard(result);
    }).catch(error => {
      if (requestId === salesRequest.current) setSalesError(error.message);
    }).finally(() => { if (requestId === salesRequest.current) setSalesLoading(false); });
    return () => { salesRequest.current++; };
  }, [tab, salesDate, salesRefresh]);
  useEffect(() => {
    if (!pendingOrder) return;
    void fetch(`${API}/orders/${pendingOrder}`).then(async response => {
      if (!response.ok) throw new Error("Could not load the saved order. Check the API and reload.");
      return response.json();
    }).then((order: Order) => {
      if (order.status === "open") setSavedOrder(order);
      else { setPendingOrder(null); sessionStorage.removeItem("smartserve.pendingOrder"); }
    }).catch(error => setMessage(error instanceof Error ? error.message : "Could not load saved order"));
  }, [pendingOrder]);
  const loadMenu = async () => setMenu(await readData<MenuItem[]>("/menu"));
  const loadInventory = async () => setInventory(await readData<InventoryItem[]>("/inventory"));
  const addToCart = (item: MenuItem) => setCart(current => current.some(line => line.id === item.id)
    ? current.map(line => line.id === item.id ? { ...line, quantity: line.quantity + 1 } : line)
    : [...current, { ...item, quantity: 1 }]);
  const changeQty = (id: number, delta: number) => setCart(current => current.flatMap(line => line.id !== id ? [line] : line.quantity + delta > 0 ? [{ ...line, quantity: line.quantity + delta }] : []));
  const saveCartOrder = async (): Promise<Order> => {
    const response = await fetch(`${API}/orders`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ order_type: orderType, items: cart.map(({ id, quantity }) => ({ menu_item_id: id, quantity })) }) });
    if (!response.ok) throw new Error("Could not create order. Check the API and try again.");
    const order: Order = await response.json();
    sessionStorage.setItem("smartserve.pendingOrder", String(order.id));
    setSavedOrder(order); setPendingOrder(order.id); setCart([]); setReceipt(null);
    return order;
  };
  const createOnly = async () => {
    if (paying.current || !cart.length || pendingOrder) return;
    paying.current = true; setBusy(true); setMessage("Creating order…");
    try {
      const order = await saveCartOrder();
      setMessage(`Order #${order.id} created. Payment is pending; inventory is unchanged.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not create order"); }
    finally { paying.current = false; setBusy(false); }
  };
  const createAndPay = async (method: "cash" | "card" | "qr") => {
    if (paying.current || (!cart.length && !pendingOrder)) return;
    paying.current = true; setBusy(true);
    setMessage("Processing simulated payment…");
    try {
      let orderId = pendingOrder;
      if (!orderId) {
      const order = await saveCartOrder();
      orderId = order.id;
      }
      const pay = await fetch(`${API}/orders/${orderId}/pay`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ method }) });
      const result = await pay.json();
      if (pay.status === 409) {
        const existing = await fetch(`${API}/orders/${orderId}`);
        if (existing.ok) {
          const saved: Order = await existing.json();
          if (saved.status === "paid") {
            setReceipt(saved); setCart([]); setSavedOrder(null); setPendingOrder(null);
            sessionStorage.removeItem("smartserve.pendingOrder");
          }
        }
      }
      if (!pay.ok) throw new Error(typeof result.detail === "string" ? result.detail : result.detail.message);
      sessionStorage.removeItem("smartserve.pendingOrder"); setPendingOrder(null); setSavedOrder(null);
      setReceipt(result.order); setCart([]); setMessage(result.message);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Payment failed"); }
    finally { paying.current = false; setBusy(false); }
  };
  const openTab = (next: Tab) => { setTab(next); setMessage(""); if (next === "orders") void readData<Order[]>(`/orders?trash=${ordersTrash}`).then(setOrders).catch(() => setMessage("Could not load orders.")); if (next === "inventory") void loadInventory().catch(() => setMessage("Could not load inventory.")); };
  const resumeOrder = (order: Order) => {
    setCart([]); setReceipt(null); setSavedOrder(order); setPendingOrder(order.id);
    sessionStorage.setItem("smartserve.pendingOrder", String(order.id));
    setTab("cashier"); setMessage(`Order #${order.id} is ready for payment.`);
  };
  const viewReceipt = (order: Order) => {
    setCart([]); setSavedOrder(null); setPendingOrder(null);
    sessionStorage.removeItem("smartserve.pendingOrder");
    setReceipt(order); setTab("cashier"); setMessage(`Showing the saved receipt for order #${order.id}.`);
  };
  const cancelOrder = async (order: Order) => {
    setBusy(true);
    try {
      const response = await fetch(`${API}/orders/${order.id}/cancel`, {method:"POST"});
      const result = await response.json();
      if (!response.ok) throw new Error(result.detail || "Could not cancel order");
      setOrders(current => current.map(item => item.id === result.id ? result : item));
      if (pendingOrder === order.id) { setPendingOrder(null); setSavedOrder(null); sessionStorage.removeItem("smartserve.pendingOrder"); }
      setMessage(`Order #${order.id} was cancelled. Inventory is unchanged.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not cancel order"); }
    finally { setBusy(false); }
  };

  const showOrderFolder = async (trash: boolean) => {
    setOrdersTrash(trash); setOrderFilter("all"); setOrderDate(""); setMessage("");
    try { setOrders(await readData<Order[]>("/orders?trash=" + trash)); }
    catch { setMessage("Could not load orders. Please refresh."); }
  };
  const manageTrash = async (order: Order, action: "trash" | "restore" | "delete") => {
    if (action === "delete" && !window.confirm("Permanently delete order #" + order.id + "? This cannot be undone.")) return;
    setBusy(true); setMessage("");
    try {
      const endpoint = "/orders/" + order.id + (action === "delete" ? "" : "/" + action);
      const response = await fetch(API + endpoint, { method: action === "delete" ? "DELETE" : "POST" });
      if (!response.ok) { const result = await response.json(); throw new Error(result.detail || "Could not update order"); }
      setOrders(await readData<Order[]>("/orders?trash=" + ordersTrash));
      setMessage(action === "trash" ? "Order moved to Trash. You can restore it for 30 days." : action === "restore" ? "Order restored to the cancelled-orders list." : "Order permanently deleted.");
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not update order"); }
    finally { setBusy(false); }
  };

  const visibleOrders = orders.filter(order => (orderFilter === "all" || order.status === orderFilter) && (!orderDate || koreaDate(new Date(order.created_at)) === orderDate));

  const ordersByMonth = visibleOrders.reduce<Record<string, Order[]>>((groups, order) => {
    const month = koreaDate(new Date(order.created_at)).slice(0, 7);
    (groups[month] ??= []).push(order);
    return groups;
  }, {});
  const orderMonths = Object.keys(ordersByMonth).sort().reverse();
  const monthLabel = (month: string) => new Intl.DateTimeFormat("en-GB", { month: "long", year: "numeric", timeZone: "Asia/Seoul" }).format(new Date(month + "-01T00:00:00+09:00"));

  return <main className="app-shell">
    <aside className="theme-control" ref={themePanel} onKeyDown={event => { if (event.key === "Escape") { setThemeMenuOpen(false); themePanel.current?.querySelector<HTMLButtonElement>(".theme-toggle")?.focus(); } }}>
      <button className="theme-toggle" aria-label="Change theme" title="Change theme" aria-expanded={themeMenuOpen} aria-controls="theme-options" onClick={() => setThemeMenuOpen(open => !open)}><svg viewBox="0 0 24 24" width="23" height="23" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18h1a2 2 0 0 0 1.7-3.1 1.5 1.5 0 0 1 1.3-2.3h2a3 3 0 0 0 3-3A9.6 9.6 0 0 0 12 3Z"/><circle cx="7.5" cy="10" r="1"/><circle cx="11" cy="6.8" r="1"/><circle cx="15.5" cy="8" r="1"/></svg></button>
      {themeMenuOpen && <fieldset id="theme-options" className="theme-options"><legend>Appearance</legend>{([{ value: "white", label: "White", detail: "Bright & clean" }, { value: "dark", label: "Dark", detail: "Soft contrast" }, { value: "code", label: "Code", detail: "Syntax highlights" }] as const).map(option => <label className={"theme-option " + (theme === option.value ? "selected" : "")} key={option.value}><input type="radio" name="theme" value={option.value} checked={theme === option.value} onChange={() => setTheme(option.value)} /><span className={"theme-swatch swatch-" + option.value} aria-hidden="true"/><span><strong>{option.label}</strong><small>{option.detail}</small></span></label>)}</fieldset>}
    </aside>
    <header><div><p className="eyebrow">CAFÉ MANAGEMENT</p><h1>SmartServe POS</h1></div><nav aria-label="Main navigation">{(["cashier", "orders", "inventory", "owner"] as const).map(item => <button aria-label={item === "cashier" || item === "inventory" ? item : undefined} className={tab === item ? "active" : ""} onClick={() => openTab(item)} key={item}>{item === "owner" ? "Owner dashboard" : item[0].toUpperCase() + item.slice(1)}</button>)}</nav></header>
    {message && <p className="notice" role="status">{message}</p>}
    {tab === "cashier" && <section className="cashier-grid">
      <div><p className="eyebrow">CHECKOUT</p><h2>Menu</h2><p className="muted">Choose items, then take a simulated payment.</p><div className="menu-grid">{menu.map(item => <button className="menu-card" disabled={busy || pendingOrder !== null} onClick={() => addToCart(item)} key={item.id}><strong>{item.name}</strong><span>{won(item.price)}</span><small>Add to order</small></button>)}</div></div>
      <aside className="panel"><div className="section-heading"><h2>{pendingOrder ? `Order #${pendingOrder}` : "Current order"}</h2>{pendingOrder && <span className="badge open">Open</span>}</div><label>Order type <select disabled={busy || pendingOrder !== null} value={savedOrder?.order_type ?? orderType} onChange={e => setOrderType(e.target.value)}><option value="dine_in">Dine in</option><option value="takeaway">Takeaway</option></select></label>
        {pendingOrder && savedOrder ? <>{savedOrder.items.map(item => <div className="cart-line" key={item.name}><span>{item.name}<small>{won(item.unit_price)} each</small></span><strong>× {item.quantity}</strong></div>)}<div className="total"><strong>Total</strong><strong>{won(savedOrder.total)}</strong></div><p className="muted">Saved order. Retry payment or manage it from Orders.</p></> : cart.length ? <>{cart.map(line => <div className="cart-line" key={line.id}><span>{line.name}<small>{won(line.price)} each</small></span><div><button disabled={busy} onClick={() => changeQty(line.id, -1)} aria-label={`Remove one ${line.name}`}>−</button>{line.quantity}<button disabled={busy} onClick={() => changeQty(line.id, 1)} aria-label={`Add one ${line.name}`}>+</button></div></div>)}<div className="total"><strong>Total</strong><strong>{won(total)}</strong></div><button className="text-button" disabled={busy} onClick={() => setCart([])}>Clear cart</button></> : <p className="muted">Choose menu items to start.</p>}
        {cart.length > 0 && !pendingOrder && <button disabled={busy} onClick={() => void createOnly()}>Create order</button>}
        {(cart.length > 0 || pendingOrder) && <div className="payments"><button disabled={busy} onClick={() => createAndPay("cash")}>Pay cash</button><button disabled={busy} onClick={() => createAndPay("card")}>Pay card</button><button disabled={busy} onClick={() => createAndPay("qr")}>Pay QR</button></div>}
      </aside>
      {receipt && <section className="receipt"><p className="eyebrow">PAYMENT COMPLETE</p><h2>Receipt #{receipt.id}</h2><p className="muted">Paid {dateTime(receipt.paid_at)} · KST</p>{receipt.items.map(item => <p key={item.name}>{item.name} × {item.quantity}</p>)}<strong>{won(receipt.total)} · {receipt.payment_method?.toUpperCase()}</strong><p className="muted">{receipt.simulated_reference}</p></section>}
    </section>}
    {tab === "orders" && <section>
      <div className="section-heading"><div><p className="eyebrow">ORDER MANAGEMENT</p><h2>{ordersTrash ? "Order Trash" : "Orders"}</h2><p className="muted">{ordersTrash ? "Trashed cancelled orders are permanently deleted after 30 days. Restore returns them as cancelled." : "Resume or cancel unpaid orders. Move cancelled orders to Trash to remove them from this list."}</p></div>
      <div className="toolbar"><label>Status<select value={orderFilter} onChange={event => setOrderFilter(event.target.value)}><option value="all">All orders</option><option value="open">Open</option><option value="paid">Paid</option><option value="cancelled">Cancelled</option></select></label><label>Order date<input type="date" value={orderDate} onChange={event => setOrderDate(event.target.value)} /></label><button onClick={() => { setOrderDate(""); setOrderFilter("all"); }}>Clear filters</button><button onClick={() => openTab("orders")}>Refresh orders</button></div></div>
      <div className="toolbar" role="group" aria-label="Order folders"><button className={!ordersTrash ? "folder-active" : ""} disabled={busy} onClick={() => void showOrderFolder(false)}>Orders list</button><button className={ordersTrash ? "folder-active" : ""} disabled={busy} onClick={() => void showOrderFolder(true)}>Trash</button><span className="muted">Dates shown in Korea time (KST)</span></div><div className="month-folders">{orderMonths.map((month, index) => {
        const key = (ordersTrash ? "trash:" : "orders:") + month;
        return <details className="month-folder" key={key} open={monthOpen[key] ?? index === 0} onToggle={event => { const open = event.currentTarget.open; setMonthOpen(current => current[key] === open ? current : { ...current, [key]: open }); }}>
          <summary><strong>{monthLabel(month)}</strong><span className="month-count">{ordersByMonth[month].length} {ordersByMonth[month].length === 1 ? "order" : "orders"}</span></summary>
          <div className="table-wrap"><table><thead><tr><th>Order</th><th>Created (KST)</th><th>Items</th><th>Total</th><th>Status</th><th>{ordersTrash ? "Auto delete (KST)" : "Paid (KST)"}</th><th>Actions</th></tr></thead><tbody>{ordersByMonth[month].map(order => <tr key={order.id}><td><strong>#{order.id}</strong><small>{order.order_type.replace("_", " ")}</small></td><td>{dateTime(order.created_at)}</td><td>{order.items.map(item => item.name + " × " + item.quantity).join(", ")}</td><td>{won(order.total)}</td><td><span className={"badge " + order.status}>{order.status === "open" ? "Open" : order.status === "paid" ? "Paid" : "Cancelled"}</span></td><td>{dateTime(ordersTrash ? order.delete_after : order.paid_at)}</td><td>{ordersTrash ? <div className="row-actions"><button disabled={busy} onClick={() => void manageTrash(order, "restore")}>Restore</button><button className="danger" disabled={busy} onClick={() => void manageTrash(order, "delete")}>Delete forever</button></div> : order.status === "open" ? <div className="row-actions"><button className="primary" disabled={busy} onClick={() => resumeOrder(order)}>Resume</button><button disabled={busy} onClick={() => cancelOrder(order)}>Cancel</button></div> : order.status === "paid" ? <button onClick={() => viewReceipt(order)}>View receipt</button> : <button disabled={busy} onClick={() => void manageTrash(order, "trash")}>Move to Trash</button>}</td></tr>)}</tbody></table></div>
        </details>;
      })}</div>{visibleOrders.length === 0 && <p className="empty-state">{ordersTrash ? "Trash is empty." : "No orders match these filters."}</p>}
    </section>}
    {tab === "inventory" && <section><h2>Inventory</h2><p className="muted">Stock is reduced only after a successful simulated payment.</p><table><thead><tr><th>Ingredient</th><th>In stock</th><th>Reorder level</th><th>Status</th></tr></thead><tbody>{inventory.map(item => <tr key={item.id}><td>{item.name}</td><td>{item.stock_quantity} {item.unit}</td><td>{item.reorder_level} {item.unit}</td><td><span className={item.low_stock ? "badge low" : "badge"}>{item.low_stock ? "Low stock" : "OK"}</span></td></tr>)}</tbody></table></section>}
    {tab === "owner" && <section>
      <div className="section-heading"><div><h2>Owner sales dashboard</h2><p className="muted">Daily totals include every paid order in the shared store, including test purchases.</p></div><a className="primary-link" href="#owner-management">Manage menu &amp; inventory</a></div>
      <div className="toolbar"><label>Sales date<input type="date" value={salesDate} onChange={event => { if (event.target.value) setSalesDate(event.target.value); }} /></label><button onClick={() => setSalesDate(koreaDate())}>Today</button><button disabled={salesLoading} onClick={() => setSalesRefresh(value => value + 1)}>Refresh sales</button><span className="muted">Korea time (KST)</span></div>
      {salesLoading && <p role="status">Loading sales…</p>}{salesError && <p role="alert" className="notice">{salesError}</p>}
      {dashboard && <><div className="stats"><article><span>{salesDate === koreaDate() ? "Sales today" : "Sales on " + dashboard.date}</span><strong>{won(dashboard.sales_total)}</strong></article><article><span>Paid orders on {dashboard.date}</span><strong>{dashboard.paid_orders}</strong></article></div><h3>Paid sales on {dashboard.date}</h3><div className="table-wrap"><table><thead><tr><th>Order</th><th>Paid (KST)</th><th>Items</th><th>Type</th><th>Total</th><th>Payment</th></tr></thead><tbody>{dashboard.recent_sales.map(order => <tr key={order.id}><td>#{order.id}</td><td>{dateTime(order.paid_at)}</td><td>{order.items.map(item => item.name + " × " + item.quantity).join(", ")}</td><td>{order.order_type.replace("_", " ")}</td><td>{won(order.total)}</td><td>{order.payment_method?.toUpperCase()}</td></tr>)}</tbody></table>{dashboard.paid_orders === 0 && <p className="empty-state">No paid sales on this date.</p>}</div></>}
      <OwnerManagement onMenuChanged={loadMenu} onInventoryChanged={loadInventory} />
    </section>}
  </main>;
}

createRoot(document.getElementById("root")!).render(
  <StrictMode><App /></StrictMode>,
);
