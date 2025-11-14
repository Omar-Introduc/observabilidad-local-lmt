# Proyecto 9 - "Observabilidad centralizada local": logs, métricas y trazas (simuladas)

**Objetivo.** Desplegar un stack local de observabilidad (contenedores "collector", "store", "viewer" simples) y estandarizar **formato de logs, métricas y trazas** simuladas para servicios de ejemplo.

**Alcance técnico**

* **IaC:** Terraform compone collector (ingesta HTTP), store (JSON append) y viewer (UI mínima), estructura: infra/modules/\* + stacks/observability con defaults sensatos, evitando imports manuales.
* **Patrones:** **Facade** para API de observabilidad con DIP tipado, **Adapter** para sinks.
* **Testing:** fixtures con payloads de log/metric/trace, parametrize para esquemas (campos obligatorios con casos límite), patch.object para IO, autospec sobre clientes, call\_args\_list para validar etiquetado (service, env, version), tracebacks PEP 657.
* **Git/CI:** hooks de formateo y chequeo de claves (no-bloqueantes iniciales con gitleaks), Action que ejecuta suite y publica artefacto de "resumen de observabilidad" (JSON), sub-issues para métricas.
* **Automatización:** Integra custom fields para trends en ingesta.

**Sprints (10 días -> 3 sprints)**

* **S1 (D1-3):** Contratos de observabilidad + collector con validación, sub-issues para tasks.
* **S2 (D4-6):** Store + Viewer básicos, métricas de ingesta, burndown visible.
* **S3 (D7-10):** E2E con dos servicios demo y reporte con trends.

**Entregables y evidencia**

* observability/(collector,store,viewer), infra/terraform/ (con tflint/tfsec), tests/, README, video 4-6 min (tablero + ingesta demo con custom fields).

**Criterios de aceptación**

* 100% logs válidos, métricas mínimas (req/s, error rate), cobertura $\ge 90\%$, 0% drift en Terraform.

**Métricas**

* % eventos válidos, latencia P95 ingesta con trends, coverage, cycle time, burndown, blocked time.
