@echo off
echo Starting Vision Study RAG (Ultra-Simple Version)...
echo =======================================

:: Activate virtual environment
call venv\Scripts\activate

:: Run the application
python -m streamlit run ultra_simple_app.py

echo =======================================
pause