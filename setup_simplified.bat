@echo off
echo Setting up Vision Study RAG environment (Simplified)...
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

:: Install basic requirements only
echo Installing streamlit...
pip install streamlit

echo =======================================
echo Basic setup complete!
echo.
echo To run the application:
echo   run_app.bat
echo.
echo Press any key to exit...
pause > nul