@echo off
cd /d "%~dp0"
echo Running comprehensive decoder...
python comprehensive_decode.py > output.txt 2>&1
type output.txt
echo.
echo Output also saved to output.txt
pause
