@echo off
REM Create the Python virtual environment and install dependencies.
setlocal
cd /d "%~dp0"
make env
exit /b %errorlevel%
