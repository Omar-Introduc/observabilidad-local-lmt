.PHONY: help tools test clean

help:
	@echo ""
	@echo "Targets disponibles:"
	@echo "  help   - Muestra esta ayuda."
	@echo "  tools  - Verifica si las herramientas necesarias (curl, dig, bats) están instaladas."
	@echo "  test   - Ejecuta las pruebas unitarias con Bats."
	@echo "  clean  - Limpia archivos generados (implementaremos en proximos sprints)."

# Definción de targets
tools:
	@echo "Verificando herramientas necesarias..."
	@command -v bash >/dev/null 2>&1 || { echo >&2 "Error: 'bash' no está instalado. Abortando."; exit 1; }
	@command -v curl >/dev/null 2>&1 || { echo >&2 "Error: 'curl' no está instalado. Abortando."; exit 1; }
	@command -v dig >/dev/null 2>&1 || { echo >&2 "Error: 'dig' no está instalado. Abortando."; exit 1; }
	@command -v bats >/dev/null 2>&1 || { echo >&2 "Error: 'bats' no está instalado. Abortando."; exit 1; }
	@echo "Todas las herramientas necesarias están instaladas. ✅"
test:
	@echo "Ejecutando pruebas con Bats..."
	@bats tests/
clean: