# ads-performance-checker
import streamlit as st

st.set_page_config(page_title="IA Meta Ads - Análise Detalhada", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .stApp {
        background-color: #0d1117;
    }
    .css-1v0mbdj, .css-1d391kg {
        color: #58a6ff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 IA de Análise Detalhada de Campanhas Meta Ads")

st.subheader("Preencha os dados da campanha")

with st.form(key='campaign_form'):
    campaign_name = st.text_input("Nome da campanha")
    spend = st.number_input("Gasto (spend) em R$", min_value=0.0, format="%.2f")
    ctr = st.number_input("CTR (%)", min_value=0.0, max_value=100.0, format="%.2f")
    cpc = st.number_input("CPC em R$", min_value=0.0, format="%.2f")
    roas = st.number_input("ROAS", min_value=0.0, format="%.2f")
    new_followers = st.number_input("Novos seguidores", min_value=0, step=1)
    reactions = st.number_input("Reações", min_value=0, step=1)
    comments = st.number_input("Comentários", min_value=0, step=1)
    shares = st.number_input("Compartilhamentos", min_value=0, step=1)

    submit_button = st.form_submit_button(label='Analisar campanha')

def analisar_campanha(nome, spend, ctr, cpc, roas, new_followers, reactions, comments, shares):
    # Benchmarks aproximados Meta Ads (exemplo)
    ctr_ideal = 1.5  # %
    cpc_ideal = 8.0  # R$
    roas_ideal = 1.0

    eficacia = min(100, max(0, round(roas * 30 + ctr * 10 - cpc + (reactions + comments + shares) * 0.3, 2)))
    engajamento_score = ctr * 0.5 + reactions * 0.2 + comments * 0.2 + shares * 0.1
    engajamento_pct = min(100, round(engajamento_score, 2))

    st.markdown(f"### Análise detalhada para campanha: **{nome}**\n")

    # Análise eficácia
    if roas >= roas_ideal and ctr >= ctr_ideal and cpc <= cpc_ideal:
        st.markdown(f"**✅ A campanha apresenta um desempenho sólido.**\n")
        st.markdown(f"- ROAS de {roas} indica que você está gerando retorno positivo sobre o investimento.\n"
                    f"- CTR de {ctr}% está acima da média recomendada ({ctr_ideal}%), sinalizando boa atração.\n"
                    f"- CPC de R${cpc} está dentro do custo esperado para o seu setor.\n")
    else:
        st.markdown(f"**⚠️ A campanha apresenta pontos a melhorar:**\n")
        if roas < roas_ideal:
            st.markdown(f"- ROAS ({roas}) abaixo do ideal ({roas_ideal}), o que significa que o retorno financeiro pode ser insuficiente.")
        if ctr < ctr_ideal:
            st.markdown(f"- CTR ({ctr}%) está abaixo da média recomendada ({ctr_ideal}%), sugerindo que o anúncio não está atraindo o público adequadamente.")
        if cpc > cpc_ideal:
            st.markdown(f"- CPC (R${cpc}) está alto, indicando que o custo para atrair cliques pode estar afetando a rentabilidade.\n")

    # Análise engajamento
    st.markdown(f"**📊 Engajamento e interação:**\n")
    st.markdown(f"- Reações: {reactions}\n- Comentários: {comments}\n- Compartilhamentos: {shares}\n- Novos seguidores: {new_followers}\n")

    if (reactions + comments + shares) < 10:
        st.markdown("⚠️ O engajamento geral está baixo, o que pode impactar negativamente o alcance orgânico e a percepção da marca.")
    else:
        st.markdown("✅ O engajamento está dentro do esperado, o que contribui para a ampliação do alcance e fortalecimento da marca.")

    # Sugestões personalizadas
    st.markdown("**🔧 Sugestões para maximizar a eficácia da campanha:**")

    if roas < roas_ideal:
        st.markdown("- Melhore a segmentação para atingir um público mais qualificado, aumentando o potencial de conversão.")
        st.markdown("- Avalie o criativo da campanha, apostando em provas sociais e ofertas claras.")
    if ctr < ctr_ideal:
        st.markdown("- Teste diferentes criativos, focando em chamadas mais diretas e visuais impactantes.")
        st.markdown("- Ajuste o posicionamento do anúncio para os canais onde seu público está mais ativo.")
    if cpc > cpc_ideal:
        st.markdown("- Analise o público-alvo para reduzir concorrência e custos.")
        st.markdown("- Otimize o orçamento para distribuir melhor os gastos ao longo do tempo.")
    if (reactions + comments + shares) < 10:
        st.markdown("- Invista em conteúdo mais interativo, como enquetes, vídeos curtos e chamadas para ação que incentivem o público a reagir.")
        st.markdown("- Use CTAs claros para incentivar compartilhamentos e comentários, aumentando o alcance orgânico.")

    st.markdown("---")
    st.markdown(f"**Eficácia estimada da campanha:** {eficacia}%  \n**Probabilidade de engajamento:** {engajamento_pct}%")

if submit_button:
    analisar_campanha(
        campaign_name, spend, ctr, cpc, roas,
        new_followers, reactions, comments, shares
    )
