import json
import os
from pathlib import Path
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = ROOT_DIR / "docs"

st.set_page_config(
    page_title="Assistente Financeiro IA", layout="wide"
)


@st.cache_resource
def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key do Gemini não encontrada!")
        st.stop()
    return genai.Client(api_key=api_key)


client = init_gemini()


def ler_arquivo_texto(caminho: Path) -> str:
    if caminho.exists():
        return caminho.read_text(encoding="utf-8")
    return ""


def load_data():
    """Carrega os dados dos arquivos locais"""
    transacoes_path = DATA_DIR / "transacoes.csv"
    perfil_path = DATA_DIR / "perfil_investidor.json"
    produtos_path = DATA_DIR / "produtos_financeiros.json"
    historico_path = DATA_DIR / "historico_atendimento.csv"

    transacoes = (
        pd.read_csv(transacoes_path) if transacoes_path.exists() else None
    )

    perfil = None
    if perfil_path.exists():
        with open(perfil_path, "r", encoding="utf-8") as f:
            perfil = json.load(f)

    produtos = None
    if produtos_path.exists():
        with open(produtos_path, "r", encoding="utf-8") as f:
            produtos = json.load(f)

    historico = (
        pd.read_csv(historico_path) if historico_path.exists() else None
    )

    return transacoes, perfil, produtos, historico


def carregar_dados_cliente() -> str:
    contexto = []

    perfil_path = DATA_DIR / "perfil_investidor.json"
    if perfil_path.exists():
        with open(perfil_path, "r", encoding="utf-8") as f:
            perfil = json.load(f)
            contexto.append(
                f"**Perfil do Cliente:**\n{json.dumps(perfil, ensure_ascii=False, indent=2)}"
            )

    transacoes_path = DATA_DIR / "transacoes.csv"
    if transacoes_path.exists():
        df_transacoes = pd.read_csv(transacoes_path)
        resumo_gastos = (
            df_transacoes.groupby("categoria")["valor"].sum().to_dict()
        )
        total_gasto = df_transacoes["valor"].sum()
        contexto.append(
            f"**Resumo Financeiro:** Total Gasto: R$ {total_gasto:.2f}\n"
            f"**Gastos por Categoria:** {json.dumps(resumo_gastos, ensure_ascii=False)}"
        )

    produtos_path = DATA_DIR / "produtos_financeiros.json"
    if produtos_path.exists():
        with open(produtos_path, "r", encoding="utf-8") as f:
            produtos = json.load(f)
            contexto.append(
                f"**Produtos Financeiros Disponíveis:**\n{json.dumps(produtos, ensure_ascii=False, indent=2)}"
            )

    return "\n\n".join(contexto)


def construir_system_instruction() -> str:
    prompt_base = ler_arquivo_texto(DOCS_DIR / "03-prompts.md")
    base_conhecimento = ler_arquivo_texto(DOCS_DIR / "02-base-conhecimento.md")
    dados_cliente = carregar_dados_cliente()

    return f"""
{prompt_base}

=== BASE DE CONHECIMENTO ===
{base_conhecimento}

=== DADOS EM TEMPO REAL DO CLIENTE (GROUNDING) ===
{dados_cliente}
"""


def main():
    st.title("💰 Assistente Financeiro Inteligente")
    st.markdown(
        "**Seu parceiro em planejamento financeiro e controle de gastos**"
    )

    transacoes, perfil, produtos, historico = load_data()

    if transacoes is None:
        st.error("Não foi possível carregar os dados. Verifique a pasta 'data/'")
        return

    # Tratamento seguro das chaves do perfil do cliente
    nome_cliente = (
        perfil.get("cliente", {}).get("nome")
        if isinstance(perfil.get("cliente"), dict)
        else perfil.get("nome", "Cliente")
    )
    tipo_perfil = (
        perfil.get("perfil_investidor", {}).get("tipo")
        if isinstance(perfil.get("perfil_investidor"), dict)
        else perfil.get("perfil_risco", "Não informado")
    )

    # Sidebar
    with st.sidebar:
        st.header("Resumo Financeiro")
        if perfil:
            st.write(f"**Cliente:** {nome_cliente}")
            st.write(f"**Perfil:** {tipo_perfil}")

            total_gastos = transacoes[transacoes["tipo"] == "debito"][
                "valor"
            ].sum()
            total_receitas = transacoes[transacoes["tipo"] == "credito"][
                "valor"
            ].sum()
            saldo = total_receitas + total_gastos

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Receitas", f"R$ {total_receitas:.2f}")
            with col2:
                st.metric("Gastos", f"R$ {abs(total_gastos):.2f}")

            delta_perc = (
                f"{(saldo / total_receitas) * 100:.1f}%"
                if total_receitas > 0
                else "0%"
            )
            st.metric("Saldo", f"R$ {saldo:.2f}", delta=delta_perc)

            st.divider()
            st.subheader("Gastos por Categoria")
            gastos_cat = (
                transacoes[transacoes["tipo"] == "debito"]
                .groupby("categoria")["valor"]
                .sum()
                .abs()
            )
            st.bar_chart(gastos_cat)

    st.divider()

    # Inicializar histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []
        welcome_msg = f"Olá, {nome_cliente}! Sou seu assistente financeiro. Posso te ajudar com planejamento financeiro, análise de gastos e sugestões de investimentos. Como posso ajudar hoje?"
        st.session_state.messages.append(
            {"role": "assistant", "content": welcome_msg}
        )

    # Exibir mensagens
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Digite sua mensagem..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            try:
                system_instruction_completa = construir_system_instruction()

                # Formata histórico de conversas para a API Gemini
                formatted_contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    formatted_contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=msg["content"])],
                        )
                    )

                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction_completa,
                        temperature=0.2,
                    ),
                )
                resposta_ia = response.text

            except Exception as e:
                try:
                    # Fallback secundário em caso de oscilação do modelo principal
                    response = client.models.generate_content(
                        model="gemini-3.1-flash-lite",
                        contents=formatted_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction_completa,
                            temperature=0.2,
                        ),
                    )
                    resposta_ia = response.text

            except Exception as e:
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=formatted_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction_completa,
                            temperature=0.2,
                        ),
                    )
                    resposta_ia = response.text
                    
            except Exception as err:
                st.error(f"Desculpe, ocorreu um erro ao gerar a resposta: {err}")
                st.stop()

            st.markdown(resposta_ia)
            st.session_state.messages.append(
                {"role": "assistant", "content": resposta_ia}
            )
            st.rerun()

    # Ações rápidas
    st.divider()
    st.subheader("⚡ Ações Rápidas")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Analisar Gastos"):
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Analise meus gastos recentes e me dê dicas de economia",
                }
            )
            st.rerun()

    with col2:
        if st.button("Minhas Metas"):
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Como estou em relação às minhas metas financeiras?",
                }
            )
            st.rerun()

    with col3:
        if st.button("Sugestões"):
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Me dê sugestões de investimentos adequados ao meu perfil",
                }
            )
            st.rerun()

    with col4:
        if st.button("Limpar Chat"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()
