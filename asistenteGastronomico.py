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
    @Rule(Hecho(codigo='O'), Hecho(codigo='Q'), salience=10)
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
    
    # Simulamos que ocurre el imprevisto (Hecho L)
    print(">> Ingresando Hecho Inicial: L (Contingencia por demora)\n")
    motor.declare(Hecho(codigo='L'))
    
    # El motor resuelve las reglas encadenadas de forma metódica
    motor.run()
    
    print("\n--- EJECUCIÓN FINALIZADA ---")
    print("Hechos guardados en la memoria de trabajo:")
    # Extraemos solo las letras para que sea fácil de leer en la terminal
    hechos_finales = [fact['codigo'] for fact in motor.facts.values() if 'codigo' in fact]
    print(hechos_finales)