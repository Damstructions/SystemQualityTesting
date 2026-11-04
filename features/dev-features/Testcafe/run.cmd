@echo off
setlocal
cd /d "%~dp0..\..\.."
set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=python"
"%PY%" -c "import sys; sys.path.insert(0, 'features/dev-features'); import cert_date; args=cert_date.chrome_args_for_date_only('https://opencart.abstracta.us/'); print(args[0] if args else '')" > "%TEMP%\oc-cert-arg.txt"
set /p CERTARG=<"%TEMP%\oc-cert-arg.txt"
set "BROWSER=chrome:headless"
if not "%CERTARG%"=="" set "BROWSER=chrome:headless %CERTARG%"
testcafe "%BROWSER%" features/dev-features/Testcafe/contact-after-logon.js --disable-native-automation --selector-timeout 20000 --assertion-timeout 20000 --page-load-timeout 30000 --screenshots path=Screenshots,takeOnFails=false,thumbnails=false --screenshots-full-page
exit /b %ERRORLEVEL%
