// Run against the isolated smartserve-payment-check Docker Compose project.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const api = 'http://localhost:8000';
const folder = path.join(__dirname, 'screenshots');
async function request(endpoint, body) {
  const response = await fetch(api + endpoint, body ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) } : {});
  return { status: response.status, body: await response.json() };
}
const stock = (items, name) => items.find(item => item.name === name).stock_quantity;

async function main() {
  fs.mkdirSync(folder, { recursive: true });
  const latte = (await request('/menu')).body.find(item => item.name === 'Caffè Latte');
  const startingInventory = (await request('/inventory')).body;
  const startingSales = (await request('/dashboard/sales')).body;
  const create = async () => {
    const result = await request('/orders', { order_type: 'dine_in', items: [{ menu_item_id: latte.id, quantity: 1 }] });
    assert.equal(result.status, 201);
    return result.body;
  };
  const toPay = await create();
  const toCancel = await create();
  const browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    await page.goto('http://localhost:5173');
    await page.getByRole('button', { name: 'Orders', exact: true }).click();
    await page.getByRole('row').filter({ hasText: `#${toPay.id}` }).getByText('Open', { exact: true }).waitFor();
    await page.screenshot({ path: path.join(folder, '01-open-orders.png'), fullPage: true });

    await page.getByRole('row').filter({ hasText: `#${toPay.id}` }).getByRole('button', { name: 'Resume' }).click();
    await page.getByRole('heading', { name: `Order #${toPay.id}` }).waitFor();
    await page.getByText('Caffè Latte', { exact: true }).last().waitFor();
    await page.getByRole('button', { name: 'Pay cash' }).click();
    await page.getByRole('heading', { name: `Receipt #${toPay.id}` }).waitFor();
    await page.getByRole('button', { name: 'Orders', exact: true }).click();
    await page.getByRole('row').filter({ hasText: `#${toPay.id}` }).getByText('Paid', { exact: true }).waitFor();
    await page.screenshot({ path: path.join(folder, '02-paid-order.png'), fullPage: true });
    await page.getByRole('row').filter({ hasText: `#${toPay.id}` }).getByRole('button', { name: 'View receipt' }).click();
    await page.getByRole('heading', { name: `Receipt #${toPay.id}` }).waitFor();
    await page.getByRole('button', { name: 'Orders', exact: true }).click();

    await page.getByRole('row').filter({ hasText: `#${toCancel.id}` }).getByRole('button', { name: 'Cancel' }).click();
    await page.getByRole('row').filter({ hasText: `#${toCancel.id}` }).getByText('Cancelled', { exact: true }).waitFor();
    await page.screenshot({ path: path.join(folder, '03-cancelled-order.png'), fullPage: true });
  } finally { await browser.close(); }

  const paid = (await request(`/orders/${toPay.id}`)).body;
  const cancelled = (await request(`/orders/${toCancel.id}`)).body;
  const payCancelled = await request(`/orders/${toCancel.id}/pay`, { method: 'cash' });
  const endingInventory = (await request('/inventory')).body;
  const endingSales = (await request('/dashboard/sales')).body;
  assert.equal(paid.status, 'paid');
  assert.equal(cancelled.status, 'cancelled');
  assert.equal(payCancelled.status, 409);
  assert.equal(stock(startingInventory, 'Milk') - stock(endingInventory, 'Milk'), 250);
  assert.equal(stock(startingInventory, 'Coffee beans') - stock(endingInventory, 'Coffee beans'), 18);
  assert.equal(endingSales.paid_orders - startingSales.paid_orders, 1);
  assert.equal(endingSales.sales_total - startingSales.sales_total, 4500);
  const result = { runAt: new Date().toISOString(), environment: 'isolated Docker frontend/API/PostgreSQL', paidOrderId: toPay.id, cancelledOrderId: toCancel.id, cancelledPaymentStatus: payCancelled.status, milkDeducted: 250, beansDeducted: 18, paidOrdersAdded: 1, salesAdded: 4500, result: 'PASS' };
  fs.writeFileSync(path.join(__dirname, 'results.json'), JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify(result, null, 2));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
