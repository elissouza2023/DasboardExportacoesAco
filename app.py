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
# FUNÇÃO PARA BACKGROUND
# ======================================================
def set_background(image_file):
    with open(image_file, "rb") as f:
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

        h1, h2, h3, p {{
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# APLICA BACKGROUND (UMA ÚNICA VEZ)
# ======================================================
BASE_DIR = Path(__file__).resolve().parent
BG_IMAGE = BASE_DIR / "assets" / "fundo.jpg"
set_background(BG_IMAGE)

# ======================================================
# CARREGAMENTO DOS DADOS
# ======================================================
@st.cache_data
def load_data():
    DATA_PATH = BASE_DIR / "data" / "processed" / "dados_siderurgia_limpos_2013_2025.csv"

    if not DATA_PATH.exists():
        st.error(f"Arquivo não encontrado: {DATA_PATH}")
        st.stop()

    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ======================================================
# TÍTULO E DESCRIÇÃO
# ======================================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/jpg;base64,{encoded});
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: #f0f2f6;
    }}

    /* Títulos e textos principais */
    .stTitle, .stSubheader, h1, h2, h3, p {{
        color: #ffffff !important;
    }}

    /* Texto padrão */
    .stMarkdown {{
        color: #ffffff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# SIDEBAR — FILTROS
# ======================================================
st.sidebar.header("Filtros")

anos_disponiveis = sorted(df["date"].dt.year.unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos",
    options=anos_disponiveis,
    default=anos_disponiveis[-3:]
)

if anos_selecionados:
    df_filtrado = df[df["date"].dt.year.isin(anos_selecionados)]
else:
    df_filtrado = df.copy()

# ======================================================
# TABS
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "Vendas Internas vs Exportações",
    "Exportações vs Importações",
    "Consumo Aparente vs Vendas Internas"
])

# ------------------------------------------------------
# TAB 1 — Vendas Internas vs Exportações
# ------------------------------------------------------
with tab1:
    st.subheader("Vendas Internas vs Exportações")

    df_melt1 = df_filtrado.melt(
        id_vars="date",
        value_vars=["vendas_internas", "exportacoes_volume"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig1 = px.bar(
        df_melt1,
        x="date",
        y="Volume (mil t)",
        color="Indicador",
        barmode="group"
    )

    pct_export = (
        df_filtrado["exportacoes_volume"]
        / (df_filtrado["vendas_internas"] + df_filtrado["exportacoes_volume"])
    ) * 100

    fig1.add_trace(
        go.Scatter(
            x=df_filtrado["date"],
            y=pct_export,
            name="% Exportações",
            yaxis="y2",
            line=dict(dash="dash")
        )
    )

    fig1.update_layout(
        yaxis2=dict(
            title="% Exportações",
            overlaying="y",
            side="right"
        )
    )

    st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------------
# TAB 2 — Exportações vs Importações (Saldo Comercial)
# ------------------------------------------------------
with tab2:
    st.subheader("Exportações vs Importações")

    df_melt2 = df_filtrado.melt(
        id_vars="date",
        value_vars=["exportacoes_volume", "importacoes"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig2 = px.bar(
        df_melt2,
        x="date",
        y="Volume (mil t)",
        color="Indicador",
        barmode="group"
    )

    saldo = df_filtrado["exportacoes_volume"] - df_filtrado["importacoes"]

    fig2.add_trace(
        go.Scatter(
            x=df_filtrado["date"],
            y=saldo,
            name="Saldo Comercial",
            yaxis="y2",
            line=dict(dash="dot")
        )
    )

    fig2.update_layout(
        yaxis2=dict(
            title="Saldo (mil t)",
            overlaying="y",
            side="right"
        )
    )

    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------
# TAB 3 — Consumo Aparente vs Vendas Internas
# ------------------------------------------------------
with tab3:
    st.subheader("Consumo Aparente vs Vendas Internas")

    df_melt3 = df_filtrado.melt(
        id_vars="date",
        value_vars=["consumo_aparente", "vendas_internas"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig3 = px.line(
        df_melt3,
        x="date",
        y="Volume (mil t)",
        color="Indicador"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ======================================================
# RODAPÉ
# ======================================================
st.markdown("---")
st.caption("Elisângela de Souza | Dados atualizados até dez/2025")
