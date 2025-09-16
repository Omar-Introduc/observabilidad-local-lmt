## Variables de entorno de configuración

| Variable       | Descripción                                 | Valor por defecto   | Ejemplo           |
|----------------|---------------------------------------------|---------------------|-------------------|
| TARGET_HOST    | Host o IP de destino para la configuración  | localhost           | 192.168.1.10      |
| TARGET_PORT    | Puerto de destino para la conexión          | 8080                | 443               |
| ENVIRONMENT    | Entorno de despliegue (dev, prod, etc.)     | development         | production        |

### Uso

Puedes definir las variables de entorno antes de ejecutar el script.  
Si no se definen, se usarán los valores por defecto.

```bash
export TARGET_HOST=192.168.1.10
export TARGET_PORT=443
export ENVIRONMENT=production
./src/configurador.sh
```