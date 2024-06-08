@echo off
@REM Run this file to initialize all docker containers developed for this project.
@REM After running this file remember to wait untill container 'databases-startup' goes down! 

@REM IMPORTANT: Only Windows can run this file!
@REM            If on UNIX based system see: start_compose.sh

:port_checking
REM Check if port 5432 is in use
netstat -ano | find "5432" > nul

IF %ERRORLEVEL% EQU 0 (
    echo Port 5432 is currently in use. Docker Compose will not start.
    GOTO process_display
) ELSE (
    echo Port 5432 is free. Starting Docker Compose.
    call start_compose.bat
    GOTO EOF
)

:process_display
netstat -ano | findstr :5432
echo Enter the process ID. This is the number on the rightmost column.
set /p pid=
GOTO process_action

:process_action
echo Process details.
tasklist /FI "PID eq %pid%"
echo Would you like to kill the process (y/n)?
set /p action=
IF /i %action% == y (
    GOTO taskkill
) ELSE IF /i %action% == n (
    echo Unable to continue setup.
    GOTO EOF
) ELSE (
    echo Incorrect value.
    GOTO process_action
)

:taskkill
echo Entered pid %pid%
taskkill /PID %pid% /F
GOTO port_checking

:EOF
echo Process finished.
