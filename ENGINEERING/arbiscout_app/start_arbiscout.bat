@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Creating local Python environment...
  python -m venv .venv
  if errorlevel 1 (
    py -3 -m venv .venv
  )
)
if not exist .venv\Scripts\python.exe (
  echo Could not create the Python environment.
  echo Install Python 3.10+ from python.org and try again.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo Could not install dependencies.
  pause
  exit /b 1
)
.venv\Scripts\python.exe control_room.py
if errorlevel 1 pause
