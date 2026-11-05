import { AccountSecurity } from "./AccountSecurity";
import { apiFetch, apiRequest, jsonBody, type AccountSession } from "./api";
import { AccountAccess } from "./AccountAccess";
import { PlatformConsole, BusinessAccountSettings } from "./AccountManagement";
import { StrictMode, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { OwnerManagement } from "./OwnerManagement";
import { BusinessSetup, businessLabels, defaultBusiness, orderLabels, type BusinessProfile } from "./Onboarding";
import { TableBoard, WorkflowDesk, type WorkTicket } from "./WorkflowDesk";
import "./styles.css";

const API = import.meta.env.PROD ? "" : "http://localhost:8000";
const isSetupPage = window.location.pathname.replace(/\/+$/, "") === "/setup";
const isOwnerPage = isSetupPage || window.location.pathname.replace(/\/+$/, "") === "/etalogin";
type MenuItem = { id: number; name: string; price: number; category: string; item_type: string; sku: string };
type MenuRecipe = { id: number; recipe: { ingredient_id: number; quantity: number }[] };
type CartLine = MenuItem & { quantity: number };
type InventoryItem = { id: number; name: string; unit: string; stock_quantity: number; reorder_level: number; low_stock: boolean };
type Order = { table_number?: number | null; ticket_id?: number | null; id: number; order_type: string; status: string; total: number; created_at: string; paid_at?: string | null; trashed_at?: string | null; delete_after?: string | null; items: { menu_item_id: number; name: string; quantity: number; unit_price: number }[]; payment_method?: string; simulated_reference?: string };
type Dashboard = { date: string; paid_orders: number; sales_total: number; recent_sales: Order[] };
type Tab = "cashier" | "orders" | "inventory" | "owner" | "tables" | "work";
type Theme = "white" | "dark" | "code";

const won = (value: number) => new Intl.NumberFormat("ko-KR", { style: "currency", currency: "KRW", maximumFractionDigits: 0 }).format(value);
const koreaDate = (value = new Date()) => new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Seoul", year: "numeric", month: "2-digit", day: "2-digit" }).format(value);
const dateTime = (value?: string | null) => value ? new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Seoul", year: "numeric", month: "short", day: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false }).format(new Date(value)) : "—";
async function readData<T>(endpoint: string): Promise<T> {
  const response = await apiFetch(`${API}${endpoint}`, { credentials: "include" });
  if (!response.ok) throw new Error("Could not load data. Please refresh and try again.");
  return response.json();
}

function App({ account }: { account: AccountSession }) {
  const canConfigure = account.user?.role === "platform_admin";
  const canManage = canConfigure || account.user?.role === "owner";
  const pendingStorageKey = `smartserve.pendingOrder.${account.store_id}.${account.user?.id}`;
  const [deferSetup, setDeferSetup] = useState(false);
  const [showSetup, setShowSetup] = useState(isSetupPage);
  const [tableNumber, setTableNumber] = useState<number | null>(null);
  const [workTicket, setWorkTicket] = useState<WorkTicket | null>(null);
  const [business, setBusiness] = useState<BusinessProfile>(defaultBusiness);
  const [businessError, setBusinessError] = useState("");
  const [businessReady, setBusinessReady] = useState(false);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All items");
  const [catalogVersion, setCatalogVersion] = useState(0);
  useEffect(() => {
    void readData<BusinessProfile>("/business").then(profile => { setBusiness(profile); setBusinessReady(true); }).catch(() => setBusinessError("Business settings could not be loaded. Refresh to try again."));
  }, []);
  const [showFeedback, setShowFeedback] = useState(false);
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
  const [tab, setTab] = useState<Tab>(account.user?.role === "owner" || (isOwnerPage && !isSetupPage) ? "owner" : "cashier");
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [recipes, setRecipes] = useState<MenuRecipe[]>([]);
  const [stockReady, setStockReady] = useState(false);
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
    const saved = Number(sessionStorage.getItem(pendingStorageKey));
    return Number.isSafeInteger(saved) && saved > 0 ? saved : null;
  });
  const foodBusiness = ["cafe", "restaurant", "bakery"].includes(business.business_type);
  const fulfillmentKey = business.order_types.join(",");
  useEffect(() => { setOrderType(business.order_types[0] || "in_store"); }, [fulfillmentKey]);
  const categories = ["All items", ...new Set(menu.map(item => item.category || "General"))];
  const filteredMenu = menu.filter(item => (category === "All items" || item.category === category) && `${item.name} ${item.sku} ${item.category}`.toLowerCase().includes(search.trim().toLowerCase()));
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
    void apiFetch(`${API}/orders/${pendingOrder}`).then(async response => {
      if (!response.ok) throw new Error("Could not load the saved order. Check the API and reload.");
      return response.json();
    }).then((order: Order) => {
      if (order.status === "open") setSavedOrder(order);
      else { setPendingOrder(null); sessionStorage.removeItem(pendingStorageKey); }
    }).catch(error => setMessage(error instanceof Error ? error.message : "Could not load saved order"));
  }, [pendingOrder]);
  const loadMenu = async () => {
    const [items, recipeItems, stockItems] = await Promise.all([readData<MenuItem[]>("/menu"), readData<MenuRecipe[]>("/owner/menu"), readData<InventoryItem[]>("/inventory")]);
    setMenu(items); setRecipes(recipeItems); setInventory(stockItems); setStockReady(true);
  };
  const shortagesFor = (lines: { id: number; quantity: number }[]) => {
    const required = new Map<number, number>();
    for (const line of lines) for (const ingredient of recipes.find(item => item.id === line.id)?.recipe ?? []) required.set(ingredient.ingredient_id, (required.get(ingredient.ingredient_id) ?? 0) + ingredient.quantity * line.quantity);
    return [...required].flatMap(([id, needed]) => {
      const ingredient = inventory.find(item => item.id === id);
      return !ingredient || needed > ingredient.stock_quantity + 0.00000001 ? [ingredient ? ingredient.name + ": needs " + Number(needed.toFixed(6)) + " " + ingredient.unit + ", only " + ingredient.stock_quantity + " " + ingredient.unit + " available" : "Ingredient is no longer available"] : [];
    });
  };
  const orderShortages = shortagesFor(pendingOrder && savedOrder ? [...savedOrder.items.map(item => ({ id: item.menu_item_id, quantity: item.quantity })), ...cart] : cart);
  useEffect(() => {
    if (tab !== "cashier") return;
    const refresh = () => { void loadMenu().catch(() => setStockReady(false)); };
    const timer = window.setInterval(refresh, 15000);
    window.addEventListener("focus", refresh);
    return () => { clearInterval(timer); window.removeEventListener("focus", refresh); };
  }, [tab]);
  const loadInventory = async () => setInventory(await readData<InventoryItem[]>("/inventory"));
  const addToCart = (item: MenuItem) => setCart(current => current.some(line => line.id === item.id)
    ? current.map(line => line.id === item.id ? { ...line, quantity: line.quantity + 1 } : line)
    : [...current, { ...item, quantity: 1 }]);
  const changeQty = (id: number, delta: number) => setCart(current => current.flatMap(line => line.id !== id ? [line] : line.quantity + delta > 0 ? [{ ...line, quantity: line.quantity + delta }] : []));
  const saveCartOrder = async (): Promise<Order> => {
    const response = await apiFetch(`${API}/orders`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ order_type: orderType, table_number: orderType === "dine_in" ? tableNumber : null, ticket_id: workTicket?.id, items: cart.map(({ id, quantity }) => ({ menu_item_id: id, quantity })) }) });
    if (!response.ok) { const result = await response.json(); throw new Error(typeof result.detail === "string" ? result.detail : "Could not create order. Check your order and try again."); }
    const order: Order = await response.json();
    sessionStorage.setItem(pendingStorageKey, String(order.id));
    setSavedOrder(order); setPendingOrder(order.id); setCart([]); setReceipt(null);
    return order;
  };
  const appendCart = async (orderId: number) => {
    if (!cart.length) return;
    const response = await apiFetch(`${API}/orders/${orderId}/items`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ items: cart.map(({ id, quantity }) => ({ menu_item_id: id, quantity })) }) });
    const result = await response.json();
    if (!response.ok) throw new Error(typeof result.detail === "string" ? result.detail : "Could not add items.");
    setSavedOrder(result); setCart([]);
  };
  const appendOnly = async () => {
    if (paying.current || !pendingOrder) return;
    paying.current = true; setBusy(true);
    try { await appendCart(pendingOrder); setMessage("Items added to the table bill. Payment is still pending."); }
    catch (failure) { setMessage(failure instanceof Error ? failure.message : "Could not add items."); }
    finally { paying.current = false; setBusy(false); }
  };
  const createOnly = async () => {
    if (paying.current || !cart.length || pendingOrder || orderShortages.length || !stockReady) return;
    paying.current = true; setBusy(true); setMessage("Creating order…");
    try {
      const order = await saveCartOrder();
      setMessage(`Order #${order.id} created. Payment is pending; inventory is unchanged.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not create order"); }
    finally { paying.current = false; setBusy(false); void loadMenu().catch(() => setStockReady(false)); }
  };
  const createAndPay = async (method: "cash" | "card" | "qr") => {
    if (paying.current || (!cart.length && !pendingOrder) || orderShortages.length || !stockReady) return;
    paying.current = true; setBusy(true);
    setMessage("Processing simulated payment…");
    try {
      let orderId = pendingOrder;
      if (!orderId) {
      const order = await saveCartOrder();
      orderId = order.id;
      }
      if (pendingOrder && cart.length) await appendCart(pendingOrder);
      const pay = await apiFetch(`${API}/orders/${orderId}/pay`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ method }) });
      const result = await pay.json();
      if (pay.status === 409) {
        const existing = await apiFetch(`${API}/orders/${orderId}`);
        if (existing.ok) {
          const saved: Order = await existing.json();
          if (saved.status === "paid") {
            setReceipt(saved); setCart([]); setSavedOrder(null); setPendingOrder(null);
            sessionStorage.removeItem(pendingStorageKey);
          }
        }
      }
      if (!pay.ok) throw new Error(typeof result.detail === "string" ? result.detail : [result.detail.message, ...(result.detail.shortages ?? [])].join(". "));
      sessionStorage.removeItem(pendingStorageKey); setPendingOrder(null); setSavedOrder(null);
      setReceipt(result.order); setCart([]); setTableNumber(null); setWorkTicket(null); setMessage(result.message);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Payment failed"); }
    finally { paying.current = false; setBusy(false); }
  };
  const openTab = (next: Tab) => { setTab(next); setMessage(""); if (next === "orders") void readData<Order[]>(`/orders?trash=${ordersTrash}`).then(setOrders).catch(() => setMessage("Could not load orders.")); if (next === "inventory") void loadInventory().catch(() => setMessage("Could not load inventory.")); };
  const resumeOrder = (order: Order) => {
    setTableNumber(order.table_number ?? null); setWorkTicket(null);
    setCart([]); setReceipt(null); setSavedOrder(order); setPendingOrder(order.id);
    sessionStorage.setItem(pendingStorageKey, String(order.id));
    setTab("cashier"); setMessage(`Order #${order.id} is ready for payment.`);
  };
  const viewReceipt = (order: Order) => {
    setCart([]); setSavedOrder(null); setPendingOrder(null);
    sessionStorage.removeItem(pendingStorageKey);
    setTableNumber(null); setWorkTicket(null); setReceipt(order); setTab("cashier"); setMessage(`Showing the saved receipt for order #${order.id}.`);
  };
  const cancelOrder = async (order: Order) => {
    setBusy(true);
    try {
      const response = await apiFetch(`${API}/orders/${order.id}/cancel`, {method:"POST"});
      const result = await response.json();
      if (!response.ok) throw new Error(result.detail || "Could not cancel order");
      setOrders(current => current.map(item => item.id === result.id ? result : item));
      if (pendingOrder === order.id) { setPendingOrder(null); setSavedOrder(null); sessionStorage.removeItem(pendingStorageKey); }
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
      const response = await apiFetch(API + endpoint, { method: action === "delete" ? "DELETE" : "POST" });
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

  if (businessReady && canConfigure && (showSetup || (!business.onboarding_complete && !deferSetup))) return <BusinessSetup profile={business} onClose={() => { setShowSetup(false); setDeferSetup(true); }} onChanged={async profile => { setShowSetup(true); setBusiness(profile); setCategory("All items"); await loadMenu(); setCatalogVersion(value => value + 1); }} />;
  if (isSetupPage && !canConfigure) return <main className="auth-page"><section className="auth-card"><h1>Setup is managed by your platform administrator.</h1><p>Your account cannot create businesses or change their preset/workflows.</p><a href="/">Return to your workspace</a></section></main>;
  if (businessReady && !business.onboarding_complete && !canConfigure) return <main className="auth-page"><section className="auth-card"><h1>Your business is being set up.</h1><p>The platform administrator needs to finish your business profile before the workspace opens.</p><button onClick={async () => { await apiRequest("/auth/logout", { method: "POST" }); window.location.assign("/"); }}>Sign out</button></section></main>;
  return <main className="app-shell">
    <aside className="theme-control" ref={themePanel} onKeyDown={event => { if (event.key === "Escape") { setThemeMenuOpen(false); themePanel.current?.querySelector<HTMLButtonElement>(".theme-toggle")?.focus(); } }}>
      <button className="theme-toggle" aria-label="Change theme" title="Change theme" aria-expanded={themeMenuOpen} aria-controls="theme-options" onClick={() => setThemeMenuOpen(open => !open)}><svg viewBox="0 0 24 24" width="23" height="23" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18h1a2 2 0 0 0 1.7-3.1 1.5 1.5 0 0 1 1.3-2.3h2a3 3 0 0 0 3-3A9.6 9.6 0 0 0 12 3Z"/><circle cx="7.5" cy="10" r="1"/><circle cx="11" cy="6.8" r="1"/><circle cx="15.5" cy="8" r="1"/></svg></button>
      {themeMenuOpen && <fieldset id="theme-options" className="theme-options"><legend>Appearance</legend>{([{ value: "white", label: "White", detail: "Bright & clean" }, { value: "dark", label: "Dark", detail: "Soft contrast" }, { value: "code", label: "Code", detail: "Syntax highlights" }] as const).map(option => <label className={"theme-option " + (theme === option.value ? "selected" : "")} key={option.value}><input type="radio" name="theme" value={option.value} checked={theme === option.value} onChange={() => setTheme(option.value)} /><span className={"theme-swatch swatch-" + option.value} aria-hidden="true"/><span><strong>{option.label}</strong><small>{option.detail}</small></span></label>)}</fieldset>}
    </aside>
    <header><div><p className="eyebrow">SMARTSERVE · {businessLabels[business.business_type] ?? "POINT OF SALE"}</p><h1>{business.logo_url && <img className="business-logo" src={business.logo_url} alt="" onError={event => { event.currentTarget.hidden = true; }}/>} {business.name}</h1></div><nav aria-label="Main navigation">{([...(canManage ? ["owner" as const] : []), "cashier", "orders", ...(business.features.includes("inventory") ? ["inventory" as const] : []), ...(business.features.includes("tables") ? ["tables" as const] : []), ...(business.features.some(feature => ["appointments", "walk_ins", "jobs"].includes(feature)) ? ["work" as const] : [])]).map(item => <button aria-label={item === "cashier" || item === "inventory" ? item : undefined} className={tab === item ? "active" : ""} onClick={() => openTab(item as Tab)} key={item}>{item === "owner" ? "Owner dashboard" : item === "work" ? "Appointments & jobs" : item[0].toUpperCase() + item.slice(1)}</button>)}{canConfigure && <a className="primary-link" href="/platform">Platform admin</a>}{(account.businesses?.length || 0) > 1 && <select aria-label="Switch business" value={account.store_id || ""} onChange={async event => { await apiRequest("/auth/switch-business", jsonBody({ store_id: event.target.value })); window.location.assign("/"); }}>{account.businesses?.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select>}<button onClick={async () => { await apiRequest("/auth/logout", { method: "POST" }); window.location.assign("/"); }}>Sign out</button></nav></header>
    <AccountSecurity/>
    {businessError && <p role="alert" className="notice">{businessError}</p>}
    {message && <p className="notice" role="status">{message}</p>}
    {tab === "cashier" && <section className="cashier-grid">
      <div><p className="eyebrow">CHECKOUT</p><h2>{foodBusiness ? "Menu" : "Item library"}</h2><button disabled={busy} onClick={() => void loadMenu().catch(() => setStockReady(false))}>Refresh availability</button><p className="muted">Choose items, then take a simulated payment.</p><label className="catalog-search">Search items<input type="search" placeholder="Search by name, category or SKU" value={search} onChange={event => setSearch(event.target.value)} /></label><div className="category-tabs" role="group" aria-label="Catalog categories">{categories.map(value => <button key={value} aria-pressed={category === value} className={category === value ? "active" : ""} onClick={() => setCategory(value)}>{value}</button>)}</div><div className="menu-grid">{filteredMenu.map(item => { const shortages = shortagesFor([{ id: item.id, quantity: 1 }]); return <button className="menu-card" disabled={busy || (pendingOrder !== null && !savedOrder?.table_number) || !stockReady || shortages.length > 0} onClick={() => addToCart(item)} key={item.id}><strong>{item.name}</strong><span>{won(item.price)}</span><span className="catalog-item-meta">{item.category}{item.item_type === "service" ? " · Service" : ""}{item.sku ? ` · ${item.sku}` : ""}</span><small>{shortages.length ? "Unavailable — " + shortages.join("; ") : "Add to order"}</small></button>; })}</div>{filteredMenu.length === 0 && <p className="empty-state">{menu.length ? "No items match your search. Try another name or category." : "Your catalog is empty. Add items or choose a business preset in owner settings."}</p>}</div>
      <aside className="panel"><div className="section-heading"><h2>{pendingOrder ? `Order #${pendingOrder}` : "Current order"}</h2>{pendingOrder && <span className="badge open">Open</span>}</div><label>Order type <select disabled={busy || pendingOrder !== null} value={savedOrder?.order_type ?? orderType} onChange={e => setOrderType(e.target.value)}>{business.order_types.map(value => <option value={value} key={value}>{orderLabels[value]}</option>)}{savedOrder && !business.order_types.includes(savedOrder.order_type) && <option value={savedOrder.order_type}>{orderLabels[savedOrder.order_type] || savedOrder.order_type}</option>}</select></label>
        {(savedOrder?.order_type ?? orderType) === "dine_in" && business.features.includes("tables") && <label>Table<select aria-label="Table" disabled={busy || pendingOrder !== null} value={savedOrder?.table_number ?? tableNumber ?? ""} onChange={event => setTableNumber(Number(event.target.value) || null)}><option value="">Choose a table</option>{Array.from({ length: business.table_count }, (_, index) => <option key={index + 1} value={index + 1}>Table {index + 1}</option>)}</select></label>}
        {workTicket && <p className="notice">Checkout for #{workTicket.id}: {workTicket.customer} · {workTicket.title}</p>}
        {pendingOrder && savedOrder ? <>{savedOrder.items.map((item, index) => <div className="cart-line" key={`${item.menu_item_id}-${index}`}><span>{item.name}<small>{won(item.unit_price)} each</small></span><strong>× {item.quantity}</strong></div>)}<div className="total"><strong>Total</strong><strong>{won(savedOrder.total)}</strong></div><p className="muted">Saved order. Retry payment or manage it from Orders.</p>{savedOrder.table_number && cart.length > 0 && <div className="notice"><strong>Items to add</strong>{cart.map(line => <p key={line.id}>{line.name} × {line.quantity} · {won(line.price * line.quantity)}</p>)}<button disabled={busy || orderShortages.length > 0} onClick={() => void appendOnly()}>Add items to bill</button></div>}</> : cart.length ? <>{cart.map(line => <div className="cart-line" key={line.id}><span>{line.name}<small>{won(line.price)} each</small></span><div><button disabled={busy} onClick={() => changeQty(line.id, -1)} aria-label={`Remove one ${line.name}`}>−</button>{line.quantity}<button disabled={busy} onClick={() => changeQty(line.id, 1)} aria-label={`Add one ${line.name}`}>+</button></div></div>)}<div className="total"><strong>Total</strong><strong>{won(total)}</strong></div><button className="text-button" disabled={busy} onClick={() => setCart([])}>Clear cart</button></> : <p className="muted">Choose items or services to start.</p>}
        {orderShortages.length > 0 && <div className="notice" role="alert"><strong>This order is unavailable</strong>{orderShortages.map(text => <p key={text}>{text}</p>)}<p>Reduce the quantity or update ingredient stock.</p></div>}{!stockReady && <p role="alert">Stock availability could not be confirmed. Refresh availability before ordering.</p>}{cart.length > 0 && !pendingOrder && <button disabled={busy || !stockReady || orderShortages.length > 0} onClick={() => void createOnly()}>Create order</button>}
        {(cart.length > 0 || pendingOrder) && <div className="payments"><button disabled={busy || !stockReady || orderShortages.length > 0} onClick={() => createAndPay("cash")}>Pay cash</button><button disabled={busy || !stockReady || orderShortages.length > 0} onClick={() => createAndPay("card")}>Pay card</button><button disabled={busy || !stockReady || orderShortages.length > 0} onClick={() => createAndPay("qr")}>Pay QR</button></div>}
      </aside>
      {receipt && <section className="receipt"><p className="eyebrow">{business.name}</p>{business.address && <p>{business.address}</p>}{business.phone && <p>{business.phone}</p>}<p className="eyebrow">PAYMENT COMPLETE</p><h2>Receipt #{receipt.id}</h2><p className="muted">Paid {dateTime(receipt.paid_at)} · KST</p>{receipt.items.map((item, index) => <p key={`${item.menu_item_id}-${index}`}>{item.name} × {item.quantity}</p>)}<strong>{won(receipt.total)} · {receipt.payment_method?.toUpperCase()}</strong><p className="muted">{receipt.simulated_reference}</p>{receipt.table_number && <p>Table {receipt.table_number}</p>}<p>{business.receipt_footer}</p></section>}
    </section>}
    {tab === "tables" && <TableBoard onSelect={async (number, orderId) => {
      if (cart.length || (pendingOrder && orderId !== pendingOrder)) { setMessage("Finish or clear your current order before opening another table."); return; }
      if (orderId) resumeOrder(await readData<Order>(`/orders/${orderId}`));
      else { setTableNumber(number); setOrderType("dine_in"); setWorkTicket(null); setReceipt(null); setTab("cashier"); setMessage(`Table ${number} selected. Add items to start the bill.`); }
    }} />}
    {tab === "work" && <WorkflowDesk features={business.features} onCheckout={async ticket => {
      if (cart.length || (pendingOrder && ticket.order_id !== pendingOrder)) { throw new Error("Finish or clear your current order before opening another bill."); }
      if (ticket.order_status === "open" && ticket.order_id) resumeOrder(await readData<Order>(`/orders/${ticket.order_id}`));
      else { setWorkTicket(ticket); setTableNumber(null); setOrderType("service"); setCart([]); setReceipt(null); setTab("cashier"); setMessage(`Choose the items or services to bill for ${ticket.customer}.`); }
    }} />}
    {tab === "orders" && <section>
      <div className="section-heading"><div><p className="eyebrow">ORDER MANAGEMENT</p><h2>{ordersTrash ? "Order Trash" : "Orders"}</h2><p className="muted">{ordersTrash ? "Trashed cancelled orders are permanently deleted after 30 days. Restore returns them as cancelled." : "Resume or cancel unpaid orders. Move cancelled orders to Trash to remove them from this list."}</p></div>
      <div className="toolbar"><label>Status<select value={orderFilter} onChange={event => setOrderFilter(event.target.value)}><option value="all">All orders</option><option value="open">Open</option><option value="paid">Paid</option><option value="cancelled">Cancelled</option></select></label><label>Order date<input type="date" value={orderDate} onChange={event => setOrderDate(event.target.value)} /></label><button onClick={() => { setOrderDate(""); setOrderFilter("all"); }}>Clear filters</button><button onClick={() => openTab("orders")}>Refresh orders</button></div></div>
      <div className="toolbar" role="group" aria-label="Order folders"><button className={!ordersTrash ? "folder-active" : ""} disabled={busy} onClick={() => void showOrderFolder(false)}>Orders list</button><button className={ordersTrash ? "folder-active" : ""} disabled={busy} onClick={() => void showOrderFolder(true)}>Trash</button><span className="muted">Dates shown in Korea time (KST)</span></div><div className="month-folders">{orderMonths.map((month, index) => {
        const key = (ordersTrash ? "trash:" : "orders:") + month;
        return <details className="month-folder" key={key} open={monthOpen[key] ?? index === 0} onToggle={event => { const open = event.currentTarget.open; setMonthOpen(current => current[key] === open ? current : { ...current, [key]: open }); }}>
          <summary><strong>{monthLabel(month)}</strong><span className="month-count">{ordersByMonth[month].length} {ordersByMonth[month].length === 1 ? "order" : "orders"}</span></summary>
          <div className="table-wrap"><table><thead><tr><th>Order</th><th>Created (KST)</th><th>Items</th><th>Total</th><th>Status</th><th>{ordersTrash ? "Auto delete (KST)" : "Paid (KST)"}</th><th>Actions</th></tr></thead><tbody>{ordersByMonth[month].map(order => <tr key={order.id}><td><strong>#{order.id}</strong><small>{(order.table_number ? `Table ${order.table_number}` : orderLabels[order.order_type] || order.order_type.replace("_", " "))}</small></td><td>{dateTime(order.created_at)}</td><td>{order.items.map(item => item.name + " × " + item.quantity).join(", ")}</td><td>{won(order.total)}</td><td><span className={"badge " + order.status}>{order.status === "open" ? "Open" : order.status === "paid" ? "Paid" : "Cancelled"}</span></td><td>{dateTime(ordersTrash ? order.delete_after : order.paid_at)}</td><td>{ordersTrash ? <div className="row-actions"><button disabled={busy} onClick={() => void manageTrash(order, "restore")}>Restore</button><button className="danger" disabled={busy} onClick={() => void manageTrash(order, "delete")}>Delete forever</button></div> : order.status === "open" ? <div className="row-actions"><button className="primary" disabled={busy} onClick={() => resumeOrder(order)}>Resume</button><button disabled={busy} onClick={() => cancelOrder(order)}>Cancel</button></div> : order.status === "paid" ? <button onClick={() => viewReceipt(order)}>View receipt</button> : <button disabled={busy} onClick={() => void manageTrash(order, "trash")}>Move to Trash</button>}</td></tr>)}</tbody></table></div>
        </details>;
      })}</div>{visibleOrders.length === 0 && <p className="empty-state">{ordersTrash ? "Trash is empty." : "No orders match these filters."}</p>}
    </section>}
    {tab === "inventory" && <section><h2>Inventory</h2><p className="muted">Stock is reduced only after a successful simulated payment.</p><table><thead><tr><th>Stock item</th><th>In stock</th><th>Reorder level</th><th>Status</th></tr></thead><tbody>{inventory.map(item => <tr key={item.id}><td>{item.name}</td><td>{item.stock_quantity} {item.unit}</td><td>{item.reorder_level} {item.unit}</td><td><span className={item.low_stock ? "badge low" : "badge"}>{item.low_stock ? "Low stock" : "OK"}</span></td></tr>)}</tbody></table></section>}
    {canManage && tab === "owner" && <section>
      <div className="section-heading"><div><h2>Owner sales dashboard</h2><p className="muted">Daily totals include every paid order in the shared store, including test purchases.</p></div><div className="dashboard-actions"><a className="primary-link" href="#owner-management">Manage catalog &amp; inventory</a><button className="primary" aria-expanded={showFeedback} aria-controls="dashboard-feedback" onClick={() => setShowFeedback(open => !open)}>{showFeedback ? "Hide feedback form" : "Give feedback"}</button></div></div>
      <section id="dashboard-feedback" className="dashboard-feedback" hidden={!showFeedback} aria-labelledby="feedback-heading">
        <h3 id="feedback-heading">Share your feedback</h3>
        <iframe title="SmartServe feedback form" src="https://docs.google.com/forms/d/e/1FAIpQLScRpmihHlNK9OvHRW0wjTLktS0NJnQ4WAz-pzQmr9QvdVaeSw/viewform?embedded=true" loading="lazy">Loading feedback form…</iframe>
      </section>
      <div className="toolbar"><label>Sales date<input type="date" value={salesDate} onChange={event => { if (event.target.value) setSalesDate(event.target.value); }} /></label><button disabled={salesLoading} onClick={() => setSalesRefresh(value => value + 1)}>Refresh sales</button><span className="muted">Korea time (KST)</span></div>
      {salesLoading && <p role="status">Loading sales…</p>}{salesError && <p role="alert" className="notice">{salesError}</p>}
      {dashboard && <><div className="stats"><article><span>{"Sales on " + dashboard.date}</span><strong>{won(dashboard.sales_total)}</strong></article><article><span>Paid orders on {dashboard.date}</span><strong>{dashboard.paid_orders}</strong></article></div><h3>Paid sales on {dashboard.date}</h3><div className="table-wrap"><table><thead><tr><th>Order</th><th>Paid (KST)</th><th>Items</th><th>Type</th><th>Total</th><th>Payment</th></tr></thead><tbody>{dashboard.recent_sales.map(order => <tr key={order.id}><td>#{order.id}</td><td>{dateTime(order.paid_at)}</td><td>{order.items.map(item => item.name + " × " + item.quantity).join(", ")}</td><td>{(order.table_number ? `Table ${order.table_number}` : orderLabels[order.order_type] || order.order_type.replace("_", " "))}</td><td>{won(order.total)}</td><td>{order.payment_method?.toUpperCase()}</td></tr>)}</tbody></table>{dashboard.paid_orders === 0 && <p className="empty-state">No paid sales on this date.</p>}</div></>}
      <section className="panel profile-summary"><div><p className="eyebrow">BUSINESS PROFILE</p><h3>{business.name}</h3><p className="muted">{businessLabels[business.business_type]} · {business.operation_mode.replace(/_/g, " ")} · {business.features.join(" / ")}</p></div>{canConfigure ? <button className="primary" onClick={() => setShowSetup(true)}>Edit business profile</button> : <span className="badge">Owner workspace</span>}</section>
      <BusinessAccountSettings session={account} profile={business} onChanged={setBusiness} />
      <OwnerManagement key={catalogVersion} onMenuChanged={loadMenu} onInventoryChanged={loadInventory} />
    </section>}
  </main>;
}

createRoot(document.getElementById("root")!).render(
  <StrictMode><AccountAccess>{account => {
    if (account.user?.role === "platform_admin" && (!account.store_id || window.location.pathname === "/platform")) return <PlatformConsole session={account} />;
    if (window.location.pathname === "/platform" && account.user?.role !== "platform_admin") return <main className="auth-page"><section className="auth-card"><h1>Platform administrator access required.</h1><a href="/">Return to your workspace</a></section></main>;
    return <App key={`${account.user?.id}:${account.store_id}`} account={account}/>;
  }}</AccountAccess></StrictMode>,
);
