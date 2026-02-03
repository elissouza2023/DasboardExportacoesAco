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
# BACKGROUND + CSS CUSTOMIZADO
# ======================================================
def set_background(image_path: Path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
            /* Plano de fundo geral */
            .stApp {{
                background-image: url(data:image/jpg;base64,{encoded});
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                background: rgba(0, 0, 0, 0.5); /* Escurece um pouco mais para contraste */
                z-index: -1;
            }}

            /* CORREÇÃO DO EFEITO VIDRO: Aplicando diretamente nos cards dos gráficos */
            div[data-testid="stVerticalBlock"] > div.element-container:has(iframe),
            div[data-testid="stVerticalBlock"] > div.stPlotlyChart {{
                background: rgba(255, 255, 255, 0.07);
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 20px;
                margin-bottom: 20px;
            }}

            /* CUSTOMIZAÇÃO DA SIDEBAR (Filtros) - Cor #b74803 */
            section[data-testid="stSidebar"] {{
                background-color: rgba(183, 72, 3, 0.15); /* #b74803 com transparência */
                backdrop-filter: blur(10px);
            }}
            
            section[data-testid="stSidebar"] h1, 
            section[data-testid="stSidebar"] h2, 
            section[data-testid="stSidebar"] label {{
                color: #e09e50 !important; /* Destaque nos títulos da barra lateral */
            }}

            /* BOTÕES DOS FILTROS (Multiselect) - Cor #e09e50 */
            span[data-baseweb="tag"] {{
                background-color: #e09e50 !important;
                color: white !important;
            }}
            
            /* Ajuste de cores de textos */
            h1, h2, h3, p, span, label {{
                color: white !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

BASE_DIR = Path(__file__).resolve().parent
# Certifique-se que o caminho da imagem está correto
set_background(BASE_DIR / "assets" / "fundo.jpg")

# ======================================================
# ESTILO PADRÃO DOS GRÁFICOS
# ======================================================
def apply_plotly_layout(fig):
    fig.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend=dict(
            bgcolor="rgba(0,0,0,0.2)",
            font=dict(color="white")
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
    )
    return fig

# ======================================================
# CARREGAMENTO DOS DADOS (Mantido original)
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
# TÍTULO E INTERFACE
# ======================================================
st.title("📊 Dashboard Mercado Siderúrgico Brasileiro")
st.markdown("Explore vendas internas, exportações, importações e consumo aparente. Fonte: Instituto Aço Brasil / MDIC.")

# SIDEBAR – FILTROS
st.sidebar.header("Configurações")
anos = sorted(df["date"].dt.year.unique())
anos_sel = st.sidebar.multiselect(
    "Selecione os anos para análise:",
    options=anos,
    default=anos[-3:]
)

df_f = df[df["date"].dt.year.isin(anos_sel)] if anos_sel else df.copy()

# ABAS
tab1, tab2, tab3 = st.tabs([
    "📦 Vendas vs Exportações",
    "🚢 Exportação vs Importação",
    "📈 Consumo Aparente"
])

# TAB 1 - Vendas Internas vs Exportações
with tab1:
    st.subheader("Vendas Internas vs Exportações")
    
    melt1 = df_f.melt(
        id_vars="date",
        value_vars=["vendas_internas", "exportacoes_volume"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    # Cores da paleta aplicada ao gráfico
    fig1 = px.bar(
        melt1, x="date", y="Volume (mil t)",
        color="Indicador", barmode="group",
        color_discrete_map={
            "vendas_internas": "#e09e50", # Ouro Queimado
            "exportacoes_volume": "#b74803" # Ferrugem
        }
    )

    total = df_f["exportacoes_volume"] + df_f["vendas_internas"]
    pct = (df_f["exportacoes_volume"] / total * 100).where(total != 0, 0)

    fig1.add_trace(go.Scatter(
        x=df_f["date"], y=pct, name="% Exportações",
        yaxis="y2", line=dict(dash="dash", color="#ffffff")
    ))

    fig1.update_layout(
        yaxis2=dict(overlaying="y", side="right", title="% Exportações", range=[0, 100], showgrid=False)
    )

    st.plotly_chart(apply_plotly_layout(fig1), use_container_width=True, config={'displayModeBar': False})

# TAB 2 - Exportações vs Importações
with tab2:
    st.subheader("Fluxo Comercial")
    
    melt2 = df_f.melt(
        id_vars="date",
        value_vars=["exportacoes_volume", "importacoes_volume"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig2 = px.bar(
        melt2, x="date", y="Volume (mil t)",
        color="Indicador", barmode="group",
        color_discrete_sequence=["#b74803", "#509ee0"] # Ferrugem vs um Azul para contraste
    )

    st.plotly_chart(apply_plotly_layout(fig2), use_container_width=True, config={'displayModeBar': False})

# TAB 3 - Consumo
with tab3:
    st.subheader("Consumo Aparente vs Vendas Internas")
    
    melt3 = df_f.melt(
        id_vars="date",
        value_vars=["consumo_aparente", "vendas_internas"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig3 = px.line(
        melt3, x="date", y="Volume (mil t)", color="Indicador",
        color_discrete_map={"consumo_aparente": "#ffffff", "vendas_internas": "#e09e50"}
    )

    st.plotly_chart(apply_plotly_layout(fig3), use_container_width=True, config={'displayModeBar': False})

st.markdown("---")
st.caption("Elisângela de Souza | Dados atualizados até dez/2025")