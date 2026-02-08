# Repair Frontend Script for Phase III
# This script addresses OOM errors and resolution issues.

Write-Host "--- Stopping Node processes ---"
Stop-Process -Name node -ErrorAction SilentlyContinue

Write-Host "--- Cleaning Frontend Cache ---"
Set-Location frontend
if (Test-Path .next) { Remove-Item -Recurse -Force .next }
if (Test-Path node_modules) { Remove-Item -Recurse -Force node_modules }

Write-Host "--- Reinstalling Dependencies ---"
npm install

Write-Host "--- Setting Memory Limits ---"
$env:NODE_OPTIONS="--max-old-space-size=4096"

Write-Host "--- Starting Development Server ---"
npm run dev
