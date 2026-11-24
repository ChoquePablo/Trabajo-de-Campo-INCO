// ========================================================
// CATÁLOGO DE ICONOS SVG (ADAPTADOS A LA PALETA DE COLOR)
// ========================================================
const SVG = {
    chef: `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 13.87A4 4 0 0 1 7.41 6a5.11 5.11 0 0 1 1.05-1.54 5 5 0 0 1 7.08 0A5.11 5.11 0 0 1 16.59 6 4 4 0 0 1 18 13.87V21H6Z"/><line x1="6" y1="17" x2="18" y2="17"/></svg>`,
    sparkle: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/></svg>`,
    calendar: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`,
    trash: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>`,
    network: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>`,
    plusCircle: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>`,
    book: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>`,
    arrowRight: `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`,
    clock: `<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    layers: `<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>`,
    lightbulb: `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>`,
    snow: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/><path d="m20 16-4-4 4-4"/><path d="m4 8 4 4-4 4"/><path d="m16 4-4 4-4-4"/><path d="m8 20 4-4 4 4"/></svg>`,
    sun: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>`,
    cloud: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>`,
    checkCircle: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`,
    xCircle: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
    alertTriangle: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
    users: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
    leaf: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>`,
    flame: `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>`,
    utensils: `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/></svg>`,
    soup: `<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21a9 9 0 0 0 9-9H3a9 9 0 0 0 9 9Z"/><path d="M7 21h10"/><path d="M19.5 12 22 6"/><path d="M16.25 3c.27.1.8.53.75 1.36-.06.83-.93 1.2-1 2.02-.05.78.34 1.24.73 1.62"/><path d="M11.25 3c.27.1.8.53.74 1.36-.05.83-.93 1.2-.98 2.02-.06.78.33 1.24.72 1.62"/><path d="M6.25 3c.27.1.8.53.75 1.36-.06.83-.93 1.2-1 2.02-.05.78.34 1.24.74 1.62"/></svg>`,
    save: `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>`,
};

function obtenerIconoPlato(iconoClave, categoria = "") {
    const cat = (categoria || "").toLowerCase();
    if (iconoClave === "soup" || cat.includes("sopa") || cat.includes("entrada") || cat.includes("caldo")) {
        return SVG.soup;
    }
    if (iconoClave === "leaf" || cat.includes("fresco") || cat.includes("restricci") || cat.includes("verano")) {
        return SVG.leaf;
    }
    if (iconoClave === "flame" || cat.includes("olla") || cat.includes("frío")) {
        return SVG.flame;
    }
    if (iconoClave === "sparkle" || cat.includes("aprendido")) {
        return SVG.sparkle;
    }
    return SVG.utensils;
}

function limpiarPrefijoEmoji(texto) {
    const sinEmoji = (texto || "").replace(/^[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}\s]+/u, "");
    return sinEmoji.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
}

function escaparHtml(str) {
    return String(str || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function deshabilitarControlesPaso(btnEl) {
    if (!btnEl) return;
    const contenedor = btnEl.closest(".msg-card");
    if (!contenedor) return;
    contenedor.querySelectorAll("button.opt-btn, input.chk-hecho-aprendido").forEach((el) => {
        el.disabled = true;
        if (el.tagName === "BUTTON") {
            el.style.opacity = "0.6";
            el.style.pointerEvents = "none";
        }
    });
}

// ========================================================
// ESTADO DE LA APLICACIÓN EN EL CLIENTE
// ========================================================
let estadoSistema = {
    hechosPersonalizados: {},
    reglasAprendidas: [],
    menuDelDia: null,
};

let entrevista = {
    activa: false,
    paso: 0,
    respuestas: {
        inicio_semana: false,
        clima: "templado",
        oferta_carne: false,
        equipo: "normal",
        restriccion: false,
        hechos_extra: [],
    },
};

function horaActual() {
    const d = new Date();
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function toggleSidebar() {
    const sb = document.getElementById("app-sidebar");
    const ov = document.getElementById("sidebar-overlay");
    if (sb && ov) {
        sb.classList.toggle("open");
        ov.classList.toggle("open");
    }
}

function cerrarSidebarMovil() {
    const sb = document.getElementById("app-sidebar");
    const ov = document.getElementById("sidebar-overlay");
    if (sb && ov) {
        sb.classList.remove("open");
        ov.classList.remove("open");
    }
}

function scrollAlFinal() {
    const vp = document.getElementById("chat-viewport");
    setTimeout(() => {
        vp.scrollTop = vp.scrollHeight;
    }, 40);
}

function agregarBurbuja(rol, htmlContenido) {
    const stream = document.getElementById("chat-stream");
    const row = document.createElement("div");
    row.className = `msg-row ${rol === "user" ? "msg-user" : "msg-bot"}`;

    if (rol === "user") {
        row.innerHTML = `<div class="msg-card">${htmlContenido}</div>`;
    } else {
        row.innerHTML = `
            <div class="msg-avatar">${SVG.chef}</div>
            <div class="msg-card">
                <div class="msg-header-meta">
                    <span>Asesor Gastronómico Inteligente</span>
                    <span>${horaActual()}</span>
                </div>
                <div>${htmlContenido}</div>
            </div>
        `;
    }

    stream.appendChild(row);
    scrollAlFinal();
}

function limpiarConversacion() {
    const stream = document.getElementById("chat-stream");
    if (stream) stream.innerHTML = "";
    mostrarMenuBienvenida();
    cerrarSidebarMovil();
}

function actualizarCabecera() {
    const cantAprendidas = estadoSistema.reglasAprendidas.length;
    const counterEl = document.getElementById("rules-counter");
    if (counterEl) {
        counterEl.textContent = `31 reglas base + ${cantAprendidas} aprendidas`;
    }

    const pillEl = document.getElementById("menu-status-pill");
    const pillText = document.getElementById("menu-status-text");
    if (pillEl && pillText) {
        if (estadoSistema.menuDelDia && estadoSistema.menuDelDia.platos?.length) {
            pillText.textContent = `Menú del Día Activo (${estadoSistema.menuDelDia.platos.length} platos)`;
            pillEl.className = "status-pill pill-active";
        } else {
            pillText.textContent = "Sin Menú Activo";
            pillEl.className = "status-pill pill-empty";
        }
    }
}

function obtenerReglasEliminadasLocal() {
    try {
        const raw = localStorage.getItem("chefbot_reglas_eliminadas");
        return raw ? new Set(JSON.parse(raw)) : new Set();
    } catch (_) {
        return new Set();
    }
}

function registrarReglaEliminadaLocal(reglaId) {
    try {
        const set = obtenerReglasEliminadasLocal();
        set.add(reglaId);
        localStorage.setItem("chefbot_reglas_eliminadas", JSON.stringify([...set]));
    } catch (_) {}
}

async function sincronizarEstadoServidor() {
    try {
        const res = await fetch("/api/estado");
        const data = await res.json();
        const eliminadasLocal = obtenerReglasEliminadasLocal();
        const reglasFiltradas = (data.reglas_platos || []).filter((r) => !eliminadasLocal.has(r.id));

        const codigosActivos = new Set(reglasFiltradas.map((r) => r.condicion_codigo));
        const hechosPers = {};
        for (const [k, v] of Object.entries(data.hechos_personalizados || {})) {
            if (codigosActivos.has(k)) {
                hechosPers[k] = v;
            }
        }

        estadoSistema.hechosPersonalizados = hechosPers;
        estadoSistema.reglasAprendidas = reglasFiltradas;
        if (data.menu_del_dia) {
            estadoSistema.menuDelDia = data.menu_del_dia;
            try {
                localStorage.setItem("chefbot_menu_del_dia", JSON.stringify(data.menu_del_dia));
            } catch (_) {}
        } else if (!estadoSistema.menuDelDia) {
            try {
                const guardado = localStorage.getItem("chefbot_menu_del_dia");
                if (guardado) estadoSistema.menuDelDia = JSON.parse(guardado);
            } catch (_) {}
        }
        actualizarCabecera();
    } catch (e) {
        console.error("Error sincronizando estado:", e);
    }
}

// ========================================================
// RENDERIZADO DE PLATOS Y RECOMENDACIONES DE LA EXPERTA
// ========================================================
function construirRecomendacionesDesdeHechos(hechosFin = [], hechosIn = []) {
    const h = new Set(hechosFin);
    const hIn = new Set(hechosIn);
    const recs = {
        insumos_y_cortes: [],
        cocina_y_equipamiento: [],
        clientes_y_servicio: [],
    };

    if (h.has("D")) {
        recs.insumos_y_cortes.push({ regla: "R1", texto: "Comprar la pieza de carne entera en el frigorífico aprovechando que es inicio de semana (Lun-Mié) y hay oferta." });
    }
    if (h.has("E")) {
        recs.insumos_y_cortes.push({ regla: "R2", texto: "Clasificar la pieza comprada como un 'ingrediente versátil' apto para múltiples preparaciones." });
    }
    if (h.has("F")) {
        recs.insumos_y_cortes.push({ regla: "R3", texto: "Planificar al menos dos platos diferentes a partir de la pieza (ej. guiso y bifes)." });
    }
    if (h.has("M")) {
        recs.insumos_y_cortes.push({ regla: "R9", texto: "Congelar la carne un poco antes de cortarla para facilitar el fileteado y reducir desperdicios." });
    }
    if (h.has("N")) {
        recs.insumos_y_cortes.push({ regla: "R10", texto: "Filetear la carne directamente en la cocina." });
    }
    if (h.has("R")) {
        recs.insumos_y_cortes.push({ regla: "R14", texto: "Aprovechar el rendimiento del fileteado propio: el margen de ganancia aumenta." });
    }
    if (h.has("AH") || h.has("AI")) {
        recs.insumos_y_cortes.push({ regla: "R26", texto: "Deshuesar/preparar una parte para el menú actual (ej. pechuga para suprema) y guardar/freezar otra parte para el día siguiente (ej. cuartos traseros)." });
    }
    if (h.has("P")) {
        recs.insumos_y_cortes.push({ regla: "R12", texto: "Preparar arroz blanco para tener de reserva en la heladera." });
    }
    if (h.has("Q")) {
        recs.insumos_y_cortes.push({ regla: "R13", texto: "NO agregar cebolla ni verduras frescas al arroz de reserva para que no fermente ni se eche a perder." });
    }
    if (h.has("AO")) {
        recs.insumos_y_cortes.push({ regla: "R31", texto: "Aprovechar cortes de oferta con hueso específicos para caldos y sopas (ej. osobuco o puchero)." });
    }
    if (h.has("AF")) {
        recs.insumos_y_cortes.push({ regla: "R24", texto: "Observar y monitorear el precio de los vegetales en el mercado (ej. espinaca)." });
    }
    if (h.has("AG")) {
        recs.insumos_y_cortes.push({ regla: "R25", texto: "Comprar y reservar esa verdura si el precio es bajo para asegurar la vianda especial." });
    }
    if (hIn.has("B") && !hIn.has("A")) {
        recs.insumos_y_cortes.push({
            regla: "R1 (A+B)",
            texto: "Marcaste oferta de carne (B), pero hoy es Jueves a Domingo (no A). Según R1, la compra y fileteado de pieza entera se activa cuando además es Lunes, Martes o Miércoles (A).",
        });
    }

    if (h.has("H")) {
        recs.cocina_y_equipamiento.push({ regla: "R4", texto: "Atención: la cocina, espacios y ollas NO están limpios a primera hora por ausencia de la ayudante." });
    }
    if (h.has("I")) {
        recs.cocina_y_equipamiento.push({ regla: "R5", texto: "Reorganizar cronograma: se retrasa el inicio de la elaboración porque Lucía debe limpiar sola." });
    }
    if (h.has("J")) {
        recs.cocina_y_equipamiento.push({ regla: "R6", texto: "El menú planificado de varios platos requiere demasiado tiempo de elaboración relativo frente al retraso." });
    }
    if (h.has("L")) {
        recs.cocina_y_equipamiento.push({ regla: "R8", texto: "Activar el protocolo de contingencia por imprevisto/demora en la cocina." });
    }
    if (h.has("AB")) {
        recs.cocina_y_equipamiento.push({ regla: "R20", texto: "Encender la plancha o freidora de forma anticipada para agilizar la salida de minutas." });
    }
    if (h.has("AJ")) {
        recs.cocina_y_equipamiento.push({ regla: "R27", texto: "Prever aumento en la demanda de platos de olla (guisos, lentejas, locro) por el frío." });
    }
    if (h.has("AD")) {
        recs.cocina_y_equipamiento.push({ regla: "R22", texto: "Planificar un plato de olla de alto volumen (ej. Locro)." });
    }
    if (h.has("AL")) {
        recs.cocina_y_equipamiento.push({ regla: "R29", texto: "Utilizar equipamiento de gran volumen (ollas grandes)." });
    }
    if (h.has("AM")) {
        recs.cocina_y_equipamiento.push({ regla: "R30", texto: "Calcular un rendimiento masivo de entre 50 y 70 platos por preparación." });
    }
    if (h.has("AE")) {
        recs.cocina_y_equipamiento.push({ regla: "R23", texto: "Organizar el espacio previendo que se ocuparán todas las hornallas de la cocina simultáneamente." });
    }

    if (h.has("Z")) {
        recs.clientes_y_servicio.push({ regla: "R18", texto: "Ofrecer un plato de entrada rápido (sopa) al cliente mientras sale el plato principal." });
    }
    if (h.has("AC")) {
        recs.clientes_y_servicio.push({ regla: "R21", texto: "Iniciar una charla con el cliente en mostrador para distraerlo mientras se termina de cocinar." });
    }
    if (h.has("S")) {
        recs.clientes_y_servicio.push({ regla: "R15", texto: "Entregar el menú rápido al cliente asegurando que no se eche a perder la guarnición." });
    }
    if (h.has("AA")) {
        recs.clientes_y_servicio.push({ regla: "R19", texto: "Sugerir al cliente agendar el número de contacto para reservar por mensaje en el futuro." });
    }
    if (h.has("Y")) {
        recs.clientes_y_servicio.push({ regla: "R17", texto: "Preparar un menú paralelo básico adaptado al cliente con restricciones alimentarias." });
    }
    if (h.has("V")) {
        recs.clientes_y_servicio.push({ regla: "R16", texto: "Sugerir activamente comidas frescas a los clientes durante la jornada de calor." });
    }

    return recs;
}

function renderizarRecomendacionesExperta(recsExperta) {
    if (!recsExperta) return "";

    const grupos = [
        {
            clave: "insumos_y_cortes",
            titulo: "Compras, Fileteado, Congelado y Conservación",
            icono: SVG.utensils,
        },
        {
            clave: "cocina_y_equipamiento",
            titulo: "Organización de Cocina, Equipamiento y Tiempos",
            icono: SVG.flame,
        },
        {
            clave: "clientes_y_servicio",
            titulo: "Atención al Cliente y Servicio",
            icono: SVG.users,
        },
    ];

    let columnasHtml = "";
    for (const g of grupos) {
        const lista = recsExperta[g.clave] || [];
        if (lista.length === 0) continue;

        const itemsHtml = lista
            .map(
                (item) => `
                <div class="expert-item">
                    <span class="expert-rule-badge">${item.regla}</span>
                    <div>${item.texto}</div>
                </div>
            `
            )
            .join("");

        columnasHtml += `
            <div class="expert-group-card">
                <div class="expert-group-header">
                    ${g.icono}
                    <span>${g.titulo}</span>
                </div>
                ${itemsHtml}
            </div>
        `;
    }

    if (!columnasHtml) return "";

    return `
        <div class="expert-recs-section">
            <div class="section-heading">
                <span class="svg-badge svg-badge-teal">${SVG.lightbulb}</span>
                <span>Recomendaciones Operativas y de Preparación de la Experta</span>
            </div>
            <div class="expert-recs-grid">
                ${columnasHtml}
            </div>
        </div>
    `;
}

function renderizarTarjetasPlatos(menuOrPlatos, descartadosArg = [], tipsArg = [], recsExpertaArg = null) {
    const esObjetoMenu = menuOrPlatos && !Array.isArray(menuOrPlatos);
    const hechosFin = esObjetoMenu ? (menuOrPlatos.hechos_finales || []) : [];
    const hechosIn = esObjetoMenu ? (menuOrPlatos.hechos_iniciales || []) : [];
    const hSet = new Set([...hechosFin, ...hechosIn]);
    const hayDemora = ["G", "H", "I", "J", "K", "L"].some((cod) => hSet.has(cod));
    const eliminadasLocal = obtenerReglasEliminadasLocal();

    let platos = esObjetoMenu ? [...(menuOrPlatos.platos || [])] : [...(menuOrPlatos || [])];
    let descartados = esObjetoMenu ? [...(menuOrPlatos.descartados || [])] : [...descartadosArg];

    // Filtrar platos de reglas aprendidas que hayan sido eliminadas
    platos = platos.filter((p) => !eliminadasLocal.has(p.regla_origen));

    // Si hay demora / falta de ayudante (G, I, K, L), filtrar Locro y Guisos largos (aunque el servidor viejo no se haya reiniciado)
    if (hayDemora) {
        const platosLargos = [];
        platos = platos.filter((p) => {
            const n = (p.nombre || "").toLowerCase();
            const esOllaLarga =
                n.includes("locro") ||
                n.includes("guiso de lentejas") ||
                n.includes("puchero") ||
                (n.includes("guiso casero") && n.includes("bifes"));
            if (esOllaLarga) {
                platosLargos.push(p.nombre);
                return false;
            }
            return true;
        });

        if (platosLargos.length > 0) {
            const yaTieneAvisoLocro = descartados.some((d) => d.toLowerCase().includes("locro"));
            if (!yaTieneAvisoLocro) {
                descartados.push(
                    "<b>Locro y Guisos de larga cocción (90-120 min) descartados hoy por demora:</b> " +
                    "debido al retraso en cocina / falta de ayudante, no hay tiempo para platos de olla largos; se priorizan minutas rápidas."
                );
            }
        }

        // Asegurar que haya al menos una minuta rápida si se filtraron los platos de olla por demora
        const tieneMinuta = platos.some((p) => (p.nombre || "").toLowerCase().includes("milanesas") || (p.nombre || "").toLowerCase().includes("costeletas"));
        if (!tieneMinuta) {
            platos.unshift({
                nombre: "Milanesas o Bifes a la Plancha con Arroz Blanco",
                icono: "utensils",
                categoria: "Plato Principal Rápido (Contingencia por Demora)",
                tiempo: "12 - 15 min",
                rendimiento: "Salida inmediata",
                descripcion: "Minutas de cocción rápida con arroz blanco de reserva para resolver la demora en la cocina.",
                tip: "Encender la plancha anticipadamente y acompañar con arroz cocinado sin cebolla ni verduras frescas.",
                regla_origen: hSet.has("L") ? "R11 + R12 + R13" : "R4 + R5 (Retraso I)",
            });
        }
    }

    const recsExperta = esObjetoMenu
        ? (menuOrPlatos.recomendaciones_experta ||
           construirRecomendacionesDesdeHechos(hechosFin, hechosIn))
        : recsExpertaArg;

    let html = `<div class="dishes-grid">`;

    for (const p of platos) {
        const svgPlato = obtenerIconoPlato(p.icono, p.categoria);
        html += `
            <div class="dish-card">
                <div>
                    <div class="dish-badge-row">
                        <span class="dish-category">${escaparHtml(p.categoria)}</span>
                        <span class="dish-rule-tag">${escaparHtml(p.regla_origen)}</span>
                    </div>
                    <div class="dish-title-row">
                        <div class="dish-icon-box">${svgPlato}</div>
                        <div class="dish-title">${escaparHtml(p.nombre)}</div>
                    </div>
                    <div class="dish-meta">
                        <span class="meta-item">${SVG.clock} Cocción: ${escaparHtml(p.tiempo)}</span>
                        <span class="meta-item">${SVG.layers} Rinde: ${escaparHtml(p.rendimiento)}</span>
                    </div>
                    <div class="dish-desc">${escaparHtml(p.descripcion)}</div>
                </div>
                <div class="dish-tip">
                    ${SVG.lightbulb}
                    <div><b>Criterio experto:</b> ${escaparHtml(p.tip)}</div>
                </div>
            </div>
        `;
    }
    html += `</div>`;

    if (descartados && descartados.length) {
        const items = descartados
            .map((d) => `<li>${SVG.xCircle} <span>${limpiarPrefijoEmoji(d)}</span></li>`)
            .join("");
        html += `
            <div class="discard-box">
                <div class="box-title">${SVG.alertTriangle} <span>Platos descartados en esta jornada:</span></div>
                <ul class="box-list">${items}</ul>
            </div>
        `;
    }

    html += renderizarRecomendacionesExperta(recsExperta);

    return html;
}

function crearBotonOpcion(onclickStr, svgIcon, texto, subtextoAccion = "") {
    return `
        <button class="opt-btn" onclick="${onclickStr}">
            <span class="opt-btn-left">
                <span class="opt-icon">${svgIcon}</span>
                <span>${texto}</span>
            </span>
            ${SVG.arrowRight}
        </button>
    `;
}

function mostrarMenuBienvenida() {
    agregarBurbuja(
        "bot",
        `
        <div class="section-heading">
            <span class="svg-badge">${SVG.chef}</span>
            <span>Sistema Inteligente de Planificación Gastronómica</span>
        </div>
        <p style="margin-top:6px; color:#475569;">
            Seleccioná una operación desde el panel lateral, haciendo clic en una tarjeta o escribiendo el número (<b>1 al 6</b>):
        </p>
        <div class="inline-options">
            ${crearBotonOpcion("ejecutarOpcion(1)", SVG.utensils, "1. Recomendar menú del día")}
            ${crearBotonOpcion("ejecutarOpcion(2)", SVG.calendar, "2. Mostrar menú del día activo")}
            ${crearBotonOpcion("ejecutarOpcion(3)", SVG.trash, "3. Borrar menú del día")}
            ${crearBotonOpcion("ejecutarOpcion(4)", SVG.network, "4. Ver trazabilidad (Reglas disparadas)")}
            ${crearBotonOpcion("ejecutarOpcion(5)", SVG.plusCircle, "5. Enseñar nuevo hecho / plato")}
            ${crearBotonOpcion("ejecutarOpcion(6)", SVG.book, "6. Ver conocimiento aprendido")}
        </div>
        `
    );
}

// ========================================================
// FLUJO DE ENTREVISTA PASO A PASO (OPCIÓN 1)
// ========================================================
async function iniciarEntrevista() {
    await sincronizarEstadoServidor();

    // Si ya existe un Menú del Día activo con platos, solicitar confirmación/eliminación previa
    if (estadoSistema.menuDelDia && estadoSistema.menuDelDia.platos && estadoSistema.menuDelDia.platos.length > 0) {
        mostrarAvisoMenuExistente();
        return;
    }

    ejecutarPasoInicialEntrevista();
}

function mostrarAvisoMenuExistente() {
    const cantPlatos = estadoSistema.menuDelDia.platos.length;
    agregarBurbuja(
        "bot",
        `
        <div class="section-heading">
            <span class="svg-badge svg-badge-amber">${SVG.calendar}</span>
            <span>Atención: Ya existe un Menú del Día registrado</span>
        </div>
        <div style="margin-top:8px; line-height:1.5; color:#334155;">
            Actualmente ya tenés un <b>Menú del Día activo</b> en la cocina con <b>${cantPlatos} plato(s) recomendados</b>.<br>
            Para generar una nueva recomendación con un contexto o condiciones distintas de la jornada, 
            primero es necesario <b>eliminar el menú anterior</b> para no sobreescribir ni mezclar las comandas planificadas.
        </div>
        <div style="margin-top:12px; display:flex; flex-direction:column; gap:8px;">
            ${crearBotonOpcion("confirmarReemplazoMenu()", SVG.trash, "Eliminar menú actual y pedir nueva recomendación")}
            ${crearBotonOpcion("mostrarMenuDelDia()", SVG.calendar, "Ver menú activo actual")}
            ${crearBotonOpcion("cancelarNuevaRecomendacion()", SVG.xCircle, "Mantener menú actual y cancelar")}
        </div>
        `
    );
}

async function confirmarReemplazoMenu() {
    await fetch("/api/menu", { method: "DELETE" });
    estadoSistema.menuDelDia = null;
    try {
        localStorage.removeItem("chefbot_menu_del_dia");
    } catch (_) {}
    actualizarCabecera();

    agregarBurbuja(
        "bot",
        `
        <div class="section-heading">
            <span class="svg-badge svg-badge-teal">${SVG.checkCircle}</span>
            <span>Menú anterior eliminado de la pizarra</span>
        </div>
        <p style="margin-top:4px; color:#475569;">Iniciando el asistente de planificación para registrar las nuevas condiciones del día...</p>
        `
    );

    ejecutarPasoInicialEntrevista();
}

function cancelarNuevaRecomendacion() {
    agregarBurbuja(
        "bot",
        `
        <div class="section-heading">
            <span class="svg-badge">${SVG.chef}</span>
            <span>Operación cancelada</span>
        </div>
        <p style="margin-top:6px; color:#475569;">
            Se mantiene el Menú del Día previamente registrado sin modificaciones. Podés consultarlo con la opción <b>2. Mostrar menú del día</b>.
        </p>
        `
    );
}

function ejecutarPasoInicialEntrevista() {
    entrevista.activa = true;
    entrevista.paso = 1;
    entrevista.respuestas = {
        inicio_semana: false,
        clima: "templado",
        oferta_carne: false,
        equipo: "normal",
        restriccion: false,
        hechos_extra: [],
    };

    agregarBurbuja(
        "bot",
        `
        <div class="section-heading">
            <span class="svg-badge">${SVG.utensils}</span>
            <span>Asistente de Planificación del Menú Diario</span>
        </div>
        <p style="margin-top:6px;">Respondé estas 5 preguntas rápidas sobre el contexto de hoy en la cocina:</p>
        <p style="margin-top:8px;"><b>Paso 1 de 5:</b> ¿En qué día de la semana estamos?</p>
        <div class="inline-options">
            ${crearBotonOpcion("responderPaso1(true, this)", SVG.calendar, "Lunes, Martes o Miércoles")}
            ${crearBotonOpcion("responderPaso1(false, this)", SVG.calendar, "Jueves a Domingo")}
        </div>
        `
    );
}

function responderPaso1(esInicio, btnEl) {
    deshabilitarControlesPaso(btnEl);
    entrevista.respuestas.inicio_semana = esInicio;
    agregarBurbuja("user", esInicio ? "Es Lunes, Martes o Miércoles" : "Es Jueves a Domingo");

    entrevista.paso = 2;
    agregarBurbuja(
        "bot",
        `
        <b>Paso 2 de 5:</b> ¿Cómo se presenta el clima en la jornada de hoy?
        <div class="inline-options">
            ${crearBotonOpcion("responderPaso2('frio', this)", SVG.snow, "Clima Frío (alta demanda de olla)")}
            ${crearBotonOpcion("responderPaso2('calido', this)", SVG.sun, "Clima Cálido / Verano")}
            ${crearBotonOpcion("responderPaso2('templado', this)", SVG.cloud, "Templado / Estándar")}
        </div>
        `
    );
}

function responderPaso2(clima, btnEl) {
    deshabilitarControlesPaso(btnEl);
    entrevista.respuestas.clima = clima;
    const etiquetas = {
        frio: "Clima frío",
        calido: "Clima cálido / verano",
        templado: "Clima templado",
    };
    agregarBurbuja("user", etiquetas[clima]);

    entrevista.paso = 3;
    agregarBurbuja(
        "bot",
        `
        <b>Paso 3 de 5:</b> ¿Hay oferta de cortes de carne por pieza entera en el frigorífico?
        <div class="inline-options">
            ${crearBotonOpcion("responderPaso3(true, this)", SVG.checkCircle, "Sí, hay oferta de pieza entera")}
            ${crearBotonOpcion("responderPaso3(false, this)", SVG.xCircle, "No hay oferta hoy")}
        </div>
        `
    );
}

function responderPaso3(hayOferta, btnEl) {
    deshabilitarControlesPaso(btnEl);
    entrevista.respuestas.oferta_carne = hayOferta;
    agregarBurbuja("user", hayOferta ? "Sí, hay oferta de pieza entera" : "No hay oferta hoy");

    entrevista.paso = 4;
    agregarBurbuja(
        "bot",
        `
        <b>Paso 4 de 5:</b> ¿Cuál es la disponibilidad del personal y tiempos en la cocina?
        <div class="inline-options">
            ${crearBotonOpcion("responderPaso4('normal', this)", SVG.users, "Equipo completo (asistió la ayudante)")}
            ${crearBotonOpcion("responderPaso4('falta_ayudante', this)", SVG.alertTriangle, "La ayudante avisó que NO asiste")}
            ${crearBotonOpcion("responderPaso4('demora_urgente', this)", SVG.clock, "Surgió una demora / imprevisto urgente")}
        </div>
        `
    );
}

function responderPaso4(equipo, btnEl) {
    deshabilitarControlesPaso(btnEl);
    entrevista.respuestas.equipo = equipo;
    const etiquetas = {
        normal: "Equipo completo (asistió la ayudante)",
        falta_ayudante: "Faltó la ayudante de cocina",
        demora_urgente: "Demora / imprevisto urgente en cocina",
    };
    agregarBurbuja("user", etiquetas[equipo]);

    entrevista.paso = 5;

    let extraHtml = "";
    const codigosPers = Object.keys(estadoSistema.hechosPersonalizados || {});
    if (codigosPers.length > 0) {
        extraHtml += `<div style="margin-top:12px; padding:12px 14px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:10px; font-size:0.86rem;">
            <b>Situaciones personalizadas aprendidas por el sistema (marcá si alguna ocurre hoy):</b><br>`;
        for (const cod of codigosPers) {
            const desc = estadoSistema.hechosPersonalizados[cod];
            extraHtml += `
                <label style="display:flex; align-items:center; gap:8px; margin-top:7px; cursor:pointer;">
                    <input type="checkbox" class="chk-hecho-aprendido" value="${escaparHtml(cod)}">
                    <span><b>${escaparHtml(cod)}</b>: ${escaparHtml(desc)}</span>
                </label>
            `;
        }
        extraHtml += `</div>`;
    }

    agregarBurbuja(
        "bot",
        `
        <b>Paso 5 de 5:</b> ¿Hay pedidos de clientes con restricciones alimentarias hoy?
        ${extraHtml}
        <div class="inline-options">
            ${crearBotonOpcion("responderPaso5(true, this)", SVG.leaf, "Sí, hay cliente con restricción alimentaria")}
            ${crearBotonOpcion("responderPaso5(false, this)", SVG.checkCircle, "No, sin restricciones hoy")}
        </div>
        `
    );
}

async function responderPaso5(hayRestriccion, btnEl) {
    entrevista.respuestas.restriccion = hayRestriccion;

    const contenedorPaso5 = btnEl ? btnEl.closest(".msg-card") : document;
    const checks = contenedorPaso5.querySelectorAll(".chk-hecho-aprendido:checked");
    const extras = [];
    checks.forEach((c) => extras.push(c.value));
    entrevista.respuestas.hechos_extra = extras;
    entrevista.activa = false;
    deshabilitarControlesPaso(btnEl);

    agregarBurbuja(
        "user",
        hayRestriccion
            ? "Sí, hay cliente con restricción alimentaria"
            : "No hay restricciones alimentarias hoy"
    );

    try {
        const res = await fetch("/api/recomendar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(entrevista.respuestas),
        });
        const menu = await res.json();
        estadoSistema.menuDelDia = menu;
        try {
            localStorage.setItem("chefbot_menu_del_dia", JSON.stringify(menu));
        } catch (_) {}
        actualizarCabecera();

        let avisoContingencia = "";
        if (menu.contingencia_automatica) {
            avisoContingencia = `
                <div class="discard-box" style="margin-bottom:10px;">
                    <div class="box-title">${SVG.alertTriangle} <span>Protocolo de Contingencia Inferido Automáticamente (R6 → R7 → R8):</span></div>
                    <div>Al combinarse una planificación de múltiples platos con el retraso por falta de ayudante, el motor descartó el guiso largo y activó la producción de minutas rápidas.</div>
                </div>
            `;
        }

        const tarjetasHtml = renderizarTarjetasPlatos(menu);

        agregarBurbuja(
            "bot",
            `
            <div class="section-heading">
                <span class="svg-badge svg-badge-success">${SVG.checkCircle}</span>
                <span>Propuesta de Menú Generada (${menu.platos.length} platos recomendados)</span>
            </div>
            ${avisoContingencia}
            ${tarjetasHtml}
            <div style="margin-top:14px; font-size:0.82rem; color:#475569;">
                Este menú quedó registrado como el <b>Menú del Día Activo</b>. Podés consultarlo con la opción <b>2</b> o auditar la traza lógica con la opción <b>4</b>.
            </div>
            `
        );
    } catch (err) {
        agregarBurbuja("bot", "Ocurrió un error al consultar el motor de inferencia.");
    }
}

// ========================================================
// OPCIONES 2, 3, 4, 5 Y 6
// ========================================================
async function mostrarMenuDelDia() {
    await sincronizarEstadoServidor();
    const menu = estadoSistema.menuDelDia;

    if (!menu || !menu.platos || menu.platos.length === 0) {
        agregarBurbuja(
            "bot",
            `<div class="section-heading"><span class="svg-badge">${SVG.calendar}</span><span>No hay ningún Menú del Día cargado actualmente</span></div>
            <p style="margin-top:6px;">Seleccioná la opción <b>1. Recomendar Menú</b> para evaluar la jornada y generar los platos.</p>`
        );
        return;
    }

    const tarjetasHtml = renderizarTarjetasPlatos(menu);
    agregarBurbuja(
        "bot",
        `<div class="section-heading"><span class="svg-badge svg-badge-success">${SVG.calendar}</span><span>MENÚ DEL DÍA ACTIVO (${menu.platos.length} platos confirmados)</span></div>${tarjetasHtml}`
    );
}

async function borrarMenuDelDia() {
    await fetch("/api/menu", { method: "DELETE" });
    estadoSistema.menuDelDia = null;
    try {
        localStorage.removeItem("chefbot_menu_del_dia");
    } catch (_) {}
    actualizarCabecera();
    agregarBurbuja(
        "bot",
        `<div class="section-heading"><span class="svg-badge">${SVG.trash}</span><span>Menú del Día eliminado correctamente</span></div>
        <p style="margin-top:6px;">La pizarra quedó libre para iniciar una nueva planificación.</p>`
    );
}

async function mostrarTrazabilidad() {
    await sincronizarEstadoServidor();
    const menu = estadoSistema.menuDelDia;

    if (!menu) {
        agregarBurbuja(
            "bot",
            `<div class="section-heading"><span class="svg-badge svg-badge-teal">${SVG.network}</span><span>Sin traza activa</span></div>
            <p style="margin-top:6px;">Primero generá un menú con la opción <b>1. Recomendar Menú</b> para inspeccionar la traza de inferencia.</p>`
        );
        return;
    }

    let pasosHtml = `<div class="trace-grid">`;
    menu.traza.forEach((paso, i) => {
        pasosHtml += `<div class="trace-item"><b>Paso ${i + 1}:</b> ${paso}</div>`;
    });
    pasosHtml += `</div>`;

    agregarBurbuja(
        "bot",
        `
        <div class="section-heading"><span class="svg-badge svg-badge-teal">${SVG.network}</span><span>Auditoría de Inferencia y Explicabilidad (XAI)</span></div>
        <div style="margin-top:10px;">
            <b>Hechos iniciales activados por la entrevista:</b> <code>${menu.hechos_iniciales.join(", ") || "Ninguno"}</code><br>
            <b>Estado final de la Memoria de Trabajo:</b> <code>${menu.hechos_finales.join(", ") || "Ninguno"}</code>
        </div>
        <div style="margin-top:10px;"><b>Cadena de reglas ejecutadas según prioridad / Salience (${menu.traza.length}):</b></div>
        ${menu.traza.length ? pasosHtml : "<div class='trace-item'>Jornada estándar sin disparo de reglas críticas.</div>"}
        `
    );
}

function mostrarFormularioAprendizaje() {
    let opcionesSelect = `
        <option value="C">Cuando el clima es frío (Hecho C)</option>
        <option value="T">Cuando el clima es cálido / verano (Hecho T)</option>
        <option value="A">Cuando es Lunes, Martes o Miércoles (Hecho A)</option>
        <option value="B">Cuando hay oferta de carne en frigorífico (Hecho B)</option>
        <option value="G">Cuando falta la ayudante de cocina (Hecho G)</option>
        <option value="L">Cuando hay contingencia o demora (Hecho L)</option>
        <option value="W">Cuando hay cliente con restricción alimentaria (Hecho W)</option>
    `;

    for (const [cod, desc] of Object.entries(estadoSistema.hechosPersonalizados || {})) {
        opcionesSelect += `<option value="${escaparHtml(cod)}">${escaparHtml(desc)} (Hecho aprendido ${escaparHtml(cod)})</option>`;
    }
    opcionesSelect += `<option value="__NUEVO__">+ Crear un NUEVO hecho / situación en la cocina...</option>`;

    agregarBurbuja(
        "bot",
        `
        <div class="section-heading"><span class="svg-badge">${SVG.plusCircle}</span><span>Módulo de Aprendizaje Continuo</span></div>
        <p style="margin-top:6px;">Incorporá nuevos hechos y platos a la Base de Conocimiento del sistema experto:</p>
        <div class="learn-form">
            <div class="learn-field-full">
                <label>Condición / Hecho que dispara la recomendación:</label>
                <select class="learn-cond-select" onchange="toggleNuevoHechoInput(this)">
                    ${opcionesSelect}
                </select>
            </div>

            <div class="nuevo-hecho-box learn-field-full" style="display:none; grid-template-columns: 1fr 2fr; gap:12px;">
                <div>
                    <label>Código del nuevo hecho (ej. VP):</label>
                    <input type="text" class="learn-nuevo-cod" placeholder="Ej: VP" maxlength="10" />
                </div>
                <div>
                    <label>Descripción del nuevo hecho:</label>
                    <input type="text" class="learn-nuevo-desc" placeholder="Ej: Es Viernes de pescado fresco en oferta" />
                </div>
            </div>

            <div>
                <label>Nombre del plato a recomendar:</label>
                <input type="text" class="learn-plato-nombre" placeholder="Ej: Filet de Merluza a la Romana con Puré" />
            </div>

            <div>
                <label>Categoría gastronómica:</label>
                <select class="learn-plato-cat">
                    <option value="Plato Principal">Plato Principal</option>
                    <option value="Plato de Olla">Plato de Olla</option>
                    <option value="Minuta Rápida">Minuta Rápida</option>
                    <option value="Menú Fresco">Menú Fresco</option>
                    <option value="Vianda Especial">Vianda Especial</option>
                </select>
            </div>

            <div>
                <label>Tiempo estimado de preparación:</label>
                <input type="text" class="learn-plato-tiempo" value="25 min" />
            </div>

            <div>
                <label>Consejo o criterio experto de Lucía:</label>
                <input type="text" class="learn-plato-tip" placeholder="Ej: Secar bien los filetes antes de empanar." />
            </div>

            <div class="learn-field-full">
                <label>Descripción del plato y guarnición:</label>
                <textarea class="learn-plato-desc" rows="2" placeholder="Ej: Filet fresco rebozado al momento acompañado con puré mixto."></textarea>
            </div>

            <button type="button" class="learn-submit-btn" onclick="guardarAprendizaje(this)">
                ${SVG.save}
                <span>Guardar Hecho y Plato en la Base de Conocimiento</span>
            </button>
        </div>
        `
    );
}

function toggleNuevoHechoInput(selectEl) {
    const form = selectEl.closest(".learn-form");
    if (!form) return;
    const box = form.querySelector(".nuevo-hecho-box");
    if (box) {
        box.style.display = selectEl.value === "__NUEVO__" ? "grid" : "none";
    }
}

async function guardarAprendizaje(btnEl) {
    const form = btnEl ? btnEl.closest(".learn-form") : document.querySelector(".learn-form");
    if (!form) return;

    const selectVal = form.querySelector(".learn-cond-select").value;
    const esNuevo = selectVal === "__NUEVO__";
    const codigo = esNuevo
        ? form.querySelector(".learn-nuevo-cod").value.trim().toUpperCase()
        : selectVal;
    const descCond = esNuevo
        ? form.querySelector(".learn-nuevo-desc").value.trim()
        : "";

    const nombrePlato = form.querySelector(".learn-plato-nombre").value.trim();
    const categoria = form.querySelector(".learn-plato-cat").value;
    const tiempo = form.querySelector(".learn-plato-tiempo").value.trim();
    const descPlato = form.querySelector(".learn-plato-desc").value.trim();
    const tip = form.querySelector(".learn-plato-tip").value.trim();

    if (!nombrePlato || !descPlato || (esNuevo && (!codigo || !descCond))) {
        alert("Completá el nombre del plato, su descripción y los datos de la condición.");
        return;
    }

    if (btnEl) {
        btnEl.disabled = true;
        btnEl.style.opacity = "0.65";
    }

    const res = await fetch("/api/aprender", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            condicion_codigo: codigo,
            condicion_descripcion: descCond,
            es_hecho_nuevo: esNuevo,
            nombre_plato: nombrePlato,
            categoria: categoria,
            tiempo_estimado: tiempo,
            descripcion_plato: descPlato,
            consejo_cocina: tip,
        }),
    });

    const data = await res.json();
    await sincronizarEstadoServidor();

    agregarBurbuja(
        "bot",
        `
        <div class="section-heading"><span class="svg-badge svg-badge-success">${SVG.checkCircle}</span><span>Conocimiento aprendido e integrado al motor</span></div>
        <div style="margin-top:8px;">
            • <b>Identificador de Regla:</b> <code>${escaparHtml(data.regla.id)}</code><br>
            • <b>Antecedente (SI):</b> <code>${escaparHtml(data.regla.condicion_codigo)}</code> (<i>${escaparHtml(data.regla.condicion_descripcion)}</i>)<br>
            • <b>Consecuente (ENTONCES):</b> Recomendar <b>${escaparHtml(data.regla.nombre_plato)}</b> (<i>${escaparHtml(data.regla.categoria)}</i>)
        </div>
        <p style="margin-top:8px;">Ya se encuentra activo para las próximas ejecuciones de <b>1. Recomendar Menú</b>.</p>
        `
    );
}

async function borrarReglaAprendidaUI(reglaId) {
    registrarReglaEliminadaLocal(reglaId);
    try {
        await fetch(`/api/aprender/${encodeURIComponent(reglaId)}`, { method: "DELETE" });
    } catch (_) {}
    await sincronizarEstadoServidor();
    agregarBurbuja(
        "bot",
        `<div class="section-heading"><span class="svg-badge">${SVG.trash}</span><span>Regla aprendida <code>${escaparHtml(reglaId)}</code> eliminada</span></div>`
    );
    mostrarBaseAprendida();
}

async function mostrarBaseAprendida() {
    await sincronizarEstadoServidor();
    const reglas = estadoSistema.reglasAprendidas;

    if (!reglas || reglas.length === 0) {
        agregarBurbuja(
            "bot",
            `<div class="section-heading"><span class="svg-badge">${SVG.book}</span><span>Base de Conocimiento Aprendida</span></div>
            <p style="margin-top:6px;">Aún no se registraron reglas personalizadas. Utilizá la opción <b>5. Agregar Hecho / Plato</b> para enseñar nuevas recomendaciones al sistema.</p>`
        );
        return;
    }

    let html = `<div class="section-heading"><span class="svg-badge">${SVG.book}</span><span>Reglas y platos aprendidos por el sistema (${reglas.length})</span></div><div class="trace-grid">`;
    for (const r of reglas) {
        html += `
            <div class="trace-item" style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
                <div>
                    <b>[${escaparHtml(r.id)}]</b> SI se cumple <code>${escaparHtml(r.condicion_codigo)}</code> (${escaparHtml(r.condicion_descripcion)})
                    → Recomendar <b>${escaparHtml(r.nombre_plato)}</b> (<i>${escaparHtml(r.categoria)}</i>)
                </div>
                <button
                    type="button"
                    onclick="borrarReglaAprendidaUI('${escaparHtml(r.id)}')"
                    style="background:transparent; border:1px solid #fca5a5; color:#dc2626; border-radius:6px; padding:4px 8px; font-size:0.75rem; font-weight:700; cursor:pointer; flex-shrink:0;"
                    title="Eliminar regla aprendida"
                >
                    Eliminar
                </button>
            </div>
        `;
    }
    html += `</div>`;
    agregarBurbuja("bot", html);
}

// ========================================================
// MANEJADOR DE OPCIONES Y ENTRADA DE TEXTO
// ========================================================
function ejecutarOpcion(num) {
    if (num === 1) {
        agregarBurbuja("user", "1. Recomendar menú del día");
        iniciarEntrevista();
    } else if (num === 2) {
        agregarBurbuja("user", "2. Mostrar menú del día");
        mostrarMenuDelDia();
    } else if (num === 3) {
        agregarBurbuja("user", "3. Borrar menú del día");
        borrarMenuDelDia();
    } else if (num === 4) {
        agregarBurbuja("user", "4. Ver trazabilidad");
        mostrarTrazabilidad();
    } else if (num === 5) {
        agregarBurbuja("user", "5. Agregar nuevo hecho / plato");
        mostrarFormularioAprendizaje();
    } else if (num === 6) {
        agregarBurbuja("user", "6. Ver conocimiento aprendido");
        mostrarBaseAprendida();
    }
}

function enviarTextoUsuario(e) {
    e.preventDefault();
    const input = document.getElementById("user-input");
    const raw = input.value.trim();
    if (!raw) return;
    input.value = "";

    const txt = raw.toLowerCase();

    if (txt === "1" || txt.includes("recomendar")) {
        ejecutarOpcion(1);
    } else if (txt === "2" || txt.includes("mostrar") || txt === "menu" || txt === "menú") {
        ejecutarOpcion(2);
    } else if (txt === "3" || txt.includes("borrar") || txt.includes("limpiar")) {
        ejecutarOpcion(3);
    } else if (txt === "4" || txt.includes("traza") || txt.includes("explicacion")) {
        ejecutarOpcion(4);
    } else if (txt === "5" || txt.includes("agregar") || txt.includes("aprender") || txt.includes("hecho")) {
        ejecutarOpcion(5);
    } else if (txt === "6" || txt.includes("conocimiento") || txt.includes("aprendido")) {
        ejecutarOpcion(6);
    } else {
        agregarBurbuja("user", escaparHtml(raw));
        mostrarMenuBienvenida();
    }
}

window.addEventListener("DOMContentLoaded", async () => {
    await sincronizarEstadoServidor();
    mostrarMenuBienvenida();
});
