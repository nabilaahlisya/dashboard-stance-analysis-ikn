@echo off
echo ========================================
echo   Membuat Virtual Environment
echo ========================================
echo.

REM Cek apakah Python terinstall
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan! Silakan install Python terlebih dahulu.
    pause
    exit /b 1
)

REM Hapus venv lama jika ada
if exist "venv" (
    echo [INFO] Menghapus virtual environment lama...
    rmdir /s /q venv
)

REM Buat virtual environment baru
echo [INFO] Membuat virtual environment baru...
python -m venv venv

REM Aktifkan venv dan install requirements
echo [INFO] Menginstall dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo   Instalasi Selesai!
echo ========================================
echo.
echo Untuk menjalankan aplikasi, gunakan: run_app.bat
echo.
pause
