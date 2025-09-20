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
	
	run bash -c '
	    source ./src/configurador.sh
	    verificar_http www.example.com 200
	'
  	
  	OUT="$output"
  	
  	#echo "$OUT" >&3
  	
 	run curl -s -o /dev/null -w "%{http_code}" www.example.com
 	codigo="$output"
  	EXPCT_OUT="Ok: La URL www.example.com devolvió el código de estado HTTP $codigo"
  	
  	
 	flag=false
 	

 	if grep -Fq "$EXPCT_OUT" <<< "$OUT"; then
 		echo "Se verificó el código HTTP correcto" >&3
 		#echo "$EXPCT_OUT" >&3
 		flag=true
 	else
 		#echo "$OUT" >&3
 		echo "Error: Código HTTP incorrecto" >&2
 		false
 	fi

}

@test "Admin: Validación de creación y eliminación de usuarios" {
	
	run bash -c '
	    source ./src/configurador.sh
	    crear_usuario juan 1 1
	 '
	usuarios_dir="out/usuarios"
	if [ ! -f "$usuarios_dir/juan" ]; then
		echo "Error: No se creo archivo de usuario" >&2
 		false
	fi
	EXPCT="$(cat "$usuarios_dir/juan")"
	if [[ ! "$EXPCT" == "UID: 1, GID: 1" ]]; then
		echo "Error: Informacion de usuario se guardo incorrectamente" >&2
		return 1
  	fi
  	
  	echo "Se guardó el usuario correctamente" >&3
	#rm -rf "$usuarios_dir/juan"}
	
	
	run bash -c '
	    source ./src/configurador.sh
	    eliminar_usuario juan
	 '
	
	 if [ -f "$usuarios_dir/juan" ]; then
		echo "Error: No se elimino el usuario correctamente" >&2
		rm -rf "$usuarios_dir/juan"
 		false
	fi
	
	echo "Se eliminó el usuario correctamente" >&3
	
}

