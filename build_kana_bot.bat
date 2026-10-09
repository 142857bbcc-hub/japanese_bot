@echo off
setlocal

set "APP_NAME=kana_bot"
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "SOURCE_FILE=%~1"
if "%SOURCE_FILE%"=="" set "SOURCE_FILE=%SCRIPT_DIR%\main.py"
set "OUTPUT_DIR=%SCRIPT_DIR%\dist"
set "OUTPUT_FILE=%OUTPUT_DIR%\%APP_NAME%.exe"
set "BUILD_DIR="

if not exist "%SOURCE_FILE%" (
    echo Error: source file not found: %SOURCE_FILE%
    echo Pass the path to your Python file as the first argument.
    goto :fail
)

set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY (
    python --version >nul 2>&1 && set "PY=python"
)
if not defined PY (
    echo Error: Python is not installed or not on your PATH.
    goto :fail
)

set "BUILD_DIR=%TEMP%\%APP_NAME%_build_%RANDOM%%RANDOM%"
mkdir "%BUILD_DIR%" || goto :fail

set "PLAYWRIGHT_BROWSERS_PATH="

echo ==^> Creating temporary virtual environment...
%PY% -m venv "%BUILD_DIR%\venv" || goto :fail
set "VPY=%BUILD_DIR%\venv\Scripts\python.exe"

echo ==^> Installing dependencies (playwright, pyinstaller)...
"%VPY%" -m pip install --quiet --upgrade pip || goto :fail
"%VPY%" -m pip install --quiet -r "%SCRIPT_DIR%\requirements.txt" pyinstaller || goto :fail

echo ==^> Installing the Playwright Chromium browser...
"%VPY%" -m playwright install chromium || goto :fail

set "HOOK=%BUILD_DIR%\rthook_playwright.py"
> "%HOOK%" echo(import os
>>"%HOOK%" echo(from pathlib import Path
>>"%HOOK%" echo(
>>"%HOOK%" echo(if "PLAYWRIGHT_BROWSERS_PATH" not in os.environ:
>>"%HOOK%" echo(    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
>>"%HOOK%" echo(    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(Path(base) / "ms-playwright")

echo ==^> Building executable with PyInstaller...
"%VPY%" -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --name "%APP_NAME%" ^
    --collect-all playwright ^
    --paths "%SCRIPT_DIR%" ^
    --runtime-hook "%HOOK%" ^
    --distpath "%BUILD_DIR%\dist" ^
    --workpath "%BUILD_DIR%\build" ^
    --specpath "%BUILD_DIR%" ^
    "%SOURCE_FILE%" || goto :fail

if not exist "%BUILD_DIR%\dist\%APP_NAME%.exe" (
    echo Error: build finished but the executable was not found.
    goto :fail
)

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
echo ==^> Placing executable in %OUTPUT_DIR% ...
if exist "%OUTPUT_FILE%" (
    echo     Existing %APP_NAME%.exe found - replacing it.
    del /f /q "%OUTPUT_FILE%" || goto :fail
)

copy /y "%BUILD_DIR%\dist\%APP_NAME%.exe" "%OUTPUT_FILE%" >nul || goto :fail

rmdir /s /q "%BUILD_DIR%" 2>nul

echo.
echo Done! Executable created at:
echo     %OUTPUT_FILE%
echo Run it with:  "%OUTPUT_FILE%"
pause
endlocal
exit /b 0

:fail
if defined BUILD_DIR if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%" 2>nul
echo.
echo Build failed.
pause
endlocal
exit /b 1
