# Proyecto API - Instrucciones para Levantar el Servidor

Este proyecto es una API que utiliza FastAPI. A continuación se detallan los pasos necesarios para realizar las migraciones, ejecutar los seeders, y levantar el servidor.

## Requisitos Previos

Asegúrate de tener instalados los siguientes requisitos en tu entorno:

- Python 3.11.5
- pip
- Virtualenv (opcional, pero recomendado)

## Instalación

1. Clona el repositorio
2. Crea y activa un entorno virtual (opcional pero recomendado):

``` python -m venv env
source env/bin/activate  # Para Linux/Mac
env\Scripts\activate  # Para Windows
```

3. Instala las dependencias del proyecto:

``` pip install -r requirements.txt ```

## Realizar la Migración

Para aplicar las migraciones de la base de datos, ejecuta el siguiente comando:

``` alembic upgrade head ```

## Ejecutar los Seeders

Para poblar la base de datos con datos iniciales (seeders), ejecuta el siguiente comando:

``` python seeder.py ```

## Levantar el Servidor

Para iniciar el servidor de desarrollo, utiliza el siguiente comando:

``` uvicorn main:app --reload ```
El servidor se levantará en http://127.0.0.1:8000 por defecto.