# Stop any existing Node.js processes that might be holding locks
Get-Process node -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*Hackathon*"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Clean the .next directory to ensure fresh start
if (Test-Path ".next") {
    Remove-Item ".next" -Recurse -Force
}

# Start the Next.js development server
Write-Host "Starting Next.js development server..." -ForegroundColor Green
npx next dev