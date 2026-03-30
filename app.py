import streamlit as st
import pandas as pd
import plotly.express as px
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
# CAMINHOS
# ======================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "dados_siderurgia_limpos_2013_2025.csv"
BACKGROUND_PATH = BASE_DIR / "assets" / "fundo.jpg"

# ======================================================
# BACKGROUND + CSS
# ======================================================
def set_background(image_path: Path):
    if not image_path.exists():
        return

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
                background: rgba(0, 0, 0, 0.60);
                z-index: -1;
            }}

            h1, h2, h3, p, label, div {{
                color: white;
            }}

            h1, h2, h3 {{
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            }}

            section[data-testid="stSidebar"] {{
                background: rgba(0,0,0,0.45);
                backdrop-filter: blur(10px);
            }}

            [data-testid="stMetric"] {{
                background: rgba(255,255,255,0.06);
                border-left: 5px solid #b74803;
                border-radius: 12px;
                padding: 12px;
                backdrop-filter: blur(8px);
            }}

            [data-testid="stMetricLabel"] {{
                color: #e09e50 !important;
                font-weight: bold;
                text-transform: uppercase;
            }}

            [data-testid="stMetricValue"] {{
                color: white !important;
                font-size: 1.8rem !important;
            }}

            .stTabs [data-baseweb="tab"] p {{
                color: white !important;
                font-weight: bold;
            }}

            span[data-baseweb="tag"] {{
                background-color: #e09e50 !important;
                color: white !important;
            }}

            .custom-footer {{
                background-color: rgba(0,0,0,0.75);
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

set_background(BACKGROUND_PATH)

# ======================================================
# FUNÇÃO PADRÃO DOS GRÁFICOS
# ======================================================
def apply_plotly_layout(fig):
    fig.update_layout(
        paper_bgcolor="rgba(30,30,30,0.7)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=13),
        margin=dict(l=50, r=50, t=50, b=50),
        legend=dict(
            bgcolor="rgba(0,0,0,0.5)",
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="white")
        )
    )
    return fig

# ======================================================
# CARREGAMENTO DOS DADOS
# ======================================================
@st.cache_data(ttl=300)
def load_data(file_mtime):
    """
    O parâmetro file_mtime faz o Streamlit invalidar o cache
    automaticamente sempre que o CSV for alterado, mesmo mantendo
    exatamente o mesmo nome de arquivo.
    """
    if not DATA_PATH.exists():
        st.error(f"Arquivo não encontrado: {DATA_PATH}")
        st.stop()

    df = pd.read_csv(DATA_PATH)

    # Garantir que a coluna de data está em datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remover linhas sem data válida
    df = df.dropna(subset=["date"])

    # Ordenar cronologicamente
    df = df.sort_values("date")

    return df

# Data de modificação do arquivo para invalidar cache automaticamente
file_mtime = DATA_PATH.stat().st_mtime

# Botão opcional para limpar cache manualmente
with st.sidebar:
    if st.button("🔄 Atualizar dados"):
        st.cache_data.clear()
        st.rerun()

df = load_data(file_mtime)

# ======================================================
# TÍTULO
# ======================================================
st.title("📊 Dashboard Mercado Siderúrgico Brasileiro")
st.markdown(
    "Explore vendas internas, exportações, importações e consumo aparente."
)

# Informação de atualização para debug
ultima_data = df["date"].max()

st.caption(
    f"Última data carregada no dashboard: {ultima_data.strftime('%m/%Y')}"
)

# ======================================================
# FILTROS
# ======================================================
st.sidebar.header("Filtros de Análise")

anos = sorted(df["date"].dt.year.unique())

default_anos = anos[-3:] if len(anos) >= 3 else anos

anos_sel = st.sidebar.multiselect(
    "Selecione os anos:",
    options=anos,
    default=default_anos
)

if anos_sel:
    df_f = df[df["date"].dt.year.isin(anos_sel)].copy()
else:
    df_f = df.copy()

# ======================================================
# KPIs
# ======================================================
if not df_f.empty:
    total_vendas = df_f["vendas_internas"].sum()
    total_export = df_f["exportacoes_volume"].sum()
    consumo_medio = df_f["consumo_aparente"].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Vendas Internas",
            f"{total_vendas:,.0f} mil t".replace(",", ".")
        )

    with col2:
        st.metric(
            "Total Exportações",
            f"{total_export:,.0f} mil t".replace(",", ".")
        )

    with col3:
        st.metric(
            "Média Consumo Aparente",
            f"{consumo_medio:,.0f} mil t".replace(",", ".")
        )

st.markdown("---")

# ======================================================
# ABAS
# ======================================================
tab1, tab2, tab3 = st.tabs([
    "📦 Vendas vs Exportações",
    "🚢 Fluxo Import/Export",
    "📈 Consumo Aparente"
])

# ======================================================
# TAB 1
# ======================================================
with tab1:
    st.subheader("Volume de Vendas Internas e Exportações")

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
        barmode="group",
        color_discrete_map={
            "vendas_internas": "#e09e50",
            "exportacoes_volume": "#b74803"
        }
    )

    fig1.update_xaxes(
        tickformat="%m/%Y"
    )

    st.plotly_chart(
        apply_plotly_layout(fig1),
        use_container_width=True
    )

# ======================================================
# TAB 2
# ======================================================
with tab2:
    st.subheader("Comparativo de Comércio Exterior")

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
        barmode="group",
        color_discrete_map={
            "exportacoes_volume": "#b74803",
            "importacoes_volume": "#7ca8cc"
        }
    )

    fig2.update_xaxes(
        tickformat="%m/%Y"
    )

    st.plotly_chart(
        apply_plotly_layout(fig2),
        use_container_width=True
    )

# ======================================================
# TAB 3
# ======================================================
with tab3:
    st.subheader("Evolução do Consumo Aparente")

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
        color="Indicador",
        markers=True,
        color_discrete_map={
            "consumo_aparente": "#FFFFFF",
            "vendas_internas": "#e09e50"
        }
    )

    fig3.update_xaxes(
        tickformat="%m/%Y"
    )

    st.plotly_chart(
        apply_plotly_layout(fig3),
        use_container_width=True
    )

# ======================================================
# RODAPÉ
# ======================================================
st.markdown(
    f"""
    <div class="custom-footer">
        <p style="margin:0; font-size:1rem;">
            <strong>Elisângela de Souza</strong> |
            Dados atualizados até {ultima_data.strftime('%b/%Y')} |
            Fonte oficial: Instituto Aço Brasil
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
