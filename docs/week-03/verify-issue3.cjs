// Run only against the isolated smartserve-issue3 Docker Compose project.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const api = 'http://localhost:8000';
const results = [];
async function request(url, body) {
  const response = await fetch(api + url, body ? {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)} : {});
  return {status:response.status, body:await response.json()};
}
async function stock() { return Object.fromEntries((await request('/inventory')).body.map(i => [i.name, i.stock_quantity])); }
function deduction(before, after, count = 1) {
  assert.equal(before.Milk - after.Milk, 250 * count);
  assert.equal(before['Coffee beans'] - after['Coffee beans'], 18 * count);
}
async function main() {
  assert.equal((await request('/health')).status, 200);
  const menu = (await request('/menu')).body;
  const latte = menu.find(i => i.name.includes('Latte'));
  const create = () => request('/orders', {order_type:'dine_in', items:[{menu_item_id:latte.id, quantity:1}]});
  let before = await stock();
  const order = (await create()).body;
  const payments = await Promise.all(Array.from({length:10}, () => request(`/orders/${order.id}/pay`, {method:'cash'})));
  assert.equal(payments.filter(p => p.status === 200).length, 1);
  assert.equal(payments.filter(p => p.status === 409).length, 9);
  deduction(before, await stock());
  results.push({test:'10 concurrent payments', order:order.id, success:1, duplicateRejected:9, result:'PASS'});
  before = await stock();
  const failedOrder = (await create()).body;
  assert.equal((await request(`/orders/${failedOrder.id}/pay`, {method:'card',result:'failed'})).status,402);
  assert.deepEqual(await stock(), before);
  assert.equal((await request(`/orders/${failedOrder.id}`)).body.inventory_deducted,false);
  assert.equal((await request(`/orders/${failedOrder.id}/pay`, {method:'card'})).status,200);
  deduction(before, await stock());
  results.push({test:'failed payment then successful retry',order:failedOrder.id,result:'PASS'});

  const browser = await chromium.launch({headless:true, ...(process.env.CHROMIUM_PATH ? {executablePath:process.env.CHROMIUM_PATH} : {})});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:900}});
    let created = 0;
    page.on('request', r => { if (r.method() === 'POST' && r.url() === api + '/orders') created++; });
    await page.goto('http://localhost:5173');
    await page.getByRole('button', {name:/Caffè Latte/}).click();
    before = await stock();
    await page.getByRole('button',{name:'Pay cash',exact:true}).evaluate(button => { button.click(); button.click(); button.click(); });
    await page.getByRole('heading',{name:/Receipt #/}).waitFor();
    assert.equal(created,1);
    deduction(before,await stock());
    await page.screenshot({path:path.join(__dirname,'issue-3-paid-once.png'), fullPage:true});
    results.push({test:'three rapid Pay clicks',ordersCreated:created,result:'PASS'});

    await page.getByRole('button',{name:/Caffè Latte/}).click();
    before = await stock();
    let markProcessed;
    const processed = new Promise(resolve => markProcessed = resolve);
    let releaseResponse;
    const hold = new Promise(resolve => releaseResponse = resolve);
    await page.route('**/orders/*/pay',async route => {
      const response = await route.fetch();
      markProcessed();
      await hold;
      try { await route.fulfill({response}); } catch { /* The page was intentionally refreshed. */ }
    });
    await page.getByRole('button',{name:'Pay card',exact:true}).click();
    await processed;
    const pending = await page.evaluate(() => sessionStorage.getItem('smartserve.pendingOrder'));
    assert.ok(pending);
    await page.reload();
    releaseResponse();
    await page.unroute('**/orders/*/pay');
    await page.getByRole('button',{name:'Pay card',exact:true}).click();
    await page.getByRole('heading',{name:`Receipt #${pending}`,exact:true}).waitFor();
    await page.getByText('This order has already been processed. Inventory was not deducted again.',{exact:true}).waitFor();
    assert.equal(created,2);
    deduction(before,await stock());
    assert.equal(await page.evaluate(() => sessionStorage.getItem('smartserve.pendingOrder')),null);
    await page.screenshot({path:path.join(__dirname,'issue-3-refresh-retry.png'),fullPage:true});
    results.push({test:'refresh after server payment, then retry same order',order:Number(pending),result:'PASS'});
  } finally { await browser.close(); }
  fs.writeFileSync(path.join(__dirname,'issue-3-live-results.json'),JSON.stringify({runAt:new Date().toISOString(),database:'isolated PostgreSQL 16',results},null,2)+'\n');
  console.log(JSON.stringify(results,null,2));
}
main().catch(error => { console.error(error); process.exitCode=1; });
