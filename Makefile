.PHONY: help tools test clean install

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

test: tools
	@echo "Ejecutando pruebas con Bats..."
	@bats tests/

run: tools
	@echo "Ejecutando el configurador.sh..."
	@bash src/configurador.sh

clean:
	@echo "Limpiando archivos generados..."
	@rm -rf out/*.log out/*.txt out/

install:
	@echo "Crear el directorio de trabajo="
	@echo "   sudo mkdir -p /opt/proyecto-devops-grupo6"
	@echo ""	
	@echo "Copiar el script principal y darle permisos="
	@echo "   sudo cp src/configurador.sh /usr/local/bin/configurador.sh"
	@echo "   sudo chmod +x /usr/local/bin/configurador.sh"
	@echo ""
	@echo "Copiar los archivos de datos necesarios="
	@echo "	  sudo cp -r out/ /opt/proyecto-devops-grupo6/"
	@echo ""
	@echo "Copiar el archivo de servicio de systemd="
	@echo "   sudo cp systemd/configurador.service /etc/systemd/system/configurador.service"
	@echo ""	
	@echo "Configuración de systemd y habilitando el servicio="
	@echo "   sudo systemctl daemon-reload"
	@echo "   sudo systemctl enable configurador.service"	
