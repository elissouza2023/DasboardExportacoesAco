import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================
st.set_page_config(
    page_title="Dashboard Siderurgia BR",
    layout="wide"
)

# ======================================================
# CARREGAMENTO DOS DADOS
# ======================================================
@st.cache_data
def load_data():
    # Caminho absoluto baseado na localização do app.py
    BASE_DIR = Path(__file__).resolve().parent
   DATA_PATH = BASE_DIR / "data" / "processed" / "dados_siderurgia_limpos_2013_2025.csv"

    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ======================================================
# TÍTULO E DESCRIÇÃO
# ======================================================
st.title("Dashboard Mercado Siderúrgico Brasileiro")
st.markdown(
    "Explore **vendas internas, exportações, importações e consumo aparente**.  \n"
    "Fonte: Instituto Aço Brasil / MDIC."
)

# ======================================================
# SIDEBAR — FILTROS
# ======================================================
st.sidebar.header("Filtros")

anos_disponiveis = sorted(df["date"].dt.year.unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos",
    options=anos_disponiveis,
    default=anos_disponiveis[-3:]  # últimos 3 anos automaticamente
)

# Filtragem
if anos_selecionados:
    df_filtrado = df[df["date"].dt.year.isin(anos_selecionados)]
else:
    df_filtrado = df.copy()

# ======================================================
# TABS DE VISUALIZAÇÃO
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

# ======================================================
# RODAPÉ
# ======================================================
st.markdown("---")
st.caption("App desenvolvido com Streamlit | Dados atualizados até dez/2025 - ELisângela de Souza - 2026")
