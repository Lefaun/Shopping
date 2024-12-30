import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Nome do arquivo CSV onde os dados serão armazenados
CSV_FILE = "compras.csv"

# Função para inicializar ou carregar o CSV
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # Criar um DataFrame vazio com estrutura esperada
        df = pd.DataFrame({"Dia": range(1, 31), "Valor": [0] * 30})
        df.to_csv(CSV_FILE, index=False)
        return df

# Função para salvar dados no CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Carregar dados existentes
compras = load_data()

# Configurar interface do Streamlit
st.title("Controle de Compras com Orçamento")
st.write("Adicione suas compras e acompanhe até atingir o limite do orçamento.")

# Entrada de orçamento total
if "budget" not in st.session_state:
    st.session_state.budget = 0.0
if "total_gasto" not in st.session_state:
    st.session_state.total_gasto = 0.0

st.session_state.budget = st.number_input("Defina seu orçamento total:", min_value=0.0, step=0.01, value=st.session_state.budget)

# Loop de adicionar compras enquanto houver orçamento
while st.session_state.total_gasto < st.session_state.budget:
    with st.form("adicionar_compra_form"):
        selected_day = st.selectbox("Selecione o dia:", compras["Dia"])
        valor = st.number_input("Insira o valor da compra:", min_value=0.0, step=0.01, key="valor_compra")
        submitted = st.form_submit_button("Adicionar Compra")

        if submitted:
            if st.session_state.total_gasto + valor > st.session_state.budget:
                st.warning("Essa compra excede o orçamento! Tente um valor menor.")
            else:
                compras.loc[compras["Dia"] == selected_day, "Valor"] += valor
                st.session_state.total_gasto += valor
                save_data(compras)
                st.success(f"Compra de {valor:.2f}€ adicionada ao dia {selected_day}.")

    if st.session_state.total_gasto >= st.session_state.budget:
        st.warning("Você atingiu ou ultrapassou o limite do orçamento!")
