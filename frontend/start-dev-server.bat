@echo off
echo Ensuring clean state...
echo Killing any existing Node.js processes...
taskkill /f /im node.exe 2>nul

echo Waiting for processes to terminate...
timeout /t 2 /nobreak >nul

echo Removing .next directory...
if exist .next (
    rmdir /s /q .next
    echo .next directory removed.
) else (
    echo .next directory not found, continuing...
)

echo Starting Next.js development server...
npx next dev

pause