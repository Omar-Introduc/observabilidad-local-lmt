## Chequeo DNS

**Comando ejecutado:**
```bash
dig example.com > out/dns_check.log 
```

**Explicación:**
Este comando consulta los registros DNS de tipo A para el dominio, lo que devuelve las direcciones IPv4 asociadas. El resultado de la consulta incluye tanto los registros de las direcciones IP como los servidores de nombres que gestionan el dominio.

**Extracto de la salida:**
```
;; QUESTION SECTION:
;example.com.			IN	A

;; ANSWER SECTION:
example.com.		31	IN	A	23.220.75.245
example.com.		31	IN	A	23.192.228.80
example.com.		31	IN	A	23.192.228.84
example.com.		31	IN	A	23.215.0.136
example.com.		31	IN	A	23.215.0.138
example.com.		31	IN	A	23.220.75.232
```

**Conclusión:**
El chequeo DNS fue exitoso. Se resolvieron varias direcciones IP para el dominio, confirmando que los servidores DNS están funcionando correctamente y que el dominio tiene múltiples direcciones asociadas. Este tipo de consulta es útil para verificar la disponibilidad y resolución de un dominio en la red.


## Chequeo HTTP
**Comando ejecutado:**
```bash
curl -i http://example.com > out/http_check.log 
```

**Explicación:**
El comando `curl -i` se empleó para enviar una solicitud HTTP al dominio especificado. La opción `-i` incluye los encabezados de la respuesta junto con el contenido HTML recibido. De esta manera, es posible analizar tanto la información de la respuesta del servidor como el cuerpo del mensaje. El resultado completo se almacenó en el archivo `out/http_check.log` para su posterior análisis.

**Extracto de la salida:**
```
HTTP/1.1 200 OK
Accept-Ranges: bytes
Content-Type: text/html
ETag: "84238dfc8092e5d9c0dac8ef93371a07:1736799080.121134"
Last-Modified: Mon, 13 Jan 2025 20:11:20 GMT
Content-Length: 1256
Cache-Control: max-age=86000
Date: Tue, 16 Sep 2025 15:50:34 GMT
Connection: keep-alive

<!doctype html>
<html>
<head>
    <title>Example Domain</title>
    ...
</head>
<body>
<div>
    <h1>Example Domain</h1>
    ...
</div>
</body>
</html>
```

**Conclusión:**
El chequeo HTTP fue exitoso. El servidor respondió con un código `200 OK` y devolvió el contenido esperado, lo que indica que el servicio HTTP está accesible y funcionando correctamente en el host y puerto configurados.