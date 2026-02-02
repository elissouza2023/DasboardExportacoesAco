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
# BACKGROUND + CSS (UMA ÚNICA VEZ)
# ======================================================
def set_background(image_path: Path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        /* Fundo principal */
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

        /* Títulos e textos */
        h1, h2, h3, p, span {{
            color: #ffffff !important;
        }}

        /* Glassmorphism para gráficos */
        .glass-card {
            width: 100%;
            background: rgba(15, 15, 15, 0.60);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 18px;
            padding: 24px;
            margin: 24px 0;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

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
# VALIDAÇÃO DAS COLUNAS (ANTI-ERRO)
# ======================================================
required_cols = [
    "date",
    "consumo_aparente",
    "exportacoes_volume",
    "vendas_internas",
    "importacoes_volume",
    "saldo_comercial_volume"
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

# ======================================================
# FUNÇÃO PADRÃO DE LAYOUT PLOTLY (TRANSPARENTE)
# ======================================================
def apply_plotly_layout(fig):
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.15)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.15)")
    )
    return fig

# ======================================================
# TAB 1 — Vendas Internas vs Exportações
# ======================================================
with tab1:
    st.subheader("Vendas Internas vs Exportações")

    melt1 = df_f.melt(
        id_vars="date",
        value_vars=["vendas_internas", "exportacoes_volume"],
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
        df_f["exportacoes_volume"]
        / (df_f["exportacoes_volume"] + df_f["vendas_internas"])
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

    fig1 = apply_plotly_layout(fig1)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# TAB 2 — Exportações vs Importações
# ======================================================
with tab2:
    st.subheader("Exportações vs Importações")

    melt2 = df_f.melt(
        id_vars="date",
        value_vars=["exportacoes_volume", "importacoes_volume"],
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
            y=df_f["saldo_comercial_volume"],
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

    fig2 = apply_plotly_layout(fig2)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# TAB 3 — Consumo Aparente vs Vendas Internas
# ======================================================
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

    fig3 = apply_plotly_layout(fig3)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# RODAPÉ
# ======================================================
st.markdown("---")
st.caption("Elisângela de Souza | Dados atualizados até dez/2025")
