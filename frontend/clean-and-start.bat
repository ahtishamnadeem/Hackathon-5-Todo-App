@echo off
echo Comprehensive Next.js lock cleanup and startup...

REM Kill all node processes
echo Terminating all Node.js processes...
taskkill /f /im node.exe 2>nul

REM Wait for processes to fully terminate
echo Waiting for processes to terminate...
timeout /t 3 /nobreak >nul

REM Force delete .next directory
echo Force deleting .next directory...
if exist .next (
    attrib -R .next /S /D 2>nul
    rmdir /s /q .next 2>nul
    echo Previous .next directory removed.
) else (
    echo No .next directory found, continuing...
)

REM Also check for any files in temp that might be holding locks
echo Checking for any remaining lock files...
dir /s /b .next 2>nul
if exist .next (
    echo ERROR: .next directory still exists after removal attempt!
    pause
    exit /b 1
)

echo Starting Next.js development server...
npx next dev

pause