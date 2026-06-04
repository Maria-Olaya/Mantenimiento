
@echo off
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo Ocurrio un error. Presiona cualquier tecla para cerrar.
    pause > nul
)