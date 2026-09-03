# 💰 Agente Financeiro Inteligente com IA Generativa

> Assistente virtual proativo para planejamento financeiro e controle de gastos, desenvolvido com OpenAI GPT-4 e Streamlit.

---
> ⚠️ **Nota sobre as chamadas de IA:**
> A funcionalidade de interação com a LLM está temporariamente pausada devido à expiração dos créditos da API da OpenAI. As demais rotas e funcionalidades do projeto seguem operacionais. O projeto será atualizado em breve para integrar uma solução de LLM com camada gratuita (ex: Groq / Google Gemini).

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como parte do desafio final do curso **GenAI e Dados** da parceria **Bradesco + DIO**.

O agente financeiro utiliza IA Generativa para:
- ✅ Antecipar necessidades financeiras ao invés de apenas responder perguntas
- ✅ Personalizar sugestões baseadas no perfil e contexto do cliente
- ✅ Cocriar soluções financeiras de forma consultiva
- ✅ Garantir segurança e confiabilidade nas respostas (anti-alucinação)

---

## 🚀 Funcionalidades

### 1. Análise de Gastos
- Categorização automática de despesas
- Identificação de padrões de consumo
- Alertas proativos sobre gastos excessivos
- Comparação mês a mês

### 2. Planejamento Financeiro
- Simulação de metas (carro, viagem, casa, etc.)
- Análise de capacidade de poupança
- Sugestões personalizadas de economia

### 3. Recomendações de Investimento
- Baseadas no perfil de risco do cliente
- Adequadas aos objetivos e prazos
- Explicação clara de riscos e retornos
- Diversificação inteligente

### 4. Interface Intuitiva
- Chat interativo em tempo real
- Visualização de métricas financeiras
- Gráficos de gastos por categoria
- Ações rápidas predefinidas

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** - Interface web
- **OpenAI GPT-4o-mini** - Motor de IA
- **Pandas** - Análise de dados
- **JSON/CSV** - Base de conhecimento

---

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/agente-financeiro-ia.git
cd agente-financeiro-ia
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure a API Key da OpenAI

**Opção 1: Usando Streamlit Secrets (Recomendado)**
Crie o arquivo `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sua-api-key-aqui"
```

**Opção 2: Usando Variável de Ambiente**
```bash
export OPENAI_API_KEY="sua-api-key-aqui"  # Linux/Mac
set OPENAI_API_KEY=sua-api-key-aqui       # Windows
```

---

## ▶️ Como Executar
```bash
streamlit run src/app.py
```

O aplicativo abrirá automaticamente em `http://localhost:8501`

---

## 📁 Estrutura do Projeto
```
lab-agente-financeiro/
│
├── data/                          # Dados mockados
│   ├── transacoes.csv            # Histórico de transações
│   ├── perfil_investidor.json    # Perfil do cliente
│   ├── produtos_financeiros.json # Catálogo de produtos
│   └── historico_atendimento.csv # Histórico de atendimentos
│
├── docs/                         # Documentação completa
│   ├── 01-documentacao-agente.md # Caso de uso e arquitetura
│   ├── 02-base-conhecimento.md   # Estratégia de dados
│   ├── 03-prompts.md             # Engenharia de prompts
│   ├── 04-metricas.md            # Avaliação e métricas
│   └── 05-pitch.md               # Roteiro do pitch
│
├── src/                          # Código-fonte
│   └── app.py                    # Aplicação Streamlit
│
├── .streamlit/                   # Configurações do Streamlit
│   └── secrets.toml              # API Keys (não versionar!)
│
├── requirements.txt              # Dependências Python
└── README.md                     # Este arquivo
```

---

## 🎮 Como Usar

### 1. Converse Naturalmente
```
"Como estão meus gastos este mês?"
"Quero comprar um carro de R$ 60.000 em 3 anos. É possível?"
"Onde devo investir R$ 5.000?"
```

### 2. Use Ações Rápidas
Clique nos botões:
- 📊 **Analisar Gastos**
- 🎯 **Minhas Metas**
- 💡 **Sugestões**
- 🔄 **Limpar Chat**

### 3. Explore os Dados
- Veja o resumo financeiro na barra lateral
- Analise o gráfico de gastos por categoria
- Acompanhe métricas em tempo real

---

## 🔒 Segurança e Anti-Alucinação

O agente implementa múltiplas camadas de segurança:

✅ **Grounding em Dados Reais**: Todas as respostas são baseadas em dados fornecidos  
✅ **Prompts Restritivos**: Instruções claras contra invenção de dados  
✅ **Validação de Contexto**: Verifica disponibilidade de informações  
✅ **Transparência**: Sempre menciona riscos e limitações  
✅ **Não Executa Transações**: Apenas recomenda ações  

Veja mais em [docs/01-documentacao-agente.md](docs/01-documentacao-agente.md)

---

## 📊 Métricas de Qualidade

| Métrica | Meta | Status |
|---------|------|--------|
| Precisão | ≥ 95% | ✅ 96% |
| Taxa Segura (Anti-Alucinação) | 100% | ✅ 100% |
| Coerência com Perfil | ≥ 90% | ✅ 92% |
| Utilidade Percebida | ≥ 80% | ✅ 85% |
| Tempo de Resposta | < 5s | ✅ 3.2s |

Veja detalhes em [docs/04-metricas.md](docs/04-metricas.md)

---

## 🎯 Casos de Uso

### Cenário 1: Controle de Gastos
```
Usuário: "Gastei muito este mês?"
Agente: "Seus gastos totais foram R$ 3.250. 
         Destaque: Alimentação aumentou 30% (R$ 790). 
         Sugestão: Economize R$ 200 com delivery..."
```

### Cenário 2: Planejamento de Meta
```
Usuário: "Quero viajar para Europa em 18 meses, preciso de R$ 15.000"
Agente: "Simulação: Investindo R$ 750/mês em CDB...
         Total em 18 meses: R$ 15.200 ✅
         Plano: ..."
```

### Cenário 3: Recomendação de Investimento
```
Usuário: "Tenho R$ 10.000 para investir"
Agente: "Para seu perfil Moderado, sugiro:
         60% CDB (R$ 6.000) - Risco Baixo
         40% Fundo Multimercado (R$ 4.000) - Risco Médio
         ⚠️ Riscos: ..."
```

---

## 🛣️ Roadmap

### ✅ Fase 1 - MVP (Concluído)
- [x] Chat funcional com GPT-4
- [x] Análise de gastos
- [x] Recomendações de investimento
- [x] Anti-alucinação implementada

### 🔄 Fase 2 - Melhorias (Próximo)
- [ ] Integração com Open Banking
- [ ] Notificações por email/SMS
- [ ] Histórico de conversas persistente
- [ ] Suporte a múltiplos clientes

### 🚀 Fase 3 - Avançado (Futuro)
- [ ] Multi-agentes especializados
- [ ] Análise preditiva com ML
- [ ] Gamificação de metas
- [ ] App mobile

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👤 Autor

**Lucas Lobato**
<p align="left">
  <a href="mailto:lucaslobsouza@gmail.com">
    <img src="https://img.shields.io/badge/Email-333333?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
  <a href="https://www.linkedin.com/in/lucas-lobato-tech" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://www.instagram.com/loobato_" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-222222?style=for-the-badge&logo=instagram&logoColor=white" />
  </a>
</p>
---

## 🙏 Agradecimentos

- **Bradesco** e **DIO** pela oportunidade do curso
- **Comunidade OpenAI** pelas ferramentas incríveis
- **Streamlit** pela framework intuitiva

---

