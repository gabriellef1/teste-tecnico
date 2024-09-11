import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Função para carregar os dados
@st.cache_data
def load_data():
    data = pd.read_csv("./data/Brasileirao_Matches_Expanded.csv")
    
    # Verificar se a coluna 'winner' já existe e criar caso não exista
    if 'winner' not in data.columns:
        # Criar a coluna 'winner' com base nos gols
        data['winner'] = data.apply(
            lambda row: 'Casa' if row['home_goal'] > row['away_goal'] else 
                        ('Visitante' if row['away_goal'] > row['home_goal'] else 'Empate'),
            axis=1
        )
    return data

# Função para exibir o cabeçalho dos dados
def show_data_info(data):
    st.write("Primeiras 5 linhas do dataset:")
    st.write(data.head())

    st.write("Estatísticas descritivas:")
    st.write(data.describe())

    st.write("Informações gerais dos dados:")
    st.write(data.info())

# Função para exibir distribuições de colunas numéricas
def plot_distribution(data, column):
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=True, color="blue")
    plt.title(f'Distribuição de {column}', fontsize=14)
    st.pyplot(plt)

# Função para exibir a correlação entre as variáveis numéricas
def show_correlation_heatmap(data):
    # Selecionar apenas colunas numéricas
    numeric_data = data.select_dtypes(include=[float, int])
    
    # Calcular a correlação
    corr = numeric_data.corr()
    
    # Plotar o mapa de calor
    plt.figure(figsize=(12, 6))
    sns.heatmap(corr, annot=True, cmap="Blues", fmt=".2f")
    plt.title('Mapa de Correlação', fontsize=14)
    st.pyplot(plt)

# Função para contagem de valores categóricos
def plot_categorical_counts(data, column):
    plt.figure(figsize=(10, 6))
    sns.countplot(x=column, data=data, palette="Set2")
    plt.title(f'Contagem de {column}', fontsize=14)
    st.pyplot(plt)

# Carregar os dados
data = load_data()

# Título do App
st.title("Análise Exploratória de Dados - Brasileirão")

# Exibir informações gerais dos dados
show_data_info(data)

# Menu lateral para selecionar a análise a ser exibida
st.sidebar.title("Opções de Análise")
option = st.sidebar.selectbox("Escolha uma análise", ["Distribuição de Gols", "Mapa de Correlação", "Contagem de Resultados"])

if option == "Distribuição de Gols":
    st.header("Distribuição de Gols")
    st.write("Aqui, podemos observar como os gols estão distribuídos nas partidas.")
    
    # Selecionar se quer exibir gols da casa ou gols do visitante
    goal_type = st.radio("Escolha o tipo de gols para visualizar", ["Gols da Casa", "Gols do Visitante"])
    
    if goal_type == "Gols da Casa":
        plot_distribution(data, "home_goal")
    else:
        plot_distribution(data, "away_goal")

elif option == "Mapa de Correlação":
    st.header("Mapa de Correlação")
    st.write("Esse gráfico mostra a correlação entre as variáveis numéricas.")
    show_correlation_heatmap(data)

elif option == "Contagem de Resultados":
    st.header("Contagem de Resultados")
    st.write("Aqui, podemos observar a contagem de vitórias, derrotas e empates.")
    plot_categorical_counts(data, "winner")

    import io

# Função para exibir o cabeçalho dos dados
def show_data_info(data):
    st.write("Primeiras 5 linhas do dataset:")
    st.write(data.head())

    st.write("Estatísticas descritivas:")
    st.write(data.describe())

    st.write("Informações gerais dos dados:")
    
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()
    
    st.text(s)

