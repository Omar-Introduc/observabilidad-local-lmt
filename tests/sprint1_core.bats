#!/usr/bin/env bats

@test "Prueba de ejecución de configurador.sh" {
    run bash ./src/configurador.sh
    if [ $status -ne 0 ]; then
        echo "Error: configurador.sh devolvió estado $status" >&2
        false
    else
        echo "configurador.sh se ejecutó sin errores" >&3
    fi
}
