## Implementacion de persistencia Store
En este paso logramos construir el servicio store para guardar permanentemente los logs.
* en codigo Creamos src/store/main.py. Su trabajo es simple: define la URL POST /save/log y guarda cualquier log que reciba en una base de datos SQLite.
* Creamos su dockerfile y su módulo de Terraform para el modulo Store.
* Para obtener una Persistenci usamos volúmenes en docker-compose.yml y Terraform para que la base de datos no se borre al apagar el contenedor.
![alt text](imagenes/verificacion-de-envio-simple.png)
![alt text](imagenes/envio-guardado-volumen.png)
* La Conexión: Le decimos a docker-compose.yml y a main.tf que "enciendan" y gestionen el nuevo servicio store.
![alt text](imagenes/verificacion-docker.png)
