import streamlit as st

# Configurar o modo wide
st.set_page_config(layout="wide")

# Títulos da aplicação
st.title("Visualização de Mapas Interativos")
st.subheader("Distribuição de Gestores de Assistência Social")

# Opções de mapas
map_options = {
    "Distribuição de Homens": "mapa_dist_homens_ass_soc.html",
    "Distribuição de Mulheres": "mapa_pydeck_feminino.html",
    "Mapa Sobreposto": "mapa_pydeck_sobreposto.html"
}

# Criar um seletor para escolha do mapa
map_choice = st.selectbox("Selecione o mapa para visualizar:", list(map_options.keys()))

# Exibir o título do mapa escolhido
st.markdown(f"## {map_choice}")

# Exibir o mapa correspondente
map_path = map_options[map_choice]

# Renderiza o mapa no Streamlit com altura maior
with open(map_path, "r", encoding="utf-8") as f:
    html_content = f.read()

st.components.v1.html(html_content, height=900)  # Altura aumentada para 900 pixels
