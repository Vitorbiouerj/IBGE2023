#====

import streamlit as st

# Definir o caminho do arquivo Markdown
markdown_file = "markdown/Análise_Auxilio-Seguranca_Alimentar.md"

# Configurar o título da aplicação
st.set_page_config(page_title="Análise Auxílio e Segurança Alimentar", layout="wide")

# Carregar e exibir o conteúdo do arquivo Markdown
try:
    with open(markdown_file, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    st.markdown(markdown_content, unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"O arquivo '{markdown_file}' não foi encontrado. Verifique o caminho e tente novamente.")

#====

