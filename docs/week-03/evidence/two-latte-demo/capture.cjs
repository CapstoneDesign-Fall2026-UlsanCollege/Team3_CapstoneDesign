// Run against the isolated smartserve-issue3 instance only.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const api = 'http://localhost:8000';
async function get(endpoint) { const r = await fetch(api + endpoint); assert.equal(r.status,200); return r.json(); }
async function main() {
  const folder = path.join(__dirname,'screenshots'); fs.mkdirSync(folder,{recursive:true});
  const browser = await chromium.launch({headless:true, executablePath:process.env.CHROMIUM_PATH});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:900}});
    const before = {inventory:await get('/inventory'),sales:await get('/dashboard/sales')};
    const shot = name => page.screenshot({path:path.join(folder,name+'.png'),fullPage:true});
    await page.goto('http://localhost:5173');
    await page.getByRole('button',{name:'inventory',exact:true}).click();
    await page.getByRole('cell',{name:'Milk',exact:true}).waitFor(); await shot('01-inventory-before');
    await page.getByRole('button',{name:'Owner dashboard',exact:true}).click();
    await page.getByText('Sales today',{exact:true}).waitFor(); await shot('02-sales-before');
    await page.getByRole('button',{name:'cashier',exact:true}).click();
    await page.getByRole('button',{name:/Caffè Latte/}).click();
    await page.getByRole('button',{name:/Caffè Latte/}).click();
    await shot('03-two-latte-order');
    const responsePromise = page.waitForResponse(r=>r.url().endsWith('/pay') && r.request().method()==='POST');
    await page.getByRole('button',{name:'Pay cash',exact:true}).click();
    const response = await responsePromise; assert.equal(response.status(),200);
    const {order} = await response.json();
    assert.equal(order.total,9000); assert.equal(order.items.length,1); assert.equal(order.items[0].quantity,2);
    await page.getByRole('heading',{name:`Receipt #${order.id}`,exact:true}).waitFor(); await shot('04-receipt');
    await page.getByRole('button',{name:'inventory',exact:true}).click();
    const after = {inventory:await get('/inventory'),sales:await get('/dashboard/sales')};
    const stock = (state,name)=>state.inventory.find(i=>i.name===name).stock_quantity;
    await page.waitForFunction(value=>document.querySelector('table')?.textContent.includes(value), `${stock(after,'Milk')} ml`);
    await shot('05-inventory-after');
    await page.getByRole('button',{name:'Owner dashboard',exact:true}).click();
    await page.getByRole('cell',{name:`#${order.id}`,exact:true}).waitFor(); await shot('06-sales-after');
    assert.equal(stock(before,'Milk')-stock(after,'Milk'),500);
    assert.equal(stock(before,'Coffee beans')-stock(after,'Coffee beans'),36);
    assert.equal(after.sales.paid_orders-before.sales.paid_orders,1);
    assert.equal(after.sales.sales_total-before.sales.sales_total,9000);
    const result = {runAt:new Date().toISOString(),performedBy:'Codex automated browser run; not a personal verification by Shuzita',order,before,after,status:'PASS'};
    fs.writeFileSync(path.join(__dirname,'results.json'),JSON.stringify(result,null,2)+'\n');
    const rows = [['Milk (ml)',stock(before,'Milk'),stock(before,'Milk')-500,stock(after,'Milk')],['Coffee beans (g)',stock(before,'Coffee beans'),stock(before,'Coffee beans')-36,stock(after,'Coffee beans')],['Paid orders',before.sales.paid_orders,before.sales.paid_orders+1,after.sales.paid_orders],['Sales (KRW)',before.sales.sales_total,before.sales.sales_total+9000,after.sales.sales_total]];
    const shots = ['01-inventory-before','02-sales-before','03-two-latte-order','04-receipt','05-inventory-after','06-sales-after'];
    fs.writeFileSync(path.join(__dirname,'README.md'),`# Two-Latte demo evidence\n\nRun: ${result.runAt}\n\nPerformed by Codex using browser automation against the isolated SmartServe test instance. Shuzita has not yet personally reviewed or reproduced this run.\n\nOrder **#${order.id}**: two Lattes, **KRW 9,000**, paid by simulated cash.\n\n| Check | Before | Expected after | Actual after | Result |\n|---|---:|---:|---:|---|\n${rows.map(r=>'| '+r.join(' | ')+' | PASS |').join('\n')}\n\n## Evidence files\n\n[Raw results](results.json) · [Capture script](capture.cjs)\n\n${shots.map(s=>'### '+s+'\n\n!['+s+'](screenshots/'+s+'.png)').join('\n\n')}\n\n## Personal review pending\n\nShuzita should compare these screenshots and recorded values, note any findings, and personally add her actual review or reproduction contribution to the shared report. This evidence does not claim that she performed the automated run.\n`);
    console.log(JSON.stringify({orderId:order.id,status:'PASS',checks:rows},null,2));
  } finally { await browser.close(); }
}
main().catch(e=>{console.error(e);process.exitCode=1;});
