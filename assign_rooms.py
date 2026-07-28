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
    asignaciones = {}  # Diccionario que almacenará el resultado final con los pares colegial-habitación

    # Asignar habitaciones actuales
    for colegial in colegiales:
        if colegial['habitacion_actual'] in habitaciones_disponibles:
            asignaciones[colegial['id']] = colegial['habitacion_actual']
            habitaciones_disponibles.remove(colegial['habitacion_actual'])

    # Se establece el orden de preferencia de los colegiales para asignar las habitaciones
    # - Primero se ordena según el número de créditos obtenidos
    # - Segundo se ordena por número de años en el colegio
    # - Tercero se ordena de forma aleatoria en caso de empate en los dos criterios anteriores
    colegiales.sort(
        key=lambda x: (x['creditos'], x['anyo'], random.random()),
        reverse=True
    )

    # Se asignan las habitaciones según el orden de preferencia de cada colegial
    cambios = True

    # Mientras haya cambios en las asignaciones, se sigue iterando
    while cambios:
        cambios = False

        # Aquí se guardan las habitaciones abandonadas durante esta vuelta.
        # No estarán disponibles hasta que termine la vuelta.
        habitaciones_liberadas = set()

        # Se recorren los colegiales según su orden de prioridad
        for colegial in colegiales:

            # Se recorren sus preferencias en el orden indicado
            for preferencia in colegial['preferencias']:

                # Si ya tiene asignada esta preferencia, deja de buscar,
                # porque las siguientes habitaciones son opciones peores
                if colegial['id'] in asignaciones and preferencia == asignaciones[colegial['id']]:
                    break

                # Si la preferencia está disponible, se asigna
                if preferencia in habitaciones_disponibles:

                    # Si ya tenía una habitación, se guarda como liberada
                    # para que pueda utilizarse en la siguiente vuelta
                    if colegial['id'] in asignaciones:
                        habitacion_anterior = asignaciones[colegial['id']]
                        habitaciones_liberadas.add(habitacion_anterior)

                    # Se asigna la nueva habitación
                    asignaciones[colegial['id']] = preferencia

                    # La nueva habitación deja de estar disponible
                    habitaciones_disponibles.remove(preferencia)

                    # Se indica que ha habido un cambio
                    cambios = True

                    # Como ya ha conseguido una habitación, no prueba más preferencias
                    break

            # Protección por si algún colegial no tiene ninguna habitación asignada
            if colegial['id'] not in asignaciones and habitaciones_disponibles:
                asignaciones[colegial['id']] = habitaciones_disponibles.pop()

        # Las habitaciones abandonadas durante esta vuelta
        # pasan a estar disponibles para la siguiente
        habitaciones_disponibles.update(habitaciones_liberadas)

    # Se ordenan las asignaciones por habitación
    asignaciones = dict(sorted(asignaciones.items(), key=lambda item: item[1]))

    return asignaciones