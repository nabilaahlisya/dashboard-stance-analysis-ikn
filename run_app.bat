@echo off
echo ========================================
echo   Menjalankan Aplikasi Web
echo ========================================
echo.

REM Cek apakah venv ada
if not exist "venv" (
    echo [ERROR] Virtual environment tidak ditemukan!
    echo [INFO] Silakan jalankan install_venv.bat terlebih dahulu.
    pause
    exit /b 1
)

REM Aktifkan virtual environment
echo [INFO] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

REM Jalankan aplikasi
echo [INFO] Menjalankan aplikasi Flask...
echo.
echo ========================================
echo   Dashboard Stance Analysis
echo   http://127.0.0.1:5000/
echo ========================================
echo.
echo Tunggu hingga server benar-benar mulai (estimasi 3 - 5 menit karena load model)...
echo.

python app.py
