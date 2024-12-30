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

st.session_state.budget = st.number_input("Defina seu orçamento total:", min_value=0.0, step=0.01, value=st.session_state.budget)

# Adicionar valor de compras por dia
selected_day = st.selectbox("Selecione o dia:", compras["Dia"])
valor = st.number_input("Insira o valor da compra:", min_value=0.0, step=0.01)

if st.button("Adicionar Compra"):
    compras.loc[compras["Dia"] == selected_day, "Valor"] += valor
    save_data(compras)
    st.success(f"Compra de {valor:.2f}€ adicionada ao dia {selected_day}.")

# Exibir tabela de compras
st.subheader("Tabela de Compras")
st.dataframe(compras)

# Mostrar orçamento e total gasto
st.subheader("Resumo")
st.write(f"Orçamento Total: {st.session_state.budget:.2f}€")
st.write(f"Total Gasto: {compras['Valor'].sum():.2f}€")

if compras["Valor"].sum() >= st.session_state.budget:
    st.warning("Você atingiu ou ultrapassou o limite do orçamento!")

# Criar gráfico de calor com valores de compras
st.subheader("Gráfico de Calor das Compras")
fig, ax = plt.subplots(figsize=(10, 1))
heatmap_data = np.array(compras["Valor"]).reshape((1, 30))
cax = ax.matshow(heatmap_data, cmap="coolwarm")
fig.colorbar(cax, orientation="horizontal")
ax.set_xticks(range(30))
ax.set_xticklabels(range(1, 31))
ax.set_yticks([])
ax.set_title("Gastos Diários")
st.pyplot(fig)
