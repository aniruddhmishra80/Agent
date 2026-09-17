@echo off
echo ======================================================================
echo Launching Executive Productivity Agent (AIONOS Batch 2027)
echo Candidate: Aniruddh Mishra (Bennett University)
echo ======================================================================

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "FastAPI Backend" cmd /k "python -m uvicorn app.api:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting Streamlit Executive Dashboard on http://localhost:8501 ...
start "Streamlit Dashboard" cmd /k "python -m streamlit run app/ui.py"

echo ======================================================================
echo Both services are running!
echo - Executive Dashboard: http://localhost:8501
echo - API Documentation:   http://127.0.0.1:8000/docs
echo ======================================================================
pause
