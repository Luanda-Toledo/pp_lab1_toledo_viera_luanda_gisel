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
    mensaje = ""

    for jugador in lista_jugadores:
        nombre = jugador["nombre"]
        posicion = jugador["posicion"]
        mensaje += f"{nombre} - {posicion}"
    
    return mensaje

def validar_entero():
    opcion = input("Ingrese un numero: ")

    if re.match("^[0-9]{1,2}$", opcion):
        opcion = int(opcion)
    else:
        return -1

    return opcion

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
    
    indice_del_jugador = validar_entero()
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
    mensaje = ""

    if jugador_encontrado is not None:
        logros = jugador_encontrado["logros"]
        logros = "\n".join(logros)
        mensaje = f"Logros de {jugador_encontrado['nombre']}: \n{logros}"   
    else:
        mensaje = "Jugador no encontrado."
    
    return mensaje

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
    mensaje = ""

    for jugador in lista_ordenada:
        nombre_jugador = jugador["nombre"]
        promedio_puntos = jugador["estadisticas"]["promedio_puntos_por_partido"]
        mensaje += f"{nombre_jugador}: {promedio_puntos} \n"

    return mensaje    

# 6 - Permitir al usuario ingresar el nombre de un jugador y mostrar si ese jugador
# es miembro del Salón de la Fama del Baloncesto.
def buscar_clave_jugador(jugador_encontrado:dict) -> None:
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

    return mensaje

# 7 - Calcular y mostrar el jugador con la mayor cantidad de rebotes totales.
# 8 - Calcular y mostrar el jugador con el mayor porcentaje de tiros de campo.
# 9 - Calcular y mostrar el jugador con la mayor cantidad de asistencias totales.
# 13 - Calcular y mostrar el jugador con la mayor cantidad de robos totales.
# 14 - Calcular y mostrar el jugador con la mayor cantidad de bloqueos totales.
# 19 - Calcular y mostrar el jugador con la mayor cantidad de temporadas jugadas
def calcular_maximo_doble_clave(lista_jugadores:list, primera_clave:str, segunda_clave:str) -> dict:
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
    mensaje = ""
    valor_ingresado = validar_entero()
    clave_normalizada = clave.replace("_", " ")

    for jugador in lista_jugadores:
        if jugador["estadisticas"][clave] > valor_ingresado:
            nombre_encontrado = jugador["nombre"]
            valor_encontrado = jugador["estadisticas"][clave]
            mensaje += f"\n{nombre_encontrado} | {clave_normalizada}: {valor_encontrado} \n"
            
    return mensaje        

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
    mensaje = ""

    promedio = calcular_promedio(lista_ordenada,"estadisticas" ,"promedio_puntos_por_partido")
    mensaje_promedio = f"El promedio de puntos por partidos sin el peor jugador es: {promedio}"
    imprimir_dato(mensaje_promedio)

    for jugador in lista_jugadores:
        nombre_jugador = jugador["nombre"]
        valor_encontrado = jugador["estadisticas"]["promedio_puntos_por_partido"]
        valor_encontrado = round(valor_encontrado, 2)
        mensaje += f'{nombre_jugador}: {valor_encontrado} \n'
        
    return mensaje

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

    return nombre_jugador_maximo

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
    valor_ingresado = validar_entero()
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
    mensaje = ""

    for jugador in lista_odenada:
        posicion_del_jugador = jugador["posicion"]
        nombre_del_jugador = jugador["nombre"]
        porcentaje_tiros_de_campo = jugador["estadisticas"]["porcentaje_tiros_de_campo"]

        mensaje += f"{posicion_del_jugador} - {nombre_del_jugador} - {porcentaje_tiros_de_campo} \n"

    return mensaje  

# 23 BONUS - Calcular de cada jugador cuál es su posición en cada uno de los siguientes ranking:
# Puntos - Rebotes - Asistencias - Robos. Exportar a csv.
def imprimir_tabla(lista_jugadores_ordenada:list) -> None:
    '''
    Recibe una lista de jugadores.
    Imprime el formato de una tabla y recorre la lista agregando filas a la tabla, con 
    los valores solicitados en cada columna.
    '''
    largo = 103
    imprimir_dato("-".center(largo,"-"))
    imprimir_dato("|               JUGADOR              |   PUNTOS     |   REBOTES     |   ASISTENCIA    |   ROBOS       |")
    imprimir_dato("-".center(largo,"-"))
    for jugador in lista_jugadores_ordenada:
        nombre_del_jugador = jugador["nombre"]
        puntos = jugador["estadisticas"]["puntos_totales"]
        rebotes = jugador["estadisticas"]["rebotes_totales"]
        asistencia = jugador["estadisticas"]["asistencias_totales"]
        robos = jugador["estadisticas"]["robos_totales"]

        imprimir_dato(f"|   {str(nombre_del_jugador).center(19)}   |   {str(puntos).center(12)}   |   {str(rebotes).center(12)}   |   {str(asistencia).center(12)}   |   {str(robos).center(12)}   |")
        imprimir_dato("-".center(largo,"-"))

def crear_lista_ordenada_segun_indice(lista_jugadores:list) -> list:
    '''
    Recibe una lista de diccionarios.
    Crea una lista y ordenas sus indices de manera descendente de las claves: 
    Puntos - Rebotes - Asistencias - Robos.
    Devuelve la lista que contiene a los diccionarios de jugadores con el numero de indice en el que 
    se encuentra en comparacion a otros jugadores, como valor en las claves especificadas.
    '''
    lista_copia = lista_jugadores[:]

    lista_estadisticas = ["rebotes_totales", "asistencias_totales", "robos_totales", "puntos_totales"]
    for estadistica in lista_estadisticas:
        lista_ordenada = ordenar_por_clave_doble(lista_copia, "estadisticas", estadistica, False)
        jugadores_con_estadisticas = []

        for i in range(len(lista_ordenada)):
            jugador = lista_ordenada[i]
            nombre = jugador["nombre"]
            jugador["estadisticas"][estadistica] = i + 1
            jugador_modificado = {
                "nombre": nombre,
                "estadisticas": jugador["estadisticas"]
            }
            jugadores_con_estadisticas.append(jugador_modificado)

    return jugadores_con_estadisticas

def convertir_a_texto(datos_obtenidos) -> str:
    '''
    Recibe una lista de diccionarios.
    Toma una lista de valores lo cuales uniendo los elementos y agregandolos a una lista, dan como 
    resultado los valeres de las filas de las tablas.
    Devuelve la nueva lista convertida en string.
    '''
    if isinstance(datos_obtenidos, list):
        lista_claves = ["nombre", "asistencias totales", "puntos_totales", "rebotes_totales", "robos_totales"]
        filas = []

        for jugador in datos_obtenidos:
            valores = [str(jugador["nombre"]), str(jugador["estadisticas"]["asistencias_totales"]),
                        str(jugador["estadisticas"]["puntos_totales"]),  str(jugador["estadisticas"]["rebotes_totales"]),
                        str(jugador["estadisticas"]["robos_totales"])]
            fila = ",".join(valores)
            filas.append(fila)

        claves_str = ",".join(lista_claves)
        datos_para_filas = "{0}\n{1}".format(claves_str, "\n".join(filas))

        return datos_para_filas

    else:
        return ""
    
# 24 - Determinar la cantidad de jugadores que hay por cada posición. Ejemplo: Base: 2 Alero: 3
def contador_segun_posicion(lista_jugadores:list) -> str:
    '''
    Recibe una lista de diccionarios.
    Cuenta segun una clave especifica, en este caso posicion la cantidad de valores posibles para
    esa clave.
    Devuelve un string que contiene el detalle de los valores encontrados.
    '''
    contador_base = 0
    contador_alero = 0
    contador_escolta = 0
    contador_ala_pivot = 0
    contador_pivot = 0

    for jugador in lista_jugadores: 
        if jugador["posicion"] == "Base":
            contador_base += 1
        elif jugador["posicion"] == "Alero":
            contador_alero += 1
        elif jugador["posicion"] == "Escolta":
            contador_escolta += 1
        elif jugador["posicion"] == "Ala-Pivot":
            contador_ala_pivot += 1
        elif jugador["posicion"] == "Pivot":
            contador_pivot += 1
    mensaje = f"Base: {contador_base}\nAlero: {contador_alero}\nEscolta: {contador_escolta}\n"
    mensaje += f"Ala-Pivot: {contador_ala_pivot}\nPivot: {contador_pivot}"
    return mensaje

# 25 - Mostrar la lista de jugadores ordenadas por la cantidad de All-Star de forma descendente. 
# La salida por pantalla debe tener un formato similar a este: Michael Jordan (14 veces All Star)
def ordenar_descendiente_segun_clave(lista_jugadores:list) -> str:
    '''
    Recibe una lista de diccionarios.
    Busca segun la clave logros que es una lista de strings los que coincidan con All-Star, saco el valor 
    numero y lo convierto a un numero entero a partir del cual voy a ordenar la nueva lista creada.
    Devuelvo la nueva lista con el nombre del jugador y la clave especifica ordenada de forma descendente.
    '''
    lista_segun_clave = []

    for jugadores in lista_jugadores:
        logros = jugadores["logros"]

        for logro in logros:
            if re.search("veces All-Star", logro):
                all_star = re.findall(r'\d+', logro)
                all_star = ",".join(all_star) 
                all_star = int(all_star)
                jugador_modificado = {
                    "Nombre": jugadores["nombre"],
                    "All Star": all_star
                }

                if len(jugador_modificado) > 0:
                    lista_segun_clave.append(jugador_modificado)

    lista_ordenada_segun_clave = ordenar_por_clave(lista_segun_clave, "All Star", False)

    cadena = ""
    for jugador in lista_ordenada_segun_clave:
        cadena += f"{jugador['Nombre']} ({jugador['All Star']} veces All Star)\n"

    return cadena

# 26 - Determinar qué jugador tiene las mejores estadísticas en cada valor. 
# La salida por pantalla debe tener un formato similar a este: Mayor cantidad de temporadas: Karl Malone (19)
def calcular_maximo(lista_jugadores:list, primera_clave:str):
    """
    Recibe una lista de diccionarios, y dos claves.
    Busca el valor máximo según las claves especificadas en la lista.
    Devuelve el diccionario del jugador máximo.
    """
    valor_maximo = 0
    jugador_maximo = None

    for jugador in lista_jugadores:
        valor = jugador["estadisticas"].get(primera_clave, 0)
        if valor > valor_maximo:
            valor_maximo = valor
            jugador_maximo = jugador

    return jugador_maximo

def maximo_segun_estadisticas(lista_jugadores:list) -> str:
    '''
    Recibe una lista de diccionarios.
    Recorre el diccionario de estadisticas y busca el mayor en cada clave de todos los 
    jugadores.
    Devuelve un mensaje contodos las claves de estadisticas y los jugadores que ocupan
    el primer lugar en ellas.
    '''
    mensaje = ""
    for jugador in lista_jugadores:
        for clave in jugador["estadisticas"]:
            max_estadisticas = calcular_maximo(lista_jugadores, clave)
            nombre_max_estadisticas = max_estadisticas["nombre"]
            valor_max_estadisticas = max_estadisticas["estadisticas"][clave]
            mensaje += f"{clave}: {nombre_max_estadisticas} - {valor_max_estadisticas}\n"

        if clave == "porcentaje_tiros_triples":
            break

    return mensaje
 
# 27- Determinar qué jugador tiene las mejores estadísticas de todos
def buscar_maximo_segun_key(lista_jugadores:list) -> None:
    """
    Recibe una lista de diccionarios.
    Recorre la lista, y por cada jugador suma los valores que tienen en las claves
    de estadisticas, y los compara con el resto de los jugadores hasta que termina de 
    recorrer la lista y se queda con el maximo.
    Devuelve un mensaje con los valores del maximo.
    """
    if lista_jugadores:
        max_jugador = None
        max_puntaje = 0

        for jugador in lista_jugadores:
            estadistica_total = 0
            for estadistica in jugador["estadisticas"].values():
                estadistica_total += estadistica
            if max_jugador is None or estadistica_total > max_puntaje:
                max_jugador = jugador
    
        nombre_jugador_maximo = max_jugador["nombre"]
        return f"El jugador que tiene las mejores estadísticas: {nombre_jugador_maximo}"
    else:
        return "Error, la lista esta vacia."

#----------------------------------MENU - MAIN-------------------------------------------------------------------------------------------
def imprimir_menu():
    imprimir_dato("\nMenú de opciones:\n")
    imprimir_dato("1. Mostrar lista de jugadores del Dream Team.")
    imprimir_dato("2. Ver estadísticas completas de un jugador seleccionado.")
    imprimir_dato("3. Guardar estadísticas de un jugador en un archivo.")
    imprimir_dato("4. Buscar un jugador por nombre y mostrar sus logros.")
    imprimir_dato("5. Calcular y mostrar el promedio de puntos por partido de todo el equipo del Dream Team, ordenado por nombre.")
    imprimir_dato("6. Verificar si un jugador es miembro del Salón de la Fama del Baloncesto.")
    imprimir_dato("7. Calcular y mostrar el jugador con la mayor cantidad de rebotes totales.")
    imprimir_dato("8. Calcular y mostrar el jugador con el mayor porcentaje de tiros de campo.")
    imprimir_dato("9. Calcular y mostrar el jugador con la mayor cantidad de asistencias totales.")
    imprimir_dato("10. Mostrar jugadores que promediaron más puntos por partido que un valor dado.")
    imprimir_dato("11. Mostrar jugadores que promediaron más rebotes por partido que un valor dado.")
    imprimir_dato("12. Mostrar jugadores que promediaron más asistencias por partido que un valor dado.")
    imprimir_dato("13. Calcular y mostrar el jugador con la mayor cantidad de robos totales.")
    imprimir_dato("14. Calcular y mostrar el jugador con la mayor cantidad de bloqueos totales.")
    imprimir_dato("15. Mostrar jugadores con un porcentaje de tiros libres superior a un valor dado.")
    imprimir_dato("16. Calcular y mostrar el promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad de puntos por partido.")
    imprimir_dato("17. Calcular y mostrar el jugador con la mayor cantidad de logros obtenidos.")
    imprimir_dato("18. Mostrar jugadores con un porcentaje de tiros triples superior a un valor dado.")
    imprimir_dato("19. Calcular y mostrar el jugador con la mayor cantidad de temporadas jugadas.")
    imprimir_dato("20. Mostrar jugadores ordenados por posición en la cancha con un porcentaje de tiros de campo superior a un valor dado.")
    imprimir_dato("23. Bonus - Posición en cada uno de los siguientes ranking: Puntos - Rebotes - Asistencias - Robos")
    imprimir_dato("24. Determinar la cantidad de jugadores que hay por cada posición. Ejemplo: Base: 2 Alero: 3")
    imprimir_dato("25. Mostrar la lista de jugadores ordenadas por la cantidad de All-Star de forma descendente." )
    imprimir_dato("26. Determinar qué jugador tiene las mejores estadísticas en cada valor.")
    imprimir_dato("27. Determinar qué jugador tiene las mejores estadísticas de todos")
    imprimir_dato("21. Exit")

def menu():

    while True:
        imprimir_menu()
        opcion = validar_entero()
        mensaje = None

        match opcion:
            case 1:
                mensaje = mostrar_jugadores(lista_jugadores)

            case 2:
                mensaje = mostrar_segun_indice(lista_jugadores)

            case 3:
                ruta_archivo = "/home/luli/Escritorio/programacion_1/primer_parcial/jugador.csv"
                datos_para_guardar = mostrar_segun_indice(lista_jugadores) #str
                guardar_archivo(ruta_archivo, datos_para_guardar)

            case 4:
                mensaje = imprimir_logros_jugador(buscar_jugador_por_nombre(lista_jugadores))

            case 5:
                mensaje = calcular_imprimir_ordenados_alfabeticamente_promedio(lista_jugadores)

            case 6:
                mensaje = buscar_clave_jugador(buscar_jugador_por_nombre(lista_jugadores))

            case 7:
                jugador_maximo = calcular_maximo_doble_clave(lista_jugadores, "estadisticas", "rebotes_totales")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["rebotes_totales"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"
                
            case 8:
                jugador_maximo = calcular_maximo_doble_clave(lista_jugadores, "estadisticas", "porcentaje_tiros_de_campo")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["porcentaje_tiros_de_campo"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo} %"

            case 9:
                jugador_maximo = calcular_maximo_doble_clave(lista_jugadores, "estadisticas", "asistencias_totales")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["asistencias_totales"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"

            case 10:
                mensaje = solicitar_mostrar_maximo_segun_clave(lista_jugadores, "promedio_puntos_por_partido")

            case 11:
                mensaje = solicitar_mostrar_maximo_segun_clave(lista_jugadores, "promedio_rebotes_por_partido")
        
            case 12:
                mensaje = solicitar_mostrar_maximo_segun_clave(lista_jugadores, "promedio_asistencias_por_partido")

            case 13:
                jugador_maximo = calcular_maximo_doble_clave(lista_jugadores, "estadisticas", "robos_totales")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["robos_totales"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"
                
            case 14:
                jugador_maximo = calcular_maximo_doble_clave(lista_jugadores, "estadisticas", "bloqueos_totales")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["bloqueos_totales"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"

            case 15:
                mensaje = solicitar_mostrar_maximo_segun_clave(lista_jugadores, "porcentaje_tiros_libres")
                
            case 16:
                mensaje = calcular_mostrar_clave_segun_jugador()

            case 17:
                mensaje = maxima_cantidad_logros(lista_jugadores)

            case 18:
                mensaje = solicitar_mostrar_maximo_segun_clave(lista_jugadores, "porcentaje_tiros_triples")
                
            case 19:
                jugador_maximo = calcular_maximo_doble_clave(lista_jugadores, "estadisticas", "temporadas")
                nombre_jugador_maximo = jugador_maximo["nombre"]
                valor_maximo = jugador_maximo["estadisticas"]["temporadas"]
                mensaje = f"{nombre_jugador_maximo}: {valor_maximo}"
                
            case 20:
                mensaje = solicitar_mostrar_segun_clave_ordenar_segun_posicion(lista_jugadores)

            case 23:
                ranking_jugadores = crear_lista_ordenada_segun_indice(lista_jugadores)
                datos_filas = convertir_a_texto(ranking_jugadores)
                imprimir_tabla(ranking_jugadores)
                ruta_archivo = "tabla_ranking.csv"
                guardar_archivo(ruta_archivo, datos_filas)

            case 24:
                mensaje = contador_segun_posicion(lista_jugadores)

            case 25:
                mensaje = ordenar_descendiente_segun_clave(lista_jugadores)

            case 26:
                mensaje = maximo_segun_estadisticas(lista_jugadores)

            case 27: 
                mensaje = buscar_maximo_segun_key(lista_jugadores)

            #Opcion 21: Salir
            case 21:
                break

            case _:
                mensaje = "Opcion invalida. Intente nuevamente"

        if mensaje is not None:
            imprimir_dato(mensaje)        

def main():
    #Ejecuta la app
    menu()

main()











