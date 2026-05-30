@echo off
echo.
echo ================================================================================
echo                         PATONA CHALLENGE SOLVER
echo ================================================================================
echo.
python ULTIMATE_SOLVER.py
echo.
echo.
echo ================================================================================
if exist FLAG_SOLUTION.txt (
    echo FLAG FOUND! Check FLAG_SOLUTION.txt
    echo.
    type FLAG_SOLUTION.txt
) else (
    echo No flag found automatically.
    echo Check decode_attempt*.txt files for manual analysis.
)
echo ================================================================================
echo.
pause
