import altair as alt
import pandas as pd
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

VARS_QUANT = [c for c in COLS_GLICEMIA + COLS_INSULINA if df[c].notna().any()]
MIN_DIAS = 10

AMARELO = "#f5c518"
AZUL = "#6c8ebf"
LARANJA = "#e8590c"
CINZA = "#8a8a8a"
CINZA_ESCURO = "#4d4d4d"
CORES_CLASSE = alt.Scale(
    domain=["Normal", "Hiperglicemia", "Sem glicemia"],
    range=[CINZA, AMARELO, CINZA_ESCURO],
)
ESCALA_CORRELACAO = alt.Scale(domain=[-1, 0, 1], range=[AZUL, "#262626", AMARELO])
ORDEM_FAIXA = ["Hipoglicemia", "Na faixa-alvo", "Hiperglicemia"]
CORES_FAIXA = alt.Scale(domain=ORDEM_FAIXA, range=[AZUL, AMARELO, LARANJA])


def titulo_cartao(texto):
    st.markdown(f"##### {texto}")


with st.sidebar:
    st.header("Filtros do Dashboard 1")

    variaveis = st.multiselect(
        "Variáveis quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
    )

    separar_por_classe = st.toggle(
        "Distinguir por classe",
        value=False,
        help="Normal ou Hiperglicemia (média das glicemias do dia > 180 mg/dL).",
    )

    intervalos = {}
    with st.expander("Intervalos das variáveis", expanded=True):
        for var in variaveis:
            minimo, maximo = float(df[var].min()), float(df[var].max())
            intervalos[var] = st.slider(
                var,
                min_value=minimo,
                max_value=maximo,
                value=(minimo, maximo),
                step=1.0,
                key=f"intervalo_{var}",
            )

df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].isna() | df_filtrado[var].between(inicio, fim)]

aba_correlacao, aba_acompanhamento = st.tabs(
    ["Dashboard 1 — Correlação entre variáveis", "Dashboard 2 — Acompanhamento glicêmico"]
)

with aba_correlacao:
    st.subheader("Avaliação de Correlação entre Variáveis Quantitativas")

    r1, r2, r3 = st.columns(3)
    r1.metric("Paciente-dias no filtro", f"{len(df_filtrado)} de {len(df)}", border=True)
    r2.metric(
        "Pacientes",
        f"{df_filtrado['paciente'].nunique()} de {df['paciente'].nunique()}",
        border=True,
    )
    r3.metric("Variáveis selecionadas", f"{len(variaveis)} de {len(VARS_QUANT)}", border=True)

    area_correlacao = st.container()

    df_corr = df_filtrado

    with st.container(border=True):
        titulo_cartao("Distribuição por variável")

        if not variaveis:
            st.warning("Selecione pelo menos 1 variável para ver a distribuição.")
        else:
            st.caption("Arraste uma faixa em um histograma para recalcular a correlação só com esses dias.")

            for inicio_linha in range(0, len(variaveis), 3):
                colunas = st.columns(3)
                for coluna, var in zip(colunas, variaveis[inicio_linha : inicio_linha + 3]):
                    with coluna:
                        dados_hist = df_filtrado[[var, "classe"]].dropna()
                        if dados_hist.empty:
                            st.warning(f"Sem dados de {var} nos intervalos escolhidos.")
                            continue

                        faixa = alt.selection_interval(name="faixa", encodings=["x"])
                        histograma = (
                            alt.Chart(dados_hist, title=var)
                            .mark_bar(color=AMARELO)
                            .encode(
                                x=alt.X(f"{var}:Q", bin=alt.Bin(maxbins=20), title=None),
                                y=alt.Y("count()", title=None),
                                tooltip=[alt.Tooltip("count()", title="Paciente-dias")],
                            )
                            .add_params(faixa)
                            .properties(height=170)
                        )
                        if separar_por_classe:
                            histograma = histograma.encode(
                                color=alt.Color("classe:N", scale=CORES_CLASSE, legend=None),
                                tooltip=["classe", alt.Tooltip("count()", title="Paciente-dias")],
                            )

                        evento = st.altair_chart(
                            histograma,
                            width="stretch",
                            on_select="rerun",
                            key=f"hist_{var}_{separar_por_classe}",
                        )

                        for inicio, fim in evento.selection.get("faixa", {}).values():
                            df_corr = df_corr[df_corr[var].between(inicio, fim)]

            if separar_por_classe:
                st.caption("Cores: amarelo = Hiperglicemia · cinza = Normal · cinza escuro = Sem glicemia.")

    with area_correlacao:
        col_heatmap, col_pares = st.columns([3, 2])

        if len(variaveis) < 2:
            col_heatmap.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
        else:
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
                col_heatmap.warning("Poucos paciente-dias nos intervalos escolhidos para calcular a correlação.")
            else:
                with col_heatmap.container(border=True):
                    titulo_cartao("Correlação (Spearman)")
                    if len(df_corr) < len(df_filtrado):
                        st.caption(f"Faixa selecionada nos histogramas: {len(df_corr)} paciente-dias.")

                    base = alt.Chart(corr[~sem_dados]).encode(
                        x=alt.X(
                            "var_x:N",
                            title=None,
                            sort=variaveis,
                            axis=alt.Axis(labelAngle=-35, labelOverlap=False, labelLimit=160),
                        ),
                        y=alt.Y("var_y:N", title=None, sort=variaveis, axis=alt.Axis(labelLimit=160)),
                    )
                    heatmap = base.mark_rect().encode(
                        color=alt.Color("correlacao:Q", title="ρ", scale=ESCALA_CORRELACAO),
                        tooltip=["var_x", "var_y", alt.Tooltip("correlacao:Q", format=".2f")],
                    )
                    valores = base.mark_text().encode(
                        text=alt.Text("correlacao:Q", format=".2f"),
                        color=alt.condition("datum.correlacao > 0.5", alt.value("black"), alt.value("white")),
                    )
                    st.altair_chart((heatmap + valores).properties(height=340), width="stretch")

                with col_pares.container(border=True):
                    titulo_cartao("Pares mais correlacionados")

                    ordem = {var: i for i, var in enumerate(variaveis)}
                    pares = corr[~sem_dados & (corr["var_y"].map(ordem) > corr["var_x"].map(ordem))].copy()
                    pares["par"] = pares["var_x"] + " × " + pares["var_y"]
                    pares["forca"] = pares["correlacao"].abs()
                    pares = pares.nlargest(6, "forca")

                    base_pares = alt.Chart(pares).encode(
                        y=alt.Y("par:N", title=None, sort="-x", axis=alt.Axis(labelLimit=260)),
                        x=alt.X("correlacao:Q", title="ρ"),
                        tooltip=["par", alt.Tooltip("correlacao:Q", format=".2f")],
                    )
                    barras_pares = base_pares.mark_bar().encode(
                        color=alt.condition("datum.correlacao >= 0", alt.value(AMARELO), alt.value(AZUL)),
                    )
                    rotulos_pares = base_pares.mark_text(align="left", dx=4, color="white").encode(
                        text=alt.Text("correlacao:Q", format=".2f"),
                    )
                    st.altair_chart((barras_pares + rotulos_pares).properties(height=340), width="stretch")

with aba_acompanhamento:
    st.subheader("Acompanhamento Glicêmico")

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

    def resumo(glic, ins):
        return {
            "mediana": glic["valor"].median(),
            "alvo": (glic["faixa"] == "Na faixa-alvo").mean() * 100,
            "hiper": (glic["faixa"] == "Hiperglicemia").mean() * 100,
            "hipo": (glic["faixa"] == "Hipoglicemia").mean() * 100,
            "insulina": ins["valor"].mean(),
        }

    geral = resumo(glicemias, insulina_dia)

    def para_data(valor):
        data = pd.to_datetime(valor, unit="ms") if isinstance(valor, (int, float)) else pd.to_datetime(valor)
        return data.tz_localize(None) if data.tzinfo else data

    def mostrar_kpis(glic, ins):
        if glic.empty:
            st.warning("Nenhuma medição de glicemia com os filtros escolhidos.")
            return

        atual = resumo(glic, ins)
        tem_recorte = len(glic) < len(glicemias)

        def delta(chave, unidade):
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

    area_kpis = st.container()

    glic_selecionada, ins_selecionada = glic_filtrada, ins_filtrada

    if not glic_filtrada.empty:
        col_semana, col_faixas = st.columns([1.5, 1])

        with col_semana:
            st.markdown("**Glicemia mediana por semana**")

            por_semana = glic_filtrada.groupby("semana", as_index=False).agg(
                mediana=("valor", "median"), medicoes=("valor", "size")
            )
            periodo_grafico = alt.selection_interval(name="periodo", encodings=["x"])

            faixa_alvo = (
                alt.Chart(pd.DataFrame({"inicio": [LIMITE_HIPO], "fim": [LIMITE_HIPER]}))
                .mark_rect(color=AMARELO, opacity=0.12)
                .encode(y="inicio:Q", y2="fim:Q")
            )
            linha = (
                alt.Chart(por_semana)
                .mark_line(color=AMARELO, point=alt.OverlayMarkDef(color=AMARELO))
                .encode(
                    x=alt.X("semana:T", title="Semana", axis=alt.Axis(format="%m/%Y")),
                    y=alt.Y("mediana:Q", title="Glicemia mediana (mg/dL)"),
                    tooltip=[
                        alt.Tooltip("semana:T", title="Semana de", format="%d/%m/%Y"),
                        alt.Tooltip("mediana:Q", title="Mediana (mg/dL)", format=".0f"),
                        alt.Tooltip("medicoes:Q", title="Medições"),
                    ],
                )
                .add_params(periodo_grafico)
            )

            evento_semana = st.altair_chart(
                (faixa_alvo + linha).properties(height=320),
                width="stretch",
                on_select="rerun",
                key=f"semanas_{paciente}",
            )
            st.caption(
                f"Faixa clara: alvo de {LIMITE_HIPO} a {LIMITE_HIPER} mg/dL. "
                "Arraste no gráfico para ver só um trecho do período."
            )

            for inicio, fim in evento_semana.selection.get("periodo", {}).values():
                inicio, fim = para_data(inicio).normalize(), para_data(fim)
                glic_selecionada = glic_filtrada[glic_filtrada["semana"].between(inicio, fim)]
                dias_insulina = pd.to_datetime(ins_filtrada["data"])
                ins_selecionada = ins_filtrada[dias_insulina.between(inicio, fim + pd.Timedelta(days=6))]

        with col_faixas:
            st.markdown("**Faixas por momento do dia**")

            por_momento = (
                glic_selecionada.groupby(["momento", "faixa"], as_index=False)
                .size()
                .rename(columns={"size": "medicoes"})
            )
            por_momento["ordem"] = por_momento["faixa"].map(ORDEM_FAIXA.index)
            clique = alt.selection_point(name="momento", fields=["momento"])

            barras = (
                alt.Chart(por_momento)
                .mark_bar()
                .encode(
                    y=alt.Y("momento:N", title=None, sort=list(MOMENTOS.values())),
                    x=alt.X("medicoes:Q", stack="normalize", title="Medições", axis=alt.Axis(format="%")),
                    color=alt.Color("faixa:N", title="Faixa", scale=CORES_FAIXA, sort=ORDEM_FAIXA),
                    order=alt.Order("ordem:Q"),
                    opacity=alt.condition(clique, alt.value(1), alt.value(0.35)),
                    tooltip=["momento", "faixa", alt.Tooltip("medicoes:Q", title="Medições")],
                )
                .add_params(clique)
                .properties(height=320)
            )

            evento_momento = st.altair_chart(
                barras, width="stretch", on_select="rerun", key=f"momentos_grafico_{paciente}"
            )
            st.caption("Clique num momento do dia para ver os KPIs só dele (shift + clique para vários).")

            clicados = [item["momento"] for item in evento_momento.selection.get("momento", [])]
            if clicados:
                glic_selecionada = glic_selecionada[glic_selecionada["momento"].isin(clicados)]

        st.markdown("**Distribuição das medições de glicemia**")
        distribuicao = (
            alt.Chart(glic_selecionada[["valor", "faixa"]])
            .mark_bar()
            .encode(
                x=alt.X("valor:Q", bin=alt.Bin(step=10), title="Glicemia (mg/dL)"),
                y=alt.Y("count()", title="Medições"),
                color=alt.Color("faixa:N", title="Faixa", scale=CORES_FAIXA, sort=ORDEM_FAIXA),
                tooltip=["faixa", alt.Tooltip("count()", title="Medições")],
            )
            .properties(height=240)
        )
        regras = (
            alt.Chart(pd.DataFrame({"limite": [LIMITE_HIPO, LIMITE_HIPER]}))
            .mark_rule(color="white", strokeDash=[4, 4])
            .encode(x="limite:Q")
        )
        st.altair_chart(distribuicao + regras, width="stretch")
        st.caption(
            f"Linhas tracejadas: limites de {LIMITE_HIPO} e {LIMITE_HIPER} mg/dL. "
            "Mostra as medições que entram nos KPIs acima."
        )

    with area_kpis:
        mostrar_kpis(glic_selecionada, ins_selecionada)
