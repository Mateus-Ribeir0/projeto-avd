import streamlit as st

from src.data_loader import COLS_GLICEMIA, COLS_INSULINA, load_data, montar_paciente_dia

st.set_page_config(
    page_title="Avaliação de Correlação entre Variáveis Quantitativas do Diabetes Dataset",
    layout="wide",
)

st.title("Avaliação de Correlação entre Variáveis Quantitativas do Diabetes Dataset")

eventos = load_data()
df = montar_paciente_dia(eventos)

# Variáveis quantitativas do estudo (mesma lista COLS_CORR do notebook de EDA)
VARS_QUANT = [c for c in COLS_GLICEMIA + COLS_INSULINA if df[c].notna().any()]

# Sidebar: filtros (variáveis + intervalo)
with st.sidebar:
    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis Quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
    )

    separar_por_classe = st.toggle(
        "Distinguir por Classe",
        value=False,
        help="Colore a distribuição pela classe do dia (Normal ou Hiperglicemia: média das glicemias > 180 mg/dL).",
    )

    # Um slider de intervalo para cada variável selecionada
    intervalos = {}
    for var in variaveis:
        minimo, maximo = float(df[var].min()), float(df[var].max())
        intervalos[var] = st.slider(
            f"Intervalo de {var}",
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=1.0,
            key=f"intervalo_{var}",
        )

# Mantém só os paciente-dias dentro de todos os intervalos escolhidos.
# Cada dia tem só parte das medições, então valor ausente não elimina o dia.
df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].isna() | df_filtrado[var].between(inicio, fim)]

st.caption(
    f"{len(df_filtrado)} de {len(df)} paciente-dias dentro dos intervalos escolhidos "
    f"({df_filtrado['paciente'].nunique()} de {df['paciente'].nunique()} pacientes)."
)

# Dashboard 1: correlação (heatmap) à esquerda, distribuição (histograma) à direita
col_correlacao, col_distribuicao = st.columns([1, 1.5])

with col_correlacao:
    st.subheader("Correlação")

    if len(variaveis) < 2:
        st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
    else:
        # TODO: matriz de correlação das variáveis selecionadas (df_filtrado[variaveis].corr(method="spearman"))
        # TODO: heatmap (plotly px.imshow) e exibir com st.plotly_chart
        pass

with col_distribuicao:
    st.subheader("Distribuição")

    # TODO: st.selectbox para escolher a variável do histograma
    # TODO: histograma (plotly px.histogram) e exibir com st.plotly_chart
    #       se separar_por_classe: color="classe"

# TODO: Dashboard 2 — KPIs (Aula 22)
