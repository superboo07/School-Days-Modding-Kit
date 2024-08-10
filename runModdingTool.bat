@echo off

:: Ensure the script is being run from within its directory
cd /d "%~dp0"

:: Prompt the user to input the directory of their School Days install
set /p install_dir="Enter the directory of your School Days install: "
if not exist "%install_dir%" (
    echo Directory does not exist!
    exit /b 1
)

python ./src/modCUI.py "%install_dir%"
exit /b 0