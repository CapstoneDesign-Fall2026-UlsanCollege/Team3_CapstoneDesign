// Run against the isolated smartserve-payment-check Docker Compose project only.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const api = 'http://localhost:8000';
const web = 'http://localhost:5173';
const folder = path.join(__dirname, 'screenshots');

async function get(endpoint) {
  const response = await fetch(api + endpoint);
  assert.equal(response.status, 200, `${endpoint}: ${response.status}`);
  return response.json();
}

function stock(state, name) {
  return state.inventory.find(item => item.name === name).stock_quantity;
}

async function main() {
  fs.mkdirSync(folder, { recursive: true });
  assert.equal((await get('/health')).status, 'ok');
  const before = {
    inventory: await get('/inventory'),
    sales: await get('/dashboard/sales'),
  };
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}),
  });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    const shot = name => page.screenshot({ path: path.join(folder, name + '.png'), fullPage: true });
    await page.goto(web);
    await page.getByRole('button', { name: 'inventory', exact: true }).click();
    await page.getByRole('cell', { name: 'Milk', exact: true }).waitFor();
    await shot('01-inventory-before');

    await page.getByRole('button', { name: 'cashier', exact: true }).click();
    await page.getByRole('button', { name: /Caffè Latte/ }).click();
    await page.getByRole('button', { name: /Caffè Latte/ }).click();
    const paymentResponse = page.waitForResponse(response => response.url().endsWith('/pay') && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Pay cash', exact: true }).click();
    const firstResponse = await paymentResponse;
    assert.equal(firstResponse.status(), 200);
    const first = await firstResponse.json();
    const orderId = first.order.id;
    await page.getByRole('heading', { name: `Receipt #${orderId}`, exact: true }).waitFor();
    await shot('02-first-payment-receipt');

    const afterFirst = {
      order: await get(`/orders/${orderId}`),
      inventory: await get('/inventory'),
      sales: await get('/dashboard/sales'),
    };
    assert.equal(afterFirst.order.status, 'paid');
    assert.equal(afterFirst.order.inventory_deducted, true);
    assert.equal(afterFirst.order.total, 9000);
    assert.equal(stock(before, 'Milk') - stock(afterFirst, 'Milk'), 500);
    assert.equal(stock(before, 'Coffee beans') - stock(afterFirst, 'Coffee beans'), 36);
    assert.equal(afterFirst.sales.paid_orders - before.sales.paid_orders, 1);
    assert.equal(afterFirst.sales.sales_total - before.sales.sales_total, 9000);
    await page.getByRole('button', { name: 'inventory', exact: true }).click();
    await page.getByRole('cell', { name: 'Milk', exact: true }).waitFor();
    await shot('03-inventory-after-first-payment');
    await page.getByRole('button', { name: 'Owner dashboard', exact: true }).click();
    await page.getByRole('cell', { name: `#${orderId}`, exact: true }).waitFor();
    await shot('04-sales-after-first-payment');

    // Reuse the paid order ID as the cashier's pending order, then retry in the real UI.
    await page.evaluate(id => sessionStorage.setItem('smartserve.pendingOrder', String(id)), orderId);
    await page.reload();
    const duplicateResponse = page.waitForResponse(response => response.url().endsWith(`/orders/${orderId}/pay`) && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Pay cash', exact: true }).click();
    const duplicate = await duplicateResponse;
    assert.equal(duplicate.status(), 409);
    const duplicateBody = await duplicate.json();
    assert.match(duplicateBody.detail, /Inventory was not deducted again/);
    await page.getByRole('heading', { name: `Receipt #${orderId}`, exact: true }).waitFor();
    await page.getByText(duplicateBody.detail, { exact: true }).waitFor();
    await shot('05-repeat-payment-receipt-and-message');

    const afterRepeat = {
      order: await get(`/orders/${orderId}`),
      inventory: await get('/inventory'),
      sales: await get('/dashboard/sales'),
    };
    assert.deepEqual(afterRepeat, afterFirst);
    await page.getByRole('button', { name: 'inventory', exact: true }).click();
    await page.getByRole('cell', { name: 'Milk', exact: true }).waitFor();
    await shot('06-inventory-after-repeat');
    await page.getByRole('button', { name: 'Owner dashboard', exact: true }).click();
    await page.getByRole('cell', { name: `#${orderId}`, exact: true }).waitFor();
    await shot('07-sales-after-repeat');

    const result = {
      runAt: new Date().toISOString(),
      environment: 'isolated smartserve-payment-check Docker Compose project',
      orderId,
      firstPaymentStatus: firstResponse.status(),
      repeatPaymentStatus: duplicate.status(),
      repeatMessage: duplicateBody.detail,
      before,
      afterFirst,
      afterRepeat,
      result: 'PASS',
    };
    fs.writeFileSync(path.join(__dirname, 'results.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify({ orderId, firstPaymentStatus: result.firstPaymentStatus, repeatPaymentStatus: result.repeatPaymentStatus, milkBefore: stock(before, 'Milk'), milkAfter: stock(afterFirst, 'Milk'), beansBefore: stock(before, 'Coffee beans'), beansAfter: stock(afterFirst, 'Coffee beans'), salesBefore: before.sales.sales_total, salesAfter: afterFirst.sales.sales_total, result: 'PASS' }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
