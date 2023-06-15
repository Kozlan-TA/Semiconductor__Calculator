@echo off
IF not EXIST .venv (
    echo creating venv...
    python3 -m venv .venv
    call .venv\Scripts\activate.bat
    echo installing packages...
    pip install -r requirements.txt
    echo virtual environment created, packages installed
    echo now you can use start.bat
) ELSE (
    echo virtual environment already exits
    echo you can use start.bat
)
pause