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
# BACKGROUND + CSS (ESTÁVEL E SEGURO)
# ======================================================
def set_background(image_path: Path):
    if not image_path.exists():
        return
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
            /* Fundo da Aplicação */
            .stApp {{
                background-image: url(data:image/jpg;base64,{encoded});
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            /* Camada de escurecimento para contraste */
            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                background: rgba(0, 0, 0, 0.6);
                z-index: -1;
            }}

            /* Leitura de textos e títulos */
            h1, h2, h3, p, label {{
                color: white !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }}

            /* Estilização da Sidebar (Filtros) */
            section[data-testid="stSidebar"] {{
                background-color: rgba(0, 0, 0, 0.4);
                backdrop-filter: blur(10px);
            }}

            /* Cor dos botões/tags de filtro (#e09e50) */
            span[data-baseweb="tag"] {{
                background-color: #e09e50 !important;
                color: white !important;
            }}

            /* Ajuste das Abas */
            .stTabs [data-baseweb="tab"] p {{
                color: white !important;
                font-weight: bold;
                font-size: 16px;
            }}
            
            /* Rodapé fixo */
            .custom-footer {{
                background-color: rgba(0, 0, 0, 0.75);
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin-top: 30px;
                border: 1px solid rgba(255,255,255,0.1);
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

BASE_DIR = Path(__file__).resolve().parent
set_background(BASE_DIR / "assets" / "fundo.jpg")

# ======================================================
# ESTILO PADRÃO DOS GRÁFICOS (ALTO CONTRASTE)
# ======================================================
def apply_plotly_layout(fig):
    fig.update_layout(
        autosize=True,
        margin=dict(l=60, r=60, t=50, b=60),
        # Efeito vidro simulado via Plotly
        paper_bgcolor="rgba(30, 30, 30, 0.7)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=13),
        legend=dict(
            bgcolor="rgba(0,0,0,0.6)",
            font=dict(color="white", size=11),
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="white", size=12),
            title_font=dict(size=14)
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="white", size=12),
            title_font=dict(size=14)
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
# INTERFACE PRINCIPAL
# ======================================================
st.title("📊 Dashboard Mercado Siderúrgico Brasileiro")
st.markdown("Explore vendas internas, exportações, importações e consumo aparente. **Fonte:** Instituto Aço Brasil / MDIC.")

# SIDEBAR – FILTROS
st.sidebar.header("Filtros de Análise")
anos = sorted(df["date"].dt.year.unique())
anos_sel = st.sidebar.multiselect(
    "Selecione os anos:",
    options=anos,
    default=anos[-3:] if len(anos) >= 3 else anos
)

df_f = df[df["date"].dt.year.isin(anos_sel)] if anos_sel else df.copy()

# ESTRUTURA DE ABAS
tab1, tab2, tab3 = st.tabs([
    "📦 Vendas vs Exportações",
    "🚢 Fluxo Import/Export",
    "📈 Consumo Aparente"
])

# TAB 1 - Vendas Internas vs Exportações
with tab1:
    st.subheader("Volume de Vendas Internas e Exportações")
    melt1 = df_f.melt(
        id_vars="date",
        value_vars=["vendas_internas", "exportacoes_volume"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig1 = px.bar(
        melt1, x="date", y="Volume (mil t)",
        color="Indicador", barmode="group",
        color_discrete_map={
            "vendas_internas": "#e09e50", # Ouro Queimado
            "exportacoes_volume": "#b74803" # Ferrugem
        }
    )

    # Linha de porcentagem (Eixo secundário)
    total = df_f["exportacoes_volume"] + df_f["vendas_internas"]
    pct = (df_f["exportacoes_volume"] / total * 100).where(total != 0, 0)

    fig1.add_trace(go.Scatter(
        x=df_f["date"], y=pct, name="% Exportações",
        yaxis="y2", line=dict(dash="dash", color="#ffffff", width=2)
    ))

    fig1.update_layout(
        yaxis2=dict(overlaying="y", side="right", title="% Exportações", range=[0, 100], showgrid=False)
    )

    st.plotly_chart(apply_plotly_layout(fig1), use_container_width=True, config={'displayModeBar': False})

# TAB 2 - Exportações vs Importações
with tab2:
    st.subheader("Comparativo de Comércio Exterior")
    melt2 = df_f.melt(
        id_vars="date",
        value_vars=["exportacoes_volume", "importacoes_volume"],
        var_name="Indicador",
        value_name="Volume (mil t)"
    )

    fig2 = px.bar(
        melt2, x="date", y="Volume (mil t)",
        color="Indicador", barmode="group",
        color_discrete_sequence=["#b74803", "#7ca8cc"] # Ferrugem e Azul frio para contraste
    )

    st.plotly_chart(apply_plotly_layout(fig2), use_container_width=True, config={'displayModeBar': False})

# TAB 3 - Consumo Aparente
with tab3:
    st.subheader("Evolução do Consumo Aparente")
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

# ======================================================
# RODAPÉ
# ======================================================
st.markdown(
    """
    <div class="custom-footer">
        <p style="margin:0; font-size: 1rem; letter-spacing: 0.5px;">
            <strong>Elisângela de Souza</strong> | Dados atualizados até dez/2025
        </p>
    </div>
    """,
    unsafe_allow_html=True
)