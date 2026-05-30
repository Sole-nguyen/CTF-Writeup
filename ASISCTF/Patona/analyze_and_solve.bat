@echo off
cd /d "%~dp0"
echo ========================================
echo Running hex analysis...
echo ========================================
python hex_analysis.py
echo.
echo.
echo ========================================
echo Running new solver...
echo ========================================
python solver_new.py
echo.
pause
