import json
import re

def leer_archivo(ruta:str)->str:
    '''
    recibe como parametro la ruta del archivo que se quiere leer
    abre, lee y cierra el archivo 
    retorna las lineas del archivo en un print
    '''
    with open(ruta, 'r') as archivo:
        contenido = json.load(archivo)
    return contenido['jugadores']
lista_jugadores = leer_archivo("/home/luli/Escritorio/programacion_1/primer_parcial/data_jugadores.json")

def imprimir_dato(cadena_de_texto:str) -> str:
    '''
    toma un strin y lo imprime
    '''
    print(cadena_de_texto)

# 1 - Mostrar la lista de todos los jugadores del Dream Team. 
# Con el formato: Nombre Jugador - Posición. Ejemplo: Michael Jordan - Escolta
def mostrar_jugadores(lista_jugadores) -> str:
    '''
    Recibe una lista de jugadores.
    Lo recorre. Toma el nombre y la posicion para luego
    imprimirlo por consola.
    '''
    for jugador in lista_jugadores:
        nombre = jugador["nombre"]
        posicion = jugador["posicion"]
        mensaje = f"{nombre} - {posicion}"
        imprimir_dato(mensaje)

# 2 - Permitir al usuario seleccionar un jugador por su índice y mostrar sus estadísticas completas, 
# incluyendo temporadas jugadas, puntos totales, promedio de puntos por partido, rebotes totales, 
# promedio de rebotes por partido, asistencias totales, promedio de asistencias por partido, robos totales, 
# bloqueos totales, porcentaje de tiros de campo, porcentaje de tiros libres y porcentaje de tiros triples.
def mostrar_segun_indice(lista_jugadores:list) -> str:
    '''
    Recibe una lista de diccionarios.
    Imprime por consola el jugador segun el indice que ingrese el usuario.
    Devuelve un string que contiene los datos de posicion y estadisticas segun el 
    jugador indcado.
    '''
    lista = []
    
    indice_del_jugador = int(input("\nIngrese el indice del jugador: "))
    if indice_del_jugador < 0 or indice_del_jugador >= len(lista_jugadores):
        imprimir_dato("Indice de jugador invalido.")
    else:
        jugador = lista_jugadores[indice_del_jugador]
        nombre = jugador["nombre"]
        posicion = jugador["posicion"]
        estadisticas = jugador["estadisticas"]

        mensaje_inicial = f"Nombre: {nombre} - Posicion: {posicion} - Estadisticas: "
        lista.append(mensaje_inicial)

        for clave, valor in estadisticas.items():
            mensaje = f"\n»{clave}: {valor}"
            mensaje_formateado = mensaje.replace("_", " ")
            lista.append(mensaje_formateado)
        
    return ''.join(lista)

# 3 - Después de mostrar las estadísticas de un jugador seleccionado por el usuario, 
# permite al usuario guardar las estadísticas de ese jugador en un archivo CSV. 
# El archivo CSV debe contener los siguientes campos: nombre, posición, temporadas, 
# puntos totales, promedio de puntos por partido, rebotes totales, promedio de rebotes por partido, 
# asistencias totales, promedio de asistencias por partido, robos totales, bloqueos totales, 
# porcentaje de tiros de campo, porcentaje de tiros libres y porcentaje de tiros triples.
def guardar_archivo(archivo:str, dato) -> str:
    '''
    Recibe la ruta donde se guardara el archivo, y los datos que seran guardados en esa ruta.
    Sino existe el archivo lo crea.
    Devuelve un mensaje en caso de que se guarde correctamente o no.
    '''
    with open(archivo, "w+") as archivo:
        archivo.write(dato)
        if len(dato) == 0:
            mensaje = f"Error al crear el archivo {archivo}"
        else: 
            mensaje = f"Se creo el archivo: {archivo}"
    return mensaje 

# 4 - Permitir al usuario buscar un jugador por su nombre y mostrar sus logros,
#  como campeonatos de la NBA, participaciones en el All-Star y pertenencia al Salón de la Fama del Baloncesto, etc.
def buscar_jugador_por_nombre(lista_jugadores:list) -> dict:
    '''
    Recibe una lista de diccionaros.
    Solicita el nombre para buscar el diccionario que coincida.
    Devuelve el diccionario del jugador que tiene ese nombre.
    '''
    nombre_jugador_ingresado = input("Ingrese el nombre del jugador que desea buscar: ")
    jugador_encontrado = None
    for jugador in lista_jugadores:
        if jugador["nombre"].lower() == nombre_jugador_ingresado.lower():
            jugador_encontrado = jugador
            break
    return jugador_encontrado

def imprimir_logros_jugador(jugador_encontrado:dict) -> str:
    '''
    Recibe una diccionarios.
    Si el jugador no es un diccionario vacio entonces imprime el nombre
    y sus logros.
    '''
    
    if jugador_encontrado is not None:
        logros = jugador_encontrado["logros"]
        logros = "\n".join(logros)
        mensaje = f"Logros de {jugador_encontrado['nombre']}: \n{logros}"
        imprimir_dato(mensaje)
    else:
        imprimir_dato("Jugador no encontrado.")

# 5 - Calcular y mostrar el promedio de puntos por partido de todo el equipo del Dream Team, 
# ordenado por nombre de manera ascendente. 
def ordenar_por_clave(lista: list, clave: str, flag_orden: bool) -> list:
    """
    Recibe una lista de diccionarios, una clave a partir de la cual va a ordenar, y un valor booleano que 
    si es True el orden es ascendente, en caso contrario es descendente.
    La función ordena una lista de diccionarios por una clave específica en orden ascendente o
    descendente.
    Devuelve una lista ordenada segun los parametros especificada
    """
    lista_nueva = lista[:]
    rango_a = len(lista) -1 
    flag_swap = True

    while flag_swap:
        flag_swap = False
        for indice_A in range(rango_a): 
            if (flag_orden == True and lista_nueva[indice_A][clave] > lista_nueva[indice_A+1][clave]) \
                    or (flag_orden == False and lista_nueva[indice_A][clave] < lista_nueva[indice_A+1][clave]):
                lista_nueva[indice_A], lista_nueva[indice_A+1] = lista_nueva[indice_A+1], lista_nueva[indice_A]
                flag_swap = True

    return lista_nueva

def calcular_promedio(jugadores:list, primera_clave:str, segunda_clave:str)-> float:
    '''
    Recibe una lista de diccionarios, y dos claves para buscar el valor al cual calcular el promedio.
    Calcula y devuelve el promedio segun las claves especificadas.
    '''
    if jugadores: # no sea vacia
        acumulador = 0
        contador = 0
        for jugador in jugadores:
            acumulador += jugador[primera_clave][segunda_clave]
            contador +=1
        if contador > 0:
            promedio = acumulador / contador
            return promedio
    return None

def calcular_imprimir_ordenados_alfabeticamente_promedio(lista_jugadores) -> None:
    '''
    Recibe una lista de diccionarios.
    Ordena la lista, calcula el promedio, e imprime el promedio total y los valores
    por jugador de la cave especificada al sacar el promedio.
    '''
    lista_ordenada = ordenar_por_clave(lista_jugadores, "nombre", True)
    promedio = calcular_promedio(lista_ordenada, "estadisticas" ,"promedio_puntos_por_partido")
    imprimir_dato(f"El promedio del Equipo es: {promedio}")

    for jugador in lista_ordenada:
        nombre_jugador = jugador["nombre"]
        promedio_puntos = jugador["estadisticas"]["promedio_puntos_por_partido"]
        mensaje = f"{nombre_jugador}: {promedio_puntos}"
        imprimir_dato(mensaje)

# 6 - Permitir al usuario ingresar el nombre de un jugador y mostrar si ese jugador
# es miembro del Salón de la Fama del Baloncesto.
def imprimir_clave_jugador(jugador_encontrado:dict) -> None:
    '''
    Recibe el diccionario de un jugador.
    Verifica si el jugador tiene un string perteneciente a una de sus claves.
    Imprime si perteneces, y en caso contrario imprime que no pertenece.
    '''
    mensaje = "Error jugador no encontrado"
    
    if jugador_encontrado is not None:
        logros = jugador_encontrado["logros"]
        for logro in logros:
            if logro == "Miembro del Salon de la Fama del Baloncesto":
                mensaje = f"{jugador_encontrado['nombre']}: \n{logro}"
            else: 
                mensaje = "El jugador no es miembro del Salon de la Fama del Baloncesto"

    imprimir_dato(mensaje)

# 7 - Calcular y mostrar el jugador con la mayor cantidad de rebotes totales.
# 8 - Calcular y mostrar el jugador con el mayor porcentaje de tiros de campo.
# 9 - Calcular y mostrar el jugador con la mayor cantidad de asistencias totales.
# 13 - Calcular y mostrar el jugador con la mayor cantidad de robos totales.
# 14 - Calcular y mostrar el jugador con la mayor cantidad de bloqueos totales.
# 19 - Calcular y mostrar el jugador con la mayor cantidad de temporadas jugadas
def calcular_maximo(lista_jugadores:list, primera_clave:str, segunda_clave:str) -> dict:
    '''
    Recibe una lista de diccionarios, y dos claves.
    Busca el valor maximo segun las claves especificadas en la lista.
    Devuelve el diccionario del jugador maximo.
    '''
    valor_maximo = 0
    jugador_maximo = None

    for jugador in lista_jugadores:
        if valor_maximo < jugador[primera_clave][segunda_clave]:
            valor_maximo = jugador[primera_clave][segunda_clave]
            jugador_maximo = jugador

    return jugador_maximo

# 10 - Permitir al usuario ingresar un valor y mostrar los jugadores que han promediado 
# más puntos por partido que ese valor.
# 11 - Permitir al usuario ingresar un valor y mostrar los jugadores que han 
# promediado más rebotes por partido que ese valor.
# 12 - Permitir al usuario ingresar un valor y mostrar los jugadores que han 
# promediado más asistencias por partido que ese valor.
# 15 - Permitir al usuario ingresar un valor y mostrar los jugadores que
#  hayan tenido un porcentaje de tiros libres superior a ese valor.
# 18 - Permitir al usuario ingresar un valor y mostrar los jugadores que hayan tenido 
# un porcentaje de tiros triples superior a ese valor.
def solicitar_mostrar_maximo_segun_clave(lista_jugadores:list, clave:str) -> list:
    '''
    Recibe una lista de diccionarios, y una clave.
    Solicita el valor a partir del cual desea buscar segun la clave especificada,
    lo valida e imprime los jugadores que cumplen con lo solicitado.
    '''
    valor_ingresado = input("Ingrese el valor que desea buscar: ")

    if re.match("^[0-9]{1,2}$", valor_ingresado): 
        valor_ingresado = int(valor_ingresado)
        clave_normalizada = clave.replace("_", " ")

        for jugador in lista_jugadores:
            if jugador["estadisticas"][clave] > valor_ingresado:
                nombre_encontrado = jugador["nombre"]
                valor_encontrado = jugador["estadisticas"][clave]
                mensaje = f"\n{nombre_encontrado} | {clave_normalizada}: {valor_encontrado}"
                imprimir_dato(mensaje)
    else:
        imprimir_dato("Valor invalido, ingrese un numero entero.")

# 16 - Calcular y mostrar el promedio de puntos por partido del equipo 
# excluyendo al jugador con la menor cantidad de puntos por partido.
def ordenar_por_clave_doble(lista: list, primera_clave: str, segunda_clave: str, flag_orden: bool) -> list:
    """
    Recibe una lista de diccionarios, dos claves a partir de la cual va a ordenar, y un valor booleano que 
    si es True el orden es ascendente, en caso contrario es descendente.
    La función ordena una lista de diccionarios por una clave específica en orden ascendente o
    descendente.
    Devuelve una lista ordenada segun los parametros especificados
    """
    lista_nueva = lista[:]
    rango_a = len(lista) -1 
    flag_swap = True

    while flag_swap:
        flag_swap = False
        for indice_A in range(rango_a): 
            if (flag_orden == True and lista_nueva[indice_A][primera_clave][segunda_clave] > lista_nueva[indice_A+1][primera_clave][segunda_clave]) \
                    or (flag_orden == False and lista_nueva[indice_A][primera_clave][segunda_clave] < lista_nueva[indice_A+1][primera_clave][segunda_clave]):
                lista_nueva[indice_A], lista_nueva[indice_A+1] = lista_nueva[indice_A+1], lista_nueva[indice_A]
                flag_swap = True

    return lista_nueva

def calcular_mostrar_clave_segun_jugador():
    '''
    No recibe parametros.
    Ordena la lista de diccionarios segun los parametros especificados de manera ascendente, elimina la primera
    que es la que contiene el valor minimo. Luego calcula el promdio del resto de los jugadores.
    Ademas, recorre la lista y muestra los jugadores que fueron incluidos para sacar el promedio.
    Y los imprime, al promedio y a los jugadores.
    '''
    lista_ordenada = ordenar_por_clave_doble(lista_jugadores, "estadisticas", "promedio_puntos_por_partido", True)
    del lista_ordenada[0]

    promedio = calcular_promedio(lista_ordenada,"estadisticas" ,"promedio_puntos_por_partido")
    mensaje_promedio = f"El promedio de puntos por partidos sin el peor jugador es: {promedio}"
    imprimir_dato(mensaje_promedio)

    for jugador in lista_jugadores:
        nombre_jugador = jugador["nombre"]
        valor_encontrado = jugador["estadisticas"]["promedio_puntos_por_partido"]
        valor_encontrado = round(valor_encontrado, 2)
        mensaje = f'{nombre_jugador}: {valor_encontrado}'
        imprimir_dato(mensaje)

# 17 - Calcular y mostrar el jugador con la mayor cantidad de logros obtenidos
def maxima_cantidad_logros(lista_jugadores:list) -> None:
    '''
    Recibe una lista de diccionarios.
    Busca el jugador con mayor cantidad de logros y lo imprime.
    '''
    valor_maximo = 0

    for jugador in lista_jugadores:
        cantidad_logros = len(jugador["logros"])
        if cantidad_logros > valor_maximo:
            valor_maximo = cantidad_logros
            nombre_jugador_maximo = jugador["nombre"]

    imprimir_dato(nombre_jugador_maximo)

# 20 - Permitir al usuario ingresar un valor y mostrar los jugadores, ordenados por
#  posición en la cancha, que hayan tenido un porcentaje de tiros de campo superior a ese valor.
def validar_opcion_expresion(expresion: str, valor_ingresado: str) -> str:
    """
    Recibe la expresion a comparar, el valor ingresado por el usuario.
    Valida que coincidan y devuelve la opcion valida.
    """
    opcion_validada = False
    if re.match(expresion, valor_ingresado):
        opcion_validada = int(valor_ingresado)

    return opcion_validada

def filtrar_jugadores_por_estadistica(lista_jugadores: list, clave: str) -> list:
    """
    Recibe una lista de diccionarios, y una clave segun la cual se va a filtrar los jugadores.
    Devuelve los jugadores filtrados en caso de que se encontraran segun el valor ingresado por el usuario, 
    en caso de que no devuelve un mensaje que informa que no hay jugadores que cumplan con lo ingresado.
    """
    jugadores_filtrados = []
    valor_ingresado = input("Ingresa un valor: ")
    valor_ingresado = validar_opcion_expresion(r'^[0-9]{1,2}$', valor_ingresado)
    no_encontrado = True

    if valor_ingresado:
        for jugador in lista_jugadores:
            if jugador["estadisticas"][clave] > valor_ingresado:
                jugadores_filtrados.append(jugador)
                no_encontrado = False

        if no_encontrado:
            mensaje = f"No se encontró ningún jugador con más puntos por partido que {valor_ingresado}"
            imprimir_dato(mensaje)

    return jugadores_filtrados
    
def solicitar_mostrar_segun_clave_ordenar_segun_posicion(lista_jugadores:dict):
    '''
    Recibe una lista de diccionarios.
    La filtra, ordena e imprime a los jugadores que complen con lo solicitado.
    '''
    lista_filtrada = filtrar_jugadores_por_estadistica(lista_jugadores, "porcentaje_tiros_de_campo")
    lista_odenada = ordenar_por_clave(lista_filtrada , "posicion", True)

    for jugador in lista_odenada:
        posicion_del_jugador = jugador["posicion"]
        nombre_del_jugador = jugador["nombre"]
        porcentaje_tiros_de_campo = jugador["estadisticas"]["porcentaje_tiros_de_campo"]

        mensaje = f"{posicion_del_jugador} - {nombre_del_jugador} - {porcentaje_tiros_de_campo}"
        imprimir_dato(mensaje)

#----------------------------------MENU - MAIN-------------------------------------------------------------------------------------------
def imprimir_menu():
    print("\nMenú de opciones:\n")
    print("1. Mostrar lista de jugadores del Dream Team.")
    print("2. Ver estadísticas completas de un jugador seleccionado.")
    print("3. Guardar estadísticas de un jugador en un archivo .")
    print("4. Buscar un jugador por nombre y mostrar sus logros.")
    print("5. Calcular y mostrar el promedio de puntos por partido de todo el equipo del Dream Team, ordenado por nombre.")
    print("6. Verificar si un jugador es miembro del Salón de la Fama del Baloncesto.")
    print("7. Calcular y mostrar el jugador con la mayor cantidad de rebotes totales.")
    print("8. Calcular y mostrar el jugador con el mayor porcentaje de tiros de campo.")
    print("9. Calcular y mostrar el jugador con la mayor cantidad de asistencias totales.")
    print("10. Mostrar jugadores que promediaron más puntos por partido que un valor dado.")
    print("11. Mostrar jugadores que promediaron más rebotes por partido que un valor dado.")
    print("12. Mostrar jugadores que promediaron más asistencias por partido que un valor dado.")
    print("13. Calcular y mostrar el jugador con la mayor cantidad de robos totales.")
    print("14. Calcular y mostrar el jugador con la mayor cantidad de bloqueos totales.")
    print("15. Mostrar jugadores con un porcentaje de tiros libres superior a un valor dado.")
    print("16. Calcular y mostrar el promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad de puntos por partido.")
    print("17. Calcular y mostrar el jugador con la mayor cantidad de logros obtenidos.")
    print("18. Mostrar jugadores con un porcentaje de tiros triples superior a un valor dado.")
    print("19. Calcular y mostrar el jugador con la mayor cantidad de temporadas jugadas.")
    print("20. Mostrar jugadores ordenados por posición en la cancha con un porcentaje de tiros de campo superior a un valor dado.")
    print("21. Exit")

def menu():
    imprimir_menu()
    opcion = int(input("Ingrese una opcion: "))

    while True:
        match opcion:
            case 1:
                mostrar_jugadores(lista_jugadores)

            case 2:
                dato = mostrar_segun_indice(lista_jugadores)
                imprimir_dato(dato)

            case 3:
                ruta_archivo = "/home/luli/Escritorio/programacion_1/primer_parcial/jugador.csv"
                datos_para_guardar = mostrar_segun_indice(lista_jugadores) #str
                guardar_archivo(ruta_archivo, datos_para_guardar)

            case 4:
                imprimir_logros_jugador(buscar_jugador_por_nombre(lista_jugadores))

            case 5:
                calcular_imprimir_ordenados_alfabeticamente_promedio(lista_jugadores)

            case 6:
                imprimir_clave_jugador(buscar_jugador_por_nombre(lista_jugadores))

            case 7:
                jugador_maximo = calcular_maximo(lista_jugadores, "estadisticas", "rebotes_totales")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["rebotes_totales"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"
                imprimir_dato(mensaje)
                
            case 8:
                jugador_maximo = calcular_maximo(lista_jugadores, "estadisticas", "porcentaje_tiros_de_campo")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["porcentaje_tiros_de_campo"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo} %"
                imprimir_dato(mensaje)

            case 9:
                jugador_maximo = calcular_maximo(lista_jugadores, "estadisticas", "asistencias_totales")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["asistencias_totales"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"
                imprimir_dato(mensaje)

            case 10:
                solicitar_mostrar_maximo_segun_clave(lista_jugadores, "promedio_puntos_por_partido")

            case 11:
                solicitar_mostrar_maximo_segun_clave(lista_jugadores, "promedio_rebotes_por_partido")
        
            case 12:
                solicitar_mostrar_maximo_segun_clave(lista_jugadores, "promedio_asistencias_por_partido")

            case 13:
                jugador_maximo = calcular_maximo(lista_jugadores, "estadisticas", "robos_totales")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["robos_totales"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"
                imprimir_dato(mensaje)
                
            case 14:
                jugador_maximo = calcular_maximo(lista_jugadores, "estadisticas", "bloqueos_totales")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["bloqueos_totales"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"
                imprimir_dato(mensaje)

            case 15:
                solicitar_mostrar_maximo_segun_clave(lista_jugadores, "porcentaje_tiros_libres")
                
            case 16:
                calcular_mostrar_clave_segun_jugador()

            case 17:
                maxima_cantidad_logros(lista_jugadores)

            case 18:
                solicitar_mostrar_maximo_segun_clave(lista_jugadores, "porcentaje_tiros_triples")
                
            case 19:
                jugador_maximo = calcular_maximo(lista_jugadores, "estadisticas", "temporadas")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["temporadas"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"
                imprimir_dato(mensaje)
                
            case 20:
                solicitar_mostrar_segun_clave_ordenar_segun_posicion(lista_jugadores)

            #Opcion 21: Salir
            case 21:
                break


def main():
    #Ejecuta la app
    menu()

main()











