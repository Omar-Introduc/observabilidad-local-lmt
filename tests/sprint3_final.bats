#!/usr/bin/env bats
CONFIG_PATH="./src/configurador.sh"



@test "Red: Verificación de dig" {
  	run bash -c '
	    source ./src/configurador.sh
	    verificar_dns www.google.com
	  '
 	OUT="$output"
 	
  
 	run dig +short www.google.com
 	EXPC_OUT="$output"
  
 	flag=true
  
 	while IFS= read -r line; do
 		if ! grep -q "$line" <<< "$OUT"; then
 			flag=false
 			break
 		fi
	done <<< "$EXPC_OUT"
	#echo "ddd" >&3
	if [[ "$flag" == "false" ]]; then
		echo "Error: No se encontraron todas las IPs esperadas" >&2
		return 1
  	fi

	echo "Se verificaron todas las IPs" >&3
}

@test "Red: Verificación de curl" {

}

@test "Admin: Validación de creación" {

}

@test "Admin: Validación de eliminación" {

}

@test "Admin: Validación de asignación" {

}
