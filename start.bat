@echo off
REM ================================================
REM  Script untuk start FastAPI app dengan uvicorn
REM  Menggunakan Python dari bin/python/
REM  Port dan worker otomatis baca dari env.yaml
REM ================================================

REM Set path Python dari folder bin/python
set PYTHON_BIN=%~dp0bin\python\python.exe

if not exist "%PYTHON_BIN%" (
    echo [ERROR] Python tidak ditemukan di %PYTHON_BIN%
    exit /b 1
)

REM Cek venv, buat jika belum ada
if not exist venv (
    echo [INFO] Virtual environment belum ada. Membuat venv...
    "%PYTHON_BIN%" -m venv venv
    echo [INFO] venv dibuat.
)

REM Aktifkan virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip & install uvicorn + pyyaml kalau belum ada
python -m pip install --upgrade pip >nul
pip install uvicorn pyyaml --quiet

REM Baca port dan worker dari env.yaml pakai Python
for /f "usebackq delims=" %%A in (`python -c "import yaml; c=yaml.safe_load(open('env.yaml'))['sqlserver']; print(c.get('port','8001'))"`) do set PORT=%%A
for /f "usebackq delims=" %%B in (`python -c "import yaml; c=yaml.safe_load(open('env.yaml'))['sqlserver']; print(c.get('worker','1'))"`) do set WORKER=%%B

if "%PORT%"=="" set PORT=8001
if "%WORKER%"=="" set WORKER=1

echo [INFO] Menjalankan Microservice MsSQL 2000 di port %PORT% dengan %WORKER% worker...

REM Jalankan uvicorn production-style
uvicorn src.main:app --host 0.0.0.0 --port %PORT% --workers %WORKER%
