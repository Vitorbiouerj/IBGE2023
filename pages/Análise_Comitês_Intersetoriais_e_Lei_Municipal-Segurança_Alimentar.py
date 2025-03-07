import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Análise da Concessão do Auxílio às Famílias",
    layout="wide"
)

# Título do aplicativo
st.title("Análise da Relação entre a Existência de Comitês Intersetoriais de Assistência Social e a Presença de uma Lei Municipal de Segurança Alimentar")

# Nome do arquivo Markdown
arquivo_md = "markdown/analise_comites_seguranca_alimentar.md"

# Ler o conteúdo do arquivo Markdown
try:
    with open(arquivo_md, "r", encoding="utf-8") as file:
        conteudo_md = file.read()

    # Exibir o conteúdo no Streamlit usando Markdown
    st.markdown(conteudo_md, unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"O arquivo '{arquivo_md}' não foi encontrado. Verifique o nome do arquivo e sua localização.")
except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")
