Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Launching Executive Productivity Agent (AIONOS Batch 2027)" -ForegroundColor Yellow
Write-Host "Candidate: Aniruddh Mishra (Bennett University)" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan

Write-Host "`n[1/2] Starting FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor White
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn app.api:app --host 127.0.0.1 --port 8000 --reload"

Write-Host "[2/2] Starting Streamlit Dashboard on http://localhost:8501..." -ForegroundColor White
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m streamlit run app/ui.py"

Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "Services Launched successfully!" -ForegroundColor Green
Write-Host "• Streamlit Dashboard: http://localhost:8501" -ForegroundColor Yellow
Write-Host "• FastAPI Docs:        http://127.0.0.1:8000/docs" -ForegroundColor Yellow
Write-Host "• Slide Deck:          Open presentation.html in your browser" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Cyan
