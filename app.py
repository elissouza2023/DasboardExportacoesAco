import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64

# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================
st.set_page_config(
    page_title="Dashboard Siderurgia BR",
    layout="wide"
)

# ======================================================
# BACKGROUND + CSS (UMA ÚNICA VEZ)
# ======================================================
def set_background(image_path: Path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        section[data-testid="stSidebar"] {{
            background-color: #f0f2f6;
        }}

        .stTitle, .stSubheader, h1, h2, h3, p {{
            color: #ffffff !important;
        }}

        .stMarkdown {{
            color: #ffffff !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

BASE_DIR = Path(__file__).resolve().parent
set_background(BASE_DIR / "assets" / "fundo.jpg")

# ======================================================
# CARREGAMENTO DOS DADOS
# ======================================================
@st.cache_data
def load_data():
    data_path = BASE_DIR / "data" / "processed" / "dados_siderurgia_limpos_2013_2025.csv"

    if not data_path.exists():
        st.error(f"Arquivo não encontrado: {data_path}")
        st.stop()

    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ======================================================
# VALIDAÇÃO DAS COLUNAS (ANTI-KeyError)
# ======================================================
required_cols = [
    "vendas_internas",
    "exportacoes",
    "importacoes",
    "consumo_aparente"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no dataset: {missing}")
    st.stop()

# ======================================================
# TÍTULO
# ======================================================
st.title("Dashboard Mercado Siderúrgico Brasileiro")
st.markdown(
    """
    Explore vendas internas, exportações, importações e consumo aparente.  
    **Fonte:** Instituto Aço Brasil / MDIC.
    """
)

# ======================================================
# SIDEBAR — FILTROS
# ======================================================
st.sidebar.header("Filtros")

anos = sorted(df["date"].dt.year.unique())
anos_sel = st.sidebar.multiselect(
    "Selecione os anos",
    options=anos,
    default=anos[-3:]
)

df_f = df[df["date"].dt.year.isin(anos_sel)] if anos_sel else df.copy()

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "Vendas Internas vs Exportações",
    "Exportações vs Importações",
    "Consumo Aparente vs Vendas Internas"
])

# ------------------------------------------------------
# TAB 1
# ------------------------------------------------------
with tab1:
    st.subheader("Vendas Internas vs Exportações")

    melt1 = df_f.melt(
        id_vars="date",
        value_vars=["vendas_internas", "exportacoes"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig = px.bar(melt1, x="date", y="Volume (mil t)", color="Indicador", barmode="group")

    pct = (df_f["exportacoes"] / (df_f["exportacoes"] + df_f["vendas_internas"])) * 100
    fig.add_trace(go.Scatter(x=df_f["date"], y=pct, name="% Exportações", yaxis="y2"))

    fig.update_layout(yaxis2=dict(overlaying="y", side="right", title="% Exportações"))
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# TAB 2
# ------------------------------------------------------
with tab2:
    st.subheader("Exportações vs Importações")

    melt2 = df_f.melt(
        id_vars="date",
        value_vars=["exportacoes", "importacoes"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig = px.bar(melt2, x="date", y="Volume (mil t)", color="Indicador", barmode="group")

    saldo = df_f["exportacoes"] - df_f["importacoes"]
    fig.add_trace(go.Scatter(x=df_f["date"], y=saldo, name="Saldo Comercial", yaxis="y2"))

    fig.update_layout(yaxis2=dict(overlaying="y", side="right", title="Saldo (mil t)"))
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# TAB 3
# ------------------------------------------------------
with tab3:
    st.subheader("Consumo Aparente vs Vendas Internas")

    melt3 = df_f.melt(
        id_vars="date",
        value_vars=["consumo_aparente", "vendas_internas"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig = px.line(melt3, x="date", y="Volume (mil t)", color="Indicador")
    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# RODAPÉ
# ======================================================
st.markdown("---")
st.caption("Elisângela de Souza | Dados atualizados até dez/2025")
