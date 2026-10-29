# Justificativa das métricas — Dashboard 2

Público-alvo: equipe que acompanha pacientes com diabetes (e o próprio paciente). As métricas usam as medições de glicemia do dataset e respondem aos filtros e às seleções dos gráficos. O delta compara o recorte com a amostra completa.

Faixas: hipoglicemia < 70 mg/dL, alvo 70–180 mg/dL, hiperglicemia > 180 mg/dL.

## Métrica 1: Glicemia mediana
- **Variável:** glicemia (mg/dL)
- **O que mede:** o valor típico da glicose no recorte.
- **Por que foi escolhida:** resume o controle em um número; a mediana é menos afetada pelos picos que a média.
- **Público-alvo:** equipe de acompanhamento e paciente.
- **Qual decisão pode ser apoiada por essa métrica?** Avaliar se o controle melhorou ou piorou.
- **O que comunica ao público-alvo:** onde a glicose costuma ficar.

## Métrica 2: Na faixa-alvo (%)
- **Variável:** glicemia (mg/dL)
- **O que mede:** a parte das medições entre 70 e 180 mg/dL.
- **Por que foi escolhida:** é fácil de entender e de comparar entre pacientes e períodos.
- **Público-alvo:** equipe de acompanhamento e paciente.
- **Qual decisão pode ser apoiada por essa métrica?** Definir metas e ver se uma mudança no tratamento funcionou.
- **O que comunica ao público-alvo:** quantas medições estão boas. Quanto maior, melhor.

## Métrica 3: Hiperglicemia (%)
- **Variável:** glicemia (mg/dL)
- **O que mede:** a parte das medições acima de 180 mg/dL.
- **Por que foi escolhida:** é o problema mais comum na amostra e o mesmo critério de classe usado no Dashboard 1.
- **Público-alvo:** equipe de acompanhamento.
- **Qual decisão pode ser apoiada por essa métrica?** Ajustar o tratamento nos momentos do dia com mais glicose alta.
- **O que comunica ao público-alvo:** com que frequência a glicose fica alta. Quanto menor, melhor.

## Métrica 4: Hipoglicemia (%)
- **Variável:** glicemia (mg/dL)
- **O que mede:** a parte das medições abaixo de 70 mg/dL.
- **Por que foi escolhida:** mostra o risco imediato do tratamento, que a mediana sozinha esconde.
- **Público-alvo:** equipe de acompanhamento e paciente.
- **Qual decisão pode ser apoiada por essa métrica?** Rever doses ou horários quando aumenta.
- **O que comunica ao público-alvo:** com que frequência a glicose fica baixa demais. Quanto menor, melhor.

## Métrica 5: Insulina por dia
- **Variável:** doses de insulina (U), somadas por dia
- **O que mede:** a média de insulina aplicada por dia.
- **Por que foi escolhida:** dá o contexto do tratamento para ler as métricas de glicemia.
- **Público-alvo:** equipe de acompanhamento.
- **Qual decisão pode ser apoiada por essa métrica?** Relacionar mudanças na glicemia com mudanças na dose.
- **O que comunica ao público-alvo:** quanto de insulina está sendo usado.
