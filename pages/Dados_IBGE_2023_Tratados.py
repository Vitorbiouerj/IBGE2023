import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Configuração do título da aplicação
st.title("Visualizador de Arquivos CSV")

# Lista de arquivos disponíveis
csv_files = {
    "Assistência Social": "csv/assistencia_social_limpo.csv",
    "Primeira Infância": "csv/primeira_infancias_limpo.csv",
    "Segurança Alimentar": "csv/seguranca_alimentar_limpo.csv"
}

# Seleção de arquivo pelo usuário
selected_file = st.selectbox("Selecione um arquivo para visualizar:", list(csv_files.keys()))

# Carregando e exibindo os dados do CSV selecionado
if selected_file:
    file_path = csv_files[selected_file]

    try:
        df = pd.read_csv(file_path)
        st.write(f"**Visualizando:** {selected_file}")
        st.dataframe(df)  # Exibe os dados como uma tabela interativa
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")

