@echo off
REM Не показываем сами команды; ошибки Python остаются видны.
REM Переходим в каталог именно этой учебной копии, даже если запускали ярлык.
cd /d "%~dp0"
REM Сначала используем её собственное окружение на другом компьютере.
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py %*
    goto finished
)
REM В исходной рабочей папке готовое окружение находится двумя папками выше.
if exist "..\..\.venv\Scripts\python.exe" (
    "..\..\.venv\Scripts\python.exe" main.py %*
    goto finished
)
REM Ничего не устанавливаем незаметно: порядок подготовки есть в README.
echo Install Python 3.12, create .venv and install requirements.txt. See README.md.
pause
exit /b 1
:finished
REM При ошибке оставляем консоль открытой, чтобы можно было прочитать причину.
if errorlevel 1 pause
