# SmartServe public link

This helper gives the existing SmartServe app one public HTTPS URL. The frontend, API, orders, inventory, and sales use the same local PostgreSQL Docker database.

## Requirements

- Windows x64, PowerShell, Node.js 22+, Git, and Docker Desktop with Linux containers.
- Internet access and host ports 8787, 5173, 8000, and 5432 available.
- Clone this repository; do not run it alongside another Compose project using those ports.

## Start

Start Docker Desktop. From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\docs\online\start.ps1
```

The script downloads the official Cloudflare tunnel executable if missing, starts the SmartServe services, installs frontend dependencies if needed, builds the frontend, and starts background web/tunnel processes.

Find the public URL:

```powershell
Get-Content .\docs\online\tunnel-error.log | Select-String 'https://.*trycloudflare.com'
```

Share that URL with the professor. Current-session URL (verified October 8, 2026):

https://creating-bridges-relief-speaker.trycloudflare.com

This is a temporary link, not a permanent deployment. A new tunnel gets a new URL. The current URL may expire after this session.

## Keep it available

Keep this PC awake, connected, and Docker running. The background Node server and Cloudflare tunnel must remain running. All visitors share the same database; their actions change orders, stock, and sales. Owner-only permissions are not enforced. Payments remain simulated.

The server listens on port 8787 and proxies API calls to port 8000. It serves the production frontend and adapts its API URL to the public origin without changing stored business data.

## Stop public access

Find the process belonging to this folder, then stop that specific process:

```powershell
Get-CimInstance Win32_Process -Filter "name = 'cloudflared.exe'" | Select-Object ProcessId, ExecutablePath, CommandLine
# Replace PROCESS_ID with this folder's tunnel process ID.
Stop-Process -Id PROCESS_ID
```

This closes public access without deleting PostgreSQL data. Use the application README's Compose stop command to stop the app itself. Never remove database volumes just to stop sharing.

## Verify

The public check creates and pays a sample order, so it changes stock and sales. Run only against dedicated sample data with an active menu item and enough stock.

Install Playwright locally in this helper folder:

```powershell
npm install --prefix .\docs\online --no-save --package-lock=false playwright
.\docs\online\node_modules\.bin\playwright.cmd install chromium
$env:SMARTSERVE_URL='YOUR_PUBLIC_URL'
node .\docs\online\verify.cjs
```

Alternatively set PLAYWRIGHT_MODULE to an existing Playwright module and CHROMIUM_PATH to a compatible installed browser. Results are saved in verification.json and public-check.png. [Current checks](latest-checks.md).

## Troubleshooting

- **Tunnel unavailable:** check tunnel-error.log and confirm the background process is running.
- **API starting:** wait for http://localhost:8000/health to respond, then refresh.
- **New changes missing:** rerun the start script to rebuild the production frontend, then refresh.
- **Local port 8787 in use:** identify its process before starting another server.
- **Docker failure:** resolve Docker Desktop startup first; do not reset database volumes as a shortcut.

Runtime logs and the downloaded executable are excluded from Git.
