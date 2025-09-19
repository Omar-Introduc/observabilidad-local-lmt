#!/usr/bin/env bats

CONFIG_PATH="./src/configurador.sh"
ARCHIVO_PATH="./config/archivo_de_usuarios.txt"

setup(){
    touch "$ARCHIVO_PATH"
    echo "ejemplo:ejemplo:admin" > "$ARCHIVO_PATH"
}

teardown(){
   rm -f "$ARCHIVO_PATH"
}


@test "Script: 'configurador.sh' es ejecutable..." {
    if [ ! -x "$CONFIG_PATH" ]; then
        echo "Error: configurador.sh no tiene permiso de ejecución" >&2
        false
    else
        echo "configurador.sh tiene permiso de ejecución" >&3
    fi
    
    run "$CONFIG_PATH"
    if [ $status -ne 0 ]; then
        echo "Error: configurador.sh devolvió estado $status" >&2
        false
    else
        echo "configurador.sh se ejecutó sin errores" >&3
    fi
}

@test "Makefile: 'make tools' finaliza con éxito..." {
    run make tools
    if [ $status -ne 0 ]; then
        echo "Error: 'make tools' devolvió estado $status" >&2
        false
    else
        echo "'make tools' se ejecutó sin errores" >&3
    fi
}
