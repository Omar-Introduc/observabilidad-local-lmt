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
    run "$CONFIG_PATH" "$ARCHIVO_PATH"
    


    OUT="$(cat "$RES_OUT_PATH")"
    EXPECTED_OUT=$'\nGilberto Leonardo\nWalter G.\n``'

    if [[ ! "$OUT" == "$EXPECTED_OUT" ]]; then
        echo "Error: Pipeline da un resultado diferente al esperado " >&2
        false
    else
        echo "Pipeline esta funcionando correctamente" >&3
    fi
}

@test "Makefile: 'make run' finaliza con éxito..." {
    echo "ejemplo:ejemplo:admin" > "$ARCHIVO_PATH"
    run make run
    if [ $status -ne 0 ]; then
        echo "Error: 'make run' devolvió estado $status" >&2
        false
    else
        echo "'make run' se ejecutó sin errores" >&3
    fi
}

@test "Makefile: 'make clean' finaliza con éxito..." {
    run make clean
    if [ $status -ne 0 ]; then
        echo "Error: 'make clean' devolvió estado $status" >&2
        false
    else
        echo "'make clean' se ejecutó sin errores" >&3
    fi
}

@test "Makefile: 'make clean' funciona correctamente" {
    mkdir "$DIR_OUT_PATH"
    touch "$RES_OUT_PATH" "$LOG_PATH"
    run make clean
    
    if [ -d $DIR_OUT_PATH ]; then
        echo "Error: 'make clean' no elimino directorio de forma correcta" >&2
        rm -rf out/*.log out/*.txt out/
        false
    else
        echo "'make clean' funciona correctamente" >&3
    fi
    
}
