import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Criar ou carregar CSV
try:
    dados = pd.read_csv("compras.csv")
except:
    dados = pd.DataFrame({"produto": [], "preco": []})
    dados.to_csv("compras.csv", index=False)

st.title("Controle de Gastos")

orcamento = st.number_input("Orçamento:", min_value=0.0)
total = dados["preco"].sum() if not dados.empty else 0

with st.form("nova_compra"):
    produto = st.text_input("Produto:")
    preco = st.number_input("Preço:", min_value=0.0)
    
    if st.form_submit_button("Adicionar"):
        if preco <= (orcamento - total):
            nova_linha = pd.DataFrame({"produto": [produto], "preco": [preco]})
            dados = pd.concat([dados, nova_linha])
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada!")
        else:
            st.error("Sem orçamento suficiente!")

if not dados.empty:
    st.write("Lista de Compras:")
    st.dataframe(dados)
    st.write(f"Total gasto: {total}€")
    st.write(f"Resta: {orcamento - total}€")

    plt.figure(figsize=(10, 5))
    plt.bar(dados["produto"], dados["preco"])
    plt.xticks(rotation=45)
    plt.xlabel("Produtos")
    plt.ylabel("Preço (€)")
    st.pyplot(plt)
