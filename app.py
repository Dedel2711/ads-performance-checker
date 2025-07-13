# ads-performance-checker
def gerar_analise(campaign):
    roas_ideal = 1.0
    ctr_ideal = 1.5  # %
    cpc_ideal = 8.0  # R$

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

    # Sempre adicionar as recomendações, independente dos outros indicadores
    analise.append("\n### 🔧 Recomendações para maximizar resultados\n")

    # Sempre sugerir pelo menos uma recomendação para cada possível problema
    if roas < roas_ideal:
        analise.append("- Reavalie a segmentação para alcançar públicos mais qualificados.")
        analise.append("- Invista em criativos com provas sociais e ofertas claras.")
    else:
        analise.append("- Continue otimizando para manter ou melhorar o ROAS.")

    if ctr < ctr_ideal:
        analise.append("- Teste variações nos anúncios com chamadas diretas e visuais impactantes.")
        analise.append("- Ajuste posicionamentos para atingir canais com maior atividade do público.")
    else:
        analise.append("- Mantenha o foco em anúncios que gerem alto interesse do público.")

    if cpc > cpc_ideal:
        analise.append("- Otimize o orçamento para reduzir custos em horários ou públicos saturados.")
        analise.append("- Explore públicos menos concorridos para baixar o custo por clique.")
    else:
        analise.append("- Continue controlando o custo por clique para manter rentabilidade.")

    if engajamento_total < 10:
        analise.append("- Utilize conteúdos interativos (enquetes, vídeos curtos) para estimular ações do público.")
        analise.append("- Incentive compartilhamentos e comentários com CTAs claros e diretos.")
    else:
        analise.append("- Continue produzindo conteúdo que estimule interação e engajamento.")

    analise.append("\n---\n")
    analise.append(f"**Eficácia estimada:** {eficacia}%  \n**Probabilidade de engajamento:** {engajamento_pct}%")

    return "\n".join(analise)
