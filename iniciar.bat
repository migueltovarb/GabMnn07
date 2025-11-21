@echo off
chcp 65001 >nul
color 0A
title Sistema de Gestión de Ingreso a Edificios

echo.
echo ====================================================
echo    SISTEMA DE GESTIÓN DE INGRESO A EDIFICIOS
echo ====================================================
echo.

:: Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] No se encontró el entorno virtual
    echo Por favor, crea el entorno virtual primero con:
    echo python -m venv venv
    echo.
    pause
    exit /b
)

:: Activar entorno virtual
echo [1/5] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [OK] Entorno virtual activado
echo.

:: Verificar e instalar dependencias
echo [2/5] Verificando dependencias...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ADVERTENCIA] Algunas dependencias no se instalaron correctamente
) else (
    echo [OK] Dependencias verificadas
)
echo.

:: Aplicar migraciones
echo [3/5] Aplicando migraciones de base de datos...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Error al aplicar migraciones
    pause
    exit /b
)
echo [OK] Migraciones aplicadas
echo.

:: Recolectar archivos estáticos (opcional)
echo [4/5] Recolectando archivos estáticos...
python manage.py collectstatic --noinput --clear 2>nul
echo [OK] Archivos estáticos listos
echo.

:: Iniciar servidor
echo [5/5] Iniciando servidor Django...
echo.
echo ====================================================
echo    SERVIDOR CORRIENDO EN: http://127.0.0.1:8000
echo    Para detener: Presiona Ctrl+C
echo ====================================================
echo.

python manage.py runserver

:: Si el servidor se detiene
echo.
echo [INFO] Servidor detenido
pause