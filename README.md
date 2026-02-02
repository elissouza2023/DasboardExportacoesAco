## 📊 Dashboard Mercado Siderurgico Brasileiro

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Em%20desenvolvimento-orange)](https://github.com/elissouza2023/DasboardExportacoesAco)

---


### 🎯 Objetivo
Demonstrar competências em **Análise de Dados** e **Visualização** aplicadas a um setor industrial estratégico, utilizando dados reais, tratamento robusto e interface amigável para suporte à tomada de decisão.

### 🏭 Contexto dos Dados
- **Fonte oficial**: [Instituto Aço Brasil](https://www.acobrasil.org.br/site/estatistica-mensal)  
- **Período coberto**: Janeiro/2013 a Dezembro/2025 (atualizado mensalmente)  
- **Granularidade**: Mensal (mil toneladas)  
- **Principais indicadores**:
  - Produção de aço bruto
  - Vendas internas (domestic sales)
  - Exportações (volume)
  - Consumo aparente
  - Importações (calculadas: consumo aparente - vendas internas)
  - Saldo comercial (exportações - importações)

Os dados são originalmente em formato XLS e processados para CSV limpo e otimizado.
---

### 🧱 Estrutura do Projeto

```

📦 dashboard-exportacoes-aco
│
📁 data
├── 📁 raw # Planilhas originais baixadas
│   └── Performance-Mensal_2025*.*.xls
├── 📁 interim   
│   
└── 📁 processed  
│    └── exportacoes_aco_mensal_long.csv
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

### 📊 Funcionalidades Principais
- Gráficos interativos com Plotly (barras agrupadas + linhas secundárias)
- Filtros na lateral:
  - Seleção de múltiplos anos
  - Intervalo de datas
- Comparações chave:
  - Vendas internas vs Exportações (% de exportação)
  - Exportações vs Importações (saldo comercial)
  - Consumo aparente vs Vendas internas (pressão de importados)
- Preparado para evolução: automação mensal via n8n + GitHub Actions - Em elaboração

---

### 🛠️ Tecnologias Utilizadas
- **Linguagem**: Python 3.10+
- **Manipulação de dados**: Pandas, NumPy
- **Visualização**: Plotly (interativo)
- **Dashboard**: Streamlit
- **Versionamento**: Git + GitHub
- **Hospedagem futura**: Streamlit Cloud

---

### ▶️ Como Executar Localmente

1. Clone o repositório:
   ```bash
    git clone https://github.com/seu-usuario/DasboardExportacoesAco.git

2.  Crie e ative um ambiente virtual
 ```bash
    python -m venv venv
    source venv/bin/activate      # Linux / macOS
    venv\Scripts\activate         # Windows
 ```

3.  Instale as dependências
 ```bash
    pip install -r requirements.txt
 ```
3. Execute o dashboard:
 ```bash
    streamlit run app.py
 ```

---

## 🔄 Próximos Passos (Evolução do Projeto)

- Automatizar a atualização dos dados mensais

- Integração com n8n para:

- Coleta automática da planilha no site oficial

- Atualização do dataset no repositório

- Inclusão de novos KPIs do setor siderúrgico

---

## 👩‍💻 Sobre a Autora

Projeto desenvolvido por Elisângela de Souza, com foco em Análise de Dados aplicada ao setor industrial, unindo interesses em:


- Análise de dados industriais
- Setor siderúrgico e commodities
- Visualização e storytelling com dados
- Automação de processos (n8n, GitHub Actions)
- Inteligência Artificial aplicada
- Engenharia e indústria
- Segurança da informação

  
---

## 📌 Observação

Este projeto tem caráter educacional e demonstrativo, utilizando dados públicos do site Aço Brasil e sem fins comerciais.

---

## ▶️ Deploy

https://mercadosiderurgicobr.streamlit.app
