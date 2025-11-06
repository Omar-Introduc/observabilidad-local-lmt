.PHONY: setup lint test validate-iac install-iac-tools

export PATH := $(CURDIR)/bin:$(PATH)

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt && pip install -r requirements-dev.txt

lint:
	flake8 src tests

test:
	pytest --cov=src

# Aun en desarrollo
validate-iac: install-iac-tools
	(cd infra/terraform/stacks/local_observability && terraform init && terraform validate && tflint --recursive && tfsec .)

# instalacion de dependencias- su utilidad como dependencia se implementara mas adelante
install-iac-tools:
	@[ -d $(CURDIR)/bin ] || mkdir -p $(CURDIR)/bin
	@echo "Installing TFLint..."
	@curl -s -L "https://github.com/terraform-linters/tflint/releases/download/v0.50.3/tflint_linux_amd64.zip" -o "/tmp/tflint.zip" && \
	unzip -o "/tmp/tflint.zip" -d "$(CURDIR)/bin/" && \
	rm "/tmp/tflint.zip"
	@echo "Installing TFSec..."
	@curl -s -L "https://github.com/aquasecurity/tfsec/releases/download/v1.28.6/tfsec-linux-amd64" -o "$(CURDIR)/bin/tfsec" && \
	chmod +x "$(CURDIR)/bin/tfsec"