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

log_archivo="out/dns_check.log"
txt_archivos="out/*.txt"

cleanup() {
    echo "Limpiando archivos temporales..."
    if [ -f "$log_archivo" ]; then
        rm -f "$log_archivo"
        echo "Archivo de log eliminado."
    else
        echo "El archivo de log no existe."
    fi

    if ls $txt_archivos 1> /dev/null 2>&1; then
        rm -f $txt_archivos
        echo "Archivos .txt eliminados."
    else
        echo "No se encontraron archivos .txt."
    fi

    echo "Archivos temporales eliminados."
}

mkdir -p "$(dirname "$log_archivo")"

trap 'cleanup' EXIT 

pipeline_de_unix() {
    archivo="out/archivo_de_usuarios.txt"  

    if [ ! -f "$archivo" ]; then
        echo "El $archivo no existe."
        exit 1
    fi

    echo "Procesando el archivo de usuarios..."
    
    cat "$archivo" | grep "admin" | awk -F ':' '{print $2}' | sort > "out/resultados_admins.txt" 

    echo "Proceso completado."

}
pipeline_de_unix