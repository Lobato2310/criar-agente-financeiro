# Base de Conhecimento do Agente

## Estratégia de Dados

### Visão Geral
A base de conhecimento do agente é composta por dados estruturados em CSV e JSON que representam o perfil financeiro completo de um cliente fictício. Esses dados alimentam o contexto do agente para gerar respostas personalizadas e precisas.

---

## 1. Arquivos de Dados

### 1.1 `transacoes.csv`

**Propósito**: Histórico completo de movimentações financeiras

**Estrutura**:
```csv
data,categoria,descricao,valor,tipo
2024-01-05,Alimentação,Supermercado Extra,-450.00,debito
```

**Campos**:
- `data`: Data da transação (YYYY-MM-DD)
- `categoria`: Categoria do gasto (Alimentação, Transporte, etc.)
- `descricao`: Descrição detalhada
- `valor`: Valor (negativo para débitos, positivo para créditos)
- `tipo`: Tipo de transação (debito/credito)

**Categorias Disponíveis**:
- 🍔 Alimentação
- 🚗 Transporte
- 🏥 Saúde
- 🎬 Lazer
- 🏠 Moradia
- 📚 Educação
- 🛍️ Compras

**Período**: Janeiro a Fevereiro de 2024 (2 meses)

**Como o Agente Usa**:
- Analisa padrões de gastos
- Identifica categorias com gastos elevados
- Calcula saldo disponível
- Sugere áreas para economia

---

### 1.2 `perfil_investidor.json`

**Propósito**: Perfil completo do cliente

**Estrutura**:
```json
{
  "cliente": { ... },
  "perfil_investidor": { ... },
  "situacao_financeira": { ... },
  "objetivos": [ ... ],
  "habitos_financeiros": { ... }
}
```

**Seções**:

#### A) Dados Pessoais (`cliente`)
- Nome, idade, profissão
- Renda mensal
- Estado civil e dependentes

#### B) Perfil de Investidor (`perfil_investidor`)
- Tipo: Conservador / Moderado / Arrojado
- Tolerância a risco
- Objetivo principal
- Prazo de investimento
- Conhecimento de mercado

#### C) Situação Financeira (`situacao_financeira`)
- Reserva de emergência
- Dívidas ativas
- Total em investimentos
- Distribuição da carteira

#### D) Objetivos (`objetivos`)
Lista de metas com:
- Descrição
- Valor alvo
- Prazo em meses

#### E) Hábitos Financeiros (`habitos_financeiros`)
- Controla gastos?
- Poupa mensalmente?
- Percentual de poupança
- Uso de crédito

**Como o Agente Usa**:
- Personaliza recomendações ao perfil de risco
- Considera objetivos ao sugerir investimentos
- Adapta linguagem à idade e conhecimento
- Valida sugestões com a situação financeira atual

---

### 1.3 `produtos_financeiros.json`

**Propósito**: Catálogo de produtos disponíveis para recomendação

**Estrutura de Cada Produto**:
```json
{
  "id": 1,
  "nome": "Tesouro Selic",
  "categoria": "Renda Fixa",
  "rentabilidade_anual": "13.65%",
  "liquidez": "Diária",
  "risco": "Muito Baixo",
  "investimento_minimo": 30.00,
  "perfil_recomendado": ["Conservador", "Moderado", "Arrojado"]
}
```

**Produtos Disponíveis**:
1. Tesouro Selic (Renda Fixa - Liquidez Diária)
2. CDB Liquidez Diária (Renda Fixa)
3. Fundo Multimercado (Fundos)
4. Ações IBOV (Renda Variável)
5. LCI/LCA (Renda Fixa)

**Como o Agente Usa**:
- Filtra produtos adequados ao perfil do cliente
- Recomenda baseado em liquidez necessária
- Explica riscos de cada produto
- Sugere diversificação adequada

---

### 1.4 `historico_atendimento.csv`

**Propósito**: Contexto de interações anteriores

**Estrutura**:
```csv
data,tipo_atendimento,assunto,resumo,status
2024-01-10,Chat,Dúvida sobre investimentos,...,Resolvido
```

**Campos**:
- `data`: Data do atendimento
- `tipo_atendimento`: Chat, Telefone, Email
- `assunto`: Tema principal
- `resumo`: Descrição da interação
- `status`: Resolvido / Em andamento

**Como o Agente Usa**:
- Evita repetir informações já fornecidas
- Retoma contexto de conversas anteriores
- Identifica dúvidas recorrentes

---

## 2. Processamento dos Dados

### 2.1 Fluxo de Carregamento
```python
# Carregamento em cache para performance
@st.cache_data
def load_data():
    transacoes = pd.read_csv('data/transacoes.csv')
    
    with open('data/perfil_investidor.json', 'r') as f:
        perfil = json.load(f)
    
    with open('data/produtos_financeiros.json', 'r') as f:
        produtos = json.load(f)
    
    historico = pd.read_csv('data/historico_atendimento.csv')
    
    return transacoes, perfil, produtos, historico
```

### 2.2 Criação de Contexto

O agente combina todos os dados em um contexto único:
```python
def criar_contexto_cliente(transacoes, perfil, produtos, historico):
    # Análises automáticas
    total_gastos = transacoes[transacoes['tipo'] == 'debito']['valor'].sum()
    gastos_categoria = transacoes.groupby('categoria')['valor'].sum()
    
    # Contexto formatado
    contexto = f"""
    PERFIL: {perfil['cliente']['nome']}
    RENDA: R$ {perfil['cliente']['renda_mensal']}
    GASTOS TOTAIS: R$ {abs(total_gastos)}
    ...
    """
    return contexto
```

---

## 3. Qualidade e Validação dos Dados

### 3.1 Dados Realistas
- ✅ Valores condizentes com salário de R$ 5.500
- ✅ Categorias de gastos típicas
- ✅ Distribuição equilibrada de despesas

### 3.2 Consistência
- ✅ Datas sequenciais e lógicas
- ✅ Perfil moderado alinhado com investimentos atuais
- ✅ Objetivos factíveis com a renda

### 3.3 Limitações
- ⚠️ Apenas 2 meses de histórico (ideal: 6-12 meses)
- ⚠️ Dados fictícios (não refletem sazonalidade real)
- ⚠️ Sem dados de investimentos em tempo real

---

## 4. Expansão da Base de Conhecimento

### Como Adicionar Mais Dados

#### Adicionar Transações:
```csv
# Adicione novas linhas em transacoes.csv
2024-03-05,Alimentação,Restaurante,-120.00,debito
```

#### Adicionar Novos Produtos:
```json
{
  "id": 6,
  "nome": "Previdência Privada",
  "categoria": "Previdência",
  "rentabilidade_anual": "Variável",
  "liquidez": "Sem liquidez",
  "risco": "Médio",
  "investimento_minimo": 200.00,
  "perfil_recomendado": ["Conservador", "Moderado"]
}
```

#### Modificar Perfil do Cliente:
- Edite diretamente `perfil_investidor.json`
- Altere renda, objetivos, tolerância a risco, etc.

---

## 5. Integração Futura (Roadmap)

### Open Banking
- Conexão com contas bancárias reais
- Atualização automática de transações
- Sincronização de investimentos

### APIs de Mercado
- Cotações em tempo real
- Rentabilidade atualizada de produtos
- Notícias financeiras relevantes

### Machine Learning
- Previsão de gastos futuros
- Detecção de anomalias
- Recomendações preditivas