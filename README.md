# Asesor Virtual Gastronómico — Sistema Experto (INCO)

Sistema Basado en Conocimiento (SBC) desarrollado para asistir en la **toma de decisiones diarias de una cocina de viandas** frente a múltiples variables concurrentes: clima, día de la semana, ofertas de carnes en frigorífico, disponibilidad de personal, tiempos de elaboración y restricciones alimentarias de los clientes.

---

## Cómo Ejecutar el Programa

El proyecto utiliza un servidor web nativo de Python (`app.py`) que sirve la interfaz **HTML5 + CSS3 + JavaScript** y se conecta directamente con el motor de inferencia **`Experta`** (`motor.py`).

### 1. Comando estándar (si Python está en el `PATH`)

```bash
python app.py
```

### 2. Comando con ruta directa en Windows (CMD / Cmder)

```cmd
"C:\Users\pablo\AppData\Local\Python\bin\python.exe" app.py
```

### 3. Comando con ruta directa en Windows (PowerShell)

```powershell
& "C:\Users\pablo\AppData\Local\Python\bin\python.exe" app.py
```

Al ejecutarlo:
1. Se iniciará el servidor local en **`http://localhost:8000`**.
2. Se abrirá automáticamente el navegador web con la aplicación lista para usar.
3. Para detener el servidor, presioná **`Ctrl + C`** en la terminal.

---

## Requisitos Previos

* **Python 3.10+** (incluye parche de compatibilidad automática para `collections.abc` en Python 3.10–3.15).
* Librería **`experta`**:

```bash
pip install experta
```

*(Con la ruta directa en Windows)*:
```cmd
"C:\Users\pablo\AppData\Local\Python\bin\python.exe" -m pip install experta
```

---

## Arquitectura y Conexión de Archivos

```text
Trabajo-de-Campo-INCO/
├── app.py                        # Servidor HTTP y API REST que conecta el frontend con motor.py
├── motor.py                      # Motor de inferencia Experta (31 reglas), catálogo de platos y aprendizaje
├── conocimiento_aprendido.json   # Base de datos JSON generada dinámicamente con hechos/platos aprendidos
├── asistenteGastronomico.py      # Script base inicial de prueba en consola
├── README.md                     # Documentación del proyecto
└── frontend/
    ├── index.html                # Estructura de la aplicación web responsiva
    ├── styles.css                # Estilos de escritorio, tablet y móvil
    └── script.js                 # Lógica interactiva del asistente y llamadas fetch() a la API
```

### Flujo de comunicación:
1. **`frontend/script.js`** captura las respuestas de la experta en la entrevista paso a paso o los comandos del usuario (`1` al `6`) y envía peticiones HTTP JSON al servidor local.
2. **`app.py`** expone los endpoints:
   - `GET /api/estado`: Devuelve las reglas aprendidas y el menú del día activo.
   - `POST /api/recomendar`: Traduce las respuestas a hechos iniciales (`Hecho(codigo=...)`), ejecuta `AsesorVirtualGastronomico.run()` y devuelve los platillos recomendados, platos descartados, consejos operativos y la traza de inferencia.
   - `DELETE /api/menu`: Limpia el menú del día activo.
   - `POST /api/aprender`: Registra nuevos hechos y platillos en `conocimiento_aprendido.json`.
3. **`motor.py`** procesa el encadenamiento hacia adelante (*forward chaining*) sobre las **31 reglas de producción (`R1`–`R31`)** más las **reglas aprendidas (`RA1+`)** y construye la carta de platillos con `construir_menu_recomendado()`.

---

## Funcionamiento del Sistema Experto

### 1. Formalismo y Motor de Inferencia
* **Formalismo**: Sistema de Producción (Reglas `SI <antecedente> ENTONCES <consecuente>`).
* **Encadenamiento**: Hacia adelante (*Forward Chaining*), partiendo de los hechos observables de la jornada hasta deducir decisiones de compra, producción, contingencia y menú.
* **Resolución de Conflictos (`salience`)**:
  - **Conflicto en `L` (Contingencia por demora)**: `R12 (40) → R11 (30) → R18 (20) → R19 (10)`
  - **Conflicto en `O` (Minutas rápidas)**: `R20 (20) → R15 (10)`
  - **Conflicto en `C` (Clima frío)**: `R27 (30) → R22 (20) → R31 (10)`
  - **Conflicto en `E` (Ingrediente versátil)**: `R3 (20) → R26 (10)`
  - **Conflicto en `AJ` (Demanda de platos de olla)**: `R28 (20) → R29 (10)`

### 2. Módulos del Asistente Interactivo (Opciones 1 a 6)
Podés operar el asistente haciendo clic en el panel lateral, en las tarjetas en pantalla o escribiendo el número en la barra inferior:

1. **`1. Recomendar Menú`**: Realiza una entrevista rápida de 5 pasos (día de la semana, clima, oferta de carne en frigorífico, asistencia de la ayudante/tiempos y restricciones alimentarias) y genera una propuesta de **platillos concretos** con tiempos de cocción, rendimiento y criterios expertos.
2. **`2. Mostrar Menú del Día`**: Muestra los platillos confirmados para la jornada actual, los platos descartados y las notas operativas de cocina.
3. **`3. Borrar Menú del Día`**: Limpia la pizarra activa para iniciar una nueva planificación.
4. **`4. Trazabilidad (XAI)`**: Muestra la explicación paso a paso de todas las reglas disparadas en orden de prioridad y el estado inicial y final de la Memoria de Trabajo.
5. **`5. Agregar Hecho / Plato (Aprendizaje Continuo)`**: Permite enseñarle al sistema nuevos hechos/situaciones de la cocina y asociarles un nuevo platillo recomendado, guardándolos de forma persistente.
6. **`6. Conocimiento Aprendido`**: Lista todas las reglas dinámicas (`RA1`, `RA2`, ...) incorporadas por la experta.
