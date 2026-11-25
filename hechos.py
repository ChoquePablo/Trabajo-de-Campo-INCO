# hechos.py
import collections
import collections.abc

# Parche de compatibilidad para Python 3.10+
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping

from experta import Fact

class Estado(Fact):
    """Representa un hecho activo en la Base de Hechos (ej: Estado(codigo='A'))."""
    pass

class MenuSugerido(Fact):
    """Representa un plato concreto recomendado por el motor."""
    pass

class PlatoUsado(Fact):
    """Registra platos ya asignados en días anteriores para evitar repeticiones."""
    pass

class MenuPrincipalDefinido(Fact):
    """Bandera interna para asegurar un único plato principal por día."""
    pass

# Diccionario de hechos extraído de la Actividad 4
DESCRIPCION_HECHOS = {
    "A": "Es Lunes, Martes o Miércoles.",
    "B": "Hay oferta de cortes de carne (pieza entera) en el frigorífico.",
    "C": "El clima es frío.",
    "D": "Se compra la pieza de carne entera.",
    "E": "Se clasifica como un 'ingrediente versátil'.",
    "F": "Se planifican al menos dos platos diferentes (ej. guiso y bifes).",
    "G": "La ayudante de cocina avisa que no asiste.",
    "H": "La cocina, espacios y ollas NO están limpios a primera hora.",
    "I": "Se retrasa el inicio de la elaboración (Lucía debe limpiar sola).",
    "J": "El menú planificado requiere demasiado tiempo de elaboración relativo.",
    "K": "Se descarta el menú diario estándar (ej. el guiso).",
    "L": "Se activa el protocolo de contingencia por imprevisto/demora.",
    "M": "Se congela la carne un poco para filetear y reducir desperdicios.",
    "N": "Se filetea la carne en la cocina.",
    "O": "Se preparan minutas de cocción rápida.",
    "P": "Se necesita preparar arroz para tener de reserva en la heladera.",
    "Q": "No se le agrega cebolla ni verduras frescas al arroz.",
    "R": "El margen de ganancia aumenta.",
    "S": "El cliente recibe el menú rápido y no se echa a perder la guarnición.",
    "T": "El clima es cálido/verano.",
    "U": "Se descartan menús calientes.",
    "V": "Se sugieren comidas frescas.",
    "W": "El cliente tiene restricciones alimentarias.",
    "Y": "Se prepara menú paralelo básico.",
    "Z": "Se ofrece un plato de entrada rápido (sopa).",
    "AA": "Se le sugiere al cliente agendar el número para reservar por mensaje.",
    "AB": "Se enciende la plancha o freidora de forma anticipada.",
    "AC": "Se inicia una charla con el cliente para distraerlo mientras se cocina.",
    "AD": "Se planifica un plato de olla de alto volumen (ej. Locro).",
    "AE": "Se ocupan todas las hornallas de la cocina simultáneamente.",
    "AF": "Se observa el precio de los vegetales en el mercado.",
    "AG": "Se compra y reserva esa verdura si el precio es bajo.",
    "AH": "Se deshuesa/prepara una parte para el menú actual (ej. pechuga para suprema).",
    "AI": "Se guarda otra parte de la pieza para el menú del día siguiente (ej. cuartos traseros).",
    "AJ": "Aumenta la demanda de platos de olla (guisos, lentejas, locro).",
    "AK": "Se descartan las comidas frías o la milanesa estándar como menú principal.",
    "AL": "Se utiliza equipamiento de gran volumen (ollas grandes).",
    "AM": "Se calcula un rendimiento masivo (entre 50 y 70 platos por preparación).",
    "AO": "Se aprovechan cortes de oferta con hueso específicos para caldos (ej. osobuco/puchero)."
}

if __name__ == "__main__":
    print(f"Entorno OK. Experta importado correctamente. Hechos cargados: {len(DESCRIPCION_HECHOS)}")