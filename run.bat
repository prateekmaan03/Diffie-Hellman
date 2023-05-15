
cls

@echo off
echo =======================
echo  WELCOME TO THE Procect 
echo =======================
echo chose your type of connection
echo 1.Direct Chat 
echo 2.Encrypted
set /p input= : 

if %input%==1 python main.py 
if %input%==2 python encrypted.py 




