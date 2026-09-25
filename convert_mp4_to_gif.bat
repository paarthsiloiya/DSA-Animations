@echo off
if /i "%~1"=="--no-install" goto convert

echo Installing required dependencies...
pip install -r requirements_converter.txt
if errorlevel 1 exit /b 1

:convert
echo.
echo Converting MP4 files to GIFs...
python mp4_to_gif_converter.py

echo.
echo Conversion complete! Press any key to exit.
pause
