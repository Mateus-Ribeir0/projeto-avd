# Declaração de Uso de IA

**Nome:** Mateus Ribeiro
**Data:** 29/10/2026

## Ferramenta

Claude Code (Anthropic), com as skills do Streamlit instaladas via `streamlit skills --yes`.

## Prompt usado

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

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** a estrutura do layout (sidebar com filtros + duas colunas para correlação e distribuição), o seletor de variáveis, um slider de intervalo por variável e o toggle de classe.
- **Modificado:** o esqueleto foi adaptado do Heart Disease Dataset para o Diabetes Dataset: a lista de variáveis passou a vir do `data_loader` e o filtro de intervalo passou a manter os dias com medição ausente, já que cada paciente-dia tem só parte das medições.
- **Rejeitado:** implementar os gráficos (heatmap e histogramas) nesta etapa, porque a atividade pede só o esqueleto com os widgets; eles ficaram como `# TODO`.
