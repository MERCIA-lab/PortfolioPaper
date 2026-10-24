$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $root "backend\.venv\Scripts\python.exe"
$backendLog = Join-Path $env:TEMP "PortfolioPaper-backend.log"
$backendErrorLog = Join-Path $env:TEMP "PortfolioPaper-backend-error.log"
$frontendLog = Join-Path $env:TEMP "PortfolioPaper-frontend.log"
$frontendErrorLog = Join-Path $env:TEMP "PortfolioPaper-frontend-error.log"

$backend = Start-Process -FilePath $python `
    -ArgumentList @("backend\manage.py", "runserver", "127.0.0.1:8000", "--noreload") `
    -WorkingDirectory $root `
    -WindowStyle Hidden `
    -RedirectStandardOutput $backendLog `
    -RedirectStandardError $backendErrorLog `
    -PassThru
$frontend = Start-Process -FilePath $python `
    -ArgumentList @("-m", "http.server", "5500", "--directory", "frontend") `
    -WorkingDirectory $root `
    -WindowStyle Hidden `
    -RedirectStandardOutput $frontendLog `
    -RedirectStandardError $frontendErrorLog `
    -PassThru

Start-Sleep -Seconds 2
Write-Output "Started backend PID $($backend.Id) and frontend PID $($frontend.Id)"
Write-Output "Logs: $backendLog, $backendErrorLog, $frontendLog, $frontendErrorLog"
