// Run only against an isolated demo database; this creates and pays sample orders.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const api = 'http://localhost:8000';
async function read(endpoint) {
  const response = await fetch(api + endpoint);
  assert.equal(response.ok, true, endpoint);
  return response.json();
}
async function main() {
  const inventoryBefore = await read('/inventory');
  const salesBefore = await read('/dashboard/sales');
  const latte = (await read('/menu')).find(item => item.name === 'Caffè Latte');
  assert.equal(latte.price, 4500, 'Use seeded demo prices');
  const browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await page.goto('http://localhost:5173');
    const add = page.getByRole('button').filter({ hasText: 'Caffè Latte' });
    await add.click(); await add.click();
    // A failed creation must preserve the cart so the cashier can retry.
    await page.route('**/orders', route => route.fulfill({ status: 503, contentType: 'application/json', body: '{"detail":"Test unavailable API"}' }));
    await page.getByRole('button', { name: 'Create order', exact: true }).click();
    await page.getByRole('status').filter({ hasText: 'Could not create order' }).waitFor();
    assert.match(await page.locator('aside').innerText(), /9,000/);
    await page.unroute('**/orders');
    const createdResponse = page.waitForResponse(response => response.url() === api + '/orders' && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Create order', exact: true }).click();
    const response = await createdResponse;
    assert.equal(response.status(), 201);
    const order = await response.json();
    assert.equal(order.status, 'open');
    assert.equal(order.total, 9000);
    assert.equal(order.items[0].quantity, 2);
    assert.equal(order.items[0].unit_price, 4500);
    assert.equal(order.inventory_deducted, false);
    await page.getByRole('heading', { name: `Order #${order.id}`, exact: true }).waitFor();
    assert.deepEqual(await read('/inventory'), inventoryBefore);
    assert.equal((await read('/dashboard/sales')).paid_orders, salesBefore.paid_orders);
    assert.equal(await add.isDisabled(), true);
    await page.reload();
    await page.locator('aside .cart-line').filter({ hasText: 'Caffè Latte' }).waitFor();
    assert.match(await page.locator('aside').innerText(), /9,000/);
    fs.mkdirSync(path.join(__dirname, 'screenshots'), { recursive: true });
    await page.screenshot({ path: path.join(__dirname, 'screenshots/01-created-order.png'), fullPage: true });
    await page.getByRole('button', { name: 'Pay cash', exact: true }).click();
    await page.getByRole('heading', { name: `Receipt #${order.id}`, exact: true }).waitFor();
    const paid = await read(`/orders/${order.id}`);
    assert.equal(paid.status, 'paid'); assert.equal(paid.total, 9000);
    const after = await read('/inventory');
    const quantity = (rows, name) => rows.find(row => row.name === name).stock_quantity;
    assert.equal(quantity(inventoryBefore, 'Milk') - quantity(after, 'Milk'), 500);
    assert.equal(quantity(inventoryBefore, 'Coffee beans') - quantity(after, 'Coffee beans'), 36);
    const duplicate = await fetch(`${api}/orders/${order.id}/pay`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ method: 'cash' }) });
    assert.equal(duplicate.status, 409);
    assert.deepEqual(await read('/inventory'), after);
    const sales = await read('/dashboard/sales');
    assert.equal(sales.paid_orders - salesBefore.paid_orders, 1);
    assert.equal(sales.sales_total - salesBefore.sales_total, 9000);
    await page.screenshot({ path: path.join(__dirname, 'screenshots/02-paid-receipt.png'), fullPage: true });
    const result = { runAt: new Date().toISOString(), result: 'PASS', environment: 'Isolated Docker PostgreSQL/FastAPI/Vite with browser automation', orderId: order.id, total: 9000, creationFailurePreservesCart: true, unpaidStockUnchanged: true, refreshRestoresOrder: true, milkDeducted: 500, beansDeducted: 36, duplicatePaymentStatus: duplicate.status, duplicateStockUnchanged: true, paidOrdersAdded: 1, salesAdded: 9000 };
    fs.writeFileSync(path.join(__dirname, 'results.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify(result, null, 2));
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
