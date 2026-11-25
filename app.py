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

# Estado en memoria del menú del día activo y rotación de platos usados (como en ramaAriel)
ESTADO_SERVIDOR = {
    "menu_del_dia": None,
    "platos_usados": [],
}


def procesar_recomendacion(datos):
    """
    Conecta las respuestas del chatbot HTML/JS con el motor de inferencia Experta
    en motor.py y devuelve el menú de platos decididos por las reglas R33-R43 y su trazabilidad.
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

    # Ejecutar motor de inferencia Experta (R1-R31 + Reglas de Platos R33-R43 + Reglas Aprendidas)
    motor = AsesorVirtualGastronomico()
    motor.reset()
    for cod in hechos:
        motor.declare(Hecho(codigo=cod))
    motor.cargar_platos_usados(ESTADO_SERVIDOR["platos_usados"])
    motor.run()

    # Si todos los platos posibles para esta condición ya fueron usados en la rotación,
    # reiniciar el ciclo de rotación de platos usados y volver a correr para que no caiga siempre en el comodín
    if (
        len(motor.menus_sugeridos) == 1
        and motor.menus_sugeridos[0]["regla"] == "R43"
        and ESTADO_SERVIDOR["platos_usados"]
        and any(c in hechos for c in ("C", "T", "G", "L", "A", "B"))
    ):
        ESTADO_SERVIDOR["platos_usados"] = []
        motor.reset()
        for cod in hechos:
            motor.declare(Hecho(codigo=cod))
        motor.run()

    # Registrar el plato principal elegido hoy en platos_usados para rotar en la siguiente consulta (como en ramaAriel)
    for m in motor.menus_sugeridos:
        if m.get("es_principal") and m["plato"] not in ESTADO_SERVIDOR["platos_usados"]:
            ESTADO_SERVIDOR["platos_usados"].append(m["plato"])

    hechos_fin = motor.obtener_hechos_finales()
    propuesta = construir_menu_recomendado(
        hechos_fin,
        motor.platos_aprendidos_disparados,
        hechos_iniciales=hechos,
        menus_reglas=motor.menus_sugeridos,
    )

    resultado = {
        "respuestas": {
            "inicio_semana": bool(datos.get("inicio_semana")),
            "clima": datos.get("clima", "templado"),
            "oferta_carne": bool(datos.get("oferta_carne")),
            "equipo": datos.get("equipo", "normal"),
            "restriccion": bool(datos.get("restriccion")),
            "hechos_extra": list(datos.get("hechos_extra", [])),
        },
        "hechos_iniciales": hechos,
        "hechos_finales": hechos_fin,
        "traza": list(motor.traza),
        "recomendaciones": list(motor.recomendaciones),
        "platos": propuesta["platos"],
        "descartados": propuesta["descartados"],
        "tips_operativos": propuesta["tips_operativos"],
        "recomendaciones_experta": propuesta["recomendaciones_experta"],
        "contingencia_automatica": ("L" in hechos_fin and "L" not in hechos),
        "platos_usados_rotacion": list(ESTADO_SERVIDOR["platos_usados"]),
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
        elif ruta_limpia == "/api/aprender/eliminar":
            regla_id = (datos.get("id") or "").strip()
            if regla_id:
                eliminar_regla_aprendida(regla_id)
            self._enviar_json({"ok": True, "eliminada": regla_id})
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
