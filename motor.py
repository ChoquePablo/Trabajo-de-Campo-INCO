import collections
import collections.abc
import json
import os

# Parche de compatibilidad para Experta en Python 3.10+
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

from experta import *

ARCHIVO_APRENDIZAJE = os.path.join(os.path.dirname(__file__), "conocimiento_aprendido.json")

# Catálogo completo de hechos del dominio (Base de Hechos)
DESCRIPCION_HECHOS = {
    "A": "Es Lunes, Martes o Miércoles",
    "B": "Hay oferta de cortes de carne (pieza entera) en el frigorífico",
    "C": "El clima es frío",
    "D": "Se compra la pieza de carne entera",
    "E": "Se clasifica como un ingrediente versátil",
    "F": "Se planifican al menos dos platos diferentes (ej. guiso y bifes)",
    "G": "La ayudante de cocina avisa que no asiste",
    "H": "La cocina, espacios y ollas NO están limpios a primera hora",
    "I": "Se retrasa el inicio de la elaboración (Lucía debe limpiar sola)",
    "J": "El menú planificado requiere demasiado tiempo de elaboración relativo",
    "K": "Se descarta el menú diario estándar (ej. el guiso)",
    "L": "Se activa el protocolo de contingencia por imprevisto/demora",
    "M": "Se congela la carne un poco para filetear y reducir desperdicios",
    "N": "Se filetea la carne en la cocina",
    "O": "Se preparan minutas de cocción rápida",
    "P": "Se necesita preparar arroz para tener de reserva en la heladera",
    "Q": "No se le agrega cebolla ni verduras frescas al arroz",
    "R": "El margen de ganancia aumenta",
    "S": "El cliente recibe el menú rápido y no se echa a perder la guarnición",
    "T": "El clima es cálido / verano",
    "U": "Se descartan menús calientes",
    "V": "Se sugieren comidas frescas",
    "W": "El cliente tiene restricciones alimentarias",
    "Y": "Se prepara menú paralelo básico",
    "Z": "Se ofrece un plato de entrada rápido (sopa)",
    "AA": "Se sugiere al cliente agendar el número para reservar por mensaje",
    "AB": "Se enciende la plancha o freidora de forma anticipada",
    "AC": "Se inicia una charla con el cliente para distraerlo mientras se cocina",
    "AD": "Se planifica un plato de olla de alto volumen (ej. Locro)",
    "AE": "Se ocupan todas las hornallas de la cocina simultáneamente",
    "AF": "Se observa el precio de los vegetales en el mercado",
    "AG": "Se compra y reserva esa verdura si el precio es bajo",
    "AH": "Se deshuesa/prepara una parte para el menú actual (ej. pechuga para suprema)",
    "AI": "Se guarda otra parte de la pieza para el menú del día siguiente (ej. cuartos traseros)",
    "AJ": "Aumenta la demanda de platos de olla (guisos, lentejas, locro)",
    "AK": "Se descartan las comidas frías o la milanesa estándar como menú principal",
    "AL": "Se utiliza equipamiento de gran volumen (ollas grandes)",
    "AM": "Se calcula un rendimiento masivo (entre 50 y 70 platos por preparación)",
    "AO": "Se aprovechan cortes de oferta con hueso específicos para caldos (ej. osobuco/puchero)",
}


# Conjunto inmutable de códigos de hechos originales de la Actividad 4
HECHOS_BASE_ORIGINALES = frozenset(DESCRIPCION_HECHOS.keys())


# ========================================================
# PERSISTENCIA DE APRENDIZAJE CONTINUO
# ========================================================
def cargar_conocimiento_aprendido():
    """Carga los hechos, reglas y platos aprendidos dinámicamente desde disco."""
    if not os.path.exists(ARCHIVO_APRENDIZAJE):
        return {"hechos_personalizados": {}, "reglas_platos": []}
    try:
        with open(ARCHIVO_APRENDIZAJE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "hechos_personalizados" not in data:
                data["hechos_personalizados"] = {}
            if "reglas_platos" not in data:
                data["reglas_platos"] = []
            return data
    except Exception:
        return {"hechos_personalizados": {}, "reglas_platos": []}


def sincronizar_reglas_aprendidas_en_codigo(data):
    """
    Escribe o actualiza físicamente las reglas @Rule de los platos aprendidos
    dentro del código fuente de motor.py (entre los marcadores de bloque),
    para que cada plato agregado quede establecido como una regla real en el código.
    """
    ruta_motor = os.path.abspath(__file__)
    if not os.path.exists(ruta_motor):
        return

    with open(ruta_motor, "r", encoding="utf-8") as f:
        codigo = f.read()

    marcador_ini = "    # [" + "INICIO_REGLAS_APRENDIDAS_CODIGO]"
    marcador_fin = "    # [" + "FIN_REGLAS_APRENDIDAS_CODIGO]"
    if marcador_ini not in codigo or marcador_fin not in codigo:
        return

    lineas_bloque = [marcador_ini]
    reglas = data.get("reglas_platos", [])
    if not reglas:
        lineas_bloque.append("    # (Cuando agregues un plato en la Opción 5, su regla @Rule se escribirá aquí automáticamente)")
    else:
        for r in reglas:
            rid = r["id"]
            fn_name = f"{rid.lower()}_plato_aprendido"
            cond = r["condicion_codigo"]
            plato = r["nombre_plato"]
            guarnicion = r["descripcion_plato"]
            cat = f"{r['categoria']} (Aprendido)"
            motivo = f"Condición [{cond}] ({r['condicion_descripcion']})"
            tiempo = r.get("tiempo_estimado", "25 min")
            tip = r.get("consejo_cocina") or motivo

            lineas_bloque.append("")
            lineas_bloque.append(f"    @Rule(Hecho(codigo={json.dumps(cond, ensure_ascii=False)}), salience=-25)")
            lineas_bloque.append(f"    def {fn_name}(self):")
            lineas_bloque.append("        self._recomendar_menu(")
            lineas_bloque.append(f"            {json.dumps(rid, ensure_ascii=False)},")
            lineas_bloque.append(f"            plato={json.dumps(plato, ensure_ascii=False)},")
            lineas_bloque.append(f"            guarnicion={json.dumps(guarnicion, ensure_ascii=False)},")
            lineas_bloque.append(f"            categoria={json.dumps(cat, ensure_ascii=False)},")
            lineas_bloque.append(f"            motivo={json.dumps(motivo, ensure_ascii=False)},")
            lineas_bloque.append("            es_principal=False,")
            lineas_bloque.append('            icono="sparkle",')
            lineas_bloque.append(f"            tiempo={json.dumps(tiempo, ensure_ascii=False)},")
            lineas_bloque.append('            rendimiento="Personalizado por Lucía",')
            lineas_bloque.append(f"            tip={json.dumps(tip, ensure_ascii=False)},")
            lineas_bloque.append("            prioridad=-25,")
            lineas_bloque.append("        )")

    lineas_bloque.append(marcador_fin)
    nuevo_bloque = "\n".join(lineas_bloque)

    idx_ini = codigo.rindex(marcador_ini)
    idx_fin = codigo.rindex(marcador_fin) + len(marcador_fin)
    nuevo_codigo = codigo[:idx_ini] + nuevo_bloque + codigo[idx_fin:]

    with open(ruta_motor, "w", encoding="utf-8") as f:
        f.write(nuevo_codigo)


def guardar_nuevo_aprendizaje(
    condicion_codigo,
    condicion_descripcion,
    es_hecho_nuevo,
    nombre_plato,
    categoria,
    descripcion_plato,
    tiempo_estimado,
    consejo_cocina,
):
    """Guarda un nuevo hecho y/o regla de recomendación de plato en la base aprendida y escribe la @Rule en motor.py."""
    data = cargar_conocimiento_aprendido()
    codigo_cond = (condicion_codigo or "C").strip().upper()

    # Proteger los hechos base A-AO para que nunca sean sobreescritos como personalizados
    if es_hecho_nuevo and codigo_cond and codigo_cond not in HECHOS_BASE_ORIGINALES:
        desc_limpia = condicion_descripcion.strip() or f"Condición personalizada {codigo_cond}"
        data["hechos_personalizados"][codigo_cond] = desc_limpia

    # Calcular ID incremental único que nunca se reutilice aunque se hayan borrado todas las reglas
    max_num = int(data.get("ultimo_id_num", 0))
    for r in data["reglas_platos"]:
        rid = r.get("id", "")
        if rid.startswith("RA") and rid[2:].isdigit():
            max_num = max(max_num, int(rid[2:]))
    nuevo_idx = max_num + 1
    data["ultimo_id_num"] = nuevo_idx
    regla_id = f"RA{nuevo_idx}"

    catalogo = obtener_catalogo_hechos_completo()
    desc_final = catalogo.get(codigo_cond) or data["hechos_personalizados"].get(codigo_cond) or condicion_descripcion.strip()

    nueva_regla = {
        "id": regla_id,
        "condicion_codigo": codigo_cond,
        "condicion_descripcion": desc_final,
        "nombre_plato": nombre_plato.strip(),
        "categoria": categoria,
        "descripcion_plato": descripcion_plato.strip(),
        "tiempo_estimado": tiempo_estimado.strip() or "25 min",
        "consejo_cocina": consejo_cocina.strip(),
    }
    data["reglas_platos"].append(nueva_regla)

    with open(ARCHIVO_APRENDIZAJE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    sincronizar_reglas_aprendidas_en_codigo(data)
    return nueva_regla


def eliminar_regla_aprendida(regla_id):
    """Elimina una regla aprendida por su ID (o todas si regla_id == 'TODAS'), limpia hechos huérfanos y actualiza motor.py."""
    data = cargar_conocimiento_aprendido()
    if regla_id == "TODAS":
        data["reglas_platos"] = []
        data["hechos_personalizados"] = {}
    else:
        data["reglas_platos"] = [r for r in data["reglas_platos"] if r.get("id") != regla_id]
        codigos_en_uso = {r.get("condicion_codigo") for r in data["reglas_platos"]}
        data["hechos_personalizados"] = {
            k: v for k, v in data.get("hechos_personalizados", {}).items() if k in codigos_en_uso
        }
    with open(ARCHIVO_APRENDIZAJE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    sincronizar_reglas_aprendidas_en_codigo(data)


def obtener_catalogo_hechos_completo():
    """Devuelve DESCRIPCION_HECHOS fusionado únicamente con los hechos de condición aprendidos (sin códigos PL_X fantasma)."""
    catalogo = dict(DESCRIPCION_HECHOS)
    aprendido = cargar_conocimiento_aprendido()
    catalogo.update(aprendido.get("hechos_personalizados", {}))
    return catalogo


class Hecho(Fact):
    """Clase base que representa los hechos en la memoria de trabajo."""
    pass


class MenuSugerido(Fact):
    """Representa un plato concreto recomendado por una regla del motor."""
    pass


class PlatoUsado(Fact):
    """Registra platos ya asignados anteriormente para evitar repeticiones (rotación)."""
    pass


class MenuPrincipalDefinido(Fact):
    """Bandera en memoria de trabajo para asegurar la selección del plato principal según salience."""
    pass


class AsesorVirtualGastronomico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.traza = []            # Explicabilidad (XAI): cadena de reglas disparadas
        self.recomendaciones = []  # Acciones concretas para mostrar a Lucía
        self.menus_sugeridos = []  # Platos recomendados formalmente por reglas R33-R43
        self.platos_aprendidos_disparados = []

    def reset(self, **kwargs):
        """Limpia las listas cada vez que se reinicia el motor."""
        super().reset(**kwargs)
        self.traza = []
        self.recomendaciones = []
        self.menus_sugeridos = []
        self.platos_aprendidos_disparados = []

    def cargar_platos_usados(self, platos):
        """Declara en la memoria de trabajo los platos ya usados para que las reglas R33-R43 roten el menú."""
        for plato in (platos or []):
            self.declare(PlatoUsado(plato=plato))

    def _recomendar_menu(
        self,
        regla_id,
        plato,
        guarnicion,
        categoria,
        motivo,
        es_principal=True,
        icono="utensils",
        tiempo="25 min",
        rendimiento="35 a 45 viandas",
        tip="",
        prioridad=0,
    ):
        """Declara formalmente el hecho MenuSugerido en el motor Experta y lo registra en la traza XAI."""
        self.declare(MenuSugerido(plato=plato, guarnicion=guarnicion, categoria=categoria))
        if es_principal:
            self.declare(MenuPrincipalDefinido())

        tipo_label = "MENÚ PRINCIPAL" if es_principal else "MENÚ COMPLEMENTARIO / PARALELO"
        prio_txt = f" (salience={prioridad})" if prioridad != 0 else ""
        self.registrar_paso(
            regla=f"{regla_id}{prio_txt}",
            explicacion=f"{motivo} -> Decide [{tipo_label}]: '{plato}' con {guarnicion}.",
            recomendacion=f"[{tipo_label} - {regla_id}] Preparar {plato} acompañado de {guarnicion}.",
        )

        self.menus_sugeridos.append(
            {
                "regla": regla_id,
                "plato": plato,
                "guarnicion": guarnicion,
                "categoria": categoria,
                "motivo": motivo,
                "es_principal": es_principal,
                "nombre": f"{plato} — {guarnicion}" if guarnicion else plato,
                "icono": icono,
                "tiempo": tiempo,
                "rendimiento": rendimiento,
                "descripcion": f"Plato: {plato}. Guarnición: {guarnicion}. ({motivo})",
                "tip": tip or motivo,
                "regla_origen": regla_id,
            }
        )

    def registrar_paso(self, regla, explicacion, recomendacion):
        """Método auxiliar para registrar la traza XAI y la recomendación."""
        self.traza.append(f"[{regla}] {explicacion}")
        self.recomendaciones.append(recomendacion)

    def obtener_hechos_finales(self):
        """Devuelve la lista limpia de códigos de hechos en la memoria de trabajo (sin códigos PL_X artificiales)."""
        catalogo_valido = obtener_catalogo_hechos_completo()
        return [
            fact["codigo"]
            for fact in self.facts.values()
            if "codigo" in fact and fact["codigo"] in catalogo_valido
        ]

    def run(self, steps=None):
        """Ejecuta el motor Experta y las reglas aprendidas (sin crear hechos PL_X fantasma en la memoria de trabajo)."""
        if steps is None:
            super().run()
        else:
            super().run(steps)

        # Evaluar reglas aprendidas que aún no se hayan disparado como @Rule en esta sesión
        aprendido = cargar_conocimiento_aprendido()
        hechos_actuales = set(self.obtener_hechos_finales())
        reglas_ya_disparadas = {m["regla"] for m in self.menus_sugeridos}

        for regla in aprendido.get("reglas_platos", []):
            rid = regla["id"]
            cond = regla["condicion_codigo"]
            if cond in hechos_actuales and rid not in reglas_ya_disparadas:
                self._recomendar_menu(
                    rid,
                    plato=regla["nombre_plato"],
                    guarnicion=regla["descripcion_plato"],
                    categoria=f"{regla['categoria']} (Aprendido)",
                    motivo=f"Condición [{cond}] ({regla['condicion_descripcion']})",
                    es_principal=False,
                    icono="sparkle",
                    tiempo=regla.get("tiempo_estimado", "25 min"),
                    rendimiento="Personalizado por Lucía",
                    tip=regla.get("consejo_cocina") or f"Activado por condición {cond}.",
                    prioridad=-25,
                )
                reglas_ya_disparadas.add(rid)

    # ========================================================
    # RAMA 1: INICIO DE SEMANA Y OFERTA DE CARNE (A + B -> D)
    # ========================================================

    @Rule(Hecho(codigo="A"), Hecho(codigo="B"))
    def r1_comprar_pieza_entera(self):
        self.registrar_paso(
            regla="R1",
            explicacion="Hechos A (Lun-Mié) + B (Oferta carne) -> Genera Hecho D (Comprar pieza entera).",
            recomendacion="Comprar la pieza de carne entera aprovechando la oferta del frigorífico.",
        )
        self.declare(Hecho(codigo="D"))

    @Rule(Hecho(codigo="D"), salience=20)
    def r2_clasificar_versatil(self):
        self.registrar_paso(
            regla="R2",
            explicacion="Hecho D (Pieza entera) -> Genera Hecho E (Ingrediente versátil).",
            recomendacion="Clasificar la pieza comprada como ingrediente versátil para múltiples preparaciones.",
        )
        self.declare(Hecho(codigo="E"))

    @Rule(Hecho(codigo="D"), salience=10)
    def r9_congelar_para_filetear(self):
        self.registrar_paso(
            regla="R9",
            explicacion="Hecho D (Pieza entera) -> Genera Hecho M (Congelar ligeramente para filetear).",
            recomendacion="Congelar un poco la carne antes de cortarla para facilitar el fileteado y reducir desperdicios.",
        )
        self.declare(Hecho(codigo="M"))

    @Rule(Hecho(codigo="M"))
    def r10_filetear_carne(self):
        self.registrar_paso(
            regla="R10",
            explicacion="Hecho M (Carne semicongelada) -> Genera Hecho N (Filetear en cocina).",
            recomendacion="Filetear la pieza de carne directamente en la cocina.",
        )
        self.declare(Hecho(codigo="N"))

    @Rule(Hecho(codigo="N"))
    def r14_aumentar_margen(self):
        self.registrar_paso(
            regla="R14",
            explicacion="Hecho N (Fileteado propio) -> Genera Hecho R (Aumenta margen de ganancia).",
            recomendacion="Aprovechar el rinde del fileteado propio: el margen de ganancia del día aumenta.",
        )
        self.declare(Hecho(codigo="R"))

    # ========================================================
    # CONFLICTO: E (Ingrediente versátil)
    # Orden de ejecución: R3 -> R26
    # ========================================================

    @Rule(Hecho(codigo="E"), salience=20)
    def r3_planificar_dos_platos(self):
        self.registrar_paso(
            regla="R3",
            explicacion="Hecho E (Ingrediente versátil) -> Genera Hecho F (Planificar al menos 2 platos).",
            recomendacion="Planificar al menos dos platos diferentes con la misma pieza (ej. guiso y bifes).",
        )
        self.declare(Hecho(codigo="F"))

    @Rule(Hecho(codigo="E"), salience=10)
    def r26_fraccionar_pieza(self):
        self.registrar_paso(
            regla="R26",
            explicacion="Hecho E (Ingrediente versátil) -> Genera Hechos AH (Parte menú actual) + AI (Guardar parte día siguiente).",
            recomendacion="Deshuesar/preparar una parte para el menú actual (ej. pechuga para suprema) y guardar otra parte para el día siguiente (ej. cuartos traseros).",
        )
        self.declare(Hecho(codigo="AH"))
        self.declare(Hecho(codigo="AI"))

    # ========================================================
    # RAMA 2: AUSENCIA DE AYUDANTE Y RETRASO (G -> H -> I)
    # ========================================================

    @Rule(Hecho(codigo="G"))
    def r4_cocina_no_limpia(self):
        self.registrar_paso(
            regla="R4",
            explicacion="Hecho G (Falta ayudante) -> Genera Hecho H (Cocina y ollas sin limpiar a primera hora).",
            recomendacion="Verificar y acondicionar la cocina, mesadas y ollas antes de comenzar (no están listas a primera hora).",
        )
        self.declare(Hecho(codigo="H"))

    @Rule(Hecho(codigo="H"))
    def r5_retraso_elaboracion(self):
        self.registrar_paso(
            regla="R5",
            explicacion="Hecho H (Cocina sin limpiar) -> Genera Hecho I (Retraso en inicio de elaboración).",
            recomendacion="Reorganizar tiempos: se retrasa el inicio de la elaboración porque Lucía debe limpiar sola.",
        )
        self.declare(Hecho(codigo="I"))

    # ========================================================
    # CONVERGENCIA A CONTINGENCIA: F + I -> J -> K -> L
    # ========================================================

    @Rule(Hecho(codigo="F"), Hecho(codigo="I"))
    def r6_tiempo_insuficiente(self):
        self.registrar_paso(
            regla="R6",
            explicacion="Hechos F (2+ platos) + I (Retraso) -> Genera Hecho J (Menú requiere demasiado tiempo).",
            recomendacion="Evaluar tiempos críticos: el menú planificado requiere demasiado tiempo frente al retraso acumulado.",
        )
        self.declare(Hecho(codigo="J"))

    @Rule(Hecho(codigo="J"))
    def r7_descartar_menu_estandar(self):
        self.registrar_paso(
            regla="R7",
            explicacion="Hecho J (Tiempo excesivo) -> Genera Hecho K (Descartar menú diario estándar).",
            recomendacion="Descartar el menú diario estándar de cocción larga (ej. el guiso).",
        )
        self.declare(Hecho(codigo="K"))

    @Rule(Hecho(codigo="K"))
    def r8_activar_contingencia(self):
        self.registrar_paso(
            regla="R8",
            explicacion="Hecho K (Menú descartado) -> Genera Hecho L (Activar protocolo de contingencia).",
            recomendacion="Activar el protocolo de contingencia por imprevisto/demora.",
        )
        self.declare(Hecho(codigo="L"))

    # ========================================================
    # CONFLICTO: L (Contingencia por demora)
    # Orden de ejecución: R12 -> R11 -> R18 -> R19
    # ========================================================

    @Rule(Hecho(codigo="L"), salience=40)
    def r12_preparar_arroz(self):
        self.registrar_paso(
            regla="R12",
            explicacion="Hecho L (Contingencia por demora) -> Genera Hecho P (Preparar arroz de reserva).",
            recomendacion="Preparar arroz blanco de reserva para tener disponible en la heladera.",
        )
        self.declare(Hecho(codigo="P"))

    @Rule(Hecho(codigo="L"), salience=30)
    def r11_preparar_minutas(self):
        self.registrar_paso(
            regla="R11",
            explicacion="Hecho L (Contingencia por demora) -> Genera Hecho O (Minutas rápidas).",
            recomendacion="Activar preparación de minutas de cocción rápida (milanesas, bifes, costeletas).",
        )
        self.declare(Hecho(codigo="O"))

    @Rule(Hecho(codigo="L"), salience=20)
    def r18_ofrecer_sopa(self):
        self.registrar_paso(
            regla="R18",
            explicacion="Hecho L (Contingencia por demora) -> Genera Hecho Z (Plato de entrada rápido).",
            recomendacion="Ofrecer un plato de entrada rápido (sopa) mientras sale el plato principal.",
        )
        self.declare(Hecho(codigo="Z"))

    @Rule(Hecho(codigo="L"), salience=10)
    def r19_sugerir_reservas(self):
        self.registrar_paso(
            regla="R19",
            explicacion="Hecho L (Contingencia por demora) -> Genera Hecho AA (Reservas por mensaje).",
            recomendacion="Sugerir al cliente agendar el número para reservar su vianda por mensaje en el futuro.",
        )
        self.declare(Hecho(codigo="AA"))

    # ========================================================
    # ENCADENAMIENTO DEL ARROZ (P -> Q)
    # ========================================================

    @Rule(Hecho(codigo="P"))
    def r13_arroz_sin_verduras(self):
        self.registrar_paso(
            regla="R13",
            explicacion="Hecho P (Arroz de reserva) -> Genera Hecho Q (Sin cebolla ni verduras frescas).",
            recomendacion="Cocinar el arroz sin cebolla ni verduras frescas para que se conserve sin echarse a perder.",
        )
        self.declare(Hecho(codigo="Q"))

    # ========================================================
    # CONFLICTO: O (Minutas de cocción rápida)
    # Orden de ejecución: R20 -> R15
    # ========================================================

    @Rule(Hecho(codigo="O"), salience=20)
    def r20_encender_plancha(self):
        self.registrar_paso(
            regla="R20",
            explicacion="Hecho O (Minutas en marcha) -> Genera Hecho AB (Encender plancha/freidora).",
            recomendacion="Encender la plancha o freidora de forma anticipada.",
        )
        self.declare(Hecho(codigo="AB"))

    @Rule(Hecho(codigo="O"), Hecho(codigo="Q"), salience=10)
    def r15_entrega_menu_rapido(self):
        self.registrar_paso(
            regla="R15",
            explicacion="Hechos O + Q (Minutas + Arroz listo) -> Genera Hecho S (Entrega exitosa).",
            recomendacion="Entregar el menú rápido con su guarnición lista al cliente sin riesgo de que se eche a perder.",
        )
        self.declare(Hecho(codigo="S"))

    # ========================================================
    # ENCADENAMIENTO DE LA PLANCHA (AB -> AC)
    # ========================================================

    @Rule(Hecho(codigo="AB"))
    def r21_charla_cliente(self):
        self.registrar_paso(
            regla="R21",
            explicacion="Hecho AB (Plancha encendida) -> Genera Hecho AC (Charla con el cliente).",
            recomendacion="Iniciar una charla con el cliente para distraerlo y ganar tiempo mientras se cocina.",
        )
        self.declare(Hecho(codigo="AC"))

    # ========================================================
    # RAMA 3: CLIMA CÁLIDO / VERANO (T -> U + V)
    # ========================================================

    @Rule(Hecho(codigo="T"))
    def r16_clima_calido(self):
        self.registrar_paso(
            regla="R16",
            explicacion="Hecho T (Clima cálido/verano) -> Genera Hechos U (Descartar menús calientes) + V (Sugerir comidas frescas).",
            recomendacion="Descartar menús calientes pesados y sugerir comidas frescas acordes al verano.",
        )
        self.declare(Hecho(codigo="U"))
        self.declare(Hecho(codigo="V"))

    # ========================================================
    # RAMA 4: CLIMA FRÍO (C)
    # Conflicto en C -> Orden: R27 -> R22 -> R31
    # ========================================================

    @Rule(Hecho(codigo="C"), salience=30)
    def r27_demanda_platos_olla(self):
        self.registrar_paso(
            regla="R27",
            explicacion="Hecho C (Clima frío) -> Genera Hecho AJ (Aumenta demanda de platos de olla).",
            recomendacion="Anticipar mayor demanda de platos de olla (guisos, lentejas, locro).",
        )
        self.declare(Hecho(codigo="AJ"))

    @Rule(Hecho(codigo="C"), salience=20)
    def r22_planificar_plato_masivo(self):
        self.registrar_paso(
            regla="R22",
            explicacion="Hecho C (Clima frío) -> Genera Hecho AD (Planificar plato de olla masivo).",
            recomendacion="Planificar un plato de olla de alto volumen (ej. Locro).",
        )
        self.declare(Hecho(codigo="AD"))

    @Rule(Hecho(codigo="C"), salience=10)
    def r31_comprar_cortes_caldo(self):
        self.registrar_paso(
            regla="R31",
            explicacion="Hecho C (Clima frío) -> Genera Hecho AO (Aprovechar cortes con hueso en oferta).",
            recomendacion="Aprovechar cortes de oferta con hueso específicos para caldos y sopas (ej. osobuco o puchero).",
        )
        self.declare(Hecho(codigo="AO"))

    @Rule(Hecho(codigo="AD"))
    def r23_ocupar_hornallas(self):
        self.registrar_paso(
            regla="R23",
            explicacion="Hecho AD (Plato de olla masivo) -> Genera Hecho AE (Ocupar todas las hornallas).",
            recomendacion="Organizar la cocina previendo que se ocuparán todas las hornallas simultáneamente.",
        )
        self.declare(Hecho(codigo="AE"))

    # ========================================================
    # CONFLICTO: AJ (Aumenta demanda de platos de olla)
    # Orden de ejecución: R28 -> R29
    # ========================================================

    @Rule(Hecho(codigo="AJ"), salience=20)
    def r28_descartar_frias_milanesa(self):
        self.registrar_paso(
            regla="R28",
            explicacion="Hecho AJ (Alta demanda de olla) -> Genera Hecho AK (Descartar frías y milanesa estándar).",
            recomendacion="Descartar las comidas frías o la milanesa estándar como menú principal del día.",
        )
        self.declare(Hecho(codigo="AK"))

    @Rule(Hecho(codigo="AJ"), salience=10)
    def r29_usar_ollas_grandes(self):
        self.registrar_paso(
            regla="R29",
            explicacion="Hecho AJ (Alta demanda de olla) -> Genera Hecho AL (Equipamiento de gran volumen).",
            recomendacion="Preparar y utilizar equipamiento de gran volumen (ollas grandes).",
        )
        self.declare(Hecho(codigo="AL"))

    @Rule(Hecho(codigo="AL"))
    def r30_rendimiento_masivo(self):
        self.registrar_paso(
            regla="R30",
            explicacion="Hecho AL (Ollas grandes) -> Genera Hecho AM (Rendimiento de 50 a 70 platos).",
            recomendacion="Calcular un rendimiento masivo estimado de entre 50 y 70 platos por preparación.",
        )
        self.declare(Hecho(codigo="AM"))

    # ========================================================
    # RAMA 5: CLIENTE CON RESTRICCIONES ALIMENTARIAS (W)
    # ========================================================

    @Rule(Hecho(codigo="W"), salience=20)
    def r17_menu_paralelo(self):
        self.registrar_paso(
            regla="R17",
            explicacion="Hecho W (Restricciones alimentarias) -> Genera Hecho Y (Menú paralelo básico).",
            recomendacion="Preparar un menú paralelo básico adaptado a las restricciones del cliente.",
        )
        self.declare(Hecho(codigo="Y"))

    @Rule(Hecho(codigo="W"), salience=10)
    def r24_observar_precio_vegetales(self):
        self.registrar_paso(
            regla="R24",
            explicacion="Hecho W (Restricciones alimentarias) -> Genera Hecho AF (Observar precio de vegetales).",
            recomendacion="Monitorear el precio de vegetales clave (ej. espinaca) en el mercado.",
        )
        self.declare(Hecho(codigo="AF"))

    @Rule(Hecho(codigo="AF"))
    def r25_comprar_verdura_economica(self):
        self.registrar_paso(
            regla="R25",
            explicacion="Hecho AF (Monitoreo de mercado) -> Genera Hecho AG (Comprar y reservar si el precio es bajo).",
            recomendacion="Comprar y reservar la verdura si el precio es bajo para asegurar la vianda especial.",
        )
        self.declare(Hecho(codigo="AG"))

    # ========================================================
    # CAPA DE REGLAS DE RECOMENDACIÓN DE PLATOS (R33 - R43)
    # Adaptadas de ramaAriel (salience < 0): se evalúan al finalizar
    # la inferencia operativa para decidir los platos del menú.
    # ========================================================

    # --- 1. Contingencia / Minutas rápidas (si hubo demora L o falta de ayudante G/I -> O y Q) ---

    @Rule(
        OR(
            AND(Hecho(codigo="O"), Hecho(codigo="Q")),
            AND(Hecho(codigo="I"), NOT(Hecho(codigo="O"))),
        ),
        NOT(MenuPrincipalDefinido()),
        NOT(PlatoUsado(plato="Milanesas (carne/pollo)")),
        salience=-10,
    )
    def r33_menu_contingencia_milanesas(self):
        self._recomendar_menu(
            "R33",
            plato="Milanesas (carne/pollo)",
            guarnicion="Arroz blanco de reserva (sin verduras)",
            categoria="Minuta / Contingencia",
            motivo="Contingencia o retraso en cocina [L/O/I] y arroz de reserva disponible [Q].",
            es_principal=True,
            icono="utensils",
            tiempo="12 - 15 min",
            rendimiento="Al instante / A demanda",
            tip="Encender plancha/freidora anticipadamente (R20) y usar arroz sin verduras (R13) para que no fermente.",
            prioridad=-10,
        )

    @Rule(
        OR(
            AND(Hecho(codigo="O"), Hecho(codigo="Q")),
            AND(Hecho(codigo="I"), NOT(Hecho(codigo="O"))),
        ),
        NOT(MenuPrincipalDefinido()),
        NOT(PlatoUsado(plato="Bifes a la plancha o Costeletas")),
        salience=-11,
    )
    def r34_menu_contingencia_bifes(self):
        self._recomendar_menu(
            "R34",
            plato="Bifes a la plancha o Costeletas",
            guarnicion="Arroz blanco de reserva (sin verduras)",
            categoria="Minuta / Contingencia",
            motivo="Contingencia activa [L/O/I] rotando plato rápido para no repetir.",
            es_principal=True,
            icono="utensils",
            tiempo="15 min",
            rendimiento="Salida inmediata",
            tip="Ideal para despachar rápido mientras se conversa con el cliente en mostrador (R21).",
            prioridad=-11,
        )

    # --- 2. Clima frío sin contingencia ni retraso (platos de olla) ---

    @Rule(
        Hecho(codigo="C"),
        Hecho(codigo="AO"),
        NOT(Hecho(codigo="L")),
        NOT(Hecho(codigo="I")),
        NOT(MenuPrincipalDefinido()),
        NOT(PlatoUsado(plato="Puchero")),
        salience=-10,
    )
    def r35_menu_frio_puchero(self):
        self._recomendar_menu(
            "R35",
            plato="Puchero",
            guarnicion="Caldo y verduras de olla",
            categoria="Clima Frío (Olla)",
            motivo="Clima frío [C] y cortes con hueso en oferta [AO] sin demoras.",
            es_principal=True,
            icono="soup",
            tiempo="70 min",
            rendimiento="50 a 70 porciones (Olla grande)",
            tip="Excelente margen de ganancia aprovechando ofertas de cortes con hueso para días fríos (R31).",
            prioridad=-10,
        )

    @Rule(
        Hecho(codigo="AD"),
        Hecho(codigo="D"),
        NOT(Hecho(codigo="L")),
        NOT(Hecho(codigo="I")),
        NOT(MenuPrincipalDefinido()),
        NOT(PlatoUsado(plato="Guiso de lentejas o carne")),
        salience=-11,
    )
    def r36_menu_frio_guiso(self):
        self._recomendar_menu(
            "R36",
            plato="Guiso de lentejas o carne",
            guarnicion="Plato único de olla (rendimiento masivo)",
            categoria="Clima Frío (Olla)",
            motivo="Clima frío [AD] aprovechando pieza entera de carne [D].",
            es_principal=True,
            icono="flame",
            tiempo="60 - 75 min",
            rendimiento="50 a 70 porciones (Olla grande)",
            tip="Alta demanda asegurada en días fríos; priorizar por sobre minutas o platos fríos (R27 + R28).",
            prioridad=-11,
        )

    @Rule(
        Hecho(codigo="AD"),
        NOT(Hecho(codigo="L")),
        NOT(Hecho(codigo="I")),
        NOT(MenuPrincipalDefinido()),
        NOT(PlatoUsado(plato="Locro")),
        salience=-12,
    )
    def r37_menu_frio_locro(self):
        self._recomendar_menu(
            "R37",
            plato="Locro",
            guarnicion="Plato único de olla grande",
            categoria="Clima Frío (Olla)",
            motivo="Clima frío [AD] con rotación de menú de alto rendimiento.",
            es_principal=True,
            icono="flame",
            tiempo="90 - 120 min",
            rendimiento="50 a 70 porciones (Olla grande)",
            tip="Usar equipamiento de gran volumen (R29) y prever la ocupación de todas las hornallas simultáneamente (R23).",
            prioridad=-12,
        )

    @Rule(
        Hecho(codigo="AJ"),
        NOT(Hecho(codigo="L")),
        NOT(Hecho(codigo="I")),
        NOT(MenuPrincipalDefinido()),
        NOT(PlatoUsado(plato="Albóndigas o Pastas a la boloñesa")),
        salience=-13,
    )
    def r38_menu_frio_albondigas(self):
        self._recomendar_menu(
            "R38",
            plato="Albóndigas o Pastas a la boloñesa",
            guarnicion="Puré o fideos",
            categoria="Clima Frío",
            motivo="Alta demanda de platos calientes [AJ] rotando opción sin repetir.",
            es_principal=True,
            icono="flame",
            tiempo="45 min",
            rendimiento="40 a 50 porciones",
            tip="Alternativa caliente de alto rendimiento cuando ya se rotaron Puchero, Guiso y Locro.",
            prioridad=-13,
        )

    # --- 3. Clima cálido sin contingencia ---

    @Rule(
        Hecho(codigo="V"),
        NOT(Hecho(codigo="L")),
        NOT(Hecho(codigo="I")),
        NOT(MenuPrincipalDefinido()),
        NOT(PlatoUsado(plato="Milanesas con ensalada")),
        salience=-10,
    )
    def r39_menu_calido_milanesas(self):
        self._recomendar_menu(
            "R39",
            plato="Milanesas con ensalada",
            guarnicion="Ensalada de espinaca y huevo / frescas",
            categoria="Clima Cálido",
            motivo="Clima cálido [T/V]: se descartan guisos y se sugieren platos frescos.",
            es_principal=True,
            icono="leaf",
            tiempo="20 min",
            rendimiento="25 a 35 viandas",
            tip="Reemplaza los guisos calientes en jornadas de calor (R16).",
            prioridad=-10,
        )

    @Rule(
        Hecho(codigo="V"),
        NOT(Hecho(codigo="L")),
        NOT(Hecho(codigo="I")),
        NOT(MenuPrincipalDefinido()),
        NOT(PlatoUsado(plato="Bifes a la plancha con ensaladas varias")),
        salience=-11,
    )
    def r40_menu_calido_bifes(self):
        self._recomendar_menu(
            "R40",
            plato="Bifes a la plancha con ensaladas varias",
            guarnicion="Ensaladas varias o arroz frío",
            categoria="Clima Cálido",
            motivo="Clima cálido [T/V] rotando menú liviano para evitar repetición.",
            es_principal=True,
            icono="leaf",
            tiempo="20 min",
            rendimiento="25 a 35 viandas",
            tip="Se sirve acompañado de guarniciones frescas, ideal para viandas en días cálidos (R16).",
            prioridad=-11,
        )

    # --- 4. Ingrediente versátil sin clima extremo ni demora ---

    @Rule(
        Hecho(codigo="AH"),
        NOT(Hecho(codigo="L")),
        NOT(Hecho(codigo="I")),
        NOT(MenuPrincipalDefinido()),
        NOT(PlatoUsado(plato="Suprema de pollo")),
        salience=-14,
    )
    def r41_menu_versatil_suprema(self):
        self._recomendar_menu(
            "R41",
            plato="Suprema de pollo",
            guarnicion="Puré o papas fritas (se reservan cuartos traseros para mañana)",
            categoria="Ingrediente Versátil",
            motivo="Despiece de ingrediente versátil [E/AH] maximizando rendimiento.",
            es_principal=True,
            icono="utensils",
            tiempo="25 min",
            rendimiento="Rinde extendido (2 días)",
            tip="Permite resolver dos días de menú con una sola compra mayorista (R26).",
            prioridad=-14,
        )

    # --- 5. Menú paralelo para clientes con restricciones (no bloquea el principal) ---

    @Rule(Hecho(codigo="Y"), salience=-20)
    def r42_menu_paralelo_restricciones(self):
        self._recomendar_menu(
            "R42",
            plato="Menú paralelo básico (bife o pollo a la plancha)",
            guarnicion="Ensalada fresca o arroz blanco sin condimentos",
            categoria="Menú Paralelo (Restricciones)",
            motivo="Cliente con restricciones alimentarias [W/Y].",
            es_principal=False,
            icono="leaf",
            tiempo="20 min",
            rendimiento="Viandas personalizadas",
            tip="Monitorear precio de vegetales en el mercado y comprar para reservar cuando esté económico (R17 + R24 + R25).",
            prioridad=-20,
        )

    # --- 6. Entrada rápida de cortesía en contingencia (no bloquea el principal) ---

    @Rule(Hecho(codigo="Z"), salience=-21)
    def r42b_entrada_sopa_contingencia(self):
        self._recomendar_menu(
            "R18 (Plato Z)",
            plato="Sopa Casera Caliente de Entrada",
            guarnicion="Caldo reconfortante de cortesía",
            categoria="Entrada Rápida (Contingencia)",
            motivo="Se ofrece un plato de entrada rápido (sopa) ante la demora [L -> Z].",
            es_principal=False,
            icono="soup",
            tiempo="3 min (servido inmediato)",
            rendimiento="1 taza por cliente en espera",
            tip="Calma la espera del cliente y mejora la experiencia ante el retraso en cocina (R18).",
            prioridad=-21,
        )

    # --- 7. Comodín si ya se agotaron las rotaciones o no se indicó clima ---

    @Rule(NOT(MenuPrincipalDefinido()), salience=-30)
    def r43_menu_comodin(self):
        self._recomendar_menu(
            "R43",
            plato="Hamburguesas o Napolitanas",
            guarnicion="Papas fritas o puré",
            categoria="Menú Estándar / Comodín",
            motivo="Opción estándar de rotación rápida fuera de restricciones críticas.",
            es_principal=True,
            icono="utensils",
            tiempo="25 min",
            rendimiento="35 viandas estándar",
            tip="Jornada estándar o rotación completada: opción versátil de alta aceptación.",
            prioridad=-30,
        )

    # ========================================================
    # 8. REGLAS DE PLATOS AGREGADOS POR EL USUARIO (OPCIÓN 5)
    # ========================================================
    # [INICIO_REGLAS_APRENDIDAS_CODIGO]
    # (Cuando agregues un plato en la Opción 5, su regla @Rule se escribirá aquí automáticamente)
    # [FIN_REGLAS_APRENDIDAS_CODIGO]


# ========================================================
# GENERADOR DE MENÚ DE PLATOS Y RECOMENDACIONES EXPERTAS
# ========================================================
def construir_menu_recomendado(hechos_fin, platos_aprendidos=None, hechos_iniciales=None, menus_reglas=None):
    """
    Convierte los hechos inferidos y los platos decididos por las reglas R33-R43 en:
    1. Platillos concretos recomendados por las reglas del motor para el menú del día.
    2. Recomendaciones operativas completas de la experta (compras, fileteado/congelado,
       conservación, equipamiento, tiempos y atención al cliente).
    3. Platos descartados y el motivo según las reglas.
    """
    h = set(hechos_fin)
    h_in = set(hechos_iniciales or [])
    platos = []
    descartados = []
    tips_operativos = []
    recomendaciones_experta = {
        "insumos_y_cortes": [],
        "cocina_y_equipamiento": [],
        "clientes_y_servicio": [],
    }

    # --------------------------------------------------------
    # A. PLATILLOS DECIDIDOS POR REGLAS DEL MOTOR (R33 - R43)
    # --------------------------------------------------------
    hay_falta_de_tiempo = bool({"G", "H", "I", "J", "K", "L"} & h)

    if menus_reglas:
        for m in menus_reglas:
            platos.append(
                {
                    "nombre": m.get("nombre") or f"{m['plato']} — {m['guarnicion']}",
                    "plato": m["plato"],
                    "guarnicion": m["guarnicion"],
                    "es_principal": m.get("es_principal", True),
                    "icono": m.get("icono", "utensils"),
                    "categoria": m["categoria"],
                    "tiempo": m.get("tiempo", "25 min"),
                    "rendimiento": m.get("rendimiento", "35 a 45 viandas"),
                    "descripcion": m.get("descripcion") or f"Plato: {m['plato']}. Guarnición: {m['guarnicion']}. ({m['motivo']})",
                    "tip": m.get("tip") or m["motivo"],
                    "regla_origen": m["regla"],
                }
            )

    if ("AD" in h or "AJ" in h) and hay_falta_de_tiempo:
        descartados.append(
            "<b>Platos de olla de larga cocción (Puchero R35, Guiso R36, Locro R37) descartados hoy por demora:</b> "
            "aunque hace frío (C), el retraso en cocina / falta de ayudante activa las reglas de contingencia (R33/R34) "
            "priorizando minutas rápidas con arroz de reserva y sopa caliente de entrada."
        )

    # --------------------------------------------------------
    # B. RECOMENDACIONES DE LA EXPERTA (TODOS LOS HECHOS DEDUCIDOS)
    # --------------------------------------------------------

    # 1. Compras, Fileteado, Congelado y Conservación de Insumos
    if "D" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R1", "hecho": "D", "texto": "Comprar la pieza de carne entera en el frigorífico aprovechando que es inicio de semana (Lun-Mié) y hay oferta."}
        )
    if "E" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R2", "hecho": "E", "texto": "Clasificar la pieza comprada como un 'ingrediente versátil' apto para múltiples preparaciones."}
        )
    if "F" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R3", "hecho": "F", "texto": "Planificar al menos dos platos diferentes a partir de la pieza (ej. guiso y bifes)."}
        )
    if "M" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R9", "hecho": "M", "texto": "Congelar la carne un poco antes de cortarla para facilitar el fileteado y reducir desperdicios."}
        )
    if "N" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R10", "hecho": "N", "texto": "Filetear la carne directamente en la cocina."}
        )
    if "R" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R14", "hecho": "R", "texto": "Aprovechar el rendimiento del fileteado propio: el margen de ganancia aumenta."}
        )
    if "AH" in h or "AI" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R26", "hecho": "AH + AI", "texto": "Deshuesar/preparar una parte para el menú actual (ej. pechuga para suprema) y guardar/freezar otra parte para el menú del día siguiente (ej. cuartos traseros)."}
        )
    if "P" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R12", "hecho": "P", "texto": "Preparar arroz blanco para tener de reserva en la heladera."}
        )
    if "Q" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R13", "hecho": "Q", "texto": "NO agregar cebolla ni verduras frescas al arroz de reserva para que no fermente ni se eche a perder."}
        )
    if "AO" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R31", "hecho": "AO", "texto": "Aprovechar cortes de oferta con hueso específicos para caldos y sopas (ej. osobuco o puchero)."}
        )
    if "AF" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R24", "hecho": "AF", "texto": "Observar y monitorear el precio de los vegetales en el mercado (ej. espinaca)."}
        )
    if "AG" in h:
        recomendaciones_experta["insumos_y_cortes"].append(
            {"regla": "R25", "hecho": "AG", "texto": "Comprar y reservar esa verdura si el precio es bajo para asegurar la vianda especial."}
        )

    # Aviso si marcó oferta de carne (B) pero NO es Lunes-Miércoles (A)
    if "B" in h_in and "A" not in h_in:
        recomendaciones_experta["insumos_y_cortes"].append(
            {
                "regla": "R1 (Condición A+B)",
                "hecho": "B sin A",
                "texto": "Hay oferta de pieza entera (B), pero hoy es Jueves a Domingo (no se cumple A). Según R1, la pieza entera se compra de Lunes a Miércoles para poder usar una parte hoy y guardar el resto para el día siguiente.",
            }
        )

    # 2. Organización de Cocina, Equipamiento y Tiempos
    if "H" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R4", "hecho": "H", "texto": "Atención: la cocina, espacios y ollas NO están limpios a primera hora por ausencia de la ayudante."}
        )
    if "I" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R5", "hecho": "I", "texto": "Reorganizar cronograma: se retrasa el inicio de la elaboración porque Lucía debe limpiar sola."}
        )
    if "J" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R6", "hecho": "J", "texto": "El menú planificado de varios platos requiere demasiado tiempo de elaboración relativo frente al retraso."}
        )
    if "L" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R8", "hecho": "L", "texto": "Activar el protocolo de contingencia por imprevisto/demora en la cocina."}
        )
    if "AB" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R20", "hecho": "AB", "texto": "Encender la plancha o freidora de forma anticipada para agilizar la salida de minutas."}
        )
    if "AJ" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R27", "hecho": "AJ", "texto": "Prever aumento en la demanda de platos de olla (guisos, lentejas, locro) por el frío."}
        )
    if "AD" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R22", "hecho": "AD", "texto": "Planificar un plato de olla de alto volumen (ej. Locro)."}
        )
    if "AL" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R29", "hecho": "AL", "texto": "Utilizar equipamiento de gran volumen (ollas grandes)."}
        )
    if "AM" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R30", "hecho": "AM", "texto": "Calcular un rendimiento masivo de entre 50 y 70 platos por preparación."}
        )
    if "AE" in h:
        recomendaciones_experta["cocina_y_equipamiento"].append(
            {"regla": "R23", "hecho": "AE", "texto": "Organizar el espacio previendo que se ocuparán todas las hornallas de la cocina simultáneamente."}
        )

    # 3. Clientes, Servicio y Entrega
    if "Z" in h:
        recomendaciones_experta["clientes_y_servicio"].append(
            {"regla": "R18", "hecho": "Z", "texto": "Ofrecer un plato de entrada rápido (sopa) al cliente mientras sale el plato principal."}
        )
    if "AC" in h:
        recomendaciones_experta["clientes_y_servicio"].append(
            {"regla": "R21", "hecho": "AC", "texto": "Iniciar una charla con el cliente en mostrador para distraerlo mientras se termina de cocinar."}
        )
    if "S" in h:
        recomendaciones_experta["clientes_y_servicio"].append(
            {"regla": "R15", "hecho": "S", "texto": "Entregar el menú rápido al cliente asegurando que no se eche a perder la guarnición."}
        )
    if "AA" in h:
        recomendaciones_experta["clientes_y_servicio"].append(
            {"regla": "R19", "hecho": "AA", "texto": "Sugerir al cliente agendar el número de contacto para reservar por mensaje en el futuro."}
        )
    if "Y" in h:
        recomendaciones_experta["clientes_y_servicio"].append(
            {"regla": "R17", "hecho": "Y", "texto": "Preparar un menú paralelo básico adaptado al cliente con restricciones alimentarias."}
        )
    if "V" in h:
        recomendaciones_experta["clientes_y_servicio"].append(
            {"regla": "R16", "hecho": "V", "texto": "Sugerir activamente comidas frescas a los clientes durante la jornada de calor."}
        )

    # --------------------------------------------------------
    # C. PLATOS DESCARTADOS
    # --------------------------------------------------------
    if "K" in h:
        descartados.append("<b>Se descarta el menú diario estándar de cocción larga (ej. el guiso):</b> no dan los tiempos por la limpieza inicial sin ayudante (Regla R7 - Hecho K).")
    if "U" in h:
        descartados.append("<b>Se descartan los menús calientes:</b> jornada de clima cálido / verano (Regla R16 - Hecho U).")
    if "AK" in h and not hay_falta_de_tiempo:
        descartados.append("<b>Se descartan las comidas frías o la milanesa estándar como menú principal:</b> alta demanda de platos de olla por el frío (Regla R28 - Hecho AK).")

    # Resumen plano en tips_operativos por compatibilidad
    for grupo in recomendaciones_experta.values():
        for item in grupo:
            tips_operativos.append(f"<b>[{item['regla']}]</b> {item['texto']}")

    return {
        "platos": platos,
        "descartados": descartados,
        "tips_operativos": tips_operativos,
        "recomendaciones_experta": recomendaciones_experta,
    }
