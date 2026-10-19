@echo off
rem First run creates a virtual environment and installs dependencies.
cd /d "%~dp0"
if not exist .venv (
  py -3 -m venv .venv
  .venv\Scripts\pip install -q --upgrade pip
  .venv\Scripts\pip install -q -r requirements.txt
)
start "" http://127.0.0.1:8765
.venv\Scripts\python app.py
