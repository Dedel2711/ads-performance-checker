# ads-performance-checker
import streamlit as st

st.set_page_config(page_title="IA Meta Ads - Formulário", layout="centered")
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

st.title("📊 IA de Análise de Campanhas Meta Ads")

st.subheader("Preencha os dados da campanha")

with st.form(key='campaign_form'):
    campaign_name = st.text_input("Nome da campanha")
    spend = st.number_input("Gasto (spend)", min_value=0.0, format="%.2f")
    ctr = st.number_input("CTR (%)", min_value=0.0, max_value=100.0, format="%.2f")
    cpc = st.number_input("CPC", min_value=0.0, format="%.2f")
    roas = st.number_input("ROAS", min_value=0.0, format="%.2f")
    new_followers = st.number_input("Novos seguidores", min_value=0, step=1)
    reactions = st.number_input("Reações", min_value=0, step=1)
    comments = st.number_input("Comentários", min_value=0, step=1)
    shares = st.number_input("Compartilhamentos", min_value=0, step=1)

    submit_button = st.form_submit_button(label='Analisar campanha')

if submit_button:
    # Calcular eficácia (exemplo ponderado)
    eficacia = min(100, max(0, round(roas * 30 + ctr * 10 - cpc + (reactions + comments + shares) * 0.3, 2)))

    # Calcular engajamento
    engajamento_score = ctr * 0.5 + reactions * 0.2 + comments * 0.2 + shares * 0.1
    engajamento_pct = min(100, round(engajamento_score, 2))

    st.markdown(f"### Resultados para campanha: `{campaign_name}`")
    st.markdown(f"**Eficácia estimada:** `{eficacia}%`")
    st.markdown(f"**Probabilidade de engajamento:** `{engajamento_pct}%`")

    melhorias = []
    if roas < 1:
        melhorias.append("Melhorar segmentação ou criativo para aumentar o ROAS")
    if ctr < 1:
        melhorias.append("Testar novos criativos para aumentar a CTR")
    if cpc > 10:
        melhorias.append("Reduzir o CPC ajustando o público ou objetivo da campanha")
    if (reactions + comments + shares) < 10:
        melhorias.append("Focar em conteúdo mais interativo ou emocional para estimular o engajamento")

    if melhorias:
        st.markdown("**🔧 Sugestões de melhoria:**")
        for item in melhorias:
            st.markdown(f"- {item}")
    else:
        st.markdown("✅ Campanha já bem otimizada.")

