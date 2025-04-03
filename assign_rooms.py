from constants import MAX_HABITACION, MIN_HABITACION

def generate_rooms_data(lista_datos):
    """Función para asignar las habitaciones."""
    colegiales = []

    # Parseo de los datos de entrada
    for data in lista_datos:
        nombre, anyo, creditos, habitacion_actual, habitaciones_solicitadas = data.split(' - ')
        anyo = int(anyo)
        creditos = float(creditos)
        habitacion_actual = int(habitacion_actual)
        habitaciones_solicitadas = [int(h) for h in habitaciones_solicitadas.strip('[]').split(',') if h]

        if creditos > 0:
            colegiales.append({
                'id': nombre,
                'anyo': anyo,
                'creditos': creditos,
                'habitacion_actual': habitacion_actual,
                'preferencias': habitaciones_solicitadas
            })

    habitaciones_disponibles = set(range(MIN_HABITACION, MAX_HABITACION + 1))
    asignaciones = {} # Diccionario que almacenara el resultado final con los pares colegial habitacion

    # Asignar habitaciones actuales
    for colegial in colegiales:
        if colegial['habitacion_actual'] in habitaciones_disponibles:
            asignaciones[colegial['id']] = colegial['habitacion_actual']
            habitaciones_disponibles.remove(colegial['habitacion_actual'])

    # Se establece el orden de preferencia de los colegiales segun sus creditos y su numero de años en el colegio
    colegiales.sort(key=lambda x: (x['creditos'], x['anyo']), reverse=True)

    # Se asignan las habitaciones segun el orden de preferencia de las habitacion para cada colegial
    for colegial in colegiales:
        for preferencia in colegial['preferencias']:
            if preferencia in habitaciones_disponibles:
                if colegial['id'] in asignaciones:
                    habitaciones_disponibles.add(asignaciones[colegial['id']])  # Liberar la habitación actual
                asignaciones[colegial['id']] = preferencia
                habitaciones_disponibles.remove(preferencia)
                break
        if colegial['id'] not in asignaciones:
            asignaciones[colegial['id']] = habitaciones_disponibles.pop()

    return asignaciones
