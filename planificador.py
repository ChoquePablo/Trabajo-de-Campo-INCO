# planificador.py
from motor_viandasv2 import MotorViandas


def planificar_n_dias(configuracion_dias):
    """
    configuracion_dias: lista de diccionarios, uno por cada día elegido.
    Ejemplo:
        [
            {"dia": "Día 1 (Lunes)", "hechos": ["A", "B", "C"]},
            {"dia": "Día 2 (Martes)", "hechos": ["A", "B", "C", "G"]},
        ]
    """
    resultados = []
    platos_usados = []

    for item in configuracion_dias:
        motor = MotorViandas()
        motor.reset()
        motor.cargar_hechos_iniciales(item["hechos"])
        motor.cargar_platos_usados(platos_usados)
        motor.run()

        # Registrar el plato principal elegido hoy para no repetirlo en los siguientes días
        for menu in motor.menus_sugeridos:
            if menu["es_principal"]:
                platos_usados.append(menu["plato"])

        resultados.append({
            "dia": item["dia"],
            "hechos_iniciales": motor.hechos_iniciales,
            "menus": motor.menus_sugeridos,
            "traza": motor.traza,
        })

    return resultados