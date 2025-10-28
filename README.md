# Proyecto 9: Stack de Observabilidad Local

Este repositorio contiene el código para un stack de observabilidad local.

## Objetivo del Proyecto

El objetivo principal es desplegar un stack local (compuesto por contenedores) para centralizar y gestionar logs, métricas y trazas simuladas de diferentes servicios.

## Arquitectura y Componentes

El stack se compone de tres servicios principales:

1.  **Collector (Colector):**
    * Es una API de ingesta HTTP construida con FastAPI.
    * Su función es recibir logs en formato JSON y validarlos contra un "contrato" o esquema predefinido (`log-schema.json`).
    * Si el log es válido, lo acepta; si no, lo rechaza.

2.  **Store (Almacén):**
    * Componente encargado de almacenar los logs válidos que recibe del *Collector* (ej. en formato JSON).

3.  **Viewer (Visor):**
    * Una interfaz de usuario (UI) mínima diseñada para mostrar los logs y métricas almacenados.

## Tecnología Principal

* **Aplicación:** Python con FastAPI.
* **Infraestructura como Código (IaC):** Terraform
* **Contenedores:** Docker.
* **Pruebas:** Pytest.
* **CI/CD:** GitHub Actions.