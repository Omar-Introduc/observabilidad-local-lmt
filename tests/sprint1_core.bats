#!/usr/bin/env bats

CONFIG_PATH="./src/configurador.sh"

@test "Script: 'configurador.sh' es ejecutable..." {
    if [! -x "$CONFIG_PATH" ]; then
        echo "Error: configurador.sh no tiene permiso de ejecución" >&2
        false
    else
        echo "configurador.sh tiene permiso de ejecución" >&3
    fi
    
    run bash "$CONFIG_PATH"
    if [ $status -ne 0 ]; then
        echo "Error: configurador.sh devolvió estado $status" >&2
        false
    else
        echo "configurador.sh se ejecutó sin errores" >&3
    fi
}
