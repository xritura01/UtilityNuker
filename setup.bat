@echo off
title Installing Dependencies for Utility Nuker
color 0A

echo Installing Python packages...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install required modules
pip install discord.py colorama

echo.
echo All dependencies installed successfully!
pause
