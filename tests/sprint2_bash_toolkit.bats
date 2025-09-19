#!/usr/bin/env bats

CONFIG_PATH="./src/configurador.sh"
ARCHIVO_PATH="./config/archivo_de_usuarios.txt"
DIR_OUT_PATH="./out"
LOG_PATH="$DIR_OUT_PATH/dns_check.log"

@test "Script: 'configurador.sh' ejecuta clean al encontrar un error" {
    echo "Este archivo" > "$ARCHIVO_PATH"
    echo "No tiene" >> "$ARCHIVO_PATH"
    echo "Una estructura válida" >> "$ARCHIVO_PATH"
    run "$CONFIG_PATH"
    
    if [ -f "$LOG_PATH" ]; then
        echo "Error: configurador.sh no ejecutó clean al entrar en error (todavía existe " >&2
        rm -f "$ARCHIVO_PATH"
        false
    else
        echo "configurador.sh manejo el error correctamente" >&3
        rm -f "$ARCHIVO_PATH"
    fi
    
    
}
