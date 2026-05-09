@echo off
REM Build the paper from the repository root.
REM
REM Usage:
REM   build.cmd            : build the paper (default)
REM   build.cmd all        : full build: env, tests, paper, promote
REM   build.cmd tests      : run pytest
REM   build.cmd clean      : remove build artifacts
REM
REM Requires GNU Make >= 4.3, a TeX distribution (MiKTeX or TeX Live),
REM and Python 3.  On Windows, run from an MSYS2 UCRT64 shell or a
REM Command Prompt that has GNU Make on PATH (e.g. via `pacman -S make`
REM in MSYS2).

setlocal

cd /d "%~dp0"

set "target=%~1"
if "%target%"=="" set "target=paper"

where make >nul 2>nul
if errorlevel 1 (
    echo build.cmd: GNU Make is required but not found in PATH. 1>&2
    exit /b 1
)

make %target%
exit /b %errorlevel%
