import streamlit as st
import pandas as pd
import os

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================
st.set_page_config(
    page_title="Sistema Big Data - Transporte Público",
    page_icon="🚇",
    layout="wide"
)

# =====================================================
# CARGA DE DATOS
# =====================================================
@st.cache_data
def load_data():

    base = "powerbi_export"

    data = {}

    files = [
        "01_afluencia_diaria",
        "02_afluencia_mensual",
        "03_afluencia_anual",
        "04_top_estaciones",
        "05_heatmap_mes_linea",
        "06_tendencia_anual",
        "07_demanda_tipo_dia",
        "08_saturacion_estaciones",
        "09_ingresos_mensual",
        "10_ingresos_vs_afluencia"
    ]

    for f in files:

        path = os.path.join(base, f"{f}.csv")

        if os.path.exists(path):

            try:

                data[f] = pd.read_csv(path, encoding="utf-8")

            except:

                data[f] = pd.read_csv(path, encoding="latin1")

    return data


data = load_data()

# =====================================================
# HEADER
# =====================================================
st.title("🚇 Sistema Big Data para Análisis de Movilidad y Transporte Público")

st.markdown("""
Este dashboard analiza patrones de movilidad en transporte público considerando:

- Rutas
- Horarios
- Demanda
- Saturación
- Comportamiento temporal
- Ingresos del sistema
""")

st.markdown("---")

# =====================================================
# JUSTIFICACIÓN BIG DATA
# =====================================================
st.subheader("Justificación Big Data")

st.markdown("""
El proyecto utiliza tecnologías Big Data debido al gran volumen de registros históricos
de movilidad, la necesidad de procesamiento distribuido mediante Spark,
almacenamiento en HDFS y análisis masivo de patrones temporales
y demanda del transporte público.
""")

st.markdown("---")

# =====================================================
# FILTROS
# =====================================================
st.sidebar.header("Filtros")

df_mensual = data["02_afluencia_mensual"]

anios = sorted(df_mensual["anio"].dropna().unique())
lineas = sorted(df_mensual["linea"].dropna().unique())

anio_sel = st.sidebar.selectbox(
    "Selecciona año",
    anios
)

linea_sel = st.sidebar.multiselect(
    "Selecciona líneas",
    lineas,
    default=lineas
)

df_filtrado = df_mensual[
    (df_mensual["anio"] == anio_sel) &
    (df_mensual["linea"].isin(linea_sel))
]

# =====================================================
# KPIs
# =====================================================
st.subheader("Indicadores principales")

col1, col2, col3, col4 = st.columns(4)

total_pasajeros = int(df_filtrado["afluencia_total"].sum())

promedio_diario = int(
    df_filtrado["afluencia_promedio_diaria"].mean()
)

df_ing = data["09_ingresos_mensual"]

ingreso_total = int(
    df_ing["ingreso_total"].sum()
)

df_eff = data["10_ingresos_vs_afluencia"]

ingreso_pasajero = (
    df_eff["ingreso_por_pasajero"]
    .fillna(0)
    .mean()
)

col1.metric(
    "Total Pasajeros",
    f"{total_pasajeros:,}"
)

col2.metric(
    "Promedio Diario",
    f"{promedio_diario:,}"
)

col3.metric(
    "Ingreso Total",
    f"${ingreso_total:,}"
)

col4.metric(
    "Ingreso por Pasajero",
    f"${ingreso_pasajero:,.2f}"
)

st.markdown("---")

# =====================================================
# TENDENCIA ANUAL
# =====================================================
st.subheader("Tendencia anual de movilidad")

trend = data["06_tendencia_anual"]

st.line_chart(
    trend.set_index("anio")["afluencia_sistema_total"]
)

st.markdown("---")

# =====================================================
# DEMANDA POR LÍNEA
# =====================================================
st.subheader("🚆 Demanda por línea")

demanda_linea = (
    df_filtrado
    .groupby("linea")["afluencia_total"]
    .sum()
)

st.bar_chart(demanda_linea)

st.markdown("---")

# =====================================================
# TOP ESTACIONES
# =====================================================
st.subheader("🏙️ Top estaciones con mayor demanda")

top_estaciones = (
    data["04_top_estaciones"]
    .nlargest(10, "afluencia_total")
)

st.bar_chart(
    top_estaciones.set_index("estacion")["afluencia_total"]
)

st.markdown("---")

# =====================================================
# SATURACIÓN
# =====================================================
st.subheader("Estaciones con mayor saturación")

sat = (
    data["08_saturacion_estaciones"]
    .sort_values(
        "indice_saturacion",
        ascending=False
    )
    .head(10)
)

st.bar_chart(
    sat.set_index("estacion")["indice_saturacion"]
)

st.dataframe(sat)

st.markdown("---")

# =====================================================
# HEATMAP
# =====================================================
st.subheader("Heatmap mes vs línea")

pivot = data["05_heatmap_mes_linea"].pivot(
    index="mes",
    columns="linea",
    values="afluencia_promedio_diaria"
)

st.dataframe(
    pivot.style.background_gradient(cmap="Reds")
)

st.markdown("---")

# =====================================================
# INGRESOS VS AFLUENCIA
# =====================================================
st.subheader("Relación ingresos vs afluencia")

st.scatter_chart(
    data["10_ingresos_vs_afluencia"],
    x="afluencia_total",
    y="ingreso_total"
)

st.markdown("---")

# =====================================================
# PREGUNTAS ANALÍTICAS
# =====================================================
st.subheader("Preguntas analíticas")

st.markdown("""
- ¿Qué estaciones presentan mayor saturación?
- ¿Cómo cambia la demanda según el tiempo?
- ¿Qué líneas tienen mayor carga?
- ¿Cuál es la eficiencia del sistema?
- ¿Existe relación entre afluencia e ingresos?
""")

st.markdown("---")

# =====================================================
# CONCLUSIONES
# =====================================================
st.subheader("Conclusiones")

linea_top = (
    demanda_linea.idxmax()
)

st.markdown(f"""
- La línea con mayor demanda fue **{linea_top}**.
- Se identifican patrones de alta demanda en periodos laborales.
- Algunas estaciones presentan saturación crítica.
- Los ingresos muestran relación directa con la afluencia.
- Existen oportunidades de optimización en horarios pico.
""")

st.markdown("---")

# =====================================================
# FUENTE
# =====================================================
st.subheader("Fuente")

st.markdown("""
**Fuente:** Pipeline Big Data (Hadoop + Spark + Hive)  
**Procesamiento:** PySpark + HDFS  
**Dashboard:** Streamlit Cloud  
**Fecha de actualización:** 2026
""")
