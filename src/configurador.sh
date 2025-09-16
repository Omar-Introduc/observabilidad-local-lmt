#!/bin/bash
set -euo pipefail

# Leer variables de entorno con valores por defecto
TARGET_HOST="${TARGET_HOST:-localhost}"
TARGET_PORT="${TARGET_PORT:-8080}"
ENVIRONMENT="${ENVIRONMENT:-development}"

echo "Configurando entorno..."
echo "TARGET_HOST: $TARGET_HOST"
echo "TARGET_PORT: $TARGET_PORT"
echo "ENVIRONMENT: $ENVIRONMENT"