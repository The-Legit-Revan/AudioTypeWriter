@echo off

rem Change the following two lines to match your virtual environment and main Python file paths
set current_dir=%cd%
set env_path=venv
set main_file=main.py

call "%current_dir%\%env_path%\Scripts\activate.bat"
python %main_file%