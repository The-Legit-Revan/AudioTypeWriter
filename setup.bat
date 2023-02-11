@echo off
set current_dir=%cd%
cd %current_dir%
echo Creating Python Virtual Environment
python -m venv venv
echo Activating Python Virtual Environment
call venv\Scripts\activate.bat
echo Installing Requirements to Virtual Environment
call pip install -r requirements.txt --no-deps
mkdir Output
del requirements.txt
del %0