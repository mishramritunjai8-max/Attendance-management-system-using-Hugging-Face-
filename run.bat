@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if not exist ".env" (
  copy ".env.example" ".env" >nul
  echo Created .env. Open it and add your Hugging Face token, then run run.bat again.
  notepad .env
  pause
  exit /b 0
)
python main.py
pause
