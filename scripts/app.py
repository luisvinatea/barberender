"""app.py
Interface simples no streamlit para visualização de dados de vendas de carros
"""

import pandas as pd

import plotly.express as px
import streamlit as st
from io import BytesIO

from pathlib import Path
import warnings

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)

# ======================== PROCESSAMENTO DE DADOS ================================================

# Definindo o diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Definindo o caminho para o arquivo CSV de veículos
car_data_path = BASE_DIR / "data" / "vehicles.csv"

# Carregando os dados
car_data = pd.read_csv(car_data_path)
car_data = car_data.dropna()


def converter_para_numerico(serie, nome_coluna):
    # Converter para string, dividir por ponto e pegar a primeira parte (remove decimais)
    serie_limpa = serie.astype(str).str.split(".").str[0]
    # Converter para numérico, tratando erros
    serie_numerica = pd.to_numeric(serie_limpa, errors="coerce").astype(
        "Int64"
    )
    return serie_numerica


# Convertendo cada coluna numérica
car_data["model_year"] = converter_para_numerico(
    car_data["model_year"], "ano do modelo"
)
car_data["odometer"] = converter_para_numerico(
    car_data["odometer"], "quilometragem"
)
car_data["cylinders"] = converter_para_numerico(
    car_data["cylinders"], "cilindros"
)
car_data["is_4wd"] = converter_para_numerico(car_data["is_4wd"], "tração 4x4")

# Extraindo a marca (primeira palavra) e modelo (segunda palavra)
car_data["brand"] = car_data["model"].str.split(" ").str[0]
car_data["model"] = car_data["model"].str.split(" ").str[1]

# Convertendo a coluna de data para formato datetime
car_data["date_posted"] = pd.to_datetime(
    car_data["date_posted"], errors="coerce"
)

# Reorganizando as colunas em ordem lógica
colunas_organizadas = [
    "date_posted",  # Data de postagem
    "brand",  # Marca
    "model",  # Modelo
    "model_year",  # Ano do modelo
    "condition",  # Condição
    "odometer",  # Quilometragem
    "cylinders",  # Cilindros
    "fuel",  # Combustível
    "transmission",  # Transmissão
    "type",  # Tipo de veículo
    "paint_color",  # Cor
    "is_4wd",  # Tração 4x4
    "days_listed",  # Dias listado
    "price",  # Preço
]

car_data = car_data[colunas_organizadas]

# Renomeando colunas para português
car_data.rename(
    columns={
        "date_posted": "Data de Postagem",
        "brand": "Marca",
        "model": "Modelo",
        "model_year": "Ano do Modelo",
        "condition": "Condição",
        "odometer": "Quilometragem",
        "cylinders": "Cilindradas",
        "fuel": "Combustível",
        "transmission": "Transmissão",
        "type": "Tipo",
        "paint_color": "Cor",
        "is_4wd": "Tração 4x4",
        "days_listed": "Dias Listado",
        "price": "Preço",
    },
    inplace=True,
)

# Agregação de dados por marca
df_brands = (
    car_data.groupby("Marca")
    .agg(
        {
            "Cilindradas": "mean",  # Média de cilindros
            "Quilometragem": "mean",  # Quilometragem média
            "Tração 4x4": "mean",  # Proporção com tração 4x4
            "Dias Listado": "mean",  # Dias médios listado
            "Preço": "mean",  # Preço médio
            "Ano do Modelo": "mean",  # Ano médio
        }
    )
    .round(0)
)

df_brands = df_brands.reset_index()
df_brands = df_brands.astype(
    {
        "Cilindradas": int,
        "Quilometragem": int,
        "Tração 4x4": int,
        "Dias Listado": int,
        "Preço": int,
        "Ano do Modelo": int,
    }
)

# Agregação de dados por tipo
df_type = (
    car_data.groupby("Tipo")
    .agg(
        {
            "Cilindradas": "mean",  # Média de cilindros
            "Quilometragem": "mean",  # Quilometragem média
            "Tração 4x4": "mean",  # Proporção com tração 4x4
            "Dias Listado": "mean",  # Dias médios listado
            "Preço": "mean",  # Preço médio
            "Ano do Modelo": "mean",  # Ano médio
        }
    )
    .round(0)
)

df_type = df_type.reset_index()
df_type = df_type.astype(
    {
        "Cilindradas": int,
        "Quilometragem": int,
        "Tração 4x4": int,
        "Dias Listado": int,
        "Preço": int,
        "Ano do Modelo": int,
    }
)

# Agregação de dados por condição
df_condition = (
    car_data.groupby("Condição")
    .agg(
        {
            "Cilindradas": "mean",  # Média de cilindros
            "Quilometragem": "mean",  # Quilometragem média
            "Tração 4x4": "mean",  # Proporção com tração 4x4
            "Dias Listado": "mean",  # Dias médios listado
            "Preço": "mean",  # Preço médio
            "Ano do Modelo": "mean",  # Ano médio
        }
    )
    .round(0)
)

df_condition = df_condition.reset_index()
df_condition = df_condition.astype(
    {
        "Cilindradas": int,
        "Quilometragem": int,
        "Tração 4x4": int,
        "Dias Listado": int,
        "Preço": int,
        "Ano do Modelo": int,
    }
)

# Agregação de dados por combustível
df_fuel = (
    car_data.groupby("Combustível")
    .agg(
        {
            "Cilindradas": "mean",  # Média de cilindros
            "Quilometragem": "mean",  # Quilometragem média
            "Tração 4x4": "mean",  # Proporção com tração 4x4
            "Dias Listado": "mean",  # Dias médios listado
            "Preço": "mean",  # Preço médio
            "Ano do Modelo": "mean",  # Ano médio
        }
    )
    .round(0)
)

df_fuel = df_fuel.reset_index()
df_fuel = df_fuel.astype(
    {
        "Cilindradas": int,
        "Quilometragem": int,
        "Tração 4x4": int,
        "Dias Listado": int,
        "Preço": int,
        "Ano do Modelo": int,
    }
)


# ================================= FUNÇÕES DE VISUALIZAÇÃO =============================================

# Gráfico de preços por marca
fig1 = px.bar(
    df_brands,
    x="Marca",
    y="Preço",
    title="Preço Médio por Marca de Veículo",
    labels={"Marca": "Marca do Veículo", "Preço": "Preço Médio (USD)"},
    color="Preço",
    color_continuous_scale="viridis",
    height=500,
)
fig1.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de preços por tipo de veículo
fig2 = px.bar(
    df_type,
    x="Tipo",
    y="Preço",
    title="Preço Médio por Tipo de Veículo",
    labels={"Tipo": "Tipo de Veículo", "Preço": "Preço Médio (USD)"},
    color="Preço",
    color_continuous_scale="plasma",
    height=500,
)
fig2.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de preços por condição de veículo
fig3 = px.bar(
    df_condition,
    x="Condição",
    y="Preço",
    title="Preço Médio por Condição de Veículo",
    labels={"Condição": "Condição do Veículo", "Preço": "Preço Médio (USD)"},
    color="Preço",
    color_continuous_scale="cividis",
    height=500,
)
fig3.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de preços por combustível
fig4 = px.bar(
    df_fuel,
    x="Combustível",
    y="Preço",
    title="Preço Médio por Tipo de Combustível",
    labels={
        "Combustível": "Tipo de Combustível",
        "Preço": "Preço Médio (USD)",
    },
    color="Preço",
    color_continuous_scale="magma",
    height=500,
)
fig4.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de dias listado por marca
fig5 = px.bar(
    df_brands,
    x="Marca",
    y="Dias Listado",
    title="Dias Médios Listado por Marca",
    labels={
        "Marca": "Marca do Veículo",
        "Dias Listado": "Dias Médios Listado",
    },
    color="Dias Listado",
    color_continuous_scale="reds",
    height=500,
)
fig5.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de dias listado por tipo
fig6 = px.bar(
    df_type,
    x="Tipo",
    y="Dias Listado",
    title="Dias Médios Listado por Tipo de Veículo",
    labels={"Tipo": "Tipo de Veículo", "Dias Listado": "Dias Médios Listado"},
    color="Dias Listado",
    color_continuous_scale="oranges",
    height=500,
)
fig6.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de dias listado por condição
fig7 = px.bar(
    df_condition,
    x="Condição",
    y="Dias Listado",
    title="Dias Médios Listado por Condição do Veículo",
    labels={
        "Condição": "Condição do Veículo",
        "Dias Listado": "Dias Médios Listado",
    },
    color="Dias Listado",
    color_continuous_scale="purples",
    height=500,
)
fig7.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de dias listado por combustível
fig8 = px.bar(
    df_fuel,
    x="Combustível",
    y="Dias Listado",
    title="Dias Médios Listado por Tipo de Combustível",
    labels={
        "Combustível": "Tipo de Combustível",
        "Dias Listado": "Dias Médios Listado",
    },
    color="Dias Listado",
    color_continuous_scale="blues",
    height=500,
)
fig8.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de quilometragem por marca
fig9 = px.bar(
    df_brands,
    x="Marca",
    y="Quilometragem",
    title="Quilometragem Média por Marca",
    labels={
        "Marca": "Marca do Veículo",
        "Quilometragem": "Quilometragem Média (km)",
    },
    color="Quilometragem",
    color_continuous_scale="blues",
    height=500,
)
fig9.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de quilometragem por tipo
fig10 = px.bar(
    df_type,
    x="Tipo",
    y="Quilometragem",
    title="Quilometragem Média por Tipo de Veículo",
    labels={
        "Tipo": "Tipo de Veículo",
        "Quilometragem": "Quilometragem Média (km)",
    },
    color="Quilometragem",
    color_continuous_scale="greens",
    height=500,
)
fig10.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de quilometragem por condição
fig11 = px.bar(
    df_condition,
    x="Condição",
    y="Quilometragem",
    title="Quilometragem Média por Condição do Veículo",
    labels={
        "Condição": "Condição do Veículo",
        "Quilometragem": "Quilometragem Média (km)",
    },
    color="Quilometragem",
    color_continuous_scale="purples",
    height=500,
)
fig11.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

# Gráfico de quilometragem por combustível
fig12 = px.bar(
    df_fuel,
    x="Combustível",
    y="Quilometragem",
    title="Quilometragem Média por Tipo de Combustível",
    labels={
        "Combustível": "Tipo de Combustível",
        "Quilometragem": "Quilometragem Média (km)",
    },
    color="Quilometragem",
    color_continuous_scale="blues",
    height=500,
)
fig12.update_layout(
    xaxis_tickangle=-45,
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)

fig13 = px.histogram(
    car_data,
    x="Ano do Modelo",
    y="Preço",
    title="Distribuição de Preços por Ano do Modelo",
    labels={
        "Ano do Modelo": "Ano do Modelo",
        "Preço": "Preço (USD)",
        "count": "Frequência",
    },
    nbins=50,
    height=500,
    color_discrete_sequence=["skyblue"],
)
fig13.update_layout(
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    bargap=0.1,
)

fig14 = px.histogram(
    car_data,
    x="Dias Listado",
    y="Preço",
    title="Distribuição de Preços por Dias Listado",
    labels={
        "Dias Listado": "Dias Listado",
        "Preço": "Preço (USD)",
        "count": "Frequência",
    },
    nbins=100,
    height=500,
    color_discrete_sequence=["lightcoral"],
)
fig14.update_layout(
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
    bargap=0.1,
)

# Gráfico: Preço vs Quilometragem
fig15 = px.scatter(
    car_data,
    x="Quilometragem",
    y="Preço",
    title="Correlação: Preço vs Quilometragem",
    labels={
        "Quilometragem": "Quilometragem (km)",
        "Preço": "Preço (USD)",
        "Ano do Modelo": "Ano Modelo",
    },
    height=500,
    trendline="ols",
    color="Ano do Modelo",
    color_continuous_scale="plasma",
    range_x=[0, 300000],
    range_y=[0, 60000],
    opacity=0.7,
)
fig15.update_layout(
    title_font_size=16, xaxis_title_font_size=14, yaxis_title_font_size=14
)

# Gráfico: Dias Listado vs Combustível
fig16 = px.box(
    car_data,
    x="Dias Listado",
    y="Combustível",
    title="Distribuição do Combustível por Dias Listado",
    labels={
        "Dias Listado": "Dias Listado",
        "Combustível": "Tipo de Combustível",
    },
    height=500,
)
fig16.update_layout(
    title_font_size=16,
    xaxis_title_font_size=14,
    yaxis_title_font_size=14,
)


# ================================== INTERFACE STREAMLIT ==========================================
def to_excel_bytes(df, sheet_name="Sheet1"):
    output = BytesIO()
    try:
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        return output.getvalue()
    except Exception as e:
        st.error(f"Erro ao gerar arquivo Excel: {e}")
        return None


st.title("Análise de Vendas de Carros")

st.header("Dataset")
st.dataframe(car_data)
st.download_button(
    "Baixar em xlsx",
    data=to_excel_bytes(car_data, sheet_name="car_data"),
    file_name="car_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.subheader("Médias Agrupadas por Marca")
st.dataframe(df_brands)
st.download_button(
    "Baixar em xlsx",
    data=to_excel_bytes(df_brands, sheet_name="df_brands"),
    file_name="df_brands.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.subheader("Médias Agrupadas por Tipo")
st.dataframe(df_type)
st.download_button(
    "Baixar em xlsx",
    data=to_excel_bytes(df_type, sheet_name="df_type"),
    file_name="df_type.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.subheader("Médias Agrupadas por Condição")
st.dataframe(df_condition)
st.download_button(
    "Baixar em xlsx",
    data=to_excel_bytes(df_condition, sheet_name="df_condition"),
    file_name="df_condition.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.subheader("Médias Agrupadas por Combustível")
st.dataframe(df_fuel)
st.download_button(
    "Baixar em xlsx",
    data=to_excel_bytes(df_fuel, sheet_name="df_fuel"),
    file_name="df_fuel.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

st.header("Visualizações")

# Dicionário mapeando nomes dos gráficos para suas figuras
graficos = {
    "Preço Médio por Marca": fig1,
    "Preço Médio por Tipo": fig2,
    "Preço Médio por Condição": fig3,
    "Preço Médio por Combustível": fig4,
    "Dias Listado por Marca": fig5,
    "Dias Listado por Tipo": fig6,
    "Dias Listado por Condição": fig7,
    "Dias Listado por Combustível": fig8,
    "Quilometragem por Marca": fig9,
    "Quilometragem por Tipo": fig10,
    "Quilometragem por Condição": fig11,
    "Quilometragem por Combustível": fig12,
    "Distribuição de Preços por Ano": fig13,
    "Distribuição de Preços por Dias Listado": fig14,
    "Correlação Preço vs Quilometragem": fig15,
    "Distribuição Combustível por Dias Listado": fig16,
}

# Selectbox para escolher um gráfico específico
grafico_selecionado = st.selectbox(
    "Selecione um Gráfico:", ["Todos"] + list(graficos.keys())
)

if grafico_selecionado == "Todos":
    if st.button("Ver Todos os Gráficos"):
        for fig in graficos.values():
            st.plotly_chart(fig)
else:
    st.plotly_chart(graficos[grafico_selecionado])
