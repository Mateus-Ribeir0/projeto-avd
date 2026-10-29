# Justificativa das métricas — Dashboard 2

Base: medições de glicemia do Diabetes Dataset (UCI), 70 pacientes, de 1988 a 1991. Todas as métricas respondem aos widgets do topo (paciente, período e momento da medição) e às seleções feitas nos gráficos (arrastar um período na linha do tempo ou clicar num momento do dia nas barras). O *delta* de cada métrica é a diferença para a amostra completa, sem nenhum filtro, o que serve de referência para comparar um paciente ou um período com o grupo todo.

Faixas usadas (valores de referência clínicos comuns para glicemia capilar): hipoglicemia abaixo de 70 mg/dL, faixa-alvo de 70 a 180 mg/dL, hiperglicemia acima de 180 mg/dL. O limite de 180 mg/dL é o mesmo usado para definir a classe "Hiperglicemia" no EDA e no Dashboard 1.

## Métrica 1: Glicemia mediana
- **Variável:** `valor` das medições de glicemia (códigos 48 e 57–64), em mg/dL
- **O que mede:** o valor central das glicemias medidas no recorte escolhido (metade das medições fica abaixo, metade acima).
- **Por que foi escolhida:** medida de tendência central. A mediana foi escolhida no lugar da média porque a distribuição da glicemia é assimétrica, com cauda longa à direita (picos acima de 400 mg/dL), e esses picos puxariam a média para cima.
- **Público-alvo:** equipe de acompanhamento (médico, enfermagem) e o próprio paciente.
- **Qual decisão pode ser apoiada por essa métrica?** Se o controle do paciente está melhorando ou piorando num período, e se vale rever o tratamento.
- **O que comunica ao público-alvo:** "no período, a glicemia típica deste paciente ficou em X mg/dL", sem precisar ler um histograma.

## Métrica 2: Na faixa-alvo (% de medições entre 70 e 180 mg/dL)
- **Variável:** `valor` das medições de glicemia
- **O que mede:** a proporção das medições que ficaram dentro da faixa considerada adequada.
- **Por que foi escolhida:** é uma proporção simples, fácil de entender e de comparar entre pacientes e períodos. É a versão por medição do indicador "tempo na faixa", usado no acompanhamento de diabetes.
- **Público-alvo:** equipe de acompanhamento e paciente.
- **Qual decisão pode ser apoiada por essa métrica?** Definir metas ("chegar a 70% das medições na faixa") e verificar se uma mudança de dose ou rotina surtiu efeito.
- **O que comunica ao público-alvo:** "X de cada 10 medições estão boas". Quanto maior, melhor.

## Métrica 3: Hiperglicemia (% de medições acima de 180 mg/dL)
- **Variável:** `valor` das medições de glicemia
- **O que mede:** a proporção das medições com glicose alta.
- **Por que foi escolhida:** é o lado do descontrole mais frequente nesta amostra (cerca de 36% das medições) e o mesmo critério da classe usada no restante do projeto. Combinada com o clique nas barras, mostra em que momento do dia o problema se concentra.
- **Público-alvo:** equipe de acompanhamento.
- **Qual decisão pode ser apoiada por essa métrica?** Ajustar a insulina ou a alimentação no momento do dia em que a hiperglicemia é mais comum.
- **O que comunica ao público-alvo:** "X% das vezes a glicose estava alta". Quanto menor, melhor (o delta fica vermelho quando sobe).

## Métrica 4: Hipoglicemia (% de medições abaixo de 70 mg/dL)
- **Variável:** `valor` das medições de glicemia
- **O que mede:** a proporção das medições com glicose baixa.
- **Por que foi escolhida:** a hipoglicemia é o risco imediato do tratamento com insulina. Olhar só a glicemia mediana esconderia esse lado: um paciente pode ter mediana boa e muitas hipoglicemias.
- **Público-alvo:** equipe de acompanhamento e paciente.
- **Qual decisão pode ser apoiada por essa métrica?** Reduzir dose ou rever horários quando a proporção de hipoglicemias aumenta.
- **O que comunica ao público-alvo:** "X% das vezes a glicose estava baixa demais". Quanto menor, melhor.

## Métrica 5: Insulina por dia (U/dia, média)
- **Variável:** `valor` das doses de insulina (códigos 33, 34 e 35: regular, NPH e ultralenta), somadas por paciente-dia
- **O que mede:** quanto de insulina foi aplicado, em média, por dia com registro de dose.
- **Por que foi escolhida:** dá o contexto do tratamento para as métricas de glicemia. A mesma glicemia mediana significa coisas diferentes com 20 ou com 60 unidades por dia.
- **Público-alvo:** equipe de acompanhamento.
- **Qual decisão pode ser apoiada por essa métrica?** Ver se uma piora (ou melhora) da glicemia veio junto de mudança na dose.
- **O que comunica ao público-alvo:** "em média, o paciente aplicou X unidades de insulina por dia no período".
