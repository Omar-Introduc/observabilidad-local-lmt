.PHONY: help tools build test run pack clean setup lint format test validate-iac install-iac-tools plan apply destroy dev-up dev-down docker-build docker-run

export PATH := $(CURDIR)/bin:$(PATH)

# COMANDOS FUNCIONALIDAS

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  setup           Instalar dependencias"
	@echo "  tools           Instalar herramientas de desarrollo"
	@echo "  build           Construir el proyecto"
	@echo "  test            Ejecutar pruebas"
	@echo "  run             Ejecutar la aplicación"
	@echo "  pack            Empaquetar la aplicación"
	@echo "  clean           Limpiar el proyecto"
	@echo "  lint            Revisar el código (linter)"
	@echo "  format          Formatear el código (black)"
	@echo "  plan            Ver el plan de Terraform"
	@echo "  apply           Aplicar cambios de Terraform"
	@echo "  destroy         Destruir con Terraform"
	@echo "  validate-iac    Validar la infraestructura (código)"
	@echo "  dev-up          Iniciar entorno de desarrollo"
	@echo "  dev-down        Detener entorno de desarrollo"
	@echo "  docker-build    Crear imagen de Docker"
	@echo "  docker-run      Ejecutar contenedor de Docker"


# DESARROLLO

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt && pip install -r requirements-dev.txt

tools: install-iac-tools
	
build: setup
	. .venv/bin/activate && python3 -m build --wheel

run:
	. .venv/bin/activate && uvicorn src.collector.main:app --host 0.0.0.0 --port 8000

pack: setup
	. .venv/bin/activate && python3 -m build --sdist

clean:
	@echo "Cleaning up..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -f .coverage
	rm -rf dist
	rm -rf .pytest_cache
	rm -rf *.egg-info

# LINT Y TEST
lint: setup
	. .venv/bin/activate && flake8 src tests

format: setup
	. .venv/bin/activate && black src tests

test: setup
	. .venv/bin/activate && pytest --cov=src --cov-fail-under=85

# INFRAESTRUCTURA DE TERRAFORM

validate-iac: install-iac-tools
	(cd infra/terraform/stacks/observability && terraform init && terraform validate && tflint --recursive && tfsec .)

plan: validate-iac
	(cd infra/terraform/stacks/observability && terraform plan)

apply: validate-iac
	(cd infra/terraform/stacks/observability && terraform apply --auto-approve)

destroy:
	(cd infra/terraform/stacks/observability && terraform destroy --auto-approve)

# FUNCIONALIDADES DE DOCKER

dev-up:
	docker-compose up -d

dev-down:
	docker-compose down

docker-build:
	docker-compose build

docker-run:
	docker-compose up


# TOOLS( Configuracion de instalacion iac a mejorar)

install-iac-tools:
	@[ -d $(CURDIR)/bin ] || mkdir -p $(CURDIR)/bin
	@echo "Installing TFLint..."
	@curl -s -L "https://github.com/terraform-linters/tflint/releases/download/v0.50.3/tflint_linux_amd64.zip" -o "/tmp/tflint.zip" && \
	unzip -o "/tmp/tflint.zip" -d "$(CURDIR)/bin/" && \
	rm "/tmp/tflint.zip"
	@echo "Installing TFSec..."
	@curl -s -L "https://github.com/aquasecurity/tfsec/releases/download/v1.28.6/tfsec-linux-amd64" -o "$(CURDIR)/bin/tfsec" && \
	chmod +x "$(CURDIR)/bin/tfsec"
