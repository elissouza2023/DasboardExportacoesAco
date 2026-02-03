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
# BACKGROUND + CSS AJUSTADO
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
                background: rgba(0, 0, 0, 0.45);  /* overlay mais forte para contraste */
                z-index: -1;
            }}
            section[data-testid="stSidebar"] {{
                background-color: #f0f2f6;
            }}
            h1, h2, h3, p, .stMarkdown {{
                color: #ffffff !important;
            }}
            .glass-card {{
                background: rgba(15, 15, 25, 0.65) !important;
                backdrop-filter: blur(14px) !important;
                -webkit-backdrop-filter: blur(14px) !important;
                border-radius: 16px !important;
                padding: 1.5rem !important;
                margin: 1.5rem 0 2.5rem 0 !important;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6) !important;
                border: 1px solid rgba(255, 255, 255, 0.18) !important;
                overflow: hidden !important;
                position: relative !important;
                min-height: 520px !important;
            }}
            .glass-card > div[data-testid="stPlotlyChart"] {{
                width: 100% !important;
                height: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

BASE_DIR = Path(__file__).resolve().parent
set_background(BASE_DIR / "assets" / "fundo.jpg")

# ======================================================
# FUNÇÃO DE ESTILO DOS GRÁFICOS
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
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.15)",
            title_font_color="white",
            tickfont_color="white"
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.15)",
            title_font_color="white",
            tickfont_color="white"
        )
    )
    return fig

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
# TÍTULO PRINCIPAL
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
    default=anos[-3:]  # últimos 3 anos por padrão
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
# TAB 1 — Vendas Internas vs Exportações
# ======================================================
with tab1:
    st.subheader("Vendas Internas vs Exportações")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
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
        
        total = df_f["exportacoes_volume"] + df_f["vendas_internas"]
        pct = (df_f["exportacoes_volume"] / total * 100).where(total != 0, 0)
        
        fig1.add_trace(
            go.Scatter(
                x=df_f["date"],
                y=pct,
                name="% Exportações",
                yaxis="y2",
                line=dict(dash="dash", color="red")
            )
        )
        
        fig1.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                title="% Exportações",
                showgrid=False,
                range=[-3000, 100]  # ajuste se o % negativo cortar muito
            ),
            height=550
        )
        
        fig1 = apply_plotly_layout(fig1)
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# TAB 2 — Exportações vs Importações
# ======================================================
with tab2:
    st.subheader("Exportações vs Importações")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
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
        
        saldo = df_f["exportacoes_volume"] - df_f["importacoes_volume"]
        
        fig2.add_trace(
            go.Scatter(
                x=df_f["date"],
                y=saldo,
                name="Saldo Comercial",
                yaxis="y2",
                line=dict(color="cyan")
            )
        )
        
        fig2.update_layout(
            yaxis2=dict(
                overlaying="y",
                side="right",
                title="Saldo (mil t)",
                showgrid=False
            ),
            height=550
        )
        
        fig2 = apply_plotly_layout(fig2)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# TAB 3 — Consumo Aparente vs Vendas Internas
# ======================================================
with tab3:
    st.subheader("Consumo Aparente vs Vendas Internas")
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
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
        
        fig3.update_layout(height=550)
        fig3 = apply_plotly_layout(fig3)
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# RODAPÉ
# ======================================================
st.markdown("---")
st.caption("Elisângela de Souza | Dados atualizados até dez/2025")