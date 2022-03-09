@echo off

echo Installing python packages...
pip install -r requirements.txt
echo.
echo.

echo Getting the database URL...
for /f "tokens=* usebackq" %%f in (`heroku pg:credentials:url DATABASE --app cs673projectbackend 2^>^&1 ^| python -c "from sys import stdin; print(next(filter(lambda s: 'postgres' in s.lower(), stdin.readlines())).strip())"`) do (
set DATABASE_URL=%%f
)
echo %DATABASE_URL%
echo.
echo.

echo Launching...
set FLASK_ENV=development
python -m cs673backend
echo.
echo.

pause