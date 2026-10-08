// Serve the existing production frontend and proxy its API on one origin.
// Only generated JS responses are adapted; application source stays unchanged.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../../smartserve-pos/frontend/dist');
const apiPrefixes = ['/menu', '/orders', '/inventory', '/owner', '/dashboard', '/health', '/docs', '/openapi.json', '/redoc'];
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon' };
http.createServer((req, res) => {
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); }
  catch { res.writeHead(400); return res.end('Invalid URL'); }
  if (apiPrefixes.some(prefix => pathname === prefix || pathname.startsWith(prefix + '/'))) {
    const upstream = http.request({ hostname: '127.0.0.1', port: 8000, path: req.url, method: req.method, headers: { ...req.headers, host: 'localhost:8000' } }, response => {
      res.writeHead(response.statusCode, response.headers); response.pipe(res);
    });
    upstream.on('error', () => { if (!res.headersSent) res.writeHead(503, { 'Content-Type': 'application/json' }); res.end('{"detail":"SmartServe API is starting. Please retry shortly."}'); });
    req.pipe(upstream); return;
  }
  if (req.method !== 'GET' && req.method !== 'HEAD') { res.writeHead(405); return res.end(); }
  let filename = path.resolve(root, '.' + pathname);
  if (filename !== root && !filename.startsWith(root + path.sep)) { res.writeHead(403); return res.end(); }
  if (!fs.existsSync(filename) || fs.statSync(filename).isDirectory()) filename = path.join(root, 'index.html');
  try {
    const extension = path.extname(filename);
    let content = fs.readFileSync(filename);
    if (extension === '.js') content = Buffer.from(content.toString('utf8').replaceAll('http://localhost:8000', ''));
    res.writeHead(200, { 'Content-Type': mime[extension] || 'application/octet-stream', 'Cache-Control': 'no-cache', 'Content-Length': content.length });
    res.end(req.method === 'HEAD' ? undefined : content);
  } catch { res.writeHead(503); res.end('Frontend build is not available yet.'); }
}).listen(8787, '0.0.0.0', () => console.log('SmartServe single-origin server listening on port 8787'));
