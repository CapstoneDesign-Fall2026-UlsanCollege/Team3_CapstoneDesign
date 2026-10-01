// Run only against the isolated smartserve-payment-check Docker Compose project.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const api = 'http://localhost:8000';
const folder = path.join(__dirname, 'screenshots');
async function get(endpoint) {
  const response = await fetch(api + endpoint);
  assert.equal(response.status, 200);
  return response.json();
}

async function main() {
  fs.mkdirSync(folder, { recursive: true });
  const suffix = Date.now().toString().slice(-6);
  const ingredientName = `Demo Matcha ${suffix}`;
  const menuName = `Demo Matcha Latte ${suffix}`;
  const browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) });
  let orderId;
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1050 } });
    await page.goto('http://localhost:5173');
    await page.getByRole('button', { name: 'Owner dashboard' }).click();
    await page.getByRole('heading', { name: 'Manage menu and inventory' }).waitFor();
    await page.getByLabel('Ingredient name').fill(ingredientName);
    await page.getByLabel('Unit', { exact: true }).fill('g');
    await page.getByLabel('Starting stock').fill('100');
    await page.getByLabel('Low-stock threshold').fill('10');
    await page.getByRole('button', { name: 'Add ingredient', exact: true }).click();
    await page.getByText(`${ingredientName} was added to inventory.`).waitFor();

    await page.getByLabel('Item name').fill(menuName);
    await page.getByLabel('Price (KRW)').fill('6000');
    await page.locator('.recipe-row select').selectOption({ label: `${ingredientName} (g)` });
    await page.locator('.recipe-row input').fill('5');
    await page.getByRole('button', { name: 'Add menu item' }).click();
    await page.getByText(`${menuName} is now available on the cashier menu.`).waitFor();
    await page.screenshot({ path: path.join(folder, '01-owner-added-menu-and-ingredient.png'), fullPage: true });

    const ingredient = (await get('/owner/inventory')).find(item => item.name === ingredientName);
    const menuItem = (await get('/owner/menu')).find(item => item.name === menuName);
    assert.equal(menuItem.recipe[0].ingredient_id, ingredient.id);
    await page.getByRole('button', { name: 'cashier', exact: true }).click();
    await page.getByRole('button', { name: new RegExp(menuName) }).click();
    const payment = page.waitForResponse(response => response.url().endsWith('/pay') && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Pay cash' }).click();
    const paidResponse = await payment;
    assert.equal(paidResponse.status(), 200);
    orderId = (await paidResponse.json()).order.id;
    await page.getByRole('heading', { name: `Receipt #${orderId}` }).waitFor();
    await page.screenshot({ path: path.join(folder, '02-new-menu-item-receipt.png'), fullPage: true });
    assert.equal((await get('/owner/inventory')).find(item => item.id === ingredient.id).stock_quantity, 95);

    await page.getByRole('button', { name: 'Owner dashboard' }).click();
    page.once('dialog', dialog => dialog.accept());
    await page.locator('.management-card').first().locator('.management-row').filter({ hasText: menuName }).getByRole('button', { name: 'Remove' }).click();
    await page.getByText(`${menuName} was removed from the cashier menu.`).waitFor();
    page.once('dialog', dialog => dialog.accept());
    await page.locator('.management-card').last().locator('.management-row').filter({ hasText: ingredientName }).getByRole('button', { name: 'Remove' }).click();
    await page.getByText(`${ingredientName} was removed from active inventory.`).waitFor();
    await page.screenshot({ path: path.join(folder, '03-owner-removed-items.png'), fullPage: true });

    assert.equal((await get('/menu')).some(item => item.id === menuItem.id), false);
    assert.equal((await get('/inventory')).some(item => item.id === ingredient.id), false);
    assert.equal((await get(`/orders/${orderId}`)).items[0].name, menuName);
    const result = { runAt: new Date().toISOString(), environment: 'isolated Docker frontend/API/PostgreSQL', ingredientId: ingredient.id, menuItemId: menuItem.id, orderId, stockBefore: 100, stockAfterPayment: 95, menuHiddenAfterRemoval: true, ingredientHiddenAfterRemoval: true, receiptPreserved: true, result: 'PASS' };
    fs.writeFileSync(path.join(__dirname, 'results.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify(result, null, 2));
  } finally { await browser.close(); }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
