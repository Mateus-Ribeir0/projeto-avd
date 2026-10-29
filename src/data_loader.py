import pandas as pd
import streamlit as st

# Variáveis do formato paciente-dia (mesma lista COLS_CORR do notebook de EDA)
COLS_GLICEMIA = [
    "glicemia_pre_cafe", "glicemia_pre_almoco", "glicemia_pre_jantar", "glicemia_pre_lanche",
]
COLS_INSULINA = ["insulina_regular", "insulina_nph"]
COD_INSULINA = [33, 34, 35]


@st.cache_data
def load_data(path="data/clean/dataset.csv"):
    """Lê o dataset já tratado (exportado ao final do notebook de EDA), um evento por linha."""
    df = pd.read_csv(path)
    df["datahora"] = pd.to_datetime(df["datahora"], errors="coerce")
    return df


@st.cache_data
def montar_paciente_dia(df):
    """Reorganiza os eventos no formato largo: uma linha por paciente-dia, como no notebook.

    Glicemias são a média do dia por momento; insulinas são a soma das doses do dia.
    A classe do dia é 'Hiperglicemia' quando a média de todas as glicemias do dia passa de 180 mg/dL,
    'Normal' caso contrário, e 'Sem glicemia' quando o dia só tem registros de insulina.
    """
    df = df.dropna(subset=["datahora"]).copy()
    df["dia"] = df["datahora"].dt.date

    glic = df[df["eh_glicemia"] & (df["valor"] > 0)]
    glic_dia = glic.pivot_table(index=["paciente", "dia"], columns="evento",
                                values="valor", aggfunc="mean")

    insulina_dia = df[df["codigo"].isin(COD_INSULINA)].pivot_table(
        index=["paciente", "dia"], columns="evento", values="valor", aggfunc="sum")

    largo = glic_dia.join(insulina_dia, how="outer")
    largo = largo.reindex(columns=COLS_GLICEMIA + COLS_INSULINA)

    media_dia = glic.groupby(["paciente", "dia"])["valor"].mean().reindex(largo.index)
    largo["classe"] = "Sem glicemia"
    largo.loc[media_dia <= 180, "classe"] = "Normal"
    largo.loc[media_dia > 180, "classe"] = "Hiperglicemia"

    return largo.reset_index()


# Dashboard 2: faixas de glicemia (mg/dL) e nome de cada momento da medição
LIMITE_HIPO = 70
LIMITE_HIPER = 180
MOMENTOS = {
    "glicemia_pre_cafe": "Pré-café",
    "glicemia_pos_cafe": "Pós-café",
    "glicemia_pre_almoco": "Pré-almoço",
    "glicemia_pos_almoco": "Pós-almoço",
    "glicemia_pre_lanche": "Pré-lanche",
    "glicemia_pre_jantar": "Pré-jantar",
    "glicemia_pos_jantar": "Pós-jantar",
    "glicemia_nao_especificada": "Não especificado",
}


@st.cache_data
def montar_glicemias(df):
    """Uma linha por medição de glicemia, com o momento do dia, a semana e a faixa (hipo / alvo / hiper)."""
    glic = df[df["eh_glicemia"] & (df["valor"] > 0)].dropna(subset=["datahora"]).copy()
    glic["momento"] = glic["evento"].map(MOMENTOS)
    glic["data"] = glic["datahora"].dt.date
    glic["semana"] = glic["datahora"].dt.to_period("W").dt.start_time
    glic["faixa"] = "Na faixa-alvo"
    glic.loc[glic["valor"] < LIMITE_HIPO, "faixa"] = "Hipoglicemia"
    glic.loc[glic["valor"] > LIMITE_HIPER, "faixa"] = "Hiperglicemia"
    return glic[["paciente", "datahora", "data", "semana", "momento", "valor", "faixa"]]


@st.cache_data
def montar_insulina_dia(df):
    """Total de insulina (regular + NPH + ultralenta) aplicado por paciente-dia."""
    ins = df[df["codigo"].isin(COD_INSULINA)].dropna(subset=["datahora"]).copy()
    ins["data"] = ins["datahora"].dt.date
    return ins.groupby(["paciente", "data"], as_index=False)["valor"].sum()
