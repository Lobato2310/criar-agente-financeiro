# 💰 Agente Financeiro Inteligente com IA Generativa

> Assistente virtual proativo para planejamento financeiro e controle de gastos, desenvolvido com **Google Gemini** / **LLMs** e **Streamlit**.

---

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como parte do desafio final do curso **GenAI e Dados** da parceria **Bradesco + DIO**.

O agente financeiro utiliza IA Generativa para:
- ✅ **Antecipar necessidades financeiras** ao invés de apenas responder perguntas.
- ✅ **Personalizar sugestões** baseadas no perfil real e no histórico do cliente (`data/perfil_investidor.json`).
- ✅ **Cocriar soluções financeiras** de forma consultiva e dinâmica.
- ✅ **Garantir segurança e confiabilidade** nas respostas com grounding em dados locais (anti-alucinação).

---

## 🚀 Funcionalidades

### 1. Análise de Gastos
- Categorização automática de despesas a partir de bases locais (`transacoes.csv`).
- Identificação de padrões de consumo e alertas proativos de gastos excessivos.
- Comparativo visual e numérico de despesas por categoria.

### 2. Planejamento Financeiro
- Simulação de metas de curto, médio e longo prazo (veículos, viagens, reserva de emergência).
- Análise da capacidade real de poupança com base no histórico financeiro.

### 3. Recomendações de Investimento
- Sugestões adequadas ao perfil de risco (Conservador, Moderado, Arrojado).
- Explicabilidade clara de riscos, liquidez, retornos esperados e diversificação.

### 4. Interface e Experiência Intuitiva
- Chat interativo com gestão dinâmica de contexto e histórico da conversa.
- Mapeamento dinâmico de diretórios para execução robusta local e em nuvem.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** (com `pathlib` para manipulação segura de caminhos)
- **Streamlit** - Interface web e gerenciamento de estado
- **Google Gemini API / Groq** - Provedor de LLM de alto desempenho
- **Pandas** - Análise e manipulação de dados
- **JSON & CSV** - Estruturação de dados locais e base de conhecimento

---

## 📦 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone [https://github.com/Lobato2310/criar-agente-financeiro.git](https://github.com/Lobato2310/criar-agente-financeiro.git)
cd lab-agente-financeiro

2. Crie e ative um ambiente virtual
# Linux / macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

3. Instale as dependências
pip install -r requirements.txt

4. Configure a API Key
Crie o arquivo .env na raiz do projeto ou configure em .streamlit/secrets.toml:
Opção A: Arquivo .env (Raiz do projeto)
GEMINI_API_KEY="sua-chave-do-google-ai-studio"
Opção B: Arquivo .streamlit/secrets.toml
GEMINI_API_KEY = "sua-chave-do-google-ai-studio"

▶️ Como Executar
Execute o comando na raiz do repositório:
streamlit run src/app.py

O aplicativo abrirá automaticamente no navegador em http://localhost:8501.

📁 Estrutura do Projeto
lab-agente-financeiro/
│
├── data/                            # Base de dados locais (Grounding)
│   ├── transacoes.csv               # Histórico de transações
│   ├── perfil_investidor.json       # Perfil do cliente
│   ├── produtos_financeiros.json    # Catálogo de produtos
│   └── historico_atendimento.csv    # Histórico de atendimentos
│
├── docs/                            # Documentação do projeto
│   ├── 01-documentacao-agente.md    # Caso de uso e arquitetura
│   ├── 02-base-conhecimento.md      # Estratégia de dados
│   ├── 03-prompts.md                # Engenharia de prompts
│   ├── 04-metricas.md               # Avaliação e métricas
│   └── 05-pitch.md                  # Roteiro do pitch
│
├── src/                             # Código-fonte principal
│   └── app.py                       # Aplicação Streamlit
│
├── .streamlit/                      # Configurações do Streamlit
│   └── secrets.toml                 # API Keys
│
├── .env                             # Variáveis de ambiente locais
├── requirements.txt                 # Dependências Python
└── README.md                        # Documentação do repositório

🔒 Segurança e Anti-Alucinação
O agente foi construído com diretrizes de segurança avançadas:

✅ Grounding em Dados Reais: Respostas estritamente fundamentadas nos arquivos da pasta data/.

✅ System Prompts Restritivos: Regras explícitas contra invenção de saldos ou dados inexistentes.

✅ Tratamento de Exceções & Fallback: Estrutura preparada para lidar com instabilidades de API.

✅ Resolução Dinâmica de Diretórios: Mapeamento relativo via Pathlib evitando erros de execução.


👤 Autor
Lucas Lobato

🙏 Agradecimentos
Bradesco e DIO pelo programa de aceleração em GenAI e Dados.
Google AI Studio pelo fornecimento de infraestrutura de LLMs.
Streamlit pela estrutura de desenvolvimento web.


## 🛡️ Estratégia de Validação e Confiabilidade

Para evitar alucinações comuns em LLMs aplicadas ao mercado financeiro, a aplicação utiliza:

1. **Deterministic Data Processing**: O agente não tenta "calcular" saldos via texto; os dados são extraídos e processados via `pandas` antes de alimentar o contexto da IA.
2. **Context Bounding (Grounding)**: A IA é explicitamente instruída a responder "Não possuo essa informação" caso a dúvida exija dados fora dos arquivos CSV/JSON fornecidos.
3. **Prompt Guardrails**: Regras de sistema impedem a recomendação de produtos incompatíveis com o perfil de risco mapeado no JSON do cliente.
