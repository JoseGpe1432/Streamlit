import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Movilidad Transporte Público", layout="wide")

# ==============================
# FASE 1: CARGA DE DATOS
# ==============================
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
            data[f] = pd.read_csv(path)

    return data

data = load_data()

# ==============================
# FASE 2: HEADER
# ==============================
st.title("Sistema Big Data para Análisis de Movilidad y Transporte Público")

st.markdown("""
Este dashboard analiza patrones de movilidad en transporte público considerando:
- Rutas
- Horarios
- Demanda
- Saturación
- Comportamiento temporal
""")

# ==============================
# FASE 3: FILTROS
# ==============================
st.sidebar.header("Filtros")

df_mensual = data["02_afluencia_mensual"]

anios = sorted(df_mensual["anio"].dropna().unique())
lineas = sorted(df_mensual["linea"].dropna().unique())

anio_sel = st.sidebar.selectbox("Año", anios)
linea_sel = st.sidebar.multiselect("Línea", lineas, default=lineas)

df_filtrado = df_mensual[
    (df_mensual["anio"] == anio_sel) &
    (df_mensual["linea"].isin(linea_sel))
]

# ==============================
# FASE 4: KPIs
# ==============================
st.subheader("Indicadores principales")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Pasajeros", int(df_filtrado["afluencia_total"].sum()))
col2.metric("Promedio Diario", int(df_filtrado["afluencia_promedio_diaria"].mean()))

df_ing = data["09_ingresos_mensual"]
col3.metric("Ingreso Total", int(df_ing["ingreso_total"].sum()))

df_eff = data["10_ingresos_vs_afluencia"]
col4.metric("Ingreso por Pasajero", round(df_eff["ingreso_por_pasajero"].mean(), 4))

# ==============================
# FASE 5: GRÁFICAS
# ==============================

st.subheader("Tendencia anual")
st.line_chart(data["06_tendencia_anual"].set_index("anio")["afluencia_sistema_total"])

st.subheader("Demanda por línea")
st.bar_chart(df_filtrado.groupby("linea")["afluencia_total"].sum())

st.subheader("Top estaciones")
st.bar_chart(data["04_top_estaciones"].nlargest(10, "afluencia_total").set_index("estacion")["afluencia_total"])

st.subheader("Saturación")
st.dataframe(data["08_saturacion_estaciones"].sort_values("indice_saturacion", ascending=False).head(10))

st.subheader("Heatmap mes vs línea")
pivot = data["05_heatmap_mes_linea"].pivot(index="mes", columns="linea", values="afluencia_promedio_diaria")
st.dataframe(pivot)

st.subheader("Ingresos vs Afluencia")
st.scatter_chart(data["10_ingresos_vs_afluencia"], x="afluencia_total", y="ingreso_total")

# ==============================
# FASE 6: PREGUNTAS ANALÍTICAS
# ==============================
st.subheader("Preguntas analíticas")

st.markdown("""
- ¿Qué estaciones presentan mayor saturación?
- ¿Cómo cambia la demanda según el tiempo?
- ¿Qué líneas tienen mayor carga?
- ¿Cuál es la eficiencia del sistema?
""")

# ==============================
# FASE 7: CONCLUSIONES
# ==============================
st.subheader("Conclusiones")

st.markdown("""
- Se identifican patrones de alta demanda en días laborales.
- Algunas estaciones presentan saturación crítica.
- La demanda impacta directamente en los ingresos.
- Existen oportunidades de optimización en horarios pico.
""")

# ==============================
# FASE 8: FUENTE
# ==============================
st.subheader("Fuente")

st.markdown("""
Fuente: Pipeline Big Data (Hadoop + Spark + Hive)  
Fecha de actualización: 2026  
""")