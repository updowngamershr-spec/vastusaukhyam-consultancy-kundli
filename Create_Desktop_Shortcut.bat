@echo off
title Create Desktop Shortcut - Vastusaukhyam Consultancy
cd /d "%~dp0"
color 0A
cls
echo ===============================================================================
echo            CREATING VASTUSAUKHYAM ASTROLOGY DESKTOP SHORTCUT
echo ===============================================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$desktop = [Environment]::GetFolderPath('Desktop');" ^
  "$ws = New-Object -ComObject WScript.Shell;" ^
  "$lnkPath = Join-Path $desktop 'वास्तुसौख्यम् कन्सलटन्सी (Vastusaukhyam Astrology).lnk';" ^
  "$s = $ws.CreateShortcut($lnkPath);" ^
  "if (Test-Path '%~dp0VastusaukhyamAstro.exe') { $s.TargetPath = '%~dp0VastusaukhyamAstro.exe'; $s.WorkingDirectory = '%~dp0'; } elseif (Test-Path '%~dp0ShivanshAstroVastu.exe') { $s.TargetPath = '%~dp0ShivanshAstroVastu.exe'; $s.WorkingDirectory = '%~dp0'; } else { $s.TargetPath = '%~dp0START_SHIVANSH_ASTRO_VASTU.bat'; $s.WorkingDirectory = '%~dp0'; }" ^
  "if (Test-Path '%~dp0app_icon.ico') { $s.IconLocation = '%~dp0app_icon.ico,0'; }" ^
  "$s.Description = 'वास्तुसौख्यम् कन्सलटन्सी - Professional Offline Kundli & Vastu Software';" ^
  "$s.Save();" ^
  "Write-Host '   SUCCESS: Desktop Shortcut Created!' -ForegroundColor Green;"

echo.
echo Shortcut created on your Windows Desktop!
echo You can now double click 'वास्तुसौख्यम् कन्सलटन्सी (Vastusaukhyam Astrology)' on your desktop to start.
echo.
pause
