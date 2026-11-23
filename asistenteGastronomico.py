import collections
import collections.abc
# Parche de compatibilidad para Experta en Python 3.10+
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

from experta import *

class Hecho(Fact):
    """Clase base que representa los hechos"""
    pass

class AsesorVirtualGastronomico(KnowledgeEngine):
    
    # ========================================================
    # FLUJO PRINCIPAL: COMPRA Y RENDIMIENTO DE CARNE (R1 - R10)
    # ========================================================

    @Rule(Hecho(codigo='A'), Hecho(codigo='B'))
    def r1_comprar_pieza_entera(self):
        print("[R1] Lunes/Martes/Miércoles y oferta: Se compra pieza entera.")
        self.declare(Hecho(codigo='D'))

    @Rule(Hecho(codigo='D'))
    def r2_ingrediente_versatil(self):
        print("[R2] La pieza comprada se clasifica como 'ingrediente versátil'.")
        self.declare(Hecho(codigo='E'))

    @Rule(Hecho(codigo='G'))
    def r4_ayudante_ausente(self):
        print("[R4] La ayudante avisa que no asiste.")
        self.declare(Hecho(codigo='H'))

    @Rule(Hecho(codigo='H'))
    def r5_retraso_inicio(self):
        print("[R5] Cocina sucia: Se retrasa el inicio de la elaboración (Lucía limpia sola).")
        self.declare(Hecho(codigo='I'))

    @Rule(Hecho(codigo='F'), Hecho(codigo='I'))
    def r6_menu_demasiado_largo(self):
        print("[R6] Dos platos + retraso: El menú requiere demasiado tiempo de elaboración.")
        self.declare(Hecho(codigo='J'))

    @Rule(Hecho(codigo='J'))
    def r7_descartar_menu_estandar(self):
        print("[R7] Se descarta el menú diario estándar (ej. el guiso).")
        self.declare(Hecho(codigo='K'))

    @Rule(Hecho(codigo='K'))
    def r8_activar_contingencia(self):
        print("[R8] Se activa el protocolo de contingencia por imprevisto/demora.")
        self.declare(Hecho(codigo='L'))

    @Rule(Hecho(codigo='D'))
    def r9_congelar_carne(self):
        print("[R9] Se congela la carne un poco para filetear y reducir desperdicios.")
        self.declare(Hecho(codigo='M'))

    @Rule(Hecho(codigo='M'))
    def r10_filetear_carne(self):
        print("[R10] Se filetea la carne en la cocina.")
        self.declare(Hecho(codigo='N'))

    # ========================================================
    # CONFLICTO: E (Se clasifica como ingrediente versátil)
    # Orden de ejecución: R3 -> R26
    # ========================================================

    @Rule(Hecho(codigo='E'), salience=20)
    def r3_planificar_dos_platos(self):
        print("[R3] Ingrediente versátil: Se planifican al menos dos platos diferentes.")
        self.declare(Hecho(codigo='F'))

    @Rule(Hecho(codigo='E'), salience=10)
    def r26_deshuesar_pollo(self):
        print("[R26] Ingrediente versátil: Se deshuesa una parte hoy y se guarda el resto.")
        self.declare(Hecho(codigo='AH'))
        self.declare(Hecho(codigo='AI'))

    # ========================================================
    # CONFLICTO: L (Contingencia por demora)
    # Orden de ejecución: R12 -> R11 -> R18 -> R19
    # ========================================================

    @Rule(Hecho(codigo='L'), salience=40)
    def r12_preparar_arroz(self):
        print("[R12] Contingencia activada: Se necesita preparar arroz para reserva.")
        self.declare(Hecho(codigo='P'))

    @Rule(Hecho(codigo='L'), salience=30)
    def r11_preparar_minutas(self):
        print("[R11] Contingencia activada: Se preparan minutas de cocción rápida.")
        self.declare(Hecho(codigo='O'))

    @Rule(Hecho(codigo='L'), salience=20)
    def r18_ofrecer_sopa(self):
        print("[R18] Contingencia activada: Se ofrece un plato de entrada rápido (sopa).")
        self.declare(Hecho(codigo='Z'))

    @Rule(Hecho(codigo='L'), salience=10)
    def r19_sugerir_reservas(self):
        print("[R19] Contingencia activada: Se sugiere al cliente agendar reservas por msj.")
        self.declare(Hecho(codigo='AA'))

    # ========================================================
    # ENCADENAMIENTO DEL ARROZ (P -> Q)
    # ========================================================

    @Rule(Hecho(codigo='P'))
    def r13_arroz_sin_verduras(self):
        print("[R13] Preparando arroz: No se le agrega cebolla ni verduras frescas.")
        self.declare(Hecho(codigo='Q'))

    # ========================================================
    # ENCADENAMIENTO DE AUMENTO DE GANANCIA (N -> R)
    # ========================================================
    
    @Rule(Hecho(codigo='N'))
    def r14_aumentar_ganancia(self):
        print("[R14] Se filetea la carne en la cocina: el margen de ganancia aumenta.")
        self.declare(Hecho(codigo='R'))

    # ========================================================
    # ENCADENAMIENTO DE CLIMA CÁLIDO (T -> U y V)
    # ========================================================
    
    @Rule(Hecho(codigo='T'))
    def r16_clima_calido(self):
        print("[R16] Clima cálido: Se descartan menús calientes y se sugieren comidas frescas.")
        self.declare(Hecho(codigo='U'))
        self.declare(Hecho(codigo='V'))

    # ========================================================
    # CONFLICTO: W (Cliente tiene restricciones alimentarias)
    # Orden de ejecución: R17 -> R24
    # ========================================================
        
    @Rule(Hecho(codigo='W'), salience=20)
    def r17_menu_paralelo(self):
        print("[R17] Cliente tiene restricciones alimentarias: se prepara menú paralelo básico.")
        self.declare(Hecho(codigo='Y'))
        
    @Rule(Hecho(codigo='W'), salience=10)
    def r24_monitorear_precio(self):
        print("[R24] Cliente tiene restricciones alimentarias: se observa precio de los vegetales.")
        self.declare(Hecho(codigo='AF'))

    # ========================================================
    # SE OBSERVA PRECIOS DE VEGETALES EN EL MERCADO (AF -> AG)
    # ========================================================
                
    @Rule(Hecho(codigo='AF'))
    def r25_comprar_verdura(self):
        print("[R25] Se observa precios de vegetales: se compra y reserva si el precio es bajo.")
        self.declare(Hecho(codigo='AG'))

    # ========================================================
    # CONFLICTO: O (Minutas de cocción rápida)
    # Orden de ejecución: R20 -> R15
    # ========================================================

    @Rule(Hecho(codigo='O'), salience=20)
    def r20_encender_plancha(self):
        print("[R20] Minutas en marcha: Se enciende la plancha o freidora anticipadamente.")
        self.declare(Hecho(codigo='AB'))

    @Rule(Hecho(codigo='O'), Hecho(codigo='Q'), salience=15)
    def r15_entrega_menu_rapido(self):
        print("[R15] Platos y guarnición listos: El cliente recibe el menú rápido.")
        self.declare(Hecho(codigo='S'))

    # ========================================================
    # CONFLICTO: C (Clima frío)
    # Orden de ejecución: R27 -> R22 -> R32
    # ========================================================

    @Rule(Hecho(codigo='C'), salience=30)
    def r27_demanda_olla(self):
        print("[R27] Clima frío: Aumenta la demanda de platos de olla.")
        self.declare(Hecho(codigo='AJ'))

    @Rule(Hecho(codigo='C'), salience=20)
    def r22_planificar_olla_volumen(self):
        print("[R22] Clima frío: Se planifica un plato de olla de alto volumen.")
        self.declare(Hecho(codigo='AD'))

    @Rule(Hecho(codigo='C'), salience=10)  # CORREGIDO: Antes decía Hecho(codigo='O')
    def r32_aprovechar_oferta_hueso(self):
        print("[R32] Clima frío: Se aprovechan cortes de oferta con hueso para caldos.")
        self.declare(Hecho(codigo='AO'))

    # ========================================================
    # ENCADENAMIENTO DE PLANIFICACIÓN DE OLLA (AD -> AE)
    # ========================================================
            
    @Rule(Hecho(codigo='AD'))
    def r23_ocupar_hornallas(self):
        print("[R23] Se planifica plato de olla: se ocupan todas las hornallas simultáneamente.")
        self.declare(Hecho(codigo='AE'))

    # ========================================================
    # CONFLICTO: AJ (Aumenta demanda de plato de olla)
    # Orden de ejecución: R28 -> R29
    # ========================================================
    
    @Rule(Hecho(codigo='AJ'), salience=20)
    def r28_descartar_frias(self):
        print("[R28] Aumenta demanda de olla: se descartan comidas frías y milanesas.")
        self.declare(Hecho(codigo='AK'))
    
    @Rule(Hecho(codigo='AJ'), salience=10)
    def r29_usar_ollas_grandes(self):
        print("[R29] Aumenta demanda de olla: usar ollas grandes.")
        self.declare(Hecho(codigo='AL'))

    # ========================================================
    # ENCADENAMIENTO DE EQUIPAMIENTO (AL -> AM)
    # ========================================================
        
    @Rule(Hecho(codigo='AL'))
    def r30_rendimiento_masivo(self):
        print("[R30] Se utiliza equipamiento de gran volumen: rendimiento masivo (50 a 70 platos).")
        self.declare(Hecho(codigo='AM'))

    # ========================================================
    # ENCADENAMIENTO DE LA PLANCHA (AB -> AC)
    # ========================================================

    @Rule(Hecho(codigo='AB'))
    def r21_charla_cliente(self):
        print("[R21] Plancha encendida: Se inicia charla con el cliente para distraerlo.")
        self.declare(Hecho(codigo='AC'))


# ========================================================
# EJECUCIÓN PASO A PASO (SIMULADOR DE ESCENARIOS)
# ========================================================
if __name__ == "__main__":
    import sys
    # Forzamos la consola a leer UTF-8 para que no salgan los rombos () en los acentos
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("--- INICIANDO ASESOR VIRTUAL GASTRONÓMICO ---\n")
    motor = AsesorVirtualGastronomico()
    
    # --------------------------------------------------------
    print(">> ESCENARIO 1: Ola de frío a principio de semana")
    # --------------------------------------------------------
    motor.reset() # Limpiamos la memoria
    motor.declare(Hecho(codigo='C')) # Hace frío
    motor.declare(Hecho(codigo='A')) # Es Lunes/Martes/Miércoles
    motor.declare(Hecho(codigo='B')) # Hay oferta
    motor.run()
    
    print("\n" + "="*50 + "\n")
    
    # --------------------------------------------------------
    print(">> ESCENARIO 2: Verano y atención de cliente fijo")
    # --------------------------------------------------------
    motor.reset() # Limpiamos la memoria para este nuevo día
    motor.declare(Hecho(codigo='T')) # Clima cálido
    motor.declare(Hecho(codigo='W')) # Cliente con restricciones
    motor.run()

    print("\n" + "="*50 + "\n")

    # --------------------------------------------------------
    print(">> ESCENARIO 3: Contingencia operativa sobre la marcha")
    # --------------------------------------------------------
    motor.reset() # Limpiamos la memoria
    motor.declare(Hecho(codigo='L')) # Se activa contingencia por demora
    motor.declare(Hecho(codigo='N')) # Se fileteó la carne
    motor.declare(Hecho(codigo='Q')) # El arroz estaba sin verduras
    motor.run()