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
    """Guarda un nuevo hecho y/o regla de recomendación de plato en la base aprendida."""
    data = cargar_conocimiento_aprendido()
    codigo_cond = (condicion_codigo or "C").strip().upper()

    # Proteger los hechos base A-AO para que nunca sean sobreescritos como personalizados
    if es_hecho_nuevo and codigo_cond and codigo_cond not in HECHOS_BASE_ORIGINALES:
        desc_limpia = condicion_descripcion.strip() or f"Condición personalizada {codigo_cond}"
        data["hechos_personalizados"][codigo_cond] = desc_limpia

    # Calcular ID incremental único aunque se hayan borrado reglas previas
    max_num = 0
    for r in data["reglas_platos"]:
        rid = r.get("id", "")
        if rid.startswith("RA") and rid[2:].isdigit():
            max_num = max(max_num, int(rid[2:]))
    nuevo_idx = max_num + 1
    regla_id = f"RA{nuevo_idx}"
    hecho_generado = f"PL_{nuevo_idx}"

    catalogo = obtener_catalogo_hechos_completo()
    desc_final = catalogo.get(codigo_cond) or data["hechos_personalizados"].get(codigo_cond) or condicion_descripcion.strip()

    nueva_regla = {
        "id": regla_id,
        "condicion_codigo": codigo_cond,
        "condicion_descripcion": desc_final,
        "hecho_generado": hecho_generado,
        "nombre_plato": nombre_plato.strip(),
        "categoria": categoria,
        "descripcion_plato": descripcion_plato.strip(),
        "tiempo_estimado": tiempo_estimado.strip() or "25 min",
        "consejo_cocina": consejo_cocina.strip(),
    }
    data["reglas_platos"].append(nueva_regla)

    with open(ARCHIVO_APRENDIZAJE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return nueva_regla


def eliminar_regla_aprendida(regla_id):
    """Elimina una regla aprendida por su ID (o todas si regla_id == 'TODAS') y limpia hechos huérfanos."""
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


def obtener_catalogo_hechos_completo():
    """Devuelve DESCRIPCION_HECHOS fusionado con los hechos aprendidos."""
    catalogo = dict(DESCRIPCION_HECHOS)
    aprendido = cargar_conocimiento_aprendido()
    catalogo.update(aprendido.get("hechos_personalizados", {}))
    for r in aprendido.get("reglas_platos", []):
        catalogo[r["hecho_generado"]] = f"Sugerir plato aprendido: {r['nombre_plato']}"
    return catalogo


class Hecho(Fact):
    """Clase base que representa los hechos en la memoria de trabajo."""
    pass


class AsesorVirtualGastronomico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.traza = []            # Explicabilidad (XAI): cadena de reglas disparadas
        self.recomendaciones = []  # Acciones concretas para mostrar a Lucía
        self.platos_aprendidos_disparados = []

    def reset(self, **kwargs):
        """Limpia las listas cada vez que se reinicia el motor."""
        super().reset(**kwargs)
        self.traza = []
        self.recomendaciones = []
        self.platos_aprendidos_disparados = []

    def registrar_paso(self, regla, explicacion, recomendacion):
        """Método auxiliar para registrar la traza XAI y la recomendación."""
        self.traza.append(f"[{regla}] {explicacion}")
        self.recomendaciones.append(recomendacion)

    def obtener_hechos_finales(self):
        """Devuelve la lista de códigos de hechos en la memoria de trabajo."""
        return [fact["codigo"] for fact in self.facts.values() if "codigo" in fact]

    def run(self, steps=None):
        """Ejecuta el motor Experta y luego evalúa las reglas aprendidas dinámicamente."""
        if steps is None:
            super().run()
        else:
            super().run(steps)

        # Evaluar reglas aprendidas continuamente
        aprendido = cargar_conocimiento_aprendido()
        hechos_actuales = set(self.obtener_hechos_finales())

        for regla in aprendido.get("reglas_platos", []):
            cond = regla["condicion_codigo"]
            hecho_gen = regla["hecho_generado"]
            if cond in hechos_actuales and hecho_gen not in hechos_actuales:
                self.declare(Hecho(codigo=hecho_gen))
                hechos_actuales.add(hecho_gen)
                self.platos_aprendidos_disparados.append(regla)
                self.registrar_paso(
                    regla=regla["id"],
                    explicacion=(
                        f"Hecho {cond} ({regla['condicion_descripcion']}) -> "
                        f"Aprendizaje activo: Recomendar '{regla['nombre_plato']}' ({hecho_gen})."
                    ),
                    recomendacion=f"[Aprendido] Incorporar al menú: {regla['nombre_plato']} ({regla['descripcion_plato']}).",
                )

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
# GENERADOR DE MENÚ DE PLATOS Y RECOMENDACIONES EXPERTAS
# ========================================================
def construir_menu_recomendado(hechos_fin, platos_aprendidos=None, hechos_iniciales=None):
    """
    Convierte los hechos inferidos en:
    1. Platillos concretos recomendados para el menú del día.
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
    # A. PLATILLOS RECOMENDADOS
    # --------------------------------------------------------

    # 1. CONTINGENCIA / MINUTAS RÁPIDAS (O, P, Q, S)
    if "O" in h:
        guarnicion = "Arroz blanco de reserva (cocinado sin cebolla ni verduras frescas)" if "Q" in h else "Arroz blanco"
        platos.append(
            {
                "nombre": "Milanesas o Bifes a la Plancha con Arroz Blanco",
                "icono": "utensils",
                "categoria": "Plato Principal Rápido (Contingencia)",
                "tiempo": "12 - 15 min",
                "rendimiento": "Al instante / A demanda",
                "descripcion": f"Minutas de cocción rápida (milanesas, bifes o costeletas) acompañadas de {guarnicion}.",
                "tip": "Encender plancha/freidora anticipadamente (R20) y usar arroz sin verduras (R13) para que no fermente.",
                "regla_origen": "R11 + R12 + R13 + R15",
            }
        )
        platos.append(
            {
                "nombre": "Costeletas a la Plancha con Arroz al Caldo",
                "icono": "utensils",
                "categoria": "Alternativa de Minuta Rápida",
                "tiempo": "15 min",
                "rendimiento": "Salida inmediata",
                "descripcion": "Costeletas doradas a la plancha rápida con porción de arroz de reserva listo para despachar.",
                "tip": "Ideal para despachar rápido mientras se conversa con el cliente en mostrador (R21).",
                "regla_origen": "R11 + R20 + R21",
            }
        )

    # 2. ENTRADA DE CORTESÍA EN DEMORA (Z)
    if "Z" in h:
        platos.append(
            {
                "nombre": "Sopa Casera Caliente de Entrada",
                "icono": "soup",
                "categoria": "Entrada Rápida de Cortesía",
                "tiempo": "3 min (servido inmediato)",
                "rendimiento": "1 taza por cliente en espera",
                "descripcion": "Caldo casero reconfortante servido como entrada rápida mientras se terminan de dorar las minutas.",
                "tip": "Calma la espera del cliente y mejora la experiencia ante el retraso en cocina (R18).",
                "regla_origen": "R18",
            }
        )

    # 3. CLIMA FRÍO: PLATOS DE OLLA MASIVOS (AD, AJ, AL, AM, AO)
    # Si hay cualquier demora o falta de ayudante (G, H, I, J, K o L), no recomendar Locro/Guiso de 90-120 min:
    hay_falta_de_tiempo = bool({"G", "H", "I", "J", "K", "L"} & h)
    if ("AD" in h or "AJ" in h) and not hay_falta_de_tiempo:
        rinde_txt = "50 a 70 porciones (Olla grande)" if "AM" in h else "30 a 40 porciones"
        platos.append(
            {
                "nombre": "Locro Criollo Masivo en Olla Grande",
                "icono": "flame",
                "categoria": "Plato Principal de Olla (Clima Frío)",
                "tiempo": "90 - 120 min",
                "rendimiento": rinde_txt,
                "descripcion": "Locro bien completo de alto volumen ideal para cubrir el pico de demanda por bajas temperaturas.",
                "tip": "Usar equipamiento de gran volumen (R29) y prever la ocupación de todas las hornallas simultáneamente (R23).",
                "regla_origen": "R22 + R23 + R29 + R30",
            }
        )
        platos.append(
            {
                "nombre": "Guiso de Lentejas Casero de Alto Rendimiento",
                "icono": "flame",
                "categoria": "Plato Principal de Olla (Clima Frío)",
                "tiempo": "60 - 75 min",
                "rendimiento": rinde_txt,
                "descripcion": "Guiso sustancioso de lentejas con carne y vegetales para despacho continuo de viandas calientes.",
                "tip": "Alta demanda asegurada en días fríos; priorizar por sobre minutas o platos fríos (R27 + R28).",
                "regla_origen": "R27 + R28",
            }
        )
    elif ("AD" in h or "AJ" in h) and hay_falta_de_tiempo:
        descartados.append(
            "<b>Locro y Guiso de Lentejas de larga cocción (90-120 min) descartados hoy por demora:</b> "
            "aunque hace frío (C), el retraso en cocina / falta de ayudante impide elaboraciones de 2 horas; "
            "se reemplazan por minutas rápidas y sopa caliente de entrada."
        )
        if "O" not in h:
            platos.append(
                {
                    "nombre": "Milanesas o Bifes a la Plancha con Arroz Blanco",
                    "icono": "utensils",
                    "categoria": "Plato Principal Rápido (Por Retraso en Cocina)",
                    "tiempo": "12 - 15 min",
                    "rendimiento": "Salida rápida",
                    "descripcion": "Minutas de cocción rápida para compensar el retraso de inicio en la cocina (Hecho I).",
                    "tip": "Permite cumplir a tiempo con los clientes cuando no alcanzan las 2 horas para un plato de olla.",
                    "regla_origen": "R4 + R5 (Retraso I)",
                }
            )

    if "AO" in h and not hay_falta_de_tiempo:
        platos.append(
            {
                "nombre": "Puchero / Sopa Sustanciosa de Osobuco",
                "icono": "soup",
                "categoria": "Plato de Olla Económico (Oferta con Hueso)",
                "tiempo": "70 min",
                "rendimiento": "40 a 50 porciones",
                "descripcion": "Caldo concentrado y puchero elaborado aprovechando cortes económicos con hueso en oferta (osobuco/puchero).",
                "tip": "Excelente margen de ganancia aprovechando ofertas de cortes con hueso para días fríos (R31).",
                "regla_origen": "R31",
            }
        )
    elif "AO" in h and hay_falta_de_tiempo:
        platos.append(
            {
                "nombre": "Caldo Rápido Concentrado de Osobuco (Entrada de Invierno)",
                "icono": "soup",
                "categoria": "Caldo Caliente en Contingencia (Oferta con Hueso)",
                "tiempo": "25 min (en olla a presión / caldo corto)",
                "rendimiento": "40 tazas de entrada",
                "descripcion": "Aprovecha los cortes con hueso en oferta (AO) para reforzar la sopa caliente de entrada rápida (Z) mientras salen las minutas.",
                "tip": "Combina la ventaja de oferta de invierno (R31) con la entrada rápida de contingencia (R18).",
                "regla_origen": "R31 + R18",
            }
        )

    # 4. CLIMA CÁLIDO / VERANO (V)
    if "V" in h:
        platos.append(
            {
                "nombre": "Ensalada Caesar Completa con Pollo Grillado",
                "icono": "leaf",
                "categoria": "Plato Principal Fresco (Verano)",
                "tiempo": "20 min",
                "rendimiento": "25 a 35 viandas",
                "descripcion": "Hojas verdes frescas, tiras de pechuga grillada, crutones caseros y aderezo liviano.",
                "tip": "Reemplaza los guisos calientes en jornadas de calor (R16).",
                "regla_origen": "R16",
            }
        )
        platos.append(
            {
                "nombre": "Tarta Primavera Fresca + Ensalada Multicolor",
                "icono": "leaf",
                "categoria": "Plato Principal Fresco (Verano)",
                "tiempo": "30 min",
                "rendimiento": "24 porciones",
                "descripcion": "Tarta liviana de vegetales de estación acompañada de ensalada fresca de tomate, zanahoria y huevo.",
                "tip": "Se sirve tibia o fría, ideal para viandas de oficina en días cálidos (R16).",
                "regla_origen": "R16",
            }
        )

    # 5. PIEZA ENTERA VERSÁTIL EN OPERACIÓN NORMAL (F, AH, AI, N sin K)
    if "F" in h and "K" not in h:
        platos.append(
            {
                "nombre": "Guiso Casero del Día + Bifes Criollos (Menú Doble)",
                "icono": "utensils",
                "categoria": "Doble Opción con Pieza Entera",
                "tiempo": "50 min",
                "rendimiento": "Optimizado (Mayor Margen R14)",
                "descripcion": "Se aprovecha la pieza de carne entera en oferta para sacar dos platos: guiso tradicional y bifes fileteados en cocina.",
                "tip": "Congelar un poco la carne antes de filetear (R9, R10) para reducir desperdicios y aumentar la ganancia (R14).",
                "regla_origen": "R1 + R2 + R3 + R9 + R10 + R14",
            }
        )
    if "AH" in h:
        platos.append(
            {
                "nombre": "Supremas de Pechuga Deshuesada al Limón o Napolitana",
                "icono": "utensils",
                "categoria": "Aprovechamiento de Pieza Versátil",
                "tiempo": "25 min",
                "rendimiento": "Rinde extendido (2 días)",
                "descripcion": "Supremas preparadas con la parte deshuesada para hoy, guardando otra parte (ej. cuartos traseros) para el menú de mañana.",
                "tip": "Permite resolver dos días de menú con una sola compra mayorista (R26).",
                "regla_origen": "R26",
            }
        )

    # 6. CLIENTE CON RESTRICCIONES ALIMENTARIAS (Y, AF, AG)
    if "Y" in h:
        platos.append(
            {
                "nombre": "Medallones / Tarta de Espinaca y Arroz Yamaní (Menú Especial)",
                "icono": "leaf",
                "categoria": "Vianda Paralela (Restricción Alimentaria)",
                "tiempo": "25 min",
                "rendimiento": "Viandas personalizadas",
                "descripcion": "Menú paralelo básico y saludable elaborado con espinaca fresca seleccionada a buen precio en el mercado.",
                "tip": "Monitorear precio de espinaca en el mercado y comprar para reservar cuando esté económico (R17 + R24 + R25).",
                "regla_origen": "R17 + R24 + R25",
            }
        )

    # 7. PLATOS APRENDIDOS CONTINUAMENTE
    if platos_aprendidos:
        for pa in platos_aprendidos:
            platos.append(
                {
                    "nombre": pa["nombre_plato"],
                    "icono": "sparkle",
                    "categoria": f"{pa['categoria']} (Aprendido)",
                    "tiempo": pa.get("tiempo_estimado", "25 min"),
                    "rendimiento": "Personalizado por Lucía",
                    "descripcion": pa["descripcion_plato"],
                    "tip": pa.get("consejo_cocina") or f"Activado por condición {pa['condicion_codigo']}.",
                    "regla_origen": pa["id"],
                }
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
