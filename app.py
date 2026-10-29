import altair as alt
import streamlit as st

from src.data_loader import (
    COLS_GLICEMIA,
    COLS_INSULINA,
    LIMITE_HIPER,
    LIMITE_HIPO,
    MOMENTOS,
    load_data,
    montar_glicemias,
    montar_insulina_dia,
    montar_paciente_dia,
)

st.set_page_config(
    page_title="Diabetes Dataset — Dashboards",
    layout="wide",
)

st.title("Diabetes Dataset — Dashboards")

eventos = load_data()
df = montar_paciente_dia(eventos)
glicemias = montar_glicemias(eventos)
insulina_dia = montar_insulina_dia(eventos)

# Variáveis quantitativas do estudo (mesma lista COLS_CORR do notebook de EDA)
VARS_QUANT = [c for c in COLS_GLICEMIA + COLS_INSULINA if df[c].notna().any()]

# Paleta do app: amarelo de destaque sobre fundo escuro (mesmas cores do config.toml)
AMARELO = "#f5c518"
CINZA = "#8a8a8a"
CINZA_ESCURO = "#4d4d4d"
CORES_CLASSE = alt.Scale(
    domain=["Normal", "Hiperglicemia", "Sem glicemia"],
    range=[CINZA, AMARELO, CINZA_ESCURO],
)

# Sidebar: filtros do Dashboard 1 (variáveis + intervalo)
with st.sidebar:
    st.header("Filtros do Dashboard 1")

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

aba_correlacao, aba_acompanhamento = st.tabs(
    ["Dashboard 1 — Correlação entre variáveis", "Dashboard 2 — Acompanhamento glicêmico"]
)

with aba_correlacao:
    st.subheader("Avaliação de Correlação entre Variáveis Quantitativas")
    st.caption(
        f"{len(df_filtrado)} de {len(df)} paciente-dias dentro dos intervalos escolhidos "
        f"({df_filtrado['paciente'].nunique()} de {df['paciente'].nunique()} pacientes)."
    )

    # Dashboard 1 (como no rascunho): distribuição (histograma) à esquerda, correlação (heatmap) à direita
    col_distribuicao, col_correlacao = st.columns([1.5, 1])

    # Dias usados na correlação: muda quando o usuário arrasta uma faixa no histograma
    df_corr = df_filtrado

    with col_distribuicao:
        st.subheader("Distribuição")

        if not variaveis:
            st.warning("Selecione pelo menos 1 variável para ver a distribuição.")
        else:
            var_hist = st.selectbox("Variável do histograma", options=variaveis)
            dados_hist = df_filtrado[[var_hist, "classe"]].dropna()

            if dados_hist.empty:
                st.warning(f"Nenhum paciente-dia com {var_hist} dentro dos intervalos escolhidos.")
            else:
                faixa = alt.selection_interval(name="faixa", encodings=["x"])

                histograma = (
                    alt.Chart(dados_hist)
                    .mark_bar(color=AMARELO)
                    .encode(
                        x=alt.X(f"{var_hist}:Q", bin=alt.Bin(maxbins=30), title=var_hist),
                        y=alt.Y("count()", title="Paciente-dias"),
                        tooltip=[alt.Tooltip("count()", title="Paciente-dias")],
                    )
                    .add_params(faixa)
                    .properties(height=380)
                )
                if separar_por_classe:
                    histograma = histograma.encode(
                        color=alt.Color("classe:N", title="Classe", scale=CORES_CLASSE),
                        tooltip=["classe", alt.Tooltip("count()", title="Paciente-dias")],
                    )

                evento = st.altair_chart(
                    histograma, width="stretch", on_select="rerun", key=f"hist_{var_hist}_{separar_por_classe}"
                )
                st.caption("Arraste uma faixa no histograma para recalcular a correlação só com esses dias.")

                # A seleção volta como {campo: [início, fim]}; com bin, o campo pode vir com prefixo do bin
                for inicio, fim in evento.selection.get("faixa", {}).values():
                    df_corr = df_filtrado[df_filtrado[var_hist].between(inicio, fim)]

    with col_correlacao:
        st.subheader("Correlação (Spearman)")

        if len(variaveis) < 2:
            st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
        else:
            # Matriz de correlação em formato longo (uma linha por par de variáveis).
            # Cada par usa só os dias em que as duas foram medidas; com menos de MIN_DIAS dias o par fica vazio.
            MIN_DIAS = 10
            if len(df_corr) < len(df_filtrado):
                st.caption(f"Faixa selecionada no histograma: {len(df_corr)} paciente-dias.")
            corr = (
                df_corr[variaveis]
                .corr(method="spearman", min_periods=MIN_DIAS)
                .rename_axis(index="var_y", columns="var_x")
                .stack(future_stack=True)
                .rename("correlacao")
                .reset_index()
            )
            sem_dados = corr["correlacao"].isna()

            if sem_dados.all():
                st.warning("Poucos paciente-dias nos intervalos escolhidos para calcular a correlação.")
            else:
                if sem_dados.any():
                    st.caption(f"Células vazias: pares com menos de {MIN_DIAS} dias medidos em comum.")

                base = alt.Chart(corr[~sem_dados]).encode(
                    x=alt.X("var_x:N", title=None, sort=variaveis, axis=alt.Axis(labelAngle=-45)),
                    y=alt.Y("var_y:N", title=None, sort=variaveis),
                )
                heatmap = base.mark_rect().encode(
                    color=alt.Color(
                        "correlacao:Q",
                        title="Spearman",
                        scale=alt.Scale(domain=[-1, 0, 1], range=["#6c8ebf", "#262626", AMARELO]),
                    ),
                    tooltip=["var_x", "var_y", alt.Tooltip("correlacao:Q", format=".2f")],
                )
                valores = base.mark_text().encode(
                    text=alt.Text("correlacao:Q", format=".2f"),
                    color=alt.condition("datum.correlacao > 0.5", alt.value("black"), alt.value("white")),
                )

                st.altair_chart((heatmap + valores).properties(height=380), width="stretch")

with aba_acompanhamento:
    st.subheader("Acompanhamento Glicêmico")

    # Widgets do Dashboard 2 (rascunho: paciente, período e momento da medição, lado a lado)
    col_paciente, col_periodo, col_momento = st.columns(3)

    with col_paciente:
        paciente = st.selectbox(
            "Paciente",
            options=["Todos"] + sorted(glicemias["paciente"].unique().tolist()),
            format_func=lambda p: "Todos os pacientes" if p == "Todos" else f"Paciente {p}",
        )

    glic_paciente = glicemias if paciente == "Todos" else glicemias[glicemias["paciente"] == paciente]
    ins_paciente = insulina_dia if paciente == "Todos" else insulina_dia[insulina_dia["paciente"] == paciente]

    with col_periodo:
        # O período disponível muda com o paciente escolhido
        primeiro_dia, ultimo_dia = glic_paciente["data"].min(), glic_paciente["data"].max()
        periodo = st.slider(
            "Período",
            min_value=primeiro_dia,
            max_value=ultimo_dia,
            value=(primeiro_dia, ultimo_dia),
            format="DD/MM/YYYY",
            key=f"periodo_{paciente}",
        )

    with col_momento:
        momentos_existentes = [m for m in MOMENTOS.values() if m in set(glic_paciente["momento"])]
        momentos = st.multiselect(
            "Momento da medição",
            options=momentos_existentes,
            default=momentos_existentes,
            key=f"momentos_{paciente}",
        )

    glic_filtrada = glic_paciente[
        glic_paciente["data"].between(*periodo) & glic_paciente["momento"].isin(momentos)
    ]
    ins_filtrada = ins_paciente[ins_paciente["data"].between(*periodo)]

    # KPIs: o delta compara o recorte com a amostra completa (todos os pacientes, todo o período)
    def resumo(glic, ins):
        return {
            "mediana": glic["valor"].median(),
            "alvo": (glic["faixa"] == "Na faixa-alvo").mean() * 100,
            "hiper": (glic["faixa"] == "Hiperglicemia").mean() * 100,
            "hipo": (glic["faixa"] == "Hipoglicemia").mean() * 100,
            "insulina": ins["valor"].mean(),
        }

    geral = resumo(glicemias, insulina_dia)

    def mostrar_kpis(glic, ins):
        if glic.empty:
            st.warning("Nenhuma medição de glicemia com os filtros escolhidos.")
            return

        atual = resumo(glic, ins)
        tem_recorte = len(glic) < len(glicemias)

        def delta(chave, unidade):
            # Sem nenhum filtro o recorte é a própria amostra, então não há o que comparar
            if not tem_recorte:
                return None
            return f"{atual[chave] - geral[chave]:+.1f} {unidade} vs. amostra"

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric(
            "Glicemia mediana", f"{atual['mediana']:.0f} mg/dL", delta("mediana", "mg/dL"),
            delta_color="inverse", border=True,
        )
        k2.metric(
            f"Na faixa-alvo ({LIMITE_HIPO}–{LIMITE_HIPER})", f"{atual['alvo']:.0f}%", delta("alvo", "p.p."),
            border=True,
        )
        k3.metric(
            f"Hiperglicemia (> {LIMITE_HIPER})", f"{atual['hiper']:.0f}%", delta("hiper", "p.p."),
            delta_color="inverse", border=True,
        )
        k4.metric(
            f"Hipoglicemia (< {LIMITE_HIPO})", f"{atual['hipo']:.0f}%", delta("hipo", "p.p."),
            delta_color="inverse", border=True,
        )
        if ins.empty:
            k5.metric("Insulina por dia", "–", border=True)
        else:
            k5.metric(
                "Insulina por dia", f"{atual['insulina']:.0f} U", delta("insulina", "U"),
                delta_color="off", border=True,
            )
        st.caption(f"{len(glic)} medições de glicemia de {glic['paciente'].nunique()} paciente(s).")

    mostrar_kpis(glic_filtrada, ins_filtrada)

    # TODO: gráficos Altair (glicemia por semana e faixas por momento do dia) ligados aos KPIs
