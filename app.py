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
                background: rgba(0, 0, 0, 0.55); /* Escurecemos um pouco mais para ajudar na leitura */
                z-index: -1;
            }}

            /* Efeito Vidro nos Gráficos */
            div[data-testid="stVerticalBlock"] > div.stPlotlyChart {{
                background: rgba(0, 0, 0, 0.4); /* Fundo escuro leve para destacar o gráfico */
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 15px;
            }}

            /* MELHORIA DE LEITURA: Sombra nos textos brancos */
            h1, h2, h3, p, label, .stTabs [data-baseweb="tab"] p {{
                color: white !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
            }}

            /* RODAPÉ ESTILIZADO */
            .footer-container {{
                background: rgba(0, 0, 0, 0.6);
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                margin-top: 50px;
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
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=14), # Aumentamos um pouco a fonte
        legend=dict(
            bgcolor="rgba(0,0,0,0.5)",
            font=dict(color="white", size=12),
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(size=12, color="white", family="Arial Black"), # Fonte mais "gorda"
            titlefont=dict(size=14, color="white")
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(size=12, color="white", family="Arial Black"),
            titlefont=dict(size=14, color="white")
        )
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
# ======================================================
# RODAPÉ
# ======================================================
st.markdown(
    """
    <div class="footer-container">
        <p style="margin:0; font-size: 0.9rem; opacity: 0.9;">
            Elisângela de Souza | Dados atualizados até dez/2025
        </p>
    </div>
    """,
    unsafe_allow_html=True
)