@echo off
echo Starting SysAdmin Sentinel...

:: Check if the virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [!] Virtual environment not found. Creating one now...
    python -m venv venv
    
    echo [!] Activating virtual environment...
    call venv\Scripts\activate.bat
    
    echo [!] Installing dependencies...
    pip install -r requirements.txt
    
    echo [!] Setup complete!
) else (
    :: Venv exists, just activate it
    call venv\Scripts\activate.bat
)

:: Run the application
python main.py
pause
