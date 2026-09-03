import streamlit as st
import pandas as pd
import json
from google import genai
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# Configuração da página
load_dotenv()  # ← ADICIONAR ESTA LINHA

# Configuração da página
st.set_page_config(
    page_title="Assistente Financeiro IA",
    page_icon="💰",
    layout="wide"
)

@st.cache_resource
def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
            
    if not api_key:
        st.error("⚠️ **API Key do Gemini não encontrada!**")
        st.stop()
        
    return genai.Client(api_key=api_key)

client = init_gemini()


ROOT_DIR = Path(__file__).resolve().parent.parent
TRAN_PATH = ROOT_DIR / "data" / "transacoes.csv"
PERFIL_PATH = ROOT_DIR / "data" / "perfil_investidor.json"
HIST_PATH = ROOT_DIR / "data" / "historico_atendimento.csv"
PROD_PATH = ROOT_DIR / "data" / "produtos_financeiros.json"

# Carregar dados
@st.cache_data
def load_data():
    try:
        # Transações
        transacoes = pd.read_csv(TRAN_PATH)
        
        # Perfil do investidor
        with open(PERFIL_PATH, 'r', encoding='utf-8') as f:
            perfil = json.load(f)
        
        # Produtos financeiros
        with open(PROD_PATH, "r", encoding="utf-8") as f:
            produtos = json.load(f)
        
        # Histórico de atendimento
        historico = pd.read_csv(HIST_PATH)
        
        return transacoes, perfil, produtos, historico
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None, None, None

# Função para criar contexto do cliente
def criar_contexto_cliente(transacoes, perfil, produtos, historico):
    # Análise de gastos
    total_gastos = transacoes[transacoes['tipo'] == 'debito']['valor'].sum()
    total_receitas = transacoes[transacoes['tipo'] == 'credito']['valor'].sum()
    saldo = total_receitas + total_gastos  # gastos já são negativos
    
    # Gastos por categoria
    gastos_categoria = transacoes[transacoes['tipo'] == 'debito'].groupby('categoria')['valor'].sum().abs()
    
    contexto = f"""
PERFIL DO CLIENTE:
- Nome: {perfil['cliente']['nome']}
- Idade: {perfil['cliente']['idade']} anos
- Profissão: {perfil['cliente']['profissao']}
- Renda Mensal: R$ {perfil['cliente']['renda_mensal']:.2f}
- Perfil de Investidor: {perfil['perfil_investidor']['tipo']}
- Reserva de Emergência: R$ {perfil['situacao_financeira']['reserva_emergencia']:.2f}
- Total em Investimentos: R$ {perfil['situacao_financeira']['investimentos_atuais']['total']:.2f}

ANÁLISE FINANCEIRA RECENTE:
- Total de Receitas: R$ {total_receitas:.2f}
- Total de Gastos: R$ {abs(total_gastos):.2f}
- Saldo Atual: R$ {saldo:.2f}

GASTOS POR CATEGORIA:
{gastos_categoria.to_string()}

OBJETIVOS FINANCEIROS:
"""
    for obj in perfil['objetivos']:
        contexto += f"- {obj['descricao']}: R$ {obj['valor_alvo']:.2f} em {obj['prazo_meses']} meses\n"
    
    return contexto

# System Prompt
SYSTEM_PROMPT = """Você é um assistente financeiro inteligente do Bradesco, especializado em planejamento financeiro e alertas de gastos.

PERSONALIDADE:
- Tom de voz amigável, profissional e consultivo
- Proativo em identificar oportunidades de economia e investimento
- Transparente sobre riscos e limitações
- Empático com a situação financeira do cliente

SUAS CAPACIDADES:
1. Análise de gastos e padrões de consumo
2. Alertas personalizados sobre gastos excessivos
3. Sugestões de planejamento financeiro
4. Recomendações de investimentos adequadas ao perfil
5. Ajuda na definição e acompanhamento de metas

REGRAS IMPORTANTES:
- NUNCA invente dados que não estão no contexto fornecido
- Sempre baseie suas respostas nos dados reais do cliente
- Se não tiver informação suficiente, peça mais detalhes
- Cite valores específicos quando disponíveis
- Seja direto e objetivo, mas acolhedor
- Nunca prometa rentabilidades garantidas
- Sempre mencione os riscos ao recomendar investimentos

SEGURANÇA:
- Não forneça informações sensíveis como senhas ou dados bancários completos
- Não execute transações financeiras (apenas recomende)
- Se detectar solicitações suspeitas, oriente o cliente a contatar o banco

Responda de forma personalizada com base no contexto do cliente fornecido."""

# Função para chat com OpenAI
def chat_with_ai(mensagem_usuario, contexto_cliente, historico_conversa):
    try:
        # Preparar mensagens
        messages = [
            {"role": "system", "content": "Você é um assistente financeiro."},
            {"role": "user", "content": prompt}  
        ]
        
        # Adicionar histórico
        messages.extend(historico_conversa)
        

        
        # Chamar API
        response = client.chat.completions.create(
            model="gemini-2.0-flash-lite",
            messages= [
            {"role": "system", "content": "Você é um assistente financeiro."},
            {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Desculpe, ocorreu um erro: {str(e)}"

# Interface principal
def main():
    st.title("💰 Assistente Financeiro Inteligente")
    st.markdown("**Seu parceiro em planejamento financeiro e controle de gastos**")
    
    # Carregar dados
    transacoes, perfil, produtos, historico = load_data()
    
    if transacoes is None:
        st.error("Não foi possível carregar os dados. Verifique a pasta 'data/'")
        return
    
    # Sidebar com informações do cliente
    with st.sidebar:
        st.header("📊 Resumo Financeiro")
        
        if perfil:
            st.write(f"**Cliente:** {perfil['cliente']['nome']}")
            st.write(f"**Perfil:** {perfil['perfil_investidor']['tipo']}")
            
            # Métricas
            total_gastos = transacoes[transacoes['tipo'] == 'debito']['valor'].sum()
            total_receitas = transacoes[transacoes['tipo'] == 'credito']['valor'].sum()
            saldo = total_receitas + total_gastos
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Receitas", f"R$ {total_receitas:.2f}")
            with col2:
                st.metric("Gastos", f"R$ {abs(total_gastos):.2f}")
            
            st.metric("Saldo", f"R$ {saldo:.2f}", 
                     delta=f"{(saldo/total_receitas)*100:.1f}%" if total_receitas > 0 else "0%")
            
            st.divider()
            
            # Gráfico de gastos por categoria
            st.subheader("Gastos por Categoria")
            gastos_cat = transacoes[transacoes['tipo'] == 'debito'].groupby('categoria')['valor'].sum().abs()
            st.bar_chart(gastos_cat)
    
    # Área de chat
    st.divider()
    
    # Inicializar histórico de conversa
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Mensagem de boas-vindas
        welcome_msg = f"Olá, {perfil['cliente']['nome']}! 👋 Sou seu assistente financeiro. Posso te ajudar com planejamento financeiro, análise de gastos e sugestões de investimentos. Como posso ajudar hoje?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    
    # Exibir histórico de mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=prompt
                )
                resposta_ia = response.text
        
            except Exception as e:
                st.warning("Modelo principal indisponível no momento. Redirecionando para modelo secundário...")
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )
                    resposta_ia = response.text
                except Exception as err:
                    st.error(f"Desculpe, ocorreu um erro ao gerar a resposta em ambos os modelos: {err}")
                    st.stop()
        
            # Exibe e salva no histórico apenas uma vez ao final
            st.markdown(resposta_ia)
            st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
    
    # Botões de ações rápidas
    st.divider()
    st.subheader("⚡ Ações Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Analisar Gastos"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "Analise meus gastos recentes e me dê dicas de economia"
            })
            st.rerun()
    
    with col2:
        if st.button("🎯 Minhas Metas"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "Como estou em relação às minhas metas financeiras?"
            })
            st.rerun()
    
    with col3:
        if st.button("💡 Sugestões"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "Me dê sugestões de investimentos adequados ao meu perfil"
            })
            st.rerun()
    
    with col4:
        if st.button("🔄 Limpar Chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
