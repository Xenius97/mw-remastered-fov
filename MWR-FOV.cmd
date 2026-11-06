@echo off
setlocal
rem Change this number to your preferred FOV (65-110).
set "FOV=90"
set "SCRIPT=%~dp0MWR-FOV.py"
if not exist "%SCRIPT%" (
    echo MWR-FOV.py is missing. Keep the CMD and Python file in the same folder.
    pause
    exit /b 1
)
py -3 -c "import sys,struct; sys.exit(0 if sys.version_info >= (3,9) and struct.calcsize('P') == 8 else 1)" >nul 2>&1
if not errorlevel 1 (
    py -3 "%SCRIPT%" --fov %FOV% %*
    exit /b
)
python -c "import sys,struct; sys.exit(0 if sys.version_info >= (3,9) and struct.calcsize('P') == 8 else 1)" >nul 2>&1
if not errorlevel 1 (
    python "%SCRIPT%" --fov %FOV% %*
    exit /b
)
echo 64-bit Python 3.9 or newer is required.
echo Install Python from https://www.python.org/downloads/windows/
echo Enable the Python launcher or add Python to PATH during setup.
echo Close this window after installing, then run this launcher again.
pause
exit /b 1
