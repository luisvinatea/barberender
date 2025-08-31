import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# Defino o diretório raiz para procurar arquivos no projeto
BASE_DIR = Path(__file__).resolve().parent

# Defino o caminho para o arquivo CSV
car_data_path = BASE_DIR / "data/vehicles.csv"
car_data = pd.read_csv(car_data_path)  # lendo os dados
hist_button = st.button("Criar histograma")  # criar um botão

if hist_button:  # se o botão for clicado
    # escrever uma mensagem
    st.write(
        "Criando um histograma para o conjunto de dados de anúncios de vendas de carros"
    )

    # criar um histograma
    fig = px.histogram(car_data, x="odometer")

    # exibir um gráfico Plotly interativo
    st.plotly_chart(fig, use_container_width=True)
