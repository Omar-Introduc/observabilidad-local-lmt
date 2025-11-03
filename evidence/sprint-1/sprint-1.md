
### Cómo vamos a Definir el contrato de datos

Para estar seguros de que solo aceptamos datos buenos, creamos un sistema de reglas y pruebas.

  * **Creamos "Contratos" con Pydantic:** Usamos una herramienta llamada Pydantic para definir cómo deben verse nuestros datos. Básicamente, escribimos reglas como:
      * Un `LogEvent` (evento de log) **debe** tener un campo `level`.
      * Ese `level` **solo** puede ser "INFO", "WARN", "ERROR", etc.
      * Un `MetricEvent` (evento de métrica) **no puede** tener un valor negativo.
  * **Probamos las Reglas:** Escribimos pruebas (`pytest`) para asegurarnos de que el vigilante haga bien su trabajo:
    1.  **Prueba a efectividad:** Le enviamos datos perfectos y comprobamos que los acepte.
    2.  **Prueba a error:** Le enviamos datos malos y comprobamos que los rechace.
  * **Hicimos que las Pruebas Funcionen:** Las pruebas no podían encontrar el código `src`. Para arreglarlo, creamos el archivo `pytest.ini`.
 ![alt text](imagenes/image.png)

