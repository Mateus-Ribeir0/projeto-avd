# Declaração de Uso de IA

Atividade Streamlit AVD – 2026.2 – Dashboards com Streamlit (Aulas 21 a 23). A versão assinada fica em `prompts/DECLARACAO_IA.pdf`.

## 1. Identificação

| | |
|---|---|
| **Turma** | 5A |
| **Nome completo** | Mateus de Almeida Ribeiro |
| **E-mail** | mar2@cesar.school |
| **Repositório** | https://github.com/Mateus-Ribeir0/projeto-avd |
| **Data de entrega** | 03/11/2026 |

## 2. Declaração geral

Utilizei IA generativa e registrei todos os usos na Seção 4. A maior parte se enquadra nas situações permitidas. Os Usos nº 3, 8, 9, 10 e 11 têm partes que não se enquadram, e isso está indicado em cada bloco.

Usei a Skill oficial do Streamlit (`streamlit skills`) a partir de 29/10/2026.

## 3. Ferramentas utilizadas

| Ferramenta | Versão / plano | Em que parte da atividade |
|---|---|---|
| Claude Code (extensão do VS Code) | Claude Pro – Opus 5.5 | notebooks/eda-com-downloads.ipynb |
| Claude Code (extensão do VS Code) | Claude Pro – Opus 5.5 | app.py e src/data_loader.py |
| Claude Code (extensão do VS Code) | Claude Pro – Opus 5.5 | Dashboard 1 |
| Claude Code (extensão do VS Code) | Claude Pro – Opus 5.5 | Dashboard 2 |
| Claude Code (extensão do VS Code) | Claude Pro – Opus 5.5 | rascunho-dashboard1.png e rascunho-dashboard2.png |
| Claude Code (extensão do VS Code) | Claude Pro – Opus 5.5 | entregas/justificativa-metricas.md |
| Claude Code (extensão do VS Code) | Claude Pro – Opus 5.5 | .streamlit/config.toml |
| Claude Code (extensão do VS Code) | Claude Pro – Opus 5.5 | README.md |
| Claude Code (extensão do VS Code) | Claude Pro – Opus 5.5 | Declaração de uso de IA |
| Skill oficial do Streamlit | Instalada com `streamlit skills --yes` em 29/10/2026 | Código dos dashboards a partir de 29/10/2026 |

## 4. Registro de usos (Opção B – bloco a bloco)

| **Uso nº 1** | |
|---|---|
| **Data** | 22/10/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5. Sem a Skill do Streamlit (ainda não instalada). |
| **Parte da atividade** | notebooks/eda-com-downloads.ipynb: célula de carregamento do dataset e células de exportação para data/raw e data/clean |
| **Finalidade** | Entender mensagens de erro e depurar código. |
| **O que foi pedido** | Adaptar a célula de carregamento, feita para o Google Colab, para ler o dataset local (diabetes-data.tar.Z); corrigir células com erro e com avisos do VS Code; converter as células "NOVA CÉLULA" do template, feitas para o Heart Disease, para salvar o dataset original e o tratado do Diabetes. |
| **O que foi aproveitado e o que foi modificado** | Aproveitei o código de extração e leitura local, as correções de tipo (float(), # type: ignore) e as células de exportação. As análises e conclusões do EDA não foram alteradas. |
| **Como verifiquei** | Rodei as células no VS Code e conferi que o dataset carregava e que data/clean/dataset.csv era gerado. |

| **Uso nº 2** | |
|---|---|
| **Data** | 22/10/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5. Sem a Skill do Streamlit (ainda não instalada). |
| **Parte da atividade** | src/data_loader.py e app.py (esqueleto do Dashboard 1) |
| **Finalidade** | Gerar o esqueleto do app.py. Não usei o Template de Prompt de 4 blocos: a IA adaptou o app.py do template da disciplina (feito para o Heart Disease) para o Diabetes Dataset, antes de o rascunho do Dashboard 1 existir. |
| **O que foi pedido** | Ajustar o app.py para o meu dataset, logo depois da adaptação do notebook. |
| **O que foi aproveitado e o que foi modificado** | Aproveitei: load_data() lendo data/clean/dataset.csv; montar_paciente_dia() com a tabela paciente-dia (média das glicemias por momento e soma das insulinas); a coluna classe (Hiperglicemia quando a média do dia passa de 180 mg/dL, o mesmo critério do meu EDA); a sidebar com seletor de variáveis, sliders de intervalo e toggle de classe. |
| **Como verifiquei** | A IA testou o app com um CSV igual ao gerado pelo notebook. Depois rodei streamlit run app.py e conferi que os widgets aparecem e respondem. |

| **Uso nº 3** | |
|---|---|
| **Data** | 22/10/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5. Sem a Skill do Streamlit (ainda não instalada). |
| **Parte da atividade** | entregas/rascunho-dashboard1.png |
| **Finalidade** | Nenhum item Permitido cobre exatamente a geração do rascunho; o mais próximo é "apoio na otimização da interface do dashboard". |
| **O que foi pedido** | Criar um PNG de rascunho do Dashboard 1 a partir do rascunho da professora, com o layout que a IA achasse melhor para o meu dataset. Depois pedi uma versão simples, com os mesmos elementos do rascunho da professora, mudando só posição e tamanho. |
| **O que foi aproveitado e o que foi modificado** | Rejeitei a primeira versão, em que a IA tinha acrescentado uma faixa de KPIs. Aproveitei a segunda, gerada em Matplotlib: sidebar igual, distribuição no meio e maior, correlação à direita e menor. As posições e os tamanhos foram escolhidos pela IA, e eu aprovei essa versão. |
| **Como verifiquei** | Comparei a imagem com o rascunho da professora e com os requisitos do Dashboard 1. |

| **Uso nº 4** | |
|---|---|
| **Data** | 29/10/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5. Nesta conversa a IA instalou a Skill oficial do Streamlit (streamlit skills --yes), usada daqui em diante. |
| **Parte da atividade** | Repositório (Aula 21): sincronização com o repositório da professora, notebooks/, entregas/README.md e prompts/declaracao-uso-ia.md |
| **Finalidade** | Usar a Skill oficial do Streamlit; dúvidas sobre Git (a IA executou os comandos). |
| **O que foi pedido** | Atualizar meu repositório com o que a professora adicionou no repositório original; conferir e fazer os passos que faltavam da Aula 21; preencher a declaração de IA. |
| **O que foi aproveitado e o que foi modificado** | A IA trouxe as mudanças do repositório original, renomeou os notebooks para os nomes pedidos, moveu o rascunho para entregas/, marcou o checklist, instalou a Skill, preencheu a declaração da Aula 21 e fez os commits e o push. |
| **Como verifiquei** | Conferi os arquivos no VS Code e no GitHub. |

| **Uso nº 5** | |
|---|---|
| **Data** | 29/10/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5, com a Skill oficial do Streamlit. |
| **Parte da atividade** | app.py (Dashboard 1) e src/data_loader.py |
| **Finalidade** | Apoio com a sintaxe de bibliotecas de visualização (Altair); entender mensagens de erro e depurar código. |
| **O que foi pedido** | Fazer a segunda parte da atividade seguindo o roteiro da Aula 22, que colei na conversa. No Dashboard 1: gráficos com @st.cache_data, testes com 0, 1 e 2+ variáveis e seleção ligada entre os gráficos (guia ALTAIR-CROSSFILTER.md). |
| **O que foi aproveitado e o que foi modificado** | Aproveitei o código como veio: histograma e heatmap de correlação em Altair (os tipos de gráfico vêm do enunciado), cache no carregamento, avisos para 0 e 1 variável e seleção no histograma recalculando a correlação. A correlação de Spearman é a mesma que usei no meu EDA; o mínimo de 10 paciente-dias por par (min_periods) foi definido pela IA. Os commits foram feitos pela IA. |
| **Como verifiquei** | A IA testou os cenários de borda com streamlit.testing e rodou o app; abri o app no navegador e testei os widgets. |

| **Uso nº 6** | |
|---|---|
| **Data** | 29/10/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5, com a Skill oficial do Streamlit. |
| **Parte da atividade** | .streamlit/config.toml e cores dos gráficos no app.py |
| **Finalidade** | Apoio na criação de identidade visual. |
| **O que foi pedido** | Tema em preto com amarelo, moderado, seguindo o roteiro. |
| **O que foi aproveitado e o que foi modificado** | A combinação preto e amarelo foi escolha minha. A IA definiu os códigos das cores (#0d0d0d, #f5c518 etc.) e as cores complementares dos gráficos (azul, laranja e cinza). Aproveitei como veio. |
| **Como verifiquei** | Abri o app e conferi a leitura dos textos e dos gráficos no tema escuro. |

| **Uso nº 7** | |
|---|---|
| **Data** | 29/10/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5, com a Skill oficial do Streamlit. |
| **Parte da atividade** | app.py (abas e aba do Dashboard 2) e src/data_loader.py (montar_glicemias, montar_insulina_dia) |
| **Finalidade** | Apoio com a sintaxe de bibliotecas de visualização (Altair); cálculo das métricas com apoio de IA. |
| **O que foi pedido** | O mesmo pedido do Uso nº 5: separar os dashboards em abas e implementar widgets, st.metric e gráficos Altair com seleção ligada aos KPIs. |
| **O que foi aproveitado e o que foi modificado** | Aproveitei o código como veio: filtros de paciente, período e momento; 5 st.metric com delta em relação à amostra; linha da glicemia mediana por semana com seleção por arraste; barras de faixas por momento do dia com seleção por clique; KPIs atualizados pelas seleções. |
| **Como verifiquei** | A IA testou com streamlit.testing; abri o app e testei os filtros e as seleções. |

| **Uso nº 8** | |
|---|---|
| **Data** | 29/10/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5, com a Skill oficial do Streamlit. |
| **Parte da atividade** | Dashboard 2: escolha das variáveis, das métricas, do público-alvo e dos widgets; entregas/rascunho-dashboard2.png; entregas/justificativa-metricas.md |
| **Finalidade** | Não se enquadra em item Permitido. A Seção 2 lista como Proibido deixar a IA escolher, propor ou justificar as métricas e pedir que ela escreva a justificativa. |
| **O que foi pedido** | O mesmo pedido do Uso nº 5. O roteiro da Aula 22 que colei incluía selecionar as variáveis, propor as métricas, definir os widgets, desenhar o rascunho e documentar a justificativa. |
| **O que foi aproveitado e o que foi modificado** | A IA escolheu as variáveis (glicemia e insulina), o público-alvo, as 5 métricas (glicemia mediana, % na faixa-alvo, % de hiperglicemia, % de hipoglicemia e insulina por dia) e os widgets (paciente, período e momento da medição), gerou o rascunho em Matplotlib e escreveu a justificativa. Aproveitei como veio. |
| **Como verifiquei** | Vi o Dashboard 2 rodando no navegador em 29/10. |

| **Uso nº 9** | |
|---|---|
| **Data** | 29/10/2026 e 03/11/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5, com a Skill oficial do Streamlit. |
| **Parte da atividade** | Projeto inteiro: app.py, entregas/ e a seção "Verificação dos requisitos" desta declaração |
| **Finalidade** | Entender mensagens de erro e depurar código. O histograma por variável vem do enunciado; o terceiro visual do Dashboard 2 foi escolhido pela IA, e não só a sintaxe dele. |
| **O que foi pedido** | Conferir se o projeto cumpre o enunciado da atividade (colei o texto) e os slides das Aulas 21, 22 e 23, e corrigir o que faltasse. Em 03/11, conferir de novo o enunciado e fazer o que estivesse faltando. |
| **O que foi aproveitado e o que foi modificado** | A IA trocou o histograma único com seletor por um histograma por variável (Dashboard 1), acrescentou a distribuição das medições como terceiro visual do Dashboard 2 e atualizou o rascunho do Dashboard 2. Em 03/11 não houve mudança nos arquivos. |
| **Como verifiquei** | A IA testou com streamlit.testing e no navegador. |

| **Uso nº 10** | |
|---|---|
| **Data** | 29/10/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5, com a Skill oficial do Streamlit. |
| **Parte da atividade** | app.py (layout dos dois dashboards), entregas/rascunho-dashboard1.png, entregas/rascunho-dashboard2.png, entregas/justificativa-metricas.md e comentários do código |
| **Finalidade** | Apoio na otimização da interface do dashboard (layout). A revisão da justificativa não se enquadra em item Permitido, porque o texto revisado tinha sido escrito pela IA (Uso nº 8). |
| **O que foi pedido** | Deixar a estrutura dos dois dashboards mais visual e organizada, ajustar os rascunhos se preciso, apagar todos os comentários do código e deixar a explicação das métricas mais geral e menos detalhada. |
| **O que foi aproveitado e o que foi modificado** | A IA reorganizou os dois dashboards em cartões (resumo no topo, pares mais correlacionados ao lado do heatmap e histogramas em grade no Dashboard 1; filtros, KPIs e gráficos agrupados no Dashboard 2), acrescentou o gráfico de pares mais correlacionados, gerou de novo as imagens dos rascunhos, apagou os comentários e encurtou a justificativa. Aproveitei como veio. |
| **Como verifiquei** | A IA testou o app depois das mudanças. |

| **Uso nº 11** | |
|---|---|
| **Data** | 29/10/2026 e 03/11/2026 |
| **Ferramenta** | Claude Code (Anthropic), extensão do VS Code, modelo Claude Opus 5.5. |
| **Parte da atividade** | prompts/declaracao-uso-ia.md e prompts/DECLARACAO_IA.pdf |
| **Finalidade** | Revisar a clareza de textos. A declaração em Markdown foi redigida pela IA a partir do que foi feito, não só revisada. |
| **O que foi pedido** | 29/10: preencher e atualizar a declaração de uso de IA. 03/11: conferir os trechos do projeto que falam de IA, rascunhar os blocos de registro a partir das conversas e do histórico do Git e ajustar esta declaração com base no PDF. |
| **O que foi aproveitado e o que foi modificado** | Usei os blocos rascunhados pela IA como base do registro no PDF e preenchi as demais seções do PDF. |
| **Como verifiquei** | Conferi os blocos com as conversas e com o histórico de commits. |

## 5. Trechos de código feitos com apoio de IA

| Arquivo / parte | Teve apoio de IA? | Tipo de apoio |
|---|---|---|
| app.py (esqueleto) | Sim | Geração do esqueleto, códigos base e testes (Usos nº 2 e 5) |
| Dashboard 1 (correlação + distribuição) | Sim | Código dos gráficos em Altair (os tipos de gráfico vêm do enunciado), seleção ligada, layout em cartões e testes (Usos nº 5, 9 e 10) |
| Dashboard 2 (KPIs) | Sim | Escolha das métricas, dos widgets e dos gráficos (Usos nº 8 e 9), implementação (Uso nº 7) e layout em cartões (Uso nº 10) |
| Deploy / configuração | Sim | Tema em .streamlit/config.toml (Uso nº 6) |

Os trechos estão marcados no código com `# [IA] Claude Code (Opus 5.5) – <finalidade>` em app.py, src/data_loader.py e .streamlit/config.toml.

## 6. Reflexão individual

A IA ajudou muito na geração de código, para concretizar de forma muito mais rápida as minhas ideias. A todo momento eu pensava em qual seria o melhor gráfico para ser utilizado ou qual o melhor contraste e as melhores práticas, mas não sabia bem como aplicar tecnicamente esses pontos nas ferramentas utilizadas, e usar IA me auxiliou muito no processo. Além disso, a IA me ajudou muito a garantir que todos os requisitos do projeto estavam sendo atendidos e a adaptar o meu dataset de acordo com o modelo apresentado pela professora, o que me poupou muito tempo.

Uma sugestão da IA que rejeitei foi a faixa de KPIs no primeiro rascunho do Dashboard 1. Já as métricas do Dashboard 2 foram escolhidas pela IA quando pedi que ela fizesse a segunda parte do roteiro (Uso nº 8), e por isso esse item está declarado como fora das situações permitidas.

## 7. Verificação dos requisitos do projeto

Verificação feita com a IA (Uso nº 9), contra a atividade, o `ROTEIRO.md` e os slides das Aulas 21, 22 e 23, testando o app com `streamlit.testing` e no navegador.

| Requisito (origem) | Situação |
|---|---|
| Notebook da EDA em `notebooks/`, salvando dados originais e tratados (Aula 21) | Cumprido: `data/raw/` e `data/clean/` |
| Sidebar com 1 seletor de variáveis e 1 slider de intervalo (Aula 21) | Cumprido |
| Rascunhos do Dashboard 1 e 2 em `entregas/` (Aulas 21 e 22) | Cumprido |
| Gráficos interativos com `@st.cache_data` (Aula 22) | Cumprido: Altair nos dois dashboards |
| Dashboard 1: heatmap de correlação e um histograma por variável (atividade, Aula 22) | Corrigido: antes havia um histograma só, com seletor |
| Testes com 0, 1 e 2+ variáveis e combinações de widgets (Aula 22) | Testado, sem erros |
| Identidade visual em `.streamlit/config.toml` (Aula 22) | Cumprido: preto e amarelo |
| Abas separando os dashboards (Aula 22) | Cumprido |
| Dashboard 2: 3 a 5 métricas, claras, acionáveis e ligadas a um público (Aulas 22 e 23) | Cumprido: 5 métricas, justificadas em `entregas/justificativa-metricas.md` |
| Dashboard 2: 3 visuais além das métricas, com seleção cruzada em Altair (Aulas 22 e 23) | Corrigido: antes eram 2 |
| Gráfico de barras agrupando uma variável (Aula 22) | Cumprido: faixas por momento do dia |
| `git status` limpo, push feito, `app.py` na raiz rodando sem erro (Aula 23) | Conferido |
| `data/clean/dataset.csv` versionado e caminho relativo (Aula 23) | Conferido |
| `requirements.txt` com as bibliotecas usadas (Aula 23) | Conferido (Altair já vem com o Streamlit) |
| Sem arquivos sensíveis (`secrets.toml`, `data/raw/dataset.csv` fora do Git) (Aula 23) | Conferido; pacientes aparecem só como número |
| Deploy, teste em janela anônima e link no README (Aula 23) | Pendente |
