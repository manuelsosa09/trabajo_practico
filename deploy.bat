@echo off
echo =====================================
echo   DEPLOY AUTOMATICO - InstrumentHub
echo =====================================

set /p MSG=Ingrese mensaje del commit: 

if "%MSG%"=="" (
    set MSG=Actualizacion automatica del proyecto
)

echo.
echo Agregando archivos a Git...
git add .

echo.
echo Creando commit...
git commit -m "%MSG%"

echo.
echo Subiendo cambios a GitHub...
git push origin main

echo.
echo Construyendo imagen Docker...
docker build -t instrumenthub .

echo.
echo Deteniendo contenedor anterior si existe...
docker stop instrumenthub_container 2>nul

echo.
echo Eliminando contenedor anterior si existe...
docker rm instrumenthub_container 2>nul

echo.
echo Ejecutando contenedor...
docker run -d --name instrumenthub_container -p 8550:8550 instrumenthub

echo.
echo =====================================
echo Aplicacion ejecutandose en:
echo http://localhost:8550
echo =====================================

pause
