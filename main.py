import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

if orcamento > 0:
    # Criar gráfico donut
    fig, ax = plt.subplots(figsize=(8, 8))
    if not dados.empty:
        produtos = dados["produto"].tolist()
        valores = dados["preco"].tolist()
        restante = orcamento - total
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)
        
        plt.pie(valores, labels=produtos, autopct='%1.1f%%', pctdistance=0.85)
        plt.title(f"Orçamento: {orcamento}€")
        # Criar buraco no meio para efeito donut
        centro = plt.Circle((0,0), 0.70, fc='white')
        ax.add_artist(centro)
        st.pyplot(fig)
    
    st.dataframe(dados)
    st.write(f"Total gasto: {total}€")
    st.write(f"Resta: {orcamento - total}€")
