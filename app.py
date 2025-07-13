# ads-performance-checker
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="IA Meta Ads — Análise Avançada",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="auto",
)

# CSS customizado para tema escuro com azul
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #2381f7;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1864d6;
        color: #e0e0e0;
    }
    .stTextInput>div>input {
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 0.4rem 0.6rem;
    }
    .stNumberInput>div>input {
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 0.4rem 0.6rem;
    }
    .css-1d391kg {
        color: #58a6ff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📊 IA Meta Ads — Análise Avançada de Campanhas")
st.markdown(
    """
    Bem-vindo! Preencha os dados abaixo para obter uma análise detalhada, insights baseados em benchmarks reais da Meta Ads e sugestões personalizadas para maximizar resultados.
"""
)

def calcula_eficacia(roas, ctr, cpc, engajamento_total):
    """
    Calcula uma pontuação de eficácia ponderada com base nos principais KPIs.
    """
    score = roas * 35 + ctr * 12 - cpc * 5 + engajamento_total * 0.4
    return round(max(0, min(100, score)), 2)

def calcula_engajamento(ctr, reactions, comments, shares):
    """
    Estima a probabilidade de engajamento baseado em interações e CTR.
    """
    score = ctr * 0.5 + reactions * 0.25 + comments * 0.15 + shares * 0.1
    return round(min(100, score), 2)

def gerar_analise(campaign):
    roas_ideal = 1.0
    ctr_ideal = 1.5  # %
    cpc_ideal = 8.0  # R$

    # KPIs da campanha
    roas = campaign['roas']
    ctr = campaign['ctr']
    cpc = campaign['cpc']
    reactions = campaign['reactions']
    comments = campaign['comments']
    shares = campaign['shares']
    new_followers = campaign['new_followers']

    engajamento_total = reactions + comments + shares
    eficacia = calcula_eficacia(roas, ctr, cpc, engajamento_total)
    engajamento_pct = calcula_engajamento(ctr, reactions, comments, shares)

    # Análise textual detalhada
    analise = []

    analise.append(f"### 🔍 Análise detalhada da campanha: **{campaign['campaign_name']}**\n")

    if roas >= roas_ideal and ctr >= ctr_ideal and cpc <= cpc_ideal:
        analise.append(
            f"✅ A campanha apresenta um desempenho sólido:\n"
            f"- ROAS de {roas:.2f} indica retorno financeiro positivo.\n"
            f"- CTR de {ctr:.2f}% está acima do benchmark recomendado ({ctr_ideal}%).\n"
            f"- CPC de R${cpc:.2f} está controlado dentro do custo esperado."
        )
    else:
        analise.append("⚠️ A campanha possui áreas para melhoria:\n")
        if roas < roas_ideal:
            analise.append(f"- ROAS baixo ({roas:.2f} < {roas_ideal}): indica retorno insuficiente para investimento.")
        if ctr < ctr_ideal:
            analise.append(f"- CTR baixo ({ctr:.2f}% < {ctr_ideal}%): sinal de baixo interesse do público.")
        if cpc > cpc_ideal:
            analise.append(f"- CPC alto (R${cpc:.2f} > R${cpc_ideal}): custo elevado por clique reduz lucratividade.")

    analise.append(f"\n### 📊 Engajamento e Interação\n")
    analise.append(f"- Reações: {reactions}\n- Comentários: {comments}\n- Compartilhamentos: {shares}\n- Novos seguidores: {new_followers}")

    if engajamento_total < 10:
        analise.append("\n⚠️ Engajamento geral baixo, limitando o alcance orgânico e o impacto da marca.")
    else:
        analise.append("\n✅ Engajamento satisfatório, favorecendo alcance e fortalecimento da marca.")

    analise.append("\n### 🔧 Recomendações para maximizar resultados\n")

    if roas < roas_ideal:
        analise.append("- Reavalie a segmentação para alcançar públicos mais qualificados.")
        analise.append("- Invista em criativos com provas sociais e ofertas claras.")
    if ctr < ctr_ideal:
        analise.append("- Teste variações nos anúncios com chamadas diretas e visuais impactantes.")
        analise.append("- Ajuste posicionamentos para atingir canais com maior atividade do público.")
    if cpc > cpc_ideal:
        analise.append("- Otimize o orçamento para reduzir custos em horários ou públicos saturados.")
        analise.append("- Explore públicos menos concorridos para baixar o custo por clique.")
    if engajamento_total < 10:
        analise.append("- Utilize conteúdos interativos (enquetes, vídeos curtos) para estimular ações do público.")
        analise.append("- Incentive compartilhamentos e comentários com CTAs claros e diretos.")

    analise.append("\n---\n")
    analise.append(f"**Eficácia estimada:** {eficacia}%  \n**Probabilidade de engajamento:** {engajamento_pct}%")

    return "\n".join(analise)

def validar_inputs(campaign):
    erros = []
    if not campaign['campaign_name']:
        erros.append("O nome da campanha é obrigatório.")
    for campo in ['spend', 'ctr', 'cpc', 'roas']:
        if campaign[campo] is None or campaign[campo] < 0:
            erros.append(f"O valor de {campo.upper()} deve ser um número positivo.")
    return erros

with st.form(key='form_campanha'):
    campaign_name = st.text_input("Nome da campanha")
    spend = st.number_input("Gasto (spend) em R$", min_value=0.0, format="%.2f")
    ctr = st.number_input("CTR (%)", min_value=0.0, max_value=100.0, format="%.2f")
    cpc = st.number_input("CPC em R$", min_value=0.0, format="%.2f")
    roas = st.number_input("ROAS", min_value=0.0, format="%.2f")
    new_followers = st.number_input("Novos seguidores", min_value=0, step=1)
    reactions = st.number_input("Reações", min_value=0, step=1)
    comments = st.number_input("Comentários", min_value=0, step=1)
    shares = st.number_input("Compartilhamentos", min_value=0, step=1)

    enviar = st.form_submit_button("Analisar campanha")

if enviar:
    dados_campanha = {
        'campaign_name': campaign_name.strip(),
        'spend': spend,
        'ctr': ctr,
        'cpc': cpc,
        'roas': roas,
        'new_followers': new_followers,
        'reactions': reactions,
        'comments': comments,
        'shares': shares,
    }

    erros = validar_inputs(dados_campanha)
    if erros:
        for e in erros:
            st.error(e)
    else:
        resultado = gerar_analise(dados_campanha)
        st.markdown(resultado)
