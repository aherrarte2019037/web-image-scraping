# Código base para iniciar
def cargar_buffer(entrada, inicio, tamano_buffer):
  # Obtiene una porción de la entrada desde 'inicio' hasta 'inicio + tamano_buffer'
  buffer = entrada[inicio:inicio + tamano_buffer]

  # Si el buffer no está lleno, añade la bandera 'eof'
  if len(buffer) < tamano_buffer:
    buffer.append("eof")
  return buffer

def procesar_buffer(buffer, entrada, inicio, tamano_buffer):
    puntero_inicio = 0  # Marca el inicio del lexema actual
    puntero_avance = 0  # Puntero para avanzar en el buffer
    lexema = []  # Almacena los caracteres del lexema actual
    
    while puntero_avance < len(buffer):
        # Si se encuentra la bandera 'eof', procesamos el último lexema si existe
        if buffer[puntero_avance] == "eof":
            if lexema:
                print("Lexema procesado:", "".join(lexema))
            break
            
        # Al encontrar un espacio, procesamos el lexema actual
        elif buffer[puntero_avance] == " ":
            if lexema:
                print("Lexema procesado:", "".join(lexema))
                lexema = []
            
        # Si no es espacio ni eof, añadimos el carácter al lexema actual
        else:
            lexema.append(buffer[puntero_avance])
            
        puntero_avance += 1
        
        # Si el puntero de avance llega al final del buffer y no es 'eof', cargamos un nuevo buffer
        if puntero_avance >= len(buffer) and buffer[-1] != "eof":
            # Actualizamos el inicio para la siguiente carga
            inicio += tamano_buffer
            # Cargamos el nuevo buffer
            buffer = cargar_buffer(entrada, inicio, tamano_buffer)
            # Reiniciamos los punteros para el nuevo buffer
            puntero_avance = 0
            puntero_inicio = 0
            
    return inicio

entrada = list("Esto es un ejemplo eof")
inicio = 0
tamano_buffer = 10

buffer = cargar_buffer(entrada, inicio, tamano_buffer)

inicio = procesar_buffer(buffer, entrada, inicio, tamano_buffer)