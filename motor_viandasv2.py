# motor_viandas.py
from hechos import Estado, MenuSugerido, PlatoUsado, MenuPrincipalDefinido, DESCRIPCION_HECHOS
from experta import KnowledgeEngine, Rule, AND, NOT


class MotorViandas(KnowledgeEngine):
    """Motor de Inferencia con módulo de Explicabilidad y Trazabilidad (XAI)."""

    def __init__(self):
        super().__init__()
        self.hechos_iniciales = []
        self.traza = []
        self.menus_sugeridos = []

    def reset(self):
        """Reinicia la memoria de trabajo y limpia el historial de explicaciones."""
        super().reset()
        self.hechos_iniciales = []
        self.traza = []
        self.menus_sugeridos = []

    def cargar_hechos_iniciales(self, codigos):
        """Declara los hechos iniciales del día y los guarda para la trazabilidad."""
        for codigo in codigos:
            if codigo not in DESCRIPCION_HECHOS:
                raise ValueError(f"Código de hecho desconocido: '{codigo}'")
            self.hechos_iniciales.append(codigo)
            self.declare(Estado(codigo=codigo))

    def _aplicar_regla(self, regla_id, antecedentes, consecuentes, prioridad=0):
        """Registra la regla disparada en la traza y declara los nuevos hechos."""
        for codigo in consecuentes:
            self.declare(Estado(codigo=codigo))

        self.traza.append({
            "paso": len(self.traza) + 1,
            "regla": regla_id,
            "prioridad": prioridad,
            "antecedentes": antecedentes,
            "consecuentes": consecuentes,
        })

    def mostrar_explicacion(self):
        """Imprime el reporte legible (XAI) del razonamiento completo."""
        linea = "=" * 80
        print(f"\n{linea}")
        print("REPORTE DE EXPLICABILIDAD Y TRAZABILIDAD (XAI) - ASESOR DE VIANDAS")
        print(linea)

        print("\n1. CONDICIONES INICIALES DETECTADAS (Base de Hechos Inicial):")
        for cod in self.hechos_iniciales:
            print(f"   • [{cod}] {DESCRIPCION_HECHOS[cod]}")

        print(f"\n2. CADENA DE RAZONAMIENTO ({len(self.traza)} reglas disparadas):")
        if not self.traza:
            print("   No se disparó ninguna regla con los hechos ingresados.")
        else:
            for item in self.traza:
                tag_prio = f" | Prioridad (salience): {item['prioridad']}" if item["prioridad"] > 0 else ""
                print(f"\n   Paso {item['paso']} — Regla {item['regla']}{tag_prio}")

                motivos = " Y ".join(
                    f"[{c}] {DESCRIPCION_HECHOS[c]}" for c in item["antecedentes"]
                )
                resultados = " Y ".join(
                    f"[{c}] {DESCRIPCION_HECHOS[c]}" for c in item["consecuentes"]
                )
                print(f"     PORQUE:   {motivos}")
                print(f"     ENTONCES: {resultados}")

        deducidos = []
        for item in self.traza:
            for c in item["consecuentes"]:
                if c not in deducidos:
                    deducidos.append(c)

        print(f"\n3. RESUMEN DE DECISIONES Y HECHOS DEDUCIDOS ({len(deducidos)}):")
        for cod in deducidos:
            print(f"   ✓ [{cod}] {DESCRIPCION_HECHOS[cod]}")
        print(f"\n{linea}\n")

    def cargar_platos_usados(self, platos):
        """Carga platos usados en días previos para que el motor los rote."""
        for plato in platos:
            self.declare(PlatoUsado(plato=plato))

    def _recomendar_menu(self, regla_id, plato, guarnicion, categoria, motivo, es_principal=True):
        """Declara el menú sugerido y lo guarda para la capa XAI y Streamlit."""
        self.declare(MenuSugerido(plato=plato, guarnicion=guarnicion, categoria=categoria))
        if es_principal:
            self.declare(MenuPrincipalDefinido())

        self.menus_sugeridos.append({
            "regla": regla_id,
            "plato": plato,
            "guarnicion": guarnicion,
            "categoria": categoria,
            "motivo": motivo,
            "es_principal": es_principal,
        })

    # =========================================================================
    # BASE DE REGLAS (R1 - R30, R32) CON PRIORIDADES DE CONFLICTO
    # =========================================================================

    # --- Cadena principal de compras, personal y contingencias (R1 - R15) ---

    @Rule(AND(Estado(codigo="A"), Estado(codigo="B")))
    def r1_comprar_pieza_entera(self):
        self._aplicar_regla("R1", ["A", "B"], ["D"])

    @Rule(Estado(codigo="D"))
    def r2_clasificar_versatil(self):
        self._aplicar_regla("R2", ["D"], ["E"])

    @Rule(Estado(codigo="E"), salience=20)
    def r3_planificar_dos_platos(self):
        self._aplicar_regla("R3", ["E"], ["F"], prioridad=20)

    @Rule(Estado(codigo="G"))
    def r4_cocina_no_limpia(self):
        self._aplicar_regla("R4", ["G"], ["H"])

    @Rule(Estado(codigo="H"))
    def r5_retraso_inicio(self):
        self._aplicar_regla("R5", ["H"], ["I"])

    @Rule(AND(Estado(codigo="F"), Estado(codigo="I")))
    def r6_tiempo_excesivo(self):
        self._aplicar_regla("R6", ["F", "I"], ["J"])

    @Rule(Estado(codigo="J"))
    def r7_descartar_menu_estandar(self):
        self._aplicar_regla("R7", ["J"], ["K"])

    @Rule(Estado(codigo="K"))
    def r8_activar_contingencia(self):
        self._aplicar_regla("R8", ["K"], ["L"])

    @Rule(Estado(codigo="D"))
    def r9_congelar_para_filetear(self):
        self._aplicar_regla("R9", ["D"], ["M"])

    @Rule(Estado(codigo="M"))
    def r10_filetear_en_cocina(self):
        self._aplicar_regla("R10", ["M"], ["N"])

    @Rule(Estado(codigo="L"), salience=30)
    def r11_preparar_minutas(self):
        self._aplicar_regla("R11", ["L"], ["O"], prioridad=30)

    @Rule(Estado(codigo="L"), salience=40)
    def r12_preparar_arroz_reserva(self):
        self._aplicar_regla("R12", ["L"], ["P"], prioridad=40)

    @Rule(Estado(codigo="P"))
    def r13_arroz_sin_verduras(self):
        self._aplicar_regla("R13", ["P"], ["Q"])

    @Rule(Estado(codigo="N"))
    def r14_aumentar_ganancia(self):
        self._aplicar_regla("R14", ["N"], ["R"])

    @Rule(AND(Estado(codigo="O"), Estado(codigo="Q")), salience=10)
    def r15_cliente_recibe_rapido(self):
        self._aplicar_regla("R15", ["O", "Q"], ["S"], prioridad=10)

    # --- Ramas de clima cálido y restricciones alimentarias (R16 - R17) ---

    @Rule(Estado(codigo="T"))
    def r16_clima_calido(self):
        self._aplicar_regla("R16", ["T"], ["U", "V"])

    @Rule(Estado(codigo="W"))
    def r17_menu_paralelo_basico(self):
        self._aplicar_regla("R17", ["W"], ["Y"])

    # --- Caminos paralelos de atención al cliente y minutas (R18 - R21) ---

    @Rule(Estado(codigo="L"), salience=20)
    def r18_ofrecer_sopa(self):
        self._aplicar_regla("R18", ["L"], ["Z"], prioridad=20)

    @Rule(Estado(codigo="L"), salience=10)
    def r19_sugerir_reservas(self):
        self._aplicar_regla("R19", ["L"], ["AA"], prioridad=10)

    @Rule(Estado(codigo="O"), salience=20)
    def r20_encender_plancha(self):
        self._aplicar_regla("R20", ["O"], ["AB"], prioridad=20)

    @Rule(Estado(codigo="AB"))
    def r21_charlar_con_cliente(self):
        self._aplicar_regla("R21", ["AB"], ["AC"])

    # --- Caminos paralelos de clima frío, vegetales y despiece (R22 - R32) ---

    @Rule(Estado(codigo="C"), salience=20)
    def r22_planificar_plato_olla(self):
        self._aplicar_regla("R22", ["C"], ["AD"], prioridad=20)

    @Rule(Estado(codigo="AD"))
    def r23_ocupar_todas_hornallas(self):
        self._aplicar_regla("R23", ["AD"], ["AE"])

    @Rule(Estado(codigo="W"))
    def r24_monitorear_vegetales(self):
        self._aplicar_regla("R24", ["W"], ["AF"])

    @Rule(Estado(codigo="AF"))
    def r25_comprar_verdura_baja(self):
        self._aplicar_regla("R25", ["AF"], ["AG"])

    @Rule(Estado(codigo="E"), salience=10)
    def r26_despiece_pollo(self):
        self._aplicar_regla("R26", ["E"], ["AH", "AI"], prioridad=10)

    @Rule(Estado(codigo="C"), salience=30)
    def r27_aumenta_demanda_olla(self):
        self._aplicar_regla("R27", ["C"], ["AJ"], prioridad=30)

    @Rule(Estado(codigo="AJ"), salience=20)
    def r28_descartar_frias_milanesas(self):
        self._aplicar_regla("R28", ["AJ"], ["AK"], prioridad=20)

    @Rule(Estado(codigo="AJ"), salience=10)
    def r29_usar_ollas_grandes(self):
        self._aplicar_regla("R29", ["AJ"], ["AL"], prioridad=10)

    @Rule(Estado(codigo="AL"))
    def r30_rendimiento_masivo(self):
        self._aplicar_regla("R30", ["AL"], ["AM"])

    @Rule(Estado(codigo="C"), salience=10)
    def r32_comprar_osobuco_oferta(self):
        self._aplicar_regla("R32", ["C"], ["AO"], prioridad=10)

    # =========================================================================
    # CAPA DE RECOMENDACIÓN DE MENÚS (R33 - R43) | salience < 0
    # Se evalúan únicamente después de completar toda la inferencia operativa.
    # =========================================================================

    # --- Contingencia / Minutas rápidas (si hubo demora L -> O y Q) ---

    @Rule(
        Estado(codigo="O"),
        Estado(codigo="Q"),
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
            motivo="Contingencia activa [L/O] y arroz de reserva disponible [Q].",
        )

    @Rule(
        Estado(codigo="O"),
        Estado(codigo="Q"),
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
            motivo="Contingencia activa [L/O] rotando plato rápido para no repetir.",
        )

    # --- Clima frío sin contingencia (platos de olla) ---

    @Rule(
        Estado(codigo="C"),
        Estado(codigo="AO"),
        NOT(Estado(codigo="L")),
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
        )

    @Rule(
        Estado(codigo="AD"),
        Estado(codigo="D"),
        NOT(Estado(codigo="L")),
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
        )

    @Rule(
        Estado(codigo="AD"),
        NOT(Estado(codigo="L")),
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
        )

    @Rule(
        Estado(codigo="AJ"),
        NOT(Estado(codigo="L")),
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
        )

    # --- Clima cálido sin contingencia ---

    @Rule(
        Estado(codigo="V"),
        NOT(Estado(codigo="L")),
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
        )

    @Rule(
        Estado(codigo="V"),
        NOT(Estado(codigo="L")),
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
        )

    # --- Ingrediente versátil sin clima específico ---

    @Rule(
        Estado(codigo="AH"),
        NOT(Estado(codigo="L")),
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
        )

    # --- Menú paralelo para clientes con restricciones (no bloquea el principal) ---

    @Rule(Estado(codigo="Y"), salience=-20)
    def r42_menu_paralelo_restricciones(self):
        self._recomendar_menu(
            "R42",
            plato="Menú paralelo básico (bife o pollo a la plancha)",
            guarnicion="Ensalada fresca o arroz blanco sin condimentos",
            categoria="Menú Paralelo (Restricciones)",
            motivo="Cliente con restricciones alimentarias [W/Y].",
            es_principal=False,
        )

    # --- Comodín si ya se agotaron las rotaciones o no se indicó clima ---

    @Rule(NOT(MenuPrincipalDefinido()), salience=-30)
    def r43_menu_comodin(self):
        self._recomendar_menu(
            "R43",
            plato="Hamburguesas o Napolitanas",
            guarnicion="Papas fritas o puré",
            categoria="Menú Estándar / Comodín",
            motivo="Opción estándar de rotación rápida fuera de restricciones críticas.",
        )