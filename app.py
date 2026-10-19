import pandas as pd
import plotly.express as px
import streamlit as st

# Criterio 2.1.1: Configuración de software y parámetros
st.set_page_config(
    page_title="Dashboard Ejecutivo de Ventas y Márgenes",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    data = pd.read_csv("clean_sales_data.csv")
    data["order_date"] = pd.to_datetime(data["order_date"])
    return data


df = load_data()

# Barra lateral: Filtros con propósito
st.sidebar.header("Filtros Globales")
regions = st.sidebar.multiselect(
    "Seleccionar Regiones:",
    options=sorted(df["region"].unique()),
    default=sorted(df["region"].unique()),
)

categories = st.sidebar.multiselect(
    "Seleccionar Categorías:",
    options=sorted(df["category"].unique()),
    default=sorted(df["category"].unique()),
)

filtered_df = df[
    (df["region"].isin(regions)) & (df["category"].isin(categories))
]

# Encabezado Narrativo: Contexto
st.title("Panel de Control: Rendimiento Comercial y Rentabilidad")
st.markdown(
    "Evaluación de ingresos netos, comportamiento de devoluciones y márgenes por descuento."
)

# Tarjetas KPI
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Ingresos Netos", f"${filtered_df['net_revenue'].sum():,.0f}")
kpi2.metric("Órdenes Totales", f"{filtered_df['order_id'].nunique():,}")
kpi3.metric(
    "Tasa de Retorno Global",
    f"{(filtered_df['returned'].mean() * 100):.1f}%",
)
kpi4.metric(
    "Margen Operativo Promedio",
    f"{filtered_df['profit_margin'].mean():.1f}%",
)

st.divider()

# Fila 1: Complejidad Baja e Intermedia
col_izq, col_der = st.columns([1, 1])

with col_izq:
    st.subheader("1. Tendencia Temporal de Ingresos Netos")
    df_trend = (
        filtered_df.set_index("order_date")
        .resample("ME")["net_revenue"]
        .sum()
        .reset_index()
    )
    fig_line = px.line(
        df_trend,
        x="order_date",
        y="net_revenue",
        markers=True,
        labels={"order_date": "Mes", "net_revenue": "Ingresos Netos ($)"},
        color_discrete_sequence=["#0d6efd"],
    )
    fig_line.update_layout(xaxis_title="", yaxis_title="Ingresos ($)")
    st.plotly_chart(fig_line, use_container_width=True)

with col_der:
    st.subheader("2. Tasa de Devolución por Categoría")
    df_ret = (
        filtered_df.groupby("category")
        .agg(tasa_ret=("returned", "mean"))
        .reset_index()
    )
    df_ret["tasa_ret"] = df_ret["tasa_ret"] * 100
    fig_bar = px.bar(
        df_ret.sort_values(by="tasa_ret", ascending=True),
        x="tasa_ret",
        y="category",
        orientation="h",
        color="tasa_ret",
        color_continuous_scale="Reds",
        labels={"tasa_ret": "% Devolución", "category": "Categoría"},
    )
    fig_bar.update_layout(xaxis_title="% Devolución", yaxis_title="")
    st.plotly_chart(fig_bar, use_container_width=True)

# Fila 2: Complejidad Alta (Dispersión multivariable con línea umbral)
st.subheader("3. Diagnóstico de Rentabilidad: Descuentos vs. Margen")
fig_scatter = px.scatter(
    filtered_df,
    x="discount",
    y="profit_margin",
    color="category",
    size="sales",
    hover_data=["region", "order_id"],
    opacity=0.7,
    labels={
        "discount": "Descuento Aplicado (Ratio)",
        "profit_margin": "Margen de Ganancia (%)",
        "category": "Categoría",
        "sales": "Ventas Brutas",
    },
)
# Línea de referencia en margen cero
fig_scatter.add_hline(
    y=0,
    line_dash="dash",
    line_color="#dc3545",
    annotation_text="Punto de Equilibrio (0% Margen)",
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Criterio 2.1.5: Declaración Ética en el pie
st.divider()
with st.expander("Declaración de Ética, Privacidad y Origen de Datos"):
    st.write(
        """
    - **Protección de Datos:** Se aplicó seudonimización mediante hashing SHA-256 sobre datos de clientes, eliminando nombres y correos.
    - **Transparencia Visual:** Las escalas numéricas y ejes temporales no han sido truncados para evitar distorsiones cognitivas.
    - **Licencia:** Datos tratados exclusivamente con fines académicos y evaluativos bajo estándares abiertos.
    """
    )