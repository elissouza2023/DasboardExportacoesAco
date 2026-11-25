## 📊 Dashboard Mercado Siderurgico Brasileiro

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.67.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-3.1.1-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-2.5.5-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.11.2-11557C)](https://matplotlib.org/)
[![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)

[![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-E95420?logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![Oracle Cloud](https://img.shields.io/badge/Oracle-Cloud%20Infrastructure-F80000?logo=oracle&logoColor=white)](https://www.oracle.com/cloud/)
[![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?logo=nginx&logoColor=white)](https://nginx.org/)
[![HTTPS](https://img.shields.io/badge/HTTPS-TLS%20Enabled-success?logo=letsencrypt&logoColor=white)](https://letsencrypt.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Version%20Control-181717?logo=github&logoColor=white)](https://github.com/)

[![Streamlit Community Cloud](https://img.shields.io/badge/Deploy-Streamlit%20Community%20Cloud-FF4B4B?logo=streamlit&logoColor=white)](https://mercadosiderurgicobr.streamlit.app/)
[![Oracle Cloud Deployment](https://img.shields.io/badge/Deploy-Oracle%20Cloud-F80000?logo=oracle&logoColor=white)](https://mercadosiderurgicobr.duckdns.org/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Publicado-success)](https://github.com/elissouza2023/DasboardExportacoesAco)

---


### 🎯 Objetivo
Demonstrar competências em **Análise de Dados** e **Visualização** aplicadas a um setor industrial estratégico, utilizando dados reais, tratamento robusto e interface amigável para suporte à tomada de decisão.

---

### 🏭 Contexto dos Dados
- **Fonte oficial**: [Instituto Aço Brasil](https://www.acobrasil.org.br/site/estatistica-mensal)  
- **Período coberto**: Janeiro/2013 a Outubro/2026 (atualizado mensalmente)  
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
- **Linguagem**: Python 3.12
- **Manipulação de dados**: Pandas, NumPy
- **Visualização**: Plotly (interativo)
- **Dashboard**: Streamlit
- **Versionamento**: Git + GitHub
- **Hospedagem **: Streamlit Cloud & Oracle Cloud (OCI)
- **Servidor web / Proxy reverso**: Nginx.
- **Gerenciamento de processos**: systemd
- **DNS**: DuckDNS
- **Certificado digital**: Let's Encrypt / Certbot
---
### ☁️ Arquitetura Cloud 

O projeto foi disponibilizado em duas plataformas de hospedagem em nuvem, demonstrando diferentes alternativas de publicação e execução de aplicações Python:

- **Streamlit Community Cloud:** hospedagem simplificada e integrada ao GitHub, utilizando a infraestrutura gerenciada da própria plataforma.

- **Oracle Cloud Infrastructure (OCI):** implantação em máquina virtual Linux, com administração do servidor Ubuntu, configuração de rede, Nginx como proxy reverso, gerenciamento de processos com systemd e comunicação segura via HTTPS.
---
### 🔐 Segurança da Infraestrutura

A implantação utiliza camadas de proteção na infraestrutura de rede e no servidor Linux.

- **1. Segurança de rede — OCI**

  - VCN dedicada ao projeto.

  - Subnet pública para disponibilização da aplicação.

  - Internet Gateway para conectividade externa.

  - Security List com regras específicas de entrada.

  - Acesso SSH (porta 22) restrito ao endereço IP público autorizado, utilizando máscara /32.

  - Portas HTTP (80) e HTTPS (443) liberadas para acesso público.

- **2. Segurança no Ubuntu**

  - Regras de firewall com iptables.

  - Portas 22, 80 e 443 autorizadas conforme a necessidade do serviço.

  - Rejeição de conexões de entrada não contempladas pelas regras.

  - Porta 8501 não exposta diretamente à internet.

  - Aplicação Streamlit executada em 127.0.0.1, acessível externamente somente por meio do Nginx.

- **3. Comunicação criptografada**

  - Certificado SSL/TLS emitido gratuitamente pela Let's Encrypt.

  - Instalação e configuração automatizadas pelo Certbot.

  - Nginx configurado para utilizar o certificado digital.

  - Renovação automática do certificado programada pelo Certbot.

- **4. Gerenciamento da aplicação**

  - Serviço systemd para execução do Streamlit em segundo plano.

  - Inicialização automática habilitada com a inicialização do sistema.

  - Política de reinicialização automática do processo em caso de falha.

  - Aplicação executada em ambiente virtual Python (.venv).

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
## ⚙️Gerenciamento da aplicação na OCI

Na infraestrutura Oracle Cloud, a aplicação é executada em uma máquina virtual Ubuntu e gerenciada pelo systemd, recurso do Linux que permite controlar serviços e configurar sua inicialização automática.

Essa configuração permite manter o dashboard em execução independentemente de uma sessão de terminal, além de facilitar sua administração e manutenção.

---

## 🔄 Próximos Passos (Evolução do Projeto)

- Automatizar a atualização dos dados mensais

- Integração com n8n para:

- Coleta automática da planilha no site oficial

- Atualização do dataset no repositório

- Inclusão de novos KPIs do setor siderúrgico
  
- Implementar persistência das regras de firewall do Ubuntu.

- Avaliar o uso do OCI Bastion para administração segura da VM.

- Realizar testes de recuperação após reinicialização da instância.

- Aprimorar monitoramento, logs e hardening do servidor.
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
- Infraestrutura e computação em nuvem (OCI)
  
---

## 📌 Observação

Este projeto tem caráter educacional e demonstrativo, utilizando dados públicos disponibilizados pelo Instituto Aço Brasil e sem fins comerciais.

A infraestrutura foi implantada com foco em utilização de recursos gratuitos da Oracle Cloud, respeitando os limites e condições do programa aplicável.

O projeto demonstra a integração entre análise de dados, desenvolvimento Python, administração Linux, infraestrutura em nuvem, publicação de aplicações e práticas de segurança.

---

## ▶️ Deploy

https://mercadosiderurgicobr.streamlit.app
https://mercadosiderurgicobr.duckdns.org
