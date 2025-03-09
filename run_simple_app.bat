@echo off
echo Starting Vision Study RAG (Simple Version)...
echo =======================================

:: Activate virtual environment
call venv\Scripts\activate

:: Run the application
python -m streamlit run simple_rag_app.py

echo =======================================
pause