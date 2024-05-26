# Proyecto scraping


## Objectivo
Se crea un sistema para extraer informacion sobre procesos judicales 
(caussa, detalles y actuaciones judiciales) de una persona a traves de su identificacion.

## Implementacion

- Se crea el servicio `/signup` para registrar los usuarios que tendran acceso a la ejecucion del scraper.
- Se crea el servicio `/login` para autenticar los usuarios previamente creados.
- Se crea el servicio `/refresh-token` para actualizar el token de acceso al endpoint de busqueda
- Se crea el servicio `/search` para ejecutar la busqueda y generar un archivo csv con la informacion.

## Documentacion

1. Para conocer los API's deben ingresar a `/docs` en su servidor local.
2. Adjunto al proyecto hay una carpeta con un archivo de `postman` en la 
ruta `/docs` como ejemplo de los datos que se deben asignar en los servicios expuestos.

## pasos para correr el proyecto en local

1. Crear un entorno virtual `python3 -m venv nombre-de-ambiente`
2. Instalar dependencias `pip3 install -r requirements.txt`
3. Crear la base de datos y configurar su `.envrc` y `alembic.ini`
4. Aplicar las migraciones con alembic `alembic upgrade head`
5. Levantar el servidor `uvicorn main:app` o `uvicorn main:app --reload` en el caso de que necesiten autorecarga del servidor.