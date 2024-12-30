import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar ou criar CSV
try:
    dados = pd.read_csv("compras.csv")
except:
    dados = pd.DataFrame(columns=["produto", "preco"])
    dados.to_csv("compras.csv", index=False)

# Título
st.title("Controle de Gastos")

# Input do orçamento
orcamento = st.number_input("Orçamento:", min_value=0.0)

# Adicionar compra
with st.form("nova_compra"):
    produto = st.text_input("Produto:")
    preco = st.number_input("Preço:", min_value=0.0)
    
    if st.form_submit_button("Adicionar"):
        if preco <= (orcamento - dados["preco"].sum()):
            nova_compra = pd.DataFrame({"produto": [produto], "preco": [preco]})
            dados = pd.concat([dados, nova_compra], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada!")
        else:
            st.error("Sem orçamento suficiente!")

# Mostrar lista de compras
st.write("Lista de Compras:")
st.dataframe(dados)

# Mostrar total
total = dados["preco"].sum()
st.write(f"Total gasto: {total}€")
st.write(f"Resta: {orcamento - total}€")

# Gráfico simples
st.write("Gráfico de gastos:")
plt.figure(figsize=(10, 5))
plt.bar(dados["produto"], dados["preco"])
plt.xticks(rotation=45)
plt.xlabel("Produtos")
plt.ylabel("Preço (€)")
st.pyplot(plt)
