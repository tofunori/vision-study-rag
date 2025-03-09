@echo off
echo Setting up Vision Study RAG environment...
echo =======================================

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt

echo =======================================
echo Setup complete!
echo.
echo To start the application, run:
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Press any key to exit...
pause > nul