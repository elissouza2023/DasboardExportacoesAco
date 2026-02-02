import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Siderurgia BR", layout="wide")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("dados_siderurgia_limpos_2013_2025.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Título e introdução
st.title("Dashboard Siderurgia Brasileira – Aço Brasil (2013–2025)")
st.markdown("Explore vendas internas, exportações, importações e consumo aparente. Fonte: Aço Brasil / MDIC.")

# Sidebar: Filtros
st.sidebar.header("Filtros")
anos_disponiveis = sorted(df['date'].dt.year.unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos",
    options=anos_disponiveis,
    default=[2023, 2024, 2025]  # default recentes
)

# Filtrar dados
if anos_selecionados:
    df_filtrado = df[df['date'].dt.year.isin(anos_selecionados)]
else:
    df_filtrado = df.copy()

# Tabs para gráficos
tab1, tab2, tab3 = st.tabs(["Vendas Internas vs Exportações", "Export vs Import", "Consumo vs Vendas Internas"])

with tab1:
    st.subheader("Vendas Internas vs Exportações")
    df_melt1 = df_filtrado.melt(id_vars='date', value_vars=['vendas_internas', 'exportacoes_volume'],
                                var_name='Tipo', value_name='Volume (mil t)')
    fig1 = px.bar(df_melt1, x='date', y='Volume (mil t)', color='Tipo', barmode='group')
    pct_export = (df_filtrado['exportacoes_volume'] / (df_filtrado['vendas_internas'] + df_filtrado['exportacoes_volume'])) * 100
    fig1.add_trace(go.Scatter(x=df_filtrado['date'], y=pct_export, name='% Exportações', yaxis='y2', line=dict(color='black', dash='dash')))
    fig1.update_layout(yaxis2=dict(title='% Exportações', overlaying='y', side='right'))
    st.plotly_chart(fig1, use_container_width=True)

# Adicione as outras tabs de forma similar (copie e adapte fig2 e fig3)

st.markdown("---")
st.caption("App desenvolvido com Streamlit | Dados até dez/2025")
