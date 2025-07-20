import streamlit as st
import pandas as pd
import plotly.express as px


# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("Car Sales.xlsx - car_data.csv")
    df.columns = [
        "ID do Carro", "Data", "Nome do Cliente", "Gênero", "Renda Anual", "Nome da Concessionária",
        "Fabricante", "Modelo", "Motor", "Transmissão", "Cor", "Preço", "Código da Concessionária",
        "Estilo de Carroceria", "Telefone", "Região da Concessionária"
    ]
    df["Data"] = pd.to_datetime(df["Data"], errors='coerce')
    df.dropna(subset=["Data"], inplace=True)
    return df

# Formatação de moeda
def formatar_moeda(valor):
    return f"US$ {valor:,.2f}"

# Paleta de cores vermelha
red_gradient = ["#FF4B4B", "#FF6B6B", "#FF8C8C", "#FFAFAF", "#FFDADA"]

df = load_data()

st.set_page_config(page_title="Dashboard de Vendas de Carros", layout="wide")
st.title("📊 Dashboard de Vendas de Carros")

# Menu lateral de navegação
menu = st.sidebar.selectbox(
    "Selecione o Insight",
    (
        "Faturamento por Gênero",
        "Modelo Mais Vendido por Região",
        "Top 5 Modelos Mais Vendidos",
        "Tipo de Carroceria Mais Vendido",
        "Vendas por Mês",
        "Top 3 Concessionárias por Faturamento"
    )
)

if menu == "Faturamento por Gênero":
    df_genero = df.groupby("Gênero")["Preço"].sum().reset_index()
    df_genero["Preço"] = df_genero["Preço"].round(2)
    fig = px.bar(
        df_genero,
        x="Gênero",
        y="Preço",
        text=df_genero["Preço"].apply(formatar_moeda),
        color="Preço",
        color_continuous_scale=red_gradient,
        title="Faturamento Total por Gênero"
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Modelo Mais Vendido por Região":
    top_modelos_regiao = (
        df.groupby(["Região da Concessionária", "Modelo"])
        .size()
        .reset_index(name="Total")
    )
    idx = top_modelos_regiao.groupby("Região da Concessionária")["Total"].idxmax()
    top_modelos = top_modelos_regiao.loc[idx]
    fig = px.bar(
        top_modelos,
        x="Região da Concessionária",
        y="Total",
        color="Modelo",
        text="Modelo",
        color_discrete_sequence=red_gradient,
        title="Modelo Mais Vendido por Região"
    )
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Top 5 Modelos Mais Vendidos":
    top_modelos = df["Modelo"].value_counts().nlargest(5).reset_index()
    top_modelos.columns = ["Modelo", "Total Vendido"]
    fig = px.bar(
        top_modelos,
        x="Modelo",
        y="Total Vendido",
        color="Total Vendido",
        text="Total Vendido",
        color_continuous_scale=red_gradient,
        title="Top 5 Modelos Mais Vendidos"
    )
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Tipo de Carroceria Mais Vendido":
    carroceria = df["Estilo de Carroceria"].value_counts().reset_index()
    carroceria.columns = ["Estilo de Carroceria", "Total"]
    fig = px.bar(
        carroceria,
        x="Estilo de Carroceria",
        y="Total",
        color="Total",
        text="Total",
        color_continuous_scale=red_gradient,
        title="Tipo de Carroceria Mais Vendido"
    )
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Vendas por Mês":
    df["Ano-Mês"] = df["Data"].dt.to_period("M").astype(str)
    vendas_mensais = df.groupby("Ano-Mês").size().reset_index(name="Vendas")
    fig = px.line(
        vendas_mensais,
        x="Ano-Mês",
        y="Vendas",
        markers=True,
        title="Vendas de Carros por Mês"
    )
    fig.update_traces(line_color="crimson")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Top 3 Concessionárias por Faturamento":
    dealer = df.groupby("Nome da Concessionária")["Preço"].agg(["count", "sum"]).reset_index()
    dealer.columns = ["Concessionária", "Total Vendido", "Faturamento"]
    top_dealers = dealer.sort_values(by="Faturamento", ascending=False).head(3)
    top_dealers["Faturamento"] = top_dealers["Faturamento"].apply(formatar_moeda)
    st.dataframe(top_dealers, use_container_width=True)
