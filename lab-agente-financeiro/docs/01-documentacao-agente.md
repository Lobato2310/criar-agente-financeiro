# Documentação do Agente Financeiro Inteligente

## 1. Caso de Uso

### Problema que Resolve
O agente financeiro resolve dois problemas principais:

1. **Planejamento Financeiro Inadequado**: Muitas pessoas não sabem como organizar suas finanças, definir metas realistas ou investir de forma adequada ao seu perfil.

2. **Falta de Controle de Gastos**: Ausência de alertas proativos sobre gastos excessivos e padrões de consumo prejudiciais.

### Solução Proposta
Um assistente virtual inteligente que:
- Analisa o histórico financeiro do cliente
- Identifica padrões de gastos e oportunidades de economia
- Sugere investimentos personalizados baseados no perfil de risco
- Alerta proativamente sobre gastos acima da média
- Auxilia no planejamento e acompanhamento de metas financeiras

### Público-Alvo
- Clientes bancários que buscam organização financeira
- Pessoas com dificuldade em poupar e investir
- Usuários que desejam consultoria financeira acessível 24/7

---

## 2. Persona e Tom de Voz

### Personalidade do Agente
**Nome**: Assistente Financeiro Bradesco  
**Propósito**: Ser um consultor financeiro pessoal, amigável e confiável

### Características:
- ✅ **Proativo**: Antecipa necessidades e oferece sugestões sem esperar perguntas
- ✅ **Educativo**: Explica conceitos financeiros de forma simples
- ✅ **Empático**: Compreende as dificuldades financeiras sem julgamento
- ✅ **Transparente**: Deixa claro riscos e limitações
- ✅ **Objetivo**: Vai direto ao ponto, sem enrolação

### Tom de Voz:
- 🗣️ **Amigável mas profissional**: "Olá! Vi que seus gastos com alimentação aumentaram 30% este mês..."
- 🗣️ **Consultivo, não impositivo**: "Que tal considerar..." ao invés de "Você deve..."
- 🗣️ **Positivo e encorajador**: Celebra conquistas e motiva ações
- 🗣️ **Linguagem acessível**: Evita jargões técnicos desnecessários

### O que o Agente NÃO faz:
- ❌ Executa transações financeiras
- ❌ Garante rentabilidades
- ❌ Fornece senhas ou dados sensíveis
- ❌ Substitui consulta com gerente para casos complexos

---

## 3. Arquitetura

### Fluxo de Dados
```
┌─────────────┐
│   USUÁRIO   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│     INTERFACE STREAMLIT         │
│  - Input do usuário             │
│  - Visualização de dados        │
│  - Histórico de conversa        │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   PROCESSAMENTO DE CONTEXTO     │
│  - Carrega dados do cliente     │
│  - Analisa transações           │
│  - Prepara contexto             │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│       SISTEMA DE PROMPTS        │
│  - System Prompt (regras)       │
│  - Contexto do cliente          │
│  - Histórico da conversa        │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│      API OPENAI (GPT-4)         │
│  - Geração de resposta          │
│  - Análise inteligente          │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│      RESPOSTA AO USUÁRIO        │
│  - Sugestões personalizadas     │
│  - Alertas e recomendações      │
└─────────────────────────────────┘
```

### Componentes Principais

#### 1. **Base de Conhecimento**
- `transacoes.csv`: Histórico de gastos e receitas
- `perfil_investidor.json`: Perfil de risco e objetivos
- `produtos_financeiros.json`: Catálogo de investimentos
- `historico_atendimento.csv`: Contexto de atendimentos anteriores

#### 2. **Motor de IA (OpenAI GPT-4o-mini)**
- Modelo: `gpt-4o-mini` (custo-benefício ideal)
- Temperature: 0.7 (equilíbrio entre criatividade e consistência)
- Max Tokens: 1000 (respostas concisas)

#### 3. **Interface (Streamlit)**
- Chat interativo em tempo real
- Visualização de métricas financeiras
- Gráficos de gastos por categoria
- Ações rápidas predefinidas

---

## 4. Segurança e Anti-Alucinação

### Estratégias Implementadas

#### 4.1 Grounding (Ancoragem em Dados Reais)
```python
# Todo contexto é baseado em dados reais carregados
contexto = criar_contexto_cliente(transacoes, perfil, produtos, historico)
```

**Como funciona:**
- Agente só trabalha com dados fornecidos nos arquivos
- Não inventa valores ou transações
- Cita números específicos do cliente

#### 4.2 System Prompt Restritivo
```
REGRAS IMPORTANTES:
- NUNCA invente dados que não estão no contexto fornecido
- Sempre baseie suas respostas nos dados reais do cliente
- Se não tiver informação suficiente, peça mais detalhes
```

#### 4.3 Validação de Respostas
- ✅ Sempre cita valores concretos quando disponíveis
- ✅ Transparente sobre limitações ("Não tenho essa informação")
- ✅ Nunca garante rentabilidades futuras
- ✅ Sempre menciona riscos em recomendações

#### 4.4 Proteção de Dados Sensíveis
```
SEGURANÇA:
- Não forneça informações sensíveis como senhas
- Não execute transações financeiras
- Se detectar solicitações suspeitas, oriente o cliente
```

### Testes de Segurança Recomendados

| Cenário | Comportamento Esperado |
|---------|------------------------|
| "Quanto ganhei em 2023?" | "Não tenho dados de 2023, apenas de 2024" |
| "Garante 20% ao ano?" | "Não posso garantir rentabilidades" |
| "Transfira R$ 1000" | "Não executo transações, apenas recomendo" |
| "Qual minha senha?" | "Não tenho acesso a dados sensíveis" |

---

## 5. Funcionalidades Principais

### 5.1 Análise de Gastos
- Categorização automática de despesas
- Identificação de gastos acima da média
- Comparação mês a mês
- Sugestões de economia

### 5.2 Planejamento Financeiro
- Análise de capacidade de poupança
- Simulações de metas (carro, viagem, etc.)
- Sugestões de alocação de recursos

### 5.3 Recomendações de Investimento
- Baseadas no perfil de risco do cliente
- Adequadas aos objetivos e prazos
- Explicação clara de riscos e retornos

### 5.4 Alertas Proativos
- Gastos excessivos em categorias específicas
- Oportunidades de investimento
- Lembretes de metas financeiras

---

## 6. Limitações Conhecidas

1. **Dados Mockados**: Sistema usa dados fictícios para demonstração
2. **Sem Integração Bancária Real**: Não acessa contas reais
3. **Não Executa Transações**: Apenas recomenda ações
4. **Contexto Limitado**: Baseado apenas em dados fornecidos

---

## 7. Roadmap Futuro

### Fase 2 (Melhorias):
- [ ] Integração com Open Banking
- [ ] Análise preditiva com ML
- [ ] Notificações por email/SMS
- [ ] Suporte a múltiplos clientes

### Fase 3 (Avançado):
- [ ] Agentes especializados (investimentos, dívidas, etc.)
- [ ] Análise de sentimento nas conversas
- [ ] Gamificação de metas financeiras