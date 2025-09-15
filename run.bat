@echo off
echo Financial Controlling Dashboard Setup
echo ======================================

REM Check if virtual environment exists, create if not
if not exist financial_env (
    echo Creating new virtual environment...
    python -m venv financial_env
    echo Virtual environment created successfully!
)

REM Activate the virtual environment
echo Activating virtual environment...
call financial_env\Scripts\activate.bat

echo Installing dependencies in virtual environment...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo Dependencies installed successfully!
    echo Starting Financial Dashboard...
    streamlit run app.py
) else (
    echo Failed to install dependencies. Please check requirements.txt.
)

REM Deactivate on exit
deactivate
pause