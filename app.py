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
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(uploaded_file, encoding='latin1')
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            st.stop()

    # Limpeza e padronização segura
    for col in ['spend', 'cpc']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('[^0-9,\.]', '', regex=True).str.replace(',', '.').astype(float)

    for col in ['ctr', 'roas']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    int_cols = ['new_followers', 'reactions', 'comments', 'shares']
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    st.subheader("📋 Dados da campanha")
    st.dataframe(df)

    st.subheader("📈 Resultados da Análise")

    for _, row in df.iterrows():
        nome = row.get('campaign_name', 'Campanha Sem Nome')
        ctr = row.get('ctr', 0)
        cpc = row.get('cpc', 0)
        roas = row.get('roas', 0)
        spend = row.get('spend', 0)
        new_followers = row.get('new_followers', 0)
        reactions = row.get('reactions', 0)
        comments = row.get('comments', 0)
        shares = row.get('shares', 0)

        # Métricas combinadas
        engajamento_total = reactions + comments + shares
        eficacia = min(100, round((roas * 35 + ctr * 12 - cpc * 5 + engajamento_total * 0.4), 2))
        eficacia = max(0, eficacia)
        engajamento_pct = min(100, round((ctr * 0.5 + reactions * 0.25 + comments * 0.15 + shares * 0.1), 2))

        st.markdown(f"### 📌 Campanha: `{nome}`")
        st.markdown(f"**🎯 Eficácia geral estimada:** `{eficacia}%`")
        st.markdown(f"**📢 Probabilidade de engajamento:** `{engajamento_pct}%`")

        st.markdown("---")
        st.markdown("**📋 Análise detalhada:**")
        if roas >= 1 and ctr >= 1.5 and cpc <= 8:
            st.markdown("✅ Campanha com bom desempenho geral. Continue otimizando públicos e criativos para manter a performance.")
        else:
            if roas < 1:
                st.markdown("- 🔻 ROAS abaixo do ideal: otimize segmentação e use criativos mais voltados à conversão.")
            if ctr < 1.5:
                st.markdown("- 🔻 CTR abaixo da média: teste variações de criativos e chamadas mais diretas.")
            if cpc > 8:
                st.markdown("- 🔻 CPC elevado: refine os públicos e evite horários muito concorridos.")

        if engajamento_total < 10:
            st.markdown("- 📉 Baixo engajamento: use conteúdo interativo, vídeos curtos e enquetes para incentivar reações.")
        else:
            st.markdown("- 👍 Bom engajamento, ideal para remarketing e construção de comunidade.")

        if new_followers < 5:
            st.markdown("- 👥 Poucos novos seguidores: inclua CTAs no criativo incentivando seguir a página.")
        else:
            st.markdown("- 📈 Crescimento saudável de seguidores gerado pela campanha.")

        st.markdown("---")

    st.success("✅ Análise finalizada com sucesso!")
else:
    st.info("Envie um arquivo CSV com colunas como: campaign_name, spend, ctr, cpc, roas, new_followers, reactions, comments, shares.")
