#!/bin/bash
set -euo pipefail

cleanup() {

    local log_dir="out"
    local log_archivo="$log_dir/dns_check.log"

    echo "Limpiando archivos temporales..."
    if [ -f "$log_archivo" ]; then
        rm -f "$log_archivo"
        echo "Archivo de log eliminado."
    else
        echo "El archivo de log no existe."
    fi

    echo "Archivos temporales eliminados."
}

pipeline_de_unix() {
    #local archivo="out/archivo_de_usuarios.txt"  
    local archivo="config/archivo_de_usuarios.txt"

    if [ ! -f "$archivo" ]; then
        echo "El $archivo no existe."
        exit 1
    fi

    echo "Procesando el archivo de usuarios..."
    
    cat "$archivo" | grep "admin" | awk -F ':' '{print $2}' | sort > "out/resultados_admins.txt" 

    echo "Proceso completado."

}

main() {

    trap 'cleanup' EXIT  

    TARGET_HOST="${TARGET_HOST:-localhost}"
    TARGET_PORT="${TARGET_PORT:-8080}"
    ENVIRONMENT="${ENVIRONMENT:-development}"

    local log_dir="out"
    mkdir -p "$log_dir"

    echo "Configuración en proceso..."
    echo "TARGET_HOST: $TARGET_HOST"
    echo "TARGET_PORT: $TARGET_PORT"
    echo "ENVIRONMENT: $ENVIRONMENT"

    pipeline_de_unix
}
main "$@"