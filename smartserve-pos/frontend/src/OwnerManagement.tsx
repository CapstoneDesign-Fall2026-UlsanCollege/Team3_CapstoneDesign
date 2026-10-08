import { useEffect, useState, type FormEvent } from "react";

const API = "http://localhost:8000";
type Ingredient = { id: number; name: string; unit: string; stock_quantity: number; reorder_level: number; active: boolean; unit_editable?: boolean; convertible_units?: string[] };
type MenuItem = { id: number; name: string; price: number; active: boolean; recipe: { ingredient_id: number; ingredient_name: string; quantity: number }[] };
type RecipeInput = { ingredient_id: string; quantity: string; unit?: string };
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
  const [menuFormOpen, setMenuFormOpen] = useState(false);
  const [ingredientFormOpen, setIngredientFormOpen] = useState(false);
  const [editingMenu, setEditingMenu] = useState<number | null>(null);
  const [editingIngredient, setEditingIngredient] = useState<number | null>(null);
  const resetMenu = () => { setMessage(""); setMenuFormOpen(false); setEditingMenu(null); setMenuName(""); setPrice(""); setRecipe([{ ingredient_id: "", quantity: "" }]); };
  const resetIngredient = () => { setMessage(""); setIngredientFormOpen(false); setEditingIngredient(null); setIngredientName(""); setUnit("g"); setStock(""); setReorder("0"); };
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const editedIngredient = ingredients.find(item => item.id === editingIngredient);
  const unitRestricted = editingIngredient !== null && editedIngredient?.unit_editable !== true;
  const allowedUnits = editedIngredient?.convertible_units ?? [editedIngredient?.unit];
  const unitLocked = unitRestricted && allowedUnits.length < 2;
  const changeUnit = (next: string) => {
    const factors: Record<string, number> = { g: 1, kg: 1000, ml: 1, l: 1000 };
    const compatible = (["g", "kg"].includes(unit) && ["g", "kg"].includes(next)) || (["ml", "l"].includes(unit) && ["ml", "l"].includes(next));
    if (editingIngredient !== null && compatible) {
      const factor = factors[unit] / factors[next];
      if (stock !== "") setStock(String(Number((Number(stock) * factor).toFixed(6))));
      if (reorder !== "") setReorder(String(Number((Number(reorder) * factor).toFixed(6))));
    }
    setUnit(next);
  };
  const activeIngredients = ingredients.filter(item => item.active);

  useEffect(() => {
    void Promise.all([request<Ingredient[]>("/owner/inventory"), request<MenuItem[]>("/owner/menu")])
      .then(([inventory, menuItems]) => { setIngredients(inventory); setMenu(menuItems); })
      .catch(error => setMessage(error.message));
  }, []);

  const addIngredient = async (event: FormEvent) => {
    event.preventDefault(); setBusy(true); setMessage("");
    try {
      const created = await request<Ingredient>(editingIngredient === null ? "/owner/inventory" : `/owner/inventory/${editingIngredient}`, { method: editingIngredient === null ? "POST" : "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: ingredientName, unit, stock_quantity: Number(stock), reorder_level: Number(reorder) }) });
      setIngredients(current => [...current.filter(item => item.id !== created.id), created].sort((a, b) => a.name.localeCompare(b.name)));
      resetIngredient();
      await onInventoryChanged();
      setMenu(await request<MenuItem[]>("/owner/menu"));
      setMessage(`${created.name} was saved in inventory.`);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Could not add ingredient"); }
    finally { setBusy(false); }
  };
  const addMenuItem = async (event: FormEvent) => {
    event.preventDefault(); setBusy(true); setMessage("");
    try {
      const created = await request<MenuItem>(editingMenu === null ? "/owner/menu" : `/owner/menu/${editingMenu}`, { method: editingMenu === null ? "POST" : "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: menuName, price: Number(price), recipe: recipe.map(line => ({ ingredient_id: Number(line.ingredient_id), quantity: Number(line.quantity), unit: line.unit || ingredients.find(item => String(item.id) === line.ingredient_id)?.unit })) }) });
      setMenu(current => [...current.filter(item => item.id !== created.id), created].sort((a, b) => a.name.localeCompare(b.name)));
      resetMenu();
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
    {message && <div className="notice owner-notice"><p role="status">{message}</p><button type="button" aria-label="Dismiss message" onClick={() => setMessage("")}>×</button></div>}
    <div className="management-grid">
      <article className="panel management-card"><h3>Menu items</h3><details className="management-disclosure" open={menuFormOpen} onToggle={event => setMenuFormOpen(event.currentTarget.open)}><summary>{editingMenu === null ? "Add menu item" : "Edit menu item"}</summary><form onSubmit={addMenuItem} className="management-form"><label>Item name<input required maxLength={120} value={menuName} onChange={event => setMenuName(event.target.value)} placeholder="e.g. Matcha Latte" /></label><label>Price (KRW)<input required min="1" step="1" type="number" value={price} onChange={event => setPrice(event.target.value)} /></label><strong>Recipe per item</strong><p className="muted form-hint">Enter the amount for one serving. Choose g/kg or ml/l; it converts automatically to the inventory unit when saved.</p>{recipe.map((line, index) => <div className="recipe-row" key={index}><label>Ingredient<select required value={line.ingredient_id} onChange={event => setRecipe(current => current.map((entry, i) => i === index ? { ...entry, ingredient_id: event.target.value, unit: ingredients.find(item => String(item.id) === event.target.value)?.unit } : entry))}><option value="">Select ingredient</option>{activeIngredients.map(item => <option value={item.id} key={item.id}>{item.name} ({item.unit})</option>)}</select></label><label>Quantity<input required min="0.000001" step="0.000001" type="number" value={line.quantity} onChange={event => setRecipe(current => current.map((entry, i) => i === index ? { ...entry, quantity: event.target.value } : entry))} /></label><label>Recipe unit<select aria-label={`Recipe unit ${index + 1}`} value={line.unit || ingredients.find(item => String(item.id) === line.ingredient_id)?.unit || ""} onChange={event => setRecipe(current => current.map((entry, i) => i === index ? { ...entry, unit: event.target.value } : entry))}>{(ingredients.find(item => String(item.id) === line.ingredient_id)?.convertible_units?.length ? ingredients.find(item => String(item.id) === line.ingredient_id)!.convertible_units! : [ingredients.find(item => String(item.id) === line.ingredient_id)?.unit || ""]).map(value => <option key={value} value={value}>{value || "Select ingredient first"}</option>)}</select></label>{recipe.length > 1 && <button type="button" aria-label={`Remove recipe row ${index + 1}`} onClick={() => setRecipe(current => current.filter((_, i) => i !== index))}>×</button>}</div>)}<button type="button" onClick={() => setRecipe(current => [...current, { ingredient_id: "", quantity: "" }])}>Add ingredient to recipe</button><button className="primary" disabled={busy || activeIngredients.length === 0} type="submit">{editingMenu === null ? "Add menu item" : "Save menu item"}</button>{editingMenu !== null && <button type="button" disabled={busy} onClick={resetMenu}>Cancel editing menu</button>}</form></details><div className="management-list">{menu.filter(item => item.active).map(item => <div className="management-row" key={item.id}><div><strong>{item.name}</strong><small>{won(item.price)} · {item.recipe.map(line => `${line.quantity} ${ingredients.find(i => i.id === line.ingredient_id)?.unit ?? ""} ${line.ingredient_name}`).join(", ")}</small></div>{item.active ? <div className="row-actions"><button disabled={busy} onClick={() => { setMenuFormOpen(true); setEditingMenu(item.id); setMenuName(item.name); setPrice(String(item.price)); setRecipe(item.recipe.map(line => ({ ingredient_id: String(line.ingredient_id), quantity: String(line.quantity) }))); setMessage(""); document.getElementById("owner-management")?.scrollIntoView({ behavior: "smooth" }); }}>Edit</button><button disabled={busy || editingMenu === item.id} onClick={() => removeMenuItem(item)}>Remove</button></div> : <span className="badge cancelled">Removed</span>}</div>)}</div></article>
      <article className="panel management-card"><h3>Ingredients</h3><details className="management-disclosure" open={ingredientFormOpen} onToggle={event => setIngredientFormOpen(event.currentTarget.open)}><summary>{editingIngredient === null ? "Add ingredient" : "Edit ingredient"}</summary><p className="muted form-hint">Choose a unit and use that same unit for stock and recipes. Switching g/kg or ml/l while editing converts stock, thresholds and saved recipes.</p><form onSubmit={addIngredient} className="management-form"><label>Ingredient name<input required maxLength={120} value={ingredientName} onChange={event => setIngredientName(event.target.value)} placeholder="e.g. Matcha powder" /></label><div className="form-pair"><label>Unit<select aria-label="Unit" disabled={unitLocked} aria-describedby={unitRestricted ? "unit-lock-help" : undefined} value={unit} onChange={event => changeUnit(event.target.value)}>{!["g", "kg", "ml", "l", "pcs"].includes(unit) && <option value={unit}>{unit}</option>}<option value="g" disabled={unitRestricted && !allowedUnits.includes("g")}>Grams (g)</option><option value="kg" disabled={unitRestricted && !allowedUnits.includes("kg")}>Kilograms (kg)</option><option value="ml" disabled={unitRestricted && !allowedUnits.includes("ml")}>Millilitres (ml)</option><option value="l" disabled={unitRestricted && !allowedUnits.includes("l")}>Litres (l)</option><option value="pcs" disabled={unitRestricted && !allowedUnits.includes("pcs")}>Pieces (pcs)</option></select>{unitRestricted && <small id="unit-lock-help" className="muted">Only compatible units are available for an ingredient with recipes or stock history. Quantities are converted when you save.</small>}</label><label>{editingIngredient === null ? "Starting stock" : "Current stock"} ({unit})<input required min="0" step="0.000001" type="number" value={stock} onChange={event => setStock(event.target.value)} /></label></div><label>Low-stock threshold ({unit})<input required min="0" step="0.000001" type="number" value={reorder} onChange={event => setReorder(event.target.value)} /></label><button className="primary" disabled={busy} type="submit">{editingIngredient === null ? "Add ingredient" : "Save ingredient"}</button>{editingIngredient !== null && <button type="button" disabled={busy} onClick={resetIngredient}>Cancel editing ingredient</button>}</form></details><div className="management-list">{activeIngredients.map(item => <div className="management-row" key={item.id}><div><strong>{item.name}</strong><small>{item.stock_quantity} {item.unit} in stock · low at or below {item.reorder_level} {item.unit}</small></div>{item.active ? <div className="row-actions"><button disabled={busy} onClick={() => { setIngredientFormOpen(true); setEditingIngredient(item.id); setIngredientName(item.name); setUnit(item.unit); setStock(String(item.stock_quantity)); setReorder(String(item.reorder_level)); setMessage(""); document.getElementById("owner-management")?.scrollIntoView({ behavior: "smooth" }); }}>Edit</button><button disabled={busy || editingIngredient === item.id} onClick={() => removeIngredient(item)}>Remove</button></div> : <span className="badge cancelled">Removed</span>}</div>)}</div></article>
    </div>
  </section>;
}
