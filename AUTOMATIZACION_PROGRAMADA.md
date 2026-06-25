# Automatización Programada - InstrumentHub

## Herramienta utilizada

Para la automatización programada se propone utilizar el Programador de tareas de Windows.

## Objetivo

Ejecutar automáticamente el archivo deploy.bat para automatizar el proceso de actualización del proyecto, subida a GitHub, construcción de la imagen Docker y ejecución del contenedor.

## Pasos generales

1. Abrir el Programador de tareas de Windows.
2. Crear una tarea básica.
3. Colocar el nombre: Deploy InstrumentHub.
4. Elegir la frecuencia de ejecución.
5. En acción, seleccionar Iniciar un programa.
6. Seleccionar el archivo deploy.bat ubicado en la carpeta del proyecto.
7. Guardar la tarea programada.

## Archivo automatizado

El archivo utilizado para la automatización es:

deploy.bat

## Funciones del archivo deploy.bat

- Ejecuta git add.
- Ejecuta git commit.
- Ejecuta git push.
- Construye la imagen Docker.
- Detiene el contenedor anterior.
- Elimina el contenedor anterior.
- Ejecuta nuevamente el contenedor actualizado.

## Conclusión

La automatización programada permite ejecutar tareas repetitivas de despliegue y actualización del proyecto, aplicando conceptos básicos de DevOps y Cloud Computing.
