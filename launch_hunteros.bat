@echo off
echo --- Initializing HunterOS Ecosystem ---
start cmd /k "cd backend && python -m uvicorn app.main:app --reload"
start cmd /k "cd frontend && npm run dev"
echo HunterOS is now launching. Check terminals for status.
pause
