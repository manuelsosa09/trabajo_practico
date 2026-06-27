# InstrumentHub

## Descripción del proyecto

InstrumentHub es una aplicación web desarrollada en Python utilizando Flet. Su objetivo es permitir la gestión y visualización de instrumentos musicales, mostrando información como nombre, categoría, descripción e imagen de cada instrumento.

La aplicación permite:

* Visualizar instrumentos musicales.
* Filtrar instrumentos por categoría.
* Buscar instrumentos por nombre.
* Ver detalles de cada instrumento.
* Gestionar favoritos.
* Visualizar perfil de usuario.
* Ejecutar la aplicación localmente o mediante Docker.

## Integrantes del grupo

* Manuel Sosa 
* Sergio Sosa 
* Fernando Ayala

## Tecnologías utilizadas

* Python
* Flet
* SQLite
* Docker
* Git y GitHub
* Render
* Trello
* Windows Task Scheduler / Programador de tareas

## Repositorio GitHub

https://github.com/manuelsosa09/trabajo_practico

## Tablero Trello

https://trello.com/invite/b/690a52011b98a819ca979953/ATTI6a2c52ba7b112da0596a713777c23a78DDE0F2ED/app-de-python

## Link del despliegue en la nube

https://instrumenthub.onrender.com

## Link del video de exposición

https://youtu.be/yccLnT_O6Ss

## Instalación y ejecución local

Para ejecutar el proyecto de forma local, primero se deben instalar las dependencias:

```bash
pip install -r requirements.txt
```

Luego se ejecuta la aplicación con:

```bash
python main.py
```

La aplicación estará disponible en:

```text
http://localhost:8550
```

## Ejecución con Docker

### Construir la imagen Docker

```bash
docker build -t instrumenthub .
```

### Ejecutar el contenedor

```bash
docker run -d --name instrumenthub_container -p 8550:8550 instrumenthub
```

### Verificar contenedor en ejecución

```bash
docker ps
```

### Acceder a la aplicación

```text
http://localhost:8550
```

## Evidencias Docker

Las evidencias se encuentran en la carpeta `evidencias/`.

* Construcción de imagen Docker: `evidencias/docker_build.png`
* Ejecución del contenedor: `evidencias/docker_ps.png`
* Aplicación funcionando: `evidencias/app_funcionando.png`

## Automatización de despliegue y ejecución

El proyecto incluye scripts de automatización para Windows y Linux.

### Windows

Archivo:

```text
deploy.bat
```

Este script automatiza:

* `git add`
* `git commit`
* `git push`
* `docker build`
* `docker stop`
* `docker rm`
* `docker run`

Ejecución:

```bash
deploy.bat
```

### Linux

Archivo:

```text
deploy.sh
```

Este script realiza funciones equivalentes al archivo de Windows.

Permiso de ejecución:

```bash
chmod +x deploy.sh
```

Ejecución:

```bash
./deploy.sh
```

## Automatización programada

Como alternativa de automatización programada, se documentó el uso del Programador de tareas de Windows.

El procedimiento se encuentra en el archivo:

```text
AUTOMATIZACION_PROGRAMADA.md
```

Esta automatización permite ejecutar el archivo `deploy.bat` de forma programada para realizar tareas repetitivas relacionadas con Git, Docker y ejecución del contenedor.

## Control de versiones

El proyecto utiliza Git y GitHub para el control de versiones.

Se trabajó con:

* Rama principal `main`.
* Ramas por integrante.
* Pull Requests para integrar cambios.
* Commits descriptivos.
* Historial de cambios en GitHub.

## Distribución de tareas

### Manuel José Sosa Cristaldo

* Desarrollo de vistas principales.
* Corrección de errores en Flet.
* Configuración Docker.
* Evidencias de ejecución.
* Actualización de README.
* Subida del proyecto a GitHub.

### Sergio José Sosa Cristaldo

* Apoyo en funcionalidades del proyecto.
* Organización de tareas.
* Participación en ramas y Pull Requests.
* Revisión de funcionamiento.

### Fernando

* Apoyo en funcionalidades del proyecto.
* Participación en tareas del tablero Trello.
* Participación en ramas y Pull Requests.
* Revisión general del proyecto.

## Gestión del proyecto

La organización del trabajo se realizó mediante Trello, utilizando tareas asignadas, estados de avance y evidencias del desarrollo.

## Estado del proyecto

El proyecto cuenta con:

* Aplicación funcional.
* Filtro por categorías.
* Visualización de instrumentos.
* Imágenes cargadas correctamente.
* Dockerfile funcional.
* Contenedor ejecutándose correctamente.
* Scripts de automatización.
* Evidencias en carpeta `evidencias/`.
* Repositorio GitHub actualizado.
