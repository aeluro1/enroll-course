@echo off

:loop
mkdir refresh
timeout 3
rmdir refresh
timeout 600
goto :loop