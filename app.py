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
    page_title="Dashboard Mercado Siderúrgico Brasileiro",
    layout="wide"
)

# ======================================================
# PATH BASE
# ======================================================
BASE_DIR = Path(__file__).resolve().parent

# ======================================================
# BACKGROUND + CSS (APLICADO UMA ÚNICA VEZ)
# ======================================================
def set_background(image_path: Path):
    if not image_path.exists():
        st.error(f"Imagem de fundo não encontrada: {image_path}")
        st.stop()

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

        h1, h2, h3, p, .stMarkdown {{
            color: #ffffff !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

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

    # Padroniza nomes para uso no app
    df = df.rename(columns={
        "exportacoes_volume": "exportacoes",
        "importacoes_volume": "importacoes",
        "saldo_comercial_volume": "saldo_comercial"
    })

    return df

df = load_data()

# ======================================================
# VALIDAÇÃO DAS COLUNAS (ANTI-ERRO)
# ======================================================
required_cols = [
    "date",
    "vendas_internas",
    "exportacoes",
    "importacoes",
    "consumo_aparente",
    "saldo_comercial"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no dataset: {missing}")
    st.stop()

# ======================================================
# TÍTULO E DESCRIÇÃO
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

anos_disponiveis = sorted(df["date"].dt.year.unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos",
    options=anos_disponiveis,
    default=anos_disponiveis[-3:]
)

df_f = df[df["date"].dt.year.isin(anos_selecionados)] if anos_selecionados else df.copy()

# ======================================================
# FUNÇÃO PADRÃO DE ESTILO PARA GRÁFICOS
# ======================================================
def apply_dark_style(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend=dict(font=dict(color="white"))
    )
    return fig

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

    melt1 = df_f.melt(
        id_vars="date",
        value_vars=["vendas_internas", "exportacoes"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig1 = px.bar(
        melt1,
        x="date",
        y="Volume (mil t)",
        color="Indicador",
        barmode="group"
    )

    pct_export = (
        df_f["exportacoes"]
        / (df_f["exportacoes"] + df_f["vendas_internas"])
    ) * 100

    fig1.add_trace(
        go.Scatter(
            x=df_f["date"],
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

    apply_dark_style(fig1)
    st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------------
# TAB 2 — Exportações vs Importações
# ------------------------------------------------------
with tab2:
    st.subheader("Exportações vs Importações")

    melt2 = df_f.melt(
        id_vars="date",
        value_vars=["exportacoes", "importacoes"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig2 = px.bar(
        melt2,
        x="date",
        y="Volume (mil t)",
        color="Indicador",
        barmode="group"
    )

    fig2.add_trace(
        go.Scatter(
            x=df_f["date"],
            y=df_f["saldo_comercial"],
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

    apply_dark_style(fig2)
    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------
# TAB 3 — Consumo Aparente vs Vendas Internas
# ------------------------------------------------------
with tab3:
    st.subheader("Consumo Aparente vs Vendas Internas")

    melt3 = df_f.melt(
        id_vars="date",
        value_vars=["consumo_aparente", "vendas_internas"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig3 = px.line(
        melt3,
        x="date",
        y="Volume (mil t)",
        color="Indicador"
    )

    apply_dark_style(fig3)
    st.plotly_chart(fig3, use_container_width=True)

# ======================================================
# RODAPÉ
# ======================================================
st.markdown("---")
st.caption("Elisângela de Souza | Dados atualizados até dez/2025")
