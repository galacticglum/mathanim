@echo off
call Windows-Clean.bat
mkdir Build
cd Build
cmake ../
mkdir Debug
mkdir Release
copy ..\Dependencies\bin\ Debug
copy ..\Dependencies\bin\ Release

cd ..