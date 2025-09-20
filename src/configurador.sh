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

verificar_dns() {
    local dominio="$1"
    local log_file="out/dns_check.log"
    
    echo ""
    echo "Vericando DNS para el dominio: '$dominio'..."

    dig "$dominio" >> "$log_file"

    local ip_resuelta

    ip_resuelta=$(dig +short "$dominio")

    if [ -z "$ip_resuelta" ]; then
        echo "Error: No se pudo resolver el dominio $dominio">&2
        return 1
    else
        echo "El dominio $dominio se resolvió a la IP: $ip_resuelta"
        return 0
    fi
}

verificar_http() {
    local dominio="$1"
    local codigo_esperado="$2"
    echo ""
    echo "Verificando HTTP para la URL: $dominio..."


    local codigo_real
    codigo_real=$(curl -s -o /dev/null -w "%{http_code}" "$dominio")

    if [ "$codigo_real" -eq "$codigo_esperado" ]; then
        echo "Ok: La URL $dominio devolvió el código de estado HTTP $codigo_real" >&2
    else
        echo "Error:  Se esperaba el código '$codigo_esperado' pero se recibió '$codigo_real' de la URL '$dominio'." 
        exit 1
    fi
}

pipeline_de_unix() {

    local archivo="$1"

    if [ ! -f "$archivo" ]; then
        echo "Error: El archivo '$archivo' no existe." >&2
        exit 1
    fi

    echo "Procesando el archivo de usuarios..."
    
    cat "$archivo" | grep "admin" | awk -F ':' '{print $2}' | LC_ALL=C sort > "out/resultados_admins.txt"

    echo "Proceso completado."

}

verificar_certificado_tls() {
    local DOMINIO=$1
    if [ -z "$DOMINIO" ]; then
        echo "ADVERTENCIA: dominio no proporcionado verificar el certificado."
        return
    fi 
    
    echo "INFO: Verificando certificado TLS para $DOMINIO..."

    local FECHA_EXP=$(echo | openssl s_client -connect $DOMINIO:443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)

    if [ -z "$FECHA_EXP" ]; then
        echo "ERROR: No se pudo obtener la fecha de expiración del certificado para $DOMINIO" >&2
        return 1
    fi

    local EXP_SEGUNDOS=$(date -d "$FECHA_EXP" +%s)
    local HOY_SEGUNDOS=$(date +%s)

    if [ "$EXP_SEGUNDOS" -lt "$HOY_SEGUNDOS" ]; then
        echo "ERROR: El certificado TLS para $DOMINIO ha expirado el $(date -d "@$EXP_SEGUNDOS")" >&2
    else
        local DIAS_RESTANTES=$(( ($EXP_SEGUNDOS - $HOY_SEGUNDOS) / 86400 ))
        echo "OK: El certificado para $DOMINIO es válido. Expira en $DIAS_RESTANTES días."
    fi

}

main() {

    trap 'cleanup' EXIT  

    local TARGET_HOST="${TARGET_HOST:-localhost}"
    local TARGET_PORT="${TARGET_PORT:-8080}"
    local ENVIRONMENT="${ENVIRONMENT:-development}"

    local CHECK_DOMAIN="${CHECK_DOMAIN:-"google.com"}"
    local CHECK_URL="${CHECK_URL:-"https://www.google.com"}"
    local EXPECTED_STATUS="${EXPECTED_STATUS:-200}"
    
    mkdir -p "out"

    echo ""
    echo "Configuración en proceso..."
    echo "TARGET_HOST: $TARGET_HOST"
    echo "TARGET_PORT: $TARGET_PORT"
    echo "ENVIRONMENT: $ENVIRONMENT"
    echo ""    


    local archivo_a_procesar="${1:-config/archivo_de_usuarios_ejemplo.txt}"
    mkdir -p "$(dirname "$archivo_a_procesar")"
    pipeline_de_unix "$archivo_a_procesar" 


    echo ""
    echo ""
    echo "Verificaciones de red..."
    verificar_dns "$CHECK_DOMAIN"
    verificar_http "$CHECK_URL" "$EXPECTED_STATUS"
    verificar_certificado_tls "$CHECK_DOMAIN"
}
main "$@"
