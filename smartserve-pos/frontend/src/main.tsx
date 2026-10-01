import { StrictMode, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "http://localhost:8000";
type MenuItem = { id: number; name: string; price: number };
type CartLine = MenuItem & { quantity: number };
type InventoryItem = { id: number; name: string; unit: string; stock_quantity: number; reorder_level: number; low_stock: boolean };
type Order = { id: number; order_type: string; status: string; total: number; items: { name: string; quantity: number; unit_price: number }[]; payment_method?: string; simulated_reference?: string };
type Dashboard = { date: string; paid_orders: number; sales_total: number; recent_sales: Order[] };
type Tab = "cashier" | "orders" | "inventory" | "owner";

const won = (value: number) => new Intl.NumberFormat("ko-KR", { style: "currency", currency: "KRW", maximumFractionDigits: 0 }).format(value);

function App() {
  const [tab, setTab] = useState<Tab>("cashier");
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [cart, setCart] = useState<CartLine[]>([]);
  const [orderType, setOrderType] = useState("dine_in");
  const [receipt, setReceipt] = useState<Order | null>(null);
  const [message, setMessage] = useState("");
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [orderFilter, setOrderFilter] = useState("all");
  const [savedOrder, setSavedOrder] = useState<Order | null>(null);
  const paying = useRef(false);
  const [busy, setBusy] = useState(false);
  const [pendingOrder, setPendingOrder] = useState<number | null>(() => {
    const saved = Number(sessionStorage.getItem("smartserve.pendingOrder"));
    return Number.isSafeInteger(saved) && saved > 0 ? saved : null;
  });
  const total = useMemo(() => cart.reduce((sum, line) => sum + line.price * line.quantity, 0), [cart]);

  useEffect(() => { void loadMenu(); }, []);
  useEffect(() => {
    if (!pendingOrder) return;
    void fetch(`${API}/orders/${pendingOrder}`).then(response => response.json()).then((order: Order) => {
      if (order.status === "open") setSavedOrder(order);
      else { setPendingOrder(null); sessionStorage.removeItem("smartserve.pendingOrder"); }
    });
  }, [pendingOrder]);
  const loadMenu = async () => setMenu(await (await fetch(`${API}/menu`)).json());
  const loadInventory = async () => setInventory(await (await fetch(`${API}/inventory`)).json());
  const loadDashboard = async () => setDashboard(await (await fetch(`${API}/dashboard/sales`)).json());
  const addToCart = (item: MenuItem) => setCart(current => current.some(line => line.id === item.id)
    ? current.map(line => line.id === item.id ? { ...line, quantity: line.quantity + 1 } : line)
    : [...current, { ...item, quantity: 1 }]);
  const changeQty = (id: number, delta: number) => setCart(current => current.flatMap(line => line.id !== id ? [line] : line.quantity + delta > 0 ? [{ ...line, quantity: line.quantity + delta }] : []));
  const createAndPay = async (method: "cash" | "card" | "qr") => {
    if (paying.current || (!cart.length && !pendingOrder)) return;
    paying.current = true; setBusy(true);
    setMessage("Processing simulated payment…");
    try {
      let orderId = pendingOrder;
      if (!orderId) {
      const create = await fetch(`${API}/orders`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ order_type: orderType, items: cart.map(({ id, quantity }) => ({ menu_item_id: id, quantity })) }) });
      if (!create.ok) throw new Error((await create.json()).detail || "Could not create order");
      const order: Order = await create.json();
      orderId = order.id;
      setSavedOrder(order);
      sessionStorage.setItem("smartserve.pendingOrder", String(orderId));
      setPendingOrder(orderId);
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
  const openTab = (next: Tab) => { setTab(next); if (next === "orders") void fetch(`${API}/orders`).then(response => response.json()).then(setOrders).catch(() => setMessage("Could not load orders.")); if (next === "inventory") void loadInventory(); if (next === "owner") void loadDashboard(); };
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

  return <main className="app-shell">
    <header><div><p className="eyebrow">SMARTSERVE POS</p><h1>Make every order count.</h1></div><nav aria-label="Main navigation">{(["cashier", "orders", "inventory", "owner"] as const).map(item => <button aria-label={item === "cashier" || item === "inventory" ? item : undefined} className={tab === item ? "active" : ""} onClick={() => openTab(item)} key={item}>{item === "owner" ? "Owner dashboard" : item[0].toUpperCase() + item.slice(1)}</button>)}</nav></header>
    {message && <p className="notice" role="status">{message}</p>}
    {tab === "cashier" && <section className="cashier-grid">
      <div><p className="eyebrow">CHECKOUT</p><h2>Menu</h2><p className="muted">Choose items, then take a simulated payment.</p><div className="menu-grid">{menu.map(item => <button className="menu-card" disabled={busy || pendingOrder !== null} onClick={() => addToCart(item)} key={item.id}><strong>{item.name}</strong><span>{won(item.price)}</span><small>Add to order</small></button>)}</div></div>
      <aside className="panel"><div className="section-heading"><h2>{pendingOrder ? `Order #${pendingOrder}` : "Current order"}</h2>{pendingOrder && <span className="badge open">Open</span>}</div><label>Order type <select disabled={busy || pendingOrder !== null} value={savedOrder?.order_type ?? orderType} onChange={e => setOrderType(e.target.value)}><option value="dine_in">Dine in</option><option value="takeaway">Takeaway</option></select></label>
        {pendingOrder && savedOrder ? <>{savedOrder.items.map(item => <div className="cart-line" key={item.name}><span>{item.name}<small>{won(item.unit_price)} each</small></span><strong>× {item.quantity}</strong></div>)}<div className="total"><strong>Total</strong><strong>{won(savedOrder.total)}</strong></div><p className="muted">Saved order. Retry payment or manage it from Orders.</p></> : cart.length ? <>{cart.map(line => <div className="cart-line" key={line.id}><span>{line.name}<small>{won(line.price)} each</small></span><div><button disabled={busy} onClick={() => changeQty(line.id, -1)} aria-label={`Remove one ${line.name}`}>−</button>{line.quantity}<button disabled={busy} onClick={() => changeQty(line.id, 1)} aria-label={`Add one ${line.name}`}>+</button></div></div>)}<div className="total"><strong>Total</strong><strong>{won(total)}</strong></div><button className="text-button" disabled={busy} onClick={() => setCart([])}>Clear cart</button></> : <p className="muted">Choose menu items to start.</p>}
        {(cart.length > 0 || pendingOrder) && <div className="payments"><button disabled={busy} onClick={() => createAndPay("cash")}>Pay cash</button><button disabled={busy} onClick={() => createAndPay("card")}>Pay card</button><button disabled={busy} onClick={() => createAndPay("qr")}>Pay QR</button></div>}
      </aside>
      {receipt && <section className="receipt"><p className="eyebrow">PAYMENT COMPLETE</p><h2>Receipt #{receipt.id}</h2>{receipt.items.map(item => <p key={item.name}>{item.name} × {item.quantity}</p>)}<strong>{won(receipt.total)} · {receipt.payment_method?.toUpperCase()}</strong><p className="muted">{receipt.simulated_reference}</p></section>}
    </section>}
    {tab === "orders" && <section><div className="section-heading"><div><p className="eyebrow">ORDER MANAGEMENT</p><h2>Orders</h2><p className="muted">Find an open order, resume payment, or cancel it before payment.</p></div><label className="filter-label">Show <select value={orderFilter} onChange={event => setOrderFilter(event.target.value)}><option value="all">All orders</option><option value="open">Open</option><option value="paid">Paid</option><option value="cancelled">Cancelled</option></select></label></div><div className="table-wrap"><table><thead><tr><th>Order</th><th>Items</th><th>Total</th><th>Status</th><th>Actions</th></tr></thead><tbody>{orders.filter(order => orderFilter === "all" || order.status === orderFilter).map(order => <tr key={order.id}><td><strong>#{order.id}</strong><small>{order.order_type.replace("_", " ")}</small></td><td>{order.items.map(item => `${item.name} × ${item.quantity}`).join(", ")}</td><td>{won(order.total)}</td><td><span className={`badge ${order.status}`}>{order.status === "open" ? "Open" : order.status === "paid" ? "Paid" : "Cancelled"}</span></td><td>{order.status === "open" ? <div className="row-actions"><button className="primary" disabled={busy} onClick={() => resumeOrder(order)}>Resume</button><button disabled={busy} onClick={() => cancelOrder(order)}>Cancel</button></div> : order.status === "paid" ? <button onClick={() => viewReceipt(order)}>View receipt</button> : "—"}</td></tr>)}</tbody></table>{orders.filter(order => orderFilter === "all" || order.status === orderFilter).length === 0 && <p className="empty-state">No orders in this view.</p>}</div></section>}
    {tab === "inventory" && <section><h2>Inventory</h2><p className="muted">Stock is reduced only after a successful simulated payment.</p><table><thead><tr><th>Ingredient</th><th>In stock</th><th>Reorder level</th><th>Status</th></tr></thead><tbody>{inventory.map(item => <tr key={item.id}><td>{item.name}</td><td>{item.stock_quantity} {item.unit}</td><td>{item.reorder_level} {item.unit}</td><td><span className={item.low_stock ? "badge low" : "badge"}>{item.low_stock ? "Low stock" : "OK"}</span></td></tr>)}</tbody></table></section>}
    {tab === "owner" && <section><h2>Owner sales dashboard</h2>{dashboard && <><div className="stats"><article><span>Sales today</span><strong>{won(dashboard.sales_total)}</strong></article><article><span>Paid orders</span><strong>{dashboard.paid_orders}</strong></article></div><h3>Recent paid sales</h3><table><thead><tr><th>Order</th><th>Type</th><th>Total</th><th>Payment</th></tr></thead><tbody>{dashboard.recent_sales.map(order => <tr key={order.id}><td>#{order.id}</td><td>{order.order_type.replace("_", " ")}</td><td>{won(order.total)}</td><td>{order.payment_method}</td></tr>)}</tbody></table></>}</section>}
  </main>;
}

createRoot(document.getElementById("root")!).render(
  <StrictMode><App /></StrictMode>,
);
