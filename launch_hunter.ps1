# HunterOS Launch Script
$ProjectRoot = "C:\Users\User\Documents\Job-Hunter"

Write-Host "--- Starting HunterOS Backend ---" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $ProjectRoot\backend; `$env:PYTHONPATH = '.'; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

Write-Host "--- Starting HunterOS Frontend ---" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $ProjectRoot\frontend; npm run dev"

Write-Host "--- HunterOS is launching... ---" -ForegroundColor Green
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"
