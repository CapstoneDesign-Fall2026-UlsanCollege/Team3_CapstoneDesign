import os,sys,json,time,tempfile,threading,subprocess,mimetypes,urllib.request,urllib.error,html,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone,timedelta
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from playwright.sync_api import sync_playwright,expect

REPO=Path('D:/Capstone_Design'); DIST=REPO/'smartserve-pos/frontend/dist'
ORIGIN='http://127.0.0.1:18980'; API='http://127.0.0.1:18981'
class Proxy(BaseHTTPRequestHandler):
 def log_message(self,*a): pass
 def do_GET(self):
  if self.path.split('?')[0].startswith(('/menu','/orders','/inventory','/owner','/dashboard','/health','/docs','/openapi.json')): return self.proxy()
  f=DIST/self.path.split('?')[0].lstrip('/')
  if not f.is_file(): f=DIST/'index.html'
  body=f.read_bytes()
  if f.suffix=='.js': body=body.replace(b'http://localhost:8000',ORIGIN.encode())
  self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(str(f))[0] or 'application/octet-stream');self.end_headers();self.wfile.write(body)
 def do_POST(self): self.proxy()
 def do_PUT(self): self.proxy()
 def proxy(self):
  data=self.rfile.read(int(self.headers.get('Content-Length',0))) if self.command!='GET' else None
  req=urllib.request.Request(API+self.path,data=data,method=self.command,headers={'Content-Type':'application/json'})
  try: r=urllib.request.urlopen(req)
  except urllib.error.HTTPError as e: r=e
  self.send_response(r.status); self.send_header('Content-Type',r.headers.get('Content-Type','application/json'));self.end_headers();self.wfile.write(r.read())

def get(path):
 with urllib.request.urlopen(API+path) as r:return json.load(r)
def run(pack,failed):
 out=Path('D:/')/pack/'evidence/agent-run-2026-10-21';out.mkdir(parents=True,exist_ok=True)
 shots=[]; results=[]; errors=[]; start=time.perf_counter()
 def check(label,expected,actual):
  results.append({'check':label,'expected':expected,'actual':actual,'pass':expected==actual})
  assert expected==actual,(label,expected,actual)
 with tempfile.TemporaryDirectory(prefix='smartserve-week7-',ignore_cleanup_errors=True) as tmp:
  env=os.environ.copy();env['DATABASE_URL']='sqlite:///'+str(Path(tmp)/'sample.db').replace('\\','/');env['PYTHONDONTWRITEBYTECODE']='1'
  log=open(out/'api.log','w',encoding='utf-8')
  proc=subprocess.Popen([sys.executable,'-B','-m','uvicorn','app.main:app','--host','127.0.0.1','--port','18981'],cwd=REPO/'smartserve-pos/backend',env=env,stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
  proxy=None
  try:
   for _ in range(100):
    try:
     if get('/health')['status']=='ok':break
    except Exception:time.sleep(.1)
   else:raise RuntimeError('Isolated API did not start')
   proxy=ThreadingHTTPServer(('127.0.0.1',18980),Proxy);threading.Thread(target=proxy.serve_forever,daemon=True).start()
   with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='C:/Users/shera/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe')
    context=browser.new_context(viewport={'width':1440,'height':1080},record_video_dir=str(out/'video'),record_video_size={'width':1440,'height':1080})
    page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    def shot(name):
     page.screenshot(path=str(out/name),full_page=True);shots.append(name)
    def nav(name):
     page.get_by_role('button',name=name,exact=True).click()
    page.goto(ORIGIN);expect(page.get_by_role('button',name='Caffè Latte',exact=False)).to_be_enabled()
    before=get('/inventory');sales0=get('/dashboard/sales');check('fresh sales',0,sales0['sales_total'])
    nav('inventory');expect(page.get_by_role('cell',name='5,000',exact=False)).to_have_count(0) if False else None
    expect(page.get_by_role('cell',name='5000 ml',exact=True)).to_be_visible();shot('01-before-inventory.png')
    nav('Owner dashboard');expect(page.get_by_text('No paid sales on this date.',exact=True)).to_be_visible();shot('02-before-sales-empty-state.png')
    nav('cashier');page.get_by_role('button',name='Caffè Latte',exact=False).click();page.get_by_role('button',name='Add one Caffè Latte',exact=True).click()
    expect(page.locator('.total')).to_contain_text('9,000');shot('03-two-latte-cart.png')
    with page.expect_response(lambda r:r.url==ORIGIN+'/orders' and r.request.method=='POST') as saved:
     page.get_by_role('button',name='Create order',exact=True).click()
    order=saved.value.json();oid=order['id'];check('two-latte total',9000,order['total']);check('order starts open','open',order['status']);check('unpaid stock unchanged',before,get('/inventory'))
    expect(page.get_by_role('status')).to_contain_text('created');shot('04-unpaid-order.png')
    if failed:
     def inject(route):route.continue_(post_data=json.dumps({'method':'card','result':'failed'}))
     page.route('**/orders/*/pay',inject)
     with page.expect_response(lambda r:r.url.endswith('/pay')) as response:page.get_by_role('button',name='Pay card',exact=True).click()
     check('failed payment HTTP',402,response.value.status)
     expect(page.get_by_role('status')).to_contain_text('failed');shot('05-failed-payment-message.png');page.unroute('**/orders/*/pay',inject)
     check('failed order stays open','open',get('/orders/'+str(oid))['status']);check('failed stock unchanged',before,get('/inventory'));check('failed sales unchanged',sales0['sales_total'],get('/dashboard/sales')['sales_total'])
     nav('inventory');expect(page.get_by_role('cell',name='5000 ml',exact=True)).to_be_visible();shot('06-stock-after-failure.png')
     nav('Owner dashboard');expect(page.get_by_text('No paid sales on this date.',exact=True)).to_be_visible();shot('07-sales-after-failure.png');nav('cashier')
    with page.expect_response(lambda r:r.url.endswith('/pay')) as response:page.get_by_role('button',name='Pay cash',exact=True).click()
    check('successful payment HTTP',200,response.value.status);expect(page.locator('.receipt')).to_contain_text('9,000');shot('08-paid-receipt.png')
    after=get('/inventory');stock={i['name']:i['stock_quantity'] for i in after};check('milk ml',4500,stock['Milk']);check('beans g',1164,stock['Coffee beans'])
    nav('inventory');expect(page.get_by_role('cell',name='4500 ml',exact=True)).to_be_visible();shot('09-final-inventory.png')
    nav('Owner dashboard');expect(page.locator('.stats')).to_contain_text('9,000');shot('10-final-sales-dashboard.png')
    duplicate=context.request.post(ORIGIN+f'/orders/{oid}/pay',data={'method':'cash','result':'paid'})
    check('duplicate payment HTTP',409,duplicate.status);check('duplicate stock unchanged',after,get('/inventory'));check('sales after duplicate',9000,get('/dashboard/sales')['sales_total']);check('paid orders',1,get('/dashboard/sales')['paid_orders'])
    nav('Orders');expect(page.get_by_role('button',name='View receipt',exact=True)).to_be_visible();shot('11-paid-order-history.png')
    page.get_by_role('button',name='View receipt',exact=True).click();expect(page.locator('.receipt')).to_contain_text('Caffè Latte');shot('12-reopened-receipt.png')
    if not failed:
     page.set_viewport_size({'width':390,'height':844});shot('13-mobile-receipt.png');page.set_viewport_size({'width':1440,'height':1080})
    check('uncaught browser errors',[],errors)
    elapsed=round(time.perf_counter()-start,2)
    metadata={'operator':'Codex agent automation; not Shuzita or shrey776','date_kst':datetime.now(timezone(timedelta(hours=9))).isoformat(),'application_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'environment':'Fresh temporary SQLite file per pack; built frontend served through isolated loopback proxy at 18980; API at 18981. No shared database touched.','failure_injection':'Browser automation changed only the outgoing simulated payment body to method=card,result=failed; real backend returned 402.' if failed else 'No failure injection; happy-path browser walkthrough and duplicate-payment HTTP check.','automation_elapsed_seconds':elapsed,'human_rehearsal_duration':'Not performed','independent_member_test':'Not performed','checks':results,'duplicate_response':duplicate.json(),'screenshots':shots,'browser_errors':errors}
    (out/'results.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    report='<html><meta charset="utf-8"><style>body{font:18px Arial;margin:40px;color:#182434}pre{font:15px monospace;white-space:pre-wrap}h1{font-size:28px}</style><h1>Agent-run HTTP and browser verification</h1><p>Actual recorded results. Operator: Codex automation. This is a generated evidence report, not the app UI or a member test.</p><pre>'+html.escape(json.dumps(metadata,ensure_ascii=False,indent=2))+'</pre></html>'
    (out/'http-browser-report.html').write_text(report,encoding='utf-8');page.set_content(report);shot('14-http-browser-results-report.png')
    context.close();browser.close()
    video=next((out/'video').glob('*.webm'));shutil.move(str(video),out/'automated-browser-walkthrough.webm');(out/'video').rmdir()
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')};(out/'screenshot-sha256.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
    print(pack+': PASS '+str(len(results))+' checks; '+str(len(shots))+' screenshots',flush=True)
  finally:
   if proxy:proxy.shutdown();proxy.server_close()
   proc.terminate();proc.wait(timeout=15);log.close()

run('shuzita_ben',True)
run('shreya_ben',False)

