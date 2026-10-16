@echo off
setlocal
set "RYLAY_PG_ROOT=%LOCALAPPDATA%\RYLAY\PostgreSQL"
set "RYLAY_PG_CTL=%RYLAY_PG_ROOT%\runtime\bin\pg_ctl.exe"
if not exist "%RYLAY_PG_CTL%" goto missing
if not exist "%RYLAY_PG_ROOT%\data\PG_VERSION" goto missing
"%RYLAY_PG_CTL%" -D "%RYLAY_PG_ROOT%\data" status >nul 2>&1
if not errorlevel 1 (
  echo RYLAY PostgreSQL is already running.
  exit /b 0
)
"%RYLAY_PG_CTL%" -D "%RYLAY_PG_ROOT%\data" -l "%RYLAY_PG_ROOT%\server.log" -w start
exit /b %ERRORLEVEL%

:missing
echo RYLAY PostgreSQL is not initialized. Follow docs\postgresql.md.
echo This launcher never creates or resets data.
exit /b 1
