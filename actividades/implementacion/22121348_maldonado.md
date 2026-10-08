# Actividad individual — Lo que hay detrás de la implementación

Nombre: David Maldonado Barajas
Matrícula: 22121348
Equipo:

## A1

El entorno virtual nos sirve para aislar las versiones de nuestras librerias de Python y que choquen con las versiones de otro proyecto, mientras que docker nos sirve para aislar el sistema operativo para que pueda desplegarse en otro entorno, por lo que las 2 opiniones estan mal ya que ningungo hace inecesario al otro.

## A2

a) No perdio el codigo, por que el codigo no esta en .venv, ahi solo estan los ejecutables de python y librerias.
b) Solo necestia volver a crear el entorno virtual, puede usar el comando `python -m venv .venv` activarlo y luego instalar las dependencias que estan en el archivo `requiriments.txt` con el comando `pip install -r requirements.txt` ya que esta es la lista de las dependencias que se usan.
c) Activar el entorno no hace ninguna instalacion, solo le indica a la computadora donde esta la ruta que debe de usar para los ejecutables de Python, pero solo esta activa durante la ventana de sesion de la terminal, por eso en una nueva terminal se require volver a activar.

## A3

a) La carpeta app solo exite dentro del contenedor de Docker, y el comando COPY . . solo copia todo el contenido de la carpeta actual del alumno (con el primer punto) hacia la carpeta de trabajo del contenedor (el segundo punto que es /app).

b) Ignorar .venv/ evita copiar gigabytes de librerías inútiles e incompatibles al contenedor. Mientras que ignorar db.sqlite3 evita sobreescribir la base de datos de producción con datos de prueba o basura locales.

## B1
