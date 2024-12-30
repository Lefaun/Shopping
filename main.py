import streamlit as st
import pandas as pd
import os

# Nome do arquivo CSV onde os dados serão armazenados
CSV_FILE = "compras.csv"

# Função para inicializar ou carregar o CSV
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # Criar um DataFrame vazio com estrutura esperada
        df = pd.DataFrame({"Artigo": [], "Preço": [], "Total Acumulado": []})
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
    st.session_state.total = 0.0

st.session_state.budget = st.number_input("Defina seu orçamento total:", min_value=0.0, step=0.01, value=st.session_state.budget)

# Adicionar itens
with st.form("add_item_form"):
    artigo = st.text_input("Nome do Artigo:")
    preco = st.number_input("Preço do Artigo:", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Adicionar Compra")

    if submitted:
        if artigo and preco > 0:
            st.session_state.total += preco
            new_row = {"Artigo": artigo, "Preço": preco, "Total Acumulado": st.session_state.total}
            compras = pd.concat([compras, pd.DataFrame([new_row])], ignore_index=True)
            save_data(compras)
            st.success(f"Artigo '{artigo}' de {preco:.2f}€ adicionado. Total acumulado: {st.session_state.total:.2f}€.")

        if st.session_state.total >= st.session_state.budget:
            st.warning("Você atingiu ou ultrapassou o limite do orçamento!")

# Exibir tabela de compras
st.subheader("Tabela de Compras")
st.dataframe(compras)

# Mostrar orçamento e total
st.subheader("Resumo")
st.write(f"Orçamento Total: {st.session_state.budget:.2f}€")
st.write(f"Total Gasto: {st.session_state.total:.2f}€")

if st.session_state.total >= st.session_state.budget:
    st.write("Você atingiu o limite do orçamento. Nenhuma compra adicional pode ser feita.")
