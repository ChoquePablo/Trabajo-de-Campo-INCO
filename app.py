import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from motor import (
    AsesorVirtualGastronomico,
    Hecho,
    cargar_conocimiento_aprendido,
    guardar_nuevo_aprendizaje,
    eliminar_regla_aprendida,
    construir_menu_recomendado,
)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
PORT = 8000

# Estado en memoria del menú del día activo
ESTADO_SERVIDOR = {
    "menu_del_dia": None,
}


def procesar_recomendacion(datos):
    """
    Conecta las respuestas del chatbot HTML/JS con el motor de inferencia Experta
    en motor.py y devuelve el menú de platos concretos y su trazabilidad.
    """
    hechos = []

    if datos.get("inicio_semana"):
        hechos.append("A")
    if datos.get("oferta_carne"):
        hechos.append("B")
    if datos.get("clima") == "frio":
        hechos.append("C")
    elif datos.get("clima") == "calido":
        hechos.append("T")
    if datos.get("equipo") == "falta_ayudante":
        hechos.append("G")
    elif datos.get("equipo") == "demora_urgente":
        hechos.append("L")
    if datos.get("restriccion"):
        hechos.append("W")

    for hx in datos.get("hechos_extra", []):
        if hx not in hechos:
            hechos.append(hx)

    # Ejecutar motor de inferencia Experta + reglas aprendidas
    motor = AsesorVirtualGastronomico()
    motor.reset()
    for cod in hechos:
        motor.declare(Hecho(codigo=cod))
    motor.run()

    hechos_fin = motor.obtener_hechos_finales()
    propuesta = construir_menu_recomendado(
        hechos_fin,
        motor.platos_aprendidos_disparados,
        hechos_iniciales=hechos,
    )

    if not propuesta["platos"]:
        propuesta["platos"].append(
            {
                "nombre": "Pastel de Papas Casero / Pollo al Horno con Papas",
                "icono": "utensils",
                "categoria": "Menú Clásico del Día (Operación Normal)",
                "tiempo": "45 min",
                "rendimiento": "35 viandas estándar",
                "descripcion": "Jornada sin alertas climáticas ni falta de personal: ideal para el menú clásico de rotación diaria.",
                "tip": "Aprovechar que el equipo está completo para adelantar producción de mañana.",
                "regla_origen": "Base Estándar",
            }
        )

    resultado = {
        "hechos_iniciales": hechos,
        "hechos_finales": hechos_fin,
        "traza": list(motor.traza),
        "recomendaciones": list(motor.recomendaciones),
        "platos": propuesta["platos"],
        "descartados": propuesta["descartados"],
        "tips_operativos": propuesta["tips_operativos"],
        "recomendaciones_experta": propuesta["recomendaciones_experta"],
        "contingencia_automatica": ("L" in hechos_fin and "L" not in hechos),
    }
    ESTADO_SERVIDOR["menu_del_dia"] = resultado
    return resultado


class ChatbotHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silenciar logs repetitivos en consola
        pass

    def _enviar_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _servir_archivo(self, nombre_archivo, content_type):
        ruta = os.path.join(FRONTEND_DIR, nombre_archivo)
        if not os.path.exists(ruta):
            self.send_error(404, "Archivo no encontrado")
            return
        with open(ruta, "rb") as f:
            contenido = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(contenido)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.end_headers()
        self.wfile.write(contenido)

    def do_GET(self):
        ruta_limpia = self.path.split("?")[0]
        if ruta_limpia in ("/", "/index.html"):
            self._servir_archivo("index.html", "text/html; charset=utf-8")
        elif ruta_limpia == "/styles.css":
            self._servir_archivo("styles.css", "text/css; charset=utf-8")
        elif ruta_limpia == "/script.js":
            self._servir_archivo("script.js", "application/javascript; charset=utf-8")
        elif ruta_limpia == "/api/estado":
            aprendido = cargar_conocimiento_aprendido()
            self._enviar_json(
                {
                    "hechos_personalizados": aprendido.get("hechos_personalizados", {}),
                    "reglas_platos": aprendido.get("reglas_platos", []),
                    "menu_del_dia": ESTADO_SERVIDOR["menu_del_dia"],
                }
            )
        else:
            self.send_error(404, "Ruta no encontrada")

    def do_POST(self):
        ruta_limpia = self.path.split("?")[0]
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            datos = json.loads(raw)
        except json.JSONDecodeError:
            self._enviar_json({"ok": False, "error": "JSON inválido"}, status=400)
            return

        if ruta_limpia == "/api/recomendar":
            menu = procesar_recomendacion(datos)
            self._enviar_json(menu)
        elif ruta_limpia == "/api/aprender":
            nombre_plato = (datos.get("nombre_plato") or "").strip()
            descripcion_plato = (datos.get("descripcion_plato") or "").strip()
            if not nombre_plato or not descripcion_plato:
                self._enviar_json({"ok": False, "error": "Faltan datos obligatorios del plato"}, status=400)
                return
            nueva_regla = guardar_nuevo_aprendizaje(
                condicion_codigo=datos.get("condicion_codigo", "C"),
                condicion_descripcion=datos.get("condicion_descripcion", ""),
                es_hecho_nuevo=bool(datos.get("es_hecho_nuevo", False)),
                nombre_plato=nombre_plato,
                categoria=datos.get("categoria", "Plato Principal"),
                descripcion_plato=descripcion_plato,
                tiempo_estimado=datos.get("tiempo_estimado", "25 min"),
                consejo_cocina=datos.get("consejo_cocina", ""),
            )
            self._enviar_json({"ok": True, "regla": nueva_regla})
        else:
            self.send_error(404, "Endpoint no encontrado")

    def do_DELETE(self):
        ruta_limpia = self.path.split("?")[0]
        if ruta_limpia == "/api/menu":
            ESTADO_SERVIDOR["menu_del_dia"] = None
            self._enviar_json({"ok": True})
        elif ruta_limpia.startswith("/api/aprender/"):
            regla_id = ruta_limpia.split("/api/aprender/")[1].strip()
            if regla_id:
                eliminar_regla_aprendida(regla_id)
            self._enviar_json({"ok": True, "eliminada": regla_id})
        else:
            self.send_error(404, "Endpoint no encontrado")


if __name__ == "__main__":
    url = f"http://localhost:{PORT}"
    print("====================================================")
    print(" 🍲 CHEFBOT - ASESOR VIRTUAL GASTRONÓMICO (HTML/CSS)")
    print(f" 🚀 Servidor corriendo en: {url}")
    print(" (Presioná Ctrl + C en la terminal para detenerlo)")
    print("====================================================")
    try:
        webbrowser.open(url)
    except Exception:
        pass

    servidor = ThreadingHTTPServer(("127.0.0.1", PORT), ChatbotHTTPHandler)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        servidor.server_close()
