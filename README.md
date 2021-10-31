Requerimientos software:

- Flask
- Postgresql
- Python3
- Libreria psycopg2 (Python3 se instala con pip3)
 

Pasos para uso de software:

1- Crear usuario con nombre y password: "tics" en postgresql

2- Crear bdd llamada "tics" en postgresql

3- Asignar permisos de tics sobre la bdd creada

4- Ejecutar el archivo setup.py con python3 (Configuración de tablas) :
      
      python3 setup.py
      
5- Ejecutar el archivo seed.py con python3 (Inicialización de valores predeterminados):
 
      python3 seed.py
      
6- Levantar el servidor con permisos de administrador (Debido a que utiliza el puerto 80) con sudo en ubuntu por ejemplo ejecutando el archivo run.py con python3.py:
 
      sudo python3 run.py
      
7- Abrir página en cualquier navegador con las ruta localhost o 0.0.0.0
8- Visualización de la Página Web

LINKS DE INTERES:
https://databaseandtech.wordpress.com/2019/10/24/como-crear-un-usuario-y-asignarle-permisos-en-postgresql/
https://stackoverflow.com/questions/57236722/what-does-import-error-symbol-not-found-pqencryptpasswordconn-mean-and-how-do
https://phoenixnap.com/kb/install-flask
https://github.com/psycopg/psycopg2/issues/1018
