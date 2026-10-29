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
