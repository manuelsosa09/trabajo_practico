#!/bin/bash

echo "====================================="
echo "  DEPLOY AUTOMATICO - InstrumentHub"
echo "====================================="

read -p "Ingrese mensaje del commit: " MSG

if [ -z "$MSG" ]; then
    MSG="Actualizacion automatica del proyecto"
fi

echo "Agregando archivos a Git..."
git add .

echo "Creando commit..."
git commit -m "$MSG"

echo "Subiendo cambios a GitHub..."
git push origin main

echo "Construyendo imagen Docker..."
docker build -t instrumenthub .

echo "Deteniendo contenedor anterior si existe..."
docker stop instrumenthub_container 2>/dev/null

echo "Eliminando contenedor anterior si existe..."
docker rm instrumenthub_container 2>/dev/null

echo "Ejecutando contenedor..."
docker run -d --name instrumenthub_container -p 8550:8550 instrumenthub

echo "====================================="
echo "Aplicacion ejecutandose en:"
echo "http://localhost:8550"
echo "====================================="