@echo off
setlocal
rem OpenCart dev-features launcher for Command Prompt and PowerShell.
rem `behave` is not on PATH. This uses the Python 3.13 virtualenv at the repo root.
cd /d "%~dp0..\.."
if not defined HEADLESS set HEADLESS=1
if not exist ".venv\Scripts\python.exe" (
  echo Missing .venv in the repository root.
  echo Create it with: py -3.13 -m venv .venv
  echo Then install: .venv\Scripts\python.exe -m pip install -r requirements.txt
  exit /b 1
)
".venv\Scripts\python.exe" -m behave features/dev-features %*
exit /b %ERRORLEVEL%
