import { useEffect, useState, type FormEvent } from "react";

const API = "http://localhost:8000";
type Ingredient = { id: number; name: string; unit: string; stock_quantity: number; reorder_level: number; active: boolean };
type MenuItem = { id: number; name: string; price: number; active: boolean; recipe: { ingredient_id: number; ingredient_name: string; quantity: number }[] };
type RecipeInput = { ingredient_id: string; quantity: string };
type Props = { onMenuChanged: () => Promise<void>; onInventoryChanged: () => Promise<void> };
const won = (value: number) => new Intl.NumberFormat("ko-KR", { style: "currency", currency: "KRW", maximumFractionDigits: 0 }).format(value);

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, options);
  const result = await response.json();
  if (!response.ok) throw new Error(typeof result.detail === "string" ? result.detail : "Could not save changes");
  return result as T;
}

export function OwnerManagement({ onMenuChanged, onInventoryChanged }: Props) {
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [ingredientName, setIngredientName] = useState("");
  const [unit, setUnit] = useState("g");
  const [stock, setStock] = useState("");
  const [reorder, setReorder] = useState("0");
  const [menuName, setMenuName] = useState("");
  const [price, setPrice] = useState("");
  const [recipe, setRecipe] = useState<RecipeInput[]>([{ ingredient_id: "", quantity: "" }]);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const activeIngredients = ingredients.filter(item => item.active);

  useEffect(() => {
    void Promise.all([request<Ingredient[]>("/owner/inventory"), request<MenuItem[]>("/owner/menu")])
      .then(([inventory, menuItems]) => { setIngredients(inventory); setMenu(menuItems); })
      .catch(error => setMessage(error.message));
  }, []);

  const addIngredient = async (event: FormEvent) => {
    event.preventDefault(); setBusy(true); setMessage("");
    try {
      const created = await request<Ingredient>("/owner/inventory", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: ingredientName, unit, stock_quantity: Number(stock), reorder_level: Number(reorder) }) });
      setIngredients(current => [...current, created].sort((a, b) => a.name.localeCompare(b.name)));
      setIngredientName(""); setStock(""); setReorder("0");
      await onInventoryChanged();
      setMessage(`${created.name} was added to inventory.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not add ingredient"); }
    finally { setBusy(false); }
  };
  const addMenuItem = async (event: FormEvent) => {
    event.preventDefault(); setBusy(true); setMessage("");
    try {
      const created = await request<MenuItem>("/owner/menu", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: menuName, price: Number(price), recipe: recipe.map(line => ({ ingredient_id: Number(line.ingredient_id), quantity: Number(line.quantity) })) }) });
      setMenu(current => [...current, created].sort((a, b) => a.name.localeCompare(b.name)));
      setMenuName(""); setPrice(""); setRecipe([{ ingredient_id: "", quantity: "" }]);
      await onMenuChanged();
      setMessage(`${created.name} is now available on the cashier menu.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not add menu item"); }
    finally { setBusy(false); }
  };
  const removeMenuItem = async (item: MenuItem) => {
    if (!window.confirm(`Remove ${item.name} from the cashier menu? Past receipts will be kept.`)) return;
    setBusy(true); setMessage("");
    try {
      const removed = await request<MenuItem>(`/owner/menu/${item.id}`, { method: "DELETE" });
      setMenu(current => current.map(entry => entry.id === item.id ? removed : entry));
      await onMenuChanged();
      setMessage(`${item.name} was removed from the cashier menu.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not remove menu item"); }
    finally { setBusy(false); }
  };
  const removeIngredient = async (item: Ingredient) => {
    if (!window.confirm(`Remove ${item.name} from active inventory?`)) return;
    setBusy(true); setMessage("");
    try {
      const removed = await request<Ingredient>(`/owner/inventory/${item.id}`, { method: "DELETE" });
      setIngredients(current => current.map(entry => entry.id === item.id ? removed : entry));
      await onInventoryChanged();
      setMessage(`${item.name} was removed from active inventory.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not remove ingredient"); }
    finally { setBusy(false); }
  };

  return <section className="owner-management" id="owner-management">
    <div className="section-heading"><div><p className="eyebrow">OWNER CONTROLS</p><h2>Manage menu and inventory</h2><p className="muted">Add ingredients first, then connect them to new menu items with a recipe.</p></div></div>
    {message && <p className="notice" role="status">{message}</p>}
    <div className="management-grid">
      <article className="panel management-card"><h3>Menu items</h3><form onSubmit={addMenuItem} className="management-form"><label>Item name<input required maxLength={120} value={menuName} onChange={event => setMenuName(event.target.value)} placeholder="e.g. Matcha Latte" /></label><label>Price (KRW)<input required min="1" step="1" type="number" value={price} onChange={event => setPrice(event.target.value)} /></label><strong>Recipe per item</strong>{recipe.map((line, index) => <div className="recipe-row" key={index}><label>Ingredient<select required value={line.ingredient_id} onChange={event => setRecipe(current => current.map((entry, i) => i === index ? { ...entry, ingredient_id: event.target.value } : entry))}><option value="">Select ingredient</option>{activeIngredients.map(item => <option value={item.id} key={item.id}>{item.name} ({item.unit})</option>)}</select></label><label>Quantity<input required min="0.01" step="0.01" type="number" value={line.quantity} onChange={event => setRecipe(current => current.map((entry, i) => i === index ? { ...entry, quantity: event.target.value } : entry))} /></label>{recipe.length > 1 && <button type="button" aria-label={`Remove recipe row ${index + 1}`} onClick={() => setRecipe(current => current.filter((_, i) => i !== index))}>×</button>}</div>)}<button type="button" onClick={() => setRecipe(current => [...current, { ingredient_id: "", quantity: "" }])}>Add ingredient to recipe</button><button className="primary" disabled={busy || activeIngredients.length === 0} type="submit">Add menu item</button></form><div className="management-list">{menu.map(item => <div className="management-row" key={item.id}><div><strong>{item.name}</strong><small>{won(item.price)} · {item.recipe.map(line => `${line.quantity} ${ingredients.find(i => i.id === line.ingredient_id)?.unit ?? ""} ${line.ingredient_name}`).join(", ")}</small></div>{item.active ? <button disabled={busy} onClick={() => removeMenuItem(item)}>Remove</button> : <span className="badge cancelled">Removed</span>}</div>)}</div></article>
      <article className="panel management-card"><h3>Ingredients</h3><form onSubmit={addIngredient} className="management-form"><label>Ingredient name<input required maxLength={120} value={ingredientName} onChange={event => setIngredientName(event.target.value)} placeholder="e.g. Matcha powder" /></label><div className="form-pair"><label>Unit<input required maxLength={20} value={unit} onChange={event => setUnit(event.target.value)} placeholder="g or ml" /></label><label>Starting stock<input required min="0" step="0.01" type="number" value={stock} onChange={event => setStock(event.target.value)} /></label></div><label>Low-stock threshold<input required min="0" step="0.01" type="number" value={reorder} onChange={event => setReorder(event.target.value)} /></label><button className="primary" disabled={busy} type="submit">Add ingredient</button></form><div className="management-list">{ingredients.map(item => <div className="management-row" key={item.id}><div><strong>{item.name}</strong><small>{item.stock_quantity} {item.unit} in stock · low at or below {item.reorder_level} {item.unit}</small></div>{item.active ? <button disabled={busy} onClick={() => removeIngredient(item)}>Remove</button> : <span className="badge cancelled">Removed</span>}</div>)}</div></article>
    </div>
  </section>;
}
