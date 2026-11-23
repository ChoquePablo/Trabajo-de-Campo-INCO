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

    @Rule(Hecho(codigo='A'), Hecho(codigo='B'), salience=100)
    def r1_comprar_pieza_entera(self):
        print("[R1] Lunes/Martes/Miércoles y oferta: Se compra pieza entera.")
        self.declare(Hecho(codigo='D'))

    @Rule(Hecho(codigo='D'), salience=90)
    def r2_ingrediente_versatil(self):
        print("[R2] La pieza comprada se clasifica como 'ingrediente versátil'.")
        self.declare(Hecho(codigo='E'))

    @Rule(Hecho(codigo='E'), salience=80)
    def r3_planificar_dos_platos(self):
        print("[R3] Ingrediente versátil: Se planifican al menos dos platos diferentes.")
        self.declare(Hecho(codigo='F'))

    @Rule(Hecho(codigo='G'), salience=95)
    def r4_ayudante_ausente(self):
        print("[R4] La ayudante avisa que no asiste.")
        self.declare(Hecho(codigo='H'))

    @Rule(Hecho(codigo='H'), salience=85)
    def r5_retraso_inicio(self):
        print("[R5] Cocina sucia: Se retrasa el inicio de la elaboración (Lucía limpia sola).")
        self.declare(Hecho(codigo='I'))

    @Rule(Hecho(codigo='F'), Hecho(codigo='I'), salience=75)
    def r6_menu_demasiado_largo(self):
        print("[R6] Dos platos + retraso: El menú requiere demasiado tiempo de elaboración.")
        self.declare(Hecho(codigo='J'))

    @Rule(Hecho(codigo='J'), salience=65)
    def r7_descartar_menu_estandar(self):
        print("[R7] Se descarta el menú diario estándar (ej. el guiso).")
        self.declare(Hecho(codigo='K'))

    @Rule(Hecho(codigo='K'), salience=55)
    def r8_activar_contingencia(self):
        print("[R8] Se activa el protocolo de contingencia por imprevisto/demora.")
        self.declare(Hecho(codigo='L'))

    @Rule(Hecho(codigo='D'), salience=70)
    def r9_congelar_carne(self):
        print("[R9] Se congela la carne un poco para filetear y reducir desperdicios.")
        self.declare(Hecho(codigo='M'))

    @Rule(Hecho(codigo='M'), salience=60)
    def r10_filetear_carne(self):
        print("[R10] Se filetea la carne en la cocina.")
        self.declare(Hecho(codigo='N'))

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
    # CONFLICTO: O (Minutas de cocción rápida)
    # Orden de ejecución: R20 -> R15
    # ========================================================

    @Rule(Hecho(codigo='O'), salience=20)
    def r20_encender_plancha(self):
        print("[R20] Minutas en marcha: Se enciende la plancha o freidora anticipadamente.")
        self.declare(Hecho(codigo='AB'))

    # Esta regla exige dos hechos simultáneos para dispararse
    @Rule(Hecho(codigo='O'), Hecho(codigo='Q'), salience=15)
    def r15_entrega_menu_rapido(self):
        print("[R15] Platos y guarnición listos: El cliente recibe el menú rápido.")
        self.declare(Hecho(codigo='S'))

    # ========================================================
    # ENCADENAMIENTO DE LA PLANCHA (AB -> AC)
    # ========================================================

    @Rule(Hecho(codigo='AB'))
    def r21_charla_cliente(self):
        print("[R21] Plancha encendida: Se inicia charla con el cliente para distraerlo.")
        self.declare(Hecho(codigo='AC'))


# ========================================================
# EJECUCIÓN PASO A PASO
# ========================================================
if __name__ == "__main__":
    print("--- INICIANDO ASESOR VIRTUAL GASTRONÓMICO ---")
    
    motor = AsesorVirtualGastronomico()
    motor.reset()
    
    # NOTA: Para probar el nuevo flujo R1-R10, ahora debemos declarar A, B y G
    # (Lunes/Martes/Miércoles, oferta de carne y ausencia de ayudante).
    print(">> Ingresando Hechos Iniciales: A (Es Lunes), B (Hay oferta), G (Falta ayudante)\n")
    motor.declare(Hecho(codigo='A'))
    motor.declare(Hecho(codigo='B'))
    motor.declare(Hecho(codigo='G'))
    
    # El motor resuelve las reglas encadenadas de forma metódica
    motor.run()
    
    print("\n--- EJECUCIÓN FINALIZADA ---")
    print("Hechos guardados en la memoria de trabajo:")
    # Extraemos solo las letras para que sea fácil de leer en la terminal
    hechos_finales = [fact['codigo'] for fact in motor.facts.values() if 'codigo' in fact]
    print(hechos_finales)