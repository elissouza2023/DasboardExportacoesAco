# 📊 Dashboard de Exportações de Aço – Brasil

Este projeto tem como objetivo analisar e visualizar dados de **exportações de aço do Brasil**, utilizando dados oficiais disponibilizados pelo **Instituto Aço Brasil**.

O dashboard foi desenvolvido em **Python**, com foco em **análise de dados aplicada ao setor siderúrgico**, e disponibilizado via **Streamlit**, permitindo uma visualização interativa e acessível das informações.

---

## 🎯 Objetivo do Projeto

Demonstrar habilidades como **Analista de Dados**, aplicadas a um contexto real do **setor siderúrgico**, unindo:

- Dados reais e atualizados
- Tratamento e organização de dados
- Análise comparativa ao longo do tempo
- Visualização clara para apoio à tomada de decisão

O projeto também foi pensado para **evolução futura**, incluindo automação de atualização dos dados.

---

## 🏭 Contexto dos Dados

- **Fonte:** Instituto Aço Brasil  
- **Período:** 2013 até janeiro de 2025  
- **Tipo de dados:** Exportações de aço por tipo de produto  
  - Produtos planos  
  - Produtos longos  
  - Semiacabados  
  - Outros segmentos do setor

Os dados originais são disponibilizados em formato de planilha e foram convertidos para **CSV**, visando melhor desempenho e versionamento.

---

## 🧱 Estrutura do Projeto

```

📦 dashboard-exportacoes-aco
│
📁 data
├── 📁 raw
│   └── Performance-Mensal_2025.12.xls
├── 📁 interim
│   └── exportacoes_aco_tratado_largo.csv
└── 📁 processed
    └── exportacoes_aco_mensal_long.csv
│
├── 📁 src
│   ├── 📁 utils
│   │   └── data_processing.py
│   │
│   ├── 📁 assets
│   │   └── logo.png
│   │
│   └── 📁 visuals
│       └── charts.py
│
├── 📁 notebooks
│   └── exploracao_dados.ipynb
│
├── 📄 app.py
├── 📄 requirements.txt
├── 📄 README.md
├── 📄 .gitignore
└── 📄 LICENSE
```
---

## 📊 Funcionalidades do Dashboard

- Visualização da evolução das exportações ao longo dos anos
- Comparação entre tipos de produtos siderúrgicos
- Filtros por período
- Gráficos interativos para análise exploratória
- Estrutura preparada para atualizações futuras dos dados

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Pandas** – tratamento e análise dos dados
- **NumPy**
- **Plotly / Matplotlib** – visualização de dados
- **Streamlit** – construção do dashboard interativo
- **Git & GitHub** – versionamento

---

## ▶️ Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/DasboardExportacoesAco.git

2. Instale as dependências:

  pip install -r requirements.txt

3. Execute o dashboard:

  streamlit run app.py


---

## 🔄 Próximos Passos (Evolução do Projeto)

- Automatizar a atualização dos dados mensais

- Integração com n8n para:

- Coleta automática da planilha no site oficial

- Atualização do dataset no repositório

- Inclusão de novos KPIs do setor siderúrgico

- Publicação do dashboard em ambiente cloud



---

## 👩‍💻 Sobre a Autora

Projeto desenvolvido por Elisângela de Souza, com foco em Análise de Dados aplicada ao setor industrial, unindo interesses em:

- Setor siderúrgico

- Engenharia e indústria

- Segurança da informação

- Inteligência Artificial

- Visualização e storytelling com dados

---

## 📌 Observação

Este projeto tem caráter educacional e demonstrativo, utilizando dados públicos do site Aço Brasil e sem fins comerciais.

---

## ▶️ Deploy

Em Elaboração
