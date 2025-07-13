# ads-performance-checker
import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="IA Meta Ads", layout="centered")
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

uploaded_file = st.file_uploader("Envie o CSV com os dados da campanha", type=["csv"])

if uploaded_file:
    df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("latin1")))

    # Convertendo colunas com segurança
    for col in ['spend', 'cpc']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('[R$ ]', '', regex=True).str.replace(',', '.').astype(float)

    for col in ['ctr', 'roas']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    st.subheader("📋 Dados da campanha")
    st.dataframe(df)

    st.subheader("📈 Resultados da Análise")

    for _, row in df.iterrows():
        nome = row['campaign_name']
        ctr = row.get('ctr', 0)
        cpc = row.get('cpc', 0)
        roas = row.get('roas', 0)
        spend = row.get('spend', 0)
        new_followers = row.get('new_followers', 0)
        reactions = row.get('reactions', 0)
        comments = row.get('comments', 0)
        shares = row.get('shares', 0)

        # Eficácia geral (peso balanceado)
        eficacia = min(100, round((roas * 30 + ctr * 10 - cpc + (reactions + comments + shares) * 0.3), 2))
        eficacia = max(0, eficacia)

        # Chance de engajamento
        engajamento_score = (ctr * 0.5 + reactions * 0.2 + comments * 0.2 + shares * 0.1)
        engajamento_pct = min(100, round(engajamento_score, 2))

        st.markdown(f"### Campanha: `{nome}`")
        st.markdown(f"**Eficácia geral estimada:** `{eficacia}%`")
        st.markdown(f"**Probabilidade de gerar engajamento:** `{engajamento_pct}%`")

        melhorias = []
        if roas < 1:
            melhorias.append("Melhorar segmentação ou criativo para aumentar o ROAS")
        if ctr < 1:
            melhorias.append("Testar novos criativos para aumentar a CTR")
        if cpc > 10:
            melhorias.append("Reduzir o CPC ajustando o público ou objetivo da campanha")
        if reactions + comments + shares < 10:
            melhorias.append("Focar em conteúdo mais interativo ou emocional para estimular o engajamento")

        if melhorias:
            st.markdown("**🔧 Sugestões de melhoria:**")
            for item in melhorias:
                st.markdown(f"- {item}")
        else:
            st.markdown("✅ Campanha já bem otimizada.")

        st.markdown("---")

    st.success("Análise concluída com sucesso!")
else:
    st.info("Envie um arquivo CSV para iniciar a análise.")
