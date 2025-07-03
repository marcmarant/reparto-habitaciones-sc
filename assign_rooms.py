import random
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

    # Se establece el orden de preferencia de los colegiales para asignar las habitaciones
    # - Primero se ordena segun el número de creditos obtenidos
    # - Segundo se ordena por número de años en el colegio
    # - Tercero se ordena de forma aleatoria en caso de empate en los dos anteriores criterios
    colegiales.sort(key=lambda x: (x['creditos'], x['anyo'], random.random()), reverse=True)

    # Se asignan las habitaciones segun el orden de preferencia de las habitacion para cada colegial
    cambios = True
    while cambios: # Mientras haya cambios en las asignaciones, se sigue iterando
        cambios = False
        for colegial in colegiales:
            for preferencia in colegial['preferencias']:
                # Si ya se le ha asignado su preferencia se salta
                if colegial['id'] in asignaciones and preferencia == asignaciones[colegial['id']]:
                    break
                # Si la preferencia está disponible, se asigna
                if preferencia in habitaciones_disponibles:
                    if colegial['id'] in asignaciones:
                        # Liberar la habitación actual si ya tiene una asignada
                        habitaciones_disponibles.add(asignaciones[colegial['id']])
                    asignaciones[colegial['id']] = preferencia
                    habitaciones_disponibles.remove(preferencia)
                    cambios = True
                    break
            if colegial['id'] not in asignaciones:
                asignaciones[colegial['id']] = habitaciones_disponibles.pop()

    # Se ordenan las asignaciones por habitación
    asignaciones = dict(sorted(asignaciones.items(), key=lambda item: item[1]))

    return asignaciones
