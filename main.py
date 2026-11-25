# menu.py
from hechos import DESCRIPCION_HECHOS
from motor_viandasv2 import MotorViandas

HECHOS_ENTRADA = ["A", "B", "C", "G", "T", "W"]


def planificar_n_dias(configuracion_dias):
    """
    Ejecuta el motor de inferencia día por día manteniendo memoria
    de los platos principales usados para evitar repeticiones.
    """
    resultados = []
    platos_usados = []

    for item in configuracion_dias:
        motor = MotorViandas()
        motor.reset()
        motor.cargar_hechos_iniciales(item["hechos"])
        motor.cargar_platos_usados(platos_usados)
        motor.run()

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


def mostrar_planificacion(resultados, mostrar_traza=False):
    """Imprime los menús recomendados por día y, opcionalmente, la traza XAI."""
    linea = "=" * 80
    print(f"\n{linea}")
    print(f"PLANIFICACIÓN DE MENÚS ({len(resultados)} DÍA/S)")
    print(linea)

    for res in resultados:
        print(f"\n>>> {res['dia'].upper()}")
        hechos_txt = ", ".join(res["hechos_iniciales"]) if res["hechos_iniciales"] else "Ninguno"
        print(f"    Condiciones iniciales: [{hechos_txt}]")

        for menu in res["menus"]:
            tipo = "MENÚ PRINCIPAL" if menu["es_principal"] else "MENÚ PARALELO"
            print(f"    • [{tipo}] ({menu['regla']}) {menu['plato']}")
            print(f"      Guarnición: {menu['guarnicion']}")
            print(f"      Categoría:  {menu['categoria']}")
            print(f"      Motivo:     {menu['motivo']}")

        if mostrar_traza:
            print(f"\n    --- Traza XAI ({len(res['traza'])} reglas operativas disparadas) ---")
            for paso in res["traza"]:
                ant = " Y ".join(paso["antecedentes"])
                cons = " Y ".join(paso["consecuentes"])
                prio = f" (salience={paso['prioridad']})" if paso["prioridad"] > 0 else ""
                print(f"      {paso['paso']:>2}. {paso['regla']}{prio}: SI {ant} -> ENTONCES {cons}")

    print(f"\n{linea}\n")


def modo_interactivo():
    """Permite elegir N días y cargar las condiciones de cada jornada."""
    while True:
        try:
            n_dias = int(input("\n¿Para cuántos días querés planificar el menú? (ej. 1 a 7): ").strip())
            if n_dias >= 1:
                break
            print("Ingresá un número mayor o igual a 1.")
        except ValueError:
            print("Por favor, ingresá un número entero válido.")

    print("\nCódigos de condiciones disponibles:")
    for cod in HECHOS_ENTRADA:
        print(f"  [{cod}] {DESCRIPCION_HECHOS[cod]}")

    configuracion = []
    for i in range(1, n_dias + 1):
        entrada = input(f"\nCondiciones para el Día {i} (separadas por espacio, o Enter si ninguna): ")
        codigos = [c.strip().upper() for c in entrada.split() if c.strip()]

        invalidos = [c for c in codigos if c not in DESCRIPCION_HECHOS]
        if invalidos:
            print(f"Error: códigos desconocidos {invalidos}. Se cancela la carga.")
            return

        configuracion.append({"dia": f"Día {i}", "hechos": codigos})

    ver_traza = input("\n¿Querés ver la traza XAI completa de reglas? (s/n): ").strip().lower() == "s"
    resultados = planificar_n_dias(configuracion)
    mostrar_planificacion(resultados, mostrar_traza=ver_traza)


def main():
    while True:
        print("\n" + "=" * 60)
        print("PRUEBAS DEL PLANIFICADOR DE MENÚS (menu.py)")
        print("=" * 60)
        print("1. Prueba 1 día: Frío + Oferta de carne (A, B, C)")
        print("2. Prueba 3 días: Frío con contingencia en el Día 2 (verifica rotación)")
        print("3. Prueba 5 días: Semana mixta (frío, contingencia, calor, restricciones)")
        print("4. Modo interactivo (elegir N días manualmente)")
        print("0. Salir")

        opcion = input("\nSeleccioná una opción: ").strip()

        if opcion == "1":
            config = [{"dia": "Día 1 (Lunes)", "hechos": ["A", "B", "C"]}]
            mostrar_planificacion(planificar_n_dias(config), mostrar_traza=True)

        elif opcion == "2":
            config = [
                {"dia": "Día 1 (Lunes)", "hechos": ["A", "B", "C"]},
                {"dia": "Día 2 (Martes - Falta ayudante)", "hechos": ["A", "B", "C", "G"]},
                {"dia": "Día 3 (Miércoles)", "hechos": ["A", "B", "C"]},
            ]
            mostrar_planificacion(planificar_n_dias(config), mostrar_traza=True)

        elif opcion == "3":
            config = [
                {"dia": "Día 1 (Lunes)", "hechos": ["A", "B", "C"]},
                {"dia": "Día 2 (Martes)", "hechos": ["A", "B", "C", "W"]},
                {"dia": "Día 3 (Miércoles - Imprevisto)", "hechos": ["A", "B", "G"]},
                {"dia": "Día 4 (Jueves - Calor)", "hechos": ["T", "W"]},
                {"dia": "Día 5 (Viernes - Calor)", "hechos": ["T"]},
            ]
            mostrar_planificacion(planificar_n_dias(config), mostrar_traza=False)

        elif opcion == "4":
            modo_interactivo()

        elif opcion == "0":
            print("Fin de las pruebas.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()