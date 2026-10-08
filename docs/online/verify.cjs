const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.SMARTSERVE_URL;
if (!base) throw new Error('Set SMARTSERVE_URL to the public URL');
async function read(endpoint) {
  const response = await fetch(base + endpoint);
  assert.equal(response.ok, true, endpoint);
  return response.json();
}
async function main() {
  assert.equal((await read('/health')).status, 'ok');
  const before = await read('/inventory');
  const salesBefore = await read('/dashboard/sales');
  const menu = await read('/menu');
  const recipes = await read('/owner/menu');
  const item = menu.find(candidate => { const recipe = recipes.find(r => r.id === candidate.id)?.recipe; return recipe?.length && recipe.every(line => before.find(stock => stock.id === line.ingredient_id)?.stock_quantity >= line.quantity); });
  assert.ok(item, 'Add an active menu item with sufficient ingredient stock before running this check.');
  const recipe = recipes.find(r => r.id === item.id).recipe;
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROMIUM_PATH });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 950 } });
    await page.goto(base);
    await page.getByRole('button').filter({ has: page.getByText(item.name, { exact: true }) }).click();
    const created = page.waitForResponse(r => r.url() === base + '/orders' && r.request().method() === 'POST');
    await page.getByRole('button', { name: 'Create order', exact: true }).click();
    const response = await created;
    assert.equal(response.status(), 201);
    const order = await response.json();
    assert.equal(order.status, 'open'); assert.equal(order.total, item.price);
    assert.deepEqual(await read('/inventory'), before);
    await page.reload();
    await page.locator('aside .cart-line').filter({ hasText: item.name }).waitFor();
    await page.getByRole('button', { name: 'Pay cash', exact: true }).click();
    await page.getByRole('heading', { name: `Receipt #${order.id}`, exact: true }).waitFor();
    const after = await read('/inventory');
    for (const ingredient of before) {
      const ending = after.find(i => i.id === ingredient.id);
      assert.ok(Math.abs(ingredient.stock_quantity - ending.stock_quantity - (recipe.find(line => line.ingredient_id === ingredient.id)?.quantity ?? 0)) < 0.000001);
    }
    const duplicate = await fetch(`${base}/orders/${order.id}/pay`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ method: 'cash' }) });
    assert.equal(duplicate.status, 409); assert.deepEqual(await read('/inventory'), after);
    const salesAfter = await read('/dashboard/sales');
    assert.equal(salesAfter.paid_orders - salesBefore.paid_orders, 1);
    assert.equal(salesAfter.sales_total - salesBefore.sales_total, item.price);
    await page.getByRole('button', { name: 'Owner dashboard', exact: true }).click();
    await page.getByRole('cell', { name: `#${order.id}`, exact: true }).waitFor();
    await page.screenshot({ path: path.join(__dirname, 'public-check.png'), fullPage: true });
    const result = { result: 'PASS', url: base, checkedAt: new Date().toISOString(), orderId: order.id, total: order.total, refreshRecovery: true, receipt: true, itemName: item.name, recipeDeductionVerified: true, duplicatePaymentStatus: duplicate.status, paidOrdersAdded: 1, salesAdded: item.price };
    fs.writeFileSync(path.join(__dirname, 'verification.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify(result, null, 2));
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
