@echo off
echo Starting Vision Study RAG...
echo =======================================

:: Activate virtual environment
call venv\Scripts\activate

:: Run the application
python -m streamlit run app.py

echo =======================================
pause