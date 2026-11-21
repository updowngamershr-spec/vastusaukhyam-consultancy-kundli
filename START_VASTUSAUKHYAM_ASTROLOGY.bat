@echo off
title वास्तुसौख्यम् कन्सलटन्सी (Vastusaukhyam Consultancy)
cd /d "%~dp0"

:: 1. Launch from Vastusaukhyam_Desktop_New_Build if it exists
if exist "%~dp0..\Vastusaukhyam_Desktop_New_Build\VastusaukhyamAstro.exe" (
    cd /d "%~dp0..\Vastusaukhyam_Desktop_New_Build"
    start "" "%~dp0..\Vastusaukhyam_Desktop_New_Build\VastusaukhyamAstro.exe"
    exit
)

if exist "%~dp0dist\Vastusaukhyam_Desktop_New_Build\VastusaukhyamAstro.exe" (
    cd /d "%~dp0dist\Vastusaukhyam_Desktop_New_Build"
    start "" "%~dp0dist\Vastusaukhyam_Desktop_New_Build\VastusaukhyamAstro.exe"
    exit
)

if exist "%~dp0Vastusaukhyam_Desktop_New_Build\VastusaukhyamAstro.exe" (
    cd /d "%~dp0Vastusaukhyam_Desktop_New_Build"
    start "" "%~dp0Vastusaukhyam_Desktop_New_Build\VastusaukhyamAstro.exe"
    exit
)

if exist "%~dp0ShivanshAstroVastu\ShivanshAstroVastu.exe" (
    cd /d "%~dp0ShivanshAstroVastu"
    start "" "%~dp0ShivanshAstroVastu\ShivanshAstroVastu.exe"
    exit
)

if exist "%~dp0ShivanshAstroVastu.exe" (
    start "" "%~dp0ShivanshAstroVastu.exe"
    exit
)

:: Python fallback
python --version >nul 2>&1
if %errorlevel% equ 0 (
    start "" python desktop_main.py
    exit
)

echo [ERROR] Application executable not found!
pause
