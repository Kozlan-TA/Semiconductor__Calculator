@echo off
IF not EXIST .venv (
    echo virtual environment is not exits, use create_venv.bat file and restart start.bat
) ELSE (
    start .venv\Scripts\activate.bat
)
pause