@echo off
echo Installing required dependencies...
pip install -r requirements_converter.txt

echo.
echo Converting MP4 files to GIFs...
python mp4_to_gif_converter.py

echo.
echo Conversion complete! Press any key to exit.
pause