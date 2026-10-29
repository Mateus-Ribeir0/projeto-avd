# Declaração de Uso de IA

**Nome:** Mateus Ribeiro
**Data:** 29/10/2026 (Aulas 21 e 22)

## Ferramenta

Claude Code (Anthropic), com as skills do Streamlit instaladas via `streamlit skills --yes`.

## Aula 21 — Prompt usado

1. **Rascunho → esqueleto do `app.py`**: template de [layout-skeleton-prompt.md](layout-skeleton-prompt.md), com a imagem do rascunho anexada ([../entregas/rascunho-dashboard1.png](../entregas/rascunho-dashboard1.png)):

```text
Contexto: sou aluno da disciplina Análise e Visualização de Dados. Estou criando um dashboard
em Streamlit para avaliar a correlação entre as variáveis quantitativas do Diabetes Dataset (UCI),
agregado por paciente-dia.

Entrada: rascunho do layout em entregas/rascunho-dashboard1.png (anexo). Sidebar com seletor de variáveis
quantitativas, sliders de intervalo e um toggle para distinguir por classe; área principal com o heatmap
de correlação à esquerda e a distribuição (histogramas) à direita. Colunas: paciente, dia, glicemias
(pré-café, pré-almoço, pré-jantar, pré-lanche), insulina_regular, insulina_nph e classe.

Restrições: usar Streamlit; editar apenas o app.py; carregar os dados via src/data_loader.py;
não implementar os gráficos ainda.

Formato de saída: esqueleto completo do app.py com os widgets funcionando e comentários # TODO
nas partes dos gráficos.
```

2. **Organização do código**: pedidos para organizar o `app.py` e o `src/data_loader.py` (separar o carregamento e a montagem paciente-dia em funções, nomes de variáveis e comentários em português, filtros aplicados de forma consistente) e para organizar os arquivos do repositório nos caminhos pedidos pela atividade.

## Aula 21 — O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** a estrutura do layout (sidebar com filtros + duas colunas para correlação e distribuição), o seletor de variáveis, um slider de intervalo por variável e o toggle de classe.
- **Modificado:** o esqueleto foi adaptado do Heart Disease Dataset para o Diabetes Dataset: a lista de variáveis passou a vir do `data_loader` e o filtro de intervalo passou a manter os dias com medição ausente, já que cada paciente-dia tem só parte das medições.
- **Rejeitado:** implementar os gráficos (heatmap e histogramas) nesta etapa, porque a atividade pede só o esqueleto com os widgets; eles ficaram como `# TODO`.

## Aula 22 — Prompts usados

Mesma ferramenta (Claude Code), numa conversa só, seguindo os passos do `ROTEIRO.md`. Resumo dos pedidos:

1. Implementar os gráficos do Dashboard 1 em Altair seguindo o rascunho (histograma à esquerda, heatmap de correlação à direita), com `@st.cache_data` no carregamento dos dados.
2. Testar o Dashboard 1 com 0, 1 e 2+ variáveis e com intervalos estreitos, e corrigir o que quebrasse.
3. Ligar o histograma à correlação com seleção do Altair (guia `ALTAIR-CROSSFILTER.md`).
4. Montar a identidade visual em preto e amarelo no `.streamlit/config.toml`.
5. Estruturar o Dashboard 2 na ordem do roteiro (variáveis → métricas → widgets → rascunho), separar os dashboards em abas e implementar widgets, `st.metric` e gráficos Altair com seleção ligada aos KPIs.
6. Organizar o código e os commits por etapa.
7. Verificar se o app cumpre os requisitos da atividade (ver seção abaixo).
8. Reorganizar o layout dos dois dashboards em cartões, atualizar os rascunhos, remover comentários do código e deixar a justificativa das métricas mais direta.

## Aula 22 — O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** gráficos em Altair nos dois dashboards; mediana (e não média) como medida central da glicemia, por causa da assimetria vista no EDA; KPIs em proporção de medições por faixa (hipo < 70, alvo 70–180, hiper > 180), com o mesmo limite de 180 mg/dL usado na classe do Dashboard 1; seleção por arraste (período) e por clique (momento do dia) atualizando os KPIs via `on_select`.
- **Modificado:** o layout passou a ser em cartões (resumo no topo, correlação e pares mais correlacionados lado a lado, histogramas em grade no Dashboard 1; filtros, KPIs e gráficos agrupados no Dashboard 2), e os rascunhos foram refeitos para acompanhar; a correlação passou a exigir pelo menos 10 dias em comum por par (`min_periods`), porque cada paciente-dia tem só parte das medições e alguns pares ficavam com valores sem sentido; os KPIs ficam acima dos gráficos, como no rascunho, usando um `st.container` preenchido depois da seleção; rótulos do heatmap e formato das datas ajustados depois de ver o app rodando.
- **Rejeitado:** usar `st.stop()` quando não há dados para a correlação, porque interromperia também o Dashboard 2 na outra aba; trocado por avisos em cada gráfico.

## Verificação dos requisitos do projeto

Pedi à IA para conferir o projeto contra a atividade, o `ROTEIRO.md` e os slides das Aulas 21, 22 e 23 (hands-on, checagem do repositório e checklist final), testando o app com `streamlit.testing` e no navegador. Itens que não estavam cumpridos foram corrigidos; os demais foram só conferidos.

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
