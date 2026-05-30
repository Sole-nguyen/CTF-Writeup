@echo off
python decode_complete.py > solution_output.txt 2>&1
type solution_output.txt
echo.
echo.
echo ==== Output saved to solution_output.txt ====
echo ==== Check FLAG_FOUND.txt if flag was discovered ====
pause
