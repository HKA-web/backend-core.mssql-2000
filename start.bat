@echo off
REM ================================================
REM  Script untuk start FastAPI app dengan uvicorn
REM  Menggunakan Python dari bin/python/
REM  Mode dev/prod dihilangkan
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

REM Upgrade pip & install uvicorn kalau belum ada
python -m pip install --upgrade pip
pip install uvicorn --quiet

REM Minta input port dari user
set /p PORT=Masukkan port untuk FastAPI (default 8001): 
if "%PORT%"=="" set PORT=8001

echo [INFO] Menjalankan FastAPI di port %PORT%...

REM Jalankan uvicorn production-style
uvicorn src.main:app --host 0.0.0.0 --port %PORT% --workers 5
