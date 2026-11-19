import { useState } from "react";
import "./home.css";

const views = {
  Checkout: {
    title: "Take orders at the counter",
    detail: "Keep open orders, find items in your catalog, and issue receipts from the same screen.",
    columns: ["Item", "Qty", "Amount"],
    rows: [["Iced latte", "2", "₩10,000"], ["Butter croissant", "1", "₩3,500"], ["Cold brew", "1", "₩4,500"]],
    summary: ["Order total", "₩18,000"],
  },
  Inventory: {
    title: "See what’s in stock",
    detail: "Track ingredients and stock levels. Link recipes to menu items so paid orders update stock.",
    columns: ["Ingredient", "On hand", "Status"],
    rows: [["Espresso beans", "740 g", "In stock"], ["Whole milk", "3.2 L", "In stock"], ["Vanilla syrup", "120 ml", "Low stock"]],
    summary: ["Low-stock alerts", "1 item"],
  },
  Sales: {
    title: "Review your sales by day",
    detail: "See paid orders, totals, and payment methods for the date you select.",
    columns: ["Order", "Method", "Total"],
    rows: [["#1042", "Card", "₩18,000"], ["#1041", "Cash", "₩12,500"], ["#1040", "QR", "₩9,000"]],
    summary: ["Sample sales", "₩39,500"],
  },
} as const;

export function Home() {
  const [selected, setSelected] = useState<keyof typeof views>("Checkout");
  const view = views[selected];
  return <div className="product-home">
    <a className="home-skip" href="#home-main">Skip to content</a>
    <header className="home-header home-width">
      <a className="home-brand" href="/"><span aria-hidden="true">S</span>SmartServe</a>
      <nav aria-label="Site navigation">
        <a className="home-product-link" href="#product">Product</a>
        <a href="/login">Sign in</a>
        <a className="home-cta home-cta-small" href="/register">Register</a>
      </nav>
    </header>
    <main id="home-main">
      <section className="home-hero home-width" id="product">
        <div className="home-intro">
          <p className="home-kicker">Point of sale for small businesses</p>
          <h1>Your business.<br/>Your own POS.</h1>
          <p>Set up SmartServe for the way you work. Take orders, manage stock, and see your daily sales in one workspace.</p>
          <a className="home-cta" href="/register">Create your business</a>
        </div>
        <section className="home-preview" aria-label="Interactive product preview">
          <div className="home-preview-top"><strong>Sample café</strong><span>Demo data</span></div>
          <div className="home-preview-body">
            <div className="home-preview-nav" role="group" aria-label="Preview a feature">
              {(Object.keys(views) as (keyof typeof views)[]).map(name => <button key={name} type="button" aria-pressed={selected === name} onClick={() => setSelected(name)}>{name}</button>)}
            </div>
            <div className="home-preview-content" aria-live="polite">
              <h2>{view.title}</h2>
              <p>{view.detail}</p>
              <table aria-label={selected + " example"}>
                <thead><tr>{view.columns.map(column => <th scope="col" key={column}>{column}</th>)}</tr></thead>
                <tbody>{view.rows.map(row => <tr key={row[0]}><th scope="row">{row[0]}</th><td>{row[1]}</td><td>{row[2]}</td></tr>)}</tbody>
              </table>
              <div className="home-preview-total"><span>{view.summary[0]}</span><strong>{view.summary[1]}</strong></div>
            </div>
          </div>
        </section>
      </section>
      <section className="home-workflows">
        <div className="home-width home-workflow-grid">
          <div><h2>Choose a setup that fits your business.</h2><p>Start with a preset or choose your own workflows during setup.</p></div>
          <dl>
            <div><dt>Cafés &amp; restaurants</dt><dd>Table service, takeaway, and recipes</dd></div>
            <div><dt>Retail &amp; groceries</dt><dd>In-store sales, pickup, and stock</dd></div>
            <div><dt>Salons &amp; service businesses</dt><dd>Appointments, walk-ins, or repair jobs</dd></div>
          </dl>
        </div>
      </section>
      <section className="home-setup home-width" aria-labelledby="home-setup-heading">
        <h2 id="home-setup-heading">Set up your POS</h2>
        <ol>
          <li><strong>Register your business</strong><p>Enter your business name and verify your email.</p></li>
          <li><strong>Choose your workflow</strong><p>Pick your business type and the tools you want to use.</p></li>
          <li><strong>Open your workspace</strong><p>Add your catalog and try checkout with simulated payments.</p></li>
        </ol>
        <a className="home-cta" href="/register">Register your business</a>
      </section>
    </main>
    <footer className="home-footer home-width"><a className="home-brand" href="/"><span aria-hidden="true">S</span>SmartServe</a><a href="/login">Sign in</a></footer>
  </div>;
}
