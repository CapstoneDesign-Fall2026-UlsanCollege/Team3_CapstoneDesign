// Automated developer-PC check, not independent teammate reproduction.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const api = 'http://localhost:8000';
async function read(endpoint) {
  const response = await fetch(api + endpoint);
  assert.equal(response.ok, true);
  return response.json();
}
async function main() {
  fs.mkdirSync(path.join(__dirname, 'screenshots'), { recursive: true });
  const before = await read('/inventory');
  const salesBefore = await read('/dashboard/sales');
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROMIUM_PATH });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
    const shot = name => page.screenshot({ path: path.join(__dirname, 'screenshots', name), fullPage: true });
    const tab = name => page.getByRole('button', { name, exact: true }).click();
    await page.goto('http://localhost:5173');
    await tab('inventory');
    await page.getByRole('cell', { name: 'Milk', exact: true }).waitFor();
    await shot('01-inventory-before.png');
    await tab('Owner dashboard');
    await page.getByText('Sales today', { exact: true }).waitFor();
    await shot('02-sales-before.png');
    await tab('cashier');
    await page.getByRole('button').filter({ hasText: 'Americano' }).click();
    await page.getByRole('button').filter({ hasText: 'Milk Tea' }).click();
    await page.locator('aside select').selectOption('takeaway');
    const created = page.waitForResponse(r => r.url() === api + '/orders' && r.request().method() === 'POST');
    await tab('Create order');
    const response = await created;
    assert.equal(response.status(), 201);
    const order = await response.json();
    assert.equal(order.total, 8500); assert.equal(order.status, 'open');
    assert.equal(order.order_type, 'takeaway'); assert.equal(order.inventory_deducted, false);
    assert.deepEqual(order.items.map(i => [i.name, i.quantity, i.unit_price]).sort(), [['Americano', 1, 3500], ['Milk Tea', 1, 5000]]);
    assert.deepEqual(await read('/inventory'), before);
    await page.getByRole('heading', { name: `Order #${order.id}`, exact: true }).waitFor();
    await shot('03-unpaid-mixed-order.png');
    await page.reload();
    await page.locator('aside .cart-line').filter({ hasText: 'Milk Tea' }).waitFor();
    assert.equal(await page.locator('aside select').inputValue(), 'takeaway');
    await tab('Pay card');
    await page.getByRole('heading', { name: `Receipt #${order.id}`, exact: true }).waitFor();
    await shot('04-paid-card-receipt.png');
    const paid = await read(`/orders/${order.id}`);
    assert.equal(paid.status, 'paid'); assert.equal(paid.payment_method, 'card');
    const after = await read('/inventory');
    const amounts = { 'Milk': 200, 'Coffee beans': 18, 'Tea leaves': 8, 'Sugar': 20 };
    const stockChecks = before.map(item => {
      const ending = after.find(i => i.id === item.id);
      const actual = item.stock_quantity - ending.stock_quantity;
      assert.equal(actual, amounts[item.name] || 0);
      return { ingredient: item.name, unit: item.unit, before: item.stock_quantity, after: ending.stock_quantity, expectedDeduction: amounts[item.name] || 0, actualDeduction: actual };
    });
    await tab('inventory');
    await page.getByRole('cell', { name: 'Milk', exact: true }).waitFor();
    await shot('05-inventory-after.png');
    const duplicate = await fetch(`${api}/orders/${order.id}/pay`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ method: 'card' }) });
    const duplicateBody = await duplicate.json();
    assert.equal(duplicate.status, 409); assert.deepEqual(await read('/inventory'), after);
    const salesAfter = await read('/dashboard/sales');
    assert.equal(salesAfter.paid_orders - salesBefore.paid_orders, 1);
    assert.equal(salesAfter.sales_total - salesBefore.sales_total, 8500);
    await tab('Owner dashboard');
    await page.getByRole('cell', { name: `#${order.id}`, exact: true }).waitFor();
    await shot('06-sales-after-repeat.png');
    const result = { result: 'PASS', runAt: new Date().toISOString(), testedCommit: 'a36f83a', provenance: 'Codex automated check on existing developer PC; not a Shuzita-authored or independent-PC test', orderId: order.id, orderType: order.order_type, items: order.items, total: order.total, paymentMethod: paid.payment_method, refreshRecovered: true, unpaidInventoryUnchanged: true, stockChecks, duplicatePaymentStatus: duplicate.status, duplicatePaymentResponse: duplicateBody, duplicateInventoryUnchanged: true, salesBefore: { count: salesBefore.paid_orders, total: salesBefore.sales_total }, salesAfter: { count: salesAfter.paid_orders, total: salesAfter.sales_total } };
    fs.writeFileSync(path.join(__dirname, 'results.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify(result, null, 2));
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
