#!/usr/bin/env bats
CONFIG_PATH="./src/configurador.sh"



@test "Red: Verificación de curl" {
	source "$CONFIG_PATH"
	run verificar_dns www.google.com 
	
	OUT="$output"
	
	#echo "$OUT" >&3
	
	
	dig +short www.google.com | while IFS= read -r line; do
		#echo "You entered: $line" >&3
		if [[ ! "$OUT" =~ "$line" ]]; then
			echo "Error: No se hallaron todas las ips">&2
			false
		fi
	done
	
	echo "Se verificaron todas las ips">&3

}

@test "Red: Verificación de dig" {

}

@test "Admin: Validación de creación" {

}

@test "Admin: Validación de eliminación" {

}

@test "Admin: Validación de asignación" {

}
