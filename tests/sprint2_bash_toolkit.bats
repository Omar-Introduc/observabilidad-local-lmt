#!/usr/bin/env bats

CONFIG_PATH="./src/configurador.sh"
ARCHIVO_PATH="./config/archivo_de_usuarios.txt"
DIR_OUT_PATH="./out"
RES_OUT_PATH="$DIR_OUT_PATH/resultados_admins.txt"
LOG_PATH="$DIR_OUT_PATH/dns_check.log"

setup(){
    touch "$ARCHIVO_PATH"
}

teardown(){
   rm -f "$ARCHIVO_PATH"
}

@test "Script: 'configurador.sh' ejecuta clean al encontrar un error" {
    echo "Este archivo" > "$ARCHIVO_PATH"
    echo "No tiene" >> "$ARCHIVO_PATH"
    echo "Una estructura válida" >> "$ARCHIVO_PATH"
    run "$CONFIG_PATH"
    
    if [ -f "$LOG_PATH" ]; then
        echo "Error: configurador.sh no ejecutó clean al entrar en error (todavía existe) " >&2
        false
    else
        echo "configurador.sh manejo el error correctamente" >&3
    fi
}

@test "Script: Pipeline de 'configurador.sh' funciona correctamente" {
    echo "herbert:Heriberto G.:user" > "$ARCHIVO_PATH"
    echo "gil:Gilberto Leonardo:admin" >> "$ARCHIVO_PATH"
    echo "walter:Walter G.:admin" >> "$ARCHIVO_PATH"
    echo "::admin" >> "$ARCHIVO_PATH"
    echo ":\`\`:admin" >> "$ARCHIVO_PATH"
    run "$CONFIG_PATH"
    
    OUT="$(cat "$RES_OUT_PATH")"
    EXPECTED_OUT=$'\n``\nGilberto Leonardo\nWalter G.'
    #echo "$OUT" >&3
    #echo "$EXPECTED_OUT" >&3
    if [[ ! "$OUT" == "$EXPECTED_OUT" ]]; then
        echo "Error: Pipeline da un resultado diferente al esperado " >&2
        false
    else
        echo "Pipeline esta funcionando correctamente" >&3
    fi
}
