import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar ou criar arquivo de compras
try:
    compras = pd.read_csv("compras.csv")
except:
    # Se arquivo não existir, criar novo
    compras = pd.DataFrame({"Dia": range(1, 31), "Valor": [0] * 30})
    compras.to_csv("compras.csv", index=False)

# Título do app
st.title("App de Controle de Gastos")

# Input do orçamento
orcamento = st.number_input("Qual seu orçamento?", value=0.0)

# Selecionar dia e valor
dia = st.selectbox("Escolha o dia:", compras["Dia"])
valor = st.number_input("Valor da compra:", value=0.0)

# Botão para adicionar compra
if st.button("Adicionar"):
    # Achar o dia na tabela e somar o valor
    compras.loc[compras["Dia"] == dia, "Valor"] += valor
    # Salvar no arquivo
    compras.to_csv("compras.csv", index=False)
    st.write("Compra adicionada!")

# Mostrar tabela
st.write("Suas compras:")
st.dataframe(compras)

# Calcular total
total = compras["Valor"].sum()
st.write(f"Total gasto: {total:.2f}€")
st.write(f"Orçamento: {orcamento:.2f}€")

# Avisar se passou do orçamento
if total > orcamento:
    st.write("Você gastou mais que o orçamento!")

# Fazer gráfico simples
st.write("Gráfico de gastos:")
plt.figure(figsize=(10, 5))
plt.bar(compras["Dia"], compras["Valor"])
plt.xlabel("Dia")
plt.ylabel("Valor (€)")
st.pyplot(plt)
