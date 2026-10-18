@echo off
echo =====================================================================
echo  Smart Technology and Patent Tracker for Critical Minerals
echo =====================================================================
echo Starting Streamlit Dashboard on local server...
cd /d "%~dp0"
python -m streamlit run app.py
pause
