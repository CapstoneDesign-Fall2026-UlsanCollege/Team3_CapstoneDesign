$ErrorActionPreference = 'Stop'
$tunnelExe = Join-Path $PSScriptRoot 'cloudflared.exe'
if (-not (Test-Path -LiteralPath $tunnelExe)) {
    Write-Output 'Downloading the official Cloudflare tunnel client for Windows x64...'
    Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile $tunnelExe
}
$projectPath = (Resolve-Path (Join-Path $PSScriptRoot '../../smartserve-pos')).Path
Push-Location $projectPath
try {
    docker compose -p smartserve-week5-check up -d
    if ($LASTEXITCODE -ne 0) { throw 'Start Docker Desktop, then retry.' }
    if (-not (Test-Path -LiteralPath (Join-Path $projectPath 'frontend/node_modules'))) {
        npm --prefix frontend ci
        if ($LASTEXITCODE -ne 0) { throw 'Frontend dependency installation failed.' }
    }
    npm --prefix frontend run build
    if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
} finally { Pop-Location }
if (-not (Get-NetTCPConnection -LocalPort 8787 -State Listen -ErrorAction SilentlyContinue)) {
    $nodePath = (Get-Command node).Source
    Start-Process -FilePath $nodePath -ArgumentList (Join-Path $PSScriptRoot 'server.cjs') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $PSScriptRoot 'server.log') -RedirectStandardError (Join-Path $PSScriptRoot 'server-error.log')
}
$runningTunnel = Get-Process -Name cloudflared -ErrorAction SilentlyContinue
if (-not $runningTunnel) {
    Start-Process -FilePath (Join-Path $PSScriptRoot 'cloudflared.exe') -ArgumentList @('tunnel','--no-autoupdate','--protocol','http2','--url','http://localhost:8787') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $PSScriptRoot 'tunnel.log') -RedirectStandardError (Join-Path $PSScriptRoot 'tunnel-error.log')
}
Write-Output 'Look for the https://...trycloudflare.com URL in tunnel-error.log. A new tunnel has a new URL.'
