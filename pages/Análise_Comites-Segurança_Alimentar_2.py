

import streamlit as st

# Definir o caminho do arquivo Markdown
markdown_file = "markdown/analise_comites_seg_alimentar_2.md"

# Configurar o título da aplicação
st.set_page_config(page_title="Análise da Relação entre a Existência de Comitês Intersetoriais de Assistência Social e a Presença de um Plano Municipal de Segurança Alimentar", layout="wide")

# Carregar e exibir o conteúdo do arquivo Markdown
try:
    with open(markdown_file, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    st.markdown(markdown_content, unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"O arquivo '{markdown_file}' não foi encontrado. Verifique o caminho e tente novamente.")