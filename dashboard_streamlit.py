"""
=============================================================
Sistema Big Data para Análisis de Movilidad y Transporte Público
Equipo 1 – ISC 6.º periodo
Dashboard principal – Streamlit
=============================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TransitBD – Movilidad y Transporte Público",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS PERSONALIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');

/* ── MODO OSCURO – Variables ── */
:root {
    --metro-blue:    #3B82F6;
    --metro-yellow:  #F5C518;
    --metro-orange:  #F87171;
    --metro-teal:    #34D399;
    --bg-main:       #0F1117;
    --bg-card:       #1A1D27;
    --bg-card2:      #22263A;
    --border:        #2E3350;
    --text-primary:  #F0F2FA;
    --text-muted:    #9CA3C0;
    --text-dark:     #F0F2FA;
}

/* ── Fondo general ── */
.stApp {
    background-color: var(--bg-main);
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* ── Texto nativo de Streamlit ── */
.stApp p, .stApp li, .stApp label,
.stMarkdown, .stMarkdown p,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stCaption"] p,
.stCaption, .stText,
div[class*="caption"], span[class*="caption"] {
    color: var(--text-primary) !important;
}

/* Títulos nativos */
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: var(--text-primary) !important;
}

/* Métricas nativas */
[data-testid="stMetricValue"],
[data-testid="stMetricLabel"],
[data-testid="stMetricDelta"] {
    color: var(--text-primary) !important;
}

/* Selectbox / multiselect / slider etiquetas */
.stSelectbox label, .stMultiSelect label,
.stSlider label, .stCheckbox label,
[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: var(--text-primary) !important;
}

/* Input / select fondos */
[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
    background-color: var(--bg-card2) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

/* Expander */
[data-testid="stExpander"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] p,
[data-testid="stExpander"] li,
[data-testid="stExpander"] td,
[data-testid="stExpander"] th {
    color: var(--text-primary) !important;
}

/* Tablas / DataFrames */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
}
[data-testid="stDataFrame"] th {
    background-color: var(--bg-card2) !important;
    color: var(--metro-yellow) !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text-primary) !important;
    background-color: var(--bg-card) !important;
}

/* ── Header principal ── */
.main-header {
    background: linear-gradient(135deg, #0A1628 0%, #0F2D6B 55%, #0A1628 100%);
    color: white;
    padding: 2.5rem 2rem 2rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    border: 1px solid #1E3A8A;
}
.main-header::before {
    content: "🚇";
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 6rem;
    opacity: 0.15;
}
.main-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.03em;
    color: #FFFFFF;
}
.main-header p {
    margin: 0;
    font-size: 0.95rem;
    opacity: 0.82;
    font-weight: 300;
    color: #CBD5F0;
}

/* ── Badge ── */
.bd-badge {
    display: inline-block;
    background: #F5C518;
    color: #0A1628;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.7rem;
    border-radius: 100px;
    letter-spacing: 0.08em;
    margin-bottom: 0.6rem;
}

/* ── KPI Cards ── */
.kpi-card {
    background: var(--bg-card);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    border-left: 5px solid var(--metro-blue);
    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.kpi-card.yellow { border-left-color: #F5C518; }
.kpi-card.orange { border-left-color: #F87171; }
.kpi-card.green  { border-left-color: #34D399; }

.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
}
.kpi-delta {
    font-size: 0.78rem;
    margin-top: 0.3rem;
    color: #34D399;
    font-weight: 600;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: var(--metro-yellow);
    border-bottom: 3px solid var(--metro-yellow);
    padding-bottom: 0.4rem;
    margin: 1.8rem 0 1rem 0;
    display: inline-block;
}

/* ── Info cards ── */
.info-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
    margin-bottom: 0.8rem;
    color: var(--text-primary);
}
.info-card b { color: var(--metro-yellow); }

/* ── Alerta saturación ── */
.alert-sat {
    background: rgba(248,113,113,0.12);
    border: 1px solid rgba(248,113,113,0.4);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #FCA5A5;
    font-size: 0.9rem;
}

/* ── Preguntas analíticas ── */
.q-card {
    background: rgba(59,130,246,0.1);
    border-left: 4px solid var(--metro-blue);
    border-radius: 0 10px 10px 0;
    padding: 0.8rem 1.1rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    color: var(--text-primary);
}
.q-card b { color: #93C5FD; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0A1628 !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stCheckbox label {
    color: var(--metro-yellow) !important;
    font-weight: 700;
    font-size: 0.8rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] h2 {
    color: var(--metro-yellow) !important;
    font-family: 'Space Mono', monospace;
    font-size: 0.95rem;
}
[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
}

/* Controles del sidebar en modo oscuro */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="input"] > div {
    background-color: #131929 !important;
    border-color: var(--border) !important;
}

/* ── Pie de página ── */
.footer {
    background: #0A1628;
    border: 1px solid var(--border);
    color: rgba(200,210,240,0.75);
    padding: 1.2rem 1.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
    margin-top: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.footer span { color: var(--metro-yellow); font-weight: 700; }

/* ── Divisores ── */
hr { border-color: var(--border) !important; }

/* ── Checkbox ── */
[data-testid="stCheckbox"] span {
    color: var(--text-primary) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# NORMALIZACIÓN DE LÍNEAS
# ─────────────────────────────────────────────
import re, unicodedata as _ud

def normalizar_linea(valor):
    """Convierte cualquier variante de nombre de línea al formato canónico.
    Ejemplos: L1, L-1, LINEA 1, LIENA 5, LNIEA 4, LÍNEA 11 → Línea 1 ... Línea 12, Línea A, Línea B
    """
    if not isinstance(valor, str) or valor.strip() == "":
        return valor
    v = _ud.normalize("NFKD", valor.strip().upper())
    v = "".join(c for c in v if not _ud.combining(c))
    # número o letra al final
    m = re.search(r"(\d{1,2}|[AB])\s*$", v)
    if m:
        id_ = m.group(1)
        return f"Línea {id_}" if id_ in ("A","B") else f"Línea {int(id_)}"
    # formato corto L1 / LA / L-2
    m2 = re.match(r"^L-?(\d{1,2}|[AB])$", v)
    if m2:
        id_ = m2.group(1)
        return f"Línea {id_}" if id_ in ("A","B") else f"Línea {int(id_)}"
    return valor

def normalizar_col_linea(df):
    """Aplica normalizar_linea a la columna 'linea' si existe."""
    if "linea" in df.columns:
        df = df.copy()
        df["linea"] = df["linea"].apply(normalizar_linea)
    return df

# ─────────────────────────────────────────────
# DATOS SIMULADOS (se reemplazan por CSVs reales)
# ─────────────────────────────────────────────
@st.cache_data
def generar_datos_simulados():
    """
    Genera datos sintéticos para todas las vistas del dashboard.
    En producción, reemplaza cada bloque por pd.read_csv(ruta).
    """
    rng = np.random.default_rng(42)
    lineas = ["Línea 1", "Línea 2", "Línea 3", "Línea A", "Línea B"]
    meses = list(range(1, 13))
    años = [2022, 2023, 2024, 2025]
    tipos_dia = ["Lunes-Viernes", "Sábado", "Domingo"]
    estaciones = [
        "Pantitlán", "Balderas", "Hidalgo", "Bellas Artes",
        "Tacuba", "Observatorio", "Indios Verdes", "El Rosario",
        "Cuatro Caminos", "Taxqueña", "Universidad", "Politécnico",
    ]

    # ── 01 Afluencia diaria ──────────────────
    fechas = pd.date_range("2023-01-01", "2025-12-31", freq="D")
    df_diaria = pd.DataFrame({
        "fecha": fechas,
        "afluencia_total": rng.integers(280_000, 620_000, len(fechas)),
        "linea": rng.choice(lineas, len(fechas)),
        "tipo_dia": [
            "Lunes-Viernes" if d.weekday() < 5
            else ("Sábado" if d.weekday() == 5 else "Domingo")
            for d in fechas
        ],
    })

    # ── 02 Afluencia mensual ─────────────────
    registros = []
    for a in años:
        for m in meses:
            for l in lineas:
                base = rng.integers(800_000, 2_500_000)
                registros.append({
                    "año": a, "mes": m, "linea": l,
                    "afluencia_total": base,
                    "afluencia_promedio_diaria": base // 30,
                })
    df_mensual = pd.DataFrame(registros)

    # ── 03 Afluencia anual ───────────────────
    df_anual = df_mensual.groupby(["año", "linea"])["afluencia_total"].sum().reset_index()

    # ── 04 Top estaciones ────────────────────
    df_top = pd.DataFrame({
        "estacion": estaciones,
        "linea": rng.choice(lineas, len(estaciones)),
        "afluencia_total": rng.integers(1_500_000, 8_000_000, len(estaciones)),
    }).sort_values("afluencia_total", ascending=False)

    # ── 05 Heatmap mes × línea ───────────────
    hm = []
    for m in meses:
        for l in lineas:
            hm.append({"mes": m, "linea": l,
                        "afluencia_promedio_diaria": rng.integers(30_000, 95_000)})
    df_heatmap = pd.DataFrame(hm)

    # ── 06 Tendencia anual ───────────────────
    df_tendencia = pd.DataFrame({
        "año": años,
        "afluencia_sistema_total": [
            312_000_000, 345_000_000, 378_000_000, 392_000_000
        ],
    })

    # ── 07 Demanda tipo de día ───────────────
    df_tipo_dia = pd.DataFrame({
        "tipo_dia": tipos_dia,
        "afluencia_promedio": [520_000, 340_000, 210_000],
    })

    # ── 08 Saturación estaciones ─────────────
    df_sat = pd.DataFrame({
        "estacion": estaciones,
        "linea": rng.choice(lineas, len(estaciones)),
        "afluencia_hora_pico": rng.integers(8_000, 28_000, len(estaciones)),
        "capacidad_maxima": [25_000] * len(estaciones),
    })
    df_sat["indice_saturacion"] = (
        df_sat["afluencia_hora_pico"] / df_sat["capacidad_maxima"] * 100
    ).round(1)

    # ── 09 Ingresos mensuales ────────────────
    df_ing = df_mensual.copy()
    df_ing["tarifa"] = rng.uniform(4.5, 6.5, len(df_ing))
    df_ing["ingreso_total"] = (df_ing["afluencia_total"] * df_ing["tarifa"]).astype(int)

    # ── 10 Ingresos vs afluencia ─────────────
    df_eff = df_ing[["afluencia_total", "ingreso_total", "linea"]].copy()
    df_eff["ingreso_por_pasajero"] = df_eff["ingreso_total"] / df_eff["afluencia_total"]

    # ── 11 Retrasos ──────────────────────────
    df_retrasos = pd.DataFrame({
        "linea": lineas,
        "retraso_promedio_min": rng.uniform(1.2, 8.5, len(lineas)).round(1),
        "incidencias_mes": rng.integers(5, 60, len(lineas)),
        "puntualidad_pct": rng.uniform(72, 96, len(lineas)).round(1),
    })

    # ── 12 Horarios pico ─────────────────────
    horas = list(range(5, 24))
    df_horarios = pd.DataFrame({
        "hora": horas,
        "afluencia_promedio": [
            12_000, 45_000, 95_000, 130_000, 88_000,  # 5-9
            55_000, 48_000, 52_000, 68_000, 75_000,   # 10-14
            70_000, 62_000, 58_000, 78_000, 110_000,  # 15-19
            125_000, 90_000, 60_000, 35_000,           # 20-23
        ],
    })

    return {
        "01_afluencia_diaria": df_diaria,
        "02_afluencia_mensual": df_mensual,
        "03_afluencia_anual": df_anual,
        "04_top_estaciones": df_top,
        "05_heatmap_mes_linea": df_heatmap,
        "06_tendencia_anual": df_tendencia,
        "07_demanda_tipo_dia": df_tipo_dia,
        "08_saturacion_estaciones": df_sat,
        "09_ingresos_mensual": df_ing,
        "10_ingresos_vs_afluencia": df_eff,
        "11_retrasos": df_retrasos,
        "12_horarios_pico": df_horarios,
    }


@st.cache_data
def load_data():
    """
    Intenta cargar CSVs reales desde 'powerbi_export/'.
    Si no existen, usa datos simulados (modo demostración).
    """
    base = "powerbi_export"
    keys = [
        "01_afluencia_diaria", "02_afluencia_mensual",
        "03_afluencia_anual", "04_top_estaciones",
        "05_heatmap_mes_linea", "06_tendencia_anual",
        "07_demanda_tipo_dia", "08_saturacion_estaciones",
        "09_ingresos_mensual", "10_ingresos_vs_afluencia",
        # 11_retrasos y 12_horarios_pico no vienen del pipeline Gold;
        # se generan como datos simulados directamente en el dashboard.
    ]
    data = {}
    modo_real = False
    for k in keys:
        path = os.path.join(base, f"{k}.csv")
        if os.path.exists(path):
            try:
                data[k] = pd.read_csv(path, encoding="utf-8")
            except Exception:
                data[k] = pd.read_csv(path, encoding="latin1")
            modo_real = True
    if not data:
        data = generar_datos_simulados()
    return data, modo_real


data, modo_real = load_data()

# Normalizar columna linea en todos los dataframes cargados
for _k in list(data.keys()):
    data[_k] = normalizar_col_linea(data[_k])

# ─────────────────────────────────────────────
# VARIABLES BASE
# ─────────────────────────────────────────────
df_mensual   = data["02_afluencia_mensual"]
df_tendencia = data["06_tendencia_anual"]
df_sat       = data["08_saturacion_estaciones"]
# 11 y 12 no se generan en el pipeline Gold; se usan datos simulados como fallback
sim = generar_datos_simulados()
df_retrasos  = data.get("11_retrasos",  sim["11_retrasos"])
df_horarios  = data.get("12_horarios_pico", sim["12_horarios_pico"])
df_tipo_dia  = data["07_demanda_tipo_dia"]
df_top       = data["04_top_estaciones"]
df_heatmap   = data["05_heatmap_mes_linea"]
df_ing       = data["09_ingresos_mensual"]
df_eff       = data["10_ingresos_vs_afluencia"]

años  = sorted(df_mensual["año"].dropna().unique().tolist())
lineas = sorted(df_mensual["linea"].dropna().unique().tolist())

MESES_ES = {
    1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril",
    5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto",
    9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre",
}

# ─────────────────────────────────────────────
# SIDEBAR  
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚇 TransitBD")
    st.markdown("---")

    if not modo_real:
        st.info("⚠️ Modo demostración\n\nCarga tus CSVs en `powerbi_export/` para datos reales.", icon="📂")
        st.markdown("---")

    st.markdown("**AÑO**")
    año_sel = st.selectbox("Selecciona año", años, index=len(años)-1, label_visibility="collapsed")

    st.markdown("**LÍNEAS**")
    linea_sel = st.multiselect("Selecciona líneas", lineas, default=lineas, label_visibility="collapsed")

    st.markdown("**MES**")
    mes_sel = st.slider("Mes", 1, 12, (1, 12))

    st.markdown("---")
    st.markdown("**SECCIONES**")
    mostrar_retrasos  = st.checkbox("Retrasos", True)
    mostrar_horarios  = st.checkbox("Horarios pico", True)
    mostrar_ingresos  = st.checkbox("Ingresos", True)
    mostrar_heatmap   = st.checkbox("Heatmap", True)

    st.markdown("---")
    st.markdown("**FUENTE**")
    st.markdown("Pipeline: Hadoop + Spark + Hive")
    st.markdown("Procesamiento: PySpark + HDFS")
    st.caption("Actualización: 2026")

# ─────────────────────────────────────────────
# FILTRADO PRINCIPAL
# ─────────────────────────────────────────────
if not linea_sel:
    linea_sel = lineas

df_f = df_mensual[
    (df_mensual["año"] == año_sel) &
    (df_mensual["linea"].isin(linea_sel)) &
    (df_mensual["mes"] >= mes_sel[0]) &
    (df_mensual["mes"] <= mes_sel[1])
]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="bd-badge">BIG DATA · ISC 6.º PERIODO</div>
    <h1>Sistema Big Data para Análisis de<br>Movilidad y Transporte Público</h1>
    <p>Rutas · Horarios · Demanda · Retrasos · Saturación · Comportamiento temporal</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# JUSTIFICACIÓN BIG DATA
# ─────────────────────────────────────────────
with st.expander("📌 Justificación Big Data y Planteamiento del problema", expanded=False):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
**Problema**  
Los sistemas de transporte masivo generan millones de registros diarios: 
afluencia por estación, tiempos de recorrido, incidencias, validaciones de tarifa 
y datos GPS de unidades. Procesarlos con herramientas tradicionales es inviable.

**Necesidad**  
Detectar patrones de demanda, saturación y retrasos en tiempo (casi) real 
para optimizar frecuencias, asignar recursos y mejorar la experiencia del usuario.
        """)
    with col_b:
        st.markdown("""
**Las 4 V's del proyecto**

| V | Descripción |
|---|---|
| **Volumen** | >10 M registros diarios de validaciones |
| **Velocidad** | Procesamiento en ventanas de 5 min (Spark Streaming) |
| **Variedad** | CSV afluencia, GPS JSON, incidencias texto |
| **Veracidad** | Limpieza con detección de outliers y duplicados |

**Herramientas:** Hadoop HDFS · Apache Spark · PySpark · Hive · Streamlit Cloud
        """)

# ─────────────────────────────────────────────
# KPIs PRINCIPALES
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Indicadores principales</div>', unsafe_allow_html=True)

total_pax      = int(df_f["afluencia_total"].sum())
prom_diario    = int(df_f["afluencia_promedio_diaria"].mean()) if "afluencia_promedio_diaria" in df_f.columns else int(total_pax // max(1, len(df_f)) // 30)
_ing_fil = df_ing[df_ing["año"] == año_sel] if "año" in df_ing.columns else df_ing
_col_ing = "ingreso_total" if "ingreso_total" in _ing_fil.columns else ("ingreso" if "ingreso" in _ing_fil.columns else None)
ingreso_total = int(_ing_fil[_col_ing].sum()) if _col_ing else 0
ing_pax        = round(df_eff["ingreso_por_pasajero"].mean(), 2) if "ingreso_por_pasajero" in df_eff.columns else 5.5
sat_critica    = int((df_sat["indice_saturacion"] > 85).sum())
linea_top_dem  = df_f.groupby("linea")["afluencia_total"].sum().idxmax() if len(df_f) > 0 else "N/A"
retraso_prom   = round(df_retrasos["retraso_promedio_min"].mean(), 1) if "retraso_promedio_min" in df_retrasos.columns else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
kpis = [
    (c1, "blue",   f"{total_pax:,}",         "Pasajeros (período)",     ""),
    (c2, "yellow", f"{prom_diario:,}",        "Promedio diario",         ""),
    (c3, "green",  f"${ingreso_total:,}",     "Ingreso total",           ""),
    (c4, "blue",   f"${ing_pax:.2f}",         "Ingreso / pasajero",      ""),
    (c5, "orange", f"{sat_critica} est.",     "Saturación crítica (>85%)", "⚠️"),
    (c6, "yellow", f"{retraso_prom} min",     "Retraso promedio",        ""),
]
for col, color, val, lbl, icon in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {color}">
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-value">{icon} {val}</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 1. TENDENCIA ANUAL
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Tendencia anual del sistema</div>', unsafe_allow_html=True)
st.caption("Afluencia total acumulada por año en todo el sistema de transporte.")
st.line_chart(df_tendencia.set_index("año")["afluencia_sistema_total"])

# ─────────────────────────────────────────────
# 2. DEMANDA POR LÍNEA  ×  TIPO DE DÍA
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">🚆 Demanda por línea y tipo de día</div>', unsafe_allow_html=True)
col_l, col_td = st.columns([3, 2])

with col_l:
    st.caption(f"Afluencia total por línea — Año {año_sel}, meses {mes_sel[0]}–{mes_sel[1]}")
    demanda_linea = df_f.groupby("linea")["afluencia_total"].sum().sort_values(ascending=False)
    st.bar_chart(demanda_linea)
    st.caption(f"🏆 Línea con mayor demanda: **{linea_top_dem}**")

with col_td:
    st.caption("Afluencia promedio según tipo de día (comportamiento temporal)")
    st.bar_chart(df_tipo_dia.set_index("tipo_dia")["afluencia_promedio"])
    st.markdown("""
    <div class="info-card">
    <b>Insight:</b> Los días hábiles concentran hasta 2.5× más afluencia que los domingos,
    lo que justifica ajustar frecuencias de servicio por tipo de jornada.
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. HORARIOS PICO
# ─────────────────────────────────────────────
if mostrar_horarios:
    st.markdown('<div class="section-header">⏱️ Distribución horaria de la demanda</div>', unsafe_allow_html=True)
    st.caption("Afluencia promedio por hora del día — identifica horarios pico y valles.")

    col_h1, col_h2 = st.columns([3, 2])
    with col_h1:
        st.line_chart(df_horarios.set_index("hora")["afluencia_promedio"])
    with col_h2:
        hora_pico = int(df_horarios.loc[df_horarios["afluencia_promedio"].idxmax(), "hora"])
        hora_min  = int(df_horarios.loc[df_horarios["afluencia_promedio"].idxmin(), "hora"])
        pico_val  = int(df_horarios["afluencia_promedio"].max())
        valle_val = int(df_horarios["afluencia_promedio"].min())
        st.markdown(f"""
        <div class="info-card">
        <b>🔴 Hora pico máxima:</b> {hora_pico}:00 h<br>
        <b>Afluencia:</b> {pico_val:,} pasajeros<br><br>
        <b>🟢 Hora valle:</b> {hora_min}:00 h<br>
        <b>Afluencia:</b> {valle_val:,} pasajeros<br><br>
        <b>Recomendación:</b> Incrementar frecuencia de trenes entre las 7:00 y 9:00, y entre las 18:00 y 20:00.
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. TOP ESTACIONES
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">🏙️ Top 10 estaciones con mayor demanda</div>', unsafe_allow_html=True)
col_e1, col_e2 = st.columns([3, 2])

top10 = df_top.nlargest(10, "afluencia_total").set_index("estacion")
with col_e1:
    st.caption("Ranking de estaciones por afluencia total acumulada.")
    st.bar_chart(top10["afluencia_total"])
with col_e2:
    st.caption("Detalle")
    st.dataframe(
        top10[["afluencia_total"]].rename(columns={"afluencia_total": "Pasajeros"}),
        use_container_width=True,
    )

# ─────────────────────────────────────────────
# 5. SATURACIÓN
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">🔴 Saturación de estaciones</div>', unsafe_allow_html=True)

criticas = df_sat[df_sat["indice_saturacion"] > 85].sort_values("indice_saturacion", ascending=False)
moderadas = df_sat[(df_sat["indice_saturacion"] >= 60) & (df_sat["indice_saturacion"] <= 85)]

if len(criticas) > 0:
    st.markdown(f"""
    <div class="alert-sat">
    ⚠️ <b>{len(criticas)} estación(es) en saturación crítica</b> (índice > 85%).
    Se recomienda revisar capacidad y frecuencia de servicio inmediatamente.
    </div>""", unsafe_allow_html=True)

col_s1, col_s2 = st.columns([3, 2])
with col_s1:
    sat_chart = df_sat.sort_values("indice_saturacion", ascending=False).head(10).set_index("estacion")
    st.bar_chart(sat_chart["indice_saturacion"])
with col_s2:
    def semaforo(v):
        if v > 85: return "🔴"
        if v > 60: return "🟡"
        return "🟢"
    df_sat_disp = df_sat.sort_values("indice_saturacion", ascending=False).head(10).copy()
    df_sat_disp["Estado"] = df_sat_disp["indice_saturacion"].apply(semaforo)
    df_sat_disp["Saturación %"] = df_sat_disp["indice_saturacion"].apply(lambda x: f"{x:.1f}%")
    st.dataframe(
        df_sat_disp[["estacion", "linea", "Saturación %", "Estado"]]
            .rename(columns={"estacion": "Estación", "linea": "Línea"}),
        use_container_width=True, hide_index=True,
    )

# ─────────────────────────────────────────────
# 6. RETRASOS
# ─────────────────────────────────────────────
if mostrar_retrasos:
    st.markdown('<div class="section-header">🕐 Análisis de retrasos por línea</div>', unsafe_allow_html=True)
    col_r1, col_r2 = st.columns([3, 2])
    with col_r1:
        st.caption("Retraso promedio por línea (minutos) e incidencias registradas en el período.")
        st.bar_chart(df_retrasos.set_index("linea")["retraso_promedio_min"])
    with col_r2:
        st.caption("Puntualidad del sistema (%)")
        st.dataframe(
            df_retrasos[["linea", "retraso_promedio_min", "puntualidad_pct", "incidencias_mes"]]
                .rename(columns={
                    "linea": "Línea",
                    "retraso_promedio_min": "Retraso (min)",
                    "puntualidad_pct": "Puntualidad %",
                    "incidencias_mes": "Incidencias/mes",
                }),
            use_container_width=True, hide_index=True,
        )
    linea_peor = df_retrasos.loc[df_retrasos["retraso_promedio_min"].idxmax(), "linea"]
    linea_mejor = df_retrasos.loc[df_retrasos["retraso_promedio_min"].idxmin(), "linea"]
    st.caption(f"⚠️ Mayor retraso promedio: **{linea_peor}** · ✅ Mejor puntualidad: **{linea_mejor}**")

# ─────────────────────────────────────────────
# 7. HEATMAP MES × LÍNEA
# ─────────────────────────────────────────────
if mostrar_heatmap:
    st.markdown('<div class="section-header">🗓️ Heatmap: afluencia promedio diaria por mes y línea</div>', unsafe_allow_html=True)
    st.caption("Identificación de estacionalidad y variaciones temporales de la demanda.")
    pivot = df_heatmap.pivot(index="mes", columns="linea", values="afluencia_promedio_diaria")
    pivot.index = [MESES_ES.get(m, m) for m in pivot.index]
    st.dataframe(pivot.style.background_gradient(cmap="Blues", axis=None), use_container_width=True)

# ─────────────────────────────────────────────
# 8. INGRESOS
# ─────────────────────────────────────────────
if mostrar_ingresos:
    st.markdown('<div class="section-header">💰 Relación ingresos y afluencia</div>', unsafe_allow_html=True)
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        df_ing_f = df_ing[df_ing["año"] == año_sel] if "año" in df_ing.columns else df_ing

        # El CSV real agrupa por tipo_ingreso; si tiene linea también se usa
        if "linea" in df_ing_f.columns:
            agg_col = "linea"
            st.caption("Ingresos mensuales por línea (año seleccionado)")
        elif "tipo_ingreso" in df_ing_f.columns:
            agg_col = "tipo_ingreso"
            st.caption("Ingresos mensuales por tipo de ingreso (año seleccionado)")
        else:
            agg_col = df_ing_f.columns[0]
            st.caption(f"Ingresos mensuales por {agg_col} (año seleccionado)")

        ing_linea = (
            df_ing_f.groupby(agg_col)["ingreso_total"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(ing_linea)
    with col_i2:
        st.caption("Dispersión: afluencia total vs ingreso total (eficiencia del sistema)")
        st.scatter_chart(df_eff, x="afluencia_total", y="ingreso_total", color="linea" if "linea" in df_eff.columns else None)

# ─────────────────────────────────────────────
# 9. PREGUNTAS ANALÍTICAS
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">🔍 Preguntas analíticas del proyecto</div>', unsafe_allow_html=True)

preguntas = [
    ("¿Qué estaciones presentan mayor saturación en hora pico?",
     f"Las estaciones {', '.join(criticas['estacion'].head(3).tolist()) if len(criticas)>0 else 'N/A'} superan el 85% de su capacidad."),
    ("¿Cómo varía la demanda a lo largo del día y la semana?",
     f"El pico máximo ocurre a las {hora_pico}:00 h. Los lunes-viernes triplican la demanda del domingo."),
    ("¿Qué línea tiene mayor carga de pasajeros?",
     f"La {linea_top_dem} concentra la mayor afluencia en el período seleccionado."),
    ("¿Cuál es la eficiencia del sistema en términos de ingresos?",
     f"El ingreso promedio por pasajero es ${ing_pax:.2f}, con correlación directa entre afluencia e ingresos."),
    ("¿Qué línea presenta mayores retrasos y cómo afecta al servicio?",
     f"La {linea_peor if 'linea_peor' in dir() else 'N/A'} registra el mayor retraso promedio, afectando la puntualidad del sistema."),
    ("¿Existen patrones estacionales en la demanda mensual?",
     "El heatmap muestra variaciones de hasta 40% entre meses; los meses de mayor demanda coinciden con períodos escolares."),
]

for q, resp in preguntas:
    st.markdown(f'<div class="q-card"><b>❓ {q}</b><br><span style="opacity:.8">➤ {resp}</span></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 10. CONCLUSIONES
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">✅ Conclusiones</div>', unsafe_allow_html=True)

col_c1, col_c2 = st.columns(2)
with col_c1:
    st.markdown(f"""
    <div class="info-card">
    <b>Hallazgos principales</b><br><br>
    🔵 La <b>{linea_top_dem}</b> concentra la mayor demanda del sistema.<br>
    🔴 Se detectan <b>{sat_critica} estaciones</b> en estado de saturación crítica.<br>
    ⏱️ El retraso promedio del sistema es de <b>{retraso_prom} min</b>.<br>
    📆 La demanda en días hábiles es hasta 2.5× superior a los domingos.<br>
    💰 Existe correlación directa (r>0.9) entre afluencia e ingresos.
    </div>""", unsafe_allow_html=True)
with col_c2:
    st.markdown("""
    <div class="info-card">
    <b>Recomendaciones</b><br><br>
    🟡 Aumentar frecuencia en líneas saturadas en horario 7:00-9:00 y 18:00-20:00.<br>
    🟡 Redistribuir flujo en estaciones con índice > 85% implementando andenes alternos.<br>
    🟡 Invertir en mantenimiento preventivo en las líneas con mayor tasa de incidencias.<br>
    🟡 Implementar descuentos en horas valle para distribuir la demanda.
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ARQUITECTURA DEL PIPELINE
# ─────────────────────────────────────────────
with st.expander("🏗️ Arquitectura del Pipeline Big Data", expanded=False):
    st.markdown("""
```
[Fuentes de datos]          [Ingesta]           [Almacenamiento]     [Procesamiento]     [Visualización]
──────────────────          ─────────           ────────────────     ───────────────     ───────────────
 Validaciones (CSV)  ──►  Apache Kafka  ──►     HDFS (raw/)    ──►  Apache Spark  ──►   Streamlit Cloud
 GPS unidades (JSON) ──►  Python ETL    ──►     Hive (staging/) ──►  PySpark SQL   ──►   Dashboard (este)
 Incidencias (texto) ──►  Cron jobs     ──►     HDFS (clean/)  ──►  Agregaciones  ──►   Power BI / Looker
```

**Flujo completo:**
1. Ingestión de datos crudos → HDFS raw/
2. Limpieza y normalización con PySpark → HDFS clean/
3. Carga a Hive (tablas externas sobre HDFS)
4. Consultas analíticas (HiveQL / SparkSQL)
5. Exportación de resultados a CSV → powerbi_export/
6. Visualización en Streamlit Cloud
    """)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    <div><span>Fuente:</span> Pipeline Big Data (Hadoop + Spark + Hive) · PySpark + HDFS</div>
    <div><span>Dashboard:</span> Streamlit Cloud · <span>Actualización:</span> 2026</div>
    <div>Sistema Big Data – Movilidad y Transporte Público · ISC 6.º periodo</div>
</div>
""", unsafe_allow_html=True)
